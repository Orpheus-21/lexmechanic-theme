# Changelog

## 1.1.0 (2026-10-06)

Added:

* The `--lex-*` palette variables at the top of each mode block. One color change there reaches every rule.
* The accent set with `--accent-h`, `--accent-s`, and `--accent-l`, and the eight base colors.
* Variables for the focus border, form field backgrounds, error and success backgrounds, the message background, the modal cover, and the notice and tooltip text colors.
* Warm colors for scrollbars, indentation guides, the canvas, the tab drag ghost, and the toggle and slider thumbs.
* Variables for block quotes, inline code borders, and the heading font and weight.
* `scripts/check_contrast.py` and `docs/contrast.md`.
* The `src/` folder and `build.sh`. `theme.css` is built from the files in `src/`.
* A Credits section and a Checks section in the README.

Changed:

* The unresolved link opacity is 1. Before, Obsidian applied 0.7 and the contrast was 2.89 to 1 in light mode.
* The link hover color and the graph node color use the current muted colors.
* The caret is the accent color in every text field.
* The list markers use the accent color.
* The block quote border is 4 pixels wide. Inline code has a 1 pixel border.
* The tag, horizontal rule, and caret styles use Obsidian variables in place of CSS rules.
* The selected item in the file list matches the active item.
* The author field of the manifest is `Orpheus-21`.
* `minAppVersion` is `1.4.13`.

Fixed:

* The 4 pixel left border of callouts did not show. The snippet used `rgb(var(--callout-color))`, which is not valid.
* The dark mode canvas color stayed gray, because Obsidian sets it on `body.theme-dark`.
* The pull quote mark sat on top of the quote border. It now sits to the right of the border.

Removed:

* The `::selection` rule, the prompt font rule, the heading rule, the `font-display` lines, and the `--text-highlight-bg-rgb` variable.

## 1.0.0 (2026-10-06)

* The first version. It has the theme, the `lexmechanic-extras` snippet, and the `lexmechanic-fun` snippet.
