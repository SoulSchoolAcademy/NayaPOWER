# IB-SMART-NOTE-20260930-sn01724

**Intelligent Block:** SN-01724
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-20
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

When a parent receipt says "N failures," don't start from N. The gap-t1032 parent claimed "9 failures" but listed items that sum to 8 (1+6+1); the re-deriving seat recounted from zero on exact head bytes and found 7 reproducible — and one listed "failure" (CLAIM 3, load_bearing_claims 15/15 PASS) was green on the merged tree. Inheriting the parent's count would have certified a phantom. The discrepancy is itself a finding: parent-count vs list-sum vs reproduced-count — three numbers, reported.

## 🩷 HUMAN NOTE

If someone tells you "there were nine problems," don't write down nine — check the list yourself. In this case the list added up to eight, and when the team re-tested every item on the exact code, only seven actually failed. One of the "problems" turned out to be fine on the final code. The old number was a miscount that got copied forward. Counting for yourself takes an extra minute and stops a wrong number from becoming a fact.

## 🟣 CHILD NOTE

Your friend says "I lost nine marbles." You look at her hand — there are only eight. You look closer — one of them is actually a bead, not a marble. So the real count is seven marbles lost, not nine. If you just wrote down "nine" because she said it, you'd be repeating a mistake. Count them yourself — and when your count doesn't match what you were told, the mismatch is part of the story.

## 🔵 GRANDMA NOTE

Dear, always count for yourself. A well-meaning friend said nine things were broken, but when the team looked at the actual list it added to eight, and when they tested each one on the real code only seven were truly broken. One had already been fixed. Trusting the first number would have certified a ghost — a problem that no longer existed. The extra counting isn't suspicion; it's care.

## 🟠 NAYA NOTE

Re-derivation discipline for inherited counts: when a parent receipt names a count ("N failures") and enumerates items: (1) sum the parent's own list — if list-sum != N, that's a finding, not a typo to ignore; (2) recount from zero on exact head bytes — re-run every listed item, never inherit pass/fail; (3) classify against the merged-commit bytes when a fix may have landed between; (4) report three numbers in the receipt: parent-count, list-sum, reproduced-count. Here: 9 claimed, 8 listed (1+6+1), 7 reproduced; CLAIM 3 green on merged bytes — the parent's "9" would have certified a phantom had the seat inherited it. A count discrepancy between parent text and parent list is never cosmetic; it means the list was written from memory or drifted, and the seat's recount is the only number that binds. Related: SN-035 (phantom-citation class); SN-01456 (audit the state, not the claim); SN-1720 (preserve-out-at-classification — evidence at the moment, not after).

## 🟢 MACHINE NOTE
```json
{
  "sn": "SN-01724",
  "lesson": "When a parent receipt names a count and lists items, the re-deriving seat recounts from zero on exact head bytes and reports three numbers — parent-count, list-sum, reproduced-count — because inheriting the parent's number can certify a phantom.",
  "applies_when": ["verify", "re-derive", "receipt", "classification"],
  "enforcement": "any re-verification receipt that certifies a parent's count must state the parent's claimed count, the sum of the parent's listed items, and the reproduced count on exact head bytes; a receipt that certifies a count without all three numbers is incomplete and bounced",
  "decision_changed": "re-verifying a parent receipt's failure/count claim: recount from zero on exact head bytes and report the three numbers, instead of trusting the parent's number",
  "falsifier": "a run where parent-count == list-sum == reproduced-count across several re-derivations would show the extra recount as pure cost — the note holds on its single counterexample (9 claimed / 8 listed / 7 reproduced, one 'failure' green on merged bytes)",
  "mechanism": "inherited counts compound the parent's arithmetic slips into certified facts: each downstream seat that trusts the number extends the error's life. Recounting from zero breaks the inheritance chain at the point of re-derivation, and the delta (list-sum vs claimed, reproduced vs listed) is itself a finding about the parent's evidence hygiene.",
  "evidence": "hidden_files/twelve-lane-receipts/gap-gap-t1032-lane4.md (2026-10-20 08:38-09:05 UTC, 9.0/10, Lane 4 Mason hat): parent's '9 failures' list summed to 8 (1+6+1); re-deriving seat re-ran the named set on exact head bytes (triple-agree pin 973177d4): named pytest test FAILED (assert 10==9), guard_liveness 6/7 failed, load_bearing_claims 15/15 PASSED — NOT reproduced; reproduced count 7; CLAIM 3 green on merged squash commit 597803d8 (freshness-stamp diff only). Mirror lesson: 'Inheriting the parent's count would have certified a phantom.'",
  "companions": "SN-035 (phantom-citation class); SN-01456 (audit the state, not the claim); SN-1720 (preserve-out-at-classification — evidence at the moment, not after)"
}
```
