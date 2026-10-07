import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import graph_groups as g  # noqa: E402


class IntTest(unittest.TestCase):
    def test_a_color_is_one_integer(self):
        self.assertEqual(g.to_int("#000000"), 0)
        self.assertEqual(g.to_int("#ffffff"), 16777215)
        self.assertEqual(g.to_int("#010203"), 1 * 65536 + 2 * 256 + 3)


class GroupTest(unittest.TestCase):
    colors = g.palette("light")

    def test_a_palette_name_gives_its_color(self):
        entry = g.group("tag:#book=red", self.colors)
        self.assertEqual(entry["query"], "tag:#book")
        self.assertEqual(entry["color"], {"a": 1, "rgb": g.to_int(self.colors["red"])})

    def test_a_hex_color_is_taken_as_it_is(self):
        self.assertEqual(g.group("x=#3B5A8A", self.colors)["color"]["rgb"], 0x3B5A8A)

    def test_a_query_may_contain_an_equal_sign(self):
        self.assertEqual(g.group("file=a=blue", self.colors)["query"], "file=a")

    def test_a_bad_color_or_spec_is_an_error(self):
        with self.assertRaises(ValueError):
            g.group("x=nope", self.colors)
        with self.assertRaises(ValueError):
            g.group("no-equal-sign", self.colors)

    def test_the_modes_have_different_palettes(self):
        self.assertNotEqual(g.palette("light")["red"], g.palette("dark")["red"])

    def test_the_output_is_json(self):
        self.assertIsInstance(json.loads(json.dumps([g.group("a=ink", self.colors)])), list)


class ExampleTest(unittest.TestCase):
    path = Path(__file__).resolve().parent.parent / "examples" / "graph.json"

    def test_the_example_is_valid_json_with_the_display_and_force_keys(self):
        data = json.loads(self.path.read_text())
        for key in ("colorGroups", "showArrow", "textFadeMultiplier", "nodeSizeMultiplier", "lineSizeMultiplier",
                    "centerStrength", "repelStrength", "linkStrength", "linkDistance"):
            self.assertIn(key, data)

    def test_the_colors_of_the_example_are_palette_colors_of_light_mode(self):
        colors = g.palette("light")
        ints = {g.to_int(v) for v in colors.values()}
        for entry in json.loads(self.path.read_text())["colorGroups"]:
            self.assertEqual(entry["color"]["a"], 1)
            self.assertIn(entry["color"]["rgb"], ints)

    def test_the_center_strength_default_is_the_default_of_obsidian(self):
        import math
        self.assertAlmostEqual(1 - math.log(0.1 * 0.99 + 0.01) / math.log(0.01), json.loads(self.path.read_text())["centerStrength"], places=12)


if __name__ == "__main__":
    unittest.main()
