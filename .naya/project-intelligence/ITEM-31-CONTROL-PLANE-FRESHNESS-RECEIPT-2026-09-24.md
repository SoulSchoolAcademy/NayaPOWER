# NayaPOWER — Item 31 Control-Plane Freshness Receipt

**Date:** 2026-09-24
**Item:** 31
**Title:** Control-plane freshness with explicit UNKNOWN identity resolution
**Status:** IMPLEMENTED — NOT VERIFIED
**Branch:** `coda2/item31-control-plane-freshness`
**Starting source:** `ad2d2ba466fe60a3443611fb18dead428a57d800` (`origin/main`)
**Commit:** `08a3b1ebc146a7f18edf56cc742f25279d5d464e`
**PR:** [#566](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/566)
**Related issue:** [#554](https://github.com/SoulSchoolAcademy/NayaPOWER/issues/554)

## Original problem

The inherited Item 31 validator inferred UNKNOWN resolution from ordinary word overlap. An unrelated known statement containing words such as `hub`, `retrieval`, `learning`, or `quality` could incorrectly resolve an UNKNOWN. That is not identity-level evidence and violates the governing law that UNKNOWN is not RESOLVED by inference.

## Implementation

### Explicit identity registry

`.naya/control-plane/UNKNOWN-REGISTRY.json` assigns stable identities to all four current `STATE.unknown` statements:

- `UNKNOWN-HUB-BRIDGE-RETRIEVAL`
- `UNKNOWN-COLD-BRIDGE-SUCCESSOR`
- `UNKNOWN-UNIVERSAL-COMPUTATION-SAVINGS`
- `UNKNOWN-UNIVERSAL-MODEL-LEARNING-QUALITY`

Each entry preserves the original statement, `UNKNOWN` status, introduction source, and evidence required for resolution. No current UNKNOWN was removed or promoted.

### Explicit resolution ledger

`.naya/control-plane/UNKNOWN-RESOLUTION-LEDGER.json` defines the proof record contract. A future record must contain an exact `resolves_unknown` identity and evidence. `RESOLVED` and `SUPERSEDED` records require a source commit that exists and is an ancestor of live HEAD. `SUPERSEDED` additionally requires explicit replacement metadata. `BLOCKED` requires a blocker and external dependency. `STILL_UNKNOWN` remains listed.

### Fail-closed validator

`scripts/validate-control-plane-freshness.py` now:

- resolves repository HEAD and branch as the current authority;
- requires exact agreement for active block, block status, and every next-action representation;
- validates UNKNOWN identities by exact ID/statement only;
- rejects missing, duplicate, stale, incomplete, or contradictory resolution records;
- validates the canonical proof contract and recording commit;
- validates the baton source snapshot and control-plane generation boundary;
- validates the canonical Hub SHA across STATE, MAP, BATON, and the Team Naya lock;
- writes `status: FRESH` only after every invariant passes, and writes a `RED` artifact on failure.

### CI workflow

`.github/workflows/validate-control-plane-freshness.yml` runs the five regression tests, the fail-closed audit, artifact assertions, and artifact upload. It is configured for `main` and scheduled audits.

## False-positive discovery and correction

The inherited implementation used:

```text
any(keyword in k.lower() for keyword in u_lower.split() if len(keyword) > 4)
```

That mechanism was removed. The validator does not inspect statement text for similarity and does not inspect `known` or unrelated proof text to infer identity. Only an exact registry identity plus an explicit resolution record can change state.

## Tests and observations

| Check | Result | Evidence |
|---|---|---|
| Python syntax | PASS | `python -m py_compile scripts/validate-control-plane-freshness.py tests/test_control_plane_freshness.py` |
| Explicit UNKNOWN regression suite | PASS | 5/5 tests in `tests/test_control_plane_freshness.py` |
| Case A: unrelated `learning` text | PASS | Does not resolve the model/provider UNKNOWN |
| Case B: exact proof reference | PASS | Resolves only when the UNKNOWN is removed from the active list and valid evidence is supplied |
| Case C: partial related text | PASS | Does not resolve |
| Case D: stale proof | PASS | Rejected; no resolution promotion |
| Case E: explicit replacement | PASS | `SUPERSEDED` resolves only with replacement metadata and valid source commit |
| Registry/STATE exact coverage | PASS | 4 registry entries exactly match 4 current STATE UNKNOWN statements |
| Full audit on execution branch | RED | Expected: `NON_MAIN_CURRENT_AUTHORITY: coda2/item31-control-plane-freshness` |
| Full audit with branch treated as main for isolated checking | RED | UNKNOWN gate passed; first remaining divergence was `BATON_FIELD_MISSING: identity` |

No Item 31 CI run has been observed on `main`. PR #566 is open; its observed checks are unrelated failing Cloudflare Workers Builds, and the new workflow is not available for dispatch until the workflow exists on the default branch. The validator has not been promoted to `VERIFIED` or `FRESH` for the live control plane.

## Item 30 dependency boundary

Item 30 remains `IMPLEMENTED — PENDING_DEPLOYMENT_VERIFICATION`:

- PR #562 is OPEN and unmerged.
- The Item 30 workflow is absent from `main`.
- Both migration paths are absent from `main`.
- A direct production RPC probe returned HTTP `404` / `PGRST202` for `nayanet_legacy_cognition_disposition_audit`.
- The release authorization artifact remains a template and deployment governance defaults to `DENY`.

Therefore no 88-event classification, fingerprint, audit, artifact, or Item 30 control-plane closure is claimed.

## Remaining UNKNOWNs and blockers

- All four registered UNKNOWNs remain `UNKNOWN` by explicit policy.
- Item 30 deployment authorization, migration application, workflow execution, and independent audit remain pending.
- The live control plane currently has a separate baton/Hub freshness boundary that must be reconciled after authorized proof, not hidden by this implementation.

## Exact successor action

Obtain explicit authorization for PR #562 deployment, merge it, apply both Supabase migrations, run the main Item 30 workflow, and independently verify the exact 88-event cohort, fingerprint `58fc76519416537537a4fd6ffaf051041ab90164aecbe60410223222cb90ec8e`, `complete: true`, and the preserved artifact before updating any control-plane closure state.

## Authority boundary

This receipt proves implementation and local regression behavior only. It does not prove production deployment, production classification, current-main CI passage, or control-plane freshness.
