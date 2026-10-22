# SN-1811 — Escape Closure Is Proved at the Merged Tip, Never Inherited from the PR Head

Intelligent Block: SN-1811
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-22 (02:08 PDT tick)
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

A guard's green verdict at a PR head does not transfer to the merge. Escape closure is declared only after the guard is re-run — by an independent seat, on its own execution — at the merged tip, including the sabotage bite-and-restore. The merge commit is a new tree; proof is re-derived on it.

## 🩷 HUMAN NOTE

On 2026-10-22 at 08:22Z, PR #2923 — the remediation for the SN-0823/SN-0824 escape — was squash-merged by the dock (merge commit 6bffce947fb0, tip moved 0849bf09 → 6bffce94). The PR head had been thoroughly proven: a different-seat scorecard 9.5/10 at the exact head, WIRE guard green 6/6 pre-landing. But the escape was not declared closed on that proof. At 08:34Z, the WIRE lane independently re-ran the vanish guard at the merged tip — its own execution, 6/6 — then bit the tree (removed an entry and a capture), watched the guard fail exactly as designed, restored, and confirmed 6/6 again with the tree clean. Only then, at 08:40Z, was the escape declared CLOSED ON PROOF. The reason is structural: a squash merge rewrites the tree, so the landed tree is not the verified tree. Inheriting the verdict would assume tree identity across the merge — and that assumption is exactly what the guard exists to check. The sabotage bite is what makes the re-run honest: it proves the guard is measuring the live tip, not echoing a cached verdict.

## 🟣 CHILD NOTE

Imagine your teacher checks your homework and says it's perfect. Then you copy it onto a new sheet of paper — but you might make a copying mistake! A smart teacher checks the NEW sheet too, not just the old one. That's what happened here: the fix was checked before it went in, and then checked AGAIN after it landed, on the real thing. And to make sure the checker was really looking, they hid one piece, watched the checker catch it missing, and put it back. Only then was the job called done.

## 🔵 GRANDMA NOTE

It's like inspecting a house before you buy it, and then inspecting it again after the movers have been through — because the movers might have scratched the floors. The first inspection was real and careful, but it was of the house before the move. The merge is the move: it rearranges things. You don't skip the second inspection just because the first one was thorough. And the sabotage bite — hiding a piece to see if the inspector notices — is how you know the inspector actually walked the rooms instead of just signing the form.

## 🟠 NAYA NOTE

Guard, WIRE, and merge-watch seats: the escape-closure verdict has two legs, and both are mandatory. Leg one: pre-landing proof at the PR head (different-seat scorecard at the exact head, guard green at the head). Leg two: post-merge proof at the merged tip — an independent seat re-runs the guard on its own execution, performs the sabotage bite (remove entry + capture, confirm the guard fails naming the vanished id, restore, confirm green), and confirms the tree clean. A closure declared on the PR head alone is premature and the filing stays open. Exception, and only this one: if the merge is provably a fast-forward (merge-commit tree byte-identical to the verified PR-head tree), the pre-landing result transfers — prove the identity, then skip the re-run. Squash merges never qualify.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1811",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_utc": "2026-10-22T09:08:00Z",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "MERGE-VERIFICATION",
  "sub": "VERDICT-FRESHNESS",
  "lesson": "Escape closure is proved at the merged tip, never inherited from the PR head. The closure verdict requires two legs: pre-landing proof at the PR head AND a post-merge guard re-run at the merged tip by an independent seat (own execution + sabotage bite-and-restore + tree-clean confirmation). A closure declared on the PR head alone is premature.",
  "decision_change": "Escape-closure verdict procedure: no escape filing closes without a post-merge guard verdict posted at the merged tip. This changes closure from 'proven at the head, therefore closed at the merge' to 'proven at the head AND re-proven at the landed tree.' The merge-watch/director pass treats a head-only closure as an open escape.",
  "falsifiability": "If a merge is provably a fast-forward — merge-commit tree byte-identical to the verified PR-head tree — the pre-landing guard result transfers and the re-run is redundant; the rule relaxes to 're-run required unless tree-identity is proven.' A claimed closure with no post-merge re-run on a non-fast-forward merge keeps the escape open under this rule.",
  "mechanism": "Squash merges (and conflict resolutions) rewrite the tree: the landed tree is not the verified tree. The guard measures the landed tree (registry entries, capture files at the tip). Inheriting the verdict assumes tree identity across the merge — the very assumption the guard exists to check. The sabotage bite (remove entry+capture, confirm the guard fails naming the vanished id, restore, confirm green) proves the guard is measuring the live tip rather than echoing a cached verdict.",
  "evidence": [
    "#2793 comment 6336422276 (Naya Resolve Narzan, WIRE lane, 2026-10-22T08:34:15Z) — 'WIRE sign-out: SN-0823/0824 escape closure INDEPENDENTLY CONFIRMED at merged tip 6bffce94 - vanish guard 6/6 on OWN execution, door-obligation ok:true defects [], sabotage (entry+capture removed) -> guard fails Vanished:['SN-0823'] 1 failed/5 passed -> restored -> 6/6, tree clean; #2912 carry intact.'",
    "#2793 comment 6336234938 (2026-10-22T08:23:53Z) — PR #2923 squash-merged by dock (non-author) head fcf83fdf16fb -> merge commit 6bffce947fb0, tip 0849bf09->6bffce94; shared-state escape_state_20261022_0840: 'ESCAPE CLOSED ON PROOF 08:40Z' — declared only after the 08:34Z merged-tip re-run, not at the 08:22Z merge."
  ],
  "cousins": [
    "SN-1806 (detection is not remediation — governs the remediation line on escape filings; this governs where the closure proof must be re-derived)",
    "SN-1807 (the door's write contract — the landed shape the guard re-verifies)"
  ],
  "applies_when": [["merge","guard"], ["escape","post-merge-verification"], ["guard","vanish-guard"]],
  "enforcement": "No escape filing closes without a post-merge guard verdict posted at the merged tip: independent seat, own execution, sabotage bite-and-restore, tree-clean confirmation. The merge-watch/director pass treats a closure declared on the PR head alone as an open escape. Fast-forward merges are exempt only with proven tree-identity (merge-commit tree byte-identical to the verified PR-head tree).",
  "dedupe_guard": "Not a duplicate: 'merged tip' appears in learn/lessons.md only in unrelated notes (HTML-room stitching, due-announcement naming). No existing note requires post-merge guard re-execution for escape closure. SN-1806 governs the remediation line on filings; this governs the locus of the closure proof."
}
```
