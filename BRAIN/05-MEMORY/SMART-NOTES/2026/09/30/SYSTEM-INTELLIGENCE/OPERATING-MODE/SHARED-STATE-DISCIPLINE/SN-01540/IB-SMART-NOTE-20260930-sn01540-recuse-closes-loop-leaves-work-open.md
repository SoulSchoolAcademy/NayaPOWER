# IB-SMART-NOTE — SN-1540

**Intelligent Block:** YES
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-17
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Category:** SYSTEM-INTELLIGENCE/OPERATING-MODE/SHARED-STATE-DISCIPLINE

## IN A NUTSHELL

A RECUSE receipt is a closed loop with open work: it closes the dispatch loop (the seat steps back) but the work stays OPEN — on disk, off rotation, eligible for a non-barred seat. The t0599 and t0602 reconcile ticks handled two such receipts by dequeuing the rotation entry while leaving the brief file OPEN on disk, then re-reading the rotation write to byte-verify it landed in the same tick — honoring the t0581 never-landed precedent (intent is not landed bytes). If the queue-removal and the on-disk-OPEN pairing do not survive the rotation write together, the brief either vanishes from pull (lost work) or lingers in rotation as a phantom (blocking). Either way the queue lies.

## HUMAN NOTE

When a volunteer recuses from a task, you take their name off the sign-up sheet — but the task itself goes back on the board for someone else, and you double-check the board before you leave the room. If you forget to erase the name, nobody can take it; if you lose the card, nobody sees it.

## CHILD NOTE

If you can't play your turn, you tell the group "I'm out for this round" — and you put the card back on the table for someone else. Then you look at the table to make sure the card is really there. Just saying it isn't enough.

## GRANDMA NOTE

When someone steps back from a chore, dear, you cross their name off the list — but the chore goes back on the board, and you check the board before you leave. A chore erased from everywhere is a chore never done.

## NAYA NOTE

Future Naya (dispatch reconcile): on a RECUSE receipt — dequeue the rotation entry AND leave the brief file OPEN on disk for an eligible non-barred seat, in the same tick; then re-read the rotation write to byte-verify both landed. The t0581 never-landed precedent governs: a rotation write is not landed until re-read. The standing rotation-disk diff tripwire catches any pairing that broke: a brief on disk with no rotation entry and no receipt is orphaned work; a rotation entry with no live file is a phantom. Cite the brief by FULL FILENAME — the t0557 collision lesson.

## MACHINE NOTE

```json
{
  "sn": "SN-1540",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured_utc": "2026-10-17T08:20:00Z",
  "applies_when": [["dispatch","reconcile"],["recuse","queue"],["rotation","write-integrity"],["brief","claim"]],
  "enforcement": "on any RECUSE receipt, the reconcile tick dequeues the rotation entry + leaves the brief file OPEN on disk in the same tick, then re-reads the rotation write to byte-verify both landed; the standing rotation-disk diff flags any broken pairing (orphaned brief = work lost; phantom entry = queue lies); cite briefs by FULL FILENAME (t0557)",
  "evidence": [
    "lesson-broadcast.md t0599/t0602 (2026-10-17 ~06:03-06:08Z): RECUSE receipts closed the dispatch loop and left work OPEN on disk (brief-t0562-lane12, brief-gap-t0413-lane3); rotation writes byte-verified on re-read per the t0581 never-landed precedent",
    "t0581 precedent: a rotation write that never landed -> queue lied until the re-read check"
  ],
  "falsifiable_by": "many ticks of RECUSE handling with no same-tick re-read and zero broken pairings — would prove the extra verification is cost without benefit",
  "mechanism": "the rotation is the single source of truth for pull; intent != landed bytes, so the pairing is only real once the write is re-read; the disk diff makes any break visible"
}
```
