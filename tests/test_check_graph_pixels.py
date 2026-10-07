import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import check_graph_pixels as g  # noqa: E402


def node(kind, x, y, radius=8):
    return {"type": kind, "x": x, "y": y, "radius": radius, "alpha": 1, "tint": "#000000"}


class PickTest(unittest.TestCase):
    canvas = [0, 0, 1000, 800]
    panel = [800, 50, 1000, 700]

    def test_it_takes_the_first_free_node_of_each_type(self):
        nodes = [node("tag", 100, 100), node("tag", 300, 300), node("resolved", 200, 200)]
        chosen = g.pick(nodes, self.panel, self.canvas)
        self.assertEqual(chosen["tag"]["x"], 100)
        self.assertEqual(set(chosen), {"tag", "resolved"})

    def test_a_node_under_the_panel_is_skipped(self):
        self.assertEqual(g.pick([node("tag", 850, 300)], self.panel, self.canvas), {})

    def test_a_node_at_the_edge_is_skipped(self):
        self.assertEqual(g.pick([node("tag", 10, 300)], self.panel, self.canvas), {})
        self.assertEqual(len(g.pick([node("tag", 20, 300)], self.panel, self.canvas)), 1)

    def test_a_node_that_is_still_fading_is_skipped_when_alphas_are_given(self):
        faded = dict(node("tag", 100, 100), alpha=0.7)
        steady = node("tag", 300, 300)
        self.assertEqual(g.pick([faded, steady], self.panel, self.canvas, {"tag": 1})["tag"]["x"], 300)
        self.assertEqual(g.pick([faded], self.panel, self.canvas, {"tag": 1}), {})
        self.assertEqual(g.pick([faded], self.panel, self.canvas)["tag"]["x"], 100)

    def test_two_nodes_that_touch_are_both_skipped(self):
        self.assertEqual(g.pick([node("tag", 100, 100), node("resolved", 110, 100)], self.panel, self.canvas), {})
        self.assertEqual(len(g.pick([node("tag", 100, 100), node("resolved", 120, 100)], self.panel, self.canvas)), 2)


class HelperTest(unittest.TestCase):
    def test_hex_to_rgb(self):
        self.assertEqual(g.hex_to_rgb("#473e34"), [0x47, 0x3E, 0x34])

    def test_pixel_reads_rgb_from_rows_of_rgba(self):
        rows = [bytearray([1, 2, 3, 255, 4, 5, 6, 255]), bytearray([7, 8, 9, 255, 10, 11, 12, 255])]
        self.assertEqual(g.pixel(rows, 4, 1, 1), [10, 11, 12])


if __name__ == "__main__":
    unittest.main()
