# Naya Design System — the Lego box

The one design language for NayaNET / NayaPOWER. Every Smart App, every Hub page, every room is built from these blocks. Nobody redesigns a button or a board ever again.

## The law (short version)

1. **Use the blocks.** `tokens.css` + the component library are the entire visual system. A page with a private button class is drift (Law 91).
2. **Block before app.** If the element you need has no block here, build the block first — with its states, do/don't, and screenshot — then build the app (Prime directive).
3. **Take the actual code.** Approved elements are copied verbatim into the library, never paraphrased from memory (Law 92).
4. **Score before showing Shawn.** Every page is scored on the 10 areas (Law 94). Floor 9.0 per area. Screenshots or it didn't happen (Law 95).

## What's here

| Path | What it is |
|---|---|
| `100-LAWS.md` | The canonical doctrine — all 100 laws, the acceptance checklist, the missing-blocks build order |
| `tokens.css` | The single token set: obsidian surfaces, neutrals, the spectrum in law order, type scale, elevation, motion, touch |
| `catalog.html` | The Lego box lid — browse every block in one page |
| `library/buttons/` | The button family source files (Elite Buttons N5, Button Set N4, the official Button Library standard N4) |
| `library/boards/` | Board and panel source files |
| `library/jewels/` | The Jewel Library N5 — jewels, badges, icon treatments |
| `library/blocks/` | The Lego block sets (Epic Elements N5, Lego Blocks N4, the Ultimate Design System) |
| `library/showcase/` | The Design Standard Showcase and the Design Contract v2 report |

## The canonical pieces (start here)

- **Button:** `.naya-btn` — one system, all variants derive from it (Laws 21–30). Source: `library/buttons/Naya_Design_Element_Set_N4.html` (the official standard).
- **Board:** the board recipe — obsidian body, theme-tinted hairline edge, white title, silver body, jewel kicker (Laws 31–40).
- **Spectrum:** assigned by position in reading order, never by category (Law 41). See `tokens.css` `--sp-*`.
- **Type:** white titles, silver body, slate detail; kicker 11px uppercase is the only colored text (Laws 51–52).

## Missing blocks (build order — Law: the library is not complete until these exist)

1. Input / form block · 2. Modal & dialog · 3. Toast / notification · 4. Data table · 5. Search interface · 6. Toggle / settings · 7. Content card · 8. Media player · 9. Chart / data-viz · 10. Smart Link / share sheet

Each new block ships with: code, states, do/don't example, screenshot. A block without a screenshot is a draft.

## For builders (including cold successors)

1. Read Laws 1–20 in `100-LAWS.md` before touching anything.
2. Link `tokens.css`. Use only canonical blocks.
3. Run the acceptance checklist. Screenshot desktop + mobile.
4. Score honestly per Law 94. Below 9.0 per area does not ship.

Corrections from Shawn become new laws or sharpened old ones — same day, in `100-LAWS.md` (Law 97).
