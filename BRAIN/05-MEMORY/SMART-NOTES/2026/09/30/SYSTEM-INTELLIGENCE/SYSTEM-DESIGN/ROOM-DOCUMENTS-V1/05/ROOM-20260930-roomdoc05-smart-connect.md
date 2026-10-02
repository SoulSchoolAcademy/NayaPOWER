# ROOM-05 — Smart Connect · Official Room Design Document (CANDIDATE)

**Status:** CANDIDATE — drafted 2026-10-02 by Naya 4 (subagent). Not ratified, not merged.
**Route:** `/connect` · **Metaphor:** THE PORTAL BAY · **Theme:** emerald (canonical name: Smart Connect; alias: Smart Doors)
**Parent law (wins on conflict):** `HUB/NAYANET-SMART-APP-ROOM-SPEC-V1.md` §14 + §21 (Shawn, canonical, main)
**Sources:** Shawn's spec §14; `HUB/ROOMS/05-smart-connect/FUNCTIONAL-SPEC.md` + `DESIGN-CONTRACT.md` (PR #1290, open); Naya Design Intelligence v1.3; DI-INFUSION-0001 R.1–R.9 shape.

**DIVERGENCE (Shawn wins):** #1290 lists theme "teal / emerald." Shawn's spec §14 and the §21 canonical theme table both say **emerald**. This doc uses emerald.

## R.1 Room outcome

See every legitimate connection channel into NayaPOWER — what it can do, its real status, and what authority is still required. One brain. Many doors.

## R.2 Surface questions

- **WHERE AM I?** → `/connect`. Central NayaPOWER core with governed doors as precision portals around it. Source: #1290 signature visual; Shawn's spec §14 (3-second: "These are the doors into NayaPOWER; connected does not mean authorized.").
- **WHAT MATTERS?** → door liveness + authority state: which doors are live, which need authority, which are degraded/blocked. Never collapsed to on/off.
- **WHAT CAN I DO?** → per door: Connect/Authenticate, Configure, View capabilities, View required authority, Test connection, Disconnect/revoke, View receipts. Global: "Which door should I use? Ask Naya." Source: #1290 primary actions.
- **WHAT HAPPENS NEXT?** → selecting a door progressively reveals capabilities → setup → connection → permissions → activity → troubleshooting. Connect flows show auth/authority steps before any grant. Source: Shawn's spec §14.

## R.3 Applicable laws

- **H1 Purpose before interface** → job: "see available connection channels, their real status and how to connect safely." Portal bay, not integration grid.
- **H2 Distill before display** → door object shows identity + status + authority note first; capabilities/setup/activity progressively revealed. Source: Shawn's spec §14.
- **H3 Recognition before recall** → 10 named door states (LIVE…DISCONNECTED), never collapsed to on/off. Source: #1290 door states.
- **H4 One obvious next action** → primary action per Shawn: "connect/configure the selected legitimate door."
- **H5 Perceptible state + immediate feedback** → liveness, auth state, permission state, health all visible per door; "Never show a roadmap or contract-only door as live." Source: Shawn's spec §14; #1290.
- **H6 Prevent error before explaining error** → required-authority shown BEFORE connect; disconnect/revoke with appropriate confirmation; "Request / prepare a new door" is a governed workflow, not instant authority. Source: #1290.
- **H7 Complexity stays in the machine** → registry is canonical (`BRAIN/10-INTERFACES/0002-SMART-DOOR-REGISTRY-V1.json`); the room projects it, never re-implements. Source: #1290.
- **H8 Stable grammar, adaptive intelligence** → door object anatomy stable (jewel · name · who-for · purpose · status · connection · authority · action · evidence); "Which door should I use? Ask Naya" adapts.
- **H9 Direct manipulation** → N/A with reason: connecting is a governed multi-step flow; direct manipulation would obscure authority steps. Neither source specifies it.
- **H10 Design must learn** → door health/receipts feed learning; mechanics OPEN.
- **V1 Meaning before decoration** → "distinct door objects with strong identity over a uniform enterprise integration grid." Source: Shawn's spec §14.
- **V2 Hierarchy before density** → core → doors → selected-door detail; roadmap ideas visually separated from live doors. Source: #1290.
- **V3 Depth before glow** → spatial portal feel with depth; emerald = the room's identity (shared with Feed — both are "living connection" surfaces; acceptable per one-hue-one-meaning within distinct rooms).
- **V4 State before animation** → liveness is real state; no animated "connecting" theater without a real handshake.
- **V5 Contrast before novelty** → status + authority note highest contrast, not the portal chrome.
- **V6 One icon/material family** → door jewels from the single family.
- **V7 Tokens before one-off styling** → emerald via tokens.
- **V8 Interaction must feel intentional** → every door action maps to a governed operation with receipts. Source: #1290 (receipt/audit visibility per door).
- **V9 Premium must remain fast** → exact budgets OPEN.
- **V10 Preserve baseline** → the registry-driven door model is the baseline.

## R.4 Cognitive checks

