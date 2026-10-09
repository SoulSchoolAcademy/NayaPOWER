# Smart Block: `toast`

Toast system: fixed live-region toast + rich toast-mini card. Reports briefly, truthfully.

- **Type:** overlays
- **Source:** `Naya Building Blocks - The Ultimate Design System - Naya 2.html`
- **Files:** `toast.css`, `specimen.html`
- **States:** none (static)
- **Dependencies:** `tokens.css`, `naya-btn`, `icon`

## Use it

1. Copy `toast.css` into your page or component folder.
2. Include the shared `tokens.css` on the page plus: `naya-btn`, `icon`.
3. Paste the markup from `specimen.html` where the component should live.
4. Set `--tone` / `--rgb` inline (or via a theme class) to give the component its identity color.

## Selectors

```css
.modal-mini small,.toast-mini small,.search-result small,.content-card small,.setting-row small,.media-copy small,.smart-link small
.modal-mini strong,.modal-mini small,.toast-mini strong,.toast-mini small,.search-result strong,.search-result small,.content-card strong,.content-card small,.setting-row strong,.setting-row small,.media-copy strong,.media-copy small,.smart-link strong,.smart-link small
.toast
.toast-mini
.toast-mini>.icon
.toast.show
```
