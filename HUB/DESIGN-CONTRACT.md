# 🔱 NAYANET INTELLIGENT HUB — FULL DEEP-DIVE & ELITE DESIGN CONTRACT

**For:** Any AI builder asked to work on the Hub. Read this entire document before touching anything.
**From:** Naya 4 — verified against the live `main` tree of `SoulSchoolAcademy/NayaPOWER`, 2026-10-01.
**Status:** DESIGN BASELINE — the current visual Hub is the reference. You may improve it. You may not replace it with something cleaner-but-generic.

---

## HOW TO USE THIS DOCUMENT

Shawn's standing complaint is real and verified: every attempt to take the Hub "to the next level" has gone backward — the design got flatter, more generic, more SaaS-dashboard. That happens because builders unconsciously interpret "production-ready" as "rebuild the UI cleanly."

That interpretation is **forbidden** here.

The rule is: **the architecture underneath changes dramatically; the visual experience changes only when the change is demonstrably better.** The current Hub is the floor, not a draft. Minimum acceptable = where it is right now.

---

## PART 1 — FULL INVENTORY: WHAT EXISTS, WHERE, EXACTLY

### 1.1 The files (live on `main`, `HUB/` directory)

| File | Size | What it is |
|---|---|---|
| `NAYANET INTERFACE CONCEPT.html` | 843,432 bytes | The Hub visual concept — the baseline |
| `NAYANET WELCOME PAGE.html` | 27,206 bytes | The entrance — jewel portal |
| `NAYANET INDENITY PAGE.html` | 11,543 bytes | The identity bridge (note: filename has a typo, "INDENITY") |
| `hub.html` | 28,571 bytes | **Not the Hub** — this is the Powercast player. Do not confuse them. |
| `manifest.webmanifest` + icons | — | PWA install assets |

### 1.2 The concept file is a laboratory, not an application

Measured 2026-10-01 from the live file:

- 27 `<script>` tags, 7 `<style>` tags
- 167 `function` declarations, 113 unique names
- **Duplicate implementations:** `run()` ×13, `css()` ×11, `boot()` ×10, `actions()` ×4, `feed()` ×3, `toast()` ×3
- 53 `addEventListener` registrations, 11 MutationObserver references, 27 `setTimeout`, 1 `setInterval`, 16 `localStorage` uses

Translation: the file contains **multiple generations of competing implementations** layered on top of each other. The visual language was discovered inside this file. The production job is to **extract the language from the laboratory** — deciding which of the 13 `run()` variants is canonical is archaeology, not cleanup. Do not "simplify" by deleting what you don't understand.

### 1.3 Page structure (top to bottom, left to right)

```
┌──────────┬──────────────────────────────────────────────┐
│          │  TOP BAR: room title · system status · LED    │
│          ├──────────────────────────────────────────────┤
│  LEFT    │  ECOSYSTEM BAR (secondary, 8 links)           │
│  RAIL    ├──────────────────────────────────────────────┤
│  (11     │  SEARCH (prominent, full-width)               │
│  buttons │──────────────────────────────────────────────┤
│  + brand │  HERO: "Good evening, Shawn" + date/time     │
│  +       │──────────────────────────────────────────────┤
│  privacy │  FEED MODE TABS: Collective / Personal /     │
│  note)   │  Activity                                     │
│          │──────────────────────────────────────────────┤
│          │  NINE INTELLIGENCE BOARDS (themed, elevated)  │
│          │──────────────────────────────────────────────┤
│          │  NAYA CARD (presence, insight, Ask Naya)      │
└──────────┴──────────────────────────────────────────────┘
```

### 1.4 Left rail — exact inventory (11 buttons, in order, with theme colors)

These are the actual `--nav` values from the live markup. **Each button already has its own theme color. Preserve all of them.**

