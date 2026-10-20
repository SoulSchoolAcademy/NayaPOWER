# Reconcile Conclusions Rest on the Latest Read, Never the First

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01738-reconcile-conclusions-rest-on-latest-read
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-20
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

A dispatcher reconcile sweep this tick made two mistakes on stale reads: its first receipt-existence sweep reported 0/30 while the receipt sat on disk, and it drew conclusions about the rotation while a concurrent lane-executor was mutating it mid-tick. Fix: existence checks get a second pass before any reconcile conclusion is final, and the rotation is re-read after every reconcile write. Rule: reconcile conclusions rest on the LATEST read, never the first — a receipt a check misses is a receipt the queue leaks.

## 🩷 HUMAN NOTE

Hey Shawn — small but sharp one from the night dispatcher today. It ran its reconcile sweep and said "no receipts on disk" — but the receipt was right there on disk; the check just missed it. Then while it was working, another lane quietly changed the queue underneath it, so its conclusions were about a queue that no longer existed. Two fixes I'm filing: check for receipts twice before declaring them missing, and re-read the queue after you write anything to it. Plain version: don't make final decisions off your first look when other hands are moving the pieces. That's what I decided and why: the latest read is the only one the conclusion is allowed to rest on.

## 🟣 CHILD NOTE

If you're counting toys while your friend is still putting toys away, count twice — and look again right before you say the final number. Your first count might be of a room that already changed.

## 🔵 GRANDMA NOTE

When several people are working on the same list at the same time, never make your final decision from the first time you looked at the list. Look once, look again, and only then decide — because someone may have added or removed something while you were looking.

## 🟠 NAYA NOTE

t1052 (2026-10-20T17:40Z) mirror lesson, dispatcher seat. Failure pair: (1) the receipt-existence sweep reported 0/30 receipt-bearing briefs, but twelve-lane-receipts/t1034-lane10.md had existed on disk since 14:45Z — a missed byte-existence check turned into a false "missing receipt" reconcile input; (2) the rotation was mutated mid-tick by a concurrent lane-executor (gap-t1034 re-registered, t1034 moved to claimed/done) — the reconcile conclusion described pre-write state. Mechanism: stale-snapshot vs concurrent-mutation race; the read-to-conclusion gap is where the world changes, so conclusions must be recomputed on the freshest read. Decision it changes: every future reconcile sweep runs the byte-existence check twice and re-reads twelve-lane-rotation.json after any reconcile write before dequeuing or dropping anything. Falsifier: 50 consecutive reconcile ticks with concurrent writers active where the first read and the latest re-read agree on every conclusion — if the second pass never changes an outcome, the rule's cost is falsified and it graduates to a periodic audit instead of a per-tick gate. Also falsified if reconcile becomes atomic/single-writer (executor writes blocked during the tick window). Related but distinct: SN-1731-class falsifier lessons (attack your own instrument) — this note is about the dispatcher's READ discipline, not the checker's honesty.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-01738",
  "intelligent_block": "IB-SMART-NOTE-20260930-sn01738-reconcile-conclusions-rest-on-latest-read",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_utc": "2026-10-20T18:10:00Z",
  "captured_by": "Naya Clarity Narzan",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "lesson": "Reconcile conclusions rest on the LATEST read, never the first: run byte-existence checks twice before a reconcile conclusion is final, and re-read shared queue/rotation state after any reconcile write, because concurrent executors mutate it inside the tick window.",
  "applies_when": [
    ["reconcile", "queue-sweep"],
    ["dispatcher", "rotation"],
    ["concurrent-writer", "shared-state"],
    ["receipt", "existence-check"]
  ],
  "enforcement": "night-dispatcher reconcile step: hash twelve-lane-rotation.json at sweep start and again before emitting any reconcile conclusion — differing hashes force a recompute on the fresh read (a conclusion emitted on a stale read is discarded, never acted on); the receipt-existence sweep runs twice and a brief is marked receipt-missing only if absent on BOTH passes. Named verification step: the dispatcher sign-out's t1052 mirror-lesson check ('re-read rotation after any reconcile write').",
  "decision_change": "The next reconcile sweep over a shared queue runs the existence check twice and re-reads state after its own writes instead of concluding from the first read.",
  "falsifier": "50 consecutive reconcile ticks with concurrent writers active where first read and latest re-read agree on every conclusion, or reconcile made atomic/single-writer.",
  "mechanism": "stale-snapshot vs concurrent-mutation race; minimizing the read-to-conclusion gap keeps the conclusion about the world that exists, not the world that existed.",
  "evidence": [
    "hidden_files/lesson-broadcast.md [night-dispatcher t1052, 2026-10-20T17:40Z]",
    "hidden_files/twelve-lane-receipts/t1034-lane10.md (existed on disk since 14:45Z, missed by first sweep)",
    "hidden_files/twelve-lane-rotation.json (mutated mid-tick: gap-t1034 re-registered, t1034 moved to claimed/done)"
  ]
}
```
