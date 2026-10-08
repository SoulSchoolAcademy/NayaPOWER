# THE NAYA DESIGN CONTRACT V1

> **STATUS: CANDIDATE — pending Shawn's ratification.**
> This contract is a proposal, not law, until Shawn ratifies it. It distills 138 enforceable
> statements from three Phase-1 extractions into one mechanically enforceable design law.
> Nothing here ships as "done" until it is ratified and independently verified.

**North star mantra:** *"Black ground. White light. Purple soul."*

**Scope:** every NayaNET surface — entrance, hub, rooms, reports, and any future page.
If it renders for a human, this contract governs it.

---

## 0. HOW TO READ THIS CONTRACT

### 0.1 Normative language
- **MUST** = mandatory. **MUST NOT** = prohibited. **SHOULD** = preferred where no stronger rule applies. **MAY** = permitted.
- A law tagged **[RATIFIED]** traces to Shawn's effective briefing or his spoken word. A law tagged **[CANDIDATE]** traces to the Design Code V1 (unratified) and binds only after ratification.
- Where sources conflict, §11 lists the conflict verbatim and marks it **FOR RATIFICATION**. The checker enforces the resolution recorded there.

### 0.2 Source precedence (this is the law of interpretation)
1. **Shawn's direct spoken specs outrank everything.** His 24/18/14 type scale and his nine team colors for reports are ground truth.
2. **The AGENT BRIEFING — NayaNET Design Laws** (effective 2026-10-08, 15 laws + 10-item pre-ship checklist) is the authoritative builder briefing. Naya 2's session learnings restate it faithfully.
3. **The Design Code V1 is CANDIDATE** (unratified). Where it conflicts with shipped pages, this contract records BOTH and marks the conflict for ratification — it never silently picks.
4. **Shipped pages are evidence, not law.** index-2.html is the token ground truth (58 vars, matches the Code's hexes); start.html is the component ground truth for the Button Law and Intelligent-Block cards. The other seven pages are reference styling that approximates the tokens with literals.
5. Reader C's drift register (D1–D13): HARD drifts are contract violations to be repaired; each is recorded in §9 as a named violation with its fix.

### 0.3 Law inventory (what this contract contains)
| Source | Count | IDs |
|---|---|---|
| Agent briefing — 15 design laws | 15 | A-LAW-01 … A-LAW-15 |
| Agent briefing — pre-ship checklist | 10 | A-SHIP-01 … A-SHIP-10 |
| Design Code V1 §§0–13 | 105 | NC-0.1 … NC-13.2 |
| Drift repair laws (Reader C D1–D13) | 13 | D1 … D13 |
| **Total enforceable statements** | **143** | |
| Design tokens pinned | 47 | §2 tables |

---

## 1. BRAND IDENTITY & NORTH STAR

**DC-001 [RATIFIED].** NayaNET is the human interface to a living intelligence — not a dashboard, database, chatbot, or feature collection. (NC-0.1)

**DC-002 [RATIFIED].** One intelligence, many doors. One governed substrate, many views. One human at the center. (NC-0.2)

**DC-003 [RATIFIED].** Alive because the intelligence is alive — never because animation pretends. Every visual decision communicates meaning. Every state tells the truth. (NC-0.3, NC-0.4, NC-11.1)

**DC-004 [RATIFIED].** The north star in three words: **Black ground. White light. Purple soul.** Black dominates. White is the light (text, clarity, the white-hot core inside every jewel). Purple is the signature (accent and glow), never solid fill. (NC-2.1–2.4)

**DC-005 [RATIFIED].** The brand voice is warm invitation, never documentation. Copy is scored like design, out of 10, before shipping. Feature lists are 5/10; the bar is the 10/10 reference: *"Keep your people close — organize them, remember them, reach them."* If it reads like documentation, rewrite it. (A-LAW-08)

**DC-006 [RATIFIED].** The header is a front door: logo + living mark + warm voice + one clear line. An invitation, not a label. The top of the page MUST be its warmest part. Never a cold all-caps nameplate. (A-LAW-15)

**DC-007 [RATIFIED].** Headers get a VOICE: a real crafted typeface — **Cormorant** for warmth — carved with layered shadow (grounding + glow) and breathing luminosity. Flat placed text is lazy work. (A-LAW-07)

---

## 2. COLOR SYSTEM

### 2.1 The Trinity — one color, one job (never mix them)
**DC-010 [RATIFIED].** Color has exactly three jobs (A-LAW-04):
- **Chrome** (buttons, actions, active states, primary actions): purple edge, white text.
- **Text**: white, 99% of the time. Separation by SIZE, never color.
- **Theme** (per-item accents: per-contact, per-list, per-card): the spectrum in natural flow —
  **purple → blue → green → yellow → gold → orange → red → magenta** (→ purple, cycling).

**DC-011 [RATIFIED].** Never cross the jobs: **no theme color on chrome, no chrome color as flood.** (A-LAW-04)

**DC-012 [CANDIDATE].** Purple is accent and glow, **never solid fill**. Solid purple fills are a violation. (NC-2.4, NC-12.2)

**DC-013 [CANDIDATE].** Black is dominant: black first, black most — page, board, button. White is the light. Purple is the signature. (NC-2.2–2.4)

### 2.2 The Field — sovereign darkness
**DC-020 [RATIFIED/CANDIDATE].** The canvas is near-black, always. Everything luminous sits *in* darkness, never on light. **No light mode. No gray backgrounds. No exceptions.** (NC-1.1–1.3)

Field tokens:

| Token | Value | Job |
|---|---|---|
| `--bg` | `#0B0D12` | The world — default base canvas for rooms |
| `--bg` (entrance variant) | `#010103` | Live-entrance/marketing obsidian — both are valid; **CONTRACTOR DECISION:** `#0B0D12` is the room default, `#010103` the entrance variant *(pending Shawn)* |
| `--bg-raise` | `#12151D` | Cards, panels (raised surfaces) |
| `--bg-card` | `#171B25` | Popovers, modals — the topmost layer |
| `--edge` | `#252B39` | 1px precision edges on raised surfaces |
| `--ink` | `#F5F7FB` | Primary text. Always |
| `--muted` | `#AAB2BF` | Secondary text. **Never for primary content** |

### 2.3 The Spectrum — tokens, flow, and discipline
**DC-030 [RATIFIED].** Complementary colors serve the trinity, never compete with it. Always the richest, most beautiful **jewel** version of each color — **never pastel, never flat, never all at once.** (NC-2.5, NC-2.7)

Spectrum tokens:

| Token | Hex | Job |
|---|---|---|
| `--purple` | `#9d75ff` | Naya's signature. Primary actions, Naya presence. Accent/glow — never solid fill |
| `--indigo` | `#6675ff` | Reports room accent *(pinned from index-2 ground truth; CONTRACTOR DECISION pending Shawn)* |
| `--blue` | `#55b9ee` | Knowledge. Calm, deep, at rest |
| `--teal` | `#40d3bb` | Connection / flow |
| `--emerald` | `#55e39a` | Alive and well. Working, true, now |
| `--lime` | `#b8ee57` | Learning / growth |
| `--gold` | `#e8b64c` | Extraordinary. The rarest word — spend it sparingly |
| `--yellow` | `#f1d75a` | Spectrum flow member *(pinned from index-2; CONTRACTOR DECISION pending Shawn)* |
| `--orange` | `#ff9a5a` | Connections room accent *(pinned from index-2; CONTRACTOR DECISION pending Shawn)* |
| `--rich-orange` | `#ff7a3d` | Mail room accent *(pinned from index-2; CONTRACTOR DECISION pending Shawn)* |
| `--red` | `#ff5a6e` | Blocked / failed. The alarm. **Never decorative** |
| `--magenta` | `#d86cff` | Human significance. The human's own things |

**DC-031 [RATIFIED].** Canonical spectrum flow order (the universe's language): **purple → blue → green → yellow → gold → orange → red → magenta → purple…** — it cycles. **CONTRACTOR DECISION:** "green" = `--emerald` `#55e39a`, "yellow" = `--yellow` `#f1d75a` (pinned from index-2's ground-truth map) *(pending Shawn)*.

**DC-032 [RATIFIED].** White light at rest, own color on touch: every interactive element shows a VISIBLE white edge light when idle — borders **1.5px minimum**, bright enough to SEE the separation (Shawn's standing complaint: *"you can't see the separation. Fix it with light."*). On hover it ignites in its OWN spectrum color, not blanket purple. Purple is for chrome; themed elements burn their own color. (A-LAW-05)

> ⚖️ **CONFLICT FOR RATIFICATION (§11, X-1):** the Design Code V1 NC-5.3 specifies the primary-button
> rest state as `1px solid purple-65`. The ratified briefing demands 1.5px+ white edge light on every
> interactive element at rest. **Contractor recommendation:** the briefing governs (white 1.5px+ at rest;
> purple ignites on hover for chrome, own-color for themed) — the briefing is effective; the Code is candidate.

**DC-033 [CANDIDATE].** Amber and rose pink are forbidden everywhere. (NC-2.9, NC-12.3) *Grandfather note: the live entrance's amber/rose orbital jewels are existing decoration pending recolor; the law governs all new work.*

**DC-034 [RATIFIED].** Body text is white, 99% — never gray body text; it's unreadable. Hierarchy comes from size, never color. (A-LAW-07)

### 2.4 Room assignments — one distinct color per room, never two rooms alike
**DC-040 [CANDIDATE, pinned].** Room accent assignments (Code §2 as named; hexes pinned from index-2 ground truth where the Code gave names without hexes — **CONTRACTOR DECISION pending Shawn**):

| Room | Accent | Hex |
|---|---|---|
| Today | magenta | `#d86cff` |
| Reports | indigo | `#6675ff` |
| Library | blue | `#55b9ee` |
| Smart Doors | teal | `#40d3bb` |
| Ledger | gold | `#e8b64c` |
| Connections | orange | `#ff9a5a` |
| Lists | purple | `#9d75ff` |
| Mail | rich-orange | `#ff7a3d` |
| Spaces | lime | `#b8ee57` |
| Smart Grow | emerald | `#55e39a` — **CONTRACTOR DECISION:** the Code leaves the tenth color TBD; emerald is the only unassigned jewel color not reserved as the red alarm, and its "alive and well / growth" semantics fit the growth room *(pending Shawn)* |

**DC-041 [RATIFIED].** Subset-by-count rule for themed item sets (nav items, chips, lists): choose the subset that presents best for the count, **always in flow order** — 1 item → purple; 3 → purple, blue, green; 5 → magenta, purple, blue, green, yellow; 6 → magenta, purple, blue, green, gold, orange; more → continue the flow, it cycles. **CONTRACTOR DECISION:** the cycle start point is the presenter's choice (beauty first, NC-5.12); the machine rule is that the sequence is a circular subsequence of the canonical flow *(pending Shawn)*. (NC-5.10–5.12)

**DC-042 [RATIFIED].** Never all lit at once — the light travels. Nav/sidebar items are NOT purple buttons: at rest quiet (white/neutral text on obsidian); on hover each ignites in its own spectrum color; the active item stays lit in its color. (NC-5.8, NC-5.9)

### 2.5 Team colors
**DC-045.** Shawn's nine team colors for reports are referenced in his spoken spec as ground truth; the values were **not present in the three Phase-1 input files** — recorded here as **PENDING INPUT**, not invented. *(Contractor note to Shawn: supply the nine hexes; they will be pinned as `--team-1 … --team-9`.)*

---

## 3. TYPOGRAPHY

**DC-050 [RATIFIED].** Size separates, color doesn't. The scale is **24 / 18 / 14** — Shawn's spoken spec, confirmed in both sources. Mapping (**CONTRACTOR DECISION** reconciling the briefing's bare "24/18/14" with the learnings' "Kicker 24, headline 18, detail 14" and the Code's §3 — *pending Shawn*):

| Role | Size | Notes |
|---|---|---|
| Body | **18px. Always.** | The single most-violated rule — 11–16px found in the wild. Enforced hard. |
| Kicker / big headline | 24px | Monumental brand voice: weight 700–950, letterspaced, uppercase for kickers and mottos |
| Headline | 18px | |
| Sub-headline / detail | 14px | |

**DC-051 [CANDIDATE].** Presentation variant (voice readout, Getting Started, Intelligent Blocks): **24px headline / 18px sub / 14px body.** The ONLY sanctioned context where body is not 18px. Intelligent Blocks layers: 1) *In a nutshell* (24px, 1–2 lines) → 2) *What it means* (18px) → 3) *How to use it* (14px) → 4) *What's in it for you* (14px). (NC-3.5, NC-8.1)

