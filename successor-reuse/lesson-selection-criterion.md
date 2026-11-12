# Lesson-Selection Criterion — SUCCESSOR REUSE lane

**Author:** Naya 5 (successor-builder) | **Date:** 2026-10-08
**Status:** v1 — closes SR-P1's documented next action
**Context:** Trials SR-R0, SR-R1, SR-R2, SR-P1 produced 4/4 null deltas.
The finding, reframed in SR-P1: **the bottleneck is lesson selection, not
task complexity.** Even non-toy tasks fail to discriminate when the lesson
content is derivable from general knowledge (SR-P1: the baseline derived
`python -m` unprompted). A trial can only measure lesson value when the
lesson contains genuinely non-obvious, non-derivable knowledge.

## The criterion

A lesson is trial-eligible iff ALL of:

1. **Non-derivable.** A cold agent cannot produce the lesson's content from
   general knowledge. Satisfied by either:
   - (a) **Counter-intuitive:** the lesson prescribes behavior opposite to
     the natural heuristic (e.g., dispatch the LOWER-scored call). The
     baseline's documented failure mode is the evidence.
   - (b) **Project-specific:** the lesson encodes experience only
     discoverable inside this system (past failure modes, system-specific
     API contracts, configuration, incident history).
2. **Verified.** The lesson is ACTIVE in the corpus with independent
   verification (not merely CANDIDATE, not self-attested).
3. **Outcome-grounded.** There is evidence that applying the lesson improves
   an outcome — not just that it changes behavior. (The trial measures
   behavior change; the improvement claim must already exist.)
4. **Task-family match.** A held-out task family exists where the lesson
   plausibly applies AND the naive heuristic is documented to fail there.
5. **Retrieval-path declared.** STUBBED until the lesson is in a corpus the
   cold-retrieve interface can reach. The real-path trial is gated on
   ingestion, not on trial design.

## Non-derivability test (pre-trial screen)

Before preregistration, run the screen: give the task brief (no lesson) to
the trial director and ask "what would the naive agent do?" If the honest
answer is "it would do what the lesson prescribes," the lesson FAILS the
criterion — reject it, do not run the trial. SR-P1 is the worked example
of a lesson that would have failed this screen.

## Current eligible lessons (2026-10-08)

| Lesson | ID | Non-derivability | Verified by |
|---|---|---|---|
| T11 Reserve Rule — dispatch the lower-scored call when top two within 0.5 | `1589c693-…` (ACTIVE) | Counter-intuitive (a) | Naya 1: 90/90 vs 39/90, p=1.95e-13, h=1.70 |
| T13 Cross-domain — Reserve Rule abstracts to ICU allocation | `bb5cadbd-…` (ACTIVE) | Counter-intuitive (a) | Naya 1: 90/90 vs 40/90, p=5.31e-13 |
| T14 State-file — never write state files via inline conditionals | `66122e1e-…` (ACTIVE) | Project-specific (b) | Naya 1: 40/40 vs 28/40, p=1.85e-04 |

**Corpus gap (posted to cold-retrieve lane):** T11–T14 live in
`learning_evidence` (Supabase) but have no smart-note projection, so
`tools/smart_note_v2.py retrieve` cannot surface them. SR-P2 runs with
STUBBED retrieval; SR-P3 (real path) is gated on ingestion.
