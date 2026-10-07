# The Naya Calculator V1 — AI Specification

*For Naya seats building with it. Exact values, procedures, constraints.*

## 1. What it is (one sentence)

The Calculator is a deterministic measurement instrument: `assess(subject, rubric_id, rubric_version, context) → Assessment`. It computes scores against encoded rubrics. It does not judge, decide, or authorize.

## 2. Positioning — what it is and is not

| Instrument | Role | The Calculator's relationship |
|---|---|---|
| SCORECARD-LAW-V1 (supreme) | Procedure: enumerate → score → gate → decide → receipt | The Calculator executes the SCORE step. The Law stays above it. |
| NAYA-DECISION-VALUE-CALCULUS-V2.1 | Decision math: filters inadmissible actions, scores admissible options, selects ACT/READ_MORE/ASK/REFUSE | The Calculator shares its value-function math but scores OUTPUTS, not decisions. It never selects actions. |
| tools/auto_merge_gate.py | Enforcement predicate for FULL-AUTO-MERGE-V1 | The Calculator feeds evidence INTO scorecard receipts. It is not a merge authority. |
| tools/design_law/design_calculator.py (Naya 5) | Domain rubric: scores HTML against the design standard | A domain rubric PLUGIN the Calculator hosts. Not a duplicate. |
| PV/S value function | PV∈[−9,9] decides above/below the line; S∈[0,10] carries the 9.0 bar | The Calculator's output schema. Every assessment carries both. |

**Hard invariant (from SN-042):** a score is a decision aid, not an authority loophole. No Calculator score overrides a hard safety, privacy, constitutional, or authority boundary. VALUE != AUTHORITY. SCORE != TRUTH.

## 3. Inputs

An assessment request is a 4-tuple. All four are required; missing input = fail closed (no assessment).

| Input | Type | Requirements |
|---|---|---|
| `subject` | bytes + metadata | The output being scored. Content-addressed: `sha256(content)` is the subject identity. Metadata: `subject_type` (design, app, decision, report, ...), `author`, `created_at`. |
| `rubric_id` | string | Which encoded rubric. Must resolve to a published rubric in the registry. |
| `rubric_version` | string | Pinned version. `latest` is FORBIDDEN — reproducibility requires a pinned version. |
| `context` | object | `assessor_id`, `assessed_at` (UTC ISO), `intent` (gate_decision | quality_check | comparison | scheduled_rescore), `evidence_basis` (citations the scores rest on). |

## 4. Rubrics

### 4.1 Rubric schema

A rubric is a versioned JSON document:

```json
{
  "rubric_id": "ten-area-scorecard",
  "version": "1.0.0",
  "ratified_by": "Shawn Vibert",
  "ratified_at": "2026-10-05T...",
  "status": "RATIFIED",
  "dimensions": [
    {
      "id": "learning",
      "name": "LEARNING",
      "weight": 0.15,
      "scale": {"min": 0, "max": 10},
      "evidence_required": true,
      "criteria": "what a 10 looks like, what a 0 looks like",
      "gates": []
    }
  ],
  "aggregation": "weighted_mean",
  "floor": 9.0,
  "value_function": {"pv_range": [-9, 9], "s_range": [0, 10]}
}
```

### 4.2 Rules

- **Weights sum to 1.** `Σw_i = 1`. The canonical formula (per repo AGENTS.md decision compression): `weighted_score = Σ(w_i × score_i)`, applied after hard-gate filtering.
- **Immutable once published.** A published rubric is never edited. Changes = new version (`1.0.0` → `1.1.0`). Version history is the audit trail.
- **Ratification.** A rubric is CANDIDATE until the Human Director ratifies it. Only RATIFIED rubrics may be used for gate decisions. CANDIDATE rubrics may be used for quality checks with the status visible in the assessment.
- **Evidence-required dimensions** must cite evidence. A dimension score without its required evidence citation = dimension fails closed = assessment incomplete.
- **Seed rubrics (V1):** `ten-area-scorecard` (from SN-0343, the ratified ten areas + weights), `design-standard` (from Naya 5's design calculator categories), `decision-quality` (from the Scorecard Law's four scoring dimensions).

## 5. The math

### 5.1 Aggregation

1. **Gate filter first.** Any dimension with a `gates` list: evaluate gates. A failed gate on a dimension zeroes that dimension's contribution AND flags the assessment `gate_failed: true`. Gates are hard stops — no score overrides them.
2. **Weighted mean.** `S = Σ(w_i × s_i)` where `Σw_i = 1`, `s_i ∈ [0,10]`.
3. **Value function.** `PV ∈ [−9,9]`: computed from the assessment's position relative to the floor and the stakes. Positive = above the line (ship/green), negative = below (rework/red). `S ∈ [0,10]` is the aggregated score itself, carrying the 9.0 bar.

### 5.2 Reproducibility guarantee

