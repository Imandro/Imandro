"""Secciones reutilizables que make_profile_svg.py compone en un unico panel.

Cada funcion devuelve (body, w, h, t): los elementos SVG, su ancho y alto, y
el delay de animacion acumulado para que las secciones encadenen en cascada.
"""
import json
import re
import textwrap
from html import escape
from pathlib import Path

from config import (USERNAME, HANDLE, BANNER_NAME, BANNER_LINES, INFO, ABOUT,
                    AWARDS_COUNT, AWARDS_LABEL, TECH, FEATURED, OTHER_MAX)
from svgkit import chip, BITS

ROOT = Path(__file__).resolve().parent.parent

# Filas de INFO que ya dice otra seccion: la pila vive en tech(), los proyectos
# en projects() y lo movil tambien esta en tech(). Quitarlas evita el repetition.
INFO_SKIP = {"Stack", "Móvil", "Proyectos"}

# Comandos de BANNER_LINES que se renderizan despues como seccion propia.
BANNER_SKIP = {"$ whoami"}

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

TROPHY = ["       ___________", "      '._==_==_=_.'", "      .-\\:      /-.", "     | (|:.     |) |",
          "      '-|:.     |-'", "        \\::.    /", "         '::. .'", "           ) (",
          "         _.' '._", "        '-------'"]


