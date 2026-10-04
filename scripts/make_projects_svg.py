"""projects.svg: destacados con detalle + el resto de repos (data/repos.json) + barra de lenguajes."""
import json, textwrap
from collections import Counter
from html import escape
from pathlib import Path
from config import HANDLE, FEATURED, OTHER_MAX, USERNAME
from svgkit import open_svg, chip, LANG_COLORS

ROOT = Path(__file__).resolve().parent.parent
W, X = 860, 26
repos = []
f = ROOT / "data/repos.json"
if f.exists():
    repos = json.loads(f.read_text())
body = [f'<text x="{X}" y="48"><tspan class="p">$</tspan> ls -l projects/</text>']
y, t = 74, 0.2
for p in FEATURED:
    body.append(f'<text class="l g b" style="animation-delay:{t:.2f}s;font-size:14px" x="{X}" y="{y}">▸ {escape(p["name"])}'
                f'<tspan class="t" dx="10" style="font-weight:normal">{escape(p["tag"])}</tspan></text>'); y += 21; t += 0.2
    for line in textwrap.wrap(p["desc"], 92) if p["desc"] else []:
        body.append(f'<text class="l" style="animation-delay:{t:.2f}s" x="{X+16}" y="{y}">{escape(line)}</text>'); y += 19; t += 0.08
    for pt in p["points"]:
        body.append(f'<text class="l t" style="animation-delay:{t:.2f}s;font-size:12.5px" x="{X+16}" y="{y}"><tspan class="g">•</tspan> {escape(pt)}</text>'); y += 19; t += 0.08
    x = X + 16; y += 4
    for s in p["stack"]:
        c, w = chip(x, y, s, "#1f6feb", t); body.append(c); x += w + 8; t += 0.04
    y += 44
names = {p["name"].lower() for p in FEATURED} | {USERNAME.lower()}
others = [r for r in repos if not r["fork"] and r["name"].lower() not in names][:OTHER_MAX]
if others:
    body.append(f'<text class="l t" style="animation-delay:{t:.2f}s" x="{X}" y="{y}">── más repositorios ({len(repos)} en total) ──</text>'); y += 24; t += 0.1
    for r in others:
        d = (r["description"] or "").strip()
        d = (d[:78] + "…") if len(d) > 79 else d
        lang = r["language"] or ""
        body.append(f'<text class="l" style="animation-delay:{t:.2f}s" x="{X+8}" y="{y}"><tspan class="g">▸</tspan> '
                    f'<tspan class="w b">{escape(r["name"])}</tspan><tspan class="t" dx="8">{escape(d)}</tspan>'
                    f'<tspan class="p" dx="8">{escape(lang)}</tspan></text>'); y += 20; t += 0.06
    y += 10
cnt = Counter(r["language"] for r in repos if r["language"] and not r["fork"])
if cnt:
    tot = sum(cnt.values()); x = X; bw = W - 2 * X
    body.append(f'<text class="l t" style="animation-delay:{t:.2f}s" x="{X}" y="{y}">lenguajes en mis repos</text>'); y += 12
    body.append(f'<clipPath id="lb"><rect x="{X}" y="{y}" width="{bw}" height="10" rx="5"/></clipPath><g clip-path="url(#lb)">')
    for lang, n in cnt.most_common():
        w = bw * n / tot
        body.append(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="10" fill="{LANG_COLORS.get(lang, "#8b949e")}"/>'); x += w
    body.append('</g>'); y += 30; x = X
    for lang, n in cnt.most_common(7):
        col = LANG_COLORS.get(lang, "#8b949e"); label = f"{lang} {round(100*n/tot)}%"
        body.append(f'<circle cx="{x+5}" cy="{y-4}" r="5" fill="{col}"/><text class="t" x="{x+15}" y="{y}">{escape(label)}</text>')
        x += 15 + len(label) * 7.2 + 18
    y += 14
H = y + 10
o = open_svg(W, H, f"{HANDLE}@github: ~/projects") + body + ["</svg>"]
(ROOT / "projects.svg").write_text("\n".join(o)); print("OK: projects.svg")
