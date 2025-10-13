import feedparser
import git
import os
import re
import logging
from html import unescape

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# 설정
rss_url = 'https://api.velog.io/rss/@limseohyeon'
repo_path = '.'
posts_dir = os.path.join(repo_path, 'velog-posts')

# 폴더 생성
os.makedirs(posts_dir, exist_ok=True)

# 레포지토리 로드 (예외 처리)
try:
    repo = git.Repo(repo_path)
except Exception as e:
    logging.error(f"Git repo load failed: {e}")
    raise

def sanitize_filename(title: str, max_len: int = 100) -> str:
    """파일명으로 안전하게 변환. 공백->대시, 특수문자 제거, 길이 제한."""
    name = unescape(title)
    name = name.strip()
    # 공백을 대시로
    name = re.sub(r'\s+', '-', name)
    # 파일명에 쓸 수 없는 문자 제거
    name = re.sub(r'[\/\\\:\*\?"<>\|\u0000-\u001f]', '', name)
    # 연속된 대시 정리
    name = re.sub(r'-{2,}', '-', name)
    # 길이 제한
    if len(name) > max_len:
        name = name[:max_len].rstrip('-')
    if not name:
        name = 'post'
    return name + '.md'

def extract_entry_content(entry) -> str:
    """
    feedparser entry에서 가능한 필드를 순서대로 검사하여 본문을 반환.
    반환값은 문자열(빈 문자열 가능).
    """
    # 1) entry.get('content') : 리스트 형태인 경우가 많음
    content = entry.get('content')
    if content:
        try:
            first = content[0]
            # feedparser의 content 아이템은 dict-like일 수 있음
            value = first.get('value') if isinstance(first, dict) else getattr(first, 'value', None)
            if value:
                return value
        except Exception:
            pass

    # 2) description
    desc = entry.get('description') or getattr(entry, 'description', None)
    if desc:
        return desc

    # 3) summary
    summary = entry.get('summary') or getattr(entry, 'summary', None)
    if summary:
        return summary

    # 4) summary_detail.value
    summary_detail = entry.get('summary_detail') or getattr(entry, 'summary_detail', None)
    try:
        if summary_detail:
            val = summary_detail.get('value') if isinstance(summary_detail, dict) else getattr(summary_detail, 'value', None)
            if val:
                return val
    except Exception:
        pass

    # 5) 기타 대안: content[0]['value'] 이미 체크했으니 없으면 빈 문자열 반환
    return ''

def unique_path(path_base):
    """같은 이름 파일이 있으면 인덱스 붙여서 유니크 경로 반환."""
    if not os.path.exists(path_base):
        return path_base
    base, ext = os.path.splitext(path_base)
    i = 1
    while True:
        candidate = f"{base}-{i}{ext}"
        if not os.path.exists(candidate):
            return candidate
        i += 1

# 피드 파싱
feed = feedparser.parse(rss_url)
if feed.bozo:
    logging.warning(f"Feed parser encountered an issue (bozo=True): {getattr(feed, 'bozo_exception', 'unknown')}")

created_files = []

for entry in feed.entries:
    try:
        title = getattr(entry, 'title', None) or entry.get('title') or 'untitled'
        logging.info(f"Processing entry: {title}")

        # 파일명 안전화
        file_name = sanitize_filename(title)
        file_path = os.path.join(posts_dir, file_name)
        file_path = unique_path(file_path)

        if os.path.exists(file_path):
            logging.info(f"File already exists, skipping: {file_path}")
            continue

        # 본문 추출 (안전하게)
        content = extract_entry_content(entry)
        if not content:
            logging.warning(f"No content found for entry: {title} — skipping file creation.")
            continue

        # 파일에 작성
        with open(file_path, 'w', encoding='utf-8') as f:
            # 필요하면 HTML->텍스트 변환 추가 가능, 현재는 원문 그대로 저장
            f.write(content)

        logging.info(f"Created file: {file_path}")
        created_files.append(file_path)

        # Git 커밋(파일 단위)
        try:
            repo.git.add(file_path)
            commit_msg = f"Add post: {title}"
            repo.git.commit('-m', commit_msg)
            logging.info(f"Committed: {file_path}")
        except Exception as e:
            logging.error(f"Git add/commit failed for {file_path}: {e}")
            # 커밋 실패해도 다음 항목 처리하도록 계속

    except Exception as e:
        logging.error(f"Error processing entry '{getattr(entry, 'title', 'no-title')}': {e}")
        # 개별 entry 에러는 무시하고 계속

# 한 번에 푸시 (created_files가 비어있지 않을 때)
if created_files:
    try:
        origin = repo.remote(name='origin')
        origin.push()
        logging.info("Pushed changes to remote.")
    except Exception as e:
        logging.error(f"Git push failed: {e}")
else:
    logging.info("No new files created. Nothing to push.")