def label(cmd, y, t):
    """Linea de prompt `$ comando`."""
    return [f'<text class="l" style="animation-delay:{t:.2f}s" x="30" y="{y}">'
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
        defs.append(f'<clipPath id="n{r}"><rect x="30" y="{y + r*LH - 14}" width="0" height="{LH + 4}">'
                    f'<animate attributeName="width" from="0" to="{len(s)*CW + 8:.1f}" '
                    f'begin="{t:.2f}s" dur="0.35s" fill="freeze"/></rect></clipPath>')
        body.append(f'<text class="g b" style="font-size:{FS}px" xml:space="preserve" '
                    f'x="30" y="{y + r*LH}" clip-path="url(#n{r})">{s}</text>')
        t += 0.12
    return body, defs, cols * CW, 7 * LH, t


def slogan(y, t):
    """Lineas de BANNER_LINES cuyo comando no se repita como seccion."""
    body = []
    for cmd, out in BANNER_LINES:
        if cmd in BANNER_SKIP:
            continue
        body.append(f'<text class="l" style="animation-delay:{t:.2f}s" x="46" y="{y}">'
                    f'<tspan class="t">&gt; </tspan>{escape(out)}</text>')
        y += 22
        t += 0.15
    return body, y - 22, t


def whoami(y, t):
    body = label("whoami", y, t)
    t += 0.15
    y += 28
    body.append(f'<text class="l w" style="animation-delay:{t:.2f}s;font-size:15px" x="46" y="{y}">'
                f'{escape(HANDLE)}@github</text>')
    y += 28
    t += 0.12
    for k, v in INFO:
        if k in INFO_SKIP:
            continue
        body.append(f'<text class="l" style="animation-delay:{t:.2f}s" x="46" y="{y}">'
                    f'<tspan class="k">{escape(k)}:</tspan><tspan dx="10">{escape(v)}</tspan></text>')
        y += 26
        t += 0.14
    return body, 930, y - 26, t


import re
_emoji = re.compile(r'[^\x00-\x7F]+')
def about(y, t):
    body = label("cat about.md", y, t)
    t += 0.15
    y += 28
    for i, para in enumerate(ABOUT):
        clean = _emoji.sub('', para)
        for line in textwrap.wrap(clean, 108):
            cls = "w" if i == 0 else ""
            body.append(f'<text class="l {cls}" style="animation-delay:{t:.2f}s" x="46" y="{y}">{escape(line)}</text>')
            y += 20
            t += 0.08
        y += 8
    return body, 930, y - 8, t


def portrait():
    """Reutiliza avi-ascii.svg (se genera aparte: necesita la foto)."""
    f = ROOT / "avi-ascii.svg"
    if not f.exists():
        return [], 0, 0
    s = f.read_text(encoding="utf-8")
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', s)
    if not m:
        return [], 0, 0
    w, h = float(m.group(1)), float(m.group(2))
    body = []
    d = re.search(r"<defs>(.*?)</defs>", s, re.S)
    r = re.search(r"</defs>(.*)</svg>", s, re.S)
    if d:
        body.append(f"<defs>{d.group(1)}</defs>")
    if r:
        body.append(r.group(1).replace("<text ", '<text class="pa" '))
    return body, w, h


def awards(y, t):
    """Contador de premios, sin trofeo ASCII ni estrellas."""
    digits = str(AWARDS_COUNT)
    NW, LH = 9.0, 18
    body, defs = [], []
    for r in range(7):
        s = ""
        for k, d in enumerate(digits):
            s += "".join("##" if c == "#" else "  " for c in BITS[d][r]) + ("  " if k < len(digits) - 1 else "")
        defs.append(f'<clipPath id="v{r}"><rect x="0" y="{y + r*LH - 16}" width="0" height="{LH + 6}">'
                    f'<animate attributeName="width" from="0" to="{len(s)*NW + 10:.1f}" '
                    f'begin="{t:.2f}s" dur="0.4s" fill="freeze"/></rect></clipPath>')
        body.append(f'<text class="g b" style="font-size:15px" xml:space="preserve" '
                    f'x="0" y="{y + r*LH}" clip-path="url(#v{r})">{s}</text>')
    t += 0.5
    y += 7 * LH + 20
    for lab in AWARDS_LABEL:
        body.append(f'<text class="l w b" style="animation-delay:{t:.2f}s;font-size:15px" x="0" y="{y}">{escape(lab)}</text>')
        y += 22
        t += 0.15
    body.append(f'<text class="l g" style="animation-delay:{t:.2f}s;font-size:14px" x="0" y="{y}">ganados</text>')
    return body, defs, 360, y + 20, t


def heatmap(t):
    f = ROOT / "data/contributions.json"
    if not f.exists():
        return [], 0, 0, t
    data = json.loads(f.read_text())
    PAL = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
    from datetime import date
    days = data["days"]
    first = date.fromisoformat(days[0]["date"])
    off = (first.weekday() + 1) % 7
    P, S, LX, TY = 16, 13, 30, 26
    cols = (len(days) + off - 1) // 7 + 1
    body, last_m = [], None
    for i, d in enumerate(days):
        col, row = (i + off) // 7, (i + off) % 7
        dt = date.fromisoformat(d["date"])
        if row == 0 and dt.month != last_m and col < cols - 2:
            body.append(f'<text class="hm l" style="animation-delay:{(col)*0.02:.2f}s" x="{LX + col*P}" y="{TY-9}">{dt.strftime("%b")}</text>')
            last_m = dt.month
        lvl = min(d["level"], 5)
        body.append(f'<rect class="c" style="animation-delay:{(col+row)*0.02:.2f}s" '
                    f'x="{LX+col*P}" y="{TY+row*P}" width="{S}" height="{S}" rx="3" fill="{PAL[lvl]}">'
                    f'<title>{d["date"]}: {d["count"]}</title></rect>')
    for r, name in ((1, "Lun"), (3, "Mié"), (5, "Vie")):
        body.append(f'<text class="hm" x="2" y="{TY+r*P+10}">{name}</text>')
    W = LX + cols * P + 20
    fy = TY + 7 * P + 22
    body.append(f'<text class="hm l" style="animation-delay:.6s" x="{LX}" y="{fy}">'
                f'{data["total"]:,} contribuciones en el último año · racha actual {data["current_streak"]}'
                f' · mejor racha {data["longest_streak"]}</text>')
    lx = W - 20 - 6 * P - 90
    body.append(f'<text class="hm" x="{lx}" y="{fy}">Menos</text>')
    for k, c in enumerate(PAL):
        body.append(f'<rect x="{lx+42+k*P}" y="{fy-10}" width="{S}" height="{S}" rx="3" fill="{c}"/>')
    body.append(f'<text class="hm" x="{lx+46+6*P}" y="{fy}">Más</text>')
    return body, W, fy + 14, t


def tech(y, t):
    COLORS = ["#3572A5", "#61dafb", "#336790", "#f1e05a", "#39d353"]
    LX, X0, MAXX = 30, 230, 930
    body = label("cat stack.yml", y, t)
    t += 0.15
    y += 32
    d = t
    for ci, (cat, items) in enumerate(TECH.items()):
        col = COLORS[ci % len(COLORS)]
        body.append(f'<text class="l g b" style="animation-delay:{d:.2f}s" x="{LX}" y="{y+17}">{escape(cat)}:</text>')
        x = X0
        for it in items:
            _, w = chip(0, 0, it, col, d)
            if x + w > MAXX:
                x = X0
                y += 32
            c, w = chip(x, y, it, col, d)
            body.append(c)
            x += w + 8
            d += 0.04
        y += 40
    return body, 930, y, t


def projects(y, t):
    f = ROOT / "data/repos.json"
    repos = json.loads(f.read_text()) if f.exists() else []
    X = 30
    body = label("ls projects/", y, t)
    t += 0.15
    y += 30
    for p in FEATURED:
        body.append(f'<text class="l g b" style="animation-delay:{t:.2f}s;font-size:14px" x="{X}" y="{y}">▸ {escape(p["name"])}'
                    f'<tspan class="t" dx="10" style="font-weight:normal">{escape(p["tag"])}</tspan></text>')
        y += 21
        t += 0.18
        for line in (textwrap.wrap(p["desc"], 100) if p["desc"] else []):
            body.append(f'<text class="l" style="animation-delay:{t:.2f}s" x="{X+16}" y="{y}">{escape(line)}</text>')
            y += 19
            t += 0.07
        for pt in p["points"]:
            for i, line in enumerate(textwrap.wrap(pt, 100)):
                pre = '<tspan class="g">•</tspan> ' if i == 0 else ""
                body.append(f'<text class="l t" style="animation-delay:{t:.2f}s;font-size:12.5px" x="{X+16}" y="{y}">{pre}{escape(line)}</text>')
                y += 19
                t += 0.06
        x = X + 16
        y += 2
        for s in p["stack"]:
            c, w = chip(x, y, s, "#1f6feb", t)
            body.append(c)
            x += w + 8
            t += 0.03
        y += 40
    skip = {p["name"].lower() for p in FEATURED} | {USERNAME.lower()}
    others = [r for r in repos if not r["fork"] and r["name"].lower() not in skip][:OTHER_MAX]
    if others:
        body.append(f'<text class="l t" style="animation-delay:{t:.2f}s" x="{X}" y="{y}">── otros repositorios ──</text>')
        y += 24
        t += 0.1
        line = "  ·  ".join(r["name"] for r in others)
        for chunk in textwrap.wrap(line, 104):
            body.append(f'<text class="l t" style="animation-delay:{t:.2f}s" x="{X}" y="{y}">{escape(chunk)}</text>')
            y += 20
            t += 0.06
    return body, 930, y, t