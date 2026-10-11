"""Law 12 mandatory bindings (Shawn's Evidence Binding Law, 2026-10-11).

"Mandatory bindings per action type; UNBOUND on mandatory = FAIL."
A production state-changing proof that leaves a mandatory field UNBOUND
is incomplete and FAILS validation — "recorded openly" is not a license
to skip what the action type requires.

Negative controls: the same UNBOUND fields on non-mandatory action types
(development, read-only) stay valid — the fix adds strictness only where
the action type demands it, and never weakens the honest-UNBOUND design
elsewhere.
"""
import pytest

from kernel import act_pipeline as ap
from kernel.protocol.proof_receipt import (
    LAW_POLICY_VERSION,
    MANDATORY_BINDING_MISSING,
    REVERIFY,
    STILL_VALID,
    UNBOUND,
    ProofContext,
    check_proof_validity,
    issue_proof_receipt,
    mandatory_bindings,
    missing_mandatory_bindings,
    reverify,
)
from kernel.value_calculus import QualityProfile

NOW = 1_790_000_000.0


def _receipt(operation="deploy", environment="production", **kw):
    base = dict(
        actor_id="naya-2",
        operation=operation,
        environment=environment,
        resource="service",
        law_verdict="ADMISSIBLE",
        reason_ids=(),
        policy_version=LAW_POLICY_VERSION,
        policy_hash=UNBOUND,
        source_sha="sha-aaa",
        resource_state_digest=UNBOUND,
        scope="service",
        evidence_ids=("ev-1",),
        issued_at=NOW,
        valid_until=NOW + 900,
        revocation_ref=None,
    )
    base.update(kw)
    return issue_proof_receipt(**base)


def _ctx(**kw):
    base = dict(
        source_sha="sha-aaa",
        policy_version=LAW_POLICY_VERSION,
        policy_hash=UNBOUND,
        resource_state_digest=UNBOUND,
        scope="service",
        now=NOW + 10,
        revoked_refs=(),
    )
    base.update(kw)
    return ProofContext(**base)


# --- the table ---

def test_production_consequential_ops_require_sha_policy_scope():
    for op in ("deploy", "migrate", "delete", "grant", "merge", "write"):
        assert mandatory_bindings(op, "production") == (
            "source_sha", "policy_version", "scope"), op


def test_development_and_readonly_have_no_mandatory_bindings():
    assert mandatory_bindings("deploy", "development") == ()
    assert mandatory_bindings("deploy", "test") == ()
    assert mandatory_bindings("read", "production") == ()
    assert mandatory_bindings("capture", "production") == ()
    assert mandatory_bindings("nope", "production") == ()


# --- validation ---

def test_production_deploy_missing_sha_fails():
    r = _receipt(source_sha=UNBOUND)
    assert missing_mandatory_bindings(r) == ("source_sha",)
    valid, event = check_proof_validity(r, _ctx())
    assert not valid
    assert event == MANDATORY_BINDING_MISSING


def test_production_deploy_missing_policy_version_fails():
    r = _receipt(policy_version=UNBOUND)
    valid, event = check_proof_validity(r, _ctx())
    assert not valid
    assert event == MANDATORY_BINDING_MISSING


def test_production_deploy_missing_scope_fails():
    r = _receipt(scope=UNBOUND)
    valid, event = check_proof_validity(r, _ctx())
    assert not valid
    assert event == MANDATORY_BINDING_MISSING


def test_production_deploy_complete_stays_valid():
    r = _receipt()
    assert missing_mandatory_bindings(r) == ()
    valid, event = check_proof_validity(r, _ctx())
    assert valid and event is None


def test_development_deploy_unbound_sha_still_valid():
    # Negative control: the fix must not over-reach into development.
    r = _receipt(environment="development", source_sha=UNBOUND)
    valid, _ = check_proof_validity(r, _ctx())
    assert valid


def test_production_read_unbound_sha_still_valid():
    # Negative control: read-only operations are not consequential.
    r = _receipt(operation="read", source_sha=UNBOUND)
    valid, _ = check_proof_validity(r, _ctx())
    assert valid


def test_mandatory_check_runs_before_world_comparison():
    # An incomplete proof fails even when the world also moved — the
    # incompleteness is reported, not masked by the later comparison.
    r = _receipt(source_sha=UNBOUND)
    valid, event = check_proof_validity(r, _ctx(source_sha="sha-moved"))
    assert not valid
    assert event == MANDATORY_BINDING_MISSING


def test_reverify_maps_missing_binding_to_reverify():
    r = _receipt(source_sha=UNBOUND)
    assert reverify(r, _ctx()) == REVERIFY
    assert reverify(_receipt(), _ctx()) == STILL_VALID


# --- end to end: consequential action cannot execute with UNBOUND mandatory SHA ---

def _profile():
    return QualityProfile(profile_id="law12-mandatory-test", version="1",
                          objective="minimum sufficient action")


def _authority(**kw):
    base = dict(action="service_deploy", scope="service_deploy",
                decided_at=NOW - 60, expires_at=None, grant_id="grant-1")
    base.update(kw)
    return ap.LawAuthority(**base)


def _candidate(cid="p1", **kw):
    base = dict(
        candidate_id=cid,
        action="service_deploy",
        description="deploy the service",
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
        stakes="high",
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


def test_execute_refuses_production_deploy_with_unbound_sha():
    # The acceptance test: a production deploy proof with UNBOUND
    # source_sha cannot execute — PLAN_PROOF_STALE names the
    # MANDATORY_BINDING_MISSING event.
    proof = _receipt(source_sha=UNBOUND, scope="service_deploy")
    candidate = _candidate()
    plan = ap.ActionPlan(
        plan_id="prod-deploy-1", action="service_deploy", chosen=candidate,
        authority=_authority(), candidate_scores=(), planned_at=NOW,
        law12_proof=proof)
    calls = []
    receipt = ap.execute_plan(
        plan,
        executor=lambda p: calls.append(p.plan_id) or "ok",
        re_resolve=lambda: _authority(decided_at=NOW - 50),
        now=NOW + 5,
        profile=_profile(),
        environment="production",
        source_sha="sha-aaa",
        resource_state_digest=None,
    )
    assert receipt.phase == "EXECUTION_REFUSED"
    assert ap.PLAN_PROOF_STALE in receipt.codes
    assert MANDATORY_BINDING_MISSING in receipt.evidence[0]
    assert calls == []


def test_execute_allows_production_deploy_with_complete_bindings():
    proof = _receipt(scope="service_deploy")
    candidate = _candidate()
    plan = ap.ActionPlan(
        plan_id="prod-deploy-2", action="service_deploy", chosen=candidate,
        authority=_authority(), candidate_scores=(), planned_at=NOW,
        law12_proof=proof)
    calls = []
    receipt = ap.execute_plan(
        plan,
        executor=lambda p: calls.append(p.plan_id) or "ok",
        re_resolve=lambda: _authority(decided_at=NOW - 50),
        now=NOW + 5,
        profile=_profile(),
        environment="production",
        source_sha="sha-aaa",
        resource_state_digest=None,
    )
    assert receipt.phase == "EXECUTION_COMPLETED"
    assert calls == ["prod-deploy-2"]
