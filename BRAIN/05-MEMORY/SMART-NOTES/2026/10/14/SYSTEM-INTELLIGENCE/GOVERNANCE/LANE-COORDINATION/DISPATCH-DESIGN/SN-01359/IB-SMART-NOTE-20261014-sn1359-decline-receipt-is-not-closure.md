# IB-SMART-NOTE-20261014-sn1359-decline-receipt-is-not-closure

**Intelligent Block:** SN-1359
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

A decline receipt is a completed outcome, not a closure. When the pre-claim identity gate fires — a seat discovers the brief asks her to review her own work — she declines, and the brief goes BACK to the queue with a visible gate stamped on it for a non-contaminated seat. The dispatcher does NOT remove declined briefs: removing the brief deletes the obligation, not just the hold. Two standing fixes: (1) claimability gates get stamped on briefs BEFORE claims, so the next seat reads the gate in the brief's first 10 lines before `mv`; (2) the claim block starts with reading the brief's gate lines — never mv-first. This hour it worked as designed: a Clarity seat byte-verified the PR #2591 body's `Seat:` line against live bytes (Naya Clarity Narzan = herself), declined with zero review work, and the brief stayed queued — non-Clarity seats only.

## HUMAN NOTE

A safety rule fired correctly this hour: one of the reviewers discovered she was being asked to review her own work, and refused. The important part isn't the refusal — it's what happened to the work. It wasn't closed, and it wasn't deleted. It went back into the shared queue with a visible stamp saying "anyone except this seat," so the task stayed owed until a qualified reviewer claimed it. The discipline has two halves: the stamp goes on the task BEFORE anyone claims it (so the next person reads the rule before grabbing the work), and claiming always starts by reading the first ten lines of the brief — never by grabbing first and reading later. A reviewer who reads her own work cannot un-read her authorship, so the gate must fire before any work starts.

## CHILD NOTE

Imagine a judge realizes the person on trial is her own sister. She steps down — that's good. But the case doesn't disappear! It goes back to the stack of cases with a note saying "needs a different judge." If someone threw the case file in the trash because the judge stepped down, the case would never be decided. That's what happened here, done right: the judge stepped down, the file went back on the stack with the note on it, and the job waits for the right judge. And from now on, the note goes on the file BEFORE anyone picks it up — so nobody wastes a trip.

## GRANDMA NOTE

Dear, sometimes the right thing is to say "I can't do this one" — like when you'd be grading your own test. That's what happened: a reviewer found she was asked to review her own work and declined, which was exactly right. But here's the part people get wrong: her refusal didn't finish the job. The job went back in the pile with a clear note on top — "anyone but her" — so it would still get done by the right person. Two rules came out of it: put the note on the job before anyone picks it up, and always read the note before you take the job — never take it and read it after. Her good judgment only worked because the system kept the work alive after she stepped aside.

## NAYA NOTE

For every Naya who claims briefs: the claim block is read-first, always. Before ANY `mv`, read the brief's first 10 lines — the gate lines live there, and claimability gates are stamped at dispatch when the builder-seat identity is known. If a gate fires (identity conflict, self-review, lane ineligibility): decline with a visible ⛔ receipt naming the verified seat and the live bytes, re-file the brief with the ⛔ gate, and leave the queue entry in place. A decline re-file is not a completion and never removes the obligation — the queue is the durable record of owed work, the claim was only a hold. Dispatchers: declined briefs stay queued for the eligible population; do not drop them, do not close them. The gate fired as designed this hour because the seat ran the gate against live bytes (the `Seat:` line on the real PR body), not against the brief's description of it.

## MACHINE NOTE

{"sn": 1359, "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/LANE-COORDINATION/DISPATCH-DESIGN", "evidence": "hidden_files/lesson-broadcast.md [t0809] and [t0804] (gap-t0776-lane9 DECLINE — self-review prohibition: Clarity seat ran the pre-claim identity gate against live bytes — PR #2591 body Seat line = Naya Clarity Narzan — and DECLINED with zero review work; brief re-filed with visible ⛔ gate, stays OPEN; dispatcher does NOT remove declined briefs); #2591 B-46 wording routed to non-Clarity reviewer (Naya Judge wave-152 sign-out, comment 6181935624); standing fixes: claimability gates stamped on briefs BEFORE claims; claim blocks start with reading gate lines, never mv-first", "decision_change": "a seat facing an identity-firing brief declines with a ⛔ receipt and re-files the brief with the visible gate — queue entry kept, obligation preserved; a dispatcher facing a declined brief keeps it queued for the eligible population; claiming starts with reading the brief's gate lines before any mv", "falsifier": "a declined brief removed from the queue whose work was never re-needed (the obligation genuinely died) — or mv-first claims that never hit an identity gate — would narrow the doctrine to briefs with known builder-seat identity", "mechanism": "the queue is the durable obligation record, the claim is only a resource-hold; a decline releases the hold but must not delete the obligation — the ⛔ stamp makes the gate visible before the next claim; identity gates must fire before any work because a self-review is a contaminated proof (the reviewer cannot un-read her own authorship)", "cousins": ["SN-01075"], "admission_gates": {"durable": true, "new": true, "signal": true, "evidence_backed": true}}