| # | Label | Icon | Theme color | Hex |
|---|---|---|---|---|
| 1 | Smart Feed | ⌂ | emerald | `#55e39a` |
| 2 | Your Intelligence Today | ✦ | magenta | `#d86cff` |
| 3 | Your Reports | ▦ | indigo | `#6675ff` |
| 4 | Intelligent Library | ◈ | sapphire blue | `#55b9ee` |
| 5 | Smart Connect | ⇄ | emerald | `#55e39a` |
| 6 | Smart Ledger | ◇ | yellow | `#f1d75a` |
| 7 | Your Connections | ⌁ | orange | `#ff9a5a` |
| 8 | Smart Lists | ☷ | purple | `#9d75ff` |
| 9 | Smart Mail | ✉ | sapphire blue | `#55b9ee` |
| 10 | Smart Spaces | ⬡ | lime | `#b8ee57` |
| 11 | Settings | ⚙ | gray | `#aaa4b1` |

Rail header: NayaNET brand mark + "INTELLIGENT HUB · V7".
Rail footer (keep verbatim): **PRIVATE BY DEFAULT** — "Shared by choice · Collective by consent · Public by decision."

> ⚠️ **Naming resolved (director decision 2026-10-01):** there is no "Smart Share." The room is **Smart Connect** — also called **Smart Doors**. It is the connection interface to the intelligence: however a human, AI, machine, or system wants to connect, there is a door for it. The full channel classification lives in the Smart Doors spec below (Part 4).

### 1.4b The Smart Doors — connection channels (from the Smart Doors spec)

One brain. Many doors. Each door is a connection channel into the same canonical intelligence, each with its own themed object in the Connect room:

| # | Door | Who connects | Purpose |
|---|---|---|---|
| 1 | **MCP** | AI agents | Agent → NayaPOWER tools and context. Priority 1. |
| 2 | **REST / OpenAPI** | Apps, agents | Programmatic access to NayaPOWER operations. |
| 3 | **GitHub App** | Coding / repository agents | Governed repo operations; the app Shawn's team creates. |
| 4 | **Webhooks** | External systems | System → NayaPOWER events in. |
| 5 | **SDK** | Developers | Embed NayaPOWER intelligence in their own products. |
| 6 | **A2A** | Agents | Agent ↔ agent collaboration. |
| 7 | **Browser / Web Hub** | Humans | The Hub itself is a door — the human cockpit. |
| 8 | **Email / messaging adapters** | Humans, networks | Human and network communication channels. |
| 9 | **Enterprise identity** | Organizations | Organization-level authorization. (Later.) |
| 10 | **Private MCP tunnel** | Private / on-prem agents | Specialized private access. |

**Door Law (frozen):** every door object shows what it is, who it's for, live connection status, and the connect action with a real causal path. Connecting through a door never implies permission to act — connection ≠ authority. That distinction is architectural law.

### 1.5 Top bar

- Current room/surface title (left)
- System status text + glowing LED indicator (right)
- The LED uses `--gold` (`#e8c766`) with `box-shadow: 0 0 12px` glow
- Purpose: the human always knows **where am I** and **what is the system state**

### 1.6 Ecosystem bar (secondary navigation — 8 links)

HOME · NAYA POWER · "5" DAY CHALLENGE · ENTER FREE · POWERCAST · WHITE PAPER · ABOUT US · HMC LOGIN

These are **ecosystem/external destinations**, not intelligence rooms. They must always look visually **secondary** to the rail. Never promote them to primary navigation.

### 1.7 Search — placement and philosophy (DO NOT MOVE)

- Position: full-width, directly under the ecosystem bar, above the hero. **Prominent, not tucked in a corner.**
- Placeholder: "Search intelligence — what, why, source, learning, meaning…"
- The language is deliberate: you search **intelligence**, not documents.
- Visual recipe (live CSS): `min-height:58px; border:2px solid #8f6aff77; border-radius:17px; background:linear-gradient(145deg,#15101d,#07070b); box-shadow: inset 0 1px #fff6, 0 18px 42px #000b, 0 0 28px #8b63ff10`
- Focus state: border goes magenta, glow intensifies (`0 0 40px #d86cff20`)
- Keep this placement unless real user testing proves a better one. Never move it to satisfy dashboard convention.

### 1.8 Hero / greeting

