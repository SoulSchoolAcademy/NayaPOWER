"""Law 12 (proofs expire on material change): the receipt is bound to the
exact world it was proven against, and the world moving invalidates it.

Negative controls included: each invalidation test is paired with the
proof that the SAME receipt stays valid when that one field does NOT move,
and that an immaterial (unbound) change never invalidates.
"""
import dataclasses

import pytest

from kernel.protocol.proof_receipt import (
    EXPIRED,
    INTEGRITY_TAMPERED,
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
    # A receipt that never bound the SHA is not invalidated by a SHA move;
    # the unbound-ness is recorded openly (UNBOUND), never silently assumed.
    r = _receipt(source_sha=UNBOUND, policy_hash=UNBOUND,
                 resource_state_digest=UNBOUND)
    assert r.source_sha == UNBOUND
    valid, event = check_proof_validity(r, _ctx(source_sha="sha-bbb"))
    assert valid and event is None


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
