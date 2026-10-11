"""Safety: do-no-harm enforcement at the ACT execution seam.

Module under test: kernel/act_pipeline.plan_action.

The Decision Value Calculus carries hard do-no-harm gates (PROHIBITED for
hard violations, explicit unsafe flags, tail risk, distributional harm).
These tests falsify the seam: a harmful candidate must be excluded from
selection and can never win or execute, no matter how high its Q score.
If any of these tests fail, harmful actions are executable — the safety
floor is broken.

Falsifier pattern: every test would FAIL if the gate were bypassed (i.e.
if plan_action selected on Q alone).
"""
import pytest

from kernel import act_pipeline as ap
from kernel.value_calculus import QUALITY_DIMENSIONS, QualityProfile, TailRisk

ALL_DIMS = tuple(QUALITY_DIMENSIONS)

NOW = 1_790_000_000.0


def _profile():
    return QualityProfile(profile_id="safety-act-test", version="1",
                          objective="do-no-harm enforcement")


def _authority(**kw):
    base = dict(action="naya_node_apply", scope="naya_node_apply",
                decided_at=NOW - 60, expires_at=None, grant_id="grant-1")
    base.update(kw)
    return ap.LawAuthority(**base)


def _candidate(cid="p1", **kw):
    base = dict(
        candidate_id=cid,
        action="naya_node_apply",
        description="apply retained intelligence to NAYA-NODE-0001",
        quality={"objective_fit": 9.5, "evidence_sufficiency": 9.5,
                 "applicability": 9.5, "robustness": 9.5,
                 "reversibility": 9.5, "blast_containment": 9.5,
                 "simplicity": 9.5},
        confidence={"objective_fit": 0.95, "evidence_sufficiency": 0.95,
                    "applicability": 0.95, "robustness": 0.95,
                    "reversibility": 0.95, "blast_containment": 0.95,
                    "simplicity": 0.95},
        reversibility="REVERSIBLE",
        # Explicitly safe: unknown (None) hard-gate flags are fail-closed
        # refused at plan (PLAN_SAFETY_UNKNOWN) — "clean" means proven safe,
        # not unknown. Tests needing None/False pass explicit kwargs.
        lawful=True, rights_safe=True, privacy_safe=True, safety_safe=True,
        expected_outcome="node state updated, previous state restorable",
        proof_requirements=("execution_receipt", "state_diff"),
        stakes="low",
        benefit=5.0, harm=1.0, cost=1.0, risk=0.5,
        value_confidence={"B": 0.9, "H": 0.9, "C": 0.9, "R": 0.9},
        value_evidence_count=3,
    )
    base.update(kw)
    return ap.PlanCandidate(**base)


def _perfect_q(cid="p1", **kw):
    """A candidate with near-perfect decision quality — the falsifier's
    bait. If the gate is bypassed, this candidate always wins on Q."""
    kw.setdefault("quality", {"objective_fit": 9.9, "evidence_sufficiency": 9.9,
                 "applicability": 9.9, "robustness": 9.9,
                 "reversibility": 9.9, "blast_containment": 9.9,
                 "simplicity": 9.9})
    kw.setdefault("confidence", {"objective_fit": 0.99, "evidence_sufficiency": 0.99,
                    "applicability": 0.99, "robustness": 0.99,
                    "reversibility": 0.99, "blast_containment": 0.99,
                    "simplicity": 0.99})
    return _candidate(cid, **kw)


# ---------------- hard violation ----------------

def test_hard_violation_candidate_is_refused():
    plan, receipt = ap.plan_action(_authority(), [_candidate(hard_violation=True)],
                                  _profile(), now=NOW)
    assert plan is None
    assert receipt.phase == "PLAN_REFUSED"
    assert ap.PLAN_SAFETY_PROHIBITED in receipt.codes
    assert any("JUDGMENT_RULE_HARD_STOP" in e for e in receipt.evidence)


def test_high_q_hard_violation_cannot_win():
    """FALSIFIER: a near-perfect-Q harmful candidate must not beat a
    mediocre clean one. Without the gate, the harmful candidate wins."""
    harmful = _perfect_q("p-harmful", hard_violation=True)
    clean = _candidate("p-clean")
    plan, receipt = ap.plan_action(_authority(), [harmful, clean],
                                  _profile(), now=NOW)
    assert plan is not None
    assert plan.chosen.candidate_id == "p-clean"
    assert any("p-harmful" in e and "EXCLUDED" in e for e in receipt.evidence)
    # the prohibited candidate gets zero value: no score recorded for it
    assert [cid for cid, _q, _v, _d in plan.candidate_scores] == ["p-clean"]


# ---------------- explicit unsafe flags ----------------

