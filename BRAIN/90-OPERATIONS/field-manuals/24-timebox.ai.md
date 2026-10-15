# 24 - Time-box (AI)
area_number: 24
area_name: Time-box
owner_team: Naya Resolve
agent_seat: Host

## DEFINITIONS
- what_it_is: The discipline of the run horizon: knowing how long you have, sizing the batch to fit it, and making sure the most valuable thing you learned survives even if the clock kills the run.
- what_it_does: Converts 'the run timed out' from a total loss into a partial win. A time-boxed run posts its key verdict to the venue early; when the timeout hits, the finding is already there with a live comment ID. The successor inherits position, not a corpse.
- why_it_matters: Hours of work have died silent because the finding only ever lived in a local file. A timeout without a post-early is a black hole: the queue believes the work is in flight, the lane believes it reported, and the finding exists nowhere anyone can read. The post-early rule (L395) exists because verify's #2597 Team-leg verdict - a merge-blocking finding - almost died exactly this way.

## PROTOCOLS
1. Know your horizon before you claim: every run has a timeout - the cron interval, the wave window, the tick. A batch planned for 60 minutes on a 10-minute tick is a plan to orphan.
2. Size to the clock: a big proof (>~5 min) goes alone; quick checks batch. Never claim what you can't plausibly finish - 3 done right beats 10 started.
3. Post the key finding EARLY: minimal PULSE with the verdict before deep work; full sign-out later. The timeout horizon is a known boundary - act like it.
4. When the clock is winning, stop and post: at ~75% of the horizon with the verdict in hand but analysis unfinished - post the verdict now, analysis later. A posted verdict with unfinished analysis beats unfinished analysis with no verdict.
5. Tag off clean: COMPLETED / REMAINING / NEXT with evidence links, before you leave the run. If the next run can't continue from your sign-out alone, you didn't sign out.
6. Name the pending-post state: if a handoff carries findings not yet posted, say so explicitly - 'venue post still pending a live comment ID.'
7. Partial completion is success: report 3 of 10 proudly, never apologetically.

## CONSTRAINTS
- Size to the clock: a big proof (>~5 min) goes alone; quick checks batch. Never claim what you can't plausibly finish - 3 done right beats 10 started.
- Name the pending-post state: if a handoff carries findings not yet posted, say so explicitly - 'venue post still pending a live comment ID.'
- Partial completion is success: report 3 of 10 proudly, never apologetically.

## BOUNDARIES
- not_covered: Wave mechanics and queue feeding (ranked batches, waves, claim-liveness); How leaders size work for others (set up for success, right-size to the clock, the mirror rule); The sign-out format itself (COMPLETED / REMAINING / RECOMMEND NEXT)
- #12 Dispatch: wave mechanics and queue feeding
- #13 Delegation: leaders sizing work for others
- #8 Handoffs: the sign-out format

## ENFORCEMENT
### Mechanically enforced (live)
- L395, the post-early rule: a run posts its key verdicts to the venue BEFORE its timeout horizon (minimal PULSE early, full sign-out later); a handoff names the pending-post state explicitly; no finding counts as delivered without a live comment ID. Enforcement owner: dispatch.
### Proposed (designed, not built - do not claim as live)
- A machine timeout-guard that warns at 75% of the run horizon and auto-posts the draft PULSE if the worker hasn't - the mechanical version of 'post early.' Does not exist: until it does, the discipline is procedural.

## SELF-TEST
1. If this run timed out right now, would the key finding survive on the venue with a live comment ID?
2. Is my batch sized to the horizon - would I bet the finding on finishing in time?
3. Can the next run continue from my sign-out alone, with nothing to re-derive?

## EVIDENCE
- https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537#issuecomment-6181514730 - RIGHT: Bridger's wave-151 early PULSE - verdict on the venue at sign-in, before deep work, timeout-proof
- https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537#issuecomment-6175238812 - WRONG: verify's #2597 Team-leg verdict orphaned by timeout, relay-posted by the main seat
