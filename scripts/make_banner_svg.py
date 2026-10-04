"""Genera banner.svg: logo ASCII con efecto 'tecleado' + slogan estilo terminal."""
from html import escape
from pathlib import Path
from config import BANNER_NAME, BANNER_LINES
from make_logo import logo_parts
_ldefs, _lcss, _lbody = logo_parts('bn')

ROOT = Path(__file__).resolve().parent.parent
F = {  # fuente 5x7
 "I": ["#####","..#..","..#..","..#..","..#..","..#..","#####"],
 "M": ["#...#","##.##","#.#.#","#.#.#","#...#","#...#","#...#"],
 "A": [".###.","#...#","#...#","#####","#...#","#...#","#...#"],
 "N": ["#...#","##..#","##..#","#.#.#","#..##","#..##","#...#"],
 "D": ["####.","#...#","#...#","#...#","#...#","#...#","####."],
 "R": ["####.","#...#","#...#","####.","#.#..","#..#.","#...#"],
 "O": [".###.","#...#","#...#","#...#","#...#","#...#",".###."],
 "S": [".####","#....","#....",".###.","....#","....#","####."],
 "E": ["#####","#....","#....","####.","#....","#....","#####"],
 "C": [".####","#....","#....","#....","#....","#....",".####"],
 "U": ["#...#","#...#","#...#","#...#","#...#","#...#",".###."],
 "T": ["#####","..#..","..#..","..#..","..#..","..#..","..#.."],
 "Y": ["#...#","#...#",".#.#.","..#..","..#..","..#..","..#.."],
 "B": ["####.","#...#","#...#","####.","#...#","#...#","####."],
 "P": ["####.","#...#","#...#","####.","#....","#....","#...."],
 "V": ["#...#","#...#","#...#","#...#","#...#",".#.#.","..#.."],
 "L": ["#....","#....","#....","#....","#....","#....","#####"],
}
# 1) logo: cada pixel = 2 caracteres
cols = len(BANNER_NAME) * 6 - 1
grid = [[0] * cols for _ in range(7)]
for n, ch in enumerate(BANNER_NAME.upper()):
    for y, row in enumerate(F[ch]):
        for x, c in enumerate(row):
            if c == "#":
                grid[y][n * 6 + x] = 1
rows = []
for y in range(7):
    s = ""
    for x in range(cols):
        if grid[y][x]: s += "##"
        else: s += "  "
    rows.append(s)

CW, FS, LH = 7.4, 12.3, 15
W = 860; X0 = 30; Y0 = 70
H = Y0 + len(rows) * LH + 34 + len(BANNER_LINES) * 52 + 20
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
 f'<style>text{{font-family:ui-monospace,Menlo,Consolas,"DejaVu Sans Mono",monospace;font-size:{FS}px;fill:#c9d1d9;white-space:pre}}'
 '.g{fill:#39d353}.d{fill:#1f6f3a}.p{fill:#58a6ff}.t{fill:#8b949e;font-size:12px}'
 '@keyframes b{0%,49%{opacity:1}50%,100%{opacity:0}}.cur{animation:b 1s steps(1) infinite}' + _lcss + '</style>',
 f'<rect width="{W}" height="{H}" rx="10" fill="#0d1117" stroke="#30363d"/>',
 '<circle cx="20" cy="18" r="5" fill="#ff5f56"/><circle cx="38" cy="18" r="5" fill="#ffbd2e"/><circle cx="56" cy="18" r="5" fill="#27c93f"/>',
 f'<text class="t" x="76" y="22">imandro@github: ~</text>', "<defs>", _ldefs]

def clip(i, x, y, w, begin, dur):
    return (f'<clipPath id="c{i}"><rect x="{x}" y="{y-14}" width="0" height="20">'
            f'<animate attributeName="width" from="0" to="{w}" begin="{begin:.2f}s" dur="{dur:.2f}s" fill="freeze"/></rect></clipPath>')

items = []; t = 0.2; i = 0
for r, s in enumerate(rows):
    y = Y0 + r * LH
    o.append(clip(i, X0, y, len(s) * CW + 4, t, 0.35))
    runs = []
    for ch in s:
        k = "g" if ch == "#" else ("d" if ch == ":" else "")
        if runs and runs[-1][0] == k: runs[-1][1] += ch
        else: runs.append([k, ch])
    spans = "".join(f'<tspan class="{k}">{v}</tspan>' if k else f'<tspan>{v}</tspan>' for k, v in runs)
    items.append(f'<text xml:space="preserve" x="{X0}" y="{y}" clip-path="url(#c{i})">{spans}</text>')
    t += 0.12; i += 1

y = Y0 + len(rows) * LH + 34
for cmd, out in BANNER_LINES:
    line = f'<tspan class="p">{escape(cmd)}</tspan>'
    o.append(clip(i, X0, y, (len(cmd)) * CW + 4, t, 0.5))
    items.append(f'<text xml:space="preserve" x="{X0}" y="{y}" clip-path="url(#c{i})">{line}</text>')
    t += 0.55; i += 1
    y += 22
    o.append(clip(i, X0, y, (len(out) + 2) * CW + 4, t, 0.8))
    items.append(f'<text xml:space="preserve" x="{X0}" y="{y}" clip-path="url(#c{i})">&gt; {escape(out)}</text>')
    t += 0.9; i += 1
    y += 30
items.append(f'<text x="{X0}" y="{y-8}"><tspan class="p">$ </tspan><tspan class="g cur">█</tspan></text>')
o.append("</defs>"); o += items; items_logo = f'<g transform="translate(672,46) scale(.98)">{_lbody}</g>'; o.append(items_logo); o.append("</svg>")
(ROOT / "banner.svg").write_text("\n".join(o))
print("OK: banner.svg")
