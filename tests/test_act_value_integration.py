"""ACT x Value Calculus integration: the math decides which action wins.

Module under test: kernel/act_pipeline.plan_action (value-routed selection).

These tests falsify the integration gap: before this change, ACT selected on
quality score Q with benefit/cost/risk zeroed out, so the canonical value
calculus never determined the winner. Every test here would FAIL on that
old path (selection by Q with zeroed value components).

Falsifier pattern: each test constructs a case where Q-ranking and
value-ranking disagree, or where value evidence is missing — and asserts
the canonical evaluate_candidates() path decides.
"""
import pytest

from kernel import act_pipeline as ap
from kernel.value_calculus import (
    NEEDS_EVIDENCE,
    QUALITY_DIMENSIONS,
    QualityProfile,
)

NOW = 1_790_000_000.0
ALL_DIMS = tuple(QUALITY_DIMENSIONS)


def _profile(**kw):
    base = dict(profile_id="act-value-test", version="1",
                objective="value-routed selection")
    base.update(kw)
    return QualityProfile(**base)


def _authority(**kw):
    base = dict(action="act1", scope="act1",
                decided_at=NOW - 60, expires_at=None, grant_id="grant-1")
    base.update(kw)
    return ap.LawAuthority(**base)


def _candidate(cid="v1", **kw):
    base = dict(
        candidate_id=cid,
        action="act1",
        description="value-routed candidate",
        quality={d: 9.5 for d in ALL_DIMS},
        confidence={d: 0.95 for d in ALL_DIMS},
        reversibility="REVERSIBLE",
        expected_outcome="done",
        proof_requirements=("p",),
        stakes="low",
        lawful=True, rights_safe=True, privacy_safe=True, safety_safe=True,
        benefit=5.0, harm=1.0, cost=1.0, risk=0.5,
        value_confidence={"B": 0.9, "H": 0.9, "C": 0.9, "R": 0.9},
        value_evidence_count=3,
    )
    base.update(kw)
    return ap.PlanCandidate(**base)


def _plan(candidates, **kw):
    return ap.plan_action(_authority(), candidates, _profile(), now=NOW, **kw)


# ---------------- the S7 case: value beats quality ----------------

def test_high_q_negative_value_loses_to_lower_q_positive_value():
    """The headline falsifier: flashy has higher Q but negative value;
    solid has lower Q but positive value. The canonical path must pick
    solid. On the old Q-sort path, flashy wins."""
    flashy = _candidate("flashy",
                        quality={d: 9.8 for d in ALL_DIMS},
                        benefit=2.0, harm=8.0, cost=0.0, risk=0.0)
    solid = _candidate("solid",
                       quality={d: 9.1 for d in ALL_DIMS},
                       benefit=6.0, harm=1.0, cost=1.0, risk=0.5)
    plan, receipt = _plan([flashy, solid])
    assert plan is not None, f"expected a plan, got {receipt.codes}"
    assert receipt.phase == "PLAN_ACCEPTED"
    assert plan.chosen.candidate_id == "solid"
    by_id = {cid: (q, v, d) for cid, q, v, d in plan.candidate_scores}
    assert by_id["flashy"][1] < 0 < by_id["solid"][1], \
        "v_safe must be negative for flashy, positive for solid"
    assert any("canonical value ranking" in e for e in receipt.evidence)
    assert any("interval=[" in e for e in receipt.evidence), \
        "the math is visible: intervals recorded"


def test_negative_value_never_wins_even_when_alone():
    """A single ADMISSIBLE candidate with negative conservative value:
    the canonical path yields no selection -> PLAN_NEEDS_EVIDENCE."""
    plan, receipt = _plan([_candidate("neg", benefit=1.0, harm=5.0)])
    assert plan is None
    assert receipt.phase == "PLAN_REFUSED"
    assert ap.PLAN_NEEDS_EVIDENCE in receipt.codes


def test_zero_value_candidate_is_not_selected():
    """v_safe exactly 0 is not > 0: no selection, honest refusal."""
    plan, receipt = _plan([_candidate("zero", benefit=2.0, harm=1.0,
                                      cost=1.0, risk=0.0,
                                      value_confidence={"B": 1.0, "H": 1.0,
                                                        "C": 1.0, "R": 1.0})])
    # pv = 2-1-1-max(0, 1*(1-1.0)) = 0 -> v_safe = 0 -> not eligible
    assert plan is None
    assert ap.PLAN_NEEDS_EVIDENCE in receipt.codes


