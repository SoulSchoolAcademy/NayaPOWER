# NayaPOWER — Item 31 BATON Snapshot Integration Receipt

**Date:** 2026-09-24
**Item:** 31
**Status:** SNAPSHOT REPAIR VERIFIED ON RECONCILED BRANCH — MAINLINE PROOF PENDING
**Branch:** `coda2/item31-control-plane-freshness`
**Source parent HEAD:** `3f1c5786ef0f446d90900e5f66cf07753b21f78f`
**Live origin/main:** `14f8d56448198af39030b01a7585cee36f7833ca`
**PR:** #566
**Issue:** #554

## Reconciliation

The branch was originally based on `d1d60396...`; live main advanced while the local repair was being prepared. The working changes were stashed, the branch was rebased onto the freshly fetched `14f8d564...`, and the stash was reapplied without conflict. The only intended integration files are this receipt and `.naya/control-plane/BATON.json`.

The current main delta since the previously cited `3a227c38...` only changed `.github/workflows/verify-governed-intelligence-commit.yml`; no control-plane source was overwritten.

## Existing regeneration contract

The canonical producer remains `.naya/runtime/baton.py`:

- `build_baton()` derives `source_snapshot.live_head` from the current Git `HEAD`.
- `write_baton()` validates and persists the derived artifact.
- `.github/workflows/verify-next-action-handoff-cycle.yml` is the existing workflow that invokes `baton.py build-and-validate` and commits its durable handoff update.
- Its history intentionally removed control-plane paths from the push trigger (`0cabf453...`) to prevent state mutation and self-trigger loops. `.github/workflows/verify-control-plane-sync.yml` validates synchronization but does not regenerate BATON.

No second generation authority was introduced. The lifecycle hardening gap is recorded as a separate future boundary.

## Two-field repair

Only these derived fields were changed in `.naya/control-plane/BATON.json`:

- `generated_at` → `2026-09-24T15:15:58.3256825Z`
- `source_snapshot.live_head` → `3f1c5786ef0f446d90900e5f66cf07753b21f78f`

The Hub SHA field, builder, validators, canonical control-plane sources, UNKNOWN registry/ledger, Item 30 surfaces, dependencies, and authority model were not changed.

## Verification before integration commit

- Rebase against `origin/main`: PASS, no conflicts.
- Direct `validate_baton(...)` snapshot check: PASS.
- Focused freshness suite: 15/15 PASS.
- Python compilation: PASS.
- Workflow YAML parse: PASS.
- BATON JSON parse: PASS.
- `git diff --check`: PASS.
- Canonical `baton.py validate`: EXPECTED RED at the separate `BATON_HUB_SOURCE_MISMATCH`; intentionally untouched.
- Hub `npm run typecheck`: BLOCKED because `tsc` is unavailable; no lint script is declared.

## Truth boundary

The snapshot repair is verified against the reconciled branch and is ready for the existing PR/integration path. Full Item 31 remains `IMPLEMENTED — NOT VERIFIED` until the resulting change is on current `main` and the mainline freshness workflow has run. No merge, deployment, service-role operation, Hub repair, or production proof has been claimed.

## Exact successor action

Push the bounded commit to PR #566, observe the required checks, and verify the actual post-integration `main` with the Item 31 freshness workflow; stop at the first deterministic RED and keep the Hub mismatch separate.
