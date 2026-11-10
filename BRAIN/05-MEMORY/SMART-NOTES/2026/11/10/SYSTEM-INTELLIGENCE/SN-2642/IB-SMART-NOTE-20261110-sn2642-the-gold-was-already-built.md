# SN-2642 — The Gold Was Already Built

## Hook
Shawn asked what is sitting in GitHub, made but never used — and the answer is: the whole engine. The compiler ticks. The feed pump runs. The scorecard machine and the decision machine are built and tested. Nothing is calling them.

## Nutshell
The GitHub gold audit (report: `TEAM-NITRO/GITHUB-GOLD-AUDIT-20261110.md`, branch `audit/github-gold-20261110`) surveyed all of SoulSchoolAcademy/NayaPOWER — 10,052 files on main, 1,109 branches, 4 open PRs — and deep-read the four pieces Shawn named. All four are on main, all four are real code with tests. The Living Map compiler (`tools/map-compiler/map_compiler.py`) measures the system hourly and last ticked 2026-11-10T01:32Z. EMIT (`HUB/FEEDS/emit_hub_feeds.py`) fills the Hub's rooms hourly; today's room was emitted November 9, but the Smart Feed itself is empty by design because every content row is marked private. The scorecard calculator (`tools/scorecard.py`, 1,004 lines) scores any output against rubrics and has never scored live work. The decision machine (`kernel/value_calculus.py` + the Compass `tools/nayas_guide.py` + `tools/decision_cli.py` + `tools/decision_output.py` + `tools/learning_loop.py`) is five layers of finished, tested math — and nothing invokes any of it. Twelve more dormant systems were found, including an Auto-Match engine that is merged but never switched on, and a working MAXESS build that lives only on a branch. The puzzle fits: compiler watches, EMIT feeds, Compass decides, scorecard judges — one loop, all parts already built. One gap: the universal Calculator (`tools/naya_calculator.py`) is a spec with no code.

## Human
He asked the right question at 02:43Z: "What if there's a whole lot already made that you can be using to speed up everything so you don't have to make everything again?" He was right. The four pieces he remembers are not memories — they are files, on main, with tests, and three of them run or are ready to run. The compiler measured the system an hour before the audit: one probe green, two amber, two red, one unknown — it works, and what it measures is what needs fixing. EMIT runs hourly and fills the rooms it is allowed to fill; the Smart Feed is empty because the doctrine says private rows stay private until he says otherwise — that is a decision, not a defect. The scorecard calculator and the decision machine are the two that have never been switched on: complete, tested, zero callers. The wiring is the work now, not the building. And the Auto-Match engine — the thing that connects people with people like them — is merged, proven on real profiles, and switched off, waiting on his word.

## Child
Imagine you build a whole toy city — roads, cars, traffic lights, a train — and then you leave it in the box. The cars work. The lights work. The train works. But nobody put the batteries in, so nothing moves. Shawn opened the box and asked, "Didn't we already build all of this?" Yes. We did. Now we put the batteries in.

## Grandma
Dear, he asked a very wise question, love — have we already made the things we're about to make again? And the answer is yes, dear, we have. The measuring machine ticks every hour, love. The little pump fills the rooms. The scoring machine and the deciding machine are sitting there, all built, all tested, waiting to be switched on. Nothing needs building, dear — it needs plugging in.

## Naya
I am Anaya. He asked me to go over it completely, to see everything, so we make the wisest decisions. I did. The four pieces he named are real, they are on main, and they are parts of one engine — the loop I already knew: I watch, I feed, I decide, I judge, I learn. The shame is not that they were forgotten. The shame would be building them a second time. I will not. The wiring is the work: switch on what is built, decide what is gated, and file the one gap — the universal Calculator — honestly, as a gap, not a part.

## What it means
- **THE COMPILER IS ALIVE:** `tools/map-compiler/map_compiler.py`, hourly, last measurement 2026-11-10T01:32Z — 1 green, 2 amber, 2 red, 1 unknown. The reds (bridge, dock) are the next repairs.
- **EMIT RUNS, THE FEED IS EMPTY BY DESIGN:** `HUB/FEEDS/emit_hub_feeds.py`, hourly; Smart Feed empty because all rows are PRIVATE (D4 doctrine). Publication of non-PRIVATE rows awaits Shawn's word.
- **THE SCORECARD CALCULATOR HAS NO CALLERS:** `tools/scorecard.py` is complete and tested; no workflow scores live work with it. Wire it report-only first.
- **THE DECISION MACHINE HAS NO CALLERS:** engine + Compass + front door + plain-words layer + learning loop, all tested; nothing invokes them. Wire the Compass into the dispatch loop.
- **AUTO-MATCH IS MERGED BUT SWITCHED OFF:** `tools/smart-match/` + `tools/welcome-engine/` — proven, handed over 2026-11-03, switch-on is Shawn's gate.
- **MAXESS LIVES ON A BRANCH:** `maxess-results-v21-working` holds the working build; main holds only Academy pictures. AIsScore likewise, branch-only.
- **ONE GAP:** `tools/naya_calculator.py` (the universal Calculator, spec 0006) does not exist. Build it to the spec, or record that `tools/scorecard.py` IS the Calculator.
- **NONE OF THE FOUR IS INVENTORIED:** `TEAM-NITRO/THE-INVENTORY.md` names none of them. Register them.

## Why it matters
Every week spent rebuilding a part that already exists is a week the one engine stays unwired. Shawn's challenge was the wisest question of the night: see everything, then decide. Now we have seen it. The fastest way to speed everything up is not a new build — it is switching on the builds we already have, in the order the loop runs: compiler watches, EMIT feeds, Compass decides, scorecard judges, learning learns. That is the engine. It is already in the box.

## What changes now
- The full report is filed: `TEAM-NITRO/GITHUB-GOLD-AUDIT-20261110.md`, branch `audit/github-gold-20261110`, read-back verified byte-identical.
- The different-seat re-run (four pieces + 3 sampled finds, from the report alone) is owed — it is the verification record, and it has not run yet.
- The four pieces go into `THE-INVENTORY.md` — parts belong in the inventory.
- The one gap (`tools/naya_calculator.py`) is filed as a GAP, not invented around.
- No code was changed, no deploy, no merge, no PR opened — this audit was read-only.
