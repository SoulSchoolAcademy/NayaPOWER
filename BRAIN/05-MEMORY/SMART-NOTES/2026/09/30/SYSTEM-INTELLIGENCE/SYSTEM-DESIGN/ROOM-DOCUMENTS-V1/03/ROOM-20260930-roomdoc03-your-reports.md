# ROOM-03 — Your Reports · Official Room Design Document (CANDIDATE)

**Status:** CANDIDATE — drafted 2026-10-02 by Naya 4 (subagent). Not ratified, not merged.
**Route:** `/reports` · **Metaphor:** THE FILM ROOM · **Theme:** indigo
**Parent law (wins on conflict):** `HUB/NAYANET-SMART-APP-ROOM-SPEC-V1.md` §12 (Shawn, canonical, main)
**Sources:** Shawn's spec §12; `HUB/ROOMS/03-your-reports/FUNCTIONAL-SPEC.md` + `DESIGN-CONTRACT.md` (PR #1290, open); Naya Design Intelligence v1.3; DI-INFUSION-0001 R.1–R.9 shape.

No divergences between Shawn's spec and #1290 on this room; they are complementary (Shawn: anatomy + law; #1290: projection boundary + compare mode + handoffs).

## R.1 Room outcome

Understand patterns, progress, changes and meaning across time — turn accumulated intelligence into understandable synthesis, not record counts.

## R.2 Surface questions

- **WHERE AM I?** → `/reports`. Top: featured current report + period selector + scope/Space + freshness and verification. Source: #1290 signature visual; Shawn's spec §12 (3-second: selected time scope + primary conclusion).
- **WHAT MATTERS?** → executive meaning: what changed and why it matters. Source: Shawn's spec §12 anatomy item 1.
- **WHAT CAN I DO?** → Open report, Ask Naya, Compare periods, Inspect evidence, Save / Add to List, Share (governed), Export where supported. Source: #1290 primary actions.
- **WHAT HAPPENS NEXT?** → opening a report unrolls narrative → evidence; compare shows changed/improved/declined/newly learned/unresolved/contradictory; consequential conclusions route to Ledger/Lists. Predictable.

## R.3 Applicable laws

- **H1 Purpose before interface** → job fixed: "understand patterns, progress, changes and meaning across time." Report theater, not table UI.
- **H2 Distill before display** → executive meaning first; evidence appendix last. "A report is not '37 records found.'" Source: #1290 promise.
- **H3 Recognition before recall** → period selector + report types visible (Daily/Weekly/Monthly/Quarterly/Yearly; project/decision/learning/relationship/thematic). No remembered query syntax.
- **H4 One obvious next action** → primary action per Shawn: "inspect or act on the most consequential finding."
- **H5 Perceptible state + immediate feedback** → report freshness and verification shown at top; empty state explains missing data/runtime requirements honestly. Source: #1290.
- **H6 Prevent error before explaining error** → compare mode makes "no automatic good/bad judgment without declared criteria" — prevents misreading. Source: #1290. Share/export gated by governance.
- **H7 Complexity stays in the machine** → synthesis done upstream via governed pipeline; the room opens/compares/explains — it does not become the canonical report author. Source: #1290 projection boundary.
- **H8 Stable grammar, adaptive intelligence** → report anatomy stable (meaning → evidence → change → drivers → uncertainty → next moves → proof); content adapts per period/type.
- **H9 Direct manipulation** → N/A with reason: reading/comparison dominate; neither source specifies manipulation.
- **H10 Design must learn** → learning is a first-class report section ("what I learned"); promotion of lessons follows v1.3 evidence rules. Loop mechanics OPEN.
- **V1 Meaning before decoration** → visualizations only when they clarify meaning; "no ornamental charts." Source: Shawn's spec §12; #1290.
- **V2 Hierarchy before density** → featured report → nutshell → sections → evidence appendix.
- **V3 Depth before glow** → film-room depth; indigo as meaning (time/synthesis), not decoration.
- **V4 State before animation** → section transitions restrained; state (freshness/verification) leads.
- **V5 Contrast before novelty** → primary conclusion highest contrast, not the chart chrome.
- **V6 One icon/material family** → report-type jewels from the single family.
- **V7 Tokens before one-off styling** → indigo theme via tokens.
- **V8 Interaction must feel intentional** → compare mode deltas explicit (changed/improved/declined/newly learned/unresolved/contradictory). Source: #1290.
- **V9 Premium must remain fast** → progressive disclosure on mobile (cover → sections → evidence); exact budgets OPEN.
- **V10 Preserve baseline** → the report-anatomy order is the baseline; replacements must prove superior.

## R.4 Cognitive checks

