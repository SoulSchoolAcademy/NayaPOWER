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

## Appendix: naya5/smart-blocks-library demo mapping (2026-10-09)

The 58 branch demos reconciled against the canonical library. Demos are not blocks: each demo below either became a canonical block (11 demos → 13 blocks) or is a composition recipe naming the canonical blocks it is built from.

### A. Demos ported as canonical blocks (13)

- `new-avatars-naya-avatar-naya-avatar-stack` → **`naya-avatar`, `naya-avatar-stack`** (Avatars .naya-avatar / .naya-avatar-stack)
- `new-badges-naya-badge` → **`naya-badge`** (Badges .naya-badge)
- `inputs-jeweled-checkbox-naya-check` → **`naya-check`** (Jeweled checkbox .naya-check)
- `new-notification-drawer-naya-drawer` → **`naya-drawer`** (Notification drawer .naya-drawer)
- `new-page-shell-naya-shell` → **`naya-shell`** (Page shell .naya-shell)
- `new-skeleton-loading-naya-skel` → **`naya-skel`** (Skeleton loading .naya-skel)
- `new-empty-error-loading-naya-state-naya-spinner` → **`naya-state`, `naya-spinner`** (Empty · error · loading .naya-state / .naya-spinner)
- `new-live-data-table-table-naya-table-data-sortable` → **`naya-table`** (Live data table table.naya-table[data-sortable])
- `cards-nested-cards-nestcard` → **`nestcard`** (Nested cards .nestcard)
- `data-law-library-law-group` → **`law-group`** (Law library .law-group)
- `specialty-interaction-physics-physics-row` → **`physics-row`** (Interaction physics .physics-row)

### B. Composition demos (47) — build from these canonical blocks

