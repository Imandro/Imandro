"""Piezas comunes para los SVG estilo terminal."""
from html import escape

FONT = 'ui-monospace,Menlo,Consolas,"DejaVu Sans Mono",monospace'
CSS = (f'text{{font-family:{FONT};font-size:13px;fill:#c9d1d9;white-space:pre}}'
       '.g{fill:#39d353}.d{fill:#1f6f3a}.p{fill:#58a6ff}.t{fill:#8b949e;font-size:12px}'
       '.w{fill:#f0f6fc}.y{fill:#e3b341}.b{font-weight:bold}'
       '.l{opacity:0;animation:in .45s ease-out forwards}'
       '.u{opacity:0;animation:up .4s ease-out forwards}'
       '@keyframes in{from{opacity:0;transform:translateX(-10px)}to{opacity:1;transform:none}}'
       '@keyframes up{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}'
       '@keyframes bl{0%,49%{opacity:1}50%,100%{opacity:0}}.cur{animation:bl 1s steps(1) infinite}')

def open_svg(W, H, title, css=""):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
            f'<style>{CSS}{css}</style>',
            f'<rect width="{W}" height="{H}" rx="10" fill="#0d1117" stroke="#30363d"/>',
            '<circle cx="20" cy="18" r="5" fill="#ff5f56"/><circle cx="38" cy="18" r="5" fill="#ffbd2e"/>'
            '<circle cx="56" cy="18" r="5" fill="#27c93f"/>',
            f'<text class="t" x="76" y="22">{escape(title)}</text>']

def chip(x, y, text, color="#30363d", delay=0.0, cw=7.3):
    w = len(text) * cw + 22
    s = (f'<g class="u" style="animation-delay:{delay:.2f}s">'
         f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="24" rx="12" fill="#161b22" stroke="{color}"/>'
         f'<text class="w" x="{x+11:.1f}" y="{y+16}" style="font-size:12px">{escape(text)}</text></g>')
    return s, w

LANG_COLORS = {"Python": "#3572A5", "TypeScript": "#3178c6", "JavaScript": "#f1e05a", "HTML": "#e34c26",
               "CSS": "#563d7c", "Dart": "#00B4AB", "Java": "#b07219", "Kotlin": "#A97BFF", "C++": "#f34b7d",
               "C#": "#178600", "C": "#555555", "PHP": "#4F5D95", "Shell": "#89e051", "PowerShell": "#012456",
               "SQL": "#e38c00", "PLpgSQL": "#336790", "Vue": "#41b883", "Go": "#00ADD8", "Rust": "#dea584"}

BITS = {  # fuente 5x7 para dígitos
 "0": [".###.","#...#","#..##","#.#.#","##..#","#...#",".###."],
 "1": ["..#..",".##..","..#..","..#..","..#..","..#..",".###."],
 "2": [".###.","#...#","....#","...#.","..#..",".#...","#####"],
 "3": ["####.","....#","....#",".###.","....#","....#","####."],
 "4": ["#...#","#...#","#...#","#####","....#","....#","....#"],
 "5": ["#####","#....","####.","....#","....#","#...#",".###."],
 "6": [".###.","#....","#....","####.","#...#","#...#",".###."],
 "7": ["#####","....#","...#.",".#...".replace(".#...","..#.."),".#...",".#...",".#..."],
 "8": [".###.","#...#","#...#",".###.","#...#","#...#",".###."],
 "9": [".###.","#...#","#...#",".####","....#","....#",".###."],
}
