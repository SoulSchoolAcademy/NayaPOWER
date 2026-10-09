# `li-tabs`

Glass filter tabs: pill buttons with per-tab identity color (`--tab-c`), lift on hover, glow on `.on`.

- **Type:** tabs
- **Source:** `Ledger Page Design.html` (specimen reconstructed from the FILTERS section; count badges carry verbatim inline styles — `.li-tab-count` has no CSS rule in source)
- **Files:** `li-tabs.css`, `specimen.html`
- **States:** `:hover` (lift + identity border), `.on` / `:focus-visible` (identity color text + glow)
- **Dependencies:** `tokens.css` (none required — `--tab-c` set inline per tab)
- **Overlap note:** genuinely different from indexed `seg-tab`. `seg-tab` is a room-control segmented pill with `.lv-aware` proximity variants. `li-tabs`/`li-tab` are identity-colored glass filter pills driven by `--tab-c` with count badges. Different purpose, different treatment — extracted, not skipped.

## Use it

```html
<div class="li-stage">
  <nav class="li-tabs">
    <button class="li-tab on" type="button" style="--tab-c:#c084fc" aria-pressed="true"><span>ALL</span><span style="margin-left:8px;font-size:12px;opacity:.7;background:rgba(255,255,255,.1);padding:2px 8px;border-radius:99px;">{{count}}</span></button>
    <button class="li-tab" type="button" style="--tab-c:#38bdf8" aria-pressed="false"><span>INTEL</span><span style="…">{{count}}</span></button>
  </nav>
</div>
```

## Selectors

```css
.li-stage .li-tabs
.li-stage .li-tab
.li-stage .li-tab:hover
.li-stage .li-tab.on, .li-stage .li-tab:focus-visible
```
