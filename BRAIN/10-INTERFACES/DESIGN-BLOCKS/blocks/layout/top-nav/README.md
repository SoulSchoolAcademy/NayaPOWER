# Smart Block: `top-nav`

Sticky top nav: orb mark, wordmark label, section links. Collapses on mobile.

- **Type:** layout
- **Source:** `Naya Building Blocks - The Ultimate Design System - Naya 2.html`
- **Files:** `top-nav.css`, `specimen.html`
- **States:** `:hover`
- **Dependencies:** `tokens.css`, `nav-orb`

## Use it

1. Copy `top-nav.css` into your page or component folder.
2. Include the shared `tokens.css` on the page plus: `nav-orb`.
3. Paste the markup from `specimen.html` where the component should live.
4. Set `--tone` / `--rgb` inline (or via a theme class) to give the component its identity color.

## Selectors

```css
.nav
.nav-label
.nav-links
.nav-links a
.nav-links a:hover
.nav-links a:nth-child(n+5)
.nav-n
```