- **attention** → primary conclusion wins first glance. Correct per Shawn's 3-second rule.
- **choice complexity** → time scopes (5) + report types (5) visible but grouped; compare is opt-in.
- **target acquisition** → period selector + featured report as large targets; mobile progressive disclosure.
- **memory burden** → uncertainty section states "known vs inferred vs unresolved" explicitly — no recall of what was proven. Source: Shawn's spec §12 anatomy.
- **mental model** → a film room/studio: watch the story, inspect the evidence. Matches.
- **feedback latency** → report open immediate from mirror; generation happens upstream (projection boundary honest about async).
- **error probability** → misreading prevented by declared-criteria rule in compare; share/export governed.
- **recovery** → back to report list; compare dismissible; no destructive actions.
- **progressive disclosure** → nutshell → sections → evidence appendix → drill-down proof layer. Source: Shawn's spec §12.
- **trust** → every conclusion links to canonical evidence + report-generation provenance. Source: #1290 five-layer mapping (PROOF).

## R.5 Computable predicates

- **P-HICK** — ≤4 sibling choices per level → 5 time scopes grouped; 7 anatomy sections sequential. **PASS** (spec).
- **P-FITTS** — period selector + featured report large targets. **PASS** (spec); re-verify at render.
- **P-MILLER** — executive meaning ≤4 chunks (changed / why matters / evidence / next move). **PASS** (spec).
- **P-DOHERTY** — section expand <400ms; report arrival via projection adapter acknowledged. **UNMEASURABLE** — no render seat.

## R.6 Causal paths (per control)

- **PERIOD SELECTOR** → INTENT: change time scope → SCOPE: selected period → CAPABILITY: report retrieval → OBSERVATION: report renders → UI_STATE: period header + freshness → EVIDENCE: generation provenance shown.
- **COMPARE PERIODS** → INTENT: see change → SCOPE: two periods → CAPABILITY: diff computation → OBSERVATION: delta view → UI_STATE: compare mode → EVIDENCE: per-delta evidence links; no auto good/bad without criteria.
- **INSPECT EVIDENCE** → INTENT: verify a conclusion → SCOPE: one claim → CAPABILITY: proof drill-down → OBSERVATION: evidence layer → UI_STATE: appendix/deep view → EVIDENCE: canonical objects.
- **SHARE (governed)** → INTENT: distribute → SCOPE/AUTHORITY: governed share policy → CAPABILITY: share action → OBSERVATION: confirmation → UI_STATE: sharing state → EVIDENCE: share receipt.
- **CONSEQUENTIAL CONCLUSION → LEDGER/LIST** → INTENT: act on finding → SCOPE: one conclusion → CAPABILITY: handoff by reference → OBSERVATION: target room → UI_STATE: target context → EVIDENCE: same canonical object (no copy).

## R.7 Benchmark-to-beyond

- **Frontier surveyed:** BI dashboards, analyst report formats, "year in review" products. (Proposal.)
- **Principles extracted:** narrative-first; uncertainty stated; comparison as the unit of insight.
- **What we preserve:** projection boundary (room never fakes authorship); every conclusion evidence-linked; uncertainty as a first-class section — dashboards don't do this.
- **Beyond-benchmark option:** reports that arrive by themselves (projection/event adapter, no manual upload), carry their own uncertainty model, and compare periods without inventing judgments.
- **10× claim:** ambition only. Candidate metric: time-to-primary-conclusion + evidence-trace success rate. No factor claimed.

## R.8 Anti-patterns watched

- **fake_data** → guard: empty state says "No report can be generated from the available verified intelligence yet" — never sample reports. Source: #1290.
- **spectacle_over_readability** → guard: "visualization should communicate meaning, not decorate." Source: Shawn's spec §12.
- **unmeasured_improvement** → guard: compare deltas without declared criteria get no good/bad labels. Source: #1290.
- **client_state_as_canonical_truth** → guard: reports mirrored from upstream pipeline; room never generates canonical reports locally. Source: #1290 projection boundary.
- **competing_design_systems** → guard: single report anatomy across all types.
- **self_grading_as_final_proof** → guard: acceptance journey is human-executed.

## R.9 Acceptance

- **Cold-Naya test:** read this doc → explain the room's promise → identify DNA (indigo synthesis + narrative-first + uncertainty-stated) → propose one bounded improvement with evidence.
- **Taste items for Shawn:** report-cover visual language; chart style restraint level; yearly "Year in Intelligence" ceremony weight.
- **OPEN:** report-generation pipeline mechanics are upstream (out of room scope, correctly); compare-criteria declaration UX unspecified in sources.

## Working notes

- 2026-10-02 — Document created (CANDIDATE). No divergences; Shawn's spec and #1290 complementary.
