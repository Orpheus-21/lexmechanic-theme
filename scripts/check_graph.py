#!/usr/bin/env python3
"""Check the effective colors of the graph view.

Usage:
  python3 scripts/check_graph.py              print a report, exit 1 if a hook is too low
  python3 scripts/check_graph.py --markdown   print the report as Markdown tables
  python3 scripts/check_graph.py --json       print the report as JSON
  python3 scripts/check_graph.py --write      write the tables into docs/contrast.md
  python3 scripts/check_graph.py --preset FILE  check the theme with a preset snippet on top

Obsidian draws the graph with PixiJS. It reads its colors from hidden elements,
div.graph-view.color-fill and ten more, and takes `color` and `opacity` of each.
The final alpha is the opacity times the color alpha. This script loads Obsidian's
app.css and the theme in headless Chromium, reads the same elements in both modes, lays
each color over the page color, and checks the contrast. It also checks that the node
types differ in lightness. It needs Chromium and an installed Obsidian.
"""
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import browser  # noqa: E402
import colors  # noqa: E402
from check_contrast import blend, ratio  # noqa: E402

DOC = browser.ROOT / "docs" / "contrast.md"
START, END = "<!-- graph:start -->", "<!-- graph:end -->"

# (hook, what it draws, minimum contrast on the page)
HOOKS = [
    ("fill", "resolved node", 3.0), ("fill-focused", "focused node", 3.0), ("fill-tag", "tag node", 3.0),
    ("fill-attachment", "attachment node", 3.0), ("fill-unresolved", "unresolved node", 3.0),
    ("arrow", "arrow", 3.0), ("circle", "focus ring", 3.0), ("line", "line", 1.5), ("text", "label text", 4.5),
    ("fill-highlight", "hover highlight of a node", 3.0), ("line-highlight", "hover highlight of a line", 3.0),
]
# Pairs of hooks that must differ in lightness by at least MIN_DL (CIE L*).
DISTINCT = [
    ("fill", "fill-unresolved"), ("fill", "fill-attachment"), ("fill", "fill-tag"), ("fill-tag", "fill-focused"),
    ("fill-attachment", "fill-unresolved"), ("fill-focused", "fill-highlight"),
]
MIN_DL = 10.0
# Results below the minimum that the author knows about. The value is the issue that will fix it.
KNOWN = {}

SCRIPT = """
const hooks = %s;
const canvas = document.createElement('canvas'); canvas.width = canvas.height = 1;
const ctx = canvas.getContext('2d', {willReadFrequently: true});
const rgba = (css) => { ctx.clearRect(0, 0, 1, 1); ctx.fillStyle = '#000'; ctx.fillStyle = css; ctx.fillRect(0, 0, 1, 1); return Array.from(ctx.getImageData(0, 0, 1, 1).data); };
const result = {};
for (const hook of hooks) {
  const div = document.body.appendChild(document.createElement('div'));
  div.className = 'graph-view color-' + hook;
  const style = getComputedStyle(div);
  result[hook] = {color: rgba(style.color), opacity: parseFloat(style.opacity)};
  div.remove();
}
const probe = document.body.appendChild(document.createElement('div'));
probe.style.backgroundColor = 'var(--background-primary)';
result.page = rgba(getComputedStyle(probe).backgroundColor);
document.getElementById('out').textContent = JSON.stringify(result);
"""


def hexa(rgb):
    return "#%02x%02x%02x" % tuple(rgb[:3])


def effective(color, opacity, page):
    """Lay the node color, with its alpha times the opacity, over the page color (hex)."""
    return blend(hexa(color), page, color[3] / 255 * opacity)


