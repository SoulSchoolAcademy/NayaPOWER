"""Tests for learn_clock_broadcast_wire.py (Naya Eta, w173).

The claim under test: a real carried item from the broadcast collect pass
produces a real T0 emit — stamped with the ITEM's timestamp (the evidence's
time), never with now. Plus the wire's two load-bearing properties:
idempotency (one event -> one T0, re-runs emit nothing) and fail-closed
skips (unparseable timestamps are never guessed).
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from learn_clock import LearnClock  # noqa: E402
from learn_clock_broadcast_wire import (  # noqa: E402
    _event_ts, _fingerprint, _is_t0_event, wire_fresh_t0,
)

BASE = datetime(2026, 10, 14, 18, 5, tzinfo=timezone.utc)


def item(at, kind="DIARY", text="lesson text here", why=""):
    return {"at": at, "kind": kind, "text": text, "why": why}


def harness(tmp_path):
    clock = LearnClock(tmp_path / "lc.jsonl")
    wm_path = tmp_path / "t0wm.json"
    meta_rows = []
    return clock, wm_path, meta_rows


def test_carried_item_emits_t0_with_event_timestamp(tmp_path):
    """The wired path: real item -> real T0, stamped at the event's time."""
    clock, wm_path, meta_rows = harness(tmp_path)
    before = datetime.now(timezone.utc)
    rep = wire_fresh_t0([item(BASE.isoformat())], clock=clock,
                        watermark_path=wm_path,
                        meta_writer=lambda *a, **k: meta_rows.append((a, k)))
    assert len(rep["emitted"]) == 1
    e = rep["emitted"][0]
    assert e["lesson_id"].startswith("LC-20261014-")
    # the T0 row carries the EVENT's timestamp, not now
    assert e["ts"] == BASE.isoformat()
    rows = [json.loads(l) for l in
            (tmp_path / "lc.jsonl").read_text().splitlines()]
    assert len(rows) == 1
    assert rows[0]["stage"] == 0 and rows[0]["stage_name"] == "T0_EVENT"
    assert rows[0]["ts"] == BASE.isoformat()
    assert datetime.fromisoformat(rows[0]["ts"]) < before
    # watermark maps the event to its lesson for T1+ continuation
    wm = json.loads(wm_path.read_text())
    assert wm[_fingerprint(item(BASE.isoformat()))] == e["lesson_id"]
    # meta row written with the evidence
    assert len(meta_rows) == 1


def test_rerun_emits_nothing_idempotent(tmp_path):
    clock, wm_path, _ = harness(tmp_path)
    items = [item(BASE.isoformat(), text="first"),
             item("2026-10-14T18:06:00+00:00", text="second")]
    r1 = wire_fresh_t0(items, clock=clock, watermark_path=wm_path,
                       meta_writer=lambda *a, **k: None)
    r2 = wire_fresh_t0(items, clock=clock, watermark_path=wm_path,
                       meta_writer=lambda *a, **k: None)
    assert len(r1["emitted"]) == 2 and len(r1["already"]) == 0
    assert len(r2["emitted"]) == 0 and len(r2["already"]) == 2
    rows = (tmp_path / "lc.jsonl").read_text().strip().splitlines()
    assert len(rows) == 2  # one T0 per event, never duplicated
    ids = [e["lesson_id"] for e in r1["emitted"]]
    assert ids[0] != ids[1]  # distinct events -> distinct lessons


def test_unparseable_timestamp_skipped_fail_closed(tmp_path):
    clock, wm_path, meta_rows = harness(tmp_path)
    rep = wire_fresh_t0(
        [item("sometime yesterday"), item(BASE.isoformat())],
        clock=clock, watermark_path=wm_path,
        meta_writer=lambda *a, **k: meta_rows.append((a, k)))
    assert len(rep["skipped"]) == 1
    assert rep["skipped"][0]["reason"] == "unparseable at"
    assert len(rep["emitted"]) == 1  # the good item still wired
    rows = (tmp_path / "lc.jsonl").read_text().strip().splitlines()
    assert len(rows) == 1


def test_date_only_uses_noon_utc_convention(tmp_path):
    """TOOLS.md/dock evidence is day-granular: noon UTC, never a guess."""
    clock, wm_path, _ = harness(tmp_path)
    rep = wire_fresh_t0([item("2026-10-14", kind="TOOLS")], clock=clock,
                        watermark_path=wm_path,
                        meta_writer=lambda *a, **k: None)
    assert rep["emitted"][0]["ts"] == "2026-10-14T12:00:00+00:00"


def test_wm_tagged_items_use_stable_identity(tmp_path):
    """Items carrying broadcast's own _wm tag fingerprint on it."""
    clock, wm_path, _ = harness(tmp_path)
    a = item("2026-10-14", kind="TOOLS", text="title one")
    a["_wm"] = ("tools", "2026-10-14", "title one")
    b = dict(a, text="title one (edited summary)")
    assert _fingerprint(a) == _fingerprint(b)  # same event, same key
    rep = wire_fresh_t0([a, b], clock=clock, watermark_path=wm_path,
                        meta_writer=lambda *a_, **k: None)
    assert len(rep["emitted"]) == 1 and len(rep["already"]) == 1


def test_event_ts_rejects_empty_and_garbage():
    assert _event_ts(item("")) is None
    assert _event_ts({}) is None
    assert _event_ts(item("not a date")) is None
    # naive ISO without timezone is rejected (fail-closed: no guessing tz)
    assert _event_ts(item("2026-10-14T18:05:00")) is None


def test_passed_drills_are_not_t0_events():
    """Routine practice must not fill the clock with unfinishable T0s."""
    passed = item(BASE.isoformat(), kind="DRILL",
                  text="P-001 drill passed: score your options")
    failed = item(BASE.isoformat(), kind="DRILL",
                  text="P-002 drill FAILED: recommend-don't-ask violated")
    assert _is_t0_event(passed) is False
    assert _is_t0_event(failed) is True
    assert _is_t0_event(item(BASE.isoformat(), kind="DIARY")) is True
    assert _is_t0_event(item(BASE.isoformat(), kind="VERIFIED FIX")) is True
    assert _is_t0_event(item(BASE.isoformat(), kind="TOOLS")) is True
    assert _is_t0_event(item(BASE.isoformat(), kind="DOCK")) is True


def test_collect_discovers_all_broadcast_sources():
    """A new collect_* source on the bus must not be silently omitted."""
    import types
    from learn_clock_broadcast_wire import collect_fresh_items
    fake = types.SimpleNamespace()
    fake.collect_alpha = lambda: [item("2026-10-14T01:00:00+00:00",
                                       kind="DIARY", text="alpha")]
    fake.collect_beta = lambda: [item("2026-10-14T02:00:00+00:00",
                                      kind="DRILL", text="P-1 drill passed: x")]
    fake.not_a_collector = lambda: [item("2026-10-14T03:00:00+00:00")]
    items = collect_fresh_items(broadcast_mod=fake)
    assert [i["text"] for i in items] == ["alpha"]  # beta filtered (passed)
