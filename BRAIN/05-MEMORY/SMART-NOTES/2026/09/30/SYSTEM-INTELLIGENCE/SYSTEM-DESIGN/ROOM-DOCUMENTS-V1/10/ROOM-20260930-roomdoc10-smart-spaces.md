# ROOM-10 — Smart Spaces · Official Room Design Document (CANDIDATE)

**Status:** CANDIDATE — drafted 2026-10-02 by Naya 4 (subagent). Not ratified, not merged.
**Route:** `/spaces` · **Metaphor:** THE WORLDS · **Theme:** lime
**Parent law (wins on conflict):** `HUB/NAYANET-SMART-APP-ROOM-SPEC-V1.md` §19 (Shawn, canonical, main)
**Sources:** Shawn's spec §19; `HUB/ROOMS/10-smart-spaces/FUNCTIONAL-SPEC.md` + `DESIGN-CONTRACT.md` (PR #1290, open); Naya Design Intelligence v1.3; DI-INFUSION-0001 R.1–R.9 shape.

No divergences; #1290's privacy-level warning ("Do not turn labels into security guarantees without runtime enforcement") reinforces Shawn's "never silently broadens authority."

## R.1 Room outcome

Enter a durable context — project, family, team, research, community — where the relevant people and intelligence belong together, and know exactly what context I'm in.

## R.2 Surface questions

- **WHERE AM I?** → `/spaces`. Gallery of context worlds; entering a space changes visible Hub context with a clear persistent indicator. Source: #1290; Shawn's spec §19 (3-second: "This space has a purpose, members, intelligence and current state.").
- **WHAT MATTERS?** → space object: identity, purpose, members/roles, privacy/scope, recent intelligence, current goal/state, primary action. Source: Shawn's spec §19.
- **WHAT CAN I DO?** → Enter Space, Create Space, Invite/connect, Set privacy/sharing, Add/link intelligence, Open Space Feed/Report, Open members, Ask Naya in this Space, Archive/leave (governed safeguards). Source: #1290 primary actions.
- **WHAT HAPPENS NEXT?** → entering re-contexts the Hub (persistent indicator); inside: space feed, intelligence, people, lists, reports, messages, activity/proof, Naya scoped to the space. Leaving/archiving guarded. Source: Shawn's spec §19; #1290 space home.

## R.3 Applicable laws

- **H1 Purpose before interface** → job: "enter a durable context where relevant people and intelligence belong together." Worlds, not folders.
- **H2 Distill before display** → space object distills context to purpose + goal + state; full member/intelligence lists on entry.
- **H3 Recognition before recall** → spaces as visible worlds with identity jewels; current-space indicator persistent — never rely on remembering which context is active.
- **H4 One obvious next action** → primary action per Shawn: "enter/resume the most relevant space."
- **H5 Perceptible state + immediate feedback** → privacy/scope visible per space; context indicator persistent; archive/leave guarded with explicit states.
- **H6 Prevent error before explaining error** → "A space never silently broadens authority." Privacy labels never imply guarantees without runtime enforcement. Create/invite flows show scope before commit. Source: Shawn's spec §19; #1290.
- **H7 Complexity stays in the machine** → space-scoped projections computed underneath; human sees one coherent context.
- **H8 Stable grammar, adaptive intelligence** → "The shell remains NayaNET. The space changes context, not product identity." Naya scoped to the space adapts. Source: Shawn's spec §19.
- **H9 Direct manipulation** → N/A with reason: entering/managing contexts are discrete flows; neither source specifies manipulation.
- **H10 Design must learn** → space health/open loops tracked; mechanics OPEN.
- **V1 Meaning before decoration** → lime = living context; identity jewel per space carries meaning.
- **V2 Hierarchy before density** → gallery → space object → space home (purpose → intelligence → people → activity).
- **V3 Depth before glow** → worlds with depth; entering feels like travel, glow restrained.
- **V4 State before animation** → context transitions reflect real scope change; no decorative world-switching theater.
- **V5 Contrast before novelty** → current-space indicator highest contrast — you must always know where you are.
- **V6 One icon/material family** → space jewels from the single family.
- **V7 Tokens before one-off styling** → lime via tokens.
- **V8 Interaction must feel intentional** → space home is "a context projection of existing rooms, not a second set of databases." Source: #1290.
- **V9 Premium must remain fast** → exact budgets OPEN.
- **V10 Preserve baseline** → the projection model (no second databases) is the baseline.

## R.4 Cognitive checks

