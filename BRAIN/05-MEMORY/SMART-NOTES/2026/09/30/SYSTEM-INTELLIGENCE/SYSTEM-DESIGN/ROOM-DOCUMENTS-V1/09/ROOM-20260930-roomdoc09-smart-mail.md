# ROOM-09 — Smart Mail · Official Room Design Document (CANDIDATE)

**Status:** CANDIDATE — drafted 2026-10-02 by Naya 4 (subagent). Not ratified, not merged.
**Route:** `/mail` · **Metaphor:** THE SIGNAL ROOM · **Theme:** sapphire
**Parent law (wins on conflict):** `HUB/NAYANET-SMART-APP-ROOM-SPEC-V1.md` §18 + §21 (Shawn, canonical, main)
**Sources:** Shawn's spec §18; `HUB/ROOMS/09-smart-mail/FUNCTIONAL-SPEC.md` + `DESIGN-CONTRACT.md` (PR #1290, open); Naya Design Intelligence v1.3; DI-INFUSION-0001 R.1–R.9 shape.

**DIVERGENCE (Shawn wins):** #1290 lists theme "sapphire / cyan." Shawn's spec §18 and the §21 canonical theme table both say **sapphire**. This doc uses sapphire.

## R.1 Room outcome

Understand, prioritize and respond to real governed communication — what needs my attention, what it means, and what action each message needs.

## R.2 Surface questions

- **WHERE AM I?** → `/mail`. Priority inbox (reason for priority inspectable) + conversation list + detail + Naya assist. Source: Shawn's spec §18 (3-second: "These are the messages/conversations that matter, with Naya helping me understand and act.").
- **WHAT MATTERS?** → priority inbox grouped by meaning: Needs response / Important / Waiting on someone / FYI / Related to active Space. Source: #1290 default view.
- **WHAT CAN I DO?** → Open, Reply, Compose, Archive, Mark/prioritize, Ask Naya, Add to List, Attach/link to Space, Open sender in Connections. Source: #1290 primary actions.
- **WHAT HAPPENS NEXT?** → Naya assist summarizes/drafts/identifies commitments; sending requires explicit appropriate authority + clear recipient/content confirmation where consequential. Source: Shawn's spec §18; #1290.

## R.3 Applicable laws

- **H1 Purpose before interface** → job: "understand, prioritize and respond to real governed communication." Signal console, not email clone. Source: #1290.
- **H2 Distill before display** → grouped by meaning, not chronology; each preview shows essence + why-it-matters. Source: #1290.
- **H3 Recognition before recall** → meaning groups visible; chronological inbox available but not default.
- **H4 One obvious next action** → primary action per Shawn: "open/respond to the highest-value real conversation."
- **H5 Perceptible state + immediate feedback** → response/action state per message; truthful connection state — "if no provider is connected, show the setup/unavailable state beautifully." Source: Shawn's spec §18.
- **H6 Prevent error before explaining error** → "Sending requires explicit appropriate authority and clear recipient/content confirmation where consequential." "Naya must not send consequential messages without applicable user authorization." Source: Shawn's spec §18; #1290. This room's H6 is load-bearing.
- **H7 Complexity stays in the machine** → triage/summarization underneath; human sees signals with reasons.
- **H8 Stable grammar, adaptive intelligence** → inbox/detail/compose grammar stable; priority grouping adapts; Naya assist contextual.
- **H9 Direct manipulation** → N/A with reason: triage/respond flows dominate; neither source specifies manipulation.
- **H10 Design must learn** → priority reasons should improve from outcomes; mechanics OPEN.
- **V1 Meaning before decoration** → sapphire = trusted communication; priority reason inspectable per item. Source: Shawn's spec §18.
- **V2 Hierarchy before density** → priority inbox → conversation → detail → Naya assist.
- **V3 Depth before glow** → signal-room depth; restrained.
- **V4 State before animation** → message/connection states lead; no animated "intelligence" theater.
- **V5 Contrast before novelty** → needs-response group highest contrast.
- **V6 One icon/material family** → message-state jewels from the single family.
- **V7 Tokens before one-off styling** → sapphire via tokens.
- **V8 Interaction must feel intentional** → every triage decision explainable ("reason for priority inspectable"). Source: Shawn's spec §18.
- **V9 Premium must remain fast** → exact budgets OPEN.
- **V10 Preserve baseline** → the governed-communication model (authority-gated sending) is the baseline.

## R.4 Cognitive checks

