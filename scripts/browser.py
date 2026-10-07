"""Helpers that run a page in headless Chromium and read a JSON result from the DOM.

The page must write its result as JSON text into an element `<pre id="out">`.
Set CHROMIUM to the path of a Chromium or Chrome binary if it is not on PATH.
"""
import html
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from extract_obsidian_css import find_asar, read_file  # noqa: E402


def chromium():
    for name in (os.environ.get("CHROMIUM"), "chromium", "chromium-browser", "google-chrome", "google-chrome-stable", "chrome"):
        if name and shutil.which(name):
            return shutil.which(name)
    sys.exit("Chromium not found. Set CHROMIUM to the path of a Chromium or Chrome binary.")


def obsidian_css(tmp):
    """Write app.css of the installed Obsidian into tmp and return its path."""
    path = Path(tmp) / "app.css"
    path.write_bytes(read_file(find_asar(), "app.css"))
    return path


def theme_files(root=ROOT, extra=()):
    """Return the theme and the snippets, in load order. Extra files, such as a preset, come last."""
    return [root / "theme.css"] + sorted((root / "snippets").glob("*.css")) + [Path(p) for p in extra]


def presets(root=ROOT):
    """Return the preset snippets. Each one is an alternative that you put on top of the theme."""
    return sorted((root / "snippets" / "presets").glob("*.css"))


def page(mode, stylesheets, body, script):
    links = "".join(f'<link rel="stylesheet" href="{Path(p).as_uri()}">' for p in stylesheets)
    return (f'<!doctype html><meta charset="utf-8">{links}<body class="theme-{mode}">{body}'
            f'<pre id="out"></pre><script>{script}</script>')


def run(document, budget=5000):
    """Load an HTML document and return the JSON that its script wrote into #out."""
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "page.html"
        path.write_text(document)
        result = subprocess.run(
            [chromium(), "--headless=new", "--no-sandbox", "--disable-gpu", "--allow-file-access-from-files",
             f"--virtual-time-budget={budget}", "--dump-dom", path.as_uri()],
            capture_output=True, text=True, timeout=180)
    start = result.stdout.find('<pre id="out">')
    if start < 0:
        sys.exit("The page wrote no result. Chromium said: " + result.stderr[-300:])
    end = result.stdout.index("</pre>", start)
    return json.loads(html.unescape(result.stdout[start + len('<pre id="out">'):end]))
