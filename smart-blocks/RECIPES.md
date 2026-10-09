# RECIPES — Page Compositions for NayaNET

How Naya builds a page: pick the recipe, pull each block by `id` from `manifest.json`,
paste the `html`, link `blocks/naya-blocks.css` (plus `blocks/naya-blocks.js` when any
block has `js_needed: true`). Self-contained single file on delivery. Black ground only.

Block ids below are exact `manifest.json` ids.

---

## 1. Welcome / Entrance
Front door: invitation, not a label. Warmest part of the product.
- `new-page-shell-naya-shell` (header variant, no sidebar)
- `specialty-orb-system-orb-sm-xs-black-hero-twin-glyph-icon` (hero orb, center)
- `inputs-orbiting-login-login-card-login-orbit`
- `buttons-hero-cta-living-btn` (exactly one)
- `new-real-footer-naya-footer`

## 2. Smart Hub — Today
The intelligent hub. Three things need you; the rest can wait.
- `new-page-shell-naya-shell` (sidebar: Today / Spaces / Ledger / Mail)
- `navigation-app-room-nav-app-nav`
- `cards-metric-trio-metric` (What matters / What changed / What's next)
- `cards-elevated-board-elevated-board-board-spine-board-corner` (one per room, own spectrum identity)
- `new-notification-drawer-naya-drawer`
- `overlays-toast-system-nayablocks-toast`

## 3. Smart Ledger
The living record. Every event, queryable, sortable.
- `new-page-shell-naya-shell`
- `inputs-search-field-search-field` (wired to `new-command-palette-nayablocks-wirepalette`)
- `buttons-segmented-control-segmented` (All / Verified / Claims / Demo)
- `new-live-data-table-table-naya-table-data-sortable`
- `cards-truth-cards-orbs-truthgrid-truth-torb` (legend: ✓ verified / ? claim / ◈ demo)
- `new-empty-error-loading-naya-state-naya-spinner` (empty + loading states)

## 4. Smart Spaces
Rooms you step into. People, not products — vertical flow, never a product grid.
- `new-page-shell-naya-shell`
- `cards-elevated-board-elevated-board-board-spine-board-corner` (one per space)
- `new-avatars-naya-avatar-naya-avatar-stack` (member stacks)
- `buttons-room-micro-controls-like-pill-act-chip-day-dot-send-cta-mic-` (like, act, day-pick, send, talk)
- `overlays-share-sheet-smart-link-share-actions`

## 5. Smart Mail
- `new-page-shell-naya-shell`
- `navigation-pill-tabs-smarttabs-smarttab` (Inbox / Sent / Drafts)
- `new-live-data-table-table-naya-table-data-sortable` (message rows)
- `inputs-recessed-field-recessed-field` (compose)
- `buttons-canonical-button-naya-btn` (Send)

## 6. Smart Stats
The calculator. Every instrument names what it measures.
- `new-page-shell-naya-shell`
- `inputs-search-field-search-field` ("give me the stats on X")
- `new-command-palette-nayablocks-wirepalette`
- `cards-metric-trio-metric`
- `data-self-scorecard-scorecard-score-row-verdict`
- `data-law-library-law-group` (for the 20-area stat index, collapsible)

## 7. Maxis App (assessment)
- `new-page-shell-naya-shell` (header only)
- `cards-elevated-board-elevated-board-board-spine-board-corner` (question boards)
- `buttons-room-micro-controls-like-pill-act-chip-day-dot-send-cta-mic-` (interest chips)
- `data-self-scorecard-scorecard-score-row-verdict` (score reveal)
- `buttons-hero-cta-living-btn` (one: continue)

---

## Rules every recipe obeys
- One hero CTA per page. One nav system per page. One media moment per view.
- Exactly one spectrum identity per board; spectrum flows purple→blue→green→yellow→gold→orange→red→magenta.
- Every page gets its empty, loading, and error states from `new-empty-error-loading-naya-state-naya-spinner` — no exceptions.
- Copy is invitation, never documentation. Score it before shipping.
- Deliverable is ONE self-contained HTML file. Verify from an empty folder before handing over.
