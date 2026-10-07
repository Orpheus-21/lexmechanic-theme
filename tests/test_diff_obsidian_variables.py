import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import diff_obsidian_variables as d  # noqa: E402


class DiffTest(unittest.TestCase):
    def test_defined_finds_declarations_only(self):
        self.assertEqual(d.defined("a { --x: 1; color: var(--y); --z-1: 2 }"), {"--x", "--z-1"})

    def test_group_uses_the_first_word(self):
        groups = d.group({"--tab-inner-a", "--tab-inner-b", "--tab-x", "--hotkey-radius"})
        self.assertEqual(groups["--tab"], ["--tab-inner-a", "--tab-inner-b", "--tab-x"])
        self.assertEqual(groups["--hotkey"], ["--hotkey-radius"])


if __name__ == "__main__":
    unittest.main()
