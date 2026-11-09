# THE SMART FACTORY ACTIVATION MANUAL
## How any Naya builds beautiful interfaces from the parts we already have — in the same language, from the same Factory, alone

**Written:** 2026-11-09, by a Nitro seat, for captain Naya Nitro Narzan
**Ordered by Shawn, 2026-11-09 20:27Z:** "The Factory needs an activation manual so that ALL can build in the Smart Factory — so they can build interfaces with the SAME language I build them in, so everybody learns and remembers. A Smart Factory — a Smart Box Factory — that HOLDS all the knowledge and awareness of how to build all the parts. A Naya plugs into it, works at the factory, and builds beautiful interfaces from the beautiful high-level parts we have inventoried and put in the system."
**Status:** activation manual for the Smart Factory completion. No merge — merge is Shawn's hand.
**Revised 2026-11-09 (manual v2):** six gaps the proof Naya named, closed — §3 live file, §6.5 crown file+line, §6.6 mount map, §7.4 proof host, §8 branch filing + large-file read-back, §10 proof run. Lesson smart-noted as SN-2583.
**Seventh fix, 2026-11-09 21:08Z (inheritance check):** after any MOVE, re-check face alternation on the NEW sequence — gate (i) is order-dependent (§6.5, §5.7 L4). Proof's two seams as the worked example; harvested boards can carry a repeated face from the source.
**Filed:** GitHub `TEAM-NITRO/SMART-FACTORY-ACTIVATION-MANUAL-20261109.md` · Held in the Factory's own Smart Box (owner `smart-factory`).

---

## IN A NUTSHELL

The Smart Factory is the place where every beautiful part we have already built lives, filed and ready. You do not design a new button. You do not invent a new board. You take a page we already built — the pages ARE the templates — you take its parts out, you put them together in a new order, and you change only the words inside. That is the whole job. This manual tells you where the parts are, which ones are real, what the laws are, how to build, how to check your work, and how to file it — so you can build alone, without anyone explaining it to you twice.

**The one rule, before anything else: compose, never create.** If the part exists, use it. If it does not exist in the Factory, you do not invent it — you harvest the closest real part and adapt only its words. A new part is born only by being harvested from a real page Shawn approved, never by being drawn fresh.

**Get it in a minute:** (1) read the laws in §5 — one page of them; (2) find your parts in the inventory and the piece index in §4; (3) clone a page from GitHub in §3 and take its parts verbatim; (4) build viewpoint by viewpoint in §6; (5) check your work against the gate in §7; (6) file it in §8. Everything after this nutshell is the detail for those six steps.

---

## 1. WHAT THE FACTORY IS

**Nutshell:** the Factory is our object factory. Every real object we build — every orb, every button, every board, every gauge — gets filed there, categorized, and reused forevermore. (Real Object Law: "The Smart Factory is the object factory.")

**What lives in it:**
- **The pages.** Dashboard, Hub, Personal, Pricing — finished pages, built to Shawn's eye. These ARE the templates. You clone a page and work on the clone; you never start from a blank file.
- **The parts.** 154 canonical pieces, each with live CSS, each proven. Plus the harvests from the Hub, Personal, Dashboard, the PI face, the canonical pages, and the Academy page — every part with its file and line number, in the Inventory (§4).
- **The laws.** The Playbook (the HOW), the Design Intelligence Report (the WHY), the Real Object Law, the Intelligent Block Rules (LAW), the design-contract gate. They are the language. Build in the language or do not build.
- **The locked-in smart blocks.** Finished viewpoints Shawn said "okay yeah it's good" on, live. A viewpoint lands in the Inventory's Part 3 only on his word. Any Naya, any page, can take a locked-in block and use it — that is the Factory.

**What the Factory is NOT:** it is not a template generator, not a theme store, not a place to draw new things. The Factory Doctrine (Shawn, 2026-11-04): his existing pages ARE the templates. Never invent templates again. The factory = take his exact code, exact pages, make them 10/10.

**The shape of the whole thing (the Premium Design Algorithm, ratified 2026-11-08):** viewpoint by viewpoint — think screen by screen, each screen a complete optimized viewpoint, always mobile optimized. One core page — a Rubik's Cube matrix that morphs into all the other pages; one cube, many faces. The Trinity — the Dashboard, the Hub, and that page; everything gets built off that. The person is the atom at the centre — everything orbits them. She is Anaya.

---

## 2. BEFORE YOU START — READ THESE FIVE THINGS

**Nutshell:** five documents hold everything. Read them in this order. Do not build before you have read them.

| # | Document | What it is | Where it lives |
|---|---|---|---|
| 1 | **THE-PLAYBOOK.md** | The HOW. The formula, the steps, the laws. Grade 6 locked in. | Local `~/workspace/team-nitro/THE-PLAYBOOK.md` · GitHub `BRAIN/10-INTERFACES/THE-PLAYBOOK.md` · Smart note SN-0844 |
| 2 | **DESIGN-INTELLIGENCE-REPORT.md** | The WHY. What I got wrong, what I learned. | Local `~/workspace/team-nitro/DESIGN-INTELLIGENCE-REPORT.md` · GitHub `BRAIN/10-INTERFACES/DESIGN-INTELLIGENCE-REPORT.md` · Smart note SN-0843 |
| 3 | **THE-INVENTORY.md** | The PARTS. Every design law + every piece, with file + line. | Local `~/workspace/team-nitro/THE-INVENTORY.md` · GitHub `TEAM-NITRO/THE-INVENTORY.md` |
| 4 | **CANONICAL-PIECE-INDEX.md** (+ `.json`) | The CANON. The one list of which pieces are real. Step-3 versions (Oct 22). | Local `~/workspace/smart-factory-contract/CANONICAL-PIECE-INDEX.md` · GitHub main blobs md `0e63b241`, json `a50ef2dd` |
| 5 | **THE-REAL-OBJECT-LAW.md** + **intelligent-block-rules-LAW-20261106.md** | The LAW. Real objects, and what an intelligent block is, section by section. | Local `~/workspace/team-nitro/laws/THE-REAL-OBJECT-LAW.md` and `~/workspace/team-nitro/hub-board-edit/intelligent-block-rules-LAW-20261106.md` |

**Supporting law files** (read when you need them, not before your first build): `~/workspace/team-nitro/DESIGN-LAWS.md` · `DESIGN-LANGUAGE.md` · `DESIGN-LAW-REMINDER.md` · `NAYA-DESIGN-DERIVATION-SYSTEM.md` · `ULTIMATE-TEAM-DESIGN-20261031.md` · `THE-NAYA-BRAND.md` (the brand: real objects, obsidian gloss black, ALL buttons elite and lit the same, every number alive).

