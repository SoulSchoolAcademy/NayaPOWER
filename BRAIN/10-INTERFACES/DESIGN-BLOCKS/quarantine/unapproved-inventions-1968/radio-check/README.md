# Smart Block — forms/radio-check

Machined 24px radios and checkboxes over native inputs — CSS carries every visual, keyboard and assistive tech stay native.

- **Type:** form control · input
- **Source:** Designed 2026-10-09 in Naya design language — gap build, not extraction
- **CSS:** `radio-check.css` (scoped `.rc-*`)
- **JS:** `radio-check.js` (minimal — native inputs, CSS handles visuals; sets `data-rc-ready`)
- **Specimen:** `specimen.html`

## States
- Radio unchecked (dark center, machined border)
- Radio checked (12px purple dot + purple glow halo)
- Checkbox unchecked (dark, 7px radius)
- Checkbox checked (purple-tinted fill, white checkmark, purple edge glow)
- Hover row (subtle shift + box ignite)
- Focus-visible (purple ring on the box)

## Dependencies
- `tokens.css` shared tokens (inlined at top of `radio-check.css`, commented "shared")

## Use it
1. Wrap options in `.rc-group`; label the group with `.rc-grouplabel` (14px uppercase, letterspaced).
2. Each option: `<label class="rc-row rc-radio|rc-check">` containing a native `input`, a decorative `.rc-box`, and `.rc-text` (`.rc-label` 18px + `.rc-detail` 14px).
3. Radio groups share one `name`; checkboxes are independent.
4. Include `radio-check.js` (optional, tiny) or skip it — CSS works standalone.

## Selectors
```css
.rc-group       /* vertical stack, 16px gaps */
.rc-grouplabel  /* 14px/800 uppercase letterspaced group label */
.rc-row         /* option row; .rc-radio or .rc-check modifier */
.rc-box         /* 24px machined box (circle / 7px square) */
.rc-text        /* label stack */
.rc-label       /* 18px white option label */
.rc-detail      /* 14px secondary detail line */
```
