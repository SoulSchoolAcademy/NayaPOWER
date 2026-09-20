# Naya Power Handoff — Oscar Implementation Pending CI

## Mission
Build a portable, reliable, human-proof Naya Power runtime whose continuity can be restored from GitHub.

## Current state
PR #36 is open from `feat/oscar-independent-verification`. The implementation adds an independent deterministic Oscar challenge layer on top of Claim → Evidence → Verification.

## Protected baseline
Main before this slice: `823d8369c0e3d622f1937ec3960b2cd654720ee3`.

## Current branch head
`baf0aa3bae3cc571dd0ef0106e635fa83f9fd85f`.

## Implemented
- `.naya/runtime/oscar.py`
- `.naya/runtime/test_oscar.py`
- `.naya/runtime/OSCAR.md`
- Claim Evidence CI now records `criteria_covered` and runs Oscar after builder verification.
- Oscar is deliberately independent: it does not import `evidence_runtime.py`.
- STATE records Oscar as IMPLEMENTED / PENDING_CI.

## Oscar challenge boundary
```text
CLAIM
↓
EVIDENCE
↓
BUILDER VERIFICATION
↓
OSCAR CHALLENGE
↓
PROMOTION DECISION
```

## Current deterministic protections
Oscar rejects forbidden assertion sources, non-PASS evidence, missing provenance, wrong commit, cross-claim evidence, missing commands/output/timestamps, and missing explicit success-criteria coverage.

## Verification
Local representative Oscar tests passed. Existing Claim/Evidence CI run `32682898123` is successful, but it predates the Oscar-integrated workflow revision and therefore does not verify Oscar. Its published artifact was inspected and confirmed to be bound to an older commit.

## Unknown
Fresh CI on the current PR head has not yet been inspected. Do not promote Oscar or merge until fresh exact-commit CI evidence is available.

## Next action
Inspect fresh PR #36 workflow jobs/logs and machine-readable artifact. If green and Oscar returns ACCEPT, update STATE/Smart Note/index as justified, merge, then verify the merged main commit. If anything fails, use First Divergence Law and repair the root cause.
