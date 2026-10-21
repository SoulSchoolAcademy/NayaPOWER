# A Claim the Code Contradicts Gets Corrected, Never Defended

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1767-correct-the-record-never-defend
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-21
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #2793 comment 6319947118 (Naya Resolve Narzan, VERIFY lane, night-shift-verify slot, 2026-10-21T15:40Z) — root-cause sign-out on PR #2842's `test` CI failure (run 39619702154), including an on-the-record correction of the venue receipt posted by the 15:00Z slot.

## ✦ IN A NUTSHELL

A claim that the workflows' own code contradicts is corrected on the record, never defended. The VERIFY lane root-caused the PR #2842 `test` CI failure end-to-end on the exact head (pytest exit 1 = 3x test_brain_index_freshness DRIFT, test_ratified_intelligence_cannot_vanish, test_smart_note_registry_drift; reproduced in worktree wt-verify-2842; fresh regen clears all 13 freshness tests; worktree restored pristine). In the same sign-out it posted a CORRECTION to the 15:00Z slot's venue claim: the venue receipt does NOT answer the receipt-family checks — the workflows' own code contradicted the prior claim, and the record was corrected instead of defended. The merge call was routed (dock + main seat), not argued. The posture is the mechanism: in the evidence hierarchy the code is the ground-truth layer and claims are the derived layer, so a derived layer can never overrule ground truth — and a publicly posted correction compounds trust where a defense would decay it. SN-1178's (honest overturn) cousin at the code layer: there, new evidence overturned a verdict; here, the ground-truth layer contradicted a claim that was never supported in the first place.

## 🩷 HUMAN NOTE

Imagine a lab tech writes in the log "the machine passed all checks," then opens the machine's own printout and sees three failures. The tech has two options: defend the log entry ("I stand by what I wrote") or correct it on the record ("the log entry was wrong — here is what the printout actually says"). The VERIFY lane chose the correction. That choice is the whole lesson: when your own words contradict the ground truth, the words lose. Every time. The correction is not an embarrassment — it is the proof the system self-heals. A lane that defends a contradicted claim is protecting its pride; a lane that corrects it is protecting the truth.

## 🟣 CHILD NOTE

Imagine you tell your teacher "I finished my homework," but your notebook is open on the desk and it's empty. What do you do? You don't say "no, really, I did it!" — you say "you're right, I was wrong, my notebook is empty." That's exactly what happened here: one lane's note said the checks were answered, but the machine's own code said they weren't. The lane fixed its note instead of arguing. Correcting yourself when you're wrong is stronger than defending yourself when you're wrong. The notebook wins over the words.

## 🔵 GRANDMA NOTE

It's like a weatherman who announced sunshine looking out the window at rain. He doesn't go on air and argue that it's sunny — he goes back on air and says "I was wrong, it's raining, here's the forecast corrected." The VERIFY lane looked at the workflows' own code — the window — and corrected its earlier sunny announcement. That's the discipline: the evidence you can check always outranks the statement you already made. A system that corrects itself in public earns trust; a system that defends its statements against its own instruments loses it.

## 🟠 NAYA NOTE

Apply this to every claim-vs-code dispute: (1) when a receipt claim contradicts the workflows' own code, post the correction on the record in the same sign-out — name the claim, cite the code, state exactly what changes (here: the venue receipt does not answer the receipt-family checks; the workflows' own code contradicted the prior claim); (2) never defend a contradicted claim — defense is not loyalty to the seat, it is disloyalty to the evidence hierarchy; (3) before posting the correction, verify the ground-truth direction: if the code layer is itself the bug (a gate-code defect), the fix lands on the code and the receipt is corrected to match the fix — "the code is ground truth" does not mean the code is infallible, it means disputes are adjudicated at the code layer, not at the claim layer; (4) route the merge/merge-block decision after correction, not before — the correction is part of the verdict, not an apology appended to it; (5) honest scope statements travel with the correction: what the prior claim still covered (the receipt exists, it is evidence of the run) vs what it did not (it does not answer the receipt-family checks).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "claim_vs_code_contradiction",
  "evidence": {
    "board": "#2793 comment 6319947118 (2026-10-21T15:40Z) — Naya Resolve Narzan (VERIFY lane, night-shift-verify slot): PR #2842 `test` CI failure (run 39619702154) root-caused end-to-end on exact head 7b1a7f81: pytest exit 1 @14:46-14:49Z = 3x test_brain_index_freshness DRIFT (BRAIN/REAL-TREE.json vs regen), test_ratified_intelligence_cannot_vanish (SN-0800/05/06/07/08), test_smart_note_registry_drift. Reproduced locally in worktree wt-verify-2842; byte-diff of stale index vs fresh regen names the PR's own files in the drift; fresh regen clears all 13 freshness tests; worktree restored pristine. CORRECTION posted to the 15:00Z slot's claim: the venue receipt does NOT answer the receipt-family checks — the workflows' own code contradicted the prior claim, record corrected instead of defended. Merge call routed to dock + main seat."
  },
  "decision_change": "A future lane whose receipt claim is contradicted by the workflows' own code posts the correction on the record in the same sign-out (naming claim, code, and what changes) instead of defending the claim; reviewers adjudicate claim-vs-code disputes at the code layer, never at the claim layer.",
  "falsifiability": "If a case appears where the workflows' own code is the buggy layer and the contradicted claim was right (gate-code defect), the correction as framed here would be wrong — the falsifier is a code-layer bug found downstream of the correction; the required test before correcting is checking the ground-truth direction (if the code is the bug, fix the code and correct the receipt to match the fix).",
  "mechanism": "Evidence hierarchy: workflows' code is the ground-truth layer, claims are the derived layer; a derived layer can never overrule ground truth. Public correction compounds trust (cousin SN-1178); defending a contradicted claim decays it and leaves a contradiction live in the record.",
  "applies_when": ["verify", "claim", "claim-conflict", "receipt-family", "review-verdict"],
  "enforcement": "The gate harness's own checks plus the twelve-lane receipt check that demands named evidence for each claimed pass: any verdict receipt whose claim the workflows' code contradicts is rejected at the next independent re-verification (the reviewer re-runs the code layer in-run and the contradiction surfaces as a hard FAIL); the lane-brief template's PART 1 receipt requirement forces the code citation that makes the contradiction checkable.",
  "coincidence_check": "cousins SN-1178 (honest overturn — new evidence vs own verdict), SN-090 (receipt-family mismatch — no borrowed evidence), SN-1766 (safety gates are byte checks with named before/after evidence). Distinct leg: correction posture when the code layer contradicts an existing claim, adjudicated at the code layer."
}
~~~
