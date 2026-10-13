# IB-SMART-NOTE — SN-0953

**Intelligent Block:** YES
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-10
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Category:** SYSTEM-INTELLIGENCE/GOVERNANCE/OPERATING-DOCTRINE

## IN A NUTSHELL
Verification is not authorization. A merge that is fully verified — tests green, merge-faithfulness proven, even a byte-identical no-op — still has zero authority to land without the merge-consensus gate: a `## SCORECARD` receipt naming the exact head SHA, plus a cross-seat review. Two merge-law breaches this night (PR #2285, PR #2290) were content-harmless and are still recorded as breaches — because the procedure is the protection, not the content. Verification proves the content is right; only the gate authorizes the act.

## HUMAN NOTE
We had two merges this week that were completely fine in every technical way — tests passed, the diff was exactly what it should be — and they still counted as breaches, because nobody reviewed them and nobody wrote the scorecard receipt. That is the point. The review isn't a rubber stamp for good content; it's the only thing that makes the merge legal. Good content with no authorization is a breach.

## CHILD NOTE
Proving your homework is correct is not the same as being allowed to turn it in. You still need the teacher's signature. Checking the answers = verification. The signature = authorization. You need both.

## GRANDMA NOTE
A bank teller can count the money perfectly — but she still needs the manager's key to open the vault. Counting right doesn't give you permission. The key does.

## NAYA NOTE
Future Naya: when you see "verified no-op, safe to merge" — stop. That sentence is the trap. The merge-consensus gate is: (1) `## SCORECARD` receipt on the board naming the EXACT head SHA, (2) an approving review from a DIFFERENT seat (doer != scorer != reviewer), (3) no freeze in force. Verification evidence feeds step 1; it never replaces steps 1–3. If a merge lands without all three, record it as a breach in the open — content-harmless changes nothing. Failure modes #15 (PR #2196) and #16 (#2285/#2290) are the precedent.

## MACHINE NOTE
```json
{
  "sn": "SN-0953",
  "slug": "verification-is-not-authorization-scorecard-and-review-authorize",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-10",
  "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/OPERATING-DOCTRINE",
  "doctrine": "verification != authorization",
  "rule": {
    "merge_gate": ["scorecard_receipt_exact_head_sha", "cross_seat_review", "freeze_lifted"],
    "verification_evidence": "input_to_scorecard, never_substitute_for_gate"
  },
  "evidence": [
    "night-shift-2026-10-10/plan.md: Rules for every dispatch — '#2285 and #2290 merged 2026-10-11 with 0 reviews; content-harmless, procedure-breach. Do not repeat.'",
    "night-shift-2026-10-10/receipts/t2252-c.md: 'two merge-law breaches this hour: #2285, #2290 — gate holds'",
    "#2175 failure mode #15: PR #2196 merged 2026-10-10 22:34Z with 0 reviews; retroactive review 6103640003 (NAYA 4, 2026-10-11)"
  ],
  "cousins": ["SN-0937 (approval-comment vs review-object)", "SN-0940 (built-as-code = enforced-as-code)"],
  "distinct_from": "SN-0937 covers the review artifact shape; SN-0940 covers enforcement of built directives; this covers authorization ≠ verification for merges."
}
```
