# P0 Machine-Falsifiable Gates

**Branch:** `naya5/p0-machine-gates`
**Status:** BUILT — behavioral proofs staged; static checks live.
**Law:** A claim is OPERATIVE only if a machine can falsify it. A gate that cannot fail is not a gate.

## The problem

45 Smart Notes captured real lessons. Most are DESCRIPTIVE (well-written), not OPERATIVE (machine-enforced). Defect classes found that no note prevented:

1. Unbound identifier shipping as opaque HTTP 400 with 13/13 tests green (tests asserted source text, never executed the path).
2. Idempotency key silently undefined → replay guard inert, failing OPEN (1,603 NULL rows).
3. Nine of fourteen edge functions never executed, only grepped.
4. Proof artifact claiming `independent_verification: true` no independent process produced.

## The three gates

### Gate 1 — Idempotency / Replay Safety
`scripts/gate-idempotency-replay.py`

| Check | What it falsifies |
|-------|-------------------|
| I1 | Null/empty/whitespace/wrong-type key ACCEPTED → must be REJECTED (fail closed) |
| I2 | Same key submitted twice, second ACCEPTED → must be REJECTED (replay proved) |
| I3 | Migration without UNIQUE INDEX on idempotency_key → constraint is the law |
| I4 | Receipt-insert code path not setting the key → static population check |

Behavioral core mirrors production semantics: partial unique index (DB refuses duplicates) + fail-closed null rejection (the index alone cannot reject NULLs — NULLs bypass partial unique indexes, which is exactly the 2026-10-06 root cause).

### Gate 2 — Independent Verification
`scripts/gate-independent-verification.py`

| Check | What it falsifies |
|-------|-------------------|
| V1 | verifier identity == executor identity (or missing) → self-attestation reads as NOT verified |
| V2 | no recognized verifier_mode → no declared method |
| V3 | no recomputation evidence AND no concrete reconstruction path → trust is not verification. Two tiers: STRONG (embedded recomputation) / RECONSTRUCTABLE (named artifacts a third party can re-read) |
| V4 | executor_claim_trusted == true → trust is not verification |
| V5 | not reconstructable → no third-party path |

Self-test: the two production receipts PASS (one STRONG, one RECONSTRUCTABLE — tier reported honestly); fabricated self-attested receipts FAIL.

### Gate 3 — Nine-Node Behavioral Influence
`scripts/gate-nine-node-influence.py`

Extends K1–K6 (structural) with the behavioral chain per node:

```
EXISTS → LOADS → INVOKES → INFLUENCES → APPLIES
```

- E: in manifest. L: referenced in runtime CODE (docs/specs excluded). I: invocation call sites. F: decision records showing differential influence. A: applied outcome receipts.
- Honest current state: E passes, L/I/F/A fail → gate FAILS overall. That is the correct signal until the runtime exists. The gate tracks reality, not intent.

## Wiring (follow the gates that already work)

Like `tools/regenerate_brain_index.py --check`: runnable scripts, clear exit codes (0 = pass, 1 = fail naming the gate), deterministic, CI-suitable. Proposed CI wiring:

```yaml
- run: python3 scripts/gate-idempotency-replay.py --root . --migrations supabase/migrations
- run: python3 scripts/gate-independent-verification.py --self-test --root .
- run: python3 scripts/gate-nine-node-influence.py --root . --manifest .naya/specifications/NAYA-MASTER-NODE-KERNEL-V1.json
```

Note: Gate 3 is EXPECTED to fail until the nine-node runtime is built — that failure is the honest signal, not a defect in the gate. CI should record its output as the influence scoreboard.

## Score

- Gate 1: 9/10 — behavioral core proven, static checks live; full DB replay proof needs a live database (read-only constraint).
- Gate 2: 9/10 — self-test green on real + fabricated receipts; tier reporting honest.
- Gate 3: 8/10 — stage logic proven on simulated + real structure; influence/applies stages await the runtime they measure.

Nothing here is merged, deployed, or behaviorally proven in CI. Built ≠ proven. The gates are staged for review.
