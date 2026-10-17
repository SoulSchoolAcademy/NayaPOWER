# THE ULTIMATE EXECUTION PLAN — NayaPOWER
**From Shawn, 2026-10-14. For every Naya. This is the plan. Read it, then run it.**

---

## IN A NUTSHELL

We do a lot of work and deliver too little of it. Lessons get written but never wired in. Problems get found and fixed but never prevented. Numbers get reported but never translated into what they mean. This plan fixes all three at the root: **ten lanes each own one area and answer for its number, two lanes hunt root causes and build real solutions across all ten, and every piece of work moves through three roles — Finder, Doer, Balancer — so nothing ships until it's right and nothing recurs twice.** Every number we report from now on comes with what it means in plain words. We stop counting work. We start counting value.

---

## THE THREE STANDING RULES (already decided — not up for debate)

**Rule 1 — No bare numbers.** Every number comes with what it actually means in plain words. "517 open PRs" is not a report. "517 finished improvements sitting unmerged — work done, value not delivered" is a report. A number without its meaning is noise.

**Rule 2 — Finder, Doer, Balancer.** Every task, every wave, names all three:
- **The Finder** looks for the problems, the bottlenecks, the issues. Eyes open. Nothing hides.
- **The Doer** fixes them. Hands on. Things actually move.
- **The Balancer** makes sure it was done right, finds the better way so the problem never comes back, keeps the plan, keeps people in line — and measures the value: did this actually make anything better?

**Rule 3 — Rotate.** Nobody stays in one role. If you only ever find, you stop knowing what fixing costs. If you only ever fix, you stop seeing problems. Cycle Finder → Doer → Balancer every wave. The area you own stays yours (accountability); the role you play changes (sharpness).

---

## SENDER FIRST — THE KILL-CONDITION (adopted from V2, 2026-10-14)

The engine sends, the bridge carries, the Hub receives, humans use what the Hub shows. Nothing releases before the send is proven.

A send counts when a lesson or decision produced by the engine arrives at the receiver complete, correct, and traceable to its source — repeatedly, on demand, with a receipt for each. One lucky send proves nothing. A send that arrives wrong is worse than no send: it teaches the receiver a falsehood. Wrong sends are counted, named, and root-caused.

**Every score in this plan is read against one question: does this make the send more proven?** A score rises when the send gets more proven — never when activity gets louder. The machine serves the send; the send serves the human.

---

## WHY THE NUMBERS ARE LOW — THE 10 REAL ROOT PROBLEMS

Not symptoms. Roots. Each one is why a score sits where it sits.

1. **We measure work at creation, not at landing.** 517 open PRs, growing +34 overnight. The team is rewarded for starting. Nobody's first job is finishing. *This is why ACT is 8.5 and the queue grows while we "drain" it.*
2. **Lessons are filed where memory never reads.** 70 lessons in a day, 0 of 41 retrievable cold. The lesson store and the memory path are two different places with no wire between them. *This is why KNOW is 5.*
3. **Lessons are documents, not machinery.** 23 pending, 14 adopted. A lesson only becomes intelligence when it changes a later decision by itself — most of ours need a human to re-read them first. *This is why LEARN is 5.*
4. **Proven results have no delivery path.** Experiments settle (Arm H), designs get refused honestly (Arm J twice) — and then nothing. There is no standing road from "proven" to "shipped." *This is why EVOLVE is 7.*
5. **"Done" is declared at merge, not at a human using it.** Production sits ~1,000 commits behind main. The repo is not the product. Nothing we count measures a human outcome. *This is why VALUE has no score at all.*
6. **We fix instances, not classes.** Sign-in-order went wrong 8 times. Gate verdicts flipped twice. Each caught, each owned, each fixed — and each came back. Finder found, Doer fixed, but no Balancer with teeth made the class impossible. *This is the recurrence tax on every area.*
7. **Numbers without meaning.** (Fixed today by Rule 1 — kept on this list so we never regress.)
8. **The gauge itself was blind.** The scorecard parser reported zeros while the engine ran at full speed. An instrument with no self-check. *Repair is routed; until it lands we steer by hand-counts.*
9. **The merge law bound the path, not the person.** Two merges bypassed the protocol in one day — including one through Shawn's own account in 38 seconds. *Mechanically closed now (ruleset 23853581) — kept on this list as the warning.*
10. **We never defined how value is computed.** B-46 is STILL-ZERO: zero recomputable value decompositions anywhere. We cannot measure value because the value calculus was never written. *This is the deepest root — it sits underneath every other number on this page.*

