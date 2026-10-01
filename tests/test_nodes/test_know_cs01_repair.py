"""CS-01 repair verification: the receiving node must ACTUALLY contain blocks.

Regression at 73e17e81: cold_reconstruct built `fresh` but never installed
onto self. The report said "1 block restored" while self.blocks was empty.

This test proves via the PUBLIC RETRIEVAL INTERFACE (not the report) that
the successor contains the restored blocks.
"""
from naya_kernel.nodes.know_node import KnowNode


def _make_ingest_receipt(node: KnowNode, content: str) -> dict:
    """Create a valid INGEST receipt via the node's public interface."""
    candidate = {
        "content": content,
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
    node.ingest(candidate, principal, now="2026-10-01T00:00:00+00:00")
    # Return the last INGEST receipt.
    for r in reversed(node.receipts):
        if r.get("operation") == "INGEST":
            return r
    raise AssertionError("ingest did not produce a receipt")


def test_cs01_successor_contains_blocks_via_public_retrieval():
    """After cold_reconstruct, self must serve blocks via public API."""
    # Producer: ingest a block, get its receipts.
    producer = KnowNode()
    _make_ingest_receipt(producer, "test content")
    receipts = list(producer.receipts)
    assert len(receipts) > 0

    # Successor: cold reconstruct from receipts.
    successor = KnowNode()
    assert len(successor.blocks) == 0, "successor starts empty"

    report = successor.cold_reconstruct(receipts)

    # The report says blocks were restored...
    assert report["restored_block_count"] >= 1

    # ...AND the successor ACTUALLY contains them (the regression).
    assert len(successor.blocks) >= 1, (
        "REGRESSION: report says restored but self.blocks is empty")

    # Via PUBLIC RETRIEVAL INTERFACE (not just .blocks).
    # The successor must serve the restored block in a search.
    block_id = report["block_ids"][0]
    principal = {"identity": "test", "entitled_scopes": ["public"]}
    query = {
        "text": "test content",
        "requested_scopes": ["public"],
        "identity_binding": {"verified": True},
    }
    result = successor.retrieve(query, principal)
    assert result["admitted"], f"retrieve not admitted: {result['reasons']}"
    served_ids = [b["id"] for b in result["blocks"]]
    assert block_id in served_ids, (
        f"restored block {block_id} not served via public retrieve(); "
        f"served: {served_ids}")


def test_cs01_sequence_continuity():
    """After reconstruct, new ingests must not collide with replayed seq."""
    producer = KnowNode()
    _make_ingest_receipt(producer, "content 1")
    receipts = list(producer.receipts)
    max_seq = max(r.get("seq", 0) for r in receipts)

    successor = KnowNode()
    successor.cold_reconstruct(receipts)

    # New ingest on successor must get seq > max replayed.
    candidate = {
        "content": "new content",
        "proposed_class": "CONTEXT",
        "class_signals": [{"signal": "auto-classifier-v0", "value": 0.82}],
        "classifier": "auto",
        "provenance": {"sources": [{
            "kind": "EXTERNAL", "ref": "ext://example/test2",
            "capturedAt": "2026-10-01T00:00:00+00:00",
            "capturedBy": "naya-test"}]},
        "identity_binding": {"verified": True},
        "owner_scope": "public",
        "epistemic_state": "INGESTED",
    }
    principal = {"identity": "test", "entitled_scopes": ["public"]}
    successor.ingest(candidate, principal, now="2026-10-01T01:00:00+00:00")
    new_receipt = successor.receipts[-1]
    assert new_receipt.get("seq", 0) > max_seq, (
        f"sequence collision: new seq {new_receipt.get('seq')} "
        f"not > max replayed {max_seq}")


def test_cs01_receipt_history_restored():
    """The successor must retain the replayed receipt history."""
    producer = KnowNode()
    _make_ingest_receipt(producer, "content 1")
    receipts = list(producer.receipts)

    successor = KnowNode()
    report = successor.cold_reconstruct(receipts)

    # Receipt history includes replayed + RESTORE receipt.
    assert len(successor.receipts) >= len(receipts)
    # Last receipt is the RESTORE.
    assert successor.receipts[-1].get("operation") == "RESTORE"
