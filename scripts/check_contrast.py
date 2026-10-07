#!/usr/bin/env python3
"""Check the contrast of the colors in theme.css.

Usage:
  python3 scripts/check_contrast.py              print a report, exit 1 if a pair is too low
  python3 scripts/check_contrast.py --markdown   print the report as Markdown tables
  python3 scripts/check_contrast.py --json       print the report as JSON
  python3 scripts/check_contrast.py --write      write the tables into docs/contrast.md
  python3 scripts/check_contrast.py --check-doc  exit 1 if docs/contrast.md is out of date

The script reads the .theme-light and .theme-dark blocks, resolves var() references,
and compares colors. Text colors must reach 4.5 to 1 on the page, panel, and alt panel
colors. Other pairs, such as the focus ring, must reach 3 to 1. A color of the form
color-mix(in srgb, COLOR N%, transparent) is laid over the page color first.
It uses only the Python standard library.
"""
import json
import re
import sys
from pathlib import Path

TEXT_MIN = 4.5
UI_MIN = 3.0
ROOT = Path(__file__).resolve().parent.parent
DOC = ROOT / "docs" / "contrast.md"
START, END = "<!-- contrast:start -->", "<!-- contrast:end -->"

# Pairs below their minimum that the author decided to keep. The value tells where the decision is.
KNOWN = {
    ("dark", "--text-accent", "--background-secondary-alt"): "#74",
    ("dark", "--code-keyword", "--background-secondary-alt"): "#74",
    ("dark", "--code-tag", "--background-secondary-alt"): "#74",
    ("light", "--background-modifier-border", "--background-primary"): "#314",
    ("dark", "--background-modifier-border", "--background-primary"): "#314",
}

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
# (label, foreground, background, minimum): "selection" is the selected text on the selection color
PAIRS = [
    ("--text-on-accent on --interactive-accent", "--text-on-accent", "--interactive-accent", TEXT_MIN),
    ("--text-normal on the selection color", "--text-normal", "selection", TEXT_MIN),
    ("--interactive-accent on the page", "--interactive-accent", "--background-primary", UI_MIN),
    ("--checkbox-color on the page", "--checkbox-color", "--background-primary", UI_MIN),
    ("--background-modifier-border-focus on the page", "--background-modifier-border-focus", "--background-primary", UI_MIN),
    ("--background-modifier-border-hover on the page", "--background-modifier-border-hover", "--background-primary", UI_MIN),
    ("--toggle-thumb-color on --interactive-accent", "--toggle-thumb-color", "--interactive-accent", UI_MIN),
    ("--background-modifier-border on the page", "--background-modifier-border", "--background-primary", UI_MIN),
]


def read_blocks(css):
    css = re.sub(r"url\('data:[^']*'\)", "", css)
    blocks = {}
    for mode in ("light", "dark"):
        m = re.search(r"^\.theme-%s \{\n(.*?)\n\}" % mode, css, re.S | re.M)
        blocks[mode] = dict(re.findall(r"^\s*(--[a-z0-9-]+):\s*(.+?);\s*$", m.group(1), re.M))
    return blocks


def shared_block(css):
    """Return the variables of the block that holds both modes."""
    css = re.sub(r"url\('data:[^']*'\)", "", css)
    m = re.search(r"^\.theme-dark, \.theme-light \{\n(.*?)\n\}", css, re.S | re.M)
    return dict(re.findall(r"^\s*(--[a-z0-9-]+):\s*(.+?);\s*$", m.group(1), re.M)) if m else {}


def resolve(name, values, seen=()):
    """Return the #rrggbb color of a variable, or None if it is not a solid color."""
    value = values.get(name)
    if value is None or name in seen:
        return None
    ref = re.fullmatch(r"var\((--[a-z0-9-]+)\)", value.strip())
    if ref:
        return resolve(ref.group(1), values, seen + (name,))
    return value.strip() if re.fullmatch(r"#[0-9a-fA-F]{6}", value.strip()) else None


