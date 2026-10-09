# Smart Block: `avatar-stack`

Stacked presence avatars. Overlapping circles with spectrum identity order, presence dots, +N overflow.

- **Type:** media
- **Source:** built 2026-10-09 (gap build — no design-file source; designed in Naya's language)
- **CSS:** `avatar-stack.css`
- **Specimen:** `specimen.html`
- **States found:** :hover, .is-away, .is-off, .as--sm, .as--lg, .as-more
- **Dependencies:** tokens.css

## Use it

1. Include `tokens.css` (once per page).
2. Include `avatar-stack.css`.
3. Copy the `.as` markup. Put an `<img>` inside `.as-ava` for real photos, or an initial letter.

## Selectors in this block

```
.as
.as--lg
.as--sm
.as-ava
.as-ava .as-dot
.as-ava.is-away .as-dot
.as-ava.is-off .as-dot
.as-ava:hover
.as-ava img
.as-more
.as-more:hover
```

## Notes

- Avatar backgrounds follow the global jewel spectrum (magenta → purple → blue → green → gold); adjacent never repeat.
- Presence: green = online, gold = away, dim = offline.
- `.as-more` is a button — wire it to open the member list.
- No JavaScript required — pure CSS block.
