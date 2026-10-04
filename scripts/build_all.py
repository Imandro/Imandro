"""Genera todo: python scripts/build_all.py  (sin foto: omite el retrato)."""
import subprocess, sys
steps = ["make_about_svg.py", "make_banner_svg.py", "make_info_card.py", "make_awards_svg.py", "make_tech_svg.py",
         "fetch_contributions.py", "render_heatmap_svg.py", "fetch_repos.py", "make_projects_svg.py"]
for s in steps:
    print("→", s); subprocess.run([sys.executable, s], check=False)
