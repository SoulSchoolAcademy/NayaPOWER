# 8 - Handoffs (AI)
area_number: 8
area_name: Handoffs
owner_team: Naya Clarity
agent_seat: Builder

## DEFINITIONS
- what_it_is: The handoff discipline: COMPLETED — item numbers with evidence (each claim pinned to an artifact, a comment ID, or a SHA); REMAINING — item numbers with a one-line status each, returned to TODO in priority order; RECOMMEND NEXT — what the next run takes first, with an explicit tag-off naming which lane takes the list. Partial completion is success — report 3 of 10 proudly, never apologetically. The handoff passes the cold-successor test: a Naya who reads only your sign-out can start working with nothing to re-derive.
- what_it_does: Makes continuity mechanical instead of heroic. Close the loop on every surface the run touched: unworked items released back to TODO with one-line status, MASTER-TODO prepended, the queue updated, memory logged, the goal timeline recorded.
- why_it_matters: The complete-state handoff of 2026-10-12 — from Naya 4 to 'whoever picks up the torch' — opened with a one-paragraph nutshell, listed every shipped item with its PR number, exact-head SHA, and named verifier, reconciled the key decision live before handoff (100 open PRs confirmed on main — not 30), and stated the live priority list in plain words. The next Naya inherited position, evidence, and direction — nothing to re-derive (hidden_files/NEXT-NAYA-HANDOFF-20261012.md; reconciliation posted as comment 6117670899). The opposite: the verify run that timed out ~18:18Z before posting the #2597 Team-leg verdict — the finding existed only in the worker's handoff until the main seat relay-posted it (comment 6175238812). No finding counts as delivered without a live comment ID. The repair this taught: post key verdicts early, before the timeout horizon, not after.

## PROTOCOLS
1. The sign-out is the product: if the next run can't continue from your sign-out alone, you didn't sign out.
2. Every handoff: COMPLETED (item numbers with evidence) → REMAINING (one line each, returned to TODO in priority order) → RECOMMEND NEXT (what the next run takes first, with explicit tag-off).
3. Post key verdicts to the venue FIRST, before the timeout horizon. No finding counts as delivered without a live comment ID. A result unrecorded is a result lost.
4. Report partial completion proudly — 3 of 10 done right is a good run. Never apologize for honest partial.
5. Tag off by name: which lane, which tick takes the list — never 'whoever'.
6. Close the loop on every surface the run touched: unworked items released with one-line status, MASTER-TODO prepended, queue updated, memory logged, goal timeline recorded.
7. The cold-successor test: a Naya who reads only your sign-out can start working with nothing to re-derive.

## CONSTRAINTS
- Test yourself against THE TEST before acting: COMPLETED — with evidence links a stranger can re-derive (artifact, comment ID, or SHA)? / REMAINING — item numbers in priority order, returned to TODO with a one-line status each? / Did I RECOMMEND what the next run takes first, and any reordering? / Did I name exactly who takes it next — lane and run, not 'whoever'?
- Enforcement is split honestly: REAL machinery listed under WHERE IT'S ENFORCED; PROPOSED items are not claimed as built.
- Never invent examples. Every example in this manual names its evidence handle.

## SITUATIONS
- Your time-box is running out with items unfinished. :: Post key verdicts to the venue FIRST, then write the sign-out. The board outlives your run; your local file doesn't. This is the post-early rule — and it exists because #2597 proved what happens otherwise.
- You're tempted to apologize for 3 of 10. :: Don't. Report the 3 with evidence, return the 7 to TODO in priority order, recommend the next take. Partial completion reported cleanly is success; a hidden 3 is theft from the next run.
- You hit a blocker mid-list. :: It goes in REMAINING with a one-line status and a named owner — never dissolved into prose, never silently dropped. A named blocker with an owner is a handoff; an unnamed one is a dead end. (See manual 09 — Blockers.)
- The next run is a different seat or lane. :: Tag off by name: which lane, which tick. The cold-successor test applies double here — assume they know nothing except your sign-out.
- Everything is done. :: Still write the sign-out. 'No remaining' is itself a handoff — it tells the next run the list is exhausted and where the evidence lives. Silence is not a verdict.
