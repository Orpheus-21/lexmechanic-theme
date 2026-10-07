# Variables

This file lists each Obsidian variable that the theme or a snippet sets, with its value in each mode. The palette (`--lex-*`) is in `docs/palette.md`. A value that starts with `var(` uses another variable.

The tables come from the source. Run `python3 scripts/make_docs.py --write` to make them again.

## Fonts

The text, interface, and monospace fonts. The names that end in `-theme` are the ones that the font settings of Obsidian replace.

| Variable | Light | Dark | Set in |
|---|---|---|---|
| `--font-interface-theme` | `'Volume Tc Sans', Verdana, 'Noto Sans', sans-serif` | `'Volume Tc Sans', Verdana, 'Noto Sans', sans-serif` | theme |
| `--font-monospace-theme` | `ui-monospace, 'SF Mono', Consolas, monospace` | `ui-monospace, 'SF Mono', Consolas, monospace` | theme |
| `--font-text-theme` | `'Volume Tc', Georgia, 'Times New Roman', 'Noto Serif', serif` | `'Volume Tc', Georgia, 'Times New Roman', 'Noto Serif', serif` | theme |

## Backgrounds and borders

The page and panel colors, borders, the hover color, the error and success fills, the form field fill, and the modal cover. All of them come from the palette, so that no gray of Obsidian is left.

| Variable | Light | Dark | Set in |
|---|---|---|---|
| `--background-modifier-border` | `color-mix(in srgb, var(--lex-sand) 25%, transparent)` | `color-mix(in srgb, var(--lex-sand) 15%, transparent)` | theme |
| `--background-modifier-border-focus` | `var(--interactive-accent)` | `var(--interactive-accent)` | theme |
| `--background-modifier-border-hover` | `var(--lex-sand)` | `var(--lex-sand)` | theme |
| `--background-modifier-cover` | `color-mix(in srgb, var(--lex-sand) 35%, transparent)` | `color-mix(in srgb, var(--lex-ground) 60%, transparent)` | theme |
| `--background-modifier-error` | `var(--lex-error)` | `var(--lex-error)` | theme |
| `--background-modifier-error-hover` | `var(--lex-error-hover)` | `var(--lex-error-hover)` | theme |
| `--background-modifier-error-rgb` | `var(--lex-error-rgb)` | `var(--lex-error-rgb)` | theme |
| `--background-modifier-form-field` | `var(--background-primary)` | `var(--background-primary)` | theme |
| `--background-modifier-form-field-hover` | `var(--background-primary-alt)` | `var(--background-primary-alt)` | theme |
| `--background-modifier-hover` | `color-mix(in srgb, var(--lex-sand) 12%, transparent)` | `color-mix(in srgb, var(--lex-sand) 10%, transparent)` | theme |
| `--background-modifier-message` | `color-mix(in srgb, var(--lex-ink) 92%, transparent)` | `var(--background-secondary-alt)` | theme |
| `--background-modifier-success` | `var(--text-success)` | `var(--text-success)` | theme |
| `--background-primary` | `var(--lex-ground)` | `var(--lex-ground)` | theme |
| `--background-primary-alt` | `var(--lex-panel)` | `var(--lex-panel)` | theme |
| `--background-secondary` | `var(--lex-panel)` | `var(--lex-panel)` | theme |
| `--background-secondary-alt` | `var(--lex-panel-alt)` | `var(--lex-panel-alt)` | theme |

## Text

The colors of normal, quiet, and faint text, the accent, the status colors, and the selection. Each one has a contrast of 4.5 to 1 or more on the page.

