# NayaPOWER — Item 31 BATON Snapshot Integration Receipt

**Date:** 2026-09-24
**Item:** 31
**Status:** SNAPSHOT REPAIR PUSHED — MAINLINE PROOF BLOCKED
**Branch:** `coda2/item31-control-plane-freshness`
**Source parent HEAD:** `3f1c5786ef0f446d90900e5f66cf07753b21f78f`
**Integration commit:** `b7bbd627` plus non-force ancestry merge `d807046ce0c51abb8240b317791f52f867066591`
**Live origin/main:** `14f8d56448198af39030b01a7585cee36f7833ca`
**PR:** #566
**Issue:** #554

## Reconciliation

The branch was originally based on `d1d60396...`; live main advanced while the local repair was being prepared. The working changes were stashed, the branch was rebased onto the freshly fetched `14f8d564...`, and the stash was reapplied without conflict. The remote branch retained pre-rebase ancestry, so a normal fast-forward push was first rejected; no force-push was used. The inspected remote ancestry was merged locally, producing `d807046c` while preserving the rebased tree.

The current main delta since the previously cited `3a227c38...` only changed `.github/workflows/verify-governed-intelligence-commit.yml`; no control-plane source was overwritten.

## Existing regeneration contract

The canonical producer remains `.naya/runtime/baton.py`:

- `build_baton()` derives `source_snapshot.live_head` from the current Git `HEAD`.
- `write_baton()` validates and persists the derived artifact.
- `.github/workflows/verify-next-action-handoff-cycle.yml` is the existing workflow that invokes `baton.py build-and-validate` and commits its durable handoff update.
- Its history intentionally removed control-plane paths from the push trigger (`0cabf453...`) to prevent state mutation and self-trigger loops. `.github/workflows/verify-control-plane-sync.yml` validates synchronization but does not regenerate BATON.

No second generation authority was introduced. The lifecycle hardening gap remains a separate future boundary.

## Two-field repair

Only these derived fields were changed in `.naya/control-plane/BATON.json`:

- `generated_at` → `2026-09-24T15:15:58.3256825Z`
- `source_snapshot.live_head` → `3f1c5786ef0f446d90900e5f66cf07753b21f78f`

The Hub SHA field, builder, validators, canonical control-plane sources, UNKNOWN registry/ledger, Item 30 surfaces, dependencies, and authority model were not changed.

## Verification before and after push

- Rebase against `origin/main`: PASS, no conflicts.
- Direct `validate_baton(...)` snapshot check: PASS before and after commit.
- Focused freshness suite: 15/15 PASS before and after commit.
- Python compilation: PASS.
- Workflow YAML parse: PASS.
- BATON JSON parse: PASS.
- `git diff --check`: PASS.
- Canonical `baton.py validate`: EXPECTED RED at the separate `BATON_HUB_SOURCE_MISMATCH`; intentionally untouched.
- Hub `npm run typecheck`: BLOCKED because `tsc` is unavailable; no lint script is declared.
- Push to PR #566: PASS; remote branch head is `d807046c`.

## Integration boundary

At observation, PR #566 is `OPEN`, `MERGEABLE`, and `UNSTABLE`. The first integration RED is external: Vercel reports deployment rate limiting, multiple Cloudflare Workers Builds fail, and CodeRabbit reports that manual review is required. No check was retried or bypassed. The Item 31 workflow is not yet on current `main`, so no mainline Item 31 execution is claimed.

## Truth boundary

The snapshot repair is verified on the reconciled branch and pushed through the existing PR path. Full Item 31 remains `IMPLEMENTED — NOT VERIFIED`; current `main` does not yet contain the repair, the separate Hub source mismatch remains open, and no merge, deployment, service-role operation, Hub repair, or production proof was performed.

## Exact successor action

Await authorized review/integration of PR #566; once it is on `main`, run the Item 31 freshness workflow and classify its first deterministic RED without repairing the separate Hub mismatch.
