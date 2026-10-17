"""Law 11 v2 exclusion audit trail: the v2 phase must name what it excluded.

Wire's 2026-10-11 T-04 battery found the gap on merged bytes: Law 11 v1 and
Conflict Resolution exclusions are written to receipt evidence, but
law11v2_excluded was collected and then dropped — a candidate refused by the
uncertainty handler vanished from the audit trail (the refusal even
misattributed it to Conflict Resolution). These tests prove the fix: every
exclusion layer names its candidates in the receipt evidence.
"""
import pytest

from kernel import act_pipeline as ap
from kernel.value_calculus import QualityProfile
from kernel.protocol.harm_assessment import (
    HARM_UNCERTAIN,
    SEVERITY_LOW,
    NEUTRAL_TRUE_ZERO,
    NEUTRAL_UNKNOWN,
    HarmAssessment,
)
from kernel.protocol.conflict_resolution import (
    ImpactMatrix,
    OutcomeCell,
    OBS_COMPLETE,
)

NOW = 1_790_000_000.0


def _profile():
    return QualityProfile(profile_id="v2-evidence-trail-test", version="1",
                          objective="minimum sufficient action")


def _authority(**kw):
    base = dict(action="naya_node_apply", scope="naya_node_apply",
                decided_at=NOW - 60, expires_at=None, grant_id="grant-1")
    base.update(kw)
    return ap.LawAuthority(**base)


def _full_assessment(**overrides):
    """Baseline: fully assessed, low severity, safe neutrality."""
    base = dict(
        stakeholder_group="test_group",
        group_size=100,
        harm_type=HARM_UNCERTAIN,
        severity=SEVERITY_LOW,
        likelihood=0.1,
        likelihood_reliability="high",
        reversibility="reversible",
        time_to_appear="immediate",
        cumulative_risk=False,
        detectability="high",
        mitigation_available=True,
        consent_obtained=True,
        monitoring_ready=True,
        stop_conditions_defined=True,
        neutrality_state=NEUTRAL_TRUE_ZERO,
    )
    base.update(overrides)
    return HarmAssessment(**base)


def _candidate(cid="p1", **kw):
    base = dict(
        candidate_id=cid,
        action="naya_node_apply",
        description="v2 evidence trail test",
        quality={"objective_fit": 9.0, "evidence_sufficiency": 9.0,
                 "applicability": 9.0, "robustness": 9.0,
                 "reversibility": 9.0, "blast_containment": 9.0,
                 "simplicity": 9.0},
        confidence={"objective_fit": 0.9, "evidence_sufficiency": 0.9,
                    "applicability": 0.9, "robustness": 0.9,
                    "reversibility": 0.9, "blast_containment": 0.9,
                    "simplicity": 0.9},
        reversibility="REVERSIBLE",
        expected_outcome="done",
        proof_requirements=("receipt",),
        stakes="low",
        lawful=True,
        rights_safe=True,
        privacy_safe=True,
        safety_safe=True,
        value_benefit=8.0, value_harm=1.0, value_cost=1.0, value_risk=0.5,
        value_confidence={"B": 0.9, "H": 0.9, "C": 0.9, "R": 0.9},
        value_evidence_count=3,
    )
    base.update(kw)
    return ap.PlanCandidate(**base)


def _v2_excluded_candidate(cid="p-v2"):
    """Passes the v1 gate, excluded by the v2 uncertainty handler
    (unknown neutrality -> NEEDS_EVIDENCE)."""
    return _candidate(
        cid,
        harm_assessments=(_full_assessment(neutrality_state=NEUTRAL_UNKNOWN),),
    )


def _joined(receipt):
    return " ".join(receipt.evidence)


def test_v2_exclusion_named_in_all_excluded_refusal():
    """All candidates excluded by v2: the refusal evidence names the
    Law 11 v2 layer, the candidate, and the verdict — no silent drop."""
    plan, receipt = ap.plan_action(
        _authority(), [_v2_excluded_candidate()], _profile(), now=NOW)
    assert plan is None
    assert receipt.phase == "PLAN_REFUSED"
    assert ap.PLAN_SAFETY_NEEDS_EVIDENCE in receipt.codes
    joined = _joined(receipt)
    assert "Law 11 v2" in joined
    assert "p-v2" in joined
    assert "NEEDS_EVIDENCE" in joined


