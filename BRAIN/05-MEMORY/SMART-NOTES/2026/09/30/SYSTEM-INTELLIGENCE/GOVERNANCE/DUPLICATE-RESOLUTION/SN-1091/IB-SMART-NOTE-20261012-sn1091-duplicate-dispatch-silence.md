# Duplicate Dispatch of a Closed Slot Writes Nothing — Silence Is the Correct Output

**Intelligent Block:** IB-SMART-NOTE-20261012-sn1091-duplicate-dispatch-silence
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-12 ~08:08 PDT
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Filed by:** smart-note-distillation loop (08:38 PDT tick, inline review).
**Provenance:** 🧠 LEARNING EVENT, distillation window 2026-10-12T14:04:36Z → 15:04:35Z, board #2175 comment 6126971594 (2026-10-12 15:06:37Z): "L25 (WIN-PATTERN) — Duplicate dispatch of a closed slot writes nothing: no claim, no sign-out, no venue post — only a deconfliction note in the lane's own log. A duplicate dispatch's correct output is silence." Corroborated by ⚡ INTELLIGENT EVENT comment 6126974095, adoption #6: "L25 lived before it was filed (verify, 14:39Z): a duplicate dispatch stood down to total silence on a closed slot."

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

At 14:39Z a duplicate dispatch found its slot already closed behind the live 14:30 sibling receipt — and it did exactly the right thing: nothing. No claim, no sign-out, no venue post. Just a deconfliction note in its own log, and silence everywhere else. This is L25, filed as a WIN-PATTERN because the instinct runs the other way: a spawned worker wants to justify its existence, to report, to touch something. But a duplicate dispatch is a second actor on an occupied slot — anything it writes to shared surfaces is contamination: a competing claim splits ownership, a sign-out overwrites the real lane's receipt, a venue post confuses the record. **The correct output of a duplicate dispatch is silence.** Zero residue is the success signal, not a missing deliverable. The only permitted artifact is a private deconfliction note in the lane's own log, so the duplicate-dispatch root cause can be traced upward without polluting shared state. Paired with SN-1090 (dead-claim timeout): SN-1090 tells you when a claim is dead; SN-1091 tells you what the duplicate must do about it — nothing.

## 🩷 HUMAN NOTE

Shawn, a small win-pattern from this morning's learning window, now in AGENTS.md as L25: when a dispatch turns out to be a duplicate — its slot already closed behind the real lane's receipt — the right move is total silence. No claim, no sign-out, no board post. At 14:39Z a duplicate dispatch did exactly this on a closed slot: just a private deconfliction note in its own log, zero residue everywhere else. The instinct to report would have been contamination — a competing claim splits ownership, a sign-out overwrites the real lane's receipt. Silence is the deliverable here, and zero residue is the success signal.

## 👶 CHILD NOTE

Imagine you and your friend both get told to tidy the same room. You arrive and see your friend already finished it — everything is clean. What do you do? You don't start tidying again (you'd mess it up!), you don't announce "I tidied the room" (that would be a lie — your friend did it). You just quietly leave a note for yourself — "the room was already done" — and walk away silently. Doing nothing on purpose IS the right thing when someone already did it.

## 👵 GRANDMA NOTE

Dear, the team sometimes sends two workers to the same job by mistake — a duplicate dispatch. This morning one arrived at 14:39Z to find the job already done by the 14:30 worker. Now, the natural instinct is to announce yourself, file a report, do *something*. But anything it says out loud causes harm: a second claim confuses who owns the work, a second sign-out buries the real worker's receipt, a post on the board muddies the record. So the standing rule, L25: the duplicate stands down to complete silence. The only thing it may leave is a private note in its own log — "arrived, slot already closed" — so we can fix the dispatch mix-up that sent it there, without any trace on the shared record.

## 🧠 NAYA NOTE

Cold successor: a duplicate dispatch (same slot dispatched twice — verify by checking the lane's claim log / sign-out receipts before writing anything) must emit zero shared-surface artifacts: no claim, no sign-out, no venue/board post, no PR comment, no comment edit. The only permitted write is a deconfliction note in the lane's OWN log ("duplicate dispatch, slot closed behind live receipt at <time>"), which exists solely to let the duplicate-dispatch root cause be routed upward (see SN-1090). "Did nothing" from a duplicate dispatch is a WIN, not a missed deliverable — score it as correct behavior. The failure mode it prevents: competing claims splitting ownership, sign-outs overwriting the live lane's receipt, venue posts confusing the record. F4 DECONFLICTION-SKIP (~7 instances) is nearly learned; this rule makes the correct behavior mechanical even when deconfliction is skipped at dispatch time.

## 🤖 MACHINE NOTE

```json
{
  "rule": "a duplicate dispatch of a closed slot writes nothing to shared surfaces; silence is the correct output",
  "detection": "check lane claim log / sign-out receipts before any write; slot already closed behind a live sibling receipt",
  "forbidden": ["claim", "sign-out", "venue/board post", "PR comment", "comment edit"],
  "permitted": "one deconfliction note in the lane's own log (root-cause traceability only)",
  "success_signal": "zero residue on shared surfaces",
  "prevented_failure": "competing claims split ownership; sign-outs overwrite the live lane's receipt; venue posts confuse the record",
  "sibling": "SN-1090 (dead-claim timeout: how to detect the dead claim); F4 DECONFLICTION-SKIP (~7 instances, nearly learned)",
  "evidence": "#2175 comment 6126971594 (2026-10-12T15:06:37Z), L25 win-pattern; #2175 comment 6126974095 adoption #6: verify lane 14:39Z stood down to total silence on a closed slot",
  "promotion": "appended to AGENTS.md under 'Distilled lessons — 2026-10-12 15:04Z batch (distillation v2)'"
}
```
