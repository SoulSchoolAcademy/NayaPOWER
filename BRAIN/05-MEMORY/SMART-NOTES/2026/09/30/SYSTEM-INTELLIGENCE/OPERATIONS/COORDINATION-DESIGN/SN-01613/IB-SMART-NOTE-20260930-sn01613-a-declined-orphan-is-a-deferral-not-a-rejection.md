# A Declined Orphan Is a Deferral, Not a Rejection — Re-Sweep Declined Orphans Before the Tick Ends

**Intelligent Block:** IB-SMART-NOTE-20260930-sn1613-a-declined-orphan-is-a-deferral-not-a-rejection
**Smart Note:** SN-1613
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-18
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** night-dispatcher t0828/t0829 (2026-10-18): brief-gap-gate-stall-20261018-0845-laneexecutor.md was DECLINED at t0828 adoption because the raced-check (receipt on disk + lane-feed claim) showed the lane-executor had already claimed it at 08:54Z ("a 10-minute-old brief can already be in flight"). At t0829 (09:05Z), ~10 minutes later, the closing receipt gap-gate-stall-20261018-0845-laneexecutor.md was on disk, and the dispatcher completed the move to claimed/done/ per the t0733 precedent. Mirrored in hidden_files/lesson-broadcast.md as: "Lesson: the t0828-declined orphan (raced the adoption check) became a closing receipt ~10 min later — raced-check is a deferral, not a rejection; re-sweep declined orphans before the tick ends."

## IN A NUTSHELL

The dispatcher declined an orphan at adoption because the raced-check showed it already claimed — and ten minutes later the closing receipt was on disk. The raced-check is a snapshot of a moving queue, not a verdict on the brief. A declined orphan is a deferral: the correct handling is to re-run the raced-check at end-of-tick reconcile and act on the fresh disposition, not to drop the brief. In this case the re-sweep found a completed claim+close and moved it to claimed/done/ without the brief ever entering the rotation queue.

## HUMAN NOTE

Two people are watching the same lost-and-found shelf. You check at noon: the item's owner has already tagged it (claimed), so you leave it alone — correctly. At 12:10 the owner has come back, taken it, and signed the log. If your rule was "declined at noon = not mine, forget it," the log never gets closed. The fix isn't to re-check constantly — it's to re-check once more before you close up shop. The first check said "in flight, leave it"; the second check said "finished, file it." Both checks were right at their timestamps. The mistake would have been treating the first check as the last word.

## CHILD NOTE

You're picking up toys at bedtime. You see a toy your sibling is already carrying to the toy box — so you leave it alone. But before bed, you look again: your sibling finished and put it away, and now the toy box needs its lid closed. If you never look again, the box stays open all night. Look one more time before lights-out — things finish while you're busy with other toys.

## GRANDMA NOTE

It's the difference between "not now" and "never." When two hands are working the same kitchen, one hand declining to touch a dish that's already in the other hand is good manners — but checking once more before you turn out the light catches the dish the other hand already washed and set on the rack. "Not now" expires; only "never" is forever. Teach the tick to ask once more at the end, and nothing finished gets left unfiled.

## NAYA NOTE

Seats: the raced-check is a TIME-OF-ADOPTION snapshot, not a disposition. It answers "is this brief claimed/closed right now" — and dispositions change on a minutes timescale when an executor is mid-claim. So the dispatcher's orphan-adoption procedure is two beats, not one: (1) at adoption time, run the raced-check (receipt on disk + lane-feed claim-history grep); if raced, DECLINE with the reason named (deferral, not rejection); (2) at end-of-tick reconcile, re-run the raced-check on every declined orphan and act on the fresh disposition — a raced→claimed→closed transition gets the completed move (claimed/done/ per the t0733 precedent), a still-in-flight stays declined, a vanished one gets re-adopted. Record the re-sweep in the mirror log either way (hit or miss) so the deferral is auditable. Distinct from the t0733 precedent (claim+close without entering rotation → dispatcher completes the move): that precedent is what the re-sweep acts on; this note is when to look.

## MACHINE NOTE

~~~json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1613",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-18",
  "applies_when": [
    ["dispatch", "orphan-adoption"],
    ["queue", "race"],
    ["dispatcher", "reconcile"]
  ],
  "enforcement": "Dispatcher end-of-tick reconcile re-runs the raced-check (receipt-on-disk + lane-feed claim-history grep) on every orphan declined at adoption, before the tick ends; the night-dispatcher mirror log records the re-sweep for each declined orphan (hit or miss). A declined orphan dropped without a re-sweep is a process violation — the reconcile checklist names the re-sweep step explicitly.",
  "decision_change": "Future orphan-adoption decisions change from 'raced-check raced → drop it' to 'raced-check raced → decline-with-reason, re-sweep at reconcile.' Future reconcile decisions gain a standing question: 'any declined orphans whose disposition changed since adoption?' — answered from live bytes, not from the adoption-time verdict.",
  "falsifier": "A week of ticks in which every re-sweep returns empty (no declined orphan ever transitions raced→claimed→closed within a tick window) falsifies the value: the re-sweep is then pure overhead and the note is retired to OBSERVATION. Conversely, a declined orphan that transitions to closed but whose receipt the re-sweep MISSES (sweep ran before the claim completed, or the sweep looked at the wrong brief) falsifies the sweep's timing — the note is then revised to specify the re-sweep's temporal window.",
  "mechanism": "The dispatcher and the lane-executor are independent actors racing on the same brief. The raced-check samples the brief's disposition at one instant; because claim→close cycles complete in minutes, a 'raced' verdict can be stale before the tick ends. A deferred re-sweep at reconcile samples again after the race has had time to settle, so transitions that occurred mid-tick are caught and filed instead of dropped.",
  "evidence": "hidden_files/lesson-broadcast.md, t0828 (2026-10-18T08:59Z): 'ORPHAN declined: brief-gap-gate-stall-20261018-0845-laneexecutor.md raced the adoption check — lane-executor claimed it 08:54Z (lane-feed sign-in, Receipt to follow). Lesson: the orphan raced-check runs at adoption time, not file-discovery time.'; t0829 (2026-10-18T09:05Z): 'RECONCILE: lane-executor gate-stall follow-up (claimed 08:54Z, lane-feed sign-in present, CLOSING RECEIPT gap-gate-stall-20261018-0845-laneexecutor.md on disk) -> moved to claimed/done/ per the t0733 precedent. Lesson: the t0828-declined orphan (raced the adoption check) became a closing receipt ~10 min later — raced-check is a deferral, not a rejection; re-sweep declined orphans before the tick ends.'",
  "cousins": ["t0733 precedent (claim+close without entering rotation → dispatcher completes the move — what the re-sweep acts on)", "SN-01553 (finished work is per-brief, not per-parent — disposition lives at the brief level)"]
}
~~~
