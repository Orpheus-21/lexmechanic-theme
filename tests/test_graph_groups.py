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


if __name__ == "__main__":
    unittest.main()
