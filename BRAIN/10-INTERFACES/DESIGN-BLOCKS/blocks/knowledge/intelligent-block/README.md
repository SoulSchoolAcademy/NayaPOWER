# Smart Block: `intelligent-block`

THE signature block of NayaNET. Header (jewel + kind + title + truth badge), the "in a nutshell" 4-layer answer, expandable jewel layers, provenance footer. Every knowledge surface composes this.

## Why

This is the signature: NayaNET’s whole promise in one block. Jewel header, truth badge, the four-layer ‘in a nutshell,’ expandable layers, provenance footer — knowledge you can trust because it shows its work.

- **Type:** knowledge
- **Source:** `Naya Smart Hub Design.html` (extracted verbatim, never rewritten)
- **CSS:** `intelligent-block.css`
- **Specimen:** `specimen.html`
- **States found:** .ib-layer-head.open, .ib-layer-play.playing, .ib-layer.is-deeper, :hover
- **Dependencies:** intelligent-block.js (layer toggle + play), tokens.css

## Use it

1. Include `tokens.css` (once per page).
2. Include `intelligent-block.css`.
3. Copy the HTML from `specimen.html`.
4. Include `intelligent-block.js` for layer expand/collapse.
5. Set `--tone` on `.ib-jewel` per layer color; truth badge via `.ib-truth`.

## Selectors in this block

```
.ib-blocktop
.ib-identity
.ib-jewel
.ib-title
.ib-subtitle
.ib-meta
.ib-truth
.ib-nutshell
.ib-nutshell-label
.ib-layers
.ib-layer
.ib-layer-head
.ib-layer-head.open
.ib-layer-body
.ib-layer-play
.ib-layer-play.playing
.ib-foot
.ib-state
.ib-id
.ib-layer.layer-purple/.ib-layer.layer-sapphire/... (12 tone variants)
```
