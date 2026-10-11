"""Unified Law 11 + Law 12 machine API: evaluate() binds the verdict to the
world; execute_checked() re-gates at the last responsible moment.

Negative controls: every "blocked" test asserts the executor was NOT called,
and the Law 12 block is proven to be the proof (not the Law 11 door) by a
case where the door passes but the proof is stale.
"""
import pytest

from kernel.protocol.law_enforcement import (
    ADMISSIBLE_STATE,
    EXECUTOR_NEVER_CALLED,
    NEEDS_AUTHORITY_STATE,
    NEEDS_EVIDENCE_STATE,
    PROHIBITED_STATE,
    PROOF_INVALIDATED,
    EnforcementContext,
    evaluate,
    execute_checked,
)
from kernel.protocol.proof_receipt import UNBOUND
from kernel.protocol.typed_action import TypedAction

NOW = 1_790_000_000.0
POLICY = "CURRENT"


def _clean_action(**kw):
    base = dict(
        actor_id="naya-2",
        operation="write",
        environment="development",
        resource="smart_notes",
        authority_ref="grant-1",
        policy_version=POLICY,
        reversibility="reversible",
        rights_safe=True,
        safety_safe=True,
        privacy_safe=True,
        consent_obtained=True,
    )
    base.update(kw)
    return TypedAction(**base)


def _ctx(**kw):
    base = dict(
        actor_id="naya-2",
        source_sha="sha-aaa",
        policy_version=POLICY,
        policy_hash="ph-1",
        resource_state_digest="rs-1",
        scope="smart_notes",
        now=NOW,
        proof_ttl_seconds=900,
        current_authority_ref="grant-1",
        current_resource="smart_notes",
    )
    base.update(kw)
    return EnforcementContext(**base)


# --- evaluate() states ---

def test_evaluate_clean_action_is_admissible_with_bound_receipt():
    d = evaluate(_ctx(), _clean_action(), POLICY, ("ev-1",))
    assert d.state == ADMISSIBLE_STATE and d.admissible
    assert d.receipt_id and d.scope == "smart_notes"
    assert d.expiry == NOW + 900
    p = d.proof
    assert p.integrity_ok()
    assert p.law_verdict == ADMISSIBLE_STATE
    assert p.source_sha == "sha-aaa" and p.policy_version == POLICY
    assert p.resource_state_digest == "rs-1" and p.evidence_ids == ("ev-1",)


def test_evaluate_inherently_prohibited_never_admissible():
    d = evaluate(_ctx(), _clean_action(operation="fabricate_evidence"), POLICY)
    assert d.state == PROHIBITED_STATE and not d.admissible
    assert any("INHERENTLY_PROHIBITED" in r for r in d.reason_ids)


def test_evaluate_unknown_safety_is_needs_evidence_not_safe():
    # Missing harm data is NEEDS_EVIDENCE, never SAFE or TRUE_ZERO.
    d = evaluate(_ctx(), _clean_action(safety_safe=None), POLICY)
    assert d.state == NEEDS_EVIDENCE_STATE and not d.admissible


def test_evaluate_protected_op_without_authority():
    d = evaluate(_ctx(), _clean_action(operation="deploy", environment="production",
                                        authority_ref=None), POLICY)
    assert d.state == NEEDS_AUTHORITY_STATE and not d.admissible


def test_evaluate_binds_unbound_fields_openly():
    d = evaluate(_ctx(source_sha=UNBOUND), _clean_action(), POLICY)
    assert d.admissible
    assert d.proof.source_sha == UNBOUND  # recorded, not silently valid


# --- execute_checked(): the last responsible moment ---

def test_execute_checked_fires_when_world_held():
    calls = []
    d = evaluate(_ctx(), _clean_action(), POLICY)
    out = execute_checked(
        d, _clean_action(), lambda: calls.append(1) or "done",
        planned_authority_ref="grant-1", planned_resource="smart_notes",
        fresh_context=_ctx(now=NOW + 5),
    )
    assert out.executed and out.result == "done" and calls == [1]


def test_execute_checked_blocks_on_stale_proof_door_would_pass():
    # The Law 11 door passes (authority + target unchanged); the Law 12
    # proof is what blocks: SHA moved between plan and execution.
    calls = []
    d = evaluate(_ctx(), _clean_action(), POLICY)
    out = execute_checked(
        d, _clean_action(), lambda: calls.append(1) or "done",
        planned_authority_ref="grant-1", planned_resource="smart_notes",
        fresh_context=_ctx(now=NOW + 5, source_sha="sha-moved"),
    )
    assert not out.executed and calls == []
    assert PROOF_INVALIDATED in out.reason_ids
    assert EXECUTOR_NEVER_CALLED in out.reason_ids


def test_execute_checked_blocks_on_authority_withdrawn():
    calls = []
    d = evaluate(_ctx(), _clean_action(), POLICY)
    out = execute_checked(
        d, _clean_action(), lambda: calls.append(1) or "done",
        planned_authority_ref="grant-1", planned_resource="smart_notes",
        fresh_context=_ctx(now=NOW + 5, current_authority_ref=None),
    )
    assert not out.executed and calls == []
    assert any("AUTHORITY_WITHDRAWN" in r for r in out.reason_ids)


def test_execute_checked_blocks_on_target_changed():
    calls = []
    d = evaluate(_ctx(), _clean_action(), POLICY)
    out = execute_checked(
        d, _clean_action(), lambda: calls.append(1) or "done",
        planned_authority_ref="grant-1", planned_resource="smart_notes",
        fresh_context=_ctx(now=NOW + 5, current_resource="other_store"),
    )
    assert not out.executed and calls == []
    assert any("TARGET_CHANGED" in r for r in out.reason_ids)


def test_execute_checked_blocks_on_expired_proof():
    calls = []
    d = evaluate(_ctx(), _clean_action(), POLICY)
    out = execute_checked(
        d, _clean_action(), lambda: calls.append(1) or "done",
        planned_authority_ref="grant-1", planned_resource="smart_notes",
        fresh_context=_ctx(now=NOW + 901),
    )
    assert not out.executed and calls == []
    assert PROOF_INVALIDATED in out.reason_ids
