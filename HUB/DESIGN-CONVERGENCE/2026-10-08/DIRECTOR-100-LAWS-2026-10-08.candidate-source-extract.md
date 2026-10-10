# Director's 100 Laws of Elite Smart App Interfaces — PDF source text (CANDIDATE extraction)

> **Provenance:** User-supplied `naya-100-laws-elite-interfaces.pdf` dated 2026-10-08. This text is extracted from that PDF and is supplied to cold-Naya reviewers as SOURCE MATERIAL; the original PDF is authoritative for visual/text fidelity.
>
> **Governance:** The source calls itself "Canonical Standard Locked" but its closing line says human ratification is Shawn's word. This addition is placed only on the existing **DRAFT PR #1912** branch; it does not overwrite ratified `BRAIN/10-INTERFACES/NAYA-DESIGN-CONTRACT-V1.md` or `HUB/DESIGN-CONTRACT.md`. `CANDIDATE_SOURCE_PRESERVED` is NOT `RATIFIED` nor `CI_ENFORCED`.
>
> **Verification:** Programmatic full-file extraction contained 100 uniquely numbered laws 1–100, across ten sections. PDF text reflow may retain original line wraps; do not silently "correct" the underlying law. Conflicts and open authority decisions are in `DIRECTOR-100-LAWS-RECONCILIATION.candidate.md`.

---

<PARSED TEXT FOR PAGE: 1 / 11>
The 100 Laws of Elite Smart App Interfaces
NayaNET / NayaPOWER — Canonical Standard Locked in place for every Smart App, every Hub
page, every board, button, icon, and element.

  Prime directive: Premium, not fancy. Living depth, always. Zero flat.

This is the Lego library law. If an element exists in NayaNET, it has a block here. If it has no block,
we build the block before we build the app. Any Naya, any seat, any cold successor must be able
to pick up this document and build an elite interface without re-asking Shawn the same
questions.




How to use this document

    Before building: Read Laws 1–20. They are non-negotiable.
    While building: Use only canonical blocks. One button system, one board system, one icon
    family.
    Before shipping: Run the Acceptance Checklist at the end. Screenshot at desktop, tablet, and
    phone. Score honestly. Below 9.0 does not ship to Shawn.
    When Shawn corrects: The correction becomes a new law or sharpens an old one — same
    day, in this file.




I. Elevation & Living Depth — Laws 1–10

Law 1 — Elevation always. Every button, every board, every card, all the time. If it does not sit off
the page, it is not finished. Flat is a defect, not a style.

Law 2 — No 2D in NayaNET. There is no flat plane. Every interactive surface has at least three
layers: base surface, edge light, seating shadow. Non-interactive surfaces have at least two.

Law 3 — Living depth. Depth is not a static shadow. On hover, focus, or approach, the element
lifts, its edge catches light, and its shadow deepens. The element feels alive — we call this Active
Intelligence.

Law 4 — Shadow is weight. A heavier shadow means a more important element. Primary actions
cast the deepest shadow; tertiary elements cast the lightest. Shadow hierarchy = action hierarchy.

Law 5 — The page is a physical space. Elements exist on the page, not in it. A board overlapping
another board must resolve with elevation, not z-index tricks. If it looks pasted on, rebuild it.
<PARSED TEXT FOR PAGE: 2 / 11>
Law 6 — Depth before color. Establish the elevation system in black and white first. If it does not
read as premium in monochrome, color will not save it.

Law 7 — Seating shadow, never drop shadow. Use a soft, offset, dark seating shadow that
grounds the element. Never a uniform blur halo — that reads as glow, not weight.

Law 8 — Edge light is a hairline. The top edge catches a 1px highlight at 12–20% white. The
sides fade. The bottom edge is shadow. This is how real objects catch light.

Law 9 — Inner depth counts. Recessed wells (inputs, code blocks, media players) are carved into
the page with inner shadow. Raised and recessed are the only two directions. Nothing is level with
the page.

Law 10 — If it doesn't move, it's dead. Every board and button responds to pointer proximity.
No response = no good. Ship the hover state with the element, not after it.




II. Premium Material & Contrast — Laws 11–20