**DC-052 [RATIFIED].** Font: **Inter / system stack for UI.** Display serif **Cormorant Garamond** permitted for editorial surfaces (reports, voice) only. **CONTRACTOR DECISION:** the Apple SF Pro stack counts as "system stack" under the Code's "Inter/system stack" wording — cosmetic, no rebuild required *(pending Shawn)*. (NC-3.8, NC-3.9, D13)

**DC-053 [RATIFIED].** Brand voice is monumental — weight 700–950, letterspaced, uppercase for kickers and mottos — but never shouty; carved, not written. (NC-3.6, NC-3.7)

**DC-054 [CANDIDATE].** Minimum touch target: **44px**. (NC-3.10, NC-10.1)

---

## 4. LAYOUT & SURFACES

### 4.1 Layout is meaning
**DC-060 [RATIFIED].** The UX metaphor is a decision, not a decoration. A grid says "browse products." A vertical stack says "these are your people." Ask *"what is this?"* before *"how do I lay it out?"* Contacts scroll vertically. Never default to grids. (A-LAW-03)

**DC-061 [RATIFIED].** Full width. No max-width caps on the chassis or rooms — content owns the width. The Naya logo lives **top-left, always**. If a region sits empty and black, the layout is wrong — fix the layout, don't decorate the void. No sidebars of black nothing. (A-LAW-12, NC-6.14)

