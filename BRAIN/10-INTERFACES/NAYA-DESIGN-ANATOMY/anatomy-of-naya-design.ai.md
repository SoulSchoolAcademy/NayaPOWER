# THE ANATOMY OF NAYA DESIGN — AI Tongue (Builder Contracts)

**For:** builder seats and agents · **From:** Naya Resolve · **Date:** 2026-10-31
**Status: RATIFIED — Shawn, 2026-10-31 18:07Z ("Official — lock it in").** Amended at ratification: Signature is obsidian (Diamond White rejected); Law 6 — alive means it answers touch — binds every contract below.
**Source of truth:** `the-anatomy-of-naya-design-2026-10-31.human.md` (the decision document). This tongue carries the same decisions as executable contracts: anatomy, invariants, chosen concept, and the gate check that proves each. Where the human tongue does not fix a numeric token, this file marks it `MEASURE-FROM-APPROVED` — take the value from the approved pages (Life with Naya, the certificate page, the Smart Tabs kit v9) and record it in the machine tongue when measured. Never invent a token.

---

## 0. GLOBAL INVARIANTS (every element, no exceptions)

| ID | Invariant | Gate check |
|---|---|---|
| G1 | Obsidian ground: black-with-depth background, white text, high contrast. No white/light/pastel/matte-flat surfaces. | Computed background + text contrast measured on the served page |
| G2 | Living depth: every interactive element is layered (shadow + base + multi-line rim). Flat 2D = fail. | Layer/rim presence via computed styles |
| G3 | Ignition: white light at rest; on hover/touch/focus the element ignites in its own color only. Glow has no other job. | State inspection: rest vs hover/focus |
| G4 | Spectrum walk: magenta → purple → blue → green → gold (magenta leads — Law 10, one global sequence per page, richest first); never the same color twice in a row; one color job per element; a color means the same thing on every page. | Adjacency scan of colored elements in DOM order |
| G5 | Geometry: boards/cards 16:9; buttons pill-shaped; touch targets ≥ 44px; type ≥ 14px. | Measured bounding boxes + computed font sizes |
| G6 | Alive honestly: motion only from real events/data. Decorative ticking = fail. | Every animated element bound to a real event kind |
| G7 | State completeness: rest, hover, pressed, selected, loading, empty, error — all designed and truthful. No dead buttons, no fakes; SOON lawful only as an honest, non-interactive label — a SOON button/tappable element is a dead control and fails; unwired renders its honest frame. | State matrix walk per element |
| G8 | Family: one canonical component, imported everywhere; never copied, never locally varied. Approved pages are the element library. | Part identity vs Factory registry (byte/class match) |
| G9 | Two-second read: essence first, glanceable, push-button simple. | Cold-read review (human judgment, recorded) |
| G10 | Every number carries magnitude + shape + direction + a human sentence (SN-0822), or it does not ship. | DOM scan for bare numerals on stats surfaces |

## 1. BUTTON — `.naya-btn`

**Anatomy (7 layers, bottom → top):** (1) elevation shadow, colored, below the object · (2) base plate: obsidian glass, vertical gradient lighter at top · (3) rim: ≥ 3 lines — outer hairline of light, spectrum edge in the button's own color, inner shadow line · (4) icon chip: jewel disc or rounded square, left, glyph inside, button's color · (5) label: white, semibold, sentence case, ≥ 14px, optically centered against the chip · (6) live slot (optional): right-side number/state word, tabular figures · (7) state skin.

**States:** rest = white light in rim · hover/touch = rim + chip ignite in own color, lift 1–2px · pressed = sink 1px, inner glow deepens · selected = white-hot rim · disabled = never hidden; dimmed with the reason readable.

