# NAYA SMART BLOCKS — the catalog

Every reusable piece. Name it, snap it in, never reinvent it.
A block ships with: its code, its states, a do/don't, and honest anatomy.
A block without all four is a draft.

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

## Truth components — "A claim and a proof must never look the same."

| Block | Use |
|---|---|
| `.truth` card + `.torb` orb | Three states: VERIFIED (green ✓ — independent evidence exists) · CLAIM (gold ? — shown honestly, awaiting its stamp) · DEMONSTRATION (magenta ◈ — beautiful on purpose, a specimen, not live). |
| Truth badges | ✓ AUTH·VERIFIED / ? CLAIM·UNVERIFIED / ◈ DEMONSTRATION — stamped on content. |
| Truth orbs as objects | Green = proven · gold = shown · blue = stated. |

Law 75: loading is honest. Fake success is a trust violation.

## The Intelligent Block pattern

The Smart Note anatomy. "A lesson that stays learned. One object. Four
layers of understanding. One clear next action."

**IN A NUTSHELL** → **WHAT IT MEANS** → **HOW TO USE IT** → **WHAT YOU GET.**

Every Smart Note card, every lesson surface, every report summary follows this
anatomy. Same order, every time.

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

## Supporting pieces

`.spectrum-bar` (5-segment law-order bar) · `.law-card` (ignites own color on
hover) · `.rule-board` (do/don't boards) · `.callout` (magenta-edged) ·
`.checklist` (green ✓) · `.copy-btn` + `pre.code` (every component ships
copy-paste code) · `.toc` pills · `.gate-bar` (spectrum launch bar).

## What is NOT here (yet)

Nothing open. Every gap the sources named is closed; every ruling recorded
above. New gaps go here when found — never buried.
