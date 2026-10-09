# Smart Block: `activity-hero`

A glass activity banner — large glowing title + sub-line, centered, for the top of the activity stream.

- **Type:** cards
- **Source:** `Naya Smart Hub Design.html`
- **Files:** `activity-hero.css`, `specimen.html`
- **Dependencies:** tokens.css
- **States:** responsive `@media` (inherited source breakpoints)
- **Notes:**
  - CSS-ONLY in the source: these classes have NO rendered instance in the file (never referenced in markup or JS). The specimen is reconstructed from the CSS class names and marked as such.
  - Possible overlap: the indexed `hero` type block (page opening with eyebrow/title/sub/CTA) — this is a simpler glass banner with no eyebrow or CTA row; extracted, note the kinship.

## Use it

1. Copy `activity-hero.css` next to your page.
2. Link `tokens.css` first, then `activity-hero.css`.
3. Paste the markup:

```html
<div class="activity-hero">
  <div class="activity-hero-inner">
    <h2 class="activity-hero-title">{{title}}</h2>
    <p class="activity-hero-sub">{{sub-line}}</p>
  </div>
</div>
```

## Selectors

```
.activity-hero
.activity-hero-inner
.activity-hero-title
.activity-hero-sub
```
