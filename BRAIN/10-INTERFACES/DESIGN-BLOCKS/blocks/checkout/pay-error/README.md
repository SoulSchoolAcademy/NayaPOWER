# Smart Block: `checkout/pay-error`

Error state: calm red-tone board naming the cause in plain words, an honest next-step list, and a chrome-purple retry that disables while a retry is in flight.

## Why

**Law:** Law 1 (calm surfaces can still be alive — the retry button ignites, the panel breathes) · Law 2 (red = urgency, not alarm — an edge and a glow, never a flood, never flashing) · the plain-words law from PAY-002 validation (never blame the user).

**Do / Don't** — **DO** say "no money moved" before anything else. The user's first fear is the double-charge; kill it in the first sentence, then explain. **DON'T** show the raw processor code as the headline ("Error 402: card_declined") or paste a stack trace anywhere near the user. The reference code exists — small, monospace, at the bottom, for the bank call — but the panel speaks human first. And never, ever imply the user did something wrong: no "you entered," no "your fault," no red ✕ stamped over their card.

- **Type:** checkout
- **Catalog:** NAYA-PAY-004
- **Source:** `gap-blocks/checkout-blocks.md` (harvested, never restyled)
- **CSS:** `block.css`
- **Specimen:** `specimen.html`
- **States found:** `.pay-board:hover` (lift 5px, red edge brightens), `.pay-retry:active` (presses like every `.naya-btn`), `.pay-retry:disabled` (retry in flight — "Trying again…"), `.pay-receipt-jewel` (cause jewels in brand colors)
- **Dependencies:** none — self-contained

## Use it

1. Include `block.css` (self-contained: board shell + `.naya-btn` DNA + error styles).
2. Name the cause honestly in the headline; set the retry button `disabled` + label "Trying again…" while a retry is in flight.

## Selectors in this block

```
.pay-board
.pay-board:hover
.pay-corner
.pay-head
.pay-kicker
.pay-title
.naya-btn
.naya-btn:hover
.naya-btn:active
.naya-btn:focus-visible
.naya-btn:disabled
.naya-btn:disabled:hover
.pay-receipt-jewel
.pay-receipt-jewel[data-tone="magenta"]
.pay-receipt-jewel[data-tone="blue"]
.pay-receipt-jewel[data-tone="green"]
.pay-receipt-jewel i
.naya-btn--quiet
.naya-btn--quiet:hover
.pay-error
0%
100%
50%
.pay-error:hover
.pay-error .pay-corner
.pay-error-what
.pay-error-next
.pay-error-next li
.pay-error-next li:last-child
.pay-error-next strong
.pay-error-code
.pay-error-code code
.pay-error-actions
.pay-error-actions .naya-btn
.pay-retry
@keyframes pay-calm
```

## Notes

- The shared PAY board shell (Law 3 board formula) and the checkout-local `.naya-btn` DNA are carried into this block's CSS from PAY-001 so the family is self-contained — one include renders the whole board.
- `.pay-receipt-jewel` and `.naya-btn--quiet` are carried from PAY-003 for the same reason.
- Anatomy (from the source spec): - **The red:** an edge and a glow, at ~45% border strength, breathing. Red is urgency — "look at this" — not alarm. No flashing, no pulsing icons, no red flood. A panel that screams at a declined card teaches users to fear the checkout. - **"No money moved":** the load-bearing sentence. It is only rendered when the backend confirms no charge was created — the block never assumes it. If the charge state is genuinely unknown (timeout with no confirmation), the line reads "We're confirming with …
