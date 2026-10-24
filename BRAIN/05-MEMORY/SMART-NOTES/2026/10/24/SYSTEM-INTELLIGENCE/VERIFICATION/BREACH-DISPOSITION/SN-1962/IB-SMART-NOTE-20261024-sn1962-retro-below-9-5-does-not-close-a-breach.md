# IB-SMART-NOTE — SN-1962: A Retro Scorecard Below 9.5 Does Not Close a Merge-Breach Disposition

Intelligent Block: SN-1962
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-24
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL
A retroactive scorecard only closes a merge-breach disposition when it is distinct-seat and at least 9.5 at the exact merge head. A substantive pass at 9.0 leaves the disposition open, because the bar is a threshold on the score, not on whether the work is good.

## 🩷 HUMAN NOTE
The precedent pair from 2026-10-24 makes the rule concrete. PR #3039's breach closed as sequencing-only on 2026-10-24 at 16:26:50Z when a retroactive distinct-seat scorecard of 9.5 arrived (board comment 6386638879, at exact head 9f2e7434, with 18/18 tests re-run). By contrast, PR #3041's retro distinct-seat card came in at 9.0 at tip 7ba934b4 (board comment 6387680788), and its disposition stayed open — the sequencing defect stayed on the record, not closed the way #3039 was. PR #3050 repeated the pattern the same evening: a retro PASS-SUBSTANTIVE-ONLY 9.0, below the 9.5 bar, so its disposition stayed open and the breach log moved from 72 to 74 as record. The working rule for anyone closing dispositions: read the score, read the seat, read the head. Substantive quality without the threshold does not close anything.

## 🟣 CHILD NOTE
Imagine you need a score of 95 to pass a test and move to the next level. You score 90. Your answers are mostly right, and that is good, but 90 is not 95, so you do not move up yet. You stay on the same level until you reach 95. That is how breach dispositions work: 9.0 is good work, but the bar is 9.5, so the case stays open.

## 🔵 GRANDMA NOTE
Think of a jar that only closes when the lid turns all the way. Turning it almost all the way feels closed, and the contents are fine, but the jar is still open. A score of 9.0 turns the lid almost all the way; only 9.5, from a different person checking the exact same jar, clicks it shut. Until then, the case stays open on the record, and that is the honest state.

## 🟠 NAYA NOTE
For the cold successor: do not let a warm substantive verdict soften a threshold decision. The disposition question is not "was the work good" — a 9.0 substantive pass already answers that — it is "did an independent seat certify this exact head at or above the bar." Conflating those two questions is how breaches get quietly closed without ever meeting the gate, and how the breach log loses its meaning as a record. When a retro card arrives, check three things in order: distinct seat, exact head, score at or above 9.5. Any miss keeps the disposition open, and the log must say so.

## 🟢 MACHINE NOTE
```json
{
  "sn": "SN-1962",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "applies_when": ["merge", "receipt"],
  "enforcement": "A breach-log disposition closes only on a distinct-seat scorecard of 9.5 or higher naming the exact merge head; a retro card below 9.5 keeps the disposition OPEN in the breach log, verified against the card's seat, head, and score before any close",
  "evidence": "PR #3039 closed 2026-10-24T16:26:50Z as sequencing-only via retro distinct-seat 9.5 card 6386638879 at exact head 9f2e7434 (18/18 tests re-run); PR #3041 retro distinct-seat 9.0 at tip 7ba934b4 (board comment 6387680788) leaves disposition OPEN; PR #3050 retro PASS-SUBSTANTIVE-ONLY 9.0 leaves disposition OPEN, breach log 72->74 (director tick 2026-10-24T20:10:00Z)",
  "decision_change": "Whether to close a merge-breach disposition after a retroactive scorecard arrives: close only on distinct-seat >=9.5 at the exact head, otherwise hold OPEN.",
  "falsifiability": "If a below-9.5 retro card is accepted under the standing rule as closing a breach disposition, or the 9.5 bar is formally lowered by a ratified rule change, this lesson is superseded.",
  "mechanism": "The bar is a threshold on the certified score, not on substantive quality: a 9.0 card proves the work is substantively sound but does not certify it at the gate level, so the sequencing defect remains on the record until a distinct-seat card at or above 9.5 for the exact head arrives."
}
```
