#!/usr/bin/env python3
"""Find a property that is set twice in one CSS block.

Usage:
  python3 scripts/check_duplicates.py              check src/*.css and snippets/*.css
  python3 scripts/check_duplicates.py FILE ...     check the given files

The second declaration hides the first one, and nothing warns about it. The script
reads each block, and lists the properties and variables that occur twice. It exits
with 1 when it finds one. It uses only the Python standard library.
"""
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def clean(text):
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    return re.sub(r"url\('data:[^']*'\)", "url()", text)


def duplicates(text):
    """Return a list of (selector, property, count) for properties set twice in one block."""
    found = []
    for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", clean(text)):
        names = re.findall(r"(?:^|;)\s*([a-zA-Z-]+|--[a-zA-Z0-9-]+)\s*:", m.group(2))
        for name, count in Counter(names).items():
            if count > 1:
                found.append((" ".join(m.group(1).split())[:60], name, count))
    return found


def main():
    paths = [Path(a) for a in sys.argv[1:]] or sorted((ROOT / "src").glob("*.css")) + sorted((ROOT / "snippets").glob("*.css"))
    total = 0
    for path in paths:
        for selector, name, count in duplicates(path.read_text()):
            print(f"{path}: {name} is set {count} times in {selector}")
            total += 1
    print(f"{total} duplicate(s)" if total else f"no duplicate in {len(paths)} file(s)")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
