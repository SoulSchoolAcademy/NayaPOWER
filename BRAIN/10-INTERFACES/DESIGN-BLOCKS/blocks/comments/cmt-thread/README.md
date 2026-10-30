# Smart Block: `comments/cmt-thread`

Full comment thread: composer on top, replies nested to depth 3 under depth-color rails, per-comment collapse, "Continue thread" panel, tombstones, honest empty state.

## Why

The whole conversation: a composer on top, top-level comments below, replies nested under honest rails to depth 3, then a "Continue thread" panel for the rest. Collapse/expand per comment, plain-words timestamps, tombstones for the removed. Law 1: nothing dead — collapse chevrons lift, rails ignite on hover, the Post button is alive the moment there's something to say.

**Do / Don't** — Do: cap nesting at 3 and say so in the open — the "Continue thread" panel names the cap, so no one mistakes it for a bug. Don't: indent a fourth level "just this once"; one fake indent is a lie the whole thread inherits. Do: derive every timestamp from a real datetime in the markup — the plain-words label is a rendering of truth, not a substitute for it. Don't: write "just now" for anything older than a minute, and don't write "2 hours 14 minutes ago" for anything — precision you don't have is theater.

- **Type:** comments
- **Catalog:** NAYA-CMT-001
- **Source:** `gap-blocks-2/comments-blocks.md` (harvested, never restyled)
- **CSS:** `block.css`
- **JS:** `block.js`
- **Specimen:** `specimen.html`
- **States found:** `comment `:hover` (nesting rail ignites in depth color: magenta → purple → blue)`, `:active` (settle 1px), `:focus-visible` (white 2px ring on chevron, actions, Post, composer), `collapsed (kids hidden, chevron flips, honest "2 replies" count)`, `.cmt-more` ("Continue thread — 3 more replies", dashed, honest), `.cmt-tomb` (dashed edge, italic "This comment was removed."), `.cmt-empty` (jewel, "No comments yet"), `.cmt-edited` (quiet italic tag by the timestamp)
- **Dependencies:** none — self-contained

## Use it

1. Include `block.css`.
2. Include `block.js` — wires collapse chevrons, the continue-thread panel, love toggles, and the composer Post button (disabled until the box has text).

## Selectors in this block

```
.cmt
.cmt-thread
.cmt-compose
.cmt-field
.cmt-field::placeholder
.cmt-field:focus
.cmt-post
.cmt-post:hover:not(:disabled)
.cmt-post:active:not(:disabled)
.cmt-post:focus-visible
.cmt-post:disabled
.cmt-item
.cmt-av
.cmt-av b
.cmt-main
.cmt-head
.cmt-name
.cmt-time
.cmt-edited
.cmt-body
.cmt-actions
.cmt-act
.cmt-act svg
.cmt-act:hover
.cmt-act:hover svg
.cmt-act:active
.cmt-act:focus-visible
.cmt-act.is-on
.cmt-act.is-on svg
.cmt-love
.cmt-reply
.cmt-share
.cmt-kids
.cmt-item:hover>.cmt-kids
.cmt-kids.d1
.cmt-kids.d2
.cmt-kids.d3
.cmt-fold
.cmt-chev
.cmt-chev i
.cmt-chev[aria-expanded="false"] i
.cmt-chev:hover
.cmt-chev:focus-visible
.cmt-fold .n
.cmt-more
.cmt-more:hover
.cmt-more:focus-visible
.cmt-more svg
.cmt-deep
.cmt-deep[hidden]
.cmt-deep .cap
.cmt-tomb
.cmt-empty
.cmt-empty .jewel
.cmt-empty h3
.cmt-empty p
.cmt-sr
```

## Notes

- `.cmt-sr` (screen-reader-only) had no rule in the source; the block carries the registry's own 1px-clip sr rule (same as `chat/sp-chat`'s `.sr`).
- Anatomy (from the source spec): - **Composer:** the thread's front door — avatar jewel of the poster, dark field, 52px Post button. Post is disabled until there's text; your app wires the real submit and the server's receipt. - **Avatar jewel:** rotated diamond, white → tone → black radial, initials in serif, glow in the author's own stable color. The color is assigned once per author (hash of the display name) and never changes between renders — identity, not decoration. - **Name row:** serif display name (16px), plain-words …
