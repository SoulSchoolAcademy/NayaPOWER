# Smart Block — forms/range-slider

Inset 8px track with a purple→magenta glowing fill, a white-hot machined thumb, and a floating value bubble. Drag with pointer or drive with the keyboard.

- **Type:** form control · input
- **Source:** Designed 2026-10-09 in Naya design language — gap build, not extraction
- **CSS:** `range-slider.css` (scoped `.rs-*`)
- **JS:** `range-slider.js` (pointer drag, arrows/PageUp/PageDown/Home/End, fill + bubble + readout sync)
- **Specimen:** `specimen.html`

## States
- Idle (purple fill, halo thumb)
- Drag (thumb scales 1.15, glow intensifies)
- Keyboard focus (purple ring on thumb)
- Bubble follows thumb, shows current value live

## Dependencies
- `tokens.css` shared tokens (inlined at top of `range-slider.css`, commented "shared")

## Use it
1. Use the `.rs-root` markup: `.rs-bubble`, `.rs-track` (containing `.rs-fill` + `.rs-thumb`), and a hidden native `.rs-input` for assistive tech.
2. Set `data-min`, `data-max`, `data-step`, `data-value`, and `data-suffix` on `.rs-root`.
3. Include `range-slider.css` and `range-slider.js`.
4. Listen for the `rs-change` event (`event.detail.value`) to sync external readouts.

## Selectors
```css
.rs-root    /* wrapper; data-min/max/step/value/suffix */
.rs-track   /* 8px inset track */
.rs-fill    /* purple→magenta glowing fill */
.rs-thumb   /* 26px white-hot thumb; .rs-drag = dragging */
.rs-bubble  /* floating value pill above thumb */
.rs-input   /* hidden native input (a11y + keyboard) */
.rs-value   /* optional external readout text */
```
