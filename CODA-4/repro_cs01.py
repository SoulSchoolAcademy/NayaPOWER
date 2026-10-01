"""Minimal CS-01 reproducer — KNOW cold_reconstruct does not populate the node.

Run from the repository root against a checkout of the PR #1216 candidate:

    python -m pytest tests/test_nodes/test_coda4_cold_successor.py -q
    python CODA-4/repro_cs01.py        # exit 1 == CS-01 present

Owner: Naya 4 (`naya_kernel/`). Found by Coda 4. Not patched here.

The report says the store was restored and the hash matches the predecessor.
The node itself is empty, so nothing is retrievable. A caller that trusts the
report gets a green restore and an unusable node.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from naya_kernel.nodes import know_node  # noqa: E402

NOW = "2026-10-01T04:00:00+00:00"
PRINCIPAL = {"identity": "coda4-repro",
             "entitled_scopes": ["public", "team"]}


def main():
    # --- predecessor: one real ingest through the real seam -----------------
    producer = know_node.KnowNode()
    receipt = producer.ingest({
        "content": json.dumps({"lesson_id": "PROV-BEFORE-APPLY-1"},
                              sort_keys=True),
        "proposed_class": "REUSABLE",
        "class_signals": [{"signal": "coda4-repro", "value": 0.9}],
        "classifier": "coda4-repro",
        "provenance": {"sources": [{
            "kind": "EXTERNAL", "ref": "ext://coda4/repro/lesson",
            "capturedAt": NOW, "capturedBy": "coda4-repro"}]},
        "identity_binding": {"verified": True},
        "owner_scope": "public", "epistemic_state": "INGESTED"},
        PRINCIPAL, now=NOW)
    assert receipt["afterState"] == "ACTIVE", receipt

    # --- successor: a genuinely fresh node, receipts only --------------------
    successor = know_node.KnowNode()
    report = successor.cold_reconstruct([receipt])

    served = successor.retrieve(
        {"text": "PROV-BEFORE-APPLY-1", "requested_scopes": ["public"],
         "identity_binding": {"verified": True}}, PRINCIPAL, now=NOW)

    print("REPORTED restored_block_count :", report["restored_block_count"])
    print("REPORTED store_hash           :", report["store_hash"][:16])
    print("PRODUCER live _store_hash()   :",
          producer._store_hash()[:16])
    print("hashes equal                  :",
          report["store_hash"] == producer._store_hash())
    print("ACTUAL successor.blocks       :", len(successor.blocks))
    print("ACTUAL successor._hash_index  :", len(successor._hash_index))
    print("ACTUAL retrieve() blocks      :",
          [b.get("id") for b in served.get("blocks", [])])

    present = (len(successor.blocks) == 0
               and report["restored_block_count"] == 1
               and report["store_hash"] == producer._store_hash())
    print()
    print("CS-01 PRESENT:", present)
    print("EXIT 1 means the defect is present; EXIT 0 means it was repaired.")
    return 1 if present else 0


if __name__ == "__main__":
    sys.exit(main())