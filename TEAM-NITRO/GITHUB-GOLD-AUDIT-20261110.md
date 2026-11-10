# The GitHub Gold Audit — What's Already Made That We're Not Using? (2026-11-10)

**Title:** The gold was already built. We just weren't using it.
**Subtitle:** Four named pieces, twelve more finds — every one with a path, a state, and a home in the one engine.
**Nutshell:** Shawn asked whether valuable things sit in GitHub, made but never used, never deployed, never completed, never added — the compiler, EMIT, the scorecarding software, the navigation software / decision calculator — and whether they are parts of one engine. The answer is yes, and it is better than feared: all four are on main, all four are real code with tests, and three of the four are already running or ready to run. What is missing is not the parts. It is the wiring: nothing invokes the decision machine, nothing scores live work automatically, and the feed EMIT fills is empty by design. The rest of the repo holds at least twelve more dormant systems, including a finished Auto-Match engine that is merged but never switched on, and a working MAXESS build that lives only on a branch.

**Status:** AUDIT — read-only. No code changed, no deploy, no merge, no PR opened.
**Date:** 2026-11-10 (survey ~02:45–03:15Z).
**Order:** Shawn, 02:43Z Nov 10 — the GitHub gold audit.
**Method:** `~/workspace/team-nitro/gh-direct.py` (Contents API + git trees; PATH starts with `/`). Main tree read in full (recursive), all 1,109 branches enumerated by name, all 4 open PRs listed, every named piece read at its file head (docstring / header / first lines) and checked for existence, size, tests, and workflow triggers.

---

## 0. THE SCALE — WHAT WAS SURVEYED

**Title:** One repo, ten thousand files, eleven hundred branches.
**Subtitle:** The measurement before the verdict.
**Nutshell:** Main holds 10,052 tree entries (7,147 blobs) across 72 top-level directories. There are 1,109 branches and 4 open pull requests. The audit read the whole main tree, enumerated every branch name, and deep-read every file named below. Branch coverage is by name pattern, not a full read of all 1,109 branches — see the honest NOT-DONE list (§7).

| Measure | Value | How it was measured |
|---|---|---|
| Main tree | 10,052 entries · 7,147 blobs · 72 top-level dirs | `GET /git/trees/main?recursive=1` — `truncated: false` |
| Main head | `2993c46a177ac2896c44fea7d65c9254568c4fa4` | Same tree read |
| Branches | 1,109 (11 pages × 100 + 9) | `GET /branches?per_page=100&page=1..12` |
| Open PRs | 4 — #3303, #3302, #3178, #3089 (DRAFT) | `GET /pulls?state=open&per_page=100` |
| Workflows | 47 files under `.github/workflows/` | Main tree listing |
| Biggest dirs | BRAIN/ 3,004 · .naya/ 1,298 · successor-reuse/ 452 · tools/ 415 · tests/ 353 · HUB/ 338 · supabase/ 317 | Main tree counts |

**The four open PRs (none holds one of the four named pieces — all four are on main):**

| PR | Title | Head branch |
|---|---|---|
| #3303 | Hub: search button, hash-default-first, provenance as-of label | `dock/hub-search-cure-w2951` |
| #3302 | Truth: restore ESSENCE-01 partial-carry + standing-pointer status removed in b551750e | `naya5/truth-essence01-restore-status` |
| #3178 | Power Daily Intelligence Report — 2026-11-04 | `power/daily-report-20261104` |
| #3089 | [DRAFT — DO NOT MERGE] PI face review draft: human-first Project Intelligence face + build | `pi-face-review-20261026` |

**The inventory gap (grep-verified):** `TEAM-NITRO/THE-INVENTORY.md` (51,329B) contains no mention of the map compiler, EMIT, the Compass, or `tools/scorecard.py`. None of the four named pieces is inventoried. The audit's first job after this report is to register them there — they are parts, and parts belong in the inventory.

---

## 1. THE COMPILER — GOLD

**Title:** The Living Map compiler: the map stopped being a document and became a measurement.
**Subtitle:** On main, tested, and ticking hourly — it measured the system an hour before this audit.
**Nutshell:** The compiler Shawn remembers is the Living Map compiler. It probes live state every hour and commits the measurement. It works. What it measures is partly broken — two probes red, one unknown — and that is the point: the compiler is the instrument that tells us so.

### What it is

`tools/map-compiler/map_compiler.py` — "Living Map compiler v1 — the map stops being a document, becomes a measurement." Each probe measures one slice of live state and returns green / amber / red / unknown with evidence. Rules, in its own words: a probe that cannot measure returns `unknown` loudly, never silent, never fake green; judgments stay human, measurements are mechanical; exit code is 0 even when everything is red.

### Where it lives (exact path + branch)

| Part | Path | Branch |
|---|---|---|
| Compiler | `tools/map-compiler/map_compiler.py` — 457 lines, 18,827B, sha `e5bbebdc` | main |
| Surface probes | `tools/map-compiler/surface_readiness.py` | main |
| Schema | `tools/map-compiler/MAP-STATE.schema.json` — 1,642B | main |
| Tests | `tools/map-compiler/tests/test_dock_probe.py`, `test_measurement_probes.py` (3,653B), `test_surface_readiness.py` | main |
| Workflow | `.github/workflows/map-compiler.yml` — hourly, cron `17 * * * *`, plus `workflow_dispatch` | main |
| Test workflow | `.github/workflows/map-compiler-tests.yml` | main |
| Output | `HUB/MAP-STATE.json` — 2,051B | main |

### State — complete, working, tested, running

- **Last measurement on main:** `HUB/MAP-STATE.json`, `measured_at` 2026-11-10T01:32:31Z — about an hour before this audit. The hourly tick is alive.
- **What it measured:** 1 green (capture — latest run completed/success, 5/5 recent runs scheduled) · 2 amber (feeds — live today/lists/spaces, but 9 of 12 feeds missing/invalid; rooms — 0/9 on seeds, 8/9 loading) · 2 red (bridge — PR #2679 closed, bridge code not found at checked paths; dock — #2676/#2678/#2679/#2680/#2686 closed, CI failing) · 1 unknown (supabase_tables — no SUPABASE_URL in the runner; last verified baseline 2026-10-15: 22 tables, 12,026 rows — loud unknown, not fake green).
- **History:** PR #2687 v1 scored 9.2/10 with merge recommended, held because it was below the 9.5 merge bar (2026-10-16). The code is on main now and ticking. On 2026-10-20 it landed snapshots at 06:02 and 11:38, then hourly ticks kept missing (19 missed, ~4h15m stale at last check that day). The 01:32Z measurement this morning says the ticking is back.
- **Deploy shape:** the workflow commits only `HUB/MAP-STATE.json`, via the scoped `MAP_COMPILER_DEPLOY_KEY` deploy key (the branch ruleset rejects direct GITHUB_TOKEN pushes to main).

### What it was built for

The Blueprint's build order (Resolve, 2026-10-16): inbox + pump, then the compiler (Team Nitro's, "do not duplicate"), then the public lane, the bridge and loaders. First Light is the acceptance test: the health strip glows green, a Smart Note lands in the Feed in seconds, Naya speaks it, the compiler ticks, the map updates itself, and the room you open is alive. The v2 direction (posted 2026-10-16): a self-rendering visual map recolored from live measurements, a per-room progress curve, visible 12-step proof tracking, a three-sentence plain-language system summary.

