"""Secciones reutilizables que make_profile_svg.py compone en un unico panel.

Cada funcion devuelve (body, end_y, t) o (body, defs, end_y, t): los elementos
SVG, la coordenada Y final (absoluta) y el delay de animacion acumulado para
que las secciones encadenen en cascada.
"""
import json
import re
import textwrap
from datetime import date
from html import escape
from pathlib import Path

from config import (HANDLE, BANNER_NAME, BANNER_LINES, INFO, ABOUT,
                    AWARDS_COUNT, AWARDS_LABEL)

ROOT = Path(__file__).resolve().parent.parent
W, X = 960, 30

# Filas de INFO que ya dice otra seccion: la pila y los proyectos viven en el
# README, asi que la tarjeta se queda solo con la identidad.
INFO_SKIP = {"Stack", "Móvil", "Proyectos"}

# Comandos de BANNER_LINES que se renderizan despues como seccion propia.
BANNER_SKIP = {"$ whoami"}

# Emoji y pictogramas: se quitan porque la fuente monoespaciada no los dibuja.
# Los acentos y signos propios del espanol se conservan.
EMOJI = re.compile("[\U0001F000-\U0001FAFF\u2600-\u27BF\uFE0F]")

LETTERS = {  # fuente 5x7
    "I": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"],
    "M": ["#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"],
    "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "N": ["#...#", "##..#", "##..#", "#.#.#", "#..##", "#..##", "#...#"],
    "D": ["####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."],
    "R": ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
    "O": [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
    "E": ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
    "C": [".####", "#....", "#....", "#....", "#....", "#....", ".####"],
    "U": ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "T": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
    "Y": ["#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."],
    "B": ["####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."],
    "P": ["####.", "#...#", "#...#", "####.", "#....", "#....", "#...."],
    "V": ["#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."],
    "L": ["#....", "#....", "#....", "#....", "#....", "#....", "#####"],
}


def label(cmd, y, t, x=X):
    """Linea de prompt `$ comando`."""
    return [f'<text class="l" style="animation-delay:{t:.2f}s" x="{x}" y="{y}">'
            f'<tspan class="p">$</tspan> {escape(cmd)}</text>']


def ascii_name(y, t):
    """Nombre en ASCII con animacion de tecleo."""
    cols = len(BANNER_NAME) * 6 - 1
    grid = [[0] * cols for _ in range(7)]
    for n, ch in enumerate(BANNER_NAME.upper()):
        for ry, row in enumerate(LETTERS[ch]):
            for rx, c in enumerate(row):
                if c == "#":
                    grid[ry][n * 6 + rx] = 1
    CW, FS, LH = 7.4, 12.3, 15
    body, defs = [], []
    for r in range(7):
        s = "".join("##" if grid[r][x] else "  " for x in range(cols))
        defs.append(f'<clipPath id="n{r}"><rect x="{X}" y="{y + r*LH - 14}" width="0" height="{LH + 4}">'
                    f'<animate attributeName="width" from="0" to="{len(s)*CW + 8:.1f}" '
                    f'begin="{t:.2f}s" dur="0.35s" fill="freeze"/></rect></clipPath>')
        body.append(f'<text class="g b" style="font-size:{FS}px" xml:space="preserve" '
                    f'x="{X}" y="{y + r*LH}" clip-path="url(#n{r})">{s}</text>')
        t += 0.12
    return body, defs, y + 7 * LH, t


def slogan(y, t):
    """Lineas de BANNER_LINES cuyo comando no se repita como seccion."""
    body = []
    for cmd, out in BANNER_LINES:
        if cmd in BANNER_SKIP:
            continue
        body.append(f'<text class="l" style="animation-delay:{t:.2f}s" x="{X + 16}" y="{y}">'
                    f'<tspan class="t">&gt; </tspan>{escape(out)}</text>')
        y += 22
        t += 0.15
    return body, y, t


def _portrait(x, y, t):
    """Inserta avi-ascii.svg (se genera aparte: necesita la foto)."""
    f = ROOT / "avi-ascii.svg"
    if not f.exists():
        return "", 0, 0
    s = f.read_text(encoding="utf-8")
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', s)
    if not m:
        return "", 0, 0
    w, h = float(m.group(1)), float(m.group(2))
    d = re.search(r"<defs>(.*?)</defs>", s, re.S)
    r = re.search(r"</defs>(.*)</svg>", s, re.S)
    parts = []
    if d:
        # El retrato anima al cargar; lo desplazamos para que entre en cascada.
        inner = re.sub(r'begin="([\d.]+)s"',
                       lambda mm: f'begin="{float(mm.group(1)) + t:.2f}s"', d.group(1))
        parts.append(f"<defs>{inner}</defs>")
    if r:
        parts.append(r.group(1).replace("<text ", '<text class="pa" '))
    # Difumina el borde inferior del retrato: el recorte se ve intencional.
    parts.append(f'<defs><linearGradient id="pfade" x1="0" y1="0" x2="0" y2="1">'
                 f'<stop offset="0" stop-color="#0d1117" stop-opacity="0"/>'
                 f'<stop offset="1" stop-color="#0d1117"/></linearGradient></defs>'
                 f'<rect x="0" y="{h - 46:.1f}" width="{w:.1f}" height="46" fill="url(#pfade)"/>')
    return f'<g transform="translate({x},{y})">{"".join(parts)}</g>', w, h


def _card(x, y, w, t):
    """Tarjeta neofetch con identidad, logros y foco actual."""
    H = 374
    inner = x + 20
    body = [f'<rect x="{x}" y="{y}" width="{w}" height="{H}" rx="10" '
            f'fill="#0d1117" stroke="#21262d"/>']

    cy = y + 32
    body += label("whoami", cy, t, x=inner)
    cy += 30
    body.append(f'<text class="l w b" style="animation-delay:{t + 0.14:.2f}s;font-size:15px" '
                f'x="{inner}" y="{cy}">{escape(HANDLE)}@github</text>')
    cy += 28
    for k, v in INFO:
        if k in INFO_SKIP:
            continue
        body.append(f'<text class="l" style="animation-delay:{t + 0.22:.2f}s" x="{inner}" y="{cy}">'
                    f'<tspan class="k">{escape(k)}:</tspan><tspan dx="10">{escape(v)}</tspan></text>')
        cy += 27
        t += 0.02

    dy = y + 196
    body.append(f'<line x1="{inner}" y1="{dy}" x2="{x + w - 20}" y2="{dy}" stroke="#21262d"/>')
    body.append(f'<text class="l g b" style="animation-delay:{t + 0.30:.2f}s;font-size:38px" '
                f'x="{inner}" y="{dy + 52}">{AWARDS_COUNT}</text>')
    ly = dy + 28
    for line in AWARDS_LABEL:
        body.append(f'<text class="l t" style="animation-delay:{t + 0.36:.2f}s" '
                    f'x="{inner + 62}" y="{ly}">{escape(line)}</text>')
        ly += 18
        t += 0.02

    ny = dy + 78
    body.append(f'<line x1="{inner}" y1="{ny}" x2="{x + w - 20}" y2="{ny}" stroke="#21262d"/>')
    body.append(f'<text class="l t" style="animation-delay:{t + 0.44:.2f}s" '
                f'x="{inner}" y="{ny + 24}">ahora:</text>')
    ay = ny + 44
    for line in ("AliviaApp en producción · NanoAgent en Rust",
                 "abierto a colaborar en impacto social"):
        body.append(f'<text class="l" style="animation-delay:{t + 0.50:.2f}s" '
                    f'x="{inner}" y="{ay}"><tspan class="g">▸ </tspan>'
                    f'<tspan class="t">{escape(line)}</tspan></text>')
        ay += 19
    return body, H, t + 0.56



def hero(y, t):
    """Retrato + tarjeta, lado a lado, ocupando todo el ancho."""
    pb, pw, ph = _portrait(X, y, t)
    cw = 470
    cb, ch, t = _card(W - X - cw, y + max(0, (ph - 374)) // 2, cw, t + 0.15)
    body = ([pb] if pb else []) + cb
    return body, [], y + max(ph, ch), t


def about(y, t):
    body = label("cat about.md", y, t)
    t += 0.15
    y += 28
    for i, para in enumerate(ABOUT):
        clean = EMOJI.sub("", para).strip()
        for line in textwrap.wrap(clean, 104):
            cls = "l w" if i == 0 else "l"
            body.append(f'<text class="{cls}" style="animation-delay:{t:.2f}s" '
                        f'x="{X + 16}" y="{y}">{escape(line)}</text>')
            y += 20
            t += 0.07
        y += 10
    return body, y - 10, t


def heatmap(y, t):
    """Calendario real de contribuciones, 53 semanas x 7 dias."""
    body = label("./contributions.sh", y, t)
    t += 0.15
    y += 24
    f = ROOT / "data/contributions.json"
    if not f.exists():
        return body, y + 20, t
    data = json.loads(f.read_text(encoding="utf-8"))
    PAL = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
    days = data["days"]
    first = date.fromisoformat(days[0]["date"])
    off = (first.weekday() + 1) % 7
    P, S, LX = 16, 13, X + 14
    TY = y
    cols = (len(days) + off - 1) // 7 + 1
    last_m = None
    for i, d in enumerate(days):
        col, row = (i + off) // 7, (i + off) % 7
        dt = date.fromisoformat(d["date"])
        if row == 0 and dt.month != last_m and col < cols - 2:
            body.append(f'<text class="hm l" style="animation-delay:{(col)*0.02:.2f}s" '
                        f'x="{LX + col*P}" y="{TY-9}">{dt.strftime("%b")}</text>')
            last_m = dt.month
        lvl = min(d["level"], 5)
        body.append(f'<rect class="c" style="animation-delay:{(col+row)*0.02:.2f}s" '
                    f'x="{LX+col*P}" y="{TY+row*P}" width="{S}" height="{S}" rx="3" fill="{PAL[lvl]}">'
                    f'<title>{d["date"]}: {d["count"]}</title></rect>')
    for r, name in ((1, "Lun"), (3, "Mié"), (5, "Vie")):
        body.append(f'<text class="hm" x="{LX-28}" y="{TY+r*P+10}">{name}</text>')
    grid_w = cols * P
    fy = TY + 7 * P + 22
    body.append(f'<text class="hm l" style="animation-delay:.6s" x="{LX}" y="{fy}">'
                f'{data["total"]:,} contribuciones en el último año · racha actual '
                f'{data["current_streak"]} · mejor racha {data["longest_streak"]}</text>')
    lx = LX + grid_w - 6 * P - 92
    body.append(f'<text class="hm" x="{lx}" y="{fy}">Menos</text>')
    for k, c in enumerate(PAL):
        body.append(f'<rect x="{lx+42+k*P}" y="{fy-10}" width="{S}" height="{S}" rx="3" fill="{c}"/>')
    body.append(f'<text class="hm" x="{lx+46+6*P}" y="{fy}">Más</text>')
    return body, fy + 14, t
