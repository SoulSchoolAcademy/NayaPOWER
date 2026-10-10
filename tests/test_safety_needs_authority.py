"""Fail-closed falsifiers for NEEDS_AUTHORITY verdicts at the ACT seam.

The hole: NEEDS_AUTHORITY verdicts were silently absorbed into "admissible"
at both seams. Concretely, an IRREVERSIBLE (or UNKNOWN-reversibility) plan —
which the calculus verdicts NEEDS_AUTHORITY / CONSEQUENTIAL_OR_IRREVERSIBLE
because the seam cannot observe human authorization — was selected and
executed on a bare LAW grant. The calculus's own contract says such
candidates can never auto-act (can_auto requires reversible + low stakes);
the boot contract says destructive/irreversible risk is not tradeable and
requires ASK. The seam cannot ASK, so it must REFUSE.

The fix:
- _candidate_to_calculus maps authorized=True (both seams only run with a
  bound, scope-verified, time-valid LawAuthority — that grant IS the
  authority the calculus channel demands), retiring the meaningless
  always-on AUTHORITY_MISSING verdict.
- plan_action refuses the whole plan with PLAN_SAFETY_NEEDS_AUTHORITY when
  any candidate verdicts NEEDS_AUTHORITY (fail-closed; never silently
  narrowed). execute_plan's re-gate does the same before the executor fires.
- NEEDS_EVIDENCE reasons are recorded in receipt evidence (quality gates,
  not harm — they do not block).
"""
from kernel import act_pipeline as ap
from kernel.value_calculus import (
    QualityProfile,
    RiskPolicy,
    gate_candidate,
    NEEDS_AUTHORITY,
)

NOW = 1_790_000_000.0  # fixed clock for deterministic tests


def _profile():
    return QualityProfile(profile_id="safety-needs-auth-test", version="1",
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
    authority = _authority(decided_at=now - 60)
    return ap.ActionPlan(plan_id="hand-1", action=authority.action,
                         chosen=candidate, authority=authority,
                         candidate_scores=(), planned_at=now)


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


def test_authority_channel_is_honest():
    # The bound LAW grant IS the authority the calculus channel demands:
    # a clean reversible candidate must no longer verdict AUTHORITY_MISSING.
    gate, reasons, _q = gate_candidate(
        ap._candidate_to_calculus(_candidate()), _profile(), RiskPolicy())
    assert not (gate == NEEDS_AUTHORITY and "AUTHORITY_MISSING" in reasons), \
        f"unmapped authority channel: {gate} {reasons}"


def test_irreversible_plan_refused_at_plan_time():
    plan, receipt = ap.plan_action(
        _authority(), [_candidate(reversibility="IRREVERSIBLE")],
        _profile(), now=NOW)
    assert plan is None
    assert receipt.phase == "PLAN_REFUSED"
    assert ap.PLAN_SAFETY_NEEDS_AUTHORITY in receipt.codes
    assert any("CONSEQUENTIAL_OR_IRREVERSIBLE" in e for e in receipt.evidence)


def test_unknown_reversibility_plan_refused_at_plan_time():
    # UNKNOWN reversibility cannot satisfy the calculus's reversibility
    # precondition for auto-action — fail closed, not fail open.
    plan, receipt = ap.plan_action(
        _authority(), [_candidate(reversibility="UNKNOWN")],
        _profile(), now=NOW)
    assert plan is None
    assert ap.PLAN_SAFETY_NEEDS_AUTHORITY in receipt.codes


def test_mixed_plan_refused_not_silently_narrowed():
    # One NEEDS_AUTHORITY candidate refuses the whole plan — the seam must
    # not silently drop it and auto-execute the "safe" alternative.
    plan, receipt = ap.plan_action(
        _authority(),
        [_candidate("safe", reversibility="REVERSIBLE"),
         _candidate("risky", reversibility="IRREVERSIBLE")],
        _profile(), now=NOW)
    assert plan is None
    assert ap.PLAN_SAFETY_NEEDS_AUTHORITY in receipt.codes
    assert any("risky" in e for e in receipt.evidence)


def test_irreversible_hand_plan_refused_at_execute_time():
    # The bypass path: hand-crafted plan carrying an IRREVERSIBLE candidate.
    receipt, calls = _execute(_hand_plan(_candidate(reversibility="IRREVERSIBLE")))
    assert receipt.phase == "EXECUTION_REFUSED"
    assert ap.PLAN_SAFETY_NEEDS_AUTHORITY in receipt.codes
    assert calls == [], "executor must never fire on a NEEDS_AUTHORITY plan"


def test_reversible_clean_plan_still_executes():
    # Regression: the fail-closed change must not block ordinary plans.
    plan, plan_receipt = ap.plan_action(
        _authority(), [_candidate()], _profile(), now=NOW)
    assert plan is not None and plan_receipt.phase == "PLAN_ACCEPTED"
    receipt, calls = _execute(plan)
    assert receipt.phase == "EXECUTION_COMPLETED"
    assert receipt.executed is True
    assert len(calls) == 1


def test_needs_evidence_reasons_are_recorded():
    # Unknown safety flags (None) are quality-gate concerns, not harm:
    # they do not block, but their reasons must appear in the evidence.
    plan, receipt = ap.plan_action(
        _authority(), [_candidate()], _profile(), now=NOW)
    assert plan is not None
    assert any("NEEDS_EVIDENCE" in e for e in receipt.evidence)
