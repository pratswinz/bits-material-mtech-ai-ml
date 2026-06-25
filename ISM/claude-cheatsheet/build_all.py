#!/usr/bin/env python3
"""Rebuild all ISM claude-cheatsheet HTML outputs."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def run(script: str) -> None:
    print(f"\n=== {script} ===")
    subprocess.run([sys.executable, str(ROOT / script)], check=True, cwd=ROOT)


def main() -> None:
    run("build_theory.py")
    run("build_workbook.py")
    run("build_study_plan.py")
    run("build_past_papers.py")
    run("build_revision.py")
    print("\nAll done. Open index.html in ISM/claude-cheatsheet/")


if __name__ == "__main__":
    main()
