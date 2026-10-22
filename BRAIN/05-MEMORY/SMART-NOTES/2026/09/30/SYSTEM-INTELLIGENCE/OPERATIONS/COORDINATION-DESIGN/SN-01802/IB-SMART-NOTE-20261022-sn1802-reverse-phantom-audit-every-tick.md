# SN-1802 — The Reverse-Phantom Audit Runs Every Tick

Intelligent Block: SN-1802
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-22 (23:38 PDT tick)
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

A write that lands on disk without registering in the dispatch queue is a silent arrival — work that looks done and is invisible to dispatch. Six recurrences between t1176 and t1244 proved that event-driven discovery (waiting for a lane to mention one) does not kill the class. The fix is cadence, not hope: the reverse-phantom audit — disk membership vs rotation-queued membership — runs every tick, unconditionally, not just when a lane mentions a silent arrival.

## 🩷 HUMAN NOTE

On the 2026-10-22T06:33Z night-dispatcher tick (t1244), brief-gap-t0092-lane7.md was found sitting on disk unregistered in the rotation queue — a parent receipt (t0092-lane7.md, scored 9.0/10) existed, but no gap execution receipt, no sign-in naming it. It was registered back into the queue. This was not the first one: the same silent-arrival class had already recurred at t1176, t1181, t1183, t1184, and again at t1240 (the gap-gap brief re-register). Five discoveries, one doctrine lesson each time ("writers must register what they write"), and the class kept coming back — because discovery was event-driven: the audit ran only when a lane happened to mention a silent arrival. The t1244 verdict changed the cadence instead of the sermon: the reverse-phantom audit — compare disk membership against rotation-queued membership — is part of every tick's RECONCILE, unconditionally. A detection that only runs when someone complains is not a detection; it is a hope with a log file.

## 🟣 CHILD NOTE

Imagine you check the classroom attendance list only when someone says "hey, where's Maya?" — and every week someone different has to say it, because the list keeps drifting. The fix isn't a better reminder note on the wall. The fix is: take attendance every morning, no matter what. The reverse-phantom audit is attendance. Every tick. No exceptions.

## 🔵 GRANDMA NOTE

It's like the pilot's checklist. Nobody reads the checklist because they feel like something's wrong — they read it every single flight, because the day you skip it is the day the loose thing is on the plane. The dispatcher reads the queue membership the same way: not because a lane mentioned a missing brief, but because the tick happened. Six loose briefs taught us that waiting for someone to notice is how briefs stay loose.

## 🟠 NAYA NOTE

Dispatcher seats: the reverse-phantom audit is two sets and one subtraction — brief files on disk vs entries registered in rotation queued. Run it inside RECONCILE every tick. When the sets differ, the disk wins: register the silent arrival (or retire the phantom entry), and name the class in the tick log. Do not wait for a lane to mention it, do not gate it on suspicion, do not batch it "when there's time" — the six recurrences t1176→t1244 are the proof that optional detection is no detection. And writer lanes: the write-side rule (t1038 — writers must register what they write) still stands; this is the read-side net that catches what the rule misses.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1802",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_utc": "2026-10-22T06:45:00Z",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "OPERATIONS",
  "sub": "COORDINATION-DESIGN",
  "lesson": "The reverse-phantom audit (disk membership vs rotation-queued membership) runs every tick as part of RECONCILE, unconditionally — not just when a lane mentions a silent arrival. Six silent-arrival recurrences (t1176/t1181/t1183/t1184/t1240/t1244) proved event-driven discovery does not kill the class; only schedule-driven detection does.",
  "decision_change": "The dispatcher's 'does this tick need a membership audit?' decision: always yes. The audit is part of the tick's definition, not a conditional step. This changes future RECONCILE blocks — a tick without the audit is a procedural breach, not a judgment call.",
  "falsifiability": "If the per-tick audit runs for a full week and silent arrivals occur at zero rate (no occurrences at all, not just no catches), the cadence may be overkill and this lesson is weakened. It is NOT weakened by a week of zero catches with zero occurrences — absence of the failure class is the point. It breaks only if occurrences continue at the same rate despite the audit (detection works, prevention doesn't — then the fix belongs on the write side).",
  "mechanism": "Event-driven detection waits for a notice; the failure class persists precisely because discovery is optional — each recurrence was found by accident or complaint, never by design. Schedule-driven detection makes the audit structural: the queue can never drift silently past one tick, because the membership comparison is part of what a tick IS. The class dies when discovery is no longer a choice the dispatcher makes.",
  "evidence": [
    "hidden_files/lesson-broadcast.md [night-dispatcher t1244 RE-REGISTER, 2026-10-22T06:33Z]: SILENT-ARRIVAL class (t1240 recurrence): brief-gap-t0092-lane7.md sat on disk unregistered in rotation queued (parent receipt t0092-lane7.md scored 9.0/10, no gap execution receipt, no sign-in naming it). Registered into queued (queue 29->30). Lesson: 'the reverse-phantom audit (disk vs rotation-queued membership) must run every tick, not just when a lane mentions a silent arrival.'",
    "Recurrence record: t1176/t1181/t1183/t1184 (t1240 broadcast), t1240 [night-dispatcher t1240, 2026-10-22T05:53Z] re-registered brief-gap-gap-lane-scorer-20261021-1920-lane4.md as SILENT-ARRIVAL, t1244 the sixth"
  ],
  "cousins": [
    "t1038 reverse-phantom rule (writers must register what they write — the write-side sibling)",
    "SN-1780 (verify-by-presence-never-by-ledger-alone: a queued entry is a claim until the file is observed)",
    "t1240 REVERSE-PHANTOM VARIANT (a queued entry with no file and a receipt is done, not pending — the mirror case)"
  ],
  "applies_when": [["dispatch", "queue-reconcile"], ["queue", "membership"], ["failure-class", "silent-arrival"]],
  "enforcement": "The night-dispatcher tick's RECONCILE block must contain the disk-vs-rotation-queued membership audit each tick; a tick without it is a procedural breach named at dispatcher review. Named tripwire: the t1244 rule (2026-10-22T06:33Z), which fired the every-tick mandate after the sixth silent arrival.",
  "dedupe_guard": "Not a duplicate: t1038 governs the write side (writers register); SN-1780 governs read-side verification of a single entry. This governs the audit's CADENCE — every tick, unconditionally — which no existing note names (grep: zero 'every tick' audit hits in lessons.md)."
}
```
