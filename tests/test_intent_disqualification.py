"""Tests for the Intent Doctrine / Disqualification Doctrine (Shawn, 2026-10-11).

An action intended to harm is DISQUALIFIED — excluded from A_admissible —
not scored zero. Intent is the disqualifier, not risk: a well-intentioned
action with calculated, manageable risk remains admissible.
"""
import pytest

from kernel.value_calculus import (
    ADMISSIBLE,
    ELIGIBLE_BLOCKED,
    PROHIBITED,
    Candidate,
    OperationRequest,
    PVEstimate,
    QualityProfile,
    RiskPolicy,
    TailRisk,
    consequential_use_eligible,
    evaluate_candidates,
    gate_candidate,
    retrieval_eligible,
)


@pytest.fixture
def profile():
    return QualityProfile(
        profile_id="NAYAPOWER-DECISION",
        version="2.1",
        objective="maximum responsible verified value",
        min_evidence_count=2,
        relative_margin=0.10,
    )


@pytest.fixture
def policy():
    return RiskPolicy()


def pv(B=8, H=0, C=1, R=0.2, conf=0.95, evidence_count=3):
    return PVEstimate(B, H, C, R, {k: conf for k in ("B", "H", "C", "R")}, evidence_count)


def quality(score=9.5, conf=0.95, **overrides):
    dims = {
        "objective_fit": score,
        "evidence_sufficiency": score,
        "applicability": score,
        "robustness": score,
        "reversibility": score,
        "blast_containment": score,
        "simplicity": score,
    }
    dims.update(overrides)
    return dims, {k: conf for k in dims}


def cand(cid, *, baseline=False, B=8, score=9.5, conf=0.95, **kwargs):
    q, c = quality(score, conf)
    hard = dict(lawful=True, rights_safe=True, privacy_safe=True, safety_safe=True)
    hard.update({k: kwargs.pop(k) for k in list(kwargs) if k in hard})
    return Candidate(
        cid, q, c, pv(B=B, conf=conf), authorized=True, reversible=True,
        human_authorized=False, is_baseline=baseline, **hard, **kwargs
    )


def test_intent_to_harm_disqualified(profile, policy):
    """intent_to_harm=True → PROHIBITED with HARMFUL_INTENT_DISQUALIFIED."""
    c = cand("harmful", intent_to_harm=True)
    gate, reasons, _ = gate_candidate(c, profile, policy)
    assert gate == PROHIBITED
    assert reasons == ["HARMFUL_INTENT_DISQUALIFIED"]


def test_disqualification_not_zero_scoring(profile, policy):
    """A PROHIBITED candidate is EXCLUDED from eligible — it cannot win even
    with the highest v_safe. Disqualification != zero-scoring: a zero-scored
    candidate still competes; a disqualified one is not in the race."""
    baseline = cand("baseline", baseline=True, B=1, score=6.0)
    # The harmful candidate has the HIGHEST value score — if it were merely
    # zero-scored it could still win against weak alternatives. Disqualified
    # candidates must not appear in eligible/ranked_all at all.
    harmful = cand("harmful", intent_to_harm=True, B=99, score=10.0)
    good = cand("good", B=8, score=9.0)
    result = evaluate_candidates([baseline, harmful, good], "baseline", profile, policy)
    eligible_ids = [r["candidate_id"] for r in result["rows"] if r["gate"] == ADMISSIBLE]
    frontier_ids = [r["candidate_id"] for r in result["frontier"]]
    top3_ids = [r["candidate_id"] for r in result["top3"]]
    assert "harmful" not in eligible_ids
    assert "harmful" not in frontier_ids
    assert "harmful" not in top3_ids
    assert result["selected"] is not None
    assert result["selected"] != "harmful"


def test_well_intentioned_risk_admissible(profile, policy):
    """intent_to_harm=False with a tail risk below severity/probability
    thresholds → ADMISSIBLE. Risk != intent."""
    low_tail = TailRisk(severity=5.0, probability=0.005, harm_class="general")
    c = cand("helper", intent_to_harm=False, tails=[low_tail])
    gate, reasons, _ = gate_candidate(c, profile, policy)
    assert gate == ADMISSIBLE, f"well-intentioned risk must be admissible, got {gate}: {reasons}"


def test_intent_gate_first(profile, policy):
    """intent_to_harm=True with every other flag clean → still PROHIBITED.
    The intent check runs before all other gates."""
    c = cand("sneaky", intent_to_harm=True, hard_violation=False)
    gate, reasons, _ = gate_candidate(c, profile, policy)
    assert gate == PROHIBITED
    assert reasons == ["HARMFUL_INTENT_DISQUALIFIED"]


def test_operation_request_intent_disqualified_retrieval():
    """OperationRequest with intent_to_harm → ELIGIBLE_BLOCKED on retrieval."""
    req = OperationRequest(
        operation_id="op-1",
        requester_id="r1",
        requester_scope="owner:a",
        object_scope="owner:a",
        intent_to_harm=True,
    )
    receipt = retrieval_eligible(req)
    assert receipt["state"] == ELIGIBLE_BLOCKED
    assert receipt["reasons"] == ["HARMFUL_INTENT_DISQUALIFIED"]


def test_operation_request_intent_disqualified_consequential(profile):
    """OperationRequest with intent_to_harm → ELIGIBLE_BLOCKED on consequential use."""
    req = OperationRequest(
        operation_id="op-2",
        requester_id="r1",
        requester_scope="owner:a",
        object_scope="owner:a",
        consequential=True,
        human_authorized=True,
        intent_to_harm=True,
    )
    receipt = consequential_use_eligible(req, profile)
    assert receipt["state"] == ELIGIBLE_BLOCKED
    assert receipt["reasons"] == ["HARMFUL_INTENT_DISQUALIFIED"]
