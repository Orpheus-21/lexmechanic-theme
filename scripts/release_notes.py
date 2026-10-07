#!/usr/bin/env python3
"""Read and prepare the changelog of a release.

Usage:
  python3 scripts/release_notes.py VERSION             print the notes of VERSION
  python3 scripts/release_notes.py --prepare VERSION   turn Unreleased into VERSION and set the manifest version

--prepare renames the Unreleased heading to `## [VERSION] (DATE)`, adds an empty Unreleased heading above
it, moves the compare links, and writes the version into manifest.json. It changes no other file and makes
no commit. scripts/release.sh calls it, and the release workflow prints the notes with it. It uses only the
Python standard library.
"""
import datetime
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO = "https://github.com/Orpheus-21/lexmechanic-theme"


def notes(text, version):
    """Return the text under the heading of a version, without the heading and the link lines."""
    m = re.search(r"^## \[%s\][^\n]*\n(.*?)(?=^## |^\[[^\]]+\]: )" % re.escape(version), text, re.S | re.M)
    if not m:
        raise ValueError(f"CHANGELOG.md has no section for {version}")
    return m.group(1).strip() + "\n"


def prepare(text, version, date):
    """Return the changelog with the Unreleased section renamed to version."""
    previous = re.search(r"^## \[(\d+\.\d+\.\d+)\]", text, re.M)
    if not previous:
        raise ValueError("CHANGELOG.md has no released version")
    if f"## [{version}]" in text:
        raise ValueError(f"CHANGELOG.md has {version} already")
    body = re.search(r"^## \[Unreleased\]\n(.*?)(?=^## )", text, re.S | re.M)
    if not body or not body.group(1).strip():
        raise ValueError("The Unreleased section is empty")
    text = text.replace("## [Unreleased]\n", f"## [Unreleased]\n\n## [{version}] ({date})\n", 1)
    old = previous.group(1)
    text = re.sub(r"^\[Unreleased\]: .*$", f"[Unreleased]: {REPO}/compare/{version}...HEAD\n[{version}]: {REPO}/compare/{old}...{version}", text, count=1, flags=re.M)
    return text


def main(argv):
    if len(argv) == 1 and not argv[0].startswith("--"):
        print(notes((ROOT / "CHANGELOG.md").read_text(), argv[0]), end="")
        return 0
    if len(argv) == 2 and argv[0] == "--prepare":
        version = argv[1]
        if not re.fullmatch(r"\d+\.\d+\.\d+", version):
            sys.exit("The version has the form x.y.z")
        log = ROOT / "CHANGELOG.md"
        log.write_text(prepare(log.read_text(), version, datetime.date.today().isoformat()))
        manifest = ROOT / "manifest.json"
        data = json.loads(manifest.read_text())
        data["version"] = version
        manifest.write_text(json.dumps(data, indent=2) + "\n")
        print(f"prepared {version}")
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
