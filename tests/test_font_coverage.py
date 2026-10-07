import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import font_coverage as f  # noqa: E402


class FontsTest(unittest.TestCase):
    fonts = f.read_fonts((ROOT / "src" / "10-fonts.css").read_text())

    def test_three_fonts_are_found(self):
        self.assertEqual([(a, b) for a, b, _ in self.fonts],
                         [("Volume Tc", "normal"), ("Volume Tc", "italic"), ("Volume Tc Sans", "normal")])

    def test_each_font_has_basic_latin_and_no_cjk(self):
        for _, _, woff in self.fonts:
            cps = f.codepoints(f.tables(woff)["cmap"])
            self.assertTrue(all(c in cps for c in range(0x20, 0x7F)))
            self.assertFalse(any(0x4E00 <= c <= 0x9FFF for c in cps))

    def test_the_fonts_have_only_the_kern_feature(self):
        for _, _, woff in self.fonts:
            self.assertEqual(f.features(f.tables(woff)), ["GPOS: kern"])

    def test_the_em_dash_is_missing(self):
        cps = f.codepoints(f.tables(self.fonts[0][2])["cmap"])
        self.assertNotIn(0x2014, cps)

    def test_the_document_is_current(self):
        self.assertEqual(f.DOC.read_text(), f.document())


if __name__ == "__main__":
    unittest.main()
