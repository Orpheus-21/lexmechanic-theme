#!/usr/bin/env python3
"""Check that the real graph draws the node colors that the theme sets.

Usage:
  python3 scripts/obsidian_window.py start         start a temporary window first
  python3 scripts/check_graph_pixels.py [--dir DIR]
  python3 scripts/obsidian_window.py stop --clean

The script opens a new graph view in the temporary window with tags and attachments on and with no
color groups, waits until the nodes have taken their colors, and takes a screenshot. For each node type
(resolved, tag, attachment, unresolved) it picks a node that no other node or panel covers, reads the
pixel at its center, and compares it with the color that Obsidian read from the theme for that type.
The check fails when a pixel differs by more than 3 in a channel, or when Obsidian draws a node with
another alpha than the hook has. A hook with an alpha below 1 is laid over the page color first. The
check proves that the theme reaches the real graph. The contrast of the colors is checked by
check_graph.py. It needs a running window and Node 22, and it uses only the Python standard library.
"""
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import obsidian_window as w  # noqa: E402
from check_screenshots import read_png  # noqa: E402

TOLERANCE = 3
HOOKS = {"resolved": "fill", "tag": "fillTag", "attachment": "fillAttachment", "unresolved": "fillUnresolved"}

BODY = """
await send('Emulation.setDeviceMetricsOverride', { width: 1400, height: 900, deviceScaleFactor: 1, mobile: false });
await sleep(500);
await ev(`(async () => {
  app.workspace.detachLeavesOfType('graph');
  const leaf = app.workspace.getLeaf(true);
  await leaf.setViewState({type: 'graph', state: {}, active: true});
  leaf.view.dataEngine.setOptions({colorGroups: [], showTags: true, showAttachments: true, search: '', showArrow: false});
  return 0;
})()`);
await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: 5, y: 5 });
await sleep(2000);
// zoom out, so that the whole graph is on the screen and every node type has free nodes
await ev(`(() => { const r = app.workspace.activeLeaf.view.renderer; r.setScale(0.45); r.targetScale = 0.45; return 0; })()`);
const snap = `(() => {
  const r = app.workspace.activeLeaf.view.renderer;
  const canvas = document.querySelector('.graph-view canvas, .view-content canvas').getBoundingClientRect();
  const panel = document.querySelector('.graph-controls').getBoundingClientRect();
  const hex = o => '#' + o.rgb.toString(16).padStart(6, '0');
  const nodes = r.nodes.filter(n => n.circle).map(n => {
    const b = n.circle.getBounds();
    return {id: n.id, type: n.type || 'resolved', x: b.x + b.width / 2 + canvas.left, y: b.y + b.height / 2 + canvas.top, radius: b.width / 2, alpha: n.circle.alpha, tint: '#' + n.circle.tint.toString(16).padStart(6, '0')};
  });
  const hooks = Object.fromEntries(Object.entries(r.colors).map(([k, v]) => [k, {color: hex(v), alpha: v.a}]));
  return JSON.stringify({nodes, hooks, page: getComputedStyle(document.body).getPropertyValue('--background-primary').trim(), panel: [panel.left, panel.top, panel.right, panel.bottom], canvas: [canvas.left, canvas.top, canvas.right, canvas.bottom]});
})()`;
// the layout moves and the nodes fade for some seconds: wait until two snapshots are the same
let before = JSON.parse(await ev(snap));
for (let i = 0; i < 60; i++) {
  await sleep(1000);
  const now = JSON.parse(await ev(snap));
  const old = Object.fromEntries(before.nodes.map(n => [n.id, n]));
  const still = now.nodes.length > 0 && now.nodes.length === before.nodes.length && now.nodes.every(n => old[n.id] && Math.abs(n.x - old[n.id].x) < 0.3 && Math.abs(n.y - old[n.id].y) < 0.3 && Math.abs(n.alpha - old[n.id].alpha) < 0.005);
  before = now;
  if (still && i > 4) break;
}
await shot(%s);
const after = JSON.parse(await ev(snap));
const was = Object.fromEntries(before.nodes.map(n => [n.id, n]));
after.nodes = after.nodes.filter(n => was[n.id] && Math.abs(n.x - was[n.id].x) < 0.5 && Math.abs(n.y - was[n.id].y) < 0.5 && Math.abs(n.alpha - was[n.id].alpha) < 0.005);
console.log(JSON.stringify(after));
"""


def pick(nodes, panel, canvas, alphas=None):
    """Return one node of each type that no other node or the panel covers, and that lies inside the canvas.
    With alphas ({type: alpha of the hook}) a node that is still fading, or dimmed by the highlight of another
    node, is skipped. The check needs a node that has reached its final alpha."""
    chosen = {}
    for node in nodes:
        if alphas and abs(node["alpha"] - alphas.get(node["type"], node["alpha"])) > 0.02:
            continue
        x, y, r = node["x"], node["y"], node["radius"]
        if not (canvas[0] + 15 < x < canvas[2] - 15 and canvas[1] + 15 < y < canvas[3] - 15):
            continue
        if panel[0] - 10 < x < panel[2] + 10 and panel[1] - 10 < y < panel[3] + 10:
            continue
        if any(o is not node and abs(o["x"] - x) < r + o["radius"] and abs(o["y"] - y) < r + o["radius"] for o in nodes):
            continue
        chosen.setdefault(node["type"], node)
    return chosen


def hex_to_rgb(color):
    return [int(color[i:i + 2], 16) for i in (1, 3, 5)]


def pixel(rows, bpp, x, y):
    row = rows[int(round(y))]
    i = int(round(x)) * bpp
    return list(row[i:i + 3])


def main():
    args = sys.argv[1:]
    directory = args[args.index("--dir") + 1] if "--dir" in args else str(w.DEFAULT_DIR)
    state = w.need_state({"--dir": directory})
    with tempfile.TemporaryDirectory() as tmp:
        png = Path(tmp) / "graph.png"
        out = w.js(directory, state["port"], BODY % json.dumps(str(png)))
        data = json.loads(out.strip().splitlines()[-1])
        width, height, bpp, rows = read_png(png.read_bytes())
    chosen = pick(data["nodes"], data["panel"], data["canvas"], {kind: data["hooks"][hook]["alpha"] for kind, hook in HOOKS.items()})
    failed = 0
    for kind, hook in HOOKS.items():
        node, expected = chosen.get(kind), data["hooks"][hook]
        if node is None:
            print(f"{kind}: no free node to sample")
            failed += 1
            continue
        got = pixel(rows, bpp, node["x"], node["y"])
        want = hex_to_rgb(expected["color"])
        # the theme sets the alpha of the hook, and Obsidian draws it
        page = hex_to_rgb(data["page"]) if data["page"].startswith("#") else [255, 255, 255]
        alpha = expected["alpha"]
        diff = max(abs(a - round(c * alpha + p * (1 - alpha))) for a, c, p in zip(got, want, page))
        alpha_ok = abs(node["alpha"] - expected["alpha"]) < 0.02
        ok = diff <= TOLERANCE and alpha_ok
        failed += not ok
        print(f"{kind:10} hook {expected['color']} alpha {expected['alpha']:.2f} | node alpha {node['alpha']:.2f} | pixel {'#%02x%02x%02x' % tuple(got)} | {'ok' if ok else 'FAIL'}")
    print(f"{failed} problem(s)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
