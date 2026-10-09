# Smart Block: `smart-tab-strip`

The canonical reusable SmartTabs strip: a horizontal scrollable row of tab pills, each with a glowing tone dot (color set per-tab via `--tone`), a silver label, and an optional count badge. The selected tab gets a sliding glowing indicator bar that glides along the strip with the signature ease — positioned entirely by `transform: translateX/scaleX` for compositor-cheap motion. Keyboard navigable with roving tabindex (ArrowLeft/ArrowRight/Home/End move focus, Enter/Space activates), full `tablist`/`tab`/`aria-selected` semantics, and a fixed 44px circular "+" add-tab affordance pinned at the strip end.

- **Type:** tabs
- **Source:** authored 2026-10-09 for Hub/Ledger completion
- **Files:** `smart-tab-strip.css`, `smart-tab-strip.js`, `specimen.html`
- **Dependencies:** tokens.css
- **States:** `:hover` (soft wash), `:active` (press scale), `:focus-visible` (2px purple ring), `[aria-selected="true"]` (white label, brightened dot/badge, indicator underneath), `@media (prefers-reduced-motion: reduce)` (transitions off; JS snaps indicator without animation)
- **Notes:**
  - Replaces the earlier SmartTabs demo that referenced external `lego/` files which do not exist — this block is fully self-contained.
  - The JS auto-initializes every `.smart-tab-strip` on the page; no per-strip wiring needed. It creates the `.smart-tab-indicator` if omitted, enforces exactly one selected tab (defaults to the first), and recomputes indicator geometry on resize, font load, and container resize via `ResizeObserver`.
  - Tone dots take `--tone` inline per tab (falls back to `--purple`). Jewel colors appear only as the dots, the indicator glow, and the add-button edge — never as text fills.
  - RTL-aware arrow handling is deliberately not included (per brief); add `dir` mapping later if RTL ships.

## Use it

1. Copy `smart-tab-strip.css` and `smart-tab-strip.js` next to your page.
2. Link `tokens.css` first, then `smart-tab-strip.css`.
3. Paste the strip; mark one tab `aria-selected="true"`. Include `smart-tab-strip.js` at the end of body:

```html
<div class="smart-tab-strip">
  <div class="smart-tab-scroll">
    <div class="smart-tab-list" role="tablist" aria-label="Library sections">
      <button class="smart-tab" role="tab" type="button" aria-selected="true" style="--tone:var(--purple)">
        <span class="smart-tab-dot" aria-hidden="true"></span><span>All</span><span class="smart-tab-count">48</span>
      </button>
      <button class="smart-tab" role="tab" type="button" aria-selected="false" style="--tone:var(--emerald)">
        <span class="smart-tab-dot" aria-hidden="true"></span><span>Rooms</span><span class="smart-tab-count">12</span>
      </button>
      <span class="smart-tab-indicator" aria-hidden="true"></span>
    </div>
  </div>
  <button class="smart-tab-add" type="button" aria-label="Add tab">+</button>
</div>
```

## Selectors

```
.smart-tab-strip
.smart-tab-scroll (+ ::-webkit-scrollbar)
.smart-tab-list
.smart-tab (+ :hover / :active / :focus-visible / [aria-selected="true"])
.smart-tab-dot (+ [aria-selected="true"] .smart-tab-dot)
.smart-tab-count (+ [aria-selected="true"] .smart-tab-count)
.smart-tab-indicator
.smart-tab-add (+ :hover / :active / :focus-visible)
```
