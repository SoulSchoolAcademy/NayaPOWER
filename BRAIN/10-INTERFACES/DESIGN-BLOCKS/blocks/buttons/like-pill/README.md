# Smart Block: `like-pill`

Like pill — heart counter that ignites red (`.on`) with text-shadow glow when liked.

- **Type:** buttons
- **Source:** `Naya Beautiful Button Set N4.html`
- **Files:** `like-pill.css`, `specimen.html`, `like-pill.js`
- **Dependencies:** tokens.css
- **States:** :hover, .on, .lv-aware

## Use it

1. Copy `like-pill.css` (and `like-pill.js` if present) next to your page.
2. Link `tokens.css` first, then `like-pill.css`.
3. Paste the markup from `specimen.html` (set the `--` variables shown to theme it).
4. Wire the JS (`like-pill.js`) — it is byte-true and self-initializing.

## Selectors

```
.like-pill
.like-pill:hover
.like-pill.on
.seg-tab
.act-chip
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
