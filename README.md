# Lexmechanic

Lexmechanic is a theme for Obsidian. It uses a warm paper ground, dark brown text, and a red ink accent.

![Lexmechanic in light mode and in dark mode](screenshot.png)

The screenshot shows a note in reading view in Obsidian 1.14.4. Light mode is on the left. Dark mode is on the right.

## What it does

The theme sets the colors, fonts, and link styles for the editor and the interface. It has a light mode and a dark mode. The light mode follows the colors of fromjason.xyz. The dark mode is a new version of the same colors.

Two optional CSS snippets add more styles. You can turn each snippet on or off alone.

## Requirements

* Obsidian for desktop, with installer version 1.4.13 or newer.
* The theme uses `color-mix()`. This function needs Chromium 111 or newer.
* Installer 1.4.13 has Electron 25.8.1. The installer is a different download from the app updates, and you must update it by hand. Get the newest installer from https://obsidian.md/download.
* The theme is not tested with an older installer.

## Compatibility

| Obsidian app | Installer | System | Result |
|---|---|---|---|
| 1.14.4 | 1.13.7 | Linux | Tested: reading view and Live Preview in both modes, and the checks of `scripts/` |
| Any | Older than 1.4.13 | Any | Not supported. The theme needs `color-mix()`. |
| Any | 1.4.13 or newer | Windows, macOS | Not tested |
| Any | Any | Android, iOS | Not tested |

## Install

1. Download this repo, or run `git clone https://github.com/Orpheus-21/lexmechanic-theme.git`.
2. Find the folder of your vault. The vault has a hidden folder named `.obsidian`.
3. Copy the files into the vault. Choose one way:
   * On Linux and macOS, run `scripts/install.sh VAULT` in the repo folder. Replace `VAULT` with the path of your vault.
   * On Windows, run `.\scripts\install.ps1 -Vault "C:\path\to\vault"` in PowerShell. This script is not tested on Windows.
   * In a terminal, run these commands in the repo folder:

```
mkdir -p "VAULT/.obsidian/themes/Lexmechanic" "VAULT/.obsidian/snippets"
cp manifest.json theme.css "VAULT/.obsidian/themes/Lexmechanic/"
cp snippets/*.css "VAULT/.obsidian/snippets/"
```

   * In a file manager, make the folders `.obsidian/themes/Lexmechanic` and `.obsidian/snippets` in the vault if they do not exist. Copy `manifest.json` and `theme.css` into the first folder. Copy the files of `snippets/` into the second folder.
4. Open Obsidian. Open Settings, then Appearance.
5. Under Themes, choose `Lexmechanic`.
6. Under CSS snippets, turn on `lexmechanic-extras` and `lexmechanic-fun`. This step is optional.

The folder name `Lexmechanic` must match the `name` in `manifest.json`.

A file manager can hide the `.obsidian` folder. In Finder on macOS, press Command, Shift, and the period key. In Explorer on Windows, open View, then Show, then Hidden items. Most file managers on Linux show hidden items with Ctrl and H.

## Update

1. Get the new version: run `git pull` in the clone, or download the repo again.
2. Copy the files into the vault again, in the same way as the install. The new files replace the old ones.
3. Restart Obsidian.

The file `CHANGELOG.md` lists the changes of each version.

## Uninstall

1. Open Settings, then Appearance. Under Themes, choose another theme. Under CSS snippets, turn off `lexmechanic-extras` and `lexmechanic-fun`.
2. Delete the folder `.obsidian/themes/Lexmechanic` in the vault.
3. Delete the files `lexmechanic-extras.css` and `lexmechanic-fun.css` in the folder `.obsidian/snippets`.

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
* A block quote in reading view gets a large quote mark.
* A code block gets a red left border.
* Highlighted text (`==text==`) gets a red tint.
* Internal links have a dotted underline.

## Troubleshooting

