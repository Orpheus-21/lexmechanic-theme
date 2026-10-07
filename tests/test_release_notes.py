import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import release_notes as r  # noqa: E402

LOG = """# Changelog

## [Unreleased]

Added:

* A thing.

## [1.1.0] (2026-10-06)

* Older.

## [1.0.0] (2026-10-05)

* First.

[Unreleased]: https://github.com/Orpheus-21/lexmechanic-theme/compare/1.1.0...HEAD
[1.1.0]: https://github.com/Orpheus-21/lexmechanic-theme/compare/394b876...1.1.0
[1.0.0]: https://github.com/Orpheus-21/lexmechanic-theme/commit/394b876
"""


class ReleaseNotesTest(unittest.TestCase):
    def test_notes_of_a_version(self):
        self.assertEqual(r.notes(LOG, "1.1.0"), "* Older.\n")

    def test_notes_of_the_last_version_stop_before_the_links(self):
        self.assertEqual(r.notes(LOG, "1.0.0"), "* First.\n")

    def test_notes_of_an_unknown_version_fail(self):
        with self.assertRaises(ValueError):
            r.notes(LOG, "9.9.9")

    def test_prepare_renames_unreleased_and_moves_the_links(self):
        out = r.prepare(LOG, "1.2.0", "2026-10-07")
        self.assertIn("## [Unreleased]\n\n## [1.2.0] (2026-10-07)\n\nAdded:", out)
        self.assertIn("[Unreleased]: https://github.com/Orpheus-21/lexmechanic-theme/compare/1.2.0...HEAD\n[1.2.0]: https://github.com/Orpheus-21/lexmechanic-theme/compare/1.1.0...1.2.0\n[1.1.0]:", out)
        self.assertEqual(r.notes(out, "1.2.0"), "Added:\n\n* A thing.\n")

    def test_prepare_refuses_an_empty_unreleased_section(self):
        with self.assertRaises(ValueError):
            r.prepare(LOG.replace("Added:\n\n* A thing.\n\n", ""), "1.2.0", "2026-10-07")

    def test_prepare_refuses_a_version_that_exists(self):
        with self.assertRaises(ValueError):
            r.prepare(LOG, "1.1.0", "2026-10-07")


if __name__ == "__main__":
    unittest.main()
