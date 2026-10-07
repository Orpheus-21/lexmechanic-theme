#!/usr/bin/env python3
"""Compare screenshots of a sample page with stored images.

Usage:
  python3 scripts/check_screenshots.py            compare with tests/screenshots/
  python3 scripts/check_screenshots.py --update   write new images

The script loads Obsidian's app.css and the theme in headless Chromium, takes a screenshot of
the sample page of check_baseline.py in light and in dark mode, and compares each one with the
stored image. A pixel differs when a channel is off by more than 8. The check fails when more than
0.005% of the pixels differ (about 45 pixels of the page). Two runs on one machine give no difference at all, and
a quote border that is 9 pixels wide instead of 4 changes 620 pixels. The numbers of check_baseline.py do not show a change of the look
that no property reveals, and this check does. The images depend on the Obsidian version, the
Chromium version, and the fonts of the system, so keep them for one machine. The script
needs Chromium and an installed Obsidian, and it uses only the Python standard library.
"""
import struct
import subprocess
import sys
import tempfile
import zlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import browser  # noqa: E402
from check_baseline import BODY  # noqa: E402

DIR = browser.ROOT / "tests" / "screenshots"
OUT = browser.ROOT / "tests" / "output"
SIZE = (820, 1100)
TOLERANCE = 8
MAX_FRACTION = 0.00005


def read_png(data):
    """Decode a PNG of 8 bit RGB or RGBA without interlace. Return (width, height, bytes per pixel, rows)."""
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file")
    pos, idat = 8, b""
    while pos < len(data):
        size = struct.unpack(">I", data[pos:pos + 4])[0]
        kind, chunk = data[pos + 4:pos + 8], data[pos + 8:pos + 8 + size]
        pos += 12 + size
        if kind == b"IHDR":
            width, height, depth, ctype, _, _, interlace = struct.unpack(">IIBBBBB", chunk)
        elif kind == b"IDAT":
            idat += chunk
    if depth != 8 or ctype not in (2, 6) or interlace:
        raise ValueError("only 8 bit RGB and RGBA PNG files without interlace are supported")
    bpp = 3 if ctype == 2 else 4
    stride = width * bpp
    raw = zlib.decompress(idat)
    rows, prev = [], bytearray(stride)
    for y in range(height):
        kind = raw[y * (stride + 1)]
        line = bytearray(raw[y * (stride + 1) + 1:(y + 1) * (stride + 1)])
        for i in range(stride):
            a = line[i - bpp] if i >= bpp else 0
            b = prev[i]
            c = prev[i - bpp] if i >= bpp else 0
            if kind == 1:
                line[i] = (line[i] + a) & 255
            elif kind == 2:
                line[i] = (line[i] + b) & 255
            elif kind == 3:
                line[i] = (line[i] + (a + b) // 2) & 255
            elif kind == 4:
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                line[i] = (line[i] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 255
        rows.append(line)
        prev = line
    return width, height, bpp, rows


def compare(first, second, tolerance=TOLERANCE):
    """Return (number of differing pixels, number of pixels, bounding box or None) for two PNG files."""
    w1, h1, bpp1, rows1 = read_png(first)
    w2, h2, bpp2, rows2 = read_png(second)
    if (w1, h1) != (w2, h2):
        return w1 * h1, w1 * h1, (0, 0, w1, h1)
    count, box = 0, None
    for y in range(h1):
        a, b = rows1[y], rows2[y]
        if a == b:
            continue
        for x in range(w1):
            pa, pb = a[x * bpp1:x * bpp1 + 3], b[x * bpp2:x * bpp2 + 3]
            if max(abs(pa[0] - pb[0]), abs(pa[1] - pb[1]), abs(pa[2] - pb[2])) > tolerance:
                count += 1
                box = (x, y, x, y) if box is None else (min(box[0], x), min(box[1], y), max(box[2], x), max(box[3], y))
    return count, w1 * h1, box


def shoot(mode, css, target):
    sheets = [css] + browser.theme_files()
    # The prompt, the editor line, and the file list items are for the style test only, and they overlap the page.
    hide = "<style>#prompt, #cmc, #navact, #navsel { display: none; }</style>"
    html = browser.page(mode, sheets, hide + BODY, "").replace("<body", '<body style="margin:0"', 1)
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "page.html"
        path.write_text(html)
        subprocess.run([browser.chromium(), "--headless=new", "--no-sandbox", "--disable-gpu", "--allow-file-access-from-files",
                        "--hide-scrollbars", "--force-device-scale-factor=1", f"--window-size={SIZE[0]},{SIZE[1]}",
                        "--virtual-time-budget=4000", f"--screenshot={target}", path.as_uri()],
                       capture_output=True, timeout=180)


def main():
    update = "--update" in sys.argv
    bad = 0
    with tempfile.TemporaryDirectory() as tmp:
        css = browser.obsidian_css(tmp)
        for mode in ("light", "dark"):
            stored = DIR / f"{mode}.png"
            new = (DIR if update else OUT) / f"{mode}.png"
            new.parent.mkdir(parents=True, exist_ok=True)
            shoot(mode, css, new)
            if update:
                print(f"wrote {new.relative_to(browser.ROOT)}")
                continue
            count, total, box = compare(stored.read_bytes(), new.read_bytes())
            share = count / total
            verdict = "ok" if share <= MAX_FRACTION else "FAIL"
            print(f"{mode}: {count} of {total} pixels differ ({share:.3%}) {verdict}" + (f", box {box}" if box else ""))
            bad += verdict == "FAIL"
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
