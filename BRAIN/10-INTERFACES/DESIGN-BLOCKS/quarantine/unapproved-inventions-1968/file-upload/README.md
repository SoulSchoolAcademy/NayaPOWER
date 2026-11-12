# forms/file-upload

Drag & drop upload zone in Naya's design language. Obsidian dropzone with a dashed machined edge; on dragover the edge ignites solid purple and the jewel icon lifts. Each file becomes a 52px machined row with a spectrum-typed jewel, purple-glow progress bar, and a green check on completion.

**Type:** Smart Block (form control)
**Source:** Designed 2026-10-09 in Naya design language — gap build, not extraction

## CSS
`file-upload.css` — scoped `.fu-` selectors; shared tokens in `:root`, commented.

## JS
`file-upload.js` — drag/drop handlers, hidden file-input fallback, simulated upload progress, remove-file. Runs on any `[data-fu]` root; auto-boots on DOMContentLoaded.

## Specimen
`specimen.html` — working demo on `#050507`: live dropzone (drag files in or tap to browse), pre-seeded uploading + complete rows, dragover ignite state.

## States
- **Rest:** dashed 2px white .25 border, obsidian gradient, upload jewel, "Drop files here" 18px/700 + "or tap to browse" 14px secondary.
- **Dragover:** solid purple border, purple glow wash inside, icon lifts.
- **Uploading:** 52px row, spectrum jewel by type, name 16px, size 14px, 4px purple progress bar with glow.
- **Complete:** green ✓ jewel, progress bar hidden.
- **Focus-visible:** purple edge glow (keyboard accessible).

## Dependencies
- `tokens.css` (shared design tokens — duplicated in `:root` per spec, commented as shared)
- No external libraries.

## Use it
1. Include `file-upload.css` and `file-upload.js` on the page.
2. Wrap the block in an element with `data-fu`.
3. Add a `.fu-dropzone` containing a hidden `input[type="file"]`, `.fu-icon`, `.fu-title`, `.fu-hint`, followed by an empty `.fu-list`.
4. On `drop` or input `change`, rows are created and progress simulated — replace the simulator with a real upload callback.

## Selectors
```css
.fu-dropzone      /* dashed obsidian drop target */
.fu-dragover      /* ignite state during drag */
.fu-icon          /* 48px upload jewel */
.fu-title         /* "Drop files here" 18px/700 */
.fu-hint          /* "or tap to browse" 14px secondary */
.fu-list          /* file row stack */
.fu-row           /* 52px machined row */
.fu-row.fu-done   /* completed state (green check) */
.fu-type          /* spectrum jewel, data-type="img|doc|audio|video|zip|code" */
.fu-name / .fu-size
.fu-bar / .fu-fill/* 4px purple progress track + fill */
.fu-status        /* green ✓ jewel */
.fu-remove        /* × remove button */
```
