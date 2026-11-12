# Smart Block: `checkout/pay-order-summary`

Order summary board: line items with quantity steppers, one promo code, subtotal/tax/total rows, and one honest line so nobody feels tricked at the total.

## Why

**Law:** Law 3 (board formula, tone spine, corner jewel, 5px lift, own-tone ignition) · Law 1 (the total rests white, ignites gold — gold is attention, earned). Data-table law: labels left, numbers right.

**Do / Don't** — **DO** let the grand total be the one gold moment on the board — serif, earned, only on hover. The total is the final word of the page; it should feel like it. **DON'T** show a strike-through "original price" theater next to numbers you never charged. The honest microcopy line — *"Prices confirmed at checkout"* — is a promise, not decoration. If the backend can't confirm a price yet, say "Price loads at the next step" instead.

- **Type:** checkout
- **Catalog:** NAYA-PAY-001
- **Source:** `gap-blocks/checkout-blocks.md` (harvested, never restyled)
- **CSS:** `block.css`
- **Specimen:** `specimen.html`
- **States found:** `.pay-board:hover` (lift 5px, tone ignition), `.pay-item:hover` (lift 2px, own-tone ignition), `:active` steppers (compress 1px, scale .96), `:focus-visible` (2px white ring on steppers, input, buttons), `.pay-apply:disabled` (45% opacity, never ignites), `.pay-summary.is-empty` (quiet empty panel), `.pay-promo.is-applied` (emerald edge, confirmed line) / `.is-invalid` (red edge, plain-words error)
- **Dependencies:** none — self-contained

## Use it

1. Include `block.css` (self-contained: board shell + `.naya-btn` DNA + summary styles).
2. Toggle `.is-empty` for the empty panel, `.is-applied` / `.is-invalid` on `.pay-promo` for promo feedback.

## Selectors in this block

```
.pay-board
.pay-board:hover
.pay-corner
.pay-head
.pay-kicker
.pay-title
.pay-items
.pay-item
.pay-item[data-tone="magenta"]
.pay-item[data-tone="purple"]
.pay-item[data-tone="blue"]
.pay-item[data-tone="green"]
.pay-item[data-tone="gold"]
.pay-item:hover
.pay-thumb
.pay-thumb i
.pay-item-body
.pay-item-name
.pay-item-meta
.pay-stepper
.pay-step
.pay-step:hover
.pay-step:active
.pay-step:focus-visible
.pay-qty
.pay-price
.pay-promo
.pay-promo-label
.pay-promo-row
.pay-promo-input
.pay-promo-input::placeholder
.pay-promo-input:focus
.pay-promo-msg
.pay-promo.is-applied .pay-promo-input
.pay-promo.is-applied .pay-promo-msg
.pay-promo.is-invalid .pay-promo-input
.pay-promo.is-invalid .pay-promo-msg
.naya-btn
.naya-btn:hover
.naya-btn:active
.naya-btn:focus-visible
.naya-btn:disabled
.naya-btn:disabled:hover
.pay-totals
.pay-total-row
.pay-total-row dt
.pay-total-row dd
.pay-grand
.pay-grand dt
.pay-grand dd
.pay-grand:hover
.pay-grand:hover dd
.pay-honest
.pay-summary.is-empty .pay-totals
.pay-empty
.pay-summary.is-empty .pay-empty
.pay-empty .pay-title
.pay-empty p
```

## Notes

- The shared PAY board shell (Law 3 board formula) and the checkout-local `.naya-btn` DNA are carried into this block's CSS from PAY-001 so the family is self-contained — one include renders the whole board.
- `.pay-apply` is a hook-only class; the button's full styling comes from the `.naya-btn` DNA it also wears.
- Anatomy (from the source spec): - **Corner jewel ◆:** the board's identity mark — purple, choosing intelligence. It says "this board belongs to the checkout." - **Thumb jewels:** rotated diamonds, one spectrum step per item in law order. They are *identity*, not decoration — in a cart of five lookalike items, the jewel is how your eye finds the one you're editing. - **Qty stepper:** real `<button>`s, 34px with 44px of usable tap through padding, `<output aria-live>` so screen readers hear the count change. It will not fake — …
