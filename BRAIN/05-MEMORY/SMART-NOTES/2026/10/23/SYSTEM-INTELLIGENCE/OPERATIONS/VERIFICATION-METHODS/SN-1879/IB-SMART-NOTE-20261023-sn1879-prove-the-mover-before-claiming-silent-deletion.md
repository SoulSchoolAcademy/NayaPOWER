Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-23
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

The 14:20Z learning event framed ~6–7 unclaimed brief-*.md files leaving the brief queue as "silently vanished ... a deletion outside the claim protocol with no record of who or where" (13:03:48Z; no mv into claimed/, done/, archived/, stale/, or superseded/; no receipts, no feed entries). The 15:20Z review corrected the framing: the mover was proven four ways — (1) the ctime pin: all six files' ctimes in a 16ms batch at 13:03:48.801–817Z; (2) the run summary's own confession: the t1415 dispatcher "reconcile" (run 6f86273f, 13:02–13:04Z) retired the six gap briefs (brief-gap-t1192-lane2, t1286/t1295-lane4, t1296/t1305-lane11, t1310-lane3) on "existing receipts" — but no receipt's Brief: line exact-names any of the six, making the retire premature by the t1074 exact-name bar; (3) the memory log; (4) the lesson-broadcast mirror at the exact second. Every alternative mover was excluded: zero sign-ins in the hour, both retire scripts exonerated. The lesson: a "silent deletion" claim must survive the mover check before it stands. When independent witnesses agree on the mover, the anomaly is a disputed action, not a mystery deletion — and the remedy differs: a disputed action is owed restore-or-accept-with-named-drops; a true mystery is owed SN-1873's write-audit trail. Mystery and dispute are different incident classes; the mover check is what tells them apart.

## 🩷 HUMAN NOTE

Shawn — yesterday's learning event said six queue files had "silently vanished" with no trace of who took them. An hour later the review corrected that: there WAS a trace, four of them. The files' timestamps all changed in the same 16 milliseconds, the dispatcher's own run summary said it retired those exact files, and the memory log plus the broadcast mirror agreed to the second. Nobody signed in that hour, and both cleanup scripts were cleared. So it wasn't a mystery deletion at all — it was a disputed retirement, done too early on grounds that didn't hold up. The lesson: before calling something a "silent" mystery, run the mover check — timestamps, run summaries, logs, mirrors. If they agree on who moved the files, you don't have a mystery, you have a dispute, and disputes get fixed differently than mysteries (you restore the files or formally accept the loss by name, instead of building an audit trail for a ghost).

## 🟣 CHILD NOTE

Imagine six toys disappear from the toy box, and someone shouts "a ghost took them!" But then you check: the security camera shows all six toys picked up in the same two seconds, your brother's diary says "I cleaned up six toys," and the house log agrees. It wasn't a ghost — it was your brother, and he threw away toys he shouldn't have. The lesson: before you say "ghost," check the cameras, the diary, and the log. If they all point to the same person, there's no ghost — there's a disagreement to fix. Ghosts and brothers need different solutions.

## 🔵 GRANDMA NOTE

Honey, it's simple: don't cry "thief in the night" until you've asked the household. Six files went missing, and the first report said nobody knew who took them. But the timestamps, the dispatcher's own notes, the memory log, and the broadcast all pointed to the same mover in the same minute. It wasn't a mystery — it was a mistake, a retirement done too early. Mysteries need detective work; mistakes need fixing. The lesson is to tell them apart BEFORE you sound the alarm: check the four witnesses first.

## 🟠 NAYA NOTE

This is claim discipline for incident response, and it is load-bearing because the two incident classes demand different remedies. A "silent deletion" claim without a mover check routes the system toward mystery machinery (audit trails, watches); a "disputed action" claim routes it toward adjudication (restore-or-accept-with-named-drops). The t1415 case shows the cost of the wrong class: the 14:20Z framing said "deletion outside the claim protocol with no record of who or where," which is false on the record — the mover was proven four ways, and the actual defect was a premature retire on unscoped "existing receipts" (no receipt's Brief: line exact-names any of the six; t1074 exact-name bar; same premature-dequeue class as the t992 incident). The four witnesses — ctime batching, run-summary confession, memory log, broadcast mirror — are independent: agreement across them identifies the mover without trusting any single one, and disagreement across them is itself the signal of a true mystery. The decision this changes: the next queue-integrity anomaly gets the mover check before any "silent" framing is announced. The method grades itself — if any leg fails, the claim is "mover unproven," not "proven."

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn-1879-prove-the-mover-before-claiming-silent-deletion",
  "lesson": "A 'silent deletion' claim must survive the mover check before it stands. The 14:20Z learning event framed ~6-7 unclaimed brief-*.md files leaving the brief queue as 'silently vanished ... a deletion outside the claim protocol with no record of who or where' (13:03:48Z). The 15:20Z review corrected the framing: the mover was proven four ways — (1) ctime pin: all six files' ctimes in a 16ms batch at 13:03:48.801-817Z; (2) the run summary's own confession: the t1415 dispatcher 'reconcile' (run 6f86273f, 13:02-13:04Z) retired the six gap briefs (brief-gap-t1192-lane2, t1286/t1295-lane4, t1296/t1305-lane11, t1310-lane3) on 'existing receipts' — but no receipt's Brief: line exact-names any of the six, making the retire premature by the t1074 exact-name bar (same premature-dequeue class as the t992 incident); (3) the memory log; (4) the lesson-broadcast mirror at the exact second. Every alternative mover excluded: zero sign-ins in the hour, both retire scripts exonerated. When independent witnesses agree on the mover, the anomaly is a disputed action, not a mystery deletion — and the remedy differs: a disputed action is owed restore-or-accept-with-named-drops; a true mystery is owed SN-1873's write-audit trail. Mystery and dispute are different incident classes; the mover check is what tells them apart.",
  "applies_when": ["incident", "claim-discipline", "queue", "integrity", "verification", "methods", "anomaly", "framing", "deletion", "attribution"],
  "enforcement": "A 'silent deletion' learning event must name the mover-check legs (ctime range, run summary, memory log, broadcast mirror) and each leg's result before the 'silent' framing stands; an event that skips the mover check is bounced as unproven framing. If the legs disagree or no mover is found, the class is MYSTERY and SN-1873's write-audit trail is the remedy; if they agree, the class is DISPUTE and restore-or-accept-with-named-drops is owed.",
  "evidence": ["hidden_files/learning-events-2026-10-23-14.md (14:00 PDT hour: the 'silently vanished' framing)", "hidden_files/learning-events-2026-10-23-15.md (15:00 PDT hour: framing corrected, mover proven four ways, alternatives excluded)", "hidden_files/twelve-lane-receipts/gap-seat-stall-20261023-0637-lane0.md (VIOLATION LOG entry: premature retire on unscoped receipts, t1074 exact-name bar)", "hidden_files/twelve-lane-receipts/seat-stall-20261023-0637.md (original queue-delta observation)"]
}
```
