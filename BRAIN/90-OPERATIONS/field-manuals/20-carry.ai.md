# 20 - Carry (AI)
area_number: 20
area_name: Carry
owner_team: Naya Resolve
agent_seat: Archivist

## DEFINITIONS
- what_it_is: The persistent state of the work - what survives between runs. Not the run's sign-out (that's the act of passing). Carry is the standing top-10 list per area, the unresolved items with their context, the blockers with their owners. The worker rotates every wave; the list does not.
- what_it_does: Answers the successor's first question - 'where do I start?' - before she asks it. And answers the machine's question: gap-recycling. An unresolved item doesn't get dropped or re-derived from scratch - it returns to the queue with its full context intact.
- why_it_matters: Without carry, every wave starts cold: the new worker re-reads everything, gaps die in local notes. Paid for twice: stale carries outliving their resolution (a 'still pending' carried forward after the resolution already landed - the list lying to its reader), and waves starting cold with no standing list. A carry list that lies is worse than no list.

## PROTOCOLS
1. Keep a standing ranked top-10 list per area: living, current, ranked by what blocks success most. Lives in the run's venue sign-out (REMAINING section - the freshest copy), the queue it feeds (the durable copy), and the area's own standing list. The successor reads the sign-out first, the queue second - she continues from the list, never rebuilds it.
2. Every carry line names its last-verified timestamp. A line without a timestamp is a rumor, not a carry.
3. A carried 'still pending' is a claim - re-verify it at carry time: check against the newest sibling receipts before carrying forward. When two receipts disagree, the live byte-check decides - route to bytes before routing to a judge (L401). Carry nothing you haven't re-checked.
4. Gap-recycling: unresolved items return to the queue with their context - what was tried, what failed, who owns the unblock. The next run starts at the gap, not at zero.
5. Never hand-carry a cached copy across runs: re-derive state at run start. A stale torch is worse than none.
6. Drop what's resolved, and note the resolution: carrying a closed item forward is the stale-carry defect.

## CONSTRAINTS
- Keep a standing ranked top-10 list per area: living, current, ranked by what blocks success most. Lives in the run's venue sign-out (REMAINING section - the freshest copy), the queue it feeds (the durable copy), and the area's own standing list. The successor reads the sign-out first, the queue second - she continues from the list, never rebuilds it.
- Every carry line names its last-verified timestamp. A line without a timestamp is a rumor, not a carry.
- Gap-recycling: unresolved items return to the queue with their context - what was tried, what failed, who owns the unblock. The next run starts at the gap, not at zero.
- Never hand-carry a cached copy across runs: re-derive state at run start. A stale torch is worse than none.

## BOUNDARIES
- not_covered: The run transition itself - the act of passing (COMPLETED / REMAINING / RECOMMEND NEXT + explicit tag-off); The accountability loop - who's working, the ghost rule, the read receipt; Tip-match at action time
- #8 Handoffs: the act of passing
- #3 Sign-in/Sign-out: the accountability ritual
- #15 Freshness: tip-match at action time

## ENFORCEMENT
### Mechanically enforced (live)
- The briefing's 14-question orientation: 'WHAT happened previously? Read the venue tail and the learning log' - the carry list is the entry gate of every run.
- The claim-liveness audit (L399): ghost claims are recycled back to the queue automatically.
- The sign-out procedure (COMPLETED / REMAINING / RECOMMEND NEXT) is the carry list's authoring format.
### Proposed (designed, not built - do not claim as live)
- A machine check that diffs carry lines against newest receipts before accepting them. Does not exist - the re-verification-at-carry-time rule is a norm, enforced by reviewers and the L401 precedent, not by code.

## SELF-TEST
1. Does every 'still pending' on my carry list name its last-verified timestamp?
2. Could a cold successor start from my list alone - no questions, no re-derivation?
3. Did I re-verify each carry line against the newest receipts before carrying it forward?

## EVIDENCE
- https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537#issuecomment-6180896504 - The stale carry: '#2598 wire-proof still pending' carried 3 min AFTER the wire lane's WIRE DONE re-proof - the resolution the carry missed
- https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537#issuecomment-6180933138 - Wave-149 STALLED adjudicated: claims released, missions returned to the ranked queue - gap-recycling working
