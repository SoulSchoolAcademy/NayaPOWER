# Making Brain-Index Drift Mechanically Block Merges

**The one action required from Shawn (the Human Director):** mark the
`brain-index-freshness` status check as REQUIRED in branch protection for
`main`. Without this click, the workflow runs but cannot block. With it,
any PR that changes `BRAIN/` without re-stamping the index cannot merge.

This is a protected gate (repository settings change). No agent can or
should make this change — it requires your explicit action.

---

## Why this matters

The brain index (`BRAIN/REAL-TREE.json`, `BRAIN/REAL-TREE.md`) drifted
11 times. Each time, a PR changed `BRAIN/` files without running
`tools/regenerate_brain_index.py`, and the drift was caught after the
merge — never prevented.

PR #2372 added a mechanical freshness check. PR #2380 (this PR's
companion) added a dedicated `brain-index-freshness.yml` workflow that
runs that check on every PR touching `BRAIN/**`.

But a workflow that runs is not a workflow that blocks. GitHub only
blocks merges on status checks that are marked **required** in branch
protection. That marking is a settings change only you can make.

## Exact steps

1. Go to https://github.com/SoulSchoolAcademy/NayaPOWER/settings/branches
2. Under "Branch protection rules," click **Edit** on the `main` rule
   (or **Add rule** if none exists for `main`).
3. Check **Require status checks before merging**.
4. In the search box, type `brain-index-freshness`.
   - It appears after the workflow has run at least once on any PR.
     If it doesn't appear yet, merge this PR first (the workflow runs
     on PRs touching `BRAIN/**`; this PR doesn't, so open any test PR
     that touches a `BRAIN/` file, or wait for the next one).
5. Check the box next to `brain-index-freshness`.
6. Click **Save changes**.

## What changes after the click

- Any PR that modifies files under `BRAIN/` triggers the
  `brain-index-freshness` check.
- If the index is stale (drift), the check FAILs and the PR **cannot
  merge** until the author runs `python3 tools/regenerate_brain_index.py`,
  reviews the diff, and commits the regenerated files.
- PRs that don't touch `BRAIN/` are unaffected — the workflow doesn't
  run, no extra CI minutes spent.

## What this does NOT do

- It does not auto-fix drift. The author must run the regen and commit.
- It does not check semantic correctness of the index — only the
  mechanical layer (counts, blob SHAs, pointers). A wrong-but-consistent
  index still passes; that is caught by review, not by this gate.
- It does not replace the existing `kernel-tests.yml` freshness step,
  which continues to run on every PR as a second layer.

## Verification

After the click, open any PR that touches `BRAIN/` without re-stamping.
The `brain-index-freshness` check should show as required and failing,
and the merge button should be blocked. That is the enforcement working.
