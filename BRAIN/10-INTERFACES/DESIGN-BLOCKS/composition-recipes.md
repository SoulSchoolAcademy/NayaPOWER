# Naya Design — Composition Recipes

Proven page compositions from Shawn's designs. Not theory — these are the actual patterns
extracted from the design files. Each recipe names the blocks, the order, the layout pattern,
and the design file that proved it.

**Law:** If a block exists for the job, use it. Custom CSS for a solved job is a violation.

---

## 1. Feed Page — "every event is a card, not a line"

**Proved by:** Naya Smart Hub Design.html (activity feed), Ledger Page Design.html (intel stream)

**Blocks, in order:**
1. `page-shell` — the chassis (every page starts here)
2. `room-chrome` — head (kicker + title + lede) + toolbar
3. `smart-tabs` + `lens-tabs` — feed filtering (Collective / Personal / Activity)
4. `activity-stream` — the time-grouped container
5. `activity-card` × N — one per event (or `li-card` for truth-aware intel)
6. `li-day` — day dividers between time groups
7. `eco-bottombar` — mobile thumb-zone nav
8. `drawer` — side navigation

**Layout pattern:** single column stream, full-width. Cards stack vertically in time groups.
Filter tabs sit above the stream; the stream is the page.

**When to vary:** Ledger intel feed swaps `activity-card` → `li-card` (adds truth badges,
source labels, hint pills) and opens `li-modal` on tap. Same stream, smarter cards.

---

## 2. Knowledge / Intel Page — "the answer, beautifully"

**Proved by:** Naya Smart Hub Design.html (intelligent blocks everywhere)

**Blocks, in order:**
1. `page-shell`
2. `room-chrome` — head + toolbar
3. `intelligent-block` — THE signature block: header (jewel + kind + title + truth badge),
   "in a nutshell" 4-layer answer, expandable jewel layers, provenance footer
4. `metric-ribbon` — supporting stats beneath the answer
5. `state-badge` — inline on every claim inside the block
6. `nl-playbtn` + `voice-type` — "press to hear Naya read it"

**Layout pattern:** focused single column. One intelligent-block per question/answer.
Stats ribbon grounds the claims. Voice playback is the premium touch.

**When to vary:** Multiple related answers → stack intelligent-blocks in a `section`
with `headline` dividers. Never put two truth-badge blocks side-by-side competing.

---

## 3. Space / Community Page — "where connections live"

**Proved by:** Smart Spaces Page Design.html

**Blocks, in order:**
1. `page-shell`
2. `room-chrome`
3. `row-grid` (3-col) of `sp-card` — discovery grid, each with `--sc` accent + cover art
4. Tap a card → `sp-detail` — cover, head, `sp-dtabs` (About / Chat / Members), `sp-about-rows`
5. `sp-chat` — message list + composer inside the detail view
6. `sp-audio-msg` — voice notes inline in chat
7. `sp-inv-chip` — invites: "tap to step into a room"
8. `eco-bottombar` — mobile nav

**Layout pattern:** grid → detail. Discovery is a grid; tapping enters the space (detail view).
Chat lives inside the space, not beside it.

---

## 4. Assessment / Quiz — "the asking face"

**Proved by:** Maxis App Design.html (assessment flow)

**Blocks, in order:**
1. `page-shell`
2. `progress-hud` — top: location dot + label, animated fill, percent. Always visible.
3. `question` — eyebrow label + title + hairline rule
4. `answer` × N — jewel icon + title + sub + chevron, per-answer `--accent`
   (or `interest-picker` for onboarding preference capture)
5. `primo` / `naya-btn` — continue CTA
6. Results: `score-stage` — the 260px reveal moment
7. `dimension-constellation` — 9-dimension breakdown
8. `scorecard` — dimension scores with notes
9. `verdict` — the judgment, spoken plainly

**Layout pattern:** one question per screen, linear flow. Progress HUD is the constant.
Results are a crescendo: score-stage (the number) → constellation (the breakdown) →
scorecard (the detail) → verdict (the word).

