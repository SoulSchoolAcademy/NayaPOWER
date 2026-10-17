# Shawn's Diagrams → Executable Specs Mapping

All diagrams Shawn transmitted on 2026-10-10 are implemented as code,
not filed as images. This document records the mapping.

## 1. Naya_Protocol_1.svg → AER-LIVE-7 pumping witness
- **Diagram**: Entry (Prefix P) → Cycle C (Debt +k, repeat n times) → Exit (Suffix X).
  "P · Cⁿ · X is valid for every n ≥ 0. A finite certificate for
  arbitrarily large finite histories."
- **Code**: `aer_live7_pumping.py` on branch `naya5/aer-live-7-pumping`
  (PR #2206). Certificate requirements, finite-token mutation,
  minimal pumping-witness integrity.
- **Status**: Implemented, tested, PR open.

## 2. Naya_pro_process.svg → Dependency containment
- **Diagram**: Suspect claim A → Lesson B (depends entirely on A → blocked,
  needs revalidation) vs Lesson C (also has evidence X → independently
  tested, valid portion continues). "Contain dependence, not the entire graph."
- **Code**: `revocation.contain_dependence()` — walks the dependency graph
  from a suspect claim; nodes depending ENTIRELY on it → BLOCKED;
  nodes with other evidence → REQUALIFY. Transitive blocking.
- **Tests**: `test_revocation.py::test_contain_dependence_*` (3 tests).
- **Status**: Implemented, tested, on this branch.

## 3. Process_flow.svg → Self-reinforcing error guard
- **Diagram**: ORIGINAL ERROR → CAPTURE → RETRIEVAL → SELF-EVALUATION →
  FALSE PROMOTION → SUCCESSOR REUSE → feedback loop.
- **Code**: `compounding_pipeline.self_reinforcing_error_guard()` —
  blocks promotion when a claim has been repeated ≥2 times with no
  independent evidence. Checked first in `run_pipeline()`.
- **Tests**: `test_compounding_pipeline.py::test_self_reinforcing_error_guard_fires`,
  `test_pipeline_blocks_on_self_reinforcement`.
- **Status**: Implemented, tested, on this branch.

## 4. The_compounding_process.svg → 10-stage pipeline
- **Diagram**: EXPERIENCE → CAPTURE → UNDERSTAND → QUALIFY → RETRIEVE →
  APPLY → MEASURE → VERIFY → PROMOTE → COLD_REUSE.
- **Code**: `compounding_pipeline.py` — executable state machine with
  `PipelineState`, stage-ordered `advance()`, and blocking with reasons.
  MEASURE requires LESSON_IMPROVES; VERIFY requires independent evidence;
  PROMOTE issues a `ProofReceipt`; COLD_REUSE is the terminal stage.
- **Tests**: 13 tests in `test_compounding_pipeline.py`.
- **Status**: Implemented, tested, on this branch.

## 5. process_smart_flow.svg → Independent evidence families
- **Diagram**: Original claim A (unverified) → Naya 2 summary + Naya 5
  evaluation → "Claim A repeated — still one evidence family" vs
  "Independent observation B — separate measurement or authoritative source."
- **Code**: `compounding_pipeline.EvidenceFamily` (SAME_FAMILY vs
  INDEPENDENT_OBSERVATION) + `verify_independent()` — returns True only
  if INDEPENDENT_OBSERVATION is present. Enforces AGENTS.md anti-citogenesis.
- **Tests**: `test_same_family_repetition_not_independent`,
  `test_independent_observation_qualifies`,
  `test_pipeline_blocks_without_independent_evidence`.
- **Status**: Implemented, tested, on this branch.

## 6. Experiment outcomes chart → MEASURE ordering property
- **Diagram**: Control ~65%, Correct lesson ~88%, Wrong lesson ~60%.
  Caption: "Hypothetical results — not observed NayaNET measurements."
- **Code**: `compounding_pipeline.measure_lesson()` — asserts the ordering
  treatment > control > wrong with minimum separation (default 0.05).
  Returns LESSON_IMPROVES / LESSON_HARMS / LESSON_NEUTRAL / INCONCLUSIVE.
  Grounded in ratified SN-042 (Epistemic Calibration Law §3).
- **Tests**: `test_shawn_chart_ordering` uses the exact chart values
  (0.65 / 0.88 / 0.60).
- **Status**: Implemented, tested, on this branch.

## 7. System_intelligence_review.html → Top 5 actionable items
1. **Control/treatment/wrong-lesson experiment design** → `measure_lesson()`
   + `ExperimentArms`. IMPLEMENTED.
2. **Interaction proof receipt schema** → `ProofReceipt` dataclass
   (interaction_id, participants, invariant, preconditions, environment,
   positive/negative/independent, qualification). IMPLEMENTED.
3. **Three-phase decisive experiment** (A: components pass, B: interaction
   fails via revocation, C: repair + requalify, then cold successor
   reconstructs) → NOT YET IMPLEMENTED. Next work item.
4. **Positive/negative test pairs** ("a system that refuses all execution
   does not demonstrate correct integration") → partially covered by
   `ProofReceipt.positive_test`/`negative_test` fields; full harness pending.
5. **"A merge may inherit valid component evidence. It must not inherit
   proof of an interaction that was never established"** → governing
   principle recorded; enforcement in the interaction-qualification
   module (future work).
