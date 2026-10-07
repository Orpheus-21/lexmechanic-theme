import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import make_site  # noqa: E402


class MakeSiteTest(unittest.TestCase):
    def test_the_page_is_up_to_date(self):
        self.assertEqual((ROOT / "docs" / "index.html").read_text(), make_site.render())

    def test_the_page_shows_every_palette_color_of_both_modes(self):
        page = make_site.render()
        colors = make_site.palette()
        for name in ("ground", "accent", "graph-tag"):
            self.assertIn(colors["light"][name], page)
            self.assertIn(colors["dark"][name], page)

    def test_every_image_of_the_page_exists_in_docs(self):
        import re
        for src in re.findall(r'src="([^"]+)"', make_site.render()):
            self.assertTrue((ROOT / "docs" / src).exists(), src)


if __name__ == "__main__":
    unittest.main()
