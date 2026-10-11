# In a Shared Clone, Verify the Branch Before AND After Every Commit

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0855-shared-clone-verify-branch-before-and-after-commit
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.
> Source: #1354 comment 6092172979 (2026-10-10 UTC), Gate 2 of 7 — Authority Coverage Audit, environment notes; correction comment 6092205586 (shared checkout repaired by orchestrator). Branch `brain-build/authority-coverage-v1`; sibling branch `brain-build/completeness-gate-v1` restored to `93030048d`.

## ✦ IN A NUTSHELL

A checkout shared with sibling lanes actively switching branches is a loaded gun: between your branch check and your commit, someone else's lane can switch HEAD — and your commit lands on their branch. That's exactly what happened during the Gate 2 authority-coverage work: the commit initially landed on `brain-build/completeness-gate-v1` (a sibling lane's branch) by a mid-commit branch switch. The repair used `update-ref` plumbing: the commit was moved so it exists only on `brain-build/authority-coverage-v1`, the sibling branch was restored to its prior SHA (`93030048d`), and the working tree was verified free of interference. The rule: in a shared clone, verify which branch HEAD points to immediately BEFORE commit creation AND immediately AFTER — never assume the branch you were on thirty seconds ago is the branch you're on now. If a commit lands on the wrong branch, repair it the same tick with plumbing (update-ref), restore the sibling branch to its exact prior SHA, and verify no working-tree interference — never leave a stray commit on someone else's branch, and never silently rewrite their ref.

## 🩷 HUMAN NOTE

When several people share one workspace and everyone's switching between tasks, the "current task" can change under your feet. You check "I'm on my branch," start your work, and by the time you save, someone else switched the workspace to their branch — so your work lands in their task. The fix is a habit: check which branch you're on right before you commit AND right after. If your commit went to the wrong place, move it immediately with the plumbing tools, put their branch back exactly how you found it, and make sure you didn't disturb their work.

## 🟣 CHILD NOTE

If you share a desk with someone and you both keep moving your papers around, always check whose pile you're putting your paper on — right before you put it down AND right after. If you accidentally put your paper on their pile, move it to yours right away, put their pile back exactly like it was, and make sure you didn't mess anything up.

## 🔵 GRANDMA NOTE

In a shared workshop, always check whose workbench you're setting your tools on — before you set them down and after. If they landed on the wrong bench, move them at once, leave the other bench exactly as you found it, and make sure nothing of theirs was disturbed.

## 🟠 NAYA NOTE

When working in a shared clone (or any checkout sibling lanes can touch): (1) re-verify `git symbolic-ref HEAD` (or equivalent) immediately before commit/tree creation AND immediately after — the branch is mutable shared state, not a constant; (2) prefer a private detached worktree for commit assembly when sibling lanes are active (per the VERIFY-driver pattern) — isolation beats vigilance; (3) if a commit lands on the wrong branch: repair the same tick with `update-ref` plumbing, restore the sibling branch to its exact prior SHA, verify zero working-tree interference, and report it openly on the feed — never leave a stray commit, never force-move someone else's ref silently; (4) treat "I was on my branch a minute ago" as no evidence at all.

## 🟢 MACHINE NOTE

~~~json
{
  "rule": "SHARED_CLONE_BRANCH_VERIFICATION",
  "failure": {
    "mechanism": "mid-commit branch switch by a sibling lane in a shared checkout",
    "effect": "commit landed on brain-build/completeness-gate-v1 instead of brain-build/authority-coverage-v1"
  },
  "repair": {
    "method": "update-ref plumbing",
    "sibling_branch_restored_to": "93030048d",
    "working_tree": "verified no interference",
    "reported": "openly on #1354 (6092172979 notes, 6092205586 correction)"
  },
  "prescription": [
    "verify HEAD branch immediately BEFORE and AFTER every commit",
    "prefer private detached worktree when sibling lanes are active",
    "same-tick plumbing repair; restore sibling ref to exact prior SHA; never silent"
  ],
  "truth_ceiling": "CANDIDATE"
}
~~~
