# Room Design-Intelligence Infusion — Template + Worked Example (CANDIDATE)

Doc: DI-INFUSION-0001
Truth state: CANDIDATE (Naya 4, 2026-10-02 — staged on draft lane, not merged, not ratified)
Parent law: `NAYA-ACTIVATION/DESIGN/NAYA-DESIGN-INTELLIGENCE-STANDARD-V1.md` + machine contract v1.3 (canonical, main)
Enforcement: DS-0001 (candidate)
Target: fold into each room's `DESIGN-CONTRACT.md` in PR #1290 (open) — this doc does NOT replace those contracts.

## Purpose

Every room DESIGN-CONTRACT already carries creative intent, composition, and visual
law. The infusion adds the **human-intelligence layer**: why each choice serves the
human, how the machine checks it, and what the frontier taught us. A room is done
when a cold Naya can read its contract and build the room without asking Shawn
what matters.

## The infusion section-shape (for every room)

For room R, append these sections to its DESIGN-CONTRACT:

### R.1 Room outcome
One sentence: the human outcome this room exists for. (Not what it shows — what the
human can DO or UNDERSTAND after using it.)

### R.2 Surface questions (answered, not aspirational)
- WHERE AM I? → route, room identity, mode — legible in under a second.
- WHAT MATTERS? → what wins first glance, and why it deserves to.
- WHAT CAN I DO? → the obvious next actions, visible without recall.
- WHAT HAPPENS NEXT? → the consequence of each primary action, predictable before acting.

### R.3 Applicable laws (from the 20)
Name the visual laws (10) and human-experience laws (10) that bear on THIS room and
state concretely how each is satisfied. Laws that don't apply are named as N/A with
one line of reason — never silently skipped.

### R.4 Cognitive checks (the 10)
attention · choice complexity · target acquisition · memory burden · mental model ·
feedback latency · error probability · recovery · progressive disclosure · trust.
Each answered for the room in one to two lines.

### R.5 Computable predicates
P-FITTS / P-HICK / P-MILLER / P-DOHERTY with room-specific values and measurement
points. Format: PREDICATE — requirement — where measured — current verdict
(PASS / FAIL + location / UNMEASURABLE + reason).

### R.6 Causal paths (per control)
For every control: CONTROL → INTENT → SCOPE/AUTHORITY → CAPABILITY → OBSERVATION →
UI_STATE → EVIDENCE_WHERE_REQUIRED.

### R.7 Benchmark-to-beyond (for this room)
Frontier surveyed → principles extracted → what we already do better (preserve) →
the beyond-benchmark option generated → how it was tested or will be.
"10× better" is the ambition; a factor is claimed only with a real metric.

### R.8 Anti-patterns watched
From the 14: which threaten THIS room, and the concrete guard in place.

### R.9 Acceptance
The cold-Naya test (understand → explain → identify DNA → find highest-value gap →
build bounded improvement → prove → learn) plus the human taste items queued for
Shawn — never decided by the machine.

---

## Worked example: Room 01 — Smart Feed (`/feed`)

