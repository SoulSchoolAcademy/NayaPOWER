# Smart Block: `checkout/pay-confirm`

Confirmation state: emerald-tone board, breathing hologram total, one gold ignition on processor success, receipt rows in the truth language (green ✓ = proven, gold ? = claimed).

## Why

**Law:** Law 1 (maximum life, minimum noise — one ignition, then a soft breathe) · Law 2 (emerald/green: alive and well) · the truth language (green ✓ = proven by the backend, gold ? = claimed, awaiting its stamp).

**Do / Don't** — **DO** make the paid amount the most beautiful number on the page — Georgia, hologram layers, one ignition, then breathe. This is the moment the user trusted you with money; the number should feel *held*, not just displayed. **DON'T** add confetti, coin bursts, or a "YOU DID IT!!!" modal. Maximum life, minimum noise. A payment confirmation is a receipt, not a birthday party — restraint is what makes the one ignition feel like something.

- **Type:** checkout
- **Catalog:** NAYA-PAY-003
- **Source:** `gap-blocks/checkout-blocks.md` (harvested, never restyled)
- **CSS:** `block.css`
- **Specimen:** `specimen.html`
- **States found:** `.pay-board:hover` (lift 5px, emerald ignition), `.pay-holo.is-ignited` (exactly one 1.1s gold ignition, then calm), `.pay-receipt-sent` (emerald ✓ — backend confirmed), `.pay-receipt-pending` (gold ? — claimed, awaiting stamp)
- **Dependencies:** none — self-contained

## Use it

1. Include `block.css` (self-contained: board shell + `.naya-btn` DNA + confirmation styles).
2. The integrator adds `.is-ignited` to `.pay-holo` exactly once on processor success. Receipt rows: `.pay-receipt-sent` (emerald ✓) or `.pay-receipt-pending` (gold ?).

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
.pay-confirm
.pay-confirm:hover
.pay-confirm .pay-corner
.pay-holo
.pay-holo-amount
.pay-holo.is-ignited .pay-holo-amount
0%
45%
100%
50%
.pay-holo-sub
.pay-receipt
.pay-receipt-row
.pay-receipt-row:last-child
.pay-receipt-jewel
.pay-receipt-jewel[data-tone="magenta"]
.pay-receipt-jewel[data-tone="blue"]
.pay-receipt-jewel[data-tone="green"]
.pay-receipt-jewel i
.pay-receipt-k
.pay-receipt-v
.pay-receipt-sent
.pay-receipt-pending
.pay-confirm-actions
.pay-confirm-actions .naya-btn
.naya-btn--quiet
.naya-btn--quiet:hover
@keyframes pay-ignite
@keyframes pay-breathe
```

## Notes

- The shared PAY board shell (Law 3 board formula) and the checkout-local `.naya-btn` DNA are carried into this block's CSS from PAY-001 so the family is self-contained — one include renders the whole board.
- Anatomy (from the source spec): - **Hologram amount:** Georgia 56px, four layers of shadow — top light, grounding, glow, far glow. "You look *into* the data, not *at* it." It breathes because numbers breathe (Law 1); it never blinks, spins, or dances. - **Charged-to line:** brand + last-4 only ("Visa ···· 4242") — the full number never appears here, per the PAY-002 privacy boundary. Last-4 arrives from the backend's masked response; the front end never truncates a PAN it shouldn't have. - **Receipt rows:** what / where (the …
