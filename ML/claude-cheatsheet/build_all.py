#!/usr/bin/env python3
"""Rebuild all ML claude-cheatsheet HTML outputs."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def run(script: str) -> None:
    print(f"\n=== {script} ===")
    subprocess.run([sys.executable, str(ROOT / script)], check=True, cwd=ROOT)


def main() -> None:
    run("build_past_papers.py")
    run("enrich_workbook.py")
    print("\nAll done. Open index.html in ML/claude-cheatsheet/")


if __name__ == "__main__":
    main()
