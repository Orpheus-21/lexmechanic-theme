import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import check_graph as g  # noqa: E402


class EffectiveTest(unittest.TestCase):
    def test_half_opacity_black_on_white_is_gray(self):
        self.assertEqual(g.effective([0, 0, 0, 255], 0.5, "#ffffff"), "#808080")

    def test_color_alpha_and_opacity_multiply(self):
        self.assertEqual(g.effective([0, 0, 0, 128], 0.5, "#ffffff"), g.effective([0, 0, 0, 255], 0.251, "#ffffff"))

    def test_hexa_ignores_alpha(self):
        self.assertEqual(g.hexa([1, 2, 3, 99]), "#010203")

    def test_every_known_entry_names_a_hook_pair_or_hook(self):
        hooks = {h[0] for h in g.HOOKS}
        for key in g.KNOWN:
            self.assertIn(key[0], ("light", "dark"))
            self.assertTrue(set(key[1:]) <= hooks)


if __name__ == "__main__":
    unittest.main()