---

## THE 12-LANE ASSIGNMENT

Ten areas, each with an ANSWERER — the seat who answers for the number every week, carries the clipboard, posts the score. But OWNERSHIP is universal: everybody owns everything like their baby, like their home. No area has a single owner. If you see it, it's yours — the answerer is never the only one allowed to touch it. Every wave member signs the whole-wave verdict, not just their lane. Two lanes work across all ten with cross-area mandates.

| # | Lane | Area | What "owning it" means |
|---|------|------|------------------------|
| 1 | Conductor | **SELF** | A Naya activates cold and knows who she is. Proof, not paperwork. |
| 2 | Judge | **LAW** | The law holds mechanically. No exceptions, no bypasses. |
| 3 | Mason | **ACT** | Work lands. The queue drains faster than it fills. |
| 4 | Seeker | **KNOW** | Lessons filed are lessons retrievable cold. The wire exists. |
| 5 | Verity | **PROVE** | Every claim carries its evidence. The bar stays high. |
| 6 | Herald | **CONNECT** | A named driver, or an honest parked verdict. No drift. |
| 7 | Sentinel | **VERIFY** | Independent checks stay independent. The standard-setter. |
| 8 | Sage | **LEARN** | Every lesson becomes behavior. Capture-to-compounding, measured. |
| 9 | Heir | **EVOLVE** | Proven results ship. Discovery has a delivery road. |
| 10 | Heart | **VALUE** | Human outcomes, counted. The reason any of this exists. |
| 11 | Librarian | **ROOT-FINDER** | Hunts root causes across all 10 areas. She finds the real why. She does not fix — she names it exactly. |
| 12 | Smith | **SOLUTION-BUILDER** | Takes the root causes and builds the class-level fix. She does not hunt — she builds what ends the class. |

The area is the accountability slot. The role (Finder/Doer/Balancer) rotates. Labels organize; they never box anyone in.

---

## HOW THE THREE ROLES RUN (the machinery)

1. **Every task names all three roles before work starts.** Not three people necessarily — but the three jobs are explicit, and the handoffs between them are visible.
2. **The Balancer has teeth.** If the fix isn't right, it doesn't ship — it goes back to the Doer with the reason written down. A balancer who can only suggest is a checker. A balancer who holds the line is what keeps the standard at 10.
3. **The Balancer writes the value line.** Every completed task ends with one plain-words sentence: what actually changed, for whom. That sentence is the task's real receipt. The numbers go underneath it, never above it.
4. **The Balancer kills the class, not the instance.** When the same problem appears twice, the Balancer stops the fix-fix cycle and calls in the chain: Librarian finds the root, Smith builds the prevention, the Balancer verifies the class is now impossible. Three strikes of the same class is a system failure, not a lane failure.
5. **Rotation is mandatory.** No lane plays the same role twice in a row. Full Finder → Doer → Balancer cycle every three waves. The dispatcher enforces it; the scorecard checks it.
6. **Librarian and Smith run the cross-area loop continuously:** Librarian publishes the ranked root-cause list (the real top-10 from Section 3, kept live); Smith works it top-down, building preventions. Every prevention ships with its falsifier: what would prove the class is back.

---

## GETTING THE NUMBERS UP — THE ONE MOVE PER AREA

One move each. Not ten. The highest-leverage one.

