# Smart Block: `sp-textin`

The Smart Spaces text input — recessed field in the sp language with a visible 11px kicker label. Inset-shadow well at rest, own-color ignite on focus-within. Includes the `.sp-tall` textarea variant for longer copy like space descriptions.

- **Type:** inputs
- **Source:** authored 2026-10-09 for Smart Spaces completion
- **Files:** `sp-textin.css`, `specimen.html`
- **States:** `:focus-within` (jewel ignite), `::placeholder`, `.sp-textin--tall`, `@media (prefers-reduced-motion: reduce)`
- **Dependencies:** none — self-contained; optional `--sc` inline to tint the focus ignite.

## Use it

1. Copy `sp-textin.css` into your page or component folder.
2. Paste the markup below; wrap the input in a `<label>` (or wire `for`/`id`).
3. Add `.sp-textin--tall` to the label for the textarea variant.
4. Set `--sc` inline to tint the focus ignite.

```html
<label class="sp-textin" style="--sc:#7c3aed">
  <span class="sp-textin-label">Space name</span>
  <span class="sp-textin-well"><input type="text" placeholder="Give it a name people remember"></span>
</label>

<label class="sp-textin sp-textin--tall" style="--sc:#7c3aed">
  <span class="sp-textin-label">Description</span>
  <span class="sp-textin-well"><textarea placeholder="What happens here? Who is it for?"></textarea></span>
  <span class="sp-textin-hint">A sentence or two is plenty — the people make the place.</span>
</label>
```

## Selectors

```css
.sp-textin
.sp-textin-label
.sp-textin-well
.sp-textin-well:focus-within
.sp-textin-well input, .sp-textin-well textarea
.sp-textin--tall .sp-textin-well textarea
.sp-textin-hint
```
