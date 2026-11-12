"""Regression guard: the LIVE receipt verifiers must still BITE.

Coder 2, 2026-09-28.

WHY THIS FILE EXISTS
--------------------
`test_causal_learning_experiment_contract` and `test_independent_learning_influence`
now SKIP when their live receipts are absent. A skip is only honest if the
assertion logic behind it is still real and still capable of failing.

Without this guard, someone could later gut either verifier and the suite would
stay green, because the test would simply keep skipping. That is precisely the
"manufacture green" failure mode this project forbids.

So: every contract assertion is re-tested here against a synthetic receipt that
VIOLATES it. If any degraded receipt is accepted, this file fails.

These are pure in-process checks. They require no credentials, no runtime, and
no database, and they assert NOTHING about live behaviour. They establish only
that the verifier logic has not been hollowed out.
"""

import copy

import pytest

from test_causal_learning_experiment_contract import verify_causal_learning_experiment_receipt
from test_independent_learning_influence import verify_learning_influence_receipt


def _causal() -> dict:
    return {
        "schema": "NAYANET_CAUSAL_LEARNING_EXPERIMENT_V1",
        "target_id": "NAYA-NODE-0001",
        "learning_id": "de0b794b-224b-4d8b-ad1a-3afc6f8d0771",
        "control": {"retained_intelligence_used": False, "behavior": "REQUIRE_DIRECT_CANONICAL_INTELLIGENCE"},
        "treatment": {"retained_intelligence_used": True, "behavior": "PRESERVE_PROVENANCE_BEFORE_APPLY"},
        "causal_verification": {"causal_assessment": "CAUSAL_SUPPORTED", "verification_status": "OUTCOME_VERIFIED"},
        "independent_verification": True,
    }


def _influence() -> dict:
    return {
        "schema": "NAYANET_LEARNING_INFLUENCE_RUNTIME_V1",
        "status": "PASS",
        "target_id": "NAYA-NODE-0001",
        "learning_level": "E5_CAN_TEACH",
        "source_event_id": "NAYA-NODE-0001-APPLY",
        "behavioral_change": True,
        "control_verified_value": 3,
        "treatment_verified_value": 9,
        "fresh_session_decision": "USE_VERIFIED_LEARNING_CONTEXT",
        "influenced": True,
        "learning_id": "de0b794b-224b-4d8b-ad1a-3afc6f8d0771",
        "evidence_id_from_decision": "de0b794b-224b-4d8b-ad1a-3afc6f8d0771",
    }


# ---- positive controls: conforming receipts MUST be accepted -----------------

def test_conforming_causal_receipt_is_accepted():
    verify_causal_learning_experiment_receipt(_causal())


def test_conforming_influence_receipt_is_accepted():
    verify_learning_influence_receipt(_influence())


# ---- negative controls: the verifier must REJECT each violation --------------

def test_rejects_control_that_received_the_retained_lesson():
    """The single most important causal property: the control must be clean."""
    r = copy.deepcopy(_causal())
    r["control"]["retained_intelligence_used"] = True
    with pytest.raises(AssertionError):
        verify_causal_learning_experiment_receipt(r)


def test_rejects_treatment_that_did_not_receive_the_retained_lesson():
    r = copy.deepcopy(_causal())
    r["treatment"]["retained_intelligence_used"] = False
    with pytest.raises(AssertionError):
        verify_causal_learning_experiment_receipt(r)


def test_rejects_identical_control_and_treatment_behavior():
    """No observable behavioural delta means no causal claim is warranted."""
    r = copy.deepcopy(_causal())
    r["treatment"]["behavior"] = r["control"]["behavior"]
    with pytest.raises(AssertionError):
        verify_causal_learning_experiment_receipt(r)


def test_rejects_causal_assessment_other_than_causal_supported():
    r = copy.deepcopy(_causal())
    r["causal_verification"]["causal_assessment"] = "UNSUPPORTED"
    with pytest.raises(AssertionError):
        verify_causal_learning_experiment_receipt(r)


def test_rejects_unverified_outcome_status():
    r = copy.deepcopy(_causal())
    r["causal_verification"]["verification_status"] = "PENDING"
    with pytest.raises(AssertionError):
        verify_causal_learning_experiment_receipt(r)


def test_rejects_self_certified_receipt_without_independent_verification():
    """An executor asserting its own correctness is not independent verification."""
    r = copy.deepcopy(_causal())
    r["independent_verification"] = False
    with pytest.raises(AssertionError):
        verify_causal_learning_experiment_receipt(r)


def test_rejects_wrong_schema():
    r = copy.deepcopy(_causal())
    r["schema"] = "SOMETHING_ELSE"
    with pytest.raises(AssertionError):
        verify_causal_learning_experiment_receipt(r)


# ---- learning-influence negatives -------------------------------------------

def test_rejects_influence_where_treatment_did_not_beat_control():
    """A stored lesson that changed nothing is not learning."""
    r = copy.deepcopy(_influence())
    r["treatment_verified_value"] = r["control_verified_value"]
    with pytest.raises(AssertionError):
        verify_learning_influence_receipt(r)


def test_rejects_influence_where_treatment_is_worse_than_control():
    r = copy.deepcopy(_influence())
    r["treatment_verified_value"] = 1
    with pytest.raises(AssertionError):
        verify_learning_influence_receipt(r)


def test_rejects_absent_behavioral_change():
    r = copy.deepcopy(_influence())
    r["behavioral_change"] = False
    with pytest.raises(AssertionError):
        verify_learning_influence_receipt(r)


def test_rejects_uninfluenced_outcome():
    r = copy.deepcopy(_influence())
    r["influenced"] = False
    with pytest.raises(AssertionError):
        verify_learning_influence_receipt(r)


def test_rejects_broken_learning_lineage():
    """The decision must cite the same learning id that was retained."""
    r = copy.deepcopy(_influence())
    r["evidence_id_from_decision"] = "a-different-learning-id"
    with pytest.raises(AssertionError):
        verify_learning_influence_receipt(r)


def test_rejects_decision_that_ignores_verified_context():
    r = copy.deepcopy(_influence())
    r["fresh_session_decision"] = "IGNORE_LEARNING"
    with pytest.raises(AssertionError):
        verify_learning_influence_receipt(r)


def test_rejects_non_passing_status():
    r = copy.deepcopy(_influence())
    r["status"] = "FAIL"
    with pytest.raises(AssertionError):
        verify_learning_influence_receipt(r)
