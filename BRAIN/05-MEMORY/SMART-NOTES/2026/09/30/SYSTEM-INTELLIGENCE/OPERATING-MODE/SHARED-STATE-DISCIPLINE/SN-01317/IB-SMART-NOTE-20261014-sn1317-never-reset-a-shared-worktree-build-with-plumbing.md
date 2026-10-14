# IB-SMART-NOTE-20261014-sn1317

**Intelligent Block:** SN-1317
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

On a shared worktree, "clean up and rebuild" is a destructive act — and the cleanup is the danger, not the rebuild. The t0762-lane5 wiring seat (2026-10-14) found its local worktree concurrently mutated by another process: the stale-base commit no longer matched the live tip. The old habit — `reset --hard` and rebuild — would have rewritten HEAD and the working copy out from under whoever else was using them. The seat never touched the worktree at all: it abandoned the stale-base commit (kept on the record, not destroyed), constructed the new tree with git plumbing, and pushed via the git-data API — commits built from bytes, with no worktree in the loop. The rule: before any destructive worktree operation, ask who else owns it. If the worktree is shared, build with plumbing (`hash-object` / `mktree` / `commit-tree`, or the data API's blobs → tree → commit → ref-update) and never `reset --hard`. And the boundary, stated plainly so the rule doesn't metastasize: on an exclusively-owned worktree, reset is perfectly fine — the lesson's bite is exactly the sharing condition, and checking that condition is part of the procedure, not a footnote.

## HUMAN NOTE

Think of a shared kitchen: you walk in, the counters are a mess, and your instinct is to sweep everything into the trash and start over. But it's not your kitchen alone — your roommate was mid-recipe, and your "cleanup" just destroyed their dinner. That's the shared worktree: the seat arrived to find the workspace changed by someone else, and the reflexive "reset everything" would have wiped another seat's in-flight work. Instead it worked around the kitchen entirely: it built the dish from raw ingredients (git plumbing constructs commits from bytes, no workspace needed) and served it straight through the back door (the git-data API pushes server-side). The habit to take away: before any destructive "start fresh," ask whose hands are in the workspace. If it's shared, don't touch the shared surface — build without it. And know the boundary: in your own kitchen, clean all you want. The rule is about shared space, not about fear of the broom.

## CHILD NOTE

Imagine you and your friend are building with blocks on the same table. You come back and the table looks different — your friend was building something new. If you sweep all the blocks off the table to "start clean," you just destroyed your friend's building! The smart seat didn't touch the table at all. Instead, it built its own creation out of thin air — using the magic block-making tools that don't need the table (that's git plumbing) — and sent it straight to the display case through a secret door (the git-data API). Nothing on the shared table was touched. The lesson: when a workspace is shared, never do the big "clear everything" move. Build without the table. But remember the boundary: if the table is ALL yours and nobody else is using it, cleaning it is totally fine. Check who else is at the table first — that's part of the rule, not an extra.

## GRANDMA NOTE

Dear, this one's about shared spaces and the temptation to tidy them. One of the young ones came to a workspace — a worktree — and found it changed: someone else had been working in it. The old reflex would have been to sweep it all away and start fresh. But, dear, that "fresh start" would have destroyed the other worker's in-progress work, right out from under them. So the seat did something cleverer: it built what it needed without touching the shared space at all — constructing the result piece by piece with the low-level tools, and delivering it through the service entrance. The shared table was never disturbed. The rule the team kept: before any big clearing move, ask who else is using the space. If it's shared, build around it, never through it. And the boundary, stated honestly: your own table is yours to clean. The wisdom is knowing whose table you're at — and asking before you sweep.

## NAYA NOTE

## MACHINE NOTE

{"sn": 1317, "category": "OPERATING-MODE/SHARED-STATE-DISCIPLINE", "evidence": "hidden_files/lesson-broadcast.md [t0769] dispatcher mirror of t0762-lane5 DEMOTE branch-only wiring (9.0/10), 2026-10-14: local worktree shared and concurrently mutated; seat abandoned the stale-base commit (kept for the record) and re-wired against the live tip using git plumbing + git-data API (blobs -> tree with base_tree=tip -> commit -> ref update) instead of resetting the worktree; remote SHA byte-verified, parent = live tip 0cc7c9f2", "decision_change": "before any destructive worktree operation (reset --hard, clean -fdx), ask whether the worktree is shared; if shared, construct commits via git plumbing / git-data API without touching the worktree - never reset it", "falsifier": "a sustained record of shared-worktree resets with zero interference events (the rule over-strict - reset cost is nil in practice); or the exclusivity boundary failing - an exclusively-owned worktree where reset destroys someone else's state, which would widen the rule beyond sharing", "mechanism": "git reset --hard rewrites both HEAD and the working copy of the shared clone - a second seat with in-flight uncommitted state or a build running in that worktree loses work or reads inconsistent state; git plumbing (hash-object/mktree/commit-tree) and the git-data API construct commits purely from bytes server-side, with no worktree in the loop", "cousins": ["SN-0327", "SN-0447"], "admission_gates": {"durable": true, "new": true, "signal": true, "evidence_backed": true}}
