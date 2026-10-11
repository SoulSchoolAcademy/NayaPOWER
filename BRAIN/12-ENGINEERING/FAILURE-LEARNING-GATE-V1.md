# Failure Learning Gate V1 — implementation contract

**Status:** implementation proposal on a review branch; not ratified as new constitutional law and not yet merged or independently verified.

## Objective

Every failure should increase collective capability. Team members surface issues, cooperate on root cause and repair, preserve a provenance-bound lesson, and install a guard against recurrence. Do not treat discussion, storage, or green status alone as proof of learning.

## Enforceable receipt

For every cycle with `failure_detected=true`, the machine gate requires non-empty:

- `expected_vs_actual`: what should have happened versus what happened;
- `root_cause_or_unknown`: a measured root cause or an explicit UNKNOWN;
- `team_share_ref`: durable link/receipt showing the issue was surfaced to the relevant team;
- `repair_or_blocker`: the mechanism repair or exact blocker/unblock condition;
- `regression_guard`: a test/guard reference, or a concrete statement recorded in that field explaining why a guard cannot yet exist;
- `canonical_lesson_ref`: link to the durable canonical lesson record.

If a reusable lesson is supplied, a `smart_note_id` is also required. A no-lesson disposition must state a reason. Missing fields fail closed; malformed (non-string) fields fail closed with a reason — the validator never raises on a malformed receipt.

## Required team workflow

1. Surface the failure in the owning lane; share material cross-lane risks in coordination.
2. Preserve exact revision, run, logs, expected/actual behavior and uncertainty. Never post secrets or protected fixture keys.
3. Ask for specific peer help; do not claim dispatch or acknowledgement without a receipt.
4. Reproduce safely and identify the failed layer: contract, code, test, environment, runtime, authority or evidence.
5. Repair the mechanism, add adversarial/regression coverage, and obtain independent verification.
6. Record the lesson with provenance and canonical references.
7. Verify successor retrieval and appropriate application on a later task before claiming ACTIVE/EFFECTIVE/COMPOUNDING learning.

## Authority and truthful status

This gate records and validates a receipt shape; it does not itself publish team messages, write a Smart Note, prove links resolve, enforce GitHub workflow completion, or prove future behavior changed. Those require integrations and independent behavioral tests. It creates no authority to merge, deploy, write production data, change protected law, or bypass a freeze. Existing branch protection, review, scorecard and human gates remain in force.

## Acceptance tests

- complete failure receipt passes;
- missing team-share receipt fails;
- missing root-cause classification fails;
- missing repair/blocker disposition fails;
- missing regression guard fails;
- missing canonical lesson fails;
- reusable lesson without Smart Note identity fails;
- ordinary non-failure cycle retains existing behavior;
- no-lesson failure cannot silently pass;
- independent reviewer reruns focused tests and verifies exact PR head;
- a later cold successor retrieves the lesson and demonstrates appropriate reuse before any claim of compounding learning.

## Measures

Track, per failure class: time-to-surface, time-to-root-cause, time-to-repair, independent-verification result, recurrence rate, successful successor retrieval/application, and prevented repeated work. Do not claim improvement without a defined baseline and measured comparison.
