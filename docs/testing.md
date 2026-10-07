# Testing

The theme has three kinds of tests. Each one needs more than the one before.

## Unit tests

Run `python3 -m unittest discover -s tests`. They need only Python 3. They test the scripts: the contrast math, the color math, the parsers, the generators, and that `theme.css` is the join of `src/`. The CI workflow runs them.

`make all` runs the unit tests, the build check, stylelint, and the contrast checks.

## Checks in headless Chromium

These scripts load Obsidian's own `app.css` and the theme in headless Chromium, in light and dark mode. They need Chromium (set `CHROMIUM` to its path if it is not on `PATH`) and an installed Obsidian. They do not start Obsidian.

* `scripts/check_variables.py` lists the variables that the theme sets and Obsidian does not use, and checks the graph hooks.
* `scripts/check_resolve.py` finds a variable with an empty value, such as a `var()` with a typo.
* `scripts/check_baseline.py` records the resolved color of every variable and the computed style of a sample reading view page. It compares them with `tests/baseline.json`.
* `scripts/check_graph.py` reads the 11 graph hooks and checks the effective contrast.
* `scripts/check_screenshots.py` takes a screenshot of the sample page in both modes and compares it with `tests/screenshots/`. It finds a change of the look that no computed property shows. The images belong to one machine, because the Chromium version and the system fonts change them.

`scripts/extract_obsidian_css.py` copies `app.css` out of an asar file. The repo does not hold that file, because it belongs to Obsidian.

The baseline depends on the Obsidian version. When a change must alter the look, run `python3 scripts/check_baseline.py` to read the differences, and then `python3 scripts/check_baseline.py --update`. The new baseline goes into the same commit. When a change only moves a rule into a variable, the run must show no difference.

## Tests in the real Obsidian

Some things only show in the real app: Live Preview, the settings window, the graph, and the canvas. Use a temporary window with its own profile and its own vault. This method needs a screen.

1. Make a demo vault and install the theme: `python3 scripts/make_demo_vault.py DIR`, then `scripts/install.sh DIR`.
2. Make a profile folder `PROFILE`. Put a file `obsidian.json` in it that lists the vault and says `"open": true`:

```
{"vaults": {"demo0000000001": {"path": "DIR", "ts": 1, "open": true}}}
```

3. Copy the newest `obsidian-*.asar` of `~/.config/obsidian` into `PROFILE`, so that the same app version loads.
4. Start Obsidian with the profile and a debug port. The command depends on the system. On Linux with the Electron package it looks like this:

```
electron43 /usr/lib/obsidian/app.asar --user-data-dir=PROFILE --remote-debugging-port=9333 --remote-allow-origins='*'
```

5. Control the window with `node scripts/cdp.mjs SCRIPT.mjs`. The script can run JavaScript in the page, which has the global `app` of Obsidian, and can take screenshots. For example, `app.changeTheme('moonstone')` switches to light mode and `app.workspace.openLinkText('Note', '', false)` opens a note.
6. Stop the window. Stop the processes whose command line has the path of `PROFILE`. Then delete the profile and the demo vault.

### Safety rules

* Always start Obsidian with `--user-data-dir`. Without it, even `obsidian --version` starts the app on your normal profile and opens your last vault.
* Never test in a vault that holds your notes. Use the demo vault, or a copy.
* The debug port gives full control of the window. Use it only on this machine, and stop the window when you are done.
* Do not use `pkill -f` with a pattern that your own command line contains. Find the process ids first.

The method was tested with Obsidian 1.14.4 and Node 26. `scripts/cdp.mjs` needs Node 22 or newer.

### Scripts for the window

* `python3 scripts/obsidian_window.py start` does steps 1 to 4 for you. It makes the demo vault and a separate profile, and it starts the window. The commands `reload`, `theme`, `open`, `eval`, `shot`, and `run` control it. `stop --clean` stops only the process group that `start` made. It also tells you if your own Obsidian config or vault files changed.
* `python3 scripts/check_graph_pixels.py` opens a graph in the window and compares the pixel of a free node of each type with the color that the theme sets. It needs a running window.
* `python3 scripts/take_screenshots.py` makes the images of the README in `docs/images/`: the note in reading view in both modes, Live Preview, the graph in both modes, the note on a phone in both modes, and the Appearance page of Settings. It needs a running window.
* The mobile emulation of Obsidian (`app.emulateMobile(true)` with `Emulation.setDeviceMetricsOverride` and `mobile: true`) shows the layout of a phone. It does not show safe areas, touch, or the WebView of a real phone.
* A window that Obsidian opens for Settings has the address `about:blank`. Set `CDP_TARGET=Settings` to control it with `scripts/cdp.mjs`.