---

## 5. Report — "governance made visible"

**Proved by:** Naya Design Elements N2.html (Design Contract report), Naya Design Element Set N4.html

**Blocks, in order:**
1. `page-shell`
2. `hero` — report title with kicker
3. `hub-quote` — the opening voice (optional, 1 max)
4. `headline` + `section` — per-section structure
5. `scorecard` — scored dimensions
6. `law-steps` — pipeline/process as a staircase
7. `lawcard` × N — one card per law/rule
8. `checks` — verification checklist
9. `tongue` — three-language display where the standard applies
10. `verdict` — the closing judgment
11. `truthgrid` — honesty-system explainer (appendix/onboarding)

**Layout pattern:** editorial document flow. Score → process → laws → verification → verdict.
The verdict closes — nothing after it but footer.

---

## 6. Landing / Entrance — "the front door"

**Proved by:** Welcome Page Design.html

**Blocks, in order:**
1. `page-shell`
2. `portal` — orbit rings + purple glow, the arrival moment
3. `presence` — the one-line state ("SOVEREIGN ENTRANCE")
4. `hero` — display headline + sub + CTA row
5. `living-btn` or `naya-btn` — THE action (one only)
6. `hub-quote` — editorial voice (optional)
7. `row-grid` of `door` — "one brain, many doors" entry grid
8. `footer`

**Layout pattern:** arrival → statement → action → doors. The portal is the door;
everything after it earns the entry. One hero action — never two competing CTAs.

---

## 7. Dashboard / Stats — "the intelligence, alive"

**Proved by:** Smart Graphs visual language (7 graph blocks), Naya Smart Hub Design.html (digest)

**Blocks, in order:**
1. `page-shell`
2. `room-chrome` — head + `period-strip`-style time filter (use `seg-tab`)
3. `metric-ribbon` — the KPI strip (with honest `.unknown` states)
4. `row-grid`: `living-counter` (hero number) + `pulse-orb` (breathing metric)
5. `jewel-pillar` — comparisons
6. `spectrum-flow` — part-to-whole over time
7. `pulse-rings` — live heartbeat (if real-time)
8. `orbit-dial` — any 0-10 score

**Layout pattern:** ribbon → hero numbers → comparisons → flows. Most important number
gets the living-counter; supporting stats share the ribbon. Never more than one
pulse-orb per view.

---

## 8. App Screen (generic room) — "the interior"

**Proved by:** Naya Smart Hub Design.html (room system)

**Blocks, in order:**
1. `page-shell`
2. `drawer` — side nav (tucks away on mobile)
3. `room-chrome` — head + toolbar + body + outlet, `--room-accent` per room
4. Room content (any recipe above, adapted)
5. `eco-bottombar` — mobile thumb nav
6. `share-fab` — the one mobile action (optional, one per screen)

**Layout pattern:** chrome frames content. The room accent colors the kicker and LED;
content follows whichever recipe fits the room's job.

---

## 9–58. Smart Blocks branch demos — folded, not forked