Law 11 — Premium, not fancy. Fancy is effects. Premium is material, contrast, weight, and
restraint. When in doubt, subtract. A button that whispers is more expensive than one that
shouts.

Law 12 — Deep black is the base. Default surface: rich obsidian (#0a0a0f to #12121a range). Not
gray, not navy, not purple-tinted. Black is the canvas; color is the jewel set into it.

Law 13 — Contrast is a law, not a preference. Body text on its surface must pass WCAG AA at
minimum, AAA preferred. If you have to squint, it fails. Red on red, purple on purple, gold on
yellow — automatic rejection.

Law 14 — Glow lives on the border, not in the air. Accent glow is a tight border light-up: 0–4px
spread, high precision. Outward bloom beyond 8px reads as cheap neon. The board lights up; it
does not radiate.

Law 15 — White glow requires blacker black. If a white or silver glow is used, the surface
beneath must be deepened first. Glow on mid-gray washes out. Contrast first, glow second.

Law 16 — Luxury is restraint. One accent per element. One jewel per board. The moment
everything glows, nothing is premium. Empty black space is a design material.

Law 17 — Text is printed, not rendered. Type must look like it was set by a master printer: crisp
antialiasing, intentional weight, no text-shadow blur. If text looks like a screenshot of text, the
weight or size is wrong.

Law 18 — Materials have names. We use: Obsidian (base), Frosted Obsidian (translucent
panels), Jewel (accent surfaces), Paper White (text), Silver (secondary text). Inventing a new
<PARSED TEXT FOR PAGE: 3 / 11>
material per page is forbidden.

Law 19 — The most expensive element test. Look at the page. Every element should be a
candidate for "most expensive thing here." If one element visibly cheapens the page, it is the
page's quality ceiling. Fix it or remove it.

Law 20 — Subtract before adding. "10x better" means better human experience, not more
effects (SN-0733). Before adding a gradient, animation, or glow, ask: does removing something
make this more premium? Usually yes.




III. Buttons — The Jewel Standard — Laws 21–30

Law 21 — One canonical button. .naya-btn is the only button system. All variants derive from
it. A second button implementation on the same page is a consistency violation, not a creative
choice.

Law 22 — The three front-door buttons set the bar. The first three actions a user sees are the
flagship component. They must be the most polished controls in the product. If a Smart Tab
button looks more professional than the hero button, the hero button fails.

Law 23 — Black body, jewel accent. Buttons are deep black with a jewel-toned accent: hairline
border, kicker text, icon, or edge light. Never a full-color fill for body text or large surfaces. Color is
the setting, not the stone.

Law 24 — Five mandatory states. Rest, Hover, Press, Focus, Disabled — plus Loading and
Success where the action is async. Missing a state means the button is unfinished. Press
compresses 1–2px; hover lifts 2–4px.

Law 25 — A circle flows around it. Icon buttons and primary CTAs may carry a rotating or
flowing ring accent on hover — a thin jewel line that travels the perimeter. It signals life without
bloom. Keep it under 2px and under 40% opacity.

Law 26 — Delete is dark, not glowing red. Destructive actions use deep black with a
desaturated red accent (border, icon, or text at rest). Glowing red hover is forbidden — it reads as
alarm, not elegance. Confirmation does the safety work, not the glow.

Law 27 — Labels are verbs, one line. "Create", "Publish", "Connect", "Save". sentence case, no
period, no exclamation. A label that wraps to two lines means the copy or the button width is
wrong.

Law 28 — Minimum touch target 44×44px. Every button, everywhere, no exceptions (mobile-
first law). Visual size may be smaller only if the hit area is not. Desktop density never overrides
touch law.
<PARSED TEXT FOR PAGE: 4 / 11>
Law 29 — Buttons in a row are a family. Same height, same radius, same depth system. The
primary is elevated highest; secondaries sit one step lower. A row of mismatched buttons reads as
three different products.

Law 30 — Never re-teach the button. When Shawn approves a button, that exact code becomes
the block (SN-0735: take the actual code). Rebuilding it "from memory" next time is how flat
buttons come back. Copy the block verbatim, then vary only the variant class.




IV. Boards, Cards & Panels — Laws 31–40

Law 31 — The board recipe. Dark obsidian body, theme-tinted hairline edge, rich radial wash
confined to the cover/header zone, white title, silver body text, jewel kicker. This recipe is not
optional decoration — it is the board.

Law 32 — The outer board is alive too. Hovering a board lights its border and lifts the whole
board, not just inner elements. A dead outer board with live buttons inside is a half-finished
board.

Law 33 — Black board, colored border. Boards are black first. The spectrum color lives in the
border, the kicker, the badge, and the hover edge-light — never as a full purple/red/green wash
over the whole surface.

Law 34 — Glow stays in the frame. Board glow = border illumination only. Light does not spill
more than 6px outside the frame. Spill washes out neighboring boards and destroys the "jewels
on black velvet" effect.

Law 35 — Elevation hierarchy on the page. Page background (deepest) → section panels (+1) →
boards (+2) → featured board (+3) → modal (+4). Never more than five levels visible at once. If
everything is elevated equally, nothing is.

Law 36 — "In a nutshell / How to use it" panels are boards too. Explanatory panels, spec
panels, and help blocks get the same elevation, border, and hover life as content boards. Flat
instructional text on the page background is forbidden.

Law 37 — Headline / Body / Detail are a system. Every board carries three type levels: headline
(white, largest), body (silver, readable), detail (muted, smallest but never below 12px). Skipping
the body level collapses comprehension.

Law 38 — Boards breathe. Minimum 16px internal padding, 20–24px preferred. Content
touching the border is a layout bug. Crowded boards read as cheap regardless of color.

Law 39 — Adjacent boards never share a color. Spectrum is assigned by position in the flow
(see Section V), not by category. Two same-color boards side by side is a Spectrum Law violation.
<PARSED TEXT FOR PAGE: 5 / 11>
Law 40 — The green/gold/pink test. Claimed/demonstrated state cards (green = verified, gold =
premium, pink/magenta = featured) are the reference implementation. If a new board type does
not feel like it belongs in that set, it is not done.




V. Color, Spectrum & Jewels — Laws 41–50

Law 41 — Spectrum by position. Purple → indigo → sapphire → teal → emerald → lime →
yellow → gold → orange → rich orange → red → magenta → repeat. Assign in reading order.
Theming by category clumps color and is a serious violation.

Law 42 — Jewel colors are for jewels, never text fills. Lime body text, gold paragraphs, red
labels on red — forbidden. Jewels live in: hairline borders, number badges, checkmarks, kickers,
icons, edge lights. Small, glowing, precious.

Law 43 — LAW ZERO: Readability Supremacy. No glow, gradient, accent, or depth effect may
ever make anything harder to read. If an effect and readability conflict, the effect dies. Generous
text by default.

Law 44 — Black with accents beats all-color. A black board with a teal edge is more premium
than a teal board. Default to black; spend color like money.

Law 45 — One spectrum step per board. A board owns one spectrum position. Its jewel accent,
kicker, and hover light all derive from that single hue (plus white/silver neutrals). Rainbow boards
are for the Smart Feed spine only.

Law 46 — Red is a jewel, not a surface. Red appears as: delete accent, error indicator,
notification badge, the spectrum's red step border. A red-filled board or red-on-red button (faded
numeral on red) fails contrast and fails Law 13.

