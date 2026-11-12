# Smart Block: `comments/cmt-comment`

Single comment: avatar jewel, serif name, plain-words timestamp, body, and a reply/love/share action row — the unit comment threads are built from.

## Why

One comment, fully dressed: avatar jewel, serif name, plain-words timestamp, body, and an action row — reply (chrome), love (pink toggle), share (blue). The building block CMT-001 is made of. Law 1: the actions rest quiet and ignite in their own colors; nothing in the row is flat.

**Do / Don't** — Do: keep the love count identical to the reaction row's love count — same data, same number, rendered twice, never computed twice. Don't: let the single comment drift from the thread's comment — CMT-002 *is* CMT-001's atom; if they disagree on spacing, type, or behavior, one of them is wrong. Do: clamp long bodies with a real control — four lines is a kindness, hiding text without a control is a theft. Don't: truncate with an ellipsis and no way back; a "…" with nowhere to go is a dead end wearing punctuation.

- **Type:** comments
- **Catalog:** NAYA-CMT-002
- **Source:** `gap-blocks-2/comments-blocks.md` (harvested, never restyled)
- **CSS:** `block.css`
- **JS:** `block.js`
- **Specimen:** `specimen.html`
- **States found:** `.cmt-one:hover` (lift 4px, edge brightens, tone under-glow), `action `:hover` (lift 2px, own color: reply purple, love pink, share blue)`, `.cmt-love.is-on` (`aria-pressed="true"`, held pink edge + glow), `:active` (settle 1px), `:focus-visible` (white 2px ring), `.cmt-body.is-clamped` (four lines + honest "Show more"), `disabled action (38% opacity, truly inert)`
- **Dependencies:** comments/cmt-thread block.css (comment chrome: actions, heads, timestamps)

## Use it

1. Include `block.css` AND `../cmt-thread/block.css` (comment chrome: actions, heads, timestamps).
2. Include `block.js` — wires the honest "Show more" clamp toggle on long bodies.

## Selectors in this block

```
.cmt
.cmt-one
.cmt-one:hover
.cmt-one .cmt-av
.cmt-one .cmt-av b
.cmt-one .cmt-name
.cmt-one .cmt-body
.cmt-one .cmt-body.is-clamped
.cmt-morebtn
.cmt-morebtn:hover
.cmt-morebtn:focus-visible
.cmt-one .cmt-actions
.cmt-count
```

## Notes

- Comment chrome (actions, heads, timestamps) lives in `comments/cmt-thread` — include its `block.css` alongside this one (the specimen does).
- Anatomy (from the source spec): - **Avatar jewel:** 52px here (the single comment gets a touch more presence than in-thread), initials in serif, author's stable color — same jewel law as CMT-001, one size up. - **Name row:** serif 18px display name, plain-words timestamp, quiet "edited" when true. Nothing else about the author is shown — private by default. - **Body:** 15px, white 96%, 1.6 line height. Clamps at four lines with "Show more" — the control is part of the block, not an afterthought. - **Action row:** reply / love …
