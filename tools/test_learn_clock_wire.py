#!/usr/bin/env python3
"""Tests for learn_clock_wire.py — run against a TEMP clock, never the live one.

The wire's contract: capture mints T0+T1 in order; triage emits T2 only after
T1 (the clock raises OutOfOrderError otherwise); status reports the dashboard.
Retroactive --ts must not regress.
"""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import learn_clock_wire as wire
import learn_hook as hook
from learn_clock import LearnClock, OutOfOrderError


class Args:
    def __init__(self, **kw):
        self.__dict__.update(kw)


class WireTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.clock_path = Path(self.tmp.name) / "clock.jsonl"
        self._env = dict(os.environ)
        os.environ["LEARN_CLOCK_WATERMARK"] = str(Path(self.tmp.name) / "wm.json")
        self._orig = LearnClock.__init__

        def patched(self, path=self.clock_path):
            self.path = Path(path)
            self.path.parent.mkdir(parents=True, exist_ok=True)

        LearnClock.__init__ = patched
        # _next_lesson_id reads clock.path — patched clock honors the temp path.
        # _meta_write writes into CLOCK_DIR; redirect it to the temp dir.
        self._orig_meta = wire._meta_write
        tmp_meta = Path(self.tmp.name) / "meta.jsonl"

        def meta(lesson_id, stage, title, evidence, event_ts=None, **extra):
            with open(tmp_meta, "a", encoding="utf-8") as f:
                f.write(json.dumps({"lesson_id": lesson_id, "stage": stage,
                                    "title": title, "evidence": evidence,
                                    "ts": event_ts, **extra}) + "\n")

        wire._meta_write = meta
        self.meta_path = tmp_meta

    def tearDown(self):
        LearnClock.__init__ = self._orig
        wire._meta_write = self._orig_meta
        os.environ.clear()
        os.environ.update(self._env)
        self.tmp.cleanup()

    def test_capture_mints_t0_t1(self):
        # Alpha w185: never date-hardcode the minted id — _next_lesson_id
        # derives the date from the wall clock, so capture the id from the
        # call's own stdout instead of asserting a fixed LC- prefix.
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = wire.cmd_capture(Args(title="test lesson", evidence="sign-out #1",
                                       ts_event="2026-10-14T04:00:00+00:00"))
        self.assertEqual(rc, 0)
        out, _ = json.JSONDecoder().raw_decode(buf.getvalue())
        lesson_id = out["lesson_id"]
        clock = LearnClock(self.clock_path)
        st = clock.status(lesson_id)
        self.assertEqual(st["complete_through"], "T1_CAPTURED")
        self.assertEqual(st["hit"], ["T0_EVENT", "T1_CAPTURED"])

    def test_triage_after_capture(self):
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = wire.cmd_capture(Args(title="t", evidence="e", ts_event=None))
        self.assertEqual(rc, 0)
        out, _ = json.JSONDecoder().raw_decode(buf.getvalue())
        lesson_id = out["lesson_id"]
        rc = wire.cmd_triage(Args(lesson_id=lesson_id, verdict="PROMOTE",
                                  evidence="fold entry", ts=None))
        self.assertEqual(rc, 0)
        clock = LearnClock(self.clock_path)
        self.assertEqual(clock.status(lesson_id)["complete_through"], "T2_TRIAGED")

    def test_triage_without_capture_raises(self):
        with self.assertRaises(OutOfOrderError):
            wire.cmd_triage(Args(lesson_id="LC-20261014-999", verdict="LOG",
                                 evidence="e", ts=None))

    def test_retroactive_ts_no_regression(self):
        import io, contextlib

        def capture(**kw):
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = wire.cmd_capture(Args(**kw))
            out, _ = json.JSONDecoder().raw_decode(buf.getvalue())
            return rc, out["lesson_id"]

        rc, lid1 = capture(title="t", evidence="e",
                           ts_event="2026-10-14T04:00:00+00:00")
        self.assertEqual(rc, 0)
        # T1 stamped at now; a T2 ts must be >= T1's ts, so valid triage uses now.
        rc = wire.cmd_triage(Args(lesson_id=lid1, verdict="DROP",
                                  evidence="e", ts=None))
        self.assertEqual(rc, 0)
        # regressing ts must raise
        rc, lid2 = capture(title="t2", evidence="e", ts_event=None)
        self.assertEqual(rc, 0)
        with self.assertRaises(OutOfOrderError):
            wire.cmd_triage(Args(lesson_id=lid2, verdict="DROP",
                                 evidence="e", ts="2020-01-01T00:00:00+00:00"))

    def test_status_counts_verified(self):
        wire.cmd_capture(Args(title="t", evidence="e", ts_event=None))
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            wire.cmd_status(Args())
        out = json.loads(buf.getvalue())
        self.assertEqual(out["total"], 1)
        self.assertEqual(out["verified_T6"], 0)

    def test_meta_ts_matches_clock_ts_retroactive(self):
        """Zeta w141 P-003: meta ts must equal the clock row's event ts."""
        clock = LearnClock(self.clock_path)
        clock.emit("LC-20261014-001", 0, ts="2026-10-14T04:00:00+00:00")
        clock.emit("LC-20261014-001", 1, ts="2026-10-14T04:10:00+00:00")
        wire.cmd_triage(Args(lesson_id="LC-20261014-001", verdict="PROMOTE",
                             evidence="fold", ts="2026-10-14T04:47:00+00:00"))
        clock = LearnClock(self.clock_path)
        t2_clock = [json.loads(l) for l in self.clock_path.read_text().splitlines()
                    if json.loads(l)["stage"] == 2][0]
        meta_rows = [json.loads(l) for l in self.meta_path.read_text().splitlines()]
        t2_meta = [r for r in meta_rows if r["stage"] == 2][0]
        self.assertEqual(t2_meta["ts"], t2_clock["ts"])
        self.assertEqual(t2_meta["verdict"], "PROMOTE")


