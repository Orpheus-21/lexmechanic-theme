import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import check_colorblind as cb  # noqa: E402


class DistanceTest(unittest.TestCase):
    def test_black_and_white_are_far_apart_for_everyone(self):
        d, _ = cb.distance("#000000", "#ffffff")
        self.assertGreater(d, 90)

    def test_the_distance_does_not_depend_on_the_order(self):
        self.assertAlmostEqual(cb.distance("#a8231f", "#3a6329")[0], cb.distance("#3a6329", "#a8231f")[0])

    def test_red_and_green_are_closer_with_deuteranopia(self):
        d, kind = cb.distance("#a8231f", "#3a6329")
        self.assertIn(kind, ("deuteranopia", "protanopia"))


class PairsTest(unittest.TestCase):
    def test_pairs_are_sorted_and_marked_close(self):
        rows = cb.close_pairs({"a": "#000000", "b": "#010101", "c": "#ffffff"})
        self.assertEqual(len(rows), 3)
        self.assertEqual((rows[0]["a"], rows[0]["b"]), ("a", "b"))
        self.assertTrue(rows[0]["close"])
        self.assertFalse(rows[-1]["close"])

    def test_the_callout_colors_resolve_in_both_modes(self):
        sets = cb.callout_colors()
        for mode in ("light", "dark"):
            self.assertEqual(sorted(sets[mode]), sorted(cb.BASE))
            self.assertTrue(all(v.startswith("#") for v in sets[mode].values()))


if __name__ == "__main__":
    unittest.main()
