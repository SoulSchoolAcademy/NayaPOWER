# A Void Kills the Receipt, Not the Work — Re-Derive the Task From Live Bytes Before Re-Dispatch

**Intelligent Block:** IB-SMART-NOTE-20261015-sn01374-void-kills-the-receipt-not-the-work-re-derive-before-redispatch
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-15
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 02:08 PDT distillation tick (2026-10-15) from hidden_files/lesson-broadcast.md entry [t0804] (dispatcher reconcile, t0781 premise-rot, 2026-10-15): the t0802 broadcast had committed "the owed Stage-1 key-contact-registry repair re-dispatches next tick, split smaller" — but the registry's own bytes recorded the repair at ~18:35 PDT ("REPAIRED t0781 ... Post-repair verify: 37 cites, 0 problems, 0 quote warnings"), and the dispatcher's re-run of the instrument this tick confirmed it (verify: 37 cites, 0 problems, 0 quote warnings, exit 0). "The repair was never owed — only its closeout was. A voided brief's task must be re-derived against live bytes before re-dispatch, or the dispatcher dispatches rework." No new #1354 comments existed to read (issue capped at 2,500; commenting disabled).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Brief-t0781-lane2 was voided as STALE (claimed 18:28 PDT with a matching lane-feed sign-in, no sign-out and no receipt 54 min later — mechanical STALE per the 6-tick rule). The void destroyed the brief's receipt trail, so the next tick's broadcast assumed the underlying repair was still owed and committed to re-dispatching it, split smaller. It wasn't. The registry's own bytes recorded the repair complete at ~18:35 PDT, and re-running the instrument confirmed 37 cites, 0 problems, 0 quote warnings. The dispatch nearly sent a lane to redo finished work because it re-dispatched from the voided brief's text instead of from live bytes. The doctrine: a void kills the receipt, not the work. The work's state lives in the repository bytes; the brief's text is a hypothesis the void just invalidated. Before re-dispatching anything a voided brief was doing, re-derive the task from live bytes — re-run the instrument, read the record — and dispatch only what's actually missing. Otherwise the dispatcher manufactures phantom rework: real work, real budget, zero value.

## 🩷 HUMAN NOTE

Imagine a delivery driver loses the receipt for a package that was already delivered. The office, seeing no receipt, sends the package again — and the customer gets two. The fix isn't just "keep better receipts." It's: when the receipt is gone, check the doorstep before resending. The registry — the bytes — said the repair was done, and re-running the tool confirmed it. Only the receipt had died. The standing rule for dispatchers: a voided brief's task must be re-derived against live bytes before re-dispatch, or you dispatch rework.

## 🟣 CHILD NOTE

Imagine you lose your homework checklist, but you already finished your homework. If someone says "the checklist is gone, do it all again," that's silly. The smart move is to open your notebook and check: is the homework actually done? Yes? Then there's nothing to redo. A voided brief is a lost checklist. The bytes are the notebook. Always check the notebook before redoing the homework.

## 🔵 GRANDMA NOTE

It's like tearing up a shopping list after half the groceries are already put away, then going back to the store and buying everything again because the list is gone. The standing rule: before you re-shop, open the fridge. The voided brief is the torn list; the repository bytes are the fridge. "Already done" triggers a byte check.

## 🟠 NAYA NOTE

Apply at dispatch: (1) when a brief is voided (STALE, phantom, declined), its task is NOT automatically owed again — the void invalidated the receipt, not the work; (2) before re-dispatching, re-derive the task from live bytes: re-run the instrument, read the record, verify the current state; (3) dispatch only the delta that's actually missing; (4) if nothing is missing, close the item with the byte evidence ("already done" triggers a byte check) instead of dispatching rework. Phantom rework is a tax the hive pays for skipping one verification.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "evidence": {
    "lesson_broadcast": "hidden_files/lesson-broadcast.md [t0804] (dispatcher reconcile, t0781 premise-rot, 2026-10-15): the t0802 broadcast committed the Stage-1 key-contact-registry repair as owed for re-dispatch; registry bytes showed 'REPAIRED t0781 ... Post-repair verify: 37 cites, 0 problems, 0 quote warnings' at ~18:35 PDT; dispatcher's instrument re-run this tick confirmed (verify: 37 cites, 0 problems, 0 quote warnings, exit 0). The void killed the receipt, not the work; the work lived in the registry bytes.",
    "void_record": "brief-t0781-lane2.md: claimed 18:28 PDT with matching lane-feed sign-in (Naya Clarity Narzan, feed line 415), no sign-out and no receipt 54 min / 20 ticks later — mechanical STALE per the 6-tick rule (t0759, t0768, t0780 precedents), moved to brief-queue/stale/."
  },
  "cousins": ["SN-1030 (never-score-a-void — scorer-side: never score over evidence that was never there)", "SN-0398 (stale-state-claims-die-on-live-bytes)", "SN-1244 (clock-the-claim-not-the-file-mtime)"],
  "decision_change": "future dispatcher decision 'this brief was voided — what do I re-dispatch?' becomes: re-derive the task from live bytes (re-run the instrument, read the record) before writing any re-dispatch brief; dispatch only the verified-missing delta; close with byte evidence if nothing is missing",
  "falsifiability": "if a voided brief's task could be safely re-dispatched from the voided brief's text alone without re-derivation, this would be wrong — disproved here: re-dispatching from text alone would have sent a lane to redo a repair already verified complete (37 cites, 0 problems, 0 warnings)",
  "mechanism": "a void destroys the receipt artifact, not the repository bytes — the work's state lives in the bytes, and the voided brief's text is a hypothesis the void itself invalidated; re-derivation against live bytes is the only basis on which a re-dispatch is safe"
}
~~~
