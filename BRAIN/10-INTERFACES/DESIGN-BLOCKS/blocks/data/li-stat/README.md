# `li-stat`

Stat cluster: glass number tiles (big tabular numeral + letterspaced label), used in the Living Intel hero.

- **Type:** data
- **Source:** `Ledger Page Design.html` (specimen reconstructed from the hero's stats builder; `data-ts` on the newest value drives a 30s live time-ago ticker)
- **Files:** `li-stat.css`, `specimen.html`
- **States:** none (static)
- **Dependencies:** `tokens.css` (none required — `--li-dim` is set on `.li-stage` in the source page; the specimen inherits it only if `.li-stage` styles are present — set `--li-dim:#a09a8a` inline if used standalone)
- **Overlap note:** no indexed block duplicates this (indexed `living-counter` is a count-up orb treatment, different component).

## Use it

```html
<div class="li-stage">
  <div class="li-stats">
    <div class="li-stat"><span class="li-stat-n">{{n}}</span><span class="li-stat-l">ITEMS FLOWING</span></div>
    <div class="li-stat"><span class="li-stat-n">{{n}}</span><span class="li-stat-l">SOURCES ALIVE</span></div>
    <div class="li-stat"><span class="li-stat-n" data-ts="{{ts}}">{{time-ago}}</span><span class="li-stat-l">NEWEST</span></div>
  </div>
</div>
```

## Selectors

```css
.li-stage .li-stats
.li-stage .li-stat
.li-stage .li-stat-n
.li-stage .li-stat-l
```
