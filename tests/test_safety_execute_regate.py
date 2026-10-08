"""Fail-closed falsifiers for the ACT execution seam's do-no-harm re-gate.

The hole: execute_plan trusted plan.chosen without ever consulting the
calculus's gate_candidate. A hand-crafted ActionPlan (built outside
plan_action) carrying a PROHIBITED candidate sailed through LAW
re-resolution straight into the executor.

The fix: execute_plan re-runs gate_candidate on plan.chosen at the last
responsible moment — immediately before the executor fires. PROHIBITED is
refused with PLAN_SAFETY_PROHIBITED; the executor never runs.
NEEDS_AUTHORITY verdicts stay governed by the LAW authority record.
"""
import pytest

from kernel import act_pipeline as ap
from kernel.value_calculus import QualityProfile, RiskPolicy, TailRisk

NOW = 1_790_000_000.0  # fixed clock for deterministic tests


def _profile():
    return QualityProfile(profile_id="safety-execute-test", version="1",
                          objective="minimum sufficient action")


def _authority(**kw):
    base = dict(action="naya_node_apply", scope="naya_node_apply",
                decided_at=NOW - 60, expires_at=None, grant_id="grant-1")
    base.update(kw)
    return ap.LawAuthority(**base)


def _candidate(cid="x1", **kw):
    base = dict(
        candidate_id=cid,
        action="naya_node_apply",
        description="apply retained intelligence",
        quality={"objective_fit": 9.9, "evidence_sufficiency": 9.9,
                 "applicability": 9.9, "robustness": 9.9},
        confidence={"objective_fit": 0.99, "evidence_sufficiency": 0.99,
                    "applicability": 0.99, "robustness": 0.99},
        reversibility="REVERSIBLE",
        expected_outcome="node state updated",
        proof_requirements=("execution_receipt",),
        stakes="low",
    )
    base.update(kw)
    return ap.PlanCandidate(**base)


def _hand_plan(candidate, now=NOW):
    """An ActionPlan built OUTSIDE plan_action — the bypass path."""
    authority = _authority(decided_at=now - 60)
    return ap.ActionPlan(plan_id="hand-1", action=authority.action,
                         chosen=candidate, authority=authority,
                         candidate_scores=(), planned_at=now)


def _execute(plan, profile=None, risk_policy=None):
    calls = []
    kwargs = dict(executor=lambda p: calls.append(p) or "done",
                  re_resolve=lambda: _authority(decided_at=NOW - 30),
                  now=NOW, profile=profile or _profile())
    if risk_policy is not None:
        kwargs["risk_policy"] = risk_policy
    receipt = ap.execute_plan(plan, **kwargs)
    return receipt, calls


def _assert_refused(receipt, calls, code):
    assert receipt.phase == "EXECUTION_REFUSED"
    assert receipt.executed is False
    assert code in receipt.codes
    assert calls == [], "executor must never fire on a refused plan"
    assert any("re-gate" in e for e in receipt.evidence)


# ---------------- falsifier battery: PROHIBITED must never execute ----------------

def test_handcrafted_hard_violation_refused():
    plan = _hand_plan(_candidate(hard_violation=True))
    receipt, calls = _execute(plan)
    _assert_refused(receipt, calls, ap.PLAN_SAFETY_PROHIBITED)
    assert any("JUDGMENT_RULE_HARD_STOP" in e for e in receipt.evidence)


def test_handcrafted_explicit_unsafe_flag_refused():
    plan = _hand_plan(_candidate(safety_safe=False))
    receipt, calls = _execute(plan)
    _assert_refused(receipt, calls, ap.PLAN_SAFETY_PROHIBITED)
    assert any("SAFETY" in e for e in receipt.evidence)


def test_handcrafted_tail_risk_refused():
    tails = (TailRisk(severity=9.5, probability=0.5, harm_class="test"),)
    plan = _hand_plan(_candidate(tails=tails))
    receipt, calls = _execute(plan)
    _assert_refused(receipt, calls, ap.PLAN_SAFETY_PROHIBITED)
    assert any("TAIL_RISK" in e for e in receipt.evidence)


def test_handcrafted_distributional_harm_refused():
    plan = _hand_plan(_candidate(stakeholder_harms={"community": 9.5}))
    receipt, calls = _execute(plan)
    _assert_refused(receipt, calls, ap.PLAN_SAFETY_PROHIBITED)
    assert any("DISTRIBUTIONAL_HARM" in e for e in receipt.evidence)


def test_near_perfect_q_harmful_candidate_cannot_win_by_quality():
    # Even with Q≈10, the harm hard stop wins. Zero value for harmful actions.
    tails = (TailRisk(severity=9.9, probability=0.9, harm_class="test"),)
    plan = _hand_plan(_candidate(hard_violation=True, tails=tails,
                                 stakeholder_harms={"all": 9.9}))
    receipt, calls = _execute(plan)
    _assert_refused(receipt, calls, ap.PLAN_SAFETY_PROHIBITED)


# ---------------- the gate must not block what LAW allows ----------------

def test_planned_clean_candidate_still_executes():
    authority = _authority()
    plan, plan_receipt = ap.plan_action(authority, [_candidate()], _profile(), now=NOW)
    assert plan is not None and plan_receipt.phase == "PLAN_ACCEPTED"
    receipt, calls = _execute(plan)
    assert receipt.phase == "EXECUTION_COMPLETED"
    assert receipt.executed is True
    assert len(calls) == 1
    assert any("re-gate" in e for e in receipt.evidence)


def test_needs_authority_verdict_still_executes():
    # A clean hand-crafted plan gates NEEDS_AUTHORITY (AUTHORITY_MISSING on
    # the calculus Candidate) — LAW re-resolution governs authority, not the
    # safety seam, so execution proceeds.
    plan = _hand_plan(_candidate())
    receipt, calls = _execute(plan)
    assert receipt.phase == "EXECUTION_COMPLETED"
    assert receipt.executed is True
    assert len(calls) == 1
    assert any("NEEDS_AUTHORITY" in e for e in receipt.evidence)


def test_custom_risk_policy_is_honored():
    # A tail below a custom policy's thresholds is not prohibited.
    tails = (TailRisk(severity=9.5, probability=0.5, harm_class="test"),)
    plan = _hand_plan(_candidate(tails=tails))
    receipt, calls = _execute(plan, risk_policy=RiskPolicy(severity_threshold=10.0))
    assert receipt.phase == "EXECUTION_COMPLETED"
    assert receipt.executed is True


def test_law_refusals_still_take_law_codes():
    # LAW-seam refusals keep their own codes and precede the safety re-gate:
    # a stale authority refuses on LAW grounds even for a clean candidate.
    plan = _hand_plan(_candidate())
    calls = []
    receipt = ap.execute_plan(
        plan, executor=lambda p: calls.append(p) or "done",
        re_resolve=lambda: _authority(decided_at=NOW - 3600),  # stale
        now=NOW, profile=_profile())
    assert receipt.phase == "EXECUTION_REFUSED"
    assert "LAW_AUTHORITY_STALE" in receipt.codes
    assert ap.PLAN_SAFETY_PROHIBITED not in receipt.codes
    assert calls == []
