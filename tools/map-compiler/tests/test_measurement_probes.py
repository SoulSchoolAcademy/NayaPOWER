"""Regression tests for the two honesty-critical live measurement probes."""

import datetime
import json
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.abspath(__file__))))

import map_compiler


class _Response:
    def __init__(self, headers=None):
        self.headers = headers or {}

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


class TestCaptureProbe(unittest.TestCase):
    def test_latest_failure_is_red_even_if_older_run_succeeded(self):
        now = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
        runs = {"workflow_runs": [
            {"status": "completed", "conclusion": "failure", "created_at": now,
             "event": "workflow_dispatch"},
            {"status": "completed", "conclusion": "success", "created_at": now,
             "event": "schedule"},
        ]}
        with patch.object(map_compiler, "gh_get", return_value=(runs, None)):
            result = map_compiler.probe_capture({"gh_token": "test-token"})
        self.assertEqual(result["status"], "red")
        self.assertIn("latest run completed/failure", result["evidence"])
        self.assertIn("recent success: True", result["evidence"])

    def test_in_progress_latest_run_is_unknown_not_stale_green(self):
        now = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
        runs = {"workflow_runs": [
            {"status": "in_progress", "conclusion": None, "created_at": now,
             "event": "workflow_dispatch"},
            {"status": "completed", "conclusion": "success", "created_at": now,
             "event": "schedule"},
        ]}
        with patch.object(map_compiler, "gh_get", return_value=(runs, None)):
            result = map_compiler.probe_capture({"gh_token": "test-token"})
        self.assertEqual(result["status"], "unknown")
        self.assertIn("latest run in_progress/None", result["evidence"])


class TestSupabaseSchemaProbe(unittest.TestCase):
    def _run_probe(self, exposed_tables):
        spec = {"paths": {"/" + table: {} for table in exposed_tables}}
        with patch.object(map_compiler, "fetch_text", return_value=json.dumps(spec)), patch.object(
            map_compiler.urllib.request, "urlopen", return_value=_Response({"Content-Range": "0-0/12"})
        ):
            return map_compiler.probe_supabase_tables({
                "supabase_url": "https://example.invalid",
                "supabase_key": "test-key",
            })

    def test_missing_expected_table_is_red_even_when_other_counts_succeed(self):
        exposed = map_compiler.KNOWN_TABLES[:-1]
        result = self._run_probe(exposed)
        self.assertEqual(result["status"], "red")
        self.assertIn("missing expected tables:", result["evidence"])
        self.assertIn(map_compiler.KNOWN_TABLES[-1], result["evidence"])
        self.assertIn("7/8 expected tables exposed", result["evidence"])

    def test_all_expected_tables_exposed_and_countable_is_green(self):
        result = self._run_probe(map_compiler.KNOWN_TABLES)
        self.assertEqual(result["status"], "green")
        self.assertIn("8/8 expected tables exposed", result["evidence"])


if __name__ == "__main__":
    unittest.main()