Law 47 — Gold means precious, use sparingly. Gold/yellow is restrained: premium badges,
verified marks, the gold spectrum step. Never body text, never large fills. Gold everywhere is not
luxury; it is a casino.

Law 48 — Neutrals do the heavy lifting. White (titles, primary text), silver (body), slate (detail),
obsidian (surfaces). If a page is more than ~20% saturated color by area, rebalance toward black
and neutrals.

Law 49 — Dark mode is the mode. NayaNET is designed dark-first. Light surfaces, where
needed, must be designed as their own premium material — never an inverted afterthought.

Law 50 — Color survives the screenshot test. Take a screenshot, convert to grayscale.
Hierarchy, elevation, and readability must survive. If the page only works in color, the depth
system is fake.
<PARSED TEXT FOR PAGE: 6 / 11>
VI. Typography & Readability — Laws 51–60

Law 51 — White titles, silver body, always. Titles in white, body in silver, detail in muted slate.
No exceptions for "creative" color text. Jewel color in a kicker (small, uppercase, tracked) is the
only colored text allowed.

Law 52 — Type scale is fixed. Display 32–40 / Headline 22–28 / Body 15–17 / Detail 12–13 / Kicker
11 uppercase. Inventing sizes per page fragments the system. Line-height 1.45–1.6 for body.

