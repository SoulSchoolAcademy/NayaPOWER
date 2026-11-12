# Smart Block: `lv-btn`

The living button. 7-layer stack, cursor sheen, soul core, proximity aware.

## Why

The most advanced button code: seven shadow layers, cursor sheen that follows the pointer, a soul core, wakes at 160px proximity. An action with a spectrum identity should feel like it notices you. Use for signature actions where the interface itself is the delight.

- **Type:** buttons
- **Source:** `Naya_5_Beautiful_Button_set.html` (extracted byte-true, never rewritten)
- **CSS:** `lv-btn.css`
- **Specimen:** `specimen.html`
- **States found:** :hover, :active, :focus, :focus-visible, :disabled
- **Dependencies:** lv-btn.js, tokens.css

## Use it

1. Include `tokens.css` (once per page).
2. Include `lv-btn.css`.
3. Copy the HTML from `specimen.html`.
4. Include `lv-btn.js` for interactive behavior.

## Selectors in this block

```
.lv-btn
.lv-btn .lv-label
.lv-btn .lv-label svg
.lv-btn, .lv-btn::after
.lv-btn--danger
.lv-btn--danger:hover, .lv-btn--danger:focus-visible
.lv-btn::after
.lv-btn::before
.lv-btn:active
.lv-btn:active::after
.lv-btn:disabled
.lv-btn:focus-visible
.lv-btn:hover, .lv-btn:focus-visible
.lv-btn:hover::after, .lv-btn:focus-visible::after
.lv-btn:hover::before, .lv-btn:focus-visible::before
.lv-wrap.lv-aware .lv-btn
.lv-wrap.lv-aware .lv-btn::after
.lv-wrap.lv-aware .lv-btn::before
```
