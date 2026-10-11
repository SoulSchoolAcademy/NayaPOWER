"""Law 12 (proofs expire on material change): the receipt is bound to the
exact world it was proven against, and the world moving invalidates it.

Negative controls included: each invalidation test is paired with the
proof that the SAME receipt stays valid when that one field does NOT move,
and that an immaterial (unbound) change never invalidates.
"""
import dataclasses

import pytest

from kernel.protocol.proof_receipt import (
    ASSUMPTION_CHANGED,
    EXPIRED,
    INTEGRITY_TAMPERED,
    MISSING_BINDING,
    POLICY_HASH_CHANGED,
    POLICY_VERSION_CHANGED,
    RECHECK,
    RESOURCE_STATE_CHANGED,
    REVOKED,
    REVERIFY,
    SCOPE_MISMATCH,
    SOURCE_SHA_MOVED,
    STILL_VALID,
    UNBOUND,
    ProofContext,
    check_proof_validity,
    digest_state,
    issue_proof_receipt,
    required_bindings_for,
    reverify,
)

NOW = 1_790_000_000.0


def _receipt(**kw):
    base = dict(
        actor_id="naya-2",
        operation="write",
        environment="development",
        resource="smart_notes",
        law_verdict="ADMISSIBLE",
        reason_ids=(),
        policy_version="CURRENT",
        policy_hash="ph-1",
        source_sha="sha-aaa",
        resource_state_digest="rs-1",
        scope="smart_notes",
        evidence_ids=("ev-1",),
        issued_at=NOW,
        valid_until=NOW + 900,
        revocation_ref="rev-1",
    )
    base.update(kw)
    return issue_proof_receipt(**base)


def _ctx(**kw):
    base = dict(
        source_sha="sha-aaa",
        policy_version="CURRENT",
        policy_hash="ph-1",
        resource_state_digest="rs-1",
        scope="smart_notes",
        now=NOW + 10,
        revoked_refs=(),
    )
    base.update(kw)
    return ProofContext(**base)


# --- issuance ---

def test_issue_binds_integrity_and_unique_id():
    r1, r2 = _receipt(), _receipt()
    assert r1.integrity_ok()
    assert r2.integrity_ok()
    assert r1.receipt_id != r2.receipt_id
    assert len(r1.integrity) == 64


def test_tampered_receipt_is_detected():
    r = _receipt()
    forged = dataclasses.replace(r, law_verdict="PROHIBITED")
    assert not forged.integrity_ok()
    valid, event = check_proof_validity(forged, _ctx())
    assert not valid and event == INTEGRITY_TAMPERED


def test_receipt_without_integrity_never_valid():
    r = dataclasses.replace(_receipt(), integrity="")
    valid, event = check_proof_validity(r, _ctx())
    assert not valid and event == INTEGRITY_TAMPERED


# --- the seven invalidation events ---

@pytest.mark.parametrize("field,ctx_field,event", [
    ("source_sha", "source_sha", SOURCE_SHA_MOVED),
    ("policy_version", "policy_version", POLICY_VERSION_CHANGED),
    ("policy_hash", "policy_hash", POLICY_HASH_CHANGED),
    ("resource_state_digest", "resource_state_digest", RESOURCE_STATE_CHANGED),
])
def test_material_moves_invalidate(field, ctx_field, event):
    r = _receipt()
    # control: unchanged world -> valid
    assert check_proof_validity(r, _ctx()) == (True, None)
    # moved world -> invalid with the exact event
    ctx = _ctx(**{ctx_field: "MOVED"})
    valid, got = check_proof_validity(r, ctx)
    assert not valid and got == event


def test_scope_mismatch_invalidates():
    r = _receipt()
    valid, event = check_proof_validity(r, _ctx(scope="other_scope"))
    assert not valid and event == SCOPE_MISMATCH


def test_revocation_invalidates():
    r = _receipt()
    valid, event = check_proof_validity(r, _ctx(revoked_refs=("rev-1",)))
    assert not valid and event == REVOKED


def test_expiry_invalidates():
    r = _receipt()
    valid, event = check_proof_validity(r, _ctx(now=NOW + 901))
    assert not valid and event == EXPIRED