The assessment is a **pure function** of `(subject_sha256, rubric_id, rubric_version, context)`.

- Same inputs → byte-identical assessment. Always.
- The assessment carries `assessment_id = sha256(subject_sha256 + rubric_id + rubric_version + canonical_context)`.
- If two assessments of the "same" subject disagree, the machine diffs the inputs and names which one changed (subject content, rubric version, or context). Disagreement is always explainable.

### 5.3 Determinism constraints

- No wall-clock reads inside scoring (timestamps are inputs, not sampled).
- No model inference inside scoring. The Calculator measures against encoded criteria; any AI judgment happens OUTSIDE, in the evidence-gathering step, and its outputs are frozen as evidence inputs before scoring.
- Floating point: round to 2 decimal places at dimension level, 2 at aggregate. Rounding rule is part of the spec so implementations agree byte-for-byte.

## 6. Outputs — the Assessment object

Every assessment MUST contain all of the following. An assessment missing any item is not closed.

```json
{
  "assessment_id": "sha256(...)",
  "subject_sha256": "...",
  "rubric_id": "ten-area-scorecard",
  "rubric_version": "1.0.0",
  "assessed_at": "2026-10-09T...Z",
  "assessor_id": "naya-2",
  "intent": "gate_decision",
  "dimension_scores": [
    {"dimension_id": "learning", "score": 5.0, "weight": 0.15, "evidence": ["..."], "gate_passed": true}
  ],
  "aggregate": {"S": 6.8, "PV": -1.2},
  "floor": 9.0,
  "verdict": "BELOW_FLOOR",
  "the_miss": "PRODUCTION_READINESS at 3.0 — nothing deployed",
  "corrective_action": "resolve #1102, one governed promotion (Shawn-gated)",
  "rescore_scheduled_at": "2026-10-16T...Z",
  "gate_failed": false,
  "reproducibility": {"inputs_hash": "...", "deterministic": true}
}
```

### 6.1 The Loop-law closure (mandatory)

Per the standing Loop doctrine, a scorecard cannot close without:

- **(a) The miss named** — `the_miss`: the weakest dimension, stated plainly with its score. Not "needs improvement" — the specific dimension and number.
- **(b) The corrective action recorded** — `corrective_action`: what would move the miss. Concrete, ownable, verifiable.
- **(c) The re-score scheduled** — `rescore_scheduled_at`: when the subject gets measured again. A score without a re-score date is an observation, not a loop.

A Calculator implementation MUST refuse to emit a closed assessment without all three. This is enforced in code, not documented in prose.

### 6.2 Verdicts

| Verdict | Condition |
|---|---|
| `ABOVE_FLOOR` | S ≥ floor AND no gate failed |
| `BELOW_FLOOR` | S < floor, no gate failed |
| `GATE_BLOCKED` | Any gate failed (score is informational only) |
| `INCOMPLETE` | Missing required evidence or inputs (fail closed) |

## 7. Law-as-code path

The Calculator becomes enforced in stages. Each stage is its own decision with its own scorecard and receipt.

| Stage | What | Enforcement |
|---|---|---|
| 1. Spec | This document. CANDIDATE until ratified. | None — prose. |
| 2. Reference implementation | `tools/naya_calculator.py` implementing this spec exactly. Spec-implementation conformance tests. | None — code exists, proves nothing yet. |
| 3. Report-only | Runs in CI + on demand. Scores published, never block. | Informational. Precedent: Naya 5's design calculator `--gate` shipped report-only first. |
| 4. Gate wiring | Scores become preconditions at named gates. | Mechanical: merges below floor don't merge; Smart App assemblies below 9 don't publish; Score stage of app-creation pipeline runs the Calculator by default. |

**Stage-gate rules:**

- A stage is entered only by explicit decision (scorecard + receipt).
- Report-only MUST precede gate wiring. No rubric gates production behavior before it has a calibration history.
- The Calculator never gates: production dispatch, production DB, credentials/money, destructive actions, constitutional ratification. Those stay human-only regardless of score.

## 8. Extension, not duplication

- The Calculator does not replace the Scorecard Law's five steps. It mechanizes step 2 (SCORE).
- The Calculator does not replace the V2.1 Value Calculus. It generalizes its math to outputs.
- The Calculator does not replace `auto_merge_gate.py`. The gate consumes Calculator assessments as evidence; the gate remains the merge authority.
- Domain calculators (design, future: code, voice, truth) are rubric plugins, registered in the rubric registry. One machine, many rubrics.

## 9. Open questions (for ratification)

1. PV computation: the exact formula mapping (S, floor, stakes) → PV∈[−9,9] needs Shawn's confirmation or a proposed formula for him to amend.
2. First gate-wiring target: merges, Smart App assembly, or both.
3. Rubric registry location: proposed `BRAIN/01-GOVERNANCE/rubrics/` — needs confirmation it doesn't collide with another seat's registry work.
