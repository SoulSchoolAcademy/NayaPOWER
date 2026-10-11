"""Value-calculus integration: the ACT pipeline routes selection through
the canonical evaluate_candidates().

These tests prove the integration gap is closed:
1. A high-Q candidate with negative value does NOT win (value beats quality).
2. A candidate with missing value evidence does NOT get a zero — it stays
   unknown/provisional (NEEDS_EVIDENCE), never silently zero.
3. A PROHIBITED candidate cannot reach the executor regardless of score.
4. The canonical evaluate_candidates() is actually called, not bypassed.

Module under test: kernel/act_pipeline.plan_action (selection seam).
"""
from unittest.mock import patch

import pytest

from kernel import act_pipeline as ap
from kernel.value_calculus import QualityProfile

NOW = 1_790_000_000.0


def _profile():
    return QualityProfile(profile_id="value-integration-test", version="1",
                          objective="value determines the winner")


def _authority(**kw):
    base = dict(action="naya_node_apply", scope="naya_node_apply",
                decided_at=NOW - 60, expires_at=None, grant_id="grant-1")
    base.update(kw)
    return ap.LawAuthority(**base)


def _valid_pv(**kw):
    """A supplied, evidenced, positive value estimate."""
    base = dict(
        benefit=8.0, harm=1.0, cost=1.0, risk=0.5,
        pv_confidence={"B": 0.9, "H": 0.9, "C": 0.9, "R": 0.9},
        pv_evidence_count=2,
    )
    base.update(kw)
    return base


def _candidate(cid="v1", **kw):
    base = dict(
        candidate_id=cid,
        action="naya_node_apply",
        description="value-integration candidate",
        quality={d: 9.5 for d in (
            "objective_fit", "evidence_sufficiency", "applicability",
            "robustness", "reversibility", "blast_containment", "simplicity")},
        confidence={d: 0.95 for d in (
            "objective_fit", "evidence_sufficiency", "applicability",
            "robustness", "reversibility", "blast_containment", "simplicity")},
        reversibility="REVERSIBLE",
        lawful=True, rights_safe=True, privacy_safe=True, safety_safe=True,
        expected_outcome="value created",
        proof_requirements=("execution_receipt",),
        stakes="low",
    )
    base.update(_valid_pv())
    base.update(kw)
    return ap.PlanCandidate(**base)


# ---------------- 1. value beats quality ----------------

def test_high_q_negative_value_does_not_win():
    """A near-perfect-Q candidate with negative conservative value must not
    win over a lower-Q candidate with positive value. This is the core
    integration proof: the canonical evaluator — not Q — picks the winner."""
    highq_negv = _candidate(
        "v-highq-negv",
        quality={d: 9.9 for d in (
            "objective_fit", "evidence_sufficiency", "applicability",
            "robustness", "reversibility", "blast_containment", "simplicity")},
        # PV = 2 - 1.5 - 1 - 0.5 = -1.0 -> v_safe negative -> ineligible
        benefit=2.0, harm=1.5, cost=1.0, risk=0.5,
    )
    lowq_posv = _candidate("v-lowq-posv")  # Q~9.5, v_safe=5.5
    plan, receipt = ap.plan_action(
        _authority(), [highq_negv, lowq_posv], _profile(), now=NOW)
    assert plan is not None
    assert plan.chosen.candidate_id == "v-lowq-posv"
    # the value math is visible in the receipt
    assert any("v_safe" in e for e in receipt.evidence)
    assert any("evaluate_candidates" in e for e in receipt.evidence)


def test_all_negative_value_refuses_with_value_unproven():
    """When no candidate demonstrates positive value vs. doing nothing,
    planning refuses with PLAN_VALUE_UNPROVEN — it does not pick the
    'least bad' or silently treat negative as zero."""
    neg1 = _candidate("v-neg1", benefit=1.0, harm=3.0, cost=1.0, risk=0.5)
    neg2 = _candidate("v-neg2", benefit=2.0, harm=4.0, cost=1.0, risk=0.5)
    plan, receipt = ap.plan_action(
        _authority(), [neg1, neg2], _profile(), now=NOW)
    assert plan is None
    assert receipt.phase == "PLAN_REFUSED"
    assert ap.PLAN_VALUE_UNPROVEN in receipt.codes
    assert any("unproven, not zero" in e for e in receipt.evidence)


# ---------------- 2. missing evidence stays unknown ----------------

def test_missing_pv_evidence_gates_needs_evidence_not_zero():
    """A candidate with no supplied value estimate must gate NEEDS_EVIDENCE
    (unknown/provisional) — the pipeline must never fabricate a zero PV and
    select on it. Zero Value Law: unknown != zero."""
    no_pv = _candidate("v-nopv")
    # Strip the PV estimate back to unsupplied defaults.
    no_pv = ap.PlanCandidate(
        **{**no_pv.__dict__, "benefit": 0.0, "harm": 0.0, "cost": 0.0,
           "risk": 0.0, "pv_confidence": {}, "pv_evidence_count": 0}
    )
    plan, receipt = ap.plan_action(
        _authority(), [no_pv], _profile(), now=NOW)
    assert plan is None
    assert receipt.phase == "PLAN_REFUSED"
    # NEEDS_EVIDENCE (evidence floor), not a silent zero-value selection.
    assert ap.PLAN_SAFETY_NEEDS_EVIDENCE in receipt.codes
    assert any("EVIDENCE_FLOOR" in e for e in receipt.evidence)


