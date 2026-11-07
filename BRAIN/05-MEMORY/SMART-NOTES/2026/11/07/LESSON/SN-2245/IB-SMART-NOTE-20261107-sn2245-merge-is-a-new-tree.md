# The Merge Is a New Tree: Verify the Landing, Not the Promise

SN-2245 · LESSON / DISTILLATION

**Created:** 2026-11-07 23:11Z

## IN A NUTSHELL

Verdicts bind SHAs. A PR body decays the moment the head moves — rebind it at every material change. The repo is the demo: one frozen SHA for what is viewed, what is judged, and what is repaired. The frozen SHA is the judge's anchor, and the freezer is bound by it too. Caveats must carry their expiry trigger. Re-fetch freshness before the push, not just the post. A CANDIDATE note with a disclosed unknown may merge; a disguised unknown may not. Keep the review head stable. The auto-merge gate must re-verify on the merge commit — the merge itself changes the tree. Adjudicate convergence on blob-SHA proof and close the superseded PR instead of merging a no-op. The branch must not move before the check.

## HUMAN

A pull request's description said "21 to 25 on the old base" while the actual code was "21 to 26 on the new base" — five ways drifted, nothing flagged it, and a reviewer reading the body alone would have evaluated a change that no longer existed. An auto-merge landed a brain file and left the index stale — 188 files counted while the tree held 189 — because every check had qualified the pre-merge state and the merge itself created a new tree nobody re-verified. A judge froze a review at one SHA, then committed to the same branch a minute later — and the ruling held: the frozen SHA stands; her own later commit enters the next review, not this one. A pull request sat open while other lanes landed every piece of it; instead of merging a no-op, the owning lane proved convergence with exact file comparisons and closed it as superseded. The discipline in every case is the same: the evidence belongs to an exact tree, and the moment the tree moves, the evidence expires with it.

## CHILD

Imagine a teacher grading your drawing, and while she grades it you keep drawing on it. Her grade is for the old drawing, not the new one — so she pins your drawing to the wall and grades exactly that one. If you change it afterward, that is a new drawing, and it gets a new grade. The pin is the promise: this exact drawing, this exact grade.

## GRANDMA

Judge the thing as it is, not as it was described yesterday. If the words about the work are older than the work itself, rewrite the words. If you move the furniture while someone is measuring the room, their numbers are for the old room. Measure again after the move.

## NAYA

Bind every verdict to its SHA: a decision computed on tip T is inadmissible after the tip moves. Re-derive the PR body's claims — base pin, counts, test results, repair class, supersession list — from the new head in the same motion as the mutation, and stamp the body "as of head X" explicitly. Freeze the demo as a pushed commit; what Shawn views, what the judge scores, and what the repair targets are one SHA. Re-fetch tip freshness before the branch push too — a same-topic lane may have merged inside your repair window. Adjudicate convergence on proof — merge-base three-way plus per-blob SHA equality against live main — not on "it merges clean," which means no conflicts, not that the content is needed. And never trust pre-merge checks on a post-merge tree: if the merge produces a new commit, re-run the derived-layer checks on the merge commit itself before declaring the landing healthy.

## MACHINE

The landing checklist: (1) verdict SHA == head SHA at decision time, else re-verify and re-stamp; (2) PR body re-derived from the new head on every material change; (3) demo == frozen pushed commit SHA; (4) review pins to the frozen SHA, never the branch head; (5) every time-bound caveat carries its expiry trigger — the exact event that invalidates it; (6) freshness re-fetch before push, post, and merge; (7) index / ledger / cache checks re-run on the exact merge commit; (8) convergence adjudicated on blob-SHA proof, superseded PRs closed unmerged with the residual preserved for cherry-pick; (9) the irreversible mutation comes last, after every check is green.

Distills (Batch 1, 10 of 100): SN-0185 A PR Body Is a Decaying Document — Rebind It to the Head · SN-0191 The Repo Is the Demo — the Freeze-Point Protocol · SN-0206 The Frozen SHA Is the Judge's Anchor · SN-0041 Stale-Caveat Decay · SN-0472 Deconfliction Guards the Push · SN-0325 CANDIDATE Absorbs Uncertainty · SN-0473 Review Head Stability · SN-0328 The Auto-Merge Gate Must Re-Verify on the Merge Commit · SN-0558 Adjudicate Convergence on Blob-SHA Proof · SN-0352 The Branch Must Not Move Before the Check.

## WHAT IT ALL MEANS

A merge is not a ceremony over a verified PR head — it is a new tree, and nothing proved on the old tree transfers. Every defect in this family is the same shape: evidence measured on one tree, trusted on another. The freeze, the rebind, the re-verification, and the convergence proof are all one discipline — keep the evidence and the tree in the same moment, or the evidence is void.

## WHY IT MATTERS

The team merged verified work and still shipped a stale index, judged a moving branch and manufactured disagreement, and reviewed descriptions of code that no longer existed. Each time, the work was good and the evidence was honest — and wrong, because the tree had moved underneath it. The landing check is the only thing standing between "verified" and "actually on main, healthy."

## HOW IT CONNECTS

Sibling distilled notes: SN-2241 (live bytes beat every claim — the same decay, stated for evidence generally) · SN-2246 (promotion is atomic — the pointer move is the same commit-point problem at production scale) · SN-2244 (a law is only real when a machine enforces it — the gate that must re-verify is the machine). Raw family: the ten merge-discipline notes above, from the 2026-09-30 / 2026-10-05 / 2026-10-07 clusters.

## WHAT IS IN IT FOR YOU

What you view is what was judged is what got repaired — one SHA, one review, one gate. No more "the demo looked different from the repo," and no more verdicts that quietly moved with the branch.

## THE LEARNING

Never trust pre-merge checks on a post-merge tree. Verify the landing on the exact merge commit.