Law 53 — Readability outranks density. If fitting more content means smaller text or tighter
leading, fit less content. A board that breathes beats a board that crams.

Law 54 — Serif for voice, sans for system. Display headlines and the Naya voice may use the
premium serif. UI labels, buttons, data, and body use the system sans. Never set body copy in
display serif.

Law 55 — Numbers are designed. Badges, counts, and stats use tabular numerals, optically
centered in their jewel badge. A faded number on a same-color button (red 6 on red) is invisible
and forbidden — contrast or remove.

Law 56 — Truncation is a design decision. Ellipsize with intent, provide the full text on
tap/hover, never let text overflow its board or push layout sideways. Overflow on mobile is a P0
bug.

Law 57 — Grandma standard. A non-technical reader must follow every board: what is this, what
matters, what do I do next? If they cannot, the copy or hierarchy fails — not the reader (Ten-Star
Service law).

Law 58 — No text on busy backgrounds. Text sits on solid obsidian or a controlled scrim. Text
over gradients, images, or glows without a scrim fails Law 43.

Law 59 — Weight creates hierarchy before size does. Bold white headline > regular white >
silver > slate. Reach for weight and color-value contrast before making type bigger.

Law 60 — Every label earns its place. If deleting a label costs the reader no action and no
interpretation, delete it. Decorative text is noise wearing a uniform.




VII. Icons & Micro-Elements — The Full Library — Laws 61–70

Law 61 — One icon family. Consistent stroke weight, corner treatment, optical size. Mixing icon
sets is mixing languages. Drawn at size, never shrunk from a large illustration.

Law 62 — The library is complete before apps begin. Required blocks, each with
rest/hover/active/disabled states: Like (heart), Share, Plus/Add, Play, Pause, Search, Bell/Notify,
<PARSED TEXT FOR PAGE: 7 / 11>
Bookmark/Save, Comment, More (•••), Close, Back, Check/Verified, Star/Premium, Send,
Download, External Link, Settings, Profile, Lock/Private, Globe/Public.

Law 63 — Icon buttons are circles with life. Circular hit area, black surface, jewel icon, border
light-up and lift on hover. The circle may carry the flowing ring (Law 25). A bare glyph with no
surface is not a NayaNET icon button.

Law 64 — Like is a jewel, not a emoji. Like/heart fills with its spectrum jewel on activation, with a
micro-scale pulse. Share uses the connected-nodes glyph. Plus sits in an elevated circle — it is the
most-tapped element in creation flows and must feel premium.

Law 65 — Play is a portal. Media play buttons are elevated circles with a white triangle, black
field, jewel ring. On hover the ring lights; on press it compresses. PowerCast and all media inherit
this block — no custom play buttons per page.

Law 66 — Badges sit on black. Notification counts, status dots, and verified marks sit on an
obsidian chip with a jewel numeral/symbol. Never a colored disc with a same-color numeral.

Law 67 — Icons have text names. Every icon-only control carries an accessible label and, where
space allows, a visible micro-label. Mystery-meat navigation is forbidden.

Law 68 — State is visible at a glance. Liked/not, saved/not, following/not, live/not — each state
is distinguishable by fill, weight, and jewel presence, not by color alone (colorblind-safe pairing).

Law 69 — Micro-elements get macro care. Toggles, checkboxes, radio pills, sliders, and
segmented controls use the same elevation, edge-light, and press physics as primary buttons. A
default browser control in a NayaNET app is a leak in the system.

Law 70 — Avatars are jewels too. Profile images sit in a ringed, elevated circular frame with a
spectrum or status edge. A square naked <img> is not a profile element.




VIII. Motion & Living Intelligence — Laws 71–80

Law 71 — Everything alive responds in under 100ms. Hover, press, and focus feedback begins
instantly. A press that registers late feels broken even if the action succeeds.