The 58 demo files from branch `naya5/smart-blocks-library` were reconciled (plan on #1354, comment 6084615118):
50 are **compositions** of canonical blocks (every referenced ID verified in the wave index),
6 carry the 13 **novel components** (ported as canonical blocks in this library — 239 + 13 = 252),
and 2 are **specimens** (demos, not blocks). The branch’s parallel structure is retired; nothing was lost.

**Law:** If a block exists for the job, use it. Custom CSS for a solved job is a violation.

## 9. Canonical button

**Source demo:** `smart-blocks/buttons/buttons-canonical-button-naya-btn.html` (branch `naya5/smart-blocks-library` — retired)

**Composes:** `naya-btn`

**Pattern:** The rest button, silver-white at rest — the canonical form every variant inherits.

## 10. Signature variants

**Source demo:** `smart-blocks/buttons/buttons-signature-variants-naya-btn-lead-machine-prism-proximity-str.html` (branch `naya5/smart-blocks-library` — retired)

**Composes:** `naya-btn`

**Pattern:** Five named accents (.lead / .machine / .prism / .proximity / .streak) on the canonical button — accent lives in `--sc`, never in the chrome.

## 11. Icon buttons

**Source demo:** `smart-blocks/buttons/buttons-icon-buttons-naya-btn-icon-micro-portal.html` (branch `naya5/smart-blocks-library` — retired)

**Composes:** `naya-btn` + `icon` + `portal`

**Pattern:** Icon + label lockups — micro size for toolbars, portal for the arrival moment.

## 12. Ghost & danger

**Source demo:** `smart-blocks/buttons/buttons-ghost-amp-danger-naya-btn-ghost-naya-btn-danger.html` (branch `naya5/smart-blocks-library` — retired)

**Composes:** `naya-btn`

**Pattern:** Ghost for secondary actions, danger reserved for the destructive one — color crosses chrome only here, once.

## 13. Living button

**Source demo:** `smart-blocks/buttons/buttons-living-button-lv-btn.html` (branch `naya5/smart-blocks-library` — retired)

**Composes:** `lv-btn`

**Pattern:** The breathing CTA — one per page, never two.

## 14. Hero CTA

**Source demo:** `smart-blocks/buttons/buttons-hero-cta-living-btn.html` (branch `naya5/smart-blocks-library` — retired)

**Composes:** `living-btn`

**Pattern:** The hero's single action — headline + sub + one ignited button.

## 15. Split button

**Source demo:** `smart-blocks/buttons/buttons-split-button-naya-btn-split-split-orb.html` (branch `naya5/smart-blocks-library` — retired)

**Composes:** `naya-btn` + `icon`

**Pattern:** Primary action + chevron overflow — the split-orb marks the seam.

## 16. Segmented control

**Source demo:** `smart-blocks/buttons/buttons-segmented-control-segmented.html` (branch `naya5/smart-blocks-library` — retired)

**Composes:** `segmented`

**Pattern:** Mutually exclusive choice in a pill container — the selected segment ignites.

## 17. Toggle switch

**Source demo:** `smart-blocks/buttons/buttons-toggle-switch-naya-toggle.html` (branch `naya5/smart-blocks-library` — retired)

**Composes:** `naya-toggle`

**Pattern:** Binary setting with press physics — label left, switch right.

## 18. Room micro-controls

**Source demo:** `smart-blocks/buttons/buttons-room-micro-controls-like-pill-act-chip-day-dot-send-cta-mic-.html` (branch `naya5/smart-blocks-library` — retired)

**Composes:** `like-pill` + `act-chip` + `day-dot` + `send-cta` + `mic-btn` + `fab` + `icon`

**Pattern:** A room's control cluster — reactions, chips, day markers, send, mic, FAB — each control earns its own block.

## 19. Recessed field

**Source demo:** `smart-blocks/inputs/inputs-recessed-field-recessed-field.html` (branch `naya5/smart-blocks-library` — retired)

**Composes:** `recessed-field`

**Pattern:** The input that sits INTO the page, not on it — inset shadows sell the depth.

## 20. Search field

**Source demo:** `smart-blocks/inputs/inputs-search-field-search-field.html` (branch `naya5/smart-blocks-library` — retired)

**Composes:** `search-field` + `recessed-field` + `icon`

**Pattern:** Recessed field + magnifier icon + clear affordance.

## 21. Jeweled checkbox

**Source demo:** `smart-blocks/inputs/inputs-jeweled-checkbox-naya-check.html` (branch `naya5/smart-blocks-library` — retired)

**Composes:** `naya-check (NEW, this port)` + `board`

**Pattern:** The checklist lives on a board — each promise is a jeweled checkbox that ignites green when kept.

## 22. Orbiting login

**Source demo:** `smart-blocks/inputs/inputs-orbiting-login-login-card-login-orbit.html` (branch `naya5/smart-blocks-library` — retired)

**Composes:** `login-card` + `naya-btn` + `recessed-field`

**Pattern:** The login moment as arrival — orbiting lights around the card, recessed fields, one ignited button.

## 23. Top nav bar

**Source demo:** `smart-blocks/navigation/navigation-top-nav-bar-nav-nav-orb.html` (branch `naya5/smart-blocks-library` — retired)

**Composes:** `nav` + `nav-orb`

**Pattern:** The living mark left, room links center, the orb marks presence.

## 24. Pill tabs

**Source demo:** `smart-blocks/navigation/navigation-pill-tabs-smarttabs-smarttab.html` (branch `naya5/smart-blocks-library` — retired)

**Composes:** `smarttab`

**Pattern:** Filter tabs as pills — the active pill fills, the rest stay quiet.

## 25. Favorites ribbon

**Source demo:** `smart-blocks/navigation/navigation-favorites-ribbon-sn-row-smarttabs-js.html` (branch `naya5/smart-blocks-library` — retired)

**Composes:** `nav` + `smarttab`

**Pattern:** A horizontally scrolling ribbon of favorite rooms — SmartTabs JS wires selection.

## 26. App room nav

**Source demo:** `smart-blocks/navigation/navigation-app-room-nav-app-nav.html` (branch `naya5/smart-blocks-library` — retired)

**Composes:** `app-nav` + `nav`

**Pattern:** Room switcher with accent per room — the active room's color touches the kicker only.

## 27. Anchor TOC pills

**Source demo:** `smart-blocks/navigation/navigation-anchor-toc-pills-toc-a.html` (branch `naya5/smart-blocks-library` — retired)

**Composes:** `nav`

**Pattern:** In-page navigation as pills — anchors to sections, never leaves the page.

## 28. Elevated board

**Source demo:** `smart-blocks/cards/cards-elevated-board-elevated-board-board-spine-board-corner.html` (branch `naya5/smart-blocks-library` — retired)

**Composes:** `elevated-board` + `board`

**Pattern:** The board that floats — spine and corner details sell the elevation.

## 29. Spec board

**Source demo:** `smart-blocks/cards/cards-spec-board-board.html` (branch `naya5/smart-blocks-library` — retired)

**Composes:** `board`

**Pattern:** The working surface for specs — quieter than the elevated board.

## 30. Truth cards + orbs

**Source demo:** `smart-blocks/cards/cards-truth-cards-orbs-truthgrid-truth-torb.html` (branch `naya5/smart-blocks-library` — retired)

**Composes:** `truthgrid`

**Pattern:** Claims as cards in a truth grid — orbs mark the living ones.

## 31. Law cards

**Source demo:** `smart-blocks/cards/cards-law-cards-lawcard.html` (branch `naya5/smart-blocks-library` — retired)

**Composes:** `lawcard` + `scorecard`

**Pattern:** One law per card — the scorecard beneath carries the dimension scores.

## 32. Three-tongue law cards

**Source demo:** `smart-blocks/cards/cards-three-tongue-law-cards-tongue.html` (branch `naya5/smart-blocks-library` — retired)

**Composes:** `tongue` + `jw`

**Pattern:** Each law spoken three ways (human / Naya / machine) — the jewel marks the tongue.

## 33. Type scale cards

**Source demo:** `smart-blocks/cards/cards-type-scale-cards-typecard.html` (branch `naya5/smart-blocks-library` — retired)

**Composes:** `type-scale`

**Pattern:** The type system demonstrated as cards — size separates, color doesn't.

## 34. Metric trio

**Source demo:** `smart-blocks/cards/cards-metric-trio-metric.html` (branch `naya5/smart-blocks-library` — retired)

**Composes:** `metric` + `icon`

**Pattern:** Three KPIs in a row — the hero number gets the living treatment elsewhere.

## 35. Job cards

**Source demo:** `smart-blocks/cards/cards-job-cards-job.html` (branch `naya5/smart-blocks-library` — retired)

**Composes:** `swatch`

**Pattern:** Work items as cards with spectrum swatch accents.

## 36. World tiles

**Source demo:** `smart-blocks/cards/cards-world-tiles-layer.html` (branch `naya5/smart-blocks-library` — retired)

**Composes:** `gem-bullet`

**Pattern:** World/space tiles as layered cards with gem markers.

## 37. Meaning spheres

**Source demo:** `smart-blocks/data/data-meaning-spheres-sphere.html` (branch `naya5/smart-blocks-library` — retired)

**Composes:** `sphere` + `icon`

**Pattern:** Concepts as spheres — meaning you can orbit.

## 38. Self-scorecard

**Source demo:** `smart-blocks/data/data-self-scorecard-scorecard-score-row-verdict.html` (branch `naya5/smart-blocks-library` — retired)

**Composes:** `scorecard` + `verdict`

**Pattern:** Score rows per dimension, then the verdict spoken plainly — nothing after the verdict but footer.

## 39. Data table specimen

**Source demo:** `smart-blocks/data/data-data-table-specimen-data-table.html` (branch `naya5/smart-blocks-library` — retired)

**Composes:** `data-table` + `status-dot`

**Pattern:** The div-grid table for dense data — status dots mark truth states.

## 40. Toast system

**Source demo:** `smart-blocks/overlays/overlays-toast-system-nayablocks-toast.html` (branch `naya5/smart-blocks-library` — retired)

**Composes:** `toast` + `naya-btn`

**Pattern:** Truthful, transient — toasts confirm, never interrupt; NayaBlocks.toast() fires them.

## 41. Mini modal

**Source demo:** `smart-blocks/overlays/overlays-mini-modal-modal-mini-modal-gem.html` (branch `naya5/smart-blocks-library` — retired)

**Composes:** `modal-mini` + `naya-btn`

**Pattern:** The small decision — one question, two buttons, the gem marks the premium choice.

## 42. Share sheet

**Source demo:** `smart-blocks/overlays/overlays-share-sheet-smart-link-share-actions.html` (branch `naya5/smart-blocks-library` — retired)

**Composes:** `smart-link` + `share-actions` + `naya-btn` + `icon`

**Pattern:** The share moment — smart link first, then the action row.

## 43. Media player

**Source demo:** `smart-blocks/media/media-media-player-media-player.html` (branch `naya5/smart-blocks-library` — retired)

**Composes:** `media-player` + `timeline` + `naya-btn` + `icon` + `portal`

**Pattern:** Player chrome with a timeline scrub — the portal marks the live moment.

## 44. Hero vessel

**Source demo:** `smart-blocks/media/media-hero-vessel-vessel.html` (branch `naya5/smart-blocks-library` — retired)

**Composes:** `hero` + `orb`

**Pattern:** The arrival vessel — the hero statement cradled by the orb.

## 45. Orb system

**Source demo:** `smart-blocks/specialty/specialty-orb-system-orb-sm-xs-black-hero-twin-glyph-icon.html` (branch `naya5/smart-blocks-library` — retired)

**Composes:** `orb`

**Pattern:** The orb in all its sizes — sm, xs, black, hero, twin, glyph, icon — presence, scaled.

## 46. Mini-orb

**Source demo:** `smart-blocks/specialty/specialty-mini-orb-mini-orb.html` (branch `naya5/smart-blocks-library` — retired)

**Composes:** `mini-orb`

**Pattern:** Presence at 16px — the smallest living mark.

## 47. Gem bullets

**Source demo:** `smart-blocks/specialty/specialty-gem-bullets-gem-bullet.html` (branch `naya5/smart-blocks-library` — retired)

**Composes:** `gem-bullet` + `gem-list`

**Pattern:** List markers as gems — the list earns its sparkle.

## 48. Spectrum bar

**Source demo:** `smart-blocks/specialty/specialty-spectrum-bar-spectrum-bar.html` (branch `naya5/smart-blocks-library` — retired)

**Composes:** `spectrum-bar`

**Pattern:** The full spectrum in one bar, law order — magenta leads.

## 49. Spectrum swatches

**Source demo:** `smart-blocks/specialty/specialty-spectrum-swatches-token-chips.html` (branch `naya5/smart-blocks-library` — retired)

**Composes:** `swatch`

**Pattern:** Token chips for the palette — copy the hex, use the color.

## 50. Ship-gate checklist

**Source demo:** `smart-blocks/specialty/specialty-ship-gate-checklist-gate.html` (branch `naya5/smart-blocks-library` — retired)

**Composes:** `jw`

**Pattern:** The pre-ship checklist — the jewel marks each gate passed.

## 51. Code + copy

**Source demo:** `smart-blocks/specialty/specialty-code-copy-pre-code-copy-btn.html` (branch `naya5/smart-blocks-library` — retired)

**Composes:** `recipe` + `naya-btn`

**Pattern:** Code blocks with a copy button — the recipe block carries the snippet.

## 52. Rule boards

**Source demo:** `smart-blocks/specialty/specialty-rule-boards-rule-board.html` (branch `naya5/smart-blocks-library` — retired)

**Composes:** `rule-board` + `board`

**Pattern:** Rules as boards — the board that teaches.

## 53. Page shell demo

**Source demo:** `smart-blocks/new/new-page-shell-naya-shell.html` (branch `naya5/smart-blocks-library` — retired)

**Composes:** `naya-shell (NEW, this port)` + `metric` + `orb`

**Pattern:** The chassis demo — rail, head, main with a metric trio, the orb as the brand mark.

## 54. Command palette

**Source demo:** `smart-blocks/new/new-command-palette-nayablocks-wirepalette.html` (branch `naya5/smart-blocks-library` — retired)

**Composes:** `section` + `naya-btn` + `icon`

**Pattern:** The ⌘K palette — sections of commands; NayaBlocks.wirePalette() wires it.

## 55. Live data table demo

**Source demo:** `smart-blocks/new/new-live-data-table-table-naya-table-data-sortable.html` (branch `naya5/smart-blocks-library` — retired)

**Composes:** `naya-table (NEW, this port)` + `data-table`

**Pattern:** The semantic table you can interrogate — click headers to sort; badges mark status.

## 56. Empty / error / loading demo

**Source demo:** `smart-blocks/new/new-empty-error-loading-naya-state-naya-spinner.html` (branch `naya5/smart-blocks-library` — retired)

**Composes:** `naya-state (NEW, this port)` + `naya-spinner (NEW, this port)` + `naya-btn`

**Pattern:** The three honest faces of “not yet” — each with one clear next action.

## 57. Notification drawer demo

**Source demo:** `smart-blocks/new/new-notification-drawer-naya-drawer.html` (branch `naya5/smart-blocks-library` — retired)

**Composes:** `naya-drawer (NEW, this port)` + `drawer` + `naya-btn` + `icon`

**Pattern:** The trigger opens the drawer — canonical `drawer` handles side nav, `naya-drawer` carries notifications.

## 58. Real footer

**Source demo:** `smart-blocks/new/new-real-footer-naya-footer.html` (branch `naya5/smart-blocks-library` — retired)

**Composes:** `footer`

**Pattern:** The page's quiet end — link columns, no noise.

## Specimens — demos, not blocks

### Anti-pattern drift demos

**Source demo:** `smart-blocks/specialty/specialty-anti-pattern-drift-demos-driftgrid-drift.html` (branch `naya5/smart-blocks-library` — retired)

**What it is:** the driftgrid — what design drift looks like, so builders recognize it and refuse it. A teaching specimen, never a block.

### Ambient field

**Source demo:** `smart-blocks/specialty/specialty-ambient-field-page-before.html` (branch `naya5/smart-blocks-library` — retired)

**What it is:** the page-before ambient field — atmosphere behind content. A specimen, never a block.
