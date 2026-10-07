import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import check_contrast as c  # noqa: E402

PRESETS = sorted((ROOT / "snippets" / "presets").glob("*.css"))


class PresetsTest(unittest.TestCase):
    def test_there_are_presets(self):
        self.assertGreaterEqual(len(PRESETS), 10)

    def test_each_preset_starts_with_a_comment_that_says_what_it_does(self):
        for path in PRESETS:
            text = path.read_text()
            self.assertTrue(text.startswith("/* Lexmechanic "), path.name)
            self.assertIn("*/", text.split("\n\n")[0], path.name)

    def test_each_preset_name_starts_with_lexmechanic(self):
        for path in PRESETS:
            self.assertTrue(path.name.startswith("lexmechanic-"), path.name)

    def test_each_preset_has_a_rule_with_a_declaration(self):
        for path in PRESETS:
            body = re.sub(r"/\*.*?\*/", "", path.read_text(), flags=re.S)
            self.assertTrue(re.search(r"\{[^{}]*:[^{}]*\}", body), path.name)

    def test_no_preset_makes_the_contrast_worse_than_the_known_pairs(self):
        for path in PRESETS:
            self.assertEqual(c.failures(c.compute(preset=path.read_text())), 0, path.name)

    def test_a_preset_does_not_use_a_hex_value_outside_a_variable_or_a_hook(self):
        for path in PRESETS:
            for line in path.read_text().split("\n"):
                if re.search(r"#[0-9a-fA-F]{6}", line) and not line.strip().startswith(("/*", "*")):
                    self.assertTrue(re.match(r"\s*--[a-z0-9-]+:", line), f"{path.name}: {line}")


if __name__ == "__main__":
    unittest.main()
