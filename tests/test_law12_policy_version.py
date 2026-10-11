"""Law 12 P10 + trust-boundary fixes (verify why-not-10, 2026-10-11).

P10: the policy/law version bound into Law 12 proofs must be REAL, not the
literal "CURRENT". "CURRENT" can never change, so a proof bound to it could
never expire on a law change — the binding existed in schema but was inert
in the pipeline. Now every pipeline seam binds LAW_POLICY_VERSION (the
Twelve Laws pin); a law change invalidates outstanding proofs.

Trust boundary: a hand-crafted plan with law12_proof=None SKIPS the Law 12
revalidation (documented, intentional back-compat) but NEVER skips the
Law 11 execution-door re-gate or the execution-time do-no-harm re-gate.
plan_action ALWAYS issues a proof, so the None path only exists for
externally-constructed plans, whose constructors own staleness.

Negative controls: the P10 seam tests FAIL if the "CURRENT" pins are
restored (sabotage battery); the trust-boundary tests pin the documented
behavior so a future change is a conscious decision, not drift.
"""
import pytest

from kernel import act_pipeline as ap
from kernel.protocol.law_enforcement import evaluate
from kernel.protocol.proof_receipt import (
    LAW_POLICY_VERSION,
    UNBOUND,
    ProofContext,
    check_proof_validity,
    issue_proof_receipt,
)
from kernel.protocol.typed_action import TypedAction
from kernel.value_calculus import QualityProfile

NOW = 1_790_000_000.0
OLD_LAW_VERSION = "2026-10-01-old-laws"  # a superseded governing revision


def _profile():
    return QualityProfile(profile_id="law12-p10-test", version="1",
                          objective="minimum sufficient action")


def _authority(**kw):
    base = dict(action="naya_node_apply", scope="naya_node_apply",
                decided_at=NOW - 60, expires_at=None, grant_id="grant-1")
    base.update(kw)
    return ap.LawAuthority(**base)


def _candidate(cid="p1", **kw):
    base = dict(
        candidate_id=cid,
        action="naya_node_apply",
        description="apply retained intelligence",
        quality={d: 9.0 for d in ("objective_fit", "evidence_sufficiency",
                                  "applicability", "robustness",
                                  "reversibility", "blast_containment",
                                  "simplicity")},
        confidence={d: 0.9 for d in ("objective_fit", "evidence_sufficiency",
                                    "applicability", "robustness",
                                    "reversibility", "blast_containment",
                                    "simplicity")},
        reversibility="REVERSIBLE",
        expected_outcome="done",
        proof_requirements=("receipt",),
        stakes="low",
        lawful=True,
        rights_safe=True,
        privacy_safe=True,
        safety_safe=True,
        value_benefit=8.0, value_harm=1.0, value_cost=1.0, value_risk=0.5,
        value_confidence={"B": 0.9, "H": 0.9, "C": 0.9, "R": 0.9},
        value_evidence_count=3,
    )
    base.update(kw)
    return ap.PlanCandidate(**base)


def _plan(**kw):
    plan, receipt = ap.plan_action(
        _authority(), [_candidate()], _profile(), now=NOW,
        source_sha="sha-aaa", resource_state_digest="rs-1", **kw)
    assert plan is not None, f"plan refused: {receipt.evidence}"
    return plan


def _execute(plan, now=NOW, source_sha="sha-aaa",
             resource_state_digest="rs-1", calls=None, authority=None):
    calls = calls if calls is not None else []
    auth = authority or _authority(decided_at=now - 60)
    receipt = ap.execute_plan(
        plan,
        executor=lambda p: calls.append(p.plan_id) or "ok",
        re_resolve=lambda: auth,
        now=now,
        profile=_profile(),
        source_sha=source_sha,
        resource_state_digest=resource_state_digest,
    )
    return receipt, calls


# --- P10: the real version is bound at every pipeline seam ---

def test_plan_binds_real_law_policy_version():
    plan = _plan()
    assert plan.law12_proof is not None
    assert plan.law12_proof.policy_version == LAW_POLICY_VERSION
    assert plan.law12_proof.policy_version != "CURRENT"


def test_typed_action_mapping_binds_real_version():
    typed = ap._candidate_to_typed_action(_candidate(), _authority())
    assert typed.policy_version == LAW_POLICY_VERSION


def test_typed_action_default_is_real_version():
    a = TypedAction(actor_id="t", operation="read", environment="development",
                    resource="r")
    assert a.policy_version == LAW_POLICY_VERSION


def test_evaluate_defaults_to_real_policy_version():
    from kernel.protocol.law_enforcement import EnforcementContext
    ctx = EnforcementContext(actor_id="t", source_sha="s", now=NOW,
                             proof_ttl_seconds=900, scope="r",
                             current_authority_ref="g",
                             current_resource="r")
    action = TypedAction(actor_id="t", operation="read",
                         environment="development", resource="r",
                         authority_ref="g", rights_safe=True,
                         safety_safe=True, privacy_safe=True,
                         consent_obtained=True)
    d = evaluate(ctx, action)
    assert d.proof.policy_version == LAW_POLICY_VERSION


