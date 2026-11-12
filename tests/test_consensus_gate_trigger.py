"""Trigger-relevance gate for the merge-consensus workflow (Naya Delta, w307).

Proven defect: an issue_comment event fires for ANY comment on the PR — bot
pulses, questions, drive-bys. The gate ran the full consensus evaluation on a
non-verdict comment and painted a verdict about an unrelated PR onto the main
tip (check-run 116934064137 FAILED on tip 83806f4d0e33 while evaluating PR
#2536's body, fired by a 10:43:41Z issue_comment event).

These tests are network-free: they monkeypatch run_gate and drive main()
with environment only. T1 FAILS on the pre-fix code (run_gate is reached for
a non-verdict issue_comment) and PASSES after; T2/T3 are regression guards
that pass before and after.
"""
import importlib.util
import io
import os
import sys
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location(
    "check_merge_consensus",
    os.path.join(REPO_ROOT, "tools", "check_merge_consensus.py"))
cmc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cmc)

HEAD = "83806f4d0e335b223ba2f849fd19a7a7915fdcc6"

BASE_ENV = {
    "GH_TOKEN": "fake-token-for-test",
    "REPO": "SoulSchoolAcademy/NayaPOWER",
    "PR_NUMBER": "1",
    "HEAD_SHA": HEAD,
}


def run_main(extra_env):
    """Drive main(); return (run_gate_calls, captured_stdout)."""
    old = dict(os.environ)
    os.environ.update(BASE_ENV)
    os.environ.update(extra_env)
    calls = []
    orig_run_gate = cmc.run_gate
    cmc.run_gate = lambda *a: calls.append(a)
    buf = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buf
    try:
        cmc.main()
    finally:
        sys.stdout = old_stdout
        cmc.run_gate = orig_run_gate
        os.environ.clear()
        os.environ.update(old)
    return calls, buf.getvalue()


class TriggerRelevanceTest(unittest.TestCase):
    def test_issue_comment_without_verdict_skips_gate(self):
        """T1 — the w307 defect: a plain comment must NOT reach run_gate."""
        calls, out = run_main({
            "EVENT_NAME": "issue_comment",
            "TRIGGER_COMMENT_BODY": "quick question about the docs wording",
        })
        self.assertEqual(calls, [],
                         "gate reached run_gate for a non-verdict comment")
        self.assertIn("CONSENSUS GATE SKIPPED", out)

    def test_issue_comment_with_review_verdict_runs_gate(self):
        """T2 — regression: a genuine verdict comment still runs the gate."""
        calls, _ = run_main({
            "EVENT_NAME": "issue_comment",
            "TRIGGER_COMMENT_BODY":
                "[NAYA EPSILON · REVIEW] APPROVED — 9.5/10 on head " + HEAD,
        })
        self.assertEqual(len(calls), 1)

    def test_pull_request_event_runs_gate(self):
        """T3 — regression: pull_request events are unaffected by the gate."""
        calls, _ = run_main({
            "EVENT_NAME": "pull_request",
            "TRIGGER_COMMENT_BODY": "",
        })
        self.assertEqual(len(calls), 1)


if __name__ == "__main__":
    unittest.main()
