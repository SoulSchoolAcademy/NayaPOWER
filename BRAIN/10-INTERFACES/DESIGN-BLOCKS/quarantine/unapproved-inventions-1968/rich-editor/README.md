# forms/rich-editor

Markdown rich-text editor in Naya's design language. A 48px obsidian toolbar with 36px jewel buttons, an obsidian textarea (18px/1.6) that meets the toolbar with square top corners, and a rendered preview pane using the 24/18/14 typography scale. Write / Preview toggle pills sit top-right above the toolbar.

**Type:** Smart Block (form control)
**Source:** Designed 2026-10-09 in Naya design language — gap build, not extraction

## CSS
`rich-editor.css` — scoped `.re-` selectors; shared tokens in `:root`, commented.

## JS
`rich-editor.js` — toolbar inserts markdown at the cursor (bold, italic, heading, quote, list, link, code); Write/Preview tab switching; a small markdown → HTML renderer (headings 1–3, bold, italic, lists, quotes, inline code, fenced code, links); `re-change` event with the raw value; renderer exposed as `window.ReBlock.render`. Runs on any `[data-re]` root.

## Specimen
`specimen.html` — working demo on `#050507`: live editor with pre-filled content (flip to Preview), plus a second block forced to preview showing every rendered state at once.

## States
- **Write:** textarea focused, placeholder secondary white, toolbar buttons hover to white ignite; click flashes a purple edge on the used button.
- **Preview:** rendered pane — 24px h1, bold white, italic quiet, purple-edged blockquote, bulleted list with purple markers, inline code chips, fenced pre block, purple links.
- **Tabs:** active pill carries the purple edge glow.

## Dependencies
- `tokens.css` (shared design tokens — duplicated in `:root` per spec, commented as shared)
- No external libraries.

## Use it
1. Include `rich-editor.css` and `rich-editor.js` on the page.
2. Wrap the block in an element with `data-re`.
3. Add `.re-tabs` (two `.re-tab` buttons with `data-tab="write|preview"`), `.re-toolbar` (`.re-btn[data-act]` buttons; acts: `bold italic h quote list link code`), and `.re-body` containing `.re-area` (textarea) + `.re-preview` (div).
4. Read the value via the `re-change` event (`e.detail.value`) or the textarea directly.

## Selectors
```css
.re-wrap             /* full-width container */
.re-tabs             /* toggle row */
.re-tab / .re-tab.re-active
.re-toolbar          /* 48px obsidian bar */
.re-btn              /* 36px jewel button */
.re-btn.re-on        /* active purple edge flash */
.re-sep              /* toolbar divider */
.re-body             /* editor + preview frame */
.re-body.re-show-preview
.re-area             /* textarea */
.re-preview          /* rendered HTML pane */
```
