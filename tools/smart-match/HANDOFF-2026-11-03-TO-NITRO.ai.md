# Auto-Match — handoff to Nitro (AI form: exact values, procedures, constraints)

**From:** naya-resolve (owner) · **To:** naya-nitro · **Date:** 2026-11-03 · **At Shawn's direction.**
**Anchor:** main tip `3397e52f738fa3d1b8b74497444d40dea65f6f38` (live ref read 2026-11-03). All paths verified at this tip via contents API / git blobs. Human form: `HANDOFF-2026-11-03-TO-NITRO.human.md`. Machine form: `HANDOFF-2026-11-03-TO-NITRO.machine.json`.

## 1. Identity and ownership

- Assignment (Shawn, 2026-10-27, via Nitro as delegator; Resolve accepted): **Auto-Match + Auto Organization → naya-resolve; Smart Search → naya-power.** Owner unchanged unless Shawn reassigns.
- System design: Verity (report 2026-10-19), ruled by Shawn 2026-10-24, filed as **SN-0845**.
- Early scorecards: Power — v1 5.5 → v1.1 7.0 → v1.2 7.5 (`tools/smart-match/SCORECARD.md`).
- Consent machinery: Tree's citizen-discovery walk (`HUB/citizen-discovery-core.js`, **reference branch only, NOT merged, NOT carried** per CONVERGENCE-2026-10-24).

## 2. The engine — exact contract

- **Path:** `tools/welcome-engine/smart_match.py` · **14,424 B · 318 lines · blob `92ac6ffa2326f40cf3e75876bc553018fda0f037`** · **version v1.5** ("elite hardening 2026-10-24"; lineage v1 → v1.1 concept layer → v1.2 two-tier family scoring → v1.3 word tier → v1.4 light stemming → v1.5 hardening).
- **Input:** profile vector = dict of 5 declared fields, each a list of term strings: `topics, goals, offers, needs, wants`. Optional `value_b` verified-value record; optional IDF weight table. Malformed input (None, bare numbers, non-strings) is sanitized; degrades gracefully, never crashes.
- **Scoring:**
  - `family_score` (topics, goals): phrase overlap + stemmed-word overlap blended 50/50 = raw; final = raw 50% + concept coverage 50%. Concept taxonomy = 12 governed families: MAKING, SHIPPING, PROVING, CONNECTING, SPEAKING, TALKING, THINKING, CLEARING, GUIDING, DECIDING, PUBLISHING, PEOPLE. If neither side hits the taxonomy, concept tier is silent and raw decides.
  - `cross_score` (offers↔needs, wants): signature = content phrases + concepts + stemmed content words; computed symmetrically both directions, averaged.
  - One unified 79-word stopword set filters raw words pre-stem in every tier; light deterministic stemmer.
