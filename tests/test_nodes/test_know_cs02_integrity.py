"""CS-02 RED: KnowNode.cold_reconstruct must verify receipt integrity.

Coda 4 found: KnowNode.cold_reconstruct replays receipts without
verifying their receipt_hash, where Kernel.cold_reconstruct does.
Forging a receipt's provenance ref, or widening ownerScope
public → private, replays into restored state with no failure.

These tests assert that tampered receipts are REJECTED (not replayed).
"""
import copy

import pytest

from naya_kernel.nodes.know_node import KnowNode


def _make_node_with_receipt():
    """Create a node with one ingested block; return (node, receipt)."""
    node = KnowNode()
    candidate = {
        "content": "test content for CS-02",
        "proposed_class": "CONTEXT",
        "class_signals": [{"signal": "auto-classifier-v0", "value": 0.82}],
        "classifier": "auto",
        "provenance": {"sources": [{
            "kind": "EXTERNAL", "ref": "ext://example/test",
            "capturedAt": "2026-10-01T00:00:00+00:00",
            "capturedBy": "naya-test"}]},
        "identity_binding": {"verified": True},
        "owner_scope": "public",
        "epistemic_state": "INGESTED",
    }
    principal = {"identity": "test", "entitled_scopes": ["public"]}
    receipt = node.ingest(candidate, principal, now="2026-10-01T00:00:00+00:00")
    return node, receipt


def test_cs02_tampered_receipt_hash_rejected():
    """A receipt with a forged receipt_hash must not replay."""
    _, receipt = _make_node_with_receipt()
    tampered = copy.deepcopy(receipt)
    tampered["receipt_hash"] = "0" * 64  # forged hash
    with pytest.raises(ValueError, match="integrity"):
        KnowNode().cold_reconstruct([tampered])


def test_cs02_forged_provenance_rejected():
    """Forging the provenance ref must be detected via hash mismatch."""
    _, receipt = _make_node_with_receipt()
    tampered = copy.deepcopy(receipt)
    # Forge a field that's part of the receipt body.
    tampered["upstreamReceipt"] = "forged-provenance-ref"
    # Note: we do NOT update receipt_hash — that's the attack.
    with pytest.raises(ValueError, match="integrity"):
        KnowNode().cold_reconstruct([tampered])


def test_cs02_widened_owner_scope_rejected():
    """Widening ownerScope public → private must be detected."""
    _, receipt = _make_node_with_receipt()
    tampered = copy.deepcopy(receipt)
    tampered["ownerScope"] = "private"  # was "public"
    # Hash not updated — the forgery must be caught.
    with pytest.raises(ValueError, match="integrity"):
        KnowNode().cold_reconstruct([tampered])


def test_cs02_valid_receipt_still_replays():
    """Untampered receipts must continue to replay correctly."""
    node, receipt = _make_node_with_receipt()
    report = KnowNode().cold_reconstruct([receipt])
    assert report["restored_block_count"] == 1
    assert report["replayed_receipts"] == 1