| Variable | Light | Dark | Set in |
|---|---|---|---|
| `--text-accent` | `var(--lex-accent)` | `var(--lex-accent)` | theme |
| `--text-accent-hover` | `var(--lex-accent-hover)` | `var(--lex-accent-hover)` | theme |
| `--text-error` | `var(--lex-error)` | `var(--lex-error)` | theme |
| `--text-faint` | `var(--lex-faint)` | `var(--lex-faint)` | theme |
| `--text-highlight-bg` | `color-mix(in srgb, var(--lex-accent) 20%, var(--lex-panel))` | `color-mix(in srgb, var(--lex-accent) 25%, var(--lex-panel))` | theme |
| `--text-muted` | `var(--lex-muted)` | `var(--lex-muted)` | theme |
| `--text-normal` | `var(--lex-ink)` | `var(--lex-ink)` | theme |
| `--text-on-accent` | `var(--lex-ground)` | `var(--lex-ground)` | theme |
| `--text-selection` | `color-mix(in srgb, var(--lex-accent) 22%, transparent)` | `color-mix(in srgb, var(--lex-accent) 25%, transparent)` | theme |
| `--text-success` | `var(--lex-success)` | `var(--lex-success)` | theme |
| `--text-warning` | `var(--lex-warning)` | `var(--lex-warning)` | theme |

## Accent

The accent. `--accent-h`, `--accent-s`, and `--accent-l` give Obsidian the hue, and the other variables give the colors of buttons and the caret.

| Variable | Light | Dark | Set in |
|---|---|---|---|
| `--accent-h` | `1` | `4` | theme |
| `--accent-l` | `32%` | `57%` | theme |
| `--accent-s` | `76%` | `79%` | theme |
| `--caret-color` | `var(--text-accent)` | `var(--text-accent)` | lexmechanic-fun |
| `--interactive-accent` | `var(--lex-accent)` | `var(--lex-accent)` | theme |
| `--interactive-accent-hover` | `var(--lex-accent-hover)` | `var(--lex-accent-hover)` | theme |
| `--interactive-hover` | `color-mix(in srgb, var(--lex-sand) 15%, transparent)` | `color-mix(in srgb, var(--lex-sand) 12%, transparent)` | theme |
| `--interactive-normal` | `var(--lex-panel)` | `var(--lex-panel)` | theme |

## Links

Links are the ink color. External links use the accent. Unresolved links use the faint color at full opacity, because Obsidian lowers it to 0.7 by default.

| Variable | Light | Dark | Set in |
|---|---|---|---|
| `--link-color` | `var(--lex-ink)` | `var(--lex-ink)` | theme |
| `--link-color-hover` | `var(--lex-muted)` | `var(--lex-muted)` | theme |
| `--link-external-color` | `var(--lex-accent)` | `var(--lex-accent)` | theme |
| `--link-external-color-hover` | `var(--lex-accent-hover)` | `var(--lex-accent-hover)` | theme |
| `--link-unresolved-color` | `var(--lex-faint)` | `var(--lex-faint)` | theme |
| `--link-unresolved-opacity` | `1` | `1` | theme |

## Headings

Headings use the text font in bold and the ink color. The variables reach reading view and Live Preview.

| Variable | Light | Dark | Set in |
|---|---|---|---|
| `--h1-color` | `var(--lex-ink)` | `var(--lex-ink)` | theme |
| `--h1-font` | `var(--font-text)` | `var(--font-text)` | theme |
| `--h2-color` | `var(--lex-ink)` | `var(--lex-ink)` | theme |
| `--h2-font` | `var(--font-text)` | `var(--font-text)` | theme |
| `--h2-weight` | `700` | `700` | theme |
| `--h3-color` | `var(--lex-ink)` | `var(--lex-ink)` | theme |
| `--h3-font` | `var(--font-text)` | `var(--font-text)` | theme |
| `--h3-weight` | `700` | `700` | theme |
| `--h4-color` | `var(--lex-ink)` | `var(--lex-ink)` | theme |
| `--h4-font` | `var(--font-text)` | `var(--font-text)` | theme |
| `--h4-weight` | `700` | `700` | theme |
| `--h5-color` | `var(--lex-ink)` | `var(--lex-ink)` | theme |
| `--h5-font` | `var(--font-text)` | `var(--font-text)` | theme |
| `--h5-weight` | `700` | `700` | theme |
| `--h6-color` | `var(--lex-ink)` | `var(--lex-ink)` | theme |
| `--h6-font` | `var(--font-text)` | `var(--font-text)` | theme |
| `--h6-weight` | `700` | `700` | theme |

## Code

The colors of code and of the syntax tokens, all from the palette, and the 1 pixel border.

