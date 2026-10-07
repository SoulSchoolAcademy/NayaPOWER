# ROOM-04 — Intelligent Library · Official Room Design Document (CANDIDATE)

**Status:** CANDIDATE — drafted 2026-10-02 by Naya 4 (subagent). Not ratified, not merged.
**Route:** `/library` · **Metaphor:** THE VAULT · **Theme:** sapphire
**Parent law (wins on conflict):** `HUB/NAYANET-SMART-APP-ROOM-SPEC-V1.md` §13 (Shawn, canonical, main)
**Sources:** Shawn's spec §13; `HUB/ROOMS/04-intelligent-library/FUNCTIONAL-SPEC.md` + `DESIGN-CONTRACT.md` (PR #1290, open); Naya Design Intelligence v1.3; DI-INFUSION-0001 R.1–R.9 shape.

No divergences; #1290's Drive-note reconciliation (domain rooms, "What am I missing here?") extends Shawn's spec without contradicting it.

## R.1 Room outcome

Find, understand, trust and reuse durable intelligence — everything worth retaining findable without remembering where it originally appeared.

## R.2 Surface questions

- **WHERE AM I?** → `/library`. Search-first header as the hero instrument; Library identity + current Space + search focus visible. Source: Shawn's spec §13; #1290.
- **WHAT MATTERS?** → featured intelligence (MOST RELEVANT / RECENTLY DEVELOPED / NEEDS ATTENTION) + YOUR KNOWLEDGE domain objects. Source: #1290 Drive-note reconciliation.
- **WHAT CAN I DO?** → search (natural language + semantic), browse, open, Ask Naya ("What am I missing here?"), save/favorite, add to list, see relationships, open source. Source: #1290 primary actions.
- **WHAT HAPPENS NEXT?** → result opens detail (nutshell → meaning → provenance → relationships → proof); any object moves by reference to other rooms without copying canonical truth. Source: #1290 cross-room handoffs.

## R.3 Applicable laws

- **H1 Purpose before interface** → job: "find, understand, trust and reuse durable intelligence." Organized by meaning, not file location. Source: #1290 promise.
- **H2 Distill before display** → result cards show essence + why-relevant, not full content; detail opens nutshell-first. Source: #1290 search behavior; Shawn's spec §13.
- **H3 Recognition before recall** → the room's core promise: "without remembering where it originally appeared." Facets visible (topic/person/space/type/truth state/source/date).
- **H4 One obvious next action** → primary action per Shawn: "search/open the relevant intelligence object." Search is the hero.
- **H5 Perceptible state + immediate feedback** → truth-state filters (verified/unverified); empty state says RUNTIME UNAVAILABLE / NOT VERIFIED, never sample shelves. Source: #1290.
- **H6 Prevent error before explaining error** → governed Share; no destructive actions specified in-room. Trust-state visible before use prevents acting on unverified intel as verified.
- **H7 Complexity stays in the machine** → semantic search absorbs query complexity; human sees results with why-relevant.
- **H8 Stable grammar, adaptive intelligence** → Search/Browse/Saved/Recent views stable; featured intelligence adapts.
- **H9 Direct manipulation** → N/A with reason: search/open/read dominate; map/relationship view optional and explicitly "only when graph view adds value." Source: #1290.
- **H10 Design must learn** → learning status is a facet; "recently developed / needs attention" surfaces learning. Promotion mechanics per v1.3; loop unspecified — OPEN.
- **V1 Meaning before decoration** → result = intelligence object, not file thumbnail. Source: #1290.
- **V2 Hierarchy before density** → search hero → featured → domains → results with progressive disclosure. Source: Shawn's spec §13.
- **V3 Depth before glow** → vault depth; sapphire as meaning (knowledge/trust).
- **V4 State before animation** → result-state (truth state, last meaningful update) leads; motion restrained.
- **V5 Contrast before novelty** → the search field is the highest-contrast element.
- **V6 One icon/material family** → object-type jewels from the single family.
- **V7 Tokens before one-off styling** → sapphire via tokens.
- **V8 Interaction must feel intentional** → every result explains why it matched ("why relevant"). Source: #1290 acceptance journey.
- **V9 Premium must remain fast** → search-first mobile; exact budgets OPEN.
- **V10 Preserve baseline** → semantic-organization baseline; "Do not turn the default into a filesystem." Source: #1290.

## R.4 Cognitive checks

