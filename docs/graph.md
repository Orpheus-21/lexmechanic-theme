# Graph view

This page tells how the graph view gets its colors, what a theme can change, and what it cannot. The facts come from the CSS and the JavaScript of Obsidian 1.14.4.

## How the graph reads its colors

Obsidian draws the graph with PixiJS on a canvas. A node is a white circle that the code tints with a color. CSS cannot style a node like a page element.

The code reads its colors from hidden elements. It makes a `div` with the classes `graph-view` and `color-fill` (or one of ten more names), adds it to the page, and reads `color` and `opacity` from the computed style. The final alpha of a color is the opacity times the alpha of the color. The code reads the elements again when the CSS changes.

| Hook | What it draws | Where the color comes from |
|---|---|---|
| `color-fill` | Resolved nodes | `--graph-node` |
| `color-fill-focused` | The focused node | `--graph-node-focused` |
| `color-fill-tag` | Tag nodes | `--graph-node-tag` |
| `color-fill-attachment` | Attachment nodes | `--graph-node-attachment` |
| `color-fill-unresolved` | Unresolved nodes | `--graph-node-unresolved`, and Obsidian sets `opacity: 0.5` |
| `color-arrow` | Arrows | `--text-normal` at `opacity: 0.5`, with no graph variable |
| `color-circle` | The ring around the focused node | `--graph-node-focused` |
| `color-line` | Lines | `--graph-line` |
| `color-text` | Node labels | `--graph-text` |
| `color-fill-highlight` | The node under the pointer | `--interactive-accent`, with no graph variable |
| `color-line-highlight` | The lines of that node | `--interactive-accent`, with no graph variable |

Obsidian also defines `color-fill-1` to `color-fill-6` as `--text-muted` in its CSS. The code of Obsidian 1.14.4 does not read them: its list of hook names has the 11 hooks above, and the six names do not appear in the JavaScript. Setting them has no effect.

The eight documented variables are `--graph-controls-width`, `--graph-text`, `--graph-line`, `--graph-node`, `--graph-node-unresolved`, `--graph-node-focused`, `--graph-node-tag`, and `--graph-node-attachment`. The theme sets the colors from the palette. `docs/palette.md` lists them, and `docs/contrast.md` gives the effective contrast of each hook on the page color, with the opacity counted.

## What a theme cannot change

* **The label font.** The code fixes the font of the labels: `ui-sans-serif, -apple-system, BlinkMacSystemFont, system-ui, "Segoe UI", Roboto, "Inter", ...`. The theme cannot change the stack. By default the labels use the system font. The first name, `ui-sans-serif`, is not a generic family in Chromium, and so a font face with that name is used first. A test in the real Obsidian 1.14.4 shows that one face named `ui-sans-serif` with the data of Volume Tc Sans is enough to draw the labels in Volume Tc Sans. The optional preset `lexmechanic-graph-labels` does this. It is not part of the theme, because it holds the font data a second time (54 KB). If a later Chromium knows `ui-sans-serif` as a generic family, the preset stops working, and the labels use the system font again.
* **The label size.** It is `14 + node size / 4` in the code.
* **The shape of a node.** Every node is a circle.
* **The display and force settings.** The node size, the link thickness, the text fade, the arrows, and the four forces are settings of the vault. They are in `.obsidian/graph.json`.
* **The color groups.** They are in `graph.json` too. A theme cannot add a group.

## Color groups

A color group is an entry of `colorGroups` in `graph.json`:

```
{"query": "tag:#idea", "color": {"a": 1, "rgb": 8347648}}
```

The `rgb` is one integer: red times 65536, plus green times 256, plus blue. `docs/palette.md` gives each palette color as an integer. The script `scripts/graph_groups.py` makes the list for you:

```
python3 scripts/graph_groups.py 'tag:#idea=yellow' 'tag:#project=blue' 'path:Inbox=sand'
```

A color of the light mode is not the same as the color of the dark mode. Use `--mode dark` for a dark vault.

## Settings in graph.json

The file `examples/graph.json` has every key that I found in the code. The display and force values are the defaults of Obsidian 1.14.4. The center strength 0.5187 is what the slider stores at the position 0.1. I did not open the example in Obsidian. Copy the keys that you want into your own `graph.json` and keep a copy of the old file.

## Node types differ by color only

A graph has five node types: resolved, unresolved, tag, attachment, and focused. CSS cannot change their shapes, so color is the only cue. The theme keeps the types apart by lightness and by hue. `scripts/check_graph.py` checks that the types differ in lightness by 10 points of CIE lightness or more, and `scripts/check_colorblind.py --graph` simulates protanopia, deuteranopia, and tritanopia and checks that each pair is 10 or more apart (CIEDE2000). Both checks pass, with no known exception. A reader can add a second cue with the node size setting.

The default colors are: dark brown (light mode) or pale warm gray (dark mode) for resolved nodes, teal for tags, rust or tan for attachments, the sand color for unresolved nodes, and the accent for the focused node. The hover highlight uses the ink color, so that it differs from the focus color. Obsidian draws unresolved nodes at half opacity, and the theme sets the opacity to 1.

## Tools

* `scripts/check_graph.py` reads the hooks in headless Chromium and checks the contrast.
* `scripts/check_variables.py` checks that the hooks and the variables still exist in a new Obsidian.
* `scripts/graph_groups.py` makes the `colorGroups` list.
* `scripts/make_demo_vault.py` writes a vault with 30 notes that shows every node type.
