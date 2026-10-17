# UD-15 — Baseline Evolution, With Evidence

**Plain words:** "Normal" is allowed to change — workloads grow, traffic shifts,
seasons turn. But change happens on evidence, never by drift. Every baseline
change records what changed, why, and the evidence. Old baselines are
superseded, never overwritten. Silent drift is caught, not absorbed.

## The three references (never one self-changing baseline)

| Reference | Job |
|---|---|
| `FROZEN_REFERENCE` | Immutable, independently qualified picture of normal. Never moves. |
| Adaptive candidate | Learns in shadow. Explains patterns, never replaces the contract. |
| `PROMOTED` (operational) | The current baseline. Changes only through the promotion gate. |

## The promotion gate (conjunctive — never an aggregate score)

`CANDIDATE → SHADOW → INDEPENDENTLY_QUALIFIED → PROMOTED`.
Every step must pass; one failure refuses. The hard obligations:

1. **Training clean** — no `UNRESOLVED_ANOMALY`, `CONFIRMED_REGRESSION`, or
   `INSUFFICIENT_OBSERVABILITY` in the training window. Unresolved incidents
   never define normality. Training scope must match the promoted scope.
2. **Evidence present** — cited evidence refs, a stated reason, and a recorded
   old-vs-new comparison. A silent change is refused.
3. **Independent qualification** — verifier ≠ proposer. Self-qualification refused.
4. **No local regression** — the candidate must not regress the frozen reference
   beyond tolerance (direction-aware: higher- and lower-is-better metrics).
   Aggregate improvement never overrides a local regression.

`PROMOTED` is reachable **only** via `promote()`. `advance_stage()` handles the
middle stages and refuses the final jump.

## Scope isolation (D52)

Every observation carries four permanent scope IDs
`(service, region, endpoint, tenant)`. Statistical pooling may share estimates
across comparable scopes, but **never transfers certification**: a sparse scope
under a healthy parent stays unqualified (`per_scope_qualified`).

## Dual-reference comparison (D49)

The adaptive model is compared against the immutable frozen reference. Because
the reference cannot move, "both drifting together" is still detected.

## Drift detection

`check_decision_baseline()` refuses any decision computed on a baseline that is
not the ledger's current `PROMOTED` version for that scope+metric:
`STALE_BASELINE`. `audit_promotions()` detects `PROMOTED` records smuggled in
via direct append — silent drift is flagged, with the broken chain named.

## Cold reconstruction

Every promotion is rebuildable from its record alone
(`reconstruct_promotion()`): scope, values, evidence, comparison, reason,
verifier.

## Run the tests

```
cd ~/workspace/tools && python3 -m pytest test_baseline_evolution.py -q
```

## What this does NOT claim

This module governs baseline evolution records; it does not measure the outside
world. A promoted baseline is only as good as its cited evidence and the
independence of its verifier. The statistical checks are structural guards, not
a substitute for domain measurement.
