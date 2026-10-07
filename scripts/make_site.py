#!/usr/bin/env python3
"""Write docs/index.html, the landing page of the project for GitHub Pages.

Usage:
  python3 scripts/make_site.py              print the page
  python3 scripts/make_site.py --write      write docs/index.html, docs/.nojekyll, and a copy of screenshot.png in docs/images/
  python3 scripts/make_site.py --check-doc  exit 1 if the page is out of date

The page shows the real palette. The script reads the --lex-* variables of src/30-light.css and
src/40-dark.css, so a color change reaches the page at the next run. It also counts the presets and reads
the version of manifest.json. The screenshots are the files of docs/images/. It uses only the Python
standard library.
"""
import html
import json
import shutil
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import check_contrast as c  # noqa: E402

TARGET = ROOT / "docs" / "index.html"
GROUPS = [
    ("Ground", ["ground", "panel", "panel-alt"]),
    ("Ink", ["ink", "muted", "faint", "sand"]),
    ("Accent", ["accent", "accent-hover"]),
    ("Status", ["error", "warning", "success"]),
    ("Base", ["red", "orange", "yellow", "green", "cyan", "blue", "purple", "pink"]),
    ("Graph", ["graph-node", "graph-tag", "graph-attachment", "graph-unresolved", "graph-line", "graph-highlight"]),
]

CSS = """
:root {
  --ground: %(l-ground)s; --panel: %(l-panel)s; --ink: %(l-ink)s; --muted: %(l-muted)s; --rule: %(l-sand)s; --accent: %(l-accent)s;
}
@media (prefers-color-scheme: dark) {
  :root { --ground: %(d-ground)s; --panel: %(d-panel)s; --ink: %(d-ink)s; --muted: %(d-muted)s; --rule: %(d-sand)s; --accent: %(d-accent)s; }
}
* { box-sizing: border-box; }
html { background: var(--ground); color: var(--ink); }
body { margin: 0; font: 1.125rem/1.6 'Iowan Old Style', 'Palatino Linotype', Palatino, 'Book Antiqua', Georgia, serif; }
a { color: var(--accent); text-underline-offset: 0.2em; }
a:focus-visible, summary:focus-visible { outline: 3px solid var(--accent); outline-offset: 3px; }
.skip { position: absolute; left: -999px; }
.skip:focus { left: 1rem; top: 1rem; background: var(--panel); padding: 0.5rem 1rem; }
header, main, footer { max-width: 62rem; margin: 0 auto; padding: 0 1.5rem; }
header { padding-top: 4rem; }
h1 { font-size: clamp(3rem, 9vw, 6.5rem); line-height: 0.95; margin: 0 0 1.5rem; letter-spacing: -0.03em; font-weight: 700; }
h1 span { color: var(--accent); }
h2 { font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.14em; margin: 4.5rem 0 1.25rem; padding-top: 1rem; border-top: 3px solid var(--accent); font-family: ui-monospace, 'SF Mono', Consolas, monospace; font-weight: 600; }
p { max-width: 38rem; margin: 0 0 1rem; }
.lede { font-size: 1.5rem; line-height: 1.4; max-width: 40rem; }
.hero { margin: 2.5rem 0 0; border: 1px solid var(--rule); }
img { max-width: 100%%; height: auto; display: block; }
figure { margin: 0; }
figcaption { font: 0.85rem/1.4 ui-monospace, 'SF Mono', Consolas, monospace; color: var(--muted); padding-top: 0.5rem; }
.views { display: grid; grid-template-columns: 2fr 1fr; gap: 2rem; align-items: start; margin-top: 1.5rem; }
.views .wide { grid-column: 1 / -1; display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; }
.views img { border: 1px solid var(--rule); }
.phone { max-width: 15rem; }
.palette { display: grid; grid-template-columns: repeat(auto-fill, minmax(11rem, 1fr)); gap: 0 2rem; }
.palette h3 { font: 600 0.8rem ui-monospace, 'SF Mono', Consolas, monospace; margin: 1.5rem 0 0.5rem; color: var(--muted); grid-column: 1 / -1; }
.pair { display: flex; align-items: center; gap: 0.6rem; font: 0.8rem/1.2 ui-monospace, 'SF Mono', Consolas, monospace; margin: 0 0 0.6rem; }
.pair .sw { display: flex; flex: none; }
.pair i { width: 1.3rem; height: 1.8rem; border: 1px solid var(--rule); }
.pair b { display: block; font-weight: 600; }
.pair small { color: var(--muted); font-size: 0.75rem; }
pre { background: var(--panel); border-left: 4px solid var(--accent); padding: 1rem 1.25rem; overflow-x: auto; font: 0.9rem/1.5 ui-monospace, 'SF Mono', Consolas, monospace; margin: 0 0 1.5rem; }
dl { display: grid; grid-template-columns: max-content 1fr; gap: 0.5rem 2rem; margin: 0; }
dt { font: 600 0.9rem ui-monospace, 'SF Mono', Consolas, monospace; }
dd { margin: 0; }
ol.steps { list-style: none; padding: 0; counter-reset: s; }
ol.steps li { counter-increment: s; display: grid; grid-template-columns: 3.5rem 1fr; margin-bottom: 1rem; }
ol.steps li::before { content: counter(s); font-size: 2.6rem; line-height: 1; color: var(--accent); font-weight: 700; }
footer { padding-top: 3rem; padding-bottom: 4rem; color: var(--muted); font-size: 0.95rem; }
@media (max-width: 40rem) {
  .views, .views .wide { grid-template-columns: 1fr; }
  dl { grid-template-columns: 1fr; gap: 0; }
  dd { margin-bottom: 0.8rem; }
}
"""


