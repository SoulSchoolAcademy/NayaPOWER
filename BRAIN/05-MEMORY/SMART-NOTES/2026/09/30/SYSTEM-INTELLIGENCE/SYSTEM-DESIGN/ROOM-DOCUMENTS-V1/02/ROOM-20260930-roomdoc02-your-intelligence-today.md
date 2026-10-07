# ROOM-02 — Your Intelligence Today · Official Room Design Document (CANDIDATE)

**Status:** CANDIDATE — drafted 2026-10-02 by Naya 4 (subagent). Not ratified, not merged.
**Route:** `/today` · **Metaphor:** THE HIGHLIGHT REEL · **Theme:** magenta
**Parent law (wins on conflict):** `HUB/NAYANET-SMART-APP-ROOM-SPEC-V1.md` §11 (Shawn, canonical, main)
**Sources:** Shawn's spec §11; `HUB/ROOMS/02-your-intelligence-today/FUNCTIONAL-SPEC.md` + `DESIGN-CONTRACT.md` (PR #1290, open); Naya Design Intelligence v1.3; DI-INFUSION-0001 R.1–R.9 shape.

**DIVERGENCE (Shawn wins):** #1290 specifies "Today Pulse as a sculpted metric ribbon." Shawn's spec §11 primary design law: "No metric grid unless metrics are actually the human's decision problem. The page gets *simpler* as Naya becomes smarter." This doc follows Shawn: counts support the story, never dominate it; no pulse-scores or KPI cards.

## R.1 Room outcome

Start the day already oriented — Naya has distilled current intelligence into the few things that matter, as one beautiful daily story.

## R.2 Surface questions

- **WHERE AM I?** → `/today`. Opening frame: date + current Space + "Today in a nutshell" + truth freshness ("updated 4 min ago"). Source: #1290 functional spec; Shawn's spec §11.
- **WHAT MATTERS?** → NOW: the single most important current situation/action. Then NEXT / WATCH / LEARNED / WAITING / RECENT PROOF. Source: Shawn's spec §11 recommended composition.
- **WHAT CAN I DO?** → Play / Explore Today (guided sequence), Ask Naya about today, Open in Feed, Open Source/Evidence, Save / Add to List, View day in Ledger. Source: #1290 primary actions.
- **WHAT HAPPENS NEXT?** → Play steps through highlights sequentially; Open jumps to the Feed origin; Ask Naya explains the whole day; Save files to a list. Predictable.

## R.3 Applicable laws

- **H1 Purpose before interface** → job fixed first: "start the day/session already oriented." Not a dashboard. Source: Shawn's spec §11.
- **H2 Distill before display** → highlight selection (human importance, verified change, decisions, learning, consequence — never just "recent"). Naya must explain why each item made the highlights. Source: #1290.
- **H3 Recognition before recall** → time navigation visible (Today / Yesterday / date picker / "previous meaningful day"); chapters labeled, not remembered.
- **H4 One obvious next action** → NOW section: the single most important action. Primary action per Shawn: "act on the highest-value next move."
- **H5 Perceptible state + immediate feedback** → 11 named states; quiet days stay quiet ("No major changes today") rather than manufacturing content. Source: #1290 empty state.
- **H6 Prevent error before explaining error** → no destructive actions in this room; it is a projection/synthesis surface, does not own Smart Note creation or report generation. Source: #1290.
- **H7 Complexity stays in the machine** → full stream available but not shown; only the reel surfaces. Shawn's law: page gets simpler as Naya gets smarter.
- **H8 Stable grammar, adaptive intelligence** → day-as-story structure stable; highlight selection adapts to goals/context.
- **H9 Direct manipulation** → N/A with reason: guided presentation and reading dominate; no manipulation metaphor specified in either source.
- **H10 Design must learn** → highlight-selection scoring should improve from verified outcomes; no learning loop specified in sources — OPEN.
- **V1 Meaning before decoration** → magenta marks human significance; per-highlight semantic accents (discovery/learning/decision) without breaking magenta identity. Source: #1290 contract.
- **V2 Hierarchy before density** → nutshell first, meaningful change second, stream third, Naya synthesis + carry-forward close. Source: #1290 contract.
- **V3 Depth before glow** → cinematic scenes with depth; glow never on letterforms.
- **V4 State before animation** → guided Explore sequence cinematic but restrained; reduced-motion keeps narrative intact. Source: #1290 contract.
- **V5 Contrast before novelty** → the nutshell sentence is the highest-contrast element, not a novel widget.
- **V6 One icon/material family** → highlight scenes share the object jewel language.
- **V7 Tokens before one-off styling** → magenta theme via tokens.
- **V8 Interaction must feel intentional** → "Play" is guided presentation (explicitly not video). Source: #1290.
- **V9 Premium must remain fast** → story chapters lazy; exact budgets OPEN in sources.
- **V10 Preserve baseline** → day-as-story model is the baseline anchor. Source: #1290 non-regression anchors.

