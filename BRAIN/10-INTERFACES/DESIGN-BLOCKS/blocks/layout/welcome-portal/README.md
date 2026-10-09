# Smart Block: `welcome-portal`

The welcome portal treatment — an orbital stage: a spectrum-rotating orbit ring studded with faceted jewels (`--a` angle, `--j` jewel color, `--s` scale), a unity orbit with a light mote, and the central portal jewel.

- **Type:** layout
- **Source:** `Naya Smart Hub Design.html`
- **Files:** `welcome-portal.css`, `specimen.html`
- **Dependencies:** tokens.css (`--a`, `--j`, `--s` set inline per jewel)
- **States:** `@keyframes welcome-spectrum` (78s orbit rotation), `@keyframes welcome-unity` (31s), `@keyframes jewel-breathe`, `prefers-reduced-motion` (all animation disabled), responsive `@media`
- **Notes:**
  - CSS-ONLY / LEGACY in the source: the welcome route is neutralized (legacy `#/welcome` hashes redirect into the Hub), so these classes have NO rendered instance. The specimen is reconstructed from CSS and marked as such.
  - `.portal-jewel` rules are bundled (the stage's `.portal-jewel` child).
  - Possible overlap: the indexed `hero` type block — this is an orbital visual treatment, not a headline hero; genuinely different, extracted.

## Use it

1. Copy `welcome-portal.css` next to your page.
2. Link `tokens.css` first, then `welcome-portal.css`.
3. Paste the stage; add `.welcome-orbit-jewel` elements with `--a` (angle), `--j` (color), `--s` (scale):

```html
<div class="welcome-portal-stage">
  <div class="welcome-orbit"></div>
  <div class="welcome-orbit-jewel" style="--a:0deg;--j:#9d75ff;--s:1"></div>
  <div class="welcome-orbit-jewel" style="--a:120deg;--j:#55e39a;--s:1.2"></div>
  <div class="welcome-unity-orbit">
    <div class="welcome-unity-light"></div>
  </div>
  <div class="portal-jewel">{{central jewel}}</div>
</div>
```

## Selectors

```
.welcome-portal-stage (+ .portal-jewel)
.welcome-orbit (+ .welcome-unity-orbit shared rule)
.welcome-orbit-jewel
.welcome-unity-orbit
.welcome-unity-light
.portal-jewel (+ ::after)
```