def read(mode, sheets):
    raw = browser.run(browser.page(mode, sheets, "", SCRIPT % json.dumps([h[0] for h in HOOKS])))
    page = hexa(raw["page"])
    rows = []
    for hook, label, minimum in HOOKS:
        eff = effective(raw[hook]["color"], raw[hook]["opacity"], page)
        alpha = raw[hook]["color"][3] / 255 * raw[hook]["opacity"]
        r = ratio(eff, page)
        status = "ok" if r >= minimum else ("known" if (mode, hook) in KNOWN else "fail")
        rows.append({"hook": hook, "label": label, "color": hexa(raw[hook]["color"]), "alpha": round(alpha, 3),
                     "effective": eff, "ratio": r, "minimum": minimum, "status": status, "ref": KNOWN.get((mode, hook), "")})
    by = {r["hook"]: r for r in rows}
    pairs = []
    for a, b in DISTINCT:
        d = abs(colors.lightness(by[a]["effective"]) - colors.lightness(by[b]["effective"]))
        status = "ok" if d >= MIN_DL else ("known" if (mode, a, b) in KNOWN else "fail")
        pairs.append({"a": a, "b": b, "delta": d, "minimum": MIN_DL, "status": status, "ref": KNOWN.get((mode, a, b), "")})
    return {"page": page, "rows": rows, "pairs": pairs}


def collect(preset=None):
    with tempfile.TemporaryDirectory() as tmp:
        sheets = [browser.obsidian_css(tmp)] + browser.theme_files(extra=[preset] if preset else [])
        return {mode: read(mode, sheets) for mode in ("light", "dark")}


def failures(data):
    return sum(1 for m in data.values() for r in m["rows"] + m["pairs"] if r["status"] == "fail")


def note(row):
    return {"ok": "", "known": f" (known, {row['ref']})", "fail": " (FAIL)"}[row["status"]]


def markdown(data):
    out = ["## Graph view", "",
           "Obsidian reads the graph colors from hidden `.graph-view.color-*` elements. The final alpha is the opacity times the color alpha. The ratio is the contrast of the effective color on the page color.", ""]
    for mode, m in data.items():
        out += [f"### {mode.capitalize()} mode", "", "| Hook | Draws | Color | Alpha | Needs | Ratio |", "|---|---|---|---|---|---|"]
        for r in m["rows"]:
            out.append(f"| `color-{r['hook']}` | {r['label']} | `{r['color']}` | {r['alpha']:g} | {r['minimum']:g} to 1 | {r['ratio']:.2f} to 1{note(r)} |")
        out += ["", f"Node types must differ in lightness (CIE L*) by at least {MIN_DL:g}:", "", "| Pair | Difference |", "|---|---|"]
        for p in m["pairs"]:
            out.append(f"| `{p['a']}` and `{p['b']}` | {p['delta']:.1f}{note(p)} |")
        out.append("")
    return "\n".join(out)


def report(data):
    out = []
    for mode, m in data.items():
        out.append(f"{mode} mode (page {m['page']})")
        for r in m["rows"]:
            out.append(f"  {r['status'] if r['status'] != 'ok' else 'ok':5} color-{r['hook']:16} {r['label']:26} alpha {r['alpha']:4.2f}  {r['ratio']:5.2f}  needs {r['minimum']:g}{note(r)}")
        for p in m["pairs"]:
            out.append(f"  {p['status'] if p['status'] != 'ok' else 'ok':5} lightness {p['a']} / {p['b']}: {p['delta']:.1f} (needs {p['minimum']:g}){note(p)}")
    out.append(f"{failures(data)} new result(s) below the minimum")
    return "\n".join(out)


def write_doc(data):
    text = DOC.read_text()
    section = f"{START}\n{markdown(data).rstrip()}\n{END}"
    if START in text:
        head, rest = text.split(START, 1)
        text = head + section + rest.split(END, 1)[1]
    else:
        text = text.rstrip("\n") + "\n\n" + section + "\n"
    DOC.write_text(text)


def main():
    args = sys.argv[1:]
    data = collect(args[args.index("--preset") + 1] if "--preset" in args else None)
    if "--json" in args:
        print(json.dumps(data, indent=1))
    elif "--markdown" in args:
        print(markdown(data))
    elif "--write" in args:
        write_doc(data)
        print(f"wrote the graph section of {DOC.relative_to(browser.ROOT)}")
    else:
        print(report(data))
    return 1 if failures(data) else 0


if __name__ == "__main__":
    sys.exit(main())
