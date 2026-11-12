# forms/color-picker

Swatch grid + custom hex color picker in Naya's design language. Eleven gem swatches (magenta, soul purple, blue, green, gold, teal, coral, lime, indigo, white, black) — each a radial gem with a machined edge. Selected swatch gets a 3px white ring plus its own color-glow halo. Type a hex and press Enter to mint a custom swatch with a computed gem gradient.

**Type:** Smart Block (form control)
**Source:** Designed 2026-10-09 in Naya design language — gap build, not extraction

## CSS
`color-picker.css` — scoped `.cp-` selectors; shared tokens in `:root`, commented.

## JS
`color-picker.js` — swatch selection, custom hex validation (`#abc` / `aabbcc` accepted, invalid flashes a red edge), gem-gradient computation for custom swatches, readout update, `cp-change` bubbling event with `{name, hex}` detail. Runs on any `[data-cp]` root.

## Specimen
`specimen.html` — working demo on `#050507`: live grid with Soul Purple pre-selected, custom hex input, event readout showing the `cp-change` detail.

## States
- **Rest:** 44px gem circles, 12px gaps, hover scales 1.1.
- **Selected:** 3px white ring + color glow halo.
- **Custom:** hex pill input (mono 14px), Enter mints a swatch with computed gradient; invalid hex flashes a red edge.
- **Focus-visible:** purple ring.
- **Readout:** selected name 18px/700 + hex 14px mono secondary.

## Dependencies
- `tokens.css` (shared design tokens — duplicated in `:root` per spec, commented as shared)
- No external libraries.

## Use it
1. Include `color-picker.css` and `color-picker.js` on the page.
2. Wrap the block in an element with `data-cp`.
3. Add `.cp-readout` (`.cp-name` + `.cp-hex`), a `.cp-grid` of `.cp-swatch` buttons — each swatch needs `data-name`, `data-hex`, and inline `--cp-hi/--cp-c/--cp-lo/--cp-glow` gem stops.
4. Add `.cp-custom` with a `.cp-hex-input` for custom colors.
5. Listen for `cp-change` on the root for `{name, hex}`.

## Selectors
```css
.cp-wrap            /* 420px max container */
.cp-readout         /* readout stack */
.cp-name            /* selected name 18px/700 */
.cp-hex             /* selected hex 14px mono */
.cp-grid            /* swatch grid */
.cp-swatch          /* 44px gem circle */
.cp-swatch.cp-selected
.cp-custom          /* custom row */
.cp-hex-input       /* hex pill input */
.cp-hex-input.cp-invalid
.cp-custom-label
```
