# NayaPOWER — Item 31 Control-Plane Freshness Receipt

**Date:** 2026-09-25
**Item:** 31
**Title:** Control-plane freshness with explicit UNKNOWN identity resolution
**Status:** CANDIDATE VERIFIED — MAINLINE MERGE/CI PENDING
**Branch:** `coda2/item31-control-plane-freshness-mainline-verification-20260925`
**Starting source:** `fa82d32b67131c5cdaec441d0f0787a9921f8370` (`origin/main`)
**Implementation:** PR [#566](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/566), merged as `b48aa8fd6fcc41660e22a99f357e4e2da8658c51`
**Verification commit:** `0402d4be`
**Verification PR:** [#654](https://github.com/SoulSchoolAcademy/NayaPOWER/pull/654)
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
| Explicit UNKNOWN regression suite | PASS | 15/15 tests in `tests/test_control_plane_freshness.py` |
| Case A: unrelated `learning` text | PASS | Does not resolve `UNKNOWN-UNIVERSAL-MODEL-LEARNING-QUALITY` |
| Case B: exact proof reference | PASS | Resolves only with exact `resolves_unknown` identity, valid evidence, and current source commit |
| Case C: partial related text | PASS | Does not resolve |
| Case D: stale proof | PASS | Rejected; no resolution promotion |
| Case E: explicit replacement | PASS | `SUPERSEDED` resolves only with replacement metadata and valid source commit |
| Registry/STATE exact coverage | PASS | 4 registry entries exactly match 4 current `STATE.unknown` statements |
| Pre-repair full audit on clean `origin/main` clone | RED | `BATON_SOURCE_SNAPSHOT_STALE`; the committed BATON predated later control-plane changes |
| Canonical BATON rebuild | PASS | `python .naya/runtime/baton.py build-and-validate` |
| Post-repair full audit on clean `origin/main` clone | FRESH | `status: FRESH`, `outcome: PASS`, all required checks true, `still_unknown_count: 4`, `unknown_resolution_count: 0` |
| Canonical BATON validator | PASS | `python .naya/runtime/baton.py validate` |
| Git diff whitespace check | PASS | `git diff --check` |
| Mainline CI run | NOT OBSERVED | The local clean-clone audit passed; no post-merge GitHub Actions run for this candidate has been observed |

The explicit identity model therefore passes the requested false-positive cases and the full local main-source audit. The four UNKNOWNs remain listed as `UNKNOWN`; no textual overlap, unrelated known statement, partial evidence, or stale proof promoted one.

## Item 30 dependency boundary

Item 30 remains `IMPLEMENTED — PENDING_DEPLOYMENT_VERIFICATION`:

- PR #562 is OPEN and unmerged.
- The Item 30 workflow and both migration paths are absent from `main`.
- The current unauthenticated RPC probe returned HTTP `401`; that auth boundary does not prove the function is deployed, and no service-role or owner-authenticated audit was performed.
- The release authorization artifact remains a template and deployment governance defaults to `DENY`.

Therefore no 88-event classification, fingerprint, audit result, artifact preservation, or Item 30 control-plane closure is claimed.

## Remaining UNKNOWNs and blockers

- All four registered UNKNOWNs remain `UNKNOWN` by explicit policy.
- Item 30 deployment authorization, migration application, workflow execution, and independent audit remain pending.
- This candidate has a passing clean-clone `origin/main` audit, but its BATON update and receipt still require merge and an observed post-merge CI run before canonical Item 31 closure.

## Exact successor action

Obtain explicit authorization for PR #562 deployment, merge it, apply both Supabase migrations, run the main Item 30 workflow, and independently verify the exact 88-event cohort, fingerprint `58fc76519416537537a4fd6ffaf051041ab90164aecbe60410223222cb90ec8e`, `complete: true`, and the preserved artifact before updating any Item 30 control-plane closure state.

## Authority boundary

This receipt proves the explicit UNKNOWN resolution model, the canonical BATON rebuild, and a passing audit against a clean clone of the recorded `origin/main` source. It does not prove production deployment, production classification, merged-main CI passage, or production freshness.
