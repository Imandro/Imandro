"""Uso: python scripts/make_ascii_svg.py foto.jpg
Convierte tu foto en un retrato ASCII monocromo que se 'escribe' fila por fila.
Consejo: usa una foto con buena luz y fondo simple (o quítale el fondo antes)."""
import sys
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
RAMP = " .,:;i1tfLCG08@"      # claro (ralo) -> oscuro (denso)
COLS, CW, RH, FS = 110, 3.4, 6.8, 5.7

img = Image.open(sys.argv[1]).convert("L")
img = ImageOps.autocontrast(img, cutoff=2)
rows = round(COLS * img.height / img.width * (CW / RH) * 1.0)
img = img.resize((COLS, rows), Image.LANCZOS)
px = img.load()

W, H = COLS * CW + 20, rows * RH + 20
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" width="{W:.0f}" height="{H:.0f}">',
     f'<style>text{{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:{FS}px;fill:#c9d1d9;white-space:pre}}</style>',
     f'<rect width="100%" height="100%" rx="10" fill="#0d1117"/>', "<defs>"]
for r in range(rows):
    o.append(f'<clipPath id="r{r}"><rect x="10" y="{10+r*RH-1:.1f}" width="0" height="{RH+1}">'
             f'<animate attributeName="width" from="0" to="{COLS*CW+4:.1f}" begin="{r*0.07:.2f}s" dur="0.6s" fill="freeze"/>'
             f'</rect></clipPath>')
o.append("</defs>")
for r in range(rows):
    line = "".join(RAMP[int((255 - px[c, r]) / 256 * len(RAMP))] for c in range(COLS))
    if line.strip():
        o.append(f'<text xml:space="preserve" x="10" y="{10+(r+1)*RH-1.5:.1f}" textLength="{COLS*CW:.1f}" '
                 f'lengthAdjust="spacing" clip-path="url(#r{r})">{line}</text>')
o.append("</svg>")
(ROOT / "avi-ascii.svg").write_text("\n".join(o))
print("OK: avi-ascii.svg")
