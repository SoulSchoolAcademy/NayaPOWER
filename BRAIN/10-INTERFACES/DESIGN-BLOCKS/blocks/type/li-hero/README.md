# `li-hero`

Living Intel hero: glass panel with breathing ambient glow, full-bleed EKG line, centered kicker with live dot, display title, sub-line, stat cluster, and simulated-live pill.

- **Type:** type
- **Source:** `Ledger Page Design.html` (specimen reconstructed from `LivingIntel()` HERO section; `{{ekg-path}}` generated at runtime)
- **Files:** `li-hero.css`, `specimen.html`
- **States:** `.li-flash` (1.1s entry ignite via `liflash`, toggled by JS on new beats), `@media(max-width:760px)`, `prefers-reduced-motion`
- **Dependencies:** `tokens.css`, `li-ekg` (`.li-ekg*` classes in the specimen), `li-card` (`.li-live-dot`), `li-stat` (`.li-stats` container + `.li-stat` row — the `.li-stats` container rule lives in this block's source section but is assigned to `li-stat` per the extraction map; the specimen links it)
- **Overlap note:** compared against indexed `hero` (`.naya-hero` — editorial serif headline, eyebrow kicker, CTA row, staggered entrance). `li-hero` is a different treatment: heartbeat EKG backdrop, live-dot kicker, stat cluster, simulated-live pill, `li-flash` ignite. Same job (page opening), different design language — extracted, not skipped.

## Use it

```html
<div class="li-stage">
  <section class="li-hero">
    <div class="li-glow"></div>
    <svg class="li-ekg" viewBox="0 0 1200 220" preserveAspectRatio="none">…gradient defs + base/flow/dot…</svg>
    <div class="li-hero-over">
      <p class="li-kicker"><span class="li-live-dot"></span><span> LIVING INTEL · LIVE</span></p>
      <h1 class="li-title">The heartbeat of it all</h1>
      <p class="li-sub">{{sub}}</p>
      <div class="li-stats">…li-stat rows…</div>
      <p class="li-sim"><span class="li-live-dot"></span><span> SIMULATED LIVE · demo beats arriving · flips to the real stream at launch</span></p>
    </div>
  </section>
</div>
```

## Selectors

```css
.li-stage .li-hero
.li-stage .li-glow
.li-stage .li-hero-over
.li-stage .li-kicker
.li-stage .li-title
.li-stage .li-sub
.li-stage .li-sim
.li-stage .li-hero.li-flash
@keyframes libreathe, lgpulse, liflash
@media(max-width:760px) → .li-stage .li-hero
@media (prefers-reduced-motion: reduce)
```
