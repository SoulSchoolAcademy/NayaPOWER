# "Confirm the Fix" and "Re-apply the Definition" Are Different Verbs

**Intelligent Block:** IB-SMART-NOTE-20261015-sn1443-confirm-fix-vs-reapply-definition  
**Smart Note:** SN-1443  
**Truth state:** CANDIDATE  
**Scope:** PRIVATE canonical runtime object; this file is a PUBLIC DERIVED VIEW authorized by the human director.  
**Captured:** 2026-10-15  
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This Markdown file is **not** a second source of truth.

## ✦ IN A NUTSHELL

A spot-check that only re-tests the named miss verifies the *patch*; a spot-check that re-applies the full *definition* on a disjoint sample indicts the *triage*. The distill-chain lane proved the difference live: the two named ratification misses were verified and amended into feed-distillation-554.md — but the re-applied spot-check (seed 20261016, n=30, a different sample from the parent's) surfaced TWO review-shaped misses the parent's triage never full-read (5953414793 Naya 2's team-review round; 5914610501 Naya 4's H13-H15 response) — both titled "review", so even a keyword digest should have caught them. The second sample didn't fail the amendment; it failed the gate that made the amendment necessary: the full-read selection gate, not the digest.

## HUMAN NOTE

The operating rule: when you verify a repair, run two different verbs. Verb one — "confirm the fix" — re-tests the named miss and proves the patch landed. Verb two — "re-apply the definition" — runs the full rule on a fresh, disjoint sample and proves the triage gate works. If you only run verb one, you can close every named gap while the broken gate keeps producing unnamed ones.

The lane closed at 9.5/10 by doing exactly this: the named gap closed, and the deeper root cause (the full-read gate misses review-shaped posts) was NAMED in Holes and deferred as a machinery brief for another seat — not silently absorbed. "Closing the named gap while naming the deeper cause is 9.5/10; silently absorbing the deeper cause would have been 7."

## CHILD NOTE

You fixed two spelling mistakes in your essay — but did you actually re-read the whole essay, or just those two words? If you only re-checked the two words, you don't know whether your spell-checker is still missing other mistakes. The smart move: check the two words AND re-run the checker on a different page.

## GRANDMA NOTE

It's the difference between tasting the soup you just salted (did that fix work?) and tasting a second bowl with the same recipe (does the recipe work?). We tasted the second bowl and found the recipe itself was skipping ingredients — the cook's checklist, not the salt.

## NAYA NOTE

**Verification doctrine:** match the verification scope to the claim scope. An instance claim ("these two misses are fixed") is verified by re-testing the instances. A gate claim ("the triage catches review-shaped posts") is verified only by re-applying the definition to a disjoint sample. Re-testing the named miss alone is the most common way a broken triage survives its own repair — the patch gets confirmed, the gate never gets exercised.

**Spot-check design rule (earned 2026-10-15):** the confirming sample and the definition sample must be disjoint (different seed, different n-set), and the definition sample must be large enough to plausibly contain a second miss (n=30 here). A second sample drawn from the same well tests nothing new.

**Mechanism — why it works:** instance failure and gate failure are different layers. The named miss is an instance; the full-read selection gate is the mechanism that produced it. "Confirm the fix" operates at the instance layer; only "re-apply the definition" reaches the mechanism layer. A selection gate that never sees a second sample is an untested gate wearing a passing grade.

**Named next actions from the receipt:** (1) Lane 5 amendment brief for the two review essence lines (5953414793, 5914610501); (2) triage review-shape detector is a machinery brief for another seat — no scope creep.

## 🟢 MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "smart_note": "SN-1443",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "lesson": "confirm_the_fix_vs_reapply_the_definition",
  "verbs": {
    "confirm_the_fix": "re-test the named miss; verifies the PATCH; operates at the instance layer",
    "re_apply_the_definition": "run the full rule on a disjoint sample; verifies the GATE; operates at the mechanism layer"
  },
  "mechanism": "instance failure vs gate failure are different layers; only a disjoint second sample exercises the selection gate",
  "spot_check_design": {
    "disjoint_samples": true,
    "example": "seed 20261016, n=30, different sample from the parent's",
    "rule": "the confirming sample and the definition sample must come from different wells"
  },
  "proof": {
    "named_misses_fixed": ["5953414793 (Naya 2 team-review round)", "5914610501 (Naya 4 H13-H15 response)"],
    "both_titled_review": "even a keyword digest should have caught them -> failure is the full-read selection gate, not the digest",
    "deeper_cause_named_not_absorbed": "full-read gate misses review-shaped posts -> machinery brief for another seat"
  },
  "decision_change": "when closing a triage/amendment, verify with BOTH verbs: confirm the named misses, then re-apply the full definition on a disjoint sample; never let a definition sample equal the confirmation sample",
  "falsifiable_by": "a named-miss-only re-test that indicted a triage gate itself would collapse the distinction (as of 2026-10-15, no such case: every gate failure surfaced required the second disjoint sample)",
  "cousins": {}
}
~~~

## 🧾 PROOF / PROVENANCE

- **Evidence:** hidden_files/lesson-broadcast.md [t0489] (Dispatcher mirror, gap-gap-t-distill-chain-lane5-1715 COMPLETE 9.0/10, Lane 5 Seeker, Naya Clarity, 2026-10-15) — two named ratification misses verified on live bytes and amended into feed-distillation-554.md; re-applied spot-check (seed 20261016, n=30, disjoint sample) surfaced the two review-shaped misses the parent's triage never full-read.
- **Evidence:** hidden_files/lesson-broadcast.md [t0495-lane5] (gap-gap-gap-t-distill-chain-lane5 9.5/10, 2026-10-15) — closed the named gap while naming the deeper cause (full-read gate misses review-shaped posts); triage review-shape detector deferred as a machinery brief, not absorbed.

## ⚠️ TRUTH BOUNDARY / UNCERTAINTY

This note captures a verification doctrine earned from one distill-chain wave. It does not prove the optimal disjoint-sample size, nor that every repair admits a cheap second sample — some domains can't afford two. Truth state remains CANDIDATE until the pattern repeats across a second lane.

## ➜ NEXT ACTION / SUCCESS CONDITION

Keep retrievable; apply at every fix-verification: name both verbs, run both, report both. Compound only what evidence supports.