- **attention** → the search field wins first glance. Correct: the room's job starts with a question.
- **choice complexity** → facets grouped (9 filters); views limited to 4–5.
- **target acquisition** → search field large, top; mobile search-first.
- **memory burden** → zero by design: semantic search + why-relevant + provenance remove recall entirely. This room IS the memory-burden solution.
- **mental model** → a vault/gallery of knowledge, not a filesystem. Explicitly guarded. Source: #1290.
- **feedback latency** → result streaming; why-relevant attached per result.
- **error probability** → acting on wrong-truth-state prevented by visible truth filters; governed share.
- **recovery** → search refinable; detail back to results; no destructive actions.
- **progressive disclosure** → card → detail (nutshell → meaning → provenance → relationships → proof). Source: Shawn's spec §13 object detail.
- **trust** → provenance, truth state, last meaningful update, source relationships on every object; contradictions/supersession shown, not hidden. Source: Shawn's spec §13.

## R.5 Computable predicates

- **P-HICK** — ≤4 sibling choices per level → 4–5 views; 9 facets grouped in a sheet on mobile. **PASS** (spec).
- **P-FITTS** — hero search field large; result targets full-row. **PASS** (spec); re-verify at render.
- **P-MILLER** — result card ≤4 chunks (essence / why-relevant / provenance / state). **PASS** (spec).
- **P-DOHERTY** — keystroke-to-results <400ms aspiration. **UNMEASURABLE** — no render seat; also depends on runtime retrieval availability.

## R.6 Causal paths (per control)

- **SEARCH** → INTENT: find intelligence → SCOPE: query + facets → CAPABILITY: semantic retrieval → OBSERVATION: ranked results with why-relevant → UI_STATE: results list → EVIDENCE: per-result provenance + truth state.
- **OPEN (result)** → INTENT: understand object → SCOPE: one object → CAPABILITY: detail projection → OBSERVATION: nutshell → meaning → proof → UI_STATE: detail view → EVIDENCE: provenance/relationships/supersession.
- **ASK NAYA ("What am I missing here?")** → INTENT: find gaps → SCOPE: current domain/results → CAPABILITY: gap analysis → OBSERVATION: answer → UI_STATE: inline answer → EVIDENCE: cited objects.
- **SAVE / ADD TO LIST** → INTENT: retain/organize → SCOPE: one object → CAPABILITY: reference (not copy) → OBSERVATION: confirmation → UI_STATE: saved marker → EVIDENCE: canonical object identity preserved.
- **OPEN SOURCE** → INTENT: verify origin → SCOPE: one object → CAPABILITY: source link → OBSERVATION: source view → UI_STATE: source context → EVIDENCE: origin canonical record.

## R.7 Benchmark-to-beyond

- **Frontier surveyed:** enterprise search, note apps, knowledge graphs. (Proposal.)
- **Principles extracted:** semantic over keyword; why-relevant explanations; provenance-first.
- **What we preserve:** organized by meaning not location; contradictions/supersession as first-class (no benchmark shows what an idea replaced); objects move by reference, never copied.
- **Beyond-benchmark option:** a vault where every object answers "what have we already learned that can help now?" — with its own uncertainty ("What I'm uncertain about") and Naya's gap analysis per domain.
- **10× claim:** ambition only. Candidate metric: vague-memory retrieval success rate. No factor claimed.

## R.8 Anti-patterns watched

- **fake_data** → guard: RUNTIME UNAVAILABLE / NOT VERIFIED states, "not sample shelves." Source: #1290 empty state.
- **generic_dashboard_conversion** → guard: no KPI cards; featured intelligence is relevance, not metrics.
- **client_state_as_canonical_truth** → guard: objects move by reference; canonical identity retained. Source: #1290.
- **identity_erasure** → guard: provenance + source relationships always visible; "where it has been used" tracked. Source: #1290 detail view.
- **spectacle_over_readability** → guard: map/graph view only when it adds value, never default.
- **self_grading_as_final_proof** → guard: human acceptance journey (vague-memory search test).

## R.9 Acceptance

- **Cold-Naya test:** read this doc → explain the vault promise → identify DNA (sapphire knowledge + meaning-not-location + reference-not-copy) → propose one bounded improvement with evidence.
- **Taste items for Shawn:** domain-room visual language ("What I know / learned / uncertain about" per domain); featured-intelligence editorial line (how much Naya curates vs. ranks).
- **OPEN:** semantic retrieval mechanics are runtime-side (correctly out of room scope); learning-promotion surfacing ("recently developed") thresholds unspecified.

## Working notes

- 2026-10-02 — Document created (CANDIDATE). No divergences.
