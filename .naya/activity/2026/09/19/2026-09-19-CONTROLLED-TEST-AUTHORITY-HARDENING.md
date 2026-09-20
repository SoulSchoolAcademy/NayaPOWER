# 2026-09-19 — Controlled Test Authority Hardening + Runner Evidence

## Inspected
- Live main advanced to 680701bdec5d1d4f6d4b10648da8e1ce921bf672.
- P1 run 35409836458 succeeded with the corrected runner-temp receipt path and uploaded artifact.
- Supabase nayanet_policy_transition previously accepted client-supplied authorized:true for CONTROLLED_TEST without canonical grant validation.
- Existing nayanet_issue_authority_grant and nayanet_validate_authority_grant provide the canonical grant substrate.
- Smart Mail, Proof 7, and Dream current failed runs expose no jobs through the GitHub connector.

## Executed
- Applied migration 20260919003748_require_authority_grant_for_controlled_test_202609190001.
- CONTROLLED_TEST now requires an authority grant id, validates action policy.controlled_test against the exact policy id, requires AUTHORIZED status, and requires the grant subject to equal auth.uid().
- Updated scripts/run-controlled-paired-policy-experiment.mjs to require a blocked self-authorization attempt, then issue and validate a canonical Authority Grant before CONTROLLED_TEST.
- Updated the P1 workflow trigger to include the actual migration path.

## Verified
- P1 run 35410014462 succeeded after the authority migration and produced the canonical p1-controlled-paired-policy-receipt artifact.
- Its persisted REAL_OUTCOME is VERIFIED but NOT_PROVEN: baseline responsible value 0, candidate responsible value 0.
- Fresh hardened P1 run 35410036258 is executing against commit 680701bdec5d1d4f6d4b10648da8e1ce921bf672; final result pending at record time.

## Evidence Blocker
- Runs 35410034895 (Dream), 35410035248 (Proof 7), 35410026349 (Proof 7), and 35410025861 (Dream) are completed failures, but GitHub's job endpoint returns zero jobs for each. No runtime cause is asserted.
- Classification: UNKNOWN/BLOCKED — runner execution evidence unavailable through the connected GitHub evidence surface. Gates remain intact.

## Protected
- No promotion authority was broadened.
- No verifier/gate was weakened.
- No failure was converted to PASS.
- Authenticated cold-Naya lifecycle proof remains deferred until the Authority → Controlled Test → Observe → Verify → Compare → Learn → Continue chain is proven.

## Next
Consume fresh P1 run 35410036258; if successful, verify persisted authority provenance and controlled-test transition. Then diagnose Smart Mail / Proof 7 / Dream only from obtainable runner evidence, otherwise preserve UNKNOWN/BLOCKED and proceed to the observation/verification/learning continuation boundary.
