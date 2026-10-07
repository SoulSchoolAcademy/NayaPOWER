# ROOM-06 — Smart Ledger · Official Room Design Document (CANDIDATE)

**Status:** CANDIDATE — drafted 2026-10-02 by Naya 4 (subagent). Not ratified, not merged.
**Route:** `/ledger` · **Metaphor:** THE BLACK BOX / PROOF ROOM · **Theme:** yellow/gold
**Parent law (wins on conflict):** `HUB/NAYANET-SMART-APP-ROOM-SPEC-V1.md` §15 (Shawn, canonical, main)
**Sources:** Shawn's spec §15; `HUB/ROOMS/06-smart-ledger/FUNCTIONAL-SPEC.md` + `DESIGN-CONTRACT.md` (PR #1290, open); Naya Design Intelligence v1.3; DI-INFUSION-0001 R.1–R.9 shape.

No divergences between Shawn's spec and #1290; they reinforce each other (Shawn: "Stripe-like operational clarity"; #1290: seven-state truth vocabulary).

## R.1 Room outcome

Make consequential system activity inspectable without forcing the human to read logs — what happened, under whose authority, and what proves it.

## R.2 Surface questions

- **WHERE AM I?** → `/ledger`. Trust summary (real counts/status only) + chronological receipt stream. Source: Shawn's spec §15 (3-second: "This is the accountability record.").
- **WHAT MATTERS?** → needs-attention / failed-verification view; consequential events with explicit language. Source: #1290 views.
- **WHAT CAN I DO?** → Inspect receipt, View evidence, Open related intelligence, Open actor/connection, Ask Naya to explain, Export proof where supported, Retry/recover only if runtime exposes an authorized recovery action. Source: #1290 primary actions.
- **WHAT HAPPENS NEXT?** → receipt inspector progressively reveals technical proof; every consequential action across rooms links to its Ledger proof. Source: Shawn's spec §15; #1290 cross-room handoffs.

## R.3 Applicable laws

- **H1 Purpose before interface** → job: "inspect actions, receipts, authority, evidence and outcomes." Accountability record, not activity decoration.
- **H2 Distill before display** → trust summary first (real counts only), then stream; receipt inspector reveals technical proof progressively. Source: Shawn's spec §15.
- **H3 Recognition before recall** → seven-state truth vocabulary visible (requested / authorized/refused / executed / observed / verified/not verified / failed / recovered). Source: #1290.
- **H4 One obvious next action** → primary action per Shawn: "inspect the proof for a meaningful event."
- **H5 Perceptible state + immediate feedback** → execution status + verification per event; "A green executor response is not automatically verified proof." Source: #1290.
- **H6 Prevent error before explaining error** → explicit language for consequential states; "Avoid cute copy here." Retry/recover only where runtime exposes authorized recovery. Source: Shawn's spec §15; #1290.
- **H7 Complexity stays in the machine** → technical proof behind progressive inspector; human sees action/actor/outcome first. Source: Shawn's spec §15.
- **H8 Stable grammar, adaptive intelligence** → receipt anatomy stable (action · actor · time · authority · source/target · status · outcome · verification · receipt/evidence); "Ask Naya to explain" adapts. Source: Shawn's spec §15.
- **H9 Direct manipulation** → N/A with reason: inspection dominates; no manipulation metaphor in either source.
- **H10 Design must learn** → failed-verification patterns should feed learning; mechanics OPEN.
- **V1 Meaning before decoration** → gold marks verified truth; the room's beauty is its clarity ("Stripe-like operational clarity"). Source: Shawn's spec §15.
- **V2 Hierarchy before density** → trust summary → stream → inspector; high scanability. Source: Shawn's spec §15.
- **V3 Depth before glow** → gold as meaning (precious truth), restrained.
- **V4 State before animation** → status truth first; no animated transitions that imply progress not made.
- **V5 Contrast before novelty** → failed/unverified states highest contrast — accountability must shout.
- **V6 One icon/material family** → status jewels from the single family.
- **V7 Tokens before one-off styling** → gold via tokens.
- **V8 Interaction must feel intentional** → every event links action→authority→evidence; nothing decorative.
- **V9 Premium must remain fast** → chronological stream bounded; exact budgets OPEN.
- **V10 Preserve baseline** → the receipt-anatomy order is the baseline.

## R.4 Cognitive checks