* **The theme is not in the list.** The vault must have the files `.obsidian/themes/Lexmechanic/manifest.json` and `.obsidian/themes/Lexmechanic/theme.css`. The folder name must be `Lexmechanic`. Restart Obsidian.
* **The snippets are not in the list.** The files must be in `.obsidian/snippets`, and their names must end in `.css`. Restart Obsidian.
* **Colors or borders look wrong.** The theme needs installer version 1.4.13 or newer. Look at the installer version in Settings, then General. The installer is a different download from the app updates.
* **The fonts differ from the screenshot.** Open Settings, then Appearance. If the font fields are not empty, they replace the fonts of the theme. Clear them.
* **A dash, an ellipsis, or a symbol is in another style.** The fonts of the theme have about 175 characters. Other characters use a fallback font. The file `docs/characters.md` lists them.
* **The labels in the graph view use a system font.** Obsidian fixes the font of the graph labels in its code. A theme cannot change it.
* **The theme looks wrong on a phone.** The theme is not tested on Android or iOS.

## Configuration

The theme has no settings of its own. These Obsidian settings change how it looks:

* Appearance, Text font, Interface font, and Monospace font replace the fonts of the theme.
* Editor, Readable line length turns the note column on or off. The column is 700 pixels wide. This is the default of Obsidian, and the theme does not change it.

## How it works

`theme.css` is built from the files in `src/`. Do not edit `theme.css` by hand. Edit a file in `src/`, run `./build.sh`, and commit both. Run `./build.sh --check` to test that `theme.css` is up to date. The command exits with 1 if it is not.

`theme.css` has these parts, in this order:

1. Three `@font-face` rules, in `src/10-fonts.css`. Each rule holds a font as a base64 data URI.
2. One block of variables for both modes, in `src/20-shared.css`. It sets the font variables `--font-text-theme`, `--font-interface-theme`, and `--font-monospace-theme`. It also sets the variables for block quotes, code borders, headings, and list markers. It sets the variables for scrollbars, selected items in the file list, the focus border, and form fields.
3. One block of variables for `.theme-light`, in `src/30-light.css`.
4. One block of variables for `.theme-dark`, in `src/40-dark.css`.
5. One rule for the canvas color and one rule for the font of block quotes, in `src/50-rules.css`.

Each mode block starts with the palette: the `--lex-*` variables. Change a color there, and every other line follows. The rest of the block sets the Obsidian variables for backgrounds, text, links, code, the graph view, and the status colors. It also sets the accent with `--accent-h`, `--accent-s`, and `--accent-l`. It sets the eight base colors and the ten `--code-*` variables for syntax colors.

The snippets use only these variables. They add no colors of their own.

## Checks

Run `make all` in the repo folder. It checks that `theme.css` is up to date, runs the unit tests, runs stylelint, and checks the contrast. It needs Python 3 and `npx`.

The script `scripts/check_contrast.py` checks the contrast of the colors. Text colors must reach 4.5 to 1 on the page, panel, and alt panel colors. Interface colors, such as the focus ring, must reach 3 to 1. The script exits with 1 when a pair is too low.

Some pairs are below their minimum, and the author keeps them: three dark mode pairs of the accent on the alt panel color, and the border of controls. The script lists them as known and does not fail for them.

The file `docs/contrast.md` has the contrast of every color pair, and of the graph colors. Four more checks need Chromium and an installed Obsidian: `check_variables.py`, `check_resolve.py`, `check_baseline.py`, and `check_graph.py`. The file `CONTRIBUTING.md` describes them.

## Contributing

The source is in `src/`. Run `./build.sh` after a change, and `make all` to check it. The file `CONTRIBUTING.md` has the details.

## Fonts

The fonts Volume Tc and Volume Tc Sans belong to Tom Chalky. The font files say "Copyright (c) 2022 by Tom Chalky. All rights reserved." The license terms are at https://tomchalky.com/extended-licensing. The GPL does not cover these fonts.

## Credits

* The light mode colors come from the CSS of https://www.fromjason.xyz. The dark mode colors are new.
* The fonts Volume Tc and Volume Tc Sans are by Tom Chalky: https://tomchalky.com.

## License

The CSS and the manifest of this repo use the GNU General Public License, version 3 or any later version. The `LICENSE` file has the text. The license does not cover the embedded fonts. See the Fonts section.