**DC-062 [RATIFIED].** One canonical Hub shell. Rooms plug into it; they don't rebuild it. Shared bottom nav on every room (mobile-first). No duplicated navigation. The rooms (+) button is mobile-only. (NC-9.1–9.4)

**DC-063 [CANDIDATE].** The Hub is output-only: **no capture buttons, command surfaces, or agent invocation in Hub chrome.** (NC-9.5, NC-12.9)

### 4.2 Elevation & the depth formula
**DC-064 [CANDIDATE].** Nothing is flat. Ever. Every surface sits at an elevation and the eye must read the depth. (NC-6.1, NC-6.2)

| Level | Name | Treatment |
|---|---|---|
| L0 | The field | Obsidian ground. No shadow; everything rises from it |
| L1 | Boards | Cards, panels, step blocks. Deep drop shadow + 1px top inner highlight |
| L2 | Boards within boards | Inner panels, nested wells. Deeper shadow — the sense of going *into* the page |
| L3 | Controls | Buttons, inputs, jewels. The topmost layer — they float, they invite touch |
| L4 | Overlays | Modals and drawers. Above everything, dimming what sits below *(source duplication "drawers, drawers" recorded as editorial typo)* |

**DC-065 [CANDIDATE].** The depth formula on every surface: **outer glow in its theme color + `inset 0 1px #fff6` top light + deep drop shadow.** Light comes from within. Each level: stronger shadow below, stronger highlight above. **CONTRACTOR DECISION** (pinned from index-2/start ground truth, *pending Shawn*): L1 drop = `0 18px 42px rgba(0,0,0,.73)` (`--depth-drop`), L2 drop = `0 20px 48px rgba(0,0,0,.87)` (`--depth-deep`), top inner light = `inset 0 1px #fff6` (`--depth-hi`). (NC-6.4–6.9)

