# NayaNET Smart Blocks

One canonical component library. Every block that earned its place — named, categorized,
and machine-readable so any builder (human or AI) can assemble elite pages from pieces.

## How to use

**AI / builder:** start at `manifest.json`. It lists all 58 blocks with:
- `id`, `category`, `css_classes`, `description`, `measures` (what it measures)
- `html_file` — the exact snippet file, e.g. `smart-blocks/buttons/buttons-canonical-button-naya-btn.html`
- `css_file` — the category CSS it needs, plus `needs` (full dependency list)
- `tier` — `canonical` (default pick), `alt` (earned 9+ variant), `new` (built for gaps)
- `use_when` — when to reach for it

Then read `recipes/`… (see `RECIPES.md` for the 7 page compositions) or `PAINT-JOB.md`
to repaint an existing page.

**Ground rules** (also in `manifest.json`): black ground only — never light mode;
text white 99%, hierarchy by size; buttons silver-white at rest, identity color on
interaction; color has three jobs (chrome / text / theme), never crossed; motion
encodes information, never decoration; every data instrument names what it measures.

## Layout

```
smart-blocks/
  manifest.json        <- the index. Start here.
  tokens.css           <- design tokens (colors, type, depth, motion)
  base.css             <- shared page root, type, ambient field
  naya-blocks.js       <- toast, tabs, palette, table sort, copy
  icons.svg            <- 40 vector glyphs (#i-name)
  buttons/ cards/ inputs/ navigation/ data/ overlays/ media/ specialty/ new/
    <category>.css     <- all CSS for that family
    <block-id>.html    <- the snippet, with a header naming its needs
  RECIPES.md           <- 7 page compositions (welcome, hub, ledger, spaces, mail, stats, maxis)
  PAINT-JOB.md         <- the repaint protocol
  REGISTRY.md          <- block registry with sources and drop reasons
```

## Rules for contributors

- Never invent a new button, card, or input. If no block fits, file the gap.
- One self-contained HTML file per delivered page. Verify from an empty folder.
- Shawn's eye is the final compiler.