def palette():
    css = {m: (ROOT / "src" / f"{'30-light' if m == 'light' else '40-dark'}.css").read_text() for m in ("light", "dark")}
    blocks = {m: c.read_blocks(css[m] if False else (ROOT / "theme.css").read_text())[m] for m in ("light", "dark")}
    shared = c.shared_block((ROOT / "theme.css").read_text())
    out = {}
    for mode, block in blocks.items():
        values = {**shared, **block}
        out[mode] = {k[6:]: c.resolve(k, values) for k in block if k.startswith("--lex-") and c.resolve(k, values)}
    return out


def swatches(colors):
    parts = []
    for title, names in GROUPS:
        parts.append(f"<h3>{html.escape(title)}</h3>")
        for n in names:
            lo, da = colors["light"].get(n), colors["dark"].get(n)
            if not lo:
                continue
            parts.append(f'<div class="pair"><span class="sw"><i style="background:{lo}" title="light {lo}"></i><i style="background:{da}" title="dark {da}"></i></span>'
                         f'<span><b>{html.escape(n)}</b><small>{lo} · {da}</small></span></div>')
    return "\n".join(parts)


def render():
    colors = palette()
    version = json.loads((ROOT / "manifest.json").read_text())["version"]
    presets = len(list((ROOT / "snippets" / "presets").glob("*.css")))
    names = len({n for m in colors.values() for n in m})
    css = CSS % {f"{m[0]}-{k}": colors[m][k] for m in colors for k in ("ground", "panel", "ink", "muted", "sand", "accent")}
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Lexmechanic, a theme for Obsidian</title>
<meta name="description" content="Lexmechanic is an Obsidian theme with a warm paper ground, dark brown text, and a red ink accent.">
<style>{css}</style>
</head>
<body>
<a class="skip" href="#main">Skip to the content</a>
<header>
<h1>Lexmechanic<span>.</span></h1>
<p class="lede">An Obsidian theme. It sets a paper ground, dark brown text, and a red ink accent in light mode and in dark mode. Version {version}.</p>
<figure class="hero"><img src="images/screenshot.png" alt="A note in reading view, in light mode on the left and in dark mode on the right" width="1600" height="900"><figcaption>Reading view in Obsidian 1.14.4. Light mode left, dark mode right.</figcaption></figure>
</header>
<main id="main">
<h2>Views</h2>
<p>Every image comes from a demo vault. <code>scripts/take_screenshots.py</code> makes them again.</p>
<div class="views">
<figure><img src="images/live-preview-light.png" alt="Live Preview in light mode" width="1280" height="800"><figcaption>Live Preview, light. The line of the cursor has a red tint.</figcaption></figure>
<figure class="phone"><img src="images/mobile-dark.png" alt="A note on a phone in dark mode" width="780" height="1688"><figcaption>Phone, dark. This is the mobile emulation of Obsidian.</figcaption></figure>
<div class="wide">
<figure><img src="images/graph-light.png" alt="The graph view in light mode" width="1280" height="800"><figcaption>Graph, light. Tags are teal, attachments are rust.</figcaption></figure>
<figure><img src="images/graph-dark.png" alt="The graph view in dark mode" width="1280" height="800"><figcaption>Graph, dark.</figcaption></figure>
</div>
</div>

