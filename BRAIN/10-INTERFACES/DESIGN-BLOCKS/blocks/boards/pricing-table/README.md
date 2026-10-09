# Smart Block: `pricing-table`

Pricing tiers. One board, one spectrum color per tier; the featured tier ignites.

- **Type:** boards
- **Source:** built 2026-10-09 (gap build — no design-file source; designed in Naya's language)
- **CSS:** `pricing-table.css`
- **Specimen:** `specimen.html`
- **States found:** :hover, .is-featured, .is-off
- **Dependencies:** tokens.css

## Use it

1. Include `tokens.css` (once per page).
2. Include `pricing-table.css`.
3. Copy the `.pt` markup. Set `--tier` per tier (spectrum colors; adjacent tiers never share a hue).
4. Mark one tier `.is-featured`.

## Selectors in this block

```
.pt
.pt-actions
.pt-cta
.pt-cta:hover
.pt-desc
.pt-feat
.pt-feat.is-off
.pt-feats
.pt-flag
.pt-name
.pt-per
.pt-price
.pt-tier
.pt-tier.is-featured
.pt-tier:hover
```

## Notes

- Follows the "one board, one color" law: each tier owns a single spectrum identity on spine, name, bullets, and CTA.
- Feature bullets are tier-colored jewels; excluded features are hollow.
- No JavaScript required — pure CSS block. Wire CTAs to checkout.
