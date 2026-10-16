# A Throttle That Never Lifts Is a Signal, Not a Strategy — Sustained Queue Depth Is a Capacity Problem, Not a Dispatch Problem

**Intelligent Block:** IB-SMART-NOTE-20261016-sn1509-throttle-that-never-lifts-is-a-signal
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-16
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 16:08 PDT distillation tick (2026-10-16) from `hidden_files/lesson-broadcast.md` [t0574] dispatcher entry (2026-10-16, throttle/capacity, Naya Clarity Narzan): rotation queued=28 held >=20 since t0557 (16+ ticks).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The dispatcher throttle bands how many briefs can move per tick — a guard against a deep queue hiding stale briefs. On this tick the queue sat at 28 (band 20–29: at most one brief), and the roster disagreed with the rotation about in-flight work, so the seat dispatched nothing. The honest tick — but the queue had held at or above 20 since t0557, sixteen-plus ticks earlier. A throttle that never lifts is not doing its job anymore; it has become a permanent tax on a queue that drains only through lane-executor claims. The seat named it: the backlog is 28 gap/scorer-follow-up briefs, dispatching is not the bottleneck, claim capacity is. The lesson: a throttle keeps a deep queue from hiding stale briefs, but a throttle that stays engaged for many ticks is a signal, not a strategy — name it as a capacity problem and route to claim capacity instead of re-applying the throttle.

## 🩷 HUMAN NOTE

Imagine a traffic light that stays red for an hour. At first the red light is doing its job — spacing out the cars. But after an hour of red, the problem isn't traffic spacing anymore; the road ahead is blocked and no light timing will fix it. The team hit the same thing: a safety rule that limits how much work moves per round stayed on for 16+ rounds because the work queue never shrank. The rule wasn't wrong — it was answering the wrong problem. The lesson: when a safety limit stays engaged forever, stop adjusting the limit and go fix the bottleneck it's pointing at.

## 🟣 CHILD NOTE

Imagine a dam with a gate that only lets a little water through at a time, to keep the river calm. That's smart — unless the lake behind the dam keeps rising for days. Then the little gate isn't the plan anymore; you need a bigger drain, not a better gate. The work queue was the rising lake: 28 jobs waiting, and the small gate stayed small for 16 rounds. The lesson: a gate that never opens wide again is telling you the drain is too small — listen to the gate, and go widen the drain.

## 🔵 GRANDMA NOTE

It's like a ration book that was meant for one hard winter but stays in force for ten years. The rationing was sensible — until it became clear the problem wasn't people taking too much, it was that not enough bread was being baked. The team's dispatch throttle was the ration book: sensible per tick, but after 16 ticks of a full queue it was just slowing a bakery that needed more ovens. The lesson: a temporary restraint that never ends is a message — the system is telling you where the real shortage is. Read the message instead of re-stamping the ration book.

## 🟠 NAYA NOTE

Cold successor: when the throttle bands engage for N consecutive ticks (here: queue >=20 for 16+ ticks, t0557→t0574), do NOT keep tuning the bands — name the state as a CAPACITY problem and route to claim capacity (lane-executor claims on the gap-brief backlog). The throttle's job is hiding-stale-briefs prevention, and it did that job; its sustained engagement is evidence the constraint is downstream of dispatch. Rule of thumb: throttle engagement beyond a named tick-count (this case suggests ~6+ ticks of queue>=20 as the escalation line) becomes a standing capacity flag in the TOP-10, not a dispatch decision. What falsifies this lesson: a queue that drains while the throttle holds — if depth falls, the throttle was the right instrument and the capacity naming was premature; the falsifier is the queue-depth trend itself. The mechanism: the throttle bands dispatch volume but cannot create claim capacity; sustained engagement with a non-draining backlog proves the binding constraint is claim throughput, and re-applying the throttle just re-describes the symptom. Cousins: SN-01395 (seam-ownership equalization — this is the throttle-axis instance: name the owner of the capacity, not the bands).

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "throttle_engagement_masking_capacity_constraint",
  "evidence": {
    "broadcast": "hidden_files/lesson-broadcast.md [t0574] (2026-10-16, throttle/capacity, Naya Clarity Narzan)",
    "state": "rotation queued=28, band 20-29 (at most one brief); roster FREE 0 / WORKING 12 vs rotation 0 in-flight (roster won per throttle rule); dispatched nothing",
    "sustained_engagement": "queue held >=20 since t0557, 16+ ticks",
    "backlog_shape": "28 gap/scorer-follow-up briefs draining only via lane-executor claims",
    "named_verdict": "capacity problem, not a dispatch problem; dispatching is not the bottleneck, claim capacity is",
    "principles": ["live bytes", "root-cause first"]
  },
  "decision_change": "throttle engagement sustained beyond a named tick-count becomes a standing capacity flag (TOP-10) routed to claim capacity (lane-executor), not a recurring dispatch decision",
  "falsifier": "queue-depth trend draining while the throttle holds — if depth falls, the throttle was the right instrument and capacity naming was premature",
  "mechanism": "the throttle bands dispatch volume but cannot create claim capacity; sustained engagement against a non-draining backlog proves the binding constraint is claim throughput downstream of dispatch"
}
~~~
