"""Compone el perfil en un unico panel de terminal -> profile.svg

Orden: identidad (nombre + retrato + tarjeta), historia (about) y actividad
(contribuciones). Los proyectos y el stack viven en el README como enlaces
reales: dentro de un <img> nadie puede hacer clic.
"""
from pathlib import Path

from config import HANDLE
from svgkit import open_svg
import render_parts as P

ROOT = Path(__file__).resolve().parent.parent
W, X = 960, 30

EXTRA = ('.k{fill:#58a6ff}'
         '.hm{font-size:11px;fill:#8b949e}'
         '.pa{font-size:5.7px;fill:#c9d1d9;white-space:pre}'
         '.c{opacity:0;animation:in .5s ease-out forwards}')

body, defs = [], []
y, t = 58, 0.15

# nombre en ASCII + eslogan
b, d, y, t = P.ascii_name(y, t)
body += b
defs += d
y += 10

b, y, t = P.slogan(y, t)
body += b
y += 34

# retrato + tarjeta neofetch
b, d, y, t = P.hero(y, t)
body += b
defs += d
y += 26

body.append(f'<line x1="{X}" y1="{y}" x2="{W - X}" y2="{y}" stroke="#21262d" stroke-width="1"/>')
y += 24

# historia
b, y, t = P.about(y, t)
body += b
y += 30

# actividad real (se refresca a diario con GitHub Actions)
b, y, t = P.heatmap(y, t)
body += b
y += 18

body.append(f'<text x="{X}" y="{y + 6}"><tspan class="p">$ </tspan><tspan class="g cur">█</tspan></text>')

H = y + 30
if defs:
    body.insert(0, "<defs>" + "".join(defs) + "</defs>")
(ROOT / "profile.svg").write_text(
    "\n".join(open_svg(W, H, f"{HANDLE}@github: ~", EXTRA) + body + ["</svg>"]),
    encoding="utf-8")
print(f"OK: profile.svg ({W}x{H:.0f})")