def test_unbound_fields_neither_validate_nor_invalidate():
    # A receipt that never bound a NON-MANDATORY field is not invalidated
    # by that field moving; the unbound-ness is recorded openly (UNBOUND),
    # never silently assumed. (T-19: mandatory UNBOUND fields fail — see
    # test_missing_mandatory_binding_fails below. policy_hash is not
    # mandatory for "write", so unbinding it is still neutral.)
    r = _receipt(policy_hash=UNBOUND)
    assert r.policy_hash == UNBOUND
    valid, event = check_proof_validity(r, _ctx(policy_hash="ph-2"))
    assert valid and event is None


def test_missing_mandatory_binding_fails():
    # T-19 Evidence Binding Law: a mandatory binding left UNBOUND fails
    # validation outright. "write" requires source_sha; a receipt that
    # never pinned it cannot be honored, no matter what the context says.
    r = _receipt(source_sha=UNBOUND)
    valid, event = check_proof_validity(r, _ctx())
    assert not valid and event == MISSING_BINDING


def test_missing_mandatory_binding_fails_even_when_context_unbound():
    # The failure is about the receipt's incompleteness, not a mismatch:
    # even if the context also leaves the field unbound, a mandatory
    # UNBOUND on the receipt is still MISSING_BINDING.
    r = _receipt(source_sha=UNBOUND)
    valid, event = check_proof_validity(r, _ctx(source_sha=UNBOUND))
    assert not valid and event == MISSING_BINDING


def test_immaterial_change_does_not_invalidate():
    # Only bound fields participate. A context that differs in nothing the
    # receipt bound (here: policy fields unbound on both sides) stays valid —
    # an unrelated change never erases independent outcome evidence.
    r = _receipt(policy_version=UNBOUND, policy_hash=UNBOUND)
    ctx = _ctx(policy_version="SOMETHING_ELSE", policy_hash="OTHER")
    valid, event = check_proof_validity(r, ctx)
    assert valid and event is None


# --- reverify outcomes ---

def test_reverify_still_valid():
    assert reverify(_receipt(), _ctx()) == STILL_VALID


def test_reverify_hash_drift_is_recheck():
    assert reverify(_receipt(), _ctx(policy_hash="ph-2")) == RECHECK


def test_reverify_expiry_is_reverify():
    assert reverify(_receipt(), _ctx(now=NOW + 901)) == REVERIFY


def test_reverify_tamper_is_reverify():
    r = dataclasses.replace(_receipt(), law_verdict="PROHIBITED")
    assert reverify(r, _ctx()) == REVERIFY


# --- digest helper ---

def test_digest_state_stable_and_sensitive():
    assert digest_state({"a": 1, "b": [2, 3]}) == digest_state({"b": [2, 3], "a": 1})
    assert digest_state({"a": 1}) != digest_state({"a": 2})


# --- T-19 Evidence Binding Law: six practical examples (Shawn, 2026-10-11) ---
# The machine rule: same claim, same authorized scope, same relevant target
# and conditions, valid supporting proof. Otherwise, recheck before acting.


def test_example1_sha_moved_after_tests_pass():
    # Tests ran on abc123; deployment requested for def456.
    # The tests do not prove the new commit passes. HOLD.
    r = _receipt(operation="deploy", source_sha="abc123")
    valid, event = check_proof_validity(r, _ctx(source_sha="def456"))
    assert not valid and event == SOURCE_SHA_MOVED


def test_example2_same_code_different_environment():
    # Staging test, production execution. DB schema v4 -> v5, test gateway
    # -> live gateway. The staging proof is not sufficient for production.
    # Model the environment move as a resource-state change: the bound
    # world (staging + schema v4) no longer matches the live world.
    r = _receipt(
        operation="deploy",
        environment="staging",
        resource_state_digest=digest_state({"schema": "v4", "gateway": "test"}),
    )
    live = _ctx(
        resource_state_digest=digest_state({"schema": "v5", "gateway": "live"}),
    )
    # Environment is part of the receipt's identity (actor/operation/
    # environment/resource are always mandatory). A receipt bound to
    # staging checked against a production context must not validate —
    # here proven via the resource-state digest move.
    valid, event = check_proof_validity(r, live)
    assert not valid and event == RESOURCE_STATE_CHANGED


