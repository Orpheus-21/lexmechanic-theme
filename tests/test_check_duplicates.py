import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import check_duplicates as d  # noqa: E402


class DuplicatesTest(unittest.TestCase):
    def test_a_property_set_twice_is_found(self):
        found = d.duplicates("a { color: red; margin: 0; color: blue; }")
        self.assertEqual(found, [("a", "color", 2)])

    def test_a_variable_set_twice_is_found(self):
        self.assertEqual(d.duplicates(".x { --a: 1; --a: 2; }"), [(".x", "--a", 2)])

    def test_the_same_property_in_two_blocks_is_fine(self):
        self.assertEqual(d.duplicates("a { color: red; } b { color: blue; }"), [])

    def test_comments_and_data_uris_are_ignored(self):
        text = "a { /* color: red; */ color: blue; src: url('data:font/woff;base64,AAAA;color:x'); }"
        self.assertEqual(d.duplicates(text), [])

    def test_the_project_has_no_duplicate(self):
        for path in list((ROOT / "src").glob("*.css")) + list((ROOT / "snippets").glob("*.css")):
            self.assertEqual(d.duplicates(path.read_text()), [], str(path))


if __name__ == "__main__":
    unittest.main()
