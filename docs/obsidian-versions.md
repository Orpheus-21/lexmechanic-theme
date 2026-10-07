# Obsidian versions

Obsidian changes its variables from one version to the next. This page lists the changes that touch the theme. The theme is tested with Obsidian 1.14.4. The page compares it with 1.13.7.

## From 1.13.7 to 1.14.4

Obsidian 1.14.4 removed 3 variables and added 84. The list comes from `scripts/diff_obsidian_variables.py`.

Removed:

* `--text-highlight-bg-rgb`. Older versions did not read it either, so deleting it from the theme costs nothing.
* `--text-highlight-bg`. Obsidian no longer defines it, but the new `--highlight-background` reads it as a fallback. The theme still sets it, and highlights still use it.
* `--settings-home-background`. The theme does not set it.

Added, and what the theme does about them:

* `--highlight-background`, its colored forms (`-red`, `-orange`, `-yellow`, `-green`, `-blue`, `-purple`), and `--highlight-opacity` (30%). The colored forms mix the base colors of the theme, so the theme does not set these.
* `--notice-*` and `--tooltip-*`. The theme sets `--notice-color` and `--tooltip-color`, because the default text color is `#FAFAFA`. An older Obsidian ignores these two.
* `--tab-background`, `--tab-inner-*`, and other tab variables. The theme does not set them.
* `--hotkey-*`, `--bases-kanban-*`, `--setting-item-name-*`, `--color-secondary-2` to `--color-secondary-6`, and a few more. The theme does not set them.

## Unchanged

* The eight `--graph-*` variables and the 11 `.graph-view.color-*` hook classes are the same in both versions.
* `--callout-color` is a full color in both versions, not an RGB triple. The first version of the extras snippet used `rgb(var(--callout-color))`, which is not valid, and so the callout border did not show. The snippet is fixed.

## The installer and the app

Obsidian has two version numbers. The app updates itself, and the installer is a different download that you update by hand. The installer holds Electron, and Electron holds Chromium. The theme needs Chromium 111 for `color-mix()`. Installer 1.4.13 has Electron 25.8.1.

## How to compare a new version

1. Get the `app.css` of the old and the new version with `python3 scripts/extract_obsidian_css.py --asar FILE -o app.css`.
2. Run `python3 scripts/diff_obsidian_variables.py OLD.css NEW.css`.
3. Run `python3 scripts/check_variables.py --css NEW.css` to see which variables of the theme the new version does not use.

The workflow `.github/workflows/obsidian-versions.yml` runs step 3 each week against the newest Obsidian.
