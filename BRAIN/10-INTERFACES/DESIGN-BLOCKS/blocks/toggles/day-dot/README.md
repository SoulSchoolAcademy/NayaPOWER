# Smart Block: `day-dot`

Day picker dot — 48px round selector; `.on` fills with a radial spectrum bloom.

- **Type:** toggles
- **Source:** `Naya Beautiful Button Set N4.html`
- **Files:** `day-dot.css`, `specimen.html`, `day-dot.js`
- **Dependencies:** tokens.css
- **States:** :hover, .on, .lv-aware

## Use it

1. Copy `day-dot.css` (and `day-dot.js` if present) next to your page.
2. Link `tokens.css` first, then `day-dot.css`.
3. Paste the markup from `specimen.html` (set the `--` variables shown to theme it).
4. Wire the JS (`day-dot.js`) — it is byte-true and self-initializing.

## Selectors

```
.day-dot
.day-dot:hover
.day-dot.on
.seg-tab
.like-pill
.act-chip
.tog-chip
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
