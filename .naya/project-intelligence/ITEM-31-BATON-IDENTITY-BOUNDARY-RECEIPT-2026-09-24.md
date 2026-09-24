# NayaPOWER — Item 31 BATON Identity Boundary Receipt

**Date:** 2026-09-24
**Item:** 31
**Status:** FOCUSED UNIT VERIFIED — FULL ITEM 31 NOT VERIFIED
**Branch:** `coda2/item31-control-plane-freshness`
**Live main at start:** `ad2d2ba466fe60a3443611fb18dead428a57d800`
**Implementation commit:** `10fc48e0`
**PR:** [#566](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/566)
**Issue:** [#554](https://github.com/SoulSchoolAcademy/NayaPOWER/issues/554)

## First deterministic gap

The prior Item 31 audit stopped at:

```text
BATON_FIELD_MISSING: identity
```

`BATON-CONTRACT.md` requires a top-level `identity`, but the canonical builder emitted only `source_of_truth.identity`, which is a registry path. The top-level repository identity was therefore absent.

## Smallest repair

- Added top-level `identity` to the canonical BATON artifact.
- Made the builder derive it from `state.repository` rather than hardcoding a second identity authority.
- Made both the builder validator and Item 31 freshness validator require `identity == repository == SoulSchoolAcademy/NayaPOWER`.
- Added one contract sentence defining that exact meaning.
- Added positive, committed-artifact, missing-field, and outcome-classification regression tests.

No unrelated BATON field was added in this unit. The next missing field remains explicit RED.

## Machine-readable outcome boundary

The freshness validator now emits:

- `outcome: PASS` with `status: FRESH` only when all invariants pass;
- `outcome: EXPECTED_RED` with `status: RED` and `first_divergence` for a deterministic contract divergence;
- `outcome: INFRASTRUCTURE_FAILURE` for repository/input infrastructure failure.

The workflow continues after a deterministic audit RED so it can validate and upload the machine-readable artifact, but fails on infrastructure failure. Unrelated Cloudflare Workers checks are not consumed as Item 31 evidence.

## Verification

| Check | Result |
|---|---|
| Focused regression suite | 10/10 PASS |
| Python compilation | PASS |
| Workflow YAML parse | PASS |
| BATON JSON parse | PASS |
| Builder identity output | PASS |
| Missing identity rejection | PASS |
| Expected RED classification | PASS |
| Infrastructure classification | PASS |
| Full audit on execution branch | EXPECTED RED: non-main authority |
| Full audit with branch treated as main | EXPECTED RED: `BATON_FIELD_MISSING: evidence` |
| Canonical `baton.py validate` | Existing separate `BATON_HUB_SOURCE_MISMATCH` remains |

The full Item 31 workflow has not run on `main`; PR #566 remains open and unmerged. No production, deployment, or current-main freshness claim is made.

## Remaining boundary

`BATON_FIELD_MISSING: evidence` is now the first deterministic Item 31 gap. The existing `BATON_HUB_SOURCE_MISMATCH` is a separate stale-source boundary. Neither is silently repaired here.

## Exact successor action

Inspect the canonical BATON evidence contract and add only the smallest contract-compliant `evidence` projection, then rerun the Item 31 focused suite and freshness audit; keep Item 30 deployment and all control-plane promotion boundaries untouched until their authorized proof exists.