# ---------------- prohibited / unknown can never win ----------------

def test_prohibited_high_value_candidate_cannot_win():
    """Even with enormous value, a PROHIBITED candidate is excluded."""
    bad = _candidate("bad", hard_violation=True, benefit=100.0)
    good = _candidate("good")
    plan, receipt = _plan([bad, good])
    assert plan is not None
    assert plan.chosen.candidate_id == "good"
    assert any("bad" in e and "EXCLUDED" in e for e in receipt.evidence)


def test_unknown_safety_flag_refused_not_selected():
    plan, receipt = _plan([_candidate("u", safety_safe=None)])
    assert plan is None
    assert ap.PLAN_SAFETY_UNKNOWN in receipt.codes


# ---------------- value-evidence contract: no silent zeros ----------------

def test_missing_value_components_are_refused():
    """benefit=None: PLAN_VALUE_UNDEFINED — never silently zeroed."""
    plan, receipt = ap.plan_action(
        _authority(),
        [ap.PlanCandidate(
            candidate_id="noval", action="act1", description="d",
            quality={d: 9.5 for d in ALL_DIMS},
            confidence={d: 0.95 for d in ALL_DIMS},
            reversibility="REVERSIBLE", expected_outcome="ok",
            proof_requirements=("p",),
            lawful=True, rights_safe=True, privacy_safe=True, safety_safe=True)],
        _profile(), now=NOW)
    assert plan is None
    assert receipt.phase == "PLAN_REFUSED"
    assert ap.PLAN_VALUE_UNDEFINED in receipt.codes


def test_negative_value_components_are_refused():
    plan, receipt = _plan([_candidate("negb", benefit=-1.0)])
    assert plan is None
    assert ap.PLAN_VALUE_UNDEFINED in receipt.codes


def test_empty_value_confidence_cannot_win():
    """Uncertainty is not zero: empty per-component confidence floors the
    candidate to NEEDS_EVIDENCE via the calculus — it cannot win."""
    plan, receipt = _plan([_candidate("noc", value_confidence={})])
    assert plan is None
    assert ap.PLAN_NEEDS_EVIDENCE in receipt.codes
    assert any("PV_COMPONENT_CONFIDENCE_FLOOR" in e for e in receipt.evidence)


def test_zero_evidence_count_cannot_win():
    plan, receipt = _plan([_candidate("noev", value_evidence_count=0)])
    assert plan is None
    assert ap.PLAN_NEEDS_EVIDENCE in receipt.codes
    assert any("EVIDENCE_FLOOR" in e for e in receipt.evidence)


# ---------------- explicit baseline ----------------

def test_caller_supplied_baseline_is_used():
    """Delta is measured against the caller's explicit baseline, and the
    receipt names it."""
    base = _candidate("my-base", is_baseline=True,
                      benefit=2.0, harm=0.0, cost=0.0, risk=0.0,
                      expected_outcome="stay the course")
    cand = _candidate("c1", benefit=6.0, harm=1.0, cost=1.0, risk=0.5)
    plan, receipt = _plan([base, cand])
    assert plan is not None
    assert plan.chosen.candidate_id == "c1"
    assert receipt.baseline_id == "my-base"
    # pv(c1) = 6-1-1-0.5 = 3.5; pv(base) = 2-0-0-0.1 = 1.9; delta = 1.6
    assert receipt.predicted_delta_v == pytest.approx(1.6)
    assert plan.baseline_id == "my-base"


def test_synthesized_baseline_when_caller_supplies_none():
    plan, receipt = _plan([_candidate("c1")])
    assert plan is not None
    assert receipt.baseline_id == ap.SYNTH_BASELINE_ID
    assert plan.baseline_id == ap.SYNTH_BASELINE_ID


def test_ambiguous_baseline_is_refused():
    plan, receipt = _plan([
        _candidate("b1", is_baseline=True),
        _candidate("b2", is_baseline=True),
    ])
    assert plan is None
    assert ap.PLAN_BASELINE_AMBIGUOUS in receipt.codes


def test_baseline_itself_is_never_selected():
    """Even when nothing else qualifies, the do-nothing baseline
    (v_safe = 0) is never chosen — planning refuses honestly."""
    plan, receipt = _plan([_candidate("neg", benefit=1.0, harm=5.0)])
    assert plan is None  # not a plan for the baseline
    assert ap.PLAN_NEEDS_EVIDENCE in receipt.codes


