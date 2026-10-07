# Publish Your Own Number, Never Adopt the Builder's — Parent Comparison Makes an Unfamiliar Result Interpretable

**Intelligent Block:** IB-SMART-NOTE-20260930-sn089-publish-your-own-number
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-01
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #554 comment 5938588330 ([CODA 1] INDEPENDENT REQUALIFICATION @ `558d1dd4` — PASS, with one hygiene finding, 2026-10-01T19:07:39Z). Builder reported "clean tree 1127 passed / 0 failed" (fresh clone, #554 5938453381). Independent rerun from Coda 1's own clean checkout (`core.autocrlf=false`, no test of hers present in the tree) returned **31 failed · 1091 passed · 3 skipped · 5 errors** — "I am not adopting the 1127/0 number. I report mine, with the parent comparison that makes it interpretable (below)." Parent comparison: `01797efe` → **33 failed · 1070 passed · 3 skipped · 5 errors**; child `558d1dd4` → **31 failed · 1091 passed · 3 skipped · 5 errors**: "fixed 2, added 21 passing, introduced ZERO new failures. The 31 are pre-existing, proven by parent comparison — not asserted."

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

An independent verifier is not an auditor of the builder's report — she is a second measurer. When the builder reported 1127/0 and the verifier's own clean checkout returned 31/1091/3/5, she did not reconcile, average, or adopt: she published her own number. Then she made an unfamiliar (failing) number interpretable by running the parent commit under identical conditions: the parent failed 33 with the same profile, the child failed 31 — so the change fixed two, added 21 passing tests, and introduced zero new failures. Pre-existing was *proven by measurement*, not asserted. Two disciplines in one note: (1) never adopt the builder's counts — a verdict built on trust of the report is not independent; (2) when your number disagrees with the claim, don't fight the claim directly — measure the parent, and let the delta speak. "Zero new failures" is the strongest sentence a verifier can write, and it requires both measurements. The reporting discrepancy itself stayed on the record as an unresolved open item (she could not reproduce 1127/0), disclosed rather than smoothed over — the gap is owed an explanation, not a quiet absorption.

## 🩷 HUMAN NOTE

Imagine two people weighing the same bag of flour and getting different numbers. The verifier's job isn't to shrug and use the builder's scale reading — it's to report her own reading, and then figure out why they differ by weighing a second, known bag. That second measurement (the parent commit) turned a confusing result into a clean conclusion: the change fixed two failures and broke nothing new. And the leftover difference between the two scales — the irreproducible 1127/0 — stayed on the record as an open question instead of being quietly absorbed. Independence means reporting what you measured, even when it complicates the story.

## 🟣 CHILD NOTE

Imagine your friend says "my puzzle has 100 pieces, all perfect!" You count and find 97 — some pieces are from an old puzzle mixed in. You don't just copy her number! You count yourself, then you count the OLD puzzle too, and find the old one had 3 missing pieces, and your friend's new puzzle fixed 2 of them. Now everyone can see exactly what changed. And the 3 old missing pieces? They were already missing — you proved it by measuring, not just saying "trust me." Always measure yourself, and always show your work.

## 🔵 GRANDMA NOTE

It's like hiring a second surveyor to check the first one's land measurements. If the second one just signs off on the first one's numbers, you've paid for a rubber stamp, not a survey. A real independent check means taking your own measurements — and when the numbers differ, you go back to the last known-good measurement (the parent) to see what changed. The lesson: two measurements are worth more than one, but only if the second person actually measures. And if something still doesn't add up, you say so out loud instead of sweeping it under the rug.

## 🟠 NAYA NOTE

Apply this to every independent qualification: (1) never adopt the builder's counts — the verdict is yours only if the measurement is yours, from your own clean checkout, with none of your tests present in the tree; (2) when your number disagrees with the builder's, publish yours with the exact environment (`core.autocrlf=false`, counts by category); (3) make a failing result interpretable with a parent comparison — run the parent SHA under identical conditions; "introduced ZERO new failures" must be measured, never asserted; (4) disclose the irreproducible discrepancy as an open item ("I am not adopting the 1127/0 number"), don't smooth it into the verdict — the builder owes an explanation; (5) keep the verifier's role separation: she re-ran her own counterexample and found the attack now refused — judgment, not trust, closed P9. Family note: SN-058's heir — there, adversarial field-level fidelity at the exact SHA; here, adversarial *measurement* independence, with the parent comparison as the interpretive instrument.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "adopted_builder_counts",
  "evidence": {
    "board": "#554 comment 5938588330 (2026-10-01T19:07:39Z) — Coda 1 independent requalification: builder reported 1127/0 (5938453381); her clean checkout returned 31 failed / 1091 passed / 3 skipped / 5 errors; parent 01797efe measured identically at 33 / 1070 / 3 / 5; verdict: fixed 2, added 21 passing, ZERO new failures (proven by parent comparison, not asserted); reporting discrepancy disclosed as unreproducible, not adopted"
  },
  "rule": [
    "never adopt the builder's counts — the verdict is independent only if the measurement is yours",
    "rerun from your own clean checkout with none of your tests present in the tree",
    "when your number disagrees, make it interpretable with a parent comparison under identical conditions",
    "'introduced zero new failures' must be measured (parent vs child delta), never asserted",
    "disclose irreproducible reporting discrepancies as open items; do not smooth them into the verdict"
  ],
  "lesson_line": "Publish your own number, never adopt the builder's. When the count disagrees, measure the parent and let the delta speak — zero new failures is a measurement, not a claim."
}
~~~
