# The Anatomy of Naya Design — ultimate specification

**Author:** Naya Power · **Date:** 2026-10-31 · **Status:** SPEC + LAW RECORD — not a build, not live.
**How to read the marks:** LAW = locked by Shawn's word (design laws 2026-10-17, sha
0a3ae81b; design-gate machine spec 2026-10-25). SPEC = Power's proposal in this document,
not law until Shawn rules it. PICK = Power's recommendation among the top-10 concepts;
Shawn chooses. NOTHING here claims a build exists. Nitro builds to it; Power scores the build.
**Two voices, one spec:** HUMAN (plain words — what it looks and feels like) and MACHINE
(checkable rules — what the gate tests). Both say the same thing.

---

## Part 1 — The laws (LAW, all 16, condensed verbatim in substance)

1. **White text, always.** Headings white, body white or silver, on obsidian. Hierarchy
   from size, never from gray, never from colored text. No pink, magenta, purple, or blue
   text anywhere, at any size — including kickers (Shawn's word outranks the files).
2. **Gold is earned, never applied.** Gold = shown value (favorite, LED live status, what
   something is worth). Green = proven (verified, working). Blue = stated (claimed,
   declared). A claim and a proof must never look like each other.
3. **Chrome acts. Text speaks. Theme identifies.** Spectrum colors appear ONLY on borders,
   glows, selection states, LED dots, accent rails, corner jewels, icon backings. Never on
   text. Every use of color must earn its place structurally. If removing the color changes
   nothing about understanding, remove the color.
4. **Adjacent things never share a hue.** No two neighboring elements share the same color
   or almost the same color. Yellow next to gold is banned. Orange next to rich-orange is
   banned. Teal next to emerald is banned. Each element's color must be visibly distinct
   from everything touching it.
5. **One board, one color.** Each card, board, and feature gets one fixed, unique color —
   its identity, assigned once and kept. Spine, rail, and corner jewel speak it. Color
   belongs to the thing; a user should recognize the thing by its color.
6. **White at rest. Its own color ignites on touch.** A resting, unselected control is
   white/neutral: white text, a visible 1.5px+ white rim, no color. Color appears ONLY on
   the lit state — selected, active, touched — and then in that element's OWN color, never
   anyone else's. A purple unlit button is nonsense. Five purple lit buttons in a row is
   overload. ALIVE MEANS RESPONSIVE, NOT LIT AT REST: a button that glows at rest breaks
   this law; a button that answers touch — ignites, lifts, presses — is alive.
7. **Boards are rectangles.** Lists of things lay out as horizontal rectangles, one after
   another. Not grids of squares. The eye reads down; each rectangle gets room to breathe
   and its own identity.
8. **Restraint. Never a flood.** Default to black, white, and purple; the rainbow knows its
   place. A page where everything glows is a page where nothing does. Spend color like money.
9. **Verbatim tokens, no private colors.** Tokens copied exactly. No invented hexes.
   No "close enough." If it isn't a token, it doesn't go on the page.
10. **One global spectrum sequence per page.** Magenta → purple → blue → green → gold,
    once, in order, richest first. Section accents follow in law order. Law 4 still governs
    within sections: neighboring elements get distinct, spaced colors.
11. **Preview before pick.** A template is never chosen from a small block alone. Every
    template offers a big, obvious preview. Choosing blind is the builder's failure.
12. **Mobile IS the app.** Mobile first, killer on the phone by default, install-ready
    (PWA), slide-over panels, gestures. Mobile isn't a version — mobile is the app.
13. **Every control works, or it doesn't ship.** A button that doesn't function is a lie
    on the page. Pretty but useless never ships.
14. **Compose, don't create.** Build from the library's real pieces — real HTML, real CSS,
    verbatim. Never hand-write what the library already has. Never invent a private style
    when a piece exists.
15. **Depth before color. Zero flat.** Every surface gets living depth: elevation, edge
    light, seating shadow — established in black-and-white first. If it does not read as
    premium in monochrome, color will not save it. Flat is a defect, not a style.
    Machine form: three-layered elevation, boards within boards.
16. **Size separates. Color never does.** Hierarchy comes from size and weight. Source
    scale (Elements N2): 24 kickers, 18 headlines, 14 details. Color is never the thing
    that tells the eye what matters most.

**Machine floor (design-gate, NOT a pass):** private hex = FAIL. Button background using a
spectrum token at rest = FAIL (Law 6). Card/board with no box-shadow = FAIL (Law 15).
Button with no action = FAIL (Law 13). Spectrum color on text or gold in text/button
context = MANUAL REVIEW. A machine PASS plus no Nitro rendered review is still NOT ready
for Shawn. Nitro's rendered review (desktop + phone, real address) stands above the script.

### Tokens (LAW, verbatim)

Obsidian `#050507` · deep `#020203` · white `#ffffff` / paper `#F8F7FB` ·
purple `#a06bff` · magenta `#e84fff` · blue `#3fb8ff` · green `#2fe89e` ·
gold `#ffbf3d` (N5 canonical for now; five gold variants exist across files — OPEN,
needs Shawn's eye) · red `#ff5e6c` · teal `#40d3bb` · indigo `#6675ff` ·
lime `#b8ee57` · orange `#ff9a5a`. Fonts: Inter for UI, Newsreader for voice.

## Part 2 — Color language (LAW + SPEC)

- **Obsidian is the world.** Every page sits on obsidian/deep. White text on it, always.
- **Purple is Naya's presence.** The default accent, the home hue — used sparingly, never
  as a flood (Law 8).
- **Spectrum is identity + state, never decoration.** A spectrum color on a thing says
  either "this is that thing" (Law 5 identity) or "this is its state" (Law 2 truth-state,
  Law 6 ignition). Nothing else.
- **Walk, never repeat (SPEC, from Law 4 + Law 10):** colors walk the spectrum in law
  order across a page and never repeat adjacently. Two adjacent elements with the same
  or near-same hue fail, even if both are legal tokens.
- **Color never carries meaning alone (SPEC):** every color signal also has a shape, a
  word, or a position saying the same thing. A green dot alone never means "proven" —
  the word "Verified" or a check shape stands with it. Color-blind citizens and
  monochrome screenshots must still read the page.
- **Red (SPEC):** reserved for destructive and alert states only (delete, danger, blocker).
  Never decoration, never a brand color, never a default. The laws define green/gold/blue
  truth-states; red's reservation is Power's proposal.
- **Gold (LAW, with care):** gold means shown value or live LED. Gold headings, gold
  borders for looks, and gold buttons are banned. Gold must be earned by the thing it marks.

## Part 3 — Levels (what "levels" means in Naya design)

Four level systems, never confused with each other:

**A. Control levels — how finished a control is (SPEC, built on Laws 6 + 15).**
- L0 Flat — no shadow, no rim, no depth. DEFECT. Never ships.
- L1 Raised — rim + seating shadow. The minimum for anything tappable.
- L2 Elevated — three-layered: seating shadow + rim + edge light. The standard for boards.
- L3 Alive — elevated + ignites in its own color on touch + press motion + visible focus
  ring. The required level for primary actions. Alive = responsive, never lit at rest.
- L4 Signature — alive + own-color identity + a motion narrative (lift, glow, settle) +
  the one hero job on the view. Maximum one signature control per view (Law 8 restraint).
  The Dashboard gauge and the one hero verb are signature; everything else is L3 or below.

**B. Depth levels — boards within boards (LAW 15, machine form).**
Surface (page obsidian) → board (elevated rectangle) → board-within-board (nested panel,
deeper shadow, tighter rim). Depth reads in monochrome before any color is spent.

**C. Reading levels — glance → focus → explore (SPEC, from the living-data brief).**
Glance: the number, the word, the color — understood in 2 seconds. Focus: tap → the
story (why, what it means). Explore: tap again → the records, the doors, the actions.
Every element must work at glance level; depth is one tap behind, never hidden without a door.

**D. Truth levels — stated / shown / proven (LAW 2).**
Blue = stated (claimed, quiet). Gold = shown (marked value, live LED). Green = proven
(verified, working). A control, a number, and a claim each wear exactly one truth level,
and the level is visible in shape + word, not color alone.

## Part 4 — Anatomy of a button (HUMAN + MACHINE)

HUMAN: a button looks like a small obsidian tile with a white rim you can see, white words
that say the verb, and — when you touch it — it comes off the page: it lifts, its rim
ignites in its own color, and it settles when you let go. At rest it is quiet. On touch it
answers. It never shouts when nobody asked it to.

MACHINE — layers, back to front (SPEC measurements; tokens are LAW):

1. **Seating shadow** (below): soft dark shadow grounding the tile. Shortens on press
   (the tile sinks toward the page); lengthens on hover-touch (the tile lifts).
2. **Base fill:** obsidian `#050507` (or deep `#020203` on a board). Never a spectrum
   color at rest (machine FAIL, Law 6). Never white fill with black text — white with
   black text is dead.
3. **Rim:** 1.5px+ white at rest, visible. On touch/select: the element's own spectrum
   color (Law 5 identity). Focus (keyboard): rim thickens + own-color outer glow, always
   visible — a focused button you cannot see is a defect.
4. **Edge light:** a subtle white top-inner highlight — the "coming off the page" light.
   Established in monochrome (Law 15): if the button does not read as raised in
   black-and-white, color will not save it.
5. **Icon (when present):** white lines, left of the label, one consistent stroke weight.
   Icon backing ignites in the own color on touch; at rest the backing is neutral.
6. **Label:** white, Inter, verb first ("Message", "Connect", "Open", "Save" — never
   "Follow": the verb is Connect, never Follow). One verb, plain words, no jargon.
   Size separates hierarchy (Law 16): primary verbs larger than secondary verbs.
7. **State glow:** own color, on touch/select ONLY. Gold glow only for shown value
   (Law 2). Green glow only for proven states. Never a glow at rest.
8. **Motion (SPEC):** press = sink (shadow shortens, rim brightens) + release = settle.
   Motion is once per touch, quick, quiet — never looping, never bouncing for attention.
   Looping motion is a flood (Law 8).

**States (every button must define all of them, or it doesn't ship — Law 13):**
rest (white rim, quiet) · hover-touch (ignite own color, lift) · press (sink) ·
focus (visible ring) · selected (stays lit in own color) · disabled (dimmed white/silver,
no color, no glow, no action — SPEC: a disabled button states plainly why, on tap or
beside it, or it does not appear; a dead button that looks alive is a lie) ·
loading (motion shows progress, label stays honest — never a frozen button pretending
to work).

**Sizes and touch (SPEC):** primary verbs are thumb-sized on the phone (a thumb must land
on them without pinching or precise aiming); secondary verbs smaller but never tiny.
Touch targets never overlap. 390px wide, 0px overflow, readable without pinching (Law 12).

**Verbs (LAW of language, from the record):** Connect, never Follow. Message, Open, Save,
Create, Share, Invite, Join. One verb per button. Two verbs on one button is two buttons
pretending to be one.

## Part 5 — Anatomy of an icon (HUMAN + MACHINE)

HUMAN: an icon is a small white drawing — one clean stroke, one idea — sitting on
obsidian. You know what it means before you read anything. When you touch it, its backing
ignites in its own color. It never shouts in color at rest, and it never acts without a name.

MACHINE:
- **Grid:** one square grid, optically centered (the drawing sits visually centered, not
  mathematically — eyes, not rulers, judge centering). One stroke weight everywhere;
  mixed weights on one page read as different languages.
- **Lines:** white, always (Law 1). No spectrum color on icon lines at rest (Law 3).
- **Backing:** neutral at rest (obsidian/deep, white rim where the icon is a control).
  On touch: backing ignites in the icon's own color (Law 6).
- **Truth dot (Law 2):** where status matters, a dot rides with the icon — green proven,
  gold shown/live, blue stated — plus a word or shape saying the same thing (color never
  alone, Part 2).
- **Labels:** every actionable icon has an accessible name. Primary actions show a visible
  text label beside the icon (icon + verb is the franchise standard). Icon-only buttons
  are allowed only where the meaning is universal (home, search, plus, close) AND the
  accessible name exists; a primary action that is icon-only with no label is a guess
  imposed on the citizen. Decorative icons never act (Law 13: an icon that looks tappable
  and does nothing is a dead control).
- **Sizes:** icons scale with their text (Law 16: size separates). An icon bigger than its
  label shouts; an icon smaller than its label whispers. Both are defects.

## Part 6 — Anatomy of a board (HUMAN + MACHINE)

HUMAN: a board is a wide rectangle you enter — like a room. It has one color that is its
own (you recognize it by that color), white words, room to breathe, and depth you can feel:
it sits above the page, not painted on it. Inside it, things nest: boards within boards,
each a little deeper. Nothing flat. Nothing square-grid. Nothing crowded.

MACHINE:
- **Shape:** horizontal rectangle, one after another (Law 7). Not a grid of squares.
- **Identity:** one fixed spectrum color per board (Law 5): spine, accent rail, and corner
  jewel speak it. Kicker TEXT stays white (Law 1, Shawn's word) — the color lives on the
  chrome, never the words.
- **Depth:** three-layered elevation (Law 15): seating shadow + rim + edge light, plus
  nested boards-within-boards where depth is needed. Zero flat, proven in monochrome first.
- **Header:** kicker (white, source scale 24) → headline (white, 18) → detail (silver, 14).
  Size separates (Law 16); color never does.
- **Body:** exactly what is needed (restraint law: every element helps someone get the job
  done, or it comes off). Breathing room between elements; nothing crammed.
- **Footer:** the board's actions, if any — alive buttons (Part 4), verbs plain. A board
  with no action and no information is decoration; decoration comes off.
- **Empty state:** a designed honest state, never a hole. "Nothing here yet — here's what
  goes here, and the one verb that puts it here." Blank boards are unfinished boards.
- **Neighbors:** adjacent boards never share a hue or near-hue (Law 4). The page walks
  the spectrum in law order (Law 10).

## Part 7 — Anatomy of an input (HUMAN + MACHINE)

HUMAN: a field is a quiet rectangle with a white rim and a plain-words label above it
telling you what goes in. You tap it and its rim ignites in its own color. You can type it,
speak it, or ask your AI — three doors, always, nothing a wall. What you typed stays
readable, editable, and honest. An error tells you plainly what is wrong and how to fix it,
in words, not in color alone.

MACHINE:
- **Shape:** rectangle (Law 7 spirit), white rim at rest, own-color rim on focus
  (focus = touch equivalent, Law 6). Label ABOVE the field, white, always visible.
  Placeholder text is a hint, never the label — a label that vanishes when you type is
  a label that abandons you (SPEC).
- **Three doors (SPEC, extending the Welcome law):** every major input offers Speak it
  (voice, editable after) · Type it · Ask your AI. Skip always available where the input
  is optional; nothing is a wall. Voice is gated on ear proof — the spec does not claim
  voice works where the ear-gate has not passed.
- **Composer (franchise verbatim):** multi-line field + Dictate + Schedule + one send
  verb. The SAME composer everywhere — Dictate and Schedule on every sister (the Business
  gap, missing both, never again). A composer that quietly differs is a franchise piece
  broken.
- **Inline edit (citizen pages):** text becomes a field on tap, saves on blur/enter,
  reload proves it stuck (the Personal 13-section pattern). An edit that does not survive
  reload is not an edit.
- **Choice inputs:** chips, sliders, steppers, pickers — each obeys Laws 1, 6, 13
  (white text, white at rest / own color on touch, every control works).
- **Errors (SPEC):** plain-words error below the field ("That name is taken — try another"),
  red reserved for alert (Part 2), never color-alone, never a red field with no words.
- **Dates and times:** plain words ("Friday, October 23"), never bare codes, never
  U0001fXXX-style literal strings on the face (a rendering defect, never a design).

## Part 8 — Anatomy of graphs and charts (HUMAN + MACHINE)

HUMAN: a graph is a living picture of your numbers. You see the shape in 2 seconds, you
tap any part of it and it tells you the day, the number, and the thing behind it. It never
fakes a number, never hides an empty, never mixes two crowds into one picture. A chart is
the same honesty for categories: bars you can tap, a donut whose center is the true total,
a funnel that follows one crowd from start to finish.

MACHINE — shared by graphs and charts:
- **Data:** every plotted point comes from records (Smart Stats spec, Section 3). No
  typed numbers, no sample data, no simulated series. SAMPLE is forbidden.
- **Tap → detail:** every bar, dot, slice, and cell taps to its readout (day + number +
  the thing). A chart element that highlights and reveals nothing is a dead control.
- **Empty:** an honest empty frame with a one-line caption ("No activity in this range
  yet") — never a blank hole, never a faked curve, never a hidden empty.
- **Axes and labels:** labeled in plain words, white/silver text, size hierarchy (Law 16).
  No axis without a label. No legend that does nothing (an inert legend is a dead control).
- **Color:** spectrum walk (Law 4 + Law 10), color never alone (shape + value + word),
  truth-states per Law 2 (proven green, shown gold, stated blue — a projected value is
  STATED: dashed, labeled "projected," never solid like an actual).
- **Depth, not distortion:** depth comes from layering (edge light, seating shadow),
  never from distorting the data (no pseudo-3D pies, no stretched axes, no truncated bars
  that lie about proportion).
- **Graphs (time) vs charts (categories):** graphs show change over time (River, trend,
  bars-over-time, heat calendar, sparklines, forecast). Charts compare categories
  (bars, donut, funnel, heat grid, rings, constellation). Same tokens, same walk, same
  tap-to-detail, same honesty — one visual language, two jobs.

## Part 9 — Anatomy of the remaining elements (short form; same laws throughout)

**Smart Bars (direction-settled draft, NOT fully settled law):** the two-bar frame — top
bar is that app's own fixed organization, bottom bar is the editable whole network
(apps only, never features inside). The Smart Bar is never closable; the notifications
bar always stays. Details still owed (name, speeds, phone layout, precedence) — this spec
does not invent them. Anatomy: bar = obsidian strip, white rim where it meets content,
app icons/labels white at rest, active app ignites in its own color, counts only on the
notifications bar (never mail content — privacy law). A bar that hides the way home is
a defect.

**Briefing strips:** one line, three jobs: what + why + one verb. Kicker white, narrative
white/silver, action = one alive button, identity color on the spine/rail only. A strip
with two verbs is two strips pretending to be one. A strip with no verb is a poster.

**Smart Tabs:** topic tabs (Auto Organization law): manual link always wins, system tabs
come from clusters, every placement shows its percentage + reason. Anatomy: a row of
white-rimmed rectangles, active tab ignites in its own color, inactive tabs white at
rest (Law 6). Filter tabs carry ONE "All" control, never two. Nested tabs go one level
only, never deeper — deeper is confusion wearing organization.

**Toggles (Settings law):** every switch says plainly what it does, and no switch does
nothing. Anatomy: track (obsidian, white rim at rest) + thumb (white). ON ignites the
track/thumb in the switch's own color. ON/OFF is shown by position + a plain word, never
color alone. Master switches govern groups (in-system / email masters, then per-kind
toggles). Locked toggles show plainly why they are locked (paid gating: locked is honest,
never broken-looking). Install is an action, once, never a modal gate.

**Search (one search everywhere, tracker 67):** dark pill, white rim at rest, mic,
Go ignites on touch (any rest-state glow is non-standard, not the norm). Same look and
behavior on every page. As-you-type results re-form live, top block glows, title first,
then nutshell, then block content. Never private mail content. Never a second search
system. Voice search is gated on ear proof.

**Lists and rows:** rectangles one after another (Law 7). Row = face/icon + name (white)
+ detail (silver) + action (alive button or plain-words destination). Row tap goes
somewhere real (directory rows: card-click opens the real app, not a poster). Counts
reconcile: a header count equals its rows. Ranked rows show % + reason (Auto Organization).
Swipe actions are labeled (save / share / delete), never mystery gestures.

**Faces:** everyone known by an initial as a colored initial icon, full name in
mail/details (family model). Anatomy: white initial on an own-color backing, distinct
from neighboring faces (Law 4). Live = gold LED dot (Law 2: gold = live/shown).
Photo faces where the photo is real, white rim, same dot. Anonymous faces are silhouettes
— never a fake person, never a demo persona presented as real (demo is labeled demo).

**Pills and badges:** small rectangles with white rims (Law 7 spirit), white text.
Count pills show numbers. Status pills show word + dot (Live gold / Proven green /
Stated blue, Law 2). SOON pills are LABELS, never dead buttons — either they do nothing
visually (a label) or they tap to a plain-words "coming" note; a SOON pill that taps to
nothing is a dead control (Law 13) and a franchise inconsistency (one page's SOON must
mean what every page's SOON means). Locked pills show the plain-words reason. Verified
pills show check + "Verified" only where proof exists — a claim wearing a verified pill
is a lie wearing a badge.

## Part 10 — Top 10 concepts per element (world-class, then the Naya pick)

Each concept: name + essence. FIT tags: NATIVE (satisfies the laws as drawn) ·
ADAPT (good idea, needs Naya reshaping) · CLASH (breaks a law — shown so it is never
picked blind). The pick follows each list.

### BUTTONS
1. **Jewel button** — obsidian tile, white rim, own-color ignition, corner glint. NATIVE.
2. **Pill CTA** — full-width rounded pill, verb-first, high contrast. ADAPT (friendly, but
   rectangle language prefers corners; use sparingly, never as the base).
3. **Ghost button** — transparent base, white rim only, ignites on touch. NATIVE (secondary).
4. **Split button** — main verb + caret for options. ADAPT (powerful; complexity risk —
   options must be doors, not a mystery menu).
5. **Icon+verb button** — icon left, verb right, one action. NATIVE (franchise standard).
6. **FAB** — single round hero action, fixed corner. CLASH (breaks rectangles + restraint
   unless strictly one per view; never the base).
7. **Segmented control** — row of exclusive options, active ignites. ADAPT (choice, not
   action — a different job from a button).
8. **Press-and-hold button** — hold to confirm destructive/important actions. NATIVE
   (safety for irreversible verbs).
9. **Count button** — button showing its own live count ("Messages 3"). NATIVE (data +
   action fused; count must come from records).
10. **Voice button** — mic button, waveform while listening. ADAPT (voice door; gated on
    ear proof).

**PICK — Jewel button as the base, ghost as secondary, icon+verb as the standard form.**
Why: the only concept satisfying Laws 1, 3, 5, 6, 8, 9, 15 simultaneously. Everything else
either breaks a law at rest (FAB, colored pills), serves a narrower job (split, hold,
count, voice as variants), or is a choice control, not a button. Toolbox: CSS layers +
verbatim tokens, no new tech. Blessed as three imports: primary jewel, ghost secondary,
icon+verb form.

### BOARDS
1. **Jewel board** — rectangle, one identity color (spine+rail+jewel), three-layer depth,
   white text. NATIVE.
2. **Glass board** — translucent layers, blur, depth via translucency. CLASH (readability
   + phone performance + obsidian law; pretty, not Naya).
3. **Tiered board** — boards within boards, nested depth. NATIVE (Law 15 machine form).
4. **River board** — full-width flowing panel, time-ordered. NATIVE (feed/River).
5. **Stat board** — number-first board, gauge + narrative. NATIVE (Dashboard).
6. **Action board** — board ending in one verb. NATIVE (no board without a why).
7. **Expandable board** — glance → tap → full depth. NATIVE (glance→focus→explore).
8. **Comparison board** — side-by-side, same grammar, differences lit. NATIVE (compare).
9. **Empty-honest board** — honest empty state as a designed state. NATIVE (honesty law).
10. **Preview board** — big preview before pick. NATIVE (Law 11).

**PICK — Jewel board + tiered depth as the base; expandable as the behavior;
empty-honest and preview as mandatory states.** Why: Laws 5, 7, 11, 15 all point here.
Glass is the only true clash (it trades readability for prettiness). Toolbox: CSS layers
+ tokens, no new tech.

### ICONS
1. **Jewel icon** — white line icon, neutral backing, own-color ignition on touch. NATIVE.
2. **Line icon** — pure white stroke, no fill, one weight everywhere. NATIVE (needs weight
   discipline — mixed weights read as different languages).
3. **Filled icon** — solid white shape, high visibility at small sizes. NATIVE (small sizes).
4. **LED icon** — icon + truth dot (green proven / gold shown / blue stated). NATIVE
   (status fused, word/shape alongside, never color alone).
5. **Initial icon** — letter as identity. NATIVE (family model, faces).
6. **Glyph icon** — symbol-only, universal meanings. ADAPT (ambiguity risk — needs labels
   on anything but the most universal meanings).
7. **Animated icon** — motion on touch, once (morph, settle). NATIVE (alive; looping
   motion is a flood and banned).
8. **Stacked icon** — badge count fused onto icon. NATIVE (counts at a glance, from
   records).
9. **Spectrum icon** — backing in own color at rest. CLASH (colored at rest breaks Law 6;
   backing ignites on touch, never rests lit).
10. **Voice icon** — waveform/mic, listening state visible. ADAPT (gated on ear proof).

**PICK — Jewel icon: one line weight, white lines, neutral backing at rest, own-color
ignition on touch, LED dot where status matters, visible label on primary actions.**
Why: Laws 1, 2, 3, 6 in one object. Toolbox: SVG, no new tech.

### INPUTS
1. **Jewel field** — rectangle, white rim, own-color rim on focus, label above, hint below.
   NATIVE.
2. **Pill field** — rounded search-style field. ADAPT (search only, never forms).
3. **Three-door field** — Speak it / Type it / Ask AI doors on the field. NATIVE as SPEC
   (extends the Welcome law; voice gated on ear proof).
4. **Composer** — multi-line + Dictate + Schedule + one send verb. NATIVE (franchise
   verbatim; same on every sister).
5. **Inline-edit field** — text becomes a field on tap, saves on blur/enter, reload proves
   it stuck. NATIVE (citizen-page pattern).
6. **Slider input** — drag a value, number shown live. NATIVE (numbers, ranges).
7. **Stepper input** — minus / number / plus, precise. NATIVE (counts, quantities).
8. **Choice chips** — tap-to-pick options, active ignites. NATIVE (single/multi choice).
9. **Date/time picker** — calendar + clock, plain words ("Friday, October 23"). NATIVE
   (Booking; never bare codes).
10. **Voice-first field** — mic primary, transcript editable after. ADAPT (Speak it, edit
    after — Welcome law; gated on ear proof).

**PICK — Jewel field as the base; composer as the message/note form; three-door as the
door pattern; inline-edit for citizen pages.** Why: Laws 1, 6, 13 + Welcome doors +
franchise composer, all codable now (HTML inputs + CSS + JS; voice gated, not claimed).

### GRAPHS (time)
1. **River stream** — flowing area over time, scrubable, hover readout. NATIVE (Top 25 #4).
2. **Trend line** — single line, dots at events, tap dot → event. NATIVE.
3. **Multi-line** — several series, spectrum walk, tap legend → isolate. NATIVE (legend
   must act — an inert legend is a dead control).
4. **Area + baseline** — filled area over a target/pace baseline. NATIVE (pace vs actual).
5. **Bar-over-time** — bars per day/week, tap bar → day readout. NATIVE (Smart Links).
6. **Heat calendar** — grid of days, intensity = value, tap day → detail. NATIVE.
7. **Sparkline** — tiny word-sized trend inside text/rows. NATIVE (glance level).
8. **Gauge-over-time** — momentum dial with history arc. ADAPT (beautiful; needs a real
   history, never a drawn arc from nothing).
9. **Forecast line** — solid actual + dashed projected pace. NATIVE (projection dashed
   and labeled, never solid like an actual — honesty).
10. **Event river** — timeline of events as a flowing lane. NATIVE (Journal).

**PICK — River stream as the hero time graph; bar-over-time for daily counts;
sparkline for glance; forecast as dashed projection.** Why: Top 25 + Living Data +
fine-tune lessons (trend must render, bars must read out, projections must look
projected). Toolbox: Canvas/SVG + JS, no new tech.

### CHARTS (categories)
1. **Jewel bars** — vertical bars, spectrum walk, tap → readout. NATIVE (Smart Links).
2. **Donut** — true totals, live legend, center = total. NATIVE (true or renamed — the
   fine-tune fix).
3. **Funnel** — one population, recorded → clicked → joined, labeled. NATIVE (lie-proof).
4. **Heat grid** — 2D grid (day × kind), intensity + value on tap. NATIVE (tap → detail,
   not highlight alone).
5. **Radial rings** — rings per category, capacity rings (Meet 6/10). NATIVE (capacity).
6. **Constellation** — nodes + links, proximity = match %. NATIVE (Match orbiting bodies).
7. **Tree/cluster** — groups + sub-groups, tap → drill. NATIVE (organization).
8. **Comparison bars** — paired bars, same scale, difference labeled. NATIVE (compare).
9. **Progress rings** — ring per goal, % + days-left. NATIVE (goals).
10. **Ledger bars** — money in/out as a river of bars, Wednesday payout markers. NATIVE
    (money; payout markers only where payout wiring is proven, never promised).

**PICK — Jewel bars + donut (true totals) + funnel (one population) + heat grid as the
core four; constellation for Match; rings for capacity and goals.** Why: the five chart
tests + fine-tune fixes, all in one language. Toolbox: SVG/Canvas + JS, no new tech.

### BARS (Smart Bars)
1. **Two-bar frame** — top app bar + bottom network bar. NATIVE (direction-settled shape).
2. **One-bar** — single bar, everything in it. CLASH (loses the app/network split the
   franchise needs).
3. **Rail bar** — left vertical rail, icons + labels. CLASH as primary (phone fails;
   desktop secondary at most).
4. **Floating bar** — bar floats above content, translucent. CLASH (readability + touch
   risks; obsidian law prefers grounded strips).
5. **Auto-hide bar** — hides on scroll, returns on scroll-up. CLASH for the Smart Bar
   (never closable; hiding is closing with better manners).
6. **Section bar** — bar changes per section, same frame. NATIVE (the top bar's job).
7. **Context bar** — actions for the current selection. NATIVE as a section behavior,
   not a third bar.
8. **Notification bar** — always visible, counts only. NATIVE (law: always stays; counts
   only, never mail content).
9. **Breadcrumb bar** — where you are + path back, plain words. NATIVE (wayfinding).
10. **Command bar** — tap → command palette (search + actions). ADAPT (power users;
    complements the one search, never replaces it).

**PICK — Two-bar frame + notification counts bar + context actions inside sections
(not a third bar).** Why: the settled direction + never-closable + notifications-always
+ bottom-apps-only laws. Speeds, directions, and phone layout remain OWED (draft, not
law) — this spec does not invent them. Toolbox: CSS/JS now.

### STRIPS
1. **Briefing strip** — one line: what + why + one verb. NATIVE (the blessed strip).
2. **Narrator strip** — "Naya reads it back," computed narrative. NATIVE (Living Data).
3. **Alert strip** — plain-words alert, one action, dismissible. NATIVE.
4. **Progress strip** — where you are in a walk, steps + next. NATIVE (walks).
5. **Promo strip** — one offer, one verb, honest, never fake urgency. ADAPT (offers;
   fake urgency is banned — a countdown that lies is a lie).
6. **Ticker strip** — slowly scrolling network pulse, counts only. NATIVE (collective
   pulse, counts-only).
7. **Context strip** — what this page is + what to do here, one line. NATIVE (orientation).
8. **Warning strip** — a blocker stated + the exact unblocker. NATIVE (blockers with proof).
9. **Celebration strip** — a win, stated once, then gone. NATIVE (wins; restraint — never
   looping, never permanent noise).
10. **Empty strip** — the honest placeholder that teaches. NATIVE (empty states).

**PICK — Briefing strip as the blessed one (narrator + one verb); progress strip for
walks; alert and warning as states.** Why: Top 25 (reasoning narrative, proactive
surfacing) + honesty laws. Toolbox: CSS now.

### TABS
1. **Smart Tabs** — topic tabs, manual wins, system tabs from clusters, % + reason.
   NATIVE (Auto Organization law).
2. **Pill tabs** — rounded tab row, active ignites. ADAPT (friendly; rectangle language
   prefers corners — use sparingly).
3. **Underline tabs** — text tabs, active = underline + size. NATIVE (Law 16: size
   separates, color never does).
4. **Segmented tabs** — control-style, one active. NATIVE (choice).
5. **Scroll tabs** — row scrolls slowly, tap pulls into section. NATIVE (many tabs;
   the top-bar pattern).
6. **Icon tabs** — icon + label tabs. NATIVE (app navigation; label always with icon).
7. **Vertical tabs** — side list of sections. ADAPT (desktop docs; phone secondary).
8. **Step tabs** — numbered journey steps, done / current / next states. NATIVE (walks).
9. **Filter tabs** — tabs as filters, ONE "All" control. NATIVE (feeds; "All" twice is
   the defect, never again).
10. **Nested tabs** — tabs within tabs, one level only. ADAPT (one level max — deeper is
    confusion wearing organization).

**PICK — Smart Tabs (topic, manual wins, % + reason) in rectangle/underline form
(active ignites own color, inactive white at rest); step tabs for walks; filter tabs
with a single All.** Why: Auto Organization law + Laws 1, 6, 16. Toolbox: CSS/JS now.

### TOGGLES
1. **Jewel switch** — track + thumb, white at rest, own-color ignition ON. NATIVE.
2. **Checkbox jewel** — square check, own-color check when on. NATIVE (multi-select).
3. **Radio jewel** — circle, own-color dot when selected. NATIVE (single-select).
4. **Master switch** — one switch governing a group (in-system / email masters, then
   per-kind toggles). NATIVE (Settings notification design).
5. **Slider toggle** — drag on/off, position + label. NATIVE (touch-friendly).
6. **Push toggle** — button that toggles + stays lit when on. NATIVE (action + state
   fused; lit state must mean ON, plainly).
7. **Segmented on/off** — two labeled halves, On / Off words, never color-alone. NATIVE
   (clarity).
8. **Timed toggle** — on until a time, then off, time shown. NATIVE (temporary states).
9. **Locked toggle** — shows plainly why it is locked, never broken-looking. NATIVE
   (paid gating honesty: locked is honest, broken is a lie).
10. **Install toggle** — install as action, once, never modal gate. NATIVE (Settings law).

**PICK — Jewel switch as the base (position + plain-words label + ON/OFF word, never
color-alone); master switches for groups; locked toggle with plain-words reason.**
Why: Settings law (every switch says plainly what it does, no switch that does nothing)
+ Laws 1, 6 + paid-gating honesty. Toolbox: CSS/JS now.

### SEARCH
1. **One search pill** — dark pill, white rim, mic, Go ignites on touch. NATIVE.
2. **Search + filters** — pill + WHEN/WHAT/WHERE chips below. NATIVE (chart-system
   filters).
3. **Search as you type** — results re-form live, top block glows. NATIVE (Search brief).
4. **Voice search** — mic primary, transcript editable. ADAPT (gated on ear proof).
5. **Search + tabs** — results organized by Smart Tabs. NATIVE (Auto Organization).
6. **Search drawer** — slide-over panel, full results, filters. NATIVE (mobile
   slide-over, Law 12).
7. **Search history** — recent searches, one tap to re-run, deletable. NATIVE.
8. **Search suggestions** — suggestions as you type, each a door. NATIVE (doors, not
   posters — a suggestion that goes nowhere is a dead control).
9. **Search everywhere** — same search on every page, same look/behavior. NATIVE
   (tracker 67 law).
10. **Search + narrator** — "here's what I found and what it means" above results.
    NATIVE (narrator).

**PICK — One search pill as the base + as-you-type re-forming + WHEN/WHAT/WHERE
filters + everywhere-same.** Why: tracker 67 + Search brief + Laws 1, 6, 13.
Toolbox: JS/CSS now; voice gated, not claimed.

### LISTS AND ROWS
1. **Rectangle rows** — one after another, face + name + detail + action. NATIVE (Law 7).
2. **Card rows** — each row a mini-board with depth. ADAPT (richer; heavier — use
   sparingly, never for long lists).
3. **Ranked rows** — rows ordered by score/match %, % shown + reason. NATIVE
   (personal ranking, not a public leaderboard).
4. **Timeline rows** — rows on a time spine, newest first. NATIVE (Journal/feed).
5. **Grouped rows** — rows under topic headers (tabs). NATIVE (organization).
6. **Action rows** — row tap = action, verb visible. NATIVE (no mystery taps).
7. **Swipe rows** — swipe for labeled actions (save / share / delete). NATIVE (mobile
   gestures, Law 12; actions labeled, never mystery).
8. **Expandable rows** — tap row → detail opens inline. NATIVE (glance→focus).
9. **Empty rows** — honest empty row that teaches what goes here. NATIVE (empty states).
10. **Directory rows** — card-click opens the real app. NATIVE (Space proof: card-click
    → real /space confirmed; directories open things, not posters).

**PICK — Rectangle rows as the base; ranked (with % + reason); expandable;
directory-click behavior.** Why: Law 7 + Auto Organization + Space proof.
Toolbox: CSS/JS now.

### FACES
1. **Initial jewel** — white initial on own-color backing, distinct from neighbors.
   NATIVE (family model).
2. **Photo face** — real photo, white rim, live gold dot. NATIVE (real people).
3. **Presence face** — face + presence (gold live / quiet away). NATIVE.
4. **Stack face** — overlapping faces = group, count shown. NATIVE (groups; count from
   records).
5. **Faceless** — no face, just name + role. NATIVE (privacy-respecting default).
6. **Naya face** — Naya's own face/mark, consistent everywhere. NATIVE (one living mind).
7. **Status face** — face + status word ("Building", "Away", "Live"). NATIVE (words,
   never color-alone).
8. **Mini face** — small face in rows/lists, name beside. NATIVE (lists).
9. **Hero face** — large face on profile, cover + motto. NATIVE (Personal page).
10. **Anonymous face** — silhouette for anonymous/unknown. NATIVE (honesty: never a fake
    person, never a demo persona presented as real).

**PICK — Initial jewel as the base; photo where real; gold live dot; status word.**
Why: family model + Laws 1, 2, 4 + demo honesty. Toolbox: CSS now.

### PILLS AND BADGES
1. **Count pill** — number, white text, own-color spine (not a full color flood). NATIVE.
2. **SOON pill** — label only, never a dead button (or taps to a plain-words "coming"
   note). NATIVE (franchise consistency: one page's SOON means what every page's means).
3. **Status pill** — word + dot (Live gold / Proven green / Stated blue). NATIVE (Law 2).
4. **Category pill** — topic label, taps to its tab. NATIVE (organization).
5. **New pill** — "New" marker, once, then gone. NATIVE (freshness; restraint — never
   permanent noise).
6. **Locked pill** — "Locked" with plain-words reason, never broken-looking. NATIVE
   (paid honesty).
7. **Verified pill** — check + "Verified" word, proven only. NATIVE (proof, never claimed).
8. **Member pill** — tier/level word ("Loved", level number). NATIVE (levels, personal).
9. **Alert pill** — count of alerts, taps to alerts. NATIVE (notifications, counts only).
10. **Action pill** — small verb pill (Message, Connect, Open, Save). NATIVE (small actions;
    verbs per Part 4 — Connect, never Follow).

**PICK — Count pill + status pill (truth-states) + SOON-as-label + locked-with-reason.**
Why: Laws 1, 2, 6, 13 + honesty. Toolbox: CSS now.

## Part 11 — The blessed inventory (pre-made, pre-done, no more guessing)

Build order — each blessed part is an IMPORT, never a copy. A builder pulls it in whole
or does not use it. No near-copies, no "inspired by" rewrites (Law 14 + franchise law).

1. Primary jewel button · 2. Ghost secondary button · 3. Icon+verb button ·
4. Jewel board (tiered depth) · 5. Briefing strip · 6. Jewel field · 7. Composer
(Dictate + Schedule) · 8. Jewel switch · 9. Search pill · 10. Rectangle row ·
11. Initial face · 12. Count pill + status pill · 13. Gauge · 14. River graph ·
15. Jewel bars chart · 16. Donut (true totals) · 17. Funnel (one population) ·
18. Heat grid · 19. Two-bar frame · 20. Smart Tab row.

**How a part earns blessing (SPEC, from the gate + harvest laws):** machine floor pass
(no private hex, no colored button at rest, no flat surface, no dead control) +
Same-Language Check pass + Nitro rendered review (desktop + phone, real address) +
evidence (screenshots, measurements) + harvest into the Factory inventory with its source
path. A part without evidence is not blessed, however beautiful. A blessed part that
regresses (a later build breaks it) loses blessing until it passes again — the floor only
ever rises.

**Toolbox, honestly stated (what we can code now):** HTML + CSS (layers, gradients,
shadows, borders, transitions) + SVG (icons, gauges, bars, donuts, rings) + Canvas
(River, heat, stream) + JS (scrub, tap-to-detail, filters, drawers). NOT in the toolbox
today: WebGL 3D scenes, true physics, sound design (ear-gated), device haptics. Every
pick above is codable with the stated toolbox — no pick depends on what we cannot do.
Glass boards, floating bars, and rail bars were marked CLASH partly because they spend
beyond the toolbox or beyond the laws for prettiness.

## Part 12 — What we do and what we don't do (the whole spec, one glance)

DO: white text on obsidian, always · one color per board, adjacent never sharing a hue ·
white at rest, own color ignites on touch · depth before color, zero flat · rectangles,
one after another · every control works or it doesn't ship · compose, never create ·
preview before pick · mobile is the app · size separates, color never does · green
proven, gold shown, blue stated · restraint, rainbow knows its place · verbatim tokens ·
evidence ships with the build · counts reconcile · tap any number to its records ·
honest empties, honest "not tracked yet," honest "not counted yet" · SOON as a label ·
locked as honest, never broken · demo labeled demo · color never alone (shape + word) ·
one search everywhere · one verbatim composer · one top bar, one search, one language.

DON'T: colored text of any kind · colored buttons at rest · private or "close enough"
hexes · flat surfaces · dead controls (buttons, toggles, forms, previews, legends,
suggestions that go nowhere) · square grids for lists · color floods · decorative gold ·
claims that look like proofs · icon-only primary actions with no label ·
placeholder-as-label · faked or sample data · mixed-population funnels · duplicate All
controls · demo personas presented as real · SOON as a dead button · locked looking
broken · looping motion · color-alone meaning · a second search system · a second gate ·
a near-copy of a blessed part · a page that breaks its own laws while selling them.
