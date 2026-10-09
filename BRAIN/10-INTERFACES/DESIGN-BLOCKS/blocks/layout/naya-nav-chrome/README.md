# Smart Block: `naya-nav-chrome`

Ledger's sticky topbar — the front-door chrome shared with the Hub. A black-glass sticky bar carrying the rooms drawer trigger (left), the front-door lockup — "NAYA" wordmark + breathing living dot + one-line tagline (center) — and the NayaNET drawer trigger plus an honest sync readout (right). Composes with the bottom ecosystem bar so the two feel like one organism with `layout/hub-shell`: same tokens, same 24/18/14 scale, same signature ease.

- **Type:** layout
- **Source:** authored 2026-10-09 for Hub/Ledger completion
- **Files:** `naya-nav-chrome.css`, `specimen.html`
- **Dependencies:** tokens.css
- **States:** `:hover` / `:active` on `.nav-trigger` (44px elevated circle, lift + purple glow on hover, press compression on active), breathing `.nav-live-dot`, `.nav-sync-dot--stale` (gold) / `--down` (red) for non-synced honesty, mobile truncation (`@media`), `@media (prefers-reduced-motion: reduce)` disables the breathing dot
- **Notes:**
  - This file owns the TOPBAR only. The bottom ecosystem bar ships as `layout/eco-dock` (not yet staged) — the specimen composes a clearly-labeled specimen-only placeholder; drop the real dock in when it lands.
  - Drawer opening/closing is the page's job; this block is the chrome.
  - The sync readout is an honest live region (`aria-live="polite"`): the page re-renders its text and dot class — "Synced · just now" with the emerald dot ONLY when true; stale/down states use the gold/red dots and carry their age ("Stale · 12 min ago").
  - No text uses jewel colors; jewels live in the living dot, the sync dot, and hover glows.
  - `color-mix` is used for the glass background so the only color source stays the tokens.

## Use it

1. Copy `naya-nav-chrome.css` next to your page.
2. Link `tokens.css` first, then `naya-nav-chrome.css`.
3. Paste the header as the first element in `<body>`; pair with `layout/eco-dock` at the bottom of the page:

```html
<header class="nav-chrome">
  <div class="nav-chrome-bar">
    <button class="nav-trigger" type="button" aria-label="Open rooms">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <path d="M7 21V9.5L12 4l5 5.5V21"/><path d="M10 21v-6h4v6"/>
      </svg>
    </button>
    <div class="nav-lockup">
      <span class="nav-wordmark">NAYA</span>
      <span class="nav-live-dot" aria-hidden="true"></span>
      <p class="nav-tagline">Living intel, kept.</p>
    </div>
    <div class="nav-side">
      <p class="nav-sync" aria-live="polite"><span class="nav-sync-dot" aria-hidden="true"></span>Synced · just now</p>
      <button class="nav-trigger" type="button" aria-label="Open NayaNET">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true">
          <circle cx="12" cy="5.5" r="2.2"/><circle cx="5.5" cy="18.5" r="2.2"/><circle cx="18.5" cy="18.5" r="2.2"/>
          <path d="M10.6 7.2 6.8 16.8M13.4 7.2l3.8 9.6M7.7 18.5h8.6"/>
        </svg>
      </button>
    </div>
  </div>
</header>
```

## Selectors

```
.nav-chrome
.nav-chrome-bar
.nav-trigger (+ svg / :hover / :active / :focus-visible)
.nav-lockup
.nav-wordmark
.nav-live-dot
.nav-tagline
.nav-side
.nav-sync
.nav-sync-dot (+ --stale / --down)
```
