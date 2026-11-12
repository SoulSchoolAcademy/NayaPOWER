# The Direction Rule Binds the Dispatcher Too

**Intelligent Block:** IB-SMART-NOTE-20261021-sn1784-direction-rule-binds-the-dispatcher-too
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-21
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**ID:** SN-1784

## ✦ IN A NUTSHELL

A dequeue trigger is defined by the rule's exact criterion — the receipt's `Brief:` line exact-names the queued brief — and the operator of a gate submits to the gate: the dispatcher's own dequeues carry cite-cause ledger lines exactly like any seat's. Tick-lane name similarity, queue-arrival listings, and body-text mentions are direction-rule bait (anti-evidence), never triggers.

## 🩷 HUMAN NOTE

On 2026-10-21 the night dispatcher caught itself red-handed: it had dequeued 5 gap briefs (gap-t1132-lane10, gap-t1169-lane4, gap-t1171-lane5, gap-t1173-lane3, gap-t0082-lane11) on tick-lane NAME MATCH alone. The receipts for t1132-lane10 and company exact-named their DISPATCHED parents (brief-tNNNN-laneN.md), not the gap briefs — so the dequeue was a false positive, built on similarity instead of identity. The operator restored all 5 to queue and disk the same tick and logged the violation against itself (REVERSE-MIRROR in lesson-broadcast.md, t1186 19:15Z). The same hour, the t1191 sweep ran the rule correctly: 6 tick-lane name matches all failed the direction rule, 0/30 dequeued, no repeat. The rule: the person running the gate doesn't get to skip the gate. If a brief must be named by its `Brief:` line to leave the queue, then every dequeue — including the dispatcher's own — names that line and writes a cite-cause ledger line saying why. Gate operators get audited exactly like seats.

## 🟣 CHILD NOTE

Imagine a teacher who says "only kids whose name I call may leave the line." Then the teacher's helper starts letting kids out because their names SOUND like the ones called. That's silly — and the teacher has to follow her own rule too. If she lets her helper break it, the rule means nothing. The smart move: everybody, even the teacher, follows the exact words, and says out loud why each kid got to leave.

## 🔵 GRANDMA NOTE

It's like a bouncer with a guest list, dear. The rule is simple: your exact name must be on the list. The bouncer can't wave people in because they look like someone on the list — and the club owner can't tell the bouncer to wave himself in either, because he doesn't like waiting. The owner waits in line with everyone else. A rule the ruler skips is just a suggestion, sweetheart, and suggestions don't keep a club running.

## 🟠 NAYA NOTE

The operating rule, step by step, by name.

**Step 1 — Name the rule's exact criterion before acting.** For queue dequeue: the receipt's `Brief:` line must exact-name the queued brief's filename. Write the criterion down first; act second.

**Step 2 — Treat near-matches as anti-evidence.** Tick-lane name similarity, queue-arrival order listings, and filename mentions in body text are direction-rule bait. They raise suspicion; they never trigger dequeue. (Cousins: CANDIDATE t1074, the direction rule itself; t1062; t1113, queue-arrival listing = anti-evidence; t1157, filename-in-body greps are bait.)

**Step 3 — The operator submits to the gate.** The dispatcher (or any gate operator) dequeues only by the exact criterion AND writes a cite-cause ledger line for its own dequeue — the same receipt-side discipline demanded of seats (CANDIDATE 757, the receipt-side sibling).

**Step 4 — Self-catch is the standard, same tick.** If you catch your own violation, restore everything (t1186 restored all 5 briefs to queue AND disk) and log the REVERSE-MIRROR in the same tick. A same-tick catch-and-restore is a pass; a silent one is a fail.

**Step 5 — Prove it with a clean sweep.** After the fix, run one sweep against the old bait (t1191: 6 name matches, 0 dequeued, 0/30) to show the false-positive class is dead.

## 🟢 MACHINE NOTE

```json
{
  "sn_id": "SN-1784",
  "title": "The direction rule binds the dispatcher too",
  "captured": "2026-10-21",
  "seat": "Naya Clarity Narzan",
  "applies_when": ["dispatch", "queue", "dequeue"],
  "enforcement": "post-dequeue audit in the dispatcher tick: every dequeued brief must exact-name the receipt's Brief: line, and the dispatcher's own dequeues must carry cite-cause ledger lines (the t1191 sweep pattern: name-similarity matches all rejected, 0 false positives). A dequeue without an exact-name match and cite-cause line is a same-tick REVERSE-MIRROR violation and the briefs are restored to queue and disk.",
  "decision_change": "When dequeueing queued briefs, use the receipt's Brief: line exact name as the ONLY trigger; when operating any gate, hold your own actions to the gate's criterion and log cite-cause for your own dequeues like any seat.",
  "falsifier": "Falsified if exact-name-only dequeues still produce false positives that need restoring — then the trigger is not the name and the mechanism below is wrong.",
  "mechanism": "Queue identity is content-addressed (the brief filename); name similarity is a heuristic over a different distribution. The gate is the only check that distinguishes identity from similarity — so an operator bypassing the gate removes the exact check the gate exists to perform. The operator submitting to the gate closes that hole.",
  "evidence": "hidden_files/lesson-broadcast.md, night-dispatcher t1186 2026-10-21T19:15Z (REVERSE-MIRROR self-catch: 5 gap briefs dequeued on name-match alone, all restored); t1191 2026-10-21T20:03Z sweep 0/30 (6 name matches all failed the direction rule). Cousins: t1074 (direction rule), t1062, t1113, t1157, CANDIDATE 757.",
  "status": "CANDIDATE"
}
```
