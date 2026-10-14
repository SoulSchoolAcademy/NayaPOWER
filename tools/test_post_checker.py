#!/usr/bin/env python3
"""Tests for tools/post_checker.py — the three-level post protocol gate.

Run:  python3 -m unittest tools.test_post_checker -v
      (from the repo root)
"""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from tools.post_checker import (
    check,
    check_pulse,
    check_receipt,
    check_event,
    post_sha,
)

SHA = "ce6a396f388722a0bbe84899dd23123e2259e574"  # 40 hex, cited live read
RUNID = "115834058324"


def fresh_log():
    d = tempfile.mkdtemp(prefix="postlog-")
    return os.path.join(d, "post-log.jsonl")


class PulseTests(unittest.TestCase):
    def test_pass_state_change(self):
        flags, _ = check("PULSE", "Lane 1 claimed, starting #2568 gate work")
        self.assertEqual(flags, [])

    def test_reject_no_work(self):
        flags, _ = check("PULSE", "Wave 170: NO_WORK — nothing to do")
        self.assertTrue(any("heartbeat" in f for f in flags))

    def test_reject_list_drained(self):
        flags, _ = check("PULSE", "LIST-DRAINED / nothing to report")
        self.assertTrue(any("heartbeat" in f for f in flags))

    def test_reject_too_long(self):
        flags, _ = check("PULSE", "starting work " + "x" * 300)
        self.assertTrue(any("chars" in f for f in flags))

    def test_reject_no_state_change(self):
        flags, _ = check("PULSE", "hello team, thinking about the mission")
        self.assertTrue(any("state change" in f for f in flags))

    def test_reject_still_working_no_info(self):
        flags, _ = check("PULSE", "just checking in, still working")
        self.assertTrue(any("still working" in f for f in flags))


class ReceiptTests(unittest.TestCase):
    GOOD = (
        "[Naya Verity Narzan · SIGN-OUT] Lane 1 — #2568 body edit\n"
        "Mission: repair the gate-vocabulary parser. VERDICT: DONE — "
        "parser accepts Clarity/Resolve/Verity seats, 12/12 fixtures green. "
        "Why it worked: the matcher read the live seat list."
    )

    def test_pass(self):
        flags, _ = check("RECEIPT", self.GOOD)
        self.assertEqual(flags, [])

    def test_reject_bare_naya(self):
        bad = "Naya signing out — DONE: fixed the parser"
        flags, _ = check("RECEIPT", bad)
        self.assertTrue(any("naming-law" in f for f in flags))

    def test_reject_missing_verdict(self):
        bad = "[Naya Alpha · SIGN-OUT] Lane 2 — worked on the drill, more later"
        flags, _ = check("RECEIPT", bad)
        self.assertTrue(any("verdict" in f for f in flags))

    def test_reject_too_long(self):
        bad = "[Naya Theta · SIGN-OUT] VERDICT: DONE — " + "detail " * 300
        flags, _ = check("RECEIPT", bad)
        self.assertTrue(any("chars" in f for f in flags))

    def test_reject_oath_ritual(self):
        bad = (
            "[Naya Iota · SIGN-OUT] VERDICT: DONE — kit drafted\n"
            "Oath in my own words: I measure before I act.\n"
            "The oath guides my hands today.\n"
            "I speak the oath again for the record."
        )
        flags, _ = check("RECEIPT", bad)
        self.assertTrue(any("oath" in f for f in flags))


class EventTests(unittest.TestCase):
    def test_pass_with_cited_evidence(self):
        text = (
            "[NAYA 5 · MERGE INTENT] PR #2597 at head " + SHA
            + " — CI 19/19 green, check-run " + RUNID
            + ". VERDICT: ready for different-seat merge."
        )
        flags, append = check("EVENT", text, fresh_log())
        self.assertEqual(flags, [])
        self.assertTrue(append)

    def test_flag_bare_ci_green(self):
        # The #2597 incident shape: claim, no cited live read.
        text = (
            "[MERGE INTENT] PR #2597 — CI 16/16 required green, "
            "all checks passing. Ready to merge."
        )
        flags, _ = check("EVENT", text, fresh_log())
        self.assertTrue(any("claim-check" in f for f in flags))

    def test_flag_fraction_without_citation(self):
        text = "Tests 45/45 green — merging now."
        flags, _ = check("EVENT", text, fresh_log())
        self.assertTrue(any("claim-check" in f for f in flags))

    def test_pass_claim_with_runid_only(self):
        text = "CI green on the head, check-run " + RUNID + " observed."
        flags, _ = check("EVENT", text, fresh_log())
        self.assertEqual(flags, [])

    def test_dedup_exact_duplicate(self):
        log = fresh_log()
        text = "Merge intent posted for PR #2597 — awaiting no-objection."
        flags, append = check("EVENT", text, log)
        self.assertEqual(flags, [])
        self.assertTrue(append)
        # simulate the worker actually posting (tool appends on PASS in CLI;
        # here append explicitly)
        from tools.post_checker import append_log, resolve_log_path

        append_log(log, text)
        flags2, _ = check("EVENT", text, log)
        self.assertTrue(any("duplicate" in f for f in flags2))

    def test_dedup_window_expired(self):
        import json
        from datetime import datetime, timedelta, timezone

        log = fresh_log()
        text = "Merge intent posted for PR #2597 — awaiting no-objection."
        old = {
            "sha": post_sha(text),
            "ts": (datetime.now(timezone.utc) - timedelta(hours=7)).isoformat(),
            "norm": text.lower(),
            "head": text[:80],
        }
        with open(log, "w", encoding="utf-8") as fh:
            fh.write(json.dumps(old) + "\n")
        flags, _ = check("EVENT", text, log)
        self.assertEqual(flags, [])  # outside the 6h window: passes

    def test_dedup_near_duplicate(self):
        from tools.post_checker import append_log

        log = fresh_log()
        a = "Merge intent for PR #2597 posted — no-objection window opens now."
        append_log(log, a)
        b = "Merge intent for PR #2597 posted — no-objection window opens today."
        flags, _ = check("EVENT", b, log)
        self.assertTrue(any("near-duplicate" in f for f in flags))


class StdinTests(unittest.TestCase):
    def test_stdin_mode(self):
        import io
        from unittest import mock
        from tools.post_checker import main

        with mock.patch("sys.stdin", io.StringIO("starting lane 2 work")):
            with mock.patch("sys.stdout", io.StringIO()):
                self.assertEqual(main(["--level", "PULSE"]), 0)

    def test_stdin_flagged(self):
        import io
        from unittest import mock
        from tools.post_checker import main

        with mock.patch("sys.stdin", io.StringIO("NO_WORK")):
            with mock.patch("sys.stdout", io.StringIO()):
                self.assertEqual(main(["--level", "PULSE"]), 1)


if __name__ == "__main__":
    unittest.main()
