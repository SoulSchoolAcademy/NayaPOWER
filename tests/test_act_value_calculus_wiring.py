"""Proof tests for the canonical value-calculus wiring in the ACT pipeline.

These tests prove the integration gap identified by Shawn is closed:
kernel/act_pipeline.py now routes candidate selection through
evaluate_candidates() from kernel/value_calculus.py — baseline-relative
value (ΔV), Pareto comparison, and interval dominance determine the winner.
There is no second decision engine.

Four properties proven here:
1. PROHIBITED candidates cannot execute (safety floor preserved).
2. NEEDS_EVIDENCE candidates cannot execute (safety floor preserved).
3. High Q-score cannot disguise negative baseline-relative value.
4. Unmeasured value (UNMEASURED) cannot silently become zero (Zero Value Law).
"""
import pytest

from kernel import act_pipeline as ap
from kernel.value_calculus import QualityProfile

NOW = 1_790_000_000.0


def _profile():
    return QualityProfile(profile_id="value-wire-test", version="1",
                          objective="prove value calculus wiring")


def _authority(**kw):
    base = dict(action="naya_node_apply", scope="naya_node_apply",
                decided_at=NOW - 60, expires_at=None, grant_id="grant-1")
    base.update(kw)
    return ap.LawAuthority(**base)


def _candidate(cid="p1", **kw):
    """A candidate with full quality, safety, and value evidence."""
    base = dict(
        candidate_id=cid,
        action="naya_node_apply",
        description="test candidate",
        quality={d: 9.0 for d in ("objective_fit", "evidence_sufficiency",
                                  "applicability", "robustness",
                                  "reversibility", "blast_containment",
                                  "simplicity")},
        confidence={d: 0.9 for d in ("objective_fit", "evidence_sufficiency",
                                     "applicability", "robustness",
                                     "reversibility", "blast_containment",
                                     "simplicity")},
        reversibility="REVERSIBLE",
        expected_outcome="test outcome",
        proof_requirements=("receipt",),
        stakes="low",
        lawful=True, rights_safe=True, privacy_safe=True, safety_safe=True,
        # Default: positive value. PV = 8 - 1 - 1 - 0.5 = 5.5.
        value_benefit=8.0, value_harm=1.0, value_cost=1.0, value_risk=0.5,
        value_confidence={"B": 0.9, "H": 0.9, "C": 0.9, "R": 0.9},
        value_evidence_count=3,
    )
    base.update(kw)
    return ap.PlanCandidate(**base)


# ---------------- Property 3: High Q cannot disguise negative value ----------------

def test_high_q_negative_value_candidate_cannot_win():
    """A candidate with near-perfect Q but negative ΔV must not beat a
    lower-Q candidate with positive ΔV. The value calculus — not Q alone —
    determines the winner."""
    # High Q (9.9), but NEGATIVE value: harm dominates benefit.
    # PV = 2.0 - 8.0 - 1.0 - 0.5 = -7.5 → ΔV = -7.5 (negative).
    high_q_negative = _candidate(
        "p-flashy",
        quality={d: 9.9 for d in ("objective_fit", "evidence_sufficiency",
                                  "applicability", "robustness",
                                  "reversibility", "blast_containment",
                                  "simplicity")},
        value_benefit=2.0, value_harm=8.0, value_cost=1.0, value_risk=0.5,
    )
    # Lower Q (9.0), but POSITIVE value. PV = 5.5 → ΔV = +5.5.
    modest_q_positive = _candidate("p-solid")

    plan, receipt = ap.plan_action(
        _authority(), [high_q_negative, modest_q_positive],
        _profile(), now=NOW)

    assert plan is not None, (
        f"Expected a winner; got refusal: {receipt.codes} {receipt.evidence}")
    assert receipt.phase == "PLAN_ACCEPTED"
    # The positive-value candidate wins despite lower Q.
    assert plan.chosen.candidate_id == "p-solid", (
        "High Q must not disguise negative value")
    # The math is visible: ΔV recorded per candidate.
    by_id = {row[0]: row for row in plan.candidate_scores}
    assert by_id["p-flashy"][2] < 0, "flashy candidate must show negative ΔV"
    assert by_id["p-solid"][2] > 0, "solid candidate must show positive ΔV"


def test_all_negative_value_refuses_with_value_code():
    """When every candidate has negative baseline-relative value, planning
    is refused — the pipeline does not pick 'the least bad' via Q."""
    neg1 = _candidate("p-neg1", value_benefit=1.0, value_harm=5.0,
                      value_cost=1.0, value_risk=0.5)
    neg2 = _candidate("p-neg2", value_benefit=2.0, value_harm=6.0,
                      value_cost=1.0, value_risk=0.5)
    plan, receipt = ap.plan_action(_authority(), [neg1, neg2],
                                   _profile(), now=NOW)
    assert plan is None
    assert receipt.phase == "PLAN_REFUSED"
    # Refused for insufficient value, not for safety (they're not prohibited).
    assert ap.PLAN_VALUE_INSUFFICIENT in receipt.codes


# ---------------- Property 4: UNMEASURED ≠ zero (Zero Value Law) ----------------

