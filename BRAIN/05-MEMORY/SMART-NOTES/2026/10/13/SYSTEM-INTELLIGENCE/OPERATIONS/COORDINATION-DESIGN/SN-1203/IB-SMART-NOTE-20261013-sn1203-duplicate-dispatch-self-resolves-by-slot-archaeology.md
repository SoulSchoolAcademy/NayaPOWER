# Duplicate Dispatch Self-Resolves by Slot-Archaeology Against the Live Venue

**Intelligent Block:** IB-SMART-NOTE-20261013-sn1203-duplicate-dispatch-self-resolves-by-slot-archaeology
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-13
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #2175 board comment 6149794640 — 🧠 LEARNING EVENT 2026-10-13 ~15:58Z distillation (win pattern WP-49, class F4); two duplicate 15:49Z dispatches (build + verify lanes), each finding live sibling receipts and standing down completely.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## IN A NUTSHELL

Two duplicate dispatches fired at 15:49Z (build and verify lanes) and both self-resolved without churn: each run did slot-archaeology against the live venue, found the sibling's live receipts covering its state, and stood down completely — no claim, no post, no work duplicated. The system un-claims work, not just claims it.

**The durable rule: identify the sibling by venue receipt ID, never by its self-reported slot label.** In this window the sibling's header had mislabeled its own slot; the venue record was the truth. Labels lie (stale copy, recycled text); the venue's receipt ID doesn't. When a dispatch suspects duplication: (1) read the live venue for the state it was about to cover, (2) match by receipt ID, (3) if covered, stand down silently and post nothing. Churn on a duplicate is pure waste — the highest-value action is the one you don't take.

## HUMAN NOTE

Duplicate work is inevitable in a parallel system; duplicate *cost* is optional. The two 15:49Z runs show the mature posture: the check happens before the first expensive action, and a clean stand-down posts nothing (silence is the receipt). The critical detail is which identifier you trust: the sibling's self-reported slot label was wrong; only the venue receipt ID was authoritative. This is the general discipline — when reconciling with another lane, read the venue, not the lane's own header. Headers are courtesy; venue records are fact. A lane that correctly does nothing must be scored as a success, not a no-op: WP-49 kept two workers from burning quota on already-covered state.

## CHILD NOTE

Imagine two kids are both sent to buy milk. The smart move isn't for both to go to the store — it's for the second kid to check the kitchen first. If there's already milk in the fridge (the venue), the job is done; going to the store anyway would just waste time. And when checking the fridge, look at the actual milk — not at a note on the door that might say the wrong thing.

## GRANDMA NOTE

When two people get the same errand, the wise one checks whether it's already done before starting — and checks the actual result, not somebody's possibly-mistaken note about it. Quietly not doing a job that's done is doing the job well.

## NAYA NOTE

Intelligence includes knowing when not to act. When I arrive at a task and find the venue already holds a receipt for it, the intelligent move is a silent stand-down — no claim, no duplicate artifact, no noise. And I must never trust a lane's self-reported label over the venue's own record: a stale header once mislabeled a slot, and only the receipt ID told the truth. Standing down on a duplicate is not wasted work; it is the highest-value decision available in that moment.

## MACHINE NOTE

```json
{
  "sn": "SN-1203",
  "lesson": "duplicate-dispatch-self-resolves-slot-archaeology",
  "win_pattern": "WP-49",
  "class": "F4",
  "rule": "identify sibling by venue receipt ID, never by self-reported slot label; if venue covers the state, stand down silently",
  "applies_to": ["dispatch", "coordination", "duplicate-suppression"],
  "evidence": {
    "board_comment": 6149794640,
    "events": "two 15:49Z duplicate dispatches (build + verify), both stood down on live sibling receipts"
  },
  "truth_state": "CANDIDATE",
  "supersedes": null
}
```
