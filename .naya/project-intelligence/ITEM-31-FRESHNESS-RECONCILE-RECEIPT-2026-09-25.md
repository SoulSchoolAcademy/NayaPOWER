# NayaPOWER — Item 31 Control-Plane Freshness Reconciliation Receipt

**Date:** 2026-09-25
**Item:** 31
**Title:** Reconcile baton snapshot so the Item 31 freshness audit genuinely returns FRESH on main
**Status:** RECONCILED_LOCALLY — PENDING_POST_MERGE_CI_VERIFICATION
**Branch:** `coda2/item31-freshness-reconcile-20260924`
**Based on origin/main:** `fa82d32b67131c5cdaec441d0f0787a9921f8370`
**Related PRs:** #566 (Item 31), #562 (Item 30)
**Related issue:** [#554](https://github.com/SoulSchoolAcademy/NayaPOWER/issues/554)

## Original problem

The Item 31 freshness workflow runs on main since PR #566 merged and its jobs complete
"success", but the workflow treats `EXPECTED_RED` as a pass. The latest audit artifact on
main (run `36074151604` at head `dbd3e0da9…`) reports:

```json
{ "status": "RED", "outcome": "EXPECTED_RED", "first_divergence": "BATON_SOURCE_SNAPSHOT_STALE" }
```

Green CI jobs were therefore masking a genuine control-plane coherence gap: the committed
baton was generated from snapshot `13d33c6f…` while the control-plane surfaces advanced on
main. The Item 31 validator is working as designed; the control plane had not been
reconciled after the after-main-merge projection refresh.

## Observed truth at origin/main (`fa82d32b…`)

- `STATE.current_head` is `LIVE_AT_EXECUTION_TIME` with a non-authoritative recorded head — valid.
- Active block / block status / single next action agree across STATE, BLOCKS, MAP, BATON.
- The four registered UNKNOWNs remain `UNKNOWN` with explicit identity; no resolution records exist.
- `PROOF` observed head and recording commit are valid and ancestors of live HEAD.
- Canonical Hub source SHA `eb825f34…` agrees across STATE, MAP (authority/pre-execution/top-level),
  BATON, the Team Naya lock, and `git rev-parse HEAD:NAYANET/HUB/index.html`.
- The committed `BATON.json` `source_snapshot.live_head` = `13d33c6f…`, whose control-plane
  content no longer equals current main → `BATON_SOURCE_SNAPSHOT_STALE`.

## Smallest effective change

Rebuilt `BATON.json` from the canonical surfaces at `fa82d32b…` using the checked-in builder:

```
python .naya/runtime/baton.py build-and-validate
```

Result: `PASS — BATON_BUILT_AND_VALIDATED`, `source_snapshot.live_head = fa82d32b…`.

Net diff: two fields (`generated_at`, `source_snapshot.live_head`). No STATE, BLOCKS, MAP,
PROOF, UNKNOWN-REGISTRY, or UNKNOWN-RESOLUTION-LEDGER change was required. No UNKNOWN was
resolved, superseded, or deleted.

## Verification

Local fail-closed audit in the isolated worktree (raw run):

```
status=RED  outcome=EXPECTED_RED
first_divergence=NON_MAIN_CURRENT_AUTHORITY: coda2/item31-freshness-reconcile-20260924
```

That RED is the intended feature-branch gate, not a control-plane defect.

CI-equivalent audit with branch treated as `main` (same validator, git branch gate
overridden to mirror the post-merge main run; all files/refs resolved at `fa82d32b…`):

```
status=FRESH  outcome=PASS
checks: head_authoritative=true active_block_coherence=true
active_block_status_coherence=true next_action_coherence=true
unknown_identity_resolution_explicit=true proof_commit_references_valid=true
baton_generated_from_current_state=true canonical_hub_sha_coherence=true
unknown_resolution_count=0 still_unknown_count=4
```

The four UNKNOWNs remain listed by explicit policy (UNKNOWN ≠ RESOLVED without evidence).

## What remains unproven until after merge

- A post-merge CI freshness run on `main` returning `FRESH` with `outcome: PASS`.
  This is the authoritative verification and must be observed, not assumed.

## Status of related items

- **Item 30 (PR #562):** unchanged — OPEN, unmerged, deployment blocked at the
  authorization boundary. See `ITEM-30-DEPLOYMENT-BLOCKER-RECEIPT-2026-09-24.md`.

## Exact successor action

Merge this reconciliation PR, then inspect the `Control Plane Freshness Audit (Item 31)`
run on the merge commit's `main` and verify the uploaded
`control-plane-freshness-audit.json` shows `status: FRESH` and `outcome: PASS`. Until that
artifact is observed, record Item 31 freshness as PENDING_POST_MERGE_CI_VERIFICATION.

## Authority boundary

This receipt records local reconciliation and CI-equivalent verification only. The
post-merge main CI artifact is the authority for `VERIFIED` status.