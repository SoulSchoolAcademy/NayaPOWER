# `eco-inline`

Inline ecosystem nav: a horizontally scrollable row of glowing destination dots (`.eco-dot`), centered in the topbar, with hover ignite.

- **Type:** layout
- **Source:** `Welcome Page Design.html` (verbatim markup; 11 dots in source, specimen shows 2 + `…`)
- **Files:** `eco-inline.css`, `specimen.html`
- **States:** `.eco-dot:hover` (lift + scale + identity-color ignite via `--eco-c`, SVG recolor), `.eco-dot:active`, `@media (max-width:640px)` (30px dots), `prefers-reduced-motion`
- **Dependencies:** `tokens.css` (none required)
- **Structural note:** the base `.eco-inline` and `.eco-dot` geometry lives in INLINE styles in the source (38px circle, radial-gradient ground, layered shadows, `data-color` per dot) — there are no base CSS rules for them. The CSS in this block is the scrollbar hide + hover/active ignite + the 640px media query. The specimen preserves the inline styles verbatim, so the component renders as designed without modification. `.eco-dot:hover` references `var(--eco-c, #8a5cff)`; the source markup sets `data-color` instead — the fallback `#8a5cff` applies. Byte-true, quirks included.
- **Overlap note:** no indexed block duplicates this.

## Use it

```html
<nav class="eco-inline" aria-label="NayaNET destinations" style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);display:flex;align-items:center;gap:8px;justify-content:center;flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none;padding:4px 8px;max-width:60vw;">
  <a href="{{url}}" target="_blank" rel="noopener" title="HOME" aria-label="HOME" class="eco-dot" data-color="#35e39b" style="width:38px;height:38px;min-width:38px;border-radius:50%;display:grid;place-items:center;flex:none;position:relative;border:1.5px solid rgba(232,234,242,.55);background:radial-gradient(circle at 35% 28%,rgba(52,52,66,.95),rgba(8,8,12,.98) 72%);transition:all .25s cubic-bezier(.16,.84,.22,1);cursor:pointer;box-shadow:0 0 10px rgba(232,234,242,.25),inset 0 1px rgba(255,255,255,.25),inset 0 -2px 6px rgba(0,0,0,.5),0 3px 10px rgba(0,0,0,.5);-webkit-tap-highlight-color:transparent;text-decoration:none;">
    <svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="#e8eaf2" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="filter:drop-shadow(0 0 2px #35e39b66);"><path d="…"/></svg></a>
  <!-- … more .eco-dot links … -->
</nav>
```

## Selectors

```css
.eco-inline::-webkit-scrollbar
.eco-dot:hover
.eco-dot:hover svg
.eco-dot:hover svg *
.eco-dot:active
@media (max-width:640px) → .eco-inline, .eco-dot, .eco-dot svg
@media(prefers-reduced-motion:reduce)
```
