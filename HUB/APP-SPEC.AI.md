# NayaNET Hub — Complete Application Spec (AI Builder Projection)

**Canonical:** `HUB/APP-SPEC.AI.md` · **Companion:** `HUB/APP-SPEC.HUMAN.md`
**Status:** SPECIFICATION — not implementation. Nothing here is claimed built.
**Authority:** Human Director Shawn Vibert. This spec sits under `HUB/PROJECT-INTELLIGENCE.md`
(including the input/output law, Law 1), `HUB/DESIGN-CONTRACT.md`, and the room contracts in
`HUB/ROOMS/` (PR #1290). On conflict, PROJECT-INTELLIGENCE.md wins, then this spec, then room contracts.
**Foundation:** the #1278 modular app architecture (`HUB/app/`), reconciled to this spec.
**Purpose:** the complete map. No builder starts without reading this. Spec first, then pieces, then evolution.

---

## 0. THE PRODUCT IN ONE PAGE

The Hub is the **retina of NayaPOWER**: the visual projection/experience layer of canonical
intelligence. It is output-only. Intelligence is produced outside the Hub — by Naya, by human work,
by any AI the human talks to — captured as canonical Intelligent Blocks, persisted in the
Brain/GitHub substrate, emitted as governed events, and projected into the Hub.

```
HUMAN → (any AI / work) → INTELLIGENCE GENERATED → canonical IB → GitHub/Brain persistence
  → governed event → index/runtime/provenance → HUB RECEIVES → projects into rooms
```

**Three pipelines feed the Hub, and only these three:**
1. **Smart notes** → intelligent events (captured intelligence)
2. **Activity** → the now-stream (state / change / process)
3. **Reports** → periodic intelligence (structured synthesis)

**One intelligence object → many valid projections.** A smart note is never copied into Feed,
Library, Lists, Spaces. Those surfaces project the same canonical object by ID. This gives
consistency, provenance, supersession, and traceability.

**Eleven rooms are eleven lenses on the same intelligence**, not eleven apps:
Feed (what's happening) · Today (what's important today) · Reports (what happened over time) ·
Library (what do we know) · Connect (what can intelligence connect to) · Ledger (what actually
happened) · Connections (who/what is related) · Lists (what do I need to act on) · Mail (what
signals need attention) · Spaces (what belongs to this context) · Settings (how is my
intelligence governed).

---

## 1. GOVERNING LAWS (WITH CONFLICT RESOLUTIONS)

1. **Input/output law** (PROJECT-INTELLIGENCE.md §6 Law 1, PR #1300). The Hub is the screen, not
   the camera. No capture control and no input surface of any kind exists in Hub chrome. This is
   architecture, not taste.
2. **Projection law.** One intelligence object → many valid projections. No room maintains a
   private copy of canonical intelligence. Duplication is a defect.
3. **Consent law.** Connecting a hub shares the human's *intelligence* with the collective, never
   their identity. Personal stream is identified to its owner; the collective stream is anonymized.
4. **Honesty law.** NOT_VERIFIED over fake content, always. No sample data, no simulated liveness,
   no animated aliveness without a live backend. Unbacked cards are labeled design fixtures.
5. **Cockpit law.** The Hub presents; NayaPOWER knows. The Hub is never a second brain, second
   database, or shadow memory.
6. **Rail law.** Single left rail, eleven rooms. Exactly one primary navigation surface at any
   viewport size.
7. **Search law.** Search is prominent, near the top of the center, and IS the Ask Naya surface.
   Never buried in an icon.
8. **Liveness law.** Animation communicates actual state; never manufactures it.
9. **No-shells law.** A room is not complete because a route/title/card renders. Completion =
   ORIENTATION → CURRENT STATE → INTELLIGENCE → ACTION → PROOF + all applicable states + mobile
   + accessibility + runtime + persistence + cross-room handoff + browser proof + failure proof
   + independent review.

### Conflict resolutions (binding)

- **CR-1 — CAPTURE_SMART_NOTE.** The Feed and Today room contracts (PR #1290) list
  `CAPTURE_SMART_NOTE` / `CAPTURE_FOLLOWUP` as primary causal actions. These are **SUPERSEDED**
  by the input/output law. No capture control shall be built in Hub chrome. The room contracts
  require amendment; until amended, this spec's resolution governs.
- **CR-2 — ASK_NAYA.** Room contracts list `ASK_NAYA` as a causal action. It is hereby defined:
  **retrieval-only Q&A over the NayaPOWER knowledge base** ("ask anything about NayaPOWER"),
  plus voice read-back of intelligent blocks. It is never a chatbot, never agency, never command
  execution, never a capture path. The Hub stays 100% invocation-free.
- **CR-3 — Feed modes vs smart views.** Room contracts specify three feed modes
  (Collective/Personal/Activity). The feed system (§4) keeps these as the three canonical
  **streams** and adds **smart views** (ALL, SMART NOTES, ACTIVITY, REPORTS, HIGHLIGHTS,
  LEARNING, DECISIONS, DISCOVERIES, PROJECTS, COLLECTIVE, + custom later) as projections over
  them. Streams are sources; views are lenses. Neither duplicates content.

---

## 2. THE SHELL (COMPLETE)

One persistent shell hosts all rooms. The shell has exactly these surfaces, each with one reason:

| Surface | Answers | Law |
|---|---|---|
| **Left rail** | "Where can I go?" — the eleven room lenses, and nothing else | Sacred; single; never duplicated |
| **Top context bar** | "Where am I, and what is the system state?" — room title, quiet status, LED | Quiet; useful; not another nav bar |
| **Global search** | "What do we know?" — the primary retrieval door; IS the Ask Naya surface | Prominent, near top of center; full-width; never an icon |
| **Center workspace** | The active room — transforms completely per room | The sidebar is navigation; the center is the software |
| **Naya companion** | Contextual retrieval and interpretation for the current room | Never a second dashboard; never a chatbot; never a right-rail takeover |
| **Secondary ecosystem links** | External destinations (Home, Naya Power, challenge, Powercast, …) | Visually subordinate; never primary navigation |

**Routing:** `WELCOME → IDENTITY → INTELLIGENT HUB` (frozen). Room routes under the hub:
`/feed /today /reports /library /connect /ledger /connections /lists /mail /spaces /settings`.
Browser back/forward/reload must preserve room + scroll + selection state.

**Mobile law:** exactly one primary navigation surface at every viewport. Desktop: one persistent
rail. Mobile: one drawer OR one bottom nav — never rail + drawer. The drawer overlays content,
has a backdrop, owns its own vertical scroll, closes on selection / Escape / backdrop, and
preserves the underlying page position. Opening navigation must not change document width.

**Shell QA matrix (automatic failure on any):** viewports 320 / 375 / 390 / 430 / 768 / 820px;
drawer tested at top / halfway down a long page / near bottom; portrait + landscape;
125% / 150% / 200% zoom. Fail on: double navigation, horizontal scroll, black gutter, stale
overlay, width jump, scroll-position loss.

---

## 3. THE INTELLIGENCE OBJECT

The canonical unit the Hub projects. Every object the Hub displays must resolve to one of these:

- **Identity:** canonical ID, never duplicated across rooms. Cross-room handoffs pass the ID, not a copy.
- **Provenance:** source, author (or anonymized), creation time, pipeline (note/activity/report).
- **Truth state:** one of the state model (§5); VERIFIED only with evidence.
- **Layers:** the ten-layer Intelligent Block (in-a-nutshell, human, child, grandma, Naya, machine,
  learning, meaning, how-to-use, what's-in-it-for-you). Rooms choose which layers to surface;
  the object carries all of them.
- **Relationships:** related objects, supersession chain (current vs superseded), Space/context,
  consent scope.
- **The four questions** (from the Node anatomy): WHO ALLOWS (authority) · WHY BELIEVE (evidence) ·
  WHAT NEXT (responsible action) · WHAT CONNECTS (relationships). Every block shown in the Hub
  must be able to answer all four.

---

## 4. THE FEED SYSTEM

The feed is an **intelligence consumption system**: a highly organized stream through which a
person experiences their own evolving intelligence and, where consent permits, collective
intelligence. Not social media — no attention mechanics, no vanity metrics, no engagement bait.

### 4.1 The three streams (sources, not filters)

- **🧠 Personal** — my intelligence: my smart notes, my reports, my discoveries, my decisions,
  my learning, my important moments, my intelligence events. Identified to me.
- **🌐 Collective** — intelligence shared by the network: anonymized discoveries, useful patterns,
  lessons, insights, reports/events permitted for collective sharing. Identity never travels with
  the intelligence.
- **⚡ Activity** — what is happening now: state, change, process. "Working on NayaPOWER → Node 1
  → verification running." Distinct from smart notes (captured intelligence) and reports
  (structured synthesis).

Switching streams changes **actual data and state**, never just recoloring. Each stream has its
own source; the feed never filters one pile three ways.

### 4.2 Smart views (lenses over streams)

ALL · SMART NOTES · ACTIVITY · REPORTS · HIGHLIGHTS · LEARNING · DECISIONS · DISCOVERIES ·
PROJECTS · COLLECTIVE (+ custom/user-defined later). Views are projections over canonical
objects — never separate databases, never duplicated content.

### 4.3 Required components

FeedModeSelector (streams) · SpaceContext · NewSinceLastVisit · IntelligenceStream ·
IntelligenceObject · **WhyAmISeeingThis** (every object explains its ranking: relevance, recency,
Space, relationships, goals, verified learning — no mysterious ranking) · ObjectActionDeck ·
ProgressiveFilters.

### 4.4 Causal actions (all with real paths or honest unavailable states)

OPEN · ASK_NAYA (retrieval-only, CR-2) · SAVE_FAVORITE · ADD_TO_LIST · OPEN_EVIDENCE ·
SHARE_CONNECT_IF_AUTHORIZED. (`CAPTURE_SMART_NOTE` superseded per CR-1.)

### 4.5 Anti-patterns

Social-media clone · engagement bait · vanity metrics · mysterious ranking · fake live motion ·
dense filter dashboard · duplicating content across views.

---

## 5. THE TRUTH MODEL

Every room implements the full state model. No room is exempt; no state is faked.

**States:** LOADING · EMPTY · READY · BLOCKED · NOT_VERIFIED · VERIFIED · ERROR, plus
OFFLINE · UNAUTHORIZED · UNKNOWN · DISABLED where applicable.

- LOADING = subtle living illumination, only while actually loading.
- EMPTY = quiet, not broken; beautiful zero-states that teach what will appear.
- NOT_VERIFIED = truthfully uncertain — the honest default wherever the runtime isn't live.
- VERIFIED = distinct but never gaudy; only with evidence.
- No fake mailbox, no sample data, no simulated activity, no animated aliveness without backend.

**Fixtures:** any card not backed by canonical intelligence is a **design fixture**, labeled as
such, answering "what should this look like" — never "does this exist."

**Liveness:** glowing LEDs, pulsing fields, and motion communicate actual runtime state only.

---

## 6. THE ELEVEN ROOMS (LENSES)

Every room implements the five layers — **ORIENTATION → CURRENT STATE → INTELLIGENCE →
ACTION → PROOF** — and answers five questions: Where am I? What is happening? What does Naya
understand? What can I do? Why should I trust it? Detail contracts live in `HUB/ROOMS/` (PR
#1290); this spec binds the room's identity, instrument, and non-negotiables.

### 6.1 Smart Feed — THE GAME (the live intelligence stream)
Lens: what's happening / what do I have? **Signature instrument:** IntelligenceStream +
WhyAmISeeingThis. The raw/current layer that Today later synthesizes. Real streams, real state
changes, provenance on everything, cross-room movement by canonical ID. It is not Twitter with
prettier cards.

### 6.2 Your Intelligence Today — THE HIGHLIGHT REEL (the reference masterpiece)
Lens: what's important today? **Signature instrument:** TodayPulse + WhatChangedNarrative +
HighlightScene. A human understands the day in ~10 seconds. Pulse numbers recompute from
canonical data; every highlight explains why it was selected and opens the original object;
Naya Reflection is evidence-grounded; a quiet day never manufactures content. Open loops and
tomorrow's carry-forward are visible. **Build this room first, completely, before the others.**

### 6.3 Your Reports — THE FILM ROOM / TIME MACHINE
Lens: what happened over time? **Signature instrument:** PeriodSelector + ReportCover. Day, week,
month, and year must actually differ in intelligence — never date-filter the same template.
Evidence appendix; interpretation visibly distinguished from fact. Components: DailyReport,
WeeklyStory, MonthlyPatterns, YearInIntelligence, CompareMode, NayaSynthesis.

### 6.4 Intelligent Library — THE VAULT / YOUR MIND
Lens: what do we know? **Signature instrument:** IntelligenceSearch + DomainGallery. Search-first
canonical retrieval — never a second brain. Domains are navigational lenses, not stores.
Current vs superseded, related intelligence, uncertainty, gaps, "Naya, what am I missing?"
(NayaGapAnalysis). Provenance on everything.

### 6.5 Smart Connect — THE PORTAL BAY
Lens: what can intelligence connect to? **Signature instrument:** DoorPortal + DoorStatusStack.
"One brain. Many doors." Doors render from the canonical registry
(`BRAIN/10-INTERFACES/0002-SMART-DOOR-REGISTRY-V1.json`) — never hardcoded, never a roadmap
door presented as live. CONNECT → CONFIGURE → VERIFY. Connection, authentication,
authorization, and health are separate states; **connected never equals authorized.**

### 6.6 Smart Ledger — THE BLACK BOX / PROOF ROOM
Lens: what actually happened? **Signature instrument:** CausalTimeline + StageChain:
RECEIVED → AUTHORIZED → EXECUTED → OBSERVED → VERIFIED → OUTCOME. The human inspects the trust
chain here. Never infer verification from executor success. Receipts, evidence, actor, authority,
outcome — all inspectable.

### 6.7 Your Connections — THE CONSTELLATION
Lens: who/what is related? **Signature instrument:** RelationshipConstellation +
SelectedConnectionPanel. Not a giant graph demo: select a relationship and show why it matters —
shared context, consent/share state, shared intelligence, meaningful interaction, next relevant
action. Graph visuals are secondary; consent state is primary.

### 6.8 Smart Lists — THE MISSION TABLE
Lens: what do I need to act on? **Signature instrument:** ActionLaneBoard:
NOW / NEXT / WAITING / QUESTIONS / IDEAS / OPPORTUNITIES / COMPLETED. Lists organize canonical
objects; they never copy intelligence. Smart lists explain every inclusion (WhyThisIsHere);
manual/hybrid controls; blockers and opportunities as first-class states.

### 6.9 Smart Mail — THE SIGNAL ROOM
Lens: what signals require attention? **Signature instrument:** SignalList + MessageReader +
ContextPanel. IMPORTANT / RESPOND / FOLLOW UP / DRAFTS / SENT. Message + context + related
intelligence + response/action. **No fake mailbox, ever:** runtime unavailable →
RUNTIME UNAVAILABLE; no mail → NO MAIL; auth problem → ACCESS BLOCKED. Naya drafting is
separate from authorized sending.

### 6.10 Smart Spaces — THE WORLDS
Lens: what intelligence belongs to this context? **Signature instrument:** the Space itself as
governed context. A Space is a true context environment — intelligence, people, projects, notes,
lists, activity, goals, rules, connections — and switching Space must actually alter context:
queries, interpretation, and feed ranking change. Never storage duplication. Privacy gradients:
private by default, shared by choice, collective by consent, public by decision.

### 6.11 Settings — THE CONTROL DECK
Lens: how is my intelligence governed? **Signature instrument:** the governance panel cluster.
Identity, Privacy, Authority, Connections, Notifications, Data, Security, Appearance, plus Your
Intelligence (your intelligence is yours). System diagnostics live under Settings → System
Health — never as a primary room. Infrastructure stays under the hood.

---

## 7. ASK NAYA (RETRIEVAL SPEC)

"Ask Naya" in the Hub is **ask-the-brain**: a Q&A interface over the NayaPOWER knowledge base.
The human asks anything about NayaPOWER; answers are composed from canonical intelligence with
visible provenance. The global search box IS this surface — one door, not two.

- **It is retrieval, not agency.** It answers; it never acts, never commands, never captures.
- **It is not a chatbot.** No conversation, no persona play, no open-ended dialogue. Question in,
  sourced answer out.
- **Voice read-back:** every intelligent block carries a play control that reads the block aloud.
  Output, so it belongs.
- **Honest states:** unanswered → NOT_VERIFIED ("the knowledge base has no verified answer");
  never hallucinated confidence.
- Humans talk *to* Naya through their own AI (ChatGPT, Muse, Grok, Claude, Gemini). The Hub is
  not where that happens.

---

## 8. DESIGN SYSTEM BINDINGS

The visual law is `HUB/DESIGN-CONTRACT.md` — this spec binds it, not repeats it:

- **Tokens:** the `:root` spectrum (purple → magenta in fixed order); `--room-accent` /
  `--room-glow` / `--room-surface` per room; no inline theme overrides.
- **Button law:** the 10-point recipe (material, bevel, elevation, theme energy, hover lift,
  active illumination + accent rail, press compression, focus, honest disabled, motion
  discipline `.22s cubic-bezier(.16,.84,.22,1)`). A button is incomplete until its action has a
  real causal path.
- **Board law:** each board is a distinct intelligence object — identity, theme, icon, state,
  material, depth, energy, hierarchy, provenance, actions. No two boards feel like the same card
  recolored.
- **Icon law:** one faceted jewel family; unicode/emoji icons are placeholders, zero in production.
- **Spectrum law:** color carries semantic meaning (purple = intelligence, gold = value/consequence,
  red = warning…); never decorative fill; never overpowering reading content; gold restrained.
- **Living depth:** every important object occupies space — surface, edge, highlight, shadow,
  restrained halo. Flat is not acceptable; gratuitous 3D is not acceptable.
- **Visual bliss:** generous readable type, high contrast, one clear hierarchy, restraint — every
  element earns its place. No glow, color, depth, or motion may reduce readability.
- **Typography:** body 17–18px target, 16px floor (pending Shawn's ruling on the open 15px question);
  no sub-11px text anywhere.

---

## 9. CROSS-CUTTING REQUIREMENTS

- **Mobile:** identity preserved at every size (rail → elite bottom bar / gesture nav, never boring
  cards); the shell QA matrix (§2) is the gate.
- **Accessibility:** full keyboard operation, visible elegant focus, semantic landmarks, screen
  reader correctness, `prefers-reduced-motion` honored (depth survives without motion), contrast
  AA+, usable at 200% zoom.
- **Performance:** instant response; transform/opacity animation only; no layout thrash; the 843KB
  laboratory's weight must not ship — depth earned without bulk.
- **Continuity:** sessions survive; state, lists, and learning persist; close it, come back
  tomorrow — everything is where it was left. Errors readable and recoverable, never silent.
- **Cross-room identity:** handoffs carry canonical IDs; opening an object in Library from the
  Feed shows the same object, same state, same provenance.

---

## 10. ACCEPTANCE

### 10.1 The pipeline acceptance test (Shawn's)

"Naya, create a Smart Note about X." Then, without the human touching the Hub:
canonical IB exists → governed event emitted → persistence succeeds → Feed receives it →
correct stream + smart-view categorization → Personal/Collective visibility follows consent →
provenance inspectable → Library can retrieve it → Today/Reports can incorporate it.
**If a human must carry it there, the Hub isn't finished, no matter how beautiful it looks.**

### 10.2 The room acceptance bar (no-more-shells)

Each room passes only with: five layers complete · all applicable states designed · mobile
proven · keyboard proven · zoom proven · reduced-motion proven · runtime path real or honestly
unavailable · persistence proven where promised · cross-room handoff by canonical ID ·
back/forward/reload proven · failure/refusal paths proven · independent review passed.

### 10.3 The score

D1–D8 self-score with evidence, then independent re-score. Below 9.0 = not ready. Target 10,
happy with 9.5. Scores can go down.

---

## 11. BUILD ORDER (THE PIECES)

1. **Repair/prove the app shell** (§2 + shell QA matrix). Nothing inherits a broken shell.
2. **Build Your Intelligence Today end-to-end** as the reference masterpiece (§6.2). One
   masterpiece before eleven mediocre rooms.
3. **Prove one intelligence object across the system:** capture (outside Hub) → persistence →
   Feed → Today → Library → List/Space → Ledger, same canonical ID throughout.
4. **Make search real:** governed retrieval + relevance + provenance. Stop searching rendered DOM.
5. **Compound room by room** in dependency/value order, reusing Today's proven architecture.
6. **Brutal rendered QA** until the score earns itself; independent re-score; repeat.

---

*Spec version 1.0 — 2026-10-01. Author: Naya 2. Authority: Human Director Shawn Vibert.
Supersedes no prior spec; reconciles conflicts explicitly in §1 (CR-1..CR-3). Room detail
contracts remain in HUB/ROOMS/ (PR #1290).*
