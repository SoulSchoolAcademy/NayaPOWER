# Classify a Contract-Expanding Merge's RED as Test Defect or Product Defect Before Touching Either — Compare the Harness's Fabricated World to the Shipped Contract

**Intelligent Block:** IB-SMART-NOTE-20261007-sn0570-test-defect-vs-product-defect-classification
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-07
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Kernel Tests run 37678235721 on main `b981b764` (2026-10-07): Node 554/554 PASS, Python 9 FAIL / 1022 PASS / 11 SKIP — all 9 failures from `tests/test_production_promotion_receipt_handshake.py` raising `FileNotFoundError: 'learning-act-proof-run.json'`. Diagnosed on #1354 comments 6045756874 (2026-10-07T19:59:04Z), 6045788529 (20:01Z, Naya 2 independent battery), 6045887712 (20:07Z, Naya 4 verify cycle). Repaired by PR #1761 (second-seat ACK #1354 comment 6045835989).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

PR #1759 (merged 2026-10-07 19:56Z) expanded the governed production receipt contract: it added the fifth canonical child proof (`learning-act-proof-run.json`) to `governed-supabase-production-deploy.yml` (reader at lines ~590–594, plus new asserts and `headSha`/`conclusion=="success"` wiring). The very next Kernel run on exact tip bytes went RED in exactly the place you'd expect a product defect — 9 Python failures. But the product was fine. The test harness's `run_receipt()` was still fabricating the old four-child world (`act-proof-run.json` only); the shipped contract had moved to five. **Failure class: TEST DEFECT.** The diagnosis was made by holding two artifacts side by side — what the harness fabricates vs what the shipped contract requires — and finding the mismatch in the harness, not the product.

The repair (PR #1761) changed exactly one file (`tests/test_production_promotion_receipt_handshake.py`, +35/−4): create the missing learning-ACT child run fixture, assert its run id binds into the durable parent receipt, extend the source-SHA-mismatch and non-success falsifiers to the fifth child. No production workflow, runtime, or authority behavior changed. Independent second-seat verification (detached-head, exact bytes) confirmed the falsifiers are non-vacuous — the live asserts exist in the shipped workflow — and exact-head CI came back 1033 passed / 11 skipped.

Two embedded lessons in one event. First, the classification method: **on a RED right after a contract-expanding merge, compare the harness's fabricated world against the shipped contract before suspecting the product.** A stale harness fabricates yesterday's contract; the RED it produces describes the test's age, not the product's health. The corollary: when the contract grows, the harness's fixtures are part of the merge's blast radius — if the merge doesn't update them, the RED is the merge's debt, and the repair belongs to the harness.

Second, the lane discipline: Naya 2's battery independently reproduced the RED on byte-identical bytes, corroborated the TEST DEFECT root cause — and then **stood down on the repair** because the seat behind comment 6045756874 already owned it (SN-0236: one repair per RED class). Classification got shared openly; the repair stayed single-owned. Two seats classifying the same RED is convergence; two seats repairing it is a collision.

## 🩷 HUMAN NOTE

Your city passes a new law: every building now needs five inspections, not four. The next morning the inspector fails every building in town — not because the buildings are unsafe, but because his clipboard still lists only four inspections and he marks the fifth one "missing." The buildings are fine; the clipboard is outdated. You don't condemn the buildings — you print a new clipboard. And when two inspectors show up at the same building, one of them steps back: one inspection per building, or you get two clipboards disagreeing about everything.

## 🟣 CHILD NOTE

You learn a new word at school, and the spelling test the next day includes it — but your study list from last week doesn't have it. You get it "wrong," but the word isn't the problem; your study list was old. Nobody rewrites the dictionary because of a bad study list. And if two friends both volunteer to re-study the list, one of them should pick a different job — two people re-writing the same list just makes a mess.

## 🔵 GRANDMA NOTE

Dear, it's like updating your address with the bank and then getting a letter saying "we couldn't reach you" — they sent it to the old address on their records. The letter wasn't lost because of anything you did wrong; their records were old. You update their records, you don't change your house. And if two grandchildren both offer to call the bank about the same mix-up, one of them hangs up — two callers, one problem, never works.

## 🟠 NAYA NOTE

When a RED appears on or near a contract-expanding merge:

1. **Hold the two artifacts side by side:** what the harness fabricates (fixtures, synthetic receipts, expected shapes) vs what the shipped contract now requires (readers, asserts, counts). The RED's home is wherever the mismatch lives.
2. **Classify TEST DEFECT vs PRODUCT DEFECT explicitly in the report.** A stale harness fails loudly and points at the product; naming the class protects the product lane from being patched for the harness's debt.
3. **Treat the harness's fixtures as part of the merge's blast radius.** If the merge that expanded the contract didn't expand the fixtures, the RED is that merge's debt — route the repair to the harness, not the product.
4. **Verify the repair's falsifiers are non-vacuous.** The extended falsifiers must fail on a genuinely weakened contract (check the live asserts exist in the shipped workflow), or the repair is just a green-washer.
5. **Stand down on claimed repairs (SN-0236).** Independent reproduction + public classification is convergence; a second repair PR is a collision. Record your battery verdict in your own ledger and move on.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "test_fixture_stale_after_contract_expansion",
  "evidence": {
    "kernel_red": "run 37678235721 on main b981b764 — Node 554/554 PASS, Python 9 FAIL / 1022 PASS / 11 SKIP, all 9 from tests/test_production_promotion_receipt_handshake.py → FileNotFoundError: 'learning-act-proof-run.json'",
    "contract_expansion": "#1759 merged 2026-10-07 19:56Z added the fifth canonical child proof (learning-act-proof-run.json) to governed-supabase-production-deploy.yml (reader lines ~590–594, headSha + conclusion asserts)",
    "harness_age": "run_receipt() in the test still fabricated only act-proof-run.json (four-child world)",
    "classification": "#1354 6045887712 — 'Failure class: TEST DEFECT — #1759 added the fifth canonical child proof to the governed receipt contract; the harness fabricated only four. Product contract was correct; the test was stale.'",
    "repair": "PR #1761 — one test file only (+35/−4), creates learning-ACT child fixture, binds run id into parent receipt, extends source-mismatch and non-success falsifiers; second-seat ACK #1354 6045835989; exact-head CI 1033 passed / 11 skipped",
    "no_duplicate": "#1354 6045788529 — Naya 2 reproduced the RED on byte-identical bytes and stood down on the repair (lane owned by 6045756874), per SN-0236"
  },
  "rule": "compare_harness_fabrication_to_shipped_contract_before_classifying_red",
  "procedure": [
    "on a RED at/near a contract-expanding merge, diff the harness's fabricated inputs against the shipped contract",
    "classify TEST DEFECT vs PRODUCT DEFECT explicitly before changing anything",
    "route fixture staleness to the harness; never patch the product for the harness's debt",
    "verify extended falsifiers are non-vacuous against the shipped bytes",
    "stand down on repairs another lane owns; publish the battery verdict instead"
  ],
  "related": ["SN-0392 (the first RED is the only RED)", "SN-0554 (a stale-base RED is not a current-main RED)", "SN-0236 (one repair per RED class — never duplicate)", "SN-0493 (a decision expires when the tip moves)", "SN-0569 (assertion strength — this note's sibling on regression design)"]
}
~~~
