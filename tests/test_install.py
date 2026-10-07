import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = str(ROOT / "scripts" / "install.sh")


def run(*args):
    return subprocess.run([SCRIPT, *args], capture_output=True, text=True)


class InstallTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.vault = Path(self.tmp.name)
        (self.vault / ".obsidian").mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def test_copy_puts_the_theme_and_the_two_snippets_into_the_vault(self):
        self.assertEqual(run(str(self.vault)).returncode, 0)
        theme = self.vault / ".obsidian" / "themes" / "Lexmechanic"
        self.assertEqual((theme / "theme.css").read_bytes(), (ROOT / "theme.css").read_bytes())
        self.assertTrue((theme / "manifest.json").exists())
        names = sorted(p.name for p in (self.vault / ".obsidian" / "snippets").iterdir())
        self.assertEqual(names, sorted(p.name for p in (ROOT / "snippets").glob("*.css")))

    def test_link_makes_symbolic_links(self):
        self.assertEqual(run(str(self.vault), "--link").returncode, 0)
        self.assertTrue((self.vault / ".obsidian" / "themes" / "Lexmechanic" / "theme.css").is_symlink())

    def test_presets_are_copied_only_with_the_option(self):
        run(str(self.vault))
        before = {p.name for p in (self.vault / ".obsidian" / "snippets").iterdir()}
        run(str(self.vault), "--presets")
        after = {p.name for p in (self.vault / ".obsidian" / "snippets").iterdir()}
        self.assertEqual(after - before, {p.name for p in (ROOT / "snippets" / "presets").glob("*.css")})

    def test_a_folder_without_obsidian_is_refused(self):
        other = self.vault / "plain"
        other.mkdir()
        self.assertEqual(run(str(other)).returncode, 1)

    def test_an_unknown_option_is_refused(self):
        self.assertEqual(run(str(self.vault), "--nope").returncode, 2)


if __name__ == "__main__":
    unittest.main()
