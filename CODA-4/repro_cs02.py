"""CS-02 reproducer — KNOW cold_reconstruct does not verify receipt integrity.

Separate from CS-01. CS-01 is "reconstructed state is never installed on self."
CS-02 is "the replay trusts its inputs unconditionally."

`Kernel.cold_reconstruct` verifies receipt hashes and reports
`hash_matched` / `hash_mismatched`. `KnowNode.cold_reconstruct` performs NO
integrity verification — `receipt_hash` appears only inside error message
strings. A forged KNOW receipt is replayed into state as if genuine.

    python CODA-4/repro_cs02.py     # exit 1 == CS-02 present, 0 == repaired

Owner: Naya 4 (`naya_kernel/`). Found by Coda 4. Not patched here.

SCOPE — read before treating this as an exploit:
This proves an integrity gap in the KNOW replay path. It does NOT prove a
production exploit. No production data path was exercised, no database was
touched, and no deployed system served forged content. It also does not claim
the fix is a one-line hash check: `block_snapshot` is embedded in the receipt,
so verifying `receipt_hash` would detect in-transit tampering of the whole
receipt, but the snapshot's own consistency with that hash is the owner's call.
"""

import copy
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from naya_kernel.nodes import know_node  # noqa: E402

NOW = "2026-10-01T04:00:00+00:00"
PRINCIPAL = {"identity": "coda4-cs02",
             "entitled_scopes": ["public", "team"]}


def _ingest():
    node = know_node.KnowNode()
    receipt = node.ingest({
        "content": json.dumps({"lesson_id": "CS-02-PROBE"}, sort_keys=True),
        "proposed_class": "REUSABLE",
        "class_signals": [{"signal": "coda4-cs02", "value": 0.9}],
        "classifier": "coda4-cs02",
        "provenance": {"sources": [{
            "kind": "EXTERNAL", "ref": "ext://coda4/ORIGINAL",
            "capturedAt": NOW, "capturedBy": "coda4-cs02"}]},
        "identity_binding": {"verified": True},
        "owner_scope": "public", "epistemic_state": "INGESTED"},
        PRINCIPAL, now=NOW)
    assert receipt["afterState"] == "ACTIVE", receipt
    return receipt


def main():
    receipt = _ingest()

    print("== A: forge the provenance ref inside block_snapshot ==")
    forged = copy.deepcopy(receipt)
    forged["block_snapshot"]["provenance"]["sources"][0]["ref"] = \
        "ext://coda4/FORGED"
    report = know_node.KnowNode().cold_reconstruct([forged])
    accepted_a = report["restored_block_count"] == 1
    print("   forged receipt replayed  :", accepted_a)
    print("   integrity keys in report:",
          sorted(k for k in report if "hash" in k))

    print("\n== B: forge ownerScope from public to private ==")
    forged_b = copy.deepcopy(receipt)
    forged_b["block_snapshot"]["ownerScope"] = "private"
    report_b = know_node.KnowNode().cold_reconstruct([forged_b])
    accepted_b = report_b["restored_block_count"] == 1
    print("   private-scope block accepted:", accepted_b)

    print("\n== C: contrast with Kernel.cold_reconstruct, which DOES verify ==")
    import inspect

    from naya_kernel.kernel import Kernel
    kernel_src = inspect.getsource(Kernel.cold_reconstruct)
    know_src = inspect.getsource(know_node.KnowNode.cold_reconstruct)
    for field in ("hash_matched", "hash_mismatched"):
        print("   Kernel reports %-16s %s" % (field, field in kernel_src))
        print("   KNOW   reports %-16s %s" % (field, field in know_src))

    print("\n== D: a genuinely malformed lifecycle state IS fail-closed ==")
    malformed = copy.deepcopy(receipt)
    malformed["afterState"] = "REVOKED"
    try:
        know_node.KnowNode().cold_reconstruct([malformed])
        print("   NO FAILURE RAISED  <- unexpected")
    except ValueError as exc:
        print("   ValueError (fail-closed):", str(exc)[:64])

    present = accepted_a and accepted_b and "hash_matched" not in know_src
    print()
    print("CS-02 PRESENT:", present)
    print("EXIT 1 means the defect is present; EXIT 0 means it was repaired.")
    return 1 if present else 0


if __name__ == "__main__":
    sys.exit(main())