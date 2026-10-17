# NAYA SMART BLOCKS — the catalog

Every reusable piece. Name it, snap it in, never reinvent it.
A block ships with: its code, its states, a do/don't, and honest anatomy.
A block without all four is a draft.

_Adoption 2026-10-16: 144 extracted blocks merged in (model-numbered BTN–MSC). The button-taxonomy ruling is a working default, pending Shawn's formal ruling._

_Adoption 2026-10-16: 19 gap blocks integrated (CAL/PAY/CMT/CHT/ONB) with full spec files under `DESIGN/gap-blocks/` and `DESIGN/gap-blocks-2/`. Wave 1 scored 9.0 (calendar) / 8.8 (checkout) with identified fixes pending; wave 2 mechanically verified, independent scorecard pending. Nothing here is claimed above its evidence._

## Buttons — one canonical DNA

**Law 21: one canonical button. `.naya-btn` is the only button system.**
54px min-height, 999px radius, black gradient heart, 1.5px white-ish idle
border, inset top-light + inset bottom-shadow + drop shadow. Hover lifts with
a flowing conic ring; press compresses. No flat buttons — ever.

**The seven variants — the variant for each job:**

| Variant | The job |
|---|---|
| `.naya-btn.lead` | Flagship CTA. The obsidian pill — strongest depth + restraint. |
| `.naya-btn.machine` | Maximum clarity at rest. Dense UI, law surfaces. |
| `.naya-btn.streak` | Light-streak sweep. Announcements, launches. |
| `.naya-btn.proximity` | Cursor-tracking spotlight; wakes before touch. Living controls. |
| `.naya-btn.icon` | Glyph-only actions. 58px circle (`.micro`: 44px). |
| `.naya-btn.icon.portal` | PLAY. 66px media-play circle. Play is always a portal. |
| `.naya-btn--quiet` | Low-emphasis action. Same DNA, minimal chrome — speaks softly. |

Sizes: `.small` (44px), `.compact` (42px). States: rest · hover/focus ·
active · disabled — all five, every variant.

Retired studies (`.living-btn`, `.lv-btn`, `.cx-btn`, `.orbit-btn`) are
documented in `DECISIONS.md` — considered and retired, not live options.
A new button idea becomes a `.naya-btn` variant proposal, never a new system.

**Glyph law:** the glyph promises the action — plus means add, chevron means
go, triangle means play. Icons are drawn, not shrunk: vector geometry,
readable at 16px. A shrunken render is mud.

