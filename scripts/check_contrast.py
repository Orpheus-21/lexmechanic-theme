#!/usr/bin/env python3
"""Check the contrast of the text colors in theme.css.

Usage:
  python3 scripts/check_contrast.py             print a report, exit 1 if a pair is too low
  python3 scripts/check_contrast.py --markdown  print the report as Markdown tables

The script reads the .theme-light and .theme-dark blocks, resolves var()
references, and compares each text color with each background color.
It uses only the Python standard library.
"""
import re
import sys
from pathlib import Path

MIN = 4.5

# Pairs below MIN that the author knows about. Each one has an open issue.
# The script reports them as known and does not fail for them.
KNOWN = {
    ("dark", "--text-accent", "--background-secondary-alt"): "#74",
    ("dark", "--code-keyword", "--background-secondary-alt"): "#74",
    ("dark", "--code-tag", "--background-secondary-alt"): "#74",
}
ROOT = Path(__file__).resolve().parent.parent

BACKGROUNDS = ["--background-primary", "--background-secondary", "--background-secondary-alt"]
TEXT = [
    "--text-normal", "--text-muted", "--text-faint", "--text-accent",
    "--text-error", "--text-warning", "--text-success", "--link-unresolved-color",
    "--code-comment", "--code-function", "--code-important", "--code-keyword",
    "--code-operator", "--code-property", "--code-punctuation", "--code-string",
    "--code-tag", "--code-value",
    "--color-red", "--color-orange", "--color-yellow", "--color-green",
    "--color-cyan", "--color-blue", "--color-purple", "--color-pink",
]


def read_blocks(css):
    css = re.sub(r"url\('data:[^']*'\)", "", css)
    blocks = {}
    for mode in ("light", "dark"):
        m = re.search(r"^\.theme-%s \{\n(.*?)\n\}" % mode, css, re.S | re.M)
        blocks[mode] = dict(re.findall(r"^\s*(--[a-z0-9-]+):\s*(.+?);\s*$", m.group(1), re.M))
    return blocks


def resolve(name, values, seen=()):
    value = values.get(name)
    if value is None or name in seen:
        return None
    ref = re.fullmatch(r"var\((--[a-z0-9-]+)\)", value.strip())
    if ref:
        return resolve(ref.group(1), values, seen + (name,))
    return value.strip() if re.fullmatch(r"#[0-9a-fA-F]{6}", value.strip()) else None


def luminance(hex_color):
    channels = [int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    channels = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]


def ratio(a, b):
    hi, lo = sorted((luminance(a), luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def main():
    markdown = "--markdown" in sys.argv
    blocks = read_blocks((ROOT / "theme.css").read_text())
    failures = 0
    for mode, values in blocks.items():
        backgrounds = {b: resolve(b, values) for b in BACKGROUNDS}
        rows = []
        for name in TEXT:
            color = resolve(name, values)
            if color is None:
                continue
            ratios = [ratio(color, bg) for bg in backgrounds.values()]
            notes = []
            for bg_name, r in zip(backgrounds, ratios):
                if r >= MIN:
                    notes.append("")
                elif (mode, name, bg_name) in KNOWN:
                    notes.append(f" (known, {KNOWN[(mode, name, bg_name)]})")
                else:
                    notes.append(" (FAIL)")
                    failures += 1
            rows.append((name, color, ratios, notes))
        on_accent = (resolve("--text-on-accent", values), resolve("--interactive-accent", values))
        if None not in on_accent:
            r = ratio(*on_accent)
            failures += r < MIN
            rows.append(("--text-on-accent (on --interactive-accent)", on_accent[0], [r], ["" if r >= MIN else " (FAIL)"]))
        if markdown:
            print(f"## {mode.capitalize()} mode\n")
            print("| Text color | Value | On page | On panel | On alt panel |")
            print("|---|---|---|---|---|")
            for name, color, ratios, notes in rows:
                cells = " | ".join(f"{r:.2f} to 1{n}" for r, n in zip(ratios, notes))
                print(f"| `{name}` | `{color}` | {cells} |" + (" | |" if len(ratios) == 1 else ""))
            print()
        else:
            print(f"{mode} mode (page {backgrounds['--background-primary']})")
            for name, color, ratios, notes in rows:
                flag = "FAIL" if " (FAIL)" in notes else ("known" if any(notes) else "ok  ")
                print(f"  {flag:5} {name:44} {color}  " + "  ".join(f"{r:5.2f}" for r in ratios))
    if not markdown:
        print(f"{failures} new pair(s) below {MIN} to 1")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
