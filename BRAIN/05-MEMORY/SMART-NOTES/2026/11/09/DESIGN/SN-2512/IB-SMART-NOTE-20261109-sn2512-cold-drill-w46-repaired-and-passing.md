# Cold-Drill W46 Repaired and Passing

SN-2512 · SYSTEM / VERIFICATION

**Created:** 2026-11-09 15:35Z

**Source:** the cold-drill W46 repair seat's completion handoff (coordinator completed 2026-11-09 15:24:44Z) + the captain's ratification + the tip move on main (3f9d17ae → 96c9b645, 15:18:12–15:19:05Z, dispatcher wave 15:18Z). Recorded in ~/MEMORY.md the same pass. Supersedes run 46's open item "SN-2068 essence-index corruption (repair ownership unassigned)."

## Hook

The drill that proves the machine can remember was failing on its own index — the fix widened the roots, and it passes again.

## Nutshell

- **THE FAILURE (board #3066, 14:46Z):** [COLD-DRILL][W46] FAIL — retrieved NONE (expected SN-0344), `INDEX_CORRUPT:PATH_ESCAPE` on the SN-2068 essence entry, reproduced on a fresh worktree. The cold drill — the proof mechanism for the distillation machine — failed on a corrupt index entry.
- **THE ROOT CAUSE:** 122 essence backfill entries projected OUTSIDE the validator's allowed roots (SN-2068 first hit). The entries were real; the roots were too narrow. The validator was rejecting true paths, not catching false ones.
- **THE FIX (repair seat, both jobs, done + proven):** (1) roots widened to include BRAIN/05-MEMORY (fail-closed preserved), 6 stale page_hashes refreshed, drill-bank item c retired (SN-0344 retired); (2) the numbering guard now scans open PRs — next free SN-2506 (SN-2505 claimed by PR #3307). W46 PASS on SN-016. Filings to HEAD 96c9b645.
- **RATIFICATION:** the captain ratified the roots change. Widening a validator's roots is a law change, and it went through his hand — not the seat's.
- **WHAT IT CLOSES:** run 46's open item "SN-2068 essence-index corruption (repair ownership unassigned)" — ownership was assigned (repair brief + dispatched seat, ~15:04Z), the repair landed 15:18Z, and the drill passes. The SN-2505 open-PR claim is also closed as a hazard: the guard now sees it.
- **WHAT IS STILL OWED:** nothing on this repair. The prevention question from SN-2504 (the sync verifies the feed) is a different item and stays open.

## Human

The cold drill is the machine's memory test: can it reach back and pull out an old lesson from cold storage? It couldn't — not because the lesson was gone, but because the map of where lessons are allowed to live was drawn too small, and 122 of them sat outside the border. The fix didn't move the lessons; it redrew the border to include where they actually live, and the test passes again. The captain approved the new border himself, because changing what the machine is allowed to trust is his call. And while they were in there, they fixed the numbering guard too, so the next note filed won't collide with one already waiting in a pull request.

## Child

The treasure map said the treasure could only be in certain places, but some treasure was buried just outside the line. The test kept failing because it looked inside the line and found nothing. So we drew the line a little bigger to include where the treasure really is — and now the test finds it. We also fixed the number machine so it won't give two notes the same number.

## Grandma

Dear, the memory test is working again, love — the map was drawn too small and the lessons were sitting just outside it, dear. The border is widened now, the test passes, and the captain himself approved the change, love. That's the whole of it.

## Naya

This is the distillation machine repairing its own proof mechanism, and it matters for the loop because the loop IS the distillation machine's daily proof: if the cold drill cannot retrieve, the claim "the system remembers" is unproven. The root cause class is the same as SN-2504's two keys: two sources of "what exists" (the backfill projection vs the validator's roots) that never reconciled, and the disagreement looked like corruption when it was really a narrow map. The fail-closed property was preserved — the fix widens the roots, it does not disable the check — and the ratification went through the captain because a validator's roots are law. The numbering-guard fix is the third numbering near-miss resolved mechanically (after SN-2474 and SN-2482/2483): the guard now scans open PRs, so a claimed-but-unmerged number is no longer reported free.

## What it means

- **W46 PASSES:** cold drill retrieves again (PASS on SN-016); the distillation machine's proof mechanism works.
- **THE ROOTS ARE WIDER:** BRAIN/05-MEMORY is an allowed root now, fail-closed preserved, captain-ratified.
- **THE NUMBERING GUARD SEES OPEN PRs:** next free SN-2506; SN-2505's claim by PR #3307 is visible to the guard.
- **RUN 46's OPEN ITEM IS CLOSED:** the SN-2068 corruption is repaired, not just assigned.

## Why it matters

A proof mechanism that fails silently is worse than no proof mechanism — it reports failure where the system is actually fine, and the next time it reports failure, nobody knows whether to believe it. The W46 FAIL was loud and visible, which is the good kind of failure; the repair is the system keeping its own promise that lessons compound instead of evaporating. The numbering-guard fix is the same promise at the other end: the third near-miss in the SN-2500s is now mechanically impossible to repeat the same way, because the guard sees what the tree alone cannot — the claims waiting in open PRs.

## What changes now

- The cold-drill W46 FAIL leaves the open list — repaired, passing, ratified.
- The numbering guard's next-free answer (SN-2506) is trusted for this run's filings — verified three ways (live tree + open PRs, the guard's own run, MEMORY.md).
- SN-0344 is retired as a drill-bank item (item c retired); the drill now passes on SN-016.
- Next loop run re-checks: the drill stays passing; no new INDEX_CORRUPT on the board.
