"""Lifecycle exclusion tests: restoration must not revive dead blocks.

A restored count is a diagnostic, not the success criterion. Restored
intelligence must be usable AND must preserve the reasons some
intelligence cannot be used.

- SUPERSEDED / EXPIRED / INVALIDATED / REFUSED blocks restore with their
  terminal state and are NOT served via public retrieve().
- CONTRADICTED blocks restore and ARE served (with linkage visible).
"""
import copy

from naya_kernel.nodes.know_node import KnowNode


def _ingest(node: KnowNode, content: str,
            now: str = "2026-10-01T00:00:00+00:00",
            supersedes: str = None) -> str:
    """Ingest via public API; return block_id."""
    candidate = {
        "content": content,
        "proposed_class": "CONTEXT",
        "class_signals": [{"signal": "auto-classifier-v0", "value": 0.82}],
        "classifier": "auto",
        "provenance": {"sources": [{
            "kind": "EXTERNAL", "ref": "ext://example/test",
            "capturedAt": now, "capturedBy": "naya-test"}]},
        "identity_binding": {"verified": True},
        "owner_scope": "public",
        "epistemic_state": "INGESTED",
    }
    if supersedes:
        candidate["supersedes"] = supersedes
    principal = {"identity": "test", "entitled_scopes": ["public"]}
    result = node.ingest(candidate, principal, now=now)
    return result["blockId"]


def _retrieve_ids(node: KnowNode, text: str):
    """Public retrieval; return served block ids."""
    principal = {"identity": "test", "entitled_scopes": ["public"]}
    query = {"text": text, "requested_scopes": ["public"],
             "identity_binding": {"verified": True}}
    result = node.retrieve(query, principal)
    assert result["admitted"], f"not admitted: {result['reasons']}"
    return [b["id"] for b in result["blocks"]]


def _reconstruct(receipts):
    """Cold reconstruct into a fresh node; return it."""
    successor = KnowNode()
    successor.cold_reconstruct(receipts)
    return successor


def test_lifecycle_superseded_not_served():
    """A superseded block restores as SUPERSEDED and is not served."""
    producer = KnowNode()
    old_id = _ingest(producer, "old content superseded test")
    new_id = _ingest(producer, "new content superseded test",
                     supersedes=old_id)

    successor = _reconstruct(list(producer.receipts))

    # Block restores with terminal state...
    assert successor.blocks[old_id]["state"] == "SUPERSEDED"
    # ...but is NOT served.
    served = _retrieve_ids(successor, "old content superseded test")
    assert old_id not in served, "superseded block must not be served"
    # The superseding block IS served.
    assert new_id in _retrieve_ids(successor, "new content superseded test")


def test_lifecycle_contradicted_is_served_with_linkage():
    """Contradicted blocks restore and ARE served (linkage visible)."""
    producer = KnowNode()
    id_a = _ingest(producer, "claim A contradicted test")
    id_b = _ingest(producer, "claim B contradicted test")
    principal = {"identity": "test", "entitled_scopes": ["public"]}
    producer.contradict(id_a, id_b, principal)

    successor = _reconstruct(list(producer.receipts))

    assert successor.blocks[id_a]["state"] == "CONTRADICTED"
    served = _retrieve_ids(successor, "claim A contradicted test")
    assert id_a in served, "contradicted blocks remain servable"
    # Linkage preserved.
    assert id_b in successor.blocks[id_a].get("contradicts", [])


def test_lifecycle_invalidated_not_served():
    """An invalidated block restores as INVALIDATED and is not served."""
    producer = KnowNode()
    bid = _ingest(producer, "invalidated content test")
    principal = {"identity": "test", "entitled_scopes": ["public"]}
    producer.invalidate(bid, "test invalidation", principal)

    successor = _reconstruct(list(producer.receipts))

    assert successor.blocks[bid]["state"] == "INVALIDATED"
    served = _retrieve_ids(successor, "invalidated content test")
    assert bid not in served, "invalidated block must not be served"


def test_lifecycle_expired_not_served():
    """An expired block restores as EXPIRED and is not served."""
    producer = KnowNode()
    # Ingest with a past expiry.
    candidate = {
        "content": "expired content test",
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
        "valid_until": "2026-10-01T00:00:01+00:00",  # already expired
    }
    principal = {"identity": "test", "entitled_scopes": ["public"]}
    result = producer.ingest(candidate, principal, now="2026-10-01T00:00:00+00:00")
    bid = result["blockId"]

    # Run expiry sweep to mark it EXPIRED.
    producer.expire_sweep(now="2026-10-02T00:00:00+00:00")

    successor = _reconstruct(list(producer.receipts))

    assert successor.blocks[bid]["state"] == "EXPIRED"
    served = _retrieve_ids(successor, "expired content test")
    assert bid not in served, "expired block must not be served"
