"""Tests for the capture-path broadcast-watermark check (Naya Alpha, w174).

Eta's w173 Next: the capture path (learn_hook t0) must consult
t0-broadcast-watermark.json BEFORE minting a lesson id. If the item's T0 is
already broadcast, no duplicate is minted — the existing lesson id is
returned so the fold flow continues it at t1..t7. Malformed timestamps fail
closed: no mint, no clock row, no watermark write.
"""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

import learn_hook  # noqa: E402
from learn_clock import LearnClock  # noqa: E402
from learn_hook import (MalformedTimestampError, _canonical_event_ts,  # noqa: E402
                        _capture_fingerprint, capture_t0)
from learn_clock_broadcast_wire import _event_ts as wire_event_ts  # noqa: E402
from learn_clock_broadcast_wire import _fingerprint as wire_fingerprint  # noqa: E402


def harness(tmp_path):
    return LearnClock(tmp_path / "lc.jsonl"), tmp_path / "wm.json"


def seed(wm_path, kind, at, title, lesson_id):
    fp = _capture_fingerprint(kind, at, title)
    wm_path.write_text(json.dumps({fp: lesson_id}, indent=1) + "\n",
                       encoding="utf-8")
    return fp


def rows_of(clock_path):
    p = Path(clock_path)
    if not p.exists():
        return []
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()]


def test_duplicate_prevented_returns_existing_id(tmp_path):
    """The core contract: broadcast T0 exists -> mint nothing, reuse the id."""
    clock, wm = harness(tmp_path)
    at = "2026-10-14T18:05:00+00:00"
    seed(wm, "DIARY", at, "dock line lesson", "LC-20261014-007")
    rep = capture_t0(clock, wm, title="dock line lesson", evidence="proof",
                     ts=at, kind="DIARY")
    assert rep["duplicate_prevented"] is True
    assert rep["emitted"] is False
    assert rep["lesson_id"] == "LC-20261014-007"
    assert rows_of(tmp_path / "lc.jsonl") == []  # no T0 row minted
    assert not (tmp_path / "meta.jsonl").exists()  # (function writes no meta)


def test_z_and_offset_serializations_dedupe(tmp_path):
    """The wire fingerprints the RAW at; collectors emit Z-style (as in the
    live watermark) while callers may pass +00:00 — all serializations of one
    instant must hit the same entry."""
    clock, wm = harness(tmp_path)
    seed(wm, "DIARY", "2026-10-13T08:32:53Z", "some lesson", "LC-20261014-007")
    rep = capture_t0(clock, wm, title="some lesson", evidence="proof",
                     ts="2026-10-13T08:32:53+00:00", kind="DIARY")
    assert rep["duplicate_prevented"] is True
    assert rep["lesson_id"] == "LC-20261014-007"
    assert rows_of(tmp_path / "lc.jsonl") == []


def test_fresh_item_minted_and_retry_idempotent(tmp_path):
    clock, wm = harness(tmp_path)
    at = "2026-10-14T18:05:00+00:00"
    rep = capture_t0(clock, wm, title="brand new", evidence="proof", ts=at)
    assert rep["emitted"] is True and rep["duplicate_prevented"] is False
    assert rep["lesson_id"].startswith("LC-")
    rows = rows_of(tmp_path / "lc.jsonl")
    assert len(rows) == 1
    assert rows[0]["stage"] == 0 and rows[0]["ts"] == at
    # the mint recorded the fingerprint: an identical retry reuses, never duplicates
    rep2 = capture_t0(clock, wm, title="brand new", evidence="proof", ts=at)
    assert rep2["duplicate_prevented"] is True
    assert rep2["lesson_id"] == rep["lesson_id"]
    assert len(rows_of(tmp_path / "lc.jsonl")) == 1
    wm_data = json.loads(wm.read_text())
    assert rep["fingerprint"] in wm_data


def test_no_ts_means_now(tmp_path):
    clock, wm = harness(tmp_path)
    rep = capture_t0(clock, wm, title="observed just now", evidence="proof")
    assert rep["emitted"] is True
    from datetime import datetime
    assert datetime.fromisoformat(rep["ts"]).tzinfo is not None


@pytest.mark.parametrize("bad", [
    "sometime yesterday", "2026-10-14T18:05:00", "", "   ",
    "2026-13-45", "not a date", "2026-10-14T25:00:00Z",
])
def test_malformed_timestamp_fails_closed(tmp_path, bad):
    """No mint, no clock row, no watermark write — the timestamp is never guessed."""
    clock, wm = harness(tmp_path)
    with pytest.raises(MalformedTimestampError):
        capture_t0(clock, wm, title="x", evidence="proof", ts=bad)
    assert rows_of(tmp_path / "lc.jsonl") == []
    assert not wm.exists()


