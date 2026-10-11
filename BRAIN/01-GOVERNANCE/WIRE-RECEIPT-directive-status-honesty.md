# WIRE RECEIPT — Directive Status Honesty Gate

**Wired:** 2026-10-11 · Naya 2 wire lane · PR: naya2/wire-status-honesty (stacked on PR #2294 → #2289 → #2225)
**Mechanism:** the status ladder NOT_STARTED → BUILDING → BUILT_AS_CODE → ENFORCED
(built by PR #2294: `tools/directive_status.py` + 26 tests + ladder doc).
**Status before wiring:** CODE-ONLY — the promotion tool validated flips, but nothing
forced its use. A hand-edit to `directive-register.json` could skip rungs, claim
ENFORCED with no live gate, or ship a phantom gate path, and no operating path
would object.

## What was wired

1. `tools/directive_status_honesty.py` — the honesty checker. On a base→head
   register transition it enforces:
   - **H1** NOT_STARTED carries no evidence_pr.
   - **H2** BUILT_AS_CODE / ENFORCED carry a valid evidence_pr (positive PR number).
   - **H3** ENFORCED records a gate; a gate naming a repo path must exist in the
     head tree (phantom gates refused).
   - **H4** Movement obeys the ladder: exactly one rung up per change (no
     skipping), any distance down (a removed gate is honest news, not failure).
     New entries are judged by H1–H3 only. Removed entries are refused —
     directives are never deleted from the canon.
   - Fail-closed: an unloadable register (missing/corrupt/misshapen/duplicate
     ids) is exit 2, never a silent pass. A brand-new register skips H4.
   - Reuses the canonical loader and ladder validators — no second copy of
     the rules.
2. `.github/workflows/directive-status-honesty.yml` — the enforcement gate on
   the PR merge path (and on direct pushes to main touching the register).
3. `tools/tests/test_directive_status_honesty.py` — 18 tests incl. negative
   controls for every rule, git end-to-end (exit 1 on a skip, exit 0 on an
   honest rung, exit 2 on corruption), and the repair regression test.

## Repair shipped in the same stack

While wiring, the wire lane found `tools/directive_status.py` (PR #2294)
validated `--gate` and printed it on the receipt but **never wrote it to the
entry** — the register could not answer which live mechanism enforces a
directive, and the tool contradicted its own doc. Root fix (not a workaround):
`promote_entry` now persists `entry["gate"]` on ENFORCED promotion. The build
lane's 26 tests never asserted the entry carried the gate (only the receipt),
which is how the defect shipped green. Regression test included here.

## Operating path now protected

**The PR merge path for the directive register.**
Trigger: any PR changing `BRAIN/01-GOVERNANCE/directive-register.json` (or the
checker/tool itself). Block: the `directive-status-honesty` check goes red →
the PR cannot merge. This enforces the honesty of the register's own status
accounting at the exact point where a dishonest claim would enter the tree.

## Proof the wiring works (2026-10-11, this run)

- Live fire on the real stack register (58 directives, base #2225 branch):
  0 violations — honestly clean (50 NOT_STARTED with null evidence,
  8 BUILT_AS_CODE each with a positive evidence_pr, 0 ENFORCED).
- Negative controls (each blocked with directive + rule named):
  skip NOT_STARTED→BUILT_AS_CODE → H4; skip to ENFORCED with evidence+gate → H4
  (the movement is the crime); ENFORCED without gate → H3; ENFORCED with phantom
  gate path → H3; BUILT_AS_CODE without evidence_pr → H2; NOT_STARTED carrying
  evidence_pr → H1; removed directive id → H4; corrupt JSON → exit 2 FAIL-CLOSED.
- Git end-to-end: temp repo, honest one-rung commit → exit 0; skip-rung commit
  → exit 1 naming D1/H4; corrupt head → exit 2.
- Repair proof: CLI `promote D32 --to ENFORCED --evidence-pr 2224 --gate
  .github/workflows/real-gate.yml` → reloaded entry carries
  `gate == ".github/workflows/real-gate.yml"` (before the fix: key absent).
- Test suites: 18/18 new green; 26/26 status-tool green; 24/24 register+sync
  green (68/68 total on the stacked head).

## How to verify it is still connected

1. Open any PR touching `BRAIN/01-GOVERNANCE/directive-register.json` and
   hand-edit one entry's status up two rungs — the `directive-status-honesty`
   check must go red naming the directive and rule H4.
2. `python3 tools/directive_status_honesty.py --base-ref <base-sha>
   --head-ref <head-sha>` on any register PR must exit 0 when the diff is
   honest and 1/2 otherwise.
3. Promote via the CLI and re-read the entry: `python3
   tools/directive_status.py show D<n>` must show the gate on ENFORCED entries.

## Failure mode if the wiring breaks

If the workflow file is deleted or its `paths` filter narrowed, register PRs
stop being honesty-checked: rung-skips and phantom ENFORCED claims can merge
silently and the register's statuses decay into unchecked assertions.
Detection: receipt check #1 goes unanswered (no check run on a register PR).
The checker remains usable as a CLI audit regardless
(`--base-ref`/`--head-ref` on any two SHAs).

## What remains unwired (hand-off)

- The vulnerability guard (PR #2247, Naya Code Principle #4): built and tested,
  but its workflow only runs the guard's own test suite — the guard never
  judges a real action proposal. Its natural operating path is a runtime
  action-selection seam (e.g. the ACT pipeline), not CI: wiring it into CI
  without action-proposal inputs would be theater. Hand to the build lane with
  the seam named.
- The whole stack (#2225 → #2289 → #2294 → this) is unmerged: the gates exist
  on branches, not on main's live path. Merge needs the protocol path
  (scorecard + cross-seat review) — wire lane does not merge.
