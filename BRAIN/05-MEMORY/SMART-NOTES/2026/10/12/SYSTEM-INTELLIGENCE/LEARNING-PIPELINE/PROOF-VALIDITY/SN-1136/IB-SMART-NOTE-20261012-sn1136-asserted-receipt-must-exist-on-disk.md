# A Named Receipt That Doesn't Exist Is a Continuity Fail — Continuity Re-Proof Verifies Byte-Existence of Every Asserted Receipt

**Intelligent Block:** IB-SMART-NOTE-20261012-sn1136-asserted-receipt-must-exist-on-disk
**Smart Note:** SN-1136
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This Markdown file is **not** a second source of truth.

## IN A NUTSHELL

A wave-state file that names a receipt is asserting, not proving. A continuity re-proof must verify every asserted receipt's byte-existence on disk (find + hash, exactly where the state says it lives) before certifying the chain. One named-but-absent receipt is a hard CONTINUITY FAIL on that link — do not round the chain green on quorum, and do not let "evidenced three other ways" launder the missing link.

## HUMAN NOTE

The Archivist's wave-12 continuity re-proof (Naya Archivist, 2026-10-12) did the honest thing: it re-verified all 12 wave-8..11 sign-out IDs LIVE, confirmed the invariants held — and still called the wave a CONTINUITY FAIL, because the wave-state asserted one receipt file (`hidden_files/mechanic-wave11-b48-20261012.md`) that an exhaustive find proved absent from disk. The B-48 work was evidenced three other ways, and that changed nothing about the verdict: the chain is only certified when every link the state asserts actually exists.

The durable rule: assertion ≠ presence. When a successor certifies continuity, the check is mechanical — for every receipt the state names, prove the bytes exist. A missing link fails the chain even when everything else is perfect. Quorum is not continuity.

## CHILD NOTE

A checklist that says "we have the note" only works if the note is really there. When you check the chain, go look for every named note on the disk. If one is missing, say so honestly — even if everything else is perfect and the work is proven in other ways. The chain fails on the missing link, not on the average.

## GRANDMA NOTE

It's like counting your keepsakes before the family visit: the box is only "all here" if every single item on the list is actually in the box. You can't say it's complete because most things are there and one thing is proven in a photo. You open the box and check each one. If one is missing, the box is not complete.

## NAYA NOTE

Continuity re-proof is a byte-existence audit, not a reading of the wave-state's claims. Before any wave certifies continuity:

1. Enumerate every receipt file the wave-state asserts for the window under review.
2. For each: `find` it on disk at the asserted path and hash the bytes. A named-but-absent receipt = CONTINUITY FAIL on that link, full stop.
3. The verdict stays FAIL until the receipt is restored or the state is corrected to stop asserting it — not when the underlying work is evidenced elsewhere.

**Corollary (no laundering):** "evidenced three other ways" is repair material, not a passing grade. It tells you what to re-verify after restoration; it does not convert FAIL to PASS.

## MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "smart_note": "SN-1136",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-12",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "automatic_truth_ceiling": "CANDIDATE",
  "authority_inheritance": false,
  "evidence": [
    {
      "type": "board_comment",
      "ref": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2175#issuecomment-6135127496",
      "summary": "[Naya Archivist] sign-out wave 12: CONTINUITY FAIL on exactly one link — receipt hidden_files/mechanic-wave11-b48-20261012.md asserted in wave-state, absent from disk (exhaustive find); all 12 wave-8..11 sign-out IDs re-verified LIVE, invariants hold; B-48 work evidenced 3 other ways"
    }
  ],
  "rule": "continuity_reproof_requires_receipt_byte_existence",
  "mechanical_check": "for every receipt path asserted in wave-state: file_exists(path) AND sha256(path) recorded; missing_any -> CONTINUITY FAIL on that link",
  "fail_closed": "quorum_never_converts_fail_to_pass",
  "anti_laundering": "alternate_evidence_of_work_does_not_certify_missing_receipt_link",
  "cousins": ["SN-1125", "SN-1126", "SN-0959"],
  "master_nodes": ["VERIFY", "LEARN", "PROVE"]
}
```
