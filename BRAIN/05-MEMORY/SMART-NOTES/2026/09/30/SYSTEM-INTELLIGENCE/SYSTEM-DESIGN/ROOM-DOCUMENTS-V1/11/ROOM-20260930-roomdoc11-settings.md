# ROOM-11 — Settings · Official Room Design Document (CANDIDATE)

**Status:** CANDIDATE — drafted 2026-10-02 by Naya 4 (subagent). Not ratified, not merged.
**Route:** `/settings` · **Metaphor:** THE CONTROL DECK · **Theme:** neutral gray with semantic accents
**Parent law (wins on conflict):** `HUB/NAYANET-SMART-APP-ROOM-SPEC-V1.md` §20 (Shawn, canonical, main)
**Sources:** Shawn's spec §20; `HUB/ROOMS/11-settings/FUNCTIONAL-SPEC.md` + `DESIGN-CONTRACT.md` (PR #1290, open); Naya Design Intelligence v1.3; DI-INFUSION-0001 R.1–R.9 shape.

No divergences; #1290's category detail nests cleanly under Shawn's §20 category list.

## R.1 Room outcome

Understand and control the relationship with NayaNET — clear categories, current state, no hidden consequential setting.

## R.2 Surface questions

- **WHERE AM I?** → `/settings`. Category deck: Identity & Account, Privacy & Sharing, Permissions/Authority, Connections/Smart Doors, Personalization, Notifications, Appearance, Accessibility, Data/Export/Retention, Advanced/Developer. Source: Shawn's spec §20.
- **WHAT MATTERS?** → current state per category; consequential settings surfaced, never buried. "No hidden consequential setting."
- **WHAT CAN I DO?** → varies by category — "the landing surface should not manufacture a universal primary CTA." Source: Shawn's spec §20.
- **WHAT HAPPENS NEXT?** → consequential changes require explicit wording + confirmation proportional to impact; plain language first, technical identifiers secondary. Source: Shawn's spec §20.

## R.3 Applicable laws

- **H1 Purpose before interface** → job: "understand and control the relationship with NayaNET." Control deck, not form dump.
- **H2 Distill before display** → human-concern categories distill implementation machinery; System Health advanced section holds the machinery. Source: #1290.
- **H3 Recognition before recall** → named categories; current state visible per category — no recall of what was set.
- **H4 One obvious next action** → N/A with reason — Shawn explicitly: no manufactured universal CTA on the landing surface. The honest N/A.
- **H5 Perceptible state + immediate feedback** → current state per category; change confirmations explicit.
- **H6 Prevent error before explaining error** → confirmation proportional to impact; plain-language wording before technical identifiers. Load-bearing for this room. Source: Shawn's spec §20.
- **H7 Complexity stays in the machine** → implementation machinery behind Advanced; human sees concerns.
- **H8 Stable grammar, adaptive intelligence** → category grammar stable; Naya preferences adapt assistance behavior.
- **H9 Direct manipulation** → N/A with reason: settings are discrete controls; direct manipulation not specified in either source.
- **H10 Design must learn** → preference changes are outcome signals; mechanics OPEN.
- **V1 Meaning before decoration** → neutral gray = calm control; semantic accents only where meaning demands (e.g., destructive actions).
- **V2 Hierarchy before density** → categories → current state → control; no setting walls.
- **V3 Depth before glow** → control-deck depth; restrained.
- **V4 State before animation** → state changes explicit; no animation implying safety not present.
- **V5 Contrast before novelty** → consequential/destructive controls highest contrast.
- **V6 One icon/material family** → category jewels from the single family.
- **V7 Tokens before one-off styling** → neutral gray via tokens; semantic accents tokenized.
- **V8 Interaction must feel intentional** → every control with its causal path visible (what it does, what it affects). The deck's signature.
- **V9 Premium must remain fast** → exact budgets OPEN.
- **V10 Preserve baseline** → the plain-language-first baseline: technical identifiers secondary. Source: Shawn's spec §20.

## R.4 Cognitive checks

