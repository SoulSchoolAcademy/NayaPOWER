# The Jewel Icon Set — Usage Spec

**Maker round 2026-11-24, fix round 2026-11-24 · 55 icons · branch `jewel-icon-set-20261124` · nothing live.**

Our own custom icon set, unique to NayaNET — judged against the emblem
(`~/workspace/user/media_library/image/NAYA_ICON.png`: the purple diamond
jewel in a silver winged crown frame). Every icon is a real jewel: obsidian
disc inside, silver bezel (the emblem's frame), white glyph as a real object
with depth, the icon's own deep colour as rim + outside halo + a faceted
crown jewel set at 12 o'clock. One light, top-left, always. Slow orbit ring
(60–180s, alternating direction) built into every full icon. **One
construction, everywhere — the emoji faces are the white glyph on the same
obsidian disc, never a coloured fill inside.**

## Files

All files live in this folder (`maker/`), filed to GitHub under
`TEAM-NITRO/jewel-icon-set-20261124/` on branch `jewel-icon-set-20261124`.

| Path | What |
|---|---|
| `icons/core/*.svg` (12) | The core messaging set — mail, chat, audio, video, search, compose, send, plus, contacts, lists, spaces, settings |
| `icons/presentation/*.svg` (12) | Message-presentation jewels + bottom-bar extras — naya-mark, type-chat, type-mail, type-post, react-heart, react-star, react-sparkle, bar-activity, bar-ecosystem, bar-connect, bar-add, bar-worlds |
| `icons/presentation/*-sm.svg` (7) | Small variants of the presentation jewels (48px art) — for inside message bubbles at 16–24px: naya-mark-sm, type-chat-sm, type-mail-sm, type-post-sm, react-heart-sm, react-star-sm, react-sparkle-sm |
| `icons/emoji/*.svg` (12) | The emoji set — smile, laugh, love, wow, think, cool, sad, party, peace, fire, thumbs-up, star |
| `icons/emoji/*-sm.svg` (12) | Small variants of the emoji (48px art) — for reaction rows at 16–24px: smile-sm, laugh-sm, love-sm, wow-sm, think-sm, cool-sm, sad-sm, party-sm, peace-sm, fire-sm, thumbs-up-sm, star-sm |
| `jewel-icons.css` | The touch contract: hover lift + ignite, press depress, size classes |
| `showcase.html` | The staged proof page — self-contained (all icons + CSS inlined, so it renders on the proof host as linked) |
| `showcase-template.html` | The human-editable showcase source (relative `<img>` refs); re-run `node build-showcase-inline.mjs` after editing it |
| `build-showcase-inline.mjs` | Builds the staged showcase from the template by inlining every SVG + the CSS |
| `build-jewel-icons.mjs` | The generator — every SVG comes from one construction; edit here, re-run with `node build-jewel-icons.mjs` |
| `USAGE.md` | This file |

## Colours (deep palette only — one hex per hue, everywhere)

| Icon | Colour | Hex |
|---|---|---|
| mail | Sapphire blue | `#0f52ba` |
| chat | Royal purple | `#8e24aa` |
| audio | Deep emerald | `#07925f` |
| video | Deep gold | `#d4a017` |
| search | Burnt orange | `#c2410c` |
| compose | Ruby red | `#c62828` |
| send | Deep magenta | `#a21caf` |
| plus | Deep indigo | `#3f51b5` |
| contacts | Deep cyan | `#0e7490` |
| lists | Deep violet | `#6d28d9` |
| spaces | Royal purple | `#8e24aa` |
| settings | Sapphire blue | `#0f52ba` |

Message-type colours follow the dial: **Chat purple, Mail gold, Post violet.**
Bottom bar, fixed everywhere: ADD purple · MAIL blue · ACTIVITY green ·
WORLDS gold · ECOSYSTEM orange · CONNECT red. Never the same colour twice
in a row — the spectrum cycles; nobody picks a colour by taste. The bar
uses baked variants for the two slots whose core colour differs:
`bar-add.svg` is the plus in royal purple `#8e24aa` (core `plus.svg` is
indigo) and `bar-worlds.svg` is the globe in deep gold `#d4a017` (core
`spaces.svg` is purple) — a `--c` wrapper cannot recolour a baked SVG.

## Emoji colours (deep palette only — one hex per hue, everywhere)

| Emoji | Colour | Hex |
|---|---|---|
| smile | Deep gold | `#d4a017` |
| laugh | Burnt orange | `#c2410c` |
| love | Ruby red | `#c62828` |
| wow | Royal purple | `#8e24aa` |
| think | Sapphire blue | `#0f52ba` |
| cool | Deep cyan | `#0e7490` |
| sad | Deep indigo | `#3f51b5` |
| party | Deep magenta | `#a21caf` |
| peace | Deep emerald | `#07925f` |
| fire | Burnt orange | `#c2410c` |
| thumbs-up | Deep violet | `#6d28d9` |
| star | Deep gold | `#d4a017` |

The emoji colour is the rim + halo + crown jewel only — the inside is
obsidian black, the face is white. Never a coloured fill inside.

## Small (`-sm`) inventory

- **Presentation (7):** naya-mark-sm, type-chat-sm, type-mail-sm,
  type-post-sm, react-heart-sm, react-star-sm, react-sparkle-sm.
- **Emoji (12):** smile-sm, laugh-sm, love-sm, wow-sm, think-sm, cool-sm,
  sad-sm, party-sm, peace-sm, fire-sm, thumbs-up-sm, star-sm.
- Small icons are 48×48 art, bolder glyph, thicker rim, crown jewel, no
  bezel, no orbit. Render at 16–48px. The emoji `-sm` face is the same
  face scaled half into the disc.

## Sizes

- **Full icons** are 96×96 art. Render at 24–96px (`jwl-96`, `jwl-72`,
  `jwl-64`, `jwl-48`, `jwl-32`, `jwl-24`).
- **Small (`-sm`) icons** are 48×48 art, bolder glyph, thicker rim, no
  bezel, no orbit. Render at 16–48px (`jwl-16`, `jwl-20`, `jwl-24`,
  `jwl-32`, `jwl-48`). These are the ones inside message bubbles.
- **Emoji** are 96×96 art. Render at 24–96px; the reaction row uses
  24px. Emoji `-sm` are 48×48 art for 16–24px reaction rows.

## How to consume

```html
<link rel="stylesheet" href="jewel-icons.css">

<!-- A button / tile icon -->
<span class="jwl jwl-64" style="--c:#0f52ba">
  <img src="icons/core/mail.svg" alt="Mail">
</span>

<!-- Inside a message bubble (no lift on hover — it is jewellery, not a button) -->
<span class="jwl jwl-inmsg jwl-20" style="--c:#8e24aa">
  <img src="icons/presentation/type-chat-sm.svg" alt="Chat">
</span>

<!-- A reaction row -->
<span class="jwl-reactions">
  <span class="jwl jwl-inmsg jwl-24" style="--c:#c62828">
    <img src="icons/presentation/react-heart-sm.svg" alt="Heart">
  </span>
</span>
```

Or inline the SVG directly (the file is self-contained: gradients, halo,
orbit animation and crown jewel all live inside it). Set `--c` to the
icon's own deep colour — that is what the hover light uses.

## The touch contract

- **Rest:** quiet but present — elevated, shadowed, real.
- **Hover:** the whole thing lifts (`translateY(-4px)`, scale 1.04) and
  lights whole in its own colour. The orbit keeps turning slowly.
- **Press:** it depresses (scale 0.97, 0.1s). A physical response, not a
  colour change.
- **In-message jewels** (`.jwl-inmsg`) do not lift on hover — they are the
  message's own jewellery.

## Do / don't

- **Do** use the `-sm` variants inside bubbles. Full icons below 24px
  lose the bezel detail.
- **Do** keep the icon's own colour for `--c`. The rim, halo, crown jewel
  and hover light are one colour — the icon's.
- **Don't** recolour an icon, flatten it, or strip the bezel. A flat
  version is not this set.
- **Don't** put two icons of the same colour next to each other. Cycle
  the spectrum.
- **Don't** use a system emoji where a jewel emoji exists. The jewel set
  is what makes a message read as ours.

## What is still owed

- Checker re-verification of the fix round (staged link rendered phone +
  desktop, 0 page errors) and the design-law check — dispatched by the
  captain.
- Captain's eye, then Shawn's eye — before anything goes live anywhere.
- Wiring into Messenger + Mail (the look round consumes this set; this
  round ships assets only, no page wiring).
- The spaces globe still reads as a leaf/eye at small sizes (harvested
  geometry) — a glyph redraw, not a colour fix; owed, not claimed fixed.
- The custom font (MEMORY.md point 8, ~19:15 MST) is a separate round,
  not this one.

## Count correction (checker, first round)

The first round's report claimed 48 `<img>` refs in the showcase. The
real count was 47 — the 48th is the escaped `<img
src="icons/core/mail.svg">` example inside the §5 text, not an image.
The fix-round template carries 59 real refs (47 + the 12 emoji `-sm`
row) plus that same escaped example. The staged showcase inlines all 59,
so it carries 0 external refs.
