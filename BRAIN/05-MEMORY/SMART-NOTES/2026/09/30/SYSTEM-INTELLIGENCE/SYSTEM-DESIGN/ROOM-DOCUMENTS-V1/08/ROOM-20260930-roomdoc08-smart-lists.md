# ROOM-08 — Smart Lists · Official Room Design Document (CANDIDATE)

**Status:** CANDIDATE — drafted 2026-10-02 by Naya 4 (subagent). Not ratified, not merged.
**Route:** `/lists` · **Metaphor:** THE MISSION TABLE · **Theme:** purple
**Parent law (wins on conflict):** `HUB/NAYANET-SMART-APP-ROOM-SPEC-V1.md` §17 (Shawn, canonical, main)
**Sources:** Shawn's spec §17; `HUB/ROOMS/08-smart-lists/FUNCTIONAL-SPEC.md` + `DESIGN-CONTRACT.md` (PR #1290, open); Naya Design Intelligence v1.3; DI-INFUSION-0001 R.1–R.9 shape.

No divergences; #1290's Manual/Smart/Hybrid maps cleanly onto Shawn's six list types.

## R.1 Room outcome

Create persistent, useful views of intelligence without manual duplication — what I'm deliberately organizing, tracking or returning to, kept alive.

## R.2 Surface questions

- **WHERE AM I?** → `/lists`. List collection selector (left/upper) + active list center + context layer (why it matters, rules, Naya suggestions, status). Source: #1290 signature visual.
- **WHAT MATTERS?** → the active list's purpose + why items qualify + list status. Source: Shawn's spec §17 list view order.
- **WHAT CAN I DO?** → Create List, Add item, Remove, Pin/reorder, Set smart rule, Ask Naya to organize, Open item, Share (governed), Convert to Space/report where real. Source: #1290 primary actions.
- **WHAT HAPPENS NEXT?** → items open in place by reference; smart lists update by rule with human pinning preserved (hybrid); share/export governed. Source: #1290 list types; Shawn's spec §17.

## R.3 Applicable laws

- **H1 Purpose before interface** → job: "create persistent, useful views of intelligence without manual duplication." Mission table, not spreadsheet.
- **H2 Distill before display** → "why items qualify" printed per list — the rule is the distillation. Source: Shawn's spec §17.
- **H3 Recognition before recall** → list types visible (manual / rule-based / dynamic / project / watch / follow-up); smart rules readable, not remembered. Source: Shawn's spec §17.
- **H4 One obvious next action** → primary action per Shawn: "open the most relevant list or create one."
- **H5 Perceptible state + immediate feedback** → list metadata (purpose, owner, Space, smart/manual mode, last updated, sharing state) visible; item add/remove confirms. Source: #1290.
- **H6 Prevent error before explaining error** → "Convert list into Space/report only where a real operation exists" — prevents fake conversions. Share governed. Source: #1290.
- **H7 Complexity stays in the machine** → smart rules evaluate underneath; human sees the qualifying reason.
- **H8 Stable grammar, adaptive intelligence** → list view order stable (title/purpose → why-qualify → stream → rules → actions); "Ask Naya to organize" adapts. Source: Shawn's spec §17.
- **H9 Direct manipulation when it clarifies causality** → APPLIES: "Direct manipulation is appropriate when it improves understanding, but drag/drop is not mandatory if another method is more accessible." Source: Shawn's spec §17. Pin/reorder by the most accessible working method.
- **H10 Design must learn** → smart rules + Naya suggestions should improve from outcomes; mechanics OPEN.
- **V1 Meaning before decoration** → purple = deliberate organization/mission; list items are intelligence objects, not rows.
- **V2 Hierarchy before density** → purpose → why-qualify → stream → rules → actions. Source: Shawn's spec §17.
- **V3 Depth before glow** → mission-table depth; restrained.
- **V4 State before animation** → smart/manual mode + last-updated lead; reorder motion restrained.
- **V5 Contrast before novelty** → the list's purpose line highest contrast.
- **V6 One icon/material family** → list-type jewels from the single family.
- **V7 Tokens before one-off styling** → purple via tokens.
- **V8 Interaction must feel intentional** → "Not a generic spreadsheet unless the task specifically benefits from tabular comparison." Source: #1290.
- **V9 Premium must remain fast** → exact budgets OPEN.
- **V10 Preserve baseline** → reference-not-copy is the baseline: "A Smart List should reference canonical objects, not copy them into a shadow store." Source: Shawn's spec §17.

## R.4 Cognitive checks