- **attention** → consequential settings surfaced, not buried. Correct.
- **choice complexity** → 10 categories; controls progressive within category.
- **target acquisition** → category targets large; destructive actions well-spaced (fat-finger prevention expected — not specified; OPEN as explicit requirement).
- **memory burden** → current state per category; no recall of prior settings.
- **mental model** → a control deck / bridge: each control does one understandable thing. Matches.
- **feedback latency** → toggles acknowledge immediately; consequential changes confirm before applying.
- **error probability** → impact-proportional confirmation; plain-language wording. Load-bearing.
- **recovery** → reversible where possible; destructive actions confirmed + (expected) undo window — undo specifics OPEN in sources.
- **progressive disclosure** → category → control → advanced/technical identifiers.
- **trust** → no hidden consequential settings; data/export/retention controls visible where supported. Source: #1290; Shawn's spec §20.

## R.5 Computable predicates

- **P-HICK** — ≤4 sibling choices per level → 10 categories grouped (Account/Privacy/Connections/Preferences/System); controls progressive. **PASS with grouping** (spec).
- **P-FITTS** — category targets large; destructive actions spaced. **PASS** (spec); re-verify at render, especially destructive spacing.
- **P-MILLER** — per-control ≤4 chunks (what / affects / current-state / consequence). **PASS** (spec).
- **P-DOHERTY** — toggle ack <400ms; consequential flows confirm-first. **UNMEASURABLE** — no render seat.

## R.6 Causal paths (per control)

- **PRIVACY/SHARING DEFAULT** → INTENT: set default scope → SCOPE/AUTHORITY: explicit wording, confirmed → CAPABILITY: policy update → OBSERVATION: new default → UI_STATE: category state → EVIDENCE: policy record.
- **DISCONNECT / REVOKE (door)** → INTENT: close channel → SCOPE/AUTHORITY: confirmed proportionally → CAPABILITY: revoke → OBSERVATION: disconnected → UI_STATE: door health → EVIDENCE: revocation receipt.
- **NOTIFICATION/QUIET MODE** → INTENT: control interruption → SCOPE: channels/priority → CAPABILITY: preference update → OBSERVATION: new behavior → UI_STATE: category state → EVIDENCE: preference record.
- **DATA EXPORT / RETENTION** → INTENT: own my data → SCOPE/AUTHORITY: where supported → CAPABILITY: export → OBSERVATION: artifact → UI_STATE: confirmation → EVIDENCE: export record.
- **ACCESSIBILITY CONTROL** → INTENT: adapt experience → SCOPE: appearance/motion → CAPABILITY: preference apply → OBSERVATION: immediate change → UI_STATE: applied state → EVIDENCE: preference record.

## R.7 Benchmark-to-beyond

- **Frontier surveyed:** OS settings apps, SaaS admin panels. (Proposal.)
- **Principles extracted:** human-concern grouping; impact-proportional confirmation; plain language.
- **What we preserve:** no manufactured CTA; causal path visible per control; plain-language-first with technical secondary — admin panels do the reverse.
- **Beyond-benchmark option:** a control deck where every switch tells you what it does, what it affects, and what happens if you flip it — in plain language, before you touch it.
- **10× claim:** ambition only. Candidate metric: misconfigured-setting rate + "I didn't know that was on" incidents (must trend to zero). No factor claimed.

## R.8 Anti-patterns watched

- **dark patterns** (trust) → guard: no hidden consequential settings; confirmation proportional to impact. Source: Shawn's spec §20.
- **mystery meat controls** → guard: causal path visible per control; plain language first. Source: Shawn's spec §20.
- **destructive without confirmation** → guard: explicit wording + confirmation; spacing. Source: Shawn's spec §20.
- **settings maze** → guard: 10 named categories; Advanced holds machinery. Source: #1290.
- **client_state_as_canonical_truth** → guard: settings state from canonical records.
- **self_grading_as_final_proof** → guard: human acceptance per R.9.

## R.9 Acceptance

- **Cold-Naya test:** read this doc → explain the control-deck promise → identify DNA (neutral calm + causal-path-per-control + plain-language-first) → propose one bounded improvement with evidence.
- **Taste items for Shawn:** category order and grouping; destructive-action visual language; how "advanced" the Advanced section gets.
- **OPEN:** destructive-action spacing minimums unspecified; undo windows for consequential changes unspecified; export formats unspecified in sources.

## Working notes

- 2026-10-02 — Document created (CANDIDATE). No divergences.
