#!/usr/bin/env python3
"""Check manifest.json and the version of the project.

Usage:
  python3 scripts/check_manifest.py

The script checks that manifest.json is valid JSON, that it has `name`, `version`,
`minAppVersion`, and `author`, that the version has the form x.y.z, and that the
newest version in CHANGELOG.md is the version of the manifest. With --tag NAME it
also checks that the tag is the version, without a leading v (Obsidian matches the tag
to the version). The script exits with 1 when it finds a problem. It uses only the
Python standard library.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIRED = ["name", "version", "minAppVersion", "author"]
VERSION = re.compile(r"\d+\.\d+\.\d+")


def changelog_version(text):
    """Return the newest released version in a changelog, or None. 'Unreleased' is skipped."""
    for m in re.finditer(r"^## \[?([^\]\s]+)\]?", text, re.M):
        if VERSION.fullmatch(m.group(1)):
            return m.group(1)
    return None


def problems(manifest_text, changelog_text, tag=None):
    try:
        manifest = json.loads(manifest_text)
    except json.JSONDecodeError as error:
        return [f"manifest.json is not valid JSON: {error}"]
    found = [f"manifest.json has no {key}" for key in REQUIRED if not manifest.get(key)]
    for key in ("version", "minAppVersion"):
        if manifest.get(key) and not VERSION.fullmatch(manifest[key]):
            found.append(f"{key} {manifest[key]!r} is not of the form x.y.z")
    newest = changelog_version(changelog_text)
    if newest != manifest.get("version"):
        found.append(f"the newest version in CHANGELOG.md is {newest}, the manifest has {manifest.get('version')}")
    if tag is not None and tag != manifest.get("version"):
        found.append(f"the tag {tag!r} is not the version {manifest.get('version')!r}")
    return found


def main():
    tag = sys.argv[sys.argv.index("--tag") + 1] if "--tag" in sys.argv else None
    found = problems((ROOT / "manifest.json").read_text(), (ROOT / "CHANGELOG.md").read_text(), tag)
    for line in found:
        print(line)
    print(f"{len(found)} problem(s)" if found else "manifest.json and CHANGELOG.md agree")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
