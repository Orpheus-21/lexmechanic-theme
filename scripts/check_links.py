#!/usr/bin/env python3
"""Check the links of the Markdown files.

Usage:
  python3 scripts/check_links.py              check README.md, CHANGELOG.md, CONTRIBUTING.md, and docs/*.md

The script finds each external link (http or https) and each relative link or image,
asks each external address with a HEAD request, and checks that each relative path
exists. It exits with 1 when a link is broken. It needs a network, so run it
on a schedule and not on each push. It uses only the Python standard library.
"""
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINK = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)[^)]*\)|(?<![(\[])<?(https?://[^\s<>)\]]+)")


def links(text):
    """Return the set of link targets in a Markdown text. Code blocks are skipped."""
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"`[^`\n]*`", "", text)
    return {(a or b).rstrip(".,;:") for a, b in LINK.findall(text)}


def ask(url):
    """Return the HTTP status of an address, or a text that tells what went wrong."""
    for method in ("HEAD", "GET"):
        request = urllib.request.Request(url, method=method, headers={"User-Agent": "lexmechanic-link-check"})
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                return response.status
        except urllib.error.HTTPError as error:
            if method == "HEAD" and error.code in (403, 405, 501):
                continue
            return error.code
        except (urllib.error.URLError, TimeoutError) as error:
            return str(error)
    return "no answer"


def main():
    files = [p for p in (ROOT / "README.md", ROOT / "CHANGELOG.md", ROOT / "CONTRIBUTING.md") if p.exists()] + sorted((ROOT / "docs").glob("*.md"))
    broken = 0
    for path in files:
        for target in sorted(links(path.read_text())):
            if target.startswith(("http://", "https://")):
                status = ask(target)
                if status != 200:
                    print(f"{path.relative_to(ROOT)}: {target} -> {status}")
                    broken += 1
            elif not target.startswith(("#", "mailto:")):
                if not (path.parent / target.split("#")[0]).exists():
                    print(f"{path.relative_to(ROOT)}: {target} -> missing file")
                    broken += 1
    print(f"{broken} broken link(s) in {len(files)} file(s)")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
