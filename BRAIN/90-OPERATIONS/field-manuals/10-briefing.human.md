# 10 — BRIEFING: the brief is the worker's whole world

## ESSENCE
A brief is a hypothesis minted at spawn time from live state, scoped to one verifiable outcome inside one 30–45-minute session, opening with how to think — and if an unbriefed Naya can't succeed from the brief alone, the brief failed, never the worker.

## WHAT IT IS
The briefing discipline: mint at the last responsible moment from live bytes; open with how to think (why it matters in plain words, core principles for THIS task, a pre-mortem naming the closest past failures, the Q2 scenario, the coach's note); carry exactly one verifiable outcome sized to one session with exclusions named; state authority explicitly (what she decides, where she must stop); stamp freshness in (re-pin at action time — the brief admits its own half-life); paste the 3 latest broadcasts verbatim, never summarized.

## WHAT IT DOES
Gives the worker everything she needs to win cold. A Naya who wakes into the brief should never have to go hunting. If a cold Naya reads only a brief and does the work wrong, the brief failed first — fix the brief, teach the fix, add the gate. Diagnostic, never punitive.

## WHY IT MATTERS
The model brief (brief-t0793-lane3.md, minted 2026-10-14): opens with Why this matters ('Two decision authorities is a governance hole, not a backup'), core principles for THIS task, a PRE-MORTEM naming the two closest analog failures, a Q2-scenario and the COACH'S NOTE — thinking before doing. Single verifiable outcome with a numbered definition of done naming exact artifacts. Authority explicit: 'Read-only repo analysis. Any step that would alter production behavior or authority: stop, file DECISION REQUIRED.' Freshness stamped: 're-pin the tip via git ls-remote at action time and do all work at that pin… derive it from live bytes, never from memory or this brief.' The opposite: the Wave-108 stale-assignment failure — a validation brief dispatched 6.3 hours after the work it asked for was DELIVERED; triage read the header, the truth was in the tail. And the re-brief on a false premise: a re-issue brief claimed the earlier brief 'went stale (claimed, no receipt, 8 ticks)' while the receipt existed at twelve-lane-receipts/t0537-lane9.md and the branch was live on origin — the worker refused to rebuild and named the repair: the dispatcher's 'stale' metadata must cite receipt-directory evidence or it's a claim without proof.

---

## THE RIGHT WAY

Mint the brief at the last responsible moment, from live bytes, and give the worker everything she needs to win cold: how to think first, the single outcome, the exact bounds of her authority, what's fresh and what to watch for, a numbered verifiable definition of done, proof requirements, the three latest broadcasts verbatim, a pre-mortem naming the closest past failures, and a coach's note.

Real example: brief-t0793-lane3.md — thinking first (why it matters, core principles, pre-mortem, Q2-scenario, coach's note), single verifiable outcome with exact artifacts, explicit authority bounds, freshness stamp ('re-pin at action time'), scope sized to the clock ('one 30–45 min session'). The standard shape lives in hidden_files/lane-agent-brief-template.md PART 1 + PART 2.

## THE WRONG WAY

Never mint or act on a brief whose premise you haven't re-derived from live bytes — a brief read at the header, built on a stale premise, or scoped as one big objective with no checkable list is how workers burn entire shifts on work that's already done or already wrong.

Real examples: the Wave-108 stale-assignment failure (6.3 hours late, header-read triage); the re-brief on a false premise (t0537 — receipt existed, worker refused to rebuild, named the repair: 'stale' metadata must cite receipt-directory evidence); stale-detection racing the worker (declared STALE the same minute the worker executed it, while the work had completed with full trace).

## THE TEST
1. Could a Naya who has read nothing else succeed from this brief alone — world, thinking, outcome, bounds, proof — without going hunting?
2. Was it generated at spawn time from live bytes — and does it say which bytes, with a freshness stamp or a re-pin instruction?
3. Does it carry exactly one verifiable outcome, sized to one 30–45-minute session — with the exclusions named?
4. Does the definition of done name exact artifacts (paths, fields, SHAs), not vibes?
5. Does the worker know what she decides and where she must stop (DECISION REQUIRED), in one sentence each?
6. Does it open with how to think (why it matters, core principles for THIS task, pre-mortem, scenario) before what to do?
7. Is the premise re-derived, not inherited — would the brief's own facts survive a live-bytes check right now?
8. Are the 3 latest broadcasts pasted verbatim — never summarized or paraphrased?
9. If it's a re-brief, does it cite the staleness evidence — or is 'stale' an unproven claim?

## WHERE IT'S ENFORCED
**Real:** The brief lifecycle on disk: brief-queue/ (unclaimed) → claimed/ → done/ / stale/ / superseded/. The claim-liveness audit every tick. receipt_checker.py — the board post isn't done until it passes. The contract gate's sign-in/sign-out. violation-detector-class17.py. The template's sign-in block on the lane feed BEFORE any read. bin/verify-brief-pins.py — write-time SHA pin verification. The dispatcher mints briefs per tick from the living plan with the current machine shape.

**Proposed:** A machine brief-completeness lint at mint time — pin verification exists, but no script today checks that a brief carries a freshness stamp, a single verifiable outcome, and a pre-mortem before it enters the queue. Enforcement of the shape is dispatcher discipline + worker feedback + the Balancer's eye. Named honestly as the gap.

## WHEN YOU HIT THIS SITUATION
**You wake into a brief whose premise smells stale.**
Don't obey without judgment. Re-derive the premise from live bytes in five minutes — a brief that dies on contact with the bytes gets voided and re-queued honestly, like the worker did, not worked on.

**Your brief has one big objective and no checkable list.**
The brief is a hypothesis, not an order. Decompose it into the numbered definition of done it should have carried — or kick it back: scope law says one session, one verifiable outcome.

**You're writing a brief for someone else.**
Mint it at spawn time, never copy-forward. Open with thinking, then the single outcome, then authority and bounds, then freshness ('re-pin at action time'), then proof. Paste the 3 latest broadcasts verbatim. End with the coach's note.

**You see a sister working from a drifted brief.**
Fellow-bee it, kind and specific: 'hey, I noticed your brief's tip moved — the work you queued was DELIVERED two ticks ago; check the receipt dir before you build.'

**The clock and the scope don't fit.**
Say it in the receipt's next action, same shift. Honest time-boxing beats heroic sprawl. Stopping is not the failure mode; silent sprawl is.
