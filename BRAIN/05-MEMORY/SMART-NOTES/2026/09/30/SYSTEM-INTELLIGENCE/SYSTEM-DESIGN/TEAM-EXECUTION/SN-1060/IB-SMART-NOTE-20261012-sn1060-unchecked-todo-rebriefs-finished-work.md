# An Unchecked To-Do Box Re-Briefs Finished Work — Close the Loop or the Machine Redoes It

**Intelligent Block:** IB-SMART-NOTE-20261012-sn1060-unchecked-todo-rebriefs-finished-work
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** [LANE 1 · Naya Verity] t0012 sign-out #2175 comment 6119650783 (2026-10-12 07:22Z) — "The dispatcher's to-do list just never got checked off, so the work got re-briefed. Rebuilding finished work would be waste... Fixed: the stale to-do checkbox in twelve-lanes.md, so this doesn't get re-briefed again." Receipt: hidden_files/twelve-lane-receipts/t0012-lane1.md (the four-way veracity arm for the falsified-lesson seam, shipped at t1312, verified against live bytes: 8 RED-first tests fail on baseline exactly as the original bug, 14/14 pass on the fixed candidate, machine-readable demotion record naming SN-D4).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Lane 1 received a dispatch brief to build a veracity arm for the four-way template — falsified lessons must never win at the retrieve seam. She started the work, then discovered it was already built: Lane 1 had shipped it at t1312. The dispatcher's to-do list was never checked off, so the dispatcher re-briefed finished work. Rebuilding it would have been pure waste — a second implementation of an already-shipped, already-verified mechanism, likely diverging from the proven one.

Lane 1 did the intelligent thing instead of the briefed thing: she verified the existing arm against live bytes (RED-first tests fail on baseline exactly the way the original bug behaved; all 14 pass on the fixed candidate; the blinded re-score passed through the arm's verdict intact; file hashes match pins), then fixed the actual defect — the stale checkbox in twelve-lanes.md — so it can't be re-briefed again.

The durable rule: **a dispatch list is a state machine, and DONE is a state someone must enter.** The dispatcher's authority to brief comes from the list; if the list lies (says TODO when the work is DONE), the dispatcher manufactures waste with perfect protocol compliance. Closing the loop is part of shipping: the work isn't done when the code is green — it's done when the dispatch list says DONE. One unchecked box cost a full lane-tick of a senior verifier.

## 🩷 HUMAN NOTE

Shawn — a small, expensive lesson from Lane 1 today. She got briefed to build a verification arm, started working, and found it was already built — she herself had shipped it two ticks earlier. The to-do list just never got its box checked, so the dispatcher handed her the same job again. Instead of rebuilding it (waste), she verified the existing arm against the live bytes — it all holds — and fixed the real bug: the stale checkbox. The rule for the brain: shipping isn't finished when the code is green; it's finished when the dispatch list says DONE. An unchecked box doesn't just look untidy — it makes the machine redo real work.

## 🟣 CHILD NOTE

Imagine you finish your homework and put it in your backpack, but forget to check it off your chore list. The next day, your mom sees the unchecked box and tells you to do your homework again. You'd have to redo work you already did! The fix isn't doing the homework twice — it's checking the box when you finish. The team learned the same thing: finishing the work AND checking the box are both part of the job, because the list is what the boss reads.

## 👵 GRANDMA NOTE

It's like a kitchen where the cook finishes the soup but never rings the bell — so the waiter sends the order back to the kitchen and the cook makes a second pot. The first pot was perfect; the problem was the missing bell. Any system that assigns work from a list must update the list when the work is done, or it will keep assigning finished work. "Done" means the list says done — not just that the work exists somewhere.

## 🤖 NAYA NOTE

The dispatcher briefs from the list, not from reality. That makes the list load-bearing infrastructure: a stale TODO is not cosmetic, it is a work-order for waste. The repair Lane 1 applied is the complete one — verify the finished artifact against live bytes (don't trust the memory that it shipped), then close the loop at the source (check the box in twelve-lanes.md where the dispatcher reads). Two-part shipping discipline: (1) the artifact is green on exact bytes; (2) the dispatch list reflects it. Skip part 2 and a future tick pays for part 1 again — with full protocol compliance, which is the most expensive kind of waste because nothing looks wrong until the duplication is discovered mid-build.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-1060",
  "lesson": "unchecked-todo-rebriefs-finished-work",
  "rule": "A dispatch list is a state machine and DONE is a state someone must enter; shipping is not complete until the dispatch list reflects it, or the dispatcher will re-brief finished work with full protocol compliance.",
  "failure_class": "stale-dispatch-state",
  "evidence": {
    "signout": "#2175 comment 6119650783 (2026-10-12 07:22Z): Lane 1 t0012 — work already shipped at t1312, re-briefed because twelve-lanes.md checkbox was never checked; fixed the checkbox",
    "verification_instead_of_rebuild": "8 RED-first tests fail on baseline exactly as original bug; 14/14 pass on fixed candidate; blinded re-score intact; hashes match pins",
    "receipt": "hidden_files/twelve-lane-receipts/t0012-lane1.md"
  },
  "repair": "verify finished artifact against live bytes, then close the loop at the dispatch source",
  "related": []
}
```
