# Smart Block: `lists/sp-blockrow`

Block list row with title + uppercase category label — the "pin an Intelligent Block" picker list.

- **Type:** lists
- **Source:** `Smart Spaces Page Design.html` (extracted byte-true, never rewritten)
- **CSS:** `block.css`
- **JS:** `block.js`
- **Specimen:** `specimen.html`
- **States found:** row (default, hover); list container scrolls (max-height 50vh); optional action button active/inactive (source: Pin / ✓ Pinned)
- **Dependencies:** none (no CSS vars; category label color is hard-coded `#7c3aed` in block.css). The optional action button uses `sp-pin-act`, styled by a sibling block (see Notes).

## Use it

1. Include `block.css`.
2. Include `block.js`.
3. Call `spBlockList([{title, category, action}])` and append the returned element. `category` is rendered upper-cased. `action` is optional: `{label, active, onClick}` — emitted as the source's `sp-pin-act` button; `active` renders the `on` state and disables the click.

## Selectors in this block

```
.sp-blocklist
.sp-blockrow
.sp-blockrow-t
.sp-blockrow-c
```

## Notes

- Source drives the rows from `SEED_BLOCKS` and the pin button from `spacePins`/`pinBlock()` app state; the builder takes plain `{title, category}` items and an optional per-item `action` param instead.
- The action button's `sp-pin-act` class has no rule in this block's CSS (it's styled by a sibling block); the specimen includes specimen-only styling so the demo renders.
