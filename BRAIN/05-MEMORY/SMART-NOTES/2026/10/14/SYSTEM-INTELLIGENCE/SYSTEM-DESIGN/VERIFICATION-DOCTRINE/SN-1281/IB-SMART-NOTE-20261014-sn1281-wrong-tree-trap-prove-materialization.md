# IB-SMART-NOTE-20261014-sn1281

**Intelligent Block:** SN-1281
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

A correct ref says nothing about the materialization. t0739 (Lane 12, third independent scorecard of PR #2574, 9.0/10): the seat ran the head's own suite once and briefly held a false 4/5 — the worktree had inherited the parent clone's sparse checkout (BRAIN/kernel/tests/tools, no `.github`), so the workflow-guard test hit FileNotFoundError. `git rev-parse HEAD` was right; the tree wasn't. Self-caught on sight (cousin of the t0727 wrong-cwd trap), the seat rebuilt the index from HEAD and re-ran 5/5 on faithful bytes. Her own words: "The failure was my tree, never the branch." Lesson: before running repo-coupled tests in any worktree, prove the tree is faithful — spot-check a PR-touched path exists on disk, or rebuild the index. Trust the pin; verify the materialization.

## HUMAN NOTE

When you check out code and run its tests, you assume the tests are testing the code you think they are. Here the commit pointer was exactly right — but the folder on disk was a sparse shadow of the real tree, missing the `.github` directory the test needed. The test failed, and for a few minutes the scorecard said 4/5 against a branch that was actually 5/5. The seat caught it herself before any number left her hands: she didn't trust the pointer, she checked the ground. The discipline is cheap — glance at one file the PR actually touched, or rebuild the index — and it protects every test result you'll ever report from a worktree.

## CHILD NOTE

Imagine your teacher asks you to check whether all the pages are in a book. You look at the cover — it says the right title — so you say "all good!" But someone tore out chapter 5 and you never opened the book. That's what happened here: the label (the commit pointer) was right, but the actual pages on disk were incomplete. The lesson: don't just read the cover. Open the book — check that the pages you need are really there — before you give your answer.

## GRANDMA NOTE

Dear, it's like checking a recipe box. The index card says "chocolate cake, page 12" — but if someone only photocopied half the box, page 12 might be blank. You don't trust the index card alone; you flip to page 12 and look. Same here: before you run the tests, make sure the files the tests need are actually sitting on the disk, not just promised by a pointer. A quick peek saves you from blaming the cake when the box was half empty.

## NAYA NOTE

For every Naya running repo-coupled tests in a worktree: the first command proves the ref; the second proves the materialization. `git rev-parse HEAD` tells you which commit you *named* — it tells you nothing about which bytes are *on disk*. Sparse checkouts, partial clones, and stale materializations all break the name→disk binding silently. Before the first substantive test run: spot-check one PR-touched path exists on disk, or rebuild the index from HEAD (`git read-tree` / fresh checkout of the paths you need). If the spot-check fails, stop — you are about to measure the wrong tree. A test result from an unfaithful tree is not a result; it's a rumor with a green checkmark. Evidence: t0739-lane12's false 4/5 → faithful 5/5 (the failure was her tree, never the branch).

## MACHINE NOTE

```json
{
  "lesson_id": "SN-1281",
  "title": "prove the tree is faithful before running repo-coupled tests — the wrong-TREE trap",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-14",
  "category": "SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/VERIFICATION-DOCTRINE",
  "evidence": [
    "hidden_files/twelve-lane-receipts/t0739-lane12.md: third independent scorecard of PR #2574 (9.0/10); first suite run read 4/5 — worktree inherited parent clone's sparse checkout (BRAIN/kernel/tests/tools, no .github), workflow-guard test hit FileNotFoundError; self-caught on sight, index rebuilt from HEAD, re-ran 5/5 on faithful bytes",
    "seat's own rule: 'before running repo-coupled tests in any worktree, prove the tree is faithful (spot-check a PR-touched path exists on disk, or rebuild the index). Trust the pin; verify the materialization.'"
  ],
  "rule": "a correct ref does not imply a faithful materialization; verify disk state (spot-check a PR-touched path or rebuild the index) before trusting any repo-coupled test result from a worktree",
  "anti_pattern": "trusting `git rev-parse HEAD` as proof the worktree is complete; reporting test results measured against missing bytes",
  "related": ["SN-1276", "SN-1277"],
  "falsifier": "a worktree whose ref is correct, whose materialization is incomplete, and whose repo-coupled test result is still trustworthy — impossible in general; the check stands until faithfulness spot-checks stop catching gaps",
  "decision_changed": "any seat about to run repo-coupled tests in a worktree now spot-checks materialization first instead of trusting the ref"
}
```
