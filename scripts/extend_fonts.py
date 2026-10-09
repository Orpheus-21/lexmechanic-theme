#!/usr/bin/env python3
"""Add the missing common characters to the three embedded fonts of src/10-fonts.css.

Usage:
  /path/to/python scripts/extend_fonts.py              add the glyphs, print what was added
  /path/to/python scripts/extend_fonts.py --dry-run    print what would be added, change nothing

Volume Tc and Volume Tc Sans have no em dash, en dash, ellipsis, bullet, multiplication sign, division
sign, degree sign, plus or minus sign, superscript two and three, one half, a and A with ring, and arrows.
Each such character used to come from a fallback font. This script draws them from the outlines that the
fonts already have: bars with the weight of the hyphen, dots like the period, the digits scaled for the
superscripts, and the letter a or A with a ring. It skips a character that the font has, so a second
run changes nothing. It needs the package fonttools: `pip install fonttools`. The unit
tests of the repo skip the tests of this file when fonttools is missing.
"""
import base64
import io
import math
import re
import sys
from pathlib import Path

from fontTools.pens.transformPen import TransformPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
CSS = ROOT / "src" / "10-fonts.css"
DATA = re.compile(r"(url\('data:font/woff;base64,)([A-Za-z0-9+/=]+)('\))")
K = 0.5522847498  # control point factor of a circle made from four cubic curves


def bounds(glyphs, name):
    pen = BoundsPen(glyphs)
    glyphs[name].draw(pen)
    return pen.bounds


def rect(pen, x0, y0, x1, y1):
    pen.moveTo((x0, y0))
    pen.lineTo((x0, y1))
    pen.lineTo((x1, y1))
    pen.lineTo((x1, y0))
    pen.closePath()


def circle(pen, cx, cy, r, clockwise=True):
    k = K * r
    pts = [((cx + r, cy), (cx + r, cy + k), (cx + k, cy + r), (cx, cy + r)),
           ((cx, cy + r), (cx - k, cy + r), (cx - r, cy + k), (cx - r, cy)),
           ((cx - r, cy), (cx - r, cy - k), (cx - k, cy - r), (cx, cy - r)),
           ((cx, cy - r), (cx + k, cy - r), (cx + r, cy - k), (cx + r, cy))]
    if clockwise:  # the points above go counter clockwise, so reverse them
        pts = [(b[3], b[2], b[1], b[0]) for b in reversed(pts)]
    pen.moveTo(pts[0][0])
    for _, c1, c2, end in pts:
        pen.curveTo(c1, c2, end)
    pen.closePath()


def ring(pen, cx, cy, outer, inner):
    circle(pen, cx, cy, outer, clockwise=True)
    circle(pen, cx, cy, inner, clockwise=False)


def bar(pen, x0, y0, x1, y1, t):
    """A bar of thickness t from (x0, y0) to (x1, y1), with square ends."""
    dx, dy = x1 - x0, y1 - y0
    n = math.hypot(dx, dy)
    ox, oy = -dy / n * t / 2, dx / n * t / 2
    pen.moveTo((x0 + ox, y0 + oy))
    pen.lineTo((x1 + ox, y1 + oy))
    pen.lineTo((x1 - ox, y1 - oy))
    pen.lineTo((x0 - ox, y0 - oy))
    pen.closePath()


def draw_glyph(glyphs, name, matrix, pen):
    glyphs[name].draw(TransformPen(pen, matrix))


