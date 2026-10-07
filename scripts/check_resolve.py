#!/usr/bin/env python3
"""Check that every variable of the theme resolves in headless Chromium.

Usage:
  python3 scripts/check_resolve.py

The script loads Obsidian's app.css, theme.css, and the snippets, in light mode and in
dark mode. It reads each variable that the theme sets. A variable with an empty value
is not valid. A typo in a var() name makes it so. The script exits with 1 when it finds
one. It needs Chromium and an installed Obsidian.
"""
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import browser  # noqa: E402
from check_variables import theme_variables  # noqa: E402

SCRIPT = """
const names = %s;
const style = getComputedStyle(document.body);
const result = {};
for (const name of names) result[name] = style.getPropertyValue(name).trim();
document.getElementById('out').textContent = JSON.stringify(result);
"""


def main():
    names = sorted(theme_variables())
    bad = 0
    with tempfile.TemporaryDirectory() as tmp:
        sheets = [browser.obsidian_css(tmp)] + browser.theme_files()
        for mode in ("light", "dark"):
            values = browser.run(browser.page(mode, sheets, "", SCRIPT % json.dumps(names)))
            empty = [n for n in names if values[n] == ""]
            print(f"{mode}: {len(names)} variables, {len(empty)} empty")
            for n in empty:
                print(f"  {n}")
            bad += len(empty)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
