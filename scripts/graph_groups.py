#!/usr/bin/env python3
"""Print the colorGroups of a graph.json with colors of the palette.

Usage:
  python3 scripts/graph_groups.py [--mode light|dark] 'tag:#book=red' 'path:Projects=blue' ...
  python3 scripts/graph_groups.py --list [--mode light|dark]

Each argument is QUERY=COLOR. QUERY is a search query of the graph, such as `tag:#book`.
COLOR is the name of a palette color (red, orange, yellow, green, cyan, blue, purple, pink,
accent, ink, muted, faint, sand, and the others of docs/palette.md) or a #rrggbb value.
The script prints a JSON list for the colorGroups key of .obsidian/graph.json. Obsidian
saves a color as one integer: red times 65536, plus green times 256, plus blue. The script
does not read or write a vault. It uses only the Python standard library.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_contrast import resolve  # noqa: E402
from make_docs import modes  # noqa: E402


def to_int(hex_color):
    """Return the integer that Obsidian saves for a #rrggbb color."""
    return int(hex_color[1:], 16)


def palette(mode):
    light, dark = modes()
    values = light if mode == "light" else dark
    names = {}
    for name in values:
        if name.startswith("--lex-") and (color := resolve(name, values)):
            names[name[len("--lex-"):]] = color
    return names


def group(spec, colors):
    """Turn 'QUERY=COLOR' into a colorGroups entry."""
    query, sep, color = spec.rpartition("=")
    if not sep or not query:
        raise ValueError(f"{spec!r} is not QUERY=COLOR")
    if color.startswith("#") and len(color) == 7:
        value = color.lower()
    elif color in colors:
        value = colors[color]
    else:
        raise ValueError(f"unknown color {color!r}. Use --list to see the names.")
    return {"query": query, "color": {"a": 1, "rgb": to_int(value)}}


def main(argv):
    mode = argv[argv.index("--mode") + 1] if "--mode" in argv else "light"
    rest = [a for i, a in enumerate(argv) if a != "--mode" and (i == 0 or argv[i - 1] != "--mode")]
    colors = palette(mode)
    if "--list" in rest:
        for name, value in colors.items():
            print(f"{name:18} {value}  {to_int(value)}")
        return 0
    specs = [a for a in rest if not a.startswith("--")]
    if not specs:
        print(__doc__)
        return 2
    try:
        print(json.dumps([group(s, colors) for s in specs], indent=2))
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