def test_policy_change_invalidates_old_proof():
    # The Law 12 promise, end to end: a proof earned under a superseded
    # governing revision is refused once the law moves — even when the
    # SHA, resource state, scope and window all still hold.
    old_proof = issue_proof_receipt(
        actor_id="naya-2", operation="write", environment="development",
        resource="smart_notes", law_verdict="ADMISSIBLE", reason_ids=(),
        policy_version=OLD_LAW_VERSION, policy_hash=UNBOUND,
        source_sha="sha-aaa", resource_state_digest="rs-1",
        scope="smart_notes", evidence_ids=("ev-1",),
        issued_at=NOW, valid_until=NOW + 900)
    fresh_ctx = ProofContext(
        source_sha="sha-aaa", policy_version=LAW_POLICY_VERSION,
        policy_hash=UNBOUND, resource_state_digest="rs-1",
        scope="smart_notes", now=NOW + 10, revoked_refs=())
    valid, event = check_proof_validity(old_proof, fresh_ctx)
    assert not valid
    assert event == "POLICY_VERSION_CHANGED"


def test_same_policy_version_still_valid():
    plan = _plan()
    fresh_ctx = ProofContext(
        source_sha="sha-aaa", policy_version=LAW_POLICY_VERSION,
        policy_hash=UNBOUND, resource_state_digest="rs-1",
        scope="naya_node_apply", now=NOW + 10, revoked_refs=())
    valid, _ = check_proof_validity(plan.law12_proof, fresh_ctx)
    assert valid


def test_execute_refuses_plan_from_superseded_law():
    # Hand-crafted plan carrying a proof issued under the old law revision:
    # execute_plan must refuse with PLAN_PROOF_STALE even though the
    # Law 11 door would pass (safe candidate, fresh authority).
    plan = _plan()
    old_proof = issue_proof_receipt(
        actor_id="naya-2", operation=plan.law12_proof.operation,
        environment="development", resource="naya_node_apply",
        law_verdict="ADMISSIBLE", reason_ids=(),
        policy_version=OLD_LAW_VERSION, policy_hash=UNBOUND,
        source_sha="sha-aaa", resource_state_digest="rs-1",
        scope="naya_node_apply", evidence_ids=("receipt",),
        issued_at=NOW, valid_until=NOW + 900)
    stale_plan = ap.ActionPlan(
        plan_id=plan.plan_id, action=plan.action, chosen=plan.chosen,
        authority=plan.authority, candidate_scores=plan.candidate_scores,
        planned_at=plan.planned_at, law12_proof=old_proof)
    receipt, calls = _execute(stale_plan, now=NOW + 5)
    assert receipt.phase == "EXECUTION_REFUSED"
    assert ap.PLAN_PROOF_STALE in receipt.codes
    assert calls == []


# --- Trust boundary: law12_proof=None ---

def test_plan_action_always_issues_a_proof():
    # Pins the mitigation: in the pipeline's own flow the None branch never
    # fires — only externally-constructed plans can carry law12_proof=None.
    for _ in range(3):
        plan = _plan()
        assert plan.law12_proof is not None


def test_none_proof_does_not_bypass_safety_floor():
    # Hand-crafted plan, no proof, UNSAFE candidate: the Law 11 door and the
    # do-no-harm re-gate still refuse. Skipping Law 12 revalidation is NOT
    # skipping safety.
    unsafe = _candidate(safety_safe=False)
    plan = ap.ActionPlan(
        plan_id="hand-1", action="naya_node_apply", chosen=unsafe,
        authority=_authority(), candidate_scores=(), planned_at=NOW,
        law12_proof=None)
    receipt, calls = _execute(plan, now=NOW + 5)
    assert receipt.phase == "EXECUTION_REFUSED"
    assert ap.PLAN_SAFETY_PROHIBITED in receipt.codes
    assert calls == []


def test_none_proof_skips_only_staleness_revalidation():
    # Documents the boundary honestly: a hand-crafted None-proof plan with a
    # SAFE candidate on a MOVED world still executes — staleness is the
    # external constructor's responsibility, and this test pins that so any
    # change is a conscious decision, not drift.
    plan = ap.ActionPlan(
        plan_id="hand-2", action="naya_node_apply", chosen=_candidate(),
        authority=_authority(), candidate_scores=(), planned_at=NOW,
        law12_proof=None)
    receipt, calls = _execute(plan, now=NOW + 5, source_sha="sha-moved-far")
    assert receipt.phase == "EXECUTION_COMPLETED"
    assert calls == ["hand-2"]
