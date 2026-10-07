#!/usr/bin/env python3
"""List the variables that the theme sets and Obsidian does not use.

Usage:
  python3 scripts/check_variables.py               use the app.css of the installed Obsidian
  python3 scripts/check_variables.py --css FILE    use a given app.css

The script reads theme.css and the snippets. It skips the `--lex-*` palette. A
variable is fine when app.css defines it or reads it with var(). Obsidian 1.14.4
removed --text-highlight-bg-rgb, and the theme went on to set it without effect.
The script also checks the graph: app.css must have the 11 hook classes that the graph
reads (.graph-view.color-fill and ten more) and define the eight --graph-* variables.
A new Obsidian version can rename them, and the theme would lose its graph colors
without a warning. The script exits with 1 when it finds a problem. It uses only the
standard library.
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from extract_obsidian_css import find_asar, read_file  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
GRAPH_HOOKS = ["fill", "fill-focused", "fill-tag", "fill-attachment", "fill-unresolved", "arrow", "circle",
               "line", "text", "fill-highlight", "line-highlight"]
GRAPH_VARIABLES = ["--graph-controls-width", "--graph-text", "--graph-line", "--graph-node", "--graph-node-unresolved",
                   "--graph-node-focused", "--graph-node-tag", "--graph-node-attachment"]
DATA_URI = re.compile(r"url\('data:[^']*'\)")


def theme_variables(root=ROOT):
    """Return the custom properties that the theme and the snippets declare."""
    text = DATA_URI.sub("", (root / "theme.css").read_text())
    for snippet in sorted((root / "snippets").glob("*.css")):
        text += snippet.read_text()
    names = set(re.findall(r"(--[a-z0-9-]+)\s*:", text))
    return {n for n in names if not n.startswith("--lex-")}


def obsidian_variables(css):
    """Return the custom properties that app.css defines or reads."""
    return set(re.findall(r"(--[a-z0-9-]+)\s*:", css)) | set(re.findall(r"var\(\s*(--[a-z0-9-]+)", css))


def unused(theme_names, css):
    return sorted(theme_names - obsidian_variables(css))


def graph_problems(css):
    """Return the graph hook classes and variables that app.css lacks."""
    defined = set(re.findall(r"(--[a-z0-9-]+)\s*:", css))
    missing = [f".graph-view.color-{h}" for h in GRAPH_HOOKS if not re.search(r"\.graph-view\.color-%s\s*[{,]" % re.escape(h), css)]
    return missing + [v for v in GRAPH_VARIABLES if v not in defined]


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--css", type=Path)
    args = parser.parse_args()
    css = args.css.read_text() if args.css else read_file(find_asar(), "app.css").decode()
    names = theme_variables()
    missing = unused(names, css)
    print(f"{len(names)} variables set by the theme, {len(missing)} not used by Obsidian")
    for name in missing:
        print(f"  {name}")
    lost = graph_problems(css)
    print(f"graph: {len(GRAPH_HOOKS)} hook classes and {len(GRAPH_VARIABLES)} variables, {len(lost)} missing in app.css")
    for name in lost:
        print(f"  {name}")
    return 1 if missing or lost else 0


if __name__ == "__main__":
    sys.exit(main())