class WireT6T7Tests(unittest.TestCase):
    """Alpha w189: verify (T6) and compound (T7) follow the triage leg's shape —
    evidence required, clock enforces order, fail-closed on OUT_OF_ORDER.
    T6's live owner is the dispatcher fold (different-seat independent
    verification); T7's live owner is the director review (adopted_utc)."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.clock_path = Path(self.tmp.name) / "clock.jsonl"
        self._env = dict(os.environ)
        os.environ["LEARN_CLOCK_WATERMARK"] = str(Path(self.tmp.name) / "wm.json")
        self._orig = LearnClock.__init__

        def patched(self, path=self.clock_path):
            self.path = Path(path)
            self.path.parent.mkdir(parents=True, exist_ok=True)

        LearnClock.__init__ = patched
        self._orig_meta = wire._meta_write
        tmp_meta = Path(self.tmp.name) / "meta.jsonl"

        def meta(lesson_id, stage, title, evidence, event_ts=None, **extra):
            with open(tmp_meta, "a", encoding="utf-8") as f:
                f.write(json.dumps({"lesson_id": lesson_id, "stage": stage,
                                    "title": title, "evidence": evidence,
                                    "ts": event_ts, **extra}) + "\n")

        wire._meta_write = meta
        self.meta_path = tmp_meta

    def tearDown(self):
        LearnClock.__init__ = self._orig
        wire._meta_write = self._orig_meta
        os.environ.clear()
        os.environ.update(self._env)
        self.tmp.cleanup()

    def _mint_through_t5(self, lid):
        clock = LearnClock()
        for stage in range(6):  # T0..T5 staged out-of-band (hook CLI owns T3+ today)
            clock.emit(lid, stage)
        return clock

    def test_verify_without_t5_fails_closed(self):
        clock2 = LearnClock()
        clock2.emit("LC-20990101-002", 0)
        clock2.emit("LC-20990101-002", 1)
        rc = wire.main(["verify", "LC-20990101-002", "--evidence", "comment-123"])
        self.assertEqual(rc, 2)  # OUT_OF_ORDER, fail-closed

    def test_verify_after_t5_marks_verified(self):
        lid = "LC-20990101-003"
        self._mint_through_t5(lid)
        rc = wire.main(["verify", lid, "--evidence", "comment-123"])
        self.assertEqual(rc, 0)
        st = LearnClock().status(lid)
        self.assertNotIn("T6_VERIFIED", st["missing"])

    def test_verify_writes_t6_meta_row(self):
        lid = "LC-20990101-004"
        self._mint_through_t5(lid)
        wire.main(["verify", lid, "--evidence", "comment-123"])
        rows = [json.loads(l) for l in self.meta_path.read_text().splitlines()]
        t6 = [r for r in rows if r["lesson_id"] == lid and r["stage"] == 6]
        self.assertEqual(len(t6), 1)
        self.assertIn("comment-123", t6[0]["evidence"])

    def test_compound_without_verify_fails_closed(self):
        lid = "LC-20990101-005"
        self._mint_through_t5(lid)
        rc = wire.main(["compound", lid, "--evidence", "review-note-7"])
        self.assertEqual(rc, 2)  # T7 needs T6 first

    def test_compound_after_verify_complete_through_t7(self):
        lid = "LC-20990101-006"
        self._mint_through_t5(lid)
        self.assertEqual(wire.main(["verify", lid, "--evidence", "comment-123"]), 0)
        self.assertEqual(wire.main(["compound", lid, "--evidence", "review-note-7"]), 0)
        st = LearnClock().status(lid)
        self.assertNotIn("T7_COMPOUNDED", st["missing"])
        self.assertTrue(st["complete_through"].startswith("T7"))

    def test_evidence_required_fail_closed(self):
        lid = "LC-20990101-007"
        self._mint_through_t5(lid)
        with self.assertRaises(SystemExit):
            wire.main(["verify", lid])  # --evidence required by argparse


class WireWatermarkTests(unittest.TestCase):
    """Eta w175: the wire's capture must consult t0-broadcast-watermark.json
    BEFORE minting a lesson id, mirroring Alpha's w174 capture-side check
    (learn_hook.capture_t0). Run against a TEMP clock and TEMP watermark,
    never the live ones."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.clock_path = Path(self.tmp.name) / "clock.jsonl"
        self.wm_path = Path(self.tmp.name) / "wm.json"
        self._env = dict(os.environ)
        os.environ["LEARN_CLOCK_WATERMARK"] = str(self.wm_path)
        self._orig = LearnClock.__init__

        def patched(self, path=self.clock_path):
            self.path = Path(path)
            self.path.parent.mkdir(parents=True, exist_ok=True)

        LearnClock.__init__ = patched
        self._orig_meta = wire._meta_write
        tmp_meta = Path(self.tmp.name) / "meta.jsonl"

        def meta(lesson_id, stage, title, evidence, event_ts=None, **extra):
            with open(tmp_meta, "a", encoding="utf-8") as f:
                f.write(json.dumps({"lesson_id": lesson_id, "stage": stage,
                                    "title": title, "evidence": evidence,
                                    "ts": event_ts, **extra}) + "\n")

        wire._meta_write = meta
        self.meta_path = tmp_meta

    def tearDown(self):
        LearnClock.__init__ = self._orig
        wire._meta_write = self._orig_meta
        os.environ.clear()
        os.environ.update(self._env)
        self.tmp.cleanup()

    def _rows(self):
        if not self.clock_path.exists():
            return []
        return [json.loads(l) for l in self.clock_path.read_text().splitlines()
                if l.strip()]

    def _capture(self, **kw):
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = wire.cmd_capture(Args(**kw))
        out, _ = json.JSONDecoder().raw_decode(buf.getvalue())
        return rc, out

    def _seed_broadcast(self, kind, at, title, lesson_id):
        """A broadcast T0 that already exists: watermark entry + clock T0 row."""
        LearnClock().emit(lesson_id, 0, ts=at)
        hook._record_watermark(self.wm_path,
                               [hook._capture_fingerprint(kind, at, title)],
                               lesson_id)

    def test_duplicate_t0_reused_no_double_mint(self):
        """Broadcast T0 exists -> wire reuses the id, mints NO second T0."""
        at = "2026-10-14T18:05:00+00:00"
        self._seed_broadcast("DIARY", at, "dock line lesson", "LC-20261014-007")
        rc, out = self._capture(title="dock line lesson", evidence="sign-out #1",
                                ts_event=at, kind="DIARY")
        self.assertEqual(rc, 0)
        self.assertTrue(out["duplicate_prevented"])
        self.assertEqual(out["lesson_id"], "LC-20261014-007")
        t0 = [r for r in self._rows() if r["stage"] == 0]
        self.assertEqual(len(t0), 1)  # exactly one T0 row, no duplicate
        self.assertEqual(t0[0]["lesson_id"], "LC-20261014-007")
        self.assertEqual(self._rows()[1]["stage_name"], "T1_CAPTURED")

    def test_malformed_ts_event_fails_closed(self):
        """Malformed --ts-event -> no mint, no clock row, no watermark write."""
        import io, contextlib
        buf, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(err):
            rc = wire.cmd_capture(Args(title="bad ts lesson", evidence="e",
                                       ts_event="not-a-time", kind="DIARY"))
        self.assertNotEqual(rc, 0)
        self.assertIn("MALFORMED_TS", err.getvalue())
        self.assertEqual(buf.getvalue().strip(), "")  # nothing printed on success path
        self.assertEqual(self._rows(), [])
        self.assertFalse(self.wm_path.exists())

    def test_fresh_mint_records_watermark_and_retry_idempotent(self):
        """Fresh capture records all fingerprint variants; an identical retry
        reuses the id and emits no second T0."""
        at = "2026-10-14T19:00:00+00:00"
        rc, out = self._capture(title="brand new", evidence="sign-out #3",
                                ts_event=at, kind="DIARY")
        self.assertEqual(rc, 0)
        self.assertFalse(out["duplicate_prevented"])
        lid = out["lesson_id"]
        wm = json.loads(self.wm_path.read_text(encoding="utf-8"))
        self.assertIn(hook._capture_fingerprint("DIARY", at, "brand new"), wm)
        self.assertEqual(wm[hook._capture_fingerprint("DIARY", at, "brand new")], lid)
        # identical retry: duplicate prevented, id reused, still exactly one T0
        rc2, out2 = self._capture(title="brand new", evidence="sign-out #3",
                                  ts_event=at, kind="DIARY")
        self.assertEqual(rc2, 0)
        self.assertTrue(out2["duplicate_prevented"])
        self.assertEqual(out2["lesson_id"], lid)
        t0 = [r for r in self._rows() if r["stage"] == 0]
        self.assertEqual(len(t0), 1)


if __name__ == "__main__":
    unittest.main()
