# Smart Block: `eco-dock`

The bottom ecosystem bar — a fixed full-bleed quick-switcher (Hub / Ledger / Rooms / Spaces, inline-SVG glyphs, 10.5px silver labels) with a central 48px elevated plus button that opens a small action menu. Designed to slot into the `layout/hub-shell` dock area. Top hairline + soft top glow, safe-area padding, alive-at-rest breathing dot on the active item.

- **Type:** layout
- **Source:** authored 2026-10-09 for Hub/Ledger completion
- **Files:** `eco-dock.css`, `eco-dock.js`, `specimen.html`
- **Dependencies:** tokens.css
- **States:** `.is-active` on `.eco-item` (glowing emerald dot + lifted tint; dot breathes), `[aria-expanded="true"]` on `.eco-plus` (menu open, plus glyph rotates 45°), `:hover`/`:active` mirrors on items, plus orb, and menu buttons, responsive safe-area `@media`, `prefers-reduced-motion` (breathe + transitions off)
- **Notes:**
  - Glyphs are simple geometric inline SVGs: circle (Hub), three ledger lines (Ledger), doorway (Rooms), 2×2 grid (Spaces), plus-sign for the orb.
  - Menu is the adjacent sibling of the plus button so `+ .eco-menu` applies; keep that order.
  - The JS is behavior only: toggling, `aria-expanded`, Escape close, outside-pointer close, `eco:action` CustomEvent with `data-action` detail on menu picks, and demo active-switching (the app router owns active state in production).
  - Active uses a glowing dot and lifted tint — never a full-color fill on the item.
  - Pair with `layout/hub-shell`: render inside `.shell-dock` (the shell's grid area) or as a plain fixed bar on any page. `.eco-dock-spacer` clears the shell outlet's scroll area.

## Use it

1. Copy `eco-dock.css` and `eco-dock.js` next to your page.
2. Link `tokens.css` first, then `eco-dock.css`.
3. Paste the dock inside the hub-shell dock slot (or anywhere on the page), then include the script:

```html
<div class="shell-dock">
  <nav class="eco-dock" aria-label="Ecosystem">
    <div class="eco-dock-bar">
      <button class="eco-item is-active" type="button" aria-current="page">
        <span class="eco-dot"></span>
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="12" cy="12" r="7"/></svg>
        <span class="eco-label">Hub</span>
      </button>
      <button class="eco-item" type="button">
        <span class="eco-dot"></span>
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M5 7h14M5 12h14M5 17h9"/></svg>
        <span class="eco-label">Ledger</span>
      </button>
      <button class="eco-plus" type="button" aria-expanded="false" aria-label="Create">
        <span class="eco-plus-orb"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg></span>
      </button>
      <div class="eco-menu" role="menu">
        <button type="button" role="menuitem" data-action="new-room"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M4 20V9l8-5 8 5v11"/><path d="M10 20v-6h4v6"/></svg>New room</button>
        <button type="button" role="menuitem" data-action="add-intelligence"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M12 3v18M5 8l14 8M19 8L5 16"/></svg>Add intelligence</button>
        <button type="button" role="menuitem" data-action="scan"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M4 8V4h4M16 4h4v4M20 16v4h-4M8 20H4v-4"/><circle cx="12" cy="12" r="3"/></svg>Scan</button>
      </div>
      <button class="eco-item" type="button">
        <span class="eco-dot"></span>
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M4 20V9l8-5 8 5v11"/><path d="M10 20v-6h4v6"/></svg>
        <span class="eco-label">Rooms</span>
      </button>
      <button class="eco-item" type="button">
        <span class="eco-dot"></span>
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="5" y="5" width="6" height="6" rx="1.5"/><rect x="13" y="5" width="6" height="6" rx="1.5"/><rect x="5" y="13" width="6" height="6" rx="1.5"/><rect x="13" y="13" width="6" height="6" rx="1.5"/></svg>
        <span class="eco-label">Spaces</span>
      </button>
    </div>
  </nav>
</div>
<script src="eco-dock.js"></script>
```

## Selectors

```
.eco-dock
.eco-dock-bar
.eco-item (+ .eco-label / :hover / :active)
.eco-item .eco-dot
.eco-item.is-active
.eco-plus (+ .eco-plus-orb / svg / [aria-expanded="true"])
.eco-menu (+ button / button svg / :hover / :active)
.eco-dock-spacer
```
