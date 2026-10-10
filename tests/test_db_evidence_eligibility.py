"""Tests for kernel/db_evidence_eligibility.py — the DB-path reader/gate.

Every test pins the contract: the held-out evidence markers in
observed_value.held_out_evidence, the self-certification refusals, and the
exact Phase-2 semantics (no markers = no incident on record, never
"unassessed under an incident").
"""

import pytest

from kernel.db_evidence_eligibility import (
    HELD_OUT_EVIDENCE_SCHEMA,
    db_lesson_eligibility_hook,
    db_row_eligibility,
)
from kernel.memory_metabolism import (
    ELIGIBLE,
    INELIGIBLE_NOT_ACTIVE,
    INELIGIBLE_REVOKED,
    INELIGIBLE_SUSPENDED,
    INELIGIBLE_UNCERTAIN,
)


def _row(status="ACTIVE", observed=None, **extra):
    row = {
        "id": "00000000-0000-4000-8000-000000000001",
        "member_id": "00000000-0000-4000-8000-000000000002",
        "target_id": "NAYA-NODE-0001",
        "level": "E1_UNDERSTANDS",
        "provenance": "VERIFICATION",
        "status": status,
        "claim": "synthetic lesson claim",
        "observed_value": observed if observed is not None else {},
        "verification_method": "SYNTH-VERIFY-001",
        "source_event_id": "evt-001",
    }
    row.update(extra)
    return row


def _held(**overrides):
    """A clean held_out_evidence block; overrides replace top-level keys."""
    block = {
        "schema": HELD_OUT_EVIDENCE_SCHEMA,
        "recorded_at": "2026-10-10T19:30:00+00:00",
        "recorded_by": "nayanet-learning-verify",
        "evidence_families": [
            {"family_id": "treatment-arm", "independent_of_lesson": True,
             "basis": "machine measurement against the pre-registered criterion"},
            {"family_id": "verifier-held-out", "independent_of_lesson": True,
             "basis": "different-seat re-measurement on held-out task instances"},
        ],
        "held_out_evaluation": {
            "evaluation_id": "HO-001",
            "evaluator": "naya-2",
            "evaluator_role": "verifier",
            "verdict": "VERIFIED",
            "measured_at": "2026-10-10T19:00:00+00:00",
            "support_arm_ids": ["arm-treatment-001", "arm-control-001"],
            "evaluation_arm_ids": ["arm-heldout-001", "arm-heldout-002"],
            "overlap_with_support": False,
            "held_out_from_support": True,
        },
        "revocation_verdict": "UNAFFECTED",
        "uncertainty_assessment": "independently_cleared",
        "incident_id": None,
    }
    block.update(overrides)
    return block


def _observed_with_held(doer="naya-5", scorer="naya-1", verifier="naya-2", **held_overrides):
    return {
        "doer": doer,
        "scorer": scorer,
        "verifier": verifier,
        "verdict": "VERIFIED",
        "admission_admitted_as": "CANDIDATE",
        "held_out_evidence": _held(**held_overrides),
    }


# --- no markers: "no incident on record" -------------------------------------

def test_active_row_no_markers_eligible():
    assert db_row_eligibility(_row()) == ELIGIBLE


def test_active_row_observed_value_missing_eligible():
    row = _row()
    del row["observed_value"]
    assert db_row_eligibility(row) == ELIGIBLE


def test_active_row_observed_value_none_eligible():
    assert db_row_eligibility(_row(observed=None)) == ELIGIBLE


def test_active_row_observed_without_held_key_eligible():
    assert db_row_eligibility(_row(observed={"doer": "naya-5"})) == ELIGIBLE


# --- status gate ---------------------------------------------------------------

@pytest.mark.parametrize("status", ["CANDIDATE", "NOT_VERIFIED", "RETIRED", "NOT_SUPPORTED", ""])
def test_non_active_status_never_certifies(status):
    assert db_row_eligibility(_row(status=status)) == INELIGIBLE_NOT_ACTIVE


def test_non_dict_row_never_certifies():
    assert db_row_eligibility(None) == INELIGIBLE_NOT_ACTIVE
    assert db_row_eligibility("ACTIVE") == INELIGIBLE_NOT_ACTIVE
    assert db_row_eligibility([]) == INELIGIBLE_NOT_ACTIVE


# --- clean held-out markers ----------------------------------------------------

def test_held_out_markers_clean_eligible():
    row = _row(observed=_observed_with_held())
    assert db_row_eligibility(row) == ELIGIBLE


def test_evaluator_may_equal_verifier():
    # The verifier IS the independent party; doer != scorer != verifier.
    row = _row(observed=_observed_with_held(doer="naya-5", scorer="naya-1", verifier="naya-2"))
    hoe = row["observed_value"]["held_out_evidence"]["held_out_evaluation"]
    hoe["evaluator"] = "NAYA-2"  # case-insensitive match to verifier
    assert db_row_eligibility(row) == ELIGIBLE


# --- self-certification ----------------------------------------------------------

def test_self_certification_held_out_from_support_false_refused():
    hoe = {"held_out_from_support": False}
    row = _row(observed=_observed_with_held())
    row["observed_value"]["held_out_evidence"]["held_out_evaluation"].update(hoe)
    assert db_row_eligibility(row) == INELIGIBLE_UNCERTAIN


