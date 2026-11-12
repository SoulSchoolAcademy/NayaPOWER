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


from learning_admission_gate import ADMISSION_SCHEMA
from learning_admission_gate import (
    submit_learning_claim,
)


def admitted_candidate():
    # B8: the queue only accepts gate-admitted candidates, so the fixture
    # must BE one — a minimal dict is refused at the door by design.
    return {
        "schema": ADMISSION_SCHEMA,
        "claim": "Retry-with-backoff reduces failed capture writes.",
        "falsification_condition": "If failure rates are identical over 30 trials, the claim is wrong.",
        "task": "capture-write-retry",
        "success_criterion": "Treatment shows >=20% fewer failed writes than control over 30 trials.",
        "criterion_independent_of_lesson": True,
        "criterion_registered_at": "2026-10-09T09:00:00Z",
        "measurement": {"method": "machine"},
        "doer": "naya-5",
        "scorer": "naya-2",
        "arms": {
            "treatment": {"observable": "retries writes", "measured_at": "2026-10-09T10:00:00Z"},
            "control": {"observable": "no retry", "measured_at": "2026-10-09T10:05:00Z"},
        },
        "asserts_behavioral_change": True,
        "behavioral_measure": "failed-write count",
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


# ---------------------------------------------------------------------------
# Round 2 — B8: the gate FIRES on every queue write (SN-0435: a script nobody
# calls is not enforcement). B6b: identity normalized on claim.
# ---------------------------------------------------------------------------

def test_b8_enqueue_refuses_rejected_candidate():
    bad = dict(admitted_candidate())
    bad["task"] = ""  # gate rejects: NO_NAMED_TASK
    with pytest.raises(ValueError) as exc:
        enqueue(bad, "cand-bad", clock=clock_at(T0))
    assert "ADMISSION_REJECTED" in str(exc.value)
    assert "NO_NAMED_TASK" in str(exc.value)


def test_b8_enqueue_refuses_tautological_candidate():
    bad = dict(admitted_candidate())
    bad["claim"] = "Applying the lesson changes behavior."
    bad["falsification_condition"] = "if applying the lesson did not change behavior"
    with pytest.raises(ValueError) as exc:
        enqueue(bad, "cand-taut", clock=clock_at(T0))
    assert "TAUTOLOGICAL_FALSIFICATION" in str(exc.value)


def test_b8_enqueue_refuses_honest_null():
    # Honest nulls are kept as negative evidence — never queued for
    # verification. There is no path into the queue around the gate.
    null = dict(admitted_candidate())
    null["outcome"] = "null"
    assert submit_learning_claim(null).admitted_as == "NOT_VERIFIED"
    with pytest.raises(ValueError) as exc:
        enqueue(null, "cand-null", clock=clock_at(T0))
    assert "NOT_A_VERIFICATION_CANDIDATE" in str(exc.value)


def test_b8_gate_call_precedes_entry_construction():
    # Source-text proof (repo's edge-function test style): the deployed seam
    # is importable Python, so assert the call ORDER in source — the gate
    # must run before any QueueEntry is constructed.
    from pathlib import Path
    src = (Path(__file__).resolve().parents[1] / "tools" / "learning_verification_queue.py").read_text()
    fn_start = src.index("def enqueue(")
    gate_pos = src.index("submit_learning_claim(", fn_start)
    entry_pos = src.index("QueueEntry(", fn_start)
    assert gate_pos < entry_pos, "the gate must fire before queue entry construction"
    assert "ADMISSION_REJECTED" in src


def test_b6b_claim_rejects_case_variant_of_doer():
    e = enqueue(admitted_candidate(), "cand-001", clock=clock_at(T0))
    with pytest.raises(ValueError):
        claim(e, "NAYA-5", clock=clock_at(T0))  # case variant of doer naya-5
    with pytest.raises(ValueError):
        claim(e, " naya-2 ", clock=clock_at(T0))  # whitespace variant of scorer
    e2 = claim(e, "naya-3", clock=clock_at(T0))
    assert e2.verifier == "naya-3"
