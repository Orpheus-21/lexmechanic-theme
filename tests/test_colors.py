import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import colors as c  # noqa: E402


class LabTest(unittest.TestCase):
    def test_white_and_black_lightness(self):
        self.assertAlmostEqual(c.lightness("#ffffff"), 100.0, places=2)
        self.assertAlmostEqual(c.lightness("#000000"), 0.0, places=2)

    def test_gray_has_no_chroma(self):
        _, a, b = c.lab("#808080")
        self.assertAlmostEqual(a, 0.0, places=1)
        self.assertAlmostEqual(b, 0.0, places=1)


class DeltaETest(unittest.TestCase):
    """Reference pairs 1 and 7 of Sharma, Wu, and Dalal (2005) give 2.0425 and 27.1492."""

    def with_labs(self, one, two):
        original = c.lab
        c.lab = {"a": one, "b": two}.__getitem__
        try:
            return c.delta_e("a", "b")
        finally:
            c.lab = original

    def test_sharma_pair_1(self):
        self.assertAlmostEqual(self.with_labs((50, 2.6772, -79.7751), (50, 0, -82.7485)), 2.0425, places=4)

    def test_sharma_pair_7(self):
        self.assertAlmostEqual(self.with_labs((50, 2.5, 0), (73, 25, -18)), 27.1492, places=4)

    def test_same_color_has_distance_0(self):
        self.assertAlmostEqual(c.delta_e("#901714", "#901714"), 0.0, places=6)


class SimulateTest(unittest.TestCase):
    def test_gray_stays_gray_for_every_kind(self):
        for kind in c.CVD:
            self.assertEqual(c.simulate("#808080", kind), "#808080")

    def test_red_and_green_get_close_for_deuteranopia(self):
        far = c.delta_e("#ff0000", "#00aa00")
        near = c.delta_e(c.simulate("#ff0000", "deuteranopia"), c.simulate("#00aa00", "deuteranopia"))
        self.assertLess(near, far)


if __name__ == "__main__":
    unittest.main()