def build(font):
    """Return {codepoint: (glyph name, advance, draw function)} for the font."""
    glyphs = font.getGlyphSet()
    cmap = font.getBestCmap()
    n = lambda ch: cmap[ord(ch)]  # noqa: E731
    hy = bounds(glyphs, n("-"))
    t = hy[3] - hy[1]  # the weight of the hyphen
    yc = (hy[3] + hy[1]) / 2  # its height
    xh = font["OS/2"].sxHeight
    cap = font["OS/2"].sCapHeight
    period = bounds(glyphs, n("."))
    pw = period[2] - period[0]
    pa = font["hmtx"][n(".")][0]
    plus = bounds(glyphs, n("+"))
    axis = (plus[1] + plus[3]) / 2  # the height of the center of the plus sign
    arm = (plus[2] - plus[0]) / 2  # half the width of the plus sign
    stem = max(t, 0.9 * (plus[2] - plus[0]) / 8)
    out = {}

    def dash(width, side):
        def draw(pen):
            rect(pen, side, yc - t / 2, width - side, yc + t / 2)
        return draw
    out[0x2013] = ("endash", 520, dash(520, 20))
    out[0x2014] = ("emdash", 1000, dash(1000, 20))

    gap = pa * 0.55

    def ellipsis(pen):
        for i in range(3):
            draw_glyph(glyphs, n("."), (1, 0, 0, 1, i * (pa + gap), 0), pen)
    out[0x2026] = ("ellipsis", int(3 * pa + 2 * gap), ellipsis)

    def bullet(pen):
        circle(pen, 190, xh * 0.52, pw * 0.95)
    out[0x2022] = ("bullet", 380, bullet)

    def multiply(pen):
        cx, cy = arm + 40, axis
        d = arm * 0.8
        bar(pen, cx - d, cy - d, cx + d, cy + d, stem)
        bar(pen, cx - d, cy + d, cx + d, cy - d, stem)
    out[0x00D7] = ("multiply", int(2 * arm + 80), multiply)

    def divide(pen):
        cx, r = arm + 40, max(pw * 0.55, stem * 0.85)
        rect(pen, 40, axis - stem / 2, 2 * arm + 40, axis + stem / 2)
        circle(pen, cx, axis + arm * 0.74, r)
        circle(pen, cx, axis - arm * 0.74, r)
    out[0x00F7] = ("divide", int(2 * arm + 80), divide)

    def plusminus(pen):
        w = 2 * arm
        cy = axis + stem * 1.4
        rect(pen, 40, cy - stem / 2, 40 + w, cy + stem / 2)
        rect(pen, 40 + w / 2 - stem / 2, cy - w * 0.46, 40 + w / 2 + stem / 2, cy + w * 0.46)
        rect(pen, 40, axis - w * 0.5 - stem / 2, 40 + w, axis - w * 0.5 + stem / 2)
    out[0x00B1] = ("plusminus", int(2 * arm + 80), plusminus)

    def degree(pen):
        r = 0.135 * cap + 28
        ring(pen, 140, cap - r - 10, r, r - stem * 0.62)
    out[0x00B0] = ("degree", 280, degree)

    def sup(digit):
        b = bounds(glyphs, n(digit))
        s = 0.62
        shift = cap - (b[3] * s) - 20

        def draw(pen):
            draw_glyph(glyphs, n(digit), (s, 0, 0, s, 12, shift), pen)
        return draw, int(font["hmtx"][n(digit)][0] * s + 24)
    for cp, name, digit in ((0xB2, "twosuperior", "2"), (0xB3, "threesuperior", "3")):
        draw, adv = sup(digit)
        out[cp] = (name, adv, draw)

    def half(pen):
        s = 0.64
        b1 = bounds(glyphs, n("1"))
        a1 = font["hmtx"][n("1")][0] * s
        draw_glyph(glyphs, n("1"), (s, 0, 0, s, 10, cap - b1[3] * s - 20), pen)
        slash_x = a1 + 20
        bar(pen, slash_x - 10, -20, slash_x + 190, cap + 10, stem * 0.8)
        b2 = bounds(glyphs, n("2"))
        draw_glyph(glyphs, n("2"), (s, 0, 0, s, slash_x + 150, -b2[1] * s - 15), pen)
    a2 = font["hmtx"][n("2")][0] * 0.64
    out[0x00BD] = ("onehalf", int(font["hmtx"][n("1")][0] * 0.64 + 20 + 150 + a2 + 20), half)

    def with_ring(letter, top):
        b = bounds(glyphs, n(letter))
        r = 82

        def draw(pen):
            draw_glyph(glyphs, n(letter), (1, 0, 0, 1, 0, 0), pen)
            ring(pen, (b[0] + b[2]) / 2, top + r + 30, r, r - stem * 0.62)
        return draw
    out[0x00E5] = ("aring", font["hmtx"][n("a")][0], with_ring("a", xh))
    out[0x00C5] = ("Aring", font["hmtx"][n("A")][0], with_ring("A", cap))

    def arrow(direction):
        def draw(pen):
            x0, x1, h = 60, 840, arm * 0.8
            tip = x1 if direction > 0 else x0
            tail = x0 if direction > 0 else x1
            bar(pen, tail, axis, tip, axis, stem)
            bar(pen, tip, axis, tip - direction * h, axis + h, stem)
            bar(pen, tip, axis, tip - direction * h, axis - h, stem)
        return draw
    out[0x2192] = ("arrowright", 900, arrow(1))
    out[0x2190] = ("arrowleft", 900, arrow(-1))
    return out


def add(font, cp, name, advance, draw):
    cff = font["CFF "].cff
    top = cff.topDictIndex[0]
    glyphs = font.getGlyphSet()
    pen = T2CharStringPen(advance, glyphs)
    draw(pen)
    charstring = pen.getCharString(private=top.Private, globalSubrs=cff.GlobalSubrs)
    strings = top.CharStrings
    strings.charStrings[name] = len(strings.charStringsIndex)
    strings.charStringsIndex.append(charstring)
    top.charset.append(name)
    bp = BoundsPen(None)
    charstring.draw(bp)
    lsb = int(bp.bounds[0]) if bp.bounds else 0
    font["hmtx"][name] = (int(advance), lsb)
    for table in font["cmap"].tables:
        if table.format == 4:
            table.cmap[cp] = name


def extend(data):
    font = TTFont(io.BytesIO(data))
    added = []
    for cp, (name, advance, draw) in build(font).items():
        if cp in font.getBestCmap():
            continue
        add(font, cp, name, advance, draw)
        added.append(chr(cp))
    if not added:
        return data, added
    font["OS/2"].recalcUnicodeRanges(font)
    out = io.BytesIO()
    font.flavor = "woff"
    font.save(out)
    return out.getvalue(), added


def main():
    args = sys.argv[1:]
    text = CSS.read_text()
    results = []

    def swap(m):
        data, added = extend(base64.b64decode(m.group(2)))
        results.append(added)
        return m.group(1) + base64.b64encode(data).decode() + m.group(3)
    new = DATA.sub(swap, text)
    for i, added in enumerate(results):
        print(f"font {i}: added {' '.join(added) if added else 'nothing'}")
    if "--dry-run" not in args and new != text:
        CSS.write_text(new)
        print("wrote src/10-fonts.css")
    return 0


if __name__ == "__main__":
    sys.exit(main())