## R.4 Cognitive checks

- **attention** → the nutshell sentence + NOW win first glance. Correct.
- **choice complexity** → six sections max (NOW/NEXT/WATCH/LEARNED/WAITING/RECENT PROOF); actions per highlight concise.
- **target acquisition** → Play/Explore as the primary large control; mobile full-screen chapters swipeable.
- **memory burden** → "why it mattered" printed per highlight; open loops + tomorrow carry-forward externalized. No recall of yesterday's state required.
- **mental model** → a briefing/story, not a dashboard. Shawn: "more like an intelligent briefing than a dashboard."
- **feedback latency** → chapter transitions immediate; evidence opens as sheet without breaking story.
- **error probability** → read-only synthesis surface; low by construction.
- **recovery** → back returns to story position; date navigation non-destructive.
- **progressive disclosure** → nutshell → highlight → evidence → Feed origin, four depths.
- **trust** → every highlight and pulse number traces to canonical evidence; counts real only ("real canonical counts only"). Source: #1290 anchors + five-layer mapping.

## R.5 Computable predicates

- **P-HICK** — ≤4 sibling choices per level → 6 story sections; per-highlight actions ≤5. Sections are sequential narrative, not competing choices. **PASS** (spec).
- **P-FITTS** — Play/Explore primary control large; mobile swipe targets full-screen. **PASS** (spec); re-verify at render.
- **P-MILLER** — one nutshell sentence carries the day; per-highlight "what/why/changed" ≤4 chunks. **PASS** (spec).
- **P-DOHERTY** — chapter advance <400ms. **UNMEASURABLE** — no render seat.

## R.6 Causal paths (per control)

- **PLAY / EXPLORE TODAY** → INTENT: guided review of the day → SCOPE: today's highlights → CAPABILITY: sequential presentation → OBSERVATION: scenes advance → UI_STATE: chapter position → EVIDENCE: each scene links origin/evidence.
- **ASK NAYA ABOUT TODAY** → INTENT: understand the whole day → SCOPE: today's intelligence → CAPABILITY: synthesis Q&A → OBSERVATION: answer → UI_STATE: inline/threaded answer → EVIDENCE: sources cited.
- **OPEN IN FEED** → INTENT: see origin context → SCOPE: one highlight → CAPABILITY: deep link → OBSERVATION: Feed object → UI_STATE: feed position → EVIDENCE: same canonical object.
- **VIEW DAY IN LEDGER** → INTENT: inspect consequential activity → SCOPE: today's receipts → CAPABILITY: ledger deep link → OBSERVATION: filtered ledger → UI_STATE: ledger view → EVIDENCE: receipts.
- **TIME NAVIGATION (Yesterday / picker)** → INTENT: review another day → SCOPE: selected date → CAPABILITY: day projection → OBSERVATION: that day's story → UI_STATE: date header → EVIDENCE: that day's canonical data.

## R.7 Benchmark-to-beyond

- **Frontier surveyed:** morning-briefing products, daily-digest apps, executive briefing formats. (Proposal.)
- **Principles extracted:** one-screen orientation; narrative over metrics; carry-forward.
- **What we preserve:** real-counts-only discipline; quiet days stay quiet (no manufactured content — no benchmark does this honestly); highlight→origin→evidence chain.
- **Beyond-benchmark option:** a daily story Naya narrates with reasons ("why this made the highlights"), ending in tomorrow carry-forward — a briefing that writes its own next episode.
- **10× claim:** ambition only. Candidate metric: 10-second orientation test (acceptance journey step 1). No factor claimed.

## R.8 Anti-patterns watched

- **generic_dashboard_conversion** → guard: Shawn's primary design law — no metric grid unless metrics are the decision problem. (Divergence enforced.)
- **fake_data** → guard: "Do not manufacture highlights to fill space"; quiet days stay quiet. Source: #1290.
- **vanity pulse scores** → guard: counts support the story, never dominate; listed in "must never become." Source: #1290 contract.
- **canned inspirational reflection** → guard: Naya's reflection generated from evidence, "no motivational filler." Source: #1290.
- **spectacle_over_readability** → guard: cinematic but restrained; reduced-motion intact narrative.
- **self_grading_as_final_proof** → guard: acceptance journey is human-executed (10-second test), not builder-scored.

## R.9 Acceptance

- **Cold-Naya test:** read this doc → explain the day's promise → identify DNA (magenta significance + story-not-dashboard + real-counts-only) → propose one bounded improvement with evidence.
- **Taste items for Shawn:** nutshell sentence voice (Naya's register); NOW-card visual weight; whether RECENT PROOF strip shows by default.
- **OPEN:** highlight-selection scoring weights unspecified in sources (candidate list exists, no weights/thresholds); learning loop for selection unspecified.

## Working notes

- 2026-10-02 — Document created (CANDIDATE). One divergence recorded above (metric ribbon vs. no-metric-grid; Shawn wins).
