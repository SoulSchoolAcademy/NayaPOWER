# 04 — Verification, Governance and Delivery

## State vocabulary
Use repository evidence to distinguish: `VERIFIED`, `LIVE VERIFIED`, `INDEPENDENTLY VERIFIED`, `IMPLEMENTED`, `TESTED`, `UNKNOWN`, `STALE`, `SUPERSEDED`, `BLOCKED`.

Never promote a conceptual definition to VERIFIED without runtime evidence appropriate to the claim.

## Build gate
```text
REQUIREMENT
 ↓
SOURCE OF TRUTH
 ↓
IMPLEMENTATION
 ↓
BUILD
 ↓
DEPLOY
 ↓
AUTHENTICATED RUNTIME
 ↓
OBSERVE
 ↓
VERIFY
 ↓
RECORD EVIDENCE
```

## Front-end verification
- Correct route and navigation.
- Correct authenticated identity.
- Correct loading/empty/error/unauthorized states.
- Correct data from canonical API.
- Consequential actions produce observable result.
- Refresh/retrieval preserves intended state.
- Source/build/deployed UI parity is checked where deployment is involved.

## Back-end verification
- API/function exists at the expected runtime boundary.
- Authentication and object-level authorization are enforced.
- Mutation persists to canonical store.
- Expected event/receipt/ledger state is emitted.
- Fresh retrieval returns the resulting state.
- Replay/idempotency behavior is proven where required.
- Revocation-at-use is proven for authority-sensitive operations.

## Evidence lineage
For consequential capabilities, record the complete chain:
```text
REQUEST → AUTHORITY → EXECUTION → RESULT → PERSISTENCE → RETRIEVAL → OBSERVATION → VERIFICATION → RECEIPT/EVIDENCE
```
A screenshot alone is not persistence proof. A database row alone is not user-experience proof. A successful build is not production proof.

## Governance
- Human authority remains the source of consequential permission.
- Quality is part of correctness.
- Recommendation is not authority.
- Popularity is not truth.
- No physical harm.
- No retry without new information.
- No dead-end completion state when an actionable continuation exists.
- Builder and Judge roles remain distinct.

## Oscar / scorecard
Scorecarding may evaluate quality, but it does not replace evidence or runtime verification. Every failed acceptance criterion becomes an explicit repair item; after repair, rerun the relevant proof.

## Feature acceptance baseline
A NayaNET feature is ready for runtime closure only when the feature specification's required human flow, API/data flow, permissions, persistence, cross-system events, failure cases and verification path are implemented and observed. Any remaining uncertainty must be stated rather than hidden.

## Source authority
01–58 system directive; `.naya/2026-09-11-16-50-NAYAPOWER-26-SCORECARDING-OSCAR-SMART-NOTE.md`; `.naya/2026-09-11-18-20-NAYAPOWER-31-AUTHORITY-REGISTRY.md`; `.naya/2026-09-12-NAYAPOWER-51-HUB-RUNTIME-DEPLOYMENT-VERIFICATION-CONTRACT.md`; `.naya/2026-09-12-NAYAPOWER-52-HUB-MASTER-BUILD-PLAN-AND-ACCEPTANCE-TEST.md`; `.naya/2026-09-12-NAYAPOWER-58-ULTIMATE-TRUST-LOOP-BLUEPRINT.md`.
