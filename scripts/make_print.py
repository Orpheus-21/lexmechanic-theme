#!/usr/bin/env python3
"""Write src/45-print.css, the rule that prints a dark mode note with the light colors.

Usage:
  python3 scripts/make_print.py              print the file
  python3 scripts/make_print.py --write      write it
  python3 scripts/make_print.py --check-doc  exit 1 if the file is out of date

Paper is white, and the light text of the dark mode is not readable on it. The file repeats the
variables of the .theme-light block of src/30-light.css under `@media print` for .theme-dark. The
script copies them, so the print colors follow every change of the light mode. It uses only the
Python standard library.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "src" / "45-print.css"


def render(light):
    block = re.search(r"^\.theme-light \{\n(.*?)\n\}", light, re.S | re.M).group(1)
    body = "\n".join(("  " + line) if line.strip() else line for line in block.split("\n"))
    return ("/* Print: paper is white, so a dark mode note prints with the light colors.\n"
            "   scripts/make_print.py writes this file from src/30-light.css. Do not edit it. */\n"
            "@media print {\n  .theme-dark {\n" + body + "\n  }\n}\n")


def main():
    text = render((ROOT / "src" / "30-light.css").read_text())
    if "--write" in sys.argv:
        TARGET.write_text(text)
        print(f"wrote {TARGET.relative_to(ROOT)}")
    elif "--check-doc" in sys.argv:
        if not TARGET.exists() or TARGET.read_text() != text:
            print("src/45-print.css is out of date. Run: python3 scripts/make_print.py --write")
            return 1
        print("src/45-print.css is up to date")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
