# Smart Block — forms/dropdown

Black pill trigger + obsidian option menu: chevron rotates 180° on open, purple edge ignites, selected option gets the purple left edge and a jewel checkmark.

- **Type:** form control · input
- **Source:** Designed 2026-10-09 in Naya design language — gap build, not extraction
- **CSS:** `dropdown.css` (scoped `.dd-*`)
- **JS:** `dropdown.js` (toggle, select, arrows, type-ahead, Escape/click-outside)
- **Specimen:** `specimen.html`

## States
- Closed trigger (chevron down, secondary)
- Open trigger (purple edge glow, chevron up in purple)
- Option hover (white text ignites, white left edge)
- Option selected (purple 3px left edge + purple jewel checkmark)

## Dependencies
- `tokens.css` shared tokens (inlined at top of `dropdown.css`, commented "shared")

## Use it
1. Use the `.dd-root` markup: `.dd-trigger` (label + chevron) and `.dd-menu` with `.dd-option` buttons.
2. Include `dropdown.css` and `dropdown.js`.
3. Mark the initial selection with `.dd-selected` on the option and matching `.dd-label` text.
4. Multiple instances on one page keep independent state.

## Selectors
```css
.dd-root      /* positioning wrapper */
.dd-trigger   /* 52px black pill; .dd-open = menu visible */
.dd-label     /* trigger label text */
.dd-chevron   /* rotates 180deg on .dd-open */
.dd-menu      /* obsidian panel; .dd-show = visible */
.dd-option    /* 52px row; .dd-hover = keyboard/hover focus, .dd-selected */
.dd-text      /* option label */
.dd-check     /* purple jewel checkmark */
```
