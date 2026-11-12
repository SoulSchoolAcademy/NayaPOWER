# Naya Design — Block Selection Guide

"Which button in which situation." The decision guide for choosing between similar blocks.
Format: SITUATION → BLOCK → WHY. No guessing.

---

## BUTTONS — "which button?"

**SITUATION: The single most important action on the page** (submit, continue, enter, confirm)
→ `naya-btn` — WHY: It's the canonical. 95% restraint, 5% fire. 7-layer shadow, engraved label.
This is the default — reach for it first.

**SITUATION: A secondary or repeated action** (save draft, load more, form submit #2)
→ `primo` — WHY: Disciplined workhorse, no idle animation to compete with the hero.
Theme it per context (theme-blue/gold/green/magenta/purple).

**SITUATION: The hero action on a landing/entrance page** (the ONE thing)
→ `living-btn` — WHY: Breathes at idle, sheen sweep. Maximum presence for the arrival moment.
Only one per page. (If Shawn finds the idle animation busy, strip it — noted in source.)

**SITUATION: An action that should feel magical** (entering a space, activating a feature)
→ `orbit-btn` — WHY: Conic ring of light orbiting the perimeter. Law 25 made real.
Spend it on moments, not mundanity.

**SITUATION: Interactive surface where hover feedback matters** (dashboards, tool palettes)
→ `lv-btn` — WHY: Cursor sheen, soul core, proximity-aware. Responds before the click.
Needs lv-btn.js.

**SITUATION: A clean CTA inside content** (card footer, in-article action)
→ `cx-btn` — WHY: Essential CTA, simpler tier. Clear without ceremony.

**SITUATION: Icon-only action, space is tight** (close, menu, settings)
→ `icon-btn` — WHY: 52px round, SVG icons, aria-pressed state. Never below 44px touch.

**SITUATION: Toggle action on content** (like, save, bookmark)
→ `nl-iconbtn` — WHY: .liked/.saved states show the toggle visibly. For state that persists.

**SITUATION: Tertiary action** (cancel, skip, learn more, dismiss)
→ `nl-btn-ghost` — WHY: Minimal chrome. Never the primary — ghosts don't convert.
Always pair with a real button.

**SITUATION: Utility action in dense UI** (table row action, toolbar button)
→ `nl-btn` — WHY: Generic elevated, --tone themable. Function over soul.

**SITUATION: Audio/voice playback** ("press to hear")
→ `nl-playbtn` — WHY: Play ring with .playing state. For Intelligent Block voice playback,
audio messages, any listen moment.

---

## CARDS — "which card?"

**SITUATION: Knowledge content with truth states** (answers, Smart Notes, intelligence)
→ `intelligent-block` — WHY: THE signature. Header + truth badge + 4-layer answer +
expandable layers + provenance footer. If it has a truth state, it goes here.

**SITUATION: Intelligence item with provenance** (ledger entry, finding, claim)
→ `li-card` — WHY: Identity edge bar, jewel, source label, time-ago, hint pill.
Truth-aware like intelligent-block but feed-shaped. Opens `li-modal` on tap.

**SITUATION: Feed event / activity** (something happened)
→ `activity-card` — WHY: "Every event is a card, not a line." Jewel, narrative (16px/1.65),
source + time meta. For events, not knowledge.

**SITUATION: A space/community in a grid** (discovery)
→ `sp-card` — WHY: Cover art + name + topic + meta, --sc accent. Taps through to `sp-detail`.

**SITUATION: Generic content with media** (article, media tile)
→ `nl-ccard` — WHY: The everyday default when no specialized card fits.

**SITUATION: A content section deserving destination feel** (feature area, grouped content)
→ `board` — WHY: Identity spine, one board one color. REQUIRED: set --ic.
For stronger spine presence, `board-tone` (5px glowing edge).

**SITUATION: Law, rule, principle** (one per card)
→ `lawcard` — WHY: Numbered, diamond marker, title + body. Governance made visible.

---

## TABS — "which tabs?"

**SITUATION: Feed filtering with customizable tabs** (user can add/remove)
→ `smart-tabs` — WHY: Horizontal scroll, per-tab --tc theming, popover editor.
"Tabs are navigation intent, never storage."

**SITUATION: Exactly three view lenses** (Collective / Personal / Activity)
→ `lens-tabs` — WHY: Designed for exactly three. Don't repurpose for other counts.

**SITUATION: 2-5 fixed options, tight space** (view mode, small filter set)
→ `seg-tab` — WHY: Compact segmented control. For small option groups.

**SITUATION: Detail view sections with counts** (Members 12, Posts 48)
→ `sp-dtabs` — WHY: Underline style with count badges. Needs --sc accent context.

---

## GRAPHS — "which visualization?"

**SITUATION: One hero metric, alive** → `pulse-orb` (breathes with the value)
**SITUATION: KPI number with count-up** → `living-counter` (theater deliberate)
**SITUATION: Comparing 3-8 categories** → `jewel-pillar` (jeweled bars)
**SITUATION: Part-to-whole over time** → `spectrum-flow` (stacked river)
**SITUATION: Relationships / networks** → `constellation` (nodes + arcs)
**SITUATION: Live system pulse** → `pulse-rings` (heartbeat — must beat)
**SITUATION: A 0-10 score rendered beautifully** → `orbit-dial` (the ring means "judged")

---

## OVERLAYS — "which overlay?"

**SITUATION: Focused task needing full attention** (confirm, focused form)
→ `nl-modal` — WHY: Backdrop + dialog. Always with clear dismiss. Never stack.

**SITUATION: Intel deep-dive from a card** → `li-modal` — WHY: Stat grid + explanation +
full a11y (focus trap, Escape, restore). Tied to li- grammar.

**SITUATION: Transient feedback** (saved, error, status)
→ `nl-toast` — WHY: Auto-dismissing. Fire-and-forget. Never for actions.

**SITUATION: Mobile share/actions** → `nl-sheet` — WHY: Bottom sheet. Mobile only.

---

## CHROME — "which frame?"

**SITUATION: App side navigation** → `drawer` (tucks away on mobile, needs drawer.js)
**SITUATION: Mobile thumb-zone nav** → `eco-bottombar` (46px round buttons + jewel plus)
**SITUATION: The one mobile action** (compose/share/create) → `share-fab` (56px, one per screen)
**SITUATION: App room/screen frame** → `room-chrome` (--room-accent per room)
**SITUATION: Integration/connection entry point** → `door` (per-door --door-accent)

---

## QUICK DECISION TREE

```
Need a button?
  Primary action → naya-btn
  Hero/landing → living-btn
  Magical moment → orbit-btn
  Everyday/secondary → primo
  In-content CTA → cx-btn
  Icon only → icon-btn (one-shot) / nl-iconbtn (toggle)
  Tertiary → nl-btn-ghost
  Dense UI utility → nl-btn
  Play audio → nl-playbtn

Need a card?
  Has truth state → intelligent-block (knowledge) / li-card (feed intel)
  It's an event → activity-card
  It's a space → sp-card
  It's a law → lawcard
  Generic content → nl-ccard
  Section destination → board / board-tone

Need tabs?
  Customizable feed filter → smart-tabs
  Exactly 3 lenses → lens-tabs
  2-5 fixed options → seg-tab
  Detail sections + counts → sp-dtabs
```
