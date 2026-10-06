# Contrast of the text colors

This file lists the contrast of each text color on each background color. The aim is 4.5 to 1 or more.

The tables come from the script `scripts/check_contrast.py`. To make them again, run this command in the repo folder:

```
python3 scripts/check_contrast.py --markdown
```

Replace the two tables below with the output of the command.

Backgrounds:

* Page: `--background-primary`
* Panel: `--background-secondary`
* Alt panel: `--background-secondary-alt`

A note "known" means that the pair is below 4.5 to 1 and an issue is open for it.

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
| `--text-on-accent (on --interactive-accent)` | `#faf9f5` | 8.60 to 1 | | |

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
| `--text-on-accent (on --interactive-accent)` | `#14110d` | 4.86 to 1 | | |