| Variable | Light | Dark | Set in |
|---|---|---|---|
| `--code-background` | `var(--lex-panel)` | `var(--lex-panel)` | theme |
| `--code-border-width` | `1px` | `1px` | theme |
| `--code-comment` | `var(--lex-faint)` | `var(--lex-faint)` | theme |
| `--code-function` | `var(--lex-warning)` | `var(--lex-warning)` | theme |
| `--code-important` | `var(--lex-error)` | `var(--lex-error)` | theme |
| `--code-keyword` | `var(--lex-accent)` | `var(--lex-accent)` | theme |
| `--code-normal` | `var(--lex-code-normal)` | `var(--lex-code-normal)` | theme |
| `--code-operator` | `var(--lex-muted)` | `var(--lex-muted)` | theme |
| `--code-property` | `var(--lex-code-property)` | `var(--lex-code-property)` | theme |
| `--code-punctuation` | `var(--lex-muted)` | `var(--lex-muted)` | theme |
| `--code-string` | `var(--lex-success)` | `var(--lex-success)` | theme |
| `--code-tag` | `var(--lex-accent)` | `var(--lex-accent)` | theme |
| `--code-value` | `var(--lex-code-value)` | `var(--lex-code-value)` | theme |

## Block quotes

A 4 pixel accent border, like the border of callouts and code blocks.

| Variable | Light | Dark | Set in |
|---|---|---|---|
| `--blockquote-border-color` | `var(--lex-accent)` | `var(--lex-accent)` | theme |
| `--blockquote-border-thickness` | `4px` | `4px` | theme |
| `--blockquote-color` | `var(--lex-ink)` | `var(--lex-ink)` | theme |

## Lists, tasks, and guides

Accent list markers and checkboxes, and warm indentation guides.

| Variable | Light | Dark | Set in |
|---|---|---|---|
| `--checkbox-color` | `var(--lex-accent)` | `var(--lex-accent)` | theme |
| `--checkbox-color-hover` | `var(--lex-accent-hover)` | `var(--lex-accent-hover)` | theme |
| `--indentation-guide-color` | `color-mix(in srgb, var(--lex-sand) 30%, transparent)` | `color-mix(in srgb, var(--lex-sand) 30%, transparent)` | theme |
| `--indentation-guide-color-active` | `color-mix(in srgb, var(--lex-sand) 60%, transparent)` | `color-mix(in srgb, var(--lex-sand) 60%, transparent)` | theme |
| `--list-marker-color` | `var(--text-accent)` | `var(--text-accent)` | theme |

## Interface

Parts of the interface that use a gray or a white in Obsidian: the file list, scrollbars, the drag ghost, toggles, sliders, notices, tooltips, dividers, and the canvas.

| Variable | Light | Dark | Set in |
|---|---|---|---|
| `--canvas-color` | `var(--lex-sand)` | `var(--lex-sand)` | theme |
| `--canvas-dot-pattern` | `color-mix(in srgb, var(--lex-sand) 45%, var(--background-primary))` | `color-mix(in srgb, var(--lex-sand) 45%, var(--background-primary))` | theme |
| `--divider-color` | `color-mix(in srgb, var(--lex-sand) 20%, transparent)` | `color-mix(in srgb, var(--lex-sand) 15%, transparent)` | theme |
| `--drag-ghost-background` | `color-mix(in srgb, var(--lex-ink) 88%, transparent)` | `color-mix(in srgb, var(--lex-ink) 88%, transparent)` | theme |
| `--drag-ghost-text-color` | `var(--lex-ground)` | `var(--lex-ground)` | theme |
| `--nav-item-background-active` | `color-mix(in srgb, var(--lex-accent) 12%, transparent)` | `color-mix(in srgb, var(--lex-accent) 15%, transparent)` | theme |
| `--nav-item-background-selected` | `var(--nav-item-background-active)` | `var(--nav-item-background-active)` | theme |
| `--nav-item-color-active` | `var(--lex-accent)` | `var(--lex-accent)` | theme |
| `--nav-item-color-selected` | `var(--nav-item-color-active)` | `var(--nav-item-color-active)` | theme |
| `--notice-color` | `var(--lex-ground)` | `var(--lex-ink)` | theme |
| `--scrollbar-active-thumb-bg` | `color-mix(in srgb, var(--text-faint) 65%, transparent)` | `color-mix(in srgb, var(--text-faint) 65%, transparent)` | theme |
| `--scrollbar-thumb-bg` | `color-mix(in srgb, var(--text-faint) 40%, transparent)` | `color-mix(in srgb, var(--text-faint) 40%, transparent)` | theme |
| `--slider-thumb-background` | `var(--lex-ground)` | `var(--lex-ground)` | theme |
| `--slider-thumb-background-hover` | `var(--lex-panel)` | `var(--lex-panel)` | theme |
| `--toggle-thumb-color` | `var(--lex-ground)` | `var(--lex-ground)` | theme |
| `--tooltip-color` | `var(--lex-ground)` | `var(--lex-ink)` | theme |

