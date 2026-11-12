# THE OFFICIAL NAYA DESIGN INVENTORY

**OFFICIAL — ratified by Shawn Vibert, 2026-11-12 16:39:37Z, by his tap 'Yes — stamp it official.'** This inventory is for the Nayas, not for him — it belongs in Project Intelligence, the Smart Factory, the Smart Hub, and the Smart Box, one system, so the machine can design and build itself. It is a harvest-only unification of the design sources that already exist, written so any Naya can build from it without looking around. One part of what it carries is already LAW — the Intelligent Block Rules (§1.3, §2 element 03) were ratified by Shawn's "1000% YES!" on 2026-11-06. The Clarity Confirmation Act it is built on remains DRAFT.

- **Compiled:** 2026-11-12, design-inventory seat (Team Nitro).
- **Branch:** `design/inventory-20261112` · **File:** `BRAIN/10-INTERFACES/THE-OFFICIAL-NAYA-DESIGN-INVENTORY.md`.
- **Local twin:** `~/workspace/team-nitro/design-inventory-20261112/THE-OFFICIAL-NAYA-DESIGN-INVENTORY.md` (byte-identical to the filing).
- **Verification date:** 2026-11-12 ~16:2xZ (live URLs curled, files test-`f`'d, GitHub read-back done — see §7 and §11).

---

## 0. WHAT THIS DOCUMENT IS — AND THE ONE SYSTEM IT SERVES

Shawn's order, 2026-11-12 16:12Z (his words, operative parts): the Smart Factory, Project Intelligence, and the Smart Hub must become **one ultimate system** — the Factory is the store, PI is the record, the Hub is the eyes. The Factory holds everything aligned — all the design pieces, elements, design contracts, examples, the inventory — so any Naya can get in there and build and have all the pieces and not look all around. "Just make it official and put everything there — design contracts, examples, inventory, the whole of everything." And: do the most intelligent thing, not necessarily literally merging code, but the right way to make them one system in sync.

**This document IS the Factory's official inventory.** It lives in the Factory as the store's canonical list, carrying the design contracts, the examples, and the full inventory. It does not merge the Factory, PI, and the Hub into one codebase — that was never the order. It makes them one system in the way that matters: one record of what exists, one language, one place to look.

- **The Factory is the STORE.** It holds the pieces (the 22 signature pieces, the 6 page templates, the Smart Box template) and this inventory is its canonical list. Working Factory: `~/workspace/smart-factory/`. Repo catalog: `BRAIN/10-INTERFACES/DESIGN-BLOCKS/signature-pieces/`.
- **Project Intelligence is the RECORD.** It is internal-only — for us, not for the public — but its presentation (colour language, elevation, flow of colours) is adopted for public pages. PI's Live Wall board language is carried in §4 so public pages can speak it.
- **The Smart Hub is the EYES.** The citizen's operating center — today, projects, people, journal on one timeline, in one place. The Hub's feed boards are the living example of element 03 (the intelligent block).

### How to use this document (any Naya)

1. **Start at the laws (§1).** The 11 shared laws run through every object. Learn them before touching a piece.
2. **Find the element (§2).** Each of the 22 carries: what it is, what it looks like, what it feels like, what it does, its laws, its CHECK, **what situation to use it in**, a **live example URL**, and the **code-grab path** — the exact file to take the code from.
3. **Take the code verbatim.** Grab the piece from the Factory signature piece or the harvested source. Never restyle it, never rebuild it. If no piece exists for the job, that is a GAP (§9) — file it, don't invent it.
4. **Compose, don't create.** Pages are assembled from inventoried elite pieces — real HTML, real CSS, verbatim — never hand-invented private styles. A private colour or a private style is an automatic fail.
5. **Prove it (§8).** The seconds test, the click test, independent scoring. A lesson counts only when a future decision changes because of it.

### The grab-code permission (Shawn's word, 2026-11-12 15:59Z)

Every agent has permission to **literally grab the code from any page or the Smart Factory and use it**. Nobody reinvents or restarts; take the best of the best and make one better ONLY if it is extraordinary. Nobody designs their own without understanding the language — that is how you get flat buttons, dead boards, and tons of text where it should be mostly visuals and icons. The pricing page is one of our best pages for presentation: study it first.

### What this document is NOT

- It is not a redesign. Nothing in it restyles a page or rebuilds a template. It names what already exists.
- It is not a merge of the Factory, PI, and the Hub into one codebase. The convergence is by record and language, not by collapsing the systems.
- It does not resolve conflicts or fill gaps. Conflicts are reported (§10), gaps are named (§9), both awaiting Shawn's eye.
- It does not make the Act official. The Act is DRAFT until Shawn stamps it; this inventory is OFFICIAL by his tap of 2026-11-12 16:39:37Z.

---

## 1. THE LAWS THAT GOVERN EVERYTHING

One set of laws runs through every object — buttons, boards, intelligent blocks, icons, smart apps, pages, sections, gauges, all of it. The same elevation, the same one light, the same real shadow, the same own-color light, the same real-object language. A button and a gauge and a board are the same laws wearing different shapes. No law is restated per element in §2; each element says only how it follows these.

### 1.1 The Real Object Law — seven principles (canonical 2026-11-01, all of NayaNET, forever)

1. **Everything is an object.** Not a flat shape with effects. Not a diagram. A thing you could reach out and touch. If it doesn't look touchable, it doesn't ship.
2. **One light source (top-left).** The entire system is lit from top-left, like a studio. Every gradient runs 135°. Every shadow falls down-right. Every highlight sits on the upper edge.
3. **Real materials.** Obsidian glass (`#0a0a0f` → `#1a1a20`, never pure black, never grayish), brushed metal, engraved gold, light with volume. Never neon, never pink glow.
4. **Real shadows.** Objects sit ON the page. They cast soft shadows down-right. No shadow = floating = fake. Depth is mass, not glow; glow is light.
5. **Touch = physical response.** It depresses slightly (scale 0.97, 0.1s), the light shifts across its surface, it rises on hover (`translateY(-2px)`), presses in on active (`translateY(1px)`).
6. **Speak in objects.** Icons, circles, boards, buttons — minimal text.
7. **Viewport is the stage.** (SN-0858.)

Source: `~/workspace/team-nitro/laws/THE-REAL-OBJECT-LAW.md`. Full law there.

### 1.2 The Playbook's five truths (Grade 6, locked 2026-11-02, SN-0844)

1. **Every position is calculated by formula. Never eyeballed.** 8px grid for linear layouts; text sizes 12 / 14 / 16 / 20 / 28 / 48 (never 13px, never 27px).
2. **Every element is a physical object with material, weight, and a light source.** Top-left light, 135° gradients, shadows down-right, highlights on the upper edge.
3. **Movement means the machine is working.** If it's not working, it doesn't move. Ambient 60–180s, active 18–25s, never faster than 12s. Nothing bounces. Nothing pulses for effect. If you can't say what the moving part DOES in one sentence, delete the animation.
4. **The whole system speaks one language.** Every component is family.
5. **Shawn's eye overrides everything.** Including this document.

Source: `~/workspace/team-nitro/THE-PLAYBOOK.md`.

### 1.3 The eleven shared laws (Intelligent Block Rules, LAW — ratified 2026-11-06 by Shawn's "1000% YES!")

- **L1** Every element is a real physical object. **L2** One light source, top-left, always. **L3** Real shadows and real elevation — depth is mass, not glow. **L4** Own-color light — color is identity, and it ignites on touch. **L5** White text, never colored, never gray — and text never lights up. **L6** Touch is physical — it moves, it yields, it opens. **L7** The spectrum is the order things sit in. **L8** Every position is calculated by formula — never eyeballed. **L9** Movement means the machine is working — slow, and it means something. **L10** One language — every component is family. **L11** Shawn's eye wins — his verdict is the final compile.

Source: `~/workspace/team-nitro/hub-board-edit/intelligent-block-rules-LAW-20261106.md` (GitHub `BRAIN/10-INTERFACES/INTELLIGENT-BLOCK-RULES-LAW-20261106.md`). The companion file remains the full detail; §2 element 03 carries its block rules in substance.

### 1.4 The capstone (Shawn's words, 2026-11-06 00:14Z — the standard every object is judged against)

> "The whole thing must be a live living object, all the way through, layered on layers upon layers — because that gives the dimensional feel, the multi-dimensional in and out, the 3D real physical object effect."

Is it alive, is it layered, does it feel dimensional and real? If any answer is no, the object is not done — no matter how many rules it follows.

### 1.5 The spectrum — colour is grammar, not paint

The spectrum, in order (Anatomy + Playbook): **purple → blue → green → gold → orange → red → magenta**. Never the same color twice in a row — each section owns the NEXT color, so you feel yourself moving through the page. Adjacent things never share a hue. Chrome acts, text speaks, theme identifies. Depth before colour. Size separates; colour never does.

**Canonical tokens (live on the pricing page, read 2026-11-12):**

| Token | Hex (live) | Its job |
|---|---|---|
| Obsidian | `#050507` | The ground. Black is the soul; everything lit is lit against it. |
| Magenta | `#e84fff` | Leads the spectrum — richest first. |
| Purple | `#a06bff` | Naya's chrome — her presence, the house colour. |
| Blue | `#3fb8ff` | Stated — a claim, a declaration, information. |
| Green | `#2fe89e` | Proven — verified, working, live. |
| Gold | `#ffbf3d` | Shown value — earned, never applied as decoration. |
| Orange | `#ff9a5a` | Action / creations. |
| Red | `#ff5e6c` | Warning and exclusion — the ✕ in the ledger. |
| White | `#ffffff` | All text, and every control at rest. |

**Conflict, recorded not resolved:** the same hue names carry different hexes across sources (Act CONFLICTS #1; companion C1). Purple `#a06bff` (Anatomy/Playbook/wheel) vs `#9d75ff` (Hub variables) vs `#8a5cff` (jewel map); magenta `#e84fff` vs `#d86cff` vs `#ed42c4`; emerald/green `#2fe89e` / `#35e0a1` vs `#55e39a` vs `#2e9e6a`; gold `#ffbf3d` vs `#e8b64c` vs `#e8c766` vs `#d4a017`. Indigo `#6675ff` is agreed everywhere — the one stable value. A single canonical hex set still wants Shawn's stamp. The tokens above are the pricing page's live values, which the study records as "the live source uses the canonical tokens verbatim."

**The five denominators, tested (companion, LAW):** D1 real object that lifts and catches the one light — PARTIAL (object-ness yes, "round" no: boards are rectangles, buttons are pills, only icons are circles). D2 color IS identity — SUPPORTED. D3 light is life — SUPPORTED (rest = black face + white edge + glowing jewel). D4 everything is a door — PARTIAL (law for numbers; behavior for the rest). D5 the spectrum is the order — SUPPORTED, with the order caveat (§10).

**Shawn's vocabulary, awaiting his definition (00:13Z — no source defines these):** the elevators ("the things that lift"), the enhancers ("the things that make it shine"), the pinnacle points ("the peaks, the highest points everything rises to").

### 1.6 The realism law (Shawn's charge, 2026-11-11 21:39Z)

It has to look like the elements are DESIGNED to be together, like they're supposed to be there. Never overlay text (or a button, or a board) on an image just because you can place it there. **The test before anything reaches his eyes: does this look like it was DESIGNED to be here, or like it was PLACED here?** Designed = it belongs, it's part of the screen. Placed = a sticker on a picture. If it was placed, it doesn't go.

---

## 2. THE 22 ELEMENTS — ALL OF THEM

Every element below carries the same laws (§1). The inventory counts **22 entries**: 9 named by Shawn (2026-11-06 00:16Z), 8 more named in the canon, and 5 gauge parts named by the Real Object Law. If a source names an element, it is in this list. The substance of each entry is the Clarity Confirmation Act §4, verbatim in substance; the code-grab path is the Factory signature piece, verified on GitHub main 2026-11-12 (see §7).

**How to read an entry:** *What it is / looks like / feels like / does / laws / CHECK* is the Act. *Situation* is when to reach for it. *Live example* is a real page you can open. *Grab the code* is the exact file — take it verbatim. *Craft* is Shawn's 00:31Z word on what makes that piece extraordinary.

### The nine Shawn named

#### 01. Button — the one button

- **Act:** §4.1. **What it is:** the single DNA for every action (`.naya-btn`), with job variants (lead, machine, streak, proximity, icon, portal). **What it looks like:** really black center (`#050505`), white text with an icon, white border 1.5px+ at rest, inset top highlight + deep drop shadow. **What it feels like:** liftable — it rises on hover (2px), depresses on press (2px down), ignites purple for chrome or its own color for themed. **What it does:** the action. It promises its behavior with its glyph — a plus promises "add," a chevron promises "go somewhere." **Laws:** Design Laws Law 5; Real Object Law principles 1–5; Playbook rule 10 (harvest, don't invent). **CHECK:** touch target ≥44px (principal CTA ≥52px); focus + pressed states present; a flat button fails.
- **The button law (pricing study, verbatim in substance):** at rest, a button is quiet — white text, a visible white rim of at least 1.5px, no colour. A coloured unselected button is nonsense — it claims an active state that has not happened. On touch, it ignites in its own colour — never anyone else's. Restraint governs the row: five lit buttons in a row is overload. Every control works, or it does not ship. The quality test, in one line: press it. If nothing true happens — no state changes, no door opens, no number moves — it was decoration wearing a button's clothes. Cut it or make it real.
- **Situation:** every action on every page. One DNA, job variants for lead / machine / streak / proximity / icon / portal. A button that does not function is a lie on the page — never ship it.
- **Live example:** the pricing page — *Start free* ◆, *See how the money works* ◆ — https://naya-model-pricing.nayapower.workers.dev/ (HTTP 200, 11,350,562 B, verified 2026-11-12). Button wiring read in code; **no live click test was performed — click-proven is still owed** (study's own honest gap).
- **Grab the code:** `signature-pieces/01-button.html` — local `~/workspace/smart-factory/signature-pieces/01-button.html` · repo `BRAIN/10-INTERFACES/DESIGN-BLOCKS/signature-pieces/01-button.html` · harvested from `smart-factory/harvested/dashboard.html` (61 rules / 198 lines) · rollout group 1, first on Dashboard. Shared tokens first: `signature-pieces/00-shared-tokens.html`.
- **Craft (Shawn 00:31Z):** "The most extraordinary button: one DNA, really black, white-rimmed at rest, igniting in its own color — molded to be the single action a person trusts without reading."

#### 02. Board — the outer board

- **Act:** §4.2. **What it is:** the slab that holds a world — a Smart Link, a page summary, a note — one board per thing. **What it looks like:** obsidian body (dark gradient `#1a171f → #09090d → #030304`), 1.5px tone-mixed border, 24px radius, 5-layer shadow, tone spine (7px, glowing), corner-jewel orbs, white-lit edges at rest. **What it feels like:** a slab lifted off the field — it rises 5px on hover and ignites in its own tone. **What it does:** holds one thing, one glance, and opens it on touch. **Laws:** Design Laws Law 3; Real Object Law; Hub Board Law (black elevated on black; lights in its own icon's color as you scroll, following the spectrum; nested boards ride higher). **CHECK:** 5-layer shadow values present; border 1.5px; radius 24px; a board that blends into the field fails.
- **Board anatomy (pricing study, verbatim in substance):** obsidian body (`#050507` / `#0b0b12`) with living depth — elevation, edge light, seating shadow. Zero flat: if it does not read as premium in monochrome, colour will not save it. One colour, owned: each board carries exactly one spectrum colour — its identity, assigned once and kept — spoken by its corner jewel, its rail, and its glow. Never two, never borrowed. A jewel, not a dot: the diamond marker (◆) is the board's signature and its bullet. White words, always: hierarchy comes from size, never from grey or coloured text. One job: one pain, one feature, one decision per board. Boards are horizontal rectangles, one after another, so the eye reads down a path instead of scanning a grid. Room to breathe: generous padding and space between boards.
- **Situation:** one board per thing, full width, stacked one-two-three-four-five down the page (Shawn 2026-11-05 19:28Z: world boards are NOT two side by side — one board across, icon in the corner, words on the left, button on the right, centered). A board succeeds when a cold reader can say, in seconds, what it is, what colour owns it, and what single thing it wants them to do.
- **Live example:** the pricing page's ten pain boards — https://naya-model-pricing.nayapower.workers.dev/ · and the Hub feed boards — https://nayanet.app/hub (HTTP 200, 5,548,347 B, sha256 `f60ab625…` exact, verified 2026-11-12).
- **Grab the code:** `signature-pieces/02-board.html` — local `~/workspace/smart-factory/signature-pieces/02-board.html` · repo `BRAIN/10-INTERFACES/DESIGN-BLOCKS/signature-pieces/02-board.html` · harvested from `smart-factory/harvested/hub.html` L1172–1248 (21 rules / 77 lines) · rollout group 2, first on Personal.
- **Craft (Shawn 00:31Z):** "The most extraordinary board: one slab per thing, obsidian, tone-spined, jewel-cornered — molded to hold a whole world at one glance and open it on touch."
- **Conflict touching it:** board radius — Act §4.2 says 24px (Design Laws Law 3); the Hub ships 26px (hub.html:1176). Unresolved — Shawn's eye.

#### 03. Intelligent block — the grand block

- **Act:** §4.3 + §5 (the companion, LAW). **What it is:** the Smart Note board — the elite of all blocks, the major block, the grand block. It carries every design law all the way through. **What it looks like:** an outer board (elevated, black on black) holding inner boards — the nutshell, Human Note, Child Note, Grandma Note, Naya Note, What It Means — each its own board with its own border, its own lift, its own icon-color light. The top title/quote area is not an inner board; the inner boards start at the nutshell. **What it feels like:** elevation upon elevation — a living object, layered on layers, dimensional, in and out. **What it does:** tells the truth about one piece of intelligence, in every voice (human, child, grandma, Naya, meaning), so anyone can understand it. **Laws:** Hub Board Law as amended 00:06Z + 00:08Z; Design Laws Laws 1–3; Real Object Law; the companion rules (§5). **CHECK:** each inner layer visibly lifted off the outer board; each lit in its own icon color; nutshell text 20px white; no voice; no flat lighter box. **CHECK: his eye** on whether it is the grand block.
- **The block, section by section (companion, LAW — substance):** the board itself — one Smart Note, one board; obsidian at rest; spectrum in the jewel, the edge, and the light, never ambient wash; tone from the note (default purple); border 2px tone-mixed, radius 26px (phone 20px), padding 32px 32px 24px; 4px glowing vertical tone bar at the left edge; rest opacity `.84`, scroll-lit to `1` at 12% visible; hover `translateY(-3px)` + per-tone 60px glow. Title/quote area (NOT an inner board) — white text; title size contested (three competing rules; Shawn: not massive). Date/meta line — 11px / 800 / .08em, `#817a89`, full date + time + relative age. Nutshell — the whole note in one short paragraph; text 20px white; the layer is an elevated board, never a flat lighter box; body truncated to 600 characters in render (a render fact, not a design decision). Human Note — plain, direct, warm, "you" voice; magenta layer, hot-pink jewel `#ed42c4`; open by default. Child Note — opens with an "Imagine..." analogy; sapphire layer, violet jewel `#8a5cff`; open by default. Grandma Note — opens "Dear," warm elder wisdom; emerald layer, indigo jewel `#6675ff`; open by default. Naya Note — the instruction to Naya, opens "You are the..."; purple layer, blue jewel `#3ca8ff`; open by default. What It Means — the synthesis, the durable lesson; indigo layer, lime jewel `#b8ee57`; tier deeper, starts CLOSED. Layer board (shared) — layers stack 12px apart; each a bordered (2px tone-mixed), radius-18px board; head is a full-width button (a door); head label 18px / .07em; body 17px / 1.7; lists with jewel bullets cycling hot pink → purple → blue → green → gold. Icon (the jewel) — black core, color ring, bold white glyph, 32×32; the one element allowed to glow at rest; the 12px dot is retired. Provenance foot — `#8f8898`, 12.5px; "Official NayaNET Guide · from the Intelligent Library" or "Smart Note <id> · from your Smart Feed". **The play button (voice) is present in code and FORBIDDEN by law** — NO voice anywhere on the board.
- **Situation:** one Smart Note, one board, in the feed. The feed's unit. The Personal feed carries the Hub's Intelligent Block verbatim (Smart Notes, Naya Notes, Activity — one mirror, two faces).
- **Live example:** the Hub feed — https://nayanet.app/hub (HTTP 200, 5,548,347 B, verified 2026-11-12) · and the Personal feed — https://nayanet.app/personal (HTTP 200, 1,466,205 B, verified 2026-11-12; see §7 note on the byte count).
- **Grab the code:** `signature-pieces/03-intelligent-block.html` — local `~/workspace/smart-factory/signature-pieces/03-intelligent-block.html` · repo `BRAIN/10-INTERFACES/DESIGN-BLOCKS/signature-pieces/03-intelligent-block.html` · harvested from `smart-factory/harvested/hub.html` (67 rules / 220 lines) · rollout group 2, first on Personal. Full rules: `~/workspace/team-nitro/hub-board-edit/intelligent-block-rules-LAW-20261106.md`.
- **Craft (Shawn 00:31Z):** "The most extraordinary block: the grand block, elevation upon elevation, every voice of one intelligence — molded to tell the truth so anyone understands it."
- **Conflicts touching it:** title size (three competing rules); nutshell presentation (three rules + v4 override); one layer, two colors (border/glow map vs jewel map disagree on EVERY layer); inner-board depth (principle vs code — inner shadow shallower than outer); voice (code vs law); chevron (styled vs hidden); v4 overrides vs base rules (the flat-black defect). All recorded in §10, none resolved here.

#### 04. Icon — drawn, not shrunk

- **Act:** §4.4. **What it is:** native vector geometry — bold, simple, luminous — the drawn mark of a thing. **What it looks like:** readable at 16px, own-color glow, a sheen facet. **What it feels like:** a jewel — small, hard, bright. **What it does:** says what the thing is and promises what it does. A chevron promises "go somewhere." A plus promises "add." **Laws:** Design Laws Law 4; Real Object Law principle 6 (speak in objects). **CHECK:** readable at 16px; a beautiful but inert affordance fails. **CHECK: his eye** on whether the glyph keeps its promise.
- **Situation:** every button, every board corner, every layer head, every nav pill. Icons are drawn, not shrunk. Bullets are jewels (rotated-square diamonds), not dots. Every glyph must promise its real behavior.
- **Live example:** the Hub's black-circle nav icons (9 pills, white glyphs) — https://nayanet.app/hub · the pricing page's tier glyphs (✦ Power, ★ Pro, ♛ Max) — https://naya-model-pricing.nayapower.workers.dev/
- **Grab the code:** `signature-pieces/04-icon.html` — local `~/workspace/smart-factory/signature-pieces/04-icon.html` · repo `BRAIN/10-INTERFACES/DESIGN-BLOCKS/signature-pieces/04-icon.html` · harvested from `smart-factory/harvested/hub.html` + `smart-factory/harvested/dashboard.html` (12 rules / 14 lines) · rollout group 2, first on Personal. Jewel library: `~/workspace/user/files/Naya_Jewel_Library_-_N5.html`.
- **Craft (Shawn 00:31Z):** "The most extraordinary icon: drawn, not shrunk, a faceted jewel readable at 16px — molded to say what a thing is and promise what it does."

#### 05. Orb — the constellation orb

- **Act:** §4.5. **What it is:** a glass sphere — one per category — orbiting the gauge. The nine (Playbook map — see CONFLICTS #17: the live dashboard code rotates three of these colors): Sales (magenta `#e84fff`, 100 pts), Joins (purple `#a06bff`, 50), Smart notes (deep blue `#3fb8ff`, 35), Invites (light blue `#7fd4ff`, 25), Creations (orange `#ff9a5a`, 25), Shares (green `#2fe89e`, 15), Comments (gold `#ffbf3d`, 5), Likes (red `#ff5e6c`, 1), Saves (`#c9a0ff`, 2). **What it looks like:** obsidian glass sphere, own-color light, orbiting at its angle around the gauge. **What it feels like:** a planet — it lifts 8px on hover and ignites in its own color. **What it does:** opens its drill-down on touch; every number is a door. **Laws:** Playbook (Color; the 8 orbs); Design Laws Laws 1–2; Real Object Law. **CHECK:** color per category, fixed; hover lift 8px; tap opens the drill-down. (Point values locked 2026-11-01: create 25, note 35, like/love 1, comment 5, share 15, invite 25, join 50, sale 100, saves 2; clicks and messages earn no points.)
- **Situation:** the Dashboard's constellation around the Smart Score gauge — one orb per category. Also the login dial's jewel orbit (108 jewels, 36-colour palette × 3). An orb is a number you can touch.
- **Live example:** the Dashboard — https://nayanet.app/dashboard (HTTP 200, 1,817,928 B, sha256 `bb41114d…` exact, verified 2026-11-12).
- **Grab the code:** `signature-pieces/05-orb.html` — local `~/workspace/smart-factory/signature-pieces/05-orb.html` · repo `BRAIN/10-INTERFACES/DESIGN-BLOCKS/signature-pieces/05-orb.html` · harvested from `smart-factory/harvested/dashboard.html` + `smart-factory/harvested/hub.html` (14 rules / 39 lines) · rollout group 1, first on Dashboard.
- **Craft (Shawn 00:31Z):** "The most extraordinary orb: a glass planet in its own color, orbiting the gauge — molded to be a number you can touch, a door into its drill-down."
- **Conflicts touching it:** orb colors rotate for Creating/Shares/Comments — Playbook map (Creating orange, Shares green, Comments gold) vs live dashboard code (CREATIONS green, SHARES gold, COMMENTS orange). Recorded, NOT resolved — Shawn's eye. Notes orb is `#3fb8ff` in BOTH the Playbook and the live code (the working record's `#3a5bff` appears in neither as the orb color — do not use it for the orb). Orb geometry (size, glow radius, orbit) lives in code, not in the canon docs (§9).

#### 06. Gauge — the instrument

- **Act:** §4.6. **What it is:** the precision instrument that shows your score — the dial, the needle, the numbers, the machine you can see working. **What it looks like:** obsidian bezel, aluminum chapter ring, 6 numerals (0, 100, 200, 300, 400, 500) at `angle = -135 + (value/500)*270`, ticks every 10, majors every 50, 3 center gears (3-6-9, time axis) and 6 pyramid layers (1-2-4-8-7-5, matter flow), outer toothed ring (48 teeth, r=99, 180s), hex screws. **What it feels like:** a Bugatti cockpit — the needle sweeps like acceleration, the energy builds like an engine revving. **What it does:** shows your score out of 500 so you get it in 2 seconds. **Laws:** Playbook (Formula, Vortex, Materials, Motion); Real Object Law ("Naya Is a High-Performance Machine"); Design Laws Laws 1–3. **CHECK:** numeral angles exact by formula; all six numerals present (none skipped); ambient rotation 60–180s, active 18–25s, never under 12s; directions alternate; teeth, never solid rings.
- **The gauge, in the pricing study's words:** a real dial — a fixed $0–$10,000 scale, minor ticks every $200, major ticks every $1,000, a needle that reads the score on that one scale, and a band line that always states where you stand ("$X of $10,000 — next rung"). It behaves like a physical instrument, so progress feels measured, not marketed. Tiles and text are rounded by the same function so the two can never disagree — the chart cannot contradict itself. One honest limit: on a slow scroll in the study the needle did not move and no numbers counted — the motion is designed in the code, not observed live.
- **Situation:** the Dashboard's Smart Score — the number is a proven asset: tiled everywhere numbers appear, number on top and gauge underneath, in points, percentage, and money modes with a space separator, the needle lapping the dial in sets of 500 and the gauge following the number. The gauge follows the number (Shawn's ruling — the earlier 83%-vs-52% mismatch is closed by it).
- **Live example:** the Dashboard gauge — https://nayanet.app/dashboard · the pricing page's money gauge — https://naya-model-pricing.nayapower.workers.dev/
- **Grab the code:** `signature-pieces/06-gauge.html` — local `~/workspace/smart-factory/signature-pieces/06-gauge.html` · repo `BRAIN/10-INTERFACES/DESIGN-BLOCKS/signature-pieces/06-gauge.html` · harvested from `smart-factory/harvested/dashboard.html` (37 rules / 224 lines) · rollout group 1, first on Dashboard. Its five parts are elements 18–22. Note: `harvested/gauge-verbatim.html` is FLAGGED, not rewritten — its header claims dashboard.html offsets but the content is a plus-icon SVG, not the gauge. The real gauge is `signature-pieces/06-gauge.html`.
- **Craft (Shawn 00:31Z):** "The most extraordinary gauge: the Bugatti instrument, numerals by formula, needle sweeping like acceleration — molded to give your score in 2 seconds."

#### 07. Smart app — the one app

- **Act:** §4.7. **What it is:** NayaNET — ONE ultimate app with different doors, never a bunch of separate apps. **What it looks like:** the same dashboard, mail, smart notes, smart lists, and ledger behind every door. **What it feels like:** one machine with many faces — you never leave the app, you just open more doors. **What it does:** connects all major elements in one system, optimized for your max level of experience; auto-match, auto-connect, auto-organize, auto-optimize. **Laws:** NAYA Protocol §5 (SN-0874); Real Object Law (Viewpoint Law, Rubik's Cube). **CHECK:** no second dashboard, no second mail, no second notes system — a duplicate is a fail.
- **Situation:** the whole system. Every page is a door into the one app, never a separate app. Memberships are an ADD-ON to any page, never a separate app. The standard kit on every page: Smart Mail + Instant Messenger · Smart Lists · Scheduler/Booker · About · products/services — one syncing system.
- **Live example:** nayanet.app itself — Personal https://nayanet.app/personal · Hub https://nayanet.app/hub · Dashboard https://nayanet.app/dashboard (all HTTP 200, verified 2026-11-12).
- **Grab the code:** `signature-pieces/07-smart-app.html` — local `~/workspace/smart-factory/signature-pieces/07-smart-app.html` · repo `BRAIN/10-INTERFACES/DESIGN-BLOCKS/signature-pieces/07-smart-app.html` · sourced from `team-nitro/NAYA-PROTOCOL.md` L134 (0 rules / 0 lines — it is a shape, not a style) · rollout group 3, first on Shared.
- **Craft (Shawn 00:31Z):** "The most extraordinary app: one app, many doors, the same dashboard behind every door — molded so you never leave the machine, you only open more of it."

#### 08. Page — a door

- **Act:** §4.8. **What it is:** one door into the one app — Personal, Business, Space, Membership (Smart Access). **What it looks like:** the same code and language, different labels; every page carries the standard kit (Smart Mail + Instant Messenger, Smart Lists, Scheduler/Booker, About, products/services). **What it feels like:** a world — your personal world, your business world, your space. **What it does:** opens one viewpoint, one purpose per view. **Laws:** NAYA Protocol §5; Real Object Law (Viewpoint Law); MEMORY.md (One App, Four Doors, SN-0891; Finisher Rule, SN-0892 — one page at a time to FINISHED, his eye verifies). **CHECK:** one page at a time to finished; his eye verifies each before the next begins.
- **Situation:** each door is one viewpoint with one purpose. Page order, settled: Dashboard → Personal → Hub → Pricing, each finished and proven before the next. A page is a viewpoint — its own object, its own world, its own purpose. Every page gets a COVER, then the MENU BAR, then the PAGE (§5).
- **Live example:** Personal — https://nayanet.app/personal · Hub — https://nayanet.app/hub · Dashboard — https://nayanet.app/dashboard · Pricing — https://naya-model-pricing.nayapower.workers.dev/
- **Grab the code:** `signature-pieces/08-page.html` — local `~/workspace/smart-factory/signature-pieces/08-page.html` · repo `BRAIN/10-INTERFACES/DESIGN-BLOCKS/signature-pieces/08-page.html` · sourced from the Act §4.8 (0 rules / 0 lines) · rollout group 3, first on Shared. Whole-page templates: `~/workspace/smart-factory/templates/` — personal, business, space, membership, dashboard, hub (assembled 2026-11-03 from harvested hub + dashboard; swap only the middle, fill the slots in the file header).
- **Craft (Shawn 00:31Z):** "The most extraordinary page: one door, one viewpoint, one purpose — molded to be a whole world with the standard kit inside."
- **Gap touching it:** the precise boundary between section, page, and board is not defined in the sources (§9).

#### 09. Section — a themed zone

- **Act:** §4.9. **What it is:** one part of a page, themed one color, lighting up in it. **What it looks like:** a zone with its own accent from the spectrum, distinct from its neighbors. **What it feels like:** a room inside the world. **What it does:** holds one purpose, one set of things. **Laws:** Design Laws Law 2 (themed zones — one section may be themed one color; a whole page or a run of adjacent zones never wears one hue). **CHECK:** adjacent zones read as distinct (spectral order, never clumped).
- **Situation:** a room inside a world. One section, one color, one purpose. The Hub's rooms wear one accent color each — never two rooms alike. The 13-section colour sequence on the Smart Hub fix (no adjacent hues shared) is the live example of the rule working.
- **Live example:** the Hub's rooms — https://nayanet.app/hub · the Smart Hub's sections — staged fix (see §7) · the pricing page's journey (letter → ten pains → choose your level → money boards) — https://naya-model-pricing.nayapower.workers.dev/
- **Grab the code:** `signature-pieces/09-section.html` — local `~/workspace/smart-factory/signature-pieces/09-section.html` · repo `BRAIN/10-INTERFACES/DESIGN-BLOCKS/signature-pieces/09-section.html` · harvested from `smart-factory/harvested/dashboard.html` + `smart-factory/harvested/hub.html` (9 rules / 9 lines) · rollout group 3, first on Shared.
- **Craft (Shawn 00:31Z):** "The most extraordinary section: one themed zone, one color, distinct from its neighbors — molded to be a room inside the world."
- **Gap touching it:** section/page/board boundary undefined (§9).

### Eight more the canon names

#### 10. Jewel — bullets are diamonds

- **Act:** §4.10. **What it is:** the bullet, the gem, the corner orb. **What it looks like:** a rotated square (diamond) — white → tone → black gradient, own-color glow, sheen facet; faceted gems for signal moments (true diamond geometry, white-hot crown fading to deep black base, vertical light facet). Boards wear jewels as corner orbs, lit from within, glowing in the board's tone. **What it feels like:** a cut stone. **What it does:** separates ideas — colors separate ideas, they don't compete with the words. Five-jewel cycle in law order, never twice in a row. **Laws:** Design Laws Law 4. **CHECK:** bullets are rotated squares, not dots; no color twice in a row.
- **Situation:** every bullet, every board corner, every layer jewel. The jewel is the color made physical — the one element allowed to glow at rest. The 12px dot is retired — replaced by faceted jewels. The board's own jewel is 64×64.
- **Live example:** the pricing page's ◆ bullets — https://naya-model-pricing.nayapower.workers.dev/ · the Hub's board corner jewels — https://nayanet.app/hub
- **Grab the code:** `signature-pieces/10-jewel.html` — local `~/workspace/smart-factory/signature-pieces/10-jewel.html` · repo `BRAIN/10-INTERFACES/DESIGN-BLOCKS/signature-pieces/10-jewel.html` · harvested from `smart-factory/harvested/hub.html` + `smart-factory/harvested/dashboard.html` (5 rules / 42 lines) · rollout group 2, first on Personal. Jewel library: `~/workspace/user/files/Naya_Jewel_Library_-_N5.html`.
- **Craft (Shawn 00:31Z):** "The most extraordinary jewel: bullets are diamonds, a cut stone that separates ideas — molded to be the color made physical, glowing even at rest."

#### 11. Chart — the data display

- **Act:** §4.11. **What it is:** bars, flow charts, the big number — the other faces of the data the gauge shows. **What it looks like:** the same materials, light, and motion as the gauge — obsidian, white text, slow motion, own-color ignition. **What it feels like:** the same machine, another instrument. **What it does:** shows the numbers so you understand your world in 2 seconds. **Laws:** Playbook Truth 4 (one language); Design Laws Laws 1–2. **CHECK:** same materials and light as the gauge; 2-second test passed.
- **The chart, in the pricing study's words:** the comparison structure (✓ included / ✕ not included, level by level) lets a reader verify the claim "you can check that on the chart" — the letter literally invites the check. Gold here is earned: it marks shown value, never decoration. Every chart cell carries number plus text plus check, all aligned, with chart value cells stacked and centered.
- **Situation:** wherever numbers must be understood in 2 seconds — the pricing comparison, the Dashboard's ledger and stats, the Smart Score. The chart is the page on pricing: the chart IS the page, the Top 10 pains open it, the founder's letter closes it.
- **Live example:** the pricing comparison chart — https://naya-model-pricing.nayapower.workers.dev/ · the Dashboard charts — https://nayanet.app/dashboard
- **Grab the code:** `signature-pieces/11-chart.html` — local `~/workspace/smart-factory/signature-pieces/11-chart.html` · repo `BRAIN/10-INTERFACES/DESIGN-BLOCKS/signature-pieces/11-chart.html` · harvested from `smart-factory/harvested/dashboard.html` (17 rules / 21 lines) · rollout group 1, first on Dashboard.
- **Craft (Shawn 00:31Z):** "The most extraordinary chart: the gauge's other face, same materials, same light, same motion — molded to show the numbers so you understand your world in 2 seconds."

#### 12. Tab / pill — the quiet element

- **Act:** §4.12. **What it is:** a secondary control — a tab, a pill, a quiet link. **What it looks like:** dark, white text, resting quiet. **What it feels like:** light — it may glow without lifting. **What it does:** switches a view, filters a list. **Laws:** Design Laws Law 1 (graded, not absolute — secondary elements may glow without lifting; what is never allowed is neither). **CHECK:** glows on hover. An element that does nothing on hover fails.
- **Situation:** view switches and filters — the Hub's feed bar (COLLECTIVE / PERSONAL / ACTIVITY + filter pills), the PI Live Wall's category pills (§4), the Smart Organizer tabs (§5). Tabs are signature pieces: 10/10, OFFICIAL for the whole network (the Smart Organizer round makes them so — queued after this inventory).
- **Live example:** the Hub's feed tabs — https://nayanet.app/hub · the pricing page's plan doors (monthly / quarterly / yearly) — https://naya-model-pricing.nayapower.workers.dev/
- **Grab the code:** `signature-pieces/12-tab-pill.html` — local `~/workspace/smart-factory/signature-pieces/12-tab-pill.html` · repo `BRAIN/10-INTERFACES/DESIGN-BLOCKS/signature-pieces/12-tab-pill.html` · harvested from `smart-factory/harvested/dashboard.html` (33 rules / 108 lines) · rollout group 1, first on Dashboard.
- **Craft (Shawn 00:31Z):** "The most extraordinary tab: the quiet element, dark at rest, glowing on hover without lifting — molded to switch a view without shouting."

#### 13. Smart Link — the attested link

- **Act:** §4.13. **What it is:** a claimed name that routes to a destination — the link itself is the attestation: SEE, VERIFY, confirm. **What it looks like:** a button or board carrying a name and a destination. **What it feels like:** a door with a receipt. **What it does:** takes a person to the destination and counts the click, the return, the join. **Laws:** Essence 06 (the note system itself); MEMORY.md (Smart Links mechanics; mint-at-publish). **CHECK:** a Smart Link carries its receipt (claim, verification, count).
- **Situation:** every link that must be attested — the ambassador link (the default Smart Link, featured at the top), plan links on pricing, the nine Smart Links minted 2026-11-06 (owner flagship-personal, all 302 → PayPal plan IDs). Mint-at-publish is the settled shape. Honest boundary: the Smart Link sees the click and the return, not the payment itself — the dashboard marks it "returned from PayPal," never payment-proven.
- **Live example:** the pricing page's plan links — https://naya-model-pricing.nayapower.workers.dev/ · Smart Links featured at the top of pages, ambassador link as the default.
- **Grab the code:** `signature-pieces/13-smart-link.html` — local `~/workspace/smart-factory/signature-pieces/13-smart-link.html` · repo `BRAIN/10-INTERFACES/DESIGN-BLOCKS/signature-pieces/13-smart-link.html` · harvested from `smart-factory/harvested/dashboard.html` (7 rules / 7 lines) · rollout group 1, first on Dashboard.
- **Craft (Shawn 00:31Z):** "The most extraordinary link: a door with a receipt — SEE, VERIFY, confirm — molded to carry its claim, its verification, and its count."
- **Gap touching it:** the Smart Link visual spec is missing — its visual rules (sizes, colors, states) are not in the canon design docs (§9). Smart List and Smart Mail visual specs are missing the same way.

#### 14. Header — the warm front door

- **Act:** §4.14. **What it is:** the top of a page or board. **What it looks like:** logo + living mark + warm voice + one clear line, full width — content owns the width, no max-width caps. **What it feels like:** a welcome. **What it does:** tells you where you are and what this is, in one line. **Laws:** Design Laws Law 3. **CHECK:** one clear line; full width.
- **Situation:** the top of every page and every board. One clear line. The membership login's top black bar carries the course name only, on one line (Shawn 2026-11-12 16:06Z, F6).
- **Live example:** the Personal page header — https://nayanet.app/personal · the pricing page's letter opening — https://naya-model-pricing.nayapower.workers.dev/
- **Grab the code:** `signature-pieces/14-header.html` — local `~/workspace/smart-factory/signature-pieces/14-header.html` · repo `BRAIN/10-INTERFACES/DESIGN-BLOCKS/signature-pieces/14-header.html` · harvested from `smart-factory/harvested/dashboard.html` + `smart-factory/harvested/hub.html` (6 rules / 34 lines) · rollout group 2, first on Personal.
- **Craft (Shawn 00:31Z):** "The most extraordinary header: the warm front door, logo + living mark + warm voice + one clear line, full width — molded to welcome in one line."

#### 15. Overlay — the top layer

- **Act:** §4.15. **What it is:** the layer above the controls — a popover, a derivation sheet, a menu that unfolds. **What it looks like:** a glass sheet riding above the board, lit, readable. **What it feels like:** a sheet held above the page. **What it does:** shows the detail (the derivation, the next move, the menu) and folds away. **Laws:** Design Laws Law 3 (elevation order: Field > Board > Nested panel > Control > Overlay). **CHECK:** rides visibly above the control it serves; folds away when dismissed.
- **Situation:** detail on demand — derivation sheets, menus, the membership login overlay (`#mwSmartAccess` on Personal), the first-visit install dialog. The overlay is the top layer; it never becomes the page.
- **Live example:** the membership login overlay on Personal — https://nayanet.app/personal (open via the membership door) · the pricing page's money-story overlays, which open in place and close back to exactly where you were — https://naya-model-pricing.nayapower.workers.dev/
- **Grab the code:** `signature-pieces/15-overlay.html` — local `~/workspace/smart-factory/signature-pieces/15-overlay.html` · repo `BRAIN/10-INTERFACES/DESIGN-BLOCKS/signature-pieces/15-overlay.html` · harvested from `smart-factory/harvested/dashboard.html` + `smart-factory/harvested/hub.html` (10 rules / 17 lines) · rollout group 3, first on Shared.
- **Craft (Shawn 00:31Z):** "The most extraordinary overlay: the top layer, a glass sheet riding above the board — molded to show the detail and fold away."

#### 16. Control — the working element

- **Act:** §4.16. **What it is:** an input, a gear, a setting, a toggle — the element that takes an instruction. **What it looks like:** dark, white text, visible edge. **What it feels like:** a switch or dial you can operate. **What it does:** takes the person's choice (PTS or %, a setting, a name to claim). **Laws:** Design Laws Laws 1, 3 (elevation order); Real Object Law principle 5 (touch = physical). **CHECK:** responds physically on touch; its state is visible.
- **Situation:** every working element — toggles, gears, settings, the calculator's pace setter, the Smart Bar's add-editor. A control's state is always visible; a control that hides its state is unfinished.
- **Live example:** the pricing calculator — https://naya-model-pricing.nayapower.workers.dev/ · the Dashboard's controls — https://nayanet.app/dashboard
- **Grab the code:** `signature-pieces/16-control.html` — local `~/workspace/smart-factory/signature-pieces/16-control.html` · repo `BRAIN/10-INTERFACES/DESIGN-BLOCKS/signature-pieces/16-control.html` · harvested from `smart-factory/harvested/dashboard.html` + `smart-factory/harvested/hub.html` (7 rules / 32 lines) · rollout group 1, first on Dashboard.
- **Craft (Shawn 00:31Z):** "The most extraordinary control: the working element, a switch you can operate, its state visible — molded to take a person's choice and show it."

#### 17. Input — the well

- **Act:** §4.17. **What it is:** a dark recessed channel, carved inset shadow, white text. The inverse of a button — you press INTO it. (Anatomy N1, "The Well": "Dark recessed channel, carved inset shadow, white text. The inverse of a button — you press INTO it." Status: BUILT. Law: inputs are wells.) **What it looks like:** a dark field with a white edge and white text — a slot carved into the page, not a box sitting on it. **What it feels like:** a well you put something into; a button presses back, a well receives. **What it does:** receives the person's words and validates them (a claim form says plainly whether a name is free, taken, or reserved — nothing is saved when claiming is closed). The Hub's Ask Naya well (N10 Search Well) is deep, purple-ringed, voice-ready; search lives BELOW the bar, never inside it. **Laws:** Anatomy §1.4 law 11 ("Inputs are wells") and §2.4 (N1 the Well, N10 the Search Well, N8 the Rich Composer); Real Object Law principle 1 (everything is an object); Essence 01 (the record must tell the truth). **CHECK:** validation speaks plainly; nothing is saved when it shouldn't be; the well is recessed (inset shadow), not raised.
- **Situation:** every place a person types — the login name pill, the claim form, the Ask Naya well, the Smart Bar add-editor, the project-naming step. Inputs always have lots of depth. A well receives; it never presses back.
- **Live example:** the login name pill (gold at rest → lights purple on focus) — https://nayanet.app/ · the Hub's Ask Naya well — https://nayanet.app/hub · the Personal "Make a post" entry — https://nayanet.app/personal
- **Grab the code:** `signature-pieces/17-input-well.html` — local `~/workspace/smart-factory/signature-pieces/17-input-well.html` · repo `BRAIN/10-INTERFACES/DESIGN-BLOCKS/signature-pieces/17-input-well.html` · harvested from `smart-factory/harvested/hub.html` + `smart-factory/harvested/dashboard.html` (6 rules / 12 lines) · rollout group 2, first on Personal.
- **Craft (Shawn 00:31Z):** "The most extraordinary input: the well, a dark recessed channel you press INTO — molded to receive a person's words and answer plainly."

### Five gauge parts the Real Object Law names

The gauge (element 06) is five parts, each a separate object at a different depth. All five harvest from `smart-factory/harvested/dashboard.html`, rollout group 1, first on Dashboard.

#### 18. Case — the gauge body

- **Act:** §4.18. The body of the instrument — obsidian, the housing everything else sits in. **Laws:** Real Object Law ("Mastering 3D Objects" — assembly: a gauge has a case, bezel, dial, crystal, needle, each a separate part at a different depth).
- **Situation:** the housing. Build the case first; everything else sits in it.
- **Live example:** the Dashboard gauge — https://nayanet.app/dashboard
- **Grab the code:** `signature-pieces/18-gauge-case.html` (2 rules / 25 lines; dashboard.html L2428–2441, L2489–2499) — local `~/workspace/smart-factory/signature-pieces/` · repo `BRAIN/10-INTERFACES/DESIGN-BLOCKS/signature-pieces/`.
- **Craft (Shawn 00:31Z):** "The most extraordinary case: the housing everything sits in, obsidian, the body of the instrument — molded to hold the machine together."

#### 19. Bezel — the machined edge

- **Act:** §4.19. The machined edge of the instrument — brushed metal, the ring the eye hits first. Finish the outside: the bezel is what frames the center. (Playbook: "The outside is what frames the center... Finish it."; Design Intelligence Report: "I left the bezel plain. Shawn called it incomplete.")
- **Situation:** the frame. The eye hits the bezel first — a plain bezel makes the whole instrument read incomplete.
- **Live example:** the Dashboard gauge — https://nayanet.app/dashboard
- **Grab the code:** `signature-pieces/19-gauge-bezel.html` (2 rules / 3 lines; dashboard.html L2660–2662).
- **Craft (Shawn 00:31Z):** "The most extraordinary bezel: machined aluminum, the edge the eye hits first — molded to frame the center."

#### 20. Dial — the face

- **Act:** §4.20. The face — the aluminum chapter ring the numerals sit on, engraved, not floating, shadow offset (0.8px, 0.8px). (Playbook rule 20.)
- **Situation:** the face the numerals sit on. Numerals are engraved on the dial, never floating above it.
- **Live example:** the Dashboard gauge — https://nayanet.app/dashboard
- **Grab the code:** `signature-pieces/20-gauge-dial.html` (2 rules / 23 lines; dashboard.html L2501–2508, L2639–2653).
- **Craft (Shawn 00:31Z):** "The most extraordinary dial: the face, numerals engraved on aluminum, never floating — molded to be read at a glance."

#### 21. Crystal — the glass

- **Act:** §4.21. The glass over the dial — light catching the glass as the machine settles, the highlight that rotates slowly. (Playbook Step 4.)
- **Situation:** the glass. Light catching it as the machine settles is what proves it is glass, not a picture.
- **Live example:** the Dashboard gauge — https://nayanet.app/dashboard
- **Grab the code:** `signature-pieces/21-gauge-crystal.html` (1 rule / 10 lines; dashboard.html L2490–2499).
- **Craft (Shawn 00:31Z):** "The most extraordinary crystal: real glass over the dial, light catching it as the machine settles — molded to prove it is glass, not a picture."

#### 22. Needle — the value

- **Act:** §4.22. The value — it sweeps like acceleration. It is the number made physical. (Real Object Law, "Naya Is a High-Performance Machine".)
- **Situation:** the value, made physical. The needle reads the live value on the one scale; the gauge follows the number.
- **Live example:** the Dashboard gauge — https://nayanet.app/dashboard · the pricing money gauge — https://naya-model-pricing.nayapower.workers.dev/
- **Grab the code:** `signature-pieces/22-gauge-needle.html` (2 rules / 22 lines; dashboard.html L2556–2562, L2621–2635).
- **Craft (Shawn 00:31Z):** "The most extraordinary needle: the value made physical, sweeping like acceleration, casting its shadow — molded to be the number you feel."

**Inventory count: 22 elements.** (9 named by Shawn + 8 named in the canon + 5 gauge parts.)

---

## 3. POWER'S PRICING GRAMMAR — THE REFERENCE PAGE

The pricing page is one of our best pages for presentation (Shawn's word, 2026-11-12 15:59Z — that is why he had Naya Power study it). The study below is hers, taken from the live page and its live source on 2026-11-12 — not from memory. The board anatomy and button law are carried in elements 02 and 01; this section gathers what is specific to the page: the journey, the money story, the colour flow, and the training programme's home.

**The verdict (the study's own words):** "It does not describe the product. It performs it. … The selling instrument and the product are the same object. The boards, buttons, charts, calculator and glowing dial a visitor meets on the way to paying are the same boards, buttons, charts and dials they will live with inside NayaNET."

**The journey — ten pains, in sequence, do the selling.** The page opens as a letter from the founder — "Get in the Bugatti — or stay in the golf cart. The door's open." — with two reading speeds offered at once (*Keep reading*, or *read the whole letter at once*). Then the Top Ten Reasons to Join, each board in the same four-beat rhythm: the pain in plain words, why it happens, the solution, and what's in it for you — closing with a bridge into the next pain. Only after the tenth pain does the page ask for a decision: "Choose your level." It closes by gathering all ten audiences — "This is who it's for. Be honest. This is for you."

**The money, shown not asserted.** Power $25 / month (Ambassador half $12.50) · Pro $50 (half $25) · Max $100 (half $50), the trial level. Yearly behind the yearly door: $150 / $300 / $600 at the founding half price. The first 1,000 founding members get half price, the number rendered on the page as digit tiles. Nine days free on Max, no card, nothing charged; day ten charges only the level the member picked; levels can be re-picked any period. A clean sale pays on day ten; if a processor holds a payment, the member's half lands when the money arrives. Revenue, not profit: "we make a dollar, you make fifty cents." No downline, no upline. The calculator ("What a pace adds up to") turns the abstract 50% into the reader's own arithmetic: one Max join a day is $50 a day; three a day is $150 a day — $4,500 a month — recurring every period they stay.

**The colour flow (the study's rules):** one global spectrum sequence per page, richest first, every neighbouring element in a visibly distinct hue. Adjacent things never share a hue — the most repeated law in the whole design corpus. Yellow next to gold is banned; teal next to emerald is banned. Chrome acts, text speaks, theme identifies. Depth before colour. Size separates; colour never does.

**What mastery consists of (the study):** recognising a thing by its colour before reading its title (one board, one colour). Trusting a glow, because a glow has never lied (white at rest, own colour on touch; green only when proven). Feeling depth before noticing colour (zero flat, always). Knowing the next step without being told (one job per board, rectangles reading down). Mobile first — mobile *is* the app: slide-over panels, gestures, install-ready. The phone is not a smaller version; it is the version.

**The standard it sets:** understood within seconds, unaided — or it does not ship. That is the acceptance test this page was built to, and the test every agent in the training programme (§8) is held to.

**Honest gaps on the pricing page itself (the study, verified live 2026-11-12 — carried, not hidden):** no site footer; truncated audience lines on every Top Ten card ("This one is for..." cut off mid-word); no $0 price for Free; vague Max-only cells (Smart Video "★ contact", Smart Events "★ contact for pricing"); numbers built digit-by-digit as tiles (awkward to select/copy, easy for text extraction to miss); light that does not move on slow scroll (needle did not move, no numbers counted — the instrument is drawn, in that observation it did not perform); length is a risk the design must keep earning; proof by click is still the standard — and still owed (no live click test was performed; button function is not click-proven; the full checkout journey is unclaimed). Not gaps, confirmed fine by Shawn: prices follow the table header; no lifetime price (removed by his decision). Annual pricing exists behind the yearly door — not a gap.

**Source:** `~/workspace/user/files/pricing-page-design-study__1.pdf` — "NayaNET · Design Study — The pricing page is the product, demonstrating itself." Live page: https://naya-model-pricing.nayapower.workers.dev/ (HTTP 200, 11,350,562 B, verified 2026-11-12). Public name: nayanet.app/pricing.

---

## 4. THE PI LIVE WALL BOARD LANGUAGE — ADOPTED FOR PUBLIC PAGES

Project Intelligence is internal-only — for us, not for the public (Shawn's word, 2026-11-12 15:59Z). But its presentation — the colour language, the elevation, the flow of colours — is adopted for public pages: the Smart Hub, the Smart Factory, Intel Today, even lists. This section records the Live Wall's language from Shawn's screenshot (2026-11-12 15:59Z, `~/workspace/user/media_library/image/image-5.png`), so public pages can speak it. PI itself stays internal.

**The Live Wall (inside Personal) — what it looks like:** elevated obsidian boards, one spectrum colour per board, full width, stacked down the page. A purple-glow search bar at the top ("Search the network..."). Category pills above it (Overall list · Not placed · All · Personal & apps · Hub & dashboard · People, mail & match · Factory, voice & membership · Smart Notes feed · To go in (files) · The 25 missions · Doubled-page rulings · Day Journal). App pills at the bottom (Personal · Business · Space · Intel Today · Smart Mail · Smart Lists · Library · Project Intel · Pricing).

**The four-beat board language — every board says four things, in this order, each board one spectrum colour:**

| Beat | Colour (as seen) | What it says |
|---|---|---|
| **What it is** | Gold / orange | The thing, named plainly. "The live wall inside Personal — what is happening, in the open." |
| **What it does** | Red | The action it takes. |
| **Why it matters** | Magenta / purple | Why it belongs — "It is one of the official pages, so it belongs in PI in one place, with its link and its to-do list, or the whole picture is incomplete." |
| **How it connects** | Purple / blue | Where it sits in the system — "It sits in its record area's to-do list; its Front/Back panels below show that area's jobs in plain words (front) and machine words (back)." |

**The Standing note board (blue):** the open feed inside Personal — what is happening, in the open. It lives inside your Personal page, beside your other sections, so what is happening around you is visible in one place. It opens with Personal at nayanet.live/personal.

**The "Governs this app" strip (purple):** A0 · Constitution · D0 · Design contract · E1 · Spectrum tokens · E2 · Dominant tokens · E4 · Board mapping · E5 · Action colors · Design law (DESIGN scope) → · All governing law →. Strip buttons use short labels; full packet titles live on the governing cards.

**How to use this language on public pages:** the four-beat structure (what it is / what it does / why it matters / how it connects) + the Standing note board + the per-board spectrum colour (no adjacent hues shared) is the Smart Hub fix's E10 strip, applied 2026-11-12: four full-width boards (gold · red · magenta · purple) + footer as Standing note board (blue). That is the adoption in practice — the language travels, PI stays internal.

**Live example (internal only):** nayanet.live/personal — **unreachable from this VM at verification time (curl 000, 2026-11-12 ~16:2xZ; same as the 14:39Z director pass). Recorded honestly: not verified live in this round.** The screenshot is the evidence for this section, not a live probe.

---

## 5. PAGE LAWS THAT RIDE WITH THE INVENTORY

### 5.1 Cover → menu → page (Shawn's charge, 2026-11-12 15:25Z — "ALL PAGES SHOULD MIRROR THIS CONCEPT FOR ACTIVENESS LOOK AND FEEL")

Every page gets a COVER, then the MENU BAR, then the PAGE — like a website's top menu bar, except instead of the menu at the very top it is cover → menu → page. Every page looks beautiful the moment you land on it. The feed under the menu is full page. The pricing page is the activeness reference — ALL pages mirror its concept for activeness, look and feel. Shawn makes a feature cover image for each page; the cover slot is the deliverable, his image swaps in when he makes it. The Smart Hub is the first page to carry it.

**The charges that ride with it, all from the same dictation:** obsidian black ("city in black"), NEVER gray (gray is hard to read) · all icons lit white even at rest, on obsidian black · way less small text on the boards (title + subtitle + nutshell, nothing more) · the 1-2-3 steps MUCH bigger (easy as 1-2-3) · the operating-center heading centered · EVERY box elevated (the main box, the bridge, the middle boxes — no flat boxes, no flat buttons) · the bridge boxes in three colors (purple · blue · green, from the pricing page) · every board and button LIGHTS UP on hover (like the pricing page — that's LAW; moving on hover without lighting up FAILS; unlit at rest is white, on hover it lights purple or the board's color) · HARVEST FROM THE FACTORY, never invent parts — if a new part must be created, do it in the EXACT same format as the harvested ones (elevated, lit, real objects).

### 5.2 The Smart Organizer — the smart tabs ARE the organizer (Shawn's order, 2026-11-12 15:43Z)

The smart tabs are the organizer — the system auto-sorts notes into categories and makes a tab for each; the tabs scroll across. Rename/add categories, add a URL, star it, save notes into a smart list and save the list as a smart tab. The tabs are signature pieces, 10/10, OFFICIAL for the whole network. The Smart Organizer round (queued after this inventory) harvests the Hub's smart-tabs code verbatim, makes the tab buttons 10/10 and OFFICIAL, and plugs them into Personal / Business / Space. The tabs live in the feed, below the feed buttons — NOT a bottom bar.

### 5.3 Navigation law (current, 2026-11-12)

- **NO smart bar at the bottom on ANY page (Shawn 2026-11-12 15:43Z).** The top Smart Bar was also removed (03:43Z). Navigation = plus buttons (top left + top right corners) + profile buttons + the bottom icon row.
- **The trio (Mail · Activity · Space) is on ALL pages, above the bottom row.** It FADES on scroll down and returns on scroll stop (Shawn 15:10Z). The Hub nav v2 staged build holds it fixed (never moves/fades) — that is the build as built, superseded by the ruling; staged only, not merged, not live.
- **The Hub's bottom navigation row gets the BLACK CIRCLE icon treatment** — elevated, no badge off Activity, Hub-only. (Black-icons fix round, staged v3, captain double-check in progress at this writing.)
- **Sidebars:** the corner + buttons pop the sidebar on THEIR side — LEFT + pops the left sidebar, RIGHT + pops the right sidebar (Shawn 2026-11-12 16:06Z, F4 — both currently pop left, a defect the Personal row round fixes). Left sidebar (Personal): Home/Hub · Personal · Business · Space · Your Reports · Intel Today · Your Connections · Smart Meet. Right sidebar default: Smart Factory · memberships · Leaderboards · chosen spaces · custom URLs · About Us + White Paper at bottom. Personal/Business/Space relabel to the actual page names.
- **Search is a dedicated experience opened on purpose, never a hard-coded page element.** The search engine is for NayaNET only, not the web; match plus search are two halves of one auto-connection.
- **The official navigation spec:** `~/workspace/team-nitro/official-navigation/THE-OFFICIAL-NAVIGATION.md` (110 lines, "Status: the standard"). The root copy `~/workspace/team-nitro/THE-OFFICIAL-NAVIGATION.md` (204 lines) is a STALE draft — never point a delivery at it.

---

## 6. THE 7 LIBRARIES + THE FACTORY TEMPLATES

### 6.1 The seven canonical libraries (all test-`f` verified present, 2026-11-12)

The libraries are the raw material the Factory harvests from. Each is a full HTML design system — buttons, blocks, elements, jewels, hubs — built before the Act, and the source of the signature pieces.

| # | Library | Path (`~/workspace/user/files/`) |
|---|---|---|
| 1 | Naya Beautiful Button Set N4 | `Naya_Beautiful_Button_Set_N4.html` |
| 2 | Naya Building Blocks — The Ultimate Design System — Naya 2 | `Naya_Building_Blocks_-_The_Ultimate_Design_System_-_Naya_2.html` |
| 3 | Naya Design Element Set N4 | `Naya_Design_Element_Set_N4.html` |
| 4 | Naya Design Elements N2 | `Naya_Design_Elements_N2.html` |
| 5 | Naya Design Standard Showcase 1 | `Naya_Design_Standard_Showcase__1.html` |
| 6 | Naya Epic Elements — Lego pieces N5 | `Naya_Epic_Elements_-_Lego_pieces_N5.html` |
| 7 | Naya Jewel Library — N5 | `Naya_Jewel_Library_-_N5.html` |
| — | Naya Smart Hub Design (the Hub's design file) | `Naya_Smart_Hub_Design.html` |

Use them as harvest sources, never as templates to ship whole. A piece taken from a library is filed as a signature piece with its source + lines, like the 22 in §2.

### 6.2 The Factory templates (6 standard pages + Smart Box)

| Page | Factory path | Source | Fill slots |
|---|---|---|---|
| Personal | `templates/personal.html` | assembled 2026-11-03 from harvested/hub.html + harvested/dashboard.html | {{name}}, {{vision}} + content slots (see file header) |
| Business | `templates/business.html` | assembled 2026-11-03 from harvested/hub.html + harvested/dashboard.html | {{name}}, {{vision}} + content slots |
| Space | `templates/space.html` | assembled 2026-11-03 from harvested/hub.html + harvested/dashboard.html | {{name}}, {{vision}} + content slots |
| Membership | `templates/membership.html` | assembled 2026-11-03 from harvested/hub.html + harvested/dashboard.html | {{name}}, {{vision}} + content slots |
| Dashboard | `templates/dashboard.html` | `~/workspace/smart-factory/harvested/dashboard.html` | hero headline + score, gauge score + band, constellation orb values (9 orbs), feed / stats / charts |
| Hub | `templates/hub.html` | `~/workspace/smart-factory/harvested/hub.html` | hero kicker + title + quote, feed items (Smart Notes), sidebar doors + tabs, search well placeholder |
| Smart Box (system template) | `templates/smart-box/` | Packaged 2026-11-06 from Nitro's personal Smart Box (2,086 entries, re-verification DONE) — verified tools + operating law, no entries carried | Live working example: https://nayanet.app/smartbox (the REAL Box, worker `naya-smart-box`; PR #3237 open, not merged) |

Templates are taken whole; swap only the middle; fill the slots in the file header. Never restyle a template shell. The Factory inventory that lists all of this: `~/workspace/smart-factory/INVENTORY.md` + `inventory.json` (22 pieces, 6 templates, 4 conflicts, 3 fixes) — and this document is linked from it (see §12).

### 6.3 The canonical piece index — the authority on what is canonical

`BRAIN/10-INTERFACES/SMART-FACTORY-CANON/CANONICAL-PIECE-INDEX.md` / `.json` (reconciled 2026-10-21, amended 2026-10-22, Shawn's approval; landed by PR #2849, merged 2026-10-21, independent re-score by Resolve 9.5/10 APPROVED): **571 unique IDs → 154 canonical + 1 superseded (NAYA-INP-001 → NAYA-INP-008) + 3 verified-not-canonical + 413 retired** ("no artifact found in store, factory page, showcase, inventory, or templates"). The 416 unverified = the 413 retired + the 3 verified-not-canonical. The blessed inventory builds from the 181 real parts (157 interface + 24 functional), not the 566. **The canonical index IS the authority on retired status** — a snippet-level check that doesn't consult it will undercount. Quarantined, never use: NAYA-NAV-001, NAYA-NAV-007, NAYA-TYP-001, NAYA-TYP-002, NAYA-TYP-007, NAYA-TYP-008.

---

## 7. LIVE EXAMPLE PAGES — LINK-CHECK TABLE

Verified by curl with a browser User-Agent, 2026-11-12 ~16:2xZ. Sizes and sha256 prefixes are the check — a later reader re-curls and compares.

| Page | URL | Status | Size | sha256 (first 16) | Notes |
|---|---|---|---|---|---|
| Pricing (worker) | https://naya-model-pricing.nayapower.workers.dev/ | 200 | 11,350,562 B | `7a0b837c481f5dfc` | The activeness reference. Same bytes as nayanet.app/pricing. |
| Pricing (public name) | https://nayanet.app/pricing | 200 | 11,350,562 B | `7a0b837c481f5dfc` | Byte-identical to the worker URL. |
| Personal | https://nayanet.app/personal | 200 | 1,466,205 B | `eeb0f6ea252ed4ae` | **FLAG — differs from the round-6 + fix-1 + reconcile live record (1,489,832 B, sha256 `c2d0fdf5…`, confirmed 15:0xZ). Verified twice in this round, stable. The captain is told; this document does not explain the change.** |
| Hub | https://nayanet.app/hub | 200 | 5,548,347 B | `f60ab625b27483fe` | Exact match to the live-Hub record. |
| Dashboard | https://nayanet.app/dashboard | 200 | 1,817,928 B | `bb41114dcca4cedd` | Exact match (pass-10 live). Pass-13 staged, not live. |
| Login (gate) | https://nayanet.app/ | 200 | 620,595 B | `0c8628d5769c10e6` | Variant C live, exact match. |
| PI Live Wall | https://nayanet.live/personal | 000 (unreachable) | — | — | **NOT verified live in this round.** Unreachable from this VM (same as the 14:39Z director pass). Internal only. §4 rests on Shawn's screenshot, not a live probe. |
| Smart Hub fix (staged) | https://naya-proof-host.nayapower.workers.dev/?file=SMART-HUB/smart-hub.html&ref=smart-hub/fix-20261112&cb=fdd05b150642f611a0b4b1810be3e3e9681c8195 | staged | 66,316 B | `b474f9f0…` | Fix round staged 16:09:51Z, honest 9/10. Captain double-check owed. Not merged, not live. |
| Hub black-icons (staged v3) | https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/hub-bar-black-icons-20261112/hub-bar-black-icons-fixed.html&ref=hub/bar-black-icons-20261112-v3&cb=e002772b5e2402201ea57760e450b8d89fa2adaaa48823f0d3fe25fb86cca43f | staged | 5,610,508 B | `e002772b…` | Staged v3, honest 9/10. Captain double-check in progress. Not merged, not live. |

**GitHub read-back (2026-11-12 ~16:2xZ):** `BRAIN/10-INTERFACES/DESIGN-BLOCKS/signature-pieces/` on main holds all 22 pieces (`01-button.html` … `22-gauge-needle.html`) + `00-shared-tokens.html` + `INVENTORY.md` (sha `84aacdb16759807361fa992b4b362d6f31716df9`, 30,326 B, 107 lines) + `ROLLOUT.md` + `inventory.json` + `rollout.json` — 27 entries. The local `~/workspace/smart-factory/INVENTORY.md` is the same document, byte-identical in substance (verified by reading both).

**Coverage: 22/22 elements carry a live example URL and a code-grab path in §2.** No element is listed without both.

---

## 8. THE TRAINING PROGRAMME — HOW EVERY AGENT REACHES THIS LEVEL

From the pricing study (Stage 1–4), the curriculum this inventory is written to teach. Right now the team has one master designer of interfaces and the rest are learning. That gap does not close with talent or taste. It closes with a loop, run on every page, until the language is reflex.

**Stage 1 — Study (before touching anything).** Read the 16 Design Laws in full, live, and record the file and date read. A stale citation is not a source. Reverse-engineer one master page per week — the pricing page first — board by board, button by button, token by token, exactly as the study does. Name every piece; if you cannot name it, you have not seen it. This inventory is the naming list.

**Stage 2 — Compose (build only from the language).** Assemble from inventoried elite pieces, verbatim. Invent nothing the library already has; a private colour or a private style is an automatic fail. One board, one colour, one job. White text. White at rest. Depth before colour. Rectangles reading down. Mobile first.

**Stage 3 — Prove (no self-awarded marks).** The seconds test: a cold reader understands the page within seconds, unaided — or it does not ship. The click test: every button pressed, every door opened, at the real address, on desktop and phone. Pretty but useless never ships. Independent scoring: the builder scores the page, then a different seat scores the exact final version. A lesson counts only when a future decision changes because of it.

**Stage 4 — Teach it forward.** Every correction lands in the shared record the same pass, so the next agent starts from the lesson, not from the mistake. Graduation is demonstrated, not declared: an agent is a master when a cold successor can take their page, speak its language, and extend it without breaking a single law.

**The charge (the study's):** "We are extraordinary, and not at bullseye yet — mastery has no finish line. Study this page until you can rebuild its grammar from memory, then build to its standard until you no longer need to check. That is how one master designer becomes a team of them."

**The activation habit (Shawn's order, 2026-11-02):** before ANY design work, read `~/workspace/team-nitro/THE-PLAYBOOK.md` (the HOW) and `~/workspace/team-nitro/DESIGN-INTELLIGENCE-REPORT.md` (the WHY). Before ANY system work, also read `~/workspace/team-nitro/THE-ANATOMY-OF-A-SMART-APP-PAGE.md` (the MAP) with `~/workspace/team-nitro/THE-HEART-OF-THE-MACHINE.md` (the WHY the map works). Every seat brief names `~/workspace/team-nitro/THE-ULTIMATE-ORIENTATION.md` and `THE-ANATOMY-OF-A-SMART-APP-PAGE.md`.

---

## 9. HONEST GAPS — WHAT THE SOURCES DO NOT DEFINE

Stated plainly. None of these is invented here. Each one is for Shawn's eye, or for a later round, to close. (Act GAPS 1–22 + companion G1–G11, condensed; the Act's full gap list is in the Act file.)

1. **Elevators, enhancers, pinnacle points.** Shawn's terms (00:13Z). No canon source defines them. Their definitions come from him.
2. **Tone assignment.** No mapping from the note's tone field to a board colour — what tone each colour MEANS is not defined.
3. **Date composition.** Two forms coexist; the exact composition is not pinned to one function.
4. **Do the five layers walk the spectrum?** Undecided — the layer colours do not follow any single spectrum order, and the board's jewel, the layers' borders, and the layers' jewels use different colours for the same layer.
5. **Content length rules.** No length rule for any section. The 600-character nutshell slice exists in code only.
6. **Door law for icons/orbs.** "Every number is a door" is law for numbers; whether icons and orbs follow the same law is a behavior claim, not a stated law.
7. **"Active intelligence" as a measurable state.** No source defines what the machine measures for "active."
8. **Canonical board-title size.** Three competing rules; Shawn: not massive. No single canonical value.
9. **Elevated nutshell — exact construction.** The law says the nutshell layer is an elevated board, but no source gives its exact border, shadow, and lift values.
10. **No single canonical hex set.** Same hue names, different hexes (§1.5). Needs Shawn's stamp.
11. **Voice font.** Cormorant (teaching) vs Georgia/Newsreader (specimens). Open reconciliation in DESIGN-LAWS.md.
12. **Type hierarchy.** Playbook sizes (12/14/16/20/28/48) vs Design Laws (24/18/14). Different systems; needs reconciliation.
13. **The 24h birth-expiry question.** Does the ×2 birth multiplier expire after 24 hours? Code applies ×2 unconditionally; only comments claim "first 24h." Shawn must rule.
14. **Section vs page vs board boundary.** The sources use all three terms. No precise definition of where a section ends and a page or a board begins.
15. **Smart Link, Smart List, Smart Mail visual specs.** Named in the Protocol and in PI, but their visual rules (sizes, colors, states) are not in the canon design docs.
16. **Orb geometry spec.** Orb colours and point values are locked, but orb size, glow radius, and orbit geometry live in code, not in the canon docs.
17. **The 416 unverified piece IDs.** The canonical piece index (§6.3): 571 unique IDs, of which 416 are unverified (413 retired + 3 verified-not-canonical). They are never canonical — do not use them as canonical pieces. Re-verification of any one of them is a separate round, against the canonical index.
18. **Quarantined IDs, never use:** NAYA-NAV-001, NAYA-NAV-007, NAYA-TYP-001, NAYA-TYP-002, NAYA-TYP-007, NAYA-TYP-008.
19. **The Act is DRAFT.** Official only on Shawn's word. The NIA Design Contract question (whether V1 or the DRAFT is the document he means) is for his word, not the drafter's.
20. **Power's study gaps (carried from §3):** no site footer on pricing; truncated audience lines; no $0 for Free; vague Max-only cells; digit-tile numbers; static light on slow scroll; proof by click still owed (button function not click-proven, checkout journey unclaimed).
21. **Closed gaps (recorded so no one re-opens them):** the companion draft exists and its rules are folded into Act §5; the NIA Code DRAFT exists on main; the ultimate templates exist in the working Factory; the signature-piece inventory exists; the must-read (`BRAIN/00-ACTIVATION/READ-ME-FIRST.md`) and the activation (`BRAIN/00-ACTIVATION/DESIGN-ACTIVATION.md`) exist on main, both linking the Act as DRAFT.

---

## 10. CONFLICTS — WHERE TWO SOURCES DISAGREE

Both sides reported. None resolved silently. (Act CONFLICTS 1–17 + companion C1–C10, condensed; the Act's full conflict list is in the Act file.)

1. **Hex drift.** Same hue names, different hexes (§1.5). Needs Shawn's stamp.
2. **One layer, two colors in the same file.** The layer's border/glow colour (Hub variables) disagrees on EVERY layer with the layer's jewel colour (`layerColorFor` / `LAYER_COLORS`). Screenshots show the icons following the jewel map. Which map is "the layer's colour" is undecided.
3. **Spectrum order — two (three) different sequences.** Anatomy + Playbook: purple → blue → green → gold → orange → red → magenta. DESIGN-LAWS wheel: magenta → purple → indigo → blue → emerald → green → lime → gold → orange → red → pink. Hub board rotation: "purple → sapphire → emerald." All claim to be "the spectrum, in order."
4. **Type hierarchy.** Playbook 12/14/16/20/28/48 vs Design Laws 24/18/14.
5. **Voice font.** Cormorant vs Georgia/Newsreader.
6. **Title size — three competing `.ib-title` rules.** (a) `clamp(24px, 2.8vw, 32px)` / 1.12 / 800; (b) `clamp(24px, 3vw, 38px)` / 1.05 / 850; (c) phone `clamp(24px, 6.4vw, 32px)`. Shawn: the title came out massive.
7. **Nutshell presentation — three competing rules plus the v4 override.** (a) 18px / tone left border / tone gradient; (b) bordered `#08080d` box; (c) v4 override: 20px / transparent / no border / no shadow. Plus the label conflict (#12). Live-file check 2026-11-06: the served rule is a fourth variant — the conflict is live.
8. **Text glow — DESIGN-LAWS Law 6 vs Anatomy §1.2.5.** One says text carries glow; the other says only the edge lights. Unresolved.
9. **Chevron: styled vs hidden.** One block styles `.ib-chev`; another sets `display: none`.
10. **Inner-board depth: principle vs code.** Law: a board inside a board rides higher. Code: the inner layer's shadow is SHALLOWER than the outer board's. Either "rides higher" means stacking order, or the code under-delivers the law.
11. **Voice: code vs law.** `.ib-layer-play` + `NayaVoice.play` exist in the file; the law says NO voice anywhere on the board. Still in the served Hub bytes at the 2026-11-06 live-file check.
12. **Nutshell label: two styles.** `.ib-nutshell b` (12px, `#f4f2f7`) vs `.ib-nutshell-label` (11px, tone colour).
13. **The v4 overrides vs the base rules (the live defects).** v4 forces flat black (`#050607 !important`, transparent layers, 20px transparent nutshell/subtitle). The v5 edit (PR #3220) restores the base rules with elevation. Live-file check 2026-11-06: the v4 board-background override appears 4× in the served Hub bytes — not fully removed live.
14. **Nutshell "no box" vs nested-board border — RESOLVED, recorded as an evolution.** "No box" meant no FLAT lighter box; the nutshell LAYER is an elevated board, its TEXT stays 20px white. The flat box stays forbidden; the elevated board is required.
15. **Strip vs walk — RESOLVED 2026-10-16.** Two instruments, not a conflict: the Walk and the Strip both draw from the one wheel.
16. **Birth as flat 75 vs ×2 — code inconsistency, flagged not fixed.** A dashboard derivation sheet treats birth as a flat 75, contradicting the ×2 canon.
17. **Orb colours — the Playbook map vs the live dashboard code.** Three orbs rotate (Creating orange/green, Shares green/gold, Comments gold/orange). The Act's entry 05 uses the Playbook map and flags this; the live dashboard shows the other map. Which one is canonical is for Shawn's eye.
18. **Factory conflicts (from `~/workspace/smart-factory/INVENTORY.md`):** C-ORB-17 (same as #17 — touches piece 05). C-NOTES-HEX — Notes orb is `#3fb8ff` in both Playbook and live code; the working record's `#3a5bff` appears in neither as the orb colour (it appears as the notes accent in the notes drill-down — a later-build usage, not the orb). C-BOARD-RADIUS — Act says 24px, Hub ships 26px (touches piece 02). C-CONTRACT-NAME — the Naya Design Contract V1 exists, but no file says "NIA Design Contract" — whether V1 IS the document Shawn means is Shawn's word.

**Note on the old "spectrum count" conflict:** the Playbook lists 7 spectrum colours; DESIGN-LAWS lists 11 stops. The Act uses the 11-stop wheel and the 9-orb set (Saves, `#c9a0ff`, 2 pts, added after the Playbook was written) and flags the Playbook as stale on this point.

---

## 11. SOURCES — WHERE EVERY CLAIM COMES FROM

**Read in full for this inventory (2026-11-12):**

- `~/workspace/team-nitro/clarity-confirmation-act-DRAFT-20261106.md` (94,301 B, 615 lines) — the Act, DRAFT. §4 (the 22 elements), §5 (the companion, LAW), §6 (distribution + Factory), GAPS, CONFLICTS, SOURCES, STATUS. GitHub: `BRAIN/10-INTERFACES/CLARITY-CONFIRMATION-ACT-DRAFT-20261106.md`.
- `~/workspace/team-nitro/hub-board-edit/intelligent-block-rules-LAW-20261106.md` — the companion, LAW (ratified 2026-11-06 01:02Z). 11 shared laws, 5 tested denominators, 6 object classes, 13 block sections, 10 conflicts, 11 gaps. GitHub: `BRAIN/10-INTERFACES/INTELLIGENT-BLOCK-RULES-LAW-20261106.md`.
- `~/workspace/team-nitro/THE-PLAYBOOK.md` — Grade 6, locked 2026-11-02, SN-0844. GitHub: `BRAIN/10-INTERFACES/THE-PLAYBOOK.md`.
- `~/workspace/team-nitro/DESIGN-INTELLIGENCE-REPORT.md` — the WHY, SN-0843. GitHub: `BRAIN/10-INTERFACES/DESIGN-INTELLIGENCE-REPORT.md`.
- `~/workspace/team-nitro/THE-ANATOMY-OF-A-SMART-APP-PAGE.md` — the MAP (official 2026-11-11, SN-2655). GitHub: `TEAM-NITRO/THE-ANATOMY-OF-A-SMART-APP-PAGE.md`.
- `~/workspace/team-nitro/THE-HEART-OF-THE-MACHINE.md` (SN-2657, PR #3334) — the psychology, the mission, the heart.
- `~/workspace/team-nitro/THE-ULTIMATE-ORIENTATION.md` (GitHub `TEAM-NITRO/THE-ULTIMATE-ORIENTATION.md`, blob 5ac24744) — given to every agent; also SN-2285/2286/2287.
- `~/workspace/team-nitro/THE-NAYA-BRAND.md` — the brand: real objects, obsidian gloss black, ALL buttons elite and lit the same, every number alive.
- `~/workspace/team-nitro/THE-BULLSEYE.md` — the target.
- `~/workspace/team-nitro/THE-ULTIMATE-WAKE-UP-PROTOCOL.md` — the wake-up.
- `~/workspace/user/files/pricing-page-design-study__1.pdf` — Power's pricing study (read 2026-11-12; full text carried in §3 and elements 01/02/06/11).
- `~/workspace/user/media_library/image/image-5.png` — Shawn's PI Live Wall screenshot (2026-11-12 15:59Z; viewed 2026-11-12; carried in §4).
- `~/workspace/smart-factory/INVENTORY.md` + `inventory.json` — the Factory inventory (22 pieces with harvest sources, 6 templates, 4 conflicts, 3 fixes). Repo twin verified on main (§7).
- `~/workspace/team-nitro/official-navigation/THE-OFFICIAL-NAVIGATION.md` — the navigation standard (110 lines). The root copy is a STALE draft — never used.
- `~/workspace/team-nitro/BRIEF-DESIGN-INVENTORY-20261112.md` — the brief for this round (checker 9/9).

**Verified live / on main for this inventory (2026-11-12 ~16:2xZ):** the 7 library files + the Act + the companion + the Playbook + the Intelligence Report + the Anatomy + the Brand + the Bullseye + the Heart + the Orientation + the Wake-Up Protocol (all test-`f` OK); the signature-pieces directory on GitHub main (22 pieces + tokens + INVENTORY.md sha `84aacdb1…`, 30,326 B); the six live URLs in §7 (pricing ×2, Personal, Hub, Dashboard, login) + PI unreachable (recorded honestly); the canonical piece index census via PR #2849's merged record (571 = 154 + 1 + 3 + 413).

**Not re-read in this round (cited via the Act and the Factory inventory, not re-verified):** `DESIGN-LAWS.md`, `laws/THE-REAL-OBJECT-LAW.md`, `NAYA-PROTOCOL.md`, the essence notes (`ESSENCE-01…07.md`), `NAYA-DESIGN-ANATOMY-2026-10-31.md`. Their substance is carried through the Act's §4 and the companion, both read in full. A later round that needs a line-level citation from any of them reads the file itself.

---

## 12. STATUS — WHAT THIS DOCUMENT IS AND WHAT HAPPENS NEXT

**This is OFFICIAL.** It was ratified by Shawn Vibert, 2026-11-12 16:39:37Z, by his tap 'Yes — stamp it official.' Nothing in it is declared law by the drafter beyond what he ratified. It was compiled harvest-only from the sources in §11; every claim carries its source; gaps are listed, not filled; conflicts are reported, not resolved. One part is already law: the Intelligent Block Rules (§1.3, §2 element 03) were ratified by Shawn's "1000% YES!" on 2026-11-06. The Clarity Confirmation Act it is built on remains DRAFT.

**Where it lives:** filed on branch `design/inventory-20261112` as `BRAIN/10-INTERFACES/THE-OFFICIAL-NAYA-DESIGN-INVENTORY.md` (this file, byte-identical local twin at `~/workspace/team-nitro/design-inventory-20261112/THE-OFFICIAL-NAYA-DESIGN-INVENTORY.md`). Linked from the Factory's store list: one line added to `~/workspace/smart-factory/INVENTORY.md`:

> - **The Official Naya Design Inventory (OFFICIAL — ratified by Shawn Vibert, 2026-11-12 16:39:37Z):** `BRAIN/10-INTERFACES/THE-OFFICIAL-NAYA-DESIGN-INVENTORY.md` — the one canonical spec: the Act's 22 elements with situation + live example + code-grab path each, Power's pricing grammar, the PI Live Wall board language, cover → menu → page, the Smart Organizer, the 7 libraries, the training programme, honest gaps and conflicts. Branch `design/inventory-20261112`. Local twin: `~/workspace/team-nitro/design-inventory-20261112/THE-OFFICIAL-NAYA-DESIGN-INVENTORY.md`.

**What happens next, on his word:**

1. He reads it and corrects it — his eye is the final compile step, and it outranks every line in this document.
2. It is filed on main (the maker merges after the captain's double-check; this round files on the branch only — no merge, no PR, no main writes beyond the branch filing, no live edits).
3. It is given to all the NIAs with the links — the Act, the companion, the canon sources, the Factory pieces.
4. Its measurable rules are CODED into the build systems as gates — the formula made inevitable. Judgment-only rules stay judgment — his eye — and are never faked into a measurement.
5. The Smart Organizer round follows (queued): harvest the Hub's smart-tabs code verbatim, make the tab buttons 10/10 and OFFICIAL for the whole network, plug them into Personal / Business / Space.

**How this inventory updates:** the same way the Playbook updates. Shawn corrects, the correction is written down in the right section with its source, and the document is filed again. The inventory is living — it grows as the work grows. What never changes: the fingerprint, the light source, white text, his eye wins.

*Absolute clarity, forevermore — that is what this inventory is for, and that is how it will be judged.*

*Compiled 2026-11-12 by the design-inventory seat (Team Nitro, single agent, harvest-only). For Shawn's eye.*
