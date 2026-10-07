#!/usr/bin/env python3
"""Write the app.css of an installed Obsidian to a file.

Usage:
  python3 scripts/extract_obsidian_css.py                 print the path of a temporary copy
  python3 scripts/extract_obsidian_css.py -o app.css      write the file to a path
  python3 scripts/extract_obsidian_css.py --asar FILE     read a given asar file
  python3 scripts/extract_obsidian_css.py --file app.js   extract another file of the asar

The script reads the asar header and copies one file. It does not start Obsidian.
Without --asar it uses the newest update in the Obsidian config folder, and then
the installed obsidian.asar. It uses only the Python standard library.
"""
import argparse
import json
import os
import struct
import sys
import tempfile
from pathlib import Path


def find_asar():
    config = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "obsidian"
    updates = sorted(config.glob("obsidian-*.asar"), key=lambda p: [int(x) for x in p.stem[9:].split(".") if x.isdigit()])
    candidates = updates[-1:] + [
        Path("/usr/lib/obsidian/obsidian.asar"),
        Path("/opt/Obsidian/resources/obsidian.asar"),
        Path("/Applications/Obsidian.app/Contents/Resources/obsidian.asar"),
        Path(os.environ.get("LOCALAPPDATA", "")) / "Obsidian" / "resources" / "obsidian.asar",
    ]
    for path in candidates:
        if path.is_file():
            return path
    sys.exit("No Obsidian asar file found. Use --asar FILE.")


def read_file(asar, name):
    with open(asar, "rb") as f:
        f.read(12)
        size = struct.unpack("<I", f.read(4))[0]
        header = json.loads(f.read(size))
        entry = header
        for part in name.split("/"):
            if part not in entry.get("files", {}):
                sys.exit(f"{name} is not in {asar}")
            entry = entry["files"][part]
        f.seek(16 + size + int(entry["offset"]))
        return f.read(entry["size"])


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--asar", type=Path)
    parser.add_argument("--file", default="app.css")
    parser.add_argument("-o", "--output", type=Path)
    args = parser.parse_args()
    asar = args.asar or find_asar()
    if not asar.is_file():
        sys.exit(f"{asar} is not a file.")
    data = read_file(asar, args.file)
    if args.output:
        out = args.output
        out.write_bytes(data)
    else:
        out = Path(tempfile.mkdtemp(prefix="obsidian-css-")) / Path(args.file).name
        out.write_bytes(data)
    print(out)
    print(f"from {asar} ({len(data)} bytes)", file=sys.stderr)


if __name__ == "__main__":
    main()
