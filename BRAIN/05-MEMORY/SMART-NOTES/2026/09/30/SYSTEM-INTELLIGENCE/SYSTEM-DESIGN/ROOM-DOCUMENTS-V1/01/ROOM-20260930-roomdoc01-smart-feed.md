# ROOM-01 — Smart Feed · Official Room Design Document (CANDIDATE)

**Status:** CANDIDATE — drafted 2026-10-02 by Naya 4 (subagent). Not ratified, not merged.
**Route:** `/feed` · **Metaphor:** THE GAME · **Theme:** emerald
**Parent law (wins on conflict):** `HUB/NAYANET-SMART-APP-ROOM-SPEC-V1.md` §10 (Shawn, canonical, main)
**Sources:** Shawn's spec §10; `HUB/ROOMS/01-smart-feed/FUNCTIONAL-SPEC.md` + `DESIGN-CONTRACT.md` (PR #1290, open); Naya Design Intelligence v1.3 (20 laws, 10 cognitive checks, 14 anti-patterns); DI-INFUSION-0001 R.1–R.9 shape.

## R.1 Room outcome

Receive useful, relevant intelligence without manually checking every room — open the Feed and immediately understand what changed or matters, ordered for you.

## R.2 Surface questions

- **WHERE AM I?** → `/feed`, Smart Feed. Slim orientation header + current mode (PERSONAL / COLLECTIVE / ACTIVITY) always visible. Source: Shawn's spec §10 composition A; #1290 contract.
- **WHAT MATTERS?** → the focus strip: one or a few highest-value items (Shawn's spec §10-B), then the stream. New-since-last-visit marked by the new-intelligence seam.
- **WHAT CAN I DO?** → switch mode (3 large controls); per object: Open, Ask Naya, Save/Favorite. Source: #1290 primary actions.
- **WHAT HAPPENS NEXT?** → mode switch re-materializes the stream with new data; Open reveals the object; Ask Naya explains; Save files to Library. Predictable before acting.

## R.3 Applicable laws

- **H1 Purpose before interface** → the room's job ("receive useful intelligence without checking every room") fixed the composition before any visual treatment. Source: Shawn's spec §10 human job.
- **H2 Distill before display** → focus strip + essence/nutshell per item; raw event volume never shown directly. Source: Shawn's spec §10-B/C.
- **H3 Recognition before recall** → three visible mode controls; no hidden gestures for primary navigation.
- **H4 One obvious next action** → primary action per Shawn: "open/act on the highest-value intelligence item."
- **H5 Perceptible state + immediate feedback** → 11 named room states (LOADING…DISABLED); each preserves room identity, no generic error card. Source: #1290 contract states.
- **H6 Prevent error before explaining error** → no destructive primary actions in the stream; consequential actions live behind Open/bottom sheet. (Contract-derived; no explicit error-prevention copy in sources — guard in R.8.)
- **H7 Complexity stays in the machine** → filters progressive, never spread across the canvas. Source: #1290 contract.
- **H8 Stable grammar, adaptive intelligence** → one continuous vertical river always; content/priority adapt per mode. Source: Shawn's spec §10 (mode changes data, not only color).
- **H9 Direct manipulation when it clarifies causality** → N/A with reason: the stream is read/triage; manipulation lives in object actions (bottom sheet), the correct scope. Neither source specifies direct manipulation here.
- **H10 Design must learn from human outcomes** → ranking law inputs (relevance, consequence, unresolved status) are outcome-shaped; promotion requires evidence per v1.3 learning rules. No learning loop specified for ranking yet — OPEN (see R.9).
- **V1 Meaning before decoration** → jewel identity + truth state carry meaning; emerald energy marks live objects only.
- **V2 Hierarchy before density** → focus strip first, stream second, Naya synthesis third. Source: Shawn's spec §10 A–D.
- **V3 Depth before glow** → emerald semantic energy on live objects; edge/elevation for importance, not decorative gradients. Source: #1290 contract.
- **V4 State before animation** → restrained state-linked motion only; no fake pulsing stream. Source: #1290 contract.
- **V5 Contrast before novelty** → current mode and new-since-last-visit immediately legible; novelty never at the cost of legibility.
- **V6 One coherent icon/material family** → jewel identity per object type from the single family. Source: Shawn's spec §10 item anatomy (jewel).
- **V7 Tokens before one-off styling** → room theme emerald via tokens; no per-object color inventions.
- **V8 Interaction must feel intentional** → mode switch re-materializes data (not a filter tint); every control has a causal path (R.6).
- **V9 Premium must remain fast** → variable-height objects, bounded stream; performance budget per v1.3. Exact budgets OPEN — not specified for this room in sources.
- **V10 Preserve the working baseline** → the river model is the baseline; any replacement must prove superior. No replacement proposed.

## R.4 Cognitive checks

- **attention** → focus strip + new seam win first glance. Correct: they answer "what changed since I was here."
- **choice complexity** → 3 modes, not 30 filters. Filters deferred progressively. PASS.
- **target acquisition** → three large mode controls, sticky/reachable; object actions in accessible bottom sheet (thumb-reachable).
- **memory burden** → "why now" printed per object (Shawn's spec item anatomy); scroll restoration + return position remove spatial recall. Source: #1290 contract.
- **mental model** → a river of intelligence, not an algorithmic feed; Activity mode is factual chronology, not recommendations. Source: Shawn's spec §10.
- **feedback latency** → new verified objects enter with immediate restrained motion; mode switch re-materializes without spinners where possible.
- **error probability** → no destructive primary actions in-stream; low by construction.
- **recovery** → scroll restoration; back returns to exact position. Source: #1290 contract.
- **progressive disclosure** → filters, tags, relationships appear only when useful; evidence depth optional per item. Source: Shawn's spec item anatomy.
- **trust** → truth state + provenance on every object, always available. Ranking law: never hide critical items. Source: Shawn's spec §10 ranking law.

## R.5 Computable predicates

- **P-HICK** — ≤4 sibling choices per disclosure level → 3 mode controls; per-object actions concise (Open / Ask Naya / Save). **PASS** (spec count). Source: both.
- **P-FITTS** — primary targets large + reachable → three large sticky mode controls; bottom-sheet actions thumb-reachable. **PASS** (spec); re-verify at render.
- **P-MILLER** — ≤4 chunks to triage → jewel + title + nutshell + why-now visible per object; no recall required. **PASS** (spec).
- **P-DOHERTY** — acknowledge <400ms → new-arrival seam immediate; mode switch without spinners where possible. **UNMEASURABLE** — no render seat (13th lock open); never PASS by default.

## R.6 Causal paths (per control)

- **MODE SWITCH (Personal/Collective/Activity)** → INTENT: change intelligence scope → SCOPE/AUTHORITY: user's consented visibility → CAPABILITY: stream re-query → OBSERVATION: stream re-materializes → UI_STATE: mode header + seam update → EVIDENCE: mode label + provenance preserved per object. Source: Shawn's spec §10 (mode changes data).
- **OPEN (object)** → INTENT: inspect intelligence → SCOPE: single object → CAPABILITY: object detail → OBSERVATION: detail view → UI_STATE: object expanded/sheet → EVIDENCE: provenance + truth state shown.
- **ASK NAYA** → INTENT: explain/summarize → SCOPE: visible objects + uncertainty → CAPABILITY: Naya explanation → OBSERVATION: answer with exposed uncertainty → UI_STATE: inline explanation → EVIDENCE: sources cited.
- **SAVE / FAVORITE** → INTENT: preserve → SCOPE: single object → CAPABILITY: library write → OBSERVATION: saved confirmation → UI_STATE: saved marker → EVIDENCE: library location shown.

## R.7 Benchmark-to-beyond

- **Frontier surveyed:** social feeds (pattern fluency), Superhuman-style triage speed, Oura-level distillation. (Proposal — not in sources.)
- **Principles extracted:** continuous vertical rhythm; ruthless distillation; calm over dense.
- **What we preserve (already better):** governed truth states + provenance on every object; mode changes data not color; ranking law that never hides critical items. No benchmark combines all three.
- **Beyond-benchmark option:** an intelligence river with truth-state physics — objects rise by verified relevance, Naya narrates the seam between visits, provenance structural not decorative. Anti-feed failure per Shawn: never engagement bait, never mysterious ranking.
- **10× claim:** ambition only. Candidate metric (not in sources): time-to-"what matters" vs. baseline triage + comprehension spot-checks. No factor claimed.

## R.8 Anti-patterns watched

- **fake_liveness** → guard: new-arrival seam only for verified objects; "no fake pulsing stream" in contract. Source: #1290 "must never become."
- **spectacle_over_readability** → guard: variable-height objects, calm reading rhythm.
- **engagement bait / vanity metrics** → guard: no engagement numbers; ranking inputs are relevance/consequence, never dwell.
- **mysterious ranking** → guard: ranking law inspectable; Naya explains why-now per object.
- **generic_dashboard_conversion** → guard: focus strip is 1–3 items, never a KPI row (Shawn: "not a KPI row").
- **self_grading_as_final_proof** → guard: acceptance requires independent verification (R.9), never builder self-score.

## R.9 Acceptance

- **Cold-Naya test:** read this doc → explain the Feed's promise → identify its DNA (emerald living-depth + truth physics + mode-changes-data) → propose one bounded improvement with evidence → leave the room better.
- **Taste items for Shawn (queued, never decided by machine):** exact motion-restraint values for the new-intelligence seam; focus-strip cardinality (1 vs 3); Activity-mode final composition (noted open in #1290 functional spec).
- **OPEN:** ranking-weight learning loop unspecified in sources — how verified outcomes tune ranking weights is not defined. P-DOHERTY UNMEASURABLE until render seat exists.

## Working notes

- 2026-10-02 — Document created (CANDIDATE) from Shawn's spec §10 + #1290 contracts + v1.3. No divergence between Shawn's spec and #1290 on this room.
