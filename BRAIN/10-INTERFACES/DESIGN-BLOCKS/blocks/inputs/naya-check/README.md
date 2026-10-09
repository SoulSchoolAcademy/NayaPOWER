# Smart Block: `naya-check`

A checkbox with jewel physics — it ignites green when the promise is kept, and the label rests when it is done.

- **Type:** inputs
- **Source:** `smart-blocks/inputs/inputs-jeweled-checkbox-naya-check.html + smart-blocks/inputs/inputs.css (branch naya5/smart-blocks-library)`
- **Files:** `naya-check.css`, `specimen.html`
- **Dependencies:** `tokens.css`
- **States:** `:checked`, `:hover`, `:active`, `:focus-visible`

## Use it

1. Copy `naya-check.css` next to your page.
2. Link `tokens.css` first, then `naya-check.css`.
3. Paste the markup from `specimen.html` (set the `--` variables shown to theme it).

## Selectors

```
.naya-check
.naya-check input
.naya-check .box
.naya-check:hover .box
.naya-check input:checked + .box
.naya-check input:focus-visible + .box
.naya-check:active .box
.naya-check .txt
.naya-check input:checked ~ .txt
```
