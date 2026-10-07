#!/usr/bin/env python3
"""List the variables that two versions of Obsidian's app.css add and remove.

Usage:
  python3 scripts/diff_obsidian_variables.py OLD.css NEW.css

Get the files with scripts/extract_obsidian_css.py. The script groups the names by the
first word after the dashes, and marks the variables that the theme sets. It uses only the Python
standard library.
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_variables import theme_variables  # noqa: E402


def defined(css):
    return set(re.findall(r"(--[a-z0-9-]+)\s*:", css))


def group(names):
    groups = defaultdict(list)
    for name in sorted(names):
        groups["--" + name[2:].split("-")[0]].append(name)
    return groups


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    old, new = (defined(Path(p).read_text()) for p in argv)
    mine = theme_variables()
    for title, names in (("Removed", old - new), ("Added", new - old)):
        print(f"{title}: {len(names)}")
        for key, items in group(names).items():
            marked = [n + (" (set by the theme)" if n in mine else "") for n in items]
            print(f"  {key}: " + ", ".join(m[2:] for m in marked))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