- Time-aware: "Good morning / Good afternoon / Good evening, Shawn" (computed from local hour)
- Subline: "Smart notes are where intelligence becomes useful."
- Meta row: live TIME, DATE, COUNTRY
- The name must derive dynamically from identity in production — never hardcode "Shawn"
- Job: the bridge between human and system. Personal without being a chatbot.

### 1.9 Feed mode tabs

Three modes, and **the tab must change actual data and state, never just recolor itself**:

- **COLLECTIVE** — shared/collective intelligence
- **PERSONAL** — the user's own intelligence
- **ACTIVITY** — what has happened in the intelligence system

### 1.10 The nine intelligence boards

Each board is a **distinct intelligent object with its own theme** — not a card in a grid:

1. **WHAT IS NAYA POWER?** — foundational system explanation
2. **WHAT IS NAYA?** — identity and conceptual definition
3. **WHAT ARE SMART NOTES?** — the intelligence-capture concept
4. **YOUR INTELLIGENCE TODAY** — the daily intelligence cockpit
5. **INTELLIGENCE REPORTS** — cross-time synthesis
6. **WHAT IS THE INTELLIGENT LIBRARY?** — persistent intelligence retrieval
7. **SMART LISTS** — organization of saved intelligence
8. **INTELLIGENT FEED / SMART FEED** — the live intelligence stream
9. **SMART TABS** — navigation of intelligence surfaces

### 1.11 The intelligence layers (product philosophy, not decoration)

Every board distills through recurring cognitive layers. **This is the product philosophy — one intelligence object understood at multiple cognitive levels:**

- **HUMAN NOTE** — the human's input
- **CHILD** — simplified explanation
- **GRANDMA NOTE** — why it matters / why notice
- **NAYA NOTE** — Naya's interpretation
- **MACHINE NOTE** — the evidence boundary (what is proven vs. claimed)
- **ADAPTIVE LEARNING** — what the system learned
- **WHAT IT MEANS** — significance
- **WHAT'S IN IT FOR YOU?** — human value

UI rule: layers must feel like **nested intelligence**, not repeated sections. Each layer gets its own colored border, illuminated sphere, facet icon, and state — already partially built in the concept.

### 1.12 The Naya Card (presence)

- Naya visual + current insight + "Ask Naya" + "What should I know?" + trust-state info
- Purpose is **interpretation and human assistance** — "Naya is here," not "here is another dashboard"
- Never let it become a competing right rail

---

## PART 2 — THE DESIGN LANGUAGE (EXTRACTED FROM THE LIVE FILE, NOT INVENTED)

### 2.1 Design tokens (the actual `:root` block, verbatim)

```css
--bg:#050507;        /* obsidian foundation */
--ink:#f8f7fb;       /* primary text */
--muted:#aaa4b1;     /* secondary text */
--line:#ffffff18;    /* hairline borders */
--purple:#9d75ff;
--indigo:#6675ff;
--blue:#55b9ee;      /* sapphire */
--green:#55e39a;     /* emerald */
--lime:#b8ee57;
--yellow:#f1d75a;
--gold:#e8c766;
--magenta:#d86cff;
--red:#ff5e6c;
--ease:cubic-bezier(.16,.84,.22,1);  /* the motion signature */
```

**These tokens are already the spectrum.** The file knew the answer before the contract did.

### 2.2 The button recipe (exact, from live CSS — this is the standard)

Every primary button in the production app must implement this grammar:

```css
/* BASE — dark material, precise edge */
.nav button {
  min-height: 43px;
  border: 2px solid #8b63ff42;
  border-radius: 13px;
  background: transparent;
  display: flex; align-items: center; gap: 9px;
  font-size: 10px; font-weight: 850;
  transition: .22s cubic-bezier(.16,.84,.22,1);
  overflow: hidden;
}

/* HOVER — lift, brighten, sharpen, glow */
.nav button:hover {
  background: #ffffff08;
  border-color: #a989ff;
  transform: translateY(-2px);
  box-shadow: 0 12px 25px #0008, inset 0 1px #fff3;
}

/* ACTIVE — persistent illumination + theme energy */
.nav button.active {
  background: linear-gradient(145deg, #20182b, #0d0c12);
  border-color: #d86cffaa;
  box-shadow: inset 0 1px #fff7, 0 14px 32px #000a, 0 0 30px #d86cff22;
}

/* ACTIVE INDICATOR — the glowing accent rail */
.nav button.active:after {
  content: ""; position: absolute; right: 7px;
  width: 3px; height: 21px; border-radius: 4px;
  background: var(--magenta);
  box-shadow: 0 0 16px var(--magenta);
}
```