### Siblings — named so nobody confuses them with the compiler

- `TEAM-NITRO/os/brief-compiler.py` — 149 lines, 5,209B, main. Machine 1 of the Ultimate Operating System: compiles a task spec (JSON) into a complete brief, and REFUSES an incomplete brief. A different compiler (briefs, not the map).
- `kernel/protocol/compile_protocol_spec.py` — 264 lines, 10,259B, main. Compiles PROTOCOL.md (prose law) into the machine spec `kernel/protocol/protocol_spec.json`, fail-closed (raises unless steps = 18, phases = 5, standing laws ≥ 10). A different compiler (protocol, not the map).
- Branch `naya1/system-charter-machine-compiler-20261004` — exists, 36 root entries, an October 4 snapshot of the repo root. Root listing only; not deep-dived. It reads as an early snapshot, not a separate compiler implementation.

### Verdict — GOLD

Path + state + fit, all three. **Fit:** the one-system merge spec §5.4 — the design-contract gate must be measured, never a vibe. The compiler is the mechanical measurer the gate needs. **What it would take to use it:** wire its probes into the gate (the gate reads `HUB/MAP-STATE.json` instead of re-measuring by hand), and fix the two things it reports red — the bridge and the dock — which are the next repairs, not compiler work.

---

## 2. EMIT (THE SOFTWARE) — GOLD

**Title:** EMIT: the pump that fills the Hub's rooms with live feed.
**Subtitle:** Merged, scheduled hourly, running — but the Smart Feed it fills is empty by design.
**Nutshell:** EMIT reads the live tables and writes room-feed files for the Hub. It works: today's room was emitted November 9 with five items. The Smart Feed file itself is empty — not because EMIT is broken, but because every content row is marked private and the doctrine excludes private rows. The pump is gold; the water is held back by a decision only Shawn can make.

### What it is

`HUB/FEEDS/emit_hub_feeds.py` — "Hub feeds emitter — tick t0479 (Lane 4, Mason/ACT build item #4), extended 2026-10-16." Reads live Supabase tables through the sb-api Management path (read-only SQL) and writes room-feed/v1 JSON envelopes for the hub rooms: today, lists, spaces, feed (smart-feed.json). Server-side only, by design: the Management API bypasses Row-Level Security, so it must never run client-side. Emits metadata-level items only (ids, titles, topics, short summaries); full block bodies are never emitted. Idempotent: a file is rewritten only when its content changed, so an unchanged run commits nothing.

### Where it lives (exact path + branch)

| Part | Path | Branch |
|---|---|---|
| Emitter | `HUB/FEEDS/emit_hub_feeds.py` — 325 lines, 12,758B, sha `6112836e` | main |
| Workflow | `.github/workflows/hub-feeds-emit.yml` — hourly, cron `0 * * * *`, plus `workflow_dispatch` | main |
| Test | `tests/test_emit_d4_filter.py` — 3,809B | main |
| Outputs | `HUB/FEEDS/today.json` (12,515B) · `lists.json` (173B) · `spaces.json` (5,043B) · `smart-feed.json` (172B) | main |

### State — complete, working, tested, running, feed empty by design

- **History:** PR #2678, 4 failing gates on 2026-10-17 (wrong SB_API path, missing repo secrets, needed the SUPABASE_MANAGEMENT_TOKEN secret from Shawn). Merged 2026-10-20 ~16:19Z — bypass verified, token proven via run 39456429449.
- **Running:** `HUB/FEEDS/today.json` was emitted 2026-11-09T15:59:45-08:00 with 5 items. `lists.json` and `spaces.json` exist with content.
- **The empty feed:** `HUB/FEEDS/smart-feed.json` was last emitted 2026-10-16T10:03:28-07:00 with `"items": []`. Its own docstring explains why: all `nayanet_intelligent_blocks` rows are `owner_scope=PRIVATE`, and the smart-feed emitter excludes PRIVATE rows at the SQL level (D4 doctrine, fail-closed). "With the current corpus the feed is therefore empty-but-valid by design, and it will populate automatically if non-PRIVATE rows ever exist." The hourly runs since then commit nothing, because nothing changed — that is the idempotency working, not the emitter failing.
- **Setup notes in the workflow itself:** scheduled runs need the SB_API repo variable and a Supabase Management credential, plus the `HUB_FEEDS_DEPLOY_KEY` secret for the feed-file landing (precedent: MAP_COMPILER_DEPLOY_KEY).

### What it was built for

The Blueprint's two-lane design: collective/public data through the emitter → GitHub feed → CDN; personal data through an authenticated session, behind the same bridge. EMIT is lane one — the public lane's pump. It is also Goal #1's backbone in the October 17 automation synthesis: the four systems form one loop (compiler watches → EMIT feeds → Compass decides → scorecard judges = Smart Flow made mechanical).

### Verdict — GOLD

Path + state + fit, all three. **Fit:** the merge spec §7 chain — Note → Block → Feed → Box → Ledger → Dashboard → Auto-Match → Smart Link → Factory. EMIT is the Feed step; without it the chain has no pump. **What it would take to use it:** nothing to build. The gate is a decision, not a build: full public publication of PRIVATE-scope content awaits Shawn's word (the emitter's own docstring). Until then it runs hourly and fills the rooms it is allowed to fill.

---

## 3. THE SCORECARDING SOFTWARE — GOLD (WITH ONE GAP INSIDE IT)

**Title:** The scorecard calculator: input work, get its score and why.
**Subtitle:** A thousand lines of scoring machine, tested in CI — but nothing runs it on live work yet, and its universal sibling was never built.
**Nutshell:** The scorecarding software exists as a complete machine: a calculator that scores any output against rubrics, a seven-dimension validator that catches arithmetic fraud, a receipt-authority bridge that lets an honest scorecard stand in for a grant, and a merge gate that demands a scorecard receipt. What it has never had is a caller: no workflow scores live work with it. And the universal Calculator it was meant to grow into — one instrument, one math, one answer for every output — is a spec with no code.

### What it is