<h2>Palette</h2>
<p>The theme has {names} named colors in <code>src/30-light.css</code> and <code>src/40-dark.css</code>. Each pair below is the light color, then the dark color. A color change there reaches every rule. Text colors reach 4.5 to 1 on the page, with three known exceptions that <code>docs/contrast.md</code> lists.</p>
<div class="palette">
{swatches(colors)}
</div>

<h2>Install</h2>
<ol class="steps">
<li><div>Copy the theme into a vault. The folder <code>.obsidian</code> must exist in the vault.</div></li>
<li><div>Open Settings, Appearance. Choose Lexmechanic under Themes.</div></li>
<li><div>Optional: turn on the snippets <code>lexmechanic-extras</code> and <code>lexmechanic-fun</code>, and any of the {presets} presets.</div></li>
</ol>
<pre>git clone https://github.com/Orpheus-21/lexmechanic-theme.git
cd lexmechanic-theme
scripts/install.sh /path/to/vault --presets</pre>
<p>On Windows, run <code>.\\scripts\\install.ps1 -Vault "C:\\path\\to\\vault" -Presets</code>. It is not tested on Windows. The plugin BRAT can install the theme alone.</p>

<h2>Limits</h2>
<dl>
<dt>Obsidian</dt><dd>Installer 1.4.13 or newer. The theme uses <code>color-mix()</code>, which needs Chromium 111.</dd>
<dt>Tested</dt><dd>Obsidian 1.14.4 on Linux. Windows, macOS, Android, and iOS are not tested.</dd>
<dt>Fonts</dt><dd>Volume Tc has about 175 characters. Other characters use a fallback font.</dd>
<dt>Graph labels</dt><dd>Obsidian fixes the font of the labels. The preset <code>lexmechanic-graph-labels</code> replaces it.</dd>
<dt>Options</dt><dd>The plugin Style Settings shows the accent, the column width, the fonts, the heading sizes, and the graph colors.</dd>
</dl>
</main>
<footer>
<p><a href="https://github.com/Orpheus-21/lexmechanic-theme">Source on GitHub</a>. <a href="https://github.com/Orpheus-21/lexmechanic-theme/blob/main/docs/palette.md">Palette</a>, <a href="https://github.com/Orpheus-21/lexmechanic-theme/blob/main/docs/variables.md">variables</a>, <a href="https://github.com/Orpheus-21/lexmechanic-theme/blob/main/docs/graph.md">graph</a>, and <a href="https://github.com/Orpheus-21/lexmechanic-theme/blob/main/docs/testing.md">testing</a> are in the repo. GPL 3 license.</p>
</footer>
</body>
</html>
"""


def main():
    text = render()
    if "--write" in sys.argv:
        TARGET.write_text(text)
        (ROOT / "docs" / ".nojekyll").write_text("")
        shutil.copyfile(ROOT / "screenshot.png", ROOT / "docs" / "images" / "screenshot.png")
        print(f"wrote {TARGET.relative_to(ROOT)}")
    elif "--check-doc" in sys.argv:
        copy = ROOT / "docs" / "images" / "screenshot.png"
        if not TARGET.exists() or TARGET.read_text() != text or not copy.exists() or copy.read_bytes() != (ROOT / "screenshot.png").read_bytes():
            print("docs/index.html is out of date. Run: python3 scripts/make_site.py --write")
            return 1
        print("docs/index.html is up to date")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
