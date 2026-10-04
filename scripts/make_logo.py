"""Símbolo de marca: hexágono (escudo) + 'i' con candado + corchetes de código + cursor."""
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent

def logo_parts(u="lg"):
    defs = (f'<linearGradient id="{u}g" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0" stop-color="#39d353"/><stop offset="1" stop-color="#58a6ff"/></linearGradient>')
    css = (f'.{u}h{{stroke-dasharray:430;stroke-dashoffset:430;animation:{u}d 1.4s ease-out .2s forwards}}'
           f'@keyframes {u}d{{to{{stroke-dashoffset:0}}}}'
           f'.{u}f{{opacity:0;animation:{u}a .5s ease-out forwards}}@keyframes {u}a{{to{{opacity:1}}}}'
           f'.{u}n{{opacity:0;transform-box:fill-box;transform-origin:center;animation:{u}p .4s ease-out forwards}}'
           f'@keyframes {u}p{{from{{opacity:0;transform:scale(0)}}to{{opacity:1;transform:scale(1)}}}}'
           f'.{u}c{{animation:{u}k 1.1s steps(1) 2.2s infinite}}@keyframes {u}k{{50%{{opacity:.35}}}}')
    nodes = [(80, 10), (140.6, 45), (140.6, 115), (80, 150), (19.4, 115), (19.4, 45)]
    body = (f'<polygon class="{u}h" points="80,10 140.6,45 140.6,115 80,150 19.4,115 19.4,45" fill="#0d1117" '
            f'stroke="url(#{u}g)" stroke-width="4" stroke-linejoin="round"/>'
            f'<polygon class="{u}f" style="animation-delay:.9s" points="80,24 128.5,52 128.5,108 80,136 31.5,108 31.5,52" '
            f'fill="none" stroke="url(#{u}g)" stroke-width="1.2" opacity=".4"/>')
    for i, (x, y) in enumerate(nodes):
        body += f'<circle class="{u}n" style="animation-delay:{1.0 + i*.12:.2f}s" cx="{x}" cy="{y}" r="3.6" fill="#39d353"/>'
    body += (f'<g class="{u}f" style="animation-delay:1.5s">'
             '<polyline points="52,62 36,80 52,98" fill="none" stroke="#39d353" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
             '<polyline points="108,62 124,80 108,98" fill="none" stroke="#58a6ff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
             f'<circle cx="80" cy="52" r="8" fill="url(#{u}g)"/>'
             '<circle cx="80" cy="50.5" r="2.2" fill="#0d1117"/><rect x="79" y="51" width="2" height="5" rx="1" fill="#0d1117"/>'
             f'<rect class="{u}c" x="72" y="68" width="16" height="48" rx="3" fill="url(#{u}g)"/></g>')
    return defs, css, body

if __name__ == "__main__":
    d, c, b = logo_parts("lg")
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 160" width="160" height="160">'
           f'<style>{c}</style><defs>{d}</defs>{b}</svg>')
    (ROOT / "logo.svg").write_text(svg)
    print("OK: logo.svg")
