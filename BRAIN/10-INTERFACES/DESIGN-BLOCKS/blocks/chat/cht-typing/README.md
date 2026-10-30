# Smart Block: `chat/cht-typing`

Typing indicator: three dots breathing at 72bpm with quarter-beat stagger, rendered only with a live signal id; a non-negotiable 30s watchdog dismisses them otherwise.

## Why

Three living dots in a bubble shell: the calm heartbeat of someone about to speak. It pulses at 72bpm, staggers softly, and — this is the whole point — it exists **only while a live signal says someone is typing**. No signal, no dots. And it carries a contract: 30 seconds with no keep-alive and no message, and it dismisses itself honestly — replaced by the message that arrived, or simply gone.

**Do / Don't** — Do: require a live signal id for every render — the `throw` in `show()` is the law in code: no signal, no dots, no exceptions. Don't: keep the indicator alive to look responsive while the other side went quiet; after 30 seconds the honest answer is absence, not persistence. A typing indicator that outlives the typist is a ghost with styling.

- **Type:** chat
- **Catalog:** NAYA-CHT-004
- **Source:** `gap-blocks-2/chat-blocks.md` (harvested, never restyled)
- **CSS:** `block.css`
- **JS:** `block.js`
- **Specimen:** `specimen.html`
- **States found:** `live (quarter-beat stagger, breath travels left → right)`, `watchdog expiry (fades, unmounts, fires `chat:typing-expired`)`, `message arrival (replaced by the real message)`, `@media (prefers-reduced-motion:reduce)` (three steady dots, 85% opacity)
- **Dependencies:** none — self-contained

## Use it

1. Include `block.css`.
2. Include `block.js` — `chatTyping.show(el, signalId)` requires a live transport signal id (throws without one); `chatTyping.keepalive(id)` re-asserts; `chatTyping.arrived(id)` swaps the dots for the real message.

## Selectors in this block

```
.chat
.chat-typing
.chat-typing .chat-ava
.chat-dots
.chat-dots i
.chat-dots i:nth-child(2)
.chat-dots i:nth-child(3)
0%
100%
50%
.chat-typing .who
.chat-typing[hidden]
@keyframes chat-breathe
```

## Notes

- Anatomy (from the source spec): - **Shell:** the incoming bubble's geometry — same dark gradient, same white-lit edge, same left tail — so the dots read as *Sam's* unfinished sentence, in Sam's place. - **Dots:** three 9px white orbs, Law-4 glow. The stagger is a quarter-beat walk — 0, .208s, .416s — so the pulse travels left to right like a breath, never a flicker. - **The heartbeat:** `--bpm:0.833s` — 72 beats per minute, the resting human pulse. Frantic is forbidden: nothing in this block animates faster than one beat. - …
