# Design

This page tells why the theme looks the way it does.

## Colors

* The light mode follows fromjason.xyz: an ivory page, dark brown ink, and a red accent. The dark mode is new. It uses a warm black (`#14110d`) and not a true black, so that it stays in the same paper family.
* All colors are in the palette: the `--lex-*` variables at the top of each mode file. A rule uses a palette color and never a hex value. A change to one color then reaches every rule, and a stale copy cannot stay behind.
* The accent is a red ink. Links are the ink color and have an underline. Only external links use the accent, because the red marks a special thing, not each link.
* The error color is orange and not red, so that an error differs from the accent.
* Quiet text (`--text-muted`) and faint text (`--text-faint`) are dark enough for 4.5 to 1 on the page, the panel, and the alt panel. The step between normal, quiet, and faint text is small on purpose.
* Unresolved links use the faint color at full opacity. Obsidian sets 0.7 opacity by default, and that lowered the contrast below 3 to 1.

## Contrast

Text must reach 4.5 to 1. Interface colors, such as the focus ring, must reach 3 to 1. `scripts/check_contrast.py` checks both. Three dark mode pairs are below 4.5 to 1 (the accent on the alt panel), and the quiet border of controls is below 3 to 1. The author keeps them, and the script lists them as known.

## Shape

* A 4 pixel accent border marks a block quote, the left side of a callout, and a code block. One width gives the three parts one look.
* A horizontal rule is a short red dash and not a full line.
* Code and tags have a quiet border or a quiet badge. Callouts and tables use the panel color.

## Fonts

* The body text is a serif font, Volume Tc. The interface, block quotes, callout titles, tags, and table headers use the sans font Volume Tc Sans.
* The fonts are inside `theme.css` as base64 data. Obsidian does not reliably load a font from a relative path in a theme.
* Each font has one weight. The browser draws bold text by smearing the glyphs.
* The fonts have only about 190 characters. The rest use the fallback fonts. `docs/characters.md` lists what is missing.
* A font setting of Obsidian can replace the fonts, because the theme sets the `-theme` variables and not the final ones.

## Rules and variables

* The theme prefers an Obsidian variable to a CSS rule. A variable reaches reading view, Live Preview, and the interface. A rule on an element often reaches only one view. A rule stays when Obsidian has no variable, such as the pull quote mark.
* A variable that Obsidian sets on `body.theme-dark` beats a rule on `.theme-dark`. The canvas color is one. The theme sets it on `body.theme-light` and `body.theme-dark`.

## Snippets

The theme has two optional snippets. `lexmechanic-extras` styles callouts, tables, and tags, which the source site does not have. `lexmechanic-fun` adds polish: the caret, the active line, the rule, the pull quote, the code border, highlights, and dotted internal links. Each snippet works alone, and the theme does not need them.

## Source and build

`theme.css` has about 220 KB of font data on three lines. The source is split into files in `src/`, and `build.sh` joins them. A change to a color then makes a small diff.

## Tests

A change that moves a rule into a variable must leave the page as it is. `scripts/check_baseline.py` compares the computed styles with a stored baseline, and shows each difference. `docs/testing.md` describes all the tests.
