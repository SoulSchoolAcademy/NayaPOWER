"""Fail-closed falsifiers for the ACT seam's consent enforcement.

The hole: the LAW grant binds to the action TEXT, but irreversibility is a
property of the plan candidate — decided at plan time, AFTER the grant. No
grant-time check on the action text can cover it, and the calculus's
CONSEQUENTIAL_OR_IRREVERSIBLE human-consent gate was unreachable at this
seam (the mapping drops consent fields; NEEDS_AUTHORITY is deferred to
LAW). Net: an IRREVERSIBLE plan executed under any valid grant for the
action string, with zero human-consent evidence anywhere in the seam.

The fix: LawAuthority carries human_authorized (fail-closed default False).
plan_action refuses non-REVERSIBLE chosen candidates without recorded human
consent (PLAN_CONSENT_MISSING); execute_plan re-verifies the consent
dimension against the LIVE re-resolved grant at the last responsible
moment — consent may have been revoked since plan time, or the plan
hand-crafted. The executor never fires on an irreversible plan without live
human consent. Reversible plans need no consent evidence.
"""
import pytest

from kernel import act_pipeline as ap
from kernel.value_calculus import QualityProfile

NOW = 1_790_000_000.0  # fixed clock for deterministic tests


def _profile():
    return QualityProfile(profile_id="safety-consent-test", version="1",
                          objective="consent seam enforcement")


def _authority(**kw):
    base = dict(action="naya_node_apply", scope="naya_node_apply",
                decided_at=NOW - 60, expires_at=None, grant_id="grant-1")
    base.update(kw)
    return ap.LawAuthority(**base)


def _candidate(cid="c1", **kw):
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


def _hand_plan(candidate, now=NOW, authority=None):
    """An ActionPlan built OUTSIDE plan_action — the bypass path."""
    auth = authority or _authority(decided_at=now - 60)
    return ap.ActionPlan(plan_id="hand-1", action=auth.action,
                         chosen=candidate, authority=auth,
                         candidate_scores=(), planned_at=now)


def _execute(plan, fresh_authority, profile=None):
    calls = []
    receipt = ap.execute_plan(
        plan,
        executor=lambda p: calls.append(p) or "done",
        re_resolve=lambda: fresh_authority,
        now=NOW,
        profile=profile or _profile(),
    )
    return receipt, calls


def _assert_plan_refused(plan, receipt, code):
    assert plan is None
    assert receipt.phase == "PLAN_REFUSED"
    assert code in receipt.codes
    assert any("consent" in e.lower() for e in receipt.evidence)


def _assert_execution_refused(receipt, calls, code):
    assert receipt.phase == "EXECUTION_REFUSED"
    assert receipt.executed is False
    assert code in receipt.codes
    assert calls == [], "executor must never fire on a refused plan"
    assert any("consent" in e.lower() for e in receipt.evidence)


# ---------------- plan-time falsifiers ----------------

def test_plan_action_irreversible_without_consent_refused():
    # The hole: this sailed through on a grant cleared for the action text.
    plan, receipt = ap.plan_action(
        _authority(), (_candidate(reversibility="IRREVERSIBLE"),),
        _profile(), now=NOW)
    _assert_plan_refused(plan, receipt, ap.PLAN_CONSENT_MISSING)


def test_plan_action_unknown_reversibility_without_consent_refused():
    # UNKNOWN reversibility fails closed — consent is required, not assumed.
    plan, receipt = ap.plan_action(
        _authority(), (_candidate(reversibility="UNKNOWN"),),
        _profile(), now=NOW)
    _assert_plan_refused(plan, receipt, ap.PLAN_CONSENT_MISSING)


def test_plan_action_irreversible_with_consent_accepted():
    plan, receipt = ap.plan_action(
        _authority(human_authorized=True),
        (_candidate(reversibility="IRREVERSIBLE"),),
        _profile(), now=NOW)
    assert plan is not None
    assert receipt.phase == "PLAN_ACCEPTED"


def test_plan_action_reversible_without_consent_accepted():
    # Reversible plans need no consent evidence — the grant alone suffices.
    plan, receipt = ap.plan_action(
        _authority(), (_candidate(reversibility="REVERSIBLE"),),
        _profile(), now=NOW)
    assert plan is not None
    assert receipt.phase == "PLAN_ACCEPTED"


# ---------------- execute-time falsifiers (last responsible moment) ----------------

def test_execute_plan_consent_revoked_between_plan_and_execute_refused():
    # Consent was recorded at plan time but the LIVE grant no longer carries
    # it — execution must fail closed on the fresh authority.
    plan = _hand_plan(_candidate(reversibility="IRREVERSIBLE"),
                      authority=_authority(human_authorized=True))
    fresh = _authority(decided_at=NOW - 30)  # consent gone
    receipt, calls = _execute(plan, fresh)
    _assert_execution_refused(receipt, calls, ap.PLAN_CONSENT_MISSING)


def test_execute_plan_handcrafted_irreversible_no_consent_refused():
    # A hand-crafted plan bypasses plan_action entirely — the execute-time
    # re-check is the only thing standing between it and the executor.
    plan = _hand_plan(_candidate(reversibility="IRREVERSIBLE"))
    fresh = _authority(decided_at=NOW - 30)
    receipt, calls = _execute(plan, fresh)
    _assert_execution_refused(receipt, calls, ap.PLAN_CONSENT_MISSING)


def test_execute_plan_irreversible_with_live_consent_executes():
    plan = _hand_plan(_candidate(reversibility="IRREVERSIBLE"))
    fresh = _authority(decided_at=NOW - 30, human_authorized=True)
    receipt, calls = _execute(plan, fresh)
    assert receipt.phase == "EXECUTION_COMPLETED"
    assert receipt.executed is True
    assert len(calls) == 1


def test_execute_plan_reversible_without_consent_executes():
    plan = _hand_plan(_candidate(reversibility="REVERSIBLE"))
    fresh = _authority(decided_at=NOW - 30)
    receipt, calls = _execute(plan, fresh)
    assert receipt.phase == "EXECUTION_COMPLETED"
    assert len(calls) == 1
