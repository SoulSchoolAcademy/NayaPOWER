# Produce More, Waste Less — and See Both: the Project Intelligence Spec
SN-0835 · SYSTEM / intelligence
**Created:** 2026-10-23T18:48:00Z

## IN A NUTSHELL

Shawn's direction, in his words: spec it out — engineer the project system so it's highly effective; we must produce more and waste less (right now we're wasting a lot and producing very little — reverse that); and we must be aware of what we're producing and able to SEE it — that's what the project page is about. The spec (~/workspace/project-intelligence/SPEC.md v1) designs one loop — Produce → Prove → Publish → See — on top of what already exists: CPI state, the 15-minute refresh, the Smart Ledger, and the Projects page. Its core law: every act of work ends as a visible state change with proof, or it counts as waste — and the project page shows production and waste side by side, always current, maintained by the AIs as protocol, never typed in by the human.

## HUMAN

The math is counts, not adjectives. Production = a verified state transition to done-proven (the same event the Smart Ledger chains). Waste = activity that produced no transition and no evidence. The ratio — activity ÷ production — was audited at 173:1 on 2026-10-22; the target is under 60:1 by 2026-10-30, published daily. The spec names six wastes, each with a detector and a cure: zero-output loops, built-but-invisible work, aging items, duplicate work, report churn, and verification debt. The page gains a Production board next to the Intelligence board: today's landings and ratio in one human sentence, a 7-day trend strip, and a Waste panel that names aging items (with days standing still) and zero-output loops (with run counts) — or honestly says "none today." What waits on Shawn is pinned at the top, because his attention is the scarcest resource in the system and the page spends it first.

## CHILD

Imagine a workshop with a big board on the wall. Every time someone finishes making something real, they pin its picture on the board with a little tag showing where it is. If someone spent all day running around but finished nothing, the board shows that too — a list that says "ran all day, finished nothing." Nobody has to write reports; the board just always shows what got made and what got wasted. The rule of the workshop: if it's not on the board with its tag, it didn't happen.

## GRANDMA

It's like a good kitchen ledger. What came in, what went to the table, what spoiled in the pantry — all written down where everyone can see it. Nothing fancy: you cook, you serve, you write it in the book. If a bag of flour sat untouched for a week, the book shows it, and somebody deals with it. A house run this way stops wasting food without anyone giving speeches about wasting food — the book does the talking.

## NAYA

Engineering notes. The refresh computes a `production` block into state (transitions today/7d, done-proven total reconciling with the Intelligence strip, Smart Ledger tip, activity count from the census instrument, ratio — null until both sides honestly exist, never faked), plus aging (no transition ≥3 days) and zero-output loops (runs>0, transitions=0, 24h). The publisher projects items + production into the NayaPOWER project; the page renders Intelligence + Production boards and prints its own "intelligence as of" stamp — stale data that looks fresh is the one unforgivable defect in this system. The director runs the day from the page; any question the page can't answer is a spec defect filed as an intel item the same day. Acceptance is the Page Test: one full working day run exclusively from the project page (first run 2026-10-24), plus three-way reconciliation (page == state == Ledger tip) at every landing. The v2 build already in flight absorbed §4/§6 by director's instruction the same hour the spec was written.

## MACHINE

SPEC: PROJECT-INTELLIGENCE v1. LOOP: PRODUCE→PROVE→PUBLISH→SEE. DEFINITIONS: production_unit := verified transition to done-proven == one Smart Ledger entry (keyed by item id, counted once). activity_unit := census instrument count. ratio := activity/production per UTC day. BASELINE: 173:1 (2026-10-22 audit). TARGET: <60:1 by 2026-10-30. WASTE CLASSES: W1 zero-output loop (runs≥20/24h, transitions=0) · W2 built-but-invisible (no live proof 24h) · W3 aging (no transition ≥3d) · W4 duplicate claim · W5 report churn (no transition, no decision) · W6 verification debt (>1 director pass). GUARDS: publisher failure-isolated; ratio null when unmeasured; transitions without evidence rejected structurally; TEST data never enters counts. ACCEPTANCE: PAGE_TEST 2026-10-24; three-way reconcile page==state==ledger.

## WHAT IT ALL MEANS

This morning's assessment named the disease (173 actions per outcome) and tonight's Fourteen Questions named the interface. This spec is the treatment plan wired into the product itself: instead of productivity being a report somebody writes, it becomes a property of the page everybody already looks at. When waste is visible and named — with its owner and its age — it stops being a culture problem and becomes a work item. And when production is the same board, the team can finally see the ratio move as they change how they work, which is the only way a ratio ever really moves.

## WHAT'S IN IT FOR YOU

For Shawn: one page answers "what did we produce, what did we waste, what waits on me" in under a minute — no asking, no reports, no typing. For every Naya: your work becomes visible the moment it lands, with your name on real outcomes instead of activity; and the waste panel tells you what to stop doing, which is worth more than any instruction to do more. For members watching the system being built: this is the transparency engine — the same machinery that will show any project's truth to its owner.

## HOW IT APPLIES TO TEAM NAYA

Effective tonight: (1) claim work by state from CPI — claiming is a transition; (2) land with proof at landing time — the transition and the Ledger entry are part of the landing, not an end-of-day batch; (3) disagreements become review items, most-recently-verified wins, conflicts logged never silently resolved; (4) director passes read the page and the state, not chat claims; (5) the first Page Test runs 2026-10-24 and its defects become intel items the same day; (6) the daily ratio continues (Resolve lane) and now also lives on the page itself.

## THE DECLARED BEHAVIOR CHANGE

From tonight, I count my own work the way the spec counts everyone's: a day is production only where a state visibly changed with proof attached. Before I dispatch anything new, I will look at the waste panel — aging items and zero-output loops first — because clearing named waste is production too, and starting new work on top of unnamed waste is how 173:1 happened. If I cannot point to the transition, I will not call it progress, including in my own reports to Shawn.
