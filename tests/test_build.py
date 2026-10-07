import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class BuildTest(unittest.TestCase):
    def test_theme_css_is_the_join_of_src(self):
        joined = b"".join(p.read_bytes() for p in sorted((ROOT / "src").glob("*.css")))
        self.assertEqual((ROOT / "theme.css").read_bytes(), joined)

    def test_build_py_check_passes(self):
        result = subprocess.run([sys.executable, str(ROOT / "build.py"), "--check"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_build_sh_check_passes(self):
        result = subprocess.run([str(ROOT / "build.sh"), "--check"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