## Graph

The colors of the graph view. Obsidian reads them through hidden elements. See `docs/graph.md`.

| Variable | Light | Dark | Set in |
|---|---|---|---|
| `--graph-line` | `color-mix(in srgb, var(--lex-sand) 45%, transparent)` | `color-mix(in srgb, var(--lex-sand) 35%, transparent)` | theme |
| `--graph-node` | `var(--lex-muted)` | `var(--lex-muted)` | theme |
| `--graph-node-attachment` | `var(--lex-graph-attachment)` | `var(--lex-graph-attachment)` | theme |
| `--graph-node-focused` | `var(--lex-accent)` | `var(--lex-accent)` | theme |
| `--graph-node-tag` | `var(--lex-graph-tag)` | `var(--lex-graph-tag)` | theme |
| `--graph-node-unresolved` | `var(--lex-graph-unresolved)` | `var(--lex-graph-unresolved)` | theme |
| `--graph-text` | `var(--lex-ink)` | `var(--lex-ink)` | theme |

## Base colors

The eight colors that Obsidian uses for callouts, the canvas, and highlights, from the palette.

| Variable | Light | Dark | Set in |
|---|---|---|---|
| `--color-blue` | `var(--lex-blue)` | `var(--lex-blue)` | theme |
| `--color-blue-rgb` | `59, 90, 138` | `138, 166, 214` | theme |
| `--color-cyan` | `var(--lex-cyan)` | `var(--lex-cyan)` | theme |
| `--color-cyan-rgb` | `47, 93, 110` | `127, 179, 196` | theme |
| `--color-green` | `var(--lex-green)` | `var(--lex-green)` | theme |
| `--color-green-rgb` | `58, 99, 41` | `143, 191, 111` | theme |
| `--color-orange` | `var(--lex-orange)` | `var(--lex-orange)` | theme |
| `--color-orange-rgb` | `184, 56, 0` | `255, 122, 69` | theme |
| `--color-pink` | `var(--lex-pink)` | `var(--lex-pink)` | theme |
| `--color-pink-rgb` | `160, 70, 104` | `224, 138, 168` | theme |
| `--color-purple` | `var(--lex-purple)` | `var(--lex-purple)` | theme |
| `--color-purple-rgb` | `107, 74, 125` | `185, 154, 208` | theme |
| `--color-red` | `var(--lex-red)` | `var(--lex-red)` | theme |
| `--color-red-rgb` | `168, 35, 31` | `255, 107, 94` | theme |
| `--color-yellow` | `var(--lex-yellow)` | `var(--lex-yellow)` | theme |
| `--color-yellow-rgb` | `127, 96, 0` | `224, 176, 74` | theme |

## Snippet variables

Set by the snippets: the tag badge and the horizontal rule.

| Variable | Light | Dark | Set in |
|---|---|---|---|
| `--hr-color` | `var(--text-accent)` | `var(--text-accent)` | lexmechanic-fun |
| `--hr-thickness` | `3px` | `3px` | lexmechanic-fun |
| `--tag-background` | `var(--background-primary-alt)` | `var(--background-primary-alt)` | lexmechanic-extras |
| `--tag-border-width` | `0` | `0` | lexmechanic-extras |
| `--tag-color` | `var(--text-accent)` | `var(--text-accent)` | lexmechanic-extras |
| `--tag-radius` | `2px` | `2px` | lexmechanic-extras |
