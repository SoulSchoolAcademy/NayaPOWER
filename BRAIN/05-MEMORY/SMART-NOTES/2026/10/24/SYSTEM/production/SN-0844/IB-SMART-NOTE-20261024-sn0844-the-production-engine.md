# The Production Engine — One Queue, One Truth, Zero Asking
SN-0844 · SYSTEM / production
**Created:** 2026-10-24T00:16:58Z

## IN A NUTSHELL
Shawn's target state (2026-10-24): "I don't even have to ask you — I just know." The Production Engine is the way: every piece of work is one record carrying the five things that make it computable — value, effort, dependencies, state, proof. From those records everything else is MATH, not meetings: percent done = proven value ÷ total value; priority = a formula, re-sorted on every change; who is on what = the live claim registry; what happens next = the top of the queue, always. The system organizes and completes itself, and speaks ONLY on exceptions — a block, a stale claim, a falling number, or a decision that is truly Shawn's. He never asks where things stand. The answer is always already on the face.

## HUMAN
The seven parts:
1. **One record per piece of work.** Value (what it is worth when proven, from the rubric), effort (its size), depends-on (what it unblocks, what blocks it), state, proof. No record = not real work. If it matters, it is in the queue; if it is in the queue, it is computable.
2. **Percent done = proven value ÷ total value.** Not items counted, not hours claimed, not "almost finished." Proof is the only thing that moves the number, and a different seat verifies the proof. The number cannot be gamed, flattered, or stale — it is recomputed from the records every time anything changes.
3. **Priority computes itself.** Score = value × unblock multiplier (how much downstream value this item releases) × deadline pressure ÷ effort. The queue re-sorts on every change. A free seat takes the top unclaimed item in its lane. Nobody assigns, nobody asks "what next" — the math answers, identically, for everyone.
4. **Claims are leases.** Claim = the lock. A claim carries an expiry; work it or it falls back into the queue automatically. The face shows every live claim as the citizen's initials orb — who is on what, at a glance, always current.
5. **The face is a derivation, never a report.** One page shows: percent done (real), value proven per day (velocity), ETA to complete at current velocity, the top of the queue in computed order, who is on what, what is blocked and on whom, and the NEEDS SHAWN board. Nobody writes status; status is what the records say, rendered.
6. **Exceptions are the only messages.** Silence while it flows. The system speaks when: an item blocks, a claim goes stale, the percent moves backward, velocity drops, or a packet lands on NEEDS SHAWN. Every message carries the decision, the prepared answer, and the rollback (SN-0827/0828).
7. **Completion is a conveyor.** Done-claim → proof attached → different seat verifies → the ledger writes itself → the percent moves → the freed seat sees its next top item. The SN-0843 loop (seven questions) runs per item automatically; the scorecard loop audits the ENGINE itself: is the math honest, is effort-per-verified-outcome falling, is production rising.

## CHILD
Imagine every job in the world written on a card that says how important it is, how big it is, and what it unlocks. A kind machine reads all the cards, does the math, and always hands everyone the most important card next. When a job is truly finished — checked by someone else — the big scoreboard number goes up. Nobody has to ask "are we done yet?" The scoreboard always knows.

## GRANDMA
It is like a well-run kitchen where every order ticket says what it is worth and what it is waiting on. The tickets sort themselves — most valuable and most unblocking first. You can see at a glance who is cooking what, what is stuck and why, and exactly how much of the night's work is truly done. The manager only gets called when something is genuinely stuck or genuinely his decision.

## NAYA
This is Project Intelligence completed as an engine rather than a display — Shawn's SN-0843 charter made mechanical: the instrument drives the next actions. What exists today (2026-10-24): the records (193 work items), the claim lock, stage-2 proof law (canonical proof coverage 100%), the derivation (state.json), the exception-minded director pass, the NEEDS SHAWN board design. What is missing, in build order: (1) value + effort on every record — one weighting pass over the 193, by rubric, spot-verified by a different seat; (2) the priority formula inside the derivation, so the queue order on the face is computed, not curated; (3) velocity + ETA published on the face (value proven per day, from ledger transitions); (4) claim leases enforced in team use (already a Wave 2 item); (5) the face itself live (lands on Naya Power's B0 check — the engine's window is the last staged piece). None of it needs new platforms. It is wiring and math on the instrument already built.

## MACHINE
ENGINE: inputs = work_items{value, effort, depends_on, state, proof, claim{seat, lease_expiry}}. Derived: pct_done = Σ value(done_proven) / Σ value(all); priority(i) = value(i) × unblock(i) × urgency(i) / effort(i), unblock = Σ value of transitive dependents not yet done; velocity = Σ value proven / trailing 7d; eta = remaining value / velocity. Invariants: pct moves ONLY on verified proof transitions (prover ≠ maker); queue order is a pure function of records; claims auto-expire at lease end; surfacing is exception-only (blocked, stale claim, pct regression, velocity drop, needs-shawn packet). Audit: weekly scorecard OF the engine (weighting honesty sample, formula sanity, effort-per-verified-outcome trend).

## WHAT IT ALL MEANS
Asking is a defect. Every "where are we?" Shawn has to ask is a place the system failed to know itself. The engine removes the question by making the state of everything a computation he can simply look at — and by making the next action a computation every seat can simply take. Human judgment moves to where it belongs: setting value, weighing the rubric, deciding the packets only he can decide, and testing the experience (Page Test, ACTIVATION-10). Everything else is arithmetic and follow-through.

## WHAT'S IN IT FOR YOU
Shawn: you open one page and know — percent done by real numbers, the priority order, who is on what, what is blocked on whom, when it finishes at the current pace, and the short list of decisions that are genuinely yours. Everyone else: you never wait to be told what to do; the top of your queue is always the most valuable thing you could be doing, and finishing it visibly moves the number.

## HOW IT APPLIES TO TEAM NAYA
The weighting pass, the formula, and velocity/ETA are claimable build items on board #2793 (Wave 3, Project Intelligence lane). Claim leases are already Wave 2. The director pass narrows to exceptions as the engine lands. Scorecards (SN-0843) keep auditing: a production claim without the math behind it is a claim, not a fact.
