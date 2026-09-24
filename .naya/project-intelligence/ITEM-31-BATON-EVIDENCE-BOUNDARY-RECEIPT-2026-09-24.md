# NayaPOWER — Item 31 BATON Evidence Boundary Receipt

**Date:** 2026-09-24
**Item:** 31
**Status:** FOCUSED UNIT VERIFIED — FULL ITEM 31 NOT VERIFIED
**Branch:** `coda2/item31-control-plane-freshness`
**Live main at start:** `ad2d2ba466fe60a3443611fb18dead428a57d800`
**Implementation commit:** `ec8d84ef`
**PR:** [#566](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/566)
**Issue:** [#554](https://github.com/SoulSchoolAcademy/NayaPOWER/issues/554)

## First deterministic gap

The prior Item 31 audit stopped at:

```text
BATON_FIELD_MISSING: evidence
```

`BATON-CONTRACT.md` requires a top-level `evidence` field. The existing block evidence list describes required evidence categories; it is not itself a proof receipt. The smallest valid projection therefore uses existing canonical proof sources without copying or promoting claims.

## Smallest repair

The canonical BATON now projects two read-only evidence pointers:

- the active block's existing `proof_receipt`: `.naya/project-intelligence/2026-09-22-PI-HOME-RUN-RECEIPT-35789192530.md`;
- the canonical proof contract's `current_evidence` field in `.naya/control-plane/PROOF.json`.

The builder emits these pointers from existing `BLOCKS.json` and `PROOF.json` data. Both validators require a non-empty evidence list, structured source pointers, safe relative paths, and existing local source files. No evidence store, proof claim, or historical record was rewritten.

## Verification

| Check | Result |
|---|---|
| Focused regression suite | 15/15 PASS |
| Python compilation | PASS |
| Workflow YAML parse | PASS |
| BATON JSON parse | PASS |
| Builder evidence projection | PASS |
| Committed evidence pointers | PASS |
| Missing evidence rejection | PASS |
| Malformed evidence rejection | PASS |
| Missing evidence source rejection | PASS |
| Full audit on execution branch | EXPECTED RED: non-main authority |
| Full audit with branch treated as main | EXPECTED RED: `BATON_SOURCE_SNAPSHOT_STALE` |
| Canonical `baton.py validate` | Existing separate `BATON_HUB_SOURCE_MISMATCH` remains |

The next freshness boundary is `BATON_SOURCE_SNAPSHOT_STALE`, caused by the BATON snapshot predating control-plane changes. The Hub source mismatch remains a separate boundary and was not touched.

## Truth and authority

The focused evidence projection is verified at source/test scope. Full Item 31 remains `IMPLEMENTED — NOT VERIFIED`; PR #566 remains open/unmerged; no main workflow, deployment, service-role operation, or control-plane promotion is claimed.

## Exact successor action

Inspect the canonical BATON snapshot-generation contract and repair only the stale source-snapshot boundary, then rerun the focused suite and freshness audit; do not touch the separate Hub SHA mismatch or Item 30 deployment.
