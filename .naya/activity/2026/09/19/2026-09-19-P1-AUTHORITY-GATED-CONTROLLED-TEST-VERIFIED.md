# 2026-09-19 — Hardened P1 Authority-Gated Controlled Test Verified

- Hardened P1 run: 35410036258
- Source commit executed: 680701bdec5d1d4f6d4b10648da8e1ce921bf672
- Job: Real V1/V2 paired Smart Mail outcome experiment — SUCCESS
- Canonical receipt artifact: p1-controlled-paired-policy-receipt
- Artifact id: 10574395779
- Artifact digest: sha256:92987797df03502e8e526c6c090b8836cc6c8e427991a97adc7581962eb7e326

## Authority proof
- The experiment first attempted CONTROLLED_TEST with authorized:true but no grant and required the canonical gate to reject it.
- It then issued and validated a canonical Authority Grant with action policy.controlled_test scoped to the exact policy id.
- Persisted grants for run 35410036258 have issuer_id = subject_id and ACTIVE status.
- Supabase nayanet_policy_transition now requires that grant and validates it through nayanet_validate_authority_grant.

## Outcome
- REAL_OUTCOME is VERIFIED.
- Baseline responsible value: 0.
- Candidate responsible value: 0.
- Result: NOT_PROVEN.
- Baseline receipt: 5e55a270-f2b5-4e13-8592-c9f88a592731.
- Candidate receipt: f56d44c2-ca8e-4a1f-8fbd-a93e662cf59e.
- Equal verified value remains correctly NOT_PROVEN; no promotion follows.

## Evidence blocker
Current Smart Mail / Proof 7 / Dream failed runs remain completed failures with zero jobs returned by the connected GitHub job endpoint. Their runtime causes remain UNKNOWN/BLOCKED. No gate has been weakened and no runtime cause has been invented.

## Next exact action
Move to OBSERVE → VERIFY → COMPARE → LEARN for the governed controlled-test transaction, and only after that resume authenticated cold-Naya lifecycle proof. In parallel, obtain runner-level evidence for Smart Mail / Proof 7 / Dream through an evidence surface that exposes job/step/log output; otherwise preserve UNKNOWN/BLOCKED.