@pytest.mark.parametrize("flag,reason", [
    ("lawful", "LAW"), ("rights_safe", "RIGHTS"),
    ("privacy_safe", "PRIVACY"), ("safety_safe", "SAFETY"),
])
def test_explicit_unsafe_flag_is_refused(flag, reason):
    plan, receipt = ap.plan_action(_authority(), [_candidate(**{flag: False})],
                                  _profile(), now=NOW)
    assert plan is None
    assert receipt.phase == "PLAN_REFUSED"
    assert ap.PLAN_SAFETY_PROHIBITED in receipt.codes
    assert any(reason in e for e in receipt.evidence)


def test_explicit_law_false_never_reaches_execute():
    plan, _receipt = ap.plan_action(_authority(), [_candidate(lawful=False)],
                                    _profile(), now=NOW)
    # refusal happens in PLAN; there is no plan to hand to execute_plan,
    # so the executor can never be invoked on a prohibited candidate
    assert plan is None


# ---------------- tail risk ----------------

def test_tail_risk_candidate_is_refused():
    plan, receipt = ap.plan_action(
        _authority(),
        [_candidate(tails=(TailRisk(severity=9.5, probability=0.5),))],
        _profile(), now=NOW)
    assert plan is None
    assert ap.PLAN_SAFETY_PROHIBITED in receipt.codes
    assert any("TAIL_RISK" in e for e in receipt.evidence)


def test_high_q_tail_risk_cannot_win():
    harmful = _perfect_q("p-tail", tails=(TailRisk(severity=9.9, probability=0.9),))
    clean = _candidate("p-clean")
    plan, receipt = ap.plan_action(_authority(), [harmful, clean],
                                  _profile(), now=NOW)
    assert plan is not None
    assert plan.chosen.candidate_id == "p-clean"


# ---------------- distributional harm ----------------

def test_distributional_harm_is_refused():
    plan, receipt = ap.plan_action(
        _authority(),
        [_candidate(stakeholder_harms={"users": 9.5})],
        _profile(), now=NOW)
    assert plan is None
    assert ap.PLAN_SAFETY_PROHIBITED in receipt.codes
    assert any("DISTRIBUTIONAL_HARM" in e for e in receipt.evidence)


def test_high_q_distributional_harm_cannot_win():
    harmful = _perfect_q("p-harm", stakeholder_harms={"users": 9.9})
    clean = _candidate("p-clean")
    plan, receipt = ap.plan_action(_authority(), [harmful, clean],
                                  _profile(), now=NOW)
    assert plan is not None
    assert plan.chosen.candidate_id == "p-clean"


# ---------------- evidence + regression ----------------

def test_all_prohibited_refusal_names_every_candidate():
    plan, receipt = ap.plan_action(
        _authority(),
        [_candidate("p-a", hard_violation=True),
         _candidate("p-b", safety_safe=False)],
        _profile(), now=NOW)
    assert plan is None
    assert ap.PLAN_SAFETY_PROHIBITED in receipt.codes
    joined = " ".join(receipt.evidence)
    assert "p-a" in joined and "p-b" in joined
    assert "nothing admissible" in joined


def test_clean_candidates_select_by_value():
    """Regression: clean candidates are unaffected by the gate —
    selection runs on canonical value, scores still recorded."""
    weak = _candidate("p-weak",
                      quality={d: 9.1 for d in ALL_DIMS},
                      benefit=2.0, harm=0.5, cost=0.5, risk=0.2)
    strong = _candidate("p-strong",
                        quality={d: 9.5 for d in ALL_DIMS},
                        benefit=6.0, harm=1.0, cost=1.0, risk=0.5)
    plan, receipt = ap.plan_action(_authority(), [weak, strong],
                                  _profile(), now=NOW)
    assert plan is not None
    assert receipt.phase == "PLAN_ACCEPTED"
    assert plan.chosen.candidate_id == "p-strong"
    assert len(plan.candidate_scores) == 2
    assert not any("EXCLUDED" in e for e in receipt.evidence)


def test_plan_candidate_safety_defaults_are_clean():
    # Dataclass-level defaults (not the test helper's): unset safety flags
    # default to None = unknown, which the gate now fail-closed refuses.
    c = ap.PlanCandidate(
        candidate_id="p-defaults", action="naya_node_apply",
        description="defaults probe",
        quality={"objective_fit": 8.0}, confidence={"objective_fit": 0.9},
        reversibility="REVERSIBLE", expected_outcome="x",
        proof_requirements=("execution_receipt",),
    )
    assert c.hard_violation is False
    assert c.lawful is None and c.rights_safe is None
    assert c.privacy_safe is None and c.safety_safe is None
    assert c.tails == ()
    assert c.stakeholder_harms == {}
