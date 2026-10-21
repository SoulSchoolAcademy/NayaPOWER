# The Direction Rule Runs Both Ways

**Intelligent Block:** IB-SMART-NOTE-20261021-sn1789-direction-rule-runs-both-ways
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-21
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**ID:** SN-1789

## ✦ IN A NUTSHELL

The exact-name direction rule has a converse. The forward direction says a dequeue fires only when a receipt's `Brief:` line exact-names the queued brief. The converse: when the brief's file is gone from disk but its receipt exists with the exact name AND the work is already recorded completed, the lingering queue entry is an orphan — dequeue it with a cite-cause line, don't leave it. Receipt-present + completed + absent-on-disk = dequeue, not leave.

## 🩷 HUMAN NOTE

On 2026-10-21 the night-dispatcher caught a reconcile-orphan: `brief-t1195-lane11.md` sat in rotation-queued with its receipt present (`twelve-lane-receipts/t1195-lane11.md`, `Brief:` exact-name verified) and the work already recorded under completed — but the file itself was gone from disk. The operator removed the orphaned queued entry and appended the cite-cause ledger line. The lesson it names: the t1074 direction rule runs both ways. Forward: never dequeue without exact-name evidence. Converse: never LEAVE a queue entry when the exact-name evidence (receipt + completed record) proves the work is done and the artifact is gone. Queue entries can outlive their files — deletion without dequeue is the failure mode, and the registry's own evidence is what authorizes the cleanup. (Evidence: hidden_files/lesson-broadcast.md — [night-dispatcher t1203, 2026-10-21T22:51:34Z] MIRROR reconcile-orphan.)

## 🟣 CHILD NOTE

Imagine a library checkout card still pinned on the board for a book that was already returned and reshelved — but the book itself was thrown away. The card says "out," the shelf says "gone," and the return log says "back." Leaving the card up just confuses everyone. The return log plus the empty shelf is all the proof you need to take the card down. That's the rule: clean up the card when the evidence says the book is done, not just when someone checks it out.

## 🔵 GRANDMA NOTE

It's like keeping a dentist appointment on the calendar after you've already been, the tooth is fixed, and the office closed down. The appointment card, the "all done" note from the dentist, and the empty building — together they say there's nothing to wait for anymore. Take it off the calendar, dear. A reminder for something that's finished isn't a reminder — it's clutter. The rule works in both directions: don't cancel without proof, and don't keep what's proven finished.

## 🟠 NAYA NOTE

The operating rule, step by step.

**Step 1 — Detect the orphan.** A queued entry whose file is absent from disk is a candidate orphan. Check the two evidence legs: (a) a receipt whose `Brief:` line exact-names the entry, and (b) the work recorded under completed.

**Step 2 — Apply the converse.** Receipt-present + completed + absent-on-disk = DEQUEUE. Remove the entry, append the cite-cause ledger line naming the file + op + cause. The same exact-name evidence that authorizes dequeue-by-receipt authorizes dequeue-by-absence.

**Step 3 — Never leave on partial evidence.** Absent-on-disk alone (no receipt, no completed record) is NOT an orphan — it may be a reverse-phantom (present-on-disk variant) or a lost file. The converse fires only on the full conjunction.

**The trap it defeats:** queue hygiene checked in only one direction. The forward rule stops false dequeues; without the converse, finished work leaves permanent ghost entries that the reconciler must trip over every tick.

## 🟢 MACHINE NOTE

```json
{
  "id": "SN-1789",
  "truth_state": "CANDIDATE",
  "captured": "2026-10-21",
  "applies_when": ["queue", "dispatcher", "reconcile", "direction-rule"],
  "enforcement": "The dispatcher's reconcile pass treats receipt-present + completed + absent-on-disk as a dequeue trigger: the orphaned entry is removed with a cite-cause ledger line (brief field exact-names the removed file + op + cause). A reconcile that leaves such an entry is flagged as an incomplete sweep.",
  "evidence": ["hidden_files/lesson-broadcast.md [night-dispatcher t1203, 2026-10-21T22:51:34Z] MIRROR reconcile-orphan: brief-t1195-lane11.md sat in rotation queued with its receipt (Brief: exact-name verified) and already recorded under completed, but the file is gone from disk — orphaned queued entry removed, cite-cause ledger line appended"],
  "falsifier": "If the file reappears on disk, the entry was not an orphan and the dequeue was wrong — the full conjunction (absent-on-disk) is load-bearing. If the receipt is revoked or the completed record is retracted, the converse does not fire.",
  "mechanism": "Queue entries can outlive their artifacts: deletion without dequeue leaves ghost entries. The exact-name receipt plus the completed record is the same class of evidence that authorizes the forward dequeue — applied symmetrically, it authorizes the converse cleanup instead of leaving the ghost for every future reconcile to trip over.",
  "cousins": ["CANDIDATE 770 / SN-1784 (the direction rule binds the dispatcher too — the forward direction)", "t1074 exact-name rule", "CANDIDATE 757 (cite-cause — the receipt-side sibling)"]
}
```
