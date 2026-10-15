# 11 — RANKING: value × unlock ÷ effort — triage is the highest-leverage act in the system

## ESSENCE
Rank by mission value × unlock ÷ effort — never by arrival order, loudness, or who shouted last; dependencies outrank leaves, and ties go to learning. Ranking is a verb, not a document: it runs every tick, and the top item must be the one you'd bet the hour on — with the bet defended in one sentence.

## WHAT IT IS
The triage discipline: the living plan's standing top-ten, re-ranked every director tick by mission leverage × unblockability ÷ effort — closed items drop with their proof, newly found holes enter with owners, every item's position defended in a line or two. The dispatcher's pull order: FEEDBACK CHECK FIRST, then SURGE CHECK, then the grand to-do list (STAGE 0 first), up to three items, never more than free lanes — then a MISSION-IMPACT FILTER weighting toward Stage 1 (protect) or Stage 2 (prove). Shawn's dispatch law stands as the override: work lowest numbers first (a 5→9 beats a 9→10), activation gates everything, near-instant learning is built first when other gains depend on it.

## WHAT IT DOES
Puts unlockers before the work they unlock. Dependencies outrank leaves. Arrival order is not value order — the dispatcher's STEP 3 exists precisely to forbid FIFO. A rank that can't be executed (stacked on occupied lanes, or only one worker can touch it while lanes idle) is a wish list, not a queue.

## WHY IT MATTERS
The t0770 executor dispatch sat held until the t0780 second-seat verdict CONFIRMED (sealed) that the SURGE semantic-arm hypothesis-change is a genuine new hypothesis — then dispatch was unblocked immediately, with the right executor shape. The unlocker was ranked above the work it unlocked. The opposite: the phantom claim — the scorecard brief that was the single merge blocker for milestone 1, sitting in claimed/ 18+ minutes with no sign-in while the rotation still listed it queued. A queue that loses its top item has no ranking at all — just a pile. And one tick wrote new briefs to lanes already holding two queued briefs each — the ranking had ignored lane capacity (t0704, memory/2026-10-13.md). Dispatch is PULL to free lanes only.

---

## THE RIGHT WAY

Ranking is a verb, not a document. It runs every tick, and the top item must be the one you'd bet the hour on — with the bet defended in one sentence.

Real examples: the live top-ten re-ranked every director tick (live-plan.md TOP-10 STANDING SECTION — item 1 the B-50 escalation carried to the main seat; the t0767 verdict gap visibly CLOSED and moved from holes to upgrades with its receipt; the Brainbase '24x7 Intelligence Factory' retired outright per Shawn's 2026-10-08 standing word). The dispatcher's pull order (night-dispatcher STEP 3: feedback → SURGE → to-do, STAGE 0 first, ≤ free lanes; STEP 4 mission-impact filter). Dependencies outrank leaves in action: t0770 held for the t0780 sealed verdict, then unblocked immediately. The machine form: the decision value calculus scores dependency_unlock as its own dimension (kernel/value_calculus.py).

## THE WRONG WAY

FIFO dispatch — dispatching in arrival order because 'it was here first.' Ranking by loudness or recency — the board's measured failure mode is REDUNDANCY WITHOUT DELTA, template repetitions burying signal under volume; recency is the laziest ranking function there is. Losing the top item — the phantom claim (#2533, 18+ minutes, the merge blocker silently lost). Dispatching to occupied lanes — t0704 wrote to lanes already holding two queued briefs each. Letting a stale claim rot at the top — Wave 149's three executors silent ~2 hours, adjudicated STALLED, claims released to the ranked queue (the L24 dead-claim rule: claim-then-sign-out within the window or the claim is void).

## THE TEST
1. Can you state the top item and defend it in one sentence — would you bet the hour on it?
2. Is the order driven by value × unlock ÷ effort, or by arrival, loudness, or recency?
3. Does anything ranked above another item unblock it — are dependencies ahead of their leaves?
4. Can the top items actually be worked — or can only one worker touch them while the free lanes idle?
5. Is every ranked item assigned to a FREE lane (pull only), or are you stacking onto occupied lanes?
6. Did closed items drop with their proof, and did new holes enter with named owners?
7. If two items tie, does learning win?
8. Does Shawn's dispatch law change the order — and did you apply it instead of skipping it?

## WHERE IT'S ENFORCED
**Real:** The live plan's TOP-10 standing section: re-ranked every director tick by mission leverage × unblockability ÷ effort (hidden_files/live-plan.md). The night-dispatcher STEP 3 pull plus STEP 4 mission-impact filter (crons/minutely/night-dispatcher__interval@10m.md). Queue accounting in twelve-lane-rotation.json, the claim-liveness audit, and the L24 dead-claim rule. Shawn's dispatch law as the standing override (MEMORY.md, 2026-10-13). The value calculus scores dependency_unlock as a real dimension.

**Proposed:** The red-gates auto-file-queues system fix is owed and listed in the live plan's next actions; it is not wired yet. There is no automated 'ranker' service: ranking today is director-tick discipline plus dispatcher procedure, not machine law. Calling it enforced beyond the items above would be a lie.

## WHEN YOU HIT THIS SITUATION
**You're handed a queue of N items and one hour.**
Run the calculus on each: mission value × what it unblocks ÷ the effort to do it. Put unlockers before the work they unlock. Write the one-sentence defense for #1. If you can't defend #1, you don't understand the queue — go read live state before you touch anything.

**A claim goes quiet.**
Run the liveness audit: sign-in within the window, receipt after 6 ticks. No sign-in → phantom claim, void it back to the queue. Sign-in but no receipt after 6 ticks → STALE, release it. Never let a silent claim hold the top slot.

**Two items tie.**
Learning wins. If near-instant learning means other gains depend on it, build it first — that's Shawn's dispatch law, and it overrides the mechanical rank.

**A new hole appears mid-tick.**
It enters the ranked list with a named owner at its computed position — never appended at the bottom by default, never shoved to the top by recency.

**The whole queue stalls.**
Check the ranking, not the workers. A stalled queue is almost always a ranking failure: a phantom claim at the top, dispatch stacked on occupied lanes, or dependencies buried under their leaves. Fix the rank first.
