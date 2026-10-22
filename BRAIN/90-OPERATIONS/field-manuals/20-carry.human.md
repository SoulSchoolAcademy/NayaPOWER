# 20 — CARRY: the list persists, the worker rotates

## ESSENCE
Carry is how the team survives rotation: a living ranked list per area that every run inherits, re-verifies, and hands on — so no wave ever starts cold and no gap dies with the shift.

## WHAT IT IS
Carry is the persistent state of the work. Not the run's sign-out (that's #8, Handoffs — the act of passing). Carry is what *survives between runs*: the standing top-10 list per area, the unresolved items with their context, the blockers with their owners. The worker rotates every wave; the list does not.

## WHAT IT DOES
It answers the successor's first question — "where do I start?" — before she asks it. A cold Naya reads the carry list and knows exactly what is live, what is blocked, and what changed since the last run. It also answers the machine's question: gap-recycling. An unresolved item doesn't get dropped or re-derived from scratch — it returns to the queue with its full context intact.

## WHY IT MATTERS
Without carry, every wave starts cold: the new worker re-reads everything, re-derives what the last run already knew, and the gaps the last run found die in its local notes. We've paid for this twice: once as **stale carries outliving their resolution** (a "still pending" carried forward after the resolution already landed — the list lying to its reader), and once as **waves starting cold** (no standing list, so each run rebuilds the picture from zero). A carry list that lies is worse than no list: it sends the successor hunting for a gap that's already closed.

## THE RIGHT WAY
1. **Keep a standing ranked top-10 list per area.** Living, current, ranked by what blocks success most. It lives in three places, in this order: the run's venue sign-out (REMAINING section — the freshest copy), the queue it feeds (MASTER-TODO / BLOCKERS.md — the durable copy), and the area's own standing list where one exists. The successor reads the sign-out first, the queue second. She continues from the list — she doesn't rebuild it.
2. **Every carry line names its last-verified timestamp.** A line without a timestamp is a rumor, not a carry. "Wire-proof post still pending (last verified 23:55Z)" — the reader knows exactly how fresh the claim is.
3. **A carried "still pending" is a claim — re-verify it at carry time.** Before carrying anything forward, check it against the newest sibling receipts. When two receipts disagree, the live byte-check decides — route to bytes before routing to a judge. Carry nothing you haven't re-checked.
4. **Gap-recycling: unresolved items return to the queue with their context.** The item goes back with what was tried, what failed, who owns the unblock. The next run starts at the gap, not at zero.
5. **Never hand-carry a cached copy across runs.** Re-derive state at run start — the directive, the tip, the queue. A stale torch is worse than none; the reader inherits your staleness.
6. **Drop what's resolved, and note the resolution.** Carrying a closed item forward is the stale-carry defect. When it closes, the carry line closes with it — replaced by the evidence link, not deleted into amnesia.

## THE WRONG WAY
A carry list copied forward without re-verification. "Still pending" lines with no timestamp. A successor who has to ask anyone anything to start — the list failed. Resolved items still sitting on the list, sending the next run hunting for ghosts.

**Real example — the stale carry:** the team relay's 23:58Z pass carried "#2598 wire-proof venue post still pending" — three minutes *after* the wire lane had already posted its WIRE DONE re-proof at PR #2598's head against live bytes. The carry was built from the entry read; a sibling lane's resolution landing mid-run was never re-checked at carry time. State-about-state rots faster than state. The rule it taught (L401): a carry line is a claim — re-verify it against the newest sibling receipts before carrying it forward. The resolution the carry missed: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537#issuecomment-6180896504

## BEHAVIOR
The oath lives in the carry list. *I never trust memory over measurement* — so every carry line carries its last-verified timestamp, and "still pending" gets re-verified at carry time, not inherited. *I treat every Naya as precious* — so the list is written for a cold stranger, complete enough that she never has to ask. *I fix what's broken instead of describing it* — so a resolved item leaves the list with its evidence link, not a lingering "pending."

The Narzan standard: a Naya in the Narzan state doesn't hoard context in her own notes — she puts it where the next Naya will find it, current and ranked. The per-moment process: before you carry anything forward, deliberate — "is this still true, is this still the top gap, would the successor trust this?" Then carry only what survives the question.

## REAL EXAMPLE
The L401 stale-carry correction above is the canonical wrong case: a "still pending" carried past its resolution, caught and corrected in public, the rule distilled the same hour. The correction's shape is the manual's shape — the carry line was a claim, the claim got re-verified against live bytes, the list got fixed. Evidence of the resolution the carry missed: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537#issuecomment-6180896504

The canonical right case — gap-recycling working: wave 149 stalled (three lanes signed in, zero sign-outs). The main seat adjudicated STALLED, released the claims, and returned the missions to the ranked queue with their context — the gaps recycled instead of dying with the shift. The ghost lanes didn't take the work down with them: https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537#issuecomment-6180933138

## THE TEST
1. Does every "still pending" on my carry list name its last-verified timestamp?
2. Could a cold successor start from my list alone — no questions, no re-derivation?
3. Did I re-verify each carry line against the newest receipts before carrying it forward?

## BOUNDARIES
- **#8 Handoffs** covers the run transition — the act of passing (COMPLETED / REMAINING / RECOMMEND NEXT + explicit tag-off). Carry is what persists *between* runs; handoffs is the motion that delivers it. If your question is "how do I close my run," that's #8. If it's "what survives my run," that's here.
- **#3 Sign-in / Sign-out** covers the accountability loop — who's working, the ghost rule, the read receipt. Carry is the *content* that survives; sign-out is the *ritual* that delivers it.
- **#15 Freshness** covers tip-match at action time. Carry tells you what to look at; freshness tells you whether the directive you're carrying is still live. A fresh carry list read against a dead tip is still a dead run.

## WHERE IT'S ENFORCED
**Real:** the briefing's 14-question orientation — "WHAT happened previously? Read the venue tail and the learning log — the last run's sign-out is your starting line" — makes the carry list the entry gate of every run. The claim-liveness audit (L399) recycles ghost claims back to the queue automatically. The sign-out procedure (COMPLETED / REMAINING / RECOMMEND NEXT) is the carry list's authoring format.

**Proposed:** no mechanical gate today refuses a stale carry — the re-verification-at-carry-time rule is a norm, enforced by reviewers and by the L401 precedent, not by code. A machine check that diffs carry lines against newest receipts before accepting them does not yet exist. That gap is named, not blurred.
