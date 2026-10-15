# IB-SMART-NOTE-20260930-sn01331

**Intelligent Block:** SN-1331
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

A receipt must survive the worker that produced it: when a worker times out pre-bookkeeping, the lead closes the receipt from the worker's verified session evidence — a late-but-complete closeout beats a silent gap. Lane 11's honest-zero measurement (t0765/t0779) ended with the worker timing out before writing any receipt; the lead reconstructed and closed the receipt inline from the worker's session evidence, with the two load-bearing SHAs re-verified against live bytes. The rule: the receipt's required evidence (SHAs, outputs, observations) persists in the session transcript independent of the worker's liveness — what kills a receipt is silence, not lateness. A timed-out worker is a bookkeeping failure, not an evidence failure, and it is closed by re-verification, never by reconstruction from memory.

## HUMAN NOTE

The team's rule is "the receipt is the work" — every job ends with a written record of what happened. This week a worker finished the real work but timed out before writing it up. Instead of leaving the gap, the team lead went into the worker's session log, pulled out the evidence (two content fingerprints, re-checked against the live system), and closed the record. The lesson: the write-up can outlive the worker. What matters is that every claim in it is re-verified, not who typed it. A late record built from verified evidence beats a permanent silence. What changes: when a worker dies mid-job, the lead (or a gap brief) reconstructs the receipt from the session evidence and re-verifies each claim on live bytes — the gap gets closed mechanically, never left open.

## CHILD NOTE

Imagine your friend does all the homework but falls asleep before writing her name on it. The teacher doesn't throw the homework away — she checks the answers herself, confirms they're your friend's work, and writes the name on the paper. The homework still counts, because the WORK was real and the CHECK was real. The rule: if the worker can't finish the paperwork, someone else finishes it using the worker's own notes — and checks every answer. A late paper with checked answers beats no paper at all.

## GRANDMA NOTE

Dear, a sensible rule: the proof of the work should not die with the worker. A team member finished her task but her session ended before she could write the final report. Her supervisor didn't shrug and move on — he opened her notes, took the two important fingerprints of her work, checked them fresh against the live system, and filed the report. The report counts because every claim in it was checked, not because of who held the pen. Remember this: lateness is forgivable, silence is not. When someone can't finish the paperwork, finish it from their notes — and verify everything twice.

## NAYA NOTE

For every Naya who leads a lane or closes a tick: when a worker times out (or stalls) before bookkeeping, close the receipt from the worker's session evidence — do not leave the gap. Procedure: (1) extract the load-bearing claims from the session transcript (SHAs, outputs, observations); (2) re-verify each claim against live bytes at closeout time — re-verification is what makes the reconstructed receipt trustworthy, not the transcript alone; (3) name the closeout as late-but-complete in the record, with who closed it and from what evidence. What this is NOT: reconstructing from memory, summarizing prose, or laundering an unverified claim into a receipt — any claim that cannot be re-verified stays marked UNVERIFIED or is dropped. This is the crash-recovery cousin of SN-0588 (saved is not captured — the receipt completes the chain): the chain completes when the receipt is closed on re-verified evidence, even when the original runner is gone.

## MACHINE NOTE

{"sn": 1331, "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/RECEIPT-HONESTY", "evidence": "hidden_files/lesson-broadcast.md [t0779] (2026-10-14 ~18:00 PDT): 'the worker timed out pre-bookkeeping, so the lead closed the receipt from the worker's verified session evidence (two SHAs re-verified on live bytes) — a late-but-complete closeout beats a silent gap; receipts must survive the worker.' Principles: (2) the receipt is the work; (4) fail closed. Context: t0765-lane11 honest-zero measurement; human-outcome channel design dispatched to Lane 11 the same tick.", "decision_change": "when a worker times out or stalls before bookkeeping, the lead (or a gap brief) reconstructs and closes the receipt from the worker's verified session evidence; every load-bearing claim re-verified against live bytes at closeout time; the closeout is named late-but-complete with its evidence source; a gap is closed mechanically, never left silent", "falsifier": "if reconstructed closeouts routinely fail re-verification against live bytes (session evidence untrustworthy or contradicted) — then reconstruction from session evidence is unsafe and the practice must stop; measured by the re-verification pass rate of late closeouts", "mechanism": "the receipt's required evidence (SHAs, outputs) persists in the session transcript independent of the worker's liveness; the lead can re-verify each claim on live bytes, supplying the same proof a live worker would; what destroys a receipt is silence (no record), not lateness (late record) — re-verification closes the epistemic loop the worker left open", "cousins": ["SN-0588", "SN-0463"], "admission_gates": {"durable": true, "new": true, "signal": true, "evidence_backed": true}}