**Status:** CANDIDATE infusion over `HUB/ROOMS/01-smart-feed/DESIGN-CONTRACT.md` V1 (PR #1290, open).

### R.1 Room outcome
Open the Feed and immediately understand the living flow of your intelligence —
what appeared, changed, connected, mattered, or requires your attention.

### R.2 Surface questions
- WHERE AM I? → `/feed`, Smart Feed. Slim orientation header + current mode
  (PERSONAL / COLLECTIVE / ACTIVITY) always visible.
- WHAT MATTERS? → current mode and new-since-last-visit. Intelligence objects
  dominate; the "new intelligence" seam marks fresh verified arrivals.
- WHAT CAN I DO? → switch mode (3 large controls), Open, Ask Naya, Save/Favorite —
  concise actions per object, visible without menus.
- WHAT HAPPENS NEXT? → mode switch re-materializes the stream; Open reveals the
  object; Ask Naya explains; Save files it to the library. All predictable.

### R.3 Applicable laws
- DISTILL BEFORE DISPLAY → each object shows essence/title + "why it is here",
  never raw data dumps. Provenance secondary until needed.
- RECOGNITION BEFORE RECALL → three visible mode controls; no hidden gestures
  or remembered commands for primary navigation.
- ONE OBVIOUS NEXT ACTION → per-object concise actions; Naya suggests next useful
  actions ("why am I seeing this?" answered in place).
- PERCEPTIBLE STATE + IMMEDIATE FEEDBACK → 11 named states (LOADING…DISABLED);
  each preserves room identity — no generic error card.
- COMPLEXITY STAYS IN THE MACHINE → filters progressive, not spread across canvas.
- STABLE GRAMMAR, ADAPTIVE INTELLIGENCE → one continuous vertical river, always;
  content/priority adapt per mode.
- DEPTH BEFORE GLOW → emerald semantic energy on live objects; edge/elevation for
  importance, not decorative gradients.
- STATE BEFORE ANIMATION → restrained state-linked motion only; no fake pulsing stream.
- N/A with reason: DIRECT MANIPULATION — the stream is primarily read/triage;
  manipulation lives in object actions (bottom sheet), which is the correct scope.

### R.4 Cognitive checks
- attention → current mode + new seam win first glance. Correct: they answer
  "what changed since I was here."
- choice complexity → 3 modes, not 30 filters. Filters deferred progressively.
- target acquisition → three LARGE mode controls, sticky/reachable; object actions
  in an accessible bottom sheet (thumb-reachable).
- memory burden → "why it is here" printed per object; scroll restoration + return
  position remove spatial recall.
- mental model → a river of intelligence, not an algorithmic feed. No engagement
  ranking to reverse-engineer.
- feedback latency → new verified objects enter with immediate restrained motion;
  mode switch re-materializes without spinners where possible.
- error probability → no destructive primary actions in the stream; consequential
  actions live behind Open/bottom sheet.
- recovery → scroll restoration; back returns to exact position.
- progressive disclosure → filters, tags, relationships appear only when useful.
- trust → truth state + provenance on every object, always available, never
  disappearing on any viewport.

### R.5 Computable predicates
- P-HICK — ≤4 sibling choices per level → 3 mode controls; per-object actions
  concise (Open / Ask Naya / Save). PASS (spec count).
- P-FITTS — primary targets large + reachable → three large mode controls
  sticky; bottom-sheet actions thumb-reachable. PASS (spec); re-verify at render
  (13th lock: render seat pending).
- P-MILLER — ≤4 chunks to triage → essence + why-here + truth state visible per
  object; no recall required. PASS (spec).
- P-DOHERTY — acknowledge <400ms → new-arrival seam immediate; UNMEASURABLE
  until render seat exists (honest boundary, never PASS by default).

### R.6 Causal paths (per control)
- MODE SWITCH (Personal/Collective/Activity) → INTENT: change intelligence scope →
  SCOPE: user's consented visibility → CAPABILITY: stream re-query →
  OBSERVATION: stream re-materializes → UI_STATE: mode header + seam update →
  EVIDENCE: mode label + provenance preserved per object.
- ASK NAYA → INTENT: explain/summarize → SCOPE: visible objects + uncertainty →
  CAPABILITY: Naya explanation → OBSERVATION: answer with exposed uncertainty →
  UI_STATE: inline explanation → EVIDENCE: sources cited.
- SAVE/FAVORITE → INTENT: preserve → SCOPE: single object → CAPABILITY: library
  write → OBSERVATION: saved confirmation → UI_STATE: saved marker →
  EVIDENCE: library location shown.

### R.7 Benchmark-to-beyond (Smart Feed)
- Frontier surveyed: social feeds (pattern fluency), Oura (distillation),
  Linear (focus/calm).
- Principles extracted: continuous vertical rhythm; ruthless distillation;
  calm over dense.
- What we already do better (preserve): governed truth states + provenance on
  every object; living-depth materiality; "why am I seeing this" answered by Naya.
  No benchmark combines all three.
- Beyond-benchmark option: an intelligence river with truth-state physics —
  objects rise by verified relevance, Naya narrates the seam between visits,
  provenance is structural not decorative. No social-feed clone on the market
  does this.
- 10× claim: ambition only. Metric when built: time-to-"what matters" vs.
  baseline feed triage, plus comprehension spot-checks.

### R.8 Anti-patterns watched
engagement bait · vanity metrics · mysterious ranking · fake live motion ·
dense filter dashboard — all five already named in the contract's "Must never
become." Guard: any metric proposal for this room must cite a human outcome,
not an engagement number.

### R.9 Acceptance
Cold-Naya test: read this contract → explain the Feed's promise → identify its
DNA (emerald living-depth + truth physics) → propose one bounded improvement
with evidence → leave the room better. Taste items for Shawn: final Activity
mode composition (noted open in functional spec); exact motion restraint values.

---

## How lanes use this

1. Copy the R.1–R.9 shape into the room's DESIGN-CONTRACT (PR #1290 branch, by its owners).
2. Fill it from the room's functional spec + the v1.3 machine contract. Do not invent
   room behavior to fill sections — mark UNMEASURABLE/OPEN honestly.
3. Naya 2 verifies each infused contract independently (her lane).
4. Shawn gives taste per room up front, where cheap — the final 5%.
5. Lessons that survive evidence promote via LEARN; the infusion shape itself
   improves by the same path.
