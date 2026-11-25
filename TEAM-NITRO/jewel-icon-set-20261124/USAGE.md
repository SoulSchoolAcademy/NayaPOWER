# The Jewel Icon Set — Usage Spec

**Maker round 2026-11-24 · 41 icons · branch `jewel-icon-set-20261124` · nothing live.**

Our own custom icon set, unique to NayaNET — judged against the emblem
(`~/workspace/user/media_library/image/NAYA_ICON.png`: the purple diamond
jewel in a silver winged crown frame). Every icon is a real jewel: obsidian
disc inside, silver bezel (the emblem's frame), white glyph as a real object
with depth, the icon's own deep colour as rim + outside halo + a faceted
crown jewel set at 12 o'clock. One light, top-left, always. Slow orbit ring
(60–180s, alternating direction) built into every full icon.

## Files

All files live in this folder (`maker/`), filed to GitHub under
`TEAM-NITRO/jewel-icon-set-20261124/` on branch `jewel-icon-set-20261124`.

| Path | What |
|---|---|
| `icons/core/*.svg` (12) | The core messaging set — mail, chat, audio, video, search, compose, send, plus, contacts, lists, spaces, settings |
| `icons/presentation/*.svg` (10) | Message-presentation jewels + bottom-bar extras — naya-mark, type-chat, type-mail, type-post, react-heart, react-star, react-sparkle, bar-activity, bar-ecosystem, bar-connect |
| `icons/presentation/*-sm.svg` (7) | Small variants of the presentation jewels (48px art) — for inside message bubbles at 16–24px |
| `icons/emoji/*.svg` (12) | The emoji set — smile, laugh, love, wow, think, cool, sad, party, peace, fire, thumbs-up, star |
| `jewel-icons.css` | The touch contract: hover lift + ignite, press depress, size classes |
| `showcase.html` | The staged proof page — every icon at phone (390) and desktop, hover/active alive |
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
in a row — the spectrum cycles; nobody picks a colour by taste.

## Sizes

- **Full icons** are 96×96 art. Render at 24–96px (`jwl-96`, `jwl-72`,
  `jwl-64`, `jwl-48`, `jwl-32`, `jwl-24`).
- **Small (`-sm`) icons** are 48×48 art, bolder glyph, thicker rim, no
  bezel, no orbit. Render at 16–48px (`jwl-16`, `jwl-20`, `jwl-24`,
  `jwl-32`, `jwl-48`). These are the ones inside message bubbles.
- **Emoji** are 96×96 gem orbs. Render at 24–96px; the reaction row uses
  24px.

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

- Checker renders (phone 390 + desktop, 0 page errors) and the design-law
  check — dispatched by the captain.
- Captain's eye, then Shawn's eye — before anything goes live anywhere.
- Wiring into Messenger + Mail (the look round consumes this set; this
  round ships assets only, no page wiring).