**The 10-point Button Law (frozen):**

1. **Material** — dark obsidian/graphite body, never flat
2. **Bevel** — subtle inner highlight (`inset 0 1px #fff3`-class)
3. **Elevation** — real shadow separation from the surface
4. **Theme energy** — accent glow tied to the button's meaning color
5. **Hover lift** — small Z-axis illusion (`translateY(-2px)`), brighten, sharpen, glow
6. **Active state** — persistent illumination + the glowing accent rail
7. **Press state** — compress, darken, reduce shadow depth
8. **Focus state** — accessible, visible, elegant (keyboard users)
9. **Disabled state** — visually honest; never looks clickable when it isn't
10. **Motion discipline** — fast, smooth, physical. `.22s` with the signature ease. Never bouncy.

**A button is not complete until its action has a real causal path.** A beautiful button that does nothing is a lie.

### 2.3 The board recipe

Each board is an intelligence object with: identity icon · theme color · theme glow · material surface · elevation · status · content hierarchy · interpretation layers · actions · state.

Minimum visual grammar per board: surface → edge → inset highlight → elevation shadow → theme glow → hover lift → pressed compression → active illumination → accessible focus → honest disabled.

### 2.4 The Spectrum Law (DIRECTOR-RESOLVED 2026-10-01)

Shawn's explicit word, overriding the old `VISUAL-LANGUAGE.md` line 13 ("No yellow or gold accents"):

> The interface moves through a living color field:
> **purple → indigo → sapphire → teal → emerald → lime → yellow → gold → orange → rich orange → red → magenta → (back to purple)**

Semantic energy map (color carries meaning, never decoration):

| Color | Meaning |
|---|---|
| 🟣 Purple | intelligence, emergence, identity |
| 🔵 Indigo | comprehension, depth |
| 💎 Sapphire | knowledge, information |
| 🩵 Teal | connection, flow |
| 🟢 Emerald | active / healthy / available |
| 🟩 Lime | learning / growth |
| 🟡 Yellow | attention / signal |
| 🟨 Gold | value / consequence |
| 🟠 Orange | action / movement |
| 🔶 Rich orange | transition / momentum |
| 🔴 Red | warning / consequence / intensity |
| 🩷 Magenta | human significance / expression |

**Constraint (preserved from the old discipline):** spectrum accents must be semantically justified. Never flat decorative background fills. Never overpower primary reading content. Primary text stays high-contrast white/light neutral.

### 2.5 The Living Depth Law (frozen)

A flat interface is not acceptable. Every important interactive object must look like it occupies space:

- **Surface** — dark, dense, premium material
- **Edge** — a precise illuminated boundary
- **Upper surface** — very subtle specular highlight
- **Lower surface** — deep shadow / bevel impression
- **Ambient field** — restrained halo in the object's theme color
- **Hover** — lift → brighten → sharpen → glow
- **Press** — compress → darken → reduce shadow depth
- **Active** — retain elevation + increase energy

Not fake-90s-3D. Not excessive glassmorphism. Not floating cartoon buttons. **Physical presence.**

### 2.6 The Icon Law (the biggest visual gap — see scorecard)

One NayaNET icon family. The concept already started it (`naya-elite-icon`: 28px, drop-shadow, theme-toned). Lock in:

- faceted, jewel-like, precision geometry — "precision-cut crystal / luminous technical emblem"
- identical geometry rules, stroke philosophy, optical depth, internal facet logic across all icons
- theme-driven illumination per board
- **No random emoji as primary production iconography.** The current rail uses ⌂ ✦ ▦ ◈ ⇄ ◇ ⌁ ☷ ✉ ⬡ ⚙ — these are placeholders the jewel system must replace, one family at a time, board by board.

