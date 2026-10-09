# `li-ekg`

Live pulse/heartbeat line: full-bleed SVG EKG trace with a dim base path, a glowing gradient flow path (`liflow` dash animation), and a traveling dot (`animateMotion`).

- **Type:** data
- **Source:** `Ledger Page Design.html` (specimen reconstructed from the hero's SVG builder; `{{ekg-path}}` is generated at runtime by `ekgPath(W,H,7)` — a 7-beat trace across the viewBox)
- **Files:** `li-ekg.css`, `specimen.html`
- **States:** continuous `liflow` 9s dash-flow animation, `prefers-reduced-motion`
- **Dependencies:** `tokens.css` (none required — gradient stops are hardcoded; `.li-ekg-flow` references `url(#li-ekg-grad)` which the specimen's `<defs>` provides)
- **Overlap note:** no indexed block duplicates this.

## Use it

```html
<div class="li-stage">
  <svg class="li-ekg" viewBox="0 0 1200 220" preserveAspectRatio="none">
    <defs>
      <linearGradient id="li-ekg-grad" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0" stop-color="#a855f7"/><!-- … full 10-stop spectrum in specimen … --><stop offset="1" stop-color="#ec4899"/>
      </linearGradient>
    </defs>
    <path class="li-ekg-base" d="{{ekg-path}}"/>
    <path class="li-ekg-flow" d="{{ekg-path}}"/>
    <circle class="li-ekg-dot" r="7">
      <animateMotion dur="9s" repeatCount="indefinite" path="{{ekg-path}}"/>
    </circle>
  </svg>
</div>
```

## Selectors

```css
.li-stage .li-ekg
.li-stage .li-ekg-base
.li-stage .li-ekg-flow
.li-stage .li-ekg-dot
@keyframes liflow
@media (prefers-reduced-motion: reduce)
```
