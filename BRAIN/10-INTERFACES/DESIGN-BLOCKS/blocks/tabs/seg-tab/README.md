# Smart Block: `seg-tab`

Segmented tab from room controls.

## Why

Segmented tab from room controls. When views are siblings, tabs beat navigation — one tap, no journey. Switching contexts feels weightless.

- **Type:** tabs
- **Source:** `Naya_5_Beautiful_Button_set.html` (extracted byte-true, never rewritten)
- **CSS:** `seg-tab.css`
- **Specimen:** `specimen.html`
- **States found:** :hover, .on
- **Dependencies:** seg-tab.js, tokens.css

## Use it

1. Include `tokens.css` (once per page).
2. Include `seg-tab.css`.
3. Copy the HTML from `specimen.html`.
4. Include `seg-tab.js` for interactive behavior.

## Selectors in this block

```
.seg-tab
.seg-tab, .like-pill, .act-chip, .tog-chip, .day-dot, .send-cta
.seg-tab.lv-aware, .like-pill.lv-aware, .act-chip.lv-aware, .tog-chip.lv-aware, .day-dot.lv-aware
.seg-tab.lv-aware::before, .like-pill.lv-aware::before, .act-chip.lv-aware::before,
.tog-chip.lv-aware::before, .day-dot.lv-aware::before, .send-cta.lv-aware::before
.seg-tab.on
.seg-tab.on::after, .like-pill.on::after, .act-chip.on::after, .tog-chip.on::after, .day-dot.on::after
.seg-tab::before, .like-pill::before, .act-chip::before, .tog-chip::before, .day-dot::before, .send-cta::before
.seg-tab:hover
```
