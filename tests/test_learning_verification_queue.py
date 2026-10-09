"""Tests for the learning verification queue: worked, not watched."""

import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from learning_verification_queue import (
    SLA_HOURS,
    STATUS_CLAIMED,
    STATUS_NOT_VERIFIED,
    STATUS_QUEUED,
    STATUS_RETIRED,
    STATUS_VERIFIED,
    claim,
    enqueue,
    load_queue,
    record_verdict,
    save_queue,
    sweep_overdue,
)

T0 = datetime(2026, 10, 9, 12, 0, tzinfo=timezone.utc)


def clock_at(t):
    return lambda: t


def admitted_candidate():
    return {
        "claim": "Retry-with-backoff reduces failed capture writes.",
        "task": "capture-write-retry",
        "doer": "naya-5",
        "scorer": "naya-2",
    }


def test_enqueue_sets_48h_sla():
    e = enqueue(admitted_candidate(), "cand-001", clock=clock_at(T0))
    assert e.status == STATUS_QUEUED
    assert e.verify_by == (T0 + timedelta(hours=SLA_HOURS)).isoformat()
    assert SLA_HOURS == 48


def test_claim_requires_independent_verifier():
    e = enqueue(admitted_candidate(), "cand-001", clock=clock_at(T0))
    with pytest.raises(ValueError):
        claim(e, "naya-5", clock=clock_at(T0))  # the doer
    with pytest.raises(ValueError):
        claim(e, "naya-2", clock=clock_at(T0))  # the scorer
    e2 = claim(e, "naya-3", clock=clock_at(T0))
    assert e2.status == STATUS_CLAIMED and e2.verifier == "naya-3"


def test_verdict_requires_claim_and_reason():
    e = enqueue(admitted_candidate(), "cand-001", clock=clock_at(T0))
    with pytest.raises(ValueError):
        record_verdict(e, STATUS_VERIFIED, "x", clock=clock_at(T0))  # not claimed
    e2 = claim(e, "naya-3", clock=clock_at(T0))
    with pytest.raises(ValueError):
        record_verdict(e2, STATUS_VERIFIED, "  ", clock=clock_at(T0))  # no reason
    e3 = record_verdict(e2, STATUS_VERIFIED, "30/30 trials, machine-measured", clock=clock_at(T0))
    assert e3.status == STATUS_VERIFIED and e3.decided_at != ""


def test_honest_null_verdict_kept():
    e = claim(enqueue(admitted_candidate(), "c", clock=clock_at(T0)), "naya-3", clock=clock_at(T0))
    e2 = record_verdict(e, STATUS_NOT_VERIFIED, "no effect observed, kept as negative evidence", clock=clock_at(T0))
    assert e2.status == STATUS_NOT_VERIFIED


def test_overdue_entries_retired_not_left_to_rot():
    e = enqueue(admitted_candidate(), "cand-old", clock=clock_at(T0))
    kept, retired = sweep_overdue([e], clock=clock_at(T0 + timedelta(hours=49)))
    assert kept == [] and len(retired) == 1
    assert retired[0].status == STATUS_RETIRED
    assert "SLA_EXPIRED" in retired[0].verdict_reason


def test_fresh_entries_survive_sweep():
    e = enqueue(admitted_candidate(), "cand-new", clock=clock_at(T0))
    kept, retired = sweep_overdue([e], clock=clock_at(T0 + timedelta(hours=47)))
    assert len(kept) == 1 and retired == []


def test_decided_entries_untouched_by_sweep():
    e = claim(enqueue(admitted_candidate(), "c", clock=clock_at(T0)), "naya-3", clock=clock_at(T0))
    e2 = record_verdict(e, STATUS_VERIFIED, "proof", clock=clock_at(T0))
    kept, retired = sweep_overdue([e2], clock=clock_at(T0 + timedelta(hours=500)))
    assert kept == [e2] and retired == []


def test_queue_round_trips_through_json(tmp_path):
    e = enqueue(admitted_candidate(), "cand-001", clock=clock_at(T0))
    p = tmp_path / "queue.json"
    save_queue([e], p)
    loaded = load_queue(p)
    assert loaded == [e]


def test_missing_queue_file_loads_empty(tmp_path):
    assert load_queue(tmp_path / "nope.json") == []
