import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import obsidian_window as w  # noqa: E402


class CommandTest(unittest.TestCase):
    def test_the_command_has_its_own_profile_and_a_debug_port(self):
        cmd = w.build_command(["obsidian"], "/tmp/p", 9444)
        self.assertEqual(cmd[0], "obsidian")
        self.assertIn("--user-data-dir=/tmp/p", cmd)
        self.assertIn("--remote-debugging-port=9444", cmd)

    def test_the_command_keeps_the_window_awake(self):
        self.assertIn("--disable-renderer-backgrounding", w.build_command(["obsidian"], "/tmp/p", 1))

    def test_other_obsidian_processes_do_not_count_our_own(self):
        ps = "electron43 /usr/lib/obsidian/app.asar --user-data-dir=/tmp/p\nelectron43 /usr/lib/obsidian/app.asar\nbash\n"
        self.assertEqual(w.other_obsidian_processes(ps, "/tmp/p"), 1)


class WatchTest(unittest.TestCase):
    def test_the_watched_files_are_the_config_and_the_json_files_of_each_vault(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            vault = tmp / "v"
            (vault / ".obsidian").mkdir(parents=True)
            (vault / ".obsidian" / "app.json").write_text("{}")
            config = tmp / "cfg"
            config.mkdir()
            (config / "obsidian.json").write_text(json.dumps({"vaults": {"a": {"path": str(vault)}}}))
            files = w.watched_files(config)
            self.assertEqual([f.name for f in files], ["obsidian.json", "app.json"])
            before = w.mtimes(files)
            (vault / ".obsidian" / "app.json").write_text('{"x": 1}')
            after = w.mtimes(files)
            self.assertNotEqual(before, after)

    def test_a_missing_config_gives_only_the_config_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(len(w.watched_files(Path(tmp))), 1)


class StateTest(unittest.TestCase):
    def test_a_missing_state_is_none_and_a_dead_process_is_not_alive(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertIsNone(w.read_state(tmp))
            self.assertFalse(w.alive({"pgid": 999999999, "profile": "/tmp/p"}))

    def test_a_process_with_another_command_line_is_not_taken_for_ours(self):
        import os
        self.assertFalse(w.alive({"pgid": os.getpid(), "profile": "/definitely/not/in/this/command/line"}))

    def test_parse_splits_options_and_words(self):
        args, rest = w.parse(["start", "--mode", "dark", "--port", "9400"])
        self.assertEqual((args, rest), ({"--mode": "dark", "--port": "9400"}, ["start"]))


if __name__ == "__main__":
    unittest.main()