Law 72 — The signature ease. .22s cubic-bezier(.16,.84,.22,1) for lifts and lights. Snappy in,
gentle settle. Different easing per page fragments the feel of the product.

Law 73 — Press is compression. On press, the element settles 1–2px toward the page and its
shadow tightens. Release springs it back. This single behavior sells physicality more than any
gradient.
<PARSED TEXT FOR PAGE: 8 / 11>
Law 74 — Light travels, it doesn't blink. Edge light sweeps or fades in along the border; it never
hard-toggles. Cursor-tracking spotlight on flagship buttons is allowed — subtle, warm, and it dies
the moment it distracts (Law 20).

Law 75 — Loading is honest. Spinners, skeletons, and progress reflect real work. A success state
appears only when the action actually succeeded. Fake success is a trust violation (Functional
Truth).

Law 76 — Motion explains, never decorates. Every animation answers: what changed, where
did it go, what can I do now? Animation that answers nothing gets cut.

Law 77 — Respect reduced motion. prefers-reduced-motion disables lifts, rings, and sweeps;
state still changes via light and contrast. Accessibility is not a variant; it is the same product,
honored.

Law 78 — Breathing is reserved. Slow ambient pulse is allowed only on the single most-alive
element per view (e.g., the voice orb, live indicator). Three breathing buttons in a row is a
screensaver, not an interface.

Law 79 — Transitions between views are spatial. Boards slide, fade, and elevate in the direction
of navigation. A hard cut between app views reads as a page reload — the old internet. Smart
Apps move like objects in one space.

Law 80 — Alive at rest, brilliant on approach. At rest: quiet white/silver, black, restrained. On
hover/active: the board's jewel lights. Rest/ignite is the rhythm of the whole system — never
monochrome dead, never neon at rest.




IX. Mobile-First & Touch — Laws 81–90

Law 81 — Mobile is the primary canvas. We build smart mobile apps that also work on laptop
— never desktop pages shrunk down. Design, screenshot, and score the phone view first.

Law 82 — Extraordinary on both, equal quality. Laptop gets the same elevation, jewel, and
motion system, expanded spatially. Mobile gets its own composition, not a squeezed column of
the desktop layout.

Law 83 — 44px is the floor, 48px is the target. All touch targets (buttons, icons, tabs, list rows)
meet Law 28. Legacy elements under 44px are defects to batch-fix, not styles to preserve.

Law 84 — Tap mirrors hover. Every :hover has an :active twin. A phone user must feel the
same lift/light/compress physics through touch. Hover-only delight is desktop-only exclusion.

Law 85 — No horizontal scroll, ever. Content fits the viewport width at 360px. Fixed bottom bars
must reserve padding so they never cover content. Cut-off text or sideways scroll is a P0 release
<PARSED TEXT FOR PAGE: 9 / 11>
blocker.

Law 86 — Safe areas are respected. Notch, gesture bar, and home indicator insets are padded.
Boards and bars never slide under hardware.

Law 87 — Bottom navigation is real buttons. Nav items are elevated, labeled, jewel-active-state
blocks from the canonical library. Blank circles or naked glyphs in a bottom bar fail Law 63 and
Law 67.

Law 88 — Thumb-first layout. Primary action within thumb reach on phone. Destructive actions
never adjacent to primary actions in the thumb zone.

Law 89 — Inputs are boards. Form fields are recessed obsidian wells (Law 9) with jewel focus
border, 16px text (prevents iOS zoom), visible label, and inline validation state. A white default
input ends the premium spell.

Law 90 — Test on real viewports. Phone (390×844), small phone (360×800), tablet (768×1024),
laptop (1440×900). Screenshots at each. "It looked fine in the browser resize" is not evidence.




X. Consistency, Library & Proof — Laws 91–100

Law 91 — One library, one DNA. Buttons, boards, icons, inputs, tabs, modals, toasts, tables,
navigation — each element exists once, canonically. Pages consume blocks; they do not reinvent
them. A page with a private button class is drift.

Law 92 — Take the actual code (SN-0735). Approved elements are extracted line-by-line into the
library. Paraphrasing approved CSS from memory reintroduces the exact flatness Shawn rejected.
The block is the memory.

