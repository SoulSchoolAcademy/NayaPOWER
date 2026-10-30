# Smart Block: `chat/cht-bubbles`

Atomic chat bubbles: incoming white-lit left, outgoing purple-edged right, tails, grouped collapse, honest transport-driven read receipts, and an edited honesty tag.

## Why

The atomic message object: incoming on the left (dark board, white-lit edge), outgoing on the right (purple-ignited edge), a tail that points the way the words came from. Consecutive messages from one sender collapse into a group — one avatar, one timestamp, no repeated faces. Read receipts are honest truth-states: sent, delivered, read — and "read" is never shown before the other side renders.

**Do / Don't** — Do: render receipts only from the transport's truth — the block displays states, it never invents them; `setReceipt` is the single writer of `data-state`. Don't: ever show "read" because the message is old, because the app was backgrounded, or because it looks better — a fake read is a trust violation with styling, and this family has exactly one unforgivable sin.

- **Type:** chat
- **Catalog:** NAYA-CHT-003
- **Source:** `gap-blocks-2/chat-blocks.md` (harvested, never restyled)
- **CSS:** `block.css`
- **JS:** `block.js`
- **Specimen:** `specimen.html`
- **States found:** `.chat-row:hover .chat-bub.in` (lift 2px, white ignition), `.chat-row:hover .chat-bub.out` (lift 2px, purple ignition), `.chat-bub:active` (settle 1px), `.chat-row.grp` (avatar hidden, corners tightened, tail suppressed), `.chat-ticks[data-state="sending"|"sent"|"delivered"|"read"]` (gold SEEN on read), `.chat-edited` (italic honesty tag), `@media (prefers-reduced-motion:reduce)` (no motion)
- **Dependencies:** none — self-contained

## Use it

1. Include `block.css`.
2. Include `block.js` — `chatReceipt(el, state)` is the ONLY writer of `data-state` ("sending" → "sent" → "delivered" → "read", forward only). Group runs: same sender <5 min apart get `.grp`, first gets `.grp-first`.

## Selectors in this block

```
.chat
.chat-row
.chat-row.out
.chat-ava
.chat-ava.in
.chat-bub
.chat-bub.in
.chat-bub.out
.chat-bub.in::after
.chat-bub.out::after
.chat-row:hover .chat-bub.in
.chat-row:hover .chat-bub.out
.chat-bub:active
.chat-row.grp
.chat-row.grp .chat-ava
.chat-row.grp .chat-bub.in
.chat-row.grp-first .chat-bub.in
.chat-row.grp-first .chat-bub.out
.chat-row.grp .chat-bub.in::after
.chat-row.grp .chat-bub.out::after
.chat-meta
.chat-row.out .chat-meta
.chat-name
.chat-time
.chat-ticks
.chat-ticks svg
.chat-ticks[data-state="sending"] svg
.chat-ticks[data-state="sent"] svg
.chat-ticks[data-state="delivered"] svg
.chat-ticks[data-state="read"] svg
.chat-ticks[data-state="read"]::after
.chat-ticks .sr
.chat-edited
```

## Notes

- Anatomy (from the source spec): - **Row:** flex line, avatar + bubble, `align-items:flex-end`. Outgoing rows reverse; the column edge is the speaker's edge. - **Avatar orb:** 36px lit jewel orb in Law 4's language — white-hot crown fading through the speaker's tone to black. Incoming orbs wear blue, outgoing wear purple: the tone follows the speaker's edge. In grouped rows the orb hides but keeps its space. - **Bubble:** the unit. 15px/1.5 line-height text (never smaller — chat is read at a glance, in motion), 11px × 15px …
