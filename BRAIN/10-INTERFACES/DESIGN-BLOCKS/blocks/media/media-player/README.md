# Smart Block: `media-player`

Media player row: portal play button, copy + timeline, download action.

- **Type:** media
- **Source:** `Naya Building Blocks - The Ultimate Design System - Naya 2.html`
- **Files:** `media-player.css`, `specimen.html`
- **States:** none (static)
- **Dependencies:** `tokens.css`, `naya-btn`, `icon`, `timeline`

## Use it

1. Copy `media-player.css` into your page or component folder.
2. Include the shared `tokens.css` on the page plus: `naya-btn`, `icon`, `timeline`.
3. Paste the markup from `specimen.html` where the component should live.
4. Set `--tone` / `--rgb` inline (or via a theme class) to give the component its identity color.

## Selectors

```css
.media-player
.media-player>.naya-btn:last-child
.modal-mini small,.toast-mini small,.search-result small,.content-card small,.setting-row small,.media-copy small,.smart-link small
.modal-mini strong,.modal-mini small,.toast-mini strong,.toast-mini small,.search-result strong,.search-result small,.content-card strong,.content-card small,.setting-row strong,.setting-row small,.media-copy strong,.media-copy small,.smart-link strong,.smart-link small
```