Law 93 — The machine-readable contract. Design laws ship as a machine-readable design
contract (tokens: colors, elevation steps, spacing, type scale, motion) that every page and every
report generator reads. A law that lives only in a chat is a law that will be broken by the next
pipeline (SN-0733 lineage).

Law 94 — Scorecard before showing Shawn. Every page is scored on: Buttons, Boards,
Typography, Icons, Motion, Color/Material, Layout, Mobile, Accessibility, Functional Truth. Per-
area floor 9.0; nothing below 9.0 is presented. Name what is not a 10 and why.

Law 95 — Screenshot or it didn't happen. Delivery includes timestamped screenshots (desktop
+ mobile) of the actual file shipped, with hash/size. Claiming "elevated" without a hover-state
screenshot is an assertion, not evidence.

Law 96 — The cold-Naya graduation test (SN-0731). A fresh Naya, given only this document and
the library, must build a Smart App scoring 9.5+ independently, with instruction-repetition
<PARSED TEXT FOR PAGE: 10 / 11>
counted. If it needs Shawn to re-teach a law, the law or the block is incomplete — fix the system,
not the student.

Law 97 — Corrections compound the same day. Every Shawn correction is distilled into this
document or the library within the same session. A correction that lives only in chat will be re-
taught by Shawn next week — that repetition is our defect, not his.

Law 98 — Never ship the same flaw twice (SN-0734). If a rebuild goes flatter than what Shawn
loved, revert to the loved version verbatim and rebuild from there. No-ego reversion beats
stubborn iteration.

Law 99 — Audit every page against this standard. Connect, Connections, Index, Ledger,
Library, Lists, Mail, Reports, Spaces, Start, Today — and every future Smart App — are audited
law-by-law. Already good stays untouched; anything below standard gets upgraded. There are no
exempt pages.

Law 100 — 10x better than the best, by experience. The target is not Apple, Linear, or Stripe —
it is the felt experience those never delivered: a living, intelligent surface that remembers,
responds, and feels like a jewel in the hand. Define "better" as the human experience first (Law
20), then build. Shawn's eye is the ground truth; the scorecard is the hypothesis.




Quick reference — Do / Don't

                   Do                                   Don't

  Elevate every board & button         Ship flat panels or labels as buttons

  Black body, jewel border/kicker      Full-color board fills

  Border light-up, tight glow          Outward neon bloom

  White title, silver body             Jewel-colored body text

  Spectrum by position in flow         Same color by category, clumped

  44px+ touch targets                  28px legacy tap areas

  Press = compress & settle            No press state

  One canonical .naya-btn              A new button class per page

  Dark delete, red accent only         Glowing red delete hover

  Screenshot desktop + mobile          "It's done" without proof
<PARSED TEXT FOR PAGE: 11 / 11>
Acceptance checklist (per page)

    All buttons are .naya-btn variants; zero legacy button classes remain
    Every board lifts and lights its border on hover; state boards included
    No element is flat: elevation step assigned to every surface
    Spectrum assigned by position; no adjacent boards share a color
    Contrast spot-check: no same-hue text-on-fill anywhere (esp. badges)
    All icon buttons from Law 62 library, circular, labeled
    All touch targets ≥44px; :active mirrors every :hover
    No horizontal scroll at 360px; bottom bar never covers content
    Inputs, modals, toasts, nav use canonical blocks (Law 91)
    Scored ≥9.0 per area with screenshots attached (Law 94–95)




Missing blocks — build order

The library is not complete until these exist as canonical blocks:

  1. Input / form block (Law 89)
  2. Modal & dialog block
  3. Toast / notification block
  4. Data table block
  5. Search interface block
  6. Toggle / settings block
  7. Content card block (distinct from board)
  8. Media player block (Law 65)
  9. Chart / data-viz block
10. Smart Link / share sheet block

Each block ships with: code, states, do/don't example, and a screenshot. A block without a
screenshot is a draft.




Distilled from Shawn's teachings 2026-09-30 → 2026-10-08: premium not fancy, elevation always, living
depth, Spectrum Law, LAW ZERO, Button Law, mobile-first, the $10-trillion-button standard, and SN-
0731/0733/0734/0735. Corrections to this document go through Shawn; ratification is his word.
