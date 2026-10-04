"""Lee TODOS tus repos públicos con la API de GitHub (sin token; en Actions usa GITHUB_TOKEN si existe)."""
import json, os
from pathlib import Path
import requests
from config import USERNAME

ROOT = Path(__file__).resolve().parent.parent
h = {"Accept": "application/vnd.github+json", "User-Agent": "profile-art"}
if os.environ.get("GITHUB_TOKEN"):
    h["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]
repos, page = [], 1
while True:
    r = requests.get(f"https://api.github.com/users/{USERNAME}/repos",
                     params={"per_page": 100, "page": page, "sort": "pushed"}, headers=h, timeout=30)
    r.raise_for_status()
    b = r.json(); repos += b
    if len(b) < 100: break
    page += 1
keys = ("name", "description", "language", "stargazers_count", "forks_count", "pushed_at", "fork", "archived", "html_url", "topics")
(ROOT / "data").mkdir(exist_ok=True)
(ROOT / "data/repos.json").write_text(json.dumps([{k: x.get(k) for k in keys} for x in repos], indent=1, ensure_ascii=False))
print(f"OK: {len(repos)} repos")
