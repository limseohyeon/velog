import os
import re
import git
import json
import unicodedata
import hashlib
import requests
from datetime import datetime

# ===== 설정 =====
GRAPHQL_ENDPOINT = "https://v2.velog.io/graphql"  # Velog GraphQL 엔드포인트
USERNAME = "limseohyeon"                           # Velog 아이디
REPO_PATH = "."
OUT_DIR = os.path.join(REPO_PATH, "velog-posts")

# ===== 유틸 =====
def ensure_dir(p):
    os.makedirs(p, exist_ok=True)

def slugify(text: str) -> str:
    text = unicodedata.normalize('NFKD', text).strip()
    text = re.sub(r'[\\/:*?"<>|]+', '-', text)
    text = re.sub(r'\s+', '-', text)
    text = re.sub(r'-{2,}', '-', text)
    return text.strip('-')

def file_changed(path: str, new_text: str) -> bool:
    if not os.path.exists(path):
        return True
    with open(path, 'r', encoding='utf-8') as f:
        old = f.read()
    return hashlib.sha256(old.encode('utf-8')).hexdigest() != hashlib.sha256(new_text.encode('utf-8')).hexdigest()

def fetch_posts(username: str, limit: int = 200):
    """
    Velog GraphQL: 사용자 글 목록 + 시리즈 정보
    페이징이 필요하면 cursor 기반으로 더 가져오도록 확장 가능.
    """
    query = """
    query($username: String!, $limit: Int!) {
      posts(username: $username, limit: $limit) {
        id
        title
        body
        short_description
        released_at
        updated_at
        url_slug
        tags
        series {
          name
          url_slug
        }
        link
      }
    }
    """
    variables = {"username": username, "limit": limit}
    r = requests.post(GRAPHQL_ENDPOINT, json={"query": query, "variables": variables}, timeout=30)
    r.raise_for_status()
    data = r.json()
    if "errors" in data:
        raise RuntimeError(data["errors"])
    return data["data"]["posts"]

# ===== 메인 =====
ensure_dir(OUT_DIR)
repo = git.Repo(REPO_PATH)

posts = fetch_posts(USERNAME, limit=500)  # 필요시 더 크게/페이징

for p in posts:
    title = p["title"].strip()
    body = p.get("body") or p.get("short_description") or ""
    released_at = p.get("released_at") or p.get("updated_at")
    # released_at이 None일 수도 있으니 안전 처리
    date_iso = (released_at or datetime.utcnow().isoformat())
    date_prefix = date_iso[:10]

    series = (p.get("series") or {}).get("name") or "_no-series"
    series_slug = slugify(series)
    title_slug = slugify(title)

    series_dir = os.path.join(OUT_DIR, series_slug)
    ensure_dir(series_dir)

    filename = f"{date_prefix}_{title_slug}.md"
    path = os.path.join(series_dir, filename)

    link = p.get("link") or f"https://velog.io/@{USERNAME}/{p.get('url_slug','')}"
    tags = p.get("tags") or []

    front_matter = [
        '---',
        f'title: "{title}"',
        f'date: "{date_iso}"',
        f'series: "{series}"',
        f'link: "{link}"',
        f'tags: [{", ".join([f\'"{slugify(str(x))}"\' for x in tags])}]',
        '---',
        ''
    ]
    content = "\n".join(front_matter) + body

    if file_changed(path, content):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        repo.git.add(path)
        repo.git.commit('-m', f'Velog sync: [{series}] {title}')

# push
origin = repo.remote(name='origin')
origin.push()