### 2.7 The Liveness Law (frozen)

**Animation communicates actual state. Animation never manufactures state.**

- Glowing green LED = connected — only if actually connected
- Pulsing purple field = processing — only while processing
- Gold state = value/attention — only with evidence for that state
- Loading shimmer = loading — only while loading

Never "make it look alive so the user assumes it works." That's the difference between a living interface and a fake one. The concept's "YOUR INTELLIGENCE TODAY" already marks things **NOT VERIFIED** when retrieval is unavailable — that honesty is the standard.

### 2.8 Room state model (every room, no exceptions)

`LOADING` · `EMPTY` · `READY` · `BLOCKED` · `NOT_VERIFIED` · `VERIFIED` · `ERROR`

Each with standardized visuals: LOADING = subtle living illumination; EMPTY = quiet, not broken; BLOCKED = clearly unavailable; NOT_VERIFIED = truthfully uncertain; VERIFIED = distinct but never gaudy; ERROR = readable and actionable.

---

## PART 3 — SCORECARD (Naya 4's scores, 2026-10-01)

### 3.1 Hub visual concept

| Surface | Score | Notes |
|---|---|---|
| Buttons / left rail | **9.2** | The button recipe is genuinely elite. Keep it exactly. |
| Boards | **8.5** | Strong objects, but themes aren't yet systematic — Shawn's note: "even the boards need some work" |
| Color system | **8.7** | The spectrum exists in tokens but isn't enforced as a system |
| Icons | **6.5** | The weakest visual link — unicode placeholders vs. the jewel system that started |
| Search | **9.0** | Placement, philosophy, and styling are all correct |
| Hero / greeting | **8.5** | Personal, warm, time-aware |
| Layout / composition | **8.8** | Single rail, no dashboard grid, good discipline |
| Motion / liveness | **8.0** | Rich, but some motion is decorative rather than state-driven |
| **Overall visual** | **8.7** | |
| **As a functioning application** | **4.5** | It's a concept file, not an app. Honest score. |

### 3.2 Why not a 10 — the specific gaps

**Visual 10 requires:**
1. **Icon consistency** (biggest gap, 6.5) — replace all unicode placeholder icons with the faceted jewel family, one board at a time
2. **Board theme systematization** — every board gets its spectrum assignment from the token system, not ad-hoc inline styles
3. **Motion tied to state** — audit every animation against the Liveness Law; decorative-only motion gets cut or connected
4. **Responsive** — mobile must preserve identity, not collapse into generic cards
5. **Accessibility** — focus states, keyboard nav, reduced-motion, semantics
6. **Token discipline** — no more `style="--nav:#ff9a5a"` inline; everything through `--room-accent` / `--room-glow` / `--room-surface` tokens

**Application 10 requires:**
1. Real component model (AppShell, LeftRail, Board, IntelligenceLayer, Icon, ActionButton, Room…)
2. Real room router — one shell, many rooms, one intelligence substrate
3. Runtime adapter — Hub asks the governed runtime; never raw database queries from the UI
4. Real identity → real retrieval → real data → real persistence → real verification
5. The honest state model in every room

### 3.3 Welcome page — scorecard

| Dimension | Score |
|---|---|
| Visual | **8.8** |
| Concept | **8.7** |
| **Overall** | **8.7** |

The jewel portal (108 generated jewels across a 12-family spectrum palette, orbital motion, "Naya Responding" state change on name entry, portal push-forward) is already the living-system metaphor. **Verdict: needs little.** Possible level-ups: smoother entrance sequencing, the identity handoff transition into the Identity page (make it feel like one continuous journey, not two pages), audio-reactive shimmer if tasteful. Do not explain NayaPOWER here — the Welcome page's job is **invitation**, not explanation.

### 3.4 Identity page — scorecard

| Dimension | Score |
|---|---|
| Visual | **6.1** |
| Concept | **6.4** |
| Function | **4.8** |
| **Overall** | **5.8** |

