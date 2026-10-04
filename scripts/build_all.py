"""Genera todo: python scripts/build_all.py"""
import subprocess, sys, os
steps = ["fetch_contributions.py", "fetch_repos.py", "make_profile_svg.py"]
for s in steps:
    print("→", s)
    subprocess.run([sys.executable, s], check=False, cwd=os.path.dirname(os.path.abspath(__file__)))