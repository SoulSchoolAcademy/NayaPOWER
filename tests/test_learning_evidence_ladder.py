"""Behavioral tests for the E0-E7 evidence ladder evaluator (convergence item C).

These tests exercise the actual seam the evaluator guards: the boundary
between a CLAIMED level and the EARNED level the observable evidence
supports. SN-0546: a level is a transition, or it is not a level.
"""

import pytest

from tools.learning_evidence_ladder import (
    LEVEL_ORDER,
    SCHEMA,
    _TRANSITIONS,
    evaluate,
    load_ladder,
)


def _ev(**over):
    base = {
        "capture_receipt": {
            "intelligent_block_id": "IB-TEST-1",
            "captured_at": "2026-10-08T00:00:00Z",
        }
    }
    base.update(over)
    return base


def _record(evidence, claimed_level="E1_UNDERSTANDS", **over):
    rec = {"id": "L1", "target": "NAYA-NODE-0001", "producer_id": "naya-5",
           "claimed_level": claimed_level, "evidence": evidence}
    rec.update(over)
    return rec


def _e1_evidence(verifier="naya-1"):
    return _ev(comprehension={
        "control_receipt": "cr-1", "treatment_receipt": "tr-1",
        "independent_verifier": verifier, "verified_at": "2026-10-08T01:00:00Z",
    })


def _full_chain_through_e5():
    return _ev(
        comprehension={
            "control_receipt": "cr-1", "treatment_receipt": "tr-1",
            "independent_verifier": "naya-1", "verified_at": "2026-10-08T01:00:00Z",
        },
        application_receipt={
            "retrieval_ref": "ret-1", "task_ref": "task-A",
            "applied_at": "2026-10-08T02:00:00Z", "applier": "naya-5",
        },
        outcome={
            "measured_effect": "+12% accuracy",
            "independent_verification": {"verifier": "naya-2", "verified_at": "2026-10-08T03:00:00Z"},
        },
        transfer=[{
            "task_ref": "task-B", "domain": "retrieval",
            "measured_effect": "+8% accuracy",
            "independent_verification": {"verifier": "naya-2", "verified_at": "2026-10-08T04:00:00Z"},
        }],
        successor_use=[{
            "successor_id": "naya-6", "task_ref": "task-C",
            "independent_verification": {"verifier": "naya-1", "verified_at": "2026-10-08T05:00:00Z"},
        }],
    )


# ---------------------------------------------------------------- law sync

def test_ladder_json_and_code_stay_in_sync():
    ladder = load_ladder()
    json_ids = [lvl["id"] for lvl in ladder["levels"]]
    assert json_ids == list(LEVEL_ORDER), "ladder JSON drifted from evaluator order"
    assert set(_TRANSITIONS) == set(LEVEL_ORDER), "transition predicates drifted from level order"
    assert ladder["schema"] == "NAYANET_LEARNING_EVIDENCE_LADDER_V1"
    for lvl in ladder["levels"]:
        assert lvl["required_evidence"], f"{lvl['id']} declares no required evidence"


def test_output_schema_and_no_authority_fields():
    result = evaluate(_record(_e1_evidence()))
    assert result["schema"] == SCHEMA
    blob = str(result)
    for forbidden in ("authorized", "grant", "self_authorized"):
        assert forbidden not in blob.lower(), "evaluation must never carry authority fields"


# ---------------------------------------------------------------- core seam

def test_e1_evidence_claiming_e4_is_rejected_naming_e2():
    result = evaluate(_record(_e1_evidence(), claimed_level="E4_TRANSFER"))
    assert result["earned_level"] == "E1_UNDERSTANDS"
    assert result["verdict"] == "REJECTED"
    assert result["verdict_code"] == "LEVEL_NOT_EARNED"
    assert result["honest_label"] == "candidate learning, E1-proven"
    assert any("E2_CAN_DO unproven" in u for u in result["unproven"])


