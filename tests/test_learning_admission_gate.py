"""Tests for the learning-candidate admission gate (machine law).

Fixtures are modeled on the 13 real failed candidates analyzed 2026-10-09
(1 definitional tautology, 4 honest nulls, 5 non-experiments, 3 definitional
token changes) plus the 23 chain-test artifacts swept into learning_evidence
as CANDIDATEs on 2026-10-09. Every one of those must be rejected at the door
— or, for honest nulls, admitted as NOT VERIFIED, never as CANDIDATE.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from learning_admission_gate import (
    ADMISSION_SCHEMA,
    CANDIDATE,
    NOT_VERIFIED,
    REJECTED,
    admit_candidate,
    rejection_log,
)


def valid_candidate(**overrides):
    base = {
        "schema": ADMISSION_SCHEMA,
        "claim": "Applying the retry-with-backoff lesson reduces failed capture writes on flaky networks.",
        "falsification_condition": "If treatment and control show identical failure rates over 30 flaky-network trials, the claim is wrong.",
        "task": "capture-write-retry",
        "lesson_id": "SN-0000",
        "success_criterion": "Treatment arm shows >=20% fewer failed writes than control over 30 trials.",
        "criterion_independent_of_lesson": True,
        "doer": "naya-5",
        "scorer": "naya-2",
        "measurement": {"method": "machine", "detail": "write-failure counter in trial harness"},
        "arms": {
            "treatment": {"observable": "retries each failed write up to 3x with backoff", "measured_at": "2026-10-09T10:00:00Z"},
            "control": {"observable": "fails the write immediately, no retry", "measured_at": "2026-10-09T10:05:00Z"},
        },
        "asserts_behavioral_change": True,
        "behavioral_measure": "failed-write count per 30-trial run",
        "outcome": "pending",
    }
    base.update(overrides)
    return base


def test_valid_candidate_admitted():
    r = admit_candidate(valid_candidate())
    assert r.admitted and r.admitted_as == CANDIDATE and r.reasons == ()


def test_schema_mismatch_rejected():
    r = admit_candidate(valid_candidate(schema="WRONG"))
    assert not r.admitted and r.admitted_as == REJECTED
    assert "SCHEMA_MISMATCH" in r.reasons


def test_missing_falsification_condition_rejected():
    # The 2026-10-09 finding: "treatment says applied the lesson" with no
    # falsifiable criterion is a tautology, not an experiment.
    r = admit_candidate(valid_candidate(falsification_condition=""))
    assert not r.admitted
    assert "CLAIM_NOT_FALSIFIABLE" in r.reasons


def test_no_named_task_rejected():
    r = admit_candidate(valid_candidate(task=""))
    assert not r.admitted
    assert "NO_NAMED_TASK" in r.reasons


def test_criterion_not_independent_rejected():
    r = admit_candidate(valid_candidate(criterion_independent_of_lesson=False))
    assert not r.admitted
    assert "CRITERION_NOT_INDEPENDENT" in r.reasons


def test_no_criterion_rejected():
    r = admit_candidate(valid_candidate(success_criterion=""))
    assert not r.admitted
    assert "NO_PREREGISTERED_CRITERION" in r.reasons


def test_heuristic_measurement_rejected():
    r = admit_candidate(valid_candidate(measurement={"method": "vibes", "detail": "felt right"}))
    assert not r.admitted
    assert "NO_MACHINE_MEASUREMENT" in r.reasons


@pytest.mark.parametrize("method", ["machine", "different_seat", "deterministic"])
def test_all_measurement_methods_admitted(method):
    r = admit_candidate(valid_candidate(measurement={"method": method}))
    assert r.admitted_as == CANDIDATE


def test_doer_equals_scorer_rejected():
    r = admit_candidate(valid_candidate(doer="naya-5", scorer="naya-5"))
    assert not r.admitted
    assert "DOER_EQUALS_SCORER" in r.reasons


def test_tautological_arms_rejected():
    # Real failure mode 2026-10-09: treatment "applied the lesson",
    # control "did not" — no observable behavioral difference specified.
    r = admit_candidate(valid_candidate(arms={
        "treatment": {"observable": "", "measured_at": "2026-10-09T10:00:00Z"},
        "control": {"observable": "", "measured_at": "2026-10-09T10:05:00Z"},
    }))
    assert not r.admitted
    assert "ARMS_REQUIRE_OBSERVABLE_BEHAVIOR" in r.reasons


def test_indistinguishable_arms_rejected():
    r = admit_candidate(valid_candidate(arms={
        "treatment": {"observable": "does the thing", "measured_at": "2026-10-09T10:00:00Z"},
        "control": {"observable": "does the thing", "measured_at": "2026-10-09T10:05:00Z"},
    }))
    assert not r.admitted
    assert "ARMS_INDIMINISHABLE" in r.reasons


def test_non_experiment_unmeasured_arms_rejected():
    # Real failure mode 2026-10-09: 5 of 13 "never tested anything".
    r = admit_candidate(valid_candidate(arms={
        "treatment": {"observable": "retries writes", "measured_at": ""},
        "control": {"observable": "no retry", "measured_at": ""},
    }))
    assert not r.admitted
    assert "NON_EXPERIMENT_NO_MEASURED_ARMS" in r.reasons


def test_token_difference_rejected():
    # Real failure mode 2026-10-09: 3 definitional token changes —
    # both arms returned REQUIRE_DIRECT_CANONICAL_INTELLIGENCE.
    r = admit_candidate(valid_candidate(asserts_behavioral_change=False))
    assert not r.admitted
    assert "TOKEN_DIFFERENCE_NOT_BEHAVIOR" in r.reasons


def test_honest_null_admitted_as_not_verified():
    # Real finding 2026-10-09: 4 honest nulls. Kept as negative evidence,
    # NEVER as candidates.
    r = admit_candidate(valid_candidate(outcome="null"))
    assert r.admitted and r.admitted_as == NOT_VERIFIED


def test_chain_test_artifact_rejected():
    # Real failure mode 2026-10-09: 23 chain-test utterances ("Almost there",
    # "Should work now") swept into learning_evidence as CANDIDATEs.
    r = admit_candidate({
        "schema": ADMISSION_SCHEMA,
        "claim": "Almost there",
        "provenance": "USER",
        "verification_method": "PENDING_OUTCOME_VERIFICATION",
    })
    assert not r.admitted and r.admitted_as == REJECTED
    assert "CLAIM_NOT_FALSIFIABLE" in r.reasons
    assert "NO_NAMED_TASK" in r.reasons


def test_non_object_rejected():
    r = admit_candidate("just a string")
    assert not r.admitted
    assert "CANDIDATE_MUST_BE_OBJECT" in r.reasons


def test_rejection_log_names_reasons():
    r = admit_candidate(valid_candidate(task=""))
    log = rejection_log("abc123", r)
    assert "abc123" in log and "NO_NAMED_TASK" in log
