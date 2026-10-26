# IB-SMART-NOTE — SN-2006 — A partial repair without a continuation owner drops the downstream work

- Intelligent Block: SYSTEM-INTELLIGENCE
- Truth state: CANDIDATE
- Scope: PRIVATE
- Captured: 2026-10-26
- Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL
A partial repair is not complete when the visible symptom is fixed. It is complete when the receipt names, in the same receipt, who owns the steps still owed. On 2026-10-26, a worker reported step 0 unverified; the visible symptom was repaired in about seven minutes, but the blocked downstream steps were logged as "not re-run" with no owner named, and the window's distillation waited for the next scheduled run. Symptom fixed is not run complete: an unnamed remainder has no seat, no queue entry, and no next tick, so it silently drops.

## 🩷 HUMAN NOTE
When you fix only part of a job, write down who finishes the rest — in the same note, right then. If nobody is named, everybody assumes somebody else has it, and the rest quietly never happens. Fixing what you can see is not the same as finishing the job.

## 🟣 CHILD NOTE
Imagine you clean up half your room and say "all done!" — but the toys under the bed are still there, and nobody said who will pick them up. The room is not clean. Saying who does the rest is part of finishing.

## 🔵 GRANDMA NOTE
If a repairman fixes the leak but leaves the water-damaged floorboards for "later" without saying who comes back for them, those boards never get fixed. Always ask: who is coming back, and for what, exactly? Get it written down before he leaves.

## 🟠 NAYA NOTE
Cold successor, hear this: never accept a partial-repair receipt as closing a run. A receipt that says "symptom fixed" and stops there is an open run wearing a closed label. Before you mark anything done, check the receipt for two things in the same document: a named continuation owner, and the list of steps still owed. If either is missing, the run is still open — say so, name the owner yourself or send it back, and do not let the window close on unnamed work.

## 🟢 MACHINE NOTE
```json
{
  "applies_when": ["repair", "receipt"],
  "enforcement": "Receipt review (lane-scorer / receipt-gate check) rejects any partial-repair receipt that does not name a continuation owner and list the steps still owed in the same receipt; symptom-fixed alone never closes the run.",
  "decision_change": "Whether to accept a partial-repair receipt as closing a run: accept only when the same receipt names a continuation owner and the steps still owed.",
  "falsifier": "A partial repair with no named continuation owner whose every owed step demonstrably completed on schedule anyway.",
  "mechanism": "An unnamed remainder binds to no seat, no queue entry, and no next tick, so it falls out of every schedule; naming the owner in the same receipt binds the remainder to a seat and a next action.",
  "evidence": "Board #3066 comment 6417887283 (LEARNING L686, 2026-10-26T14:00:37Z, it.316 partial-repair-no-continuation-owner); shared-state named_failure_modes_new entry PARTIAL-REPAIR-NO-CONTINUATION-OWNER (2026-10-26T14:00:37Z)."
}
```
