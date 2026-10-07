#!/bin/sh
# Install the theme and the snippets into a vault.
#
# Usage: scripts/install.sh VAULT [--link]
#
# VAULT is the folder of the vault, the one that holds the hidden .obsidian folder.
# The script copies manifest.json and theme.css to VAULT/.obsidian/themes/Lexmechanic/ and the
# files of snippets/ to VAULT/.obsidian/snippets/. With --link it makes symbolic links in place
# of copies, so that a build in this repo reaches the vault at once. It does not turn the
# theme on: choose it in Settings, Appearance.
set -eu
if [ $# -lt 1 ] || [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
  sed -n '2,10p' "$0" | sed 's/^# \{0,1\}//'
  exit 2
fi
vault=$1
mode=${2:-copy}
repo=$(cd "$(dirname "$0")/.." && pwd)
if [ ! -d "$vault/.obsidian" ]; then
  echo "$vault has no .obsidian folder. Open the vault in Obsidian once, or check the path." >&2
  exit 1
fi
theme="$vault/.obsidian/themes/Lexmechanic"
snippets="$vault/.obsidian/snippets"
mkdir -p "$theme" "$snippets"
put() {
  if [ "$mode" = "--link" ]; then
    ln -sf "$1" "$2/$(basename "$1")"
  else
    rm -f "$2/$(basename "$1")"
    cp "$1" "$2/"
  fi
}
for file in manifest.json theme.css; do put "$repo/$file" "$theme"; done
for file in "$repo"/snippets/*.css; do put "$file" "$snippets"; done
echo "installed into $vault/.obsidian ($mode)"
