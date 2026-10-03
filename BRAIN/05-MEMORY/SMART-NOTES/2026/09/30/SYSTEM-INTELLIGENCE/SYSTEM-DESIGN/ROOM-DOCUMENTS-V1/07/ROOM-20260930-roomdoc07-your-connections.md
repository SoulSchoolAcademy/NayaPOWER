# ROOM-07 — Your Connections · Official Room Design Document (CANDIDATE)

**Status:** CANDIDATE — drafted 2026-10-02 by Naya 4 (subagent). Not ratified, not merged.
**Route:** `/connections` · **Metaphor:** THE CONSTELLATION · **Theme:** orange
**Parent law (wins on conflict):** `HUB/NAYANET-SMART-APP-ROOM-SPEC-V1.md` §16 (Shawn, canonical, main)
**Sources:** Shawn's spec §16; `HUB/ROOMS/07-your-connections/FUNCTIONAL-SPEC.md` + `DESIGN-CONTRACT.md` (PR #1290, open); Naya Design Intelligence v1.3; DI-INFUSION-0001 R.1–R.9 shape.

**DIVERGENCE (Shawn wins):** #1290 leads with the constellation visualization as the primary experience. Shawn's spec §16: "Default list/group view for clarity. Optional relationship map when graph form adds understanding." This doc follows Shawn — list/group default, constellation optional.

## R.1 Room outcome

Understand people, Nayas, systems and governed relationships connected to the human — who and what I'm connected to, and on what terms.

## R.2 Surface questions

- **WHERE AM I?** → `/connections`. Default list/group view: People, Nayas/agents, Organizations, Shared Spaces, Requests/pending. Source: #1290 primary views; Shawn's spec §16.
- **WHAT MATTERS?** → requests/pending first; then relationship scope and consent state. Connection lines encode relationship type/state — never hidden permissions. Source: #1290.
- **WHAT CAN I DO?** → Open connection, Message, Open shared Space, View shared intelligence, Adjust sharing/consent (when authorized), Disconnect/revoke (with confirmation), Invite/connect, Ask Naya about this relationship. Source: #1290 primary actions.
- **WHAT HAPPENS NEXT?** → opening a connection shows identity, type, shared scope, consent/privacy state, history, permissions boundary. Disconnect/revoke confirms proportionally to impact. Source: #1290 relationship detail.

## R.3 Applicable laws

- **H1 Purpose before interface** → job: "understand people, Nayas, systems and governed relationships." Terms first, visualization second.
- **H2 Distill before display** → grouped views distill the relationship set; detail per connection on demand.
- **H3 Recognition before recall** → named views (People / Nayas / Organizations / Shared Spaces / Requests); no remembered navigation.
- **H4 One obvious next action** → primary action per Shawn: "inspect/manage a selected connection."
- **H5 Perceptible state + immediate feedback** → consent/privacy state + relationship status visible per connection; "No relationship graph should imply access the human does not have." Source: Shawn's spec §16.
- **H6 Prevent error before explaining error** → disconnect/revoke with appropriate confirmation; adjust-sharing only when authorized; never imply access not held. Source: #1290; Shawn's spec §16.
- **H7 Complexity stays in the machine** → permission graphs computed underneath; human sees terms in plain language.
- **H8 Stable grammar, adaptive intelligence** → connection object anatomy stable (identity · type · shared scope · status · consent/boundary · last interaction · actions); "Ask Naya about this relationship" adapts. Source: Shawn's spec §16.
- **H9 Direct manipulation** → N/A with reason: relationship management is inspect/confirm flows; constellation is optional visualization, not manipulation surface.
- **H10 Design must learn** → "recent relevant interaction" informs ordering; mechanics OPEN.
- **V1 Meaning before decoration** → orange = human warmth/relationships; constellation lines encode type/state (meaning), never decoration. Source: #1290.
- **V2 Hierarchy before density** → requests/pending → groups → detail; list default keeps density honest.
- **V3 Depth before glow** → constellation depth spatial; glow never on letterforms.
- **V4 State before animation** → connection states real; no animated "closeness."
- **V5 Contrast before novelty** → consent/boundary state highest contrast — the terms must be unmissable.
- **V6 One icon/material family** → connection-type jewels from the single family.
- **V7 Tokens before one-off styling** → orange via tokens.
- **V8 Interaction must feel intentional** → every action (message/share/revoke) maps to a governed operation. "Do not invent suggested people unless a legitimate discovery system exists and its basis is shown." Source: #1290 empty state.
- **V9 Premium must remain fast** → list default is fast; constellation optional. Exact budgets OPEN.
- **V10 Preserve baseline** → the governed-relationship model (terms visible) is the baseline.

