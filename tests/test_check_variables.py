import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import check_graph as g  # noqa: E402
import check_variables as v  # noqa: E402

CSS = """
body { --a: 1; --graph-line: red; }
.graph-view.color-fill { color: var(--graph-node); }
.graph-view.color-line, .graph-view.color-text { color: red; }
"""


class UnusedTest(unittest.TestCase):
    def test_a_defined_or_read_variable_is_fine(self):
        self.assertEqual(v.unused({"--a", "--graph-node"}, CSS), [])

    def test_an_unknown_variable_is_reported(self):
        self.assertEqual(v.unused({"--a", "--gone"}, CSS), ["--gone"])

    def test_the_palette_is_not_part_of_the_check(self):
        self.assertFalse(any(n.startswith("--lex-") for n in v.theme_variables()))


class GraphTest(unittest.TestCase):
    def test_missing_hooks_and_variables_are_listed(self):
        lost = v.graph_problems(CSS)
        self.assertIn(".graph-view.color-arrow", lost)
        self.assertIn("--graph-node-tag", lost)
        self.assertNotIn(".graph-view.color-fill", lost)
        self.assertNotIn(".graph-view.color-line", lost)
        self.assertNotIn(".graph-view.color-text", lost)
        self.assertNotIn("--graph-line", lost)

    def test_the_two_scripts_use_the_same_hooks(self):
        self.assertEqual([h[0] for h in g.HOOKS], v.GRAPH_HOOKS)


if __name__ == "__main__":
    unittest.main()
