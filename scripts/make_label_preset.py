#!/usr/bin/env python3
"""Write snippets/presets/lexmechanic-graph-labels.css, the preset that draws the graph labels in Volume Tc Sans.

Usage:
  python3 scripts/make_label_preset.py              print the preset
  python3 scripts/make_label_preset.py --write      write it
  python3 scripts/make_label_preset.py --check-doc  exit 1 if the file is out of date

Obsidian draws the labels of the graph with a font stack that it fixes in its JavaScript, and the stack
starts with ui-sans-serif. Chromium does not know ui-sans-serif as a generic family, so a font face with
that name is used first. The preset defines such a face with the data of the Volume Tc Sans font. The data
is the same as in theme.css, which is why the preset is large and why a script copies it. It uses
only the Python standard library.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "snippets" / "presets" / "lexmechanic-graph-labels.css"

HEADER = """/* Lexmechanic graph labels preset: the labels of the graph use Volume Tc Sans.
   Obsidian draws the labels with a font stack that starts with ui-sans-serif. Chromium does not know
   ui-sans-serif as a generic family, so this font face, which has that name, is used first. The data
   below is the data of Volume Tc Sans in theme.css. scripts/make_label_preset.py copies it, so do not
   edit this file by hand. Characters that the font lacks use the next font of the stack. */

"""


def sans_face(css):
    m = re.search(r"@font-face \{\n  font-family: 'Volume Tc Sans';\n  src: (.*?);\n", css, re.S)
    return m.group(1)


def preset(root=ROOT):
    src = sans_face((root / "src" / "10-fonts.css").read_text())
    return HEADER + f"@font-face {{\n  font-family: 'ui-sans-serif';\n  src: {src};\n  font-weight: 400;\n  font-style: normal;\n}}\n"


def main():
    text = preset()
    if "--write" in sys.argv:
        TARGET.write_text(text)
        print(f"wrote {TARGET.relative_to(ROOT)} ({len(text)} bytes)")
    elif "--check-doc" in sys.argv:
        if not TARGET.exists() or TARGET.read_text() != text:
            print("The labels preset is out of date. Run: python3 scripts/make_label_preset.py --write")
            return 1
        print("the labels preset is up to date")
    else:
        print(text[:600] + "...")
    return 0


if __name__ == "__main__":
    sys.exit(main())
