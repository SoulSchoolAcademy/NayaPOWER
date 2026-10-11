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

PR #2372 added a mechanical freshness check. This PR adds a dedicated
`brain-index-freshness.yml` workflow that runs on every pull request and
reports the check — `NOT_APPLICABLE` for PRs that don't touch `BRAIN/`,
the full gate for ones that do.

But a workflow that runs is not a workflow that blocks. GitHub only
blocks merges on status checks that are marked **required** in branch
protection. That marking is a settings change only you can make.

## Required-check safety: why the workflow runs on every PR

The workflow's trigger is deliberately UNCONDITIONAL — it runs on every
pull request, not just ones touching `BRAIN/`. GitHub documents that a
check marked REQUIRED which is skipped by a paths-filtered workflow
stays **Pending** forever, which blocks every PR the workflow does not
run on. A `BRAIN/**`-only trigger would have frozen the entire merge
queue the moment this check became required. (P0 repair, 2026-10-11.)

The BRAIN-scope decision happens inside the job instead, cheaply: PRs
that change nothing under `BRAIN/` report success immediately as
`NOT_APPLICABLE` (no regen run, seconds of CI time). PRs that touch
`BRAIN/` run the full freshness gate. Anything the job cannot
determine — missing SHAs, a git failure — fails closed to the full gate.

## Exact steps

1. Go to https://github.com/SoulSchoolAcademy/NayaPOWER/settings/branches
2. Under "Branch protection rules," click **Edit** on the `main` rule
   (or **Add rule** if none exists for `main`).
3. Check **Require status checks before merging**.
4. In the search box, type `brain-index-freshness`.
   - It appears after the workflow has run at least once on any PR.
     If it doesn't appear yet, merge this PR first (the workflow runs
     on every PR, so the next PR of any kind will surface it).
5. Check the box next to `brain-index-freshness`.
6. Click **Save changes**.

## What changes after the click

- Any PR that modifies files under `BRAIN/` runs the full freshness
  check. If the index is stale (drift), the check FAILs and the PR
  **cannot merge** until the author runs
  `python3 tools/regenerate_brain_index.py`, reviews the diff, and
  commits the regenerated files.
- PRs that don't touch `BRAIN/` report success immediately as
  `NOT_APPLICABLE` — they are never blocked by this check, and cost only
  seconds of CI time.

## What this does NOT do

- It does not auto-fix drift. The author must run the regen and commit.
- It does not check semantic correctness of the index — only the
  mechanical layer (counts, blob SHAs, pointers). A wrong-but-consistent
  index still passes; that is caught by review, not by this gate.
- It does not replace the existing `kernel-tests.yml` freshness step,
  which continues to run on every PR as a second layer.

## Verification

After the click:

1. Open any PR that touches `BRAIN/` without re-stamping. The
   `brain-index-freshness` check should show as required and failing,
   and the merge button should be blocked. That is the enforcement
   working.
2. Open (or watch) any PR that does NOT touch `BRAIN/`. The check should
   report success quickly with a `NOT_APPLICABLE` result — no PR is ever
   left Pending by this gate. If a non-BRAIN PR ever sits Pending on
   this check, that is a defect: file it against the LAW lane
   immediately.
