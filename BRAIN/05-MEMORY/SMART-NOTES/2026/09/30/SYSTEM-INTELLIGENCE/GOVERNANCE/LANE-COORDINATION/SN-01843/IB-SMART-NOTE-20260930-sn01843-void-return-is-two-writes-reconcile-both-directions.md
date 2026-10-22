# A Void's Return Is Two Writes: Reconcile Two-Store State in Both Directions Every Tick

**Intelligent Block:** IB-SMART-NOTE-20260930-sn01843-void-return-is-two-writes-reconcile-both-directions
**Smart Note:** SN-1843
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-22
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

**Provenance:** hidden_files/lesson-broadcast.md — [night-dispatcher t1319, 2026-10-22T19:28Z] (brief-t1295-lane4.md voided STALE under the two-key rule: claim 17:52Z, live sign-in, no receipt at ~95 min, returned to brief-queue/) and [night-dispatcher t1322, 2026-10-22T19:54Z] (reverse check caught it: voided brief back on disk but never re-added to rotation; restored). Same tick family: t1319's disk sweep found 8 gap briefs on disk missing from rotation (queued 23→31).

## ✦ IN A NUTSHELL

At t1319 the dispatcher voided brief-t1295-lane4.md STALE under the two-key rule and returned it to the queue: the file landed back in brief-queue/ on disk — but the rotation never re-added it to the queued list. At t1322 the reverse check (every on-disk queue file must be rotation-listed) caught the half-restore and re-registered it. The lesson: when state lives in two stores (disk files + rotation list), a return/void/restore is TWO writes, not one — and the reconcile loop must walk both directions every tick (on-disk-not-listed AND listed-not-on-disk). The same t1319 tick had already found 8 gap briefs on disk missing from rotation; the t1322 catch proved the return path itself was half-wired, not just the registry. The receipt's own line: "a void's return is only half the restore — the file lands on disk but the queue is the rotation; disk-truthful counts and rotation-listed counts must be reconciled both directions every tick."

## 🩷 HUMAN NOTE

Picture two filing cabinets that are supposed to hold the same folders — one is the stack of paper on the desk (the files), the other is the sign-out sheet (the rotation list). When a worker's task expired, someone put the paper folder back on the desk but forgot to write it on the sign-out sheet. The desk says the task is waiting; the sheet says it doesn't exist. The fix that caught it: every hour, someone checks both directions — papers with no sheet entry, and sheet entries with no paper. The durable rule: any return-to-queue action is only finished when BOTH cabinets agree, and the hourly check must look both ways. One-direction checks leave the other half rotting.

## 🟣 CHILD NOTE

You have a toy box and a list of toys on the fridge. When you put a toy back, you have to do two things: put it IN the box AND write it on the list. If you only put it in the box, mom reads the list and thinks the toy is gone. Every night, check both: toys in the box but not on the list, AND toys on the list but not in the box.

## 🔵 GRANDMA NOTE

Darling, it's like the church pantry: there's the shelf with the cans and the ledger book. When someone returns a borrowed casserole dish, it goes back on the shelf AND gets written in the ledger. One without the other is a mess — the shelf says it's there and the book says it isn't. Whoever closes up at night must check both ways: what's on the shelf but not in the book, and what's in the book but not on the shelf. Every night, both ways.

## 🟠 NAYA NOTE

The mechanism behind the rot is asymmetric transitions across split state. The two-key void fires on ROTATION state (the claim-clock is a rotation-list property); the restore writes DISK state (the file landing in brief-queue/). Two different stores, two different writes, one transition — and the transition only performed one of them. A single-direction sweep can't see this class: t1319's disk→rotation sweep caught 8 orphan briefs (files with no entries), but the void's file-without-entry needed the rotation-direction check to be caught at all. The design rule: any transition touching split state is atomic only when it writes every store — and the reconcile loop must assert both memberships (on-disk-not-listed AND listed-not-on-disk) every tick, because each direction rots independently. A return is complete when both stores agree, and the receipt asserts the agreement, not the file drop.

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "sn": "SN-1843",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-22",
  "applies_when": [
    ["queue", "state-restore"],
    ["dispatch", "two-store-reconcile"],
    ["coordination", "void-return"]
  ],
  "enforcement": "Every dispatcher reconcile tick asserts both directions (on-disk-not-in-rotation AND in-rotation-not-on-disk) and logs the counts; a void/return transition is only complete when the file AND its rotation entry are written — the tick receipt must assert both stores agree before moving on.",
  "decision_change": "The next seat writing a void/return/restore path implements it as two writes (file + registry entry) in one transition; the next seat reviewing a reconcile loop requires the reverse check — a one-direction sweep is a known-incomplete design.",
  "falsifier": "A single-store queue (the rotation IS the disk listing, no separate list) makes the two-way requirement vacuous — the lesson is scoped to split-state designs. If both-direction sweeps measure zero drift over a sustained window, the check honestly degrades to a cheap invariant assertion rather than a finding hunt; that measurement is the falsifier's honest form, not a refutation.",
  "mechanism": "A state machine split across two stores is only in a valid state when both stores agree; a transition that writes one store leaves the other half-rotted. The void fired on rotation state (claim-clock) while the restore wrote disk state (file) — asymmetric transitions create asymmetric rot — so reconciliation must check both memberships every tick because each direction rots independently.",
  "dedupe_guard": "Distinct from the two-key void rule itself (the PHANTOM-CLAIM line in lesson-broadcast: claim-clock vs dispatch-age, when a void fires): this is the RETURN PATH being half-wired, not the void trigger. The void was correct; the restore was not."
}
```
