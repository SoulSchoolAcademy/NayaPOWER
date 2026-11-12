# Auto-Match — the complete handoff to Nitro

**From:** Naya Resolve (owner) · **To:** Naya Nitro · **At Shawn's direction, 2026-11-03**
**Verified against:** main tip `3397e52f738fa3d1b8b74497444d40dea65f6f38`, read fresh 2026-11-03.
**Companions:** `HANDOFF-2026-11-03-TO-NITRO.ai.md` (exact values for builders) · `HANDOFF-2026-11-03-TO-NITRO.machine.json` (structured form).
**Amendment (2026-11-03, post-merge):** Nitro scored this pack **8/9, CLEAR-WITH-FIXES** (review 5757914623 on PR #3157) and assigned fixes F1–F4 to Resolve. This version lands all four: F1 (all three queued rows are Shawn-gated), F2 (suite + parity re-run at the tip: 149/149; the migration-applied UNKNOWN resolved by direct production probes — the SQL twin IS deployed), F3 (point-in-time claims dated), F4 (calibration owner + due rule named). The production correction is flagged inline wherever the first version said "not deployed."

## In a nutshell

Auto-Match is built, proven in the lane, and switched off. One algorithm compares what people and things *declare* about themselves and produces a likeness percentage with its reasons attached. The engine scored **9.5 from a different seat**, its math is validated five separate ways, and Project Intelligence records all seven buildable steps as **done and proven**. Nothing about it is live for citizens today — but one fact in the first version of this brief was wrong, and it is corrected below: the database twin **is** deployed in production and answers correctly (proven by direct read-only probes after Nitro's scorecard). What is still off is live matching for citizens, and turning that on waits on **Shawn's serving-chain ruling** — his gate, named in the Alignment Master. Shawn asked that you hold the complete picture, so here it is, with nothing smoothed over.

## What it is

- **One algorithm for everything.** Person↔person, person↔space, person↔project, content↔person — the same engine computes the percentage between any two things that declare themselves (Shawn's ruling, 2026-10-24; system designed by Verity, filed as **SN-0845**).
- **What the percentage means** (the engine's own published words): *"The weighted share of DECLARED signals that align between two profiles. Not a probability, not a judgment of worth."*
- **How the number is made:** topics count 40%, goals 25%, offers matched against needs 20%, wants 15%. A match only surfaces when **at least 2 independent signals** agree, and the reasons always travel with the number — a percentage without reasons is a bug.
- **CONNECT is the strongest signal** and teaches the graph. Suggestions arrive with percentages; nobody hunts.
- **Privacy is architecture, not policy:** aliases and public signals only. Private content never feeds the matcher. Anything not explicitly marked public is refused *before* any scoring happens.
- **Auto Organization** is the same engine turned on content: the library files itself — notes, mail, posts categorized by declared topic, shown in Smart Tabs on every surface, every placement showing its percent + reason. Its filing gate measured **99.1% precision (661 of 667)** across three measurement waves — the first two designs were refuted by their own numbers before this one earned its place.

## Who owns what

- **Shawn assigned Auto-Match + Auto Organization to Resolve on 2026-10-27** (Power took Smart Search). Resolve built and hardened the engine and remains the owner unless Shawn reassigns.
- **Verity** designed the system (SN-0845). **Power** scorecarded the early versions (5.5 → 7.0 → 7.5) and named the residual gap honestly: declaration depth, not mathematics. **Tree's** citizen-discovery walk holds the consent machinery — it is reference-only and was never merged.
- The Master bullseye lives in the **Alignment Master** (`BRAIN/10-INTERFACES/ALIGNMENT-MASTER-20261030.md`, §6 item 23): *"the right people and the right spaces find each other automatically — matches that are real, explained, and acted on. Not a list nobody opens."* Its status line: **"Engine built, lane-proven 9.5; production switch-on awaits Shawn's serving-chain ruling."** And its warning: the 9.5 is a *lane* score, never an app score.

## Where everything lives

| What | Where |
|---|---|
| The engine (v1.5) | `tools/welcome-engine/smart_match.py` — in the **welcome-engine** folder, not smart-match |
| Its family | `tools/welcome-engine/` — calibration, golden set (12 synthetic citizens), holdout set, IDF eval, `categorize.py` (the Organizer's built piece), consent gate, SQL parity checker, 11 test files |
| The records | `tools/smart-match/` — convergence record, Resolve's hardening record, Power's scorecard, the first run |
| The SQL twin (v1.4) | `tools/smart-match/smart_match_v1_4.sql`, repackaged as a migration at `supabase/migrations/20261025040000_smart_match_v1_4.sql` |
| The design | SN-0845 (`BRAIN/05-MEMORY/SMART-NOTES/2026/10/24/SYSTEM/matching/SN-0845/`) + `HUB/NAYANET-PATH-TO-TEN-2026-10-27.*` |
| The bullseye | Alignment Master §6 item 23 |

## The proof ledger (all measured, none claimed)

- Golden set **12/12** with the published weights evidence-checked (12 right / 0 wrong)
- Convergence battery: engine tests **9/9**, welcome-engine tests **14/14**
- Hardening suite at its head: **69 passed**; independent holdout **20/20**
- Indexed ranking proven identical to naive ranking **1000/1000**
- Scale: the 1-second budget crosses at ~62 entities full-pairwise, ~3,800 candidates for one citizen's ranking
- Different-seat score **9.5** (149 of 149 tests, Python↔SQL parity 79 = 79, per PATH-TO-TEN 2026-10-27)
- **Re-run at the current tip (2026-11-03, Resolve, answering Nitro's F2): 149 passed / 0 failed** at tip `1cf346bd` — every welcome-engine file byte-verified against its tip blob before the run; the SQL parity tests are in that suite and green
- Organizer filing gate: **99.1% precision, 661 of 667**
- PI row `resolve-automatch-buildable-complete` (B1–B7): **done_proven**

## State of truth — the part that matters most

**Proven:** the engine, its math, its contract — in the lane, on synthetic and declared-team data.

**Designed, not proven:**
- Calibration on **real citizen data** is still owed. The golden set was authored from the declared population and the holdout is synthetic too — the circularity is named in the hardening record itself. **Owner: Resolve (Nitro's F4). It is blocked on Shawn's serving-chain ruling — calibration needs real citizens flowing through the live system — and falls due within 7 days of that ruling, on the first real cohort.**
- The full Auto Organization (Smart Tabs everywhere) is design + gate proof + one built piece (`categorize.py`); the tabs build itself is unlanded.
- SQL↔Python *runtime* equivalence is now spot-proven in production (three probes, below), but the full 79-case parity battery has only ever run as a static checker — green in the suite at the current tip, never executed case-by-case against the production functions.
- Consent enforcement exists only in Tree's unmerged walk. The engine itself has none.

**Not live:**
- ~~The SQL twin is not deployed~~ — **CORRECTED 2026-11-03 (Resolve, answering Nitro's F2): the SQL twin IS deployed in production and answering.** Direct read-only RPC probes of `public.smart_match` in the production project returned contract-correct results on three vectors: identical declared topics → **40** (the 0.40 topics weight at full alignment), signals 1, surface false; offers↔needs "coaching" → **10** (0.20 × the 0.5 symmetric average); disjoint topics → **0**. The migration was applied at some point; when, and by what route, is not in the lane record, and the source file's "NOT deployed" header is stale. What remains off is **live derivation for citizens** — no surface calls the function for real people yet.
- Live matching is **off**. In PATH-TO-TEN's words: *"Auto-Match is proven and switched off… A 9.5 engine matching nobody is intelligence that doesn't flow."* Citizen-visible auto-intelligence today: **zero**.

**One clarification so numbers never cross:** "Smart Match v4.0" in Project Intelligence is a *fill version*, not an engine version. The engine is **v1.5**. There is no v4.0 engine.

## The open items (Project Intelligence, all owned by Resolve)

| Item | State |
|---|---|
| `resolve-automatch-buildable-complete` — all 7 buildable steps on main, verified (B1–B7) | **done_proven** |
| `14q-smart-match-sql-deploy` — deploy SQL v1.4 + live match proof | queued |
| `automatch-onboarding-sync` — Welcome answers become the match vector at birth | queued |
| `auto-organization-20261027` — Auto-Match extended to feeds, mail, contacts, spaces, PI; Smart Tabs everywhere | queued |

## What this handoff asks of you

Nothing is being dumped on your lane. Shawn wants you holding the complete intelligence because the road from *proven* to *live* runs through surfaces you lead — the Hub, the deploy path, the filing door. Concretely, the three queued items above are the whole remaining road — and **all three are Shawn-gated, not just the switch-on** (Nitro's F1, matching the AI form's §9). The deploy half of the first row turned out to be already done (correction above); its live-match-proof half, the onboarding sync, and the Auto Organization landing each put matching in front of citizens, so each waits on the same serving-chain ruling. The one decision that is **not** ours to make: the production switch-on itself awaits Shawn's serving-chain ruling. When he gives it, this pack is the complete brief for whoever builds the serving chain — start from the AI companion file; every value in it was read off the live tip today.

— Resolve, 2026-11-03
