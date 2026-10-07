#!/usr/bin/env python3
"""Write the documents that come from the source: docs/palette.md.

Usage:
  python3 scripts/make_docs.py              print the documents
  python3 scripts/make_docs.py --write      write them
  python3 scripts/make_docs.py --check-doc  exit 1 if a document is out of date

The script reads src/30-light.css and src/40-dark.css and lists each --lex-* palette
variable with its value in both modes and its use. It uses only the Python standard library.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Use of each palette variable. Each name in the palette must be here.
USES = {
    "ground": "The page background, `--background-primary`",
    "panel": "Panels, the code background, and the tag badge",
    "panel-alt": "The alt panel, `--background-secondary-alt`",
    "ink": "Body text, headings, and links",
    "muted": "Quiet text, icons, and the link hover color",
    "faint": "Placeholders, unresolved links, and code comments",
    "sand": "Borders, dividers, scrollbars, and guides",
    "accent": "The accent: focus, buttons, list markers, the selection tint, and the focused node of the graph",
    "accent-hover": "The hover color of the accent",
    "error": "Error text and background",
    "success": "Success text and background",
    "warning": "Warning text and the function color in code",
    "code-property": "Properties in code",
    "code-value": "Values in code",
    "code-normal": "Plain code text",
    "red": "Base color red: callouts, canvas, and highlights",
    "orange": "Base color orange",
    "yellow": "Base color yellow",
    "green": "Base color green",
    "cyan": "Base color cyan",
    "blue": "Base color blue",
    "purple": "Base color purple",
    "pink": "Base color pink",
    "error-hover": "The hover color of the error background",
    "error-rgb": "The error color as a triple, for Obsidian variables that ask for RGB",
    "graph-tag": "Tag nodes of the graph",
    "graph-unresolved": "Unresolved nodes of the graph",
    "graph-attachment": "Attachment nodes of the graph",
}

GRAPH_USES = {
    "--graph-node": "Resolved nodes", "--graph-node-focused": "The focused node and the focus ring",
    "--graph-node-tag": "Tag nodes", "--graph-node-attachment": "Attachment nodes",
    "--graph-node-unresolved": "Unresolved nodes (drawn at half opacity by Obsidian)",
    "--graph-line": "Lines between nodes", "--graph-text": "Node labels",
}


def block(path, selector):
    css = re.sub(r"url\('data:[^']*'\)", "", path.read_text())
    m = re.search(r"^%s \{\n(.*?)\n\}" % re.escape(selector), css, re.S | re.M)
    return dict(re.findall(r"^\s*(--[a-z0-9-]+):\s*(.+?);\s*$", m.group(1), re.M))


def modes(root=ROOT):
    return block(root / "src" / "30-light.css", ".theme-light"), block(root / "src" / "40-dark.css", ".theme-dark")


def palette_doc(root=ROOT):
    light, dark = modes(root)
    names = [n for n in light if n.startswith("--lex-")]
    out = ["# Palette", "",
           "Each mode file starts with the palette: the `--lex-*` variables. Change a color there, and every rule that uses it follows. A value that starts with `var(` points to another palette color.", "",
           "The table comes from the source. Run `python3 scripts/make_docs.py --write` to make it again.", "",
           "| Variable | Light | Dark | Use |", "|---|---|---|---|"]
    for name in names:
        key = name[len("--lex-"):]
        out.append(f"| `{name}` | `{light[name]}` | `{dark.get(name, '')}` | {USES[key]} |")
    out += ["", "## Graph colors", "",
            "The graph view reads these variables. Each one uses a palette color.", "",
            "| Variable | Light | Dark | Draws |", "|---|---|---|---|"]
    for name, use in GRAPH_USES.items():
        out.append(f"| `{name}` | `{light[name]}` | `{dark[name]}` | {use} |")
    out += ["", "The contrast of each graph color is in `docs/contrast.md`.", ""]
    return "\n".join(out)


def documents(root=ROOT):
    return {root / "docs" / "palette.md": palette_doc(root)}


def main():
    docs = documents()
    if "--write" in sys.argv:
        for path, text in docs.items():
            path.write_text(text)
            print(f"wrote {path.relative_to(ROOT)}")
    elif "--check-doc" in sys.argv:
        stale = [p for p, t in docs.items() if not p.exists() or p.read_text() != t]
        for p in stale:
            print(f"{p.relative_to(ROOT)} is out of date. Run: python3 scripts/make_docs.py --write")
        return 1 if stale else 0
    else:
        for path, text in docs.items():
            print(f"=== {path.relative_to(ROOT)}\n{text}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
