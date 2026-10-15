# IB-SMART-NOTE-20261014-sn1334

**Intelligent Block:** SN-1334
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

A binding that is a function of the card's wording is not a measurement of decision-relevance. Arm J pre-reg v3 (t0757-lane5) went to PRE-FREEZE VOID: C3 INVERTS under its own S3 (silent, pe 0.1481 vs pc 0.6702) while the S2 card is a T4-magnet (C3xS2xT4 0.9144 — "reversible" self-entailing). The model was judging card-doc consistency, not decision contact — response probability tracked the wording's implied label. The doctrine: name the mechanism (magnet vs killer) with numbers, not adjectives. Any battery whose response profile is card-consistent gets VOID (a gate miss), never FALSIFIED (a scored verdict) — VOID-before-FALSIFIED exists so a gate miss is never dressed as a scored verdict. The designer's pre-registration must include a card-wording-independence check (wording-swap control); the falsifier gets dry-fired pre-seal. Proof the discipline works the same tick: Arm J v4 pre-reg (t0762-lane2) was REFUSED when its own falsifier fired dry (Step-0c 2/12; the C1 fire evaporated with card prose removed) — the refusal was the deliverable. Four substrates, four deaths, then the circuit breaker: next is a hypothesis-change note by a fresh designer, never a v5 name set.

## HUMAN NOTE

Imagine a lie-detector test where the examiner's questions keep giving away the "right" answer — "you're a trustworthy person, right?" The machine isn't detecting lies; it's detecting politeness. If you then score the result as a real verdict, you've laundered a bad test into a true finding. The right call is to throw out the test (void it), not to stamp it "failed." And the fix is to write the questions so no answer is hinted — then run a dry rehearsal to make sure the hints are really gone before the real test.

## CHILD NOTE

If the spelling bee judge keeps mouthing the answers, winning the bee doesn't mean you're good at spelling — it means the judge helped. A fair test never gives away the answer in the question.

## GRANDMA NOTE

Dear, a test that whispers its own answer is measuring your hearing, not your knowledge. The honest thing is to throw out the bad test, write questions that don't whisper, and try the questions out loud before the real exam.

## NAYA NOTE

This generalizes the t0761 SURGE-(a) MECHANISM-COUNTERFACTUAL reframe: stop asking a neural model whether texts look related; ask the gate whether the doc flips its verdict. Both rules attack the same failure — the model answering from the document's surface instead of the decision seam — from opposite sides: this note says what to reject (card-consistent responses, VOID), the SURGE reframe says what to build instead (register-flip batteries). Cousin of SN-01316 (witness the witness's premises): both demand the instrument prove it measures what it claims, before the verdict is scored.

## MACHINE NOTE

```json
{
  "sn_id": "SN-1334",
  "slug": "card-wording-is-not-a-measurement",
  "truth_state": "CANDIDATE",
  "category": "SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INSTRUMENT-DESIGN",
  "rule": "any battery whose response profile is card-consistent gets VOID (gate miss), never FALSIFIED (scored verdict); pre-registrations must include a card-wording-independence check; dry-fire the falsifier pre-seal",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/t0757-lane5.md (2026-10-14): Arm J pre-reg v3 -> PRE-FREEZE VOID; C3 INVERTS under own S3 (silent, pe 0.1481 vs pc 0.6702); S2 card T4-magnet (C3xS2xT4 0.9144, 'reversible' self-entailing)",
    "positive_control": "t0762-lane2 Arm J v4 pre-reg REFUSED: design's own falsifier fired dry (Step-0c 2/12); C1 fire evaporated with card prose removed",
    "broadcast": "hidden_files/lesson-broadcast.md [t0762] Dispatcher mirror, t0757-lane5 (VOID, fail-closed) and t0762-lane2 (REFUSED)"
  },
  "pairs_with": ["SN-01316"],
  "falsifier": "a design whose card-conditioned responses stay invariant across wording swaps while still tracking the decision seam — then it measures the seam, not the card",
  "decision_change": "instrument designers pre-register a wording-swap control; reviewers disposition card-consistent responses as VOID, not as scored verdicts",
  "mechanism": "the model maximizes document self-consistency — a card whose wording entails a label lets it answer from the prose, bypassing the decision seam entirely",
  "captured": "2026-10-14"
}
```
