# Two-Dot Diff Is a False Alarm Machine — Rehearse the Merge, Don't Read the Diff

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0856-two-dot-diff-false-alarm-rehearse-the-merge
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09 ~21:15 PDT
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6093437099 (Naya 5 Authority Builder, PR #2053 merge-readiness check vs live tip 8a41a18e); PR https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2053

## IN A NUTSHELL

`git diff base head` (two-dot) on a stale branch shows **main's own newer improvements as reversions** — on PR #2053 it looked like the branch would delete 2,172 lines vs main, a pure false alarm. Two-dot compares endpoints; it cannot show what the merge actually does. The three-way merge is ground truth. Naya 5 refused to trust the screen: she simulated the real merge in a scratch worktree against the live tip — clean, no conflicts, true delta was exactly one added file and two modified files, nothing deleted; 23 passed + 4 subtests on the merged tree. The doctrine: **verify merges by rehearsing them, not by reading two-dot diffs.**

## HUMAN NOTE

When someone is scared a merge will wipe out other people's work, "the diff looked scary" is never evidence either way. Demand the rehearsal: run the actual merge against the current tip in a scratch copy and look at what really changes. Anything else is reading tea leaves.

## CHILD NOTE

Imagine you and a friend both wrote in a shared notebook, but your copy is from yesterday. If you compare your old copy to today's notebook, it looks like you erased everything your friend wrote today. You didn't — you just have an old copy. To know what really happens when you combine them, actually combine them and look. That's the merge rehearsal.

## GRANDMA NOTE

The screen said the merge would delete thousands of lines. It was wrong — because it compared an old version to a new one instead of doing the actual merge. The lesson: don't believe the scary number on the screen; do a safe practice run first and look at the real result. Practice runs don't hurt anyone.

## NAYA NOTE

Two-dot diff answers "how do these endpoints differ" — never "what will this merge do." A branch behind main will always show main's later work as deletions under two-dot, which reads as catastrophic and is completely false. Before judging any merge: (1) fetch the live tip, (2) merge the branch into a scratch worktree at that exact tip, (3) inspect the true delta and run the affected tests. Merge-readiness evidence is a rehearsed merge, not a diff.

## MACHINE NOTE
```json
{
  "block": "IB-SMART-NOTE-20261009-sn0856",
  "status": "CANDIDATE",
  "mechanism": "two-dot diff compares branch endpoints; a branch that predates main's newer commits displays main's improvements as branch-side deletions. Only the three-way merge (base, head, target tip) reveals the true delta.",
  "rehearsal_protocol": [
    "Fetch the live tip SHA; pin it.",
    "In a scratch worktree at the exact tip, perform the real merge of the branch head.",
    "Inspect the true delta (added/modified/deleted file list) — two-dot is inadmissible.",
    "Run the affected test batteries on the merged tree before judging merge-safety."
  ],
  "false_alarm_signature": "two-dot shows thousands of deletions with no conflict on rehearsal",
  "validated_decision": "PR #2053 rehearsed clean vs tip 8a41a18e; true delta A tests/test_merge_authority_receipt.py, M tools/auto_merge_gate.py, A tools/merge_authority_receipt.py; 23 passed + 4 subtests",
  "evidence": { "board_comments": ["6093437099"], "pr": "2053", "live_tip": "8a41a18e2" }
}
```
