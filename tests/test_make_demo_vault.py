import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import make_demo_vault as m  # noqa: E402


class DemoVaultTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "vault"
        self.names = m.build(self.path, 30, "dark")

    def tearDown(self):
        self.tmp.cleanup()

    def test_it_writes_thirty_notes_in_three_folders(self):
        self.assertEqual(len(self.names), 30)
        self.assertEqual({p.parent.name for p in self.path.glob("*/*.md")}, {"Projects", "Ideas", "Inbox"})

    def test_the_graph_has_every_node_type(self):
        text = "".join(p.read_text() for p in self.path.glob("*/*.md"))
        links = set(re.findall(r"(?<!!)\[\[([^\]]+)\]\]", text))
        self.assertTrue(links & set(self.names), "resolved links")
        self.assertTrue(any(l.startswith("Missing note") for l in links), "unresolved links")
        self.assertIn("#idea", text)
        self.assertTrue(list((self.path / "Attachments").glob("*.png")))
        self.assertIn("![[diagram-1.png]]", text)

    def test_the_settings_choose_the_theme_and_the_mode(self):
        appearance = json.loads((self.path / ".obsidian" / "appearance.json").read_text())
        self.assertEqual(appearance["cssTheme"], "Lexmechanic")
        self.assertEqual(appearance["theme"], "obsidian")
        graph = json.loads((self.path / ".obsidian" / "graph.json").read_text())
        self.assertEqual(len(graph["colorGroups"]), 3)

    def test_a_second_run_in_a_full_folder_is_refused(self):
        with self.assertRaises(SystemExit):
            m.build(self.path)

    def test_the_notes_are_the_same_on_each_run(self):
        with tempfile.TemporaryDirectory() as other:
            second = m.build(Path(other) / "v", 30, "dark")
            self.assertEqual(second, self.names)


if __name__ == "__main__":
    unittest.main()