- **Weights (Lock Packet, Issue #3029):** `topics 0.40 · goals 0.25 · offers↔needs 0.20 · wants 0.15`. **Percent = `round(100 × weighted sum)`.**
- **Percent semantics (verbatim, normative):** "The weighted share of DECLARED signals that align between two profiles. Not a probability, not a judgment of worth."
- **Surface rule:** a suggestion surfaces only on **≥2 independent signals**. Reasons always ride in the output; a % without reasons is a defect.
- **Output contract:** `{score, rank, signals, surface, parts, reasons, signal_coverage_percent, calibrated: true}`.
- **Value rule:** only a verified-value record `{state: VERIFIED|FINAL, value 0..1}` adjusts **rank** by `×(0.9 + 0.1·v)`; it **never** moves the %. Bare floats and PENDING/OBSERVED records are neutral.
- **Scale:** IDF mode optional, **default OFF** (tokens in >50% of population down-weighted ×0.25). `rank_matches_indexed` (inverted-index pre-filter) proven result-identical to naive ranking (1000/1000). `rank_matches` excludes the entity itself. Bench: 1-second budget crosses at ~62 entities full-pairwise; ~3,800 candidates for one citizen's ranking.
- **Folder family** (`tools/welcome-engine/`, all at tip): `welcome_engine.py`, `declared_vectors.py`, `calibrate.py`, `golden_set.py` (12 synthetic citizens), `holdout_set.py`, `idf_eval.py`, `corpus.py`, `categorize.py`, `consent_gate.py`, `derive_matches.py`, `intake_bridge.py`, `sql_parity.py`, 3 bench scripts, 11 test files.

## 3. The SQL twin

- `tools/smart-match/smart_match_v1_4.sql` (10,023 B). **Header: "NOT deployed — for the wiring lanes" — STALE (see the correction at the end of this section).**
- Defines 11 functions in `public`: `sm_stopwords, sm_terms, sm_stem, sm_words, sm_sig_words, sm_terms_content, sm_concepts, sm_coeff, sm_family, sm_cross`, entry point **`public.smart_match(a jsonb, b jsonb, value_b numeric)`** returning the same contract.
- 4 named divergences from Python: (1) bare-numeric `value_b` vs verified-record contract; (2) Postgres vs banker's rounding on exact .5; (3) no `reasons`; (4) non-array jsonb errors instead of degrading.
- Deployable repackaging: `supabase/migrations/20261025040000_smart_match_v1_4.sql` (11,587 B, blob `30236ba8…`, same 11 bodies verbatim, idempotent create-or-replace, B5 2026-10-25). **Presence in migrations/ is NOT evidence of application — and application is now proven directly: CORRECTED 2026-11-03 (Resolve, answering Nitro's F2).** Read-only RPC probes against the production project (sb-api, `POST /rest/v1/rpc/smart_match`, pure immutable function, no mutation): (1) a=b={topics:["making"]} → `{score: 40, rank: 40, signals: 1, surface: false}` = 0.40 topics weight at full alignment, ≥2-signal rule holding; (2) a={offers:["coaching"]}, b={needs:["coaching"]} → `{score: 10, signals: 1, surface: false}` = 0.20 × 0.5 symmetric average; (3) disjoint topics → `{score: 0, signals: 0, surface: false}`. All three contract-correct — the 11 functions exist and execute in production. When/by what route the migration was applied: not in the lane record. **Deployed ≠ live: no surface calls it for citizens; live derivation remains off; the switch-on remains Shawn's gate (§9).**

## 4. Auto Organization

- Design sources in authority order: (1) SN-0845 (`BRAIN/05-MEMORY/SMART-NOTES/2026/10/24/SYSTEM/matching/SN-0845/IB-SMART-NOTE-20261024-sn0845-smart-match.md`, 6,919 B); (2) 2026-10-27 extension, owner Resolve: `HUB/NAYANET-PATH-TO-TEN-2026-10-27.HUMAN.md` + `.AI.md`.
- Rules: files **by declaration, not guesses**; governed label set is its constitution; capture rule requires a validated declaration at the door; **Smart Tabs** = navigation on ALL pages ("All" exists, never the only view); manual pin/link always wins and teaches; system creates tabs from clusters (near-duplicates merge, no spam); every auto placement shows **percent + reason**; corrections teach; deleting a tab never deletes contents.
- Gate measurement: **99.1% precision (661/667)**, three waves; designs 1–2 refuted by their own numbers.
- Built piece: `tools/welcome-engine/categorize.py` (9,757 B; B7, 2026-10-25): item → engine vector → `score()` vs every space/project → filed with best match **only** at the ≥2-signal bar; below bar → **UNFILED with reason named**; `visibility != "public"` → **REFUSED before any scoring** (structural, first check).
- State: proven and **unlanded**; decomposed into a 5-piece landing packet (PATH-TO-TEN).

## 5. Bullseye (Alignment Master)

- `BRAIN/10-INTERFACES/ALIGNMENT-MASTER-20261030.md` (48,571 B), §6 item 23, "Smart Match — system, no page (engine)". (The root `0000-NAYAPOWER-MASTER-DESIGN-CONTRACT-V1.md` has 12 sections; §23 is NOT there.)
- Bullseye moment: "the right people and the right spaces find each other automatically — matches that are real, explained, and acted on. Not a list nobody opens."
- Chain: walk answers in → matched people/spaces out → Booking (introduces) → Meet (hosts); connects Connections, Spaces, Personal.
- Fix directive: EDIT — post-merge verification first, then production switch-on (**awaits Shawn's serving-chain ruling**), then the owed acceptance fields. **"Engine 9.5 is a LANE score — never an app score."**
- Inventory status line (verbatim): "Engine built, lane-proven 9.5; production switch-on awaits Shawn's serving-chain ruling."

## 6. Proof ledger (measured; sources named)

| Claim | Evidence | Source |
|---|---|---|
| Golden set 12/12, weights confirmed 12 right / 0 wrong | `calibrate.py` | CONVERGENCE-2026-10-24 |
| test_smart_match 9/9 · test_welcome_engine 14/14 | convergence battery | CONVERGENCE-2026-10-24 |
| Hardening suite 69 passed at head | PR #3041 lineage, branch `resolve/auto-match-elite-v2`, base `05f209ae…` | HARDENING-ELITE-V2-2026-10-24 |
| Independent holdout 20/20 (synthetic) | exposed stemmer lemma/plural bug, fixed; test not adjusted | HARDENING §(holdout) |
| Index identity 1000/1000 | bench | HARDENING |
| Different-seat score 9.5; 149/149 tests; Python↔SQL parity 79 = 79 | **not re-run this pass** — rests on PATH-TO-TEN 2026-10-27 | PATH-TO-TEN |
| Organizer gate 99.1% precision (661/667) | 3 measurement waves | PATH-TO-TEN |
| B1–B7 done_proven | PI row `resolve-automatch-buildable-complete` | sb-api read 2026-11-03 |

Test-suite state at tip: **VERIFIED by re-run 2026-11-03 (Nitro's F2)** — full welcome-engine suite at tip `1cf346bdceee419c2ba08539ee39f410d3702731`: **149 passed / 0 failed**. Method: all 33 welcome-engine files byte-verified against their tip blobs (31 identical in the local checkout; `welcome_engine.py` + `test_welcome_engine.py` refreshed from tip bytes; the SQL twin + the B5 migration + `HUB/app/js/naya-intake.js` staged at tip bytes for path-dependent tests). The parity tests in the suite guard the migration file and its four-divergence header — green. Production runtime spot-proof: §3 correction (3 RPC probes). First-run record (`tools/smart-match/FIRST-RUN-2026-10-24.md`): nitro→Team Nitro space 54%, naya-power→NayaPOWER space 52%; Resolve ~0 vs every project = vocabulary failure, drove v1.1+.

## 7. Project Intelligence rows (sb-api, store `work_items`, project `a554e536-66a6-4808-8c36-988f13d9f394`; rows keyed by `item_key` — the table has NO numeric `n` column; `project_intel_items` store: 0 matches)

Core (all owner `naya-resolve`):
- `resolve-automatch-buildable-complete` — "Auto-match: all 7 buildable steps on main, verified (B1–B7)" — **done_proven**
- `14q-smart-match-sql-deploy` — "14Q: Deploy Smart Match SQL v1.4 + live match proof" — **queued**
- `automatch-onboarding-sync` — "Sync auto-match with onboarding: Welcome answers become the match vector at birth" — **queued**
- `auto-organization-20261027` — "Auto Organization: Auto-Match extended to categorize notes feeds, mail, contacts, spaces and PI - Smart Tabs everywhere" — **queued**

Adjacent (not core): `build-welcome-flow-engine` in_progress (naya-power) · `auto-page-birth-mission` in_progress (naya-resolve) · `build-welcome-flow` queued (no owner). `smart-search-fix-20261027` = Smart Search (Power) — false positive, exclude.

Open PRs mentioning smart-match/automatch: **none** (5 open total: #3156, #3131, #3108 zombie — MUST NOT MERGE, #3089 draft, #2981).

## 8. Version clarification (normative)

"Smart Match v4.0" = a **PI fill version**, not an engine version. **The engine is v1.5.** No v4.0 engine exists in the tree. Do not let the numbers cross.

## 9. Gates and constraints

- **Production switch-on = Shawn's gate** (serving-chain ruling, Alignment Master §23). No seat flips it.
- SQL deploy is a production step — same gate family; PI row stays queued until ruled.
- Privacy: private content NEVER feeds the matcher; refusal is structural and precedes scoring (see §4, categorize.py).
- Falsifiers for any future "live" claim: (a) a served surface returns a real match with % + reasons for a real citizen vector — **OPEN**; (b) the SQL functions answer in production (deploy proof, not file presence) — **SATISFIED 2026-11-03** (§3 correction: 3 read-only RPC probes, contract-correct); (c) the claim holds across two consecutive checks (standing live-proof bar) — **OPEN**. (a) and (c) belong to the switch-on gate; (b) alone never made anything live.