def test_self_certification_overlap_with_support_refused():
    row = _row(observed=_observed_with_held())
    row["observed_value"]["held_out_evidence"]["held_out_evaluation"]["overlap_with_support"] = True
    assert db_row_eligibility(row) == INELIGIBLE_UNCERTAIN


def test_self_certification_evaluator_is_doer_refused():
    row = _row(observed=_observed_with_held(doer="naya-5", scorer="naya-1", verifier="naya-2"))
    row["observed_value"]["held_out_evidence"]["held_out_evaluation"]["evaluator"] = "Naya-5 "
    assert db_row_eligibility(row) == INELIGIBLE_UNCERTAIN


def test_self_certification_evaluator_is_scorer_refused():
    row = _row(observed=_observed_with_held(doer="naya-5", scorer="naya-1", verifier="naya-2"))
    row["observed_value"]["held_out_evidence"]["held_out_evaluation"]["evaluator"] = "naya-1"
    assert db_row_eligibility(row) == INELIGIBLE_UNCERTAIN


def test_self_certification_empty_evaluator_refused():
    row = _row(observed=_observed_with_held())
    row["observed_value"]["held_out_evidence"]["held_out_evaluation"]["evaluator"] = "  "
    assert db_row_eligibility(row) == INELIGIBLE_UNCERTAIN


def test_self_certification_missing_evaluator_refused():
    row = _row(observed=_observed_with_held())
    del row["observed_value"]["held_out_evidence"]["held_out_evaluation"]["evaluator"]
    assert db_row_eligibility(row) == INELIGIBLE_UNCERTAIN


def test_malformed_held_out_evaluation_refused():
    row = _row(observed=_observed_with_held())
    row["observed_value"]["held_out_evidence"]["held_out_evaluation"] = ["not", "a", "dict"]
    assert db_row_eligibility(row) == INELIGIBLE_UNCERTAIN


def test_malformed_held_out_block_refused():
    assert db_row_eligibility(_row(observed={"held_out_evidence": "yes"})) == INELIGIBLE_UNCERTAIN
    assert db_row_eligibility(_row(observed={"held_out_evidence": 42})) == INELIGIBLE_UNCERTAIN


def test_absent_held_out_evaluation_not_self_certification():
    # Markers present for revocation/uncertainty but no held-out evaluation
    # recorded: not self-certification, delegate to the vocabulary.
    held = _held()
    del held["held_out_evaluation"]
    assert db_row_eligibility(_row(observed={"held_out_evidence": held})) == ELIGIBLE


# --- revocation vocabulary (Phase 2, verbatim) -----------------------------------

@pytest.mark.parametrize(("verdict", "expected"), [
    ("REVOKED", INELIGIBLE_REVOKED),
    ("revoked", INELIGIBLE_REVOKED),          # case-insensitive, like Phase 2
    ("SUSPENDED", INELIGIBLE_SUSPENDED),
    ("INSUFFICIENT_DATA", INELIGIBLE_UNCERTAIN),
    ("DOWNGRADED", ELIGIBLE),
    ("REQUALIFIED", ELIGIBLE),
    ("UNAFFECTED", ELIGIBLE),
    ("SOMETHING_ELSE", INELIGIBLE_UNCERTAIN),  # unrecognized: fail closed
])
def test_revocation_verdicts_match_phase2(verdict, expected):
    row = _row(observed=_observed_with_held(revocation_verdict=verdict))
    assert db_row_eligibility(row) == expected


# --- uncertainty vocabulary (Phase 2, verbatim) -----------------------------------

@pytest.mark.parametrize(("assessment", "incident", "expected"), [
    ("confirmed_compromised", None, INELIGIBLE_UNCERTAIN),
    ("possibly_compromised", None, INELIGIBLE_UNCERTAIN),
    ("Possibly_Compromised", None, INELIGIBLE_UNCERTAIN),  # case-insensitive
    ("independently_cleared", None, ELIGIBLE),
    ("unassessed", "INC-001", INELIGIBLE_UNCERTAIN),  # live incident, never assessed
    ("unassessed", None, ELIGIBLE),                   # no incident on record
    ("whatever", None, INELIGIBLE_UNCERTAIN),         # unrecognized: fail closed
])
def test_uncertainty_assessments_match_phase2(assessment, incident, expected):
    row = _row(observed=_observed_with_held(
        uncertainty_assessment=assessment, incident_id=incident))
    assert db_row_eligibility(row) == expected


def test_revocation_and_uncertainty_compose():
    # Adverse revocation wins even when uncertainty is cleared.
    row = _row(observed=_observed_with_held(
        revocation_verdict="REVOKED", uncertainty_assessment="independently_cleared"))
    assert db_row_eligibility(row) == INELIGIBLE_REVOKED


# --- the hook ---------------------------------------------------------------------

def test_hook_delegates_to_row():
    rows = {"L1": _row(observed=_observed_with_held())}
    hook = db_lesson_eligibility_hook(rows)
    assert hook("L1") == ELIGIBLE


def test_hook_unknown_lesson_fails_closed():
    hook = db_lesson_eligibility_hook({})
    assert hook("no-such-lesson") == INELIGIBLE_UNCERTAIN


def test_hook_refused_row_propagates_verdict():
    rows = {"L9": _row(observed=_observed_with_held(revocation_verdict="SUSPENDED"))}
    hook = db_lesson_eligibility_hook(rows)
    assert hook("L9") == INELIGIBLE_SUSPENDED
