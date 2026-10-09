# Smart Block: `chat/sp-chat`

Space chat message list, chat composer (text input + mic + send), and post composer (textarea + schedule + post button).

## Why

Conversation needs both a floor and a door. The message list and composer handle the talk; the post composer with scheduling handles the saying-to-everyone. Same surface, both modes.

- **Type:** chat
- **Source:** `Smart Spaces Page Design.html` (extracted byte-true, never rewritten)
- **CSS:** `block.css`
- **JS:** `block.js`
- **Specimen:** `specimen.html`
- **States found:** `.sp-composer-ta:focus`, `.sp-composer-ta::placeholder`, `.sp-sched-btn.set`, `.sp-post-btn:hover`, `.sp-chat-ti:focus`, `.sp-chat-send:hover`, `.sp-mic-btn:hover`, `.sp-mic-btn.rec`, `@keyframes sppulse` (recording pulse)
- **Dependencies:** `--sc` (space accent, used by `.sp-mic-btn:hover`; set via `opts.accent`)

## Use it

1. Include `block.css`.
2. Include `block.js`.
3. Call `spChatList(messages, opts)` / `spChatComposer(opts)` / `spPostComposer(opts)` and append the returned element.

## Selectors in this block

```
.sp-empty
.sp-composer
.sp-composer-ta
.sp-composer-ta:focus
.sp-composer-ta::placeholder
.sp-composer-row
.sp-sched-btn
.sp-post-btn
.sp-sched-btn.set
.sp-post-btn:hover
.sp-chat-list
.sp-chat-msg
.sp-chat-body
.sp-chat-head
.sp-chat-name
.sp-chat-time
.sp-chat-text
.sp-chat-input
.sp-chat-ti
.sp-chat-ti:focus
.sp-chat-send
.sp-chat-send:hover
.sp-mic-btn
.sp-mic-btn:hover
.sp-mic-btn.rec
@keyframes sppulse
```

## Notes

- `avatar()` from the source was replaced by a minimal inline-styled initial-letter circle, since the `sp-ava` class has no CSS in this block's stylesheet. Same visual role, zero external dependency.
- The `sp-local-note` element ("Voice messages are stored on this device only.") from `renderChatTab` was dropped: it has no CSS rule in this block's stylesheet and would render as unstyled text.
- The schedule picker (`openSchedulePicker`) from `renderPostsTab` is outside this block's scope; the Schedule button accepts an `onSchedule(current, setFn)` callback, otherwise toggles a standalone scheduled state.
- Recording is not implemented here: the mic button exposes `onMic(btn)`. Playback of voice messages belongs to `chat/sp-audio-msg`; `spChatMsg` hands audio messages off to `window.spAudioMsg` when that block is loaded, else falls back to a text label.
- Builders: `spChatList`, `spChatMsg`, `spChatAppend`, `spChatComposer`, `spPostComposer`.