def test_honest_claim_matching_evidence_is_accepted():
    result = evaluate(_record(_e1_evidence(), claimed_level="E1_UNDERSTANDS"))
    assert result["verdict"] == "ACCEPTED"
    assert result["verdict_code"] == "CLAIM_MATCHES_EVIDENCE"


def test_claim_below_evidence_is_underclaimed_not_rejected():
    result = evaluate(_record(_full_chain_through_e5(), claimed_level="E2_CAN_DO"))
    assert result["earned_level"] == "E5_CAN_TEACH"
    assert result["verdict"] == "UNDERCLAIMED"
    assert result["verdict_code"] == "EVIDENCE_EXCEEDS_CLAIM"


def test_no_capture_evidence_is_unproven_not_e0():
    result = evaluate(_record({}, claimed_level="E1_UNDERSTANDS"))
    assert result["earned_level"] == "UNPROVEN"
    assert result["verdict"] == "UNPROVEN"
    assert result["honest_label"] == "unproven — no capture evidence"


def test_unknown_claimed_level_is_rejected():
    result = evaluate(_record(_e1_evidence(), claimed_level="E9_GODMODE"))
    assert result["verdict"] == "REJECTED"
    assert result["verdict_code"] == "UNKNOWN_CLAIMED_LEVEL"


# ---------------------------------------------------------------- falsifiers

def test_conflicting_evidence_falsifies_above_e0():
    ev = _full_chain_through_e5()
    ev["conflicts"] = [{"with": "L2", "about": "opposite outcome on task-B"}]
    result = evaluate(_record(ev, claimed_level="E5_CAN_TEACH"))
    assert result["verdict"] == "FALSIFIED"
    assert result["verdict_code"] == "EVIDENCE_CONFLICT"
    assert result["earned_level"] == "E0_EXPOSED"


def test_self_attestation_at_e1_is_unproven():
    ev = _e1_evidence(verifier="naya-5")  # verifier == producer
    result = evaluate(_record(ev, claimed_level="E1_UNDERSTANDS", producer_id="naya-5"))
    assert result["earned_level"] == "E0_EXPOSED"
    assert result["verdict"] == "REJECTED"


def test_executor_owned_outcome_observation_fails_e3():
    ev = _e1_evidence()
    ev["application_receipt"] = {
        "retrieval_ref": "ret-1", "task_ref": "task-A",
        "applied_at": "2026-10-08T02:00:00Z", "applier": "naya-5",
    }
    ev["outcome"] = {
        "measured_effect": "+12%",
        "independent_verification": {"verifier": "naya-5", "verified_at": "2026-10-08T03:00:00Z"},
    }
    result = evaluate(_record(ev, claimed_level="E3_INDEPENDENT"))
    assert result["earned_level"] == "E2_CAN_DO"
    assert result["verdict"] == "REJECTED"
    assert any("E3_INDEPENDENT unproven" in u for u in result["unproven"])


def test_same_task_repetition_is_not_transfer():
    ev = _e1_evidence()
    ev["application_receipt"] = {
        "retrieval_ref": "ret-1", "task_ref": "task-A",
        "applied_at": "2026-10-08T02:00:00Z", "applier": "naya-5",
    }
    ev["outcome"] = {
        "measured_effect": "+12%",
        "independent_verification": {"verifier": "naya-2", "verified_at": "2026-10-08T03:00:00Z"},
    }
    ev["transfer"] = [{
        "task_ref": "task-A",  # same task relabeled — anti-memorization
        "measured_effect": "+12%",
        "independent_verification": {"verifier": "naya-2", "verified_at": "2026-10-08T04:00:00Z"},
    }]
    result = evaluate(_record(ev, claimed_level="E4_TRANSFER"))
    assert result["earned_level"] == "E3_INDEPENDENT"
    assert result["verdict"] == "REJECTED"


