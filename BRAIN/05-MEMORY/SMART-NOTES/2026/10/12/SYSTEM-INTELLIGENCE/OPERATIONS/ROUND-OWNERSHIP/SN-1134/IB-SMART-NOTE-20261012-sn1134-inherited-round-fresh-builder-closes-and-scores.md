# A Cancelled Builder's Round Is Inherited, Not Lost — the Fresh Builder Closes It and Owns the Scorecard

**Intelligent Block:** IB-SMART-NOTE-20261012-sn1134-inherited-round-fresh-builder-closes-and-scores
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Filed by:** smart-note-distillation loop (17:38 PDT tick, inline review).
**Provenance:** #2175 board, 6134966036 (2026-10-12 17:02 PDT): [Naya Mechanic] wave-11 B-48 CONTINUATION round-3 sign-out. The prior builder was cancelled mid-round-3; the fresh builder inherited PR #2494 (`naya2/b48-receipt-gate-edited-trigger` @ `947c55b3ea23`, base == live tip `dbe06f9e73`), byte-verified the inherited diff against the B-48 spec, repaired the stale dogfood receipt and the scorer's doc-precision items, ran a third live `edited`-trigger confirmation (run 38324679767), and closed the round. Distinct-seat scorer: 9.6/10 SHIP. PR marked ready-for-review; never self-merged. Cousins: SN-1091 (duplicate dispatch — distinct: that governs a second claim on a closed slot; this governs a fresh seat inheriting an *open* round left by a cancelled builder).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

When a builder is cancelled mid-round, the round's budget is not lost and the work is not orphaned. The fresh builder inherits the open state — PR, branch, pin SHAs, prior builder's partial evidence — verifies every inherited byte as if it were their own build, completes the remaining work, and closes the round with a full scorecard in their own name. The closure belongs to the inheritor, not to a ghost. The inherited state is an assertion to be byte-verified, never trusted on arrival: the fresh builder re-verified the diff line-by-line against the spec, fixed the stale receipt, and ran a fresh live confirmation before claiming the ship.

## HUMAN NOTE

Shawn, this is the team proving it can hand off mid-flight without dropping the ball. The circuit breaker's third round was in progress when the builder was cancelled — and instead of the work evaporating, a fresh seat picked up the exact same PR and state, treated every inherited byte with suspicion, verified it against the spec, finished what was left, and shipped with a real 9.6/10 from an independent scorer. The standing lesson: cancellation ends the builder's turn, not the round. Ownership transfers with the open state, the inheritor closes it, and the scorecard is earned on verified bytes — never inherited on faith.

## CHILD NOTE

Imagine you're building a LEGO castle with a friend and your friend has to go home. You don't knock the castle down — you look at every piece they placed to make sure it's right, then you finish the tower and get the credit for the whole castle. That's what happened here: the new builder checked every piece the old builder left, fixed two pieces that were wrong, added the last tower, and the finished castle got a 9.6/10. A cancelled builder means a new builder takes over — not that the castle disappears.

## GRANDMA NOTE

When a relay runner drops the baton, the next runner doesn't stand there waiting — they pick it up and finish the race. Here the baton was a half-finished round of work. The fresh builder picked it up, checked the track ahead for cracks (verified every byte against the spec), ran the last stretch, and earned a strong finish. The wise habit for any team: when someone has to stop mid-task, the task goes to the next person with everything they left behind — and the new person checks it all before calling it done.

## NAYA NOTE

For my own work: if I ever inherit an open round from a cancelled builder, I will treat the inherited state as unproven. I re-verify the diff against the spec at the live head, repair stale pins and receipts, and run at least one fresh live confirmation of the mechanism before I sign out. I score the inherited bytes as my own build — the 0.4 deductions and all. I close the round in my own name and I do not merge: merge sequencing stays with the merge lane. The round's budget survives the cancellation; only the builder changes.

## MACHINE NOTE

```json
{
  "note_id": "SN-1134",
  "type": "doctrine",
  "rule": "Cancellation ends the builder's turn, not the round. A fresh builder inherits the open state (PR, branch, pins, prior evidence), byte-verifies every inherited artifact against the spec at the live head, completes the remaining work, and closes the round with a full independent scorecard in their own name; the inherited state is an assertion, never trusted on arrival; merges remain with the merge lane.",
  "trigger": "a builder is cancelled mid-round (any round of a budgeted attempt)",
  "check": "does the inheriting builder's sign-out show: inherited diff byte-verified at live head + stale pins/receipts repaired + at least one fresh live confirmation of the mechanism + distinct-seat scorecard, and PR marked ready-for-review without self-merge?",
  "evidence": "#2175 6134966036 (2026-10-12 17:02 PDT): B-48 wave-11 CONTINUATION round-3 — prior builder cancelled mid-round; fresh builder inherited PR #2494 @ 947c55b3ea23, verified types diff + observability step vs B-48 spec, fixed stale dogfood receipt + scorer's doc items, third live edited-trigger run 38324679767; distinct-seat scorer 9.6/10 SHIP; ready-for-review, never self-merged"
}
```
