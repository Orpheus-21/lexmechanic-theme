import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import make_print  # noqa: E402


class MakePrintTest(unittest.TestCase):
    def test_the_file_is_up_to_date(self):
        self.assertEqual((ROOT / "src" / "45-print.css").read_text(), make_print.render((ROOT / "src" / "30-light.css").read_text()))

    def test_the_print_rule_holds_the_light_palette_for_dark_mode(self):
        text = make_print.render(".theme-light {\n  --lex-ground: #faf9f5;\n\n  --lex-ink: #2c251d;\n}\n")
        self.assertIn("@media print {\n  .theme-dark {\n    --lex-ground: #faf9f5;\n\n    --lex-ink: #2c251d;\n  }\n}", text)


if __name__ == "__main__":
    unittest.main()