**Button ruling (2026-10-16 — working default, pending Shawn's formal ruling).**
The seven job-based variants above stay canonical. The N4 v2.0 names are
documented aliases, not new variants: `primary` → `lead` · `secondary` →
`machine` · `ghost` → `quiet`. `danger` is a new variant PROPOSAL —
documented, not adopted. The other variant candidates (`.naya-btn.split`,
`.naya-btn.prism`) are proposals, not adopted. A new button idea becomes a
`.naya-btn` variant proposal, never a new system.

**BTN-008 — Button color variants.** Four job-colored skins on the same
`.naya-btn` DNA, framed under the canonical taxonomy. The `lead` skin (v2.0
"primary"): purple edge fire (`--nb-accent:#8a5cff`) — the one action the
page exists to do, one per view, never two side by side. The `machine` skin
(v2.0 "secondary"): same obsidian body with silver-white fire (`#e8e6df`)
— sits beside a lead without competing; supporting actions, paired actions,
toolbars. The `quiet` skin (v2.0 "ghost"): transparent body, hairline rim
only, white fire, the softest breathing in the set — low-stakes, reversible,
dismissive exits. The `danger` skin: obsidian body washed with red, red edge
fire (`#ff4d5e`) — destructive or hard-to-undo actions, always with
confirmation, never the default dialog button; a variant PROPOSAL,
documented, not adopted. Icon slots take glyphs (✦, →, ✕).
_Source:_ Naya_Design_Element_Set_N4.html

**BTN-009 — Primary button set (the hub `.btn`).** Pill button (42px min,
12.5px bold small-caps label, optional 15px icon): accent-tinted gradient
with white inset edge and colored glow; hover lifts 2px and brightens;
active presses in. The quiet variant (v2.0 "ghost") is transparent with a
hairline border that tints accent on hover. Disabled drops to 45% opacity,
no motion. _Use:_ Lead and machine actions everywhere — buttons inherit
`--btn-accent`.
_Source:_ Naya_Smart_Hub_Design.html · _hub implementation of `.naya-btn` DNA_

## The 21 universal actions

Twenty-one actions. One living DNA. Every icon block derives from `.naya-btn`.

LIKE · SHARE · ADD · PLAY · PAUSE · SEARCH · NOTIFY · SAVE · COMMENT · MORE ·
CLOSE · BACK · VERIFIED · PREMIUM · SEND · DOWNLOAD · OPEN LINK · SETTINGS ·
PROFILE · PRIVATE · PUBLIC.

PLAY is a portal (white triangle, black field, jewel ring). Every other action
keeps the same physical law: black body, white icon, one accent.

## SmartTabs

The universal favorites ribbon — one ribbon, follows the user across every
page. Pills with add/edit/heart/star/remove, right-click menu, localStorage
persistence. Hearts outrank stars: the most important tabs rise to the top.
Mount once: `SmartTabs.mount({container, storageKey})`.

**TAB-001 — SmartTabs v9.** A pill-shaped ribbon bar (dark glassy track with
a white inner rim and deep inset shadow) holding pill shortcut tabs: 44px
tall dark pills with 1.5px white rims, white bold labels, a ⋯ edit
affordance at each pill's end, and per-tab spectrum colors that ignite on
touch. Demonstrated tabs: SoulSchool 💜 (heart/priority state, active,
magenta), Ambassadors ⭐ (star/favorite, purple), ViralTips (blue),
SmartHealth (green), plus a dashed-outline "＋ Add" pill. The heart tab shows
a lavender inner halo; the active tab glows in its own color. A status line
beneath speaks state ("Now showing: SoulSchool — click navigates, ⋯
edits."); adding tabs cycles colors from the palette. _Use:_ "Your favorites
follow you everywhere" — one persistent ribbon, mounted once on every page;
pill shortcuts with heart (priority) and star (favorite) states.
_Source:_ Naya_Design_Element_Set_N4.html · _v9 implementation + state machine_

## Boards — "A world, not a rectangle. One board, one color."

Three systems (N5, copy-paste ready):

| Block | Use |
|---|---|
| `.board-mix` | Theme-edged destination: glowing spine, corner jewel (◆), theme border. A world you enter. |
| `.board-tone` | Tone spine + radial tone wash, hover border-light. Quieter destinations. |
| `.layer` | Nested meaning cards inside boards — "In a nutshell" → "What it means" → "How to use it". |

CSS → canonical type: `.board-mix` = **Destination** · `.board-tone` = **Reading** · `.layer` = **Orbit** (nested meaning-layers).

Board recipe (Law 31): dark obsidian body · theme-tinted hairline edge ·
radial wash in the cover zone only · white title · silver body · jewel kicker.
One spectrum step per board. One accent per element. One jewel per board.

Board type framing (Naya_2 canonical, verified 2026-10-16): **Destination**
(a world you enter — strongest elevation) / **Reading** (asymmetric, quieter
spectrum — reports, dense text) / **Orbit** (circular crown — connected
objects).

**BRD-005 — Destination board (specimen).** A black board with a 7-pixel
vertical identity spine in magenta on its left edge, a lit semantic edge, a
visible "lower deck" at the bottom, and a spark icon set into a
`board-corner` jewel. Labeled "A · NAYA 4 · AUTHORITY — The destination
board"; footer tags: "Strongest elevation", "Best for primary intelligence".
_Use:_ Primary intelligence surfaces — the board that must feel placed in
space, not pasted on a page.
_Source:_ Naya_Building_Blocks_Naya_2.html · _extends the Destination type_

**BRD-006 — Orbit board (specimen).** A black board with a softened circular
crown — the top edge curves in a circular arc — in a blue tone with an orbit
icon in the corner jewel. Labeled "C · RELATIONAL — The orbit board"; footer
tags: "Best for connected objects", "Circular + board language". _Use:_
Connected objects — systems, relationships, movement — where circular
language meets board authority.
_Source:_ Naya_Building_Blocks_Naya_2.html · _extends the Orbit type_

**BRD-007 — Reading board (specimen).** A black board with an asymmetric
silhouette and a quieter indigo spectrum field (blue #6675ff tone, bars icon
in the corner jewel). Labeled "B · EDITORIAL — The reading board"; footer
tags: "Best for reports", "Supports dense explanation". _Use:_ Long-form
understanding — reports and dense explanation that need to feel composed, not
carded.
_Source:_ Naya_Building_Blocks_Naya_2.html · _extends the Reading type_

**BRD-008 — Theme board.** A large rounded (22px) dark panel, theme-edged: a
2px glowing border in one spectrum color (`--ic`), a vertical glowing spine
on the left edge (white fading into the theme color), a hairline key-light
across the top, and a glowing corner jewel (rounded square with radial-gem
fill) at top right. Inside: a letterspaced kicker in the theme color, a serif
voice headline (24px), and body text in white. On hover the whole board lifts
3px and its color glow intensifies. Described as "lit at rest." _Use:_ The
intelligent object — "one board, one color, a destination you enter."
Theme-edged, jewel-marked, elevated; spine, kicker, and corner jewel all
speak the same single spectrum color; text stays white.
_Source:_ Naya_Design_Element_Set_N4.html · _extends `.board-mix`_

**LST-002 — Intelligence layer rows.** Three stacked rows, each opening with
a small faceted glowing gem bullet and a tracked kicker — "WHAT IT MEANS"
(magenta), "HOW TO USE IT" (blue), "WHAT YOU GET" (gold) — followed by one
plain sentence each ("Learning changes what the intelligence does next.",
etc.). _Use:_ The three questions every lesson must answer — meaning, use,
value — inside any intelligence board.
_Source:_ Naya_Building_Blocks_Naya_2.html · _extends `.layer` rows_

## Orbs & jewels — "Spherical. Orbital. Lit from within."

| Block | Use |
|---|---|
| `.orb` | 120px sphere: white hotspot, color core, black falloff, orbiting light ring, light pool beneath, 5s breathe. One `--oc`/`--oc-rgb` property drives everything. |
| `.orb--xs` / `--sm` | 30px bullets / 56px section marks. |
| `.orb--black` | Dark soul, color rim. |
| `.orb--hero` | 200px, twin counter-rotating orbits. One per page, never more. |
| `.orb--glyph` / `--icon` | App icon at core / 64px room icons. |
| `.orb--twin` / `--btn` | Twin rings / pressable (scales .9). |
| `.mini-orb` | 34px luminous mark. |
| `.gem-bullet` | 12px rotated diamond, white→color gradient, glowing. Every bullet a jewel — never twice in a row. |

Five-jewel bullet cycle: magenta → purple → blue → green → gold, in law
order, never adjacent duplicates. One global sequence per page.

**ORB-010 — Logo orb.** A 110px perfect circle (64px in the footer, 88px on
mobile) carrying the Naya emblem, ringed by a soft purple drop-shadow glow
(`drop-shadow(0 0 30px rgba(138,92,255,.6))`) so it floats as a ball of light
on the obsidian field. Footer version is smaller with a softer halo. _Use:_
The mark of the page — front door and sign-off.
_Source:_ Naya_Design_Element_Set_N4.html · _logo-as-orb_

**ORB-011 — Orb mark.** A 58px black orb with a jewel-dark radial face (lit
from upper-left), an inset highlight and deep bottom shadow. A thin ring of
orbiting light — purple-to-white arc segments — spins around its edge on a 5s
loop (conic gradient masked to a ring). Behind it, a soft white backlight
breathes (6s scale/opacity pulse). _Use:_ Brand mark / "living" identity
element — the signature orb treatment that says "Naya is here," used in
headers and front doors.
_Source:_ Naya_Design_Elements_N2.html · _orbiting-light + backlight spec_

**ORB-012 — Hero vessel.** A tall dark "vessel" stage holding the Naya
crystal logo, surrounded by three thin, slowly rotating orbit rings (classes
`orbit`, `orbit b`, `orbit c`), with a small tracked caption anchored at the
bottom ("ONE INTELLIGENCE · MANY DOORS"). _Use:_ The hero/entrance sign of
life — decorative motion that says the system is alive, never spectacle.
_Source:_ Naya_Building_Blocks_Naya_2.html · _hero-scale orbital display_

**ORB-013 — Orbital diagram.** A board headlined "Relationship is circular."
carrying a decorative orbit diagram: two thin concentric track rings around a
glowing `orbital-core` with a people icon. Caption: "A center, its context
and the forces moving around it." _Use:_ Showing connection and systems
without turning every surface into a card — circular language for
relationships.
_Source:_ Naya_Building_Blocks_Naya_2.html

**ORB-014 — Sphere cards.** Five small dark cards, each with a glowing
sphere — a luminous orb with a white line icon inside — above a heading and
one-line purpose: Priority (magenta #e455f4, spark icon, "What matters now"),
Presence (purple #8d63f5, orbit icon, "Naya is here"), Understanding (blue
#3f9ff5, book icon, "Knowledge in context"), Verified (green #34d38a,
"Evidence exists"), Value (gold #e7c65a, "What was gained"). _Use:_ Making
invisible relationships visible — identity, state, signal, connection,
portals. Never use a sphere where a plain button would communicate better.
_Source:_ Naya_Building_Blocks_Naya_2.html

**JWL-001 — Five-jewel cycle strip.** A centered row of five 30px
rounded-square jewels, each a radial-gradient glowing gem (white hot-spot
top-left, spectrum color, melting to black) with a white 1px rim and colored
glow, each bearing a white glyph (◆ ✧ ▲ ✦ ◆). The colors cycle magenta →
purple → blue → green → gold. _Use:_ Displaying the jewel palette's
canonical five-stop cycle.
_Source:_ Naya_Lego_Blocks_N4.html · _cycle reference specimen_

**JWL-002 — Gem bullet (canonical spec).** A small (30px, down to 20px
inline) rotated-square diamond with a radial-gradient glow — bright white-hot
highlight top-left, the spectrum color at its heart fading to black — white
1px rim and a colored outer glow. Carries a glyph (◆ ✧ ▲ ✦ ✓ ? ◈ ✕) in
white. Colors cycle the page's five-jewel sequence: magenta → purple → blue
→ green → gold; no two adjacent jewels share a color. A "dark" failure
variant exists: near-black heart, red rim, red glow, ✕/✖/× glyph — used for
drift reports. _Use:_ The atomic marker of the visual language — bullets,
markers, board corners, section-head accents. Every bullet a jewel, never
twice in a row.
_Source:_ Naya_Design_Standard_Showcase__1.html · _canonical `.gem-bullet` spec_

**JWL-004 — Corner jewel.** A 36px rounded-square gem (◆) set in the
top-right corner of a board — glossy white facet highlight over the board's
identity color, ringed in white, glowing. _Use:_ Marking a board's identity
color; the jewel that says "this board belongs to this spectrum slot."
_Source:_ Naya_Epic_Elements_-_Lego_pieces_N5.html

**JWL-005 — Identity emblem.** 84px rounded-square spectrum jewel (conic
magenta→green) with white highlight and purple halo; hover grows 1.05× and
tilts 2°. _Use:_ The identity card's emblem (login/identity view).
_Source:_ Naya_Smart_Hub_Design.html

**JWL-006 — Jewel bullet list.** A vertical list where each item opens with
a glowing jewel (cycling magenta → purple → blue → green → gold) followed by
18px white text. Each bullet's color advances the page sequence, and the
closing item earns the gold jewel. A spacious panel variant (`.hbul`) uses
larger gaps for philosophy/panel contexts. _Use:_ Any list where bullets must
be drawn jewels, not dots — each point glowing its own spectrum color.
_Source:_ Naya_Design_Standard_Showcase__1.html

**JWL-007 — Jewel socket.** A faceted jewel socket — a small cut-gem shape
with a glowing spectrum edge — holding fine white line art. Ten shown as
tiles: Today (diamond, magenta, spark), Spaces (circle, purple, grid),
Reports (square, indigo, bars), Mail (diamond, blue, mail), Ask (circle,
cyan, search), Doors (square, green, door), People (circle, light green,
people), Ledger (diamond, gold, pulse), Grow (circle, orange, orbit), Guard
(square, red, shield). _Use:_ Micro icons that stay beautiful at 16px —
destinations, states, and intelligence given one shared jewel language. The
icon stays white; the meaning supplies the spectrum color.
_Source:_ Naya_Building_Blocks_Naya_2.html

**JWL-008 — Layer jewel.** 36px circle: black core, 2.5px colored stroke ring
+ faint outer ring, bold white glyph centered, colored glow halo around the
whole thing. _Use:_ The jewel that sits in each `.ib-layer` header.
_Source:_ Naya_Smart_Hub_Design.html

**JWL-009 — Portal jewel.** 118px rounded square (38px radius) carrying the
full conic spectrum (magenta→purple→indigo→sapphire→blue→teal→green→
lime→yellow→gold→orange→red→magenta) under a white specular sheen, with an
inset rim and a 90px magenta halo; gently "breathes" (scale 1→1.035, 5s).
_Use:_ The welcome screen's centerpiece — the "one brain" symbol.
_Source:_ Naya_Smart_Hub_Design.html

**JWL-010 — Premium jewel.** Small (26px) or large (44px) rounded-square
jewel tile: radial-lit color face, white highlight, inset depth, colored glow
shadow; can hold a tiny bold glyph or number. _Use:_ Reports-grade decorative
markers and numbered/lettered list markers (JS-rendered).
_Source:_ Naya_Smart_Hub_Design.html

**JWL-011 — V10 jewel.** 30–32px SVG jewel drawn as true faceted geometry:
identity-color core + white facet light + black shade depth + crisp white
edge rim, with a dual drop-shadow (dark + colored glow). _Use:_ Per-layer
icons in the intelligent board — each intelligence layer gets its own jewel,
never a generic dot.
_Source:_ Naya_Smart_Hub_Design.html

## Truth components — "A claim and a proof must never look the same."

| Block | Use |
|---|---|
| `.truth` card + `.torb` orb | Three states: VERIFIED (green ✓ — independent evidence exists) · CLAIM (gold ? — shown honestly, awaiting its stamp) · DEMONSTRATION (magenta ◈ — beautiful on purpose, a specimen, not live). |
| Truth badges | ✓ AUTH·VERIFIED / ? CLAIM·UNVERIFIED / ◈ DEMONSTRATION — stamped on content. |
| Truth orbs as objects | Green = proven · gold = shown · blue = stated. |

Law 75: loading is honest. Fake success is a trust violation.

**JWL-003 — Truth orbs.** Three 56px section-mark orbs (`.orb--sm`), each
locked to one truth color with its name underneath: green "VERIFIED —
Proven, glowing green", gold "DEMONSTRATION — Shown, golden", blue "CLAIM —
Stated, quiet blue". The truth language as objects. _Use:_ Marking the
verification state of content inline — proven (green), demonstrated specimen
(gold), stated claim (blue); the verification ladder, made visual.
_Source:_ Naya_Jewel_Library_-_N5.html · _extends the truth orbs_

**CRD-006 — Truth cards.** Three dark cards, each with a 44px glowing
circular orb (`.torb`) on the left — green with ✓, gold with ?, magenta with
◈ — then an uppercase letterspaced label ("AUTH · VERIFIED" / "CLAIM ·
UNVERIFIED" / "DEMONSTRATION") and one 18px white sentence. The orb is a
ringed circle with a radial glow in its truth color; the card lifts 3px on
hover and glows in that same color. _Use:_ "Truth is part of the visual
language": a claim and a proof must never look the same. Green = verified
(independent evidence exists); gold = claimed but unverified (shown honestly,
never hidden); magenta = demonstration/specimen content (beautiful on
purpose, not pretending to be live).
_Source:_ Naya_Design_Element_Set_N4.html · _extends `.truth` / `.torb`_

**BDG-002 — Honesty state badge.** Inline small-caps pill with a *dashed*
accent border — "the honesty system, inline". _Use:_ Declaring an object's
honest state (e.g. IN USE on a door) wherever a full panel is too much.
_Source:_ Naya_Smart_Hub_Design.html · _extends the truth badges_

**BDG-003 — Truth badge.** A tiny dark pill (11px, letterspaced,
uppercase-feeling) with a glowing 8px status dot in front. Variants: `.live`
(green dot), `.demo` (gold dot), `.local` (blue dot); dot color driven by
`--tc`. _Use:_ Labeling a specimen's truth state — live data vs demo vs
local — inline next to a component name.
_Source:_ Naya_Design_Elements_N2.html · _extends the truth badges_

## The Intelligent Block pattern

The Smart Note anatomy. "A lesson that stays learned. One object. Four
layers of understanding. One clear next action."

**IN A NUTSHELL** → **WHAT IT MEANS** → **HOW TO USE IT** → **WHAT YOU GET.**

Every Smart Note card, every lesson surface, every report summary follows this
anatomy. Same order, every time.

**ACC-001 — Intel layer accordion.** Rounded panel (18px radius) whose border
and halo are tinted by the layer's meaning-color; the header row is a button
with the layer jewel, bold label, a right-side state label and (where
replaced) a chevron; the body holds 17px prose, jewel-bulleted lists and code
chips. Each of the 13 layer types wears a fixed law color: white (the words)
· magenta (human significance) · sapphire (calm clarity) · emerald (alive
and well) · purple (Naya's signature) · indigo (comprehension) · lime
(growth) · gold (the extraordinary) · orange (action) · teal (flow) ·
yellow (attention) · rich-orange (momentum) · red (the alarm). Deeper layers
render quieter until opened. _Use:_ The layered voices of a Smart Note —
human / child / grandma / naya / machine / meaning / apply / value /
decisions / learning / connects / proof / truth-boundary / next-action.
_Source:_ Naya_Smart_Hub_Design.html

## The ten canonical blocks

| Block | Job | Do / Don't |
|---|---|---|
| INPUT / FORM | Capture user input | Do elevate above context · Don't float without weight |
| MODAL / DIALOG | Focused decisions | One clear action · Never trap without escape |
| TOAST / NOTIFICATION | Report what happened | Do report truthfully, brief, dismissible · Don't fake success |
| DATA TABLE | Aligned data | Do align labels left, numbers right · Don't center every column |
| SEARCH INTERFACE | Governed search | Do show scope + truth state · Don't return mystery results |
| TOGGLE / SETTINGS | Binary + preference state | State unmistakable · Never ambiguous |
| CONTENT CARD | Distinct content unit | One idea per card · Don't overload |
| MEDIA PLAYER | Audio/video | Portal-style play · Honest buffering |
| CHART / DATA-VIZ | Honest numbers | Axes labeled, no truncated deception |
| SMART LINK / SHARE SHEET | Send intelligence out | Destination clear · Confirm before sending |

Status: specified with do/don't doctrine. Copy-paste code specimens: all 10
built and verified in `BLOCKS-CODE.md` (2026-10-16) — code, states, do/don't,
anatomy each.

**FRM-002 — Add-intel composer.** Dark inset box under the board:
small-caps label + a row with a full-width text input (glowing purple focus)
and a send button. _Use:_ Adding a human note to an intelligence board.
_Source:_ Naya_Smart_Hub_Design.html

**FRM-003 — Star rating.** Inline cluster of large gold star buttons
(46×44px) inside a dark gold-bordered rounded tray; hover/selected stars turn
bright cream with a gold glow; the pressed star does a quick scale pulse.
_Use:_ Rating an intelligent block.
_Source:_ Naya_Smart_Hub_Design.html

**MDL-002 — Mobile drawer.** The left rail slides in as a fixed 300px panel
from the left over a dimmed blurred backdrop; the page locks scrolling
behind it. _Use:_ Mobile navigation drawer.
_Source:_ Naya_Smart_Hub_Design.html

**MDL-003 — Tab popover.** Fixed floating popover panel: small-caps section
titles, rows with tab name + topic retarget dropdown + delete button, "add"
rows, toggle chips (heart/star marks — selected chip gets an inset glow ring),
footer with Cancel / primary-gradient Save. _Use:_ Adding, retargeting, and
deleting human Smart Tabs.
_Source:_ Naya_Smart_Hub_Design.html

**TBL-002 — Predicate row.** A single machine-law line: a 20px jewel, a
monospace predicate name (`jewel.adjacent_duplicate`,
`typography.hierarchy_px`), and a colored value (`forbidden`, `24 / 18 /
14`, `≥ 1.5`), separated by a faint hairline rule beneath. Jewel colors cycle
the spectrum; value text is colored to match its jewel. _Use:_ Checkable
machine predicates — the normative form of every law; a builder or a machine
can verify each row mechanically.
_Source:_ Naya_Design_Element_Set_N4.html · _machine-predicate readout_

**TBL-003 — Scorecard.** A bordered panel holding scored rows. Each row: a
dimension label (left, 18px bold), a large serif score number (32px Cormorant,
glowing in the row's own color), and a plain-words note. Rows carry a per-row
accent color on a 4px left border. Nine dimensions scored (Color discipline,
Lighting, Typography & craft, Copy, Icons & marks, Header composition, Layout
& metaphor, Aliveness, Gate honesty). _Use:_ The mandatory honest
self-scorecard — scoring the *rendered experience* against contract
dimensions, with the gap named rather than hidden.
_Source:_ Naya_Design_Elements_N2.html · _honest score readout_

**SRH-002 — Activity search pill.** Full-width pill input (white 25% border
on black); focus turns the border purple with a purple halo. _Use:_
Filtering the activity feed.
_Source:_ Naya_Smart_Hub_Design.html · _extends the SEARCH INTERFACE_

**SRH-003 — Ask Naya search.** Full-width search row (17px radius) — muted
search icon left, large 16px transparent input; focus turns the border
purple. Sits in its own padded chassis slot, always visible. _Use:_ The
hub-wide "ask Naya" search field.
_Source:_ Naya_Smart_Hub_Design.html

**SRH-004 — Global search results.** A result block under the search row:
15.5px/1.65 answer text plus an honest empty instrument when there's nothing.
_Use:_ Displaying the hub-wide search answer.
_Source:_ Naya_Smart_Hub_Design.html

**SRH-005 — Library search field.** Pill search bar (accent-tinted border,
deep shadow) with an icon and a transparent 15px input. _Use:_ Searching the
library room.
_Source:_ Naya_Smart_Hub_Design.html

**TOG-002 — Preference toggle chip.** Small rounded chip (white edge on
dark); selected gets an inset white ring + purple glow. _Use:_ Binary
preferences in the tab editor (heart/star marks).
_Source:_ Naya_Smart_Hub_Design.html

**TOG-003 — Rail toggle.** 48px black marble circle with an elegant white
plus, luminous white glow at rest. Hover: scales up 1.1× and the whole button
rotates 90° while the plus counter-rotates — igniting purple with a purple
halo. _Use:_ Collapsing/expanding the left rail (desktop); the ecosystem
plus variant opens the destinations menu.
_Source:_ Naya_Smart_Hub_Design.html

**CRD-004 — Activity card.** Event card (20px radius, blurred dark): glowing
6px accent bar down the left edge (pulsing), then jewel icon + small-caps
source + time row, bold headline, narrative paragraph, monospace metadata
line. The high-priority variant is larger with a ★ marker. Hover lifts 3px
and ignites the border in the accent; tap presses in. Cards animate in with a
rise-fade. _Use:_ The activity feed — "every event is a card, not a line."
_Source:_ Naya_Smart_Hub_Design.html · _extends the CONTENT CARD_

**MDA-002 — Naya voice play.** 32px black glass circle with a purple edge,
white play glyph glowing purple; hover grows it; while playing, the purple
halo breathes (1.8s pulse). _Use:_ Playing a spoken Naya Voice reading of
each intelligence layer.
_Source:_ Naya_Smart_Hub_Design.html

**CHT-002 — Metric ribbon.** A single bordered ribbon of stat cells
(hairline dividers, no gaps): each cell has a 28px bold number on top and a
10px small-caps muted label below. Unknown values render in accent color at a
smaller size instead of faking a number. _Use:_ At-a-glance numbers (reports,
dashboards).
_Source:_ Naya_Smart_Hub_Design.html · _extends CHART/DATA-VIZ_

## Supporting pieces

`.spectrum-bar` (5-segment law-order bar) · `.law-card` (ignites own color on
hover) · `.rule-board` (do/don't boards) · `.callout` (magenta-edged) ·
`.checklist` (green ✓) · `.copy-btn` + `pre.code` (every component ships
copy-paste code) · `.toc` pills · `.gate-bar` (spectrum launch bar).

**CRD-005 — Law cards.** Small dark cards in a 3-column grid, each headed by
a pill-shaped tag (uppercase letterspaced, colored border — e.g. lavender
"Primary", cream "Secondary", white "Ghost", pink "Danger", gold "Icon-only",
green "The Laws") followed by a serif voice heading ("The one action") and a
short plain-words paragraph with inline code chips naming example labels
(`Create App`, `Publish`, `Save`). _Use:_ Binding usage law to each button
variant — when to use it, when never to use it. The sixth card ("The Laws")
states the non-negotiables: one DNA across every app, verb-first
sentence-case labels, 44px minimum touch, focus ignites like hover, disabled
never ignites, fire is 5%.
_Source:_ Naya_Design_Element_Set_N4.html · _extends `.law-card`_

**LST-001 — Checklist.** Vertical stack of interactive rows: each row is a
dark rounded (16px) bar with a colored left accent border (per `--cc`). The
checkbox itself is custom — a 26px rounded square with a jewel-sheen face; on
hover the row shifts right 4px. When checked: the box fills with a green
jewel glow plus a white ✓, the row's border turns green, and the label text
strikes through and fades. _Use:_ Pre-ship / pre-flight checklists where each
item is individually confirmed; six items shown, each with its own spectrum
accent.
_Source:_ Naya_Design_Elements_N2.html · _extends `.checklist`_

**MSC-003 — Code recipe block.** A dark rounded code panel (monospace 14px,
line-height 1.7, soft inner top highlight) with lightweight syntax coloring:
comments in slate blue, keywords in magenta, strings in gold, function names
in blue. Contains the copy-verbatim button markup, the CSS recipe (condensed),
and the aware-proximity JS. White space pre-wrapped, word-break for long
lines. _Use:_ "The code that teaches" — paste-ready, minimal, commented
specimens builders copy verbatim into smart apps.
_Source:_ Naya_Design_Element_Set_N4.html · _extends `pre.code` / `.copy-btn`_

**MSC-004 — Spectrum meaning strip.** A wide rounded panel: a 64px
full-width gradient bar running magenta→purple→blue→green→gold across the
top; below it a "SPECTRUM — Meaning. One color per thing. Adjacent things
never share a hue." label; then five flexible cards, each glowing in one
spectrum color with its name and its meaning ("MAGENTA — The living edge",
"PURPLE — Choosing intelligence", "BLUE — Knowledge moving", "GREEN — Alive
and well", "GOLD — Attention, earned"). Each card lifts and ignites on hover.
_Use:_ Showing the whole spectrum at once with each color's identity meaning
— the reference strip for "one color per thing."
_Source:_ Naya_Design_Standard_Showcase__1.html · _extends `.spectrum-bar`_

**MSC-005 — Block-law footer strip.** A small footer inside each block-card:
bold "DO …" and "DON'T …" one-liners naming the rule that protects the
block. _Use:_ Keeping the governing law attached to every specimen.
_Source:_ Naya_Ultimate_Design_System_Naya_2.html

**MSC-006 — Board footer.** 12.5px muted line above a faint top border —
provenance/id text, wraps. _Use:_ Board provenance and machine identifiers.
_Source:_ Naya_Smart_Hub_Design.html

**MSC-007 — CTA row.** Centered wrapping flex row of buttons with 12–14px
gaps. _Use:_ Grouping call-to-action buttons (welcome, identity card).
_Source:_ Naya_Smart_Hub_Design.html

**MSC-008 — Constellation.** A dark panel (min 360px) with two faint
concentric orbit rings and a glowing accent core tile (74px rounded square)
at the center — a stylized node constellation; beside it a detail column.
_Use:_ The connections room's visual centerpiece.
_Source:_ Naya_Smart_Hub_Design.html · _connection graph_

**MSC-009 — Divider.** 1px hairline fading from transparent → line color →
transparent. _Use:_ Separating content.
_Source:_ Naya_Smart_Hub_Design.html

**MSC-010 — Empty instrument.** Dashed accent-bordered rounded box,
centered: 15px bold title + small muted explanation; the premium variant adds
a 76px glowing jewel icon on top and more padding. _Use:_ Honest "nothing
here" states inside search results and room compositions.
_Source:_ Naya_Smart_Hub_Design.html

**MSC-011 — Gate checklist.** A large rounded dark panel with a purple
glowing border and soft purple halo, containing a letterspaced kicker
("Pre-ship checklist · all must pass"), two phase eyebrows ("I · SEE", "II ·
PROVE"), and rows of checklist items — each a jewel followed by an 18px white
check line with bolded key verbs ("Rendered and **looked at** — screenshot
reviewed, not assumed."). Rows separated by faint hairlines. Checks split
mechanical (machine-checked: jewel colors, zero gray text, type scale) vs
human (real logo, human words, honest score 9.0+). _Use:_ The pre-ship gate —
every page runs it before it ships; "One fail — back to the bench." The
checklist where the fifteen laws become pass/fail.
_Source:_ Naya_Design_Element_Set_N4.html

**MSC-012 — Graduation loop.** Three concentric orbit rings around a glowing
core, ringed by nine numbered step markers: 01 Research, 02 Understand, 03
Distill, 04 Invent, 05 Build, 06 Experience, 07 Verify, 08 Learn, 09
Reproduce — under the headline "THE GRADUATION STANDARD — Excellence is a
loop that can teach itself." _Use:_ The system's own definition of done —
graduation is earned only when a cold Naya reproduces elite work without
being retaught; a process diagram, decorative rather than functional.
_Source:_ Naya_Building_Blocks_Naya_2.html

**MSC-013 — Hero date.** 18px semibold date line in primary text with a muted
time fragment after it. _Use:_ The dynamic date header in the feed.
_Source:_ Naya_Smart_Hub_Design.html

**MSC-014 — Honest state panel.** Centered panel (max 620px, 44px padding):
66px glowing accent icon, 17px heading, muted explanatory paragraph, and a
row of action buttons. The panel itself has a dashed accent border on a dark
wash — "nothing ever fakes data." _Use:_ The universal room state — every
room renders one of these for empty/error/unavailable; built by
`StatePanel()` with accent, icon, title, body, actions.
_Source:_ Naya_Smart_Hub_Design.html · _honesty system_

**MSC-015 — Microcopy trust signals.** 10px small-caps muted row split
left/right, sitting on a faint top border at the bottom of the board. _Use:_
Quiet provenance/trust microcopy under each board.
_Source:_ Naya_Smart_Hub_Design.html

**MSC-016 — Mission quote.** Centered moment above the bottom bar: 22px bold
quote text with a 15px muted sub-line beneath. _Use:_ A mission statement
moment pinned above the ecosystem bar.
_Source:_ Naya_Smart_Hub_Design.html

**MSC-017 — Premium empty state.** Centered column: glowing jewel icon, 19px
white honest title, 16px plain muted body (max 520px). Never a dev "not
connected" box — the `unavailable()` builder titles it "Quiet here —
honestly". _Use:_ The premium honest empty state for rooms with no qualifying
intelligence.
_Source:_ Naya_Smart_Hub_Design.html

**MSC-018 — Project activity section.** Purple-tinted glowing panel (20px
radius): muted explanatory note + a simple timeline (icon, 14px text, 12px
time). _Use:_ GitHub-synced project activity inside the activity room.
_Source:_ Naya_Smart_Hub_Design.html

**MSC-019 — Report footer.** A single small (14px) white meta line at page
bottom: status, version, amendment lineage, normative-source note, builder
credit, build date ("CANDIDATE · v2.0.0 · Amends v1.2 (PR #1910) · …").
_Use:_ Document provenance on contract/report pages — status, version,
lineage, who built it and when.
_Source:_ Naya_Design_Elements_N2.html

**MSC-020 — Shape key legend.** A small three-item legend: a tiny square
outline swatch + "Square = destination", a tiny circle outline + "Circle =
state", a tiny diamond outline + "Diamond = intelligence". _Use:_ Teaching
the jewel socket grammar at a glance — shape carries meaning, so icons never
need captions.
_Source:_ Naya_Building_Blocks_Naya_2.html

**MSC-021 — Spectrum token swatches.** 52px rounded-square color jewels —
each a saturated spectrum color with a glossy white highlight and its own
glow; on hover they lift and grow slightly. _Use:_ Interactive color pickers
in demos; the "try the law" controls.
_Source:_ Naya_Epic_Elements_-_Lego_pieces_N5.html

**MSC-022 — Verdict.** A centered serif display line (24px, white with a
soft gold halo glow) with the operative word in gold — "If a page violates
any **SHALL**, it does not ship." — followed by a small letterspaced sub-line
in muted white: "That is the whole contract." _Use:_ The final word on any
page — the one non-negotiable sentence; used to close a doctrine page with
the whole contract in two lines.
_Source:_ Naya_Design_Element_Set_N4.html

**LDR-001 — Loading shimmer.** Grid of 190px rounded skeleton cards; a
diagonal light band sweeps across them in the room's accent color (1.6s
loop). _Use:_ Loading placeholders while a room fetches data — shimmer, never
fake success (Law 75: loading is honest).
_Source:_ Naya_Smart_Hub_Design.html

## Button systems & specimens — one DNA, many jobs

One DNA, many jobs. Systems and specimens that live under the seven
canonical variants — a new idea becomes a `.naya-btn` variant proposal,
never a new system.

**BTN-010 — Board action system.** A footer bar split into left/center/right
zones holding tall (52px) pill buttons, each tinted by its action kind:
create-space purple, favorite gold, save blue, love red, like blue,
share-intel violet. Hover lifts and brightens; the active ("on") state
deepens the glow (love-on turns dark red). Includes an inline star-rating
cluster and a count chip on each action. _Use:_ Social intelligence actions
on a board (love/like/favorite/save/share/star/create-space).
_Source:_ Naya_Smart_Hub_Design.html · _social action language_

**BTN-011 — Button state specimens.** Three dark cards in a row, each with a
letterspaced eyebrow ("01 · SLEEPING" in dim cream, "02 · AWARE" in bright
silver, "03 · IGNITED" in glowing lavender), a live button specimen inside,
and a one-paragraph plain-words explanation of the state below it. The
Ignited card's specimen is frozen mid-hover (lifted 3px, scaled 1.012) so
the state is visible without touching anything. _Use:_ Teaching a
motion/interaction state statically — shows what each awareness state looks
like and says what it means, so builders implement them correctly without
running the demo.
_Source:_ Naya_Design_Element_Set_N4.html

**BTN-012 — Button state strip.** A single dark row of four small (`small`)
buttons — "Rest" (purple), "Hover / focus" (blue, force-lit), "Active"
(green, force-pressed), "Disabled" (dimmed, unclickable) — proving all five
mandatory states side by side. _Use:_ State coverage proof — no button ships
without rest, hover, focus, active, and disabled shown together.
_Source:_ Naya_Building_Blocks_Naya_2.html · _state-coverage specimen_

**BTN-013 — Foundation buttons.** Three large horizontal specimen buttons in
a flex row (`.trinity`), each min 74px tall with a 34px glowing jewel
(◆/✧/▲) on the left, a serif voice title ("BLACK GROUND" / "WHITE LIGHT" /
"PURPLE SOUL") and a letterspaced subtitle ("Obsidian field" / "Living
light" / "Soul signature") stacked beneath it. The three skins change
*material* only: obsidian (dark body, white fire), light (inverted —
white/pearl body, dark text, purple fire), soul (purple gradient body, gold
fire). They are toggles: the selected one holds the permanent accent ring; an
aria-live status line beneath the row speaks its message ("Black Ground —
Obsidian is the field: deep, calm, and built to make light visible.").
_Use:_ The page's front door — the three founding materials of the standard;
used as selectable foundation/theme specimens; clicking swaps selection and
announces the message via the status line.
_Source:_ Naya_Design_Element_Set_N4.html · _button-as-theme skins_

**BTN-014 — Mini button.** Compact ghost button (32px, 11px) used in card
action rows. _Use:_ Secondary actions inside intel rows (Open, Evidence).
_Source:_ Naya_Smart_Hub_Design.html

**BTN-015 — Orb button.** A base orb (120px scale, demonstrated in gold)
that is a real `<button>`: cursor pointer, borderless, inherits font. Presses
like something real — `:active` scales to 0.9 in 0.1s. `focus-visible` shows
a 2px white outline offset 8px. Carries `aria-label` ("Activate orb").
_Use:_ A pressable jewel — activation controls, "power on" moments, tactile
CTA jewels; use when the tap target should feel like a physical object rather
than a flat button. Not a `.naya-btn` — a jewel that presses.
_Source:_ Naya_Jewel_Library_-_N5.html · _tactile CTA jewel_

**BTN-016 — Portal split button.** Gold-toned (`--tone:#e7c65a`) dark pill
labeled "View proof" with a glowing checkmark orb fused to its right end (the
`split-orb`). Captioned "Portal variant". _Use:_ Actions that pass through a
portal — where the button's job is to take you somewhere verified (proof, a
portal destination). Documented variant candidate (`.naya-btn.split`); not
adopted.
_Source:_ Naya_Building_Blocks_Naya_2.html · _variant candidate_

**BTN-017 — Powercast button.** Pill button (48px tall) — black gradient with
a luminous white edge at rest, white uppercase-ish bold label; hover ignites
purple (border + glow), lifts 2px; active presses down. _Use:_ The Powercast
action in the topbar.
_Source:_ Naya_Smart_Hub_Design.html

**BTN-018 — Prism CTA.** Two hero CTAs on dark: "Experience the components"
(blue tone, with a `btn-orb` spark orb at its left) and "Use the system"
(`prism` class, `prism-mark` code icon at its left). True-black bodies,
hairline edge light. _Use:_ Hero/front-door calls to action — the two moves
a visitor can make (experience the system, use the system). Documented
variant candidate (`.naya-btn.prism`); not adopted.
_Source:_ Naya_Building_Blocks_Naya_2.html · _variant candidate_

**BTN-019 — Rooms plus.** 48px rounded-square (14px radius) purple jewel
button with a white plus and a violet halo; appears only on mobile in the
topbar. _Use:_ Opening the rooms drawer on mobile.
_Source:_ Naya_Smart_Hub_Design.html · _mobile add_

**BTN-020 — Share FAB.** Fixed bottom-right gold jewel square (56px, 18px
radius) with a white share glyph, glowing gold halo; mobile only; press
shrinks it. _Use:_ One-tap share on mobile.
_Source:_ Naya_Smart_Hub_Design.html

**BTN-021 — Swatch buttons.** Four 52px rounded squares (16px radius), each a
single flat spectrum color with a jeweled radial sheen on its face and a glow
in its own color. On hover they lift and grow slightly. Clicking one re-tints
the demo board (JS sets `--c`). _Use:_ Color picking in a live demo — "the
spectrum law, live." Each swatch is labeled (Purple — Naya herself; Blue —
calm truth; Green — living growth; Gold — earned wisdom).
_Source:_ Naya_Design_Elements_N2.html · _color picker_

**BTN-022 — Themed join button.** Same black heart, white rim, breathing glow
and shimmer sweep as the canonical DNA, but its hover ignition uses its own
section/theme color (`--sc`) instead of chrome purple. Shown as "＋ Join the
space" (blue ignition) and "✓ Joined" (green ignition — the joined/active
state). _Use:_ Contextual membership/join actions inside themed things
(spaces, sections) where the button should ignite in the thing's own color,
not chrome purple.
_Source:_ Naya_Design_Standard_Showcase__1.html

## Icons — one jewel icon family

One jewel icon family (SVG, never emoji). The icon stays white; the meaning
supplies the spectrum color.

**ICO-003 — Jewel icon renderer.** Programmatic SVG orb: blurred halo + core
orb with radial depth (white → currentColor → deep night), crisp white rim,
rotated specular highlight, and a white semantic glyph floating on top. ~49
glyph names (feed, spark, note, report, library, connect, ledger, nodes,
lists, mail, tabs, spaces, gear, core, mcp, api, github, webhook, sdk, a2a,
browser, db, mic, cal, shield, tunnel, search, plus, plusBold, doors, orbit,
home, bolt, users, brief, doc, cap, trophy, gauge, star, heart, key, check,
alert, lock, arrow, clock, menu). _Use:_ The single icon family for the whole
hub — "one jewel icon family (SVG, never emoji)"; ~30 glyphs beyond the 21
universal actions.
_Source:_ Naya_Smart_Hub_Design.html

## Cards — one card, one job

One idea per card. A card that tries to hold two ideas holds none.

**CRD-007 — Color job cards.** A dark rounded card holding a wide glowing
color swatch (44px tall bar, white rim, inset sheen) above a tracked-caps
name ("OBSIDIAN", "WHITE", "PURPLE") and a 14px role description. On hover
it lifts and the card's rim and glow take on the swatch's own color. _Use:_
Documenting a color's job in the system (field/light/soul) — each card is a
specimen of one color doing its one job.
_Source:_ Naya_Design_Standard_Showcase__1.html

**CRD-008 — Contrast cards.** Two small dark specimen cards. The "good" card
shows a like button with a black body, white heart icon, and red accent,
labeled "Black body · white icon · red accent" — "The action stays readable
before and after it wakes." The "bad" card shows a red icon on a red surface
("Red icon · red surface · lost meaning") — "Same-hue foreground and
background flattens the control and fails Law 13." _Use:_ Teaching the
contrast law by example — the fastest way to show what "separate body, voice
and soul" means; do/don't teaching specimens.
_Source:_ Naya_Building_Blocks_Naya_2.html

**CRD-009 — Domain card.** Small card (13px radius, min 120px tall): bold
14px name + 12px muted description; auto-fills 210px columns. _Use:_ Library
domain tiles.
_Source:_ Naya_Smart_Hub_Design.html

**CRD-010 — Door card.** Card (17px radius) with an accent-colored radial
wash at the top-right: row with 48px icon + name + "for" line, a flexible
description, and a footer holding either a status pill + "IN USE" honesty
badge (live doors) or a ghost "Contract" button (upcoming doors). Hover lifts
4px and intensifies the colored halo. _Use:_ The Connect room's destination
cards — one per ecosystem door.
_Source:_ Naya_Smart_Hub_Design.html

**CRD-011 — Drift cards.** Three dark cards, each with a dark red-glowing
warning icon (rounded square, ✕/✖/× in pale red) and two lines: a white "They
read *…*" line (e.g. *"white light at rest"*) and a muted "…and shipped
hairline borders." line. Below the grid, a centered serif verdict in
gold-accented white: "If a page violates any **SHALL**, it does not ship."
with a letterspaced sub-line "That is the whole contract." _Use:_ Drift
documentation — three times a principle was read and three times it drifted,
so every principle on the page is a checkable predicate; the anti-pattern
gallery that justifies the machine-law approach.
_Source:_ Naya_Design_Element_Set_N4.html

**CRD-012 — Identity card.** Centered card (max 560px, 26px radius, purple
edge + glow): identity emblem jewel, 30px title, muted lede, an alias preview
row (34px spectrum avatar + name/handle), a small-caps privacy statement over
a hairline, and a centered CTA button row (tall 50px buttons). _Use:_ The
identity bridge view (login/alias claim).
_Source:_ Naya_Smart_Hub_Design.html

**CRD-013 — Intel row card.** Compact card (13px radius): small-caps accent
type label, 16px bold title, 13px muted summary, a row of small pill metadata
chips, and a mini-button action row (Open / Evidence). Hover tints the border
accent. _Use:_ Standard list item for intelligence across rooms; built by
`intelCard()` in js/rooms/shared.js.
_Source:_ Naya_Smart_Hub_Design.html

**CRD-014 — Rail info card.** Small quiet panel in the rail — 13px radius,
faint border, small-caps muted heading, 13px body text. _Use:_ Secondary info
(tips, context) inside the sidebar.
_Source:_ Naya_Smart_Hub_Design.html

**CRD-015 — Reflection quote.** Full-height panel with accent-tinted
gradient and glow: 18px quote text + small muted attribution. _Use:_ A
reflective/evidenced quote moment (reports).
_Source:_ Naya_Smart_Hub_Design.html

**CRD-016 — Report card.** Dark card (18px radius) with a visible 1.5px white
border at rest and a slowly "breathing" white edge glow (6s loop —
`edgebreathe`). On hover: the border ignites in the card's own accent color,
a matching glow blooms, and the card lifts 3px. Header row pairs a jewel
bullet with an 18px bold title; body text is white 17px. Each card carries its
own `--accent`/`--accent-soft` spectrum color; laid out in an auto-fit grid.
_Use:_ Law/rule statements, principle statements — any self-contained content
unit that must show "white edge at rest, own color on touch."
_Source:_ Naya_Design_Elements_N2.html

**CRD-017 — Space card.** Card (17px radius, min 180px) with an accent
radial wash at the top-right: 18px title, muted description, deep shadow;
auto-fills 240px columns. _Use:_ Space tiles in the spaces room.
_Source:_ Naya_Smart_Hub_Design.html

**CRD-018 — Spectrum chips.** Ten equal-width chips in a row, each a rounded
14px panel with a vertical gradient from its spectrum color into black at the
bottom, a glowing colored rim, and inner white text-shadow. Each carries a
tracked color NAME on top and a one-line meaning under it ("PURPLE /
Choosing intelligence", "INDIGO / Calm authority", "BLUE / Knowledge moving",
"TEAL / Clear passage", "GREEN / Alive and well", "LIME / New growth",
"YELLOW / Attention, earned", "ORANGE / People and warmth", "RED / Act now,
rarely", "MAGENTA / The living edge"). _Use:_ Assigning each spectrum color
a job and a meaning — the identity palette at a glance.
_Source:_ Naya_Lego_Blocks_N4.html · _per-color meaning cards_

**CRD-019 — Tongue cards.** Three dark cards, each themed to one "tongue" of
the contract: MACHINE LAW · NORMATIVE (purple, checkable predicates), AI LAW
· PROCEDURE (blue, build/prove phases with jewel-bullet steps), HUMAN LAW ·
PHILOSOPHY (green, warm sentences). Lit at rest with a theme-colored glow;
hover lifts and intensifies in its own color. The machine card lists
monospace predicates (`lighting.idle.border_min_px ≥ 1.5`); the AI card has
phase eyebrows ("I · BUILD", "II · PROVE"); the human card is plain
sentences. _Use:_ One contract, three tongues — same truth in three
languages: normative predicates a machine can check, procedures a builder
follows in order, philosophy a human feels. On conflict, the machine wins.
_Source:_ Naya_Design_Element_Set_N4.html · _three-tongue contract_

## Board patterns — the board, assembled

Every board is identity + body + footer. Parts snap in; the law holds.

**BRD-009 — App dashboard board.** A dark board inside the app shell headlined
"Your day, already understood." with the lede "What matters, what changed
and the clearest next action." Three metric rows follow, each with a small
glowing `metric-mark` jewel, a white bold label, and a silver explanation:
"What matters — Priority is explicit.", "What changed — Context stays
visible.", "What happens next — Direction is clear." _Use:_ The Today-room
briefing pattern — a day's understanding organized into priority, change, and
next action.
_Source:_ Naya_Building_Blocks_Naya_2.html

**BRD-010 — Block top identity.** Row: jewel + large title (24–38px, tight) +
small-caps meta line, with the truth badge on the opposite end. _Use:_ The
board's identity strip (title + provenance meta).
_Source:_ Naya_Smart_Hub_Design.html · _Intelligent Block sub-part_

**BRD-011 — Board builder.** Smaller intelligent object (17px radius, 22px
padding): header row with 40px icon, bold title + muted subtitle, then a body
slot; inherits the room accent; hover lifts 3px and deepens the colored halo.
Built by the `Board()` JS constructor which also queues social-action
enhancement. _Use:_ Room-level boards (vs the feed's larger `.intel-board`).
_Source:_ Naya_Smart_Hub_Design.html · _JS builder API_

**BRD-012 — Board header.** Row at the top of the board: 64px circular
metallic jewel (coin/medal finish), small-caps tone-colored kind label, muted
ID text, and a truth chip pinned to the right. _Use:_ Identifying the board
— what kind of intelligence this is.
_Source:_ Naya_Smart_Hub_Design.html · _Intelligent Block sub-part_

**BRD-013 — Demo board.** A large rounded (22px) dark board whose entire
light scheme — border tint, glow, and the colored name text — is driven by one
CSS custom property `--c`. A 1px light "beam" runs across the top edge. When
a swatch is clicked, every light on the board re-fires in the new color (the
demo-name text glows in it too). Contains inline `code` chips. _Use:_ Live
law demonstrations — the specimen that proves "one property drives every
light; set it, and the board obeys." Pattern for any re-tintable surface.
_Source:_ Naya_Design_Elements_N2.html · _one-property re-tinting pattern_

**BRD-014 — Digest banner.** Slim banner row (16px radius, faint white wash):
small-caps kicker + right-aligned stats with big 22px glowing numbers.
_Use:_ "Orient at a glance" digest summary atop the activity feed.
_Source:_ Naya_Smart_Hub_Design.html

**BRD-015 — Intel board.** Large rounded panel (26px radius, 32px padding):
glowing vertical tone bar on the left edge, radial tone wash at the top, deep
drop shadow + colored halo. Board tone cycles the canonical spectrum (purple
→ sapphire → emerald → …) down the feed; hover lifts it 3px. Each tone
recolors border, halo and the left edge-light. _Use:_ The Smart Feed's core
unit — one intelligent block per note.
_Source:_ Naya_Smart_Hub_Design.html · _Intelligent Block implementation_

**BRD-016 — Lane board.** Auto-fit columns of dark lanes (min 200px tall,
small-caps header + muted count): each holds `.list-card` items (12.5px bold
title) with a "WHY ·" prefixed muted rationale line in accent. _Use:_
Kanban-style lanes (lists room) where every item carries its reason.
_Source:_ Naya_Smart_Hub_Design.html

**BRD-017 — Nutshell moment.** Treated as a *moment*, not a label: 18px/1.7
summary text with a 3px tone-colored left border and a tone-tinted gradient
wash behind it, headed by a small-caps tone label ("IN A NUTSHELL"). _Use:_
The one-paragraph essence of an intelligent block.
_Source:_ Naya_Smart_Hub_Design.html · _Intelligent Block sub-part_

**BRD-018 — Ship-gate panel.** A dark sunken panel containing: a track with a
spectrum-gradient fill bar (magenta→purple→blue→green→gold) that widens as
checks clear, a glossy shine over the bar, and a status line ("◈ GATE CLOSED
· 0/6 checks cleared" — flipping to green-glowing "✓ CLEARED FOR LAUNCH"
with a pulsing glow when all six clear). Below it, six check rows: numbered
stage markers in spectrum colors with custom square checkboxes that fill green
with a white ✓ when ticked; a completed row's number turns green and its text
strikes through. _Use:_ The ship gate — "all six, or it doesn't ship"; a
launch-sequence checklist with visible progress.
_Source:_ Naya_Epic_Elements_-_Lego_pieces_N5.html · _extends `.gate-bar`_

## Navigation — the way in, the way back

Navigation tells you where you are, not only where you can go.

**NAV-002 — Bottom ecosystem bar.** Fixed bottom bar (fades in from
transparent over the content, blurred) holding a row of 46px black-glass
circular icon buttons; hovering one lifts it and shows a small uppercase
label tooltip above, the icon glowing in the destination's color. _Use:_
Always-visible quick access to all ecosystem destinations.
_Source:_ Naya_Smart_Hub_Design.html

**NAV-003 — Brand lockup.** 44px circular logo image with a soft purple halo,
next to a bold uppercase wordmark (15px, wide letter-spacing) with a smaller
muted tagline beneath it. _Use:_ Top of the left rail — product identity.
_Source:_ Naya_Smart_Hub_Design.html

**NAV-004 — Ecosystem quick menu.** Same black-circle plus button as the
rail toggle; on open it expands into a 300–340px floating panel (blurred
dark, purple-edged) with a small-caps header and rows of destination links —
each row has a colored icon tile, label, and optional external-link marker;
hover lights the row and icon in the destination's own color. _Use:_
Top-right quick-jump menu to every NayaNET destination.
_Source:_ Naya_Smart_Hub_Design.html

**NAV-005 — Hero page nav.** Dark pill nav bar with a small glowing purple
orb logo on the left and small text links (Foundations, Buttons, Boards,
Actions, Icons, Tabs+Login, App shell, Blocks, 100 laws). Mobile collapses
links into a 4-column grid of bordered chips with 44px touch targets. _Use:_
In-page orientation for long design-system documents.
_Source:_ Naya_Ultimate_Design_System_Naya_2.html

**NAV-006 — Pill nav buttons.** Dark near-black pill buttons (999px radius)
with a white 1.5px border at rest, white text, and a small colored glyph
(colored via `--c`) on the left. On hover: the border ignites in the pill's
own spectrum color, a matching colored glow blooms, and the pill lifts 2px.
Six shown, each with its own color (purple, blue, green, gold, orange,
magenta). _Use:_ Chrome navigation — section anchors / layer jumps in
report-style pages. Each pill "burns its own spectrum color, never anyone
else's."
_Source:_ Naya_Design_Elements_N2.html

**NAV-007 — Sidebar nav button.** Full-width row: 40px rounded-square icon
tile tinted in the room's own color + text label. At rest it's quiet
(transparent bg, dim text); hover gives it white light, a 3px nudge right,
and the icon tile ignites in the room color with a glow; active is subtle —
white edge + a 3px vertical color bar at the left edge, NO permanent glow.
_Use:_ Room navigation in the left rail (each room wears its own `--nav`
color).
_Source:_ Naya_Smart_Hub_Design.html

**NAV-008 — Topbar.** Sticky blurred bar across the top; small caps title
left, right side has a green pulsing LED dot + muted status text. _Use:_
Persistent app topbar with liveness indicator.
_Source:_ Naya_Smart_Hub_Design.html

## Tab patterns — switch the lens, never the page

Tabs switch the lens, never the page. Color belongs to hover; active stays
quiet.

**TAB-002 — Lens tabs.** Three equal-width buttons in one row (12px radius,
white edge at rest). Hover ignites each in its own signature color —
collective purple, personal blue, activity green. Active is a subtle white
indicator only (color reserved for hover). _Use:_ Switching the feed lens:
collective / personal / activity.
_Source:_ Naya_Smart_Hub_Design.html

**TAB-003 — Period strip.** Wrapping row of small period buttons (min 78px
wide). _Use:_ Selecting a report period (day/week/month/year).
_Source:_ Naya_Smart_Hub_Design.html

**TAB-004 — Segmented control.** A dark rounded track holding three short
text segments — "Human" (active), "Naya", "Machine" — one visibly lit and
elevated, the others quiet. Captioned "Smart lens". _Use:_ Switching
perspective/lens over the same content — who the view is for — without
changing the page.
_Source:_ Naya_Building_Blocks_Naya_2.html · _lens/view switcher_

## Badges & status — the smallest truth on the page

The smallest truth on the page. A status you can't read at a glance is
decoration.

**BDG-004 — Action count badge.** Small round count chip (22px) inside an
action button — white-on-glass at rest, brighter when the action is on.
_Use:_ Showing how many times an action was taken.
_Source:_ Naya_Smart_Hub_Design.html

**BDG-005 — Layer state label.** Small quiet gray text label pinned to the
right side of a layer header. _Use:_ Declaring the layer's state (e.g.
open/closed status text).
_Source:_ Naya_Smart_Hub_Design.html

**BDG-006 — Rating number.** 13px bold gold number next to a rating control.
_Use:_ Showing the numeric rating beside stars.
_Source:_ Naya_Smart_Hub_Design.html

**BDG-007 — Room status line.** Small inline row: 8px glowing accent LED dot
+ 12px muted status text. _Use:_ A room's live status line (e.g. in a room
toolbar).
_Source:_ Naya_Smart_Hub_Design.html

**BDG-008 — Status pill.** Small pill (11px bold small-caps) with a 7px dot:
live = green with pulsing glowing dot; ready = blue; soon = white/gold;
contract = lavender; spec = muted gray. _Use:_ Object status (doors,
contracts, specs).
_Source:_ Naya_Smart_Hub_Design.html

**BDG-009 — Trinity pills.** Three pill-shaped badges in a centered row,
black hearts with 1.5px rims, 14px tracked-caps labels: "BLACK GROUND"
(white text, gray rim), "WHITE LIGHT" (white text, white rim), "PURPLE SOUL"
(purple text, purple rim). _Use:_ Stating the brand's three color doctrines
as a mantra strip under a page header.
_Source:_ Naya_Design_Standard_Showcase__1.html

## Typography — the voice leads, never shouts

Headers get the voice; everything else stays in the UI sans. Hierarchy from
size, never from gray or colored text.

**TYP-001 — Design-note subtitle.** 13px muted text with slight
letter-spacing, small top margin. _Use:_ Subtitles under block titles
(design-spec annotations).
_Source:_ Naya_Smart_Hub_Design.html

**TYP-002 — Kicker.** A tiny (14px) ultra-letterspaced (.28em) uppercase
label in a theme color (`--kc`, default purple), sitting above headlines —
e.g. "Nayanet · The Design Standard · Button Library Official · v2.0" over
the front door, "Intelligent block · Specimen" on the board, "Pre-ship
checklist · all must pass" in the gate. _Use:_ The eyebrow that names what
the thing below *is* — section identity, provenance, or specimen tag; sets
context before the headline speaks.
_Source:_ Naya_Design_Element_Set_N4.html

**TYP-003 — Phase label.** A small 14px tracked-caps label in dimmed white
("I · BUILD", "II · PROVE", "I · SEE") used as a phase divider inside panels
and checklists. _Use:_ Marking the phases of a procedure or checklist (build
then prove; see then prove) inside a panel.
_Source:_ Naya_Design_Standard_Showcase__1.html

**TYP-004 — Section header.** A section unit: a small tracked section number
line ("01 · Color") with a 34px glowing rule bar before it; a large 24px
white serif law statement ("Color has four jobs. Never cross them.") with a
soft black text-shadow; and an 18px white deck paragraph explaining it. All
left-aligned. _Use:_ Opening every section of a standard page — number names
the section, the law names the principle, the deck explains it.
_Source:_ Naya_Lego_Blocks_N4.html

**TYP-005 — Type specimens.** Three dark cards with color-tinted borders,
each demonstrating one rung of the type scale: "HEADLINE · 24PX" with a serif
voice sample line ("Your intelligence, collected."), "BODY · 18PX" with a
two-line sample, "DETAIL · 14PX" with an evidence sample ("Evidence lives
here: PR #1858 · tip 78661f59 · 40/40 tests."). Each has a muted 14px caption
explaining the rung ("Serif voice. Light-carved. It leads, never shouts.").
_Use:_ The type contract made visible: 24 headlines, 18 body (most text lives
here), 14 details/evidence — the floor, nothing readable smaller; hierarchy
from size, never from gray or colored text (text is white 99%).
_Source:_ Naya_Design_Element_Set_N4.html

**TYP-006 — Voice headline.** A 24px serif display face (Cormorant Garamond,
Georgia fallback) in white with a soft black text-shadow for legibility on
obsidian — the "voice" that speaks over the UI sans. `h1.voice` centers on
the front door ("One standard. Every page. *No drift.*" with italic
emphasis); `h2.law` opens every section ("The living button. One DNA, every
app."). Headers get the voice; everything else stays in the UI sans. _Use:_
Display headlines — the serif voice leads, never shouts; section titles, page
titles, verdicts, footer sign-offs.
_Source:_ Naya_Design_Element_Set_N4.html

## Layouts — doors, rooms, and stages

A layout is a promise about what matters. The entrance comes first; the
content earns it.

**LAY-001 — Activity hero.** Centered blurred banner (24px radius, white
edge): a breathing radial pulse ring behind, small-caps kicker with a live
green pulsing dot, big 36–56px title, 16px muted subtitle. _Use:_ The
activity room's top-of-page moment.
_Source:_ Naya_Smart_Hub_Design.html

**LAY-002 — Ambient aliveness layer.** Three huge blurred (100px)
translucent color blobs — purple top-left, magenta mid-right, blue
bottom-center — fixed behind all content at 15% opacity, drifting slowly on
18–26s alternate loops (translate + slight scale). Pure atmosphere;
pointer-events none, aria-hidden. _Use:_ Page-wide ambient aliveness — the
"black is the night" background that breathes; slow, calm, never shouting.
_Source:_ Naya_Design_Elements_N2.html

**LAY-003 — Demo stage.** A large dark rounded (20px) panel with a 1.5px
white rim, a subtle diagonal gradient (lifted top-left, deeper bottom), a
soft inner top highlight and deep contact shadow — the elevated "stage" every
specimen set sits on. Generous 32px padding (20px on mobile). All 11
sections' specimens live inside one. _Use:_ The specimen stage — every demo,
board, grid, and recipe renders on it; it separates the teaching chrome
(section number, law headline, deck) from the living specimens.
_Source:_ Naya_Design_Element_Set_N4.html

**LAY-004 — Front-door header.** A centered page entrance: the glowing
circular logo (110px, 88px on small screens), a letterspaced kicker ("Nayanet
· The Design Standard · Button Library Official · v2.0"), a serif voice
headline ("One standard. Every page. *No drift.*"), an 18px invitation
paragraph in white, then the three foundation buttons in a row, then the
aria-live status line and a small explainer note. Generous vertical padding
(84px top). _Use:_ The page's front door — identity, promise, and invitation
before any content; "Make the header a front door" is itself one of the
AI-law steps.
_Source:_ Naya_Design_Element_Set_N4.html

**LAY-005 — Hub footer.** Centered page footer: mission headline (21px
white), 16px mission paragraph (max 640px), then a wrap of small-caps muted
links each preceded by an 8px purple glowing dot. _Use:_ Mission statement +
footer links at the bottom of every room.
_Source:_ Naya_Smart_Hub_Design.html

**LAY-006 — Mail layout.** Two-pane mail: left column of `.signal` preview
cards (12.5px bold subject + muted snippet; selected gets accent border +
tint), right pane a `.message-reader` (14px/1.7 body) with a `.context-box`
panel below for related context. _Use:_ The mail room's reading experience.
_Source:_ Naya_Smart_Hub_Design.html

**LAY-007 — Main show hero.** Top-of-feed hero: small-caps colored eyebrow
label, large fluid headline (clamp 30–52px), 17px muted sub-paragraph (max
760px). _Use:_ The Smart Feed's main-show heading area.
_Source:_ Naya_Smart_Hub_Design.html

**LAY-008 — Orbiting login.** A small dark login card floating between two
thin concentric orbit rings. Inside: a glowing circular login-mark, "Welcome
back.", "Enter through one secure door.", a recessed email field showing
"you@example.com" with a mail icon, a small purple "Continue securely" button
with an arrow icon, and a note: "Presentation specimen · no credentials are
collected". _Use:_ The front door — entry that feels alive: orbital motion as
a quiet sign of living intelligence behind one secure door.
_Source:_ Naya_Building_Blocks_Naya_2.html · _auth entry_

**LAY-009 — Report header lockup.** A flex lockup: 58px logo image at left,
title block center, living orb mark at right. Generous padding (38px top),
arranged as "a front door, not a nameplate." _Use:_ Page front doors — the
composed header of report-style pages: logo, title, living mark as one
lockup.
_Source:_ Naya_Design_Elements_N2.html

**LAY-010 — Report section.** Simple stacked section: 13px spaced heading,
13px muted body, hairline divider below (last one clean). _Use:_ Body
sections of a report.
_Source:_ Naya_Smart_Hub_Design.html

**LAY-011 — Room head.** Non-feed room header: small-caps accent kicker, 27px
title, 15.5px muted description (max 760px). _Use:_ Standard header for every
non-feed room.
_Source:_ Naya_Smart_Hub_Design.html

**LAY-012 — Smart app shell.** A full app-frame specimen: left rail with an
"intelligence" header (Your intelligence · Connected and ready), a sphere,
and five room buttons (Today, Reports, Smart Spaces, Smart Mail, Smart
Ledger) each with a diamond nav-jewel that ignites when selected; main area
with a top row (room title in serif + truth-pill status with green dot), an
app-board content panel, and three metric cards with metric-marks. _Use:_
Demonstrating "one intelligence, many rooms" — persistent orientation while
content changes; room buttons swap title/head/copy via JS.
_Source:_ Naya_Ultimate_Design_System_Naya_2.html · _full product frame_

**LAY-013 — Story grid.** Two-column grid (wide + narrow): the main column
holds a `.highlight` panel — radial accent wash, small-caps accent eyebrow,
21px headline, 13.5px body; the narrow column stacks smaller cards. _Use:_
Featured story + supporting items (reports/today).
_Source:_ Naya_Smart_Hub_Design.html

**LAY-014 — Welcome portal.** Full-viewport centered invitation: a portal
jewel (118px rounded-square with the full conic spectrum + breathing
animation), a sheen-sweeping gradient headline (clamp 38–76px), muted lede, a
centered row of CTA buttons, tiny foot note. The precision variant adds a
360px stage with a 108-jewel orbit ring (78s rotation) plus one
counter-rotating white "unity light". _Use:_ First-run welcome / entrance
experience.
_Source:_ Naya_Smart_Hub_Design.html

## Lists — order you can check

A list is an order you can check. Physics provides consistency; every element
moves the same way.

**LST-003 — Activity row.** Simple event row: 11px glowing purple dot + bold
white title + 15px muted body, hairline divider below. _Use:_ Compact
activity entries (the older row style, vs the card law).
_Source:_ Naya_Smart_Hub_Design.html

**LST-004 — Activity time group.** Time-bucketed list: 12px small-caps muted
group heading over a hairline, then activity rows. _Use:_ Grouping activity
events by time.
_Source:_ Naya_Smart_Hub_Design.html

**LST-005 — Interaction physics.** A dark list of five motion rules, each a
bold label + small silver value: "Approach — 170px · light only", "Hover —
−3px · .22s signature ease", "Press — +1px · immediate", "Focus — 2px white
ring · 4px offset", "Reduced — No orbit or float animation". _Use:_ The
reproduction kit — physics provides consistency; every element moves the
same way.
_Source:_ Naya_Building_Blocks_Naya_2.html · _motion doctrine specimen_

**LST-006 — Law steps.** A vertical stack of procedure rows: mini jewel
marker on the left, then a bold 17px title line with a smaller explanatory
line beneath. Rows sit on a faint white wash with a hairline border. Shown
nested inside cards. _Use:_ Ordered build procedures / law enumerations —
"ten steps, in order; no skipping."
_Source:_ Naya_Design_Elements_N2.html

**LST-007 — Timeline.** Vertical timeline: a 1px gradient spine with 9px
glowing accent dots, each event a small dark card (13px radius); below an
event, a wrapping row of tiny 9.5px stage chips. _Use:_ Chronological event
streams and their stage markers.
_Source:_ Naya_Smart_Hub_Design.html

## Calendar — five blocks, one law order

_Family score: 9.0/10 (independent review, 2026-10-16). Identified fixes pending — see GAP-BUILD-NOTES.md._

Family contract, one line each: one meaning per color across all five blocks (magenta = celebrations, purple = deep work, blue = meetings, green = health, gold = decisions/deadlines; a sixth type takes orange, a seventh red — the wheel continues, never restarts); today is white-hot chrome and outranks selection, always; nothing invents events — uncertainty is styled, never hidden; named as not-yet: week-view grid, drag-to-reschedule, recurring-event editor (future CAL-006+).

**CAL-001 — Month-view board.** A full month on black ground: serif weekday headers, 104px day cells with white-lit edges, today ignited in white-hot chrome with a slow 4s breathe, event pills walking the wheel in law order (adjacent pills never duplicate a color). In-month cells lift and ignite on hover; out-of-month cells sit dimmed and jump to their month when clicked. Overflow shows two pills, then jewel dots in wheel order, then an honest `+N more` chip that opens the day's agenda (CAL-004) — it never pretends the cell showed everything. States: rest (black cell, serif number, pills dark with tinted borders) · hover (2px lift, chrome-purple ignition; pills ignite their own event color) · selected (held purple edge + glow, one at a time — clicking moves it, never stacks it) · today (2px white-hot chrome edge + white glow; a selected day that is not today wears purple) · out-of-month (dimmed, no ignition, still jumps to its month — dimmed is not dead) · overflow (+N more is the real count of hidden events). Do: walk the wheel down each cell — magenta → purple → blue → green → gold, adjacent pills always in law order. Don't: paint event types by mood of the day; a color's meaning is fixed across the whole family or the wheel becomes decoration. Anatomy: board chrome (5-layer shadow, 24px radius, tone under-glow) · serif month title with letterspaced year kicker · drawn CSS chevrons on 44px targets with chrome-purple ignition · serif uppercase weekday row · the day cell (number + pills + dots + more-chip, in that order) · the event pill (diamond jewel + time + title — the bullet law at calendar scale). It never invents events for empty cells, and today comes from the viewer's clock or an explicit `data-today` — never a guess. _Use:_ The month grid of a scheduling surface — month-level browsing with day selection feeding an agenda (CAL-004).
_Source:_ gap-blocks/calendar-blocks.md

**CAL-002 — Event card.** One event, fully dressed: an 86px time rail (serif time + uppercase duration), a glowing 3px spine in the event's fixed type color, a letterspaced type tag, serif title, and a location/attendees row with drawn SVG glyphs (pin, people — never emoji). All-day events collapse the rail into a glowing color band with an "ALL DAY" flag; multi-day spans carry the range in the rail ("Oct 20 → 22"); tentative events get a dashed edge, a `~` after the time, and say so in plain words. States: rest (dark card, color only on spine, tag, and glyph strokes — never a flood) · hover (lifts 6px, edge + glow ignite in the event's own color — the card is themed, so it burns its own hue) · active/press (settles back 4px) · focus (2px white ring) · all-day (never shows a fake `00:00–23:59`) · multi-day span (the rail carries the range; in CAL-001 the same event renders one pill per day with `→` honesty markers) · tentative (dashed edge + tilde + plain-words note). Do: let the card ignite in the event's own spectrum color — purple for deep work, blue for meetings, gold for deadlines. Don't: rest the card in its color; a card that wears its hue at rest is a flood, and floods are forbidden. Anatomy: the time rail · the 3px glowing spine (the identity mark, shared with CAL-004's timeline) · the type tag in the event's fixed color · the serif title · the meta row of drawn glyphs · the tentative styling (the honesty layer). It renders the time it was given — no invented timezone, no silent conversion; the attendee count is the real count or the row is omitted. _Use:_ One event in full detail — agenda rows, search results, reminders.
_Source:_ gap-blocks/calendar-blocks.md

**CAL-003 — Date picker.** A compact picker for embedding in forms: an input-styled trigger showing the chosen date (or an honest "Choose a date" placeholder — never a fake pre-filled date), opening a dropdown mini month grid with keyboard-honest focus states; past dates are visibly dimmed and truly inert. States: trigger rest (black body, white edge, drawn calendar glyph) · trigger hover (2px lift, purple chrome ignition — it is chrome, it burns chrome's color) · dropdown open (elevated panel; `aria-expanded` tells the truth) · day hover (purple ignition) / day focus (white ring — arrow keys move, Enter chooses, Esc closes and returns focus to the trigger) · chosen (held purple edge + glow + bold number, one at a time) · today in the mini-grid (white-hot chrome edge + white number — the family rule at 36px scale) · past dates (32% opacity, strikethrough, `disabled`, out of tab order — dimmed AND inert, never the fake-disabled look that still clicks). Do: make past dates visibly dimmed and keyboard-unreachable — a disabled date that still takes focus is a lie with styling. Don't: pre-fill the trigger with "today" to look alive; an unchosen picker says "Choose a date" until a human chooses. Anatomy: the trigger (the form-facing face — reads as an input, behaves as a button) · the dropdown panel (weekday initials, 36px day buttons, serif month title) · the day button (hover ignition, chosen hold, today white-hot chrome, past inert) · the timezone footnote — "Calendar date only — no timezone is assumed or stored" — part of the block, not documentation. The value is a calendar date (`YYYY-MM-DD`), stored noon-neutral, displayed as-is — never converted, never a zone abbreviation it doesn't know. _Use:_ Date selection inside forms — booking flows, filters, schedulers.
_Source:_ gap-blocks/calendar-blocks.md

**CAL-004 — Agenda list.** The day's events as a vertical timeline: serif time gutter, a glowing 3px spectrum spine per event type, cards in CAL-002's language, and a white-hot chrome "now" line with a labeled flag — positioned from the clock, and only ever rendered when the viewed day *is* today. An empty day gets the empty state with dignity: a centered white-hot chrome jewel, "Nothing scheduled," "The day is yours" — no fake suggestions, no ghost events. States: rest (gutter times in serif, spines glowing quietly, cards dark with white-lit edges) · hover (the card lifts 4px and ignites in the event's own color — same language as CAL-002, one family) · now-line (white-hot chrome, labeled, clock-driven) · empty (jewel + two lines — emptiness is a state with dignity, not a hole to fill) · past events (spine dims to 40%, no hover lift — readable, not clickable-theater). Do: give every event one glowing spine in its fixed type color, in wheel order down the day — the timeline should read as a walked spectrum. Don't: render a now-line on any day that isn't today; a fake "now" on last Tuesday is a trust violation with styling. Anatomy: the time gutter (serif times, right-aligned — the rail the day hangs on) · the spine (CAL-002's identity mark at timeline scale) · the node jewel (the rotated diamond where gutter meets spine) · the compressed event card (tag, serif title, one meta line — one idea per card) · the now-line (the honest present) · the empty state. The event count is the real count; past events never pretend to be upcoming. _Use:_ Day-level schedule views — the day selected in CAL-001 rendered in full.
_Source:_ gap-blocks/calendar-blocks.md

**CAL-005 — Day-cell state system.** The seven honest states of a calendar day, specified once so CAL-001 and CAL-003 never drift: rest, hover, selected, today, has-events, disabled, out-of-month — each a composable class (`.s-hover`, `.s-selected`, `.s-today`, `.s-events`, `.s-disabled`, `.s-out`), with a written precedence order: today > selected > hover > has-events > rest; disabled and out-of-month modify the base independently. A state is visual truth: if it looks clickable it is clickable; if it looks dead it is dead — disabled is removed from keyboard reach and ignores clicks. States: rest (the baseline — black, white-lit, serif number; all other states are deltas from this) · hover (lift + chrome-purple ignition) · selected (the hover ignition *held* — edge, glow, lift persist; never on two days at once) · today (white-hot chrome 2px edge, white glow, 4s breathe — if today is also selected, chrome wins: today outranks selection, always) · has-events (jewel dots in wheel order — information, not decoration; their colors are the event types) · disabled (32% opacity, struck number, inert) · out-of-month (34% opacity, no ignition — but still clickable, jumping the board to its month; dimmed is not dead). Do: freeze today above selection in the precedence order — today is the fact, selection is the choice. Don't: invent an eighth state for "weekend" or "holiday" tinting; tinting days by category is a flood by another name — holidays are events, and events already have colors. Anatomy: the cell (one class per state — states compose by class, never by inline-style improvisation) · the precedence order (written down so two builders never disagree) · the state label on every specimen (teaching statically) · reduced motion (the today-breathe stops, transitions drop — motion is earned by meaning; the meaning survives without it). Today is computed, never guessed — a frozen specimen says it's a specimen. _Use:_ The state contract for any builder implementing CAL-001 or CAL-003 — implement the seven states once, never drift.
_Source:_ gap-blocks/calendar-blocks.md

## Checkout — the payment block family

_Family score: 8.8/10 (independent review, 2026-10-16). Identified fixes pending — see GAP-BUILD-NOTES.md._

Family contract, one line each: one total, one truth — PAY-001's total, PAY-002's button label, and PAY-003's hologram all render the same confirmed number; privacy is structural — card data lives in transient inputs bound for the processor, and the display layer never sees more than last-4 + brand; no fake success anywhere — confirmation ignites on a confirmed response only; every interactive thing is alive; plain words under pressure — validation and microcopy never blame the user. Named as not-yet: saved-address block, order tracking/shipment; the processing spinner is a transient Pay-button state (a spinner that outlives the attempt is a lie); 3-D Secure stays processor-owned.

**PAY-001 — Order summary board.** The board that says "here is what you're paying for" before any money moves: line items with tone-jewel thumbnails and real quantity steppers, one promo code row, and the three rows that matter — subtotal, estimated tax (*estimated* is the honesty), and the grand total — closed by one honest line so nobody feels tricked at the total: "Prices confirmed at checkout. The total is the total — no surprises on the next step." States: rest (black ground, white-lit 1.5px edges, corner jewel ◆ in choosing-purple; thumb jewels carry each item's own color, never twice in a row) · hover — board (lifts 5px, purple tone ignition), item (lifts 2px, ignites its own jewel color), grand total (the serif total ignites gold — the only place gold appears on the board, and only on touch) · active/press (steppers compress; the Apply button presses in like every `.naya-btn`) · focus (2px white ring on every stepper, input, and button) · disabled (Apply drops to 45% opacity — disabled never ignites) · empty (`.is-empty` — the quiet cart-empty panel with a live button; idle, not dead) · promo applied (emerald edge, set by a real backend response — never by the front end guessing) / promo invalid (red edge + a plain-words sentence, never blaming). Do: let the grand total be the one gold moment on the board — serif, earned, only on hover; the total is the final word of the page. Don't: show strike-through "original price" theater next to numbers you never charged; and if the backend can't confirm a price yet, say "Price loads at the next step" instead of showing a number. Anatomy: the corner jewel ◆ (the board's identity mark — purple, choosing intelligence) · the thumb jewels (rotated diamonds, identity not decoration — in a cart of five lookalike items, the jewel is how your eye finds the one you're editing) · the qty stepper (real buttons, `aria-live` output — when quantity hits 0 the item leaves the list; no phantom rows) · the promo row (one code, one button, one message line) · the totals (labels left, numbers right, tabular figures so columns stay honest). This board never shows a price the page can't prove — a missing price reads "Loading your total…", never a zero or a guess. Privacy: no card data touches this block — it totals, it never sees payment instruments. _Use:_ The "here's what you're paying for" step of checkout, plus honest cart-empty states.
_Source:_ gap-blocks/checkout-blocks.md

**PAY-002 — Payment form.** The four fields where money changes hands — name on card, card number, expiry, CVC — with floating labels, white-lit edges at rest, and purple chrome ignition on focus; validation speaks like a person, not a parser ("That number looks short" — never "Invalid input," never blame). The Pay button starts disabled and enables only when all four fields pass; it carries the real total, ≥52px, one per view. States: rest (dark fields, labels sitting inside like a placeholder — readable, nothing shouting) · focus (border ignites purple with a held glow; the label lifts, shrinks, and letterspaces into a kicker) · valid (emerald edge — alive and well, the reward for fast feedback) · invalid (red edge + red glow + one plain-words sentence underneath; red is urgency, not alarm — no shaking, no exclamation flood) · disabled (Pay at 45% opacity — it does not pulse, glow, or beg) · empty (all fields blank is the natural rest state, not an error). Do: validate inline, per field, the moment the user leaves it — fast feedback is kindness; a surprise error at the bottom of a submitted form is not. Don't: clear the whole form on a failed payment, or red-ring every field when one card number is the problem — mark the one field that's wrong, keep everything else, keep the user's typing. Anatomy: the floating labels (the field's purpose never disappears) · the card-number field (`inputmode="numeric"` for the right mobile keyboard, `cc-number` autocomplete, letter-spaced tabular figures — the pattern is a courtesy, not a contract) · the brand jewel (lights in the brand's own color from the leading digits — confirms the brand, never echoes digits) · the CVC field (`type="password"`, masked at rest, like it should be) · the one Pay button (label carries the real total from PAY-001 — never a hardcoded number the page can't prove) · the secure line — "Locked in transit. We never see your full card number — only the payment processor does" — a promise in plain words that must be *true* in the shipping build. Privacy: card data lives only in these input fields, bound for the payment backend on submit — the block never renders a card number back as text (not in a summary, not in an error message, not in a receipt preview), never logs card fields to console, analytics, or error reporters, and the display layer shows at most brand + last four, arriving from the backend already masked. A build that echoes a PAN violates the block. _Use:_ The card-details step of checkout — the one place card data is ever entered.
_Source:_ gap-blocks/checkout-blocks.md

**PAY-003 — Confirmation state.** The moment after money moves: the paid amount as a hologram number — layered Georgia light you look *into*, one ignition when the processor confirms success, then a soft 5s breathe — plus receipt rows (what / when in UTC / receipt status) and two truth states on the receipt email: green ✓ only when the backend confirms the email landed, gold ? while it's claimed and awaiting its stamp. States: rest (emerald-tone board, the hologram amount breathing on a slow loop — maximum life, minimum noise) · the one ignition (`.is-ignited` added by the confirmed success response — scale, light, settle, once; never by a timeout, a guess, or an optimistic render) · hover (the board lifts 5px and ignites emerald; receipt rows stay still — they're records, not controls) · receipt sent (emerald ✓ — the backend confirmed the email) / receipt pending (gold ? — the gold line never upgrades itself) · error-inside-confirmation (charge succeeded but the receipt email failed: "Charged ✓ — receipt email failed, retrying. Your money is safe." — red is reserved for the charge failing, not a delayed email). Do: make the paid amount the most beautiful number on the page — the moment the user trusted you with money, the number should feel *held*, not just displayed. Don't: confetti, coin bursts, or a "YOU DID IT!!!" modal — a payment confirmation is a receipt, not a birthday party; restraint is what makes the one ignition feel like something. Anatomy: the hologram amount (Georgia 56px, four layers of shadow — top light, grounding, glow, far glow; breathes, never blinks or dances) · the charged-to line (brand + last-4 only — the full number never appears here; the last-4 arrives from the backend's masked response, never truncated client-side from a PAN it shouldn't have) · the receipt rows (what / merchant of record stated plainly / when in UTC, so there's no timezone argument later — jewel bullets in law order carry the rows) · the receipt-sent line (a *claim* until the mailer says otherwise) · the actions ("Back to the Hub" primary, one per view; "Download receipt" quiet — serving the receipt the backend already generated, never fabricating one client-side). This block never claims the charge succeeded before the processor answers. Privacy: only brand + last-4 on the charged-to line — per the PAY-002 boundary. _Use:_ Post-payment confirmation — the held moment, the receipt, the honest email status.
_Source:_ gap-blocks/checkout-blocks.md

**PAY-004 — Error state.** The panel for when the payment doesn't go through: the headline and first line name the cause honestly — declined, processor didn't answer, or session timed out — and every variant opens with the load-bearing sentence: "No money moved." — rendered only when the backend confirms no charge was created, never on a guess. Three concrete next-steps in likelihood order, a real reference code for the bank call, and retry as the primary action. States: rest (red-tone board breathing on a slow 6s loop — urgency you can feel, not an alarm you flinch from; `role="alert"` announces it once) · hover (lifts 5px, red edge brightens; "Try again" wears chrome-purple — retry is *the* primary action) · active (retry presses in) · declined vs. failed vs. timed-out (the cause is always named honestly) · unknown charge state ("We're confirming with the processor whether anything was charged — nothing is final yet," offering "Check status" instead of "Try again" — guessing here is how double-charges happen) · retry-in-flight (button disables with a "Trying again…" label swap — no double-charges from double-clicks; retry is a new charge attempt and needs consent every time). Do: say "no money moved" before anything else — the user's first fear is the double-charge; kill it in the first sentence, then explain. Don't: headline the raw processor code ("Error 402: card_declined") or paste a stack trace near the user — and never imply the user did something wrong: no "you entered," no "your fault," no red ✕ stamped over their card. Anatomy: the red (an edge and a glow at ~45% border strength, breathing — no flashing, no red flood; a panel that screams at a declined card teaches users to fear the checkout) · "no money moved" (confirmed only) · the three next-steps (jewel bullets in law order, each a concrete action — "check the details" first because it's the most common cause and the cheapest fix; "ask your bank" names the amount, because the bank will ask) · the reference code (real, from the failed attempt, monospace — the one piece of machine truth the user can carry elsewhere) · retry as primary (one primary action per view — it re-submits the *same* validated form data, never clears the fields). Privacy: no card data re-rendered, no full numbers in any message; the retry re-submits transient fields, never a stored PAN. _Use:_ Failed-payment recovery — declined cards, processor failures, expired sessions.
_Source:_ gap-blocks/checkout-blocks.md

**PAY-005 — Payment method picker.** The "which card?" moment: saved methods as rows — a brand jewel in the brand's own color (Visa blue, Mastercard orange, Amex emerald), last-4, expiry, one marked default with a quiet gold chip — built as a real radiogroup where the rows *are* the controls, plus a dashed "Use a new card" row that hands off to PAY-002. Selecting a row is a choice, and choices ignite purple. States: rest (dark rows, white-lit 1.5px edges, brand jewels glowing in their brand colors; the default card wears the gold "Default" chip — gold is attention, earned, and the default card earned it) · hover (the row lifts 2px and ignites choosing-purple; the new-card row's dashed border goes solid and its → nudges 4px — a chevron promises "go somewhere") · selected (purple edge, purple wash, purple glow, and the ✓ check orb fades in at full scale — one at a time; the visual obeys the radiogroup) · focus (`:focus-within` white ring) · active (presses 1px — the row is a real control, it feels like one) · empty (no saved methods — no apology panel; the "Use a new card" row *is* the picker, pre-highlighted, heading to PAY-002). Do: mark exactly one default and let the user change it where the row lives — the chip is gold because the default is the card the user already trusted. Don't: show the expiry as a countdown ("expires in 4 months!!") or nudge the user toward any card — the picker is neutral ground, it presents, it never persuades; and never add a delete affordance inline on the row — removing a payment method is destructive and deserves its own confirmed moment elsewhere. Anatomy: the brand jewels (identity, not decoration — at a glance you know which card is which without reading a digit) · last-4 + expiry (the only numbers on the row, arriving from the backend already masked) · the default chip (gold outline, letterspaced, one per picker) · the new-card row (dashed at rest — it *promises* a different kind of action — solid on hover; the handoff carries nothing sensitive, no partial numbers, no session card data). Privacy: at most last-4 + brand, exactly as the payment backend returns them masked — the block never renders, stores, or transmits a full card number; the full PAN exists only in the processor's vault and PAY-002's transient fields. Removing a saved method goes through the processor's delete — the front end holds no card data to delete. The picker never invents a saved method for the demo, and the default chip is set by the user's stored preference, never by recency or by the block guessing. _Use:_ Saved-payment selection — choosing the instrument, handing off to PAY-002 for new cards.
_Source:_ gap-blocks/checkout-blocks.md

## Comments — conversation, kept honest

A comment thread earns its liveness the hard way: every state arrives from real
data, and everything it refuses to show is stated out loud. Nesting is capped at
three and the cap is visible; what looks nested is nested, what continues says
it continues.

_Verification: mechanical only (HTML parses, CSS balanced, zero yellow) — independent scorecard pending. Do not treat as triple-A until scored._

**CMT-001 — Comment thread.** The whole conversation: a composer on top,
top-level comments below, replies nested under honest depth rails to a hard cap
of 3, then a dashed "Continue thread" panel for the rest. Nothing is flat and
nothing is dead — collapse chevrons lift, rails ignite on hover in their depth
color (magenta → purple → blue), and the Post button is alive the moment there
is something to say. **Code:** one `.cmt` scope holds the composer (avatar
jewel, dark field, 52px Post button disabled until text exists), comment items
with action rows, the rail system (`.cmt-kids.d1/d2/d3` walking the Strip),
collapse chevrons with honest counts, the continue panel (a nested board riding
higher, labeled "Thread continues — depth capped at 3"), tombstones, and an
empty state. A family token sheet carries the ground, ink, and the fixed
reaction palette once. **States:** rest (quiet conversation, white 96% bodies);
hover (rail ignites, action pills lift 2px in their own color — reply
chrome-purple, love pink, share blue); press (settles 1px); focus (white 2px
ring on every control); collapsed (kids hidden, chevron flips, the count —
"2 replies" — stays real); continue thread (dashed button, nested board,
stated cap, deep replies flat and in order); composer rest/focus (dark field,
purple ignition, 38% truly-inert Post until text); tombstone (dashed edge,
italic "This comment was removed" — body gone, not teased); empty thread
(jewel, "No comments yet", "Say the first true thing"); edited (a quiet italic
flag, disclosed not paraded). **Do** cap nesting at 3 and name the cap in the
open; derive every timestamp from a real `datetime` in the markup — the
plain-words label ("2h ago", "Mar 4") is a rendering of truth, never "2 hours
14 minutes ago" theater and never "just now" for anything older than a minute.
**Don't** indent a fourth level "just this once"; one fake indent is a lie the
whole thread inherits. **Anatomy:** the composer is the thread's front door —
your app wires the real submit and waits for the server's receipt; the avatar
jewel is a rotated diamond in the author's stable assigned color, initials in
serif; the name row shows display name only (private by default — no emails, no
handles); the nesting rail is a 2px line in the depth's Strip color, marking
*where you are in the conversation*, never how anyone feels; the fold control
is a 44px chevron plus the real reply count; the continue panel makes the cap
visible; the tombstone is the honest grave. _Use:_ Any discussion surface that
needs threads with a stated, structural depth limit — Smart Feed comments,
lesson threads, review discussions. _Source:_ gap-blocks-2/comments-blocks.md
_What it will NOT fake:_ it never renders a fourth indent — the cap is
structural, not a suggestion. It never invents replies to fill a thread — an
empty thread says so. It never shows a "Posting…" state that resolves locally
and claims delivery. Removed comments show nothing of the body, ever.
Timestamps never claim precision the data doesn't carry.

**CMT-002 — Single comment.** The atom the thread is built from: avatar jewel
(52px, one size up for presence), serif 18px name, plain-words timestamp,
15px body, and an action row — reply in chrome-purple, love in pink as a
toggle, share in blue. **Code:** one self-contained `article` — the jewel, the
name row, the body with an honest four-line clamp (`.is-clamped`, full text
kept in the markup and the accessibility tree), and the action row from the
same `.cmt-act` family CMT-001 uses; the specimen script only toggles the clamp
and the love state locally. **States:** rest (dark board, white-lit edge,
actions transparent with white glyphs — color earned by interaction); hover
(lifts 4px, edge brightens, soft tone under-glow — chrome-adjacent, never a
reaction color); action hover (each pill lifts and ignites its own color);
love-on (`aria-pressed="true"` — held pink edge, filled heart, tabular-numeral
count, toggling off returns it to rest, because play can be taken back);
press (settles 1px); focus (white 2px ring); clamped (four lines, "Show more /
Show less" labeling the truth both ways); disabled (38% opacity, `disabled`,
truly inert — never hover theater on a dead control). **Do** keep the love
count identical to the reaction row's love count — same data, same number,
rendered twice, never computed twice; clamp long bodies with a real control.
**Don't** truncate with an orphaned ellipsis; don't let the single comment
drift from the thread's comment — CMT-002 *is* CMT-001's atom, so if they
disagree on spacing, type, or behavior, one of them is wrong. **Anatomy:** the
jewel follows the family law (assigned once per author, never changed between
renders); the name row shows display name and nothing else; the body holds
1.6 line height and the clamp control is part of the block, not an afterthought;
the action row offers reply (chrome), love (pink toggle, one count one truth
shared with the reaction row), share (blue, firing the app's real share path);
the count is the server's count in tabular numerals. _Use:_ Featured comments,
quotes, and embeds — anywhere one comment stands alone but must stay
identical to its in-thread sibling. _Source:_ gap-blocks-2/comments-blocks.md
_What it will NOT fake:_ the love count is the real count or the pill is
absent — no "0 loves", no invented social proof. Share never confirms what it
didn't do. Reply never opens a composer that can't post. The clamped body never
hides text from assistive technology.

**CMT-003 — Reaction row.** The play layer: jewel pills with honest counts,
toggle on/off, a dashed plus that opens the fixed five-reaction set in wheel
order — love pink, celebrate magenta, thoughtful purple, agree blue, laugh
green (a sixth takes indigo, never restarts the wheel). Reactions are opt-in
delight: no badges, no streaks, no "top fan", no leaderboards. **Code:** a
`.cmt-rx` group with pills (drawn SVG glyph + tabular-numeral count, 1.5px
edge in the reaction's fixed color) and a plus button; the popover holds the
five in wheel order, keyboard-operable with Esc closing and focus returning;
the specimen toggles locally, and the comment says it — a live build
re-renders counts from the server after each toggle lands. **States:** rest
(dark pills, 1.5px colored edge — present, not loud); hover (lifts 2px, glows
in the pill's own color — never blanket purple); mine (held glow + inner wash
+ filled glyph — your reaction, visibly yours); press (settles 1px); focus
(white 2px ring, Esc closes the popover); plus rest/open (the dashed circle
promises more, the elevated panel keeps the promise); zero count (the pill
does not exist — no "0" pill, no grayed ghost). **Do** render only reactions
that exist — three honest pills beat five with two zeros; let anyone take a
reaction back with no guilt copy and no "are you sure?". **Don't** sort pills
by count to manufacture a leaderboard; don't add badges, streaks, or any
status game — play that keeps score stops being play. **Anatomy:** the pill
is the unit — one per reaction that exists; glyphs are drawn, never emoji;
the plus is the fixed set's front door; reactor names appear as display names
only in the `title`, droppable where privacy rules say so — the count is
public, the names are a choice. _Use:_ The play layer under any comment —
feed cards, replies, stand-alone comments. _Source:_ gap-blocks-2/comments-blocks.md
_What it will NOT fake:_ counts are the server's counts — never rounded, never
"12k" theater, never incremented optimistically and left there when the request
fails (a failed toggle rolls the pill back and says so plainly). Zero-count
reactions are absent, not grayed out. The popover never offers a reaction
outside the fixed set.

## Chat — calm motion, truth-states only

Living but calm: motion breathes at 72 beats per minute — slow enough to be
calm, alive enough to be awake — and every state is earned. A typing indicator
exists only while a live signal says someone is typing; a read receipt turns
only after the other side actually rendered the message; the scroll sticks to
the bottom only if the reader is already there. Nothing in this family ever
performs liveness it does not have.

_Verification: mechanical only (HTML parses, CSS balanced, zero yellow) — independent scorecard pending. Do not treat as triple-A until scored._

**CHT-003 — Chat bubbles (in/out).** The atomic message object: incoming on the
left (dark board, white-lit edge — the world speaking in), outgoing on the
right (held 1.5px purple edge — my voice, choosing intelligence, going out; a
spine, never a flood), a rotated-square tail pointing the way the words came
from. Consecutive messages from one sender collapse into a group — one avatar,
one timestamp, no repeated faces. **Code:** `.chat-row` flex lines with
incoming/outgoing bubble geometry, tails as rotated squares in the bubble's own
background, grouping classes (`.grp`, `.grp-first`) with the rule stated in the
specimen — same sender *and* under 5 minutes apart, never across a date
divider; receipts are drawn SVG ticks whose only writer is `setReceipt(el,
state)`, and a screen reader hears the contract words ("Sending / Sent /
Delivered / Read"). **States:** rest in (white-lit edge, white light for the
world's words), rest out (held purple edge + soft under-glow); hover (lifts
2px, ignites white for incoming, purple for outgoing); press (settles 1px);
grouped (avatar hides but keeps its space, margins tighten 4px → 2px,
adjoining corners square, tails suppressed, one name + time on the first row);
receipts — the four forward-only truth-states: `sending` (single dim tick),
`sent` (single white tick — the server has it), `delivered` (double white tick
with glow — their device has it), `read` (double gold tick + gold "SEEN" —
their client *rendered* it, reported back through the transport); edited (an
italic tag inside the bubble — disclosed, no history paraded); long messages
(wrap at 480px/70% — a 2,000-word message is a document problem, never a "…").
**Do** render receipts only from the transport's truth — the block displays
states, it never invents them; `setReceipt` is the single writer of
`data-state`. **Don't** ever show "read" because the message is old, because
the app was backgrounded, or because it looks better — a fake read is a trust
violation with styling, and this family has exactly one unforgivable sin.
**Anatomy:** the row is a flex line, avatar + bubble, outgoing reversed; the
avatar orb is a 36px lit jewel — incoming blue, outgoing purple, the tone
following the speaker's edge; the bubble carries 15px text (never smaller —
chat is read at a glance, in motion), 18px radius with the speaker-side corner
squared where the tail grows; the meta line gives name + time for incoming,
time + ticks for outgoing; ticks are drawn strokes, never emoji, never
characters. _Use:_ The message object itself — any conversation surface, from
DMs to the Studio channel. _Source:_ gap-blocks-2/chat-blocks.md
_What it will NOT fake:_ it never marks read before the other side renders —
the `read` state arrives through the transport, never from a timer, a guess,
or the app being in the foreground. It never groups messages from different
senders, more than 5 minutes apart, or across a date divider. It never logs,
previews, or echoes message content anywhere outside the bubble. It never
shows an avatar for a speaker the renderer doesn't know — unknown senders get
the orb in chrome-white, never a fake face.

**CHT-004 — Typing indicator.** Three living dots in an incoming bubble shell —
the calm heartbeat of someone about to speak, pulsing at 72bpm, staggered at
quarter-beat intervals. Its whole point: it exists **only while a live signal
says someone is typing** — no signal, no dots — and 30 seconds with no
keep-alive and no message dismisses it honestly. **Code:** the shell reuses the
incoming bubble's geometry so the dots read as the speaker's unfinished
sentence; `chatTyping.show(el, signalId)` *throws* without a live signal id
(the throw is the law in code); `keepalive` re-asserts on a 20s cadence from
the transport; `arrived` unmounts the instant the real message renders; the
30s watchdog fires `chat:typing-expired` on honest dismissal; reduced motion
drops the pulse to steady dots, and the meaning survives. **States:** rest
(three white dots breathing in the incoming shell — the speaker is the world
speaking in); live (the pulse — scale .72 → 1.12, opacity .45 → 1, one beat
per 0.833s, `ease-in-out`, never snappy); keep-alive (invisible — the dots
simply continue while the contract resets underneath); watchdog expiry (dots
fade, the row unmounts — the honest end of an unfinished thought, no message
owed); message arrival (replaced by the words, never lingering "for effect");
reduced motion (steady dots at 85% opacity). **Do** require a live signal id
for every render — no signal, no dots, no exceptions. **Don't** keep the
indicator alive to look responsive while the other side went quiet; after 30
seconds the honest answer is absence, not persistence — a typing indicator that
outlives the typist is a ghost with styling. **Anatomy:** the shell (incoming
geometry, white-lit edge, left tail — Sam's place, Sam's unfinished sentence);
the dots (three 9px white orbs, stagger 0 / .208s / .416s so the pulse travels
left to right like a breath, never a flicker); the heartbeat (`--bpm:0.833s`
— 72 beats per minute, the resting human pulse; nothing here animates faster
than one beat); the "who" line ("Sam is typing" — felt in dots, stated in
words, announced to screen readers via `role="status"`); the watchdog (30s,
non-negotiable, in code — not a guideline, a timer). _Use:_ Any live
conversation where a transport can report typing truth — never as decoration
on a quiet screen. _Source:_ gap-blocks-2/chat-blocks.md
_What it will NOT fake:_ it never renders on a schedule, on a timer "to look
alive," or because the conversation went quiet and the screen felt dead —
those are the three classic forgeries and the `throw` exists to stop all
three. It never converts an expired indicator into a message — absence stays
absence. It never shows two indicators for one signal id. The aria
announcement fires only for real signals; a fake announcement lies to a
screen-reader user exactly as badly as fake dots lie to a sighted one.

**CHT-005 — Message list.** The conversation as a room: bubbles (CHT-003)
day-grouped under serif date dividers, in a board that scrolls with an honest
contract — it sticks to the bottom only if the reader is already there, and it
never yanks a reading user. **Code:** a 5-layer-shadowed board with a header
(avatar orb + serif room name + presence line rendered *only* from a live
presence feed), a scroll region holding date dividers ("Today · Oct 16" —
serif, letterspaced, uppercase, hairline rules fading both ways), and a sticky
"New messages" pill with an honest count; `chatAppend` is the only writer of
new rows and measures `atBottom()` (within 64px) *before* the row lands; the
empty room and the loading line ("Loading your messages…" with one breathing
orb) are specified verbatim. **States:** rest (board, header, scroll region,
serif chapter marks, bubbles per CHT-003); day divider (the hard boundary —
groups never cross it); new message with reader at bottom (the row appends and
the list glides — nothing is taken from the reader); new message with reader
up-list (the list does not move; the pill appears — "New messages" with the
honest count — a real button that keeps its promise: one tap, bottom reached,
count clears); reader scrolls home (touching the bottom edge clears the pill —
the contract resolves itself); empty (centered purple jewel, "No messages yet",
"Say the first word" — an empty room is a state with dignity); loading
history (one breathing orb, one honest sentence — words, never fake
message-shaped skeletons); presence ("3 here now" — no feed, no line; a
guessed headcount is a forgery of company). **Do** measure the edge *before*
the row lands — the decision to move belongs to the moment before the world
changed, not after. **Don't** smooth-scroll a reading user to the bottom
"because something arrived" — yanking a reader mid-sentence is the chat
equivalent of grabbing their book; the pill is the polite knock, the yank is
the shove. **Anatomy:** the board (the room — 5-layer shadow, 24px radius,
tone under-glow; bubbles live inside it); the header (the warm front door —
44px orb, serif room name); the scroll region (480px, thin purple scrollbar,
keyboard-enterable); the date divider (serif voice chapter marks — the one
place the family's TYPE law shows at chat scale); the scroll pill (the
contract made visible — sticky, 44px, chrome ignition, honest count badge);
the empty state (jewel + two lines, verbatim — the words do not improvise);
the loading state (loading is a state with words, not shapes). _Use:_ The
full conversation room — DMs, channels, group threads — wherever bubbles need
a room and a scroll contract. _Source:_ gap-blocks-2/chat-blocks.md
_What it will NOT fake:_ it never auto-scrolls a reader who isn't at the
bottom — the 64px edge is measured, not assumed. The new-messages count is the
real count of rows appended while away, never a badge for decoration. It never
renders divider labels for days with no messages on either side — a divider
marks a boundary between real rows, never an empty chapter. It never shows a
presence count without a live feed, never shows "online" from a last-seen
timestamp, and never renders fake message-shaped skeletons while loading. The
empty state never suggests what to say — "say the first word" is an
invitation, not a prompt.

## Onboarding — the welcome family

Three blocks, one family, one law order. Every reachable node lifts and
ignites (Law 1); the 5-stop strip walks the steps in law order and a color's
meaning never changes between blocks (Law 2 — magenta meets, purple chooses,
blue connects, green grows, gold earns the light; a sixth step continues the
wheel with orange, a seventh with red, never reusing a stop); the welcome
board rides the field, nodes ride above the thread, the ring rides its own
board (Law 3); serif voice on step names and headlines (Law 6). The family
laws: each step earns the next — progress is real, never theater. One job
per step, one CTA per card. Honest percentages. Celebration with restraint:
one ignition, then calm.

_Verification: mechanical only (HTML parses, CSS balanced, zero yellow) — independent scorecard pending. Do not treat as triple-A until scored._

**ONB-001 — Stepper.** The multi-step progress rail: five jewel nodes (done,
current, locked) sitting over a dark thread that fills in the 5-stop
spectrum as you advance. The fill width is derived from the current step's
real index on every render — never hardcoded per story. One job is named
per step, and skippable steps carry an honest "Optional" chip. A locked
step is dim and truly inert — disabled, out of tab order, no hover lift, no
glow; it never fakes being clickable. Never a wall of forms: the rail shows
the journey and each step carries exactly one job. If no steps are
configured, there is no rail — an honest "No steps yet" panel, and the
plain-words line that this is not step zero of five. States: Rest (dark
thread, step-colored jewel nodes, serif step titles); Hover (reachable
steps lift and ignite in their own step color — done steps are revisit
buttons, and clicking one goes back); Active/press (the node brightens, it
feels held); Current (held ignition in the step's own color plus a slow
three-second breathe; exactly one current step ever); Locked (34% opacity,
unreachable because the next step is earned, not previewed); Empty (the
honest panel). **Do** mark skippable steps with a plain "Optional" chip and
give the step's own content an honest "Skip this step" control — skipping
is a first-class choice, not a hidden shame. **Don't** unlock all steps
"for preview": a locked step you can peek into teaches the user that locks
are theater, and then nothing in the flow is trusted. Anatomy: the thread
(dark track, strip-gradient fill in law order — the fill is the walked
spectrum, it never runs backward); the node jewel (rotated diamond, white
to step-color to black with its own glow — done shows a drawn check, Law 4,
current shows the number and breathes, locked shows the number at 34%);
the label stack (letterspaced kicker, serif title, status line with a
jewel dot in the step color — the dot is information, not decoration);
the optional chip (in the step's own color — a promise the flow still
completes when skipped); the one-job line under each label (a step with
two jobs is two steps — split it). What it will NOT fake: the thread never
fills past the current step — a full thread on step two of five is a lie;
locked steps never respond to hover; the rail never renders more nodes
than the flow has; "You are here" sits on exactly one step; a skipped
optional step advances the flow honestly, it is not silently "completed."
_Use:_ Multi-step first-run flows (signup tours, setup wizards) where each
step earns the next and progress must be real — the rail that shows the
journey without becoming a wall of forms.
_Source:_ gap-blocks-2/onboarding-blocks.md (this spec file holds the full code; it is being copied into the repo alongside this catalog update).

**ONB-002 — Welcome card.** The first-run greeting board: Naya's face and
her energy — a drawn SVG orb (white to purple to black, two eyes with
catchlights, one calm arc) with a slow five-second halo breathe — a warm
front door riding the full 5-layer shadow. "First run" kicker, one serif
headline, one warm line of plain words, exactly one clear next action. The
headline greets by name only from the block's `data-name` attribute: the
specimen carries none, so the honest default renders "Welcome." — no
placeholder, no "there," no invented name. Personal without creepy: the
card's honesty footnote, printed on the block itself, says "This card knows
only what you've told it." One primary CTA — "Begin the tour" (52px, black
heart, white rim, drawn arrow glyph; it says where it goes, not "Get
started") — and one quiet text exit ("I'll explore on my own") that is an
exit, not a competing button: no lift, no glow, no color. States: Rest
(the board on its shadow, the halo breathing — presence, not decoration);
Hover (the board lifts 5px and ignites chrome-purple — it is chrome, so it
burns chrome's color — and the CTA lifts and ignites with it); Active/press
(the CTA settles 1px, it feels held); Focus (white 2px ring on the CTA —
keyboard users get the same ignition promise); Quiet exit (65% opacity,
underline only on intent); Nameless (the honest default). **Do** keep
exactly one primary CTA — the card has one job: get the user to the first
step. **Don't** add a second bright button "just in case," and never three
competing CTAs — every extra button halves the chance the user presses any
of them. Anatomy: the face (drawn geometry with energy — never an emoji,
never a stock avatar, never just a logo); the kicker (it names the moment
honestly); the headline (serif, 32px, name slot filled from `data-name`
and from nothing else); the one line (15px, warm, max 44ch — one promise,
not a paragraph of features); the one CTA (canonical button DNA); the
quiet exit (present but never competing); the honesty footnote (part of
the block, not documentation). What it will NOT fake: it never greets by
a name it wasn't given — no "Welcome, friend," no mail-merged guess from
an email local-part; it never claims the tour is "quick" unless the flow
really is five small steps; the face is drawn geometry, not a photo of a
person who doesn't exist.
_Use:_ The first-run greeting — the warm front door when the app opens for
the first time, greeting the user by name only when the name was given.
_Source:_ gap-blocks-2/onboarding-blocks.md (this spec file holds the full code; it is being copied into the repo alongside this catalog update).

**ONB-003 — Progress indicator.** Progress as honest truth: a linear bar
and a ring variant, the percent a real number from real work, and a
celebration that fires exactly one ignition and then goes calm. Four
mouths, one truth: the serif number, the bar's fill width, the ring's
stroke offset, and the progressbar's `aria-valuenow` all derive from a
single source — a mismatch is a bug, not a style choice. The specimen
freezes at 62% as a teaching state; a live build binds the number to the
work and nothing else. Numbers breathe — no static numbers on screen.
States: Rest (dark board, serif percent breathing on a 4s loop, strip-
gradient fill, honest sub-count like "5 of 8 done" — the percent's receipt);
Hover (the board lifts 3px; the ring answers with a soft glow but no lift —
it is a readout, not a button; readouts may glow without lifting); Zero
(0%, empty bar, "Ready when you are" — a real state, not a hidden one);
Complete (one 1.1s gold ignition on board and ring, then calm: gold edge,
gold 100%, the breathe stops — gold is attention, earned, and the finish
line is the only thing that wears it); Indeterminate (when the work
genuinely can't report a number, a soft spectrum drift crosses the bar and
the label says "No number yet" in plain words — never parked at 99%, never
an invented 47%); Reduced motion (ignition, breathe, and drift all stop —
100% still reads 100%; the meaning survives without the motion).
**Do** derive the number, the fill width, the ring offset, and
`aria-valuenow` from one source. **Don't** stall at 99% while work finishes
(theater), don't ease a fake 0-to-100 on load (the number must mean
completed work), and don't celebrate twice — re-adding the complete state
to re-fire the ignition is confetti with extra steps. Anatomy: the label
row (letterspaced job name plus serif percent — the percent is this block's
headline); the linear bar (12px inset track, strip fill in law order that
resolves to gold at 100%); the ring (168px SVG, round cap, gradient walked
around the path, serif number in the middle — the ring frames the truth, it
doesn't decorate it); the sub-count (the receipt; if the count isn't known,
the line says so instead of inventing one); the celebration (1.1s, once,
then calm — no confetti, no particle spam, no encore). What it will NOT fake: the percent is
completed work over total work — never time elapsed, never a guess, never "almost there" parked at 99%; the indeterminate state
is only for genuinely unmeasurable work — a measurable job shown as
indeterminate is honesty theater; the complete state is added once, when
the backend confirms 100% — the animation firing is the receipt that the
work is done.
_Use:_ Setup and sync progress where the number must mean completed work —
linear for tight layouts, ring for centered moments, indeterminate only
when the work truly can't report yet.
_Source:_ gap-blocks-2/onboarding-blocks.md (this spec file holds the full code; it is being copied into the repo alongside this catalog update).

## What is NOT here (yet)

The catalog is honest about its edges:

- **Wave-1 fixes pending.** CAL-001..005 (9.0/10) and PAY-001..005 (8.8/10)
  carry identified fixes not yet applied — see `gap-blocks/GAP-BUILD-NOTES.md`.
  Do not treat them as triple-A until the fixes land and re-score.
- **Wave-2 independent scorecard pending.** CMT-001..003, CHT-003..005,
  ONB-001..003 are mechanically verified only — a different seat has not
  yet scored them.
- **Next gap tier:** notification center, general error state, form
  validation + file upload, auth companions (signup / reset / SSO).

New gaps go here when found — never buried.