def test_v2_exclusion_named_in_accepted_receipt():
    """Happy path: one candidate excluded by v2, one clean candidate wins.
    The accepted receipt's evidence still names the v2 exclusion — the
    audit trail shows what was excluded and why, not just the winner."""
    plan, receipt = ap.plan_action(
        _authority(),
        [_v2_excluded_candidate("p-v2"), _candidate("p-good")],
        _profile(), now=NOW)
    assert plan is not None
    assert plan.chosen.candidate_id == "p-good"
    assert receipt.phase == "PLAN_ACCEPTED"
    joined = _joined(receipt)
    assert "candidate p-v2 EXCLUDED by Law 11 v2" in joined
    assert "p-good" in joined


def test_v2_exclusion_named_in_do_no_harm_gate_refusal():
    """The do-no-harm-gate refusal names v2 exclusions alongside the gate
    exclusions — every prior layer's verdict is visible."""
    v2_excluded = _v2_excluded_candidate("p-v2")
    gate_excluded = _candidate(
        "p-ok",
        quality={"objective_fit": 9.0},  # incomplete -> calculus gate refuses
        confidence={"objective_fit": 0.9},
        harm_assessments=(_full_assessment(),),  # passes v2
    )
    plan, receipt = ap.plan_action(
        _authority(), [v2_excluded, gate_excluded], _profile(), now=NOW)
    assert plan is None
    assert receipt.phase == "PLAN_REFUSED"
    assert ap.PLAN_SAFETY_NEEDS_EVIDENCE in receipt.codes
    joined = _joined(receipt)
    assert "Law 11 v2" in joined
    assert "p-v2" in joined
    assert "p-ok" in joined
    # The v2 exclusion carries its reason, not just the verdict.
    assert "NEUTRALITY" in joined


def _rights_violating_matrix():
    """Impact matrix whose no-worse-off assessment is CR PROHIBITED
    (a rights-protected cell with a negative lower bound)."""
    m = ImpactMatrix(action_id="rights-violation")
    m.add_cell(OutcomeCell(
        group_id="citizens", dimension="speech", horizon="immediate",
        unit="index", baseline_value=1.0, action_value=-1.0,
        lower_bound=-2.0, upper_bound=0.0, tolerance=0.5,
        evidence_quality="adequate", observation_status=OBS_COMPLETE,
        rights_protected=True,
    ))
    return m


def test_v2_exclusion_named_in_cr_prohibited_refusal():
    """The Conflict-Resolution PROHIBITED refusal names the v2 layer,
    the v2-excluded candidate, and its reason — the highest-stakes
    refusal receipt stays complete."""
    v2_excluded = _v2_excluded_candidate("p-v2")
    cr_prohibited = _candidate("p-cr", impact_matrix=_rights_violating_matrix())
    plan, receipt = ap.plan_action(
        _authority(), [v2_excluded, cr_prohibited], _profile(), now=NOW)
    assert plan is None
    assert receipt.phase == "PLAN_REFUSED"
    assert ap.PLAN_SAFETY_PROHIBITED in receipt.codes
    joined = _joined(receipt)
    assert "Law 11 v2" in joined
    assert "p-v2" in joined
    assert "NEUTRALITY" in joined  # the v2 exclusion's reason
    assert "p-cr" in joined


def test_v2_exclusion_named_in_do_no_harm_prohibited_refusal():
    """The do-no-harm-gate PROHIBITED refusal names the v2 layer, the
    v2-excluded candidate, and its reason."""
    v2_excluded = _v2_excluded_candidate("p-v2")
    gate_prohibited = _candidate(
        "p-gate",
        harm_assessments=(_full_assessment(),),  # passes v2
        hard_violation=True,  # calculus gate PROHIBITED (JUDGMENT_RULE_HARD_STOP)
    )
    plan, receipt = ap.plan_action(
        _authority(), [v2_excluded, gate_prohibited], _profile(), now=NOW)
    assert plan is None
    assert receipt.phase == "PLAN_REFUSED"
    assert ap.PLAN_SAFETY_PROHIBITED in receipt.codes
    joined = _joined(receipt)
    assert "Law 11 v2" in joined
    assert "p-v2" in joined
    assert "NEUTRALITY" in joined  # the v2 exclusion's reason
    assert "p-gate" in joined
