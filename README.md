# Lexmechanic

Lexmechanic is a theme for Obsidian. It uses a warm paper ground, dark brown text, and a red ink accent.

## What it does

The theme sets the colors, fonts, and link styles for the editor and the interface. It has a light mode and a dark mode. The light mode follows the colors of fromjason.xyz. The dark mode is a new version of the same colors.

Two optional CSS snippets add more styles. You can turn each snippet on or off alone.

## Requirements

* Obsidian for desktop, with installer version 1.4.13 or newer.
* The theme uses `color-mix()`. This function needs Chromium 111 or newer.
* Installer 1.4.13 has Electron 25.8.1. The installer is a different download from the app updates, and you must update it by hand. Get the newest installer from https://obsidian.md/download.
* The theme is not tested with an older installer.

## Install

1. Download this repo, or run `git clone https://github.com/Orpheus-21/lexmechanic-theme.git`.
2. Find the folder of your vault. The vault has a hidden folder named `.obsidian`.
3. Run these commands in the repo folder. Replace `VAULT` with the path of your vault.

```
mkdir -p "VAULT/.obsidian/themes/Lexmechanic" "VAULT/.obsidian/snippets"
cp manifest.json theme.css "VAULT/.obsidian/themes/Lexmechanic/"
cp snippets/*.css "VAULT/.obsidian/snippets/"
```

4. Open Obsidian. Open Settings, then Appearance.
5. Under Themes, choose `Lexmechanic`.
6. Under CSS snippets, turn on `lexmechanic-extras` and `lexmechanic-fun`. This step is optional.

The folder name `Lexmechanic` must match the `name` in `manifest.json`.

## Usage

The theme works after you choose it. It follows the light or dark setting of Obsidian.

The theme has two snippets.

`lexmechanic-extras` styles these parts:

* Callouts get a panel color and a 4 pixel left border in the color of the callout type.
* Tables get a panel color on the header row.
* Tags get a rounded badge in the accent color. The snippet sets the tag variables of Obsidian.

`lexmechanic-fun` styles these parts:

* The text caret, the cursor, and the active line use the accent color.
* A horizontal rule shows as a short red dash.
* The note column is 700 pixels wide.
* A block quote in reading view gets a large quote mark.
* A code block gets a red left border.
* Highlighted text (`==text==`) gets a red tint.
* Internal links have a dotted underline.

## Configuration

The theme has no settings of its own. These Obsidian settings change how it looks:

* Appearance, Text font, Interface font, and Monospace font replace the fonts of the theme.
* Editor, Readable line length turns the 700 pixel column on or off. The `lexmechanic-fun` snippet sets the width in the variable `--file-line-width`.

## How it works

`theme.css` is built from the files in `src/`. Do not edit `theme.css` by hand. Edit a file in `src/`, run `./build.sh`, and commit both. Run `./build.sh --check` to test that `theme.css` is up to date. The command exits with 1 if it is not.

`theme.css` has these parts, in this order:

1. Three `@font-face` rules, in `src/10-fonts.css`. Each rule holds a font as a base64 data URI.
2. One block of variables for both modes, in `src/20-shared.css`. It sets the font variables `--font-text-theme`, `--font-interface-theme`, and `--font-monospace-theme`. It also sets the variables for block quotes, code borders, headings, list markers, scrollbars, selected items in the file list, the focus border, and form fields.
3. One block of variables for `.theme-light`, in `src/30-light.css`.
4. One block of variables for `.theme-dark`, in `src/40-dark.css`.
5. One rule for the canvas color and one rule for the font of block quotes, in `src/50-rules.css`.

Each mode block starts with the palette: the `--lex-*` variables. Change a color there, and every other line follows. The rest of the block sets the Obsidian variables for backgrounds, text, links, code, the graph view, and the status colors. It also sets the accent with `--accent-h`, `--accent-s`, and `--accent-l`. It sets the eight base colors and the ten `--code-*` variables for syntax colors.

The snippets use only these variables. They add no colors of their own.

## Checks

The script `scripts/check_contrast.py` checks the contrast of the text colors. Run this command in the repo folder:

```
python3 scripts/check_contrast.py
```

The script reads `theme.css` and compares each text color with the page, panel, and alt panel colors. It exits with 1 when a pair is below 4.5 to 1. It needs only Python 3.

Three dark mode pairs are below 4.5 to 1: the accent, `--code-keyword`, and `--code-tag` on the alt panel color. The author keeps these pairs. The script lists them as known and does not fail for them.

The file `docs/contrast.md` has the contrast of every text color.

## Fonts

The fonts Volume Tc and Volume Tc Sans belong to Tom Chalky. The font files say "Copyright (c) 2022 by Tom Chalky. All rights reserved." The license terms are at https://tomchalky.com/extended-licensing. The GPL does not cover these fonts.

## Credits

* The light mode colors come from the CSS of https://www.fromjason.xyz. The dark mode colors are new.
* The fonts Volume Tc and Volume Tc Sans are by Tom Chalky: https://tomchalky.com.

## License

The CSS and the manifest of this repo use the GNU General Public License, version 3 or any later version. The `LICENSE` file has the text. The license does not cover the embedded fonts. See the Fonts section.
