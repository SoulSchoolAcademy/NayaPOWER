# Learning Contract V1

**Status:** PROPOSED CANONICAL — HUMAN DIRECTOR RATIFICATION REQUIRED

## Purpose

Learning converts verified experience into future behavioral improvement. It ensures that the system compounds intelligence over time without conflating observation with understanding or stored notes with learned behavior.

## Scope

- Candidate learning identification and capture
- Learning verification and reconciliation
- Behavioral effect measurement
- Compounding of verified learnings
- Regression protection

Out of scope: authority changes, constitutional amendments, unverified behavioral modification.

## Key Rules

1. Learning occurs only when an observed and appropriately verified outcome changes future behavior.
2. The learning pipeline: `OBSERVE → RECONCILE → CANDIDATE → VERIFY → ADOPT → MEASURE → COMPOUND`.
3. A stored note is not learning. A candidate is not verified learning.
4. Learning must not silently change authority.
5. Contradicted learnings must be preserved as historical record.
6. Compounding requires measured future behavioral effect.

## Input/Output

| Direction | Content |
|---|---|
| Input | Verified outcomes, observations, existing intelligence, contradictions |
| Output | Learning candidates, verified learnings, behavioral effect measurements, compounding records |

## Acceptance Criteria

- Every learning claim traces to a verified outcome.
- Promoted learnings have explicit applicability conditions.
- Contradicted learnings are preserved and marked.
- Compounding claims include behavioral effect measurements.
- Learning does not override governance or authority.
- **Every row-count claim against an evidence table decomposes by kind
  (`jsonb_typeof` of the evidence column) BEFORE any delta is named** —
  §7 canon (Naya Alpha, 2026-10-16; from the w229/w268 disposition, where a
  kind-blind LIKE turned 22 composite-packet rows into "missing treatment
  rows"). Mechanically enforced, fail-closed, by
  `tools/kind_decompose_check.py` (exit 1 on a kind-blind delta).

## Failure States

| Failure | Behavior |
|---|---|
| Unverified outcome | Reject as learning; retain as candidate |
| Contradicts existing verified learning | Surface conflict; mark as CONTRADICTED |
| No measurable behavioral effect | Mark as UNVERIFIED; do not compound |
| Authority boundary violation | Reject; learning never changes authority |
| Regression detected | Halt compounding; trigger review |