**DC-066 [CANDIDATE].** Living surfaces: hover lifts (translate up 1px, glow intensifies, border warms toward the theme color). Press sinks. Focus glows. Cards ignite on hover. Every interactive element *responds* — the interface feels alive because it answers touch, not because of decoration. (NC-6.10–6.13)

---

## 5. COMPONENTS & ELEMENTS

### 5.1 The Jewel — the signature mark
**DC-070 [CANDIDATE].** The white-hot diamond is the single most distinctive NayaNET mark. Construction: **faceted diamond silhouette** (exact clip-path below) → white-hot radial core → jewel-color aura. Bullets in Intelligent Blocks use the reports-tab jewel icons. (NC-4.1–4.3, NC-4.5, NC-8.2)

- `--jewel-clip`: `polygon(50% 0%, 86% 28%, 74% 82%, 50% 100%, 26% 82%, 14% 28%)` — exact.
- `--jewel-glow`: `0 0 2px rgba(255,255,255,.85), 0 0 5px <jewel>, 0 0 10px <jewel>, 0 0 16px <jewel>` — **CONTRACTOR RECONSTRUCTION** of the garbled source tail (`…16px 42`), where `<jewel>` is the jewel's own theme color *(pending Shawn; source verbatim preserved in §10)*. (NC-4.4)

**DC-071 [CANDIDATE].** Never "cheap circular Christmas-light styling" — precision-cut gemstones only. (NC-4.6)

### 5.2 Buttons — black heart, white voice, visible skin
**DC-072 [RATIFIED].** Button center: really black **`#050505`**. Text: **always white, with an icon** — colored text on buttons: **never. Ever.** Border: white, visible at rest (**1.5px+**, not hairline — see conflict X-1). Elevated: inset top highlight + deep drop shadow — it must feel liftable. Hover: purple edge + purple glow for chrome; own-color for themed. (A-LAW-06)