def test_baseline_is_synthesized_when_not_declared():
    """When no candidate declares is_baseline, the pipeline synthesizes the
    do-nothing baseline so evaluate_candidates() always has its required
    baseline-relative reference. The baseline never wins."""
    c = _candidate("v-only")
    plan, receipt = ap.plan_action(_authority(), [c], _profile(), now=NOW)
    assert plan is not None
    assert plan.chosen.candidate_id == "v-only"
    # baseline appears in the value rows but never in candidate_scores
    assert any("__baseline_do_nothing__" in e for e in receipt.evidence)
    assert all(cid != "__baseline_do_nothing__"
              for cid, _q, _v in plan.candidate_scores)


def test_explicit_baseline_is_honored():
    """A caller-declared baseline (is_baseline=True) is used as the
    evaluate_candidates() reference instead of the synthesized one."""
    # A proper explicit baseline: zero value by definition (the current
    # course against itself), but evidenced enough to gate cleanly.
    baseline = _candidate(
        "v-base", is_baseline=True,
        expected_outcome="current course maintained",
        benefit=0.0, harm=0.0, cost=0.0, risk=0.0,
        pv_confidence={"B": 1.0, "H": 1.0, "C": 1.0, "R": 1.0},
        pv_evidence_count=1,
    )
    contender = _candidate("v-contender")
    plan, receipt = ap.plan_action(
        _authority(), [baseline, contender], _profile(), now=NOW)
    assert plan is not None
    # contender has positive value vs. the explicit baseline -> wins
    assert plan.chosen.candidate_id == "v-contender"
    assert not any("__baseline_do_nothing__" in e for e in receipt.evidence)
    assert any("v-base" in e and "BASELINE" in e for e in receipt.evidence)


# ---------------- 3. prohibited cannot reach executor ----------------

def test_prohibited_high_value_candidate_cannot_execute():
    """Even a PROHIBITED candidate with stellar value and quality can never
    reach the executor — the do-no-harm gate fires before selection, and the
    execution re-gate fires before the executor."""
    bad = _candidate("v-bad", hard_violation=True,
                     benefit=100.0, harm=0.0, cost=0.0, risk=0.0)
    good = _candidate("v-good")
    plan, receipt = ap.plan_action(
        _authority(), [bad, good], _profile(), now=NOW)
    assert plan is not None
    assert plan.chosen.candidate_id == "v-good"

    # Belt-and-suspenders: hand-craft a plan with the prohibited candidate
    # and verify the execution re-gate refuses it.
    evil_plan = ap.ActionPlan(
        plan_id="evil", action="naya_node_apply", chosen=bad,
        authority=_authority(), candidate_scores=(), planned_at=NOW)
    calls = []
    exec_receipt = ap.execute_plan(
        evil_plan,
        executor=lambda p: calls.append(p) or "done",
        re_resolve=lambda: _authority(decided_at=NOW - 30),
        now=NOW, profile=_profile())
    assert exec_receipt.phase == "EXECUTION_REFUSED"
    assert exec_receipt.executed is False
    assert len(calls) == 0
    assert ap.PLAN_SAFETY_PROHIBITED in exec_receipt.codes


# ---------------- 4. canonical evaluator is actually called ----------------

def test_evaluate_candidates_is_called_not_bypassed():
    """Spy on the canonical evaluate_candidates(): plan_action must route
    through it. If the pipeline ever regresses to quality-only selection,
    this test fails."""
    c = _candidate("v-spy")
    with patch.object(ap, "evaluate_candidates",
                      wraps=ap.evaluate_candidates) as spy:
        plan, receipt = ap.plan_action(
            _authority(), [c], _profile(), now=NOW)
    assert spy.called, "plan_action bypassed the canonical evaluator"
    assert spy.call_count == 1
    # called with the do-nothing baseline synthesized
    called_candidates = spy.call_args[0][0]
    assert any(getattr(x, "is_baseline", False) for x in called_candidates)
    assert plan is not None
    assert plan.chosen.candidate_id == "v-spy"


def test_no_quality_only_fallback_when_calculus_selects_nothing():
    """When evaluate_candidates() selects nothing, plan_action must refuse —
    never fall back to quality-only ranking. Sabotage the evaluator to
    return no selection and verify the pipeline refuses."""
    c = _candidate("v-sabotage")
    fake_evaluation = {
        "decision": "READ_MORE", "selected": None, "top3": [], "rows": [],
        "frontier": [], "relative_margin": None, "interval_gap": None,
    }
    with patch.object(ap, "evaluate_candidates",
                      return_value=fake_evaluation):
        plan, receipt = ap.plan_action(
            _authority(), [c], _profile(), now=NOW)
    assert plan is None, "pipeline fell back to quality-only selection"
    assert receipt.phase == "PLAN_REFUSED"
    assert ap.PLAN_VALUE_UNPROVEN in receipt.codes
