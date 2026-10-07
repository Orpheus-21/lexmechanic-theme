import struct
import sys
import unittest
import zlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import check_screenshots as s  # noqa: E402


def png(width, height, pixels, ctype=2, filters=None):
    """Encode a PNG. pixels is a list of rows, each a list of (r, g, b). filters is a list of filter types per row."""
    bpp = 3 if ctype == 2 else 4
    raw, prev = b"", bytes(width * bpp)
    for y, row in enumerate(pixels):
        line = bytes(c for px in row for c in (px + ((255,) if ctype == 6 else ())))
        kind = (filters or [0] * height)[y]
        out = bytearray()
        for i, v in enumerate(line):
            a = line[i - bpp] if i >= bpp else 0
            b = prev[i]
            c = prev[i - bpp] if i >= bpp else 0
            if kind == 0:
                out.append(v)
            elif kind == 1:
                out.append((v - a) & 255)
            elif kind == 2:
                out.append((v - b) & 255)
            elif kind == 3:
                out.append((v - (a + b) // 2) & 255)
            else:
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                out.append((v - (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 255)
        raw += bytes([kind]) + bytes(out)
        prev = line

    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))
    header = struct.pack(">IIBBBBB", width, height, 8, ctype, 0, 0, 0)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header) + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b"")


GRID = [[(10, 20, 30), (40, 50, 60), (70, 80, 90)], [(100, 110, 120), (130, 140, 150), (160, 170, 180)], [(1, 2, 3), (4, 5, 6), (7, 8, 9)]]


class PngTest(unittest.TestCase):
    def test_every_filter_type_decodes_to_the_same_pixels(self):
        for kind in range(5):
            width, height, bpp, rows = s.read_png(png(3, 3, GRID, filters=[kind] * 3))
            self.assertEqual((width, height, bpp), (3, 3, 3))
            self.assertEqual([[tuple(r[i:i + 3]) for i in range(0, 9, 3)] for r in rows], GRID, f"filter {kind}")

    def test_an_rgba_file_is_read(self):
        _, _, bpp, rows = s.read_png(png(3, 3, GRID, ctype=6))
        self.assertEqual(bpp, 4)
        self.assertEqual(tuple(rows[0][:4]), (10, 20, 30, 255))

    def test_a_file_that_is_not_a_png_is_refused(self):
        with self.assertRaises(ValueError):
            s.read_png(b"nope")


class CompareTest(unittest.TestCase):
    def test_equal_images_have_no_difference(self):
        self.assertEqual(s.compare(png(3, 3, GRID), png(3, 3, GRID)), (0, 9, None))

    def test_a_changed_pixel_is_counted_and_boxed(self):
        other = [row[:] for row in GRID]
        other[1][2] = (250, 250, 250)
        self.assertEqual(s.compare(png(3, 3, GRID), png(3, 3, other)), (1, 9, (2, 1, 2, 1)))

    def test_a_small_change_is_below_the_tolerance(self):
        other = [row[:] for row in GRID]
        other[0][0] = (14, 20, 30)
        self.assertEqual(s.compare(png(3, 3, GRID), png(3, 3, other))[0], 0)

    def test_images_of_different_sizes_differ_everywhere(self):
        self.assertEqual(s.compare(png(3, 3, GRID), png(2, 3, [r[:2] for r in GRID]))[0], 9)

    def test_the_stored_images_exist_and_are_readable(self):
        for mode in ("light", "dark"):
            width, height, _, _ = s.read_png((s.DIR / f"{mode}.png").read_bytes())
            self.assertEqual((width, height), s.SIZE)


if __name__ == "__main__":
    unittest.main()
