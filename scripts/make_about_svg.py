import textwrap
from html import escape
from pathlib import Path
from config import ABOUT, HANDLE
from svgkit import open_svg

ROOT = Path(__file__).resolve().parent.parent
W, X, LH = 860, 26, 21
body = [f'<text x="{X}" y="48"><tspan class="p">$</tspan> cat about.md</text>']
y, t = 78, 0.3
for i, para in enumerate(ABOUT):
    for line in textwrap.wrap(para, 100):
        cls = "w" if i == 0 else ""
        body.append(f'<text class="l {cls}" style="animation-delay:{t:.2f}s" x="{X}" y="{y}">{escape(line)}</text>')
        y += LH; t += 0.12
    y += 12
body.append(f'<text x="{X}" y="{y+4}"><tspan class="p">$</tspan> <tspan class="g cur">█</tspan></text>')
H = y + 28
(ROOT / "about.svg").write_text("\n".join(open_svg(W, H, f"{HANDLE}@github: ~/about") + body + ["</svg>"]))
print("OK: about.svg")
