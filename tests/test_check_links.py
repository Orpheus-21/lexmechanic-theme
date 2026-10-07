import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import check_links as k  # noqa: E402


class LinksTest(unittest.TestCase):
    def test_markdown_links_and_images_are_found(self):
        text = "See [site](https://example.com/a) and ![shot](screenshot.png) and [anchor](#top)."
        self.assertEqual(k.links(text), {"https://example.com/a", "screenshot.png", "#top"})

    def test_a_bare_address_is_found_without_the_final_dot(self):
        self.assertEqual(k.links("Get it at https://obsidian.md/download."), {"https://obsidian.md/download"})

    def test_code_is_skipped(self):
        text = "Run `curl https://skipped.example` now.\n\n```\nhttps://also-skipped.example\n```\n"
        self.assertEqual(k.links(text), set())

    def test_a_link_with_a_title_gives_only_the_address(self):
        self.assertEqual(k.links('[a](https://example.com "title")'), {"https://example.com"})


if __name__ == "__main__":
    unittest.main()