def test_date_only_uses_noon_utc_convention(tmp_path):
    """Day-granular evidence stamps noon UTC (the wire's convention), keeping
    every clock row tz-aware so latency math can never mix naive/aware."""
    clock, wm = harness(tmp_path)
    rep = capture_t0(clock, wm, title="day granular", evidence="proof",
                     ts="2026-10-14")
    assert rep["emitted"] is True
    assert rep["ts"] == "2026-10-14T12:00:00+00:00"
    rows = rows_of(tmp_path / "lc.jsonl")
    assert rows[0]["ts"] == "2026-10-14T12:00:00+00:00"
    from datetime import datetime
    assert datetime.fromisoformat(rows[0]["ts"]).tzinfo is not None


@pytest.mark.parametrize("kind,at,text", [
    ("DIARY", "2026-10-13T08:32:53Z", "some diary text"),
    ("TOOLS", "2026-10-14", "tools note"),
    ("DOCK", "2026-10-12T22:35:52.571734Z", "dock line"),
    ("DRILL", "2026-10-14T18:05:00+00:00", "P-002 drill FAILED: x"),
    ("VERIFIED FIX", "2026-10-14T21:46:40Z", "fix shipped"),
])
def test_fingerprint_parity_with_wire(kind, at, text):
    """One convention, two modules: the capture fingerprint must equal the
    wire's fingerprint for the same item, or cross-path dedup silently dies."""
    assert (_capture_fingerprint(kind, at, text)
            == wire_fingerprint({"kind": kind, "at": at, "text": text}))


@pytest.mark.parametrize("raw", [
    "2026-10-13T08:32:53Z", "2026-10-14T18:05:00+00:00",
    "2026-10-12T22:35:52.571734Z", "2026-10-14",
    "sometime yesterday", "", "2026-10-14T18:05:00",
    "2026-13-01T00:00:00Z", "2026-10-14T25:00:00+00:00",
])
def test_canonical_ts_parity_with_wire(raw):
    """The strict-parse rule must match the wire's, or the two paths disagree
    on what 'malformed' means."""
    assert _canonical_event_ts(raw) == wire_event_ts({"at": raw})


def _patch_cli(monkeypatch, tmp_path, clock, wm):
    monkeypatch.setattr(learn_hook, "LearnClock", lambda *a, **k: clock)
    monkeypatch.setattr(learn_hook, "WATERMARK_PATH", wm)
    monkeypatch.setattr(learn_hook, "META_LOG", tmp_path / "meta.jsonl")


def test_cli_t0_duplicate_end_to_end(tmp_path, monkeypatch, capsys):
    clock, wm = harness(tmp_path)
    at = "2026-10-14T18:05:00+00:00"
    seed(wm, "DIARY", at, "cli lesson", "LC-20261014-007")
    _patch_cli(monkeypatch, tmp_path, clock, wm)
    rc = learn_hook.main(["t0", "--title", "cli lesson", "--evidence", "proof",
                          "--ts", at, "--kind", "DIARY"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "LC-20261014-007" in out and "no duplicate minted" in out
    assert rows_of(tmp_path / "lc.jsonl") == []
    assert not (tmp_path / "meta.jsonl").exists()  # no stage emitted, no meta


def test_cli_t0_malformed_ts_exits_2(tmp_path, monkeypatch):
    clock, wm = harness(tmp_path)
    _patch_cli(monkeypatch, tmp_path, clock, wm)
    with pytest.raises(SystemExit) as e:
        learn_hook.main(["t0", "--title", "x", "--evidence", "proof",
                         "--ts", "whenever"])
    assert e.value.code == 2
    assert rows_of(tmp_path / "lc.jsonl") == []
    assert not wm.exists()


def test_cli_t0_fresh_mints_and_records(tmp_path, monkeypatch, capsys):
    clock, wm = harness(tmp_path)
    _patch_cli(monkeypatch, tmp_path, clock, wm)
    rc = learn_hook.main(["t0", "--title", "fresh cli", "--evidence", "proof",
                          "--ts", "2026-10-14T19:00:00Z"])
    out = capsys.readouterr().out
    assert rc == 0
    rows = rows_of(tmp_path / "lc.jsonl")
    assert len(rows) == 1 and rows[0]["stage_name"] == "T0_EVENT"
    lid = rows[0]["lesson_id"]
    assert f"LESSON_ID={lid}" in out
    meta = [json.loads(l) for l in (tmp_path / "meta.jsonl").read_text().splitlines()]
    assert len(meta) == 1 and meta[0]["lesson_id"] == lid
    wm_data = json.loads(wm.read_text())
    assert any(v == lid for v in wm_data.values())
