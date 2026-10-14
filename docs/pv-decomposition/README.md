# PV Decomposition Recipe — B-46 unblocker (CANDIDATE, spec v0.1)

**Status: CANDIDATE, unwired.** Nothing in `kernel/` is touched by this PR.
Wiring `PV-DECOMP-0.1` into `kernel/value_calculus.py` is a protected-se semantics
change — it needs Shawn's word and seat-consensus ratification before any PR
attempts it.

## The problem it solves

`PVEstimate(B, H, C, R)` in the V2.1 decision calculus takes B/H/C/R as
author-supplied floats — there is no canonical recipe deriving them from
evidence. NAYANODE/0025 names "B/H/C/R component gaming" as a threat with no
stated defense. This directory is the missing recipe: deterministic, evidence-
bound, fail-closed term decomposition.

## Contents

| File | What it is |
|---|---|
| `PV-DECOMPOSITION-SPEC-0.1.md` | The normative recipe: Normalize(), term rubric, baseline-pricing rule, Zero Value Law empty-bucket rule |
| `pv_decompose.py` | Reference implementation (stdlib only, deterministic). Mirrors `PVEstimate.pv` with `uncertainty_scale=1.0` |
| `test_pv_decompose.py` | 9 tests: 6 fail-closed rejections, 1 fail-closed degradation invariant, 2 cold-recompute exactness controls |
| `worked-example-2576-repair.json` | Real decision #1 (receipt repair): B=6.0, H=0.0, C=1.4, R=0.4 → pv 4.2 |
| `worked-example-lane1-drill.json` | Real decision #2 (another lane's drill): B=9.0, H=0.0, C=2.0, R=0.9 → pv 6.1 |

## Quick check

```bash
python3 docs/pv-decomposition/pv_decompose.py docs/pv-decomposition/worked-example-2576-repair.json
python3 -m unittest discover -s docs/pv-decomposition -p "test_*.py" -t docs/pv-decomposition
```

## The fail-closed invariant (the load-bearing one)

An unattested empty bucket gets confidence **0.0**, which flows into
`min_component_confidence` and raises residual risk: uncertainty can only
*lower* pv relative to the full-confidence reading of the same magnitudes —
it never hides, and the 0.0 is exposed in the receipt for consumers to gate on.

## Still owed (honest)

1. **Second-seat review** — a different seat re-deriving one example from the
   receipt alone (invited; cannot be self-filled).
2. Residual calibration (`1.0 × (1 − min_conf)`) is untested against real gate
   outcomes; the hours-rate convention (2.0 points/hour) is this-lane-local.
3. Wiring into the kernel: needs Shawn's word + ratification — explicitly NOT
   in this PR.