def test_warm_successor_is_not_e5():
    ev = _full_chain_through_e5()
    ev["successor_use"] = [{
        "successor_id": "naya-5",  # same identity as producer/applier — not cold
        "task_ref": "task-C",
        "independent_verification": {"verifier": "naya-1", "verified_at": "2026-10-08T05:00:00Z"},
    }]
    result = evaluate(_record(ev, claimed_level="E5_CAN_TEACH"))
    assert result["earned_level"] == "E4_TRANSFER"
    assert result["verdict"] == "REJECTED"


def test_stale_evidence_caps_at_e1():
    ev = _full_chain_through_e5()
    ev["stale"] = True
    result = evaluate(_record(ev, claimed_level="E5_CAN_TEACH"))
    assert result["earned_level"] == "E1_UNDERSTANDS"
    assert result["verdict"] == "REJECTED"


# ---------------------------------------------------------------- higher rungs

def test_cold_successor_chain_earns_e5():
    result = evaluate(_record(_full_chain_through_e5(), claimed_level="E5_CAN_TEACH"))
    assert result["earned_level"] == "E5_CAN_TEACH"
    assert result["verdict"] == "ACCEPTED"
    assert result["honest_label"] == "E5-proven: taught to a cold successor"


def test_e6_requires_revalidation_receipt():
    ev = _full_chain_through_e5()
    result = evaluate(_record(ev, claimed_level="E6_RETAINED"))
    assert result["earned_level"] == "E5_CAN_TEACH"
    assert result["verdict"] == "REJECTED"
    ev["retention"] = {
        "revalidated_at": "2026-10-08T06:00:00Z",
        "revalidation_receipt": "rr-1",
    }
    result = evaluate(_record(ev, claimed_level="E6_RETAINED"))
    assert result["earned_level"] == "E6_RETAINED"
    assert result["verdict"] == "ACCEPTED"


def test_e7_requires_compound_mastery_evidence():
    ev = _full_chain_through_e5()
    ev["retention"] = {
        "revalidated_at": "2026-10-08T06:00:00Z",
        "revalidation_receipt": "rr-1",
    }
    result = evaluate(_record(ev, claimed_level="E7_MASTERED"))
    assert result["earned_level"] == "E6_RETAINED", "E7 must not be reachable on chain alone"
    assert result["verdict"] == "REJECTED"
    ev["mastery"] = {"distinct_verifiers": 2, "distinct_transfer_domains": 2}
    result = evaluate(_record(ev, claimed_level="E7_MASTERED"))
    assert result["earned_level"] == "E7_MASTERED"
    assert result["verdict"] == "ACCEPTED"
    assert result["honest_label"] == "E7-proven: mastered"


def test_e7_single_witness_is_not_mastery():
    ev = _full_chain_through_e5()
    ev["retention"] = {
        "revalidated_at": "2026-10-08T06:00:00Z",
        "revalidation_receipt": "rr-1",
    }
    ev["mastery"] = {"distinct_verifiers": 1, "distinct_transfer_domains": 2}
    result = evaluate(_record(ev, claimed_level="E7_MASTERED"))
    assert result["earned_level"] == "E6_RETAINED"
    assert result["verdict"] == "REJECTED"


def test_malformed_input_is_unproven_never_an_exception():
    result = evaluate({"id": "L-bad", "evidence": "not-a-dict", "claimed_level": "E1_UNDERSTANDS"})
    assert result["verdict"] == "UNPROVEN"
    result = evaluate(None)
    assert result["verdict"] == "UNPROVEN"


def test_cumulative_chain_stops_at_first_gap():
    # E2 evidence without E1 comprehension: E2 is unreachable (no skipping rungs)
    ev = _ev(application_receipt={
        "retrieval_ref": "ret-1", "task_ref": "task-A",
        "applied_at": "2026-10-08T02:00:00Z", "applier": "naya-5",
    })
    result = evaluate(_record(ev, claimed_level="E2_CAN_DO"))
    assert result["earned_level"] == "E0_EXPOSED"
    assert result["verdict"] == "REJECTED"
    assert any("unreachable" in u for u in result["unproven"])
