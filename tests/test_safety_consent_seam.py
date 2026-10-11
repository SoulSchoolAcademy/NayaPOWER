"""Fail-closed falsifiers for the ACT seam's execute-time consent re-verification.

The hole: the LAW grant binds to the action TEXT, but irreversibility is a
property of the plan candidate. Plan-time selection is owned by the merged
decision-principle engine (an IRREVERSIBLE or UNKNOWN-reversibility winner
yields decision==ASK and is refused with PLAN_NEEDS_HUMAN_JUDGMENT) — but a
plan built OUTSIDE plan_action (hand-crafted) never passes that gate, and
consent recorded at plan time may be revoked before execution. Nothing in
the merged tree verifies consent against the LIVE re-resolved grant at the
last responsible moment.

The fix: LawAuthority carries human_authorized (fail-closed default False).
execute_plan re-verifies the consent dimension against the fresh grant: a
non-REVERSIBLE chosen candidate without live human consent is refused with
PLAN_CONSENT_MISSING; the executor never fires. Reversible plans need no
consent evidence.

RED-to-GREEN: run these against the pristine merged tree and the three
hand-crafted / revoked falsifiers FAIL (the executor fires on an
irreversible plan with zero consent evidence); with this seam all pass.
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
    # Fixture matches the current gate vocabulary (post-#2273, post-#2380):
    # 7 quality dims, 7 confidences, 4 safety flags True, value evidence.
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
        lawful=True,
        rights_safe=True,
        privacy_safe=True,
        safety_safe=True,
        value_benefit=8.0,
        value_harm=1.0,
        value_cost=1.0,
        value_risk=0.5,
        value_confidence={"B": 0.9, "H": 0.9, "C": 0.9, "R": 0.9},
        value_evidence_count=3,
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


def _assert_execution_refused(receipt, calls, code):
    assert receipt.phase == "EXECUTION_REFUSED"
    assert receipt.executed is False
    assert code in receipt.codes
    assert calls == [], "executor must never fire on a refused plan"
    assert any("consent" in e.lower() for e in receipt.evidence)


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
    # A hand-crafted plan bypasses plan_action (and its ASK gate) entirely —
    # the execute-time consent re-check is the only thing standing between
    # it and the executor.
    plan = _hand_plan(_candidate(reversibility="IRREVERSIBLE"))
    fresh = _authority(decided_at=NOW - 30)
    receipt, calls = _execute(plan, fresh)
    _assert_execution_refused(receipt, calls, ap.PLAN_CONSENT_MISSING)


def test_execute_plan_handcrafted_unknown_reversibility_no_consent_refused():
    # UNKNOWN reversibility fails closed at the seam — consent required, not
    # assumed.
    plan = _hand_plan(_candidate(reversibility="UNKNOWN"))
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
    # Reversible plans need no consent evidence — the grant alone suffices.
    plan = _hand_plan(_candidate(reversibility="REVERSIBLE"))
    fresh = _authority(decided_at=NOW - 30)
    receipt, calls = _execute(plan, fresh)
    assert receipt.phase == "EXECUTION_COMPLETED"
    assert receipt.executed is True
    assert len(calls) == 1
