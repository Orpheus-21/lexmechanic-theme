# Changelog

## [Unreleased]

Fixed:

* The print rules use `page-break-after` and `page-break-inside`, and they have no `!important`. A lint of the community list reported the `break-*` properties and the `!important` flags.

## [1.1.1] (2026-10-07)

Added:

* Fifteen preset snippets in `snippets/presets/`: accent colors (blue, green, black), a true black dark mode, a newsprint light mode, a high contrast mode, a narrow and a wide column, a sans and a monospace body font, a hyphens preset, and four graph presets (colorful, monochrome, high contrast, dim).
* Checks and tools in `scripts/`: `extract_obsidian_css.py`, `check_variables.py`, `check_resolve.py`, `check_baseline.py`, `check_graph.py`, `check_colorblind.py`, `check_manifest.py`, `check_duplicates.py`, `check_links.py`, `diff_obsidian_variables.py`, `font_coverage.py`, `make_docs.py`, `graph_groups.py`, `make_demo_vault.py`, `cdp.mjs`, `install.sh`, `install.ps1`, and `dev.sh`.
* The graph checks: the effective contrast of the 11 graph hooks with the opacity counted, the lightness of the node types, and a color blindness simulation. `check_variables.py` checks that the graph hooks and variables still exist.
* An example `graph.json` in `examples/`, and a script that makes the color groups from the palette.
* Documents in `docs/`: `palette.md`, `variables.md`, `characters.md`, `graph.md`, `testing.md`, `design.md`, and `obsidian-versions.md`.
* Checks of the interface colors (3 to 1) and of the selected text in `check_contrast.py`, and the options `--json`, `--write`, and `--check-doc`.
* The graph colors in `docs/contrast.md`.
* Unit tests in `tests/`, and a baseline of the computed styles.
* A GitHub Actions workflow for the checks, and a weekly check of the newest Obsidian.
* `build.py`, a `Makefile`, a stylelint config, `.gitignore`, `.gitattributes`, and `.editorconfig`.
* `obsidian_window.py` starts a temporary Obsidian window with its own profile for tests that need the real app. `check_graph_pixels.py` checks the node colors in the real graph.
* CJK font faces (`Lex CJK Serif` and `Lex CJK Sans`), `text-wrap: balance` for headings, `text-wrap: pretty` for paragraphs, and a graph labels preset.
* Sixteen more presets: task icons, extra callouts, drop cap, paper texture, typewriter, focus, justified text, heading numbers, four table options, quote citation, hide ribbon, slides, and a graph vignette.
* A Style Settings block with options for the accent, the column width, the fonts, the heading sizes, and the graph colors and opacity, and four switches in the `lexmechanic-fun` snippet.
* Rules for a darker tab line, controls with a 3 to 1 border, forced colors, print (light colors in dark mode, no page break after a heading, the address of an external link), reduced motion, RTL, and touch targets in the graph panel on a phone.
* Variables for footnotes, Bases, modals, hotkeys, search results, the status bar, the title bar, and the ribbon.
* `scripts/take_screenshots.py` and the images in `docs/images/`, a landing page in `docs/index.html`, `scripts/release.sh`, `scripts/release_notes.py`, a release workflow, and a pre-commit hook.
* `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, issue templates, and a pull request template.

Changed:

* The graph lines reach 2 to 1 on the page, and the force settings of `examples/graph.json` are the compact set.
* Every color of the mode files is in the `--lex-*` palette: the code colors, the base colors, the error hover color, the error RGB triple, and the graph colors.
* `build.sh` stops on an error and never leaves a partial `theme.css`.
* The README says that the note column is the default width of Obsidian.

Fixed:

* Found in the real app: the code block border, the internal links, the active line, the horizontal rule, and the callout quote color in Live Preview. The graph now has its own colors for tag, attachment, unresolved, and highlighted nodes.
* The dark mode attachment node of the graph used the old faint color. It now uses the faint color of the palette. Each graph color has a name in the palette.

Removed:

* The no-op rule for the line width, and four variables that equal the defaults of Obsidian.

## [1.1.0] (2026-10-06)

Added:

* The `--lex-*` palette variables at the top of each mode block. One color change there reaches every rule.
* The accent set with `--accent-h`, `--accent-s`, and `--accent-l`, and the eight base colors.
* Variables for the focus border, form field backgrounds, error and success backgrounds, the message background, the modal cover, and the notice and tooltip text colors.
* Warm colors for scrollbars, indentation guides, the canvas, the tab drag ghost, and the toggle and slider thumbs.
* Variables for block quotes, inline code borders, and the heading font and weight.
* `scripts/check_contrast.py` and `docs/contrast.md`.
* The `src/` folder and `build.sh`. `theme.css` is built from the files in `src/`.
* A Credits section and a Checks section in the README.
* A screenshot of the theme in light mode and in dark mode.

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

* The `::selection` rule, the prompt font rule, the heading rule, the cursor rule, the `font-display` lines, and the `--text-highlight-bg-rgb` variable.

## [1.0.0] (2026-10-06)

* The first version. It has the theme, the `lexmechanic-extras` snippet, and the `lexmechanic-fun` snippet.

[Unreleased]: https://github.com/Orpheus-21/lexmechanic-theme/compare/1.1.1...HEAD
[1.1.1]: https://github.com/Orpheus-21/lexmechanic-theme/compare/1.1.0...1.1.1
[1.1.0]: https://github.com/Orpheus-21/lexmechanic-theme/compare/394b876...1.1.0
[1.0.0]: https://github.com/Orpheus-21/lexmechanic-theme/commit/394b876
