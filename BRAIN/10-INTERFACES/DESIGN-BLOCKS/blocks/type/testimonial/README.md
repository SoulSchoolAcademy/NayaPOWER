# Smart Block: `testimonial`

Attributed testimonial card. Voice serif quote, gold star row, jewel avatar attribution.

- **Type:** type
- **Source:** built 2026-10-09 (gap build — no design-file source; designed in Naya's language)
- **CSS:** `testimonial.css`
- **Specimen:** `specimen.html`
- **States found:** (static display block)
- **Dependencies:** tokens.css

## Use it

1. Include `tokens.css` (once per page).
2. Include `testimonial.css`.
3. Copy the `<figure class="tm">` markup. Use `.tm-grid` for multi-card layouts.

## Selectors in this block

```
.tm
.tm-ava
.tm-ava img
.tm-grid
.tm-name
.tm-quote
.tm-role
.tm-stars
.tm-who
```

## Notes

- The quote uses the voice serif (Cormorant Garamond) at 22px — same grammar as `voice-type`, sized for testimony.
- The giant quotation mark glows purple at low opacity — presence, not decoration.
- Real quotes only. A testimonial block carrying invented praise violates the truth-state law.
- No JavaScript required — pure CSS block.
