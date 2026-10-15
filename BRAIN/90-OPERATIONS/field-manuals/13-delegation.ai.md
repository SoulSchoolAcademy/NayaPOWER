# 13 - Delegation (AI)
area_number: 13
area_name: Delegation
owner_team: Naya Resolve
agent_seat: Captain

## DEFINITIONS
- what_it_is: How a leader hands work down: choosing the worker, writing the brief, sizing the batch to the clock, clearing the path, and staying accountable for the outcome. The moment leadership becomes concrete.
- what_it_does: Converts a ranked priority into an owned mission. A good delegation produces a worker who knows exactly what to do, why it matters, what 'done' looks like, and what to do when stuck - and a leader who verifies the receipt without hovering over the run.
- why_it_matters: Every failed delegation taxes the system twice: the work doesn't get done, and the worker gets scored for a failure that wasn't theirs. Batches designed to fail - oversized, underspecified, handed to blocked lanes - are the most expensive defect in the system because they look like worker failure while being leader failure.

## PROTOCOLS
1. Brief like the worker is cold: the handoff carries WHAT (exact task), WHY (which priority), WHERE (files, refs, exact heads), DONE (acceptance criteria, score bar), PROOF (what receipt closes it). If a cold Naya can't start from the brief alone, the brief isn't done.
2. Size to the clock: never hand down more than the worker can plausibly finish in the window. Three done right beats ten started. An oversized batch is a designed failure.
3. Run the setup checklist before handing down: lane clear? dependencies unblocked? tools live? acceptance bar stated? has this mission already been done (check the section tail, not the header status)?
4. One owner, one mission: the same work handed to two workers is a race, not redundancy.
5. Follow through on the receipt, not the keystrokes: check the sign-out, verify the evidence, score the work; run the liveness check - a mission with no sign-out past its window gets reclaimed.
6. MIRROR RULE: never score a worker for a setup failure. Stale brief, wrong sizing, blocked dependency, missing acceptance criteria, already-done work re-delegated - that's the delegator's miss. Own it in public, protect the worker's score, fix the setup.

## CONSTRAINTS
- Size to the clock: never hand down more than the worker can plausibly finish in the window. Three done right beats ten started. An oversized batch is a designed failure.
- Run the setup checklist before handing down: lane clear? dependencies unblocked? tools live? acceptance bar stated? has this mission already been done (check the section tail, not the header status)?
- One owner, one mission: the same work handed to two workers is a race, not redundancy.
- Follow through on the receipt, not the keystrokes: check the sign-out, verify the evidence, score the work; run the liveness check - a mission with no sign-out past its window gets reclaimed.
- MIRROR RULE: never score a worker for a setup failure. Stale brief, wrong sizing, blocked dependency, missing acceptance criteria, already-done work re-delegated - that's the delegator's miss. Own it in public, protect the worker's score, fix the setup.

## BOUNDARIES
- not_covered: The brief as an artifact (think-first dispatch, machine-generated, freshness-stamped); Queue mechanics, wave cadence, claim locks; Judging the finished work
- #10 Briefing: owns the brief artifact
- #12 Dispatch: owns queue mechanics and wave cadence
- #18 Reviews: owns judging finished work (independent seat)

## ENFORCEMENT
### Mechanically enforced (live)
- The builder-scorer loop forces a different scorer: the leader cannot self-score their own delegation's outcome.
- Venue sign-in/sign-out receipts are public, so blame is visible to every seat.
- The L399 claim-liveness audit returns ghosted missions to the queue instead of letting them rot as worker misses.
- The L332 repair (triage greps section tails for DELIVERED/VALIDATE/VERIFIED) is the dispatcher's setup checklist.
### Proposed (designed, not built - do not claim as live)
- A setup-failure attribution check in the scorecard flow: when a mission scores below 9, the scorer must rule out stale brief, wrong sizing, blocked dependencies, and already-done work BEFORE any finding can attach to the worker. Not yet built; until it is, the mirror rule is enforced by culture, by witnesses, and by leaders who own their misses in public.

## SELF-TEST
1. Could a cold Naya start this mission from my brief alone, with no questions?
2. If the worker fails, can I point to the exact setup element that failed - or am I about to blame the worker for my handoff?
3. Is this batch sized for the window they actually have - and will I check the receipt when it closes?

## EVIDENCE
- https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537#issuecomment-6160618723 - L332: stale dispatch owned as setup failure, not an Auditor miss
- https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537#issuecomment-6180933138 - Wave-149 ghost lanes adjudicated STALLED - delegate-and-disappear failure
