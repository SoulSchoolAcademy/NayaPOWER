**Intelligent Block:** IB-SMART-NOTE-20261024-sn1945-verification-snapshot-valid-only-at-its-instant-rebuild-as-chain
**Smart Note:** SN-1945
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-24
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** twelve-lane-receipts/t1536-lane11.md (Mirror: "the receipt is only trustworthy when the time axis is on the page"; check 5/7 reconstruction); learning-events-2026-10-24-11.md, CANDIDATE 917

## ✦ IN A NUTSHELL

A verification snapshot is only valid at its own instant — when the queue moves between the reconcile and the verification, rebuild the verdict as a chain, not onto the reconcile-time literal. t1536-lane11 found the triple-gap brief registered in queued at t1536 time (15→16) and then legitimately removed by its own worker after closing (17→16, per the task body's step 9), so "triple-gap missing from queued" at verification time would have been a manufactured discrepancy. The seat instead rebuilt the chain — dispatcher_note_t1536 → dispatch note → worker receipt gap-gap-gap-t1530-lane12, gap CLOSED at bundle level 9.4 → current state 16 = 15 gaps + me — and proved both the registration and the supersession. The same receipt classifies claimed/ residue correctly: a signed-out worker's file still in claimed/ root is finished-but-unreconciled (the dispatcher's next move), not a phantom and not a queue loss — 2 claimed files = finished triple-gap + me, 0 phantoms.

## 🩷 HUMAN NOTE

Imagine counting the chairs in a room, leaving, and coming back to find one chair gone — and declaring a chair stolen. But in between, someone legitimately finished their work and took their chair away, with a note saying so. That is what happened here: a checker compared a later count against an earlier snapshot and nearly reported a missing item, when the item had simply been completed and removed by its own worker, with a paper trail. The lesson: when the thing you are checking can move while you check it, do not judge it against a frozen snapshot. Rebuild the story in order — what was filed, what was dispatched, what was finished, what is true now — and only call it a discrepancy if the story has a hole in it. A change with a paper trail is a supersession, not a loss.

## 🟣 CHILD NOTE

Imagine you count 16 marbles in a box, then your friend finishes a game and puts one marble away, properly, while you are still counting. If you then say "a marble is missing!" you would be wrong — it was not lost, it was put away on purpose. The checker here almost made that mistake: the list had changed because a worker finished a job and removed it, exactly as the rules say. The lesson: when things can move while you count them, write down the times — what was there at the start, what happened in the middle, what is there now. If every change has a reason and a note, nothing is lost. Only a change with no reason is a real problem.

## 🔵 GRANDMA NOTE

Dear, this is about not crying "missing!" when something was simply finished. A checker took a snapshot of a queue, and by the time she verified it, one item had been properly completed and removed by its own worker — with notes at every step. Comparing the new count to the old snapshot would have invented a loss that never happened. The lesson is simple: a snapshot is only true at the moment it was taken. When the thing you are checking is alive and moving, you must lay out the timeline — the first note, the dispatch, the worker's finished receipt, the current count — and judge the whole chain. A change that leaves a paper trail is not a discrepancy; it is the work getting done. And a finished worker's file still sitting in the claimed pile is not a ghost — it is just waiting for the dispatcher to reconcile it.

## 🟠 NAYA NOTE

The mechanism is shared mutable state under concurrent workers: a reconcile snapshot freezes one instant, and any verification that compares a later live state to that frozen literal without the intervening moves will manufacture discrepancies out of legitimate work. t1536-lane11 is the worked example — registration (15→16), worker close and removal (17→16), current state (16 = 15 gaps + me) — each step documented, each transition legitimate. The discipline is the time axis: every future verification whose subject moved mid-run carries reconcile note, dispatch note, worker receipt, and current state on the page, and a composition change with a paper trail is recorded as a supersession, not a discrepancy. Cousins: CANDIDATE 913 (stall snapshot, re-scan — new filings arriving) and CANDIDATE 915 (the verifier's own claim perturbing counts) — this one is the verification-time sibling: other workers' legitimate moves between snapshots. A claimed/ file from a signed-out worker is finished-but-unreconciled, a dispatcher action, never a phantom by default.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1945",
  "title": "A verification snapshot is only valid at its own instant — when the queue moves between the reconcile and the verification, rebuild the verdict as a chain, not onto the reconcile-time literal.",
  "applies_when": ["verification", "queue", "reconcile", "lane-executor"],
  "enforcement": "A verification receipt whose subject moved mid-run is returned as incomplete unless it carries the time axis on the page — reconcile note, dispatch note, worker receipt, and current state — and classifies each composition change as either a supersession with a paper trail or a discrepancy without one; a receipt that reports a missing item against a reconcile-time literal without that chain is rejected by the verifying seat's own check before it is filed.",
  "decision_change": "Future verifications do not fail a clean reconcile when an item disappears between the reconcile and the verification — after t1536-lane11, the verifier first rebuilds the chain (registration, dispatch, worker close, current state) and only reports a discrepancy when a step has no paper trail, instead of reporting a manufactured loss.",
  "falsifiability": "Falsified if a verification that compares live state directly to a reconcile-time literal, with no time axis, is shown to produce no manufactured discrepancies across runs where the subject moved mid-run — then the chain adds nothing. Weakened if intervening moves are proven always visible in the live state itself, so the literal comparison already contains the trail.",
  "mechanism": "The queue is shared mutable state under concurrent workers: a reconcile snapshot freezes one instant, and workers legitimately add, claim, close, and remove items between snapshots. A literal comparison of later state to the frozen snapshot conflates legitimate supersession (a documented close and removal) with loss, because it erases the time dimension in which the change was authorized. Restoring the time axis — each move with its note and receipt — separates authorized change from unexplained change, which is the only distinction a verification verdict needs.",
  "evidence": ["twelve-lane-receipts/t1536-lane11.md (Mirror: 'the receipt is only trustworthy when the time axis is on the page'; check 5/7 reconstruction; dispatcher_note_t1536 → dispatch note → worker receipt gap-gap-gap-t1530-lane12, gap CLOSED at bundle level 9.4; current state 16 = 15 gaps + me; 2 claimed files = finished triple-gap + me, 0 phantoms)"]
}
```
