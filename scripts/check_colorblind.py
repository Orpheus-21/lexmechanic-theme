#!/usr/bin/env python3
"""List pairs of theme colors that look alike to a person with color blindness.

Usage:
  python3 scripts/check_colorblind.py            check the callout colors (the eight base colors)
  python3 scripts/check_colorblind.py --graph    also check the graph node types (needs Chromium)
  python3 scripts/check_colorblind.py --json     print the result as JSON

For each pair the script computes the CIEDE2000 distance with normal vision and with a
simulation of protanopia, deuteranopia, and tritanopia. A pair is too close when the
smallest distance is below 10. Callouts have an icon and a title, so a close pair of
callout colors is a note, not a failure. The script exits with 1 only for a graph pair
that is not listed in KNOWN. It uses only the Python standard library, and
--graph also needs headless Chromium and an installed Obsidian.
"""
import itertools
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import colors  # noqa: E402
from check_contrast import ROOT, read_blocks, resolve, shared_block  # noqa: E402

MIN_DE = 10.0
BASE = ["red", "orange", "yellow", "green", "cyan", "blue", "purple", "pink"]
# Graph pairs below MIN_DE that the author knows about. The value is the issue that owns it.
KNOWN = {
    ("graph node types", "light", "focused", "tag"): "#252",
    ("graph node types", "dark", "focused", "tag"): "#252",
    ("graph node types", "dark", "tag", "attachment"): "#259",
}


def distance(a, b):
    """Return (smallest distance, kind of vision where it happens) for two colors."""
    options = {"normal": colors.delta_e(a, b)}
    for kind in colors.CVD:
        options[kind] = colors.delta_e(colors.simulate(a, kind), colors.simulate(b, kind))
    kind = min(options, key=options.get)
    return options[kind], kind


def close_pairs(named):
    """named: {name: '#rrggbb'}. Return the rows for all pairs, sorted by distance."""
    rows = []
    for (n1, c1), (n2, c2) in itertools.combinations(named.items(), 2):
        d, kind = distance(c1, c2)
        rows.append({"a": n1, "b": n2, "distance": d, "kind": kind, "close": d < MIN_DE})
    return sorted(rows, key=lambda r: r["distance"])


def callout_colors():
    css = (ROOT / "theme.css").read_text()
    shared = shared_block(css)
    return {mode: {n: resolve(f"--color-{n}", {**shared, **own}) for n in BASE} for mode, own in read_blocks(css).items()}


def graph_colors():
    import check_graph
    data = check_graph.collect()
    keep = {"fill": "resolved", "fill-unresolved": "unresolved", "fill-tag": "tag", "fill-attachment": "attachment", "fill-focused": "focused"}
    return {mode: {keep[r["hook"]]: r["effective"] for r in m["rows"] if r["hook"] in keep} for mode, m in data.items()}


def main():
    sets = {"callout colors": callout_colors()}
    if "--graph" in sys.argv:
        sets["graph node types"] = graph_colors()
    result, bad = {}, 0
    for title, modes in sets.items():
        for mode, named in modes.items():
            rows = close_pairs(named)
            for r in rows:
                r["known"] = KNOWN.get((title, mode, r["a"], r["b"]), "")
                if r["close"] and title == "graph node types" and not r["known"]:
                    bad += 1
            result[f"{title}, {mode}"] = rows
    if "--json" in sys.argv:
        print(json.dumps(result, indent=1))
    else:
        for name, rows in result.items():
            close = [r for r in rows if r["close"]]
            print(f"{name}: {len(close)} close pair(s) of {len(rows)}")
            for r in close:
                tag = f" (known, {r['known']})" if r["known"] else ""
                print(f"  {r['a']} / {r['b']}: {r['distance']:.1f} with {r['kind']}{tag}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
