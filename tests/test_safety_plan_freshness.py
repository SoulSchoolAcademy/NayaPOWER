"""Fail-closed falsifiers for plan freshness at the ACT execution seam.

The hole: execute_plan re-resolved live LAW authority before executing —
but never checked the plan's own age. The plan IS a decision, and SN-0493
says decisions expire when the tip moves: the plan's safety inputs
(candidate flags, tails, stakeholder harms) are captured at plan time,
and the execution-time do-no-harm re-gate re-verifies THOSE inputs. A
stale plan — or a hand-crafted plan with a backdated planned_at — smuggles
stale safety facts through the last-responsible-moment check.

The fix: execute_plan refuses plans older than MAX_PLAN_AGE_SECONDS
(and plans with missing, non-numeric, or future-dated planned_at) with
PLAN_STALE. The caller must re-plan; the executor never fires.
"""
import pytest

from kernel import act_pipeline as ap
from kernel.value_calculus import QualityProfile

NOW = 1_790_000_000.0  # fixed clock for deterministic tests


def _profile():
    return QualityProfile(profile_id="safety-plan-freshness", version="1",
                          objective="minimum sufficient action")


def _authority(**kw):
    base = dict(action="naya_node_apply", scope="naya_node_apply",
                decided_at=NOW - 60, expires_at=None, grant_id="grant-1")
    base.update(kw)
    return ap.LawAuthority(**base)


def _candidate(**kw):
    base = dict(
        candidate_id="x1",
        action="naya_node_apply",
        description="apply retained intelligence",
        quality={"objective_fit": 9.0, "evidence_sufficiency": 9.0,
                 "applicability": 9.0, "robustness": 9.0},
        confidence={"objective_fit": 0.9, "evidence_sufficiency": 0.9,
                    "applicability": 0.9, "robustness": 0.9},
        reversibility="REVERSIBLE",
        expected_outcome="node state updated",
        proof_requirements=("execution_receipt",),
        stakes="low",
    )
    base.update(kw)
    return ap.PlanCandidate(**base)


def _hand_plan(candidate, planned_at=NOW, decided_at=NOW - 60):
    """An ActionPlan built OUTSIDE plan_action — the bypass path."""
    authority = _authority(decided_at=decided_at)
    return ap.ActionPlan(plan_id="hand-fresh", action=authority.action,
                         chosen=candidate, authority=authority,
                         candidate_scores=(), planned_at=planned_at)


def _execute(plan, **kw):
    calls = []
    kwargs = dict(executor=lambda p: calls.append(p) or "done",
                  re_resolve=lambda: _authority(decided_at=NOW - 30),
                  now=NOW, profile=_profile())
    kwargs.update(kw)
    receipt = ap.execute_plan(plan, **kwargs)
    return receipt, calls


def _assert_refused_stale(receipt, calls):
    assert receipt.phase == "EXECUTION_REFUSED"
    assert receipt.executed is False
    assert ap.PLAN_STALE in receipt.codes
    assert calls == [], "executor must never fire on a stale plan"
    assert any("stale" in e.lower() for e in receipt.evidence)


# ---------------- falsifier battery: stale plans must never execute ----------------

def test_stale_plan_refused():
    plan = _hand_plan(_candidate(), planned_at=NOW - 3600)
    receipt, calls = _execute(plan)
    _assert_refused_stale(receipt, calls)
    assert any("3600" in e or "plan age" in e.lower() for e in receipt.evidence)


def test_stale_plan_refused_even_with_fresh_authority():
    # The authority re-resolution is fresh — but the PLAN is stale. The
    # plan's safety inputs are what the re-gate verifies, so staleness
    # must win over a fresh LAW read.
    plan = _hand_plan(_candidate(), planned_at=NOW - 3600)
    receipt, calls = _execute(plan)
    _assert_refused_stale(receipt, calls)
    assert ap.PLAN_STALE in receipt.codes


def test_missing_planned_at_refused_fail_closed():
    plan = _hand_plan(_candidate(), planned_at=None)
    receipt, calls = _execute(plan)
    _assert_refused_stale(receipt, calls)


def test_future_dated_planned_at_refused_fail_closed():
    plan = _hand_plan(_candidate(), planned_at=NOW + 60)
    receipt, calls = _execute(plan)
    _assert_refused_stale(receipt, calls)


def test_custom_plan_ttl_honored():
    plan = _hand_plan(_candidate(), planned_at=NOW - 120)
    receipt, calls = _execute(plan, max_plan_age_seconds=60)
    _assert_refused_stale(receipt, calls)
    plan2 = _hand_plan(_candidate(), planned_at=NOW - 30)
    receipt2, calls2 = _execute(plan2, max_plan_age_seconds=60)
    assert receipt2.phase == "EXECUTION_COMPLETED"
    assert receipt2.executed is True
    assert len(calls2) == 1


# ---------------- the gate must not block fresh plans ----------------

def test_boundary_age_still_executes():
    # Mirrors the LAW staleness semantics: stale only when age > TTL.
    plan = _hand_plan(_candidate(), planned_at=NOW - 900)
    receipt, calls = _execute(plan)
    assert receipt.phase == "EXECUTION_COMPLETED"
    assert receipt.executed is True
    assert len(calls) == 1


def test_fresh_planned_plan_still_executes():
    authority = _authority()
    plan, plan_receipt = ap.plan_action(authority, [_candidate()], _profile(), now=NOW)
    assert plan is not None and plan_receipt.phase == "PLAN_ACCEPTED"
    receipt, calls = _execute(plan)
    assert receipt.phase == "EXECUTION_COMPLETED"
    assert receipt.executed is True
    assert len(calls) == 1
    assert ap.PLAN_STALE not in receipt.codes
