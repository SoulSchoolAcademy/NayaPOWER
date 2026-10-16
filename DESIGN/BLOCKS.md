# NAYA SMART BLOCKS — the catalog

Every reusable piece. Name it, snap it in, never reinvent it.
A block ships with: its code, its states, a do/don't, and honest anatomy.
A block without all four is a draft.

_Adoption 2026-10-16: 144 extracted blocks merged in (model-numbered BTN–MSC). The button-taxonomy ruling is a working default, pending Shawn's formal ruling._

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

## What is NOT here (yet)

Nothing open. Every gap the sources named is closed; every ruling recorded
above. New gaps go here when found — never buried.
