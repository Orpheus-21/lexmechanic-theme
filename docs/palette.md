# Palette

Each mode file starts with the palette: the `--lex-*` variables. Change a color there, and every rule that uses it follows. A value that starts with `var(` points to another palette color.

The table comes from the source. Run `python3 scripts/make_docs.py --write` to make it again.

| Variable | Light | Dark | Use |
|---|---|---|---|
| `--lex-ground` | `#faf9f5` | `#14110d` | The page background, `--background-primary` |
| `--lex-panel` | `#f3f1e8` | `#1c1811` | Panels, the code background, and the tag badge |
| `--lex-panel-alt` | `#efece0` | `#221c14` | The alt panel, `--background-secondary-alt` |
| `--lex-ink` | `#2c251d` | `#e8e0d0` | Body text, headings, and links |
| `--lex-muted` | `#655d55` | `#b5ac9b` | Quiet text, icons, and the link hover color |
| `--lex-faint` | `#6f675f` | `#938a79` | Placeholders, unresolved links, and code comments |
| `--lex-sand` | `#968d85` | `#a89f8e` | Borders, dividers, scrollbars, and guides |
| `--lex-accent` | `#901714` | `#e8483d` | The accent: focus, buttons, list markers, the selection tint, and the focused node of the graph |
| `--lex-accent-hover` | `#733331` | `#f2685d` | The hover color of the accent |
| `--lex-error` | `#b83800` | `#ff7a45` | Error text and background |
| `--lex-success` | `#3a6329` | `#8fbf6f` | Success text and background |
| `--lex-warning` | `#7a4e00` | `#e0b04a` | Warning text and the function color in code |
| `--lex-code-property` | `#2f5d6e` | `#7fb3c4` | Properties in code |
| `--lex-code-value` | `#8a3b12` | `#d98b5f` | Values in code |
| `--lex-red` | `#a8231f` | `#ff6b5e` | Base color red: callouts, canvas, and highlights |
| `--lex-orange` | `#b83800` | `#ff7a45` | Base color orange |
| `--lex-yellow` | `#7f6000` | `#e0b04a` | Base color yellow |
| `--lex-green` | `#3a6329` | `#8fbf6f` | Base color green |
| `--lex-cyan` | `#2f5d6e` | `#7fb3c4` | Base color cyan |
| `--lex-blue` | `#3b5a8a` | `#8aa6d6` | Base color blue |
| `--lex-purple` | `#6b4a7d` | `#b99ad0` | Base color purple |
| `--lex-pink` | `#a04668` | `#e08aa8` | Base color pink |
| `--lex-error-hover` | `#9a3000` | `#ff946a` | The hover color of the error background |
| `--lex-error-rgb` | `184, 56, 0` | `255, 122, 69` | The error color as a triple, for Obsidian variables that ask for RGB |
| `--lex-code-normal` | `#070504` | `var(--lex-ink)` | Plain code text |
| `--lex-graph-tag` | `#277461` | `#69b6c6` | Tag nodes of the graph |
| `--lex-graph-unresolved` | `var(--lex-sand)` | `#7d7464` | Unresolved nodes of the graph |
| `--lex-graph-node` | `#473e34` | `#dcd6d0` | Resolved nodes of the graph |
| `--lex-graph-highlight` | `var(--lex-ink)` | `var(--lex-ink)` | The hover highlight of the graph: the node under the pointer and its lines |
| `--lex-graph-attachment` | `#aa5539` | `#cda47a` | Attachment nodes of the graph |

## Graph colors

The graph view reads these variables. Each one uses a palette color.

| Variable | Light | Dark | Draws |
|---|---|---|---|
| `--graph-node` | `var(--lex-graph-node)` | `var(--lex-graph-node)` | Resolved nodes |
| `--graph-node-focused` | `var(--lex-accent)` | `var(--lex-accent)` | The focused node and the focus ring |
| `--graph-node-tag` | `var(--lex-graph-tag)` | `var(--lex-graph-tag)` | Tag nodes |
| `--graph-node-attachment` | `var(--lex-graph-attachment)` | `var(--lex-graph-attachment)` | Attachment nodes |
| `--graph-node-unresolved` | `var(--lex-graph-unresolved)` | `var(--lex-graph-unresolved)` | Unresolved nodes (drawn at half opacity by Obsidian) |
| `--graph-line` | `color-mix(in srgb, var(--lex-sand) 45%, transparent)` | `color-mix(in srgb, var(--lex-sand) 35%, transparent)` | Lines between nodes |
| `--graph-text` | `var(--lex-ink)` | `var(--lex-ink)` | Node labels |

The contrast of each graph color is in `docs/contrast.md`.

## Colors for graph.json

A color group in `graph.json` stores its color as one integer: red times 65536, plus green times 256, plus blue. The table gives each palette color that is a solid color as a hex value and as an integer. `scripts/graph_groups.py` makes the `colorGroups` list from these colors.

| Name | Light | Light integer | Dark | Dark integer |
|---|---|---|---|---|
| `ground` | `#faf9f5` | 16447989 | `#14110d` | 1315085 |
| `panel` | `#f3f1e8` | 15987176 | `#1c1811` | 1841169 |
| `panel-alt` | `#efece0` | 15723744 | `#221c14` | 2235412 |
| `ink` | `#2c251d` | 2893085 | `#e8e0d0` | 15261904 |
| `muted` | `#655d55` | 6643029 | `#b5ac9b` | 11906203 |
| `faint` | `#6f675f` | 7300959 | `#938a79` | 9669241 |
| `sand` | `#968d85` | 9866629 | `#a89f8e` | 11050894 |
| `accent` | `#901714` | 9443092 | `#e8483d` | 15222845 |
| `accent-hover` | `#733331` | 7549745 | `#f2685d` | 15886429 |
| `error` | `#b83800` | 12072960 | `#ff7a45` | 16742981 |
| `success` | `#3a6329` | 3826473 | `#8fbf6f` | 9420655 |
| `warning` | `#7a4e00` | 8015360 | `#e0b04a` | 14725194 |
| `code-property` | `#2f5d6e` | 3104110 | `#7fb3c4` | 8369092 |
| `code-value` | `#8a3b12` | 9059090 | `#d98b5f` | 14256991 |
| `code-normal` | `#070504` | 460036 | `#e8e0d0` | 15261904 |
| `red` | `#a8231f` | 11019039 | `#ff6b5e` | 16739166 |
| `orange` | `#b83800` | 12072960 | `#ff7a45` | 16742981 |
| `yellow` | `#7f6000` | 8347648 | `#e0b04a` | 14725194 |
| `green` | `#3a6329` | 3826473 | `#8fbf6f` | 9420655 |
| `cyan` | `#2f5d6e` | 3104110 | `#7fb3c4` | 8369092 |
| `blue` | `#3b5a8a` | 3889802 | `#8aa6d6` | 9086678 |
| `purple` | `#6b4a7d` | 7031421 | `#b99ad0` | 12163792 |
| `pink` | `#a04668` | 10503784 | `#e08aa8` | 14715560 |
| `error-hover` | `#9a3000` | 10104832 | `#ff946a` | 16749674 |
| `graph-node` | `#473e34` | 4668980 | `#dcd6d0` | 14472912 |
| `graph-highlight` | `#2c251d` | 2893085 | `#e8e0d0` | 15261904 |
| `graph-tag` | `#277461` | 2585697 | `#69b6c6` | 6928070 |
| `graph-unresolved` | `#968d85` | 9866629 | `#7d7464` | 8221796 |
| `graph-attachment` | `#aa5539` | 11162937 | `#cda47a` | 13476986 |
