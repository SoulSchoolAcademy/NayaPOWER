Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-23
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

night-dispatcher t1427 (2026-10-23 15:28Z) repaired the t1415-class premature retire at the root: the retire gate fires ONLY on an exact `Brief:` line naming the brief — filename SIMILARITY is not a trigger. t1415's mover ran a looser standard than the gate demands: a receipt whose brief-tNNNN-laneN.md filename "matched" the queued brief-gap-tNNNN-laneN.md counted as its execution — but the t1351/t1074 exact-name bar requires the receipt's `Brief:` line to exact-name the queued file. Six gap briefs (t1192-lane2, t1286/t1295-lane4, t1296/t1305-lane11, t1310-lane3) were retired to done/ on receipts that exact-name none of them. The repair has two edges. First: retire is a claim — the same exact-name bar that governs claims governs retirements, and the mover is held to the gate's criterion, not its own judgment ("The exact-name bar applies to retirements, not just claims"). Second: when dequeuing, name the exact brief filename — t1415's rotation-removal used brief-t1420-lane2.md where the queued file was brief-gap-t1420-lane2.md, a wrong-name removal that corrupts the rotation record. The lesson: retirement is a claim that the retirement criterion was met, and the claim is proven the same way every other claim is — an exact name in a receipt's `Brief:` line. Similarity is judgment; the gate runs on names. Sibling: SN-1875 (disputed retire → restore, never ratify) settled the response; this settles the firing condition.

## 🩷 HUMAN NOTE

Shawn — the retirements that went wrong this morning were retired because the filenames "looked close enough." A receipt for brief-t1420-lane2 was counted as the execution of brief-gap-t1420-lane2 — similar name, different brief. That's not evidence; that's judgment wearing evidence's clothes. The repair, now standing: a brief is only retired when a receipt's Brief: line names it exactly — the same exact-name rule that governs claims. And when something is removed from the queue, the removal must name the exact filename, because a near-miss name silently corrupts the rotation record. The one-line version: the gate fires on names, never on resemblance.

## 🟣 CHILD NOTE

Imagine the teacher says "pack up the books named on the list." Six kids pack up books that aren't on the list — because the names looked similar. "Dragon Tales" is not "Dragon's Tale." That's how a whole shelf got cleared by mistake. The fix is simple and strict: the list says the exact name, and you only pack a book when its exact name is on the list. Close doesn't count. And when you write down what you packed, you write the exact name — because "close enough" on paper makes the next person pack the wrong thing again.

## 🔵 GRANDMA NOTE

Honey, it's an old office lesson. Someone filed away six folders because the folder names "looked about right" — but "about right" isn't a filing system. The repair is the filing rule stated once and kept: you only retire a file when a receipt names it exactly, letter for letter. And when you pull something out of the rotation, you write down the exact name of what you pulled — because a near-miss name on paper becomes the wrong file pulled next time. Names are the gate. Resemblance is not.

## 🟠 NAYA NOTE

This is the prose→code instance of the exact-name doctrine applied to the retire action class. SN-1875 settled the response (disputed retire → restore, never ratify); this settles the firing condition. The mechanism of the t1415 failure is structural, not carelessness: verdict tables in parent receipts name parent briefs (brief-tNNNN-laneN.md), so a stem-match on a gap brief (brief-gap-tNNNN-laneN.md) will always find "receipts" that are about something else — SN-1879's Twin A parenthetical proved exactly this (substring hits are old verdict tables naming parent briefs, not executions). So the repair is load-bearing, not cosmetic: similarity cannot be a retire trigger because similarity matches the wrong class of record. The decision this changes: any seat deciding whether a brief is retired checks for an exact `Brief:` line naming the queued file — no exceptions, no judgment calls — and dequeues by exact filename. Carry for cold successors: when a retire log cites "existing receipts" without exact names, the retirement is premature by construction.

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn-1881-retire-fires-only-on-exact-brief-naming",
  "lesson": "The retire gate fires ONLY on a receipt whose Brief: line exact-names the queued brief — filename SIMILARITY is not a trigger. t1415's mover ran a looser standard than the gate demands: a receipt's brief-tNNNN-laneN.md filename 'matching' the queued brief-gap-tNNNN-laneN.md counted as execution, violating the t1351/t1074 exact-name bar. Six gap briefs (t1192-lane2, t1286/t1295-lane4, t1296/t1305-lane11, t1310-lane3) retired to done/ on receipts that exact-name none of them — premature retire, t992 class (reversed by t1427 restore). Second edge: dequeuing must name the exact brief filename — t1415's rotation-removal used brief-t1420-lane2.md where the queued file was brief-gap-t1420-lane2.md, a wrong-name removal that corrupts the rotation record. Retirement is a claim and carries the claim's exact-name bar; similarity is judgment, and the gate runs on names. The substring trap is structural: verdict tables in parent receipts name parent briefs, so stem-matches on gap briefs always find receipts about something else (SN-1879 Twin A parenthetical).",
  "applies_when": ["dispatch", "brief-retirement", "reconciliation", "queue", "guard", "claim-discipline", "rotation"],
  "enforcement": "A retirement fires ONLY on a receipt whose Brief: line exact-names the queued brief file (t1351/t1074 bar). The retire path runs receipt-briefcheck.py (hidden_files/bin/) or its successor: a brief with zero exact-name receipts is NOT retired — any retire on filename similarity is a t992-class premature-retire breach, owed restore (SN-1875). Dequeue operations must name the exact queued filename; a removal logged under a non-exact name is rejected by the rotation-removal check. The t1415 one-liner's own scan (0/30 exact-name → nothing dequeued) is the gate that held — the repair makes it explicit.",
  "evidence": ["hidden_files/lesson-broadcast.md ([night-dispatcher t1427] RETIRE-RULE REPAIR entry)", "hidden_files/learning-events-2026-10-23-16.md (16:00 UTC hour: CANDIDATE 864, premature retire reversed 15:28:21Z)", "hidden_files/twelve-lane-receipts/gap-lane-scorer-20261023-0820-lane0.md (all six restored to queue root, 9.5, scope held)", "hidden_files/bin/receipt-briefcheck.py (t1426-lane4: NO-Brief / BRIEF-ORPHAN instrument, 1587-receipt live demo: 1575 NO-Brief, 0 BRIEF-ORPHAN, 12 VALID)"]
}
```
