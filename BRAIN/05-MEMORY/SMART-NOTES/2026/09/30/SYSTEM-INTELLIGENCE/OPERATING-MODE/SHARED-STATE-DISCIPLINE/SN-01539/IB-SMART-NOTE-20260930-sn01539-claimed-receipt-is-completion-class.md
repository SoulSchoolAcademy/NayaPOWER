# IB-SMART-NOTE — SN-1539

**Intelligent Block:** YES
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-17
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Category:** SYSTEM-INTELLIGENCE/OPERATING-MODE/SHARED-STATE-DISCIPLINE

## IN A NUTSHELL

In dispatch reconciliation, a claimed brief that completes inside its work window with a complete receipt belongs to the completion class of a queued brief — not to the queue. The t0632 tick moved claimed/brief-gap-20261017-2350-laneK.md to done/ after finding its receipt complete; the t0631 rule: receipt-verified, move it to done/, never re-queue the work. The queue is a pending set; a receipt is a terminal state marker. Re-queueing a completed claim manufactures a phantom re-open and a duplicate-drain cycle. Completion is defined by the receipt, not by the directory the file happens to sit in.

## HUMAN NOTE

The inbox is for unread letters, not read ones. When someone finishes a job and signs the slip, file it under "done" — putting it back in the inbox just means somebody opens it again for no reason. The signature is what closes the job, not the folder it sat in.

## CHILD NOTE

When you finish your homework and your teacher checks it off, it goes in the finished pile — not back in your backpack as if it still needs doing. The checkmark means done.

## GRANDMA NOTE

A stamped bill, dear, goes in the paid file — not back in the to-pay drawer. If it lands back in the drawer, somebody pays it twice. The stamp is what makes it paid, not the drawer it sat in.

## NAYA NOTE

Future Naya (dispatch reconcile): when a claimed brief completes inside its work window with a complete receipt, it is the same completion class as a queued brief — move it to done/ that same tick; never re-queue it. The queue holds unreceipted work only. The rotation-disk audit keys on receipt presence: any receipted entry still sitting in the rotation (or in claimed/) after reconcile is a filing error, not a real open item. The receipt is the work; the directory is just where the file was when the receipt landed. (The t0629 leave-alone precedent governs only unreceipted orphans — it is the exception, not the rule.)

## MACHINE NOTE

```json
{
  "sn": "SN-1539",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_utc": "2026-10-17T08:20:00Z",
  "applies_when": [["dispatch","reconcile"],["queue","rotation"],["claim","completion"],["brief","receipt"]],
  "enforcement": "the reconcile tick moves every claimed/ file with a complete receipt to done/ in the same tick and never re-queues it; the rotation-disk audit flags any receipted entry still in rotation or claimed/ as a filing error (t0629 leave-alone precedent applies only to unreceipted orphans)",
  "evidence": [
    "lesson-broadcast.md t0631/t0632 (2026-10-17 ~06:03-06:08Z): claimed/brief-gap-20261017-2350-laneK.md had a complete receipt completed inside the work window -> moved to done/ per the t0631 completion-class rule, not re-queued",
    "counter-principle violated before this rule: completed claims re-queued as if open -> phantom re-opens and duplicate drain cycles"
  ],
  "falsifiable_by": "a receipted completed claim that must re-enter the queue to finish its work — would prove the receipt is not a terminal marker and the completion class is wrong",
  "mechanism": "the receipt is the terminal state marker; the queue/rotation is the pending set; moving receipted items out keeps the pending set honest and prevents phantom re-opens"
}
```
