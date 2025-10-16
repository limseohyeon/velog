import feedparser
import git
import os
import re
import logging
import json
import hashlib
from html import unescape

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# 설정
rss_url = 'https://api.velog.io/rss/@limseohyeon'
repo_path = '.'
posts_dir = os.path.join(repo_path, 'velog-posts')
index_path = os.path.join(posts_dir, '.index.json')  # 인덱스 파일

# 폴더 생성
os.makedirs(posts_dir, exist_ok=True)

# 레포지토리 로드 (예외 처리)
try:
    repo = git.Repo(repo_path)
except Exception as e:
    logging.error(f"Git repo load failed: {e}")
    raise

def sanitize_filename(title: str, max_len: int = 100) -> str:
    name = unescape(title)
    name = name.strip()
    name = re.sub(r'\s+', '-', name)
    name = re.sub(r'[\/\\\:\*\?"<>\|\u0000-\u001f]', '', name)
    name = re.sub(r'-{2,}', '-', name)
    if len(name) > max_len:
        name = name[:max_len].rstrip('-')
    if not name:
        name = 'post'
    return name + '.md'

def extract_entry_content(entry) -> str:
    content = entry.get('content')
    if content:
        try:
            first = content[0]
            value = first.get('value') if isinstance(first, dict) else getattr(first, 'value', None)
            if value:
                return value
        except Exception:
            pass
    desc = entry.get('description') or getattr(entry, 'description', None)
    if desc:
        return desc
    summary = entry.get('summary') or getattr(entry, 'summary', None)
    if summary:
        return summary
    summary_detail = entry.get('summary_detail') or getattr(entry, 'summary_detail', None)
    try:
        if summary_detail:
            val = summary_detail.get('value') if isinstance(summary_detail, dict) else getattr(summary_detail, 'value', None)
            if val:
                return val
    except Exception:
        pass
    return ''

def compute_hash(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def get_entry_id(entry) -> str:
    """
    가능한 고유 아이디를 반환.
    우선순위: entry.id -> entry.link -> title+published -> content-hash (fallback)
    """
    eid = entry.get('id') or getattr(entry, 'id', None)
    if eid:
        return str(eid)
    link = entry.get('link') or getattr(entry, 'link', None)
    if link:
        return str(link)
    title = getattr(entry, 'title', '') or entry.get('title', '')
    pub = entry.get('published') or getattr(entry, 'published', None) or ''
    if title or pub:
        return f"title:{title}|published:{pub}"
    # 최종 fallback: content hash
    content = extract_entry_content(entry) or ''
    return f"hash:{compute_hash(content)}"

def load_index() -> dict:
    """인덱스 파일(.index.json) 또는 posts_dir 내 파일들을 스캔해 인덱스 복원."""
    index = {}
    # 1) 인덱스 파일 읽기
    if os.path.exists(index_path):
        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                index = json.load(f)
                logging.info(f"Loaded index from {index_path} ({len(index)} entries).")
        except Exception as e:
            logging.warning(f"Failed to load index file: {e}. Will rebuild from files.")
            index = {}

    # 2) 인덱스에 누락된 파일들은 posts_dir에서 찾아서 보완
    # 파일 상단에 ENTRY_ID 주석 형식: <!-- ENTRY_ID: ... -->
    for fname in os.listdir(posts_dir):
        if not fname.lower().endswith('.md'):
            continue
        full = os.path.join(posts_dir, fname)
        # 이미 인덱스에 있으면 건너뜀
        if any(v == fname for v in index.values()):
            continue
        try:
            with open(full, 'r', encoding='utf-8') as f:
                first_chunk = f.read(1024)  # 상단 일부만 읽음
                m = re.search(r'ENTRY_ID:\s*(.+)', first_chunk)
                if m:
                    eid = m.group(1).strip()
                    index[eid] = fname
                    logging.info(f"Recovered index entry from file {fname}: {eid}")
                else:
                    # 만약 ENTRY_ID 주석이 없다면, 파일 본문 해시로 추정 키 생성해서 인덱스에 보관
                    f.seek(0)
                    body = f.read()
                    h = compute_hash(body)
                    key = f"filehash:{h}"
                    index[key] = fname
                    logging.info(f"No ENTRY_ID in {fname}. Added filehash-based index key.")
        except Exception as e:
            logging.warning(f"Could not read {full} to recover index: {e}")
    return index

def save_index(index: dict):
    try:
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(index, f, ensure_ascii=False, indent=2)
        logging.info(f"Index saved to {index_path} ({len(index)} entries).")
        # git add index file too
        try:
            repo.git.add(index_path)
            repo.git.commit('-m', 'Update .index.json')
        except Exception:
            # 인덱스 커밋 실패는 무시(주 프로세스 커밋에서 같이 커밋될 수 있음)
            pass
    except Exception as e:
        logging.error(f"Failed to save index: {e}")

def unique_path(path_base):
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

# 인덱스 로드 / 복원
index = load_index()

created_files = []

for entry in feed.entries:
    try:
        title = getattr(entry, 'title', None) or entry.get('title') or 'untitled'
        logging.info(f"Processing entry: {title}")

        # 항목 고유 아이디 결정
        entry_id = get_entry_id(entry)

        # 이미 인덱스에 존재하면 스킵
        if entry_id in index:
            logging.info(f"Entry already saved (index match): {entry_id} -> {index[entry_id]}")
            continue

        # 본문 추출
        content = extract_entry_content(entry)
        if not content:
            logging.warning(f"No content found for entry: {title} — skipping file creation.")
            continue

        # 파일명 안전화 및 중복 방지 이름 생성
        file_name = sanitize_filename(title)
        file_path = os.path.join(posts_dir, file_name)
        file_path = unique_path(file_path)
        final_fname = os.path.basename(file_path)

        # 파일에 ENTRY_ID 주석과 함께 작성 (앞부분에 식별자 남김)
        header = f"<!-- ENTRY_ID: {entry_id} -->\n<!-- SOURCE_TITLE: {title} -->\n\n"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(header)
            f.write(content)

        logging.info(f"Created file: {file_path}")
        created_files.append(file_path)

        # 인덱스 갱신
        index[entry_id] = final_fname

        # Git add & commit (파일 단위)
        try:
            repo.git.add(file_path)
            commit_msg = f"Add post: {title}"
            repo.git.commit('-m', commit_msg)
            logging.info(f"Committed: {file_path}")
        except Exception as e:
            logging.error(f"Git add/commit failed for {file_path}: {e}")
            # 계속 진행

    except Exception as e:
        logging.error(f"Error processing entry '{getattr(entry, 'title', 'no-title')}': {e}")

# 인덱스 저장
save_index(index)

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
