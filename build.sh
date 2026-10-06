#!/bin/sh
# Join the files in src/ into theme.css. Edit the files in src/, then run this script.
# Run "./build.sh --check" to test that theme.css is up to date. It exits with 1 if not.
cd "$(dirname "$0")" || exit 1
if [ "$1" = "--check" ]; then
  cat src/*.css | cmp -s - theme.css
else
  cat src/*.css > theme.css
fi
