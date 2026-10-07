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


class VariablesTest(unittest.TestCase):
    rows = d.variable_rows()

    def test_every_variable_of_the_theme_is_listed(self):
        import check_variables as v
        self.assertEqual(set(self.rows), v.theme_variables())

    def test_every_variable_has_an_area(self):
        self.assertEqual([n for n in self.rows if d.area_of(n) == "Other"], [])

    def test_a_shared_variable_has_one_value_for_both_modes(self):
        light, dark, where = self.rows["--font-text-theme"]
        self.assertEqual(light, dark)
        self.assertEqual(where, "theme")

    def test_a_snippet_variable_names_the_snippet(self):
        self.assertEqual(self.rows["--tag-radius"][2], "lexmechanic-extras")
        self.assertEqual(self.rows["--hr-thickness"][2], "lexmechanic-fun")

    def test_a_mode_variable_differs_between_the_modes(self):
        light, dark, _ = self.rows["--accent-h"]
        self.assertNotEqual(light, dark)


if __name__ == "__main__":
    unittest.main()
