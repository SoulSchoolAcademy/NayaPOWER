"""Fail-closed falsifiers for the ACT seam's risk-policy threading.

The hole: plan_action gated candidates under one RiskPolicy, but the
ActionPlan carried no record of it. execute_plan re-gated under whatever
policy the caller passed (or a fresh default) — the docstring asked for
"the same math", but nothing enforced it. A laxer execute-time policy
could flip a PROHIBITED verdict on a hand-crafted plan, and even a plan
produced by plan_action was re-gated under possibly different math.

The fix: plan_action records the effective plan-time risk policy on the
ActionPlan. execute_plan defaults to that recorded policy when the caller
passes None (re-verification under the SAME math), accepts an explicitly
equal policy, and fails closed with PLAN_RISK_POLICY_MISMATCH on any
explicit mismatch — the executor never fires when the math moved.
Hand-crafted plans (risk_policy=None on the plan) keep today's behavior:
the re-gate runs under the caller's policy or the default.
"""
import pytest

from kernel import act_pipeline as ap
from kernel.value_calculus import QualityProfile, RiskPolicy, TailRisk

NOW = 1_790_000_000.0  # fixed clock for deterministic tests


def _profile():
    return QualityProfile(profile_id="safety-risk-policy-test", version="1",
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


STRICT = RiskPolicy(severity_threshold=5.0, probability_threshold=0.001,
                    response="PROHIBITED", max_stakeholder_harm=5.0)
LAX = RiskPolicy(severity_threshold=9.9, probability_threshold=0.9,
                 response="PROHIBITED", max_stakeholder_harm=9.9)
DEFAULT = RiskPolicy()


def _plan(policy=None):
    kw = {}
    if policy is not None:
        kw["risk_policy"] = policy
    plan, receipt = ap.plan_action(_authority(), [_candidate()],
                                   _profile(), now=NOW, **kw)
    assert plan is not None, f"planning refused: {receipt.codes}"
    assert receipt.phase == "PLAN_ACCEPTED"
    return plan


def _execute(plan, risk_policy=...):
    """risk_policy=... means: omit the kwarg (caller passes nothing)."""
    calls = []
    kwargs = dict(executor=lambda p: calls.append(p) or "done",
                  re_resolve=lambda: _authority(decided_at=NOW - 30),
                  now=NOW, profile=_profile())
    if risk_policy is not ...:
        kwargs["risk_policy"] = risk_policy
    receipt = ap.execute_plan(plan, **kwargs)
    return receipt, calls


# ---------------- the plan records its math ----------------

def test_plan_records_explicit_plan_time_risk_policy():
    plan = _plan(STRICT)
    assert plan.risk_policy == STRICT


def test_plan_records_default_policy_when_caller_passes_none():
    plan = _plan()
    assert plan.risk_policy == DEFAULT


# ---------------- execute re-verifies under the SAME math ----------------

def test_execute_defaults_to_plan_time_policy():
    # Strict policy recorded at plan time must govern the re-gate even
    # when the caller passes nothing. The tail (6.0, 0.05) is PROHIBITED
    # under STRICT but admissible under DEFAULT — so a strict-recorded
    # plan must refuse it here, not sail through on the default.
    tails = (TailRisk(severity=6.0, probability=0.05, harm_class="test"),)
    plan, receipt = ap.plan_action(_authority(), [_candidate(tails=tails)],
                                   _profile(), now=NOW)
    # Sanity: admissible under the default plan-time policy.
    assert plan is not None and receipt.phase == "PLAN_ACCEPTED"
    # Simulate: plan was governed by STRICT math (hand-crafted equivalent
    # carrying the strict record), then executed with no policy passed.
    hand = ap.ActionPlan(plan_id="hand-strict", action=plan.action,
                         chosen=plan.chosen, authority=plan.authority,
                         candidate_scores=(), planned_at=NOW,
                         risk_policy=STRICT)
    receipt, calls = _execute(hand)  # caller passes nothing
    assert receipt.phase == "EXECUTION_REFUSED"
    assert ap.PLAN_SAFETY_PROHIBITED in receipt.codes
    assert calls == [], "executor must never fire under prohibited math"


def test_execute_with_equal_policy_uses_it():
    plan = _plan(STRICT)
    # Equal by value, not identical object — must be accepted.
    same = RiskPolicy(severity_threshold=5.0, probability_threshold=0.001,
                      response="PROHIBITED", max_stakeholder_harm=5.0)
    receipt, calls = _execute(plan, risk_policy=same)
    assert receipt.phase == "EXECUTION_COMPLETED"
    assert receipt.executed is True
    assert calls != []


def test_execute_with_matching_policy_evidence_names_the_math():
    plan = _plan(STRICT)
    receipt, _ = _execute(plan)  # caller passes nothing -> plan policy
    assert receipt.phase == "EXECUTION_COMPLETED"
    assert any("5.0" in e or "severity_threshold" in e
               for e in receipt.evidence), \
        "receipt must name the policy math it re-gated under"


# ---------------- the seam fails closed when the math moves ----------------

def test_execute_with_mismatched_policy_refused():
    plan = _plan(STRICT)
    receipt, calls = _execute(plan, risk_policy=LAX)
    assert receipt.phase == "EXECUTION_REFUSED"
    assert ap.PLAN_RISK_POLICY_MISMATCH in receipt.codes
    assert calls == [], "executor must never fire when the policy moved"


def test_mismatch_refusal_is_structural_not_outcome_dependent():
    # The candidate is perfectly clean — the refusal is about the moved
    # math, not about this candidate. A changed policy mid-flight is a
    # re-plan, never a silent re-derivation.
    plan = _plan(STRICT)
    receipt, calls = _execute(plan, risk_policy=DEFAULT)
    assert receipt.phase == "EXECUTION_REFUSED"
    assert ap.PLAN_RISK_POLICY_MISMATCH in receipt.codes
    assert receipt.executed is False
    assert calls == []
    assert any("re-plan" in e.lower() or "mismatch" in e.lower()
               for e in receipt.evidence)


def test_mismatch_does_not_refuse_when_plan_policy_unknown():
    # Hand-crafted plan with risk_policy=None: no plan-time math to
    # preserve. Today's behavior holds — caller's policy (or default)
    # governs the re-gate.
    hand = ap.ActionPlan(plan_id="hand-none", action="naya_node_apply",
                         chosen=_candidate(), authority=_authority(),
                         candidate_scores=(), planned_at=NOW)
    receipt, calls = _execute(hand, risk_policy=LAX)
    assert receipt.phase == "EXECUTION_COMPLETED"
    assert receipt.executed is True
    assert calls != []


def test_mismatch_check_runs_before_the_executor_and_before_gate():
    # Ordering matters: policy-mismatch refusal must precede any executor
    # contact AND precede the do-no-harm re-gate result, so a mismatched
    # policy can never produce an execution-shaped receipt.
    plan = _plan(STRICT)
    receipt, calls = _execute(plan, risk_policy=LAX)
    assert calls == []
    assert receipt.phase == "EXECUTION_REFUSED"
    assert ap.PLAN_SAFETY_PROHIBITED not in receipt.codes