- **attention** → current-space indicator + most relevant space win first glance. Correct.
- **choice complexity** → spaces gallery; entry is one decision at a time.
- **target acquisition** → space objects large targets; enter/resume primary.
- **memory burden** → persistent context indicator removes "which space am I in?" recall entirely. Load-bearing for this room.
- **mental model** → worlds you enter; the shell stays NayaNET. Matches Shawn's law.
- **feedback latency** → space entry re-context immediate; projections stream.
- **error probability** → wrong-context actions prevented by persistent indicator + authority never silently broadened.
- **recovery** → leave/archive with governed safeguards; re-entry restores.
- **progressive disclosure** → gallery → space object → space home → scoped projections.
- **trust** → privacy/scope per space; authority boundaries explicit; labels never exceed runtime enforcement. Source: #1290; Shawn's spec §19.

## R.5 Computable predicates

- **P-HICK** — ≤4 sibling choices per level → gallery browsed; space-home sections (8 projections) grouped. **PASS with grouping** (spec).
- **P-FITTS** — space objects + enter targets large. **PASS** (spec); re-verify at render.
- **P-MILLER** — space object ≤4 chunks (identity/purpose / members / goal-state / action). **PASS** (spec).
- **P-DOHERTY** — context switch <400ms. **UNMEASURABLE** — no render seat.

## R.6 Causal paths (per control)

- **ENTER SPACE** → INTENT: switch context → SCOPE: chosen space → CAPABILITY: context projection → OBSERVATION: re-contexted Hub → UI_STATE: persistent indicator + space home → EVIDENCE: space record.
- **CREATE SPACE** → INTENT: new context → SCOPE/AUTHORITY: privacy level chosen explicitly → CAPABILITY: space creation → OBSERVATION: new world → UI_STATE: gallery + home → EVIDENCE: space record with scope.
- **SET PRIVACY / SHARING** → INTENT: change scope → SCOPE/AUTHORITY: explicit, never silent → CAPABILITY: policy update → OBSERVATION: new boundary → UI_STATE: scope display → EVIDENCE: policy record. Labels never exceed enforcement.
- **INVITE / CONNECT** → INTENT: add member → SCOPE/AUTHORITY: governed → CAPABILITY: invite → OBSERVATION: pending → UI_STATE: members view → EVIDENCE: invite record.
- **ARCHIVE / LEAVE** → INTENT: exit context → SCOPE/AUTHORITY: governed safeguards → CAPABILITY: archive/leave → OBSERVATION: removed → UI_STATE: gallery → EVIDENCE: archive record.
- **ASK NAYA IN THIS SPACE** → INTENT: scoped help → SCOPE: space context → CAPABILITY: scoped synthesis → OBSERVATION: answer → UI_STATE: inline → EVIDENCE: cited space intelligence.

## R.7 Benchmark-to-beyond

- **Frontier surveyed:** team workspaces, shared folders, virtual worlds. (Proposal.)
- **Principles extracted:** durable context; membership clarity; scoped views.
- **What we preserve:** projection-not-duplication (no second databases); authority never silently broadened; shell identity stable across contexts — workspace apps duplicate data and blur scope.
- **Beyond-benchmark option:** contexts you inhabit — entering a space re-tints your world while Naya re-scopes with you, and the persistent indicator means you never act in the wrong world by accident.
- **10× claim:** ambition only. Candidate metric: wrong-context action rate (must stay near zero). No factor claimed.

## R.8 Anti-patterns watched

- **authority creep** (trust) → guard: "A space never silently broadens authority." Source: Shawn's spec §19.
- **security theater** → guard: "Do not turn labels into security guarantees without runtime enforcement." Source: #1290.
- **second database** → guard: space home is a projection of existing rooms. Source: #1290.
- **identity_erasure** → guard: shell remains NayaNET; space changes context, not product identity. Source: Shawn's spec §19.
- **client_state_as_canonical_truth** → guard: membership/scope from canonical records.
- **self_grading_as_final_proof** → guard: human acceptance per R.9.

## R.9 Acceptance

- **Cold-Naya test:** read this doc → explain the worlds promise → identify DNA (lime context + projection-not-duplication + never-silent-authority) → propose one bounded improvement with evidence.
- **Taste items for Shawn:** world-entry transition language (how "travel" feels); gallery density; space-home section order.
- **OPEN:** local-projection set per space type unspecified in sources (list is "possible," not fixed); space-health computation unspecified.

## Working notes

- 2026-10-02 — Document created (CANDIDATE). No divergences.
