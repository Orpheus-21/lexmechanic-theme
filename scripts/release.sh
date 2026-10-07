#!/bin/sh
# Make a release: prepare the changelog and the manifest, run the checks, commit, and tag.
#
# Usage: scripts/release.sh VERSION
#
# VERSION has the form x.y.z. The script must run on the main branch with a clean tree. It does these steps:
# it turns Unreleased in CHANGELOG.md into VERSION, writes VERSION into manifest.json, makes docs/index.html again (it shows the version), runs `make all`,
# runs scripts/check_manifest.py, makes the commit `Release VERSION`, and makes the tag VERSION. Then it
# asks before it pushes. The push of the tag starts the release workflow, which makes the GitHub release.
set -eu
if [ $# -ne 1 ]; then
  sed -n '2,9p' "$0" | sed 's/^# \{0,1\}//'
  exit 2
fi
version=$1
cd "$(dirname "$0")/.."
case "$version" in
  [0-9]*.[0-9]*.[0-9]*) ;;
  *) echo "The version has the form x.y.z" >&2; exit 2 ;;
esac
[ "$(git branch --show-current)" = "main" ] || { echo "Run this on the main branch." >&2; exit 1; }
[ -z "$(git status --porcelain)" ] || { echo "The working tree is not clean." >&2; exit 1; }
git rev-parse "$version" >/dev/null 2>&1 && { echo "The tag $version exists." >&2; exit 1; }
python3 scripts/release_notes.py --prepare "$version"
python3 scripts/make_site.py --write
make all
python3 scripts/check_manifest.py
git add CHANGELOG.md manifest.json docs/index.html
git commit -m "Release $version"
git tag "$version"
echo "Made the commit and the tag $version."
printf 'Push main and the tag now? [y/N] '
read -r answer
if [ "$answer" = "y" ]; then
  git push origin main "$version"
else
  echo "Not pushed. Run: git push origin main $version"
fi
