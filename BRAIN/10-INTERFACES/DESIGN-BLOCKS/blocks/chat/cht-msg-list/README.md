# Smart Block: `chat/cht-msg-list`

Conversation room: bubbles day-grouped under serif dividers, stick-to-bottom only if the reader is already there, honest unread pill, empty/loading/presence states.

## Why

The conversation as a room: bubbles (CHT-003) day-grouped under serif date dividers, in a board that scrolls with an honest contract — it sticks to the bottom only if the reader is already there, and it never yanks a reading user. An empty room says so plainly: "No messages yet — say the first word."

**Do / Don't** — Do: measure `atBottom()` *before* the row lands — the decision to move belongs to the moment before the world changed, not after. Don't: smooth- scroll a reading user to the bottom "because something arrived"; yanking a reader mid-sentence is the chat equivalent of grabbing their book. The pill is the polite knock; the yank is the shove.

- **Type:** chat
- **Catalog:** NAYA-CHT-005
- **Source:** `gap-blocks-2/chat-blocks.md` (harvested, never restyled)
- **CSS:** `block.css`
- **JS:** `block.js`
- **Specimen:** `specimen.html`
- **States found:** `reader at bottom (new row appends, list glides to bottom)`, `reader up-list (list does not move; pill counts honestly)`, `reader scrolls home (bottom edge clears the pill)`, `.chat-empty` (purple jewel, "No messages yet"), `loading ("Loading your messages…", one line, never fake content)`, `presence ("3 here now" — live feed only, never a guess)`
- **Dependencies:** chat/cht-bubbles block.css (bubble shells, receipts, avatars)

## Use it

1. Include `block.css` AND `../cht-bubbles/block.css` (the list owns scroll/grouping; bubble shells belong to cht-bubbles).
2. Include `block.js` — `chatAppend(rowEl)` is the ONLY writer of new rows: sticks to bottom if within 64px, otherwise counts honestly on the pill. The presence line renders only from a live presence feed.

## Selectors in this block

```
.chat
.chat-list
.chat-head
.chat-head .chat-ava
.chat-head h2
.chat-head .presence
.chat-scroll
.chat-scroll::-webkit-scrollbar
.chat-scroll::-webkit-scrollbar-thumb
.chat-day
.chat-day::before
.chat-day::after
.chat-day span
.chat-day:first-child
.chat-new
.chat-new[hidden]
.chat-new:hover
.chat-new:active
.chat-new:focus-visible
.chat-new svg
.chat-new .n
.chat-empty
.chat-empty .jewel
.chat-empty h3
.chat-empty p
.chat-loading
.chat-loading i
```

## Notes

- The list owns scroll/grouping; bubble shells, receipts, and avatars belong to `chat/cht-bubbles` — include its `block.css` alongside this one (the specimen does).
- Anatomy (from the source spec): - **Board:** the room — 5-layer board shadow, 24px radius, tone under-glow. The room is the world; bubbles live inside it. - **Header:** the warm front door — 44px avatar orb, serif room name (20px), presence line. Full width of the board. - **Scroll region:** 480px tall, thin purple scrollbar. `tabindex="0"` so keyboard users can enter the list; the region is the conversation's body. - **Date divider:** serif voice chapter marks. The family's TYPE law at chat scale — the one place the calendar …
