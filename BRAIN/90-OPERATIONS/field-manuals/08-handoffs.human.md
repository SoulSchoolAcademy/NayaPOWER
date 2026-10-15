# 08 — HANDOFFS: pass the torch, not the burden

## ESSENCE
The sign-out is the product: if the next run can't continue from your sign-out alone, you didn't sign out. Every handoff carries COMPLETED with evidence, REMAINING in priority order, and RECOMMEND NEXT with an explicit tag-off — and key verdicts hit the venue before the timeout horizon, because a result unrecorded is a result lost.

## WHAT IT IS
The handoff discipline: COMPLETED — item numbers with evidence (each claim pinned to an artifact, a comment ID, or a SHA); REMAINING — item numbers with a one-line status each, returned to TODO in priority order; RECOMMEND NEXT — what the next run takes first, with an explicit tag-off naming which lane takes the list. Partial completion is success — report 3 of 10 proudly, never apologetically. The handoff passes the cold-successor test: a Naya who reads only your sign-out can start working with nothing to re-derive.

## WHAT IT DOES
Makes continuity mechanical instead of heroic. Close the loop on every surface the run touched: unworked items released back to TODO with one-line status, MASTER-TODO prepended, the queue updated, memory logged, the goal timeline recorded.

## WHY IT MATTERS
The complete-state handoff of 2026-10-12 — from Naya 4 to 'whoever picks up the torch' — opened with a one-paragraph nutshell, listed every shipped item with its PR number, exact-head SHA, and named verifier, reconciled the key decision live before handoff (100 open PRs confirmed on main — not 30), and stated the live priority list in plain words. The next Naya inherited position, evidence, and direction — nothing to re-derive (hidden_files/NEXT-NAYA-HANDOFF-20261012.md; reconciliation posted as comment 6117670899). The opposite: the verify run that timed out ~18:18Z before posting the #2597 Team-leg verdict — the finding existed only in the worker's handoff until the main seat relay-posted it (comment 6175238812). No finding counts as delivered without a live comment ID. The repair this taught: post key verdicts early, before the timeout horizon, not after.

---

## THE RIGHT WAY

Every handoff has three parts, in order: (1) COMPLETED — item numbers with evidence ('done 1–5'), each claim pinned to something a stranger can re-derive; (2) REMAINING — item numbers with a one-line status each, returned to TODO in priority order; (3) RECOMMEND NEXT — what the next run should take first, and any reordering you'd suggest. Then tag off explicitly: name which lane's next run takes the list.

Real example — the full-state shape: the 2026-10-12 complete-state handoff (NEXT-NAYA-HANDOFF-20261012.md) with nutshell, per-item evidence, live reconciliation, and plain-words priorities. Real example — the per-item shape: the night-shift-verify sign-outs, per-item verdict + score + what would make it 10, unworked items released with one-line status, MASTER-TODO prepended, queue updated, memory logged.

## THE WRONG WAY

A handoff the successor can't continue from. Findings that live only in a local file. Apologizing for partial completion instead of reporting it. And the worst form: a key verdict that exists in your hands but never reaches the venue before your time runs out.

Real example: the verify run that timed out ~18:18Z before posting the #2597 Team-leg verdict — the finding existed only in the worker's handoff until relay-posted (comment 6175238812). A result unrecorded is a result lost.

## THE TEST
1. COMPLETED — with evidence links a stranger can re-derive (artifact, comment ID, or SHA)?
2. REMAINING — item numbers in priority order, returned to TODO with a one-line status each?
3. Did I RECOMMEND what the next run takes first, and any reordering?
4. Did I name exactly who takes it next — lane and run, not 'whoever'?
5. Could a cold successor start working from this sign-out alone, with nothing to re-derive?
6. Did I report partial completion proudly — no apologies, no burying?
7. Are key verdicts already on the venue — posted before the timeout horizon?

## WHERE IT'S ENFORCED
**Real:** The brief's sign-out receipt spec (lane-agent-brief-template.md): every run signs out with what-you-did → evidence → scorecard → holes remaining → next action. LAW 02's handoff contract: mission, state, completed, verified, open issues, constraints, exact next action, success criteria. The contract gate's sign-out lint (drift line, done-statement, honest score, protected-gate tripwire). The post-early rule (L395): key verdicts hit the venue before the timeout horizon. The claim-liveness audit: every wave closeout returns ghost claims to the queue.

**Proposed:** No byte-level check verifies that a sign-out's COMPLETED items actually carry evidence links, or that REMAINING items actually returned to TODO. The contract gate lints that the sections exist — not that they're true. Content truth is still peer-scoring and scorecard discipline. Named honestly as the gap.

## WHEN YOU HIT THIS SITUATION
**Your time-box is running out with items unfinished.**
Post key verdicts to the venue FIRST, then write the sign-out. The board outlives your run; your local file doesn't. This is the post-early rule — and it exists because #2597 proved what happens otherwise.

**You're tempted to apologize for 3 of 10.**
Don't. Report the 3 with evidence, return the 7 to TODO in priority order, recommend the next take. Partial completion reported cleanly is success; a hidden 3 is theft from the next run.

**You hit a blocker mid-list.**
It goes in REMAINING with a one-line status and a named owner — never dissolved into prose, never silently dropped. A named blocker with an owner is a handoff; an unnamed one is a dead end. (See manual 09 — Blockers.)

**The next run is a different seat or lane.**
Tag off by name: which lane, which tick. The cold-successor test applies double here — assume they know nothing except your sign-out.

**Everything is done.**
Still write the sign-out. 'No remaining' is itself a handoff — it tells the next run the list is exhausted and where the evidence lives. Silence is not a verdict.