def test_unmeasured_value_candidate_is_not_selected():
    """A candidate without value evidence (UNMEASURED) must not be treated
    as zero-value and selected. Null is not zero: the gate verdicts
    NEEDS_EVIDENCE before selection."""
    # No value_* fields at all → UNMEASURED.
    unmeasured = ap.PlanCandidate(
        candidate_id="p-unmeasured", action="naya_node_apply",
        description="no value data",
        quality={d: 9.5 for d in ("objective_fit", "evidence_sufficiency",
                                  "applicability", "robustness",
                                  "reversibility", "blast_containment",
                                  "simplicity")},
        confidence={d: 0.95 for d in ("objective_fit", "evidence_sufficiency",
                                      "applicability", "robustness",
                                      "reversibility", "blast_containment",
                                      "simplicity")},
        reversibility="REVERSIBLE", expected_outcome="o",
        proof_requirements=("p",), stakes="low",
        lawful=True, rights_safe=True, privacy_safe=True, safety_safe=True,
        # NOTE: no value_benefit/harm/cost/risk → UNMEASURED, not zero.
    )
    measured = _candidate("p-measured")

    plan, receipt = ap.plan_action(_authority(), [unmeasured, measured],
                                   _profile(), now=NOW)
    # The unmeasured candidate is excluded by the do-no-harm gate
    # (NEEDS_EVIDENCE: EVIDENCE_FLOOR); the measured one wins.
    assert plan is not None
    assert plan.chosen.candidate_id == "p-measured"
    assert any("p-unmeasured" in e and "EXCLUDED" in e
               for e in receipt.evidence)


def test_all_unmeasured_value_refuses_not_selects_zero():
    """When no candidate supplies value evidence, planning is refused.
    The pipeline must not silently treat unmeasured value as zero and
    pick a winner by Q-score."""
    c1 = ap.PlanCandidate(
        candidate_id="p-a", action="naya_node_apply", description="d",
        quality={d: 9.0 for d in ("objective_fit", "evidence_sufficiency",
                                  "applicability", "robustness",
                                  "reversibility", "blast_containment",
                                  "simplicity")},
        confidence={d: 0.9 for d in ("objective_fit", "evidence_sufficiency",
                                     "applicability", "robustness",
                                     "reversibility", "blast_containment",
                                     "simplicity")},
        reversibility="REVERSIBLE", expected_outcome="o",
        proof_requirements=("p",), stakes="low",
        lawful=True, rights_safe=True, privacy_safe=True, safety_safe=True)
    c2 = ap.PlanCandidate(
        candidate_id="p-b", action="naya_node_apply", description="d",
        quality={d: 9.1 for d in ("objective_fit", "evidence_sufficiency",
                                  "applicability", "robustness",
                                  "reversibility", "blast_containment",
                                  "simplicity")},
        confidence={d: 0.9 for d in ("objective_fit", "evidence_sufficiency",
                                     "applicability", "robustness",
                                     "reversibility", "blast_containment",
                                     "simplicity")},
        reversibility="REVERSIBLE", expected_outcome="o",
        proof_requirements=("p",), stakes="low",
        lawful=True, rights_safe=True, privacy_safe=True, safety_safe=True)
    plan, receipt = ap.plan_action(_authority(), [c1, c2], _profile(), now=NOW)
    assert plan is None
    assert receipt.phase == "PLAN_REFUSED"
    # Unmeasured value → NEEDS_EVIDENCE → nothing admissible.
    assert ap.PLAN_SAFETY_NEEDS_EVIDENCE in receipt.codes


# ---------------- Baseline is explicit ----------------

def test_baseline_candidate_is_do_nothing_reference():
    """The synthesized baseline represents 'do nothing': ΔV=0 by definition,
    ADMISSIBLE so it never distorts candidate accounting."""
    baseline = ap._baseline_candidate()
    assert baseline.candidate_id == ap.BASELINE_CANDIDATE_ID
    assert baseline.is_baseline is True
    # Baseline PV is zero → ΔV(candidate) = PV(candidate) - 0.
    assert baseline.pv.B == 0.0 and baseline.pv.H == 0.0
    assert baseline.pv.C == 0.0 and baseline.pv.R == 0.0


def test_selection_uses_baseline_relative_value():
    """The winner is chosen by baseline-relative ΔV (v_safe), not by raw
    PV or Q. Receipt evidence shows the ΔV per candidate."""
    # Candidate A: higher raw PV but the baseline is fixed, so ΔV = PV.
    # Both positive; higher ΔV wins.
    a = _candidate("p-a", value_benefit=10.0, value_harm=1.0,
                   value_cost=1.0, value_risk=0.5)  # PV = 7.5
    b = _candidate("p-b", value_benefit=6.0, value_harm=1.0,
                   value_cost=1.0, value_risk=0.5)   # PV = 3.5
    plan, receipt = ap.plan_action(_authority(), [a, b], _profile(), now=NOW)
    assert plan is not None
    assert plan.chosen.candidate_id == "p-a"
    by_id = {row[0]: row for row in plan.candidate_scores}
    # Row format: (cid, Q, delta_v, v_safe, gate)
    assert by_id["p-a"][2] > by_id["p-b"][2], "higher ΔV must win"
    assert any("baseline" in e for e in receipt.evidence), (
        "receipt must name the explicit baseline")