def test_example2_environment_identity_is_mandatory():
    # The environment is a mandatory identity binding: a proof earned in
    # staging can never be silently reused for production. Direct check:
    # the receipt's environment field is compared by the caller via the
    # identity fields (actor_id/operation/environment/resource are always
    # in REQUIRED_BINDINGS["*"]).
    assert "environment" in required_bindings_for("deploy")
    assert "environment" in required_bindings_for("write")
    assert "environment" in required_bindings_for("anything-else")


def test_example3_permission_revoked_after_evidence_passes():
    # Tests pass, human grants one write, grant revoked before execution.
    # The test evidence may still be valid, but the write cannot proceed
    # without current legitimate permission. NEEDS_AUTHORITY.
    r = _receipt(revocation_ref="grant-7")
    valid, event = check_proof_validity(r, _ctx(revoked_refs=("grant-7",)))
    assert not valid and event == REVOKED


def test_example4_irrelevant_file_change_keeps_evidence():
    # A README is edited; the tested function, its dependencies, test
    # config and required assumptions are identical. The unit-test
    # evidence remains applicable — an unrelated change never erases
    # independent outcome evidence.
    r = _receipt()
    # The context moves in nothing the receipt bound: same SHAs, same
    # digests, same scope. Only unbound/immaterial things changed.
    valid, event = check_proof_validity(r, _ctx())
    assert valid and event is None


def test_example4_sha_pinned_authorization_does_not_transfer():
    # BUT a merge/deployment approval explicitly pinned to the old full
    # commit SHA cannot transfer to the new SHA. Evidence applicability
    # and authorization validity are separate questions: the test proof
    # may stand, but the SHA-pinned grant does not move with it.
    r = _receipt(operation="deploy", source_sha="abc123")
    valid, event = check_proof_validity(r, _ctx(source_sha="def456"))
    assert not valid and event == SOURCE_SHA_MOVED


def test_example5_privacy_assumptions_changed():
    # Analytics workflow collected data categories {a, b} under the
    # assessed privacy conditions. It begins collecting category c —
    # not covered by the original assessment. Block: fresh LAW + evidence
    # required. The old proof cannot extend to the new category.
    old_assumptions = digest_state({
        "data_categories": ["a", "b"],
        "consent": "opt-in",
        "retention_days": 30,
        "policy_version": "v2.1",
    })
    new_assumptions = digest_state({
        "data_categories": ["a", "b", "c"],
        "consent": "opt-in",
        "retention_days": 30,
        "policy_version": "v2.1",
    })
    r = _receipt(operation="write", assumptions_digest=old_assumptions)
    valid, event = check_proof_validity(
        r, _ctx(assumptions_digest=new_assumptions)
    )
    assert not valid and event == ASSUMPTION_CHANGED


def test_example5_identical_assumptions_stay_valid():
    # Same assumptions, same world: the proof stands. The binding only
    # fires on actual change, not on the mere presence of assumptions.
    assumptions = digest_state({"data_categories": ["a", "b"]})
    r = _receipt(operation="write", assumptions_digest=assumptions)
    valid, event = check_proof_validity(r, _ctx(assumptions_digest=assumptions))
    assert valid and event is None


def test_example6_delayed_effects_not_measured():
    # 7/30 days observed. The reliability claim is PROVISIONAL —
    # PASS_PENDING_WINDOW, not PASS. A proof whose validity window
    # has not yet completed cannot be treated as final.
    #
    # Model: the receipt's valid_until marks the end of the required
    # observation window. Before then, the proof is not yet earned.
    r = _receipt(
        operation="write",
        issued_at=NOW,
        valid_until=NOW + 30 * 86400,  # 30-day window
    )
    # Day 7: inside the window — the receipt is structurally valid but
    # the observation is incomplete. Law 12 reports STILL_VALID for the
    # binding check; the *verdict* layer must read this as provisional.
    # What we prove here: the window is enforced — after day 30 without
    # re-issuance, the proof expires and must be re-earned.
    valid, _ = check_proof_validity(r, _ctx(now=NOW + 7 * 86400))
    assert valid  # bindings hold; provisional status is the verdict layer's job
    valid, event = check_proof_validity(r, _ctx(now=NOW + 31 * 86400))
    assert not valid and event == EXPIRED  # window lapsed, re-earn required