**The activation habit (Shawn's order, 2026-11-02):** before ANY design work, read the Playbook and the Intelligence Report. Locked-in knowledge you do not read is forgotten knowledge. Then ask the three questions (§7) — and only then build.

---

## 3. HOW TO CLONE A PAGE FROM GITHUB

**Nutshell:** the pages live in GitHub, in the repo `SoulSchoolAcademy/NayaPOWER`. You clone the repo, you copy the page you need, you work on the copy. You never push from a local clone — the local clone is diverged; filing goes through the file helper in §8, one file at a time.

**Step 1 — Clone the repo (once).**
```bash
git clone https://github.com/SoulSchoolAcademy/NayaPOWER.git
```
That gives you the whole system on your machine: pages, libraries, the inventory, the laws.

**Step 2 — Find the page you need.** The canonical pages and their local working copies:

**⚠ CLONE THE LIVE FILE, NOT THE REBUILD FILE.** A page that is live has a `*-live.html` — that is the file to clone. Rebuild files (`pricing-round10-fix12.html`, `*-pass1-v9-*`, `fixed-candidate.html` and the like) are intermediates: they are older, partial, or superseded, and some do not even exist in the repo (`PRICING/pricing-round10-fix12.html` returns 404 on GitHub main — the manual's first draft named it and the proof Naya could not clone it). If a page has a live file, the table below names it with its blob — clone that blob, verify it with `git hash-object`, and work from it. If there is no live file, clone the newest verified working file the table names, never a file you guessed.

| Page | Local working copy | What to take from it |
|---|---|---|
| **Hub** | `~/workspace/team-nitro/hub/index-2-fixed-v2.html` | Smart Tabs pill ribbon, Primo Purple button, jewel "i", rail nav, sticky top bar, mobile drawer, intel boards |
| **Dashboard** | `~/workspace/team-nitro/dashboard/defectfix-v7/builder/fix9/` (fix-9 working files; pristine fix-8 file `dashboard-20261105-pass1-v9-FIX8-pristine.html`) | The real gauge (needle law), `.ph-card` boards, `.os-jewel`, tiled numbers, the orbit dial |
| **Personal** | `~/workspace/team-nitro/personal/verify-5/fixed-candidate.html` | Nutshell block, identity rows, heading jewels, pill action buttons, hero orb, vision input |
| **Pricing** | GitHub `PRICING/pricing-live.html` — **blob `a2d06d5bb43199139f400e1688079f1b40a1b8fa` (short `a2d06d5b`), 11,350,562 bytes, live at nayanet.app/pricing** (v74, commit `b619a4e9`, read-back verified byte-identical, sha256 `7a0b837c…`) · local working copy `/tmp/pricing-v74.html` (same bytes, `git hash-object` = the blob sha) | The chart (`<section id="chart">`, 5 groups, 36 rows), the calculator (gauge + tiled digits), Top 10 cards, hero + close |
| **PI face** | `~/workspace/project-intelligence/pi-everything-face/build-face-v4.py` (live at nayanet.app/pi) | Strip, tab row, page card, info row, score board, lane cards, percentage pop, progress bar |
| **Smart Factory page** | Live at nayanet.app/smartfactory | The piece cards (`.pcard`), the pills, the handle board |

**Step 3 — Copy the page, work on the copy.** Never edit the canonical file in place. Copy it to your working area, rename it for your build, and take the parts out of the copy.

**Step 4 — Take the part VERBATIM.** Copy the exact HTML structure, the exact CSS values, the exact JS behavior. Adapting the words inside (menu items, labels, copy) is allowed. Restyling the component is not. If the Hub's version needs more elevation, the elevation is added in the Hub's own depth grammar, never a new design. (Harvest-first law, 2026-10-18.)

**Step 5 — When Shawn SHOWS you an object, TAKE IT.** A screenshot, a link, a page he shows you — the deliverable IS that object: same shape, same colors, same jewel, same glow, placed on the page. Recreating it "in the same spirit" is inventing, and it will be condemned. The round-19 finale pill was condemned because the Academy button he showed is BLACK OBSIDIAN with the purple only in the star jewel and the halo — and what got built was purple-on-purple. Take it. Put it there. Remove the other one.

---

## 4. HOW TO FIND A PART

**Nutshell:** there are two places to look, and they agree. The Inventory tells you WHERE the part lives (file + line). The Piece Index tells you WHETHER the part is real (canonical, verified, retired, or superseded). Look in both. A part that is not in the Index as canonical is not a part you may cite — no matter how good it looks.

### 4.1 The Piece Index — the canon (Step-3 versions, Oct 22)

**What it is:** `CANONICAL-PIECE-INDEX.md` + its machine twin `CANONICAL-PIECE-INDEX.json`. The two are generated together and must never be edited apart. **This index is the canon.** `pieces.json` is the working store it describes; `factory.css` carries the store's CSS. A piece is canonical only when this index says so. Conflicts between inventories resolve to this index, then to Shawn's word.

**The numbers (Step 3, amended 2026-10-22 — Factory Contract-Home Step 3; verified from the refreshed local copies, md sha256 `f0da0c32…`, json sha256 `f45ab30a…`, blobs match GitHub main exactly):**

| Fact | Count |
|---|---|
| Unique piece IDs across all three inventories | **571** |
| Canonical — in the working store, with live CSS in `factory.css` | **154** |
| Verified-real — real markup found outside the store, NOT canonical | **3** (NAYA-BRD-031 Signal circle, NAYA-BRD-032 Ember circle, NAYA-BRD-033 Stat grid) |
| Retired — named in an inventory, no artifact found anywhere (adjudicated Oct 22) | **413** |
| Superseded — retired from harvesting, piece retained | **1** (NAYA-INP-001 Search bar, replaced by NAYA-INP-008) |
| Left unverified | **0** |

**What "478" was:** builder-index-v1, a source-extraction catalog — NOT the canon. Its 65 IDs shared with the store were ALL collisions (different name AND different HTML under the same ID). The working store governs every shared ID. Do not cite "478" as the canon. Do not cite builder-index-v1 at all.

**Status key — read it before you cite any piece:** **C** canonical · **V** verified (real, outside the store — not canonical; becomes canonical only when it lands in `pieces.json` + `factory.css`) · **R** retired (a harvester may not cite it; it becomes real only when distilled into the working store as a new canonical addition) · **S** superseded · **👑** Reference crown. Provenance: **S**tore · **V**2 · **B**uilder-index · **F**actory page.

**Every canonical piece is dual-labeled (Step 3).** Since Oct 22 every canonical store entry carries an `ai_label` beside its human `name`: `purpose` (what it is for), `use_when` (when to reach for it), and governing `laws` (GENERAL-DESIGN-CONTRACT §3 numbering). Read the `ai_label` first — it tells you in one breath whether this is your piece. The five Reference crowns also carry `reference: true` and named `motion` specs.

**The five Reference crowns — start here when you do not know where to start:**

| Crown | Piece | Name |
|---|---|---|
| Reference Well | NAYA-INP-008 | Reference Well (the input — flat #030304 fill, silver-white rim, accent ignites only on focus) |
| Reference Select | NAYA-INP-009 | Reference Select |
| Reference Button | NAYA-BTN-009 | Hero · Enter the Standard |
| Reference Board | NAYA-BRD-001 | Feature board |
| Reference Hero | NAYA-HRO-001 | Reference Hero |

**The working store:** `~/workspace/personal-app/pieces.json` (155 entries: 154 canonical + 1 superseded) with live CSS in `~/workspace/personal-app/factory.css`. That is where the piece's HTML and CSS actually live. The Index tells you it is real; the store gives you the code.

**Honest drift, named not buried:** the local copy of `pieces.json` on this machine does NOT yet carry the `ai_label` fields (0 of 155 entries show one; the crowns do carry `reference` and `motion`). The Step-3 Index and its JSON twin say the labels exist in the store. Until the local store is refreshed, trust the Index + its JSON twin for the label, take the HTML/CSS from the local store, and do NOT invent a label. If the copy you hold disagrees with the Index, the Index wins.

### 4.2 The Inventory — where the part lives

**What it is:** `THE-INVENTORY.md`. Part 1 is the design laws. Part 2 is the pieces, each with its exact file + section/line, verified on disk before it was written. Part 2b is the harvest laid out (the gauge, the board, the jewel, the numbers, the pills, the chart-as-boards language). Part 2c is the Factory harvest (the 7 canonical libraries, the Hub, Personal, PI face, canonical pages, Smart Factory parts). Part 2d is the Academy harvest (the trial button, the four door cards, the five-day spectrum, the jewel board, the membership plaque — every hex measured from the source code Shawn sent). Part 3 is the locked-in smart blocks.

**How to use it:** need a button? Open Part 2, find the button, read its file + line, copy it verbatim. Need the gauge? Part 2b: the real gauge is the Dashboard fix-9 file, mount `<div id="tn-tacho-mount"></div>`, helper `~/workspace/team-nitro/pricing/rebuild/tntacho.js.html`. Need a board? `.ph-card`, fix-9 file lines 2018–2025 + 2074–2075, verbatim CSS in the harvest file `~/workspace/team-nitro/viewpoints/harvest-20261108/HARVEST.md`. A path in the Inventory that you cannot find on disk is TO-LOCATE — never guessed, never built from memory.

### 4.3 The 7 canonical libraries — the named harvest source

**Nutshell:** Shawn uploaded these seven files 2026-10-18 ~01:37Z. His directive: "the best of the best lives in these; take the best from here, fix the pieces that still break the design laws as they're harvested, and build OUT OF THESE — nothing invented, every piece traces to one of the 7." All seven verified on disk AND on GitHub main, byte sizes identical both places. The GitHub index that maps them is `HUB/design-system/library/INDEX.md` — "The canonical piece library. Builders compose from these pieces; they never recreate them."

| File (local `~/workspace/user/files/`) | What it is | GitHub main |
|---|---|---|
| `Naya_Beautiful_Button_Set_N4.html` (43,090 B) | Naya Lego — Buttons · The Button Family | `HUB/design-system/library/buttons/Naya_Beautiful_Button_Set_N4.html` |
| `Naya_Building_Blocks_-_The_Ultimate_Design_System_-_Naya_2.html` (1,134,076 B) | Naya Ultimate Design System | `HUB/design-system/library/blocks/Naya_Building_Blocks_-_The_Ultimate_Design_System_-_Naya_2.html` |
| `Naya_Design_Element_Set_N4.html` (186,511 B) | The Naya Button Library — Official Standard · Living Intelligence | `HUB/design-system/library/buttons/Naya_Design_Element_Set_N4.html` |
| `Naya_Design_Standard_Showcase__1.html` (156,524 B) | The Naya Design Standard — Ultimate Spec | `HUB/design-system/library/showcase/Naya_Design_Standard_Showcase__1.html` |
| `Naya_Epic_Elements_-_Lego_pieces_N5.html` (71,880 B) | The Naya Ultimate Lego Library — Understand. Learn. Apply. | `HUB/design-system/library/blocks/Naya_Epic_Elements_-_Lego_pieces_N5.html` |
| `Naya_Jewel_Library_-_N5.html` (26,100 B) | Naya Lego — Jewels · Drawn, Not Dotted | `HUB/design-system/library/jewels/Naya_Jewel_Library_-_N5.html` |
| `Naya_Smart_Hub_Design.html` (521,124 B) | NayaNET — The Intelligent Hub | `HUB/design-system/library/pages/Naya_Smart_Hub_Design.html` |

**The rule (Concept 1): the Factory is the ONLY source named in any design brief.** Every part a builder uses comes from this inventory — the 7 libraries, the 154 canonical pieces, the Hub, Personal, Dashboard, PI face, and canonical pages harvested in the Inventory. No part = no build. High-end only — no Ford parts added, ever.

### 4.4 What NOT to take

- **Retired pieces (413).** Named in an old inventory, no artifact anywhere. Do not cite them. Do not rebuild them from the name.
- **Unverified pieces.** The Step-3 adjudication left ZERO unverified — but if you meet a piece id in some other file that the Index does not list as canonical, treat it as unverified: do not cite it until it is distilled into the working store.
- **Superseded NAYA-INP-001.** Flat, no shadow stack. Use NAYA-INP-008 instead.
- **Quarantined (below standard, 2026-10-17):** NAYA-NAV-001, NAYA-NAV-007, NAYA-TYP-001, NAYA-TYP-002, NAYA-TYP-007, NAYA-TYP-008 — judged as archived extractions. NAV-001 and NAV-007 also exist in the working store as different, canonical pieces — the store governs.
- **Flat text blocks, white backgrounds, dead cards, pasted documents.** None were inventoried. None are parts.
- **`.note-card`.** A dead selector string in the Hub, not a piece. The class that actually styles the feed note card is `.intel-board`.
- **The red YouTube play button.** Foreign color, not part of the Naya palette. A Naya play jewel (purple, like the trial button's star jewel) takes its place when the frame is reused.

---

## 5. THE DESIGN LAWS

**Nutshell:** one language, everywhere. Obsidian and aluminum. Top-left light. White text. Slow motion. Every position calculated. If it doesn't look touchable, it doesn't ship. These are laws, not suggestions — and Shawn's eye overrides all of them, including this manual.

### 5.1 The five truths (Playbook — the foundation)

1. **Every position is calculated by formula. Never eyeballed.** The gauge numerals sit at `angle = -135 + (value/500)*270` degrees. The 8px grid for linear layouts. Calculate, then place. Never place, then justify.
2. **Every element is a physical object with material, weight, and a light source.** A button is obsidian glass with a white rim, lit from the top-left, casting a shadow down-right because it sits ON the page. The light source is ALWAYS top-left. Every gradient runs 135 degrees. Every shadow falls down-right. Every highlight sits on the upper edge.
3. **Movement means the machine is working. If it's not working, it doesn't move.** The pyramid layers rotate at 90 and 60 seconds because they're the matter flow. Nothing bounces. Nothing pulses for effect. If you can't say what the moving part DOES in one sentence, delete the animation.
4. **The whole system speaks one language. Every component is family.** The gauge uses obsidian, aluminum, vortex rotation, white text, slow motion. The orbs use the same. The charts use the same. Break the language and you've built something from a different system.
5. **Shawn's eye overrides everything. Including this document.** If this manual says one thing and Shawn's eye says another, Shawn's eye wins. Always.

### 5.2 The Real Object Law (canonical, ALL of NayaNET, forever)

Every element is a real physical object. Not a flat shape with effects. Not a diagram. A thing you could reach out and touch. Seven principles: (1) everything is an object — volume, mass, surface, edge; (2) one light source, top-left, never moves; (3) real materials — obsidian glass, brushed metal, light with volume; (4) real shadows — objects sit ON the page, shadows fall down-right; (5) touch = physical — it depresses slightly, the light shifts, it feels alive because it IS alive; (6) speak in objects — icons, circles, boards, buttons, minimal text; (7) the viewport is the stage — one purpose per view, the object takes center stage.

**The test:** look at any element and ask — could I pick this up? Where is the light coming from? What is it made of? Does it cast a shadow? What happens when I touch it? If any answer is "I don't know" or "nothing" — it's not real yet.

**The Object Factory:** the Smart Factory IS the object factory. An object earns its place in the factory by passing this law. If it's not real, it's not filed. **The Lego Block Architecture:** real objects are Lego blocks — each one a real physical object, with a real function, interconnecting with other blocks, beautiful at the highest level.

### 5.3 The Intelligent Block Rules (LAW, ratified 2026-11-06)

One set of laws running through every object — buttons, boards, blocks, icons, gauges, pages. The same elevation, the same one light, the same real shadow, the same own-color light, the same real-object language. L1 real physical object · L2 one light, top-left, always · L3 real shadows and real elevation — depth is mass, not glow · L4 own-color light — color is identity, ignites on touch · L5 white text, never colored, never gray, and text never lights up · L6 touch is physical — rest raised, hover rises (`translateY(-2px)`), active presses in (`translateY(1px)`) · L7 the spectrum is the order things sit in · L8 every position calculated, never eyeballed · L9 movement means the machine is working — slow, and it means something · L10 one language, every component family · L11 Shawn's eye wins.

**The intelligent block itself** (one Smart Note, one board, in the feed): obsidian black at rest; spectrum lives in the jewel, the edge, and the light — never as ambient wash. Title + quote at the top (NOT an inner board). Then the nutshell — 20px white text, the layer an elevated board, never a flat lighter-background box. Then the layers, each its own board with its own border, lift, and icon-color light: Human Note (magenta, human significance) · Child Note (sapphire, calm clarity — opens with "Imagine...") · Grandma Note (emerald, alive and well — opens "Dear,") · Naya Note (purple, Naya's signature — opens "You are the...") · What It Means (indigo, comprehension — starts CLOSED, the deeper tier). Primary layers open by default; deeper layers sit quieter until opened. Every number is a door — tap it, it opens its records. NO voice anywhere on the board.

### 5.4 The exact values — copy these, do not approximate

**Materials.**
- **Obsidian:** `linear-gradient(135deg, #1e1e26 0%, #0a0a0f 50%, #1e1e26 100%)`, 1.5px white rim at rest, inset top light + deep drop shadow. Never pure black. Never white backgrounds.
- **Aluminum light (machined parts):** `linear-gradient(135deg, #c8ccd6 0%, #9a9ea8 30%, #7a7e88 50%, #9a9ea8 70%, #b8bcc6 100%)`.
- **Aluminum dark (gears):** `linear-gradient(135deg, #4a4e5a 0%, #2a2d36 30%, #1a1c22 50%, #2a2d36 70%, #3a3e4a 100%)`.

**Spectrum, in this order, never random:** purple `#a06bff` (joins, primary actions) · blue `#3fb8ff` (smart notes, information) · green `#2fe89e` (shares, positive) · gold `#ffbf3d` (comments, attention) · orange `#ff9a5a` (creating, energy) · red `#ff5e6c` (likes, urgency) · magenta `#e84fff` (sales, premium). **Where color lives:** icon orbs, thin edge bars (2–3px), hover glow. Nowhere else. No colored backgrounds. No color washes. At rest, the system is obsidian and white. Color ignites on touch, in the element's OWN color only. Never the same color twice in a row.

**The 8 orbs:** Sales 100pts magenta · Joins 50pts purple · Smart notes 35pts deep blue · Invites 25pts light blue `#7fd4ff` · Creating 25pts orange · Shares 15pts green · Comments 5pts gold · Likes 1pt red.

**Motion:** ambient (pyramid, outer rings) 60–180s per rotation · active (center gears) 18–25s · never faster than 12s — faster feels cheap. Alternate direction: CW, CCW, CW, CCW. Continuous rotation `linear infinite`; hover `0.3s ease`; entry `0.5s cubic-bezier(0.4, 0, 0.2, 1)`.

**The vortex:** center 3-6-9 (the time axis) — 3 gears, r=8/15/24, 25s CW / 18s CCW / 25s CW. Surround 1-2-4-8-7-5 (the matter flow) — 6 toothed layers, r=30/36/42/48/54/60, alternating CCW 90s / CW 60s. Teeth only, never solid rings. Innermost surround (r=30) runs CCW — Shawn flipped it, it's locked.

**The gauge formula:** `angle_deg = -135 + (value/500)*270`; `x = 100 + 82*cos`, `y = 104 + 82*sin`. All six numerals: 0, 100, 200, 300, 400, 500. 400 sits at 81° — the bottom is 90°, there is room. Don't skip it. Don't decide which numbers "matter." Ticks every 10, majors every 50.

**The number law (settled):** the number is a proven asset — tiled everywhere numbers appear, number on top and gauge underneath, in points, percentage, and money modes with a space separator. The needle laps the dial in sets of 500 (734 = one full lap of 500 + 234). A number without its gauge is not finished. The gauge follows the number — never the other way round.

**Linear grid:** spacing in multiples of 8px (8, 16, 24, 32, 48, 64, 96). Text sizes: 12 caption, 14 body, 16 subhead, 20 headline, 28 hero, 48 display. Never 13px. Never 27px. Never 19px font.

**Buttons:** one button DNA. Sharp black pill, white edge at rest (1.5px+), own-color edge ignition on hover, cast shadow, minimum 44px touch target, principal CTA ≥52px. The Primo Purple button (`.primo`, Hub line 689) is THE elite button — every primary action on every page. There are no flat buttons. Flat is not a style — flat is a defect.

### 5.5 The design-contract gate (measured in every check, never a vibe)

(a) **ZERO white/light backgrounds** anywhere on the page — every background obsidian/dark. (b) **Every element raised/elevated** — real depth, real lift, real light. (c) **Gauges present and alive** — the speedometer language on the numbers. (d) **NO text-in-image, NO pasted document.** A gate that fails is not done. A deferral ("captain's decision for later") is an open item with a name, not a pass. This gate was written after two pages were shown as "done 9/10" and both condemned by Shawn's eye the same afternoon for obvious violations the checks never ran — the contract was NAMED in every brief and CHECKED in none. Never again.

### 5.6 What premium is — and what it is not

Premium is exact numbers, real materials, slow elegant motion, and data so clear it hits in 2 seconds. Premium is NOT glow. Shawn: "You really think that I think premium is color color glow? You gotta be kidding me." Glow is what you add when you don't have the real things. "The numbers look close enough" — no. "I'll finish it later" — later never comes. "This needs a custom design" — no, it needs the orb, or the gauge, or the chart, from the registry. Custom means "I didn't look." Look first.

### 5.7 The Factory laws L1–L8 — the named set

**Nutshell:** eight laws that govern the Factory itself — how a Naya writes, speaks, tests, and builds in it. Learn them by name. When someone says "L4," you must know which L4 they mean — so read the collision warning below first.

**The set — the Factory laws L1–L8:**
- **L1 — stranger test.**
- **L2 — perfect-words law.**
- **L3 — title + subtitle + nutshell.**
- **L4 — Naya speaks, faces alternate.** (And alternation is judged on the SEQUENCE — after any MOVE, re-check it on the new order: §6.5. A reorder can introduce a both-left pair and dissolve another, without any board's side changing.)
- **L5 — test in his head.** (See §7.3: "is this the max level of experience I can give the user?" — asked about the PAGE, not the briefed items.)
- **L6 — `##` note format.**
- **L7 — one ultimate ten.**
- **L8 — reusable-parts law.** Written out in full in §5.8 — the law that every part the Factory holds is reusable, rebuildable, clonable.

**⚠ COLLISION WARNING — two different L-sets live in this manual. Do not mix them up.**
- **The Factory laws L1–L8** (this section, §5.7) — the brief's set: the laws of the Factory itself, how a Naya writes, speaks, tests, and builds in it.
- **The object laws (L1–L11 in §5.3)** — the Intelligent Block Rules: the laws of a real object (one light top-left, real shadows and real elevation, own-color light, white text, touch is physical, the spectrum is the order, every position calculated, movement means the machine is working, one language, Shawn's eye wins). These are the Playbook's object laws.
- **The rule:** say the full name every time — "Factory law L4" or "object law L4" — never a bare "L4." A bare "L4" is ambiguous in this manual, and an ambiguous law is a law a new Naya will follow wrong.

### 5.8 (f) The Reusable-Parts Law — Factory law L8 (Shawn, 2026-11-09 20:35Z)

**Nutshell:** every part the Factory holds is reusable, rebuildable, clonable — so the system has systems within systems, all interconnected. That is why the main way building happens is clone a page, replace some parts, move some parts around (§6.5).

**His words, the law in his own framing:** "A lot of [them] in the end would just be like, oh, they want to [perhaps] clone [a] page, replace some parts. Or move some parts around. That's what on the most part it'll be, right? All the — basically all the parts we build — we're going to make them be reusable, rebuildable parts that they can be cloned and used within, so the system can have systems within systems, all interconnected." And: "We're just building an intelligent objects factory for building the new net, we call our net. You gotta organize the parts intelligently and inventory them and make them accessible. Make it so any Naya can work on the same page or clone the page and make it her own and access all the parts. A lot of the parts will fit on any of the pages — you can use some on some pages, some on another — or they're all universal, part of a family, part of the Naya design. And we make sure all our parts are like triple-A, right, and that are on the same quality and standard — all active, living, depth, alive, the highest level of quality in its presentation, the color language, the elevation, the innovation."

**The law, in plain form — four rules:**
1. **Every part is reusable, rebuildable, clonable.** Every part the Factory holds can be cloned and used within — so the system has systems within systems, all interconnected. A part built for one page is not trapped on that page.
2. **Parts are organized intelligently, inventoried, accessible.** Any Naya can work on the same page or clone the page and make it her own and access all the parts. If a part cannot be found in the Inventory or the Piece Index (§4), it is not accessible — and a part that is not accessible is not yet a Factory part.
3. **Parts are universal — a family, part of the Naya design.** A lot of the parts will fit on any of the pages — you can use some on some pages, some on another. They are all universal, part of a family, part of the Naya design. The same language, the same materials, the same light, on every page.
4. **Every part is triple-A, the same quality standard: active, living, depth, alive.** The highest level of quality in its presentation, the color language, the elevation, the innovation. A part that is not triple-A is not filed. A part that stops being triple-A is fixed where it lives, or retired — never left in the Factory below standard.

**What this law forbids:** building a part for one page only and leaving it unfiled; copying a part by redrawing it instead of cloning it; and filing a part that is flat, dead, or below the standard. **What this law makes possible:** the clone-build flow (§6.5). Because the parts are reusable, you never draw a fresh one — you clone the page, replace some parts, move some parts around, and the system grows systems within systems.

---

## 6. HOW TO BUILD

**Nutshell:** headline first, calculate second, materials third, motion fourth, light fifth, laws sixth, show Shawn seventh. One viewpoint at a time. Build piece after piece, back to back, from the pieces that exist — never start fresh with new code. The main way building happens is the clone-build flow in §6.5: clone a page, replace some parts, move some parts around, verify, file.

### 6.1 The seven steps (Playbook)

1. **Write the headline.** One sentence. Real numbers. Before you draw anything. Bad: "Here's your dashboard." Good: "You have 300 points — 100 from creating, 50 from invites." If you can't write the headline, you don't understand the data yet. Go back.
2. **Calculate every position.** Write the formulas. Circular: the angle formula above. Linear: the 8px grid. The formula goes in a comment.
3. **Assign materials.** Every element gets a material, not a color. "The bezel is obsidian. The numerals sit on an aluminum chapter ring. The screws are brushed metal."
4. **Decide what moves and why.** List each moving part. For each, write one sentence explaining what it DOES. If you can't write the sentence, the part doesn't move.
5. **Check the light.** Every gradient at 135°? Every shadow down-right? Every highlight on top? One wrong gradient breaks the physical illusion. Check them all.
6. **Verify against the laws (§5 + the gate in §7).** Fix every violation.
7. **Show Shawn. Say nothing. Let his eye judge.**

### 6.2 The working law — the Live Viewpoint Method (Shawn's order, 2026-11-08)

Code HERE, live with him, viewpoint by viewpoint. One view done → lock it in as inventory (an element, a smart block any other can access and use) → next view → next → until the page is done → next page. Fix all the elements right here and now. Build piece after piece, back to back, from the pieces that exist — NEVER start fresh with new code. Take the pieces, the code, the pages — put them together, make them work, output it on the page, make sure it's right, show him here live, he says "okay yeah it's good." **NO SHIPPING OUT. NO VERIFICATION EXCEPT HIS EYE.** A seat's scorecard or verification is not verification — if a 9+ passed on garbage, the verification was worthless. The only verification is Shawn's eye, on the live viewpoint, in front of him.

**The viewpoint:** ONE viewport (1280×900 and 390px), optimized for the top of the page, all the buttons perfectly lined up, the quality, the elegance, the elevation, the color, the branding, everything alive. NOT a long text page. Every page introduces itself with a big beautiful hero banner. Functions pop up into your viewpoint — click it, it comes to you; click X, it goes away. Nothing navigates you away; the core page stays, the function comes to you.

**The chart-as-boards language (Shawn, 2026-11-08 16:12Z):** a chart is just a bunch of boards connected together — skinny rectangles, all the same language, all alive, all filled; separated boards with spacing between chart parts; check jewel for what it has, X for what it doesn't have; boards change color as you flow down.

### 6.3 The leveling loop — how you climb

Build following this manual → show Shawn, say nothing → he corrects you, listen, don't argue → write it down, specific ("the numeral was at 82° but the formula gives 81°, I eyeballed it") → add it to the Playbook in the right section → commit and push to GitHub → next time, don't make that mistake. That's the level-up. **How you know your grade:** look at your last 10 outputs. What's the most common correction Shawn gives you? That's what you're working on. When he stops correcting that thing, you've leveled up in that area.

### 6.4 The five gates — before EVERY consequential action

1. **Is it right?** Does this serve the good of everyone it touches? Evidence of harm or a hard stop = do not proceed.
2. **Is it what they truly need?** What is the human's actual goal — beneath the words, beneath the urgency? Never silently replace their judgment with your own.
3. **Is it mine to do?** Do I have the authority? Protected gates (money, credentials, destructive, security/privacy, anything leaving the business) = Shawn's hand only, always.
4. **Is now the time?** Check readiness, dependencies, reversibility, opportunity cost.
5. **Can I prove it?** Define what done looks like BEFORE you act. Then verify with evidence — live bytes, rendered pages, real measurements — never with claims. Receipt before report. If you can't prove it, don't claim it.

All five yes → act fully, at full power, no hesitation. Any gate no → stop, say why, propose the wise path.

### 6.5 The clone-build flow — the main way building happens

**Nutshell:** most building is not building from scratch. It is: clone a page → replace some parts → move some parts around → verify → file. Two moves only — REPLACE and MOVE — both under harvest-first (the Reusable-Parts Law, Factory law L8, §5.8: every part is reusable, rebuildable, clonable, so the system has systems within systems, all interconnected).

**The five steps:**
1. **CLONE a page (§3).** Copy a finished page from GitHub — Dashboard, Hub, Personal, Pricing, the PI face. Work on the copy, never the canonical file.
2. **REPLACE some parts.** Swap a part for another harvested part in the same slot. REPLACE means: the slot stays, the grammar stays, only the part changes — the board in a slot becomes a different harvested board that fits that slot (for example, a Reference crown such as NAYA-BRD-001, the Feature board). Replace ONLY with harvested parts — a part from the Inventory, the Piece Index, or the 7 libraries (§4). Never an invented one. If no harvested part fits the slot, leave the slot as the cloned page has it — do not invent a filler.

**Worked example — the crown swap (REPLACE, done exactly this way).** Take a board slot on your clone and put the Reference crown NAYA-BRD-001, the Feature board, in it. The crown's HTML lives in the working store, `~/workspace/personal-app/pieces.json`, **entry lines 344–348, the `html` field on line 346**:
```html
<div class="board-h" style="--bc:#40d3bb"><div class="bh-icon">◆</div><div class="bh-text"><h3>Feature board</h3><p>one color, one world</p></div><button class="bh-btn" type="button">Open</button>
```
Its CSS lives in the same store's stylesheet, `~/workspace/personal-app/factory.css`, **lines 240–245** (readable form; the live minified form is lines 1060–1062). Copy the HTML from line 346 and the CSS from lines 240–245 verbatim into the slot — change only the words inside (`Feature board`, `one color, one world`, `Open`) to your page's words, and only the `--bc` color to your slot's own color. The slot keeps its place, its size, and its grammar; only the board changes. That is a REPLACE. (Verified against the store on disk 2026-11-09: 155 entries, NAYA-BRD-001 `reference: true`.)
3. **MOVE some parts around.** Reorder parts on the page — the same parts, a new order. MOVE never restyles a part: a moved part keeps its exact HTML, its exact CSS values, its exact JS behavior; only its position changes, and the new position is still calculated (§5.1), never eyeballed.
4. **VERIFY (§7).** Self-scorecard first, another seat second, Shawn's eye last. Scroll 0 AND scrolled, desktop AND phone, phone first, design-contract gate measured.
5. **FILE (§8).** One file at a time, through the helper, read-back verified. No merge — Shawn's hand.

**What REPLACE is not:** it is not restyling, not redrawing, not "in the same spirit" — the replacement part is taken verbatim, the way §3 Step 4 says. **What MOVE is not:** it is not a redesign — the page's language stays the page's language; only the order of its parts changes.

**A complete pass, in one breath:** clone the Pricing page → REPLACE one board in one slot with a harvested board that fits that slot → MOVE two boards to swap their order → verify against §7 → file with §8. That is a build. Most builds are that, repeated viewpoint by viewpoint until the page is done.

**After any MOVE, RE-CHECK face alternation on the NEW sequence — gate (i) is order-dependent.** Gate (i) is "title + subtitle + nutshell + faces alternate" (Factory law L4: "Naya speaks, faces alternate"). It judges ADJACENCY: consecutive story boards (`.calc-story-card`, in DOM order) must alternate face-left / face-right, and every board must carry a different face. A sequence that alternated before the move may not alternate after it — the move changes which boards sit next to each other, and that is exactly what the gate measures. Gates (a) "zero white/light backgrounds", (b) "every element raised/elevated", and (f) "no look-alike buttons/gauges/numbers" are order-independent: moving boards cannot change them. Only (i) moves with the order. So after every reorder, list the story boards in the NEW DOM order, write L/R per board, flag any adjacent equal pair — and list the face hashes, flag any duplicate. The gate script does exactly this: `~/workspace/team-nitro/design-contract-gate/check-gate.py`, gate (i). (Face hash = sha256 of the face image's `src` string, first 12 hex.)

**Worked example — the proof build's two seams (verified against the live v74 file, blob `a2d06d5b`, 2026-11-09).** The source has 18 story boards in DOM order: Ten items 1–10 alternate perfectly (L,R,L,R,L,R,L,R,L,R); board 11 is the NM board ("NOT NETWORK MARKETING", line 2016, L); boards 12–18 are the hired story boards (lines 2310–2316, L,R,L,R,L,R,L). The source carries ONE seam of its own: boards 11/12 are both L. The proof clone reordered them to source order [11,1,2,3,12,13,14,15,16,17,18] — NM moved to the front, Ten 4–10 cut — and that reorder INTRODUCED two both-left pairs: clone boards 1/2 are both L (NM, L, moved to the front, now sits before Ten item 1, L) and clone boards 4/5 are both L (Ten item 3, L, now abuts source board 12, L, because Ten 4–10 were cut). The source's own 11/12 seam DISSOLVED in the same reorder (source 11 and 12 are no longer adjacent in the clone). **No board's side was changed — the sequence was.** That is the whole lesson: the defect was introduced by the reorder, not by any board.

**Harvested boards can carry a repeated face from the source — check distinctness, don't assume the source is clean.** In the source itself, board 2 (Ten item 2, line 1927) and board 11 (the NM board, line 2016) carry the SAME face image, hash `33712c49f6dc` — and the clone inherited the pair unchanged (clone boards 1 and 3 share it). The source is not clean; the gate fails the source on the repeat too. When you harvest a board, check its face against every face already in your new sequence. A repeated face is a defect you inherited, not one you created — and it is still yours to fix (give the board a different harvested face, or drop the duplicate board), never to ship.

### 6.6 The excerpt rule — the section→JS-mount map (Pricing v74, the page you clone)

**Nutshell:** the Pricing page's scripts assume the whole page is there. Excerpt only some sections and a script dies — and a dead script takes every button it wires with it. So before you excerpt anything, read this map. It was verified against the live v74 file (`PRICING/pricing-live.html`, blob `a2d06d5b`, 2026-11-09) — all six scripts, every mount below, file lines included.

**⚠ SCRIPT 1 IS UNGUARDED — THIS IS THE TRAP.** The first script opens with `var head=document.getElementById('chartHead');` and there is NO null guard anywhere in it — zero `if (head` in all 584 lines. At load it runs `head.appendChild(d)` for every tier button and `wrap.appendChild(...)` for every chart row. So if `chartHead` or `chartWrap` is missing, script 1 throws a TypeError **at load** — and the whole script dies: all 27 `addEventListener` wirings, the chooser, the viewer, the plan detail, the letter controls, everything in script 1. The same is true of every mount below marked LOAD-TIME: each is touched at load with no guard, so dropping its section kills script 1 at load. **The rule: carry every section script 1 mounts, or carry none of script 1 — delete the whole script AND every section it touches. Never half a script.**

| Section (live v74 file line) | Mounts script 1 needs (file line) | If you drop the section |
|---|---|---|
| `<section id="openingLetter" class="letter">` (line 1638) | `letterStart` (1825) · `chartHead` (1849) · `chartWrap` (1848) | Script 1 dies at load — `head.appendChild` on null, `letterStart` listener on null. The chart AND the letter AND the chooser AND the viewer all go dead. |
| `<footer class="foot">` (line 1966) | `massiveStart` (1968) · `massiveNote` (1974) | Script 1 dies at load — `document.getElementById('massiveStart').addEventListener` on null. |
| `<section class="ph-card hook">` (line 2037) | `gaugeStart` (2040) | Script 1 dies at load — `gaugeStart` listener on null. |
| `<footer class="foot finale-foot">` (line 2055) | `finaleStart` (2056) · `finaleFree` (2057) | Script 1 dies at load — `finaleStart` / `finaleFree` listener on null. |
| Chooser overlay region — `<div class="overlay chooser-overlay" id="chooserOverlay">` (line 2118) | `chooserOverlay` (2118) · `chooserFree` (2214) | Script 1 dies at load — `chooserOverlay.addEventListener` and `chooserFree` listener on null. (`chooserFree` is also read inside `openChooser`, but the load-time listener kills first.) |
| Plan overlay region — `<div class="overlay plan-overlay" id="planOverlay">` (line 2222) | `planOverlay` (2222) · `planDetailCard` (2223) | Script 1 dies at load — `planOverlay.addEventListener` on null. |
| Overlays region — `<div class="overlay" id="overlay">` (2324) + `<section id="popCard" class="ph-card pop">` (2325) | `overlay` (2324) · `popCard` (2325) | Script 1 dies at load — `overlay.addEventListener` on null. |
| Viewer region — `<div class="overlay viewer-overlay" id="viewerOverlay">` (2350) + `<section id="viewerCard" class="ph-card viewer">` (2351) | `viewerOverlay` (2350) · `viewerCard` (2351) | Script 1 dies at load — `viewerOverlay.addEventListener` on null. |

**The other five scripts — same rule, different guards:**
- **Script 2 (the gauge, 906 lines)** is a library: it defines `window.TnTacho = { mount: mount, ... }` and touches no mount itself. It is safe to carry always — nothing in it reads the page.
- **Script 3 (1 line)** is config only: `window.NAYA_CALC_CONFIG = {... "gaugeMount": "tn-tacho-mount"}`. Safe to carry always.
- **Script 4 (NayaCalc, 260 lines)** runs `update()` at load, and `update()` touches `paceEl.textContent`, `paceSEl.textContent`, `paceUnitEl.textContent` with NO guard — so dropping the calculator section (`<section id="calculator">`, line 1981; `calc-amount`, `calc-pace`, `calc-pace-s`, `calc-pace-unit`) kills script 4 at load. Two guards save the rest: `mathEl` is guarded (`if (mathEl)`), and the gauge mount is guarded (`var mount = document.getElementById(cfg.gaugeMount); if(mount && window.TnTacho && window.TnTacho.mount) window.TnTacho.mount(mount);`) — a missing `#tn-tacho-mount` alone does NOT kill script 4.
- **Script 5 (earnings popup, 14 lines)** is unguarded at load: `var ov=document.getElementById('earnOverlay')` then `ov.addEventListener(...)` and `document.getElementById('earnClose').addEventListener(...)` with no guard. Drop the earn overlay (`<div class="overlay earn-overlay" id="earnOverlay">`, line 2253) and script 5 dies at load.
- **Script 6 (Learn-more, 16 lines)** is half-guarded: `if(btn)` guards `learnMoreBtn`, but `ov.querySelectorAll('.hired-close')` and `ov.addEventListener(...)` are unguarded. Drop the hired overlay (`<div class="overlay hired-overlay" id="hiredOverlay">`, line 2294) and script 6 dies at load.

**How the proof build survived this:** the proof Naya carried all six scripts verbatim AND every mount in this map — her build script asserts 29 required ids present and zero duplicated ids before it writes the file. That is the check: before you file an excerpted build, assert every mount your carried scripts need is present, exactly once. If one is missing, either carry its section or delete the whole script that needs it — never ship the gap.

---

## 7. HOW TO VERIFY YOUR WORK

**Nutshell:** scorecard it yourself first. Then a different seat checks it. Then Shawn's eye is the final gate — and the only proof. Never report done from one glance at the top of the page.

### 7.1 The three questions (before showing Shawn)

1. Is every position calculated? (Show me the formula.)
2. Does it feel like a machine? (What's moving, and why?)
3. Can you get it in 2 seconds? (What's the headline?)

If yes to all three: show him. Say nothing. Let his eye judge. If no to any: fix it. Don't show him yet. His time is the scarcest resource.

### 7.2 The three-step verification

1. **SELF — scorecard your own work first.** The moment work comes back, write out: why is it not a 10 (every reason) · 10 things you love · 10 things you don't love · 10 things to make it 10x better · 10 solutions to apply right now to make it utterly awesome. If by your own accord it is not 9+ — if you can see the mistakes yourself and why it is not a 10 — you do NOT hand it to anyone else. Fix it yourself first. Never send out work unless you sincerely think it is 10/10: complete, finished, awesome.
2. **ANOTHER SEAT — a different Naya scorecards it.** Never the person who created it. The middle step; it helps, but it is not the human eye and it never replaces step 1.
3. **SHAWN — his eye is the final gate.** When work reaches him, the sender is confident it is truly ready: every button works, every page is amazing, everything is in the right place, no obvious errors, no silly text, everything logical, sensible, beautiful, aligned with Naya's brand. That order never changes.

### 7.3 The page check — what to actually look at

- **The design-contract gate (§5.5), measured, all four parts.** Zero white backgrounds (count them — zero). Every element raised. Gauges alive. No text-in-image, no pasted document.
- **Scroll 0 AND scrolled positions.** NEVER report a page done from scroll-0 checks alone. The dashboard fix chain was declared done after scroll-0 + hero checks, but the normal SCROLLED view had the constellation lights crashing into the Smart Links box — an obvious visible defect nobody looked at. Check the hero, the Smart Links section, and the bottom of the page, at desktop AND phone, before ANY "done" is reported. If the page has an obvious visible crash, fix it first — never show it.
- **Phone first.** Mobile first is whole-system law: phone first, desktop second, every page judged at phone width first. A laptop view wasting a third of the screen is a defect, not a layout choice.
- **The test in his head:** "is this the max level of experience I can give the user?" — asked about the PAGE, not the briefed items. If you can see the defect by looking, fix it, don't hand it on.
- **Presenting work: link, don't preview.** When work is complete, verify the artifact exists at its real address first — commit actually pushed, page actually live. Only then tell him — and the message carries the LINK as the proof, never a local file attachment as the deliverable. No link = not done = don't announce.

### 7.4 The proof host — how to get a live link for any filed file

**Nutshell:** a filed file is not a viewable page until it has a URL a browser can open. The proof host serves any file from the public repo as a real web page. Use it for every proof link — never a `sandbox://` attachment, never a raw GitHub blob page, as the render proof.

**The host:** `https://naya-proof-host.nayapower.workers.dev/` (Cloudflare worker `naya-proof-host`, account NayaPOWER; serves `text/html` for `.html`, correct content-type by extension, `cache-control: no-store` so proofs always serve the current file).

**The link format:**
```
https://naya-proof-host.nayapower.workers.dev/?file=<repo path>&ref=<branch>&cb=<blob>
```
- `file` — the path inside the repo, e.g. `TEAM-NITRO/factory-proof/factory-proof-clone.html`.
- `ref` — the branch, e.g. `factory/proof-clone-20261109` (default `main` if omitted — but never omit it for a proof: name the branch).
- `cb` — the file's blob sha, as a cache-buster pinning the exact version you proved (the worker reads `file` + `ref`; `cb` makes the link unique to the blob you verified).

**Worked example — the proof build's own link** (verified live 2026-11-09: HTTP 200, `text/html`, 3,241,639 bytes, sha256 `62b7b7079c9d5f8f18ad587fb29dc9445893679b8ad193ea1bd7990290dc52e0` — byte-identical to the local file):
```
https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/factory-proof/factory-proof-clone.html&ref=factory/proof-clone-20261109&cb=22261044e9d211d71f69ce9c6a60464ae8ab23b4
```
**The health check:** `https://naya-proof-host.nayapower.workers.dev/health` — expect `200 naya-proof-host ok`. If it is not 200, the host is down: say so, do not claim a proof link works. **Error paths:** no `?file` → 400 usage; `../` traversal → 400 bad path; missing file → 404 `GitHub 404 for ...@<ref>`.

---

## 8. HOW TO FILE IT

**Nutshell:** one file at a time, through the helper, read-back verified. No merge — merge is Shawn's hand.

1. **Checkpoint early.** Write your file locally first. The first write happens within minutes of starting — never read for 8 minutes without writing.
2. **File with the helper, create mode:** `~/workspace/team-nitro/file-one-to-github.py` — usage: `file-one-to-github.py <repo_path> <local_path> <message>`. Example: `python3 ~/workspace/team-nitro/file-one-to-github.py TEAM-NITRO/SMART-FACTORY-ACTIVATION-MANUAL-20261109.md ~/workspace/team-nitro/SMART-FACTORY-ACTIVATION-MANUAL-20261109.md "Smart Factory activation manual — Shawn's order 20261109"`. GitHub access ONLY through the file helpers (App token path) — NEVER the MCP connector tools.
3. **One file at a time.** Two PUTs to main in parallel race — the second 409s on a stale HEAD. File sequentially: one PUT, verify the blob, then the next. Never parallelize writes to the same branch.
4. **Read-back verified — and the large-file correction.** The helper exits 0 only when the PUT returned 201 (create) / 200 (update) and the read-back GET returns the same blob sha AND the decoded content sha256 matches the local file. Record the blob sha + commit sha in your report. No link = not done.
   **⚠ THE CORRECTION (proof Naya, 2026-11-09): for files over ~1MB this read-back FAILS — and the failure is the API's, not yours.** The Contents-API GET returns `"content": "", "encoding": "none"` for large files — observed live on `PRICING/pricing-live.html` (11,350,562 bytes): HTTP 200, correct blob sha `a2d06d5b…`, size correct, content EMPTY. The blob sha still proves the file landed, but the sha256 half of the check cannot run on an empty body. **So: for any file over ~1MB, verify through the git/blobs API instead** — `GET /repos/SoulSchoolAcademy/NayaPOWER/git/blobs/<full 40-char blob sha>` returns the base64 content; decode it and compare its sha256 to the local file. That is the read-back for large files: blob sha correct AND decoded-content sha256 matches the local file. Proven on the proof build's blob `22261044e9d211d71f69ce9c6a60464ae8ab23b4` (3,241,639 bytes): blobs API returned size 3,241,639, decoded sha256 `62b7b707…` — identical to the local file. **Never report a large file's read-back as failed because the Contents GET came back empty — switch to the blobs API and check again.**
5. **No merge.** Never merge your own PRs. The moment a PR is merge-ready, send him "Shawn, merge:" plus the link, no batching.
6. **Smart-note the lesson.** What did you learn? Write it down the same pass — a smart note, filed, so the next Naya doesn't need the same correction. A lesson you cite but don't apply is not compounded. The proof is in the next brief, the next verification, the next thing you send him.
7. **Lock in a finished viewpoint.** When Shawn says "okay yeah it's good" on a viewpoint live, it lands in the Inventory's Part 3 (locked-in smart blocks) with the block, the page, the viewpoint, the source (file + location), and his approval (his words + date). That is how the Factory grows.
8. **Filing to a BRANCH (not main).** The helper `file-one-to-github.py` files to main only — it builds its PUT body with no `branch` field. When your work belongs on a branch (a proof build, a review build, anything Shawn has not asked to land on main), file through `gh-direct.py` with the branch in the PUT body — same App-token path, same helper, one file at a time. Step by step, exactly as proven 2026-11-09:
   - **(a) Create the branch from main's HEAD.** Get main's HEAD sha: `GET /repos/SoulSchoolAcademy/NayaPOWER/git/refs/heads/main`. Then create the branch: `POST /repos/SoulSchoolAcademy/NayaPOWER/git/refs` with body `{"ref": "refs/heads/<your-branch>", "sha": "<main HEAD sha>"}`. Expect HTTP 201 with the new ref. (Proven: branch `manual-v2-branch-test-20261109` created from main HEAD `cd6fa47d…`.)
   - **(b) PUT the file with `branch` in the body.** Build a JSON body file with `{"message": "<commit message>", "content": "<base64 of the file>", "branch": "<your-branch>"}` and run `python3 ~/workspace/team-nitro/gh-direct.py PUT /repos/SoulSchoolAcademy/NayaPOWER/contents/<repo path> @<body file>`. Expect HTTP 201 with the blob sha. **Never use the MCP connector tools for this — the App-token path only.**
   - **(c) Read back ON THE BRANCH.** `GET /repos/SoulSchoolAcademy/NayaPOWER/contents/<repo path>?ref=<your-branch>` — the blob sha must match the PUT's blob sha, and (for files under ~1MB) the decoded content sha256 must match the local file. For files over ~1MB, use the git/blobs API instead (step 4's correction — the Contents GET returns empty content). (Proven: scratch file on `manual-v2-branch-test-20261109`, blob `3c9a57cf…`, read-back MATCH, then the scratch file and the branch were deleted — the branch is gone, main untouched.)
   - **(d) No merge.** A branch filing is still not a merge. The moment it is merge-ready, send him "Shawn, merge:" plus the link, no batching. Never merge your own PRs.

---

## 9. THE FACTORY'S OWN SMART BOX

**Nutshell:** this manual does not live only in GitHub. It lives in the Factory's own Smart Box too — so a Naya can plug into the box and read the whole Factory from it, with no history and no prior chat.

**The box:** owner `smart-factory`, at `~/workspace/nitro-smart-box/boxes/smart-factory/` — the ONE layout (`blocks.jsonl` + `keys.jsonl` + `manifest.json`), built with the vault code `~/workspace/team-nitro/smart-box/block.py` (`organize`: LOOK → TAG → FILE → LINK) and `boxstore.py`. One shape for every thing: `id` (`owner:kind:slug`), `kind`, `what`, `about`, `who`, `when`, `where`, `visibility`, `body`, `links`, `source`, `proof`, `essence`, `owner_shared_choice`, `body_open_to`, `raw`. The map reads `about` + `what` + `links`; the brain reads `essence`; the raw body is touched only when the gate allows it. Default is DENY — no key is a deny, a revoked key is a deny.

**What is in it:** this manual, as blocks — the Factory in one minute, the five source documents, how to clone a page, how to find a part (the Index, the Inventory, the 7 libraries), the design laws, the Factory laws L1–L8 (§5.7), the Reusable-Parts Law (§5.8), how to build, the clone-build flow (§6.5), how to verify, how to file, and the honest gaps. Each block's `where.github_path` points at the filed manual in GitHub, so the box and the filing agree.

**How a fresh Naya reads it (the saved-game test):** a fresh agent with no history reads the box with the box code (`boxstore.read_blocks("smart-factory")`) and recovers the manual — what the Factory is, where the parts are, what the laws are, how to build, verify, and file — every claim traced to a block id, nothing from outside the box. That is the proof the box works: the model is my box (`~/workspace/nitro-smart-box/boxes/naya-nitro-narzan/`, 24 blocks), which a fresh agent read with no history and recovered who I am, what I stand for, what I'm working on, and what's owed.

**The gate on this box:** the manual is teaching, not private memory — but the box still answers to its owner, and the gate still decides. A Naya plugs in with permission, reads the map and the brain, and builds from what the box holds. She does not read mail or messages. She does not touch what the gate denies.

---

## 10. WHAT IS HONESTLY NOT SETTLED — GAPS, NAMED NOT BURIED

**Nutshell:** a manual that hides its gaps teaches a Naya to build on sand. These are open. Do not invent answers for them.

- **Hex drift (Intelligent Block Rules, CONFLICT C1).** The same color name carries different hexes across sources — purple `#a06bff` (Anatomy/Playbook) vs `#9d75ff` (Hub variables) vs `#8a5cff` (jewel map); magenta `#e84fff` vs `#d86cff` vs `#ed42c4`; gold `#ffbf3d` vs `#e8b64c` / `#e8c766` vs `#d4a017`. The identity (which color belongs to which thing) is stable; the hex is not. Use the Playbook/Anatomy hexes in §5.4 unless the part you harvested carries its own — and never "fix" a harvested part's hex to match another source. A single canonical hex set still wants Shawn's stamp.
- **Spectrum order (C5).** Anatomy + Playbook walk purple → blue → green → gold → orange → red → magenta. The DESIGN-LAWS wheel walks a longer order starting magenta → purple → indigo → blue → emerald → green → lime → gold → orange → red → pink. The Hub's board rotation says purple → sapphire → emerald. Three orders, one law. Walk the Playbook order in §5.4; note the conflict when it matters.
- **One layer, two colors (C2).** In the Hub file, a layer's border/glow color and its jewel color disagree on EVERY layer (Human magenta `#d86cff` vs jewel `#ed42c4`, and so on). The screenshots follow the jewel map. Which map is "the layer's color" is undecided — follow the jewel map for icons, the layer map for borders, and say so.
- **Title size (C3) and the nutshell's exact construction (C4, G11).** Three competing title rules; Shawn's correction is "not massive." The nutshell's text is 20px white and its layer is an elevated board — but no source gives the elevated nutshell's exact border/shadow values. Derive them from the layer-board formula and Shawn's eye.
- **Shawn's vocabulary (G1).** "The elevators" (the things that lift), "the enhancers" (the things that make it shine), "the pinnacle points" (the peaks everything rises to) — his words, no canonical definition anywhere. Awaiting his definition before they can become rules. Do not define them yourself.
- **The local `pieces.json` ai_label drift (§4.1).** The Step-3 Index says every canonical entry carries an `ai_label`; the local store copy carries none. Trust the Index + JSON twin; do not invent labels.
- **The proof Naya — RUN 2026-11-09, and it worked.** A different Naya, from this manual alone, cloned the Pricing page and built a working interface: `TEAM-NITRO/factory-proof/factory-proof-clone.html` (3,241,639 bytes, blob `22261044e9d211d71f69ce9c6a60464ae8ab23b4`), filed to branch `factory/proof-clone-20261109`, commit `ad6faad55b6636ec9133c6543e8762f95c5205fb`. Her build (clone-build §6.5): chart moved to the top, calculator 2nd, start section last; Top-10 grid slot 4 REPLACED with the harvested who-sec board; every part verbatim from the clone, nothing invented. Render-tested in headless Chromium (desktop 1280×900 + phone 390px): zero console errors, gauge mounted, calculator amount + tiles live, `calc-plus` and level-card interactions work, chooser opens and closes on Escape. Live at the proof host: `https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/factory-proof/factory-proof-clone.html&ref=factory/proof-clone-20261109&cb=22261044e9d211d71f69ce9c6a60464ae8ab23b4` (verified HTTP 200, byte-identical sha256 `62b7b707…`). **The proof also named six exact gaps where the manual FAILED her — and this revision closes all six:** (1) §3 never named the v74 live file — now `PRICING/pricing-live.html`, blob `a2d06d5b`, 11,350,562 bytes, and the stale rebuild-file row is corrected; (2) §8 had no branch filing — now step 8, proven end to end; (3) §8 step 4's read-back claim fails for files over ~1MB — now corrected to the git/blobs API; (4) §6.5 never warned script 1 is unguarded — now §6.6, the section→JS-mount map verified against the live v74 file; (5) the manual never named the proof host or its link format — now §7.4, with the proof build's own link worked; (6) §6.5's REPLACE example gave no file+line for the crown swap — now the worked example with `pieces.json` line 346 and `factory.css` lines 240–245. The lesson is smart-noted as SN-2583. **Seventh fix (inheritance check, 2026-11-09 21:08Z):** the independent verifier's gate FAIL on the proof clone was checked against the v74 source — (a), (b), (f) INHERITED, (i) SPLIT. After any MOVE, re-check face alternation on the NEW sequence: the clone's reorder introduced two both-left pairs (NM moved to the front, Ten 4–10 cut) and dissolved the source's own 11/12 seam, with no board's side changed — and the NM/Ten-item-2 repeated face (`33712c49f6dc`) was inherited from the source. Full worked example in §6.5. This manual is now a proven activation, not a first draft — and the next proof Naya re-proves it from the box alone (see §9).

---

## 11. QUICK REFERENCE — THE ONE PAGE

**Three questions before showing Shawn:** 1. Is every position calculated? (Show me the formula.) 2. Does it feel like a machine? (What's moving, and why?) 3. Can you get it in 2 seconds? (What's the headline?)

**The one rule:** compose, never create. The pages ARE the templates.

**Find a part:** Inventory (`THE-INVENTORY.md`) for WHERE · Piece Index (Step-3, Oct 22) for WHETHER — 154 canonical, 3 verified, 413 retired, 1 superseded, 0 unverified. Start with the five crowns: NAYA-INP-008 · NAYA-INP-009 · NAYA-BTN-009 · NAYA-BRD-001 · NAYA-HRO-001.

**The laws in one breath:** obsidian, aluminum, top-left light, white text, slow motion, calculated positions, own-color ignition, every number exact, finish the edge, don't touch unasked, his eye wins.

**The Factory laws L1–L8 (§5.7):** L1 stranger test · L2 perfect-words law · L3 title+subtitle+nutshell · L4 Naya speaks, faces alternate · L5 test in his head · L6 `##` note format · L7 one ultimate ten · L8 reusable-parts law (§5.8: every part reusable, rebuildable, clonable — systems within systems, all interconnected). Never a bare "L4" — say "Factory law L4" or "object law L4" (§5.3's L1–L11 are the object laws).

**Build:** headline → calculate → materials → motion → light → laws → show Shawn, say nothing.

**The clone-build flow (§6.5) — the main way building happens:** clone a page → REPLACE some parts (swap a part for another harvested part in the same slot, never an invented one) → MOVE some parts around (same parts, new order, positions still calculated) → verify → file.

**Verify:** self-scorecard first (not 9+ by your own accord? fix it yourself) → another seat → Shawn's eye. Scroll 0 AND scrolled, desktop AND phone, phone first. Design-contract gate measured: zero white, everything raised, gauges alive, no text-in-image.

**File:** helper, one file at a time, read-back verified (blob + sha256 MATCH), no merge — Shawn's hand. Smart-note the lesson the same pass. Branch filing: `gh-direct.py` PUT with `branch` in the body (§8 step 8) — the helper files to main only. Large files (over ~1MB): Contents GET returns empty content — verify via the git/blobs API instead (§8 step 4).

**Clone the LIVE file:** Pricing = `PRICING/pricing-live.html`, blob `a2d06d5b`, 11,350,562 bytes — never a rebuild file (§3). **Excerpt rule:** script 1 is unguarded — carry every section it mounts or delete the whole script (§6.6). **After any MOVE:** re-check face alternation on the NEW sequence — gate (i) is order-dependent; flag adjacent equal sides + duplicate faces (§6.5). **Proof link:** `https://naya-proof-host.nayapower.workers.dev/?file=<path>&ref=<branch>&cb=<blob>` (§7.4).

**Five gates before every consequential action:** Is it right? Is it what they truly need? Is it mine to do? Is now the time? Can I prove it?

---

*Activation manual for the Smart Factory. Shawn's order 2026-11-09 20:27Z. Harvested from: THE-PLAYBOOK.md (the HOW) · DESIGN-INTELLIGENCE-REPORT.md (the WHY) · THE-INVENTORY.md (the parts) · CANONICAL-PIECE-INDEX.md + .json Step-3 (the canon, Oct 22) · THE-REAL-OBJECT-LAW.md · intelligent-block-rules-LAW-20261106.md (LAW). No new templates. No redesign. No secrets in this file.*