**Levels:** Signature (one per view, the conversion action — obsidian body, maximum ignition/scale/motion; NEVER a white body) · Primary (page's main verbs) · Standard (bar/board actions) · Compact (chips inside boards; still ≥ 44px on touch) · Jewel (icon-only, ≥ 44px, label on tap/hover). **Law 6 (ratified): alive = answers touch — no halo/glow at rest; the orb carries its color as identity, solid; ignition only on interaction.**

**Chosen concept:** physical jewel glass (score 10/10 vs the laws), borrowing Apple frosted capsule's blur discipline inside the glass, Tesla instrument sizing confidence, Raycast density for pro surfaces only. **Rejected as canon:** Linear/Vercel flat (fails G2), Material You tonal (pastel risk, unfixed color meaning), neumorphism (fails contrast), flat web button (the anti-pattern).

**Contract:** a button that is not `.naya-btn` imported from the Factory is not a Naya button, whatever it looks like.

## 2. BOARD — `.naya-board`

**Anatomy (6 zones):** (1) ground plane: obsidian glass, one elevation above page ground, colored shadow · (2) rim light: same 3-line rim as the button (visible sibling) · (3) header strip: jewel + title + live state (breathing dot when streaming) + ↗ one-tap-to-detail corner · (4) body zone: exactly one subject; white space is designed material · (5) spectrum spine: thin edge/accent in the board's category color (stats boards take their WHAT-category color) · (6) footer/action zone (optional): verbs as standard buttons, never text links pretending.

**Proportions:** 16:9 family. Exceptions: strips (Pulse Strip, wide) and tiles (square members of the same family).

**Chosen concept:** obsidian bento — bento proportions + Apple Weather glass recipe + Naya rim light and spectrum spine. Stats boards additionally inherit the Trackify skin discipline via the Smart Stats spec.

## 3. ICON — `.naya-chip-icon`

**Anatomy:** (1) glyph: geometric construction on a 24-unit grid, one stroke-weight family-wide, optically sized (draw bigger what measures same but looks smaller) · (2) chip: jewel disc or rounded square with rim light — the family uniform; every system glyph lives in one · (3) color job: chip carries the element's one color; glyph white at rest, ignites with the chip.

**Native marks:** ⭐ favorite (L1) · 💜 priority (L2) · ◆ diamond bullets · ＋＋ twin pluses — drawn in the same geometry.

**Chosen concept:** custom geometric glyphs in jewel chips, drafted with SF Symbols' optical-sizing discipline. **Rejected:** emoji as system icons (device-variant rendering, no family control), downloadable generic sets as the identity (the glyph is a commodity; glyph + chip + color job + ignition is the signature).

**Family test:** a citizen identifies the icon as ours with the label removed.

## 4. INPUT / COMPOSER — `.naya-input`, `.naya-composer`

**Law:** buttons rise, inputs sink. **Anatomy:** recessed obsidian well — inner shadow at top edge, rim light at bottom edge · jewel caret · spectrum focus ring (ignition on focus, in the field's color) · furniture chips inside the well (Dictate 🎙 · Schedule · attach) rendered as standard buttons.

**States:** hint (dim, honest) · typing · error (red rim + the reason in words) · success (gold flash).

**Chosen concept:** the composer jewel — ChatGPT-composer familiarity, Linear slash-command grammar (`/`) inside Smart Mail and Ask Naya.

**Contract:** the composer is ONE canonical part, imported verbatim on every page. (Defect class this kills, from the 2026-10-31 scorecard: Business missing Dictate + Schedule that its sisters carry.)

## 5. GRAPHS & CHARTS — the Smart Stats set

**Contract:** colors locked per WHAT category (Smart Stats Build Spec v3 §3) · living draw-in on load · drill-down on every mark · human sentence under every chart (SN-0822) · honest empty frame when unwired · every animated tick driven by a real ledger event (the tick rule) · reconciliation: displayed score == value-table formula applied to displayed counts.

**Chosen concept:** the Naya Smart Stats set — 8 canonical blocks (Pulse Strip · Trend Panel · Mix Donut · Journey Funnel · Faces Board · Insight Feed · Heat & Streaks · Health Gauge) + per-source visual grammars (creating = steps · notes = constellation · likes = ripples · shares = branches · invites = funnel · sales = climb · membership = closing ring · all currents = the River). Borrows: Robinhood's flood-the-environment, Apple Health's closing ring, Strava's one-metric restraint. **Rejected:** static chart images (a photograph of data is dead data).

**Status note:** charts are the Vitality Law's proof surface — no claim without its graph.

## 6. REMAINING PARTS (one-line contracts)

- **Top bar / Smart Bar (`.naya-bar`):** two families on every bar — the app's own sections + related areas as quick tabs; living-depth pills; the breathing jewel; search mounted in the chrome, one wording, network-wide. One mount; Nitro renders, seats import.
- **Bottom network bar:** the identical 11-app bar on every page. Already live as the family constant — do not vary it.
- **Tabs (`.naya-tabs`):** Smart Tabs kit v9 anatomy — white at rest, ignite on touch, state persists and follows the user.
- **Toggle (`.naya-toggle`):** jewel sliding in a recessed track; on = ignited color + white jewel forward. Never a bare checkbox on a citizen surface.
- **Slider (`.naya-slider`):** spectrum track, jewel thumb ≥ 44px, live value in a chip that ignites while sliding.
- **Face (`.naya-face`):** real photo in a rim-lit ring; presence = breathing ring in the person's spectrum position; staleness shown honestly as data ("last active 9d ago").
- **Badges & chips:** state words only when true. A SOON chip is an honest label, never a button — a tappable SOON is banned dead chrome. Honest-state chips (Law 2 truth colors): LIVE (gold pulse — gold = live/shown) · PROVEN (green) · NOT TRACKED YET (dim frame) · SAMPLE (labeled specimens only, never removable).
- **Menus & popovers:** glass sheets rising from the summoning element; one level deep; every item a standard button row.
- **Modals & sheets (`.naya-sheet`):** page dims, sheet rises with rim light; one decision per sheet; commit action at the Signature level (obsidian, maximum ignition).
- **Toasts (`.naya-toast`):** bottom-rise; jewel + one sentence + one action; auto-dismiss except errors, which stay until answered.
- **Lists & tables:** rows as flat members of the board family (rim on hover), diamond bullets, ranked bars for ordered data; a table is a board whose body is rows.
- **Search:** ONE search — chrome-mounted, one wording ("Search the network…"), Spotlight grammar: one field, whole system; results filtered Blocks · People · Spaces · Pages · All.
- **Media player (`.naya-play-disc`):** rim-lit disc, jewels at the rim, ignites on play; progress as a closing ring.
- **Progress:** rings close, bars fill left-to-right in spectrum order, counters count; never an indeterminate spinner where a real number exists.
- **Empty state (`.naya-empty-frame`):** honest frame — what will live here, why it is empty, the one action that fills it.
- **Loading (`.naya-skeleton`):** the breathing jewel + the skeleton of the real board in its real proportions; the shape of the answer arrives before the answer.

## 7. BANNED (hard fails)

White or light backgrounds · flat buttons with an icon pasted on · glow for decoration · the same color twice in a row · locally varied components · dead buttons and SOON worn as a button (SOON as an honest, non-interactive label is lawful) · fake numbers and SAMPLE outside labeled specimens · text walls describing life instead of showing it · emoji as system icons · indeterminate spinners over knowable numbers · any element in only one state · any part a builder must redraw instead of import.

## 8. FACTORY STOCK LIST (first stocking — all imports, no redraws)

`.naya-btn` (hero/primary/standard/compact/jewel) · `.naya-board` (16:9 + strip + tile) · `.naya-chip-icon` (glyph set v1, 24-grid) · `.naya-composer` (verbatim, with Dictate + Schedule) · `.naya-input` · the 8 Smart Stats blocks · `.naya-bar` (top mount + bottom network bar) · `.naya-tabs` (kit v9) · `.naya-toggle` · `.naya-slider` · `.naya-face` · `.naya-sheet` · `.naya-toast` · `.naya-play-disc` · `.naya-empty-frame` · `.naya-skeleton`.

**Stack verdict:** every chosen part is buildable in the current stack — HTML/CSS layered shadows, gradients and blur, inline SVG glyphs and charts, the working Smart Tabs kit. No WebGL, no exotic dependency. Buildability in-stack was a selection criterion.

## 9. HOW IT LOCKS IN

Parts ship as imports from the Factory registry → the executable design gate checks this anatomy as code (layer count and rim presence via computed styles, spectrum walk, contrast ratios, touch targets, state completeness, reconciliation for stats) → every correction Shawn makes becomes a regression test → the floor only rises.

**Open token work:** values marked `MEASURE-FROM-APPROVED` (exact shadow offsets, blur radii, gradient stops) are measured once from the approved pages / Smart Tabs kit and written into the machine tongue; until then a builder uses the kit's own values, never a guess.

— Naya Resolve, 2026-10-31