**This is the weak link and it needs major work:**
- Feels like a utility activation form, not part of the Welcome/Hub universe
- **Wrong redirect:** currently sends to a `workers.dev` URL — must go to the Intelligent Hub
- Required flow: **WELCOME → IDENTITY → INTELLIGENT HUB** (frozen as a routing requirement)
- The Identity page must become the bridge: "I know who you are allowed to be here as" → "Enter your Hub"
- Needs: jewel identity emblem, deep obsidian board, elevated identity card, animated identity state, polished alias field with live NayaNET namespace preview, privacy statement, clear auth state, loading/establishing/success/fail-closed states, and the final ENTER NAYANET transition — all in the same design system as the Hub

---

## PART 4 — FUNCTIONAL CONTRACT: WHAT EACH ROOM MUST DO

Architecture (frozen): **Hub = cockpit. NayaPOWER = governed intelligence substrate.** The Hub presents intelligence from the canonical substrate; it is never a second brain, second database, or shadow memory.

**Data path:** Hub → Runtime Adapter → Governed Runtime → Canonical Intelligence. Never Hub → raw database query.

### The 11 rail rooms

**🏠 Smart Feed** — the primary human-facing intelligence stream. Shows relevant intelligence, Smart Notes/Intelligent Blocks, current context, provenance, actions (open, save, favorite, rank, share, capture). Three modes (Collective/Personal/Activity) must change **actual data**. It is the projection layer, not another database.

**✦ Your Intelligence Today** — answers: what happened, what changed, what did I learn, what matters now, what should I remember, what am I missing, what does Naya think, what can I do next. Marks **NOT VERIFIED** wherever retrieval isn't live — that honesty is the standard.

**▦ Your Reports** — cross-time synthesis: Today → Daily → Weekly → Monthly → Yearly → thematic/decision reports. A report answers "what does the accumulated intelligence *mean*?" with evidence/provenance visible. Never just "12 objects found."

**◈ Intelligent Library** — deliberate retrieval of preserved intelligence. Search, filter, inspect, explore (by time, source, subject, person, project, provenance, value, status). **Queries the canonical substrate — never becomes a second brain.**

**⇄ Smart Connect (Smart Doors)** — the connection interface. "One brain. Many doors." Every door in §1.4b gets its own themed, elevated object: what the door is, who it's for, live status (connected/available/coming soon), and the connect action with a real causal path (OAuth flow, key provisioning, webhook registration — never a dead button). Humans, AIs, machines, systems: however they want to connect, there's a door. This is the "new internet" surface — many minds, one intelligence. Connection never implies permission to act.

**◇ Smart Ledger** — the proof/accountability surface. Answers: what happened, when, who/what initiated it, under what authority, what evidence exists, what receipt proves it, what was the outcome. **This is where the human inspects the trust chain** — decision receipts, VERIFY receipts, persistence proofs live here.

**⌁ Your Connections** — governed relationships: people, Nayas, organizations, spaces, shared-intelligence relationships. Relationships are governed; connection ≠ permission.

**☷ Smart Lists** — the human-friendly organization layer: saved, favorites, topics, collections ("things I need," "decisions," "ideas," "lessons"). Organizes canonical intelligence; never becomes yet another storage system.

**✉ Smart Mail** — a real room. **No fake mailbox, ever.** Runtime unavailable → RUNTIME UNAVAILABLE. No mail → NO MAIL. Auth problem → ACCESS BLOCKED. Never "here's some sample email."

**⬡ Smart Spaces** — context boundaries (personal, family, project, business, research, collective). Respects: private by default, shared by choice, collective by consent, public by decision.

**⚙ Settings** — the human's relationship with NayaNET: identity, authentication, account, runtime status, privacy, connections, preferences, notifications, trust status. Infrastructure stays under the hood.

---

## PART 5 — THE BUILD ORDER (HOW TO GET THERE WITHOUT GOING BACKWARD)

**Forbidden:** rewriting the Hub from scratch · designing a prettier dashboard · replacing boards with generic components · flattening the board structure · removing animation as "decoration" · adopting a standard design system · turning it into a three-column dashboard · more cards, more KPIs, more glass, more gradients-in-gradients.

**The sequence:**

