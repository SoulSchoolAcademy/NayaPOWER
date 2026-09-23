# 🔱 NayaPOWER — Priority 2 Legacy Cognition Disposition Receipt — 2026-09-23

**Status:** VERIFIED COHORT / DISPOSITION REQUIRED
**Boundary:** Exact unlinked cognition cohort
**Rule:** Preserve original cognition rows; no fabricated linkage; no deletion.

## Fresh independent evidence
- Production direct read: 4,718 cognition rows; 88 have no matching `nayanet_smart_ledger` source reference.
- Existing read-only GitHub Actions audit: run `35928554000`, conclusion SUCCESS.
- Audit schema: `NAYANET_SMART_LEDGER_COVERAGE_AUDIT_V1`.
- Audit artifact fingerprint: `58fc76519416537537a4fd6ffaf051041ab90164aecbe60410223222cb90ec8e`.
- Audit grouped the 88 exactly as:
  - 45 communication / observation / nayanet-smart-mail
  - 22 intelligence / observation / nayanet-name-first-runtime-proof
  - 12 intelligence / observation / nayanet-authenticated-assistant-proof
  - 4 intelligence / decision_context_test / dream-learning-decision-proof
  - 4 intelligence / observation / dream-learning-decision-proof
  - 1 verification / authenticated_lifecycle / NayaNET 10/10 readiness gate

## Representative semantics
Representative rows are verification/observation/test evidence events. At least one Smart Mail row already carries an execution receipt; the dream decision rows are test/observation records; name-first and authenticated-assistant rows describe runtime proof observations.

## Disposition
The evidence establishes the cohort precisely, but does **not** establish that every row should receive a new ledger row. The Smart Ledger is an evidence/integrity layer, not a duplicate cognition store. Therefore the correct disposition is **REQUIRE EXPLICIT DISPOSITION ENUM/RULE BEFORE WRITE**.

No production data was changed.

## Next causal boundary
Define the non-destructive disposition contract, then classify each cohort group as one of:
- LEGITIMATE_LEDGERABLE_HISTORICAL
- ALREADY_REPRESENTED_ELSEWHERE
- INTENTIONALLY_EXCLUDED
- NEEDS_REVIEW

Only after the contract is independently verified should any reversible annotation be considered.