- **attention** → Needs-response group wins first glance. Correct.
- **choice complexity** → 6 meaning groups; per-message actions grouped.
- **target acquisition** → priority items large targets; compose/reply reachable.
- **memory burden** → "why it matters" + Space/context per preview; Naya identifies unanswered questions and commitments — no recall of thread state. Source: #1290.
- **mental model** → a signal room: signals, not an inbox pile. Matches.
- **feedback latency** → message open immediate; Naya summaries stream with state.
- **error probability** → wrong-recipient/wrong-send prevented by authority gate + confirmation. Load-bearing per H6.
- **recovery** → drafts preserved; archive reversible (expected — not specified in sources; OPEN as explicit requirement).
- **progressive disclosure** → preview → conversation → Naya assist → proof/activity where applicable. Source: #1290; Shawn's spec §18.
- **trust** → truthful connection state; "Never fabricate mail to fill the screen." Source: Shawn's spec §18.

## R.5 Computable predicates

- **P-HICK** — ≤4 sibling choices per level → 6 meaning groups; per-message actions grouped. **PASS with grouping** (spec).
- **P-FITTS** — priority items + reply/compose large targets. **PASS** (spec); re-verify at render.
- **P-MILLER** — preview ≤4 chunks (sender / essence / why-matters / action-state). **PASS** (spec).
- **P-DOHERTY** — open/reply <400ms. **UNMEASURABLE** — no render seat; provider latency runtime-dependent.

## R.6 Causal paths (per control)

- **REPLY** → INTENT: respond → SCOPE/AUTHORITY: explicit authority; consequential sends confirmed with recipient/content → CAPABILITY: send → OBSERVATION: sent state → UI_STATE: conversation update → EVIDENCE: sent record.
- **NAYA ASSIST (summarize/draft)** → INTENT: understand or prepare → SCOPE: one thread → CAPABILITY: summarization/drafting → OBSERVATION: summary/draft shown, never sent → UI_STATE: assist panel → EVIDENCE: cited thread content. Draft ≠ send, structurally.
- **MARK / PRIORITIZE** → INTENT: triage → SCOPE: one message → CAPABILITY: state update → OBSERVATION: new grouping → UI_STATE: group update → EVIDENCE: triage record + reason.
- **ADD TO LIST / ATTACH TO SPACE** → INTENT: organize → SCOPE: one message → CAPABILITY: reference → OBSERVATION: confirmation → UI_STATE: marker → EVIDENCE: canonical reference.
- **OPEN SENDER IN CONNECTIONS** → INTENT: see relationship → SCOPE: one sender → CAPABILITY: connection link → OBSERVATION: connection detail → UI_STATE: connections room → EVIDENCE: relationship record.

## R.7 Benchmark-to-beyond

- **Frontier surveyed:** Superhuman (triage speed), Hey (meaning grouping), Gmail (scale). (Proposal.)
- **Principles extracted:** meaning-first grouping; inspectable priority; assist-doesn't-send.
- **What we preserve:** authority-gated sending as structural law; never-fabricate-mail; priority reasons inspectable — triage apps don't show their reasons.
- **Beyond-benchmark option:** an inbox where every message arrives already understood — why it matters, what it needs, its commitments flagged — and Naya drafts but never sends without you.
- **10× claim:** ambition only. Candidate metric: time-to-inbox-zero-equivalent + mis-send rate (must stay zero). No factor claimed.

## R.8 Anti-patterns watched

- **fake_data** → guard: "Never fabricate mail to fill the screen." Truthful unavailable state. Source: Shawn's spec §18.
- **unverified sending** (trust) → guard: authority + confirmation gates; Naya never sends consequential mail unauthorised. Source: Shawn's spec §18; #1290.
- **mysterious ranking** → guard: "reason for priority inspectable." Source: Shawn's spec §18.
- **engagement bait** → guard: meaning groups, not engagement ordering.
- **client_state_as_canonical_truth** → guard: message state from provider/runtime, honestly labeled when unavailable.
- **self_grading_as_final_proof** → guard: human acceptance per R.9.

## R.9 Acceptance

- **Cold-Naya test:** read this doc → explain the signal promise → identify DNA (sapphire trust + meaning-groups + authority-gated sending) → propose one bounded improvement with evidence.
- **Taste items for Shawn:** priority-group taxonomy; Naya-assist visual weight in conversation detail; unavailable-state beauty bar.
- **OPEN:** archive/undo mechanics unspecified in sources — required before build; draft-autosave behavior unspecified.

## Working notes

- 2026-10-02 — Document created (CANDIDATE). One divergence recorded above (sapphire/cyan → sapphire; Shawn wins).
