# Smart Block: `tabs/sp-dtabs`

Underline tabs with count badges — active tab gets the accent underline and glow, badges render the accent chip.

- **Type:** tabs
- **Source:** `Smart Spaces Page Design.html` (extracted byte-true, never rewritten)
- **CSS:** `block.css`
- **JS:** `block.js`
- **Specimen:** `specimen.html`
- **States found:** `.sp-dtab:hover`, `.sp-dtab.on`
- **Dependencies:** `--sc` (space accent — underline, glow, badge background; set via `opts.accent`)

## Use it

1. Include `block.css`.
2. Include `block.js`.
3. Call `spDtabs(tabs, opts)` and append the returned element.

## Selectors in this block

```
.sp-dtabs
.sp-dtab
.sp-dtab:hover
.sp-dtab.on
.sp-dtab-n
```

## Notes

- Builder signature: `spDtabs([{label, count, active}], {accent, onSelect})`. `count` renders the `.sp-dtab-n` badge (only when truthy); `active` applies `.on`.
- The source derived the badge count from `spaceChat(s.id).length` on the Chat tab; that wiring is now the consumer's job via `count`.
- Selection state is data-driven: mark the selected tab `active:true` and re-render (see the `// Demo:` comment and specimen).
- Builder: `spDtabs`.