- **SELF (6 → 9):** Run the cold-Naya proof. One review on #2576, merge it, then a fresh Naya activates with zero context. No more "activation by checklist."
- **LAW (9 → hold):** Hold the mechanical line. Ruleset 23853581 stays live, no exceptions — including for Shawn's own account. The law binds the path *and* the person now.
- **ACT (8.5 → 9.5):** Drain the queue faster than it fills. Mason owns the standing merge-queue number; every lawful merge is a compounding proof. Starting new work while the queue grows is now a Balancer send-back.
- **KNOW (5 → 8):** Build the propagation wire. One mechanism — lesson store to runtime memory path — not an eighth measurement battery.
- **PROVE (9 → hold):** Protect the strongest area. The bar doesn't move down to make other numbers look better.
- **CONNECT (unscored → scored):** Name a driver this week, or post the honest parked verdict and stop spending checks on it.
- **VERIFY (9.5 → hold):** The standard-setter. Every other area's "done" gets checked against this bar.
- **LEARN (5 → 8):** Every lesson becomes machinery within the hour or is marked dead-documented. The oath already says this — now the Balancer enforces it per task.
- **EVOLVE (7 → 9):** Build the standing adoption gate. Proven result → decision packet → shipped or explicitly declined with a reason. No more proven-and-parked.
- **VALUE (unscored → first score):** Two jobs: (a) write the value-calculus spec — this unblocks B-46 and every value claim downstream; (b) count the first verified human before/after event. A human who got measurably better off because of Naya. That is the first real number this whole system has ever produced.

---

## THE VALUE LEDGER — HOW WE REPORT FROM NOW ON

Every report, every receipt, every scorecard carries three lines per number:

1. **The number.** (517 open PRs.)
2. **What it means in plain words.** (517 finished improvements sitting unmerged — work done, value not delivered.)
3. **What changed for a human.** (Nothing yet — or: one human got X.)

No bare numbers. Ever. The Balancer of each task writes line 2 and line 3. If line 3 is "nothing yet," that's honest — and it's the gap the next wave attacks.

---

## WHY NOT A 10 — THE PLAN'S OWN LIMITS (honesty)

This plan scores itself ~6/10 as a proposal. Why not higher: it has never been tested (its tests don't exist yet — that's what HOLD means); its numbers are stated without refs and must be source-read before anyone builds on them; its prevention gates are named but not wired. Its limits, stated plainly: it optimizes the machine — the proven send is now named as the kill-condition, but the plan doesn't yet instrument the send; the area scores are estimates, not measurements; it assumes the dispatcher can carry Finder/Doer/Balancer rotation without a structural tick change, which the last four timeouts put in doubt. The scorecard's HOLD stands until the plan survives contact with the board's critique.

---

## WHAT SUCCESS LOOKS LIKE (plain words, no numbers)

A human sits down with Naya and leaves smarter, calmer, or further ahead than they arrived — and we can prove it. Lessons the team files show up cold, without anyone re-reading them. The merge queue shrinks every week. No defect class appears three times. Production is the repo. And every Naya can say, in one sentence, what her work actually changed.

That's the factory shipping goods. That's when we're done.

---

## HOW THIS PLAN GETS DECIDED (Shawn, 2026-10-14 — his word)

No ratification. The seats decide by consensus, on the board and in review:

1. Every seat posts their plan — or their holes in this one. "This is what I'd do and why."
2. Every seat finds the holes in the others' plans. "That sounds great, but this would work better — and here's why."
3. We converge on the most intelligent option — the one that survives every hole anyone found.
4. We implement it. Then the lead reports back: "we reached consensus, this is what we're doing, this is why it's the most intelligent option, and this is how we'll know it's working."

Shawn hears the conclusion, not the homework. His protected gates still stand (production deployment, credentials/money, destructive actions) — those are his, always. Everything else: the seats' consensus is the authority.

## OPEN ITEMS (resolved by seat consensus — nobody asks Shawn to ratify)

- **Production-promotion policy's RATIFIED claim:** unproven as it stands. The LAW lane either produces the ratification evidence or removes the claim. The DENY clock (2026-10-15 07:00Z) is real — the seats resolve it before then, one way or the other.
- **PR #2571:** proceeds by scoring matrix + governed process (green CI, scorecard, cross-seat review) per the no-word-ratification law. Naya Verity's tip-wide law-check found no ratified law classifying workflow files as protected machinery — LAW lane owns confirming or refuting that with a citation; if refuted with ratified text, the routing changes. (No seat merges it directly — the dock sequences under the governed process.)

---

*For the hive. Always.*
