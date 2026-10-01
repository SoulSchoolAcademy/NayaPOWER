"""LEARN intake authentication guard — Coda 1 finding.

Coda 1 (#554 comment 5937399767): `_is_qualifying_verify` checks only
two caller-controlled fields. A fabricated dict with those labels is
accepted via the runtime `ingest_verify_receipt` path. Zero integrity
keywords in the intake path.

These tests PROVE the vulnerability exists. They will PASS once a
proper authentication mechanism (signature or ledger-resolvable ID)
is implemented. They are not the fix.

Classification: IMPLEMENTED but caller-asserted — not derived.
"""
import pytest

from naya_kernel.nodes.learn_node import LearnNode


def _fabricated_receipt():
    """A receipt with correct labels but zero authentication."""
    return {
        "node_id": "NAYA-KERNEL-VERIFY",
        "verification_state": "VERIFIED_PASS",
        "receipt_id": "fabricated-by-caller-001",
        # No signature, no provenance, no ledger reference,
        # no integrity proof of any kind.
    }


def test_learn_rejects_fabricated_verify_labels():
    """GUARD: fabricated VERIFY labels must NOT be accepted.

    Currently FAILS (vulnerability confirmed). Will PASS once
    authenticated VERIFY emission is implemented.
    """
    node = LearnNode()
    result = node.ingest_verify_receipt(_fabricated_receipt())
    assert result["accepted"] is False, (
        "LEARN accepted a fabricated VERIFY receipt with no authentication. "
        "Coda 1 finding #554/5937399767 is still open."
    )


def test_learn_intake_requires_authentication_evidence():
    """GUARD: intake must require evidence the caller cannot forge.

    A hash the caller can compute is not sufficient (Coda 1).
    This test documents the requirement; it passes when the
    authentication mechanism exists.
    """
    node = LearnNode()
    # Even with a self-consistent receipt_hash, the caller computed it.
    import hashlib
    import json
    body = {
        "node_id": "NAYA-KERNEL-VERIFY",
        "verification_state": "VERIFIED_PASS",
        "receipt_id": "self-hashed-fake-002",
    }
    body["receipt_hash"] = hashlib.sha256(
        json.dumps(body, sort_keys=True).encode()).hexdigest()

    result = node.ingest_verify_receipt(body)
    assert result["accepted"] is False, (
        "LEARN accepted a self-hashed receipt. Caller-computable hashes "
        "are not authentication."
    )


def test_learn_note_investigation_stays_inert():
    """Investigation placeholders must not enter scoring or promotion."""
    node = LearnNode()
    result = node.note_investigation({
        "lesson": "test lesson",
        "learning_type": "BEHAVIOR_RULE",
        "owner_id": "test",
        "scope": {"task": "test"},
    })
    # Must be marked as unverified/inert, not promotable.
    learning_id = result.get("learning_id")
    assert learning_id is not None
    # The learning must not be in the promotable pool.
    # (Implementation detail: check it requires verification first.)
    assert result.get("verification_state", "UNVERIFIED") != "VERIFIED_PASS"
