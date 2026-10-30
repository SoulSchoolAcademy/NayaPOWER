# Smart Block: `checkout/pay-payment-form`

Payment form: dark fields with white-lit edges, purple focus ignition, emerald valid / red invalid, structural privacy — the display layer never sees more than last-4 + brand.

## Why

**Law:** Law 1 (fields rest dark with white-lit edges; focus ignites purple — purple is chrome) · Law 5 (Pay is the flagship CTA: ≥52px, one per view) · Law 6 (Georgia voice on the header). Validation law: valid = emerald edge, invalid = red edge + a plain-words message. Never blame the user.

**Do / Don't** — **DO** validate inline, per field, the moment the user leaves it — and let the emerald edge be the reward. Fast feedback is kindness; a surprise error at the bottom of a submitted form is not. **DON'T** clear the whole form on a failed payment, and don't red-ring every field when one card number is the problem. Mark the one field that's wrong, keep everything else, and keep the user's typing. Wiping their work is the fastest way to lose the sale *and* the trust.

- **Type:** checkout
- **Catalog:** NAYA-PAY-002
- **Source:** `gap-blocks/checkout-blocks.md` (harvested, never restyled)
- **CSS:** `block.css`
- **Specimen:** `specimen.html`
- **States found:** `.pay-input:focus` (purple edge + held glow — purple is chrome), `.pay-input.is-valid` (emerald edge + glow), `.pay-input.is-invalid` (red edge + glow + plain-words sentence), `.pay-submit:active` (press in 1px, scale .98), `.pay-submit:disabled` (45% opacity, no theater)
- **Dependencies:** none — self-contained

## Use it

1. Include `block.css` (self-contained: board shell + `.naya-btn` DNA + form styles).
2. Mark fields `.is-valid` / `.is-invalid`; keep the Pay button `disabled` until the form validates.

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
.pay-form
.pay-form .pay-corner
.pay-field
.pay-field-row
.pay-field-row .pay-field
.pay-input
.pay-input--card
.pay-input:focus
.pay-label
.pay-input:not(:placeholder-shown) + .pay-label
.pay-input.is-valid
.pay-input.is-invalid
.pay-input.is-invalid + .pay-label
.pay-err
.pay-err[hidden]
.pay-brand
.pay-brand.is-known
.pay-brand.is-visa
.pay-brand.is-mastercard
.pay-brand.is-amex
.pay-submit
.pay-submit:not(:disabled):hover
.pay-secure
```

## Notes

- The shared PAY board shell (Law 3 board formula) and the checkout-local `.naya-btn` DNA are carried into this block's CSS from PAY-001 so the family is self-contained — one include renders the whole board.
- Anatomy (from the source spec): - **Floating labels:** rest inside the field, lift to kicker on focus or content. The field's purpose never disappears. - **Card number field:** `inputmode="numeric"` for the right mobile keyboard, `autocomplete="cc-number"` so the browser can fill it safely, `letter-spacing` + tabular figures so a 16-digit number reads in groups. The `pattern` is a courtesy, not a contract — real validation runs against the payment processor's rules. - **Brand jewel:** lights in the brand's own color once the …
