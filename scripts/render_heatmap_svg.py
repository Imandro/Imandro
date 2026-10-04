import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
data = json.loads((ROOT / "data/contributions.json").read_text())
PAL = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
days = data["days"]
first = date.fromisoformat(days[0]["date"])
off = (first.weekday() + 1) % 7          # domingo = fila 0
P, S, LX, TY = 16, 13, 30, 40
cols = (len(days) + off - 1) // 7 + 1
W, H = LX + cols * P + 20, TY + 7 * P + 62

out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
 '<style>text{font-family:ui-monospace,Menlo,Consolas,monospace;fill:#8b949e;font-size:11px}'
 '.c{opacity:0;animation:in .5s ease-out forwards}'
 '@keyframes in{from{opacity:0;transform:translateY(-8px)}to{opacity:1;transform:none}}</style>',
 f'<rect width="{W}" height="{H}" rx="10" fill="#0d1117"/>']

last_m = None
for i, d in enumerate(days):
    col, row = (i + off) // 7, (i + off) % 7
    dt = date.fromisoformat(d["date"])
    if row == 0 and dt.month != last_m and col < cols - 2:
        out.append(f'<text x="{LX + col*P}" y="{TY-10}">{dt.strftime("%b")}</text>')
        last_m = dt.month
    lvl = min(d["level"], 5)
    out.append(f'<rect class="c" style="animation-delay:{(col+row)*0.025:.2f}s" '
               f'x="{LX+col*P}" y="{TY+row*P}" width="{S}" height="{S}" rx="3" fill="{PAL[lvl]}">'
               f'<title>{d["date"]}: {d["count"]}</title></rect>')

for r, name in ((1, "Lun"), (3, "Mié"), (5, "Vie")):
    out.append(f'<text x="2" y="{TY+r*P+10}">{name}</text>')

fy = TY + 7 * P + 24
out.append(f'<text x="{LX}" y="{fy}">{data["total"]:,} contribuciones en el último año · '
           f'racha actual {data["current_streak"]} · mejor racha {data["longest_streak"]}</text>')
lx = W - 20 - 6 * P - 90
out.append(f'<text x="{lx}" y="{fy+22}">Menos</text>')
for k, c in enumerate(PAL):
    out.append(f'<rect x="{lx+42+k*P}" y="{fy+12}" width="{S}" height="{S}" rx="3" fill="{c}"/>')
out.append(f'<text x="{lx+46+6*P}" y="{fy+22}">Más</text></svg>')
(ROOT / "contrib-heatmap.svg").write_text("\n".join(out))
print("OK: contrib-heatmap.svg")
