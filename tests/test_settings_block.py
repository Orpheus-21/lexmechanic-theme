import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import check_contrast as c  # noqa: E402

BLOCK = re.search(r"/\* @settings\n(.*?)\*/", (ROOT / "src" / "60-settings.css").read_text(), re.S).group(1)


def entries():
    """Return the list of options of the Style Settings block as {key: value} dicts."""
    out = []
    for chunk in re.split(r"\n  -\n", BLOCK)[1:]:
        out.append({k: re.sub(r"^(['\"])(.*)\1$", r"\2", v.strip()) for k, v in re.findall(r"^    ([a-z-]+): (.+)$", chunk, re.M)})
    return out


class SettingsBlockTest(unittest.TestCase):
    def test_the_block_names_the_theme(self):
        self.assertIn("name: Lexmechanic\nid: lexmechanic\nsettings:", BLOCK)

    def test_every_option_has_an_id_a_title_and_a_type(self):
        for e in entries():
            self.assertTrue({"id", "title", "type"} <= e.keys(), e)

    def test_the_default_of_each_color_is_the_value_of_the_palette(self):
        css = (ROOT / "theme.css").read_text()
        blocks = c.read_blocks(css)
        shared = c.shared_block(css)
        found = 0
        for e in entries():
            if e["type"] != "variable-themed-color":
                continue
            for mode in ("light", "dark"):
                value = c.resolve("--" + e["id"], {**shared, **blocks[mode]})
                self.assertEqual(e[f"default-{mode}"].lower(), value, f"{e['id']} {mode}")
            found += 1
        self.assertGreaterEqual(found, 8)

    def test_the_default_of_each_font_is_the_value_of_the_theme(self):
        shared = c.shared_block((ROOT / "theme.css").read_text())
        for e in entries():
            if e["type"] == "variable-text":
                self.assertEqual(e["default"], shared["--" + e["id"]], e["id"])

    def test_the_class_toggles_of_the_snippet_are_used_by_a_rule(self):
        text = (ROOT / "snippets" / "lexmechanic-fun.css").read_text()
        ids = re.findall(r"id: (lex-[a-z-]+)\n    title", text)
        self.assertEqual(len(ids), 4)
        for name in ids:
            self.assertIn(f"body.{name}", text.split("/* @settings")[0], name)


if __name__ == "__main__":
    unittest.main()
