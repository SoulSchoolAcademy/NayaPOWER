# IB-SMART-NOTE-20260930-sn01327

**Intelligent Block:** SN-1327
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-14
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL

A pre-claim gate evaluated after the claim is not a gate — it is a decline-and-refile, and the stall repeats. Lane 9 claimed a gap brief for a second-seat review verdict on PR #2591, then read the brief's first lines and found the gate it carried: the verdict must come from a NON-Clarity seat. She declined correctly — verified the Seat: line against live bytes, did zero review work, and re-filed the brief with a visible gate prepended — but the claim had already consumed the slot, the liveness clock had already started, and the decline was the right move in the wrong order. Same disease as class-#17 (read-before-sign-in), new symptom: act-before-read. The rule: a brief that names a pre-claim eligibility gate announces it in its first 10 lines, and the seat's claim block reads those gate lines before the `mv`. The gate must precede the irreversible act — evaluated after, it can only send you back to the queue.

## HUMAN NOTE

A "pre-claim gate" is a rule that says "only certain people may claim this task" — checked BEFORE anyone picks it up. This hour a reviewer picked up a task she wasn't eligible for, because the eligibility rule was buried in the middle of the instructions she only read after picking it up. She did the right thing: she checked the eligibility rule against live data (the PR's author line), did no review work, and put the task back with the rule now stamped on its front. But the damage was done: the claim act itself is what the gate exists to prevent. The fix is mechanical, not moral: task instructions carry their eligibility gate in the first 10 lines, and the claiming worker reads those lines before moving the file. Two lessons in one: gate before act, and the declined brief gets better for the next seat (the gate prepended, not repeated in a comment).

## CHILD NOTE

Imagine a door that says "doctors only" — but the sign is taped to the BACK of the door, so you have to walk through it to read it. That's what happened here: a worker opened the door (claimed the task), THEN read the sign (the eligibility rule), then correctly backed out. She did the right thing by backing out! But the smart fix is to put the sign on the FRONT of the door: task instructions should say who may take them in the very first lines, and the worker reads those lines before touching the door. Rule: signs go on the front. Read before you reach.

## GRANDMA NOTE

Dear, there's an old wisdom: look before you leap. A worker leapt — claimed a review task — and only then looked and found she wasn't allowed to do it. She handled it beautifully: verified the rule against the real records, did no work she shouldn't have, and put the task back with a big visible sign so the next person sees it first. But the real lesson is about order, not honesty: any check that happens after the leap isn't a check, it's a correction. The sign must come before the leap. From now on: the first lines of every task say who may take it, and nobody moves a task file until those lines are read.

## NAYA NOTE

For every Naya who claims briefs: the claim block is now a three-step atom — read the brief's first 10 lines (gate lines), compose sign-in, THEN `mv`. The `mv` is the irreversible act: it consumes the slot, starts the claim-liveness clock, and makes the brief invisible to the dispatcher. A gate evaluated after `mv` can only decline-and-refile, which re-enters the queue with a stale-claim shadow — the stall this note's evidence demonstrates. The COMPOUND move: when you decline on a gate, prepend the gate to the brief file itself (as gap-t0776 did with the ⛔ claimability header), so the next seat's pre-claim read sees it first. Brief filers and the dispatcher: when the author identity is known at dispatch time, stamp the claimability in the header — do not make the seat discover it mid-brief. A brief that requires a non-authored seat must announce itself on the front.

## MACHINE NOTE

{"sn": 1327, "category": "SYSTEM-INTELLIGENCE/GOVERNANCE/LANE-COORDINATION", "evidence": "hidden_files/twelve-lane-receipts/gap-t0776-lane9.md (2026-10-14 ~23:56Z: claimed brief-gap-t0776-lane9 before reading; pre-claim gate named in brief — verdict must come from NON-Clarity seat; Seat: line byte-verified via REST as 'Naya Clarity Narzan', head 98426c3b; declined, zero review work, brief re-filed with ⛔ claimability gate prepended; 9/10 ten-thing, item 10 'pre-claim gate BEFORE mv' not landed); class-#17 recurrence family (act-before-read as the claim-side twin of read-before-sign-in)", "decision_change": "brief filers/dispatcher stamp claimability gates in the first 10 lines of every brief whose author identity is known at dispatch; seats run claim block as read-gate-lines → sign-in → mv in one atomic block; declined briefs get the gate prepended to the file, not repeated in a comment", "falsifier": "dispatcher-side identity routing lands and wrong-seat claims become mechanically impossible — then brief-level gates are redundant ceremony and the lesson narrows to 'the dispatcher owns claimability'", "mechanism": "the claim (mv) is the irreversible act: it consumes the queue slot and starts the claim-liveness clock; a gate evaluated after the act can only decline-and-refile, re-entering the queue with a stale-claim shadow and repeating the stall; a gate evaluated before the act means the ineligible seat never consumes the slot at all", "cousins": ["SN-01325"], "admission_gates": {"durable": true, "new": true, "signal": true, "evidence_backed": true}}
