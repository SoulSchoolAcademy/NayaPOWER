# Smart Block: `act-chip`

Action chip — small caps CTA pill (Share, Pin) with `.on` ignited state and proximity wake.

- **Type:** buttons
- **Source:** `Naya Beautiful Button Set N4.html`
- **Files:** `act-chip.css`, `specimen.html`, `act-chip.js`
- **Dependencies:** tokens.css
- **States:** :hover, .on, .lv-aware

## Use it

1. Copy `act-chip.css` (and `act-chip.js` if present) next to your page.
2. Link `tokens.css` first, then `act-chip.css`.
3. Paste the markup from `specimen.html` (set the `--` variables shown to theme it).
4. Wire the JS (`act-chip.js`) — it is byte-true and self-initializing.

## Selectors

```
.act-chip
.act-chip:hover
.act-chip.on
.seg-tab
.like-pill
.tog-chip
.day-dot
.send-cta
.seg-tab::before
.like-pill::before
.act-chip::before
.tog-chip::before
.day-dot::before
.send-cta::before
.seg-tab.lv-aware::before
.like-pill.lv-aware::before
.act-chip.lv-aware::before
.tog-chip.lv-aware::before
.day-dot.lv-aware::before
.send-cta.lv-aware::before
.seg-tab.lv-aware
.like-pill.lv-aware
.act-chip.lv-aware
.tog-chip.lv-aware
.day-dot.lv-aware
.seg-tab.on::after
.like-pill.on::after
.act-chip.on::after
.tog-chip.on::after
.day-dot.on::after
```
