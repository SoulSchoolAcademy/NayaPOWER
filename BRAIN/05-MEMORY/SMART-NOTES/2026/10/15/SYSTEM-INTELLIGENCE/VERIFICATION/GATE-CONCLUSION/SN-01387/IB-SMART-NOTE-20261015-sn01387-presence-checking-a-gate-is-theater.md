# Presence-Checking an Enforcement Gate Is Theater — Read the Gate's Conclusion, Not Its Artifacts

**Intelligent Block:** IB-SMART-NOTE-20261015-sn01387-presence-checking-a-gate-is-theater
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-15
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 05:08 PDT smart-note-distillation tick (2026-10-15) from `hidden_files/shared-state.json` `merge_watch_2533.correction_2026_10_15` — the main-seat adjudication (board comment 6186662487, verified on live bytes) that WITHDREW the director's CLEAN verdict on PR #2533. Named failure mode #60.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

PR #2533 ("[DRAFT] Activation: READ-ME-FIRST — ultimate new-Naya activation instruction set", merge `59e8a9afa22cf456565bfac0f2b52551f8a0dd6e`, merged 2026-10-13T23:33:49Z) was judged CLEAN: its PR body carried a real 3-pass receipt (pass-1 8.0 + named holes, repairs listed, pass-2 9.0 + remaining holes, pass-3 confirm, exact head `ea6c9ef8` certified, does-NOT-claim section), plus an independent Verity 9.0/10 APPROVE at the exact head. Text present, receipt present, reviews present.

The main-seat adjudication (6186662487, verified on live bytes) withdrew CLEAN and ruled the merge NON-COMPLIANT: the **'Team review + scorecard receipt' branch-protection gate FAILED 3 times at the merge commit** — of 406 check runs, code CI was GREEN and the 3 failures were all this gate — and the merge went through via the org app account anyway. Delta's NON-COMPLIANT verdict stands.

Root cause of the director's miss, in the adjudication's own words: **"the merge-receipt watch checks receipt TEXT in the body, not the gate check-run CONCLUSION at the merge commit — presence-checking a gate is theater."** A gate's text artifact (the receipt in the body) is a *claim*; the gate's check-run conclusion is the *enforcement's output*. Presence and outcome are independent variables — the watch verified the claim side and was blind to the outcome side, so a failed gate passed silently.

Fix owed (review lane / director): the watch must read the gate's check-run conclusion at the merge commit; **gate failure → RECEIPT BREACH regardless of body text**. Open question carried for Shawn (morning): authorized admin bypass, or is the check advisory in practice? Named failure mode #60.

## 🩷 HUMAN NOTE

A school requires a permission slip signed for every field trip. The office checks that a slip is *in the folder* — never whether the signature is real. One day a trip goes out with a folder full of unsigned slips, because the check was "is there paper in the folder," not "is the permission granted." Presence of paper and granted permission are different things, and a check that only looks for paper will pass a trip that was never approved.

## 🟣 CHILD NOTE

The rule is "no dessert until homework is checked." Mom's check is: "is there a worksheet on the table?" The worksheet is on the table — but it's blank. Dessert is served. The check looked for the *thing*, not the *done-ness*. A smart check reads the worksheet, not just sees it.

## 🔵 GRANDMA NOTE

It's like checking that a smoke detector is *on the ceiling* instead of checking whether it *beeps when you press the button*. The one on the ceiling with dead batteries passes the first check and fails at the only moment that matters. Test the beep, not the bracket.

## 🟠 NAYA NOTE

Apply this to every enforcement watch: (1) enumerate what the gate's *conclusion* is and where it lives (check-run conclusion at the merge commit — not the PR head, not the body text); (2) a verdict built on artifact presence (receipt text in body, stamp in file, marker in comment) must be re-derived against the conclusion, or withdrawn — presence is the claim, conclusion is the enforcement; (3) the #2507 corollary: a gate verdict is also time-bound — the 04:56:35Z FAILED receipt-gate run was correct-at-measurement and STALE after the review landed; conclusions must be pinned to the exact commit they judge (L280/L285); (4) when a bypass path exists (org app account, admin merge), the watch must name it explicitly and the open question goes to Shawn — "authorized admin bypass, or is the check advisory in practice?" is a decision, not a shrug; (5) name the failure mode (#60) so the next watch that repeats it is recognizable on sight.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "presence_checked_gate_theater",
  "evidence": {
    "adjudication": "board comment 6186662487 (main-seat adjudication, verified on live bytes) — director's CLEAN on merge_watch_2533 WITHDRAWN",
    "pr": "PR #2533 '[DRAFT] Activation: READ-ME-FIRST — ultimate new-Naya activation instruction set', merge_commit 59e8a9afa22cf456565bfac0f2b52551f8a0dd6e, merged 2026-10-13T23:33:49Z via org app account",
    "body_receipt": "3-pass receipt present in body (pass-1 8.0 + holes, repairs, pass-2 9.0 + remaining holes, pass-3 confirm, exact head ea6c9ef8 certified, does-NOT-claim section) + Verity 9.0/10 APPROVE at exact head",
    "gate_fact": "'Team review + scorecard receipt' branch-protection gate FAILED 3x at the merge commit (406 check runs: code CI GREEN; the 3 failures are all this gate) — merge went through anyway",
    "root_cause": "the merge-receipt watch checked receipt TEXT in the body, not the gate check-run CONCLUSION at the merge commit",
    "fix_owed": "watch must read the gate's check-run conclusion at the merge commit; gate failure → RECEIPT BREACH regardless of body text (review lane / director)",
    "open_question": "for Shawn (morning): authorized admin bypass, or is the check advisory in practice? Named failure mode #60",
    "source": "hidden_files/shared-state.json merge_watch_2533.correction_2026_10_15"
  },
  "rule": "presence_checking_an_enforcement_gate_is_theater_read_the_gates_conclusion_at_the_commit_it_judges",
  "procedure": [
    "for every enforcement gate, name its conclusion and where it lives: check-run conclusion at the merge commit — not the PR head, not the body text",
    "re-derive any presence-based verdict against the conclusion, or withdraw it",
    "pin gate verdicts to the exact commit they judge (L280/L285: a FAILED run correct-at-measurement goes STALE when the world moves)",
    "name the bypass path explicitly (org app account, admin merge); the bypass-vs-advisory question is a decision for Shawn, not a shrug",
    "name the failure mode (#60) so the recurrence is recognizable on sight"
  ],
  "decision_change": "every merge/enforcement watch must be rebuilt to read gate check-run conclusions at the merge commit — any watch that only checks body-text presence must have its past verdicts re-derived or withdrawn, because #2533 proves presence and outcome diverge in production",
  "falsifiability": "re-run the watch conclusion-based on a sample of merged PRs: if conclusions and body-presence always agree, the distinction is redundant — #2533 is the counterexample that currently falsifies that redundancy",
  "mechanism": "a gate's text artifact is the claim side; the check-run conclusion is the enforcement side — they are independent variables, so verifying only the claim side lets a failed gate pass silently; enforcement output, not artifact presence, is what a watch must read",
  "related": ["merge_watch_2507 (L280/L285 gate-verdict staleness — the time-bound corollary)", "FM#31 (self-condition merges — the sibling gate-bypass class)", "SN-1385 (premise rot — the sibling 'verify the world, not the bytes' lesson)"]
}
~~~
