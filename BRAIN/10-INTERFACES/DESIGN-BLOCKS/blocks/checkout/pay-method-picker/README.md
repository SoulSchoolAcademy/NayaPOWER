# Smart Block: `checkout/pay-method-picker`

Payment method picker: saved-method rows with glowing brand jewels, purple selected state, exactly one selection, and an honest new-card row (no "no cards saved" apology).

## Why

**Law:** Law 2 (purple = choosing intelligence — the selected row ignites purple) · Law 1 (rows rest dark, lift 2px, ignite their own tone) · the PAY-002 privacy boundary (last-4 + brand only, never full numbers).

**Do / Don't** — **DO** mark exactly one default and let the user change it where the row lives — a "make default" that only exists in settings is a scavenger hunt. The chip is gold because the default is the card the user already trusted. **DON'T** show the expiry as a countdown ("expires in 4 months!!") or nudge the user toward any particular card. The picker is neutral ground — it presents, it never persuades. And never add a "delete" affordance inline on the row; removing a payment method is destructive and deserves its own confirmed moment elsewhere.

- **Type:** checkout
- **Catalog:** NAYA-PAY-005
- **Source:** `gap-blocks/checkout-blocks.md` (harvested, never restyled)
- **CSS:** `block.css`
- **Specimen:** `specimen.html`
- **States found:** `.pay-method:hover` (lift 2px, choosing-purple ignition), `.pay-method.is-selected` (purple edge + wash + glow, check orb fades in), `:focus-within` (white ring), `.pay-method:active` (compress 1px)
- **Dependencies:** none — self-contained

## Use it

1. Include `block.css` (self-contained: board shell + method styles).
2. Rows are real radio controls; the selected row gets `.is-selected` (purple edge + wash + check orb).

## Selectors in this block

```
.pay-board
.pay-board:hover
.pay-corner
.pay-head
.pay-kicker
.pay-title
.pay-methods
.pay-method
.pay-method input[type="radio"]
.pay-method:hover
.pay-method:active
.pay-method:focus-within
.pay-method.is-selected
.pay-method.is-selected:hover
.pay-mcheck
.pay-method.is-selected .pay-mcheck
.pay-mbrand
.pay-mbrand.is-visa
.pay-mbrand.is-mastercard
.pay-mbrand.is-amex
.pay-mbrand--plus
.pay-mbody
.pay-mname
.pay-mdefault
.pay-mmeta
.pay-method--new
.pay-method--new:hover
.pay-mgo
.pay-method--new:hover .pay-mgo
.pay-methods-note
```

## Notes

- The shared PAY board shell (Law 3 board formula) and the checkout-local `.naya-btn` DNA are carried into this block's CSS from PAY-001 so the family is self-contained — one include renders the whole board.
- Anatomy (from the source spec): - **Brand jewels:** orbs in the brand's own color — Visa blue, Mastercard orange, Amex emerald. Identity, not decoration: at a glance you know which card is which without reading a digit. - **Last-4 + expiry:** the only numbers on the row, and both arrive from the backend already masked. The row *names* the card ("Visa ···· 4242") the way a person would. - **Default chip:** gold outline, letterspaced, quiet. One per picker. - **New-card row:** dashed border at rest (it *promises* a different …