1. **Freeze the visual reference** — `NAYANET INTERFACE CONCEPT.html` is the acceptance baseline. Snapshot typography, spacing, geometry, colors, button behavior, board treatment, icon proportions, search placement, rail placement, animation character.
2. **Extract the token system** — the `:root` tokens above become the real theme contract; eliminate inline `style="--nav:..."` in favor of `--room-accent`/`--room-glow`/`--room-surface`.
3. **Componentize without redesigning** — AppShell, LeftRail, TopBar, EcosystemBar, Search, FeedTabs, Board, IntelligenceLayer, Icon, ActionButton, StatusPill, NayaCard, Room. Same visuals, real components.
4. **Build the room router** — one shell, eleven rooms, one intelligence substrate.
5. **Build the runtime adapter** — the Hub asks the governed runtime for everything.
6. **Wire honest states** — every room implements the seven-state model; rooms without live data show NOT_VERIFIED, never fake content.
7. **Fix the identity bridge** — rebuild the Identity page in the design system; fix routing to WELCOME → IDENTITY → HUB.
8. **Complete the icon family** — replace unicode placeholders with the faceted jewel system, board by board.

**Sequencing honesty:** the application architecture (steps 1–4, 7–8) can start now. Steps 5–6 depend on the persistence path going live (NayaPOWER seam proven 2026-10-01, awaiting production merge). Rooms without live backends stay honestly NOT_VERIFIED — that is a feature, not a gap.

---

## PART 6 — THE FROZEN LAWS (SUMMARY FOR THE BUILDER)

1. **Baseline Law** — the current visual Hub is the floor. Improve, don't replace.
2. **Living Depth Law** — every important object occupies space: surface, edge, highlight, shadow, glow, hover lift, press compression.
3. **Button Law** — the 10-point recipe above. A button isn't done until its action has a real causal path.
4. **Spectrum Law** — the 12-color living field, semantically assigned, never decorative fill. (Director-resolved 2026-10-01, overriding the old yellow/gold ban.)
5. **Board Law** — each board is a distinct intelligence object with identity, theme, icon, state, and actions.
6. **Icon Law** — one faceted jewel family; no emoji placeholders in production.
7. **Liveness Law** — animation communicates actual state; never manufactures it.
8. **Rail Law** — single left rail, eleven rooms, Smart Connect (not Share), privacy footer verbatim.
9. **Search Law** — prominent placement, "search intelligence" language. Don't move it.
10. **Routing Law** — WELCOME → IDENTITY → INTELLIGENT HUB. Never to the academy page.
11. **Honesty Law** — NOT_VERIFIED over fake content, always. RUNTIME UNAVAILABLE over sample data, always.
12. **Cockpit Law** — the Hub presents; NayaPOWER knows. Never a second brain.

---

## PART 7 — THE FINISHED CONTRACT (V1.0 §§14–29)

*Completing the Elite Interface & Application Design Contract V1.0, cut off at §13. Same voice, same law. Verified against the canonical docs — net-new content only where the existing contract was silent.*

### §14. FEED MODES

