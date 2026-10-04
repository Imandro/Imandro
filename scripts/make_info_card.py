import os
from pathlib import Path
from html import escape
from config import HANDLE, INFO

ROOT = Path(__file__).resolve().parent.parent
static = os.environ.get("STATIC") == "1"
W, LH = 490, 26
H = 70 + len(INFO) * LH + 20
anim = "" if static else ("opacity:0;animation:in .45s ease-out forwards;")
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
 '<style>text{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:13px;fill:#c9d1d9}'
 '.k{fill:#58a6ff;font-weight:bold}.t{fill:#8b949e;font-size:12px}'
 '.l{%s}@keyframes in{from{opacity:0;transform:translateX(-10px)}to{opacity:1;transform:none}}</style>' % anim,
 f'<rect width="{W}" height="{H}" rx="10" fill="#0d1117" stroke="#30363d"/>',
 '<circle cx="20" cy="18" r="5" fill="#ff5f56"/><circle cx="38" cy="18" r="5" fill="#ffbd2e"/>'
 '<circle cx="56" cy="18" r="5" fill="#27c93f"/>',
 f'<text class="t" x="76" y="22">{escape(HANDLE)}@github: ~</text>',
 f'<text class="l" style="animation-delay:.2s" x="20" y="56"><tspan class="k">{escape(HANDLE)}</tspan>'
 f'<tspan>@github</tspan></text>']
for i, (k, v) in enumerate(INFO):
    y = 56 + (i + 1) * LH
    o.append(f'<text class="l" style="animation-delay:{0.4+i*0.25:.2f}s" x="20" y="{y}">'
             f'<tspan class="k">{escape(k)}:</tspan><tspan dx="8">{escape(v)}</tspan></text>')
o.append("</svg>")
(ROOT / "info-card.svg").write_text("\n".join(o))
print("OK: info-card.svg")