# ---------------- canonical tie-breaking is deterministic ----------------

def test_canonical_tiebreak_prefers_higher_confidence():
    """Same v_safe: the canonical sort key breaks the tie deterministically
    (higher aggregate confidence wins)."""
    a = _candidate("a", benefit=5.0,
                   value_confidence={"B": 0.9, "H": 0.9, "C": 0.9, "R": 0.9})
    b = _candidate("b", benefit=5.0,
                   value_confidence={"B": 0.99, "H": 0.99, "C": 0.99, "R": 0.99},
                   confidence={d: 0.99 for d in ALL_DIMS})
    plan, receipt = _plan([a, b])
    assert plan is not None
    assert plan.chosen.candidate_id == "b"


# ---------------- learning-loop stub ----------------

def test_learning_loop_fields_on_plan_receipt():
    window = {"status": "OPEN", "ends_at": "2026-11-10T00:00:00Z"}
    plan, receipt = _plan([_candidate("c1")], observation_window=window)
    assert receipt.phase == "PLAN_ACCEPTED"
    assert receipt.predicted_delta_v is not None
    assert receipt.baseline_id == ap.SYNTH_BASELINE_ID
    assert receipt.observation_window == window
    assert plan.predicted_delta_v == receipt.predicted_delta_v
    assert plan.baseline_id == receipt.baseline_id
    assert plan.observation_window == window


def test_learning_loop_fields_survive_execution_and_verify():
    plan, _ = _plan([_candidate("c1")],
                    observation_window={"status": "OPEN"})
    receipt = ap.execute_plan(
        plan, executor=lambda p: "done",
        re_resolve=lambda: _authority(decided_at=NOW - 30),
        now=NOW, profile=_profile())
    assert receipt.phase == "EXECUTION_COMPLETED"
    assert receipt.predicted_delta_v == plan.predicted_delta_v
    assert receipt.baseline_id == plan.baseline_id
    assert receipt.observation_window == {"status": "OPEN"}
    closed = ap.apply_verify_verdict(receipt, verified=True, evidence="v")
    assert closed.predicted_delta_v == plan.predicted_delta_v
    assert closed.baseline_id == plan.baseline_id


# ---------------- execute-time enforcement ----------------

def test_execute_refuses_needs_evidence_verdict(monkeypatch):
    """Insufficiently-evidenced candidates cannot execute: the re-gate
    refuses NEEDS_EVIDENCE even if a hand-crafted plan smuggles one in."""
    def fake_gate(_c, _p, _r):
        return NEEDS_EVIDENCE, ["EVIDENCE_FLOOR"], {}
    monkeypatch.setattr(ap, "gate_candidate", fake_gate)
    plan = ap.ActionPlan(plan_id="hand-1", action="act1",
                         chosen=_candidate("c1"), authority=_authority(),
                         candidate_scores=(), planned_at=NOW)
    calls = []
    receipt = ap.execute_plan(
        plan, executor=lambda p: calls.append(p) or "done",
        re_resolve=lambda: _authority(decided_at=NOW - 30),
        now=NOW, profile=_profile())
    assert receipt.phase == "EXECUTION_REFUSED"
    assert receipt.executed is False
    assert ap.PLAN_NEEDS_EVIDENCE in receipt.codes
    assert calls == []


def test_needs_authority_handcrafted_plan_still_executes():
    """The LAW-governed path is preserved: NEEDS_AUTHORITY (authority
    enforced by live re-resolution, not the safety seam) still executes."""
    plan = ap.ActionPlan(plan_id="hand-2", action="act1",
                         chosen=_candidate("c1"), authority=_authority(),
                         candidate_scores=(), planned_at=NOW)
    calls = []
    receipt = ap.execute_plan(
        plan, executor=lambda p: calls.append(p) or "done",
        re_resolve=lambda: _authority(decided_at=NOW - 30),
        now=NOW, profile=_profile())
    assert receipt.phase == "EXECUTION_COMPLETED"
    assert calls != []


def test_stakes_medium_does_not_crash_gate():
    """Pipeline stakes 'medium' maps conservatively onto the calculus
    stake order (no unknown-stake crash)."""
    plan, receipt = _plan([_candidate("m", stakes="medium")])
    assert receipt.phase == "PLAN_ACCEPTED"
    assert plan.chosen.candidate_id == "m"
