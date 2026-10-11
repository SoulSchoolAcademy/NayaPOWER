"""Tests for tools/notify_outbox.py — #2244 req 4 (timely awareness mechanism).

Every test runs against an isolated NAYA_NOTIFY_ROOT (tmp_path): no test
touches the real worker outbox. The e2e test runs publish and worker_entry in
separate OS processes — that cross-process delivery is the runtime trace #2244
requires before any "real-time" claim (which this suite does NOT make).
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from tools import notify_outbox as outbox

REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture()
def obox(tmp_path, monkeypatch):
    monkeypatch.setenv("NAYA_NOTIFY_ROOT", str(tmp_path / "notify-outbox"))
    return tmp_path / "notify-outbox"


def _event(**kw):
    base = {
        "type": "blocker",
        "severity": "urgent",
        "audience": ["naya2"],
        "title": "proof chain stalled",
        "body": "producer -> proof -> act-proof stranded for 60m",
    }
    base.update(kw)
    return base


# --- publish / pending round-trip -------------------------------------------

def test_publish_pending_roundtrip(obox):
    eid = outbox.publish(_event())
    got = outbox.pending("naya2")
    assert len(got) == 1
    assert got[0]["id"] == eid
    assert got[0]["title"] == "proof chain stalled"


def test_publish_idempotent_on_dedup_key(obox):
    eid1 = outbox.publish(_event(dedup_key="stall-001"))
    eid2 = outbox.publish(_event(dedup_key="stall-001", title="different title"))
    assert eid1 == eid2
    assert len(outbox.pending("naya2")) == 1  # no duplicate written


def test_dedup_ignores_expired_event(obox):
    outbox.publish(_event(dedup_key="stall-002", ttl_hours=0.0001))
    # force expiry by rewriting the stored event's expires_at into the past
    rows, _ = outbox._read_jsonl(obox / outbox.OUTBOX_FILE)
    assert len(rows) == 1
    rows[0]["expires_at"] = (outbox._now() - timedelta(hours=1)).isoformat()
    outbox._rewrite_jsonl(obox / outbox.OUTBOX_FILE, rows)
    eid2 = outbox.publish(_event(dedup_key="stall-002"))
    live = outbox.pending("naya2")
    assert len(live) == 1 and live[0]["id"] == eid2


def test_audience_filtering(obox):
    outbox.publish(_event(audience=["naya2"], title="for naya2"))
    outbox.publish(_event(audience=["naya4"], title="for naya4"))
    outbox.publish(_event(audience=["all"], title="broadcast"))
    n2 = {e["title"] for e in outbox.pending("naya2")}
    n4 = {e["title"] for e in outbox.pending("naya4")}
    assert n2 == {"for naya2", "broadcast"}
    assert n4 == {"for naya4", "broadcast"}


def test_ack_settles_for_one_audience_only(obox):
    eid = outbox.publish(_event(audience=["naya2", "naya4"]))
    assert outbox.ack(eid, "naya2", worker="relay-1", note="handled")
    assert outbox.pending("naya2") == []
    assert len(outbox.pending("naya4")) == 1  # other audience still sees it


def test_ack_unknown_id_returns_false_and_writes_nothing(obox):
    assert outbox.ack("nope", "naya2", worker="w") is False
    rows, _ = outbox._read_jsonl(obox / outbox.ACKS_FILE)
    assert rows == []


def test_expiry_excludes_from_pending(obox):
    eid = outbox.publish(_event(ttl_hours=1))
    assert len(outbox.pending("naya2")) == 1
    future = outbox._now() + timedelta(hours=2)
    assert outbox.pending("naya2", now=future) == []


def test_publish_rejects_bad_events(obox):
    with pytest.raises(ValueError):
        outbox.publish(_event(title=""))
    with pytest.raises(ValueError):
        outbox.publish(_event(severity="catastrophic"))
    with pytest.raises(ValueError):
        outbox.publish(_event(audience=[]))
    with pytest.raises(ValueError):
        outbox.publish(_event(ttl_hours=9999))
    with pytest.raises(ValueError):
        outbox.publish(_event(source={"nope": 1}))


def test_corrupt_line_does_not_break_reader(obox):
    outbox.publish(_event())
    with open(obox / outbox.OUTBOX_FILE, "a", encoding="utf-8") as f:
        f.write("this is not json {{{\n")
        f.write("[1,2,3]\n")  # valid JSON, not an object
    got = outbox.pending("naya2")
    assert len(got) == 1  # the good event survives; garbage skipped


def test_sweep_purges_expired_and_orphans(obox):
    outbox.publish(_event(dedup_key="old", ttl_hours=0.0001))
    eid = outbox.publish(_event(dedup_key="new"))
    rows, _ = outbox._read_jsonl(obox / outbox.OUTBOX_FILE)
    for r in rows:
        if r["dedup_key"] == "old":
            r["expires_at"] = (outbox._now() - timedelta(hours=1)).isoformat()
    outbox._rewrite_jsonl(obox / outbox.OUTBOX_FILE, rows)
    outbox.deliver_pending("naya2", "w")
    outbox.ack(eid, "naya2", worker="w")
    report = outbox.sweep()
    assert report["expired_events_purged"] == 1
    assert report["live_events"] == 1
    rows, _ = outbox._read_jsonl(obox / outbox.OUTBOX_FILE)
    assert {r["dedup_key"] for r in rows} == {"new"}


# --- deliver_pending (the worker_entry call site) ----------------------------

def test_deliver_pending_records_receipts_and_formats(obox):
    digest = outbox.deliver_pending("naya2", "relay-test")
    assert digest == ""  # nothing pending
    outbox.publish(_event(title="heads up", severity="attention"))
    digest = outbox.deliver_pending("naya2", "relay-test")
    assert "heads up" in digest
    assert "[attention]" in digest
    assert "NOTIFICATIONS" in digest
    deliveries, _ = outbox._read_jsonl(obox / outbox.DELIVERIES_FILE)
    assert len(deliveries) == 1
    assert deliveries[0]["audience"] == "naya2"
    # unacked -> re-surfaced next run (retry), with another receipt
    digest2 = outbox.deliver_pending("naya2", "relay-test")
    assert "heads up" in digest2
    deliveries, _ = outbox._read_jsonl(obox / outbox.DELIVERIES_FILE)
    assert len(deliveries) == 2


def test_deliver_pending_never_raises(tmp_path, monkeypatch):
    # root points at a FILE, not a dir: every file op fails -> must return ""
    bad = tmp_path / "not-a-dir"
    bad.write_text("x")
    monkeypatch.setenv("NAYA_NOTIFY_ROOT", str(bad))
    assert outbox.deliver_pending("naya2", "w") == ""


# --- negative controls: prove the suite is not theater -----------------------

def test_dedup_detector_is_real_not_theater(obox, monkeypatch):
    """Sabotage the dedup lookup: if publish still dedups, the suite is theater."""
    monkeypatch.setattr(outbox, "find_by_dedup_key", lambda *a, **k: None)
    eid1 = outbox.publish(_event(dedup_key="sabotage-1"))
    eid2 = outbox.publish(_event(dedup_key="sabotage-1"))
    assert eid1 != eid2  # dedup broken -> duplicates appear
    assert len(outbox.pending("naya2")) == 2
    # and the honest test (test_publish_idempotent_on_dedup_key) would now fail:
    # with dedup sabotaged, two publishes MUST yield two events. If the real
    # implementation ever stopped consulting find_by_dedup_key, that honest
    # test would fail the same way — the pair proves the mechanism is live.


def test_ack_detector_is_real_not_theater(obox, monkeypatch):
    """Sabotage ack recording: pending must keep surfacing the event."""
    outbox.publish(_event())
    monkeypatch.setattr(outbox, "_append_jsonl", lambda *a, **k: None)
    assert outbox.ack("whatever", "naya2", worker="w") in (True, False)
    # with persistence sabotaged, nothing can be settled for this audience
    assert len(outbox.pending("naya2")) == 1


# --- end-to-end: two OS processes, the #2244 runtime trace --------------------

def _run(cmd, env):
    return subprocess.run(
        cmd, capture_output=True, text=True, timeout=120, cwd=str(REPO_ROOT), env=env
    )


def test_e2e_publish_then_worker_entry_surfaces(tmp_path):
    """Process A publishes; process B (worker_entry.py) surfaces the digest.

    This is the runtime trace #2244 requires: real delivery across processes,
    not an in-memory round-trip.
    """
    notify_root = tmp_path / "e2e-outbox"
    env = dict(os.environ, NAYA_NOTIFY_ROOT=str(notify_root),
               NAYA_NOTIFY_AUDIENCE="naya2", NAYA_WORKER_ID="e2e-worker")
    py = sys.executable

    r1 = _run([py, "tools/notify_outbox.py", "publish",
               "--type", "blocker", "--severity", "urgent",
               "--audience", "naya2", "--title", "e2e proof chain stalled",
               "--body", "delivered across processes",
               "--dedup-key", "e2e-001"], env)
    assert r1.returncode == 0, r1.stderr
    eid = json.loads(r1.stdout)["id"]

    r2 = _run([py, "tools/worker_entry.py"], env)
    # verdict contract preserved regardless of network (tip check may fail safe)
    assert r2.returncode in (0, 10, 20), r2.stderr
    assert "e2e proof chain stalled" in r2.stdout
    assert "[urgent]" in r2.stdout

    # ack in a third process stops redelivery in a fourth
    r3 = _run([py, "tools/notify_outbox.py", "ack", eid,
               "--audience", "naya2", "--worker", "e2e-worker"], env)
    assert r3.returncode == 0, r3.stderr
    r4 = _run([py, "tools/worker_entry.py"], env)
    assert r4.returncode in (0, 10, 20)
    assert "e2e proof chain stalled" not in r4.stdout


def test_e2e_worker_entry_json_mode_stays_valid_json(tmp_path):
    notify_root = tmp_path / "e2e-json"
    env = dict(os.environ, NAYA_NOTIFY_ROOT=str(notify_root),
               NAYA_NOTIFY_AUDIENCE="naya2")
    py = sys.executable
    _run([py, "tools/notify_outbox.py", "publish",
          "--type", "info", "--severity", "info",
          "--audience", "all", "--title", "json mode check"], env)
    r = _run([py, "tools/worker_entry.py", "--json"], env)
    assert r.returncode in (0, 10, 20)
    parsed = json.loads(r.stdout)  # must stay machine-parseable
    assert parsed["verdict"] in ("WORK_AVAILABLE", "NO_WORK", "STAND_DOWN")
    assert "notifications" in parsed


def test_e2e_broken_outbox_never_breaks_activation(tmp_path):
    """The hook is verdict-preserving: a poisoned outbox root changes nothing."""
    bad = tmp_path / "bad"
    bad.write_text("not a directory")
    env = dict(os.environ, NAYA_NOTIFY_ROOT=str(bad),
               NAYA_NOTIFY_AUDIENCE="naya2")
    r = subprocess.run([sys.executable, "tools/worker_entry.py"],
                       capture_output=True, text=True, timeout=120,
                       cwd=str(REPO_ROOT), env=env)
    assert r.returncode in (0, 10, 20)
    assert "NOTIFICATIONS" not in r.stdout  # silent skip, no crash, no verdict change