**DC-073 [CANDIDATE].** Primary-button construction (start.html is the ground-truth instance): black fill; **pill radius 999px**; **minimum height 52–55px**; rest state `1px solid purple-65` + `0 0 22px purple-35` + `inset 0 1px #fff2` (**CONTRACTOR DECISION:** purple-65/35 = `color-mix(in srgb, #9d75ff 65%/35%, #000)`/transparent, *pending Shawn*; but see conflict X-1 — the briefing's 1.5px white edge governs until ratified); hover: glow intensifies, lifts 1px (`translateY(-1px)`); active: presses 1px. **Real elements — never clickable divs.** One button = purple. Always. (NC-5.1–5.7)

**DC-074 [RATIFIED].** Affordances tell the truth: every glyph is a promise. **+ for add, ✉ for mail, › only when it navigates.** No decorative arrows, no lying glyphs. (A-LAW-14)

**DC-075 [RATIFIED].** Icons are drawn, not shrunk: a photo render at 58px is mud. A real icon is vector geometry — bold, simple, luminous, **readable at 16px**. If you can't make it good, leave it out. New marks must speak the page's native language (e.g. the avatar sheen), not imported decoration. The black orb with orbiting light works because it is NATIVE — that orb **is the header's "living mark"** (**CONTRACTOR DECISION** *pending Shawn*). (A-LAW-09)

### 5.3 Shared chrome & components
**DC-076 [CANDIDATE].** `eco-bottombar` — shared bottom nav on every room: `position:fixed; bottom:0;` `padding:14px 20px calc(14px + env(safe-area-inset-bottom))`; gradient `transparent → rgba(5,5,8,.92) 30%`; `backdrop-filter:blur(12px)`; `border-top:1px solid rgba(255,255,255,.08)`; 46px circle buttons, `radial-gradient(circle at 35% 30%, #2a2a32, #0a0a0e 70%)`, `border:1px solid rgba(255,255,255,.3)`. *(Currently only on mail, reports, spaces, ledger — D10: roll out to all rooms.)*

**DC-077 [EVIDENCE].** Component inventory (observed across the 9 pages; all obey the depth formula):
- **Chips** — pill, uppercase micro-type, per-state color (filter chips, status chips, LIVE/COMING SOON/UNKNOWN state chips).
- **Toasts** — fixed bottom-center above the bottombar (~88px), spring entrance.
- **Drawers/modals** — overlay layer, dimming below (composer, door detail, heartbeat modal, notes modal).
- **Cards/boards** — Level-1 elevation; hover lifts and ignites.
- **Search** — obsidian input well, icon prefix, over lists.
- **Progress rail** (start.html) — dots + connecting bars; done = black.
- **naya-brand** — jewel/wordmark lockup.

**DC-078 [RATIFIED].** One system, not two: never build a second version of something that exists. Notes about people live in Connections; messages live in Smart Mail; one tap jumps between them. Anything that exists elsewhere is a **link, not a copy**. (A-LAW-11, NC-12.10)

---

## 6. MOTION

**DC-080 [RATIFIED].** Maximum life, minimum noise. The page breathes: ambient light drifts, cards pulse their edge light, avatars sheen, text glows, the orb's light orbits. Every animation slow, subtle, purposeful. Nothing may distract from reading. Restraint is the craft. (A-LAW-10)

**DC-081 [RATIFIED].** Enforceable timing (briefing): **4–7s ease-in-out loops, low opacity.** **CONTRACTOR DECISION:** "low opacity" = ambient overlay opacity **≤ 0.25** *(pending Shawn)*. (A-LAW-10)

> ⚖️ **CONFLICT FOR RATIFICATION (§11, X-2):** the Design Code V1 specifies ambient motion as **8s breathing / 78s orbital drift** (NC-7.2) vs the briefing's **4–7s loops**. The machine checker accepts **4s–78s** for ambient infinite loops until Shawn rules.

**DC-082 [CANDIDATE].** The easing: `u--ease: cubic-bezier(.16,.84,.22,1)`; interaction durations fast `.18s` / med `.28s` / slow `.5s`. Micro-interactions are the craft — hover, glow, lift, ignite; do the elevated thing when it serves beauty and function, never the basic thing when the elevated thing is possible. (NC-7.1, NC-7.5)

**DC-083 [CANDIDATE].** Every animation is a truth claim: never animate intelligence that didn't happen; never hide intelligence that did. (NC-7.4)

**DC-084 [CANDIDATE].** `prefers-reduced-motion: reduce` kills all animation. Always. A page that fails accessibility fails the Code, however beautiful. (NC-7.7, NC-10.6)

---

## 7. PAGE LOGIC — WHAT EACH SMART APP IS FOR

**DC-090 [EVIDENCE/RATIFIED].** Each room has one job. The layout metaphor follows the job (§4.1).

| Page | Job | Room accent | Signature components |
|---|---|---|---|
| **Entrance** (index) | Front door / landing: brand immersion → credential entry → launch the hub. Marketing + gate, not workspace. Hosts Auto-Login, ABOUT US, WHITE PAPER, POWERCASTS. | Purple soul (brand) | Orbital jewel field (Code-exact diamond clip-path), Enter CTA, listening field |
| **Hub** (index-2) | The canonical application shell — home screen all rooms plug into. Personalized greeting, hero time, quote strip, room grid (one tile per room, each lit in its spectrum accent), activity cards, intelligence lists, drawers. | All — `--room-accent` per room (24 runtime assignments) | Room tiles, activity cards, intel rows, boards (L1→L2 nesting), search, toasts |
| **Smart Mail** (mail) | Email client room: triage and act on mail with intelligence layered in. Folders INBOX/UNREAD/SENT/SCHEDULED/SMART POSTS/DRAFTS. | **rich-orange `#ff7a3d`** *(D2 repair)* | Folder rail, thread list + filter chips, reading pane, bulk action bar, ELITE COMPOSER modal, smart scheduler tabs, mic ring, toasts |
| **Reports** (reports) | Daily intelligence report viewer: parses report markdown into a browsable day/week presentation. Home of the Intelligent Blocks presentation contract. | **indigo `#6675ff`** *(D5 repair)* | Week strip + day tiles (spectrum-flow over time), day board with jewel bullets, thread links, rooms menu drawers |
| **Spaces** (spaces) | Community/space browser + Smart Tabs: discover and enter Spaces; per-space detail (posts · members · chat · about). | **lime `#b8ee57`** *(D3 repair)* | Space cards, Smart Tabs v9, invited strip, schedule picker |
| **Smart Doors** (connect) | The "Doors" room: connect NayaPOWER to the outside world (DOOR-GITHUB/MCP/AI/DATA/SDK), each with LIVE/COMING SOON/UNKNOWN state. | **teal `#40d3bb`** | Door boards + state chips, explain blocks, per-door drawers |
| **Connections** (connections) | People + lists + notes manager: browse connection cards, filter, detail modal with NOTES ABOUT {name}, SAVE TO LIST. | **orange `#ff9a5a`** *(D4 repair)* | Connection cards (initials avatar, name, role), filter chips, notes modal |
| **Ledger** (ledger) | The intelligence ledger / audit stream: the heartbeat as filterable receipts and evaluations (CANDIDATE→RATIFIED→RECORDED→EVALUATED→PASS/NON-PASS/NOT RUN/UNKNOWN; EFFECTS OBSERVED, VERIFIED, VALUED). | **gold `#e8b64c`** *(D6 repair)* | Status chips, source jewels row, stream rows (chip + node tag + title + time), HEARTBEAT MODAL |
| **Start** (start) | Onboarding stepper / Getting Started: 4 steps, each an Intelligent Block in card form (num, headline, nutshell, detail, action, done-mark). The first Code-native page. | Per-step theme color | Step cards, progress rail, ambient layer, privacy card, finale CTA |

**DC-091 [RATIFIED].** Truth in states: "Live" means live. "Coming soon" means not yet. **Never fake a connection, a count, or a heartbeat.** Demo data is labeled demo. Simulated activity is labeled simulated. Counts and events come from real canonical outcomes, or they don't appear. (NC-11.1–11.3)

---

## 8. PROHIBITIONS MASTER LIST

Every "never" from both sources, unified. Each is machine-checked where marked **[CHECK]**.

### From the ratified briefing (A-LAW)
1. Never score from code — score the rendered, lived page. (A-LAW-01)
2. Never ship below personal 9+ with stated specifics. (A-LAW-02)
3. Never default to grids — pick the metaphor the thing IS. (A-LAW-03)
4. Never theme color on chrome. (A-LAW-04)
5. Never chrome color as flood. (A-LAW-04)
6. Never hairline faint borders — minimum 1.5px white edge light, bright enough to SEE. (A-LAW-05) **[CHECK: edge-light]**
7. Never colored text on buttons — EVER. (A-LAW-06) **[CHECK]**
8. Never gray body text. (A-LAW-07) **[CHECK]**
9. Never 11px gray kickers. (A-LAW-07) **[CHECK: type floor]**
10. Never ship feature lists as invitations — score copy /10 first. (A-LAW-08)
11. Never a bad icon rather than none — if you can't make it good, leave it out. (A-LAW-09)
12. Never anything that distracts from reading. (A-LAW-10)
13. Never build a second version of something that exists. (A-LAW-11) **[CHECK: duplicate-system scan]**
14. Never max-width caps on chassis/rooms; never sidebars of black nothing. (A-LAW-12) **[CHECK]**
15. Never claim without verifying — "it's done" from memory. Grep the artifact. (A-LAW-13)
16. Never decorative arrows / glyphs that lie. (A-LAW-14)
17. Never a cold all-caps nameplate header. (A-LAW-15)
18. Never separate text hierarchy by color instead of size. (A-LAW-04/07)
19. Never ship an unbacked score — below 9: back to the bench, no exceptions. (A-SHIP)
20. Never flatten: flat placed text is lazy work. (A-LAW-07)

### From the Design Code V1 (CANDIDATE — binds on ratification)
21. Body text under 18px. (NC-12.1) **[CHECK]**
22. Solid purple fills — purple is glow, not paint. (NC-12.2) **[CHECK]**
23. Amber or rose pink anywhere. (NC-12.3) **[CHECK]**
24. `user-scalable=no` — never block pinch zoom. (NC-12.4) **[CHECK]**
25. Clickable divs instead of buttons. (NC-12.5) **[CHECK]**
26. Max-width caps on chassis/rooms. (NC-12.6) **[CHECK]**
27. Links to app.nayanet.technology (the old MAXIS app). (NC-12.7) **[CHECK]**
28. Fake liveness — unlabeled demo data, simulated counts presented as real. (NC-12.8)
29. Capture/command surfaces in Hub chrome. (NC-12.9) **[CHECK]**
30. A second mechanism for one decision — no duplicate systems. (NC-12.10)

### Field laws restated as prohibitions
31. No light mode. No gray backgrounds. No exceptions. (NC-1.3) **[CHECK: light backgrounds]**
32. No non-token chromatic colors outside the spectrum. (DC-030) **[CHECK]**
33. No red used decoratively — the alarm only. (NC-2.5/DC-030)
34. No two rooms alike — one distinct accent per room. (NC-2.8) **[CHECK: D2–D6]**
35. No pastel, no flat, no all-at-once. (NC-2.7)
36. No animation that distracts; no animation without `prefers-reduced-motion` handling. (NC-7.6/7.7) **[CHECK]**

---

## 9. DRIFT REPAIR REGISTER — D1–D13

Each drift is a named violation with its fix. HARD drifts are contract violations; the checker fails them.

| # | Page | Violation | Fix | Severity |
|---|---|---|---|---|
| **D1** | index.html | `user-scalable=no` + `maximum-scale=1` in viewport meta — the Code's forbidden list (NC-12.4) | Remove both; viewport MUST allow pinch zoom | **HARD** — checker FAIL |
| **D2** | mail.html | Room accent `#3ca8ff` (blue) | Recolor to Mail's assigned **rich-orange `#ff7a3d`** (index-2's `--accent-mail` agrees with the Code) | **HARD** — checker FAIL |
| **D3** | spaces.html | Room accent `#7c3aed` (purple) — reads as a second purple room | Recolor to Spaces' assigned **lime `#b8ee57`** | **HARD** — checker FAIL |
| **D4** | connections.html | Room accent `#9d75ff` (signature purple) — purple is Naya presence/actions, not a room | Recolor to Connections' assigned **orange `#ff9a5a`** | **HARD** — checker FAIL |
| D5 | reports.html | Room accent `#8a5cff` (violet) | Correct to Reports' assigned **indigo `#6675ff`** — close family, wrong hex | MEDIUM — checker FAIL (non-token chromatic) |
| D6 | ledger.html | Accent gold `#f2c94c` | Correct to Ledger's assigned **gold `#e8b64c`** — near-miss, not exact | MEDIUM — checker FAIL (non-token chromatic) |
| D7 | connect.html | Accent `#40d3bb` is the Code's teal value but named `--cn-emerald` | Rename to `--cn-teal` (value already correct) | LOW — naming repair |
| D8 | index-2.html | Jewel clip-path near-variant (`88%/12%` vs Code `86%/14%`); `--fs-body:16px` vs 18px law | Snap clip-path to Code-exact polygon; body to 18px | LOW + MEDIUM — checker warn/FAIL |
| **D9** | all pages | Body type law "18px. Always." violated systemically: start 14px (sanctioned — presentation variant), index-2 16px, mail 15px, six pages declare nothing (browser default 16px) | Declare explicit 18px body everywhere; presentation-variant pages keep 14px ONLY with the sanctioned variant markers | **HARD** — checker FAIL |
| D10 | connect, connections, index-2, index, start | `eco-bottombar` shared bottom nav missing (Code §9: every room) | Roll the shared chrome out to all rooms | MEDIUM — checker warn |
| D11 | spaces, mail | Button law: only start.html's `.btn` implements black-fill/purple-glow/pill/52px; spaces `.sn-btn` = 12px ghosts, mail `.primary` = blue-bordered | Rebuild primaries to DC-072/073 | MEDIUM — checker FAIL on solid fills / colored button text |
| D12 | 7 of 9 pages | Token discipline: only index-2 (58 vars) and start (22 vars) use real `:root` systems; the rest use prefixed vars + hundreds of hardcoded literals | Adopt the canonical `:root` token system (index-2's map) | MEDIUM — checker warn |
| D13 | mail, spaces, connect, connections, ledger, reports | Font: SF Pro stack vs Code's "Inter/system stack" | **CONTRACTOR DECISION:** SF Pro counts as system stack — no rebuild *(pending Shawn)* | LOW — recorded |

---

## 10. AMBIGUITY RESOLUTIONS — CONTRACTOR DECISIONS

Each decision states the chosen value, why, and its status. **All CONTRACTOR DECISIONs are pending Shawn's ratification** unless marked [SOURCE-GROUNDED].

| # | Ambiguity | Decision | Why |
|---|---|---|---|
| CD-1 | Type-scale mapping (briefing says only "24/18/14"; learnings map Kicker 24/headline 18/detail 14) | Body 18 / kicker-big-headline 24 / headline 18 / sub-detail 14; presentation variant 24/18/14 | The three sources agree once "kicker" = the monumental big-headline voice (NC-3.6) |
| CD-2 | "Low opacity" has no number (A-5) | Ambient overlay opacity ≤ 0.25 | Typical ambient layers in the shipped set sit at 0.05–0.25 |
| CD-3 | "Living mark" undefined (A-4) | = the black orb with orbiting light (K5's native mark) | The only concrete living mark in evidence; it speaks the page's native language |
| CD-4 | "Green"/"yellow" in spectrum flow have no hex (B/A-2) | green = `--emerald` `#55e39a`; yellow = `#f1d75a` | index-2's ground-truth map defines `--green:#55e39a`, `--yellow:#f1d75a` |
| CD-5 | Room accents "indigo"/"orange"/"rich-orange" have no hex (B/A-3) | indigo `#6675ff`; orange `#ff9a5a`; rich-orange `#ff7a3d` | index-2's `--accent-*` map, which agrees with the Code's assignments |
| CD-6 | Smart Grow's tenth color TBD (B/A-4) | emerald `#55e39a` | Only unassigned jewel color not reserved as the red alarm; "alive and well / growth" fits the growth room; satisfies NC-2.8 |
| CD-7 | purple-65/purple-35 undefined (B/A-5) | `color-mix(in srgb, #9d75ff 65%, #000)` / `color-mix(in srgb, #9d75ff 35%, transparent)` | The only reading consistent with "65/35" naming |
| CD-8 | "Deep drop shadow" has no numbers (B/A-6) | L1: `0 18px 42px rgba(0,0,0,.73)`; L2: `0 20px 48px rgba(0,0,0,.87)` | index-2/start `--depth-drop`/`--depth-deep` ground truth |
| CD-9 | Nav subset start-point conflict (B/A-7) | Start point is the presenter's choice (beauty first); machine rule = circular subsequence of the canonical flow | NC-5.12 explicitly grants the presenter the choice |
| CD-10 | "Never all at once" vs cycle rule (B/A-8) | Cycle rule governs; ≥7 items may span the full spectrum; never all as solid fills | NC-5.11's "More → continue the flow" is the more specific rule |
| CD-11 | `16px 42` garbled jewel glow (B/A-1) | `0 0 2px rgba(255,255,255,.85), 0 0 5px <jewel>, 0 0 10px <jewel>, 0 0 16px <jewel>` | Terms 2–3 lack colors in the source; the jewel's own theme color is the only coherent reading |
| CD-12 | `--bg` double value `#0B0D12` vs `#010103` (B/A-11) | `#0B0D12` = room default; `#010103` = entrance/marketing variant | The Code blesses both; the pages show the usage split |
| CD-13 | SF Pro vs Inter (D13) | SF Pro counts as "system stack" | The Code's wording is "Inter/system stack" — SF is Apple's system stack |
| CD-14 | Shawn's nine team colors (precedence rule) | **PENDING INPUT — not invented** | Referenced in the task's precedence rules but absent from all three inputs |

**[SOURCE-GROUNDED] (no invention):** "black pill" → pill = `border-radius:999px` (NC-5.2); border rule = 1.5px minimum + visible-separation test (both stated); pre-ship checklist binds (A-only, no contradiction); "modals, drawers, drawers" → editorial typo, contract reads "modals and drawers."

---

## 11. CONFLICTS FOR RATIFICATION

Recorded verbatim per precedence rule 2 — the contract does not silently pick. The checker enforces the **contractor recommendation** until Shawn rules.

**X-1 — Button rest edge: white 1.5px+ vs purple 1px.**
- Briefing (effective, A-LAW-05/06): every interactive element shows a VISIBLE white edge light at rest, borders 1.5px+.
- Code V1 (candidate, NC-5.3): primary button rest = `1px solid purple-65`.
- **Contractor recommendation:** the briefing governs — white 1.5px+ at rest; chrome ignites purple on hover, themed ignites own color. (Briefing is effective law; the Code is candidate.)

**X-2 — Ambient loop timing: 4–7s vs 8s/78s.**
- Briefing (effective, A-LAW-10): 4–7s ease-in-out loops, low opacity.
- Code V1 (candidate, NC-7.2): 8s breathing, 78s orbital drift.
- **Contractor recommendation:** accept the union band **4s–78s** for ambient infinite loops until Shawn rules.

**X-3 — Shipped pages vs Code V1 generally.** Where any page disagrees with the candidate Code, this contract records both (see §9). Ratification decides; until then the briefing + shipped ground truths (index-2 tokens, start.html button) govern.

---

## 12. MACHINE ENFORCEMENT MAP

`tools/design_law/check_design.py` enforces these laws today (exit 1 on violation):

| Check ID | Laws | What it fails |
|---|---|---|
| D1 | NC-12.4, NC-10.3 | `user-scalable=no` or `maximum-scale≤1` in viewport |
| D2/D3/D4 | NC-2.8, DC-040 | Wrong room accent for mail/spaces/connections; missing expected accent |
| D9 | NC-3.1, NC-12.1, DC-050 | Body font-size missing or < 18px (presentation variant exempt) |
| SPECTRUM | DC-030, NC-2.7 | Chromatic hex outside the token set |
| LIGHTBG | NC-1.3 | Light backgrounds (luminance ≥ 0.55) |
| BTN | A-LAW-06, NC-5.1, NC-12.2 | Colored text on buttons; solid non-black fills |
| ZOOM | (same as D1) | — |
| DIVBTN | NC-12.5 | Clickable divs (`onclick` on div) |
| MAXW | NC-6.14, NC-12.6 | max-width caps on chassis/room selectors |
| MAXIS | NC-12.7 | Links to app.nayanet.technology |
| AMBERROSE | NC-12.3, NC-2.9 | Amber/rose-pink chromatic colors |
| RM | NC-7.7 | Animations without `prefers-reduced-motion` handling |
| BODYCOLOR | A-LAW-07, DC-034 | Non-white body text color |
| PURPLEFILL | NC-12.2 | Solid purple fills |

Warnings (do not fail): jewel clip-path drift (D8), missing eco-bottombar (D10), thin token system (D12).

---

*End of THE NAYA DESIGN CONTRACT V1 — CANDIDATE pending Shawn's ratification.*
*Next: ratification → repairs D1–D9 land on the pages → checker runs in CI → the contract hardens to law.*
