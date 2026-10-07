#!/bin/sh
# Join the files in src/ into theme.css. Edit the files in src/, then run this script.
# Run "./build.sh --check" to test that theme.css is up to date. It exits with 1 if not.
set -eu
cd "$(dirname "$0")"
ls src/*.css > /dev/null
if [ "${1:-}" = "--check" ]; then
  if cat src/*.css | cmp -s - theme.css; then
    echo "theme.css is up to date"
  else
    echo "theme.css is out of date. Run ./build.sh" >&2
    exit 1
  fi
else
  tmp=$(mktemp theme.css.XXXXXX)
  trap 'rm -f "$tmp"' EXIT
  cat src/*.css > "$tmp"
  chmod 644 "$tmp"
  mv "$tmp" theme.css
  echo "wrote theme.css"
fi
