# data/accordion

Expanding content cards in Naya's design language. Each item is an 18px obsidian card with a 60px machined header (title 18px/700 left, jewel chevron right). Hover lifts the card; open adds a purple 3px left-edge accent, rotates the chevron 180°, and expands the body on a max-height animation.

**Type:** Smart Block (data display)
**Source:** Designed 2026-10-09 in Naya design language — gap build, not extraction

## CSS
`accordion.css` — scoped `.acc-` selectors; shared tokens in `:root`, commented.

## JS
`accordion.js` — toggle open/close, `data-single` attribute for one-open-at-a-time mode, animated height sized from live scrollHeight (re-seated on resize), `aria-expanded` state, `prefers-reduced-motion` instant toggle, `acc-toggle` event with `{open, item}`. Runs on any `[data-acc]` root.

## Specimen
`specimen.html` — working demo on `#050507`: multi-open stack with a pre-opened item, plus a `data-single` stack.

## States
- **Rest:** obsidian card, chevron jewel at rest.
- **Hover:** card lifts, hairline edges brighten.
- **Open:** purple 3px left edge accent, chevron rotated 180° with purple edge ignite, body expanded (16px/1.65 quiet white, 20px padding).
- **Focus-visible:** purple edge glow on the header button.
- **Single mode:** opening one item closes the others.

## Dependencies
- `tokens.css` (shared design tokens — duplicated in `:root` per spec, commented as shared)
- No external libraries.

## Use it
1. Include `accordion.css` and `accordion.js` on the page.
2. Wrap items in `.acc-stack` with `data-acc`; add `data-single` for one-open mode.
3. Each item: `.acc-item` > `.acc-head` (button with `.acc-title` + `.acc-chev`) + `.acc-body` > `.acc-body-inner`.
4. Pre-open an item by adding `acc-open` to `.acc-item`.
5. Listen for `acc-toggle` on the stack for `{open, item}`.

## Selectors
```css
.acc-stack          /* vertical item stack */
.acc-item           /* 18px obsidian card */
.acc-item.acc-open  /* open state + purple left edge */
.acc-head           /* 60px header button */
.acc-title          /* title 18px/700 */
.acc-chev           /* chevron jewel */
.acc-body           /* animated height container */
.acc-body-inner     /* 16px/1.65 body copy */
```
