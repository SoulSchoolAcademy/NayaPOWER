# AI1 capability-carry — current state after PR #1171

**Observed main:** `db8a847e990d55fce07015f2f8fb7df070a528a5`  
**Date:** 2026-09-30  
**Purpose:** reconcile the original branch-only repair receipt with live repository truth.

## Current truth

- PR #1171 is closed and its repair commits are present on current `main`.
- Current main additionally pins the four-case dual-field selector contract and deterministic disagreement behavior in `db8a847e` (AI1-FIELD-01..05); this follow-up preserves that coverage.
- The source repair is therefore **MERGED / IMPLEMENTED IN REPOSITORY**.
- Migration `20260930235959_ai1_capability_carry_v1.sql` is registered as
  `PENDING_REVIEW_NOT_PRODUCTION_APPLIED`.
- Repository implementation is **not production proof**.
- No production HIT, SN-013/SN-014 re-commit, CANDIDATE→LEARNED promotion, or
  experiment execution is established by the merge.

## Holes found after merge

1. **Revision metadata-loss seam.** Generic supersession rebuilt successor
   `content` as `{lesson}`; capability metadata could disappear.
2. **Experiment revision-chain mismatch.** Block-only supersession does not
   create the full Event → Block → Lineage → Relationship → Index → Checkpoint
   chain required by `nayanet-learning-verify`.
3. **Hash-name ambiguity.** Runtime receipt `content_hash` is raw lesson-text
   SHA-256; v2 requires canonical persisted block-content hash.
4. **Production ordering gate.** SQL capability migration is pending while Edge
   source already knows the new RPC argument. Migration/function ordering must
   be proven before production use.

## Repair in this follow-up branch

- preserve bounded capability metadata through generic supersession;
- keep legacy supersession output byte-compatible when optional fields are absent;
- clarify v2 hash semantics and require independent persisted-content reread;
- forbid block-only supersession from standing in for the experiment's full
  learning commit;
- leave deployment, data mutation, promotion, and experiment execution behind
  their existing explicit gates.

## Next consequential gate

After CI proves this follow-up, production promotion of the exact current main
must preserve migration/function deployment ordering and independently prove
runtime parity before any v2 data change.
