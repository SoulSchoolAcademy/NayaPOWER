# Naya Power — P1 Runtime Acceptance + Proof 7 Real Policy Comparison

**Date:** 2026-09-18  
**Project:** NayaNET  
**Status:** P1 runtime acceptance PASS; real policy improvement NOT PROVEN

## What was actually verified

The live P1 acceptance transaction completed end-to-end:

`V1/V2 → deterministic evaluation → adversarial PASS → holdout PASS → unauthorized promotion rejected → explicit authorization → controlled test → observed → verified → promoted → rolled back`

Runtime acceptance markers:

- `P1_POLICY_V1_V2=PASS`
- `P1_DETERMINISTIC=PASS`
- `P1_ADVERSARIAL=PASS`
- `P1_HOLDOUT=PASS`
- `P1_UNAUTHORIZED_PROMOTION_BLOCKED=PASS`
- `P1_CONTROLLED_TEST=PASS`
- `P1_OBSERVED=PASS`
- `P1_VERIFIED_PROMOTION=PASS`
- `P1_ROLLBACK=PASS`

The runtime proof was executed against the live Supabase project using an actual anonymous authenticated session. The production transition function requires the policy owner, VERIFIED state, holdout PASS, adversarial PASS, and explicit incoming authorization before promotion.

## Real Proof 7 comparison

The synthetic equal-score holdout was then bypassed for the first real outcome comparison.

Canonical policy lineage:

- **V1:** `HISTORY_ONLY_V1` — Dream P0 baseline strategy.
- **V2:** `HISTORY_PLUS_VERIFIED_RECEIPT_V1` — Dream P0 counterfactual / verified-learning strategy used by the later Proof 7 decision.

Real observed receipts used:

- **Baseline receipt:** `66631fca-2123-48a4-be1c-f6e7c03d9a78`
- **Candidate receipt:** `068b408f-8af2-49ba-9b82-5fe46b1d399f`
- Both are `smart_mail_send` SUCCESS receipts for the same Proof 7 sender/receiver lineage.
- Both contain authenticated receiver retrieval evidence and verified responsible-value fields.

The canonical deterministic comparison function is `nayanet_compare_verified_policy_outcomes(...)`. It refuses mismatched ownership/project/action lineage and refuses unverified or unsuccessful outcomes.

Observed comparison:

| Measure | V1 | V2 |
|---|---:|---:|
| Real observed outcome | verified | verified |
| Verified responsible value | 0 | 0 |
| Candidate improvement | — | false |
| Policy improvement proven | — | **false** |

**Result: `NOT_PROVEN`.**

This is the correct result. Proof 7 proves that verified learning influenced a later governed action. It does **not** prove that the learned policy produced greater responsible verified value than the baseline. The real outcome comparison now makes that distinction executable rather than inferred.

## Governance consequence

A higher Dream/counterfactual score cannot substitute for a superior verified real-world outcome. V2 remains a candidate until a genuine controlled comparison produces a verified value strictly greater than V1 under the same scoring contract and the required holdout/adversarial/authorization gates.

No policy was promoted from the real comparison. The comparison policies remain `DRAFT`.

## Next action

Build the **controlled paired outcome experiment** on the existing Smart Mail transaction substrate so V1 and V2 each execute against comparable held-out cases, with policy identity recorded in the canonical execution receipt. Then compare observed and verified responsible value without allowing Dream to self-authorize promotion.
