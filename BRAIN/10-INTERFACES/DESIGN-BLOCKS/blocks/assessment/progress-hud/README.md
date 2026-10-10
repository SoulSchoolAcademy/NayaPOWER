# Smart Block: `assessment/progress-hud`

Assessment progress HUD: pill bar with location dot + label, animated track fill, and percent readout.

- **Type:** assessment
- **Source:** `Maxis App Design.html` (extracted byte-true, never rewritten)
- **CSS:** `block.css`
- **Specimen:** `specimen.html`
- **States found:** none (fill width set inline/by JS)
- **Dependencies:** `--ease` motion curve (define once per page)

> **Provenance note:** Maxis was Shawn's earlier MAXESS assessment project — not NayaNET. Only the UI grammar was extracted; no MAXIS branding or content is carried in this block.

## Use it

1. Include `block.css`.
2. Copy the HTML from `specimen.html`.
3. Update `.progress-fill` width and `.progress-percent` text as the user advances.

## Selectors in this block

```
.progress-hud
.progress-location
.progress-dot
.progress-label
.progress-track
.progress-fill
.progress-percent

```
