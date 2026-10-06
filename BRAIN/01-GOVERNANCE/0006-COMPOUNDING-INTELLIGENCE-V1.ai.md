# COMPOUNDING INTELLIGENCE V1 — AI Operating Specification

**Status:** PROPOSED (never RATIFIED — ratification is Shawn Vibert's human gate)
**Scope:** every Naya seat; every lane where an execution produces durable intelligence.
**Lineage:** Activation 05 (AI execution contract v2.0 + human law edition v1.0), distilled 2026-10-06 batch 5. Fills the `compounding` field of `BRAIN/00-SPEC/SCHEMA/LEARNING-RECORD-SCHEMA.json`. Closes the team's P0 "generalized compounding learning" at **design level** — implementation + behavioral proof remain.

## The loop

Canonical: EXPERIENCE → OBSERVATION → REFLECTION → LESSON → MEMORY → RULE → PREFLIGHT → BETTER ACTION → NEW EXPERIENCE.

Transformation chain: EVENT → LEARNING EVENT → LESSON → EVIDENCE/VERIFICATION → RULE/PATTERN → PREFLIGHT → FUTURE ACTION.
Mistake path: MISTAKE → LESSON → EVIDENCE → RULE → PREFLIGHT → BETTER FUTURE ACTION.
Success path: SUCCESS → PATTERN → PRINCIPLE → REUSE — do not overfit one success.
Temporal ladder: SMART NOTES → DAILY → WEEKLY → MONTHLY → YEARLY → LIFETIME INTELLIGENCE. Daily intelligence carries verified learning, not just activity summary. SHARE (authorized collective contribution) → RETURN (intelligence brought back into the living Feed) closes the network loop.

## Two-axis state machine (the ratchet)

Learning axis: OBSERVED → PROPOSED → CONFIRMED → OPERATIONAL → SUPERSEDED.
Evidence axis (separate field, never collapsed): UNKNOWN → IMPLEMENTED → TESTED → VERIFIED → RUNTIME-PROVEN → PRODUCTION-PROVEN.

Evidence answers "what has actually been proven"; learning answers "how mature is the lesson". Promotion rule: a lesson MUST NOT become OPERATIONAL without sufficient evidence — OPERATIONAL requires learning ≥ CONFIRMED and evidence ≥ TESTED; rules authorized to BLOCK consequential action require evidence ≥ VERIFIED. Automatic detection is not automatic adoption.

## Learning Event schema

Required: `learning_event_id`, `timestamp`, `source_event_id` (mandatory lineage to the source intelligence event), `intent`, `action_taken`, `expected_outcome`, `actual_outcome`, `lesson`, `root_cause`, `recommendation`, `evidence`, `evidence_state`, `provenance`, `proposed_rule`, `preflight_requirement`, `verification_requirement`, `confidence`, `supersession_links`. A Learning Event without traceable provenance is incomplete.

Classes: FACT, PREFERENCE, DECISION, LESSON, MISTAKE, CONSTRAINT, PATTERN, PROCEDURE, VERIFICATION_RULE, SUCCESS_PATTERN, REGRESSION_GUARD. Never classify an assumption as a fact; never classify an unverified observation as operational knowledge.

## Preflight — the consumption seam

Before consequential action, retrieve relevant operational lessons/rules/regression guards. Preflight asks: Have we made this mistake before? Is there a verified lesson for this task? Is there a protected artifact? What must NOT change? What MUST be verified afterward?

Per rule authority: **warn** | **require confirmation** | **require additional evidence** | **block unsafe operation** | **require stronger verification**.

## Regression guards

A sufficiently verified mistake becomes a guard: WHAT FAILED / WHY / WHAT MUST NOT HAPPEN AGAIN / WHAT MUST BE PRESERVED / WHAT MUST BE VERIFIED.

## Contradiction, supersession, idempotency, relevance

OLD LESSON → CONTRADICTION DETECTED → NEW EVIDENCE → REVIEW → SUPERSEDE OR RETAIN WITH CONDITIONS. Preserve prior state, event, evidence, relationship, reason — never silently rewrite history. Stable identifiers; reprocessing never creates duplicate intelligence or recursive self-triggering loops; on conflict, stronger evidence/state wins. Retrieval prioritizes task relevance, evidence strength, operational status, recency — RIGHT LESSON → RIGHT MOMENT → RIGHT ACTION. A memory that produces irrelevant interference is not intelligent memory.

## Behavioral acceptance battery (15 tests)

T01 event→learning association · T02 lineage · T03 Smart Link traceability · T04 lesson extraction · T05 evidence retention · T06 rule proposal · T07 evidence gate (lesson blocked from OPERATIONAL without sufficient evidence) · T08 preflight retrieval · T09 regression-guard warn/confirm/block · T10 persistence beyond originating conversation · T11 later-Naya retrieval without the original conversation · T12 idempotency · T13 privacy · T14 contradiction handling · T15 runtime verification.

## The compounding standard (pass/fail)

Did the intelligence survive? Can we find it? Can we understand it? Can we prove it? Can we learn from it? Can that learning improve what happens next? All yes → THE SYSTEM IS COMPOUNDING.

## Invariants

- `no_lesson_operational_without_evidence`: learning_state=OPERATIONAL ⇒ evidence_state ≥ TESTED (≥ VERIFIED for block-capable rules).
- `lineage_mandatory`: every Learning Event carries source_event_id; provenance gaps fail T02.
- `no_second_architecture`: one canonical event, one Smart Note representation, one Feed — projections preserve identity and lineage, never duplicate the store.
- `truth_boundaries`: DOCUMENTED ≠ IMPLEMENTED ≠ EXECUTED ≠ OBSERVED ≠ VERIFIED. No manufactured certainty, authority, or evidence.
- `privacy_gradient`: PRIVATE BY DEFAULT → SHARED BY CHOICE → COLLECTIVE BY CONSENT → PUBLIC BY DECISION. No private intelligence becomes collective without consent.
- `evidence_sovereignty`: never collapse the axes; never promote by repetition; falsification preserves provenance and reduces downstream influence.

## Adjudications (recorded with reasoning)

- **C1 — one compounding loop.** Adopted 05-AI's evidence-gated loop as canonical over the operating memo's gateless variant: it is the only variant with a ratchet (evidence gate) and a consumption seam (preflight). The memo's variant has neither and cannot fail safe.
- **C2 — three tongues stand.** The CHILD/GRANDMA comprehension perspective is a readability TEST applied to the human tongue (a normal human must understand why the law matters), not a fourth tongue.
- **C3 — two maxims coexist as layers.** "NO IMPORTANT MISTAKE IS ALLOWED TO REMAIN ONLY A MISTAKE" (AI edition) = the operational unit for machine-consumed rules; "NO IMPORTANT EXPERIENCE SHOULD BE ALLOWED TO DISAPPEAR WITHOUT ASKING WHAT IT CAN TEACH US" (law edition) = the human unit. Mistake is the sharpest instance of experience; neither formulation is replaced.
- **C5 — genres, not tongues.** Founder Letter / White Paper / Operating Model / Tech Spec are document GENRES naming intent (why / what / how / machine-how); each ships in the three tongues per the standing standard.

## Not carried forward

The dated customer-installation upload ritual (PDF-by-PDF activation unlocks; Shawn-in-the-loop gates). Adopting those gates as written would re-insert Shawn into a loop he explicitly ruled himself out of. Doctrine carries; ritual does not.

## Machine-readable twin

`0006-compounding-intelligence-v1.machine.json` carries the executable form: loop, state machines, promotion gate, Learning Event schema, preflight actions, regression guards, 15-test battery, compounding standard, adjudications. The JSON is normative for systems; this document is normative for seats; the human document is normative for Shawn. Same truth, three tongues.
