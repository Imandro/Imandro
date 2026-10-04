from html import escape
from pathlib import Path
from config import AWARDS_COUNT, AWARDS_LABEL, HANDLE
from svgkit import open_svg, BITS

ROOT = Path(__file__).resolve().parent.parent
TROPHY = ["       ___________", "      '._==_==_=_.'", "      .-\\:      /-.", "     | (|:.     |) |",
          "      '-|:.     |-'", "        \\::.    /", "         '::. .'", "           ) (",
          "         _.' '._", "        '-------'"]
CW, LH = 8.4, 17
W, H = 860, 258
o = open_svg(W, H, f"{HANDLE}@github: ~/trofeos")
defs, items = [], []
o.append(f'<text x="26" y="52"><tspan class="p">$</tspan> ./trofeos --contar</text>')

def wipe(i, x, y, w, begin, dur=0.5, h=LH + 4):
    defs.append(f'<clipPath id="a{i}"><rect x="{x}" y="{y - 14}" width="0" height="{h}">'
                f'<animate attributeName="width" from="0" to="{w:.1f}" begin="{begin:.2f}s" dur="{dur:.2f}s" fill="freeze"/></rect></clipPath>')
    return f'clip-path="url(#a{i})"'

n = 0; t = 0.2; y0 = 84
for r, line in enumerate(TROPHY):                       # trofeo ASCII
    y = y0 + r * LH
    items.append(f'<text class="y" xml:space="preserve" x="44" y="{y}" {wipe(n, 40, y, len(line)*CW+8, t)}>{escape(line)}</text>')
    n += 1; t += 0.09
digits = str(AWARDS_COUNT); cols = len(digits) * 6 - 1
for r in range(7):                                      # número grande
    s = ""
    for k, d in enumerate(digits):
        s += "".join("##" if c == "#" else "  " for c in BITS[d][r]) + ("  " if k < len(digits) - 1 else "")
    y = y0 + 12 + r * LH
    items.append(f'<text class="g b" style="font-size:14px" xml:space="preserve" x="330" y="{y}" {wipe(n, 326, y, len(s)*CW+8, t+0.6, 0.45)}>{s}</text>')
    n += 1; t += 0.07
lx = 330 + len(digits) * 12 * CW + 40
items.append(f'<text class="w b" style="font-size:16px" x="{lx:.0f}" y="{y0+30}" {wipe(n, lx-4, y0+30, 330, t+1.0, .5, 24)}>{escape(AWARDS_LABEL[0])}</text>'); n += 1
items.append(f'<text class="w b" style="font-size:16px" x="{lx:.0f}" y="{y0+54}" {wipe(n, lx-4, y0+54, 330, t+1.3, .6, 24)}>{escape(AWARDS_LABEL[1])}</text>'); n += 1
items.append(f'<text class="g" style="font-size:15px" x="{lx:.0f}" y="{y0+82}" {wipe(n, lx-4, y0+82, 330, t+1.9, .4, 24)}>ganados</text>'); n += 1
items.append(f'<text class="y l" style="font-size:16px;animation-delay:{t+2.3:.2f}s" x="{lx:.0f}" y="{y0+108}">★ ★ ★ ★ ★</text>')
o.append("<defs>" + "".join(defs) + "</defs>"); o += items; o.append("</svg>")
(ROOT / "awards.svg").write_text("\n".join(o)); print("OK: awards.svg")