Three modes: **COLLECTIVE** (shared intelligence) · **PERSONAL** (the user's own) · **ACTIVITY** (what happened in the system). The tab must change **actual data and state** — never merely recolor itself. A mode switch with no data change is a lie told in UI.

### §15. INTELLIGENCE BOARDS

The nine boards are the conceptual structure of the Hub, not marketing cards: What Is Naya Power? · What Is Naya? · What Are Smart Notes? · Your Intelligence Today · Intelligence Reports · Intelligent Library · Smart Lists · Intelligent Feed / Smart Feed · Smart Tabs. Each obeys the Board Law (§6): identity, theme, icon, state, material, depth, energy, hierarchy, provenance, actions.

### §16. INTELLIGENCE LAYERS

One intelligence object, multiple cognitive levels — never competing copies of truth. The eight layers: HUMAN NOTE · CHILD (simplified) · GRANDMA NOTE (why notice) · NAYA NOTE (interpretation) · MACHINE NOTE (evidence boundary) · ADAPTIVE LEARNING · WHAT IT MEANS (significance) · WHAT'S IN IT FOR YOU (human value). Render as **nested intelligence**, not repeated sections. Each layer keeps its colored border, illuminated sphere, and faceted icon from the concept.

### §17. NAYA PRESENCE

The Naya card means **"Naya is here"** — interpretation and human assistance (insight, "Ask Naya," "What should I know?", trust state). It must never become a competing dashboard, a second rail, or a chatbot that swallows the Hub.

### §18. HERO / GREETING

The greeting ("Good evening, Shawn") is the human→system bridge: personal without being a chatbot. The production version derives identity dynamically. Keep the concept; never turn it into a headline.

### §19. WELCOME

Welcome's job is **invitation, not explanation**. Keep the orbital jewels, spectral field, portal, black environment, and restrained entrance movement. Do not turn it into an explainer page. The system noticing you — "Naya Responding," the portal pushing forward — is the metaphor. Preserve it.

### §20. IDENTITY

Identity is the bridge and the current weak link. It must feel like the system saying *"I know who you are allowed to be here as — your intelligence environment is ready"* → **ENTER NAYANET** → the real Hub. Requirements: jewel identity emblem, obsidian board, elevated identity card, live NayaNET namespace preview, privacy statement, governed session identity, NayaPOWER connection state, loading/establishing state, **fail-closed** error state, success transition. Rebuilt in the design system — never a utility form, never a redirect to an external worker.

### §21. ROOM STATE MODEL

Every room implements the seven states — LOADING · EMPTY · READY · BLOCKED · NOT_VERIFIED · VERIFIED · ERROR — with standardized visuals (see §2.8). No room is exempt. No state is faked.

### §22. JOURNEY

**WELCOME → IDENTITY → INTELLIGENT HUB.** Canonical, governed, no exceptions. Not to the Academy, not to Powercast, not to an external worker. (Routing Law, §12 frozen laws.)

### §23. RESPONSIVE

Mobile preserves identity — rail becomes an elite bottom bar or gesture nav, boards keep depth and theme. Never collapse into boring cards. The Hub must feel like the same instrument at every size.

### §24. ACCESSIBILITY

Visible elegant focus · full keyboard operation · `prefers-reduced-motion` honored (living depth survives without motion) · semantic landmarks · readable hierarchy before color. Beauty that excludes is not elite.

### §25. PERFORMANCE

Instant response. Animate transform/opacity. No layout thrash. The 843 KB laboratory's weight must not ship — the production app earns its depth without its bulk.

### §26. HONESTY

No fake capability, ever. No sample data, no simulated activity, no animated aliveness without a live backend. NOT_VERIFIED over fake content. RUNTIME UNAVAILABLE over sample data. A false impression costs more than an empty state. (Honesty Law, §12 frozen laws.)

### §27. WHAT NOT TO ADD

"Next level" never means: more cards · more KPI stats · more rounded rectangles · more glass · gradients inside gradients · giant marketing headlines · pale lavender interfaces · generic sidebar icons · random emoji · gratuitous particles · competing right rails · duplicated navigation. **More depth, not more clutter.**

### §28. THE DEFINITION OF ELITE

Elite does not mean flashy. **Elite means every visual decision feels intentional.** A premium button is premium because the geometry is exact, the edge precise, the shadow believable, the highlight restrained, the hover physical, the state meaningful, the typography right, the icon integrated, the color meaningful — not because it glows.

### §29. ACCEPTANCE

The contract is satisfied only through the eight-dimension scorecard (PROJECT-INTELLIGENCE.md §2): every dimension ≥ 9.0, Visual Excellence at 10, scored by the builder **and** an independent seat, with evidence. Below 9.0 is not ready. Scores may decrease.

---

*PART 7 completes the V1.0 contract. The full contract (§§1–29) is now expressed in three projections: HUMAN (plain words), AI (builder programming), MACHINE (spec as data) — see `HUB/PROJECT-INTELLIGENCE.HUMAN.md`, `.AI.md`, `.MACHINE.json` (PR #1276).*

---

*Verified against live main 2026-10-01 by Naya 4. PART 7 (contract §§14–29) added 2026-10-01 to complete the cut-off V1.0 contract — net-new content only; all existing sections unchanged.*
