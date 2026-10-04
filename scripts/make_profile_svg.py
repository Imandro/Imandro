"""Compone TODO el perfil en un unico panel de terminal -> profile.svg

Convencion: las secciones de render_parts devuelven la coordenada Y final
(absoluta), no un alto. Aqui se convierte con (fin - inicio).
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


def bloque(fn, *args):
    """Ejecuta una seccion y avanza y hasta donde termino."""
    global y, t
    ini = y
    r = fn(*args, y, t)
    body.extend(r[0])
    y = r[2]
    t = r[3]
    return y - ini


b, d, w, h, t = P.ascii_name(y, t)      # nombre en ASCII -> devuelve alto real
body += b
defs += d
y += h + 12

b, _, t = P.slogan(y, t)                # eslogan (omite $ whoami repetido)
body += b
y += 28

bloque(P.whoami)                        # $ whoami
y += 28

bloque(P.about)                         # $ cat about.md
y += 20

body.append(f'<line x1="{X}" y1="{y}" x2="{W - X}" y2="{y}" stroke="#21262d" stroke-width="1"/>')
y += 22

# retrato ASCII
pb, pw, ph = P.portrait()
if pb:
    body.append(f'<g transform="translate({X},{y})">{"".join(pb)}</g>')
    y += ph + 18

# premios
ab, ad, aw, ah, t = P.awards(y, t)      # devuelve y absoluta
defs += ad
body.append(f'<g transform="translate({X},{y})">{"".join(ab)}</g>')
y = ah + 18

if P.heatmap(t)[0]:                     # $ ./contributions.sh
    body += P.label("./contributions.sh", y, t)
    t += 0.12
    y += 22
    hb, hw, hh, t = P.heatmap(t)
    body.append(f'<g transform="translate({X},{y})">{"".join(hb)}</g>')
    y += hh + 24

bloque(P.tech)                          # $ cat stack.yml
y += 12

bloque(P.projects)                      # $ ls projects/

body.append(f'<text x="{X}" y="{y + 6}"><tspan class="p">$ </tspan><tspan class="g cur">█</tspan></text>')

H = y + 30
if defs:
    body.insert(0, "<defs>" + "".join(defs) + "</defs>")
(ROOT / "profile.svg").write_text("\n".join(open_svg(W, H, f"{HANDLE}@github: ~", EXTRA) + body + ["</svg>"]))
print(f"OK: profile.svg ({W}x{H})")