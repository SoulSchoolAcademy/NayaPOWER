# Smart Block: `add-intel`

The "add intelligence" composer entry — the front door to creating. A single button styled as an inviting composer bar: a small glowing plus jewel at the left (breathing softly = alive at rest), warm placeholder copy in a human voice ("Add to the intelligence… / What did you learn today?"), and a prominent dark-elevated **Add** action at the right that ignites with a purple edge on hover. This is a button-like entry point that opens the composer — not a working form. Clicking dispatches a bubbling `add-intel:open` CustomEvent so any page can wire its composer without touching this file.

- **Type:** buttons
- **Source:** authored 2026-10-09 for Hub/Ledger completion
- **Files:** `add-intel.css`, `add-intel.js`, `specimen.html`
- **Dependencies:** tokens.css
- **States:** idle (quiet, breathing plus jewel), `:hover` (lift + purple edge ignite on pill and action), `:focus-visible` (purple hairline + soft outer glow — the honest "I'm listening" state), `.is-open` (demo/forced twin of the focus state for screenshots), `:active` (press compression), `@media (prefers-reduced-motion: reduce)` (breathing and transitions off)
- **Notes:**
  - NOT a form: there is no `<input>` and no submit behavior. The whole pill is one `<button>`; the right-hand "Add" is a visual cap (`pointer-events: none`) so clicks always land on the pill. The `add-intel.js` delegation emits `add-intel:open` with `detail.source` = the clicked pill.
  - Jewel colors (purple) appear only as glows, the plus jewel, and hairlines — never as text fills; text is silver/white only.
  - `add-intel.js` is optional: pure CSS works; include the script only if the page wants the event.

## Use it

1. Copy `add-intel.css` next to your page (and `add-intel.js` if you want the event).
2. Link `tokens.css` first, then `add-intel.css`.
3. Paste the pill; wire the event to open your composer:

```html
<button class="add-intel" type="button" aria-label="Add to the intelligence — opens the composer">
  <span class="add-intel-plus" aria-hidden="true"></span>
  <span class="add-intel-copy">
    <span class="add-intel-title">Add to the intelligence…</span>
    <span class="add-intel-sub">What did you learn today?</span>
  </span>
  <span class="add-intel-action">Add</span>
</button>

<script src="add-intel.js"></script>
<script>
document.addEventListener('add-intel:open', function (e) {
  openComposer(e.detail.source);
});
</script>
```

## Selectors

```
.add-intel (+ :hover / :active / :focus-visible / .is-open)
.add-intel-plus (+ ::before / ::after)
.add-intel-copy
.add-intel-title (+ .is-open .add-intel-title)
.add-intel-sub
.add-intel-action (+ :hover/:focus-visible/.is-open .add-intel-action)
```