def blend(fg, bg, alpha):
    """Lay the color fg with an alpha over the color bg. Both are #rrggbb."""
    f = [int(fg[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(bg[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(round(x * alpha + y * (1 - alpha)) for x, y in zip(f, b))


def effective(name, values, page):
    """Resolve a color, or lay a color-mix(..., N%, transparent) over the page color."""
    solid = resolve(name, values)
    if solid:
        return solid
    m = re.fullmatch(r"color-mix\(in srgb,\s*(.+?)\s+(\d+(?:\.\d+)?)%,\s*transparent\)", values.get(name, "").strip())
    if not m:
        return None
    ref = re.fullmatch(r"var\((--[a-z0-9-]+)\)", m.group(1))
    color = resolve(ref.group(1), values) if ref else (m.group(1) if re.fullmatch(r"#[0-9a-fA-F]{6}", m.group(1)) else None)
    return blend(color, page, float(m.group(2)) / 100) if color else None


def luminance(hex_color):
    channels = [int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    channels = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]


def ratio(a, b):
    hi, lo = sorted((luminance(a), luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def compute(root=ROOT):
    """Return {mode: {"text": [...], "pairs": [...]}} for theme.css. Each row has a list of failures."""
    css = (root / "theme.css").read_text()
    shared = shared_block(css)
    result = {}
    for mode, own in read_blocks(css).items():
        values = {**shared, **own}
        backgrounds = {b: resolve(b, values) for b in BACKGROUNDS}
        page = backgrounds["--background-primary"]
        text = []
        for name in TEXT:
            color = resolve(name, values)
            if color is None:
                continue
            ratios = [ratio(color, bg) for bg in backgrounds.values()]
            status = []
            for bg_name, r in zip(backgrounds, ratios):
                if r >= TEXT_MIN:
                    status.append("ok")
                else:
                    status.append("known" if (mode, name, bg_name) in KNOWN else "fail")
            refs = [KNOWN.get((mode, name, bg_name), "") for bg_name in backgrounds]
            text.append({"name": name, "value": color, "ratios": ratios, "status": status, "refs": refs})
        pairs = []
        sel = effective("--text-selection", values, page)
        for label, fg_name, bg_name, minimum in PAIRS:
            fg = effective(fg_name, values, page)
            bg = sel if bg_name == "selection" else effective(bg_name, values, page)
            if fg is None or bg is None:
                continue
            if bg_name == "selection":
                bg = sel
            r = ratio(fg, bg)
            status = "ok" if r >= minimum else ("known" if (mode, fg_name, bg_name) in KNOWN else "fail")
            pairs.append({"label": label, "foreground": fg, "background": bg, "minimum": minimum, "ratio": r,
                          "status": status, "ref": KNOWN.get((mode, fg_name, bg_name), "")})
        result[mode] = {"page": page, "backgrounds": backgrounds, "text": text, "pairs": pairs}
    return result


def failures(data):
    return sum(1 for m in data.values() for row in m["text"] for s in row["status"] if s == "fail") + \
        sum(1 for m in data.values() for p in m["pairs"] if p["status"] == "fail")


def note(status, ref=""):
    return {"ok": "", "known": f" (known, {ref})", "fail": " (FAIL)"}[status]


def markdown(data):
    out = []
    for mode, m in data.items():
        out += [f"## {mode.capitalize()} mode", "", "| Text color | Value | On page | On panel | On alt panel |", "|---|---|---|---|---|"]
        for row in m["text"]:
            cells = " | ".join(f"{r:.2f} to 1{note(s, ref)}" for r, s, ref in zip(row["ratios"], row["status"], row["refs"]))
            out.append(f"| `{row['name']}` | `{row['value']}` | {cells} |")
        out += ["", "Other pairs:", "", "| Pair | Needs | Ratio |", "|---|---|---|"]
        for p in m["pairs"]:
            out.append(f"| `{p['label']}` | {p['minimum']:g} to 1 | {p['ratio']:.2f} to 1{note(p['status'], p['ref'])} |")
        out.append("")
    return "\n".join(out)


def report(data):
    out = []
    for mode, m in data.items():
        out.append(f"{mode} mode (page {m['page']})")
        for row in m["text"]:
            flag = "FAIL" if "fail" in row["status"] else ("known" if "known" in row["status"] else "ok")
            out.append(f"  {flag:5} {row['name']:44} {row['value']}  " + "  ".join(f"{r:5.2f}" for r in row["ratios"]))
        for p in m["pairs"]:
            flag = {"ok": "ok", "known": "known", "fail": "FAIL"}[p["status"]]
            out.append(f"  {flag:5} {p['label']:44} needs {p['minimum']:g}  {p['ratio']:5.2f}")
    out.append(f"{failures(data)} new pair(s) below the minimum")
    return "\n".join(out)


def document(data):
    """Return docs/contrast.md with the tables between the markers replaced."""
    text = DOC.read_text()
    head, rest = text.split(START, 1)
    tail = rest.split(END, 1)[1]
    return f"{head}{START}\n{markdown(data).rstrip()}\n{END}{tail}"


def main():
    data = compute()
    args = sys.argv[1:]
    if "--json" in args:
        print(json.dumps(data, indent=1))
    elif "--markdown" in args:
        print(markdown(data))
    elif "--write" in args:
        DOC.write_text(document(data))
        print(f"wrote {DOC.relative_to(ROOT)}")
    elif "--check-doc" in args:
        if DOC.read_text() != document(data):
            print("docs/contrast.md is out of date. Run: python3 scripts/check_contrast.py --write")
            return 1
        print("docs/contrast.md is up to date")
    else:
        print(report(data))
    return 1 if failures(data) else 0


if __name__ == "__main__":
    sys.exit(main())