- **attention** → active list's purpose + status win first glance. Correct.
- **choice complexity** → 6 list types; per-item actions concise; smart-rule builder progressive.
- **target acquisition** → pin/reorder targets large; mobile accessible alternative to drag/drop. Source: Shawn's spec §17.
- **memory burden** → "why items qualify" + list purpose externalized; no recall of list intent.
- **mental model** → a mission table: campaigns with rules, not a spreadsheet. Matches.
- **feedback latency** → add/remove/pin immediate; smart-rule evaluation acknowledged.
- **error probability** → destructive remove confirmed; fake conversions prevented by "only where real."
- **recovery** → remove reversible (trash/undo pattern expected — not specified in sources; OPEN as explicit requirement).
- **progressive disclosure** → list → item → rule detail → Naya suggestions.
- **trust** → each item retains canonical object identity + provenance; sharing state visible. Source: #1290; Shawn's spec §17.

## R.5 Computable predicates

- **P-HICK** — ≤4 sibling choices per level → 6 types grouped (manual/smart/hybrid); per-item actions ≤5. **PASS with grouping** (spec).
- **P-FITTS** — pin/reorder/create targets large; accessible non-drag alternative. **PASS** (spec); re-verify at render.
- **P-MILLER** — list view ≤4 chunks (purpose / why-qualify / stream / rules+actions). **PASS** (spec).
- **P-DOHERTY** — reorder/add <400ms. **UNMEASURABLE** — no render seat.

## R.6 Causal paths (per control)

- **CREATE LIST** → INTENT: organize → SCOPE: chosen type → CAPABILITY: list creation → OBSERVATION: new list → UI_STATE: list view → EVIDENCE: list metadata (purpose/owner/Space).
- **SET SMART RULE** → INTENT: automate membership → SCOPE: rule definition → CAPABILITY: rule engine → OBSERVATION: qualifying items → UI_STATE: stream + why-qualify → EVIDENCE: rule text shown.
- **PIN / REORDER** → INTENT: prioritize → SCOPE: one item → CAPABILITY: order update (hybrid preserves pins) → OBSERVATION: new order → UI_STATE: stream → EVIDENCE: order state.
- **ASK NAYA TO ORGANIZE** → INTENT: delegate organizing → SCOPE: list context → CAPABILITY: organization assist → OBSERVATION: suggestions → UI_STATE: suggestion layer → EVIDENCE: suggestion reasons.
- **SHARE LIST** → INTENT: distribute → SCOPE/AUTHORITY: governed → CAPABILITY: share → OBSERVATION: confirmation → UI_STATE: sharing state → EVIDENCE: share receipt.
- **CONVERT TO SPACE/REPORT** → INTENT: escalate context → SCOPE/AUTHORITY: only where real operation exists → CAPABILITY: conversion → OBSERVATION: new space/report → UI_STATE: target room → EVIDENCE: lineage link.

## R.7 Benchmark-to-beyond

- **Frontier surveyed:** task managers, read-later apps, smart playlists. (Proposal.)
- **Principles extracted:** rule-driven membership; human override; reference not copy.
- **What we preserve:** hybrid pinning (human order survives rule re-evaluation); why-qualify printed; reference-not-copy — playlists don't preserve provenance.
- **Beyond-benchmark option:** lists that explain themselves — every item carries its qualifying reason, every rule is readable, Naya suggests organizations with reasons.
- **10× claim:** ambition only. Candidate metric: list-maintenance effort vs. manual lists. No factor claimed.

## R.8 Anti-patterns watched

- **generic spreadsheet** → guard: "Not a generic spreadsheet unless the task specifically benefits from tabular comparison." Source: #1290.
- **shadow store** → guard: reference canonical objects, never copy. Source: Shawn's spec §17.
- **fake conversions** → guard: convert only where a real operation exists. Source: #1290.
- **unmeasured_improvement** → guard: Naya suggestions carry reasons; accepted/rejected visibly.
- **client_state_as_canonical_truth** → guard: smart-list membership re-evaluated against canonical objects.
- **self_grading_as_final_proof** → guard: human acceptance per R.9.

## R.9 Acceptance

- **Cold-Naya test:** read this doc → explain the mission-table promise → identify DNA (purple deliberation + why-qualify + reference-not-copy) → propose one bounded improvement with evidence.
- **Taste items for Shawn:** mission-table visual language (how "campaign-like"); smart-rule builder complexity ceiling; Naya-suggestion prominence.
- **OPEN:** remove/undo mechanics unspecified in sources — required before build; smart-rule evaluation cadence unspecified.

## Working notes

- 2026-10-02 — Document created (CANDIDATE). No divergences.