- **attention** → failed-verification / needs-attention wins first glance. Correct: accountability's job.
- **choice complexity** → 6 views (Timeline/Receipts/By action/By actor/By Space/Needs attention); filters concise.
- **target acquisition** → receipt rows full-width targets; inspector progressive.
- **memory burden** → authority decision + verification printed per event; related events visually connect into causal threads — no recall of what authorized what. Source: #1290.
- **mental model** → a flight recorder / proof room. Matches.
- **feedback latency** → event arrival in stream immediate; inspector progressive.
- **error probability** → misreading proof prevented by explicit consequential language + seven-state vocabulary.
- **recovery** → retry/recover only where runtime exposes it — honest boundary, never faked. Source: #1290.
- **progressive disclosure** → summary → stream row → receipt inspector → technical proof. Source: Shawn's spec §15.
- **trust** → this room IS the trust instrument: verification states explicit; "verified" never shown for merely-executed. Source: #1290 ("A green executor response is not automatically verified proof").

## R.5 Computable predicates

- **P-HICK** — ≤4 sibling choices per level → 6 views; per-event actions grouped (inspect/evidence/related). **PASS with grouping** (spec).
- **P-FITTS** — receipt rows as large targets; inspector controls reachable. **PASS** (spec); re-verify at render.
- **P-MILLER** — row ≤4 chunks (action / actor / outcome+verification / time). **PASS** (spec).
- **P-DOHERTY** — stream updates <400ms. **UNMEASURABLE** — no render seat; depends on runtime event flow.

## R.6 Causal paths (per control)

- **INSPECT RECEIPT** → INTENT: verify an event → SCOPE: one receipt → CAPABILITY: proof projection → OBSERVATION: receipt detail → UI_STATE: inspector → EVIDENCE: receipt/evidence links.
- **VIEW EVIDENCE** → INTENT: see underlying proof → SCOPE: one claim → CAPABILITY: evidence drill-down → OBSERVATION: technical proof → UI_STATE: proof layer → EVIDENCE: canonical records.
- **OPEN ACTOR / CONNECTION** → INTENT: who acted → SCOPE: one actor → CAPABILITY: identity link → OBSERVATION: actor context → UI_STATE: actor view → EVIDENCE: identity record.
- **ASK NAYA TO EXPLAIN** → INTENT: understand an event → SCOPE: one receipt → CAPABILITY: explanation → OBSERVATION: plain-language account → UI_STATE: inline explanation → EVIDENCE: cited receipt fields.
- **EXPORT PROOF** → INTENT: carry proof elsewhere → SCOPE/AUTHORITY: where supported → CAPABILITY: export → OBSERVATION: artifact → UI_STATE: export confirmation → EVIDENCE: exported receipt.
- **RETRY / RECOVER** → INTENT: fix a failure → SCOPE/AUTHORITY: only if runtime exposes authorized recovery → CAPABILITY: recovery op → OBSERVATION: new attempt → UI_STATE: updated status → EVIDENCE: new receipt (never overwrites the failure).

## R.7 Benchmark-to-beyond

- **Frontier surveyed:** Stripe dashboard (operational clarity — cited by Shawn), audit-log UIs, blockchain explorers. (Proposal; Stripe cited in Shawn's spec §15.)
- **Principles extracted:** scanable rows; explicit status language; drill-down proof.
- **What we preserve:** seven-state truth vocabulary (executed ≠ verified); causal threads between related events; authority named per event — explorers don't name authority.
- **Beyond-benchmark option:** Stripe-like clarity fused with Naya's truth model — every row carries its verification state, and "Ask Naya to explain" turns any receipt into plain language without losing the proof.
- **10× claim:** ambition only. Candidate metric: time-to-verify-a-consequential-event. No factor claimed.

## R.8 Anti-patterns watched

- **fake_data** → guard: empty state "No receipted activity in this scope"; runtime-unavailable stated explicitly. Source: #1290.
- **misleading verification** → guard: executed ≠ verified, always; seven states. Source: #1290.
- **cute copy on consequential states** → guard: "Avoid cute copy here. Consequential states need explicit language." Source: Shawn's spec §15.
- **spectacle_over_readability** → guard: "high scanability"; optional graph secondary, never required. Source: Shawn's spec §15; #1290.
- **client_state_as_canonical_truth** → guard: receipts from runtime; inspector reveals technical proof, not local claims.
- **self_grading_as_final_proof** → guard: verification is a runtime state, not a builder assertion.

## R.9 Acceptance

- **Cold-Naya test:** read this doc → explain the accountability promise → identify DNA (gold truth + seven-state vocabulary + explicit language) → propose one bounded improvement with evidence.
- **Taste items for Shawn:** trust-summary composition (which real counts); causal-thread visual language; "failed verification" alerting tone.
- **OPEN:** export-proof formats unspecified; retry/recover availability is runtime-defined (correctly out of room scope).

## Working notes

- 2026-10-02 — Document created (CANDIDATE). No divergences.
