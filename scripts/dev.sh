#!/bin/sh
# Rebuild theme.css and copy the files into a vault each time a source file changes.
#
# Usage: scripts/dev.sh VAULT
#
# The script runs ./build.sh and scripts/install.sh VAULT once, and again after each
# change in src/ or snippets/. Obsidian reads a changed theme file at once. It uses
# inotifywait when it is installed, and looks at the file times every second if not.
# Stop it with Ctrl-C.
set -eu
if [ $# -ne 1 ] || [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
  sed -n '2,9p' "$0" | sed 's/^# \{0,1\}//'
  exit 2
fi
vault=$1
repo=$(cd "$(dirname "$0")/.." && pwd)
cd "$repo"
update() {
  ./build.sh > /dev/null && scripts/install.sh "$vault" > /dev/null && echo "$(date +%H:%M:%S) updated $vault"
}
update
if command -v inotifywait > /dev/null 2>&1; then
  while inotifywait -q -r -e modify,create,delete,move src snippets > /dev/null 2>&1; do
    sleep 0.2
    update || true
  done
else
  stamp() { ls -l --time-style=+%s src/*.css snippets/*.css 2> /dev/null | cksum; }
  last=$(stamp)
  while sleep 1; do
    now=$(stamp)
    if [ "$now" != "$last" ]; then last=$now; update || true; fi
  done
fi
