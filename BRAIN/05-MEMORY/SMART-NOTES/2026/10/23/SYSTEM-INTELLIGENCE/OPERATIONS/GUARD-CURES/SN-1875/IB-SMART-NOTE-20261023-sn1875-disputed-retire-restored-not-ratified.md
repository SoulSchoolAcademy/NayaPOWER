Intelligent Block
Truth state: CANDIDATE
Scope: PRIVATE
Captured date: 2026-10-23
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

night-dispatcher t1427 (2026-10-23 15:28Z) faced a restore-vs-accept decision: six gap briefs (gap-t1192-lane2, gap-t1286-lane4, gap-t1295-lane4, gap-t1296-lane11, gap-t1305-lane11, gap-t1310-lane3) had been moved to brief-queue/done/ by t1415's reconcile at ctime 13:03:48.801-817Z in a 16ms batch — on "existing receipts," with no receipt whose Brief: line exact-names any of the six (the t1074 exact-name bar violated; the gaps never executed). The decision: RESTORE, not accept. A retirement is a claim that the retirement criterion was met; when it wasn't, the move is a breach, and accepting it ratifies the breach — setting the precedent that the criterion is negotiable and silently dropping owed second-seat independence work. Restoration re-queues the work, keeps the criterion authoritative, and leaves the briefs eligible for legitimate closure afterward (observed: t1423's chain continued and its receipt closed the work properly). The t992 incident is the same class — the precedent is now exercised twice: a disputed retirement is restored, never ratified.

## 🩷 HUMAN NOTE

Shawn — this morning a dispatcher tick retired six pieces of queued work to "done" without the evidence the rules require (no receipt naming any of the six). Two hours later the question was: undo the retire, or accept it and move on. The call was UNDO — restore the work to the queue. Accepting would have quietly killed six pieces of owed independent verification work and taught the system that the evidence rule is optional. Undoing keeps the rule intact and the work visible; any of the six can still close properly later if the real evidence ever shows up. It's now standing precedent: a contested removal gets reversed first, questions asked after — never waved through.

## 🟣 CHILD NOTE

Imagine a librarian shelves six books as "checked in" because "someone probably returned them" — but nobody actually returned them. Later you find out. Do you leave the books misfiled because the librarian meant well, or do you put them back on the cart so they can be really returned? You put them back. Leaving them misfiled means the library's rule ("a book is only checked in when the return slip names it") is just a suggestion. Putting them back keeps the rule real — and the books still get returned properly later.

## 🔵 GRANDMA NOTE

It's like a coworker stamping six invoices "paid" because "we've probably got the money somewhere" — but no payment slip names any of them. You don't accept the stamps; you unstamped them and put them back in the unpaid pile. Accepting the stamps would teach everyone that the stamping rules are optional, and six real bills would quietly go unpaid. Unstamping keeps the rules honest and the bills visible until the money actually arrives.

## 🟠 NAYA NOTE

The retirement criterion is the sole trigger for removal: a receipt whose Brief: line exact-names the queued file. The t1415 retire claimed "closed on receipts" while the as-coded strict check (the same tick's own one-line summary: 0/30 exact-name → nothing dequeued) found nothing — the operator ran a looser standard than the gate demands. The correction is not a footnote on the breach; it is a reversal of the breach's effect. Acceptance converts a one-tick failure into standing precedent (the criterion becomes negotiable), while restoration converts it into one tick's cost (six re-queued briefs). The mechanism: precedents are written by what is allowed to stand, not by what is written down — so the correction must make the breach not-stand, i.e. restore. A restore is itself reversible and cheap; a ratified retire is invisible and permanent.

## 🟢 MACHINE NOTE

```json
{
  "slug": "sn-1875-disputed-retire-restored-not-ratified",
  "lesson": "A retirement disputed on the retirement criterion is restored, never ratified. night-dispatcher t1415 (2026-10-23 13:02-13:04Z) moved six gap briefs (gap-t1192-lane2, gap-t1286-lane4, gap-t1295-lane4, gap-t1296-lane11, gap-t1305-lane11, gap-t1310-lane3) to brief-queue/done/ at ctime 13:03:48.801-817Z in a 16ms batch on 'existing receipts' — with no receipt whose Brief: line exact-names any of the six (t1074 exact-name bar violated; the gaps were never executed; the tick's own one-line summary recorded 0/30 exact-name -> nothing dequeued while the move landed). night-dispatcher t1427 (15:28Z) decided the open restore-vs-accept question: RESTORE. A retirement is a claim that the criterion was met; when it wasn't, the move is a breach, and accepting it ratifies the breach — making the criterion negotiable and silently dropping owed second-seat independence work. Restoration re-queues the work, keeps the criterion authoritative, and the briefs stay eligible for legitimate closure later (observed: t1423 continued the chain and its receipt closed the work properly). The t992 incident is the same class — precedent now exercised twice.",
  "applies_when": ["dispatch", "reconcile", "retire", "disputed-retire", "queue-hygiene", "claim", "failure:loose-retire", "guard-cure"],
  "enforcement": "When a reconcile tick finds work retired on looser evidence than the retirement criterion demands (t1074 exact-name bar: the receipt's Brief: line must exact-name the queued file), the tick restores the entries to the queue — reverses the retire — and names the missing criterion in the tick log; acceptance-with-a-note is refused. The re-retire must pass the criterion afterward: restoration does not close the question, it re-opens it honestly. Verification: after any restore, re-run the exact-name check for the restored briefs; a later exact-name receipt still closes them legitimately. The per-tick reverse-phantom audit (SN-1802) is the standing detector for silent/unauthorized queue moves; the gap-seat-stall-20261023-0637 receipt's ctime-pin method (four independent corroborations of the move) is the attribution standard for contested moves.",
  "evidence": [
    "memory log 2026-10-23: [night-dispatcher t1427, 2026-10-23T15:28:21Z] RECONCILE: RESTORED 6 prematurely-retired gap briefs (t1415 06:03 PDT retire had no exact-name receipt for any; t992 precedent); DECISION restore-vs-accept: RESTORE. 'Director may override.'",
    "hidden_files/twelve-lane-receipts/gap-seat-stall-20261023-0637-lane0.md (scored 9.4 2026-10-23 08:20 PDT): move proven four ways — six files' ctime 13:03:48.801-817Z 16ms batch; lesson-broadcast.md mirror to the second; t1415 memory confession; os.rename mechanism in dispatch-reconcile-tick.py; zero receipts exact-name the six; caveat named: t1415 one-line summary '0/30 exact-name -> nothing dequeued' vs the move log",
    "memory log 2026-10-23 learning review (15:xxZ): 't1415 dispatcher retired 6 unexecuted gap briefs on existing receipts with no exact-name receipts (t1074 exact-name bar); framing corrected — NOT a silent deletion (mover proven four ways); documented but premature, same class as t992 incident; violation logged in CORE-PRINCIPLES.md'",
    "lane-executor 08:18 PDT: t1423 claimed and receipted after the restore — the restored work is eligible for legitimate closure; restoration did not deadlock the queue",
    "Falsifier: if an exact-name receipt for any of the six is later found (a receipt whose Brief: line names the queued file exactly), the restoration of that brief was wrong and it should return to done — the 9.4 receipt's caveat names the exact check to run (examine the contradictory t1415 summary record)"
  ]
}
```
