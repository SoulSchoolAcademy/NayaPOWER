"""Reopening protocol — SPEC, not production code.

Principle (Shawn, 2026-10-10): "A resolution is the best supported
interpretation at a particular time — not an eternal declaration of truth."

This package specifies the TEMPORAL review lifecycle for interpretations:
what happens when a resolved interpretation needs re-examination. It extends
the error-defense spec (qualify_lesson, L0-L4 eligibility, claim-level
separation) and does not duplicate it.

Four objects, kept separate by design:
    SourceRecord            — what was said. Immutable.
    InterpretationSet       — plausible meanings + evidence. Versioned.
    ResolutionReceipt       — why this interpretation won, at this time,
                              under this policy. Immutable.
    ApplicabilityAssessment — can it guide THIS decision now? Reassessed.

Five review states (layered on truth states, not competing):
    RESOLVED -> CHALLENGED -> REOPENED -> REQUALIFIED | UNRESOLVED

Modules:
    objects.py      the four objects
    review.py       the five-state machine + risk-based three decisions
    triggers.py     the ten trigger registry
    policy.py       policy versioning (P1 receipt stays valid; P2 governs now)
    challenges.py   idempotent challenge handling
    descendants.py  descendant impact tracing for interpretation changes
"""
