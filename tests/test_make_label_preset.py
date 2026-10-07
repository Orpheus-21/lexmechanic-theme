import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import make_label_preset as m  # noqa: E402


class LabelPresetTest(unittest.TestCase):
    def test_the_preset_file_is_current(self):
        self.assertEqual(m.TARGET.read_text(), m.preset())

    def test_the_face_is_named_ui_sans_serif_and_holds_the_sans_font_data(self):
        text = m.preset()
        self.assertIn("font-family: 'ui-sans-serif';", text)
        sans = m.sans_face((ROOT / "src" / "10-fonts.css").read_text())
        self.assertIn(sans, text)
        self.assertIn("base64,", sans)

    def test_the_header_says_not_to_edit_the_file(self):
        self.assertIn("do not\n   edit this file by hand", m.preset())


if __name__ == "__main__":
    unittest.main()
