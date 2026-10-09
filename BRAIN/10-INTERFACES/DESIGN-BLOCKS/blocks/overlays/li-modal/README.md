# Smart Block: `overlays/li-modal`

Ledger detail modal — backdrop overlay, stat grid, explain paragraph, CLOSE button with full close plumbing (backdrop click, Escape, focus trap, focus restore).

## Why

Detail deserves focus. The ledger modal with backdrop, stat grid, and full close plumbing — backdrop click, Escape, focus trap and restore — means the deep view never traps anyone.

- **Type:** overlays
- **Source:** `Ledger Page Design.html` (extracted byte-true, never rewritten)
- **CSS:** `block.css`
- **JS:** `block.js`
- **Specimen:** `specimen.html`
- **States found:** open (limodal pop animation), CLOSE button hover / focus-visible, close on backdrop click, close on Escape, Tab focus trap inside dialog, focus restored to invoker on close
- **Dependencies:** `.li-stage` wrapper (base rule prepended into `block.css`; block is self-contained)

## Use it

1. Include `block.css`.
2. Include `block.js`.
3. Call `liModal({title, meta, stats:[[label,value],...], explain})` and append the returned element. Wrap page content in `.li-stage`.

## Selectors in this block

```
.li-stage
.li-stage .li-overlay
.li-stage .li-modal
.li-stage .li-modal-title
.li-stage .li-modal-meta
.li-stage .li-modal-stats
.li-stage .li-modal-stat
.li-stage .li-modal-stat + .li-modal-stat
.li-stage .li-modal-stat-l
.li-stage .li-modal-stat-v
.li-stage .li-modal-explain
.li-stage .li-modal-x
.li-stage .li-modal-x:hover
.li-stage .li-modal-x:focus-visible
@keyframes limodal
```

## Notes

- The source reused one module-level overlay (`overlay.style.display='flex'` to show). This builder creates one fresh overlay per `liModal()` call and returns it; closing hides it (`display:none`) and removes its listeners.
- Identity color defaults to `#a855f7` (source took the card's flow color via `fc`); pass `color` to pin it — it feeds `--ic` (modal glow) and `--tab-c` (CLOSE hover).
- The modal DOM keeps `.li-kicker` / `.li-live-dot` nodes byte-true, but their styling lives in a different extraction slice — this block's CSS does not style them. Same for the optional graph SVG (`graphSvg`) in source, which has no plain-data params here and is out of scope.
- Optional pass-throughs preserved from source: `source` (HEARTBEAT kicker label), `demo` (appends `· DEMO` to meta).
