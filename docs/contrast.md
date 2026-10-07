# Contrast of the colors

This file lists the contrast of the text colors on the background colors, and of a few interface colors. Text needs 4.5 to 1 or more.

The tables come from the script `scripts/check_contrast.py`. To make them again, run this command in the repo folder:

```
python3 scripts/check_contrast.py --write
```

The command replaces the text between the two comment markers below. Run `python3 scripts/check_contrast.py --check-doc` to test that the file is up to date.

Backgrounds:

* Page: `--background-primary`
* Panel: `--background-secondary`
* Alt panel: `--background-secondary-alt`

Text colors need 4.5 to 1. Other pairs, such as the focus ring and the toggle thumb, need 3 to 1. A note "known" means that the pair is below its minimum and the author keeps it. The note names the issue that has the decision.

<!-- contrast:start -->
## Light mode

| Text color | Value | On page | On panel | On alt panel |
|---|---|---|---|---|
| `--text-normal` | `#2c251d` | 14.35 to 1 | 13.36 to 1 | 12.77 to 1 |
| `--text-muted` | `#655d55` | 6.13 to 1 | 5.71 to 1 | 5.46 to 1 |
| `--text-faint` | `#6f675f` | 5.27 to 1 | 4.91 to 1 | 4.69 to 1 |
| `--text-accent` | `#901714` | 8.60 to 1 | 8.00 to 1 | 7.65 to 1 |
| `--text-error` | `#b83800` | 5.53 to 1 | 5.15 to 1 | 4.92 to 1 |
| `--text-warning` | `#7a4e00` | 6.83 to 1 | 6.36 to 1 | 6.08 to 1 |
| `--text-success` | `#3a6329` | 6.65 to 1 | 6.19 to 1 | 5.92 to 1 |
| `--link-unresolved-color` | `#6f675f` | 5.27 to 1 | 4.91 to 1 | 4.69 to 1 |
| `--code-comment` | `#6f675f` | 5.27 to 1 | 4.91 to 1 | 4.69 to 1 |
| `--code-function` | `#7a4e00` | 6.83 to 1 | 6.36 to 1 | 6.08 to 1 |
| `--code-important` | `#b83800` | 5.53 to 1 | 5.15 to 1 | 4.92 to 1 |
| `--code-keyword` | `#901714` | 8.60 to 1 | 8.00 to 1 | 7.65 to 1 |
| `--code-operator` | `#655d55` | 6.13 to 1 | 5.71 to 1 | 5.46 to 1 |
| `--code-property` | `#2f5d6e` | 6.85 to 1 | 6.37 to 1 | 6.09 to 1 |
| `--code-punctuation` | `#655d55` | 6.13 to 1 | 5.71 to 1 | 5.46 to 1 |
| `--code-string` | `#3a6329` | 6.65 to 1 | 6.19 to 1 | 5.92 to 1 |
| `--code-tag` | `#901714` | 8.60 to 1 | 8.00 to 1 | 7.65 to 1 |
| `--code-value` | `#8a3b12` | 7.34 to 1 | 6.84 to 1 | 6.54 to 1 |
| `--color-red` | `#a8231f` | 6.81 to 1 | 6.34 to 1 | 6.07 to 1 |
| `--color-orange` | `#b83800` | 5.53 to 1 | 5.15 to 1 | 4.92 to 1 |
| `--color-yellow` | `#7f6000` | 5.57 to 1 | 5.19 to 1 | 4.96 to 1 |
| `--color-green` | `#3a6329` | 6.65 to 1 | 6.19 to 1 | 5.92 to 1 |
| `--color-cyan` | `#2f5d6e` | 6.85 to 1 | 6.37 to 1 | 6.09 to 1 |
| `--color-blue` | `#3b5a8a` | 6.61 to 1 | 6.15 to 1 | 5.88 to 1 |
| `--color-purple` | `#6b4a7d` | 6.87 to 1 | 6.40 to 1 | 6.12 to 1 |
| `--color-pink` | `#a04668` | 5.58 to 1 | 5.20 to 1 | 4.97 to 1 |

Other pairs:

| Pair | Needs | Ratio |
|---|---|---|
| `--text-on-accent on --interactive-accent` | 4.5 to 1 | 8.60 to 1 |
| `--text-normal on the selection color` | 4.5 to 1 | 9.52 to 1 |
| `--interactive-accent on the page` | 3 to 1 | 8.60 to 1 |
| `--checkbox-color on the page` | 3 to 1 | 8.60 to 1 |
| `--background-modifier-border-focus on the page` | 3 to 1 | 8.60 to 1 |
| `--background-modifier-border-hover on the page` | 3 to 1 | 3.09 to 1 |
| `--toggle-thumb-color on --interactive-accent` | 3 to 1 | 8.60 to 1 |
| `--background-modifier-border on the page` | 3 to 1 | 1.27 to 1 (known, #314) |

## Dark mode

| Text color | Value | On page | On panel | On alt panel |
|---|---|---|---|---|
| `--text-normal` | `#e8e0d0` | 14.34 to 1 | 13.47 to 1 | 12.86 to 1 |
| `--text-muted` | `#b5ac9b` | 8.37 to 1 | 7.86 to 1 | 7.51 to 1 |
| `--text-faint` | `#938a79` | 5.51 to 1 | 5.18 to 1 | 4.94 to 1 |
| `--text-accent` | `#e8483d` | 4.86 to 1 | 4.57 to 1 | 4.36 to 1 (known, #74) |
| `--text-error` | `#ff7a45` | 7.28 to 1 | 6.84 to 1 | 6.53 to 1 |
| `--text-warning` | `#e0b04a` | 9.39 to 1 | 8.82 to 1 | 8.42 to 1 |
| `--text-success` | `#8fbf6f` | 8.83 to 1 | 8.29 to 1 | 7.92 to 1 |
| `--link-unresolved-color` | `#938a79` | 5.51 to 1 | 5.18 to 1 | 4.94 to 1 |
| `--code-comment` | `#938a79` | 5.51 to 1 | 5.18 to 1 | 4.94 to 1 |
| `--code-function` | `#e0b04a` | 9.39 to 1 | 8.82 to 1 | 8.42 to 1 |
| `--code-important` | `#ff7a45` | 7.28 to 1 | 6.84 to 1 | 6.53 to 1 |
| `--code-keyword` | `#e8483d` | 4.86 to 1 | 4.57 to 1 | 4.36 to 1 (known, #74) |
| `--code-operator` | `#b5ac9b` | 8.37 to 1 | 7.86 to 1 | 7.51 to 1 |
| `--code-property` | `#7fb3c4` | 8.20 to 1 | 7.70 to 1 | 7.35 to 1 |
| `--code-punctuation` | `#b5ac9b` | 8.37 to 1 | 7.86 to 1 | 7.51 to 1 |
| `--code-string` | `#8fbf6f` | 8.83 to 1 | 8.29 to 1 | 7.92 to 1 |
| `--code-tag` | `#e8483d` | 4.86 to 1 | 4.57 to 1 | 4.36 to 1 (known, #74) |
| `--code-value` | `#d98b5f` | 7.00 to 1 | 6.57 to 1 | 6.28 to 1 |
| `--color-red` | `#ff6b5e` | 6.74 to 1 | 6.33 to 1 | 6.04 to 1 |
| `--color-orange` | `#ff7a45` | 7.28 to 1 | 6.84 to 1 | 6.53 to 1 |
| `--color-yellow` | `#e0b04a` | 9.39 to 1 | 8.82 to 1 | 8.42 to 1 |
| `--color-green` | `#8fbf6f` | 8.83 to 1 | 8.29 to 1 | 7.92 to 1 |
| `--color-cyan` | `#7fb3c4` | 8.20 to 1 | 7.70 to 1 | 7.35 to 1 |
| `--color-blue` | `#8aa6d6` | 7.62 to 1 | 7.16 to 1 | 6.84 to 1 |
| `--color-purple` | `#b99ad0` | 7.70 to 1 | 7.23 to 1 | 6.91 to 1 |
| `--color-pink` | `#e08aa8` | 7.50 to 1 | 7.04 to 1 | 6.73 to 1 |

Other pairs:

| Pair | Needs | Ratio |
|---|---|---|
| `--text-on-accent on --interactive-accent` | 4.5 to 1 | 4.86 to 1 |
| `--text-normal on the selection color` | 4.5 to 1 | 10.72 to 1 |
| `--interactive-accent on the page` | 3 to 1 | 4.86 to 1 |
| `--checkbox-color on the page` | 3 to 1 | 4.86 to 1 |
| `--background-modifier-border-focus on the page` | 3 to 1 | 4.86 to 1 |
| `--background-modifier-border-hover on the page` | 3 to 1 | 7.18 to 1 |
| `--toggle-thumb-color on --interactive-accent` | 3 to 1 | 4.86 to 1 |
| `--background-modifier-border on the page` | 3 to 1 | 1.25 to 1 (known, #314) |
<!-- contrast:end -->

<!-- graph:start -->
## Graph view

Obsidian reads the graph colors from hidden `.graph-view.color-*` elements. The final alpha is the opacity times the color alpha. The ratio is the contrast of the effective color on the page color.

### Light mode

| Hook | Draws | Color | Alpha | Needs | Ratio |
|---|---|---|---|---|---|
| `color-fill` | resolved node | `#473e34` | 1 | 3 to 1 | 9.93 to 1 |
| `color-fill-focused` | focused node | `#901714` | 1 | 3 to 1 | 8.60 to 1 |
| `color-fill-tag` | tag node | `#277461` | 1 | 3 to 1 | 5.31 to 1 |
| `color-fill-attachment` | attachment node | `#aa5539` | 1 | 3 to 1 | 4.90 to 1 |
| `color-fill-unresolved` | unresolved node | `#968d85` | 1 | 3 to 1 | 3.09 to 1 |
| `color-arrow` | arrow | `#2c251d` | 0.5 | 3 to 1 | 3.05 to 1 |
| `color-circle` | focus ring | `#901714` | 1 | 3 to 1 | 8.60 to 1 |
| `color-line` | line | `#978e85` | 0.451 | 1.5 to 1 | 1.57 to 1 |
| `color-text` | label text | `#2c251d` | 1 | 4.5 to 1 | 14.35 to 1 |
| `color-fill-highlight` | hover highlight of a node | `#2c251d` | 1 | 3 to 1 | 14.35 to 1 |
| `color-line-highlight` | hover highlight of a line | `#2c251d` | 1 | 3 to 1 | 14.35 to 1 |

Node types must differ in lightness (CIE L*) by at least 10:

| Pair | Difference |
|---|---|
| `fill` and `fill-unresolved` | 32.4 |
| `fill` and `fill-attachment` | 19.3 |
| `fill` and `fill-tag` | 17.1 |
| `fill-tag` and `fill-focused` | 13.1 |
| `fill-attachment` and `fill-unresolved` | 13.1 |
| `fill-focused` and `fill-highlight` | 15.7 |

### Dark mode

| Hook | Draws | Color | Alpha | Needs | Ratio |
|---|---|---|---|---|---|
| `color-fill` | resolved node | `#dcd6d0` | 1 | 3 to 1 | 13.06 to 1 |
| `color-fill-focused` | focused node | `#e8483d` | 1 | 3 to 1 | 4.86 to 1 |
| `color-fill-tag` | tag node | `#69b6c6` | 1 | 3 to 1 | 8.16 to 1 |
| `color-fill-attachment` | attachment node | `#cda47a` | 1 | 3 to 1 | 8.23 to 1 |
| `color-fill-unresolved` | unresolved node | `#7d7464` | 1 | 3 to 1 | 4.08 to 1 |
| `color-arrow` | arrow | `#e8e0d0` | 0.5 | 3 to 1 | 4.30 to 1 |
| `color-circle` | focus ring | `#e8483d` | 1 | 3 to 1 | 4.86 to 1 |
| `color-line` | line | `#a99e8f` | 0.349 | 1.5 to 1 | 1.90 to 1 |
| `color-text` | label text | `#e8e0d0` | 1 | 4.5 to 1 | 14.34 to 1 |
| `color-fill-highlight` | hover highlight of a node | `#e8e0d0` | 1 | 3 to 1 | 14.34 to 1 |
| `color-line-highlight` | hover highlight of a line | `#e8e0d0` | 1 | 3 to 1 | 14.34 to 1 |

Node types must differ in lightness (CIE L*) by at least 10:

| Pair | Difference |
|---|---|
| `fill` and `fill-unresolved` | 36.7 |
| `fill` and `fill-attachment` | 15.8 |
| `fill` and `fill-tag` | 16.1 |
| `fill-tag` and `fill-focused` | 15.7 |
| `fill-attachment` and `fill-unresolved` | 20.9 |
| `fill-focused` and `fill-highlight` | 35.2 |
<!-- graph:end -->
