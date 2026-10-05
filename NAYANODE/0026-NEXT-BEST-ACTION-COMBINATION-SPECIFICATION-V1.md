# NayaPOWER Next-Best-Action Combination Specification V1

**Status:** CANDIDATE — implementation and focused tests verified on branch; human-director ratification pending.
**Purpose:** deterministic prioritization of already-admissible candidate actions for proactive Naya seats.
**Canonical parent:** `NAYANODE/0025-VALUE-CALCULUS-SPECIFICATION-V1.md` (Decision Value Calculus V2.1).

## Boundary
This is a **priority-combination layer**, not a second decision engine. It does not grant authority, override LAW, replace the Value Calculus, replace interval dominance, or create another ledger.

`RECONSTRUCT → GATE (V2.1) → GENERATE → COMBINE → RANK → SELECT/READ_MORE → ACT/ASK/REFUSE → VERIFY → LEARN`

Hard gates always precede scoring.

## Ten dimensions
Exactly ten. **Compounding & Continuity is intentionally one dimension.**

| Dimension | Weight | Direction |
|---|---:|---|
| Mission Value | 0.18 | higher is better |
| Human Value | 0.18 | higher is better |
| Urgency | 0.08 | higher means waiting matters more |
| Leverage | 0.12 | higher means more downstream unlock |
| Evidence | 0.14 | higher means stronger evidence |
| Risk | 0.10 | higher is worse; inverted |
| Cost | 0.05 | higher is worse; inverted |
| Dependencies | 0.05 | higher means more dependency resolution/unlock |
| Reversibility | 0.04 | higher means safer recovery |
| Compounding & Continuity | 0.06 | higher means stronger durable future gain |

Weights sum to **1.00**.

## Combination
For normalized inputs (x_d ∈ [0,10]):

`NBA(a) = Σ w_d × f_d(x_d)`

with `f(x)=x` for favorable dimensions and `f_risk(x)=10-x`, `f_cost(x)=10-x`.

The raw risk/cost values remain preserved for explanation and gates.

## Thresholds
- ACT-capable score: **≥ 9.0**
- Below-standard: **< 7.0**
- Evidence floor: **≥ 8.0**
- Human-value floor: **≥ 7.0**
- Risk ceiling for autonomous selection: **≤ 3.0 raw burden**
- Reversibility floor: **≥ 7.0**
- Priority dominance margin: **≥ 0.10**

These are not constitutional gates. The parent V2.1 gate and interval-dominance rules remain authoritative.

## Tie-breakers
After score: Evidence → Human Value → Urgency → Leverage → Reversibility → lower Risk → lower Cost → stable candidate ID.

A close top pair returns **READ_MORE / NO_CLEAR_DOMINANT_OPTION** rather than false certainty.

## Recalibration
Weights and thresholds are versioned hypotheses. Verified outcomes may propose changes through the existing V2.1 VALUE_RECALIBRATION pathway. Promotion requires independent verification and applicable authority.

## Proof
`SPEC → MACHINE SCHEMA → RED TEST → GREEN IMPLEMENTATION → ADVERSARIAL TESTS → DECISION RECEIPT → INDEPENDENT RECOMPUTATION → COLD SUCCESSOR`

Current branch evidence: focused suite **9/9 passed** on the authorized Windows machine. Production proof is not claimed.
