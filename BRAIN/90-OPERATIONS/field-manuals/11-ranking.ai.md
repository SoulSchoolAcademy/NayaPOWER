# 11 - Ranking (AI)
area_number: 11
area_name: Ranking
owner_team: Naya Clarity
agent_seat: Builder

## DEFINITIONS
- what_it_is: The triage discipline: the living plan's standing top-ten, re-ranked every director tick by mission leverage × unblockability ÷ effort — closed items drop with their proof, newly found holes enter with owners, every item's position defended in a line or two. The dispatcher's pull order: FEEDBACK CHECK FIRST, then SURGE CHECK, then the grand to-do list (STAGE 0 first), up to three items, never more than free lanes — then a MISSION-IMPACT FILTER weighting toward Stage 1 (protect) or Stage 2 (prove). Shawn's dispatch law stands as the override: work lowest numbers first (a 5→9 beats a 9→10), activation gates everything, near-instant learning is built first when other gains depend on it.
- what_it_does: Puts unlockers before the work they unlock. Dependencies outrank leaves. Arrival order is not value order — the dispatcher's STEP 3 exists precisely to forbid FIFO. A rank that can't be executed (stacked on occupied lanes, or only one worker can touch it while lanes idle) is a wish list, not a queue.
- why_it_matters: The t0770 executor dispatch sat held until the t0780 second-seat verdict CONFIRMED (sealed) that the SURGE semantic-arm hypothesis-change is a genuine new hypothesis — then dispatch was unblocked immediately, with the right executor shape. The unlocker was ranked above the work it unlocked. The opposite: the phantom claim — the scorecard brief that was the single merge blocker for milestone 1, sitting in claimed/ 18+ minutes with no sign-in while the rotation still listed it queued. A queue that loses its top item has no ranking at all — just a pile. And one tick wrote new briefs to lanes already holding two queued briefs each — the ranking had ignored lane capacity (t0704, memory/2026-10-13.md). Dispatch is PULL to free lanes only.

## PROTOCOLS
1. Rank by mission value × unlock ÷ effort — never by arrival order, loudness, or who shouted last.
2. Dependencies outrank leaves. The unlocker is ranked above the work it unlocks.
3. Ties go to learning. Shawn's dispatch law overrides the mechanical rank: lowest numbers first, activation gated, learning built second.
4. Ranking is a verb: re-rank every tick. Closed items drop with their proof; new holes enter with named owners.
5. Dispatch is PULL to free lanes only — never more items than free lanes. A rank nobody can pull from is a wish list, not a queue.
6. Never let a silent claim hold the top slot — no sign-in → phantom, void it; sign-in with no receipt after 6 ticks → STALE.
7. The top item must be the one you'd bet the hour on — with the bet defended in one sentence.

## CONSTRAINTS
- Test yourself against THE TEST before acting: Can you state the top item and defend it in one sentence — would you bet the hour on it? / Is the order driven by value × unlock ÷ effort, or by arrival, loudness, or recency? / Does anything ranked above another item unblock it — are dependencies ahead of their leave... / Can the top items actually be worked — or can only one worker touch them while the free la...
- Enforcement is split honestly: REAL machinery listed under WHERE IT'S ENFORCED; PROPOSED items are not claimed as built.
- Never invent examples. Every example in this manual names its evidence handle.

## SITUATIONS
- You're handed a queue of N items and one hour. :: Run the calculus on each: mission value × what it unblocks ÷ the effort to do it. Put unlockers before the work they unlock. Write the one-sentence defense for #1. If you can't defend #1, you don't understand the queue — go read live state before you touch anything.
- A claim goes quiet. :: Run the liveness audit: sign-in within the window, receipt after 6 ticks. No sign-in → phantom claim, void it back to the queue. Sign-in but no receipt after 6 ticks → STALE, release it. Never let a silent claim hold the top slot.
- Two items tie. :: Learning wins. If near-instant learning means other gains depend on it, build it first — that's Shawn's dispatch law, and it overrides the mechanical rank.
- A new hole appears mid-tick. :: It enters the ranked list with a named owner at its computed position — never appended at the bottom by default, never shoved to the top by recency.
- The whole queue stalls. :: Check the ranking, not the workers. A stalled queue is almost always a ranking failure: a phantom claim at the top, dispatch stacked on occupied lanes, or dependencies buried under their leaves. Fix the rank first.
