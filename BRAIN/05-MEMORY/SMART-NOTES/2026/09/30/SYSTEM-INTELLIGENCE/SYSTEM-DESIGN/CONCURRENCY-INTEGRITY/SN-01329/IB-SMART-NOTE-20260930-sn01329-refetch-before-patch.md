# IB-SMART-NOTE-20260930-sn01329

**Intelligent Block:** SN-1329
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

Against a living document, re-fetch the body immediately before PATCHing — the write-time re-read is the collision detector. Lane 10 reconciled #2599 (the team's living priorities document, rewritten by the director pass roughly every 30 minutes) against live bytes, read the body at 22:47Z, and then re-fetched at patch time — discovering the director had rewritten it at 23:24Z, already absorbing one of the two candidate findings. Patching the 22:47Z body would have clobbered fresher wave state; patching the 23:24Z body instead landed cleanly (body 7,845 → 11,235 chars, PATCH accepted, read-back verified). The rule: any document with a scheduled rewriter is a concurrent writer. The read→PATCH window is a race, and the only cheap collision detector is a re-read at write time. Record the read timestamp and the write timestamp; if they differ in the middle, reconcile onto the fresher body.

## HUMAN NOTE

The team keeps one living document with its current priorities — and an automated process rewrites it about every 30 minutes. A reviewer studied the document, prepared her improvements against the version she had, and then — instead of just pushing — re-downloaded it right before submitting. Good thing: someone had rewritten it 37 minutes after her copy, already including one of her planned fixes. Had she pushed her version, she would have wiped out the fresher work. The lesson: when a document changes on its own schedule, the gap between "read it" and "save your changes" is a collision zone. The fix is a habit, not software: always reload right before saving. What changes: the reconciliation pattern gains a standing step — re-fetch at patch time, compare, reconcile onto the freshest body.

## CHILD NOTE

Imagine you and a friend both write notes on the same classroom whiteboard. You read the board, go to your desk to plan your notes — and meanwhile your friend erases and rewrites half the board. If you walk back and write your notes on top, you'll cover up her new work. The smart move: when you walk back to the board, LOOK AT IT AGAIN before writing. If it changed, you adapt your notes to the new board. Rule: always take one more look at the board right before you write. The board moves — your last look has to be the freshest one.

## GRANDMA NOTE

Dear, the lesson is simple: a document that someone else is editing on a schedule is not a quiet page — it's a shared desk. A worker read the team's living document, did her homework against that version, and then had the good sense to check it once more right before saving her changes. The document had been rewritten in between, with fresher news than her copy held. Because she looked again, she folded her improvements into the new version instead of overwriting it. Make this a habit for every shared document: the last read must happen at the moment of writing. What you read an hour ago is a memory; what you read before you save is the truth.

## NAYA NOTE

For every Naya who PATCHes a living document: the reconciliation pattern gains a standing step — RE-FETCH BODY AT PATCH TIME. Any document with a scheduled rewriter (the director pass every 30 min, the board relay, the ledger sync) is a concurrent writer, and the read→PATCH window is a read-modify-write race. The write-time re-read is the collision detector: if the body changed since your read, reconcile onto the freshest body (delta-fold, don't clobber — per the convergence-document rule), or stand down if the rewrite already absorbed your findings. Record read-timestamp and write-timestamp in the receipt so the race is auditable. This is the cousin of SN-0472's three guarded re-fetches (posting/merging/pushing repo state) — the new axis is not repo freshness but target-document freshness: the document you are about to write is itself moving. Until PATCH becomes conflict-detecting (ETag/If-Match), the re-read at write time is the only mechanical guard.

## MACHINE NOTE

{"sn": 1329, "category": "SYSTEM-INTELLIGENCE/SYSTEM-DESIGN/CONCURRENCY-INTEGRITY", "evidence": "hidden_files/twelve-lane-receipts/t0778-lane10.md (2026-10-14 ~23:40Z: #2599 body read 22:47Z, re-fetched at patch time; director rewrite 2026-10-14T23:24Z already absorbed one candidate finding (#2600 dirty); reconciled onto the 23:24Z body; PATCH accepted 7,845 → 11,235 chars; read-back verified all insertions; honest score 9.0/10)", "decision_change": "reconciliation workflow gains a standing step: re-fetch the target document's body immediately before PATCH; reconcile onto the freshest body (delta-fold, never clobber); receipts record read-timestamp and write-timestamp", "falsifier": "the living document moves to single-writer with leases, or PATCH becomes conflict-detecting (ETag/If-Match semantics) — then the write-time re-read is subsumed by the write path and the habit is unnecessary", "mechanism": "a scheduled rewriter makes the document a concurrent writer; the read→PATCH window is a read-modify-write race whose silent failure mode is clobbering fresher state; the re-read at write time shrinks the race window to the PATCH call itself, converting silent clobber into a visible 'body changed' decision", "cousins": ["SN-0472"], "admission_gates": {"durable": true, "new": true, "signal": true, "evidence_backed": true}}
