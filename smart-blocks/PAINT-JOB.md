# PAINT-JOB — The Repaint Protocol

When Shawn says "update my pages with the new design" or "which ones aren't aligned,
go fix them," this is the procedure. No freestyling. No new inventions.

## Step 1 — Audit (per page)
1. Screenshot the live page. Full page, desktop + 390px mobile.
2. List every visible pattern: buttons, inputs, cards, nav, tables, states, type, motion.
3. Score each pattern against the ground rules in `manifest.json` (all ten must hold).

## Step 2 — Misalignment is defined, not felt
A page is NOT ALIGNED if any of these are true:
- Any white/light page background, or flat dark gray instead of deep rich black.
- Buttons with flat fills, missing the 5-layer shadow physics, or colored text on buttons.
- Body text in gray instead of white; hierarchy by color instead of size.
- Neon glow, rainbow floods, or more than one spectrum identity per board.
- Motion that decorates instead of informing (spinning things, pulsing things, things that move for no reason).
- Dead affordances: chevrons that go nowhere, plus signs that don't add, icons that lie.
- Missing empty/loading/error states. Missing focus rings. Text smaller than readable.
- A second, competing button/card/input style on the same page (fragmentation).

## Step 3 — Map (old pattern → canonical block id)
For each misaligned pattern, find its replacement in `manifest.json`:
- Old button → `buttons-canonical-button-naya-btn` (or the one alt that fits the room)
- Old card/panel → `cards-elevated-board-elevated-board-board-spine-board-corner`
- Old input → `inputs-recessed-field-recessed-field`
- Old tabs → `navigation-pill-tabs-smarttabs-smarttab`
- Old table → `new-live-data-table-table-naya-table-data-sortable`
- Old toast/alert → `overlays-toast-system-nayablocks-toast`
- Old modal → `overlays-mini-modal-modal-gem`
- Missing states → `new-empty-error-loading-naya-state-naya-spinner` + `new-skeleton-loading-naya-skel`
- Missing avatars → `new-avatars-naya-avatar-naya-avatar-stack`
- Missing badges → `new-badges-naya-badge`
- Page frame → `new-page-shell-naya-shell` (see RECIPES.md for the page's recipe)

Prefer `tier: canonical`. Use `tier: alt` only when the canonical genuinely doesn't fit the room.
Never invent a replacement. If no block fits, that is a gap — report it, don't freestyle.

## Step 4 — Swap
Rebuild the page from its RECIPES.md recipe, carrying over the page's real content and
real data bindings. Content stays; chrome changes. Copy gets rewritten as invitation
and scored before shipping.

## Step 5 — Verify
1. Rebuild the deliverable as ONE self-contained HTML file.
2. Copy ONLY that file to an empty folder. Screenshot it there. (The white-page incident of 2026-10-09 never repeats.)
3. Run the pre-ship checklist from the design laws: white edge light visible without hover,
   hover ignites the element's OWN color, body text white and readable, layout metaphor
   matches the thing, copy reads like invitation, page breathes without distracting,
   every glyph keeps its promise, no duplicated systems.
4. Only then hand it to Shawn. His eye is the final compiler.
