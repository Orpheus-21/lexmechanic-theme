#!/usr/bin/env python3
"""Compare the computed styles of the theme with a stored baseline.

Usage:
  python3 scripts/check_baseline.py            compare with tests/baseline.json
  python3 scripts/check_baseline.py --update   write a new baseline

The script loads Obsidian's app.css and the theme in headless Chromium, in light and
dark mode. It records the resolved color of every variable that the theme sets and the
computed style of a sample reading view page. A change that moves a rule into a
variable must leave the page as it is, and this script shows when it does not. The
baseline depends on the Obsidian version. The script prints a warning when app.css
differs. It needs Chromium and an installed Obsidian.
"""
import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import browser  # noqa: E402
from check_variables import DATA_URI  # noqa: E402

BASELINE = browser.ROOT / "tests" / "baseline.json"

BODY = """
<div class="markdown-preview-view markdown-rendered"><div class="markdown-preview-sizer">
<div class="inline-title" id="it">Title</div>
<h1 id="h1">H1</h1><h2 id="h2">H2</h2><h3 id="h3">H3</h3><h4 id="h4">H4</h4><h5 id="h5">H5</h5><h6 id="h6">H6</h6>
<p id="p">Text <strong id="strong">bold</strong> <em id="em">ital</em> <mark id="mark">mark</mark> <code id="code">code</code>
<a class="internal-link" id="il" href="#">link</a> <a class="internal-link is-unresolved" id="unres" href="#">unres</a>
<a class="external-link" id="ext" href="#">ext</a> <a class="tag" id="tag" href="#">#tag</a></p>
<blockquote id="bq"><p id="bqp">quote</p></blockquote><hr id="hr"><pre id="pre"><code>x</code></pre>
<ul><li id="li">item</li></ul><ul class="contains-task-list"><li class="task-list-item"><input type="checkbox" class="task-list-item-checkbox" id="cb"></li></ul>
<table id="tbl"><thead><tr id="thr"><th id="th">h</th></tr></thead><tbody><tr><td id="td">d</td></tr></tbody></table>
<div class="callout" data-callout="note" id="co"><div class="callout-title" id="cot"><div class="callout-title-inner" id="coti">Note</div></div><div class="callout-content" id="coc"><p>c</p></div></div>
<div class="callout" data-callout="warning" id="cow"><div class="callout-title"><div class="callout-title-inner">W</div></div></div>
</div></div>
<div class="prompt" id="prompt"><input class="prompt-input" id="pinput"></div>
<div class="cm-content" id="cmc">x</div>
<div class="nav-file-title is-active" id="navact">a</div><div class="nav-file-title" id="navsel">b</div>
"""

SCRIPT = """
const names = %s, props = %s;
const style = getComputedStyle(document.body), probe = document.createElement('div');
document.body.appendChild(probe);
const variables = {};
for (const name of names) {
  probe.style.backgroundColor = 'var(' + name + ')';
  variables[name] = [style.getPropertyValue(name).trim(), getComputedStyle(probe).backgroundColor];
}
const elements = {};
for (const el of document.querySelectorAll('[id]')) {
  if (el.id === 'out') continue;
  const c = getComputedStyle(el);
  elements[el.id] = {};
  for (const p of props) elements[el.id][p] = c[p];
  elements[el.id]['::before.content'] = getComputedStyle(el, '::before').content;
}
document.getElementById('out').textContent = JSON.stringify({variables, elements});
"""

PROPS = ["color", "backgroundColor", "fontFamily", "fontWeight", "fontSize", "lineHeight", "letterSpacing",
         "fontVariantCaps", "fontStyle", "textDecorationLine", "textDecorationStyle", "textDecorationThickness",
         "textDecorationColor", "borderLeftWidth", "borderLeftColor", "borderLeftStyle", "borderTopWidth",
         "borderTopColor", "borderTopStyle", "borderBottomWidth", "borderRadius", "paddingTop", "paddingLeft",
         "marginTop", "marginBottom", "marginLeft", "opacity", "accentColor", "caretColor"]


def all_names():
    text = DATA_URI.sub("", "".join(p.read_text() for p in browser.theme_files()))
    return sorted(set(re.findall(r"(--[a-z0-9-]+)\s*:", text)))


def snapshot():
    with tempfile.TemporaryDirectory() as tmp:
        css = browser.obsidian_css(tmp)
        digest = hashlib.sha256(css.read_bytes()).hexdigest()[:12]
        sheets = [css] + browser.theme_files()
        names = all_names()
        data = {"obsidian_css": digest, "modes": {}}
        for mode in ("light", "dark"):
            script = SCRIPT % (json.dumps(names), json.dumps(PROPS))
            data["modes"][mode] = browser.run(browser.page(mode, sheets, BODY, script))
    return data


def differences(old, new):
    """Return a list of text lines that tell how new differs from old."""
    lines = []
    for mode in new["modes"]:
        for kind in ("variables", "elements"):
            a, b = old["modes"][mode][kind], new["modes"][mode][kind]
            for key in sorted(set(a) | set(b)):
                if key not in a:
                    lines.append(f"{mode} {kind[:-1]} {key}: new")
                elif key not in b:
                    lines.append(f"{mode} {kind[:-1]} {key}: removed")
                elif a[key] != b[key]:
                    if kind == "variables":
                        old_v, new_v = (a[key][1], b[key][1]) if a[key][1] != b[key][1] else (a[key][0], b[key][0])
                        lines.append(f"{mode} variable {key}: {old_v} -> {new_v}")
                    else:
                        for prop in sorted(a[key]):
                            if a[key][prop] != b[key].get(prop):
                                lines.append(f"{mode} #{key}.{prop}: {a[key][prop]} -> {b[key].get(prop)}")
    return lines


def main():
    new = snapshot()
    if "--update" in sys.argv:
        BASELINE.parent.mkdir(exist_ok=True)
        BASELINE.write_text(json.dumps(new, indent=1, sort_keys=True) + "\n")
        print(f"wrote {BASELINE.relative_to(browser.ROOT)}")
        return 0
    old = json.loads(BASELINE.read_text())
    if old["obsidian_css"] != new["obsidian_css"]:
        print(f"warning: the baseline used app.css {old['obsidian_css']}, this run uses {new['obsidian_css']}")
    lines = differences(old, new)
    for line in lines[:60]:
        print(line.replace('"??", ', ""))
    if len(lines) > 60:
        print(f"... and {len(lines) - 60} more")
    print(f"{len(lines)} difference(s) from the baseline")
    return 1 if lines else 0


if __name__ == "__main__":
    sys.exit(main())
