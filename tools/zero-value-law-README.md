# Zero Value Law — executable machinery (PROPOSED, NOT RATIFIED)

**Status: DRAFT.** `NAYA-ZERO-VALUE-LAW-V1` is a proposed law. Ratification is
Shawn's gate. This directory holds the executable machinery as draft code only.

## What it is (plain words)

Naya must never confuse "we measured zero" with "we don't know." Unknown,
unmeasured, delayed, and inconclusive are not zero — and the receipt schema now
refuses to let anyone record them as zero.

## Files

- `zero_value_law.py` — the classifier, the cross-field receipt validator, the
  reconsideration trigger, the historical annotator, and the null-discipline auditor.
- `test_zero_value_law.py` — 23 checks: the ten required regression tests, the
  exact gap case from the spec, and supporting guards.

## The six states

| State | Meaning | What Naya does |
|---|---|---|
| TRUE_ZERO | exact zero established for the defined calculation and scope | record zero with its proof |
| PRACTICALLY_NEUTRAL | measured effects within a justified tolerance ε | record as practically neutral, never exact zero |
| UNKNOWN | outcome cannot currently be determined | preserve uncertainty, investigate |
| UNMEASURED | measurement not performed / instrumentation absent | measure before claiming |
| DELAYED | consequences may not yet have occurred/been observed | keep provisional until the window closes |
| INCONCLUSIVE | uncertainty spans positive/neutral/negative | collect more evidence or preserve unresolved |

Plus: BASELINE_ZERO (self-comparison, zero by definition) and
ROUNDED_DISPLAY_ZERO (display convenience; the raw nonzero value is stored and governs).

## The neutral zone (interval math)

With domain tolerance ε (declared, versioned, justified) and interval [L, U]:

- L > ε → POSITIVE
- U < −ε → NEGATIVE
- [L, U] ⊆ [−ε, ε] → PRACTICALLY_NEUTRAL
- everything else → INCONCLUSIVE

The interval's width matters as much as its center. Never overrides LAW or
unresolved critical harms.

## What the validator refuses (machine-readable codes)

- `NULL_ACTUAL_WITH_VERIFIED_VALUE` — d_verified numeric while delta_v_actual is null
  (the exact gap case: `{"verification": "UNVERIFIED", "delta_v_actual": null, "d_verified": 0}`)
- `VERIFIED_VALUE_WITHOUT_VERIFICATION` — d_verified set outside VERIFIED_PASS/FAIL
- `PREDICTED_IS_NOT_VERIFIED` — the prediction laundered into the verified slot
- `ZERO_WITHOUT_ESTABLISHMENT` — zero asserted without a zero interpretation + evidence
- `PRACTICAL_NEUTRALITY_NEEDS_EPSILON` — neutrality claimed without declared/versioned ε
- `INTERPRETATION_VALUE_MISMATCH` — an unknown-family interpretation carrying d_verified
- `ROUNDED_ZERO_NEEDS_RAW` — rounded display without the stored nonzero raw
- `HARM_UNRESOLVED_BLOCKS_NEUTRAL` — no neutral/zero classification over unresolved harm

## Null discipline

`null` means not established. A numeric zero is an assertion. The validator never
coerces null → 0, and `audit_null_discipline()` scans source for coercion patterns
(`or 0`, `.get(..., 0)` on value fields) so the discipline is detectable, not just
declared. This module scans clean.

## Reconciliation note (±9 vs ±10)

The signed-value fix (branch `naya4/value-calculus-signed`) removed the clamp from
`build_decision_receipt` — `d_verified` now carries the verified actual unclamped.
The ±9 anchors are reference vocabulary (display), not clipping bounds. This module
does not reimpose any clamp.

## What this does NOT claim

- It judges the classifications it is given; it does not perform measurements,
  run observation windows, or verify evidence itself.
- A TRUE_ZERO verdict is only as good as the deterministic proof cited.
- Nothing here is ratified. The law needs Shawn's word before it governs.
