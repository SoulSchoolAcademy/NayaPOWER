# Frozen E01 Integrity Gate Caught Preexisting Drift — Do Not Weaken the Guardrail

- Timestamp: 2026-08-20 20:15 PDT
- Last Updated: 2026-08-20 20:15 PDT
- Category: PROBLEM
- Status: BLOCKING / UNRESOLVED
- Scope: MAXESS / REPOSITORY INTEGRITY
- Keywords: E01, frozen baseline, integrity gate, preexisting drift, protected scope, MAXESS, preservation, blob SHA, branch drift, do not weaken gate, PR #8
- Aliases: E01 drift, frozen E01 mismatch, preservation violation, integrity gate catch, protected artifact mismatch
- Related: `docs/MAXESS-E01-FROZEN-BASELINE.md`, `.github/workflows/repository-integrity.yml`, PR #8

## Context

After repairing the stale repository identity and Smart Notes checks, PR #8's repository integrity workflow progressed to the protected E01/E02 gate and failed on the E01 frozen blob check.

The frozen E01 contract explicitly requires blob:

`c01ba966c4b1439b8b3e95161c6f8316202736d8`

The current PR merge tree contains `E01-SECTION-01-WORKING.html` at blob:

`8e0df071ebb7fa33ff8ce21dd5f1c1f1590d902b`

Therefore the integrity gate is correctly detecting preexisting protected-artifact drift in the active engineering lineage.

## What We Learned / Decided

A passing product-specific change is not enough if a protected neighboring artifact is already outside its frozen contract.

The correct response is **not** to weaken the gate, change the expected SHA to whatever happens to be present, or silently absorb the drift into the AIScore PR.

The correct response is:

**PRESERVE SCOPE → KEEP THE GUARDRAIL → CLASSIFY PREEXISTING DRIFT → RESTORE FROM AUTHORITATIVE BASELINE IN A CONTROLLED REPAIR → REVERIFY**

AIScore CLEAN V1 did not intentionally mutate E01. The failure belongs to repository state, not the AIScore first-load repair.

## Why It Matters

This is exactly what a good integrity gate is supposed to do: catch a protected regression before it is normalized into future work.

Weakening the gate would make the repository appear healthier while making the system less trustworthy.

## Required Behavior

Do not merge PR #8 while the frozen E01 gate is red.

Do not alter the E01 expected SHA merely to make CI green.

Do not include an E01 restoration inside the AIScore PR unless the task is explicitly expanded and the restoration is performed from the authoritative frozen baseline with full verification.

Create a separate controlled repair for E01 if/when authorized, then prove:

`CURRENT E01 BLOB == c01ba966c4b1439b8b3e95161c6f8316202736d8`

before resuming dependent work.

## Evidence / Source

GitHub Actions run `32443248969`, job `96657975767`, step `Frozen E01 / active E02 section integrity gate` failed after identity and Smart Notes gates passed. The frozen contract in `docs/MAXESS-E01-FROZEN-BASELINE.md` defines the authoritative E01 blob as `c01ba966c4b1439b8b3e95161c6f8316202736d8`.

## Follow-up

Keep PR #8 focused on AIScore. Track E01 restoration as a separate protected-scope integrity task.
