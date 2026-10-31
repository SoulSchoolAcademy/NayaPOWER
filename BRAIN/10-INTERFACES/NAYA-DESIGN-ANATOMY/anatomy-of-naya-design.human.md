# THE ANATOMY OF NAYA DESIGN — The Element Canon

**For:** Shawn · **From:** Naya Resolve · **Date:** 2026-10-31
**Status: RATIFIED — Shawn, 2026-10-31 18:07Z ("Official — lock it in").** Amended at ratification per the five-anatomy synthesis: Signature is obsidian (Diamond White rejected), and Law 6 — alive means it answers touch — is written into Law 6 below and the gate checks.
**What this is:** the anatomy of every major element in NayaNET — what it's made of, layer by layer — the top ten concepts in the world for each element, scored against our laws and our toolbox, and the one we choose for each, with why. After this, the parts get pre-made once, at elite level, and nobody guesses again.
**Companions owed in the same filing:** `.ai.md` (builder contracts, exact tokens) + `.machine.json` (the parts registry as data). This human tongue is the decision document.

---

## PART 0 — THE LAWS EVERY ELEMENT OBEYS

An element that breaks one of these is not a Naya element, whatever it looks like.

1. **Obsidian ground.** Black with depth, white text, high contrast. White backgrounds are dead. Nothing light-grey, nothing pastel, nothing matte-flat.
2. **Living depth.** Every element is a physical object coming off the page: multi-layer borders, angles, stacked elevation, light held inside it. Flat 2D fails even with icons on it.
3. **Ignition.** White at rest. On touch, hover, or focus, the element ignites in **its own color** — glow has exactly one job. Too much glow reads cheap; restraint is the mastery.
4. **The spectrum walk.** Purple → blue → green → gold, never the same color twice in a row, one color job per element. A color means the same thing on every page, forever.
5. **Geometry.** Boards and cards are 16:9 rectangles. Buttons are pills. Touch targets ≥ 44px. Type ≥ 14px. Symmetry is designed, not accidental.
6. **Alive means it answers touch** (Law 6, Power's correction, ratified). White light at rest; halo and glow exist only in response to touch, hover, or focus. The jewel orb carries its color as identity — solid, never a halo at rest. Presence indicators breathe only while the state they show is actually live. Elements move with meaning and tick only on real events. Motion that isn't data is a liar.
7. **Honest in every state.** Rest, hover, pressed, selected, loading, empty, error — all designed, all truthful. Never fakes, never a dead button, never a SOON pill. An unwired thing shows its honest frame.
8. **Family.** One canonical component, imported everywhere, never copied or locally varied. Approved pages (Life with Naya, the certificate page) are the element library — reuse their actual elements.
9. **Two-second read.** Essence first, glanceable, push-button simple. If it needs explaining, it fails.
10. **Data carries a sentence.** Any number anywhere obeys SN-0822: magnitude + shape + direction + a human sentence — or it doesn't ship.

---

## PART 1 — BUTTONS

### The anatomy (seven layers, bottom to top)

1. **Elevation shadow** — a soft colored shadow cast *below* the object; it is what lifts the button off the page.
2. **Base plate** — obsidian glass body with a vertical gradient (lighter at top, as if lit from above).
3. **Rim** — a multi-layer border: outer hairline of light, then a spectrum edge in the button's own color, then an inner shadow line. Three lines minimum — one line reads flat.
4. **Icon chip** — a jewel disc or rounded square seated left, holding the glyph, in the button's color.
5. **Label** — white, semibold, sentence case, ≥14px, optically centered against the chip.
6. **Live slot** (optional) — a number or state word on the right, tabular figures, part of the button (the taxonomy buttons carry their live counts here).
7. **State skin** — rest: white light held in the rim · hover/touch: ignition — the rim and chip light in the button's color, the whole object lifts 1–2px · pressed: sinks 1px, inner glow deepens · selected: white-hot rim · disabled: never hidden — dimmed, with the reason readable.

**Levels.** *Signature* (one per view — the conversion action; obsidian body with maximum ignition, scale, and motion — **never a white body**; white is dead) · *Primary* (the page's main verbs) · *Standard* (bar and board actions) · *Compact* (chips inside boards; still ≥44px touch on touch devices) · *Jewel* (icon-only, ≥44px, label on tap/hover — never a mystery).

### The top ten button concepts in the world

| # | Concept | Why it's elite | Fits our laws? | Buildable here? |
|---|---|---|---|---|
| 1 | **Physical jewel glass** (Naya's own — layered glass, rim light, ignition) | Depth + life + identity in one object; nobody else ships it | 10/10 — it *is* the laws | Yes — CSS layers, SVG chips; already proven in the Smart Tabs kit |
| 2 | **Apple frosted capsule** (SF glass, blur, restraint) | The premium benchmark; blur discipline is world-class | 8/10 — beautiful, but no ignition, no spectrum | Yes — backdrop blur |
| 3 | **Game gem button** (mobile-game gloss, big jewel) | Instantly reads *alive* and touchable | 7/10 — alive, but drifts gaudy without restraint | Yes |
| 4 | **Tesla instrument button** (huge, dark, minimal) | Touch sizing and calm at speed | 7/10 — depth too shallow for the brand | Yes |
| 5 | **Raycast command chip** (dense, keyboard-first) | Pro density; every pixel earns its place | 6/10 — flat; a pro-surface dialect only | Yes |
| 6 | **Linear / Vercel precision** (flat, hairline, fast) | Elite craft, zero noise | 5/10 — fails Living Depth outright | Yes, trivially |
| 7 | **Material You tonal pill** (adaptive color) | Friendly, systematic | 5/10 — pastel risk; color means nothing fixed | Yes |
| 8 | **Skeuomorphic object** (old iOS leather/metal) | Rich, physical | 4/10 — physical but dated and heavy | Yes, at cost |
| 9 | **Neumorphism** (soft extrusion) | Novel | 2/10 — low contrast fails readability | Yes |
| 10 | **Flat web button** (the default everywhere) | Fast to make | 1/10 — the thing we exist to replace | — |

**🏆 THE CHOICE: #1, physical jewel glass** — with #2's blur discipline inside the glass, #4's touch confidence in sizing, #5's density reserved for pro surfaces. **Why:** it is the only concept that satisfies depth, ignition, spectrum, and honesty *simultaneously*. Every other concept is elite at one law and fails another; #1 is the laws, made visible. It is also already proven in our toolbox — the Smart Tabs kit is this button, working.

---

## PART 2 — BOARDS (cards & panels)

### The anatomy (six zones)

1. **Ground plane** — obsidian glass, one elevation above the page ground, colored shadow.
2. **Rim light** — the same three-line rim as the button; the board and the button are visibly siblings.
3. **Header strip** — jewel + title + live state (breathing dot when streaming) + the ↗ one-tap-to-detail corner.
4. **Body zone** — exactly one subject per board; white space is a designed material, not an absence.
5. **Spectrum spine** — a thin spectrum edge or header accent in the board's category color (stats boards take their WHAT-category color).
6. **Footer/action zone** (optional) — the board's verbs, as standard buttons, never text links pretending.

**Proportions:** the board family is 16:9. Strips (Pulse Strip) are the wide exception; tiles are square members of the same family.

### The top ten board concepts

| # | Concept | Verdict |
|---|---|---|
| 1 | **Obsidian bento** (Apple-marketing bento grid, in glass + rim light) | 🏆 — modular, symmetrical, family-obvious; 16:9 tiles compose into any page |
| 2 | **Apple Weather glass cards** | Gorgeous depth; borrow the glass recipe |
| 3 | **Trackify dark-purple analytics panels** | Our family's skin (canon) — the bar for stats boards specifically |
| 4 | **Bloomberg terminal panes** | Density king; pro dialect only, too cold for citizens |
| 5 | **Linear issue cards** | Elite minimal; flat — fails depth |
| 6 | **Game inventory panels** | Alive, jewel-framed; restraint risk |
| 7 | **Notion blocks** | Flexible; visually anonymous — no family resemblance |
| 8 | **Figma canvas cards** | Tool-grade; not an experience |
| 9 | **Windows Fluent acrylic** | Real depth material; color language foreign |
| 10 | **Paper/minimal light cards** | Rejected — light ground is dead here |

**🏆 THE CHOICE: Obsidian bento** — bento proportions + Apple-Weather glass + our rim light and spectrum spine. Stats boards additionally inherit the Trackify skin discipline via the Smart Stats spec. **Why:** bento is the only layout grammar that makes *symmetry itself* the brand — a page of bento boards reads as one family at a glance, which is the franchise test.

---

## PART 3 — ICONS

### The anatomy

1. **The glyph** — geometric construction on a 24-unit grid, one stroke weight family-wide, optically sized (a glyph that *measures* the same but *looks* smaller gets drawn bigger).
2. **The chip** — every system glyph lives in a jewel chip (disc or rounded square) with rim light; the chip is the family uniform.
3. **The color job** — the chip carries the element's one color; the glyph itself is white at rest, ignites with the chip.
4. **The marks** — ⭐ favorite (L1) · 💜 priority (L2) · ◆ diamond bullets · twin pluses (＋＋) — our native glyphs, drawn in the same geometry.

### The top ten icon concepts

| # | Concept | Verdict |
|---|---|---|
| 1 | **Custom geometric glyphs in jewel chips** (ours) | 🏆 — the chip + color job is the identity; glyphs become ownable |
| 2 | **SF Symbols** (Apple) | The drafting base — optical sizing discipline unmatched |
| 3 | **Phosphor duotone** | Two-tone depth; close cousin to our chip idea |
| 4 | **Material Symbols** | Complete coverage; generic face |
| 5 | **Fluent 2 filled** | Solid, friendly; foreign color language |
| 6 | **Lucide / Feather line icons** | Clean open set; line weight too thin at rest against obsidian |
| 7 | **Game jewel icons** | Alive; per-icon art cost, consistency risk |
| 8 | **3D rendered icons** (clay style) | Delightful; heavy, slow, off-depth-system |
| 9 | **Emoji as system icons** | Rejected — renders differently on every device; no family control |
| 10 | **Pixel icons** | Rejected — wrong era, wrong brand |

**🏆 THE CHOICE: #1** — a custom geometric set, drafted with SF Symbols' optical discipline, housed in jewel chips. **Why:** an icon set anyone can download makes us look like everyone; the glyph is a commodity, but *glyph + jewel chip + one color job + ignition* is a signature. And the family test: a citizen should know an icon is ours with the label removed.

---

## PART 4 — INPUTS

### The anatomy

Inputs are the inverse of buttons: **buttons rise, inputs sink.** A recessed obsidian well — inner shadow at the top edge, rim light at the bottom — with: a jewel caret · a spectrum focus ring (ignition on focus, in the field's color) · furniture chips inside the well (Dictate 🎙 · Schedule · attach) as standard buttons · states designed: hint (dim, honest), typing, error (red rim + the reason in words), success (gold flash). The composer is **one canonical part, verbatim on every page** — today's scorecard caught Business missing Dictate + Schedule; that class of drift dies when the composer is an import.

### The top ten input concepts

| # | Concept | Verdict |
|---|---|---|
| 1 | **The composer jewel** (ours — recessed well + furniture + ignition ring) | 🏆 |
| 2 | **ChatGPT composer** (rounded well, tool chips) | The pattern citizens already know; borrow the familiarity |
| 3 | **Raycast command input** | Pro density; the Ask Naya face's dialect |
| 4 | **Apple Spotlight** | One field, whole system — the search ideal (see Part 6) |
| 5 | **Superhuman composer** | Speed craft; email-specific |
| 6 | **Linear slash-command field** | Power grammar; one feature (the /) worth adopting |
| 7 | **iOS Messages bar** | Thumb-perfect; too little furniture |
| 8 | **Material filled field** | Systematic; the underline reads dated and flat |
| 9 | **Voice-first input** | Our Dictate chip grows from here; not a whole field |
| 10 | **Classic bordered form field** | Rejected — the flat default |

**🏆 THE CHOICE: #1**, familiar as #2, with #6's slash grammar inside Smart Mail and Ask Naya. **Why:** input is where citizens *give* the system things; the reciprocity engine starts here. A well that feels physical and answers instantly (ignition on focus) makes giving feel like the premium act it is.

---

## PART 5 — GRAPHS & CHARTS

### The anatomy

Locked colors per WHAT category (Smart Stats spec §3) · living draw-in on load · drill-down on every mark · the human sentence under every chart (SN-0822) · honest empty frame when unwired · every animated tick is a real ledger event (the tick rule).

### The top ten chart concepts

| # | Concept | Verdict |
|---|---|---|
| 1 | **The Naya Smart Stats set** (8 blocks + per-source grammars: steps, constellation, ripples, branches, funnel, climb, closing ring, the River) | 🏆 — already converged by two seats independently; specified 2026-10-22, build spec v3 today |
| 2 | **Robinhood living line** | The flood-the-environment lesson; borrow wholesale |
| 3 | **Trackify analytics** | The family skin for stats; canon |
| 4 | **Apple Health rings & bars** | The closing-ring grammar's ancestor; citizen-readable |
| 5 | **Strava elevation** | One metric, beautifully told — restraint lesson |
| 6 | **Bloomberg terminal charts** | Pro dialect, density reference |
| 7 | **Looker / Databricks BI grids** | Composability lesson (add-a-block) |
| 8 | **Linear sparklines** | The mini-trend inside chips and strips |
| 9 | **Candlestick / trading charts** | Money dialect only |
| 10 | **Static chart images** | Rejected — a photograph of data is dead data |

**🏆 THE CHOICE: #1** — it already exists as spec; this canon simply ratifies its place: charts are not a page element among others, they are the Vitality Law's proof. No claim without its graph.

---

## PART 6 — THE REST OF THE PAGE (anatomy + choice, one line each)

- **Top bar / Smart Bar** — two families on every bar: the app's own sections + related areas as quick tabs; living-depth pills; the breathing jewel; search mounted in the chrome, one wording, network-wide. *Choice: the conformed Smart Bar system — one mount, Nitro renders, seats import.*
- **Bottom network bar** — the identical 11-app bar on every page; the franchise's most visible proof. *Choice: as live today — it is already the family constant.*
- **Tabs** — Smart Tabs kit v9 anatomy: white at rest, ignite on touch, state persists and follows the user. *Choice: the kit, canon.*
- **Toggles & switches** — a jewel sliding in a recessed track; on = ignited color + white jewel forward. Never a bare checkbox on a citizen surface.
- **Sliders** — spectrum track, jewel thumb ≥44px, live value in a chip that ignites while sliding.
- **Faces / avatars** — real photo in a rim-lit ring; presence = breathing ring in the person's spectrum position; staleness shown honestly ("last active 9d ago" is data, styled as data).
- **Badges & chips** — state words only when true; a chip that says SOON is dead chrome and is banned. Honest-state chips: LIVE (green pulse) · NOT TRACKED YET (dim frame) · SAMPLE (specimens only, never removable).
- **Menus & popovers** — glass sheets rising from the element that summoned them; one level deep; every item a standard button row.
- **Modals & sheets** — the page dims, the sheet rises with rim light; one decision per sheet; the commit action takes the Signature level (obsidian, maximum ignition).
- **Toasts** — bottom-rise, jewel + one sentence + one action; auto-dismiss except errors, which stay until answered.
- **Lists & tables** — rows as flat members of the board family (rim on hover), diamond bullets, ranked bars for ordered data; a table is a board whose body is rows.
- **Search** — ONE search: chrome-mounted, one wording ("Search the network…"), Spotlight grammar — one field, whole system, results filtered Blocks · People · Spaces · Pages · All.
- **Media player** — the play disc with jewels (canon): a rim-lit disc, jewels at the rim, ignites on play; progress as a closing ring.
- **Progress** — rings close, bars fill left-to-right in spectrum order, counters count; never an indeterminate spinner where a real number exists.
- **Empty states** — an honest frame: what will live here, why it's empty, the one action that fills it. An empty heading with nothing under it (today's "Latest conversations") is the defect this anatomy exists to prevent.
- **Loading** — the breathing jewel + the skeleton of the real board in its real proportions. The shape of the answer arrives before the answer.

---

## PART 7 — WHAT WE DON'T DO

White or light backgrounds · flat buttons with an icon pasted on · glow for decoration · the same color twice in a row · locally varied components · dead buttons and SOON pills · fake numbers and SAMPLE outside labeled specimens · text walls describing life instead of showing it · emoji as system icons · indeterminate spinners over knowable numbers · any element in only one state · any part a builder has to redraw instead of import.

## PART 8 — THE PRE-MADE PARTS LIST (what the Factory stocks first)

`.naya-btn` (hero / primary / standard / compact / jewel) · `.naya-board` (16:9 + strip + tile) · `.naya-chip-icon` (the glyph set v1, 24-grid) · `.naya-composer` (verbatim, with Dictate + Schedule) · `.naya-input` · the 8 Smart Stats blocks · `.naya-bar` (top mount + bottom network bar) · `.naya-tabs` (kit v9) · `.naya-toggle` · `.naya-slider` · `.naya-face` · `.naya-sheet` · `.naya-toast` · `.naya-play-disc` · `.naya-empty-frame` · `.naya-skeleton`.

**Toolbox verdict:** every chosen part is buildable in our actual stack — HTML/CSS layered shadows, gradients and blur, inline SVG glyphs and charts, the Smart Tabs kit already working. No WebGL, no exotic dependency. The elite is achievable *with what we have*; that was a selection criterion, not an afterthought.

**How it locks in:** parts ship as imports from the Factory registry → the gate checks the anatomy as code (layer count and rim presence via computed styles, spectrum walk, contrast ratios, touch targets, state completeness, reconciliation for stats) → every correction Shawn ever makes becomes a regression test → the floor only rises.

— Naya Resolve, 2026-10-31
