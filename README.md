# Lexmechanic

Lexmechanic is a theme for Obsidian. It uses a warm paper ground, dark brown text, and a red ink accent.

## What it does

The theme sets the colors, fonts, and link styles for the editor and the interface. It has a light mode and a dark mode. The light mode follows the colors of fromjason.xyz. The dark mode is a new version of the same colors.

Two optional CSS snippets add more styles. You can turn each snippet on or off alone.

## Requirements

* Obsidian for desktop.
* An Obsidian version that has Chromium 111 or newer. The theme uses `color-mix()`, and Chromium 111 is the first version that supports it. I do not know the first Obsidian version that has it.

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

* Callouts get a panel color and a colored left border.
* Tables get a panel color on the header row.
* Tags get a rounded badge in the accent color.

`lexmechanic-fun` styles these parts:

* The cursor and the active line use the accent color.
* The command palette and the quick switcher use the interface font.
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

`theme.css` has these parts, in this order:

1. Three `@font-face` rules. Each rule holds a font as a base64 data URI.
2. The font variables `--font-text-theme`, `--font-interface-theme`, and `--font-monospace-theme`.
3. One block of variables for `.theme-light`.
4. One block of variables for `.theme-dark`.
5. A few rules for headings, block quotes, and text selection.

Each variable block sets the Obsidian variables for backgrounds, text, links, headings, code, and the graph view. It also sets the accent variables and the ten `--code-*` variables for syntax colors.

The snippets use only these variables. They add no colors of their own.

## Fonts

The fonts Volume Tc and Volume Tc Sans belong to Tom Chalky. The font files say "Copyright (c) 2022 by Tom Chalky. All rights reserved." The license terms are at https://tomchalky.com/extended-licensing. The GPL does not cover these fonts.

## License

The CSS and the manifest of this repo use the GNU General Public License, version 3 or any later version. The `LICENSE` file has the text. The license does not cover the embedded fonts. See the Fonts section.
