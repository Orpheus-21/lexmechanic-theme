#!/usr/bin/env python3
"""Write docs/characters.md: which characters the embedded fonts have.

Usage:
  python3 scripts/font_coverage.py              print the document
  python3 scripts/font_coverage.py --write      write docs/characters.md
  python3 scripts/font_coverage.py --check-doc  exit 1 if docs/characters.md is out of date

The script reads the three WOFF fonts of src/10-fonts.css, decodes the character map
and the feature tags, and lists what each font covers. A character that a font lacks
is drawn with the next font of the font stack. It uses only the Python standard library.
"""
import base64
import re
import struct
import sys
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOC = ROOT / "docs" / "characters.md"

BLOCKS = [
    ("Basic Latin", 0x20, 0x7E), ("Latin 1 Supplement", 0xA0, 0xFF), ("Latin Extended A and B", 0x100, 0x24F),
    ("Greek", 0x370, 0x3FF), ("Cyrillic", 0x400, 0x4FF), ("General Punctuation", 0x2000, 0x206F),
    ("Arrows", 0x2190, 0x21FF), ("Mathematical Operators", 0x2200, 0x22FF), ("Dingbats", 0x2700, 0x27BF),
    ("CJK ideographs", 0x4E00, 0x9FFF),
]
COMMON = "—–…•×÷°±²³½§åÅ→←✓✔‘’“”€™"
NAMES = {"—": "em dash", "–": "en dash", "…": "ellipsis", "•": "bullet", "×": "multiplication sign",
         "÷": "division sign", "°": "degree sign", "±": "plus or minus sign", "²": "superscript two",
         "³": "superscript three", "½": "one half", "§": "section sign", "å": "a with ring",
         "Å": "A with ring", "→": "right arrow", "←": "left arrow", "✓": "check mark", "✔": "heavy check mark",
         "‘": "left single quote", "’": "right single quote", "“": "left double quote",
         "”": "right double quote", "€": "euro sign", "™": "trade mark sign"}


def read_fonts(css):
    """Return [(family, style, woff bytes)] for the @font-face rules with a woff data URI."""
    css = css.replace("\n", " ")
    fonts = []
    for m in re.finditer(r"font-family: '([^']+)';\s*src: url\('data:font/woff;base64,([^']+)'\)[^}]*?font-style: (\w+)", css):
        fonts.append((m.group(1), m.group(3), base64.b64decode(m.group(2))))
    return fonts


def tables(woff):
    """Return {tag: bytes} for the tables of a WOFF file."""
    count = struct.unpack(">H", woff[12:14])[0]
    out = {}
    for i in range(count):
        tag, offset, comp, orig, _ = struct.unpack(">4sIIII", woff[44 + 20 * i:64 + 20 * i])
        data = woff[offset:offset + comp]
        out[tag.decode()] = zlib.decompress(data) if comp < orig else data
    return out


def codepoints(cmap):
    """Return the set of code points of cmap formats 4 and 12."""
    found = set()
    for k in range(struct.unpack(">H", cmap[2:4])[0]):
        _, _, offset = struct.unpack(">HHI", cmap[4 + 8 * k:12 + 8 * k])
        fmt = struct.unpack(">H", cmap[offset:offset + 2])[0]
        if fmt == 4:
            segs = struct.unpack(">H", cmap[offset + 6:offset + 8])[0] // 2
            ends = struct.unpack(">%dH" % segs, cmap[offset + 14:offset + 14 + 2 * segs])
            starts = struct.unpack(">%dH" % segs, cmap[offset + 16 + 2 * segs:offset + 16 + 4 * segs])
            for a, b in zip(starts, ends):
                if a != 0xFFFF:
                    found.update(range(a, b + 1))
        elif fmt == 12:
            groups = struct.unpack(">I", cmap[offset + 12:offset + 16])[0]
            for g in range(groups):
                a, b, _ = struct.unpack(">III", cmap[offset + 16 + 12 * g:offset + 28 + 12 * g])
                found.update(range(a, b + 1))
    return found


def features(tabs):
    found = set()
    for name in ("GSUB", "GPOS"):
        if name in tabs:
            data = tabs[name]
            at = struct.unpack(">H", data[6:8])[0]
            for k in range(struct.unpack(">H", data[at:at + 2])[0]):
                found.add(f"{name}: {data[at + 2 + 6 * k:at + 6 + 6 * k].decode()}")
    return sorted(found)


def document(root=ROOT):
    out = ["# Characters of the embedded fonts", "",
           "This file lists which characters the fonts Volume Tc and Volume Tc Sans have. A character that a font lacks is drawn with the next font of the font stack. The text stack ends with Georgia, Times New Roman, and a serif font. The interface stack ends with Verdana and a sans-serif font. A line of text can then have glyphs of two styles.",
           "", "The tables come from `scripts/font_coverage.py`. Run `python3 scripts/font_coverage.py --write` to make them again.", ""]
    for family, style, woff in read_fonts((root / "src" / "10-fonts.css").read_text()):
        tabs = tables(woff)
        cps = codepoints(tabs["cmap"])
        out += [f"## {family}, {style}", "", f"* Characters: {len(cps)}",
                f"* Layout features: {', '.join(features(tabs)) or 'none'}", "",
                "| Block | Characters | Of |", "|---|---|---|"]
        for name, a, b in BLOCKS:
            have = sum(1 for c in range(a, b + 1) if c in cps)
            if have:
                out.append(f"| {name} | {have} | {b - a + 1} |")
        missing = [c for c in COMMON if ord(c) not in cps]
        out += ["", "Common characters that the font lacks:", ""]
        out += [f"* `{c}` {NAMES[c]} (U+{ord(c):04X})" for c in missing] or ["* none"]
        out.append("")
    out += ["## Test line", "", "Put this line in a note, and look at which glyphs differ in style:", "",
            "```", " ".join(COMMON), "```", ""]
    return "\n".join(out)


def main():
    text = document()
    if "--write" in sys.argv:
        DOC.write_text(text)
        print(f"wrote {DOC.relative_to(ROOT)}")
    elif "--check-doc" in sys.argv:
        if not DOC.exists() or DOC.read_text() != text:
            print("docs/characters.md is out of date. Run: python3 scripts/font_coverage.py --write")
            return 1
        print("docs/characters.md is up to date")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
