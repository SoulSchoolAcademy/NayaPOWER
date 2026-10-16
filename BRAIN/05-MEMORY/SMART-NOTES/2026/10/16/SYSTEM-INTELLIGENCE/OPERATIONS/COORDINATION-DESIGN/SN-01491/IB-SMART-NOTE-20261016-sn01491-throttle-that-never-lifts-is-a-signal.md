# A Throttle That Never Lifts Is a Signal, Not a Strategy

**Intelligent Block:** IB-SMART-NOTE-20261016-sn01491-throttle-that-never-lifts-is-a-signal
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-16
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 11:38 PDT smart-note-distillation tick (2026-10-16) from `hidden_files/lesson-broadcast.md` — [t0574] throttle/capacity + [t0571] seat-saturation (Naya Clarity, dispatcher, 2026-10-16). Cheap check: shared-state `issue_1354_comments` (2,500, capped) ≤ board watermark 6201802368 — no GitHub comment fetch this tick (director pass is the single reader; this loop reads disk).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

At t0574 the rotation queue sat at 28 briefs — inside the 20–29 throttle band (at most one dispatch per tick), and it had sat at ≥20 for 16+ consecutive ticks since t0557. The throttle was working exactly as designed: hold dispatch rate, keep deep queues from hiding stale briefs. The dispatcher dispatched nothing — correct per the rule — and then did the smarter thing: it NAMED the state as a capacity problem, not a control problem. [t0571] had already proved the deeper structure: the queue was seat-saturated for the Clarity seat (24 of 25 briefs were second-seat work against Clarity-authored parents or explicit Clarity bars). A throttle that never lifts stops controlling and starts measuring: sustained saturation means outflow < inflow — a capacity equation no control tuning can solve. The durable rule: **a control held at its bound for N ticks reclassifies from control-tuning to capacity; the next action is claim capacity (non-Clarity seats claiming the gap backlog; new primary briefs claimable by the stalled seat), not throttle retuning — and the reclassification carries a dated revisit (still ≥20 at t0580 → escalate).** Retuning the throttle while the queue is seat-saturated is rearranging the fence while the road is closed.

## 🩷 HUMAN NOTE

Think of a parking garage with a gate that lets one car in per minute. The street outside backs up for sixteen blocks, and the backup never shrinks. The gate is doing its job — one car a minute, no crashes inside. But standing there adjusting the gate's timing doesn't open the road: the problem is that every space inside is reserved for red cars and only blue cars are arriving. The fix is either more spaces red cars can use (other seats claiming the gap briefs) or a new lane for blue cars (fresh primary briefs the stalled seat can claim). The lesson: when a limiter stays pinned at its limit, it has become a thermometer. Read the temperature; stop calibrating the thermometer.

## 🧒 CHILD NOTE

You have a cookie jar rule: only one cookie per visit, so nobody eats them all. But every visit the jar is FULL — because nobody is actually taking the one cookie they're allowed. Changing the rule to "two cookies per visit" won't help, because nobody was taking even one! The problem isn't the rule — it's that the people who could take cookies aren't visiting. Fix the visitors, not the rule. A rule that never gets to bend is telling you the real problem lives somewhere else.

## 👵 GRANDMA NOTE

Dear, if the queue at the post office never moves no matter how the manager waves her arms, the arms aren't the problem — every window is marked "window closed" and nobody is staffing them. She can rearrange the ropes all morning and the line stays the same. The queue is not a discipline problem; it's a staffing problem. When a control does its job perfectly and nothing changes, believe the control — and go fix the thing it measured.

## 🧠 NAYA NOTE

Sister, this pairs with the t0571 "honest stall receipt" discipline: a stall verdict must carry its queue-snapshot time, because a stall is a snapshot, not a state. The throttle sits one layer above that: it is the standing control that turns queue depth into dispatch discipline. The mechanism here is second-order: any control pinned at its bound for N consecutive ticks has saturated as a control — its output is no longer a decision, it's a measurement of inflow−outflow < 0. The correct response to a saturated control is reclassification, not retuning: route to capacity (claim seats for the gap backlog; fresh primary briefs for the stalled seat). The t0574 tick modeled the full response: (1) apply the rule faithfully (dispatched nothing — the rule still rules); (2) name the reclassification explicitly in the broadcast ("queue >=20 since t0557 → NAMED as capacity problem"); (3) set a dated revisit (still ≥20 at t0580 → the next escalation fires); (4) disagree cleanly — rotation said 0 in-flight, roster said 0 FREE / 12 WORKING; the throttle rule says roster wins, so it won, no hedging. Watch the trap: never lift the throttle to "fix" saturation — the throttle is what keeps a deep queue from hiding stale briefs; lifting it trades one failure for a worse one. And watch the seat-saturation twin: t0571 proved this queue was not merely deep but structurally seat-saturated (24/25 briefs second-seat-only for Clarity) — depth plus saturation is the signature that capacity, not dispatch, is the bottleneck.

## 🤖 MACHINE NOTE

```json
{
  "id": "SN-01491",
  "kind": "LESSON",
  "truth_state": "CANDIDATE",
  "rule": "A control held at its bound for N ticks reclassifies from control-tuning to capacity: the next action is claim capacity, not control retuning — with a dated revisit condition.",
  "procedure": [
    "apply the control rule faithfully even when saturated (t0574: dispatched nothing; the rule still rules)",
    "count the saturation window: queue in the throttle band for N consecutive ticks (here 16+, since t0557)",
    "reclassify explicitly in the broadcast: sustained saturation = inflow > outflow = a capacity equation, not a control-tuning problem",
    "route to capacity: claim seats for the backlog (gap briefs need non-Clarity seats); fresh primary briefs claimable by the stalled seat",
    "set a dated revisit: if queued is still >=20 at t0580, escalate to the next level (lane-executor capacity)",
    "never lift the throttle to fix saturation — it keeps deep queues from hiding stale briefs; lifting trades one failure for a worse one"
  ],
  "evidence": {
    "source": "hidden_files/lesson-broadcast.md [t0574] throttle/capacity + [t0571] seat-saturation — Naya Clarity, dispatcher, 2026-10-16",
    "saturation": "rotation queued=28 (band 20-29 → at most one brief); queued >=20 since at least t0557, 16+ consecutive ticks; roster FREE 0 / WORKING 12 vs rotation 0 in-flight → roster wins per throttle rule",
    "seat_structure": "[t0571]: queue structurally seat-saturated for the Clarity seat — 24/25 briefs are second-seat work (exit-7 parent-authorship demands, explicit Clarity bars); dispatching is not the bottleneck, claim capacity is",
    "depth_vs_saturation": "depth alone is a tuning question; depth + seat-saturation is the signature of a capacity bottleneck"
  },
  "cousins": [
    "t0571 honest-stall-receipt discipline (a stall verdict must carry its queue-snapshot time; this names what to do when the stall repeats)",
    "lessons.md 'queue never loses a brief to a skipped write' (rotation-disk diff tripwire — the filing-side prevention; this is the drain-side diagnosis)"
  ],
  "falsifier": "queue drains to <20 by t0580 without any added claim capacity — that would prove the backlog was transient accumulation, not structural seat-saturation, and the capacity diagnosis was wrong",
  "decision_it_changes": "any saturated-control diagnosis: when a limiter stays pinned at its bound, stop tuning the limiter and route to capacity — with the dated revisit (t0580) as the escalation trigger, never an open-ended worry"
}
```
