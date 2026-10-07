# IB-SMART-NOTE — SN-0523 — Proof Scope Is Part of the Proof

**Intelligent Block:** SN-0523
**Truth state:** CANDIDATE
**Scope:** PRIVATE (Team Naya operating intelligence)
**Captured:** 2026-10-07
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## IN A NUTSHELL

A proof is not honest merely because its measurement is real. The receipt must also name **what was measured, which engine produced the measurement, and what that measurement does NOT prove**.

In the nine-node acceptance seam, the measured influence came from the reference BRAIN.Engineering.kernel_behavior_engine.KernelBehaviorEngine, while the bounded runtime kernel is kernel.nayapower_kernel.Kernel. Without an explicit boundary, a valid 9/9 reference-engine result could be misread as production-runtime influence.

The repair is therefore proof-language, not runtime behavior: receipts now state the measurement scope, runtime kernel, measured engine, and production_runtime_influence = NOT_PROVEN.

## HUMAN NOTE

Truth needs boundaries around it.

A number can be perfectly measured and still be misleading if the reader cannot tell what system produced it. If a reference engine demonstrates influence, say exactly that. Do not let the receipt silently inherit the authority of a different runtime.

The honest receipt answers four questions:

1. **Scope:** What system/path was measured?
2. **Runtime identity:** What is the canonical runtime kernel?
3. **Measurement identity:** What engine actually produced the result?
4. **Limit:** What stronger claim remains unproven?

If the stronger claim has not been earned, the receipt says so plainly.

## CHILD NOTE

If you test one toy car and it drives, you can say **that car drove**. You cannot say **every car drives**.

Always write down which car you tested and what the test does not prove.

## GRANDMA NOTE

Don't let a true number tell a bigger story than the test earned. Name the thing tested, name the thing you mean, and name the gap between them.

## NAYA NOTE

This is a proof-integrity law for every acceptance receipt.

**Measured ≠ universal.  
Reference ≠ production.  
Structural ≠ behavioral.  
Behavioral ≠ causal.  
Exact-revision proof ≠ later-main proof.**

Every proof projection should make those boundaries mechanically visible instead of relying on reader inference.

## MACHINE NOTE

```json
{
  "smart_note_id": "SN-0523",
  "truth_state": "CANDIDATE",
  "proof_rule": "RECEIPT_SCOPE_MUST_MATCH_MEASURED_SYSTEM",
  "required_fields": [
    "measurement_scope",
    "runtime_kernel",
    "measured_engine",
    "production_runtime_influence"
  ],
  "current_reference_measurement": "BRAIN.Engineering.kernel_behavior_engine.KernelBehaviorEngine",
  "canonical_runtime_kernel": "kernel.nayapower_kernel.Kernel",
  "current_production_runtime_influence": "NOT_PROVEN",
  "anti_inference_rule": "DO_NOT_PROMOTE_REFERENCE_ENGINE_MEASUREMENT_TO_PRODUCTION_RUNTIME_PROOF",
  "implementation_receipt": "live-supabase-runtime-proof.yml",
  "acceptance_test": "tests/load_bearing_claims.test.mjs"
}
```

## LEARNING LESSON

The dangerous failure was not a false measurement. It was an **ambiguous measurement boundary**.

That distinction matters because NayaPOWER is designed to compound verified intelligence. An ambiguous receipt can become future misinformation when retrieved cold, reused by another seat, or summarized into a later decision.

Therefore, proof metadata is load-bearing intelligence. The system must preserve the boundary at capture time rather than asking future readers to reconstruct it.

## HOW TO APPLY

Whenever a proof claims that a system, node, engine, workflow, or runtime has an effect:

- identify the exact measured implementation;
- identify the canonical implementation the claim might otherwise be confused with;
- state the measurement scope;
- state the strongest claim actually earned;
- state the stronger claim that remains unproven;
- make the distinction machine-testable where practical.

If the receipt cannot answer those questions, the proof is incomplete even when the underlying measurement is valid.

## PROOF / PROVENANCE

- PR: #1740 — fix(proof): label reference-engine influence boundary
- Repair commits on the active branch include the scope-label repair and exact Brain-index refresh.
- Current branch head after index refresh: d0b92f4468595e36921f1f692e5e9d0690996ec3
- Exact-main base at repair start: 75f6e225481bc0e8753cadd644e2b5b6f67d4173
- RED → GREEN load-bearing claim: 13/13
- Focused independent-verifier / influence tests: 31/31
- YAML parse: PASS
- Brain index after refresh: OK: index layer matches git tree (233 files)
- No production deployment, database mutation, credentials change, or authority change was made.

## TRUTH BOUNDARY / UNCERTAINTY

This Smart Note records a verified engineering lesson and is **CANDIDATE**, not RATIFIED. The repair proves the receipt now distinguishes reference-engine influence from production-runtime influence. It does **not** prove production-runtime nine-node influence; that remains explicitly NOT_PROVEN.

## NEXT ACTION / SUCCESS CONDITION

Carry this rule into every proof-producing workflow: **the receipt must make the proof boundary impossible to misread.**

Success is behavioral: future acceptance receipts cannot silently conflate a measured reference engine with the canonical production runtime.