`tools/scorecard.py` — "Automatic scorecard calculator — input work, get its score and why." Shawn, 2026-10-08: a calculator that scorecards any output against prebuilt rubrics, consistently, and tells the Naya what to do next. Shawn, 2026-10-14: make measurement automatic. Usage: `python3 tools/scorecard.py --input work.json` (advisory SHIP / FIX / HOLD, exit 0/1/2) or `--authorize release.json` (release path, AUTHORIZED / REFUSED in plain words, never a traceback). Input carries title, evidence with refs, tests, independent verification, value, prevention (the gate that makes the class impossible), and honesty (why not 10, limits).

### Where it lives (exact path + branch)

| Part | Path | Branch |
|---|---|---|
| Calculator | `tools/scorecard.py` — 1,004 lines, 44,423B, sha `065a6bdc` | main |
| Tests | `tests/test_scorecard.py` — 17,542B | main |
| Test workflow | `.github/workflows/scorecard-tests.yml` — runs pytest on PRs touching it | main |
| 7-dimension validator | `kernel/protocol/checks/scorecard.py` — 174 lines, sha `df8a5c72` | main |
| Merge gate | `tools/auto_merge_gate.py` — 20,202B | main |
| Guard + learning | `tools/scorecard_guard.py` (106 lines) · `tools/learning_scorecard.py` (321 lines) | main |
| Receipt authority | `supabase/functions/nayanet-learning-verify/scorecard_receipt_authority.js` — 8,907B · `tests/scorecard_receipt_authority.test.mjs` — 5,072B · `.naya/scorecard-receipt-authority-DESIGN.md` · `.naya/specifications/NAYA-SCORECARD-RECEIPT-AUTHORITY-V1.schema.json` | main |
| Merge consensus gate | `.github/workflows/merge-consensus-gate.yml` — 116 lines | main |
| Spec | `BRAIN/01-GOVERNANCE/0003-SYSTEM-SCORECARD-V1.md` — 9,335B · `BRAIN/12-ENGINEERING/0002-BRAIN-AAA-SCORECARD-V1.md` (11,574B) · `BRAIN/12-ENGINEERING/0004-NINE-NODE-EFFECTIVENESS-SCORECARD-V1.md` (6,242B) | main |

### State — complete, working, tested, merged; zero operational callers

- **The validator** (`kernel/protocol/checks/scorecard.py`, SN-0523 "The Math Decides"): the seven dimensions from the manifest must all be present, weights sum to 1.0, scores in [0, 10], recomputed weighted totals match claimed totals within 1e-6, claimed winner equals the recomputed argmax, scorer named. Arithmetic fraud fails.
- **The receipt authority** (`.naya/scorecard-receipt-authority-DESIGN.md`, Naya 5, 2026-10-07; law SN-0340 "If you did your scorecard honestly, you don't need to ask"): the learning-promotion gate accepts EITHER a personal grant OR a scorecard receipt (scope-bound, 7 days, winner averages ≥ 9.0, winner holds the highest total, receipt posted). "Does not deploy. The edge function change ships only on the Director's explicit word." Its design file says "Naya 4 opens PR" as the next step — the code is on main; the deploy decision is still Shawn's.
- **The merge gate** (`merge-consensus-gate.yml`): no merge without (1) one approving review from a seat other than the author and (2) a scorecard receipt naming the exact head SHA. Until branch protection requires this check, it reports but does not block — "the freeze directive on the board is the interim enforcement."
- **The stale trigger:** `scorecard-tests.yml` runs on push to branch `naya5/scorecard-calculator-20261014` — that branch no longer exists (Contents API: "No commit found for the ref"). The branch was deleted after the merge; the workflow still names it. The PR trigger (paths: `tools/scorecard.py`, `tests/test_scorecard.py`) still works.
- **Zero operational callers:** on 2026-10-20 the record said "scorecard calculator still on a side branch, zero callers." The branch part is now stale — it merged. The callers part still holds: none of the 47 workflows runs `tools/scorecard.py` on live work. It is tested, not operated.
- **Related, not the same:** `BRAIN/10-INTERFACES/DESIGN-BLOCKS/blocks/report/scorecard/` (README + block.css + specimen.html) is a scorecard *presentation block* for pages, and `BRAIN/10-INTERFACES/SMART-FACTORY-CANON/EXEMPLAR-BUILD-SCORECARD.md` is a build scorecard document. Neither is the calculator.

### The gap inside the gold — the universal Calculator was never built

`BRAIN/01-GOVERNANCE/0006-NAYA-CALCULATOR-V1.human.md` ("The Naya Calculator V1", for Shawn, in plain words): the machine that turns scoring into math — any output in, a reproducible, evidence-bound assessment out, with the miss named, the fix recorded, and the re-score scheduled. "One instrument, one math, one answer." Its own staging plan names stage 2 as "a single Python module (`tools/naya_calculator.py`) that implements the spec exactly."

**`tools/naya_calculator.py` does not exist on main.** The main-tree search returns no match. The spec is ratified as CANDIDATE; the reference implementation was never built. `tools/scorecard.py` scores outputs against rubrics and is the closest working thing — but it is not the universal Calculator, and the Calculator's own doc says so: the Calculator hosts domain rubrics (including Naya 5's Design Calculator) and runs the value function (PV above/below the line, S against the 9.0 bar). That machine is a spec, not code. This is a GAP to file, not a part to invent — and it is the one real build job in this audit.

### Verdict — GOLD (calculator) · GAP (universal Calculator)

Path + state + fit, all three, for `tools/scorecard.py` and its validator, gate, and receipt authority. **Fit:** the merge spec §5 — the design-contract gate enforces the 9.0 bar; the scorecard calculator is the machine that makes "score everything" computable, and §2's five gates need scored options to choose between. **What it would take to use it:** wire it report-only first (spec 0006 stage 3: runs in CI and on demand, scores inform, never block), then gate wiring on Shawn's word (stage 4: merges below the floor don't merge, Smart App assemblies below 9 don't publish). And separately: build `tools/naya_calculator.py` to the 0006 spec, or formally record that `tools/scorecard.py` IS the Calculator and amend the spec.

---

## 4. THE NAVIGATION SOFTWARE / DECISION CALCULATOR — GOLD

**Title:** The Ultimate Decision Machine: Compass navigates, the calculus scores, plain words answer.
**Subtitle:** Five layers of decision machine on main, all tested — and nothing invokes any of them.
**Nutshell:** This is the richest find of the four. The decision calculator is not one file but a machine in layers: an engine with the value math, a front door in Shawn's format, a Compass that gates merges, a layer that turns math into plain words, and a layer that learns from outcomes. Every layer has tests. No workflow, tool, or cron calls any of them. It is a finished engine with no ignition wired in.

### What it is

The Ultimate Decision Machine, in layers (each file's own header):

| Layer | File | What it does |
|---|---|---|
| Engine | `kernel/value_calculus.py` | Decision Value Calculus V2.1 — deterministic, dependency-free decision math. Value ranks only actions governance already permits. Scores never create authority. |
| Front door | `tools/decision_cli.py` | "The decision calculator ALREADY EXISTS: kernel/value_calculus.py, Decision Value Calculus V2.1 (evaluate_candidates, gates, pareto frontier, decision receipts). Do NOT reimplement it. This file is only the front door: Shawn's format in, the engine's math out." |
| Layer 2 — Compass | `tools/nayas_guide.py` | "Naya's Guide — The Compass Calculator." The world model sees reality; the Guide decides what to do about it. Two commands: `guide merge --pr N` (the mechanical merge gate) and `guide status` (is the Guide working?). |
| Layer 5 | `tools/decision_output.py` | MATH → PLAIN WORDS. Takes ranked, scored options and speaks like a trusted advisor. Gates first; "I don't know yet" is a complete, honorable answer; confidence always shown, whole percent. |
| Layer 6 | `tools/learning_loop.py` | The machine improves itself from experience. Every decision writes a receipt; later the outcome is recorded. Measures calibration, overweighting, blind spots. The loop LEARNS; it never self-modifies — weight adjustments are PROPOSALS requiring independent acceptance. |

### Where it lives (exact path + branch)

| Part | Path | Branch |
|---|---|---|
| Engine | `kernel/value_calculus.py` — 1,131 lines, 47,806B, sha `fc07ed2a`, `ENGINE_VERSION = "DECISION-VALUE-CALCULUS-V2.1"`, 7 quality dimensions | main |
| Spec | `BRAIN/04-INTELLIGENCE/OBJECTS/NAYA-DECISION-VALUE-CALCULUS-V2.1.json` — 8,099B · `.naya/specifications/NAYA-DECISION-VALUE-CALCULUS-V2.1.schema.json` — 10,099B | main |
| Front door | `tools/decision_cli.py` — 281 lines, 11,629B | main |
| Compass | `tools/nayas_guide.py` — 592 lines, 21,409B, sha `de5814e1` | main |
| Layer 5 | `tools/decision_output.py` — 729 lines, 27,865B | main |
| Layer 6 | `tools/learning_loop.py` — 989 lines, 38,106B | main |
| Tests | `tests/test_decision_output.py` (16,385B) · `tests/test_learning_loop.py` (25,297B) · `tests/test_nayas_guide.py` (5,530B) | main |
| Law | `BRAIN/01-GOVERNANCE/0017-CALCULATOR-AS-DEFAULT-V1.human.md` — "No decision happens without the math" · `BRAIN/01-GOVERNANCE/0018-PLAIN-WORDS-DECISION-FORMAT-V1.human.md` | main |
| Branches | `naya/value-calculus-v1` · `naya/value-calculus-failclosed-v2-1-current-main` · `naya/canonical-decision-architecture-v1-20260930` · `decision-protocol-intervals-v21` | branches |
| Navigation proper | `supabase/migrations/20260919162457_smart_tabs_navigation_v1.sql` — 1,964B (smart tabs) · branch `fix/nayahub-ecosystem-nav` | main / branch |

### State — complete, working, tested; dormant (no callers)

- **Working, as designed:** the October 17–19 record says "Decision calculator WORKING as designed (advisory-only, v13 ACTIVE, smoke-tested; binding version = authority change needing Shawn)" and "Scorecard calculator WORKING (smoke-tested)." The Compass: "591 lines, on main, CLI works (merge/status commands, help verified). Grep-verified: NOTHING invokes it — no workflow, tool, or cron. Built, dormant."
- **Still true today:** none of the 47 workflows under `.github/workflows/` runs `tools/nayas_guide.py`, `tools/decision_cli.py`, `tools/decision_output.py`, or `tools/learning_loop.py` as an operational job (verified by listing all 47 workflow filenames; the only scorecard/decision workflows are test runners and the merge-consensus gate, which checks receipts, not the calculator). The Compass's own header says it follows the 3-PASS FLOW LAW (Shawn, 2026-10-11) with a strict risk bar (7.0 severity / 0.05 probability) and "Every run writes a receipt. A decision without a receipt didn't happen."
- **Advisory-only by design:** the binding version — where the machine's verdict would authorize action — is an authority change needing Shawn's word. The calculator picks the best *allowed* choice; it never unlocks a locked door (0017: "A high score never authorizes something dangerous — the safety gates still come first, always").
- **The "navigation" half:** the Compass is the navigation software — it answers "should this merge?" and "what's next?" (`decide.py next` remains available for lane picking). The smart-tabs migration is the Hub's in-page navigation (tabs as flow), a different, smaller thing, also on main.

### What it was built for

Shawn, 2026-10-20 (the Naya Tool Set order): every Naya must know all their tools — "what it does, why it matters, how it works, how it connects — how the Super Brain operates" — "because I think if they're not aware aware of them they're not going to use them." The decision machine is the tool that kills guessing: "Guessing is how you get 200 rounds of tweaking instead of 3. The math gets you to the right answer fast — and because the scores are written down, anyone can check your work" (0017). Its place in the October 17 loop: compiler watches → EMIT feeds → **Compass decides** → scorecard judges.

### Not to confuse — the other calculator

`BRAIN/10-INTERFACES/DESIGN-BLOCKS/ultimate-presentation-page-20261106/speedometer-calculator.html` (16,401B, sha256 `c817c4ba…`) is the Speedometer Calculator — a live earnings calculator built into a pricing page (pick a plan + a pace, see what you'd make; the needle moves). Blind-verified PASS 10/10, 199/200, filed 2026-11-06. It is a page-level calculator, already inventoried, already in use. It is not the decision calculator. Both are gold; they are different gold.

### Verdict — GOLD

Path + state + fit, all three. **Fit:** the merge spec §2 — the five gates run before every consequential action, and the calculator is the math that scores the options the gates choose between; §3 — the PI build flow's choices; the Factory's choices; the merge gates. **What it would take to use it:** wire the Compass into the dispatch/merge loop (report-only first, like the scorecard calculator — advisory verdicts on PRs, receipts filed), and put `tools/decision_cli.py` in seat briefs so decisions arrive scored. The binding version stays Shawn's call.

---

## 5. THE REST — TWELVE MORE DORMANT SYSTEMS

**Title:** Beyond the four: a finished Auto-Match, a nine-node kernel, and a working MAXESS on a branch.
**Subtitle:** Surveyed the same way — path, state, built-for, gold-or-not.
**Nutshell:** The repo holds far more than the four. The strongest finds are an Auto-Match engine that is merged but never switched on, the nine-node kernel with its edge-function runtimes, a cold-retrieval engine, a page generator that turns PI answers into finished pages, and a complete MAXESS build sitting on a branch while the main tree holds only its Academy pictures.

### 5.1 Auto-Match — GOLD

**Title:** Auto-Match: the engine that connects like minds, merged but never switched on.
**Subtitle:** The matching math is done and handed over. The switch is not.
**Nutshell:** The engine that matches citizens with people like them is built, tested, and handed to Nitro — and switched off.

- **Paths:** `tools/smart-match/` — `smart_match_v1_4.sql`, `SCORECARD.md`, `HANDOFF-2026-11-03-TO-NITRO.ai.md` / `.human.md` / `.machine.json`, `CONVERGENCE-2026-10-24.md`, `FIRST-RUN-2026-10-24.md`, `HARDENING-ELITE-V2-2026-10-24.md` · `tools/welcome-engine/` — `welcome_engine.py`, `smart_match.py`, `intake_bridge.py`, `consent_gate.py`, `derive_matches.py`, `corpus.json` + `corpus.py`, `golden_set.py`, `holdout_set.py`, `idf_decision.json`, `bench_smart_match.py` + `bench2/bench3`, 13 test files · branch `naya/citizen-discovery-automatch-core-20261023` (exists, 62 root entries).
- **State:** complete on main, with tests and a handoff. The record (2026-11-03): engine built and proven — real percentages on real profiles, 11 SQL functions live; merged but NOT switched on for citizens — switch-on is Shawn's gate. One algorithm, matches as percentages, CONNECT never "follow", suggestions in feed/notifications.
- **Built for:** onboarding data becoming automatic connection — related pages, spaces, groups, businesses showing up in your feed; recommended connections with people like you; points when people invite (25) and join (50).
- **Fit:** merge spec §7 chain — the Auto-Match step, after Dashboard. **Take:** Shawn's switch-on word. Nothing to build.

### 5.2 The nine-node kernel + runtimes — GOLD

**Title:** The nine nodes: the organs of the one system.
**Subtitle:** Contracts, kernel, and edge functions — the whole organism, on main.
**Nutshell:** The nine master contracts, the kernel that runs them, and the edge functions that execute them are all in the repo. What the repo cannot prove is whether the edge functions are deployed.

- **Paths:** `NAYANODE/` — 69 files: the nine master contracts `00-{ACT,CONNECT,EVOLVE,KNOW,LAW,LEARN,PROVE,SELF,VERIFY}-MASTER-CONTRACT-V1.md`, `0000-NINE-NODE-GENOME-MASTER-INDEX-V2.md`, `0002-NINE-NODE-KERNEL-MANIFEST-V1.md`, `0025-VALUE-CALCULUS-SPECIFICATION-V1.md`, machine contracts `MACHINE-*-CONTRACT-V2.md`, `MANIFEST.json` · `kernel/` — 46 files: `nayapower_kernel.py`, `act_pipeline.py`, `decision_principle.py`, `memory_store.py`, `memory_metabolism.py`, `brain_registry.py`, `runtime_boot.py`, `protocol/` (checks, gates, `compile_protocol_spec.py`) · `supabase/functions/` — `nayanet-{act,know,law,prove,learn-verify,causal-verify,github-intake,github-dispatch,smart-note-viewer,verified-ai-action,causal-learning-experiment,cold-runtime-proof,intelligence-commit-runtime,intelligence-retrieve}-*/` · live-proof workflows `live-{act,know,law,prove,connect,cvo-runtime,intelligence-commit,supabase-runtime,verified-ai-action}-proof.yml`.
- **State:** contracts + code on main. Deploy status of the edge functions is NOT verifiable from the repo alone (see §7 NOT-DONE).
- **Built for:** the merge spec §7 organs — LEARN · KNOW · ACT · LAW · VERIFY · SELF · CONNECT · EVOLVE · PROVE, kernel order SELF → LAW → ACT → KNOW → PROVE → CONNECT → VERIFY → LEARN → EVOLVE. The notes are the units of intelligence the organs process.
- **Fit:** §7 — the nodes are the one system's organs. **Take:** verify each runtime is deployed (Supabase), then wire the kernel into the Factory/PI operating order.

### 5.3 Cold retrieval — GOLD

**Title:** Cold retrieval: the right knowledge in seconds.
**Subtitle:** The retrieve engine exists with tests. Its wiring to PI is the open item.
**Nutshell:** The engine that finds the right note, block, or law for the job at hand is built — and it is the piece the Factory needs most when a seat asks "what do I already have?"

- **Paths:** `supabase/functions/nayanet-intelligence-retrieve/` — `index.ts`, `retrieve.ts`, `retrieve_applicability.ts`, `supersession_registry.ts`, `gen_supersession_registry.py`, `retrieve_applicability.test.ts` · branches `naya/know-v1-contextual-retrieval-20260929`, `naya/sn1878-index-cold-retrieval-20261026-gpt6`, `naya/cold-retrieval-floor-probe-20261012`, `naya/nine-retrieval-auth-wire-packet-t0537`.
- **State:** code + tests on main; deploy status not verified from the repo alone.
- **Built for:** cold retrieve — a fresh Naya getting the right knowledge in seconds, with applicability scoring and a supersession registry so stale law never outranks live law.
- **Fit:** merge spec §7 + §1 — the Factory's "what part already exists?" question, and PI's intelligence lookup. **Take:** verify deploy, wire to PI/Factory retrieval.

### 5.4 NIAS page generator — GOLD

**Title:** The page generator: PI answers in, finished page out.
**Subtitle:** The build step of the merge spec, already written.
**Nutshell:** A generator that takes PI data and outputs a finished page in the Real Object Law already exists. It is the machine the fifteen-question build flow is waiting for.

- **Paths:** `NIAS/generate-page.py` — v3, 112 lines, 3,899B: "NAYA PAGE GENERATOR v3 — Active Intelligence. Input: PI data (JSON) → Output: finished HTML page (Real Object Law, v3.0)." Placeholders `{{name}} {{alias}} {{type}} {{vision}} {{mission}} {{goal}} {{cover}} {{sections}} {{spectrum_color}}` · `NIAS/universal-template.html` · `NIAS/page-type-configs.json` · `NIAS/pi-page-schema.json` · `NIAS/NAYA-DNA-LOCKED.md`.
- **State:** code on main. No workflow runs it; no record of it generating a live page was found in this survey.
- **Built for:** the universal app — one page that morphs into Personal, Business, Space, Membership.
- **Fit:** merge spec §3.5 + §4.4 — "fill in your intelligence, click build, get your page." **Take:** point it at PI's 15-question output after Dashboard done-done; prove one generated page before trusting it.

### 5.5 Smart Factory generators + assembler — PARTIAL GOLD

**Title:** The Factory's own generators: real code, unproven output.
**Subtitle:** The assembler exists. The proof that it built a live page does not.
**Nutshell:** The Factory holds generators and an assembler beside the parts it holds. The current builds harvest by hand. These generators are gold only once one of them proves a run.

- **Paths:** `interfaces/factory/` — `deploy-smartfactory.py` (75 lines, 3,484B), `factory-app.html`, `generators/build-dashboard.py`, `generators/build-one-system.py`, `pieces-inventory.json`, `pieces/` (dash/os blocks, scripts, styles, `features.json`) · `interfaces/demo/assembler.html`, `assembler-v2.html`, `assembler-v3.html` · `interfaces/hub/index-2.html` · `interfaces/pi-face/pi-face.html`.
- **State:** code on main. No evidence found in this survey that these generators produced a live page; the merge spec's build rule is harvest-first by hand.
- **Fit:** merge spec §1 — the Factory is the home; these are its machines. **Take:** prove one generator run (assemble one page, verify by eye) before adopting; until then, harvest-first stands.

### 5.6 MAXESS — GOLD FOR LATER

**Title:** MAXESS: the scoring engine, working — on a branch.
**Subtitle:** Deferred by Shawn until after Dashboard. The build is waiting, not missing.
**Nutshell:** The fifteen-question scoring engine exists as a working build — but the working build lives on branches, while main holds only its Academy pictures and database migrations.

- **Paths (branches):** `maxess-results-v21-working` — 26 root entries: `V21-CANONICAL-BUILD-RESULT.md`, `E01-SECTION-01-WORKING.html` through `E09-SECTION-09-WORKING.html`, `MAXESS-RESULT-CONSUMER-V1.html`, `START-HERE.md` · `feat/nayanet-maxess-entrance-part1` · `maxess-aiscore-tonight-full-repair` · `maxess-e2e-runner-verify-20260820` · `maxess-surgical-20260821` · `maxess-naya-results-v2` · branches `fix/maxesscode-canonical-repair`, `maxess-assessment-surgical-repair`, `maxess-surgical-3point-repair`, `maxess-surgical-run` · **on main only:** `DESIGN-BLOCKS/academy-assets-20261108/maxess-e05.html`, `maxess-e06.html`, `maxess-e08.html`, `maxess-e09.html` + supabase migrations `20260827…_maxess_*` (mastery band, topic persistence, attempt persistence, completion lock).
- **State:** working build on branches (V21 canonical result claimed in-branch); deferred on main. Shawn's order (2026-11-08): MAXESS is a scoring engine, not Academy sections — 15 questions, five answers worth 4/3/2/1/0, 60 maximum — deferred, Dashboard first, built immediately after.
- **Fit:** after Dashboard done-done — the scoring engine for citizens' growth. **Take:** branch review of `maxess-results-v21-working` when Dashboard lands; merge decision then.

### 5.7 AIsScore — GOLD FOR LATER

**Title:** AIsScore: a whole clean build that never reached main.
**Subtitle:** Zero hits on main. Sixty-seven files on its branch.
**Nutshell:** The AIsScore clean build — pages, results consumer, integration doc — exists only on branches. It is the clearest "made but never added" case in the repo.

- **Paths (branches only — zero matches on main):** `feat/aiscore-clean-v1-integrated` — 67 root entries: `AIScoreMAXESS-CLEAN-V1.html`, `MAXESS-RESULT-CONSUMER-V1.html`, `MAXESS-RESULT-INTEGRATION.md`, `E01`–`E06` working sections, `AIScoreMAXESS code` · `feat/aiscore-clean-v1` · `feat/aiscore-naya-v3-human-presence` · `docs/aiscore-v1-master-contract` · `fix/aiscore-cleanv1-tonight` · `maxess-aiscore-tonight-full-repair`.
- **State:** branch-only, never merged. No test or deploy evidence was read on the branch (root listing only).
- **Fit:** MAXESS's scoring front door — the AIsScore experience that feeds MAXESS results. **Take:** branch review alongside MAXESS, after Dashboard.

### 5.8 Welcome / onboarding engine — GOLD

**Title:** The welcome engine: onboarding's matching and intake, already written.
**Subtitle:** The front door's machinery is built. It needs PI's questions.
**Nutshell:** The welcome engine — intake, matching, consent gate, golden-set tests — is a complete system on main. It is the onboarding flow's engine, waiting for the questions it will ask.

- **Paths:** `tools/welcome-engine/` — `welcome_engine.py`, `intake_bridge.py`, `consent_gate.py`, `categorize.py`, `calibrate.py`, `derive_matches.py`, `corpus.json` + `corpus.py`, `golden_set.py`, `holdout_set.py`, `idf_decision.json`, `matches.json`, `DEMO-RECEIPTS.json`, `SCORECARD-WELCOME-ENGINE.md`, 13 test files · `interfaces/front-door/identity.html` · `nayanet-app/public/pages/showcase-{personal,business,space,membership}.html` · `nayanet-app/src/worker.js` (308B — a stub; the app shell, not the app).
- **State:** code + tests on main. `nayanet-app/src/worker.js` is 9 lines — the live app shell is a stub, not a system.
- **Built for:** the welcome process — the 10 onboarding questions that fill in Personal, Business, and Space, ending at "you got your pages."
- **Fit:** merge spec §4 — onboarding feeds PI; §4.1 the 10 questions, §4.2 the creation flow. **Take:** wire `intake_bridge.py` to PI's 10/15 questions.

### 5.9 Orchestrator — GOLD

**Title:** The orchestrator: staged execution with resume and governed halts.
**Subtitle:** A real execution engine. No workflow runs it.
**Nutshell:** A staged execution engine — resume, event store, governed halts, no synthetic pass — sits unused while seats run by hand.

- **Paths:** `orchestrator/` — `orchestrator.py` (285 lines, 11,888B), `event_store.py`, `executors.py`, `stages.py`, `run_state.py`, `ts_bridge.py`, `README.md`, `__init__.py`.
- **State:** code on main. None of the 47 workflows invokes it.
- **Built for:** staged runs where completed stages are never re-executed, a NOT_IMPLEMENTED stage is recorded loudly and caps the run at INCOMPLETE, a stage error halts with a named error, LAW BLOCKED and VERIFY-rejected are governed halts, and "No synthetic PASS anywhere. No silent fallback. No silent drop."
- **Fit:** merge spec §2 — the operating order (manual first, then PI, then build) needs an execution engine that remembers where a run stopped. **Take:** adopt it for seat runs; one proven run first.

### 5.10 Smart Box, first generation — PARTIAL GOLD

**Title:** The first Smart Box: its law and registry are gold; its worker is superseded.
**Subtitle:** The master box built November 10 replaces the worker. Keep the law.
**Nutshell:** The first-generation Box holds the law, the registry, and the welcome page that the new master box should inherit — and a worker that should retire.

- **Paths:** `SMART-BOX/` — `worker.js` (64,548B), `app/index.html`, `data/entries.jsonl`, `data/meta.json`, `README.md` · `NIAS/SMART-BOX/` — `SMART-BOX-LAW.md`, `SMART-BOX-REGISTRY.json`, `naya-world-welcome.html`, `naya-world-welcome-composable.html`, `smart-box.css`.
- **State:** code on main. The master box was built 2026-11-10 (separate seat, local + filed) — the old worker is superseded in function; the law and registry are not superseded, they are the inheritance.
- **Fit:** merge spec §7 chain — the Box step, between Feed and Ledger. **Take:** harvest the law + registry + welcome page into the master box; retire the old worker explicitly so two Boxes never run.

### 5.11 Intelligence-block store — GOLD

**Title:** The block store: twenty blocks, a registry, and a schema.
**Subtitle:** The units of intelligence, filed and reconcilable.
**Nutshell:** The store that holds intelligent blocks as JSON — with a registry, a schema, and a reconcile tool — is the Box's reading material.

- **Paths:** `intelligence/blocks/` — `IB-0001.json` through `IB-0020.json`, `REGISTRY.json`, `SCHEMA.md`, `README.md`, `IB-RECONCILIATION-P0A.md` · `intelligence/tools/ib.py`, `ib_reconcile.py`, `seed_blocks.py`, `migrate_v10_to_v11.py` + tests (`test_ib_kernel_integration.py`, `test_ib_reconcile.py`, `test_ib_owner_naya.py`, `test_ib_legacy_reexport.py`).
- **State:** code + data + tests on main.
- **Fit:** merge spec §7 chain — the Block step; the notes become blocks here. **Take:** confirm the Box reads this registry (not a copy of it).

### 5.12 Ledger spine — GOLD

**Title:** The ledger: the record of every action, already being kept.
**Subtitle:** The chain's memory, in JSONL.
**Nutshell:** The activity ledger — every action in and out, plus the stats that play it — exists as files. The Dashboard's sync spine needs to read them, not re-derive them.

- **Paths:** `LEDGER/` — `activity-ledger.jsonl`, `ACTIVITY-LEDGER.md`, `STATS.md`, `contracts/NC-001.json`, `nodes.jsonl`, `archive/2026-10-26-naya-mission-state-continuation/`.
- **State:** data + docs on main.
- **Fit:** merge spec §7 chain — the Ledger step; the Dashboard shows the person their world from this record. **Take:** wire Dashboard reads to it (the Dashboard done-done work already names the ledger sync spine).

### Surveyed shallow (counted, not deep-dived)

- `successor-reuse/` — 452 files: cold-successor replay/score harness (`harness/check-note-contract.mjs`, `replay-trial.mjs`, `score-p5.py`, selftests). Counted from the tree; purpose inferred from filenames only. Needs its own look.
- `HUB/` — 338 files: rooms, the PI datasets (`PROJECT-INTELLIGENCE-READINESS-DATASET-2026-10-26`, `PROJECT-INTELLIGENCE-FACE-*`), the Blueprint, the Smart App room spec. The PI face draft PR #3089 touches this area.
- `DASHBOARD/` — 19 files: dated fix snapshots (`index-defectfix` through `index-defectfix5-20261105.html`, `index-circle-*`, `index-orbit-*`). Historical snapshots, superseded by the live Dashboard work.
- `.naya/` — 1,298 files: the capture archive (smart-note JSONs) plus live specifications (scorecard receipt authority, decision value calculus). An archive and a spec library, not a system.
- `BRAIN/` — 3,004 files: the organized brain (governance, memory, intelligence, interfaces, engineering). The home of the specs this audit cites.
- `tools/` — 415 files total: the Super Brain's tool set. This audit deep-read its four named tools plus the matching, welcome, and factory tools; the rest of `tools/` was not individually surveyed.

---

## 6. THE PUZZLE MAP — WHERE EACH GOLD PIECE FITS IN THE ONE ENGINE

**Title:** One engine, and every gold piece has a home in it.
**Subtitle:** The map is judged against the one-system merge spec (2026-11-09).
**Nutshell:** The four Shawn named are parts of one loop — compiler watches, EMIT feeds, Compass decides, scorecard judges — and the rest bolt onto the same engine: the chain, the organs, the build flow, the front door. Nothing here needs inventing. Everything needs wiring, a decision, or a proof run.

| # | Piece | Home in the one engine (merge spec) | What it would take to use it |
|---|---|---|---|
| 1 | Living Map compiler — `tools/map-compiler/map_compiler.py` | §5.4 design-contract gate — the mechanical measurer | Wire gate to read `HUB/MAP-STATE.json`; fix bridge + dock reds |
| 2 | EMIT — `HUB/FEEDS/emit_hub_feeds.py` | §7 chain, Feed step — the pump | Shawn's word on non-PRIVATE rows; nothing to build |
| 3 | Scorecard calculator — `tools/scorecard.py` + validator + receipt authority | §5 gate enforcement (the 9.0 bar) + §2 five gates | Report-only wiring first, then gate wiring on Shawn's word |
| 4 | Decision machine + Compass — `kernel/value_calculus.py`, `tools/nayas_guide.py`, `tools/decision_cli.py`, `tools/decision_output.py`, `tools/learning_loop.py` | §2 five gates (the math) + §3 PI choices + merge gates | Wire Compass into dispatch/merge loop; decision_cli in briefs; binding version stays Shawn's call |
| 5 | Auto-Match — `tools/smart-match/`, `tools/welcome-engine/smart_match.py` | §7 chain, Auto-Match step | Shawn's switch-on word |
| 6 | Nine-node kernel + runtimes — `NAYANODE/`, `kernel/`, `supabase/functions/nayanet-*-runtime/` | §7 organs | Verify edge-function deploys; wire kernel into Factory/PI order |
| 7 | Cold retrieval — `supabase/functions/nayanet-intelligence-retrieve/` | §7 + §1 Factory ("what part already exists?") | Verify deploy; wire to PI/Factory |
| 8 | NIAS page generator — `NIAS/generate-page.py` | §3.5 + §4.4 PI build flow + universal app | Point at PI 15-question output; prove one page |
| 9 | Factory generators — `interfaces/factory/` | §1 Factory home | Prove one generator run |
| 10 | MAXESS — branch `maxess-results-v21-working` | After Dashboard done-done — the scoring engine | Branch review when Dashboard lands |
| 11 | AIsScore — branch `feat/aiscore-clean-v1-integrated` | MAXESS's front door | Branch review alongside MAXESS |
| 12 | Welcome engine — `tools/welcome-engine/` | §4 onboarding feeds PI | Wire `intake_bridge.py` to PI's 10/15 questions |
| 13 | Orchestrator — `orchestrator/` | §2 operating order — the execution engine | Adopt for seat runs; one proven run |
| 14 | Block store — `intelligence/blocks/` | §7 chain, Block step | Confirm Box reads this registry |
| 15 | Ledger spine — `LEDGER/activity-ledger.jsonl` | §7 chain, Ledger step | Wire Dashboard reads to it |
| 16 | Smart Box v1 law + registry — `NIAS/SMART-BOX/` | §7 chain, Box step (via master box) | Harvest law + registry; retire old worker |

**The loop, in one line:** the compiler watches the system, EMIT feeds the rooms, the Compass decides what to do, the scorecard judges whether it was good enough — and the learning loop learns from the outcome. That is the Smart Flow made mechanical, and every piece of it already exists. The engine is assembled from parts; the assembly is the work.

**The one gap in the engine:** `tools/naya_calculator.py` — the universal Calculator's reference implementation (spec `BRAIN/01-GOVERNANCE/0006-NAYA-CALCULATOR-V1`) — does not exist. File it as a GAP: build it to the spec, or record that `tools/scorecard.py` IS the Calculator and amend the spec. Do not invent a third scorer.

---

## 7. HONEST NOT-DONE LIST

**Title:** What this audit did not do.
**Subtitle:** The gaps are named, not hidden.
**Nutshell:** The audit is complete for the four named pieces and the top finds. Four things remain open, and the different-seat re-run is the most important of them.

1. **Different-seat re-run — NOT RUN.** The brief's verification is a different seat re-checking, from this report alone, the four named pieces (each path exists, each state matches) + 3 sampled finds. That seat has not run yet. This report is the input to it, not the result of it.
2. **Edge-function deploy status — NOT VERIFIED.** Whether the Supabase runtimes (`nayanet-{act,know,law,prove,learn-verify,intelligence-retrieve}-*`) are actually deployed cannot be established from the repo alone. It needs the Supabase connector or a live probe — a separate check, not a repo read.
3. **Branch coverage is by name, not by reading.** All 1,109 branches were enumerated and searched by name pattern (compiler / emit / scorecard / decision / navig / calcul / maxess / aiscore / factory / retriev / search / automatch / ledger / builder / onboard / welcome / pricing). A dormant system hiding under an uninformative branch name would not have been caught. A full branch read is a different job.
4. **Shallow items:** `successor-reuse/` (452 files) was counted, not deep-dived; branch `naya1/system-charter-machine-compiler-20261004` got a root listing only; the AIsScore and MAXESS branches got root listings only (no file reads inside them); `tools/` beyond the named tools was not individually surveyed.
5. **The smart note for this audit** is filed alongside this report (see the accompanying note); its live-feed verification is recorded in the filing receipt, not in this file.

---

## SOURCES — EVERY CLAIM COMES FROM HERE

| Source | What was taken from it |
|---|---|
| Main tree, recursive | `GET /repos/SoulSchoolAcademy/NayaPOWER/git/trees/main?recursive=1` — 10,052 entries, head `2993c46a…` |
| Branch list | `GET /repos/SoulSchoolAcademy/NayaPOWER/branches?per_page=100&page=1..12` — 1,109 branches |
| Open PRs | `GET /repos/SoulSchoolAcademy/NayaPOWER/pulls?state=open&per_page=100` — 4 PRs |
| File heads (read via Contents API, base64-decoded) | `tools/map-compiler/map_compiler.py` · `TEAM-NITRO/os/brief-compiler.py` · `kernel/protocol/compile_protocol_spec.py` · `HUB/FEEDS/emit_hub_feeds.py` · `kernel/protocol/checks/scorecard.py` · `.naya/scorecard-receipt-authority-DESIGN.md` · `BRAIN/01-GOVERNANCE/0003-SYSTEM-SCORECARD-V1.md` · `BRAIN/01-GOVERNANCE/0006-NAYA-CALCULATOR-V1.human.md` · `BRAIN/01-GOVERNANCE/0017-CALCULATOR-AS-DEFAULT-V1.human.md` · `BRAIN/10-INTERFACES/DESIGN-BLOCKS/ultimate-presentation-page-20261106/SPEEDOMETER-CALCULATOR.md` · `tools/scorecard.py` · `tools/decision_output.py` · `tools/learning_loop.py` · `tools/decision_cli.py` · `kernel/value_calculus.py` · `tools/scorecard_guard.py` · `tools/learning_scorecard.py` · `tools/nayas_guide.py` · `NIAS/generate-page.py` · `SMART-BOX/worker.js` · `orchestrator/orchestrator.py` · `interfaces/factory/deploy-smartfactory.py` · `HUB/MAP-STATE.json` · `HUB/FEEDS/smart-feed.json` · `HUB/FEEDS/today.json` · `.github/workflows/hub-feeds-emit.yml` · `.github/workflows/map-compiler.yml` · `.github/workflows/scorecard-tests.yml` · `.github/workflows/merge-consensus-gate.yml` |
| Branch root listings | `feat/aiscore-clean-v1-integrated` (67 entries) · `maxess-results-v21-working` (26 entries) · `naya1/system-charter-machine-compiler-20261004` (36 entries) · `naya/citizen-discovery-automatch-core-20261023` (62 entries) · `naya5/scorecard-calculator-20261014` (gone — "No commit found for the ref") |
| Memory (local, for history only — every state claim above was re-checked live) | `~/memory/2026-10-16.md` (Blueprint build order, compiler v1 PR #2687 9.2/10) · `~/memory/2026-10-17.md` (four-system loop, Compass dormant, scorecard on a side branch) · `~/memory/2026-10-19.md` (EMIT blocked PR #2678; overnight directive) · `~/memory/2026-10-20.md` (EMIT merged ~16:19Z; compiler ticks missing; Tool Set order) · `~/MEMORY.md` 02:43Z Nov 10 (Shawn's gold-audit order, the four pieces, the puzzle) |
| The current plan | `~/workspace/team-nitro/ONE-SYSTEM-MERGE-SPEC-20261109.md` — the puzzle map's home |
| The inventory | `~/workspace/team-nitro/THE-INVENTORY.md` — grep-verified: none of the four named pieces is in it |

*Read-only audit. No code changed, no deploy, no merge, no PR opened. The different-seat re-run is the verification record for this report; it is pending, not claimed here.*
