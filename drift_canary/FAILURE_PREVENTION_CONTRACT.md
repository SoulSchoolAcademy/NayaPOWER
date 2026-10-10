# FAILURE-PREVENTION ACCEPTANCE CONTRACT

**Source:** The Mirror — 100 failures, 100 solutions, 10 families (2026-10-10).
**Status:** SPEC. Implemented as `drift_canary/failure_prevention.py`.
**Rule:** This contract is the framework future repairs plug into. It is not
the implementation of all 100 solutions.

---

## 1. PURPOSE

Turn failures into prevention systems through one closed loop, not 100
disconnected tools. Every material failure produces a structured record;
every record flows through diagnosis, prioritization, repair, verification,
internalization, and transfer proof. A failure that recurs unchanged is a
system defect, not bad luck.

## 2. FAILURE TAXONOMY (10 families)

| Family | Failures | What goes wrong |
|--------|----------|-----------------|
| F1 Understanding | 01–10 | Does not correctly understand the job |
| F2 Truth | 11–20 | Cannot distinguish true from plausible |
| F3 Reasoning | 21–30 | Has information, reaches poor conclusion |
| F4 Planning | 31–40 | Works hard, not on the most valuable thing |
| F5 Tool use | 41–50 | Knows what to do, executes incorrectly |
| F6 Verification | 51–60 | Produces something, cannot prove it works |
| F7 Memory | 61–70 | Solves problems, fails to benefit later |
| F8 Alignment | 71–80 | Crosses a boundary that should not be crossed |
| F9 Communication | 81–90 | Correct work, difficult to understand/use |
| F10 Improvement | 91–100 | Fails to convert experience into improvement |

Classification is keyword-anchored and deterministic (`classify_failure()`).
F8 signals take precedence: a safety/authority signal anywhere in the
description classifies as F8, per the Class A hard-boundary rule.

## 3. CANONICAL FAILURE RECORD

Every material failure gets one record with these fields:

| Field | Purpose |
|-------|---------|
| expected_behavior | What should have happened |
| actual_behavior | What happened, with evidence |
| failure_family | Primary family (F1–F10) |
| root_cause | Why (distinct from the visible symptom) |
| evidence_provenance | Task, tool result, code version that produced the finding |
| prevention_control | What stops or detects recurrence |
| acceptance_test | What must pass for the repair to be accepted |
| behavioral_test | Does the repair transfer to future tasks |
| canonical_owner | Existing file/mechanism/contract that owns the fix |
| state | OBSERVED → DIAGNOSED → REPAIR_CANDIDATE → VERIFIED → BEHAVIORALLY_PROVEN / UNRESOLVED |
| recurrence | Prior occurrences and conditions |
| supersedes | Prior record this one replaces (provenance chain) |
| contributing_families | Secondary families beyond the primary |

Records are immutable; updates supersede. No separate brain: records feed
the existing Smart Note pipeline.

## 4. THE 8-STEP LOOP (executable)

Each step has entry requirements — the contract at every transition.
`step_ready()` enforces them; `next_step()` returns the next actionable step.

1. **OBSERVE** — requires: expected_behavior, actual_behavior, evidence_provenance
2. **DIAGNOSE** — requires: failure_family, root_cause
3. **PRIORITIZE** — reads the diagnosis (no new fields)
4. **REPAIR** — requires: prevention_control, canonical_owner
5. **VERIFY** — requires: acceptance_test
6. **INTERNALIZE** — preservation via Smart Note pipeline
7. **PROVE_TRANSFER** — requires: behavioral_test
8. **FREEZE_MEASURE_REPEAT** — requires: recurrence; version, measure, loop

A step cannot begin until its requirements are met. Skipping steps is a
contract violation, not an optimization.

## 5. PRIORITIZATION (Classes A/B/C/D)

| Class | When | Rule |
|-------|------|------|
| A Hard-boundary | F8 (safety, privacy, authority, consent, fabricated proof) | Always first. No score overrides a hard gate. |
| B Recurrent | Known failure happening again | Repair the shared cause, not each occurrence. |
| C High-leverage | One control prevents multiple families | Prefer single controls with wide coverage. |
| D Uncertain | Cause not established | Investigate cheaply first; do not manufacture a repair. |

`prioritize()` applies this precedence. Uses the existing
`kernel/value_calculus.py` for scoring within a class — never a competing
engine.

## 6. ACCEPTANCE CONTRACT

A repair is accepted **only** when all five elements are present:

- `prevention_control` — the mechanism, not an explanation
- `acceptance_test` — the bar the repair must clear
- `behavioral_test` — proof of transfer, not memorization
- `canonical_owner` — bound to an existing system
- `evidence_provenance` — the finding is traceable

`acceptance_contract()` returns accepted/missing/reason. An explanation is
not a repair. One passing test is not a permanent law. A lesson without
behavioral evidence is not learned.

## 7. BINDING TO EXISTING SYSTEMS

The contract reuses; it never duplicates:

| Responsibility | Canonical system |
|----------------|------------------|
| Authority/safety gates | Constitution (Team Naya Operating Protocol) |
| Prioritization math | `kernel/value_calculus.py` V2.1 |
| Duplicate prevention | `tools/duplicate_detector.py` + `solved_problem_registry.json` |
| Behavioral proof | `tools/learning_evidence_ladder.py` |
| Lesson preservation | Smart Note pipeline (`.naya/capture/`) |

`binding_for()` resolves a responsibility to its system. Build new only when
no binding exists — and still name a `canonical_owner`.

## 8. WHAT THIS DOES NOT COVER

- The 100 individual solutions (families define them; repairs implement them).
- Production wiring (spec seam only).
- Threshold calibration for the six reliability measures (needs baselines).
- The duplicate_detector/learning_evidence_ladder internals (referenced, not reimplemented).

## 9. DEFINITION OF DONE (for this contract)

- [x] Taxonomy encoded and classifiable
- [x] Record fields defined and immutable
- [x] 8-step loop executable with entry requirements
- [x] Prioritization classes with hard-boundary precedence
- [x] Acceptance contract validates repairs
- [x] Bindings reference existing systems without duplication
- [x] Tests prove each function
