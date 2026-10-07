import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import check_manifest as m  # noqa: E402

GOOD = json.dumps({"name": "T", "version": "1.2.3", "minAppVersion": "1.0.0", "author": "A"})
LOG = "# Changelog\n\n## Unreleased\n\n* x\n\n## 1.2.3 (2026-01-01)\n\n## 1.0.0 (2025-01-01)\n"


class ProblemsTest(unittest.TestCase):
    def test_a_good_manifest_has_no_problem(self):
        self.assertEqual(m.problems(GOOD, LOG), [])

    def test_invalid_json_is_reported(self):
        self.assertIn("not valid JSON", m.problems('{"name": "T",}', LOG)[0])

    def test_a_missing_key_is_reported(self):
        text = json.dumps({"name": "T", "version": "1.2.3", "minAppVersion": "1.0.0"})
        self.assertIn("manifest.json has no author", m.problems(text, LOG))

    def test_a_bad_version_form_is_reported(self):
        text = json.dumps({"name": "T", "version": "1.2", "minAppVersion": "1.0.0", "author": "A"})
        self.assertTrue(any("not of the form x.y.z" in p for p in m.problems(text, LOG)))

    def test_a_version_that_differs_from_the_changelog_is_reported(self):
        text = json.dumps({"name": "T", "version": "1.3.0", "minAppVersion": "1.0.0", "author": "A"})
        self.assertTrue(any("newest version in CHANGELOG.md is 1.2.3" in p for p in m.problems(text, LOG)))

    def test_a_tag_must_be_the_version_without_v(self):
        self.assertEqual(m.problems(GOOD, LOG, tag="1.2.3"), [])
        self.assertTrue(m.problems(GOOD, LOG, tag="v1.2.3"))

    def test_a_version_in_square_brackets_is_found(self):
        self.assertEqual(m.changelog_version("## [Unreleased]

## [1.4.0] (2026-01-01)
"), "1.4.0")

    def test_unreleased_is_skipped(self):
        self.assertEqual(m.changelog_version(LOG), "1.2.3")

    def test_the_real_project_agrees(self):
        self.assertEqual(m.problems((ROOT / "manifest.json").read_text(), (ROOT / "CHANGELOG.md").read_text()), [])


if __name__ == "__main__":
    unittest.main()