- **attention** → non-live doors (DEGRADED/BLOCKED/UNAUTHORIZED) win attention first — they need action. Correct.
- **choice complexity** → doors grouped; "Which door should I use? Ask Naya" reduces choice to a question.
- **target acquisition** → per-door connect/configure as primary targets; spatial layout must keep an equivalent list for accessibility. Source: #1290 ("accessibility must provide an equivalent list").
- **memory burden** → authority state printed per door ("CONNECTED ≠ AUTHORIZED"); no recall of what was granted where.
- **mental model** → doors/portals into one brain. Matches "One brain. Many doors."
- **feedback latency** → connection test results immediate where supported; auth flows show real progress states.
- **error probability** → authority shown before grant; test-before-trust where supported. Prevents misconfigured connections.
- **recovery** → disconnect/revoke where permitted; troubleshooting per door. Source: Shawn's spec §14.
- **progressive disclosure** → select door → capabilities → setup → permissions → activity → troubleshooting. Source: Shawn's spec §14.
- **trust** → receipt/audit visibility per door; roadmap vs live never conflated. Source: #1290; Shawn's spec §14.

## R.5 Computable predicates

- **P-HICK** — ≤4 sibling choices per level → per-door actions (7) grouped: primary (Connect/Configure) vs secondary (details). Grouping required; ungrouped 7 exceeds cap. **PASS with grouping** (spec).
- **P-FITTS** — connect/configure targets large; spatial layout needs list equivalent. **PASS** (spec); re-verify at render.
- **P-MILLER** — door card ≤4 chunks (identity / status / authority-note / action). **PASS** (spec).
- **P-DOHERTY** — status changes acknowledge <400ms. **UNMEASURABLE** — no render seat; liveness depends on runtime.

## R.6 Causal paths (per control)

- **CONNECT / AUTHENTICATE** → INTENT: open channel → SCOPE/AUTHORITY: required authority shown first; grant is explicit → CAPABILITY: auth handshake → OBSERVATION: state transition (AUTHENTICATING → CONNECTED) → UI_STATE: door status → EVIDENCE: receipt.
- **VIEW REQUIRED AUTHORITY** → INTENT: understand grant → SCOPE: one door → CAPABILITY: authority read → OBSERVATION: permission list → UI_STATE: authority panel → EVIDENCE: canonical policy reference.
- **TEST CONNECTION** → INTENT: verify health → SCOPE: one door → CAPABILITY: health check → OBSERVATION: result → UI_STATE: health indicator → EVIDENCE: check receipt.
- **DISCONNECT / REVOKE** → INTENT: close channel → SCOPE/AUTHORITY: permitted revocations only, confirmed → CAPABILITY: revoke → OBSERVATION: state → DISCONNECTED → UI_STATE: door status → EVIDENCE: revocation receipt.
- **VIEW RECEIPTS / ACTIVITY** → INTENT: audit → SCOPE: one door → CAPABILITY: ledger link → OBSERVATION: door activity → UI_STATE: activity view → EVIDENCE: ledger receipts.

## R.7 Benchmark-to-beyond

- **Frontier surveyed:** integration marketplaces, OAuth consent screens, developer dashboards. (Proposal.)
- **Principles extracted:** per-scope consent; progressive capability disclosure; health transparency.
- **What we preserve:** CONNECTED ≠ AUTHORIZED as structural law; 10-state honesty (never on/off); roadmap visually separated from live — consent screens don't do this.
- **Beyond-benchmark option:** a portal bay where every door's authority boundary is visible before you knock — connection as a governed ceremony with receipts, not a toggle.
- **10× claim:** ambition only. Candidate metric: misconfigured-connection rate vs. baseline integrations. No factor claimed.

## R.8 Anti-patterns watched

- **fake_liveness** → guard: "Never show a roadmap or contract-only door as live." Source: Shawn's spec §14.
- **identity_erasure** → guard: distinct door identities; provider/channel always named. Source: Shawn's spec §14.
- **mysterious permissions** (trust) → guard: CONNECTED ≠ AUTHORIZED printed; authority note per door. Source: #1290.
- **spectacle_over_readability** → guard: spatial bay must keep accessible list equivalent. Source: #1290.
- **client_state_as_canonical_truth** → guard: door inventory from canonical registry JSON, not local state. Source: #1290.
- **self_grading_as_final_proof** → guard: connection health from real checks, not asserted.

## R.9 Acceptance

- **Cold-Naya test:** read this doc → explain the portal promise → identify DNA (emerald doors + 10-state honesty + authority-before-grant) → propose one bounded improvement with evidence.
- **Taste items for Shawn:** portal-bay spatial composition vs. list default; emerald shared with Feed — acceptable or should Connect differentiate further?
- **OPEN:** "Request / prepare a new door" governed workflow UX unspecified; door-health check cadence unspecified in sources.

## Working notes

- 2026-10-02 — Document created (CANDIDATE). One divergence recorded above (teal/emerald → emerald; Shawn wins).
