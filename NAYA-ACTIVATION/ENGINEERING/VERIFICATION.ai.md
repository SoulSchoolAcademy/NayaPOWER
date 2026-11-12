# VERIFICATION — AI TONGUE

**Source (human tongue):** `NAYA-ACTIVATION/ENGINEERING/VERIFICATION.md`
**Machine tongue:** `NAYA-ACTIVATION/ENGINEERING/verification.machine.json`

## Verification ladder (exact — these states are not interchangeable)

**UNKNOWN -> IMPLEMENTED -> TESTED -> VERIFIED -> PRODUCTION_PROVEN**

## Claim-evidence binding

For each claim, identify the exact evidence that could prove it. Verify the evidence independently where practical. A green workflow proves what that workflow observed; it does not automatically prove the larger system claim.

## Negative evidence

Record failures, blockers, unsupported capabilities and unresolved discrepancies explicitly. Not proven is a valid and necessary result.

## Verification target

Follow the real causal path: source -> runtime seam -> persisted state -> retrieval -> behavior -> outcome -> independent evidence.

## Review

Challenge the claim, inspect actual artifacts and look for missing links, stale references, false positives, bypassed gates and hidden assumptions.