## R.4 Cognitive checks

- **attention** → requests/pending win first glance. Correct: they need decisions.
- **choice complexity** → 6 views grouped; per-connection actions (8) grouped: inspect / communicate / manage.
- **target acquisition** → list rows full-width; mobile list-first. Source: #1290 mobile.
- **memory burden** → terms printed per connection (shared scope, consent state, connected-since); no recall of what was shared with whom.
- **mental model** → an address book with terms, plus an optional star map. List-default matches the mental model; constellation is delight, not navigation.
- **feedback latency** → view switches immediate; detail full-screen on mobile.
- **error probability** → wrong-person sharing prevented by visible scope + confirmation on revoke; no implied access. Source: Shawn's spec §16.
- **recovery** → sharing adjustments reversible where authorized; revoke confirmed.
- **progressive disclosure** → group → connection → detail (identity → terms → history → permissions).
- **trust** → consent/privacy state + authority boundary per connection; "never hidden permissions." Source: #1290.

## R.5 Computable predicates

- **P-HICK** — ≤4 sibling choices per level → 6 views; per-connection actions grouped into 3 clusters. **PASS with grouping** (spec).
- **P-FITTS** — list rows large targets; constellation nodes need ≥44px touch equivalents. **PASS** (spec); re-verify at render.
- **P-MILLER** — connection row ≤4 chunks (identity / type / scope-status / last interaction). **PASS** (spec).
- **P-DOHERTY** — view switches <400ms. **UNMEASURABLE** — no render seat.

## R.6 Causal paths (per control)

- **OPEN CONNECTION** → INTENT: inspect relationship → SCOPE: one connection → CAPABILITY: relationship projection → OBSERVATION: detail → UI_STATE: detail view → EVIDENCE: identity + terms record.
- **ADJUST SHARING / CONSENT** → INTENT: change terms → SCOPE/AUTHORITY: only when authorized → CAPABILITY: consent update → OBSERVATION: new terms → UI_STATE: updated boundary display → EVIDENCE: consent record.
- **DISCONNECT / REVOKE** → INTENT: end relationship → SCOPE/AUTHORITY: confirmed proportionally to impact → CAPABILITY: revoke → OBSERVATION: removed → UI_STATE: group update → EVIDENCE: revocation record.
- **MESSAGE** → INTENT: communicate → SCOPE: one connection → CAPABILITY: mail handoff → OBSERVATION: compose → UI_STATE: mail context → EVIDENCE: message record.
- **INVITE / CONNECT** → INTENT: new relationship → SCOPE/AUTHORITY: governed invite → CAPABILITY: invite flow → OBSERVATION: pending state → UI_STATE: requests view → EVIDENCE: invite record.

## R.7 Benchmark-to-beyond

- **Frontier surveyed:** contact apps, social graphs, CRM relationship views. (Proposal.)
- **Principles extracted:** grouped clarity; relationship timelines; terms visibility.
- **What we preserve:** terms-on-every-connection (consent/authority boundary as UI, not legal fine print); "never imply access not held"; no invented suggestions — no benchmark refuses to invent people.
- **Beyond-benchmark option:** a constellation you can read two ways — list for clarity, star-map for feel — where every line between stars states its terms honestly.
- **10× claim:** ambition only. Candidate metric: time-to-answer "what can this connection see?" No factor claimed.

## R.8 Anti-patterns watched

- **fake_data** → guard: "Do not invent suggested people unless a legitimate discovery system exists and its basis is shown." Source: #1290.
- **identity_erasure** → guard: identity + relationship type + history per connection; applicable door/channel shown. Source: #1290.
- **mysterious permissions** → guard: "never hidden permissions"; graph never implies unheld access. Source: #1290; Shawn's spec §16.
- **spectacle_over_readability** → guard: list default; constellation optional-only. (Divergence enforced.)
- **client_state_as_canonical_truth** → guard: relationship/consent state from canonical records.
- **self_grading_as_final_proof** → guard: human acceptance per R.9.

## R.9 Acceptance

- **Cold-Naya test:** read this doc → explain the relationship promise → identify DNA (orange warmth + terms-visible + list-first) → propose one bounded improvement with evidence.
- **Taste items for Shawn:** constellation visual language (when it earns its place); request/pending triage design; group taxonomy.
- **OPEN:** "legitimate discovery system" for suggestions does not exist in sources — correctly absent until it does; ordering signals for groups unspecified.

## Working notes

- 2026-10-02 — Document created (CANDIDATE). One divergence recorded above (constellation-first → list-default; Shawn wins).
