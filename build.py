#!/usr/bin/env python3
"""Join the files in src/ into theme.css. The same job as build.sh, for systems without a POSIX shell.

Usage:
  python3 build.py            write theme.css
  python3 build.py --check    exit with 1 if theme.css is out of date
"""
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def joined():
    files = sorted((ROOT / "src").glob("*.css"))
    if not files:
        sys.exit("src/ has no CSS files")
    return b"".join(f.read_bytes() for f in files)


def main():
    data = joined()
    target = ROOT / "theme.css"
    if "--check" in sys.argv:
        if target.exists() and target.read_bytes() == data:
            print("theme.css is up to date")
            return 0
        print("theme.css is out of date. Run python3 build.py", file=sys.stderr)
        return 1
    fd, tmp = tempfile.mkstemp(prefix="theme.css.", dir=ROOT)
    with os.fdopen(fd, "wb") as f:
        f.write(data)
    os.chmod(tmp, 0o644)
    os.replace(tmp, target)
    print("wrote theme.css")
    return 0


if __name__ == "__main__":
    sys.exit(main())
