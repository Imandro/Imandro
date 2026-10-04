import json, re
from datetime import date, timedelta
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from config import USERNAME

ROOT = Path(__file__).resolve().parent.parent
url = f"https://github.com/users/{USERNAME}/contributions"
html = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30).text
soup = BeautifulSoup(html, "html.parser")

days = []
for td in soup.select("td.ContributionCalendar-day"):
    d = td.get("data-date")
    if not d:
        continue
    count = 0
    tip = soup.find("tool-tip", attrs={"for": td.get("id")}) if td.get("id") else None
    if tip:
        m = re.match(r"(\d+|No)\s+contribution", tip.get_text().strip())
        if m:
            count = 0 if m.group(1) == "No" else int(m.group(1))
    days.append({"date": d, "level": int(td.get("data-level", 0)), "count": count})
days.sort(key=lambda x: x["date"])
if not days:
    raise SystemExit("No se encontraron días. ¿Usuario correcto en config.py?")

total = sum(x["count"] for x in days)
longest = run = 0
for x in days:
    run = run + 1 if x["count"] > 0 else 0
    longest = max(longest, run)
cur, i = 0, len(days) - 1
if days[i]["count"] == 0:
    i -= 1  # hoy aún puede estar en cero
while i >= 0 and days[i]["count"] > 0:
    cur += 1; i -= 1
best = max(days, key=lambda x: x["count"])

(ROOT / "data").mkdir(exist_ok=True)
(ROOT / "data/contributions.json").write_text(json.dumps({
    "total": total, "current_streak": cur, "longest_streak": longest,
    "best_day": best, "days": days}, indent=1))
print(f"OK: {len(days)} días, {total} contribuciones")
