#!/usr/bin/env python3
"""Write the documents that come from the source: docs/palette.md and docs/variables.md.

Usage:
  python3 scripts/make_docs.py              print the documents
  python3 scripts/make_docs.py --write      write them
  python3 scripts/make_docs.py --check-doc  exit 1 if a document is out of date

The script reads the files of src/ and the snippets. It lists each --lex-* palette variable
with its value in both modes and its use, and each Obsidian variable that the theme sets
with its value in each mode, grouped by area. It uses only the Python standard library.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_contrast import resolve  # noqa: E402

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
    out += ["", "The contrast of each graph color is in `docs/contrast.md`.", "",
            "## Colors for graph.json", "",
            "A color group in `graph.json` stores its color as one integer: red times 65536, plus green times 256, plus blue. The table gives each palette color that is a solid color as a hex value and as an integer. `scripts/graph_groups.py` makes the `colorGroups` list from these colors.", "",
            "| Name | Light | Light integer | Dark | Dark integer |", "|---|---|---|---|---|"]
    for key in USES:
        a, b = resolve("--lex-" + key, light), resolve("--lex-" + key, dark)
        if a and b:
            out.append(f"| `{key}` | `{a}` | {int(a[1:], 16)} | `{b}` | {int(b[1:], 16)} |")
    out.append("")
    return "\n".join(out)


# (title, prefixes, why the theme sets these variables). The first area that matches a variable wins.
AREAS = [
    ("Fonts", ("--font-",), "The text, interface, and monospace fonts. The names that end in `-theme` are the ones that the font settings of Obsidian replace."),
    ("Backgrounds and borders", ("--background-",), "The page and panel colors, borders, the hover color, the error and success fills, the form field fill, and the modal cover. All of them come from the palette, so that no gray of Obsidian is left."),
    ("Text", ("--text-",), "The colors of normal, quiet, and faint text, the accent, the status colors, and the selection. Each one has a contrast of 4.5 to 1 or more on the page."),
    ("Accent", ("--accent-", "--interactive-", "--caret-"), "The accent. `--accent-h`, `--accent-s`, and `--accent-l` give Obsidian the hue, and the other variables give the colors of buttons and the caret."),
    ("Links", ("--link-",), "Links are the ink color. External links use the accent. Unresolved links use the faint color at full opacity, because Obsidian lowers it to 0.7 by default."),
    ("Headings", ("--h1-", "--h2-", "--h3-", "--h4-", "--h5-", "--h6-", "--inline-title"), "Headings use the text font in bold and the ink color. The variables reach reading view and Live Preview."),
    ("Code", ("--code-",), "The colors of code and of the syntax tokens, all from the palette, and the 1 pixel border."),
    ("Block quotes", ("--blockquote-",), "A 4 pixel accent border, like the border of callouts and code blocks."),
    ("Lists, tasks, and guides", ("--list-", "--checkbox-", "--indentation-"), "Accent list markers and checkboxes, and warm indentation guides."),
    ("Interface", ("--nav-", "--scrollbar-", "--drag-", "--toggle-", "--slider-", "--notice-", "--tooltip-", "--divider-", "--canvas-"), "Parts of the interface that use a gray or a white in Obsidian: the file list, scrollbars, the drag ghost, toggles, sliders, notices, tooltips, dividers, and the canvas."),
    ("Graph", ("--graph-",), "The colors of the graph view. Obsidian reads them through hidden elements. See `docs/graph.md`."),
    ("Base colors", ("--color-",), "The eight colors that Obsidian uses for callouts, the canvas, and highlights, from the palette."),
    ("Snippet variables", ("--tag-", "--hr-"), "Set by the snippets: the tag badge and the horizontal rule."),
]


def snippet_block(path):
    css = path.read_text()
    m = re.search(r"^\.theme-light, \.theme-dark \{\n(.*?)\n\}", css, re.S | re.M)
    return dict(re.findall(r"^\s*(--[a-z0-9-]+):\s*(.+?);\s*$", m.group(1), re.M)) if m else {}


def variable_rows(root=ROOT):
    """Return {name: (light value, dark value, where it is set)} for each variable that is not in the palette."""
    light, dark = modes(root)
    shared = block(root / "src" / "20-shared.css", ".theme-dark, .theme-light")
    rows = {}
    for name, value in shared.items():
        rows[name] = (value, value, "theme")
    for name in light:
        if not name.startswith("--lex-"):
            rows[name] = (light[name], dark.get(name, light[name]), "theme")
    rules = (root / "src" / "50-rules.css").read_text()
    for name, value in re.findall(r"body\.theme-light, body\.theme-dark \{ (--[a-z0-9-]+): (.+?); \}", rules):
        rows[name] = (value, value, "theme")
    for snippet in sorted((root / "snippets").glob("*.css")):
        for name, value in snippet_block(snippet).items():
            rows[name] = (value, value, snippet.stem)
    return rows


def area_of(name):
    for title, prefixes, _ in AREAS:
        if name.startswith(prefixes):
            return title
    return "Other"


def variables_doc(root=ROOT):
    rows = variable_rows(root)
    out = ["# Variables", "",
           "This file lists each Obsidian variable that the theme or a snippet sets, with its value in each mode. The palette (`--lex-*`) is in `docs/palette.md`. A value that starts with `var(` uses another variable.", "",
           "The tables come from the source. Run `python3 scripts/make_docs.py --write` to make them again.", ""]
    for title, _, why in AREAS + [("Other", (), "Variables that fit no other area.")]:
        names = sorted(n for n in rows if area_of(n) == title)
        if not names:
            continue
        out += [f"## {title}", "", why, "", "| Variable | Light | Dark | Set in |", "|---|---|---|---|"]
        for name in names:
            light_value, dark_value, where = rows[name]
            out.append(f"| `{name}` | `{light_value}` | `{dark_value}` | {where} |")
        out.append("")
    return "\n".join(out)


def documents(root=ROOT):
    return {root / "docs" / "palette.md": palette_doc(root), root / "docs" / "variables.md": variables_doc(root)}


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
