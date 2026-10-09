# `navigation-stack`

Stacked navigation: vertical column of full-width pill buttons with icon + letterspaced label, each with its own color theme (about = purple, whitepaper = white, powercasts = green).

- **Type:** layout
- **Source:** `Welcome Page Design.html` (verbatim markup)
- **Files:** `navigation-stack.css`, `specimen.html`
- **States:** `.nav-button:hover` (lift), `.nav-button:active` (press), theme hovers on `.about-button`/`.whitepaper-button`/`.player`, `@media(max-height:760px)`, `@media(max-height:700px)`, `@media(max-width:380px)`, `@media(min-width:700px)`, `prefers-reduced-motion`
- **Dependencies:** `tokens.css` (uses the wb-entrance `:root` vars `--purple --purple2 --green` when composed on the Welcome page; set them or override per theme)
- **Overlap note:** genuinely different from indexed `nav` (`.naya-nav` — sticky top bar: logo left, links, CTA right, hamburger). `navigation-stack` is a vertical stacked button column that sits under the portal. Different component, different layout role — extracted, not skipped.

## Use it

```html
<nav class="navigation-stack" aria-label="NayaNET navigation">
  <a class="nav-button about-button" href="{{url}}">
    <span class="nav-icon">✦</span> ABOUT US
  </a>
  <a class="nav-button whitepaper-button" href="{{url}}">
    <span class="nav-icon">◈</span> WHITE PAPER
  </a>
  <a class="nav-button player" href="{{url}}" target="_self" aria-label="Open NayaNET Powercasts">
    <span class="nav-icon">🎧</span> POWERCASTS
  </a>
</nav>
```

## Selectors

```css
.navigation-stack
.nav-button
.nav-button:hover
.nav-button:active
.nav-icon
.about-button
.about-button:hover
.whitepaper-button
.whitepaper-button:hover
.player
.player:hover
@media(max-height:760px) → .navigation-stack, .nav-button
@media(max-height:700px) → .nav-button
@media(max-width:380px) → .navigation-stack, .nav-button
@media(min-width:700px) → .navigation-stack, .nav-button
@media(prefers-reduced-motion:reduce)
```