- `buttons-canonical-button-naya-btn` (Canonical button .naya-btn) → `naya-btn`
- `buttons-signature-variants-naya-btn-lead-machine-prism-proximity-str` (Signature variants .naya-btn.lead / .machine / .prism / .proximity / .streak) → `naya-btn`
- `buttons-icon-buttons-naya-btn-icon-micro-portal` (Icon buttons .naya-btn.icon / .micro / .portal) → `icon`, `naya-btn`, `portal`
- `buttons-ghost-amp-danger-naya-btn-ghost-naya-btn-danger` (Ghost &amp; danger .naya-btn--ghost / .naya-btn--danger) → `naya-btn`
- `buttons-living-button-lv-btn` (Living button .lv-btn) → `lv-btn`
- `buttons-hero-cta-living-btn` (Hero CTA .living-btn) → `living-btn`
- `buttons-split-button-naya-btn-split-split-orb` (Split button .naya-btn.split + .split-orb) → `icon`, `naya-btn`
- `buttons-segmented-control-segmented` (Segmented control .segmented) → `segmented`
- `buttons-toggle-switch-naya-toggle` (Toggle switch .naya-toggle) → `naya-toggle`
- `buttons-room-micro-controls-like-pill-act-chip-day-dot-send-cta-mic-` (Room micro-controls .like-pill / .act-chip / .day-dot / .send-cta / .mic-btn / .fab) → `act-chip`, `day-dot`, `fab`, `icon`, `like-pill`, `mic-btn`, `send-cta`
- `inputs-recessed-field-recessed-field` (Recessed field .recessed-field) → `recessed-field`
- `inputs-search-field-search-field` (Search field .search-field) → `icon`, `recessed-field`, `search-field`
- `inputs-orbiting-login-login-card-login-orbit` (Orbiting login .login-card / .login-orbit) → `login-card`, `naya-btn`, `recessed-field`
- `navigation-top-nav-bar-nav-nav-orb` (Top nav bar .nav / .nav-orb) → `nav`, `nav-orb`
- `navigation-pill-tabs-smarttabs-smarttab` (Pill tabs .smarttabs / .smarttab) → `smarttab`
- `navigation-favorites-ribbon-sn-row-smarttabs-js` (Favorites ribbon .sn-row (SmartTabs JS)) → `nav`, `smarttab`
- `navigation-app-room-nav-app-nav` (App room nav .app-nav) → `app-nav`, `nav`
- `navigation-anchor-toc-pills-toc-a` (Anchor TOC pills .toc a) → `nav`
- `cards-elevated-board-elevated-board-board-spine-board-corner` (Elevated board .elevated-board / .board-spine / .board-corner) → `board`, `elevated-board`
- `cards-spec-board-board` (Spec board .board) → `board`
- `cards-truth-cards-orbs-truthgrid-truth-torb` (Truth cards + orbs .truthgrid / .truth / .torb) → `truthgrid`
- `cards-law-cards-lawcard` (Law cards .lawcard) → `lawcard`, `scorecard`
- `cards-three-tongue-law-cards-tongue` (Three-tongue law cards .tongue) → `jw`, `tongue`
- `cards-type-scale-cards-typecard` (Type scale cards .typecard) → `type-scale`
- `cards-metric-trio-metric` (Metric trio .metric) → `icon`, `metric`
- `cards-job-cards-job` (Job cards .job) → `swatch`
- `cards-world-tiles-layer` (World tiles .layer) → `gem-bullet`
- `data-meaning-spheres-sphere` (Meaning spheres .sphere) → `icon`, `sphere`
- `data-self-scorecard-scorecard-score-row-verdict` (Self-scorecard .scorecard / .score-row / .verdict) → `scorecard`, `verdict`
- `data-data-table-specimen-data-table` (Data table specimen .data-table) → `data-table`, `status-dot`
- `overlays-toast-system-nayablocks-toast` (Toast system NayaBlocks.toast()) → `naya-btn`, `toast`
- `overlays-mini-modal-modal-mini-modal-gem` (Mini modal .modal-mini / .modal-gem) → `modal-mini`, `naya-btn`
- `overlays-share-sheet-smart-link-share-actions` (Share sheet .smart-link / .share-actions) → `icon`, `naya-btn`, `share-actions`, `smart-link`
- `media-media-player-media-player` (Media player .media-player) → `icon`, `media-player`, `naya-btn`, `portal`, `timeline`
- `media-hero-vessel-vessel` (Hero vessel .vessel) → `hero`, `orb`
- `specialty-orb-system-orb-sm-xs-black-hero-twin-glyph-icon` (Orb system .orb / --sm / --xs / --black / --hero / --twin / --glyph / --icon) → `orb`
- `specialty-mini-orb-mini-orb` (Mini-orb .mini-orb) → `mini-orb`
- `specialty-gem-bullets-gem-bullet` (Gem bullets .gem-bullet) → `gem-bullet`, `gem-list`
- `specialty-spectrum-bar-spectrum-bar` (Spectrum bar .spectrum-bar) → `spectrum-bar`
- `specialty-spectrum-swatches-token-chips` (Spectrum swatches token chips) → `swatch`
- `specialty-ship-gate-checklist-gate` (Ship-gate checklist .gate) → `jw`
- `specialty-code-copy-pre-code-copy-btn` (Code + copy pre.code / .copy-btn) → `naya-btn`, `recipe`
- `specialty-rule-boards-rule-board` (Rule boards .rule-board) → `board`, `rule-board`
- `specialty-anti-pattern-drift-demos-driftgrid-drift` (Anti-pattern drift demos .driftgrid / .drift) → _no canonical refs (demo chrome)_
- `specialty-ambient-field-page-before` (Ambient field page ::before) → _no canonical refs (demo chrome)_
- `new-command-palette-nayablocks-wirepalette` (Command palette NayaBlocks.wirePalette()) → `icon`, `naya-btn`, `section`
- `new-real-footer-naya-footer` (Real footer .naya-footer) → `footer`

_47 composition demos. Zero demos lost: 11 ported + 47 mapped = 58._
