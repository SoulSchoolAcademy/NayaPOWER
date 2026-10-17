"""Cold-independent adversarial tests for read-only current-state parity."""
import importlib.util
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

PATH = Path(__file__).resolve().parents[1] / "tools" / "current_state_parity.py"
spec = importlib.util.spec_from_file_location("current_state_parity", PATH)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

MAIN = "d" * 40
NOW = datetime(2026, 10, 17, 15, 42, tzinfo=timezone.utc)
B = chr(96)


def src(d="#2721", mission="#2721", live="#2721", sha=MAIN, at="2026-10-17T15:40:00Z"):
    return {
        "directory": f"**Live coordination board:** [{d} — Team coordination feed](https://github.com/example)\nArchive: #2641",
        "mission": f"Live board = {mission}; prior venue #2641",
        "directive": f"*Compiled {at} from STATE-CORE.json*\nMain tip: {B}{sha}{B}\nLive venue: {live} (archive: #2537)",
    }


class CurrentStateParityTest(unittest.TestCase):
    def run_check(self, sources=None, sha=MAIN, now=NOW):
        return m.evaluate(src() if sources is None else sources, sha, now=now)

    def test_consistent_sources_pass(self):
        self.assertEqual(self.run_check()["state"], "PASS")

    def test_actual_stale_directive_venue_fails(self):
        d = self.run_check(src(live="#2641"))
        self.assertEqual(d["state"], "FAIL")
        self.assertIn("DIRECTIVE_VENUE_STALE", d["errors"])

    def test_mission_directory_conflict_fails(self):
        d = self.run_check(src(mission="#2641"))
        self.assertIn("DIRECTORY_MISSION_VENUE_CONFLICT", d["errors"])

    def test_old_directive_tip_fails(self):
        d = self.run_check(src(sha="a" * 40))
        self.assertIn("DIRECTIVE_MAIN_SHA_STALE", d["errors"])

    def test_missing_active_venue_unknown(self):
        self.assertEqual(self.run_check(src(live=""))["state"], "UNKNOWN")

    def test_missing_directory_unknown(self):
        self.assertEqual(self.run_check(src(d=""))["state"], "UNKNOWN")

    def test_missing_mission_unknown(self):
        self.assertEqual(self.run_check(src(mission=""))["state"], "UNKNOWN")

    def test_invalid_main_sha_unknown(self):
        self.assertEqual(self.run_check(sha="abcdef")["state"], "UNKNOWN")

    def test_old_compilation_fails(self):
        d = self.run_check(src(at="2026-10-17T12:40:00Z"))
        self.assertIn("DIRECTIVE_COMPILATION_STALE", d["errors"])

    def test_future_compilation_fails(self):
        d = self.run_check(src(at="2026-10-17T16:40:00Z"))
        self.assertIn("DIRECTIVE_COMPILATION_STALE", d["errors"])

    def test_archive_mention_does_not_poison_active(self):
        self.assertEqual(self.run_check()["state"], "PASS")

    def test_naive_clock_refused(self):
        with self.assertRaises(ValueError):
            self.run_check(now=datetime(2026, 10, 17, 15, 42))

    def test_offline_cli_fails_closed(self):
        with tempfile.TemporaryDirectory() as t:
            sources = src(live="#2641")
            files = {}
            for name, content in sources.items():
                file = Path(t) / (name + ".md")
                file.write_text(content, encoding="utf-8")
                files[name] = file
            cmd = [sys.executable, str(PATH), "--json", "--main-sha", MAIN]
            for name, file in files.items():
                cmd.extend(["--" + name + "-file", str(file)])
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            self.assertEqual(result.returncode, 1, result.stdout)
            self.assertEqual(json.loads(result.stdout)["state"], "FAIL")

    def test_partial_offline_unknown(self):
        z = subprocess.run([sys.executable, str(PATH), "--json", "--main-sha", MAIN],
                           capture_output=True, text=True, timeout=15)
        self.assertEqual(z.returncode, 2)
        self.assertEqual(json.loads(z.stdout)["state"], "UNKNOWN")

    def test_source_ids_fixed(self):
        self.assertEqual(m.ISSUES, {"directory": 1599, "mission": 2154, "directive": 2601})


if __name__ == "__main__":
    unittest.main()
