"""Fail-closed resource admission checks for existing Parallel Execution Law."""
from datetime import datetime, timezone
import json
import subprocess
import sys
from pathlib import Path

from tools.resource_capacity_admission import (
    assess_capacity, classify_brainbase_failure_event,
)

NOW = datetime(2026, 10, 8, 4, 1, tzinfo=timezone.utc)
SNAP = {
    "provider": "brainbase",
    "evidence_ref": "brainbase:task/representative/events",
    "observed_at": "2026-10-08T04:00:49Z",
    "measured": True, "unit": "credits",
    "allocated": 12, "used": 2,
}
REQ = {
    "unit": "credits", "per_task_cost": 2,
    "cost_measured": True, "ready_tasks": 8,
}


def check(snap=None, req=None):
    return assess_capacity(
        SNAP if snap is None else snap,
        REQ if req is None else req, now=NOW,
    )


def test_capacity_ready_is_not_authority_or_execution():
    result = check()
    assert result["decision"] == "CAPACITY_READY"
    assert result["max_ready_tasks"] == 5
    assert result["dispatch_performed"] is False
    assert result["law_authorized"] is False


def test_provider_402_blocks_retries():
    candidate = {**SNAP, "allocated": 0, "used": 0,
                 "error_code": "CREDITS_EXHAUSTED"}
    assert check(candidate)["decision"] == "BLOCKED_RESOURCE"
    assert check(candidate)["max_ready_tasks"] == 0


def test_not_enough_capacity_blocks():
    assert check({**SNAP, "allocated": 3, "used": 2})["decision"] == "BLOCKED_RESOURCE"


def test_unmeasured_unknown_fail_closed():
    for candidate in ({**SNAP, "measured": False},
                      {**SNAP, "error_code": "UNKNOWN"}):
        assert check(candidate)["decision"] == "BLOCKED_EVIDENCE"


def test_stale_future_fail_closed():
    for instant in ("2026-10-08T03:50:00Z", "2026-10-08T04:05:00Z"):
        assert check({**SNAP, "observed_at": instant})["decision"] == "BLOCKED_EVIDENCE"


def test_naive_malformed_dates_fail_closed():
    for instant in ("2026-10-08T04:00:49", "nonsense", ""):
        assert check({**SNAP, "observed_at": instant})["decision"] == "BLOCKED_EVIDENCE"


def test_missing_provider_or_ref_fails():
    for candidate in ({**SNAP, "provider": ""},
                      {**SNAP, "evidence_ref": ""}):
        assert check(candidate)["decision"] == "BLOCKED_EVIDENCE"


def test_bad_counters_fail_closed():
    for alloc, used in ((float("nan"), 0), (float("inf"), 0),
                        (True, 0), (-1, 0), (1, 2)):
        assert check({**SNAP, "allocated": alloc, "used": used})["decision"] == "BLOCKED_EVIDENCE"


def test_cost_unmeasured_and_unit_mismatch_fail_closed():
    assert check(req={**REQ, "cost_measured": False})["decision"] == "BLOCKED_EVIDENCE"
    assert check(req={**REQ, "unit": "tokens"})["decision"] == "BLOCKED_EVIDENCE"


def test_bad_costs_fail_closed():
    for cost in (-2, 0, True, float("nan"), float("inf")):
        assert check(req={**REQ, "per_task_cost": cost})["decision"] == "BLOCKED_EVIDENCE"


def test_bad_ready_counts_fail_closed():
    for count in (-1, 0, 1.5, True):
        assert check(req={**REQ, "ready_tasks": count})["decision"] == "BLOCKED_EVIDENCE"


def test_normalizes_actual_brainbase_event_shape():
    event = {"type": "idle", "details": json.dumps({
        "entitlement_error": {
            "allocated": 0, "error": "CREDITS_EXHAUSTED", "used": 0,
        }, "http_status": 402,
    })}
    candidate = classify_brainbase_failure_event(
        event, observed_at=SNAP["observed_at"],
        evidence_ref=SNAP["evidence_ref"],
    )
    result = check(candidate)
    assert result["decision"] == "BLOCKED_RESOURCE"
    assert result["evidence_refs"] == [SNAP["evidence_ref"]]


def test_malformed_events_cannot_claim_measured_capacity():
    for event in (None, {}, {"type": "idle", "details": "wrong"},
                  {"type": "assistant.message", "details": '{"http_status":402}'},
                  {"type": "idle", "details": '{"http_status":402}'}):
        candidate = classify_brainbase_failure_event(
            event, observed_at=SNAP["observed_at"],
            evidence_ref=SNAP["evidence_ref"],
        )
        assert check(candidate)["decision"] == "BLOCKED_EVIDENCE"


def test_nonobjects_fail_without_exception():
    assert assess_capacity(None, REQ, now=NOW)["decision"] == "BLOCKED_EVIDENCE"
    assert assess_capacity(SNAP, None, now=NOW)["decision"] == "BLOCKED_EVIDENCE"


def test_cli_exits_failure_for_zero_credits(tmp_path):
    snap = tmp_path / "snapshot.json"
    request = tmp_path / "request.json"
    snap.write_text(json.dumps({
        **SNAP, "allocated": 0, "used": 0,
        "error_code": "CREDITS_EXHAUSTED",
    }), encoding="utf-8")
    request.write_text(json.dumps(REQ), encoding="utf-8")
    script = Path(__file__).resolve().parents[1] / "tools" / "resource_capacity_admission.py"
    result = subprocess.run([
        sys.executable, str(script), "--snapshot", str(snap),
        "--request", str(request), "--now", "2026-10-08T04:01:00Z",
    ], capture_output=True, text=True)
    assert result.returncode == 1
    assert json.loads(result.stdout)["decision"] == "BLOCKED_RESOURCE"
