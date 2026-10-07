#!/usr/bin/env python3
"""Take the screenshots of the docs in the temporary Obsidian window.

Usage:
  python3 scripts/obsidian_window.py start          start a temporary window first
  python3 scripts/take_screenshots.py [--out DIR] [--dir WINDOWDIR]
  python3 scripts/obsidian_window.py stop --clean

The script makes seven images in DIR (default docs/images): the Showcase note in reading view in light and
dark mode, the note in Live Preview in light mode, the graph view in both modes, and the note on a phone
(Obsidian's mobile emulation, 390 by 844 at twice the pixel density) in both modes. The window shows the
demo vault, so the images hold no personal data. A new run gives the same images up to the layout of the
graph, which Obsidian draws from a random start. It needs Node 22 and a running window, and it uses only the
Python standard library.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import obsidian_window as w  # noqa: E402

THEMES = {"light": "moonstone", "dark": "obsidian"}

SETUP = """
const open = (mode) => ev(`(async () => { await app.workspace.getLeaf(false).setViewState({type: 'markdown', state: {file: 'Showcase.md', mode: '${mode}', source: false}, active: true}); return 0; })()`);
const scroll = (y) => ev(`(() => { const p = document.querySelector('.markdown-preview-view'); if (p) p.scrollTop = ${y}; return 0; })()`);
const settle = async () => {
  await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: 5, y: 5 });
  await ev(`(() => { const r = app.workspace.activeLeaf.view.renderer; r.setScale(0.6); r.targetScale = 0.6; return 0; })()`);
  await sleep(7000);
};
const graph = () => ev(`(async () => {
  app.workspace.detachLeavesOfType('graph');
  const leaf = app.workspace.getLeaf(true);
  await leaf.setViewState({type: 'graph', state: {}, active: true});
  leaf.view.dataEngine.setOptions({colorGroups: [], showTags: true, showAttachments: true, search: ''});
  return 0;
})()`);
const out = %s;
const theme = async (name) => { await ev(`app.changeTheme('${name}'); 0`); await sleep(800); };
const desktop = () => send('Emulation.setDeviceMetricsOverride', { width: 1280, height: 800, deviceScaleFactor: 1, mobile: false });
await ev(`app.emulateMobile(false); 0`);
await desktop(); await sleep(800);
for (const [mode, name] of [['light', 'moonstone'], ['dark', 'obsidian']]) {
  await theme(name);
  await open('preview'); await sleep(1500); await shot(out + `/reading-${mode}.png`);
  if (mode === 'light') { await open('source'); await sleep(1500); await shot(out + '/live-preview-light.png'); }
  await graph(); await settle(); await shot(out + `/graph-${mode}.png`);
  await ev(`(async () => { app.workspace.detachLeavesOfType('graph'); return 0; })()`);
}
await ev(`app.emulateMobile(true); 0`); await sleep(2500);
for (const [mode, name] of [['light', 'moonstone'], ['dark', 'obsidian']]) {
  await theme(name);
  await send('Emulation.setDeviceMetricsOverride', { width: 390, height: 844, deviceScaleFactor: 2, mobile: true });
  await sleep(1200); await open('preview'); await sleep(2000); await shot(out + `/mobile-${mode}.png`);
}
await ev(`app.emulateMobile(false); app.changeTheme('moonstone'); 0`);
await send('Emulation.clearDeviceMetricsOverride');
"""


def main():
    args = sys.argv[1:]
    out = Path(args[args.index("--out") + 1]) if "--out" in args else w.ROOT / "docs" / "images"
    directory = args[args.index("--dir") + 1] if "--dir" in args else str(w.DEFAULT_DIR)
    state = w.need_state({"--dir": directory})
    out.mkdir(parents=True, exist_ok=True)
    w.js(directory, state["port"], SETUP % json.dumps(str(out.resolve())))
    for f in sorted(out.glob("*.png")):
        print(f"{f.relative_to(w.ROOT) if f.is_relative_to(w.ROOT) else f}  {f.stat().st_size // 1024} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
