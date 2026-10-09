# `li-search`

Heartbeat search bar: full-width glass input with magnifier icon, gold focus ignite, and a clear button that appears only when the wrap has text (`.has-text`).

- **Type:** inputs
- **Source:** `Ledger Page Design.html` (specimen reconstructed from the SEARCH section `el()` calls)
- **Files:** `li-search.css`, `specimen.html`
- **States:** `::placeholder`, `:focus` (gold border + glow), `.li-search-wrap.has-text .li-search-clear` (clear button reveals; JS toggles the class on input)
- **Dependencies:** `tokens.css` (none required — colors hardcoded)
- **Overlap note:** genuinely different from indexed `nl-search`. `nl-search` is a `.nl-well`-based field with a generic `.icon` slot. `li-search` is a distinct treatment: oversized 17px glass bar, absolutely-positioned SVG icon, circular clear button revealed via `.has-text`, gold focus ignite. Different structure, different visual language — extracted, not skipped.

## Use it

```html
<div class="li-stage">
  <div class="li-search-wrap">
    <span class="li-search-icon"><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg></span>
    <input class="li-search" type="search" placeholder="Search the heartbeat — actions, names, values...  ( / )" aria-label="Search ledger">
    <button class="li-search-clear" type="button" aria-label="Clear search">&times;</button>
  </div>
</div>
```

## Selectors

```css
.li-stage .li-search-wrap
.li-stage .li-search
.li-stage .li-search::placeholder
.li-stage .li-search:focus
.li-stage .li-search-icon
.li-stage .li-search-clear
.li-stage .li-search-wrap.has-text .li-search-clear
```
