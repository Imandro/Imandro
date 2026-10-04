from pathlib import Path
from config import TECH, HANDLE
from svgkit import open_svg, chip

ROOT = Path(__file__).resolve().parent.parent
COLORS = ["#3572A5", "#61dafb", "#336790", "#f1e05a", "#39d353"]
W, X0, MAXX, LX = 860, 200, 835, 26
body = []; y = 60; d = 0.2
body.append(f'<text x="{LX}" y="48"><tspan class="p">$</tspan> cat stack.yml</text>')
y = 64
for ci, (cat, items) in enumerate(TECH.items()):
    col = COLORS[ci % len(COLORS)]
    body.append(f'<text class="l g b" style="animation-delay:{d:.2f}s" x="{LX}" y="{y+17}">{cat}:</text>')
    x = X0
    for it in items:
        s, w = chip(0, 0, it, col, d)
        if x + w > MAXX:
            x = X0; y += 32
        s, w = chip(x, y, it, col, d)
        body.append(s); x += w + 8; d += 0.05
    y += 40
H = y + 6
o = open_svg(W, H, f"{HANDLE}@github: ~/stack") + body + ["</svg>"]
(ROOT / "tech.svg").write_text("\n".join(o)); print("OK: tech.svg")
