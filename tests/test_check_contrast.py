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


class EffectiveTest(unittest.TestCase):
    def test_blend_half_of_black_over_white_is_gray(self):
        self.assertEqual(c.blend("#000000", "#ffffff", 0.5), "#808080")

    def test_blend_with_alpha_1_is_the_color(self):
        self.assertEqual(c.blend("#123456", "#ffffff", 1.0), "#123456")

    def test_color_mix_with_transparent_is_laid_over_the_page(self):
        values = {"--ink": "#000000", "--mix": "color-mix(in srgb, var(--ink) 50%, transparent)"}
        self.assertEqual(c.effective("--mix", values, "#ffffff"), "#808080")

    def test_a_solid_color_stays_solid(self):
        self.assertEqual(c.effective("--a", {"--a": "#112233"}, "#ffffff"), "#112233")

    def test_an_unknown_value_gives_none(self):
        self.assertIsNone(c.effective("--a", {"--a": "url(x)"}, "#ffffff"))


class ComputeTest(unittest.TestCase):
    data = c.compute()

    def test_both_modes_have_text_rows_and_pairs(self):
        for mode in ("light", "dark"):
            self.assertGreater(len(self.data[mode]["text"]), 20)
            self.assertGreater(len(self.data[mode]["pairs"]), 5)

    def test_the_theme_has_no_new_failure(self):
        self.assertEqual(c.failures(self.data), 0)

    def test_the_selection_pair_is_there(self):
        labels = [p["label"] for p in self.data["light"]["pairs"]]
        self.assertIn("--text-normal on the selection color", labels)

    def test_a_failing_pair_is_counted(self):
        bad = {"light": {"text": [{"status": ["ok", "fail", "known"]}], "pairs": [{"status": "fail"}]}}
        self.assertEqual(c.failures(bad), 2)

    def test_the_json_output_can_be_written(self):
        import json
        self.assertIn("light", json.loads(json.dumps(self.data)))

    def test_the_document_has_the_markers_and_is_current(self):
        self.assertEqual(c.DOC.read_text(), c.document(self.data))
