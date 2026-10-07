import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import check_contrast as c  # noqa: E402


class RatioTest(unittest.TestCase):
    def test_black_on_white_is_21_to_1(self):
        self.assertAlmostEqual(c.ratio("#000000", "#ffffff"), 21.0, places=6)

    def test_ratio_does_not_depend_on_the_order(self):
        self.assertAlmostEqual(c.ratio("#901714", "#faf9f5"), c.ratio("#faf9f5", "#901714"))

    def test_same_color_is_1_to_1(self):
        self.assertAlmostEqual(c.ratio("#123456", "#123456"), 1.0, places=6)

    def test_luminance_of_white_and_black(self):
        self.assertAlmostEqual(c.luminance("#ffffff"), 1.0, places=6)
        self.assertAlmostEqual(c.luminance("#000000"), 0.0, places=6)


class ResolveTest(unittest.TestCase):
    values = {"--a": "#112233", "--b": "var(--a)", "--c": "var(--b)", "--loop": "var(--loop)",
              "--mix": "color-mix(in srgb, #fff 50%, transparent)"}

    def test_a_hex_value_resolves_to_itself(self):
        self.assertEqual(c.resolve("--a", self.values), "#112233")

    def test_a_chain_of_var_references_resolves(self):
        self.assertEqual(c.resolve("--c", self.values), "#112233")

    def test_a_loop_gives_none(self):
        self.assertIsNone(c.resolve("--loop", self.values))

    def test_a_missing_name_gives_none(self):
        self.assertIsNone(c.resolve("--nope", self.values))

    def test_color_mix_is_not_a_solid_color(self):
        self.assertIsNone(c.resolve("--mix", self.values))


class BlocksTest(unittest.TestCase):
    def test_theme_css_has_both_modes_with_the_palette(self):
        blocks = c.read_blocks((ROOT / "theme.css").read_text())
        self.assertEqual(sorted(blocks), ["dark", "light"])
        for values in blocks.values():
            self.assertIn("--lex-ink", values)
            self.assertIsNotNone(c.resolve("--text-normal", values))

    def test_text_normal_is_dark_on_light_and_light_on_dark(self):
        blocks = c.read_blocks((ROOT / "theme.css").read_text())
        light = c.luminance(c.resolve("--text-normal", blocks["light"]))
        dark = c.luminance(c.resolve("--text-normal", blocks["dark"]))
        self.assertLess(light, 0.1)
        self.assertGreater(dark, 0.5)


if __name__ == "__main__":
    unittest.main()
