"""Negative tests: unresolved critical safety evidence must NOT reach the executor.

SAFETY FIX (2026-10-11): the value calculus verdicts NEEDS_EVIDENCE
when critical safety evidence is missing (e.g. safety_safe=None ->
UNKNOWN_SAFETY). Previously the ACT pipeline's admission filter — in BOTH
plan_action (act_pipeline.py) and execute_plan — was literally
`if gate == PROHIBITED`, so NEEDS_EVIDENCE candidates were planned AND
executed. The fix excludes NEEDS_EVIDENCE from admissible candidates and
refuses it at execution with PLAN_SAFETY_NEEDS_EVIDENCE.

These tests guard the fix:

1. test_calculus_flags_missing_safety_as_needs_evidence — the calculus DOES
   produce NEEDS_EVIDENCE for safety_safe=None (the premise).
2. test_plan_refuses_needs_evidence_candidate — plan_action REFUSES when all
   candidates are NEEDS_EVIDENCE (code PLAN_SAFETY_NEEDS_EVIDENCE).
3. test_executor_refuses_needs_evidence_candidate — execute_plan REFUSES a
   NEEDS_EVIDENCE chosen candidate; the executor never fires.
4. test_end_to_end_unknown_safety_executes_without_mock — documents the
   NEEDS_AUTHORITY path (via _candidate_to_calculus mapping): authority
   routing stays governed by LAW, unaffected by this fix.
"""
from unittest.mock import patch

import pytest

from kernel import act_pipeline as ap
from kernel.value_calculus import (
    ADMISSIBLE,
    NEEDS_EVIDENCE,
    PROHIBITED,
    Candidate,
    PVEstimate,
    QualityProfile,
    RiskPolicy,
    gate_candidate,
)

NOW = 1_790_000_000.0  # fixed clock for deterministic tests


def _profile():
    return QualityProfile(profile_id="needs-evidence-gap-test", version="1",
                          objective="minimum sufficient action")


def _authority(**kw):
    base = dict(action="naya_node_apply", scope="naya_node_apply",
                decided_at=NOW - 60, expires_at=None, grant_id="grant-1")
    base.update(kw)
    return ap.LawAuthority(**base)


def _candidate(cid="e1", **kw):
    base = dict(
        candidate_id=cid,
        action="naya_node_apply",
        description="apply retained intelligence",
        quality={"objective_fit": 9.9, "evidence_sufficiency": 9.9,
                 "applicability": 9.9, "robustness": 9.9,
                 "reversibility": 9.9, "blast_containment": 9.9,
                 "simplicity": 9.9},
        confidence={"objective_fit": 0.99, "evidence_sufficiency": 0.99,
                    "applicability": 0.99, "robustness": 0.99,
                    "reversibility": 0.99, "blast_containment": 0.99,
                    "simplicity": 0.99},
        reversibility="REVERSIBLE",
        expected_outcome="node state updated",
        proof_requirements=("execution_receipt",),
        stakes="low",
        # Critical safety evidence UNRESOLVED — the premise of the concern.
        lawful=True,
        rights_safe=True,
        privacy_safe=True,
        safety_safe=None,
        # V2.1 value estimate — supplied, evidenced, positive.
        benefit=8.0, harm=1.0, cost=1.0, risk=0.5,
        pv_confidence={"B": 0.9, "H": 0.9, "C": 0.9, "R": 0.9},
        pv_evidence_count=2,
    )
    base.update(kw)
    return ap.PlanCandidate(**base)


def _execute(plan, profile=None):
    calls = []
    receipt = ap.execute_plan(
        plan,
        executor=lambda p: calls.append(p) or "done",
        re_resolve=lambda: _authority(decided_at=NOW - 30),
        now=NOW,
        profile=profile or _profile(),
    )
    return receipt, calls


# ---------------- 1. calculus premise: missing safety -> NEEDS_EVIDENCE ----------------

def test_calculus_flags_missing_safety_as_needs_evidence():
    """gate_candidate verdicts NEEDS_EVIDENCE (not PROHIBITED, not ADMISSIBLE)
    when the critical SAFETY predicate is unknown."""
    candidate = Candidate(
        candidate_id="calc-1",
        quality={"objective_fit": 9.0, "evidence_sufficiency": 9.0,
                 "applicability": 9.0, "robustness": 9.0,
                 "reversibility": 9.0, "blast_containment": 9.0,
                 "simplicity": 9.0},
        confidence={"objective_fit": 0.95, "evidence_sufficiency": 0.95,
                    "applicability": 0.95, "robustness": 0.95,
                    "reversibility": 0.95, "blast_containment": 0.95,
                    "simplicity": 0.95},
        pv=PVEstimate(B=10.0, H=1.0, C=1.0, R=0.5,
                      confidence={"B": 0.9, "H": 0.9, "C": 0.9, "R": 0.9},
                      evidence_count=5),
        authorized=True,
        human_authorized=True,
        lawful=True,
        rights_safe=True,
        privacy_safe=True,
        safety_safe=None,  # <-- critical safety evidence missing
        stakes="low",
        reversible=True,
    )
    gate, reasons, _q = gate_candidate(candidate, _profile(), RiskPolicy())
    assert gate == NEEDS_EVIDENCE, f"expected NEEDS_EVIDENCE, got {gate}"
    assert "UNKNOWN_SAFETY" in reasons, f"missing UNKNOWN_SAFETY in {reasons}"
    assert gate != PROHIBITED
    assert gate != ADMISSIBLE


