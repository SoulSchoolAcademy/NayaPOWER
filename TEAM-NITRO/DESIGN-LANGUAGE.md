# THE DESIGN LANGUAGE OF NAYAPOWER / NAYANET

**What this is:** the builder's extraction of the ONE visual language the whole system
already speaks — harvested from the live pages' actual bytes, so a builder who has
never seen the system produces an in-language page, and a verifier can fail an
off-language one on sight.

**Authority chain (highest first — this doc never outranks any of them):**
1. **Master Design Contract** — `~/workspace/nayapower-repo/0000-NAYAPOWER-MASTER-DESIGN-CONTRACT-V1.md` (architecture root; AAA = evidence, not enthusiasm; change control §12).
2. **Naya Design Contract v1.1 — CANONICAL, ratified by Shawn 2026-10-03** — `~/workspace/nayapower-repo/BRAIN/10-INTERFACES/NAYA-DESIGN-CONTRACT-V1.md`. Its purpose line: *"So Shawn never has to repeat himself."* **The contract is the law; this document makes it usable.** Where this doc and the contract disagree, the contract wins and this doc gets corrected.
3. **The No-Redesign Law + the Read-Before-Design Gate** — `~/AGENTS.md`. This document is item (3) of the gate: read all three before designing, building, restyling, or deploying ANY page. Every time.
4. **The locked summary** — `~/AGENTS.md` § "Nayanet Design Language — LOCKED" (2026-10-19).
5. **The doctrine layer** — `~/workspace/team-nitro/DESIGN-LAWS.md` (Laws 1–6 + the Forbidden List, from Shawn's fifteen design files and his verbal teaching).

**How to use it:** cite sections by number in builder briefs ("build to DESIGN-LANGUAGE §4.2"). Parts are **used, or placed near-identically — never recreated** (Gate rule 2). A recreated part that already exists is a defect.

**Evidence convention:** every value below is followed by its harvest source as
`[file · pattern]`. Values marked *(contract)* come from the Design Contract itself.

---

## 0. THE LANGUAGE IN ONE BREATH

> **Glossy obsidian black, lit from within. White light at rest; on touch, each thing
> ignites in its OWN spectrum color — edge only, text stays white. Everything is
> elevated, nothing is flat. Circles carry people and numbers; horizontal rectangles
> carry content; the spectrum walks purple → blue → green → gold → orange → red →
> magenta and never repeats a color twice in a row. One chrome (the twin pluses),
> one navigation (Smart Tabs), one button DNA, on every page.**

If a page would look at home anywhere else on the internet, it is off-language.

---

## 1. LAYOUT GRAMMAR

1.1 **Full width, always.** No max-width caps on content, no narrow centered columns
with black voids on the sides `[AGENTS.md locked §5; contract §6: "Content owns the
width"]`. On mobile the page is the full screen.

1.2 **The rectangle is the content shape.** Content blocks are horizontal rectangles
(≈16:9 proportion language), stacked one after another `[AGENTS.md locked §4]`.
Never squares, never vertical rectangles for content. Circles are reserved for
avatars, orbs, icons, and data-circles (§7) — never for content cards.

1.3 **The board is the unit of composition.** A page is a vertical stack of boards
(`.ph-card` in the flagship grammar): `background:linear-gradient(180deg,#14141c,#0a0a10);
border:2px solid rgba(255,255,255,.16); border-radius:20px; padding:28px; margin-bottom:20px`
`[factory-models/backup/personal.html.pre-onesystem · .ph-card]`. Sections inside a
board are separated by section heads (§6.4), never by empty space.

1.4 **No empty space.** Empty spacing is a defect; breathing room is dosed, deliberate,
and small (SN-0823 standard). No `min-height` forcing voids `[contract §6]`. If a
region has nothing to say, it does not exist — content flows directly.

1.5 **Ground colors (the field).** The page field is near-black, and it is *layered*,
never a flat fill:
- Hub token set: `--bg:#0B0D12; --bg-panel/#12151D; --bg-card/#171B25; --edge:#252B39`
  `[index-2.html · :root tokens]`
- Canonical room pages sit even darker: `body{background:#020204}` `[reports.html · body]`,
  `body{background:#020202}` `[lists.html · body]`
- Flagship boards: `#14141c → #0a0a10` vertical gradient `[.ph-card, above]`
The north-star image (Shawn): *"beautiful glossy obsidian black — like a glossy city
at night."* A flat gray or flat black panel is off-language; every surface has a
gradient and a finish (§4).

1.6 **Radius scale.** `--radius-pill:999px; --radius-lg:17px; --radius-md:13px`
`[index-2.html · tokens]`. In practice: boards 20px `[.ph-card]`, tiles/rows 14–16px
`[os-style.html · .os-face{border-radius:16px}]`, chips/pills 999px, circles 50%.
Invented radii are a tell.

1.7 **One app, named blocks.** "One smart app doesn't mean one page — it means ONE
APP" (composition standard SN-0819): every function is a named smart block; Home
stays light (cover + primary + clear buttons); every function sits one tap behind
an obvious button. In the flagship grammar blocks are `.os-view` panels, one visible
at a time, opened by the page's own doors `[os-style.html · header comment]`.

---

## 2. CHROME — THE SAME ON EVERY PAGE

### 2.1 The twin pluses (congruency / plus standard)

Two identical buttons, extreme corners, on EVERY page. They are twins: same size,
same construction, same behavior everywhere.

- Geometry: `position:fixed; top:12px; width:48px; height:48px; border-radius:50%`,
  LEFT at `left:12px`, RIGHT at `right:12px`, `z-index:900`
  `[os-style.html · #os-chrome .rooms-plus/.eco-plus; os-chrome.html]`
- Construction: `background:linear-gradient(180deg,#1b1b24,#07070b);
  border:1.5px solid #fff; box-shadow:inset 0 1px 0 rgba(255,255,255,.35),
  inset 0 -4px 8px rgba(0,0,0,.6), 0 8px 20px rgba(0,0,0,.55)` — a round, glossy
  black circle, thin light rim, white + glyph (SVG, `stroke-width:2.8`, 20×20px)
  `[os-style.html; os-chrome.html · svg path M12 5v14M5 12h14]`
- LEFT = `.rooms-plus` — opens **THE NAYANET AREAS DRAWER**: `width:min(300px,84vw)`,
  slides from left (`transform .32s cubic-bezier(.16,.84,.22,1)`), head
  "NAYANET AREAS" (11px, letter-spacing .18em, #E8E8EC, weight 800), entries are
  raised rows (12px radius, gradient `#17171f→#0a0a0f`, 1.5px white .85 border) each
  carrying its room color in `--rc`, in Hub order: Start Here `#a06bff` · Smart Feed
  `#3fb8ff` · Smart Factory `#2fe89e` · Ask Naya `#ffbf3d` · Smart Spaces `#ff9a5a` ·
  Today's Intel `#ff5e6c` · Smart Growth `#e84fff` · Your Reports `#a06bff` ·
  Intelligent Library `#3fb8ff` · Smart Ledger `#2fe89e` · Your Connections `#ffbf3d` ·
  Smart Lists `#ff9a5a` · Smart Mail `#ff5e6c` · Settings `#e84fff`
  `[os-chrome.html · .os-drawer; os-style.html]`
- RIGHT = `.eco-plus` — opens **THE PAGE OWNER'S PERSONAL MENU** (the ecosystem menu):
  panel `top:72px; right:12px; width:min(320px,88vw); background:#171B25;
  border-radius:16px`, head "NAYANET ECOSYSTEM", 12 entries each with a jewel icon
  chip (`.eco-ico`, 26×26, own `--eco` color) `[os-chrome.html; os-style.html]`
- Hover: each plus ignites in its OWN jewel — left `--jewel:#a06bff`, right
  `--jewel:#e84fff` — border takes the jewel, `0 0 32px var(--jewel)` glow, lift
  `translateY(-2px) scale(1.04)` `[os-style.html]`
- The Hub is the harvest source for the chrome: the flagship layer copies it
  verbatim ("Twin-plus chrome (Hub geometry…)", "contents verbatim from the Hub"
  `[os-style.html comments]`). Any page whose pluses differ in size, position,
  construction, or menu contents is off-language.

### 2.2 Smart Tabs — the ONE navigation (Shawn's law, 2026-10-29: one network, many apps)

One network, many apps: the SAME tab bar on every app, never reinvented per app.
Harvest source (verbatim, never recreated): `~/workspace/welcome-build/flagship-template.html`
lines 3258–3480, `smart-tabs v1.1.4` — verified live on https://nayanet.live/dashboard
2026-10-29 (browser-measured: text stays white on hover; border brightens; per-tab
colored glow; click navigates by hash, no reload).

**The two bars and what they are:**
- TOP bar: the app's FUNCTIONS (personal app navigation). NOT editable — no ⋯ menu,
  no Add. Drifts slowly RIGHT.
- BOTTOM bar: the WHOLE APP navigation (the ecosystem). EDITABLE by law: ⋯ menu
  (Edit / Set Purple Heart / Set Gold Star / Remove) + ＋ Add pill at the end.
  Drifts slowly LEFT.
- Both: never closable. Hearts sort first, then stars. A tab with no destination
  says so — never a dead link.

**Shape:** rounded pill, dark glass face, thin light border at rest, white bold label.
`padding:12px 22px; border-radius:999px; border:2px solid rgba(255,255,255,.3);
background:rgba(0,0,0,.5); color:#fff; font-size:14px; font-weight:700;
white-space:nowrap; flex:0 0 auto`. The row never wraps: `overflow-x:auto;
flex-wrap:nowrap; scrollbar hidden`. Each tab may carry a jewel icon (`.os-jewel`,
§5.4): nav size 27×27px, glyph 14px, radius 8px.

**THE TRILLION-DOLLAR RULE (Shawn, 2026-10-29 — "too much color looks cheap"):**
color lives ONLY in the light — never in the face, never in the text.
- REST: dark glass gradient face (lighter crown, darker base), 1px bright top rim,
  white text always. Inset top highlight + inset bottom shadow + soft drop shadow.
  `background:linear-gradient(180deg,#16161e,#0a0a10); border:2px solid
  rgba(255,255,255,.28); box-shadow:inset 0 1px 0 rgba(255,255,255,.35),
  inset 0 -3px 8px rgba(0,0,0,.5), 0 6px 16px rgba(0,0,0,.5);`
- HOVER: the TEXT STAYS WHITE — this is the law the PI face broke (its pills turned
  the text the button's color; cheap). What ignites, in the tab's OWN spectrum color:
  the rim (`border-color:var(--tc)`), a TWO-LAYER outer glow (tight + wide:
  `0 0 14px var(--tc), 0 0 34px -6px var(--tc)`), the text-shadow kiss
  (`text-shadow:0 0 12px var(--tc)` — glow around white letters, never colored
  letters), and a `translateY(-2px)` lift. The face stays dark.
- ACTIVE/SELECTED: white-hot, never colored — `border-color:rgba(255,255,255,.6);
  box-shadow:0 0 16px rgba(255,255,255,.18), inset 0 1px rgba(255,255,255,.15)`.
  No permanent color glow on selection — color comes on hover, not on selection
  [contract §2].
- Per-tab color: the spectrum walk BY POSITION (purple → blue → green → gold →
  orange → red → magenta → back to purple), each tab's `--tc`.

**Drift pairing (law):** BOTTOM drifts LEFT, TOP drifts RIGHT — mirrored, gentle,
one-way. The tab set is duplicated so the wrap is invisible; drift pauses while a
hand is on the bar and resumes after. Motion is proven by measuring positions over
time at phone width — never by the presence of code.

**One-shot kit for builders:** this section + the harvest source lines above are
everything a builder needs. Any tab that colors its text, floods its face, or
invents a new shape is off-language — NOT CERTIFIED.

### 2.3 Cover / header pattern

- The flagship cover is a spectrum-art hero: layered radial spectrum washes over a
  deep base — `radial-gradient(560px 240px at 12% -10%, rgba(160,107,255,.5),
  transparent 60%), … linear-gradient(135deg,#1a1a3e,#2d1b4e 30%,#4a2b7a 55%,
  #0f3460 80%,#16537e)`, height 308px `[os-style.html · .ph-cover]`.
- The owner action row on the cover is `.ph-actions` — Dashboard is a peer door in
  the row with Message / Invite / Reports (the oversized full-width cover button
  was removed by Shawn's eye pass, 2026-10-22) `[os-style.html; DERIVE-BUILD eye-pass record]`.
- Every header is a warm front door: logo + living mark + warm voice + one clear
  line; full width `[DESIGN-LAWS.md · Law 3]`.

### 2.4 Sidebar / drawer

Sidebars are hidden by default and opened via the obvious toggle buttons
`[contract §6]`. The drawer grammar is §2.1's: near-black panel `#12151D`, raised
rows, white-lit edges at rest, own-color ignition on hover.

---

## 3. COLOR

### 3.1 The spectrum walk (the system's spine)

**Purple `#a06bff` → blue `#3fb8ff` → green `#2fe89e` → gold `#ffbf3d` → orange
`#ff9a5a` → red `#ff5e6c` → magenta `#e84fff` → back to purple**
`[AGENTS.md locked §1; os-chrome.html · drawer --rc sequence]`

- Each section/block gets the NEXT color in the walk. **Never the same color twice
  in a row.** Adjacent zones never share a hue. Color = position in the walk =
  identity: you know where you are by the color.
- The walk governs ORDERED sets: nav tabs, faces in order, stat circles, funnel
  stages, plug-in tiles, board ignition order (`--igc` assigned by board order —
  "boards walk purple → blue → green → gold → orange → red → magenta, never all
  one color" `[os-style.html · osIgnite comment]`).
- Color is assigned **by position, never by name-hash** — with ONE named exception:
  wall authors keep stable name-hash colors, because a wall is identity space
  (same person, same color every time) `[Phi ruling, eye-pass scorecard 2026-10-22]`.

### 3.2 The contract's three color jobs — never mix them

`[contract §1]` Color has three distinct jobs; do not use one job's rule for another:

1. **Accent jewels** — bullets, boards, icons: always the richest, most vibrant:
   hot pink · purple · blue · green · gold.
2. **Endless flow** — feeds and long continuous sequences: a repeating cycle
   **purple → indigo → forest emerald → lime → yellow → gold → orange → red →
   magenta → purple**.
3. **SmartNote board sections** — a FIXED mapping, not a walk: In a nutshell →
   white · Human → magenta · Child → purple · Grandma → indigo · Naya → cyan ·
   Machine → forest emerald · Why it matters → lime green · How do you use it →
   yellow · What's in it for you → orange or gold.

Contract token table `[contract §1]`: magenta (hot pink) `#ed42c4` · purple
`#8a5cff` (signature; also `#9d75ff`) · indigo `#6675ff` · cyan `#3ca8ff` ·
emerald `#35e39b` · forest emerald `#2e9e6a` · lime `#b8ee57` · yellow `#ffd45a` ·
gold `#e8c766` · orange `#ff8c42` · red `#ff5e6c`.

**Contract law:** purple/black/white are PROMINENT; spectrum colors are
complementary accents, never dominant; gold/yellow is restrained — semantic
accents, never dominant text. (Deviations between the contract tokens and the
shipping hexes are catalogued in Appendix A — read it before picking a hex.)

### 3.3 Room identity colors (Law-9 tokens)

Rooms keep their Hub identity colors wherever room chrome appears (e.g. the
bottom ribbon): Collective ↔ Spaces GOLD · Personal ↔ Mail BLUE · Activity ↔
Activity GREEN. These are identity tokens, not walk positions, and they do not
change per page `[Phi ruling, eye-pass 2026-10-22; Hub --accent-* tokens in
index-2.html: --accent-mail:var(--rich-orange)… see Appendix A.4]`.

### 3.4 White at rest, ignite on touch — EDGE ONLY

- **At rest:** white light. A visible white border/glow on every clickable edge —
  borders big enough to SEE (1.5–2px), never faint hairlines `[contract §2;
  DESIGN-LAWS.md master statement]`.
- **On hover/touch:** the element ignites in its OWN spectrum color — the BORDER
  and the GLOW only. **THE TEXT NEVER HIGHLIGHTS — it stays white.** Text
  highlighting "looks cheaper" (Shawn, eye pass 2026-10-22). The cure is written
  into the layer: `.ph-navtab:hover{color:#fff}` — "on hover/touch ONLY the edge
  ignites… the TEXT never highlights" `[os-style.html · EYE-PASS CURE comment]`.
  Board form: `.ph-card:hover{border-color:var(--igc); box-shadow:0 0 22px -6px
  var(--igc), inset 0 1px 0 rgba(255,255,255,.14)}` — border + glow, no text rule
  `[os-style.html]`.
- **Spectrum colors are never worn at rest on chrome.** Color is earned by
  interaction `[DESIGN-LAWS.md · Law 1]`. Named exception: the "Life with Naya"
  button (NAYA-BTN-005 "Primo Purple") keeps its purple ON permanently — Shawn's
  explicit call `[factory piece records · NAYA-BTN-005]`.
- Chrome (buttons, CTAs) ignites purple; themed elements burn their own color
  `[DESIGN-LAWS.md · Law 2, three jobs]`.

### 3.5 Jewel tones, never pastel

Rich, saturated, deep: rich purple, sapphire blue, emerald green, true gold,
rich orange, ruby red, deep magenta (Shawn, eye pass 2026-10-22). A faded or
pastel wash on any surface is a defect. Plug-in tiles: deep black, white text,
the number alive in its own walk color — never a faded single-color wash
`[eye-pass cure #9]`.

### 3.6 Text colors

- Body text: **white** `#fff` / `#F5F7FB` (`--ink`) / `#f8f7fb`; secondary text
  **silver** `#E8E8EC` `[index-2.html · tokens; os-style.html · .os-note{color:#F0F0F4}]`.
- **Never gray body text** — it is unreadable `[contract §1/§5; DESIGN-LAWS.md ·
  Forbidden #4]`. Separation is by size and weight, not by dimming.
- Muted labels where they exist are `#9a9ab0` and are for captions/sub-labels only,
  never body copy `[os-style.html · .os-setrow-sub]`.
- Timestamp colors are semantic and fixed: **date GREEN `#2fe89e`, time GOLD
  `#ffbf3d`** (§7.5).

---

## 4. ELEVATION — THE RECIPE

**Nothing is flat. Ever.** Every element carries multi-layer depth: an inset top
highlight (light catching the top edge), an inset bottom shade, an outer glow,
and a drop shadow. Elevation is **recursive**: boards within boards are each
raised — tiles sit ON their board, not in it `[os-style.html · FRONT CURE comment:
"elevation recursive"]`.

### 4.1 The token grammar (Hub)

- `--depth-hi: inset 0 1px #fff6` — the universal top light line
- `--depth-drop: 0 18px 42px #000b` — the standard drop
- `--depth-deep: 0 20px 48px #000d` — the deep drop
- Standard compositions: `box-shadow: var(--depth-hi), var(--depth-drop)`;
  boards with presence: `var(--depth-hi), var(--depth-deep), 0 0 36px
  color-mix(in srgb, var(--purple) 22%, transparent)` `[index-2.html · tokens + usages]`
- Timing tokens: `--dur-fast:.18s; --dur-med:.28s; --dur-slow:.5s;
  --ease:cubic-bezier(.16,.84,.22,1)` `[index-2.html · tokens]`

### 4.2 The board formula (doctrine form)

`[DESIGN-LAWS.md · Law 3]` — the 5-layer construction:
```
inset 0 2px 2px rgba(255,255,255,.12),   /* top light catching the edge */
inset 0 -8px 18px rgba(0,0,0,.55),        /* inner depth */
0 5px 0 #020203,                          /* hard base bar */
0 17px 0 -8px <tone 16% on field>,        /* tone under-bar */
0 35px 75px rgba(0,0,0,.7),               /* deep drop */
0 0 40px -17px <tone>                     /* tone glow */
```
Body: dark gradient `#1a171f → #09090d → #030304`, 1.5px tone-mixed border, 24px
radius. Layer order of the world: **Field > Board > Nested panel > Control >
Overlay** — each rides visibly above the last.

The shipping flagship form of the same recipe (the eye-pass full-strength card):
`box-shadow:inset 0 2px 0 rgba(255,255,255,.13), inset 0 -5px 13px rgba(0,0,0,.3),
0 0 0 1px rgba(255,255,255,.07), 0 16px 44px rgba(0,0,0,.55), 0 5px 18px
rgba(0,0,0,.45)` `[os-style.html · .os-view .ph-card]`.

### 4.3 The factory recipe (buttons and small controls)

Bright silver-white rim 1.5–2px + flat near-black fill (`#020203`/`#030304`
family) + one inset top shade + one white lip line + a modest white rest glow;
the element's own color appears only on focus/hover. Typed text in fields is
WHITE, never gray.

### 4.4 Wells — the recessed inverse

Depth runs both ways (§5.5). A well is the same grammar inverted: dark gradient
(`#08080d → #10101a`), `box-shadow:inset 0 3px 10px rgba(0,0,0,.75), inset 0 -1px 0
rgba(255,255,255,.28), 0 1px 0 rgba(255,255,255,.05)` — a recessed stage things
sit IN `[os-style.html · .os-well]`. Charts and sparklines live in mini-wells
inside their boards `[os-style.html · .os-spark-wrap]`.

---

## 5. BUTTONS, CONTROLS, AND DUAL-DEPTH

### 5.1 The one button DNA

There is one button construction with job variants — there are no flat buttons,
and flat is a defect, not a style `[DESIGN-LAWS.md · Law 5]`.

- Center: really black (`#050505`). Text: always white, with an icon.
- Border: white, visible at rest, 1.5px+.
- Minimum 44px touch target; principal CTA ≥ 52px.
- Hover: purple edge + glow for chrome; own-color edge + glow for themed buttons.
  Press: `translateY(2px)`; hover lift: buttons 2px, boards 5px, cards 6px,
  orbs 8px + slight scale `[DESIGN-LAWS.md · Laws 1/5]`.
- Focus and pressed states are not optional.

### 5.2 The flagship action pair (`.ph-connect` / `.ph-msg`)

- Primary (`.ph-connect`, NAYA-BTN-009 Reference Button grammar): pill (999px),
  purple family. Eye-pass full-strength form: `background:linear-gradient(180deg,
  #1b1b24,#050507); border:2px solid #a06bff; box-shadow:inset 0 1.5px 0
  rgba(255,255,255,.45), inset 0 -4px 8px rgba(0,0,0,.55), 0 0 24px -4px #a06bff,
  0 10px 22px rgba(0,0,0,.55)`; hover: border `#c09aff`, glow `0 0 36px -2px
  #a06bff`, text stays `#fff` `[os-style.html · EYE-PASS CURE]`.
- Secondary (`.ph-msg`): same construction, white rim at rest (`border:2px solid
  rgba(255,255,255,.5)`, fill `#17171f → #0a0a0f`); hover ignites the edge in the
  element's own `--ac`/`--avc`, text stays white `[os-style.html]`.
- Small action chips (`.os-like`, `.os-savebtn`, `.os-insight-act`, period pills):
  pill 999px, the same inset-lip + drop stack in miniature; an "on" state lights
  its text-shadow + edge in its own color but never floods `[os-style.html]`.

### 5.3 Primary toggle buttons (contract form)

`[contract §3]` Sidebar openers / menu triggers: **black circular buttons** —
`radial-gradient(circle at 35% 30%, #2a2a32, #0a0a0e 70%)` — bold white icon
(never thin, never dot-like), white light glow idle, purple light + scale/rotate
on hover. The twin pluses (§2.1) are this form's flagship instance.

**Semantic action colors** `[contract §3]` — pill action buttons carry a fixed
meaning color: LOVE red `#ff5e6c` · LIKE blue `#55b9ee` · FAVORITE gold `#ffd45a` ·
SAVE blue `#55b9ee` · CREATE SPACE purple `#9d75ff` · SHARE purple `#9d75ff`.
White light idle, color on hover, dynamic counts/badges where applicable.

### 5.4 The icon jewel system

Every icon sits in a raised, lit tile — never a bare glyph `[os-style.html ·
.os-jewel]`: `background:radial-gradient(circle at 32% 26%, rgba(255,255,255,.30),
transparent 48%), linear-gradient(180deg,#262633,#0b0b12 80%); border:1.5px solid
var(--jc); border-radius:9px; box-shadow:inset 0 1.5px 0 rgba(255,255,255,.55),
inset 0 -3px 6px rgba(0,0,0,.6), 0 5px 12px rgba(0,0,0,.55), 0 0 14px -3px
var(--jc); text-shadow:0 0 9px var(--jc)` — the glyph is lit in its own spectrum
color (`--jc`). Sizes: sm 23px (glyph 12px) · nav 27px (14px) · header 28px ·
md 36px (17px) · lg 46px (22px) `[os-style.html]`.

**Icon law** `[contract §4]`: unique per item — never the same shape in different
colors and call it done; each icon must represent what it IS, legible at a glance
(rooms' line-art at 24px in spectrum color; toggles bold — a plus must read as
PLUS). If you can't tell what it represents at a glance, it's wrong.

### 5.5 Dual-depth: wells vs buttons vs panels

Three depth directions, never confused:
- **Inputs are WELLS** (depth in): recessed, dark inside, white text. Flagship
  form: `.os-input` — `background:rgba(255,255,255,.06); border:1.5px solid
  rgba(255,255,255,.55); border-radius:12px; color:#fff; padding:12px 14px`;
  focus: border `#a06bff` + `0 0 18px -4px #a06bff` `[os-style.html]`. Inline edit
  fields go fully recessed: `background:#050508` with the field's own color rim
  `[os-style.html · .os-list-edit]`.
- **Actions are BUTTONS** (depth out): §5.1–5.3.
- **Displays are LIT PANELS**: boards (§4) whose numerals and graphics are light,
  not print (§7.4).

### 5.6 Switches (Settings grammar)

A real lit switch, 56×32px: recessed track (`inset 0 3px 7px rgba(0,0,0,.85)`),
24px domed knob; ON = rim + inner glow + knob all take the row's jewel color
(`--jc`), caption lights white `[os-style.html · .os-switch]`. Settings rows ride
full elevation with jewel icons; install-as-app lives inside Settings on every
page (Install Law) — never a banner at the top of a page.

---

## 6. TYPOGRAPHY

6.1 **LAW ZERO (supreme): readability beats everything.** No glow, color, or
effect may reduce readability `[contract §5]`.

6.2 **The two voices.**
- **Voice (headlines, the human layer): a real serif with warmth — Newsreader**
  (Georgia fallback). In the Hub: `font-family: Newsreader, Georgia, serif`
  `[index-2.html]`; doctrine allows Newsreader/Georgia (Cormorant Garamond is the
  licensed specimen face in Connections) `[connections.html · "Cormorant Garamond",
  Georgia, serif; DESIGN-LAWS.md · Law 6 + reconciliation 2]`.
- **UI (chrome, body, controls): Inter** — `--font: Inter, ui-sans-serif, system-ui,
  -apple-system, "Segoe UI", sans-serif` `[index-2.html · tokens]`. Every control
  inherits it (`font-family:inherit` is the most common declaration on every
  canonical page).

6.3 **Sizes.**
- Contract: body 17–18px target, **16px floor** `[contract §5]`.
- Doctrine hierarchy: **24 / 18 / 14** — kicker 24, headline 18, detail 14
  `[DESIGN-LAWS.md · Law 6]`.
- Hub token scale: `--fs-hero:clamp(38px,5.4vw,60px); --fs-title:23px;
  --fs-head:17px; --fs-body:16px; --fs-small:13px; --fs-micro:11.5px`
  `[index-2.html · tokens]`.
- Section heads (`.ph-sec-t`): 18px, weight 700, white, with the section's
  breathing dot `[personal.html.pre-onesystem]`. Big numerals: `.os-count` 34px
  weight 900 `[os-style.html]`.

6.4 **Headline treatment.** Headlines carry a hook (the note's real title is the
headline; IDs are small print). Text is never flat: section heads carry
`text-shadow:0 1px 0 rgba(255,255,255,.22), 0 3px 10px rgba(0,0,0,.65)` — a
grounding shadow, not a glow that hurts reading `[os-style.html · .ph-sec-t]`.
One clear visual hierarchy per screen `[contract §5]`.

6.5 **Order of resort: visuals → voice → text.** Icons, gems, faces, and shapes
speak before words do; text is the fallback, never the default
`[DESIGN-LAWS.md · Law 6]`.

---

## 7. DATA PRESENTATION

### 7.1 Circles carry numbers — the Orb Circle System (NAYA-ORB-002)

A lit circle that carries a number: it breathes, it glows in its own color, size
follows the data (SN-0823 ratified standard). `.os-orb`: 58×58px,
`border:2px solid var(--ac)`, dome radial + `#15151d→#08080d` gradient, inset lip
+ inset shade + drop + `0 0 15px -2px var(--ac)`, `animation:osOrbBreath 4.6s
ease-in-out infinite` (scale 1 → 1.045); the numeral is white with
`text-shadow:0 0 10px var(--ac)`; label 10.5px weight 800 `#E8E8EC` beneath
`[os-style.html · STEER 2]`. A "hot" orb wears a pulsing outer ring
(`osSparkPulse 2s`). Seven day-orbs in a row = the week (`.os-dayorbs`).

### 7.2 Reports stat circles

66×66px lit rings with a conic progress arc in the stat's own `--ac`
(`.os-rcirc::before`, masked ring), numeral 21px white glowing in `--ac`, label
10.5px beneath; the row spans the full width and wraps `[os-style.html]`.

### 7.3 The living-data blocks

The Dashboard door's eight named blocks (Living Data System): **Pulse Strip ·
Trend Panel · Mix Donut · Journey Funnel · Faces Board · Insight Feed · Heat &
Streaks · Health Gauge**. Rules that bind all of them:
- **A number in a black box is not a report** (SN-0822): every stat carries shape
  (a graphic) + direction (trend) + a human sentence. Insight Feed is the most
  intelligent pattern: data → a sentence → an action button.
- **The donut** (`.os-donut-wrap`, 120px): a beveled jewel — rotating conic sheen
  (`osSheenSpin 9s linear infinite`), drop shadow, recessed hole
  (`inset 17px`, `#14141c→#0a0a10`) carrying a lit numeral
  (white-to-`--ac` gradient text, glow drop-shadow); legend dots are tiny jewels
  (13px, white-hot radial core in their segment color) with proportion bars
  `[os-style.html]`.
- **Week bars** (`.os-week`, 92px stage inside a well): bars are lit objects —
  white-hot top melting into their `--barc` color, inset top light, own-color
  glow; they grow on arrival (`osBarGrow .8s`), breathe (brightness 1 → 1.22,
  3.4s), today's bar pulses stronger (1.45); the value rides a pill on top of
  the bar `[os-style.html]`.
- **The funnel** (`.os-funnel`): stages are slabs — vertical white-to-color
  gradient, flowing sheen sweep (`osSlabSheen 3.8s`), joined by a flowing dashed
  light arrow (`osFlow 1s linear infinite`); the count rides a lit pill. Honest
  stages only: Recorded → Joined ("Opened" is unobservable and forbidden)
  `[os-style.html; cure-wave record]`.
- **Lit numerals**: `.os-lit-num` — gradient text (white 18% → the block's color),
  clipped, with a glow drop-shadow. Numerals are light, never print
  `[os-style.html]`.

### 7.4 Boards within boards

Recursive elevation (§4) applied to data: a Faces board's tiles sit ON the board
(own gradient, own rim, own shadow) `[os-style.html · .os-face]`; a sparkline sits
in a lit mini-well INSIDE its stat board `[os-style.html · .os-spark-wrap]`.

### 7.5 Feed cards + timestamps

- Feed order is ALWAYS newest-first, categorized by TOPIC, never by kind
  (Feed Order Law).
- Every Smart Note card carries the live timestamp `.ib-stamp`: **date GREEN
  `#2fe89e`** (with `text-shadow:0 0 14px rgba(47,232,158,.40)`), **time GOLD
  `#ffbf3d`**, plus a relative label — all recomputing while the feed is open,
  never frozen `[index-2.html · .ib-stamp-date/.ib-stamp-time/.ib-stamp-rel;
  os-style.html · .os-date/.os-time carry the same token pair]`.
- Card category chips and kind icons ride the jewel system (§5.4) — icons, not
  text-only bars (eye-pass cure #8).

### 7.6 People: initials are orbs, rows are full-width

- **Every initial is an orb** — the standard is Shawn's `connections-2.html`
  `.cx-ava` (48px standard, 78px big) `[connections-2.html]`. Flagship form
  `.os-av`: 42px (60px on face rows), the initial set in a domed jewel disc —
  radial dome light + the orb's `--avc` color mixed into near-black, 2px rim in
  the color lightened with white, glow `0 0 24px -4px var(--avc)`, and **a light
  sweep that flows around the initial forever**: `.os-av::after` conic sheen,
  `osOrbFlow 7s linear infinite`; active people wear a rotating hot arc
  (`.os-av-arc`, `osArcSpin 3.2s`) `[os-style.html · "THE ORB"]`.
- **Connections layout is full-width horizontal rows, stacked** — never a
  mini-box grid: `.os-face{flex-direction:row; padding:16px 18px;
  border-radius:16px}`, orb left, name/fact stacked, action right
  `[os-style.html · EYE-PASS/steer comments cite connections-2.html as the standard]`.
- Presence: a green dot + label (`#2fe89e`, glowing, pulsing); dim state
  `#9a9ab0`, no glow `[os-style.html · .os-pres]`.

---

## 8. MOTION

Motion is meaning, never decoration — "maximum life, minimum noise"
`[DESIGN-LAWS.md · Law 1]`. The system's motion vocabulary:

8.1 **Drift** — Smart Tabs (§2.2): bottom left, top right, gentle, one-way,
pauses under a hand. The only ambient translation on chrome.

8.2 **Breathing** — living things pulse slowly: orbs `osOrbBreath 4.6s`; section
dots and donut `pulseGlow 3s infinite`; week bars `osBarBreathe 3.4s`; live dots
`livePulse 2s`. A ~72bpm heartbeat underlies the dial atoms
`[DESIGN-LAWS.md · Sources — SPECIMEN-CARD]`.

8.3 **Orb flow** — the light sweep around initials (§7.6): `osOrbFlow 7s linear
infinite`; hot arcs `osArcSpin 3.2s`; donut sheen `osSheenSpin 9s`.

8.4 **Ignition** — hover/touch transitions run on the token clock: fast `.18s`,
med `.28s`, slow `.5s`, ease `cubic-bezier(.16,.84,.22,1)` `[index-2.html ·
tokens]`. Light moves first, words follow: state changes animate BEFORE text
updates `[DESIGN-LAWS.md · Law 1]`. A changed value flares once
(`osChanged 1.25s`, brightness → 1.8 + own-color drop-shadow) `[os-style.html]`.

8.5 **Entrances** — blocks rise in: children `fadeUp .55s cubic-bezier(.2,.7,.2,1)`,
staggered 0.05s per child up to the 8th; bars/slabs draw on arrival (§7.3);
skeletons shimmer while loading (`.os-skel`, sweep 1.3s) `[os-style.html]`.

8.6 **Calm is a real control.** The Settings "Motion & glow" switch (`.os-calm`)
and `prefers-reduced-motion` still EVERY animation named above — the same scene,
lit and static. Motion that cannot be stilled is off-language
`[os-style.html · html.os-calm rules]`.

8.7 **Proof rule:** motion is proven by measuring positions/pixels over time at
phone width on the live page (pixel-motion protocol, median of ≥3 runs) — never
by code presence.

---

## 9. IDENTITY & BRANDING CONSTANTS

9.1 **Purple is the soul.** Purple `#a06bff` is the system's signature and the
first stop of every walk; the Smart Feed accent is purple; chrome ignites purple
`[contract §1 — purple = Naya's signature; AGENTS.md locked §7]`.

9.2 **The Welcome door** (`index.html`, worker `nayanet`): the greeting is
**"Naya Welcomes You"** — never "Naya Listening". Its signature art is an orbital
ring of **108 precision jewels** (diamonds) traveling counterclockwise, with a
white comet traveling clockwise — preserve exactly `[index.html · .naya-orbit
comment: "The color ring contains 108 precision jewels"]`.

9.3 **Diamonds are the signature geometry.** Bullets are jewels, not dots: a
rotated square (diamond), white → tone → black gradient, own-color glow, a sheen
facet; the jewel cycle runs in law order, never twice in a row
`[DESIGN-LAWS.md · Law 4]`. Faceted gems (clip-path diamond geometry, white-hot
crown → deep black base) mark signal moments. The factory's diamond piece is
NAYA-ICO-001.

9.4 **The certificate** (`identity.html`) is the one named exception to the
spectrum system: black dominant, **royal-purple accents, silver the family
metal** (gold is out, except the Mail box), white type, the crystal-N logo at
full presence, the name dead center as the hero, real faceted stones — never
flat glyphs `[identity.html; certificate record v2.11.2]`. Do not "fix" the
certificate into the walk; its restraint IS its language.

9.5 **Naming is branding.** Rooms keep their canonical names (Smart Feed, Ask
Naya, Smart Factory, Today's Intel, Your Reports, Intelligent Library, Smart
Ledger, Your Connections, Smart Lists, Smart Mail, Smart Spaces, Smart Growth,
Start Here) and their drawer order (§2.1) `[os-chrome.html]`. The member's own
app is "<Name>'s HUB" — first in their sidebar; Start Here is #1 for guests,
#2 for the owner (Sidebar Law).

9.6 **Honesty constants** `[contract §7]`: device-local data is labeled
device-local; no fake liveness; empty states are honest ("Nothing here yet"
beats fake content); no dead buttons — every clickable thing goes somewhere
real or it is removed `[contract §6]`. Demo/template data is deliberate
scaffolding and stays honestly labeled.

---

## 10. THE SAME-LANGUAGE CHECK

Run every item against the page BEFORE it ships. Any single FAIL = the page does
not ship (Gate rule 3: NOT CERTIFIED, no "close enough"). Items are checkable in
source or on the rendered page; the evidence column says where.

| # | Check | Evidence |
|---|-------|----------|
| 1 | **Field**: near-black layered gradient ground; no flat panel, no light surface anywhere | render + `body`/board backgrounds (§1.5) |
| 2 | **Full width**: no max-width cage; content owns the width edge to edge | render at desktop + 390px (§1.1) |
| 3 | **Shapes**: content in horizontal rectangles; circles only for avatars/orbs/icons/data-circles | render (§1.2, §7.1) |
| 4 | **No voids**: no empty spacing, no min-height deserts; every region earns its place | render (§1.4) |
| 5 | **Twin pluses**: both present, 48px, extreme top corners, identical construction; left opens the Areas drawer (Hub order, room `--rc` colors), right opens the owner's menu | click both (§2.1) |
| 6 | **Smart Tabs**: one scrolling pill bar, no wrap, jewel icon per tab, tabs actually scroll | render + scroll (§2.2) |
| 7 | **Drift**: bottom bar glides LEFT, top bar glides RIGHT — measured at phone width, median-of-3 | pixel-motion (§2.2, §8.7) |
| 8 | **Walk**: ordered sets follow purple→blue→green→gold→orange→red→magenta BY POSITION; no color twice in a row; adjacent zones never share a hue | source `--ac/--igc/--rc` sequence (§3.1) |
| 9 | **Color jobs unmixed**: SmartNote sections use the contract's FIXED mapping; feeds use the endless-flow cycle; chrome is purple/black/white | source vs contract §1 (§3.2) |
| 10 | **Rest = white light**: every clickable edge shows a visible white rim (1.5–2px) at rest; no spectrum color worn at rest on chrome (sole exception: Life with Naya) | render, no hover (§3.4) |
| 11 | **Hover = edge only**: hover/touch ignites border + glow in the element's OWN color; THE TEXT STAYS WHITE; the element lifts | real pointer, computed styles (§3.4, §5.1) |
| 12 | **Jewel tones**: saturated and rich; zero pastel/faded washes; tiles deep black with white text | render (§3.5) |
| 13 | **Elevation**: every board/control shows inset top light + inset bottom shade + drop shadow; nested elements raised ABOVE their board | computed `box-shadow` (§4) |
| 14 | **Wells vs buttons**: inputs recessed with white text; actions raised; displays lit panels | click + source (§5.5) |
| 15 | **One button DNA**: black center, white text + icon, white rim at rest, ≥44px target, focus + pressed states exist | source + keyboard (§5.1) |
| 16 | **Icons are jewels**: every icon in a raised lit tile (`--jc` rim + glow), unique per destination, legible at a glance | render (§5.4) |
| 17 | **Type**: Newsreader/Georgia headlines, Inter UI; body ≥16px; white/silver text — NO gray body text | computed styles (§6) |
| 18 | **Orbs carry people + numbers**: initials are flowing orbs (not flat discs); stat circles lit, breathing, labeled | render (§7.1, §7.6) |
| 19 | **Living data**: every stat has shape + direction + a human sentence; no naked numbers in black boxes | render (§7.3) |
| 20 | **Timestamps alive**: feed stamps show date GREEN `#2fe89e` + time GOLD `#ffbf3d` + relative label, recomputing | render over 60s (§7.5) |
| 21 | **Motion has an off switch**: Calm setting + reduced-motion still all animation | toggle + emulate (§8.6) |
| 22 | **No dead buttons, no fake liveness**: everything clickable does something real; local data labeled local; empty states honest | click everything (§9.6) |
| 23 | **Nothing recreated**: every component traces to a named existing part (Hub chrome, factory piece, os-*/ph-* grammar) — the brief names its harvest sources | brief + source (§0, Gate) |
| 24 | **Edit-only respected**: if this touched an existing page, the design is byte-stable except the named data wiring — diff against the page that was there | diff (§0, No-Redesign Law) |

---

## APPENDIX A — DEVIATIONS & INCONSISTENCIES FOUND IN THE CURRENT SYSTEM

*Findings for Shawn — named, not silently fixed. This document changes no page.*

**A.1 — Two purple lineages (contract vs shipping).** The contract's signature
purples are `#8a5cff` / `#9d75ff` `[contract §1]`; the Hub token block itself sets
`--purple:#9d75ff` `[index-2.html]`, but the shipping walk, the flagship grammar,
and AGENTS.md's locked language all run on `#a06bff` (51 occurrences in the Hub —
its most-used hex) `[index-2.html hex census]`. Same story at other stops:
contract cyan `#3ca8ff` vs walk blue `#3fb8ff`; contract emerald `#35e39b` vs walk
green `#2fe89e`; contract gold `#e8c766` / yellow `#ffd45a` vs walk gold `#ffbf3d`;
contract orange `#ff8c42` vs walk orange `#ff9a5a`; contract magenta `#ed42c4` vs
walk magenta `#e84fff` (and the Hub token `--magenta:#d86cff`, a third value).
DESIGN-LAWS.md already flags this ("a single canonical hex set still wants your
stamp" — open reconciliation 1). **The walk values won in practice; the contract
table was never updated. Shawn's stamp is the cure.**

**A.2 — Retired off-walk hexes survive as fossils.** `#40d3bb` and `#6675ff`
(the indigo) persist in the flagship bodies in disclosed fossil/token contexts
even after the eye-pass cure removed them from the walk `[eye-pass scorecard §3]`.
`#6675ff` is also the contract's indigo — fossil or token depends on which
authority you read. Named here so nobody "cleans them up" or "restores" them
without a ruling.

**A.3 — The Hub carries a wider jewel palette than the walk.** The Hub's hex
census shows `#55b9ee` (19), `#55e39a` (13), `#b8ee57` (11), `#ffea00` (14),
`#ed42c4` (10), `#35e39b` (10) alongside the walk stops `[index-2.html hex
census]`. These are the contract's endless-flow / accent-jewel stops living in
the Hub's richer surfaces (feed flow, jewel rows) — consistent with contract §1's
three jobs, but a builder copying Hub hexes at random will break the walk.
Rule of thumb this doc adopts: **walk stops for ordered sets; contract flow
stops for feeds/jewels; never improvise a hex.**

**A.4 — Room-accent token drift.** The Hub's `--accent-*` tokens do not all match
the Law-9 identity mapping (§3.3): e.g. `--accent-mail:var(--rich-orange)` and
`--accent-reports:var(--indigo)`, `--accent-today:var(--magenta)`,
`--accent-connect:var(--teal)`, `--accent-spaces:var(--lime)` `[index-2.html ·
tokens]` — the token layer predates the mapping and was only partially reconciled
(the bottom ribbon's identity tokens were ruled ACCEPTABLE as-is by Phi,
2026-10-22). Flagged, not harmonized.

**A.5 — Font reality vs the 24/18/14 doctrine.** The doctrine hierarchy is
24/18/14 `[DESIGN-LAWS.md · Law 6]`, the contract floor is body 16px
`[contract §5]`, but the Hub's own base sets `body{font-size:14px; line-height:1.7}`
in one of its style blocks `[index-2.html · body]` — below the contract floor.
The flagship token scale (`--fs-body:16px`) obeys the contract; parts of the Hub
base do not. (The Hub body rule may be overridden by later blocks — the base
declaration itself is the deviation on record.)

**A.6 — Serif voice is not uniform.** Newsreader in the Hub
`[index-2.html]`, Cormorant Garamond in Connections `[connections.html]`, plain
Georgia in parts of Today and Spaces `[today.html · Georgia,'Times New Roman',
serif; spaces.html · Georgia,serif]`. Doctrine permits Newsreader/Georgia and
names the Cormorant question an open reconciliation `[DESIGN-LAWS.md ·
reconciliation 2]`; the three-way split in the wild is wider than the doctrine
describes.

**A.7 — The canonical room pages are inline-styled; the grammar lives elsewhere.**
The room pages Shawn owns (`reports.html`, `today.html`, …) carry almost no
component classes — a class census of `reports.html` finds only the install/guide
chrome (`naya-inst-*`, `naya-guide-*`) `[reports.html · class census]`; their
boards, strips, and buttons are built inline and by script. The class-based
grammar (`ph-*`, `os-*`) exists only in the flagship layer. Consequence: the
rooms' language is real but *uncodified at the source* — which is exactly how a
replacement page could be mistaken for "the same page, dynamic." This document
is the codification; the sources remain the authority.

**A.8 — Master Contract status line.** The Design Contract is CANONICAL and
ratified (2026-10-03). The Master Design Contract's own header still reads
"PROPOSED CANONICAL — HUMAN DIRECTOR RATIFICATION REQUIRED"
`[0000-NAYAPOWER-MASTER-DESIGN-CONTRACT-V1.md · header]`. Cited here as the
architecture root per the Gate; its ratification stamp is Shawn's to give.

---

## APPENDIX B — SOURCE MAP

| Topic | Primary harvest source |
|---|---|
| The law itself | `BRAIN/10-INTERFACES/NAYA-DESIGN-CONTRACT-V1.md` (v1.1, CANONICAL) |
| Architecture root | `0000-NAYAPOWER-MASTER-DESIGN-CONTRACT-V1.md` |
| Locked summary | `~/AGENTS.md` § Nayanet Design Language — LOCKED |
| Doctrine (Laws 1–6, Forbidden List) | `~/workspace/team-nitro/DESIGN-LAWS.md` |
| Mother page (tokens, chrome, feed) | `~/workspace/user/files/index-2.html` |
| Canonical rooms | `~/workspace/user/files/{today,reports,connections,lists,library,ledger,mail,spaces,start}.html` |
| Welcome door / 108 jewels | `~/workspace/user/files/index.html` |
| Certificate exception | `~/workspace/user/files/identity.html` |
| Initials-as-orbs + Connections rows standard | `~/workspace/user/files/connections-2.html` (`.cx-ava`) |
| Flagship grammar (chrome, blocks, data, motion) | `~/workspace/factory-models/src/{os-chrome,os-style,os-script,os-head,dash-style,dash-blocks}.html` |
| Flagship base template (`.ph-*`) | `~/workspace/factory-models/backup/personal.html.pre-onesystem` |
| Piece names cited | NAYA-ICO-001 (diamond) · NAYA-ORB-002 (orb circle) · NAYA-BTN-005 "Primo Purple" · NAYA-BTN-009 (Reference Button) · NAYA-BRD-001 (Reference Board) |
| Eye-pass law refinements | Shawn 2026-10-22 via `~/MEMORY.md` + eye-pass scorecard `~/workspace/factory-models/EYEPASS-SCORECARD.md` |

*Written by Phi (φ), Team Nitro PRODUCT seat, 2026-10-22 — under the
Read-Before-Design Gate, as its item (3). Documentation only: no page was
modified, restyled, or deployed in the making of this document.*


## ADDENDUM — Shawn's eye, round 2 (2026-10-22, from his screenshots of the flagship Personal page)

Two principles, stated by Shawn as he reviewed the live page; they bind every page:

1. **NO DUPLICATED NAVIGATION — one home per action.** The flagship carried an action row (Dashboard / Message / Invite a friend / Reports) directly above a tab bar containing the same destinations. Duplication is clutter and reads unprofessional. If a destination lives in the tab bar, it does not also get a button row. An action that exists ONLY in a button row and belongs in navigation (his example: Invite a friend) moves INTO the tab bar.
2. **COVER INTEGRITY — the picture displays whole.** A cover photo is never cut off by the layout stacked under it. The identity block (name, motto, primary connect action) overlays the BOTTOM of the cover image, and the tab bar sits LEVEL with the picture's bottom edge — the picture comes down to the tabs, presenting clean and pro. Any layout that crops or crowds the cover is a defect.


## ADDENDUM — The Voice-First Standard (Shawn, 2026-10-22, from his Message-page review)

**What makes NayaNET different is user experience — and the experience is voice-first.** Standing standard for every page:

1. **Dictation on text entry.** Anywhere a person types — names, messages, notes, posts — a dictation button lets them speak it instead. Typing is the fallback, not the default.
2. **Playback on content.** Anywhere a person reads a block of content, a play button reads it in Naya's voice (the streaming play-time path; see the voice program).
3. **Text areas grow.** A writing box is never a fixed little window: it expands as the person writes and the page moves down with it. No character traps, no scrolling inside a 4-line slot.


## ADDENDUM — The About Page (Shawn, 2026-10-22, from his About review)

1. **Order**: Motto leads the page. Then Story, Goals, Mission, Vision, What I love, What I don't. The facts close the page — facts are the footnote, not the headline.
2. **Pronoun grammar**: a personal page says **my** (my story, my mission); a business or community page says **our** (our story, our mission). The pronoun is part of the section title.
3. **Every field on the page takes dictation** (see the Voice-First Standard above).


## ADDENDUM — Settings + the Smart-App Language Law (Shawn, 2026-10-22)

1. **Settings holds settings, not shortcuts.** Changing the profile picture happens by clicking the picture itself, where it lives — never through a Settings block.
2. **One idea per elevated block, in short, readable text.** No paragraphs of small print. If a block needs a wall of explanation, the block is wrong.
3. **Install lives in Settings** (standing law) and says so plainly: "Install as app" / "Install this app" + one short line. It does not advertise the rest of the system.
4. **These are smart apps.** User-facing words are *app / smart app* — never *page* or *website* — everywhere in the system.


## ADDENDUM — The Play-Naya Chip + Answers Flow Like a Feed (Shawn, 2026-10-22)

1. **The standard play element is the Life with Naya chip**: her round profile picture + her name + a round play button, compact, in ONE little element. It lives tucked out of the content's way (top-right, under the room's heading) — never parked in the middle of what it's playing.
2. **Spoken answers flow like a feed.** When Naya answers, the output reads down the page and everything below it moves down with it. No fixed box traps the conversation; no control sits in the middle blocking the words.


## ADDENDUM — The Explanation Standard (Shawn, 2026-10-22)

**Nothing in the system is a mystery.** A feature is never just labeled — it is explained, in plain words, where it stands: a short line on its elevated block, and a tappable **ⓘ** carrying the fuller note (what it is, what it does, why it's there). If a person has to wonder what something is, the page failed — not the person. Sign-in is the worked example: "Your email is how NayaNET knows it's you — it recovers your password, proves you are you, and syncs your smart apps to you on every device."


## ADDENDUM — Many Apps, One Tab Bar (Shawn, 2026-10-22)

A person can have **many smart apps** — personal, business, space, and more — each with its own URL, each chosen on its own. **Any URL entered into the system becomes a Smart Tab immediately**: the tab bar is how a person's whole world of apps stays one tap away. A new personal app is offered the **top spot** in its owner's sidebar ( ahead of Start Here ), because the sidebar's first place belongs to the person's own app.


## ADDENDUM — Aliveness Is Not Optional + Contents Chips + Clean Faces (Shawn's eye on Reports, 2026-10-22 ~18:47Z)

Born from Shawn opening a Daily Intelligence report and finding beautiful copy on dead boards. This binds EVERY page, and the Factory's contract gate must check it (§10 items):

1. **Every board is alive.** Hover or touch on ANY board, panel, or section lifts it and ignites its edge in its OWN spectrum color. A board with no hover/touch state is a defect — it does not ship, it does not certify. White/silver at rest, own color on touch, text stays white (edge-only ignition, standing eye-pass law).
2. **The hero board breathes.** The page's face board (Reports: THE BIG PICTURE) carries live energy at rest — a soft living edge/pulse in its spectrum color (purple for the face) — and ignites fully on hover/touch.
3. **Faces are clean.** A headline/face never carries machine meta: no lesson codes (L507), no filing timestamps, no parenthetical bookkeeping in the displayed face. Meta goes in small print or underneath. What shows underneath the face is the report's date/time — in the Hub stamp structure (below), not in the headline.
4. **Dates and times use the Hub stamp, everywhere.** Date in green (#2fe89e), time in gold (#ffbf3d), a live relative label that recomputes while the page is open — the `.ib-stamp` structure from the Hub. Flat single-color date text (the pink/dim 'October 18th 2026' style) is a defect on every page.
5. **Contents chips (the 'IN THIS REPORT' pattern) have rules.** (a) PURPOSE IS STATED: the block says what it is — these chips jump to the report's sections — in plain words under its kicker (Explanation Standard). (b) SHORT LABELS: a chip label is a short plain phrase — aim ≤5 words, hard cap 7; machine parentheticals and codes are stripped for display (the full heading still exists in the section itself). Long headings get a short display form, never a wrapped paragraph in a pill. (c) TIDY ROWS: chips are laid out in deliberate even rows (balanced row lengths), never a random centered cluster that wraps wherever it lands. (d) COLOR BY ROW: each ROW takes the next spectrum color (row 1 purple, row 2 blue, row 3 green, then gold, orange, red, magenta); a chip ignites on hover/touch in ITS ROW's color — edge + glow, text stays white — and lifts. All chips the same color is a defect; all chips igniting in one shared color is a defect.


## ADDENDUM — The Presentation Law: Motto, Standard, Way (Shawn, 2026-10-24 — locked as machine law / AI law)

Everything we do is elevated, clean, crisp — nothing below high level. Text presentation: high contrast, the nicest fonts. Everything placed in the perfect place with perfect spacing. Everything active intelligence. 10-star service for the user. The presentation is awe-inspiring AND easy to understand, logical, sensible. Push-button simple ease. Never more than needed — exactly what's needed, in the most elegant, beautiful, intelligent way, highly effective.

This is our motto, our standard, our way, and our law — how we operate, how we design, part of the design contract. It is coded into the system, not just said: every builder brief names it, every verifier checks it, every rendered review judges against it (§10). All seats work by it. It governs how we build extraordinary systems, smart systems, smart apps. Anything below it does not ship.

## ADDENDUM — Living Depth: The Dimension of the Whole System (Shawn, 2026-10-30)

**Living depth is not a button treatment — it is the dimension of the entire system.** Boards, icons, buttons, bullet points, chips, panels: everything gets living depth. Flat is gone everywhere, not just on the bar. This is the language the whole system speaks.

**The definition, in his words:** taking an element from flat 2D to full 3D — it looks like it's coming out of the screen, almost like you can touch it. Not a drawn oval: a real, active, touchable object.

**The mastery is "just enough."** The eye reads "real" instantly; never so much it turns gaudy. His test, applied to every element: *at a glance, does it look like it's coming out of the screen?* Borders alone are not enough — "it does look good... but it's not real looking enough."

**The means** (the craft every builder masters): top-lit gradient faces (light top → dark bottom, like a polished stone) · machined bevels (bright hairline on the top edge, dark line under the bottom edge) · real cast shadows (tight dark contact shadow + wide soft ambient — shadow says "floats above the surface," glow says "hazy") · recessed wells for inset elements (jewels sit IN, not on) · whisper glow at rest, color igniting on hover/touch as light *spilling* off the object · motion with weight (hover rises, press sinks — springy, never linear).

**The order of teaching:** the bar proves it first — then the insight goes to all Nayas with the live proof, never as words alone. The living example is the lesson.

## ADDENDUM — The Color Language (Shawn, 2026-10-30)

"There's a language to colors." Every button owns its color. Rest = beautiful black; hover/touch = ignites in its OWN color; **never all the same.** His examples (the law is the principle, the mapping may evolve): ⋯ menu — Edit green, Heart purple, Star gold, Remove red, with actually-colored ♥/★ glyphs; Edit panel — Save blue, Move left green, Move right purple, Remove red, Close white; panel chrome purple, the system color. Uniform or random hover colors are a defect — there must be logic a citizen can feel. The panel/board itself is never static: its outer edge ignites on hover. This binds every control on every surface, not just the bar.

## ADDENDUM — Readable or It Doesn't Ship (Shawn, 2026-10-30)

Fancy but unreadable is a defect, full stop. Two hard rules: **(1) HIGH CONTRAST ALWAYS** — white text on bright blue, or any low-contrast pairing, fails; if it can't be read at a glance, it's wrong, no matter how pretty. **(2) TEXT IS WHITE AND READABLE** — tiny, dim, grey-on-dark text fails; all text white, sized to read, never decorative at the cost of legibility. Elegant and beautiful AND easy to understand — never one without the other. (Born from his eye: a bright-blue "Born Connected" button with unreadable white text, and tiny dim non-white text scattered on the dashboard.)

## DEPTH NOT GLOW (Shawn's law, 2026-10-30 — "glow makes it look cheap")
Glow does not read premium. Too much glow reads cheap — hazy, flat, fake. What reads elite is LIVING DEPTH: sharp, dimensional, restrained. Light must feel like it comes from the material itself, never haze around it. The dashboard is the first thing a citizen sees — it must be extraordinary on every level: alive, sharp, real. When in doubt: less glow, more depth. Graphs and stat tiles must read as REAL data — dimensional and alive, never flat, never fake. (Applied 2026-10-30: Smart Links orange breathe-aura removed; Smart Links' identity is purple, not orange.)

## DICTATION IS STANDARD (Shawn's law, 2026-10-30)
Every search field on the whole system carries voice dictation. A mic button lives in the search pill; it uses browser-native speech recognition and degrades gracefully where unsupported (the mic hides, typing still works). Dictation is standard equipment — not a feature of one page, for everyone, everywhere. Any new search pill ships with the mic; any existing one gets it in its next pass.

---

## THE VIEWPOINT SYSTEM — UNLOCKED PARTS (Shawn, 2026-11-01)

**Status: BLESSED. Ready for use. The ultimate set.**

These 10 parts are the building blocks of every viewpoint. Every page. Every screen.
Nothing flat. Everything alive. Every part a real physical object.

| # | Part | What | Purpose |
|---|------|------|---------|
| 01 | VIEWPOINT | A complete world — one screen, one purpose | The person experiences ONE thing at maximum |
| 02 | HERO OBJECT | The centerpiece — the instrument | Where they land. The Bugatti of the internet. |
| 03 | ORB | Satellite stat — glowing sphere | Stats as objects, not sentences |
| 04 | JEWEL ORBIT | 8 spectrum jewels circling the hero | One family. Same color language. |
| 05 | DISPLAY MODULE | Recessed score readout | Hardware, not text. Set INTO the machine. |
| 06 | DIAL NUMERALS | 0-500 printed on metal | A real instrument has real markings |
| 07 | MORPH BUTTON | Tiny toggle — unfolds/folds nav | Navigation on call, not on top |
| 08 | CHROME BEZEL | Machined aluminum ring | Pick-it-up real. Precision you can feel. |
| 09 | DIAMOND CENTER | Multi-layered jewel heart | Depth you look INTO, not at |
| 10 | FLOWING LIGHT | Orb color breathing (8s cycle) | Alive = responsive. The flow is the life. |

**Source file:** `interface-factory/parts/viewpoint-system.html` (143 lines, documented)

**The laws these serve:**
- THE VIEWPOINT LAW (2026-11-01): ultimate viewpoint for ultimate experience
- THE RUBIK'S CUBE (2026-11-01): everything morphing into everything, within everything
- THE REAL OBJECT LAW (SN-0859): if it doesn't look touchable, it doesn't ship
- SN-0858 (Viewport Optimization): fade don't clutter, restore in one tap, morph don't jump

**Usage:** Compose, don't create. These parts ARE the design language. Every new page
assembles from these — never invents new ones. When a new part is needed, it must earn
its place by passing the Real Object Law, then it's filed here.
