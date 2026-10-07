# Contributing

This file tells how to change the theme and how to check a change.

## Layout of the repo

* `src/` holds the source of `theme.css`. The files are joined in the order of their names.
  * `10-fonts.css` has the three fonts as base64 data.
  * `20-shared.css` has the variables for both modes.
  * `30-light.css` and `40-dark.css` have the palette and the variables of each mode.
  * `50-rules.css` has the few rules that are not variables.
* `snippets/` holds the two optional snippets.
* `theme.css` is built from `src/`. Do not edit it by hand. Commit it with the change in `src/`.
* `scripts/` holds the checks and the tools. `tests/` holds the unit tests and the baseline. `docs/` holds the notes.

## Build

Edit a file in `src/`, then run one of these commands in the repo folder:

```
./build.sh
python3 build.py
make build
```

Run `./build.sh --check` to test that `theme.css` is up to date. The three commands make the same file.

## Checks

Run `make all`. It builds nothing. It checks that `theme.css` is up to date, runs the unit tests, runs stylelint (it needs `npx`), and checks the contrast and the contrast doc.

Four more checks need Chromium and an installed Obsidian. Run them before you open a pull request that changes a color or a variable:

* `python3 scripts/check_variables.py` lists the variables that the theme sets and Obsidian does not use. It also checks the graph hooks.
* `python3 scripts/check_resolve.py` finds a variable with an empty value, such as a `var()` with a typo.
* `python3 scripts/check_baseline.py` compares the computed styles with `tests/baseline.json`. A change that only moves a rule must show no difference. If the change is meant to alter the look, run it with `--update` and commit the new baseline.
* `python3 scripts/check_graph.py` checks the effective colors of the graph.

The scripts read `app.css` from the installed Obsidian. The repo does not hold that file. `python3 scripts/extract_obsidian_css.py -o app.css` copies it, and it does not start Obsidian.

## Test in Obsidian

Use a vault that you can lose, not your own notes.

```
scripts/install.sh VAULT --link
scripts/dev.sh VAULT
```

The first command links the files into the vault. The second builds and copies the files again after each change. Choose the theme in Settings, Appearance.

## Make a change

* Change a color in the palette (the `--lex-*` variables at the top of `30-light.css` and `40-dark.css`), and every rule follows. Do not put a hex value outside the palette.
* Prefer an Obsidian variable to a CSS rule. Obsidian 1.14.4 has more than 1,100 variables.
* Add a line to `CHANGELOG.md` under Unreleased for a change that people can see.
* Write a short subject in the imperative, such as `Set warm scrollbar colors`. Say in the body what changed and why.

## Pull requests

Open the pull request against `main`. The template has a checklist. The CI workflow runs the checks that do not need Obsidian.
