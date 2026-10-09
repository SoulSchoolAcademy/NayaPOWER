# Smart Block: `hub-shell`

The chassis every Hub-family page sits on. A full-viewport `.shell` grid — fixed left rail column + main column on desktop, rail off-canvas on mobile — with a topbar front door (wordmark + breathing jewel dot + one warm line), a rail slot, a scrollable main outlet, a dock slot, and an inert ambient-life layer drifting behind everything. Full width, no max-width caps.

- **Type:** layout
- **Source:** authored 2026-10-09 for Hub/Ledger completion
- **Files:** `hub-shell.css`, `specimen.html`
- **Dependencies:** tokens.css
- **States:** `.rail-collapsed` on `.shell` (desktop collapse per hub-rail convention: `grid-template-columns: 0 minmax(0,1fr)`, rail slides off), `.rail-open` on `.shell` (mobile off-canvas rail in), `:hover`/`:active` on `.shell-rail-toggle` (scale + rotate, purple glow), responsive `@media` (≤760px), `prefers-reduced-motion` (ambient layer + breathe disabled)
- **Notes:**
  - Defines the base `.shell` grid parent that `layout/hub-rail`'s `.shell.rail-collapsed` convention expects — pair them, don't duplicate the collapse rules.
  - The ambient layer is `position:fixed`, `z-index:0`, `pointer-events:none` — decorative only, never interactive.
  - `color-mix` is used for translucent topbar/rail grounds; older engines fall back to the `--bg`/`--bg-panel` base.
  - Dock slot pairs with `layout/eco-dock` (the dock owns its own fixed positioning and safe-area padding).

## Use it

1. Copy `hub-shell.css` next to your page.
2. Link `tokens.css` first, then `hub-shell.css`.
3. Structure the page on the grid; fill the slots; wire the toggle:

```html
<div class="shell">
  <div class="shell-ambient" aria-hidden="true">
    <div class="shell-wash w1"></div><div class="shell-wash w2"></div><div class="shell-wash w3"></div>
    <span class="shell-mote m1"></span><span class="shell-mote m2"></span>
    <span class="shell-mote m3"></span><span class="shell-mote m4"></span>
  </div>

  <header class="shell-topbar">
    <a class="shell-brand" href="#/">
      <span class="shell-jewel"></span>
      <span class="shell-wordmark">NAYA</span>
    </a>
    <p class="shell-line">Your intelligence, at work.</p>
    <div class="shell-topbar-actions">
      <button class="shell-rail-toggle" type="button" aria-label="Toggle rail" aria-expanded="true">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
      </button>
    </div>
  </header>

  <aside class="shell-rail" aria-label="Navigation rail">
    <!-- rail content goes here -->
  </aside>

  <main class="shell-outlet">
    <!-- page content goes here -->
  </main>

  <div class="shell-dock">
    <!-- layout/eco-dock goes here -->
  </div>
</div>

<script>
document.querySelector('.shell-rail-toggle').addEventListener('click', (e) => {
  const shell = document.querySelector('.shell');
  const btn = e.currentTarget;
  if (matchMedia('(max-width:760px)').matches) {
    const open = shell.classList.toggle('rail-open');
    btn.setAttribute('aria-expanded', String(open));
  } else {
    const collapsed = shell.classList.toggle('rail-collapsed');
    btn.setAttribute('aria-expanded', String(!collapsed));
  }
});
</script>
```

## Selectors

```
.shell
.shell.rail-collapsed
.shell.rail-open
.shell-ambient
.shell-wash (+ .w1 / .w2 / .w3)
.shell-mote (+ .m1–.m4)
.shell-topbar
.shell-brand
.shell-wordmark
.shell-jewel
.shell-line
.shell-topbar-actions
.shell-rail-toggle (+ svg / :hover / :active)
.shell-rail
.shell-rail-placeholder (+ b)
.shell-outlet
.shell-card (+ h3 / p / .shell-card-kicker)
.shell-dock
.shell-dock-placeholder
```