# ---------------- 2-3. pipeline blocks NEEDS_EVIDENCE (mocked gate) ----------------
# REGRESSION GUARD (2026-10-11): these tests previously PROVED the gap —
# plan_action accepted and execute_plan fired NEEDS_EVIDENCE candidates.
# The fix (act_pipeline.py: exclude NEEDS_EVIDENCE from admissible;
# refuse with PLAN_SAFETY_NEEDS_EVIDENCE at execution) closed the gap.
# They now assert the blocking behavior permanently.

def _needs_evidence_gate(candidate, profile, risk_policy):
    """Stand-in for gate_candidate returning the NEEDS_EVIDENCE verdict the
    real calculus produces for missing critical safety evidence."""
    return NEEDS_EVIDENCE, ["HARD_GATE_UNKNOWN", "UNKNOWN_SAFETY"], {}


def test_plan_refuses_needs_evidence_candidate():
    """plan_action refuses when all candidates are NEEDS_EVIDENCE."""
    authority = _authority()
    with patch.object(ap, "gate_candidate", side_effect=_needs_evidence_gate):
        plan, receipt = ap.plan_action(authority, [_candidate()], _profile(), now=NOW)
    assert plan is None, "NEEDS_EVIDENCE candidate must not be planned"
    assert receipt.phase == "PLAN_REFUSED"
    # Synthesis of #2249 + #2254: the mocked reasons carry unknown hard-gate
    # flags (HARD_GATE_UNKNOWN, UNKNOWN_SAFETY), so the specific
    # PLAN_SAFETY_UNKNOWN code takes priority over generic NEEDS_EVIDENCE.
    assert ap.PLAN_SAFETY_UNKNOWN in receipt.codes
    assert receipt.executed is False


def test_executor_refuses_needs_evidence_candidate():
    """execute_plan refuses a NEEDS_EVIDENCE chosen candidate — executor never fires."""
    authority = _authority()
    # Hand-craft a plan (bypassing plan_action) with a NEEDS_EVIDENCE candidate,
    # then verify execute_plan's re-gate refuses it.
    plan = ap.ActionPlan(
        plan_id="test-ne-plan",
        action=authority.action,
        chosen=_candidate(),
        authority=authority,
        candidate_scores=(),
        planned_at=NOW,
    )
    with patch.object(ap, "gate_candidate", side_effect=_needs_evidence_gate):
        calls = []
        receipt = ap.execute_plan(
            plan,
            executor=lambda p: calls.append(p) or "done",
            re_resolve=lambda: _authority(decided_at=NOW - 30),
            now=NOW,
            profile=_profile(),
        )
    assert receipt.phase == "EXECUTION_REFUSED", f"got {receipt.phase}"
    assert receipt.executed is False
    assert len(calls) == 0, "executor must not fire on NEEDS_EVIDENCE"
    # Synthesis: the mocked reasons carry unknown hard-gate flags, so the
    # specific PLAN_SAFETY_UNKNOWN code takes priority.
    assert ap.PLAN_SAFETY_UNKNOWN in receipt.codes


# ---------------- 4. end-to-end, no mocks: unknown safety now refused ----------------

def test_end_to_end_unknown_safety_executes_without_mock():
    """Documents the CLOSED gap: unknown safety is now fail-closed refused.

    A real PlanCandidate with safety_safe=None goes through the pipeline's
    _candidate_to_calculus mapping with authorized=True threaded from the LAW
    scope-match, so the verdict surfaces as NEEDS_EVIDENCE [HARD_GATE_UNKNOWN,
    UNKNOWN_SAFETY] — not masked as NEEDS_AUTHORITY. plan_action refuses with
    PLAN_SAFETY_UNKNOWN. The gap this test originally documented (executor
    firing with safety evidence unresolved) is closed by the unknown-flag
    refusal; unknown safety is never treated as safe.
    """
    authority = _authority()
    plan, plan_receipt = ap.plan_action(authority, [_candidate()], _profile(), now=NOW)
    assert plan is None, "unknown safety must not be planned"
    assert plan_receipt.phase == "PLAN_REFUSED"
    assert ap.PLAN_SAFETY_UNKNOWN in plan_receipt.codes
