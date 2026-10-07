import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import make_docs as d  # noqa: E402


class PaletteTest(unittest.TestCase):
    light, dark = d.modes()

    def test_both_modes_have_the_same_palette_names(self):
        a = [n for n in self.light if n.startswith("--lex-")]
        b = [n for n in self.dark if n.startswith("--lex-")]
        self.assertEqual(a, b)

    def test_every_palette_variable_has_a_use(self):
        for name in self.light:
            if name.startswith("--lex-"):
                self.assertIn(name[len("--lex-"):], d.USES, name)

    def test_every_use_is_a_palette_variable(self):
        for key in d.USES:
            self.assertIn("--lex-" + key, self.light, key)

    def test_the_graph_variables_exist_in_both_modes(self):
        for name in d.GRAPH_USES:
            self.assertIn(name, self.light)
            self.assertIn(name, self.dark)

    def test_the_documents_are_current(self):
        for path, text in d.documents().items():
            self.assertEqual(path.read_text(), text, str(path))


if __name__ == "__main__":
    unittest.main()
