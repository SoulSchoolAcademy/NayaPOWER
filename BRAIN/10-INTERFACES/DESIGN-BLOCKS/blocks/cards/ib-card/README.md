# Smart Block: `ib-card`

The intelligent block card — one Smart Note rendered whole: identity spine (faceted jewel + title + meta + truth badge), the "In A Nutshell" extract, collapsible spectrum-colored layers with voice-play buttons, provenance foot, and microcopy trust signals. The full `.intel-board` composition; its root also composes the Hub `.board` atom (bundled).

- **Type:** cards
- **Source:** `Naya Smart Hub Design.html`
- **Files:** `ib-card.css`, `specimen.html`
- **Dependencies:** tokens.css (`--tone`, `--lc`, `--room-accent` set inline). The card's root is `article.intel-board` — the `.intel-board` base rules and `.tone-*` theming live in the `intel-row` block (`data/intel-row`); the Hub `.board` atom it composes is bundled here.
- **States:** `:hover` (board lift, layer-play), `.open` on `.ib-layer-head` (chevron rotates, body shows), `.is-deeper` on `.ib-layer`, `.playing` on `.ib-layer-play`, `.ib-layer.layer-{color}` spectrum variants (white/magenta/sapphire/emerald/purple/indigo/lime/gold/orange/teal/yellow/rich-orange/red), `@keyframes ib-play-glow`, responsive `@media`, `prefers-reduced-motion`
- **Notes:**
  - JS-rendered in the source (`intelBoard`); the specimen converts it to static HTML with structure and class names verbatim. `.meta-sep` has no CSS rule in the source (unstyled separator span) — kept verbatim.
  - SOURCE QUIRK (kept verbatim): the source nests `<button class="ib-layer-play">` inside `<button class="ib-layer-head">`. Browsers will reparent the inner button — noted, not "fixed".
  - `.ib-head`, `.ib-id`, `.ib-kind`, `.ib-state`, `.ib-dot`, `.ib-chev`, `.ib-microcopy`, `.ib-nutshell-label`, `.ib-truth` have CSS but no instance in the `intelBoard` builder shown — they belong to sibling board variants / the enhance() path; included so the block covers the whole ib-* family.
  - Possible overlap: the indexed `board` / `board-tone` blocks — this is the Smart Note card with identity spine, layers, and truth state; genuinely different, extracted.

## Use it

1. Copy `ib-card.css` next to your page.
2. Link `tokens.css` first, then `ib-card.css`.
3. Paste the markup (see `specimen.html` for the full composition); toggle `.open` + `aria-expanded` on layer heads to expand/collapse:

```html
<article class="intel-board tone-purple board" aria-label="Smart Note {{id}}" data-intelligence-id="smart-note-{{id}}">
  <div class="ib-blocktop">
    <div class="ib-identity">
      <span class="ib-jewel" aria-hidden="true" style="--tone:var(--purple);color:#9d75ff">
        <svg class="v10-icon" viewBox="0 0 32 32" aria-hidden="true">
          <polygon class="core" points="16,3 28,12 16,29 4,12"/>
          <polygon class="facet" points="16,3 22,12 16,12"/>
          <polygon class="facet" points="16,3 10,12 16,12" opacity=".3"/>
          <polygon class="shade" points="16,29 28,12 16,12"/>
          <polygon class="edge" points="16,3 28,12 16,29 4,12"/>
        </svg>
      </span>
      <div>
        <h2 class="ib-title">{{title}}</h2>
        <div class="ib-meta"><span>{{category}}</span><span class="meta-sep">·</span><span>{{topic}}</span></div>
      </div>
    </div>
  </div>
  <div class="ib-nutshell"><b>IN A NUTSHELL</b><p>{{nutshell}}</p></div>
  <div class="ib-layers">
    <div class="ib-layer layer-purple">
      <button class="ib-layer-head open" aria-expanded="true">
        <span class="layer-jewel-wrap" style="--lc:#55e39a">…layer jewel svg…</span>
        <b>{{layer name}}</b>
        <button class="ib-layer-play" data-layer-name="{{name}}" aria-label="Hear Naya read {{name}}" title="Play in Naya's voice"><span>▶</span></button>
      </button>
      <div class="ib-layer-body"><p>{{body}}</p></div>
    </div>
  </div>
  <div class="ib-foot"><span>Smart Note {{id}} · from your Smart Feed</span></div>
  <div class="ib-microcopy">
    <span class="left">ONE INTELLIGENCE · MANY VIEWS · ONE IDENTITY</span>
    <span class="right">TRUST: SOURCE / INTERPRETATION SEPARATED</span>
  </div>
</article>
```

## Selectors

```
.board
.board.lift:hover
.ib-blocktop
.ib-chev
.ib-dot
.ib-foot
.ib-head
.ib-id
.ib-identity
.ib-identity .ib-jewel
.ib-jewel
.ib-kind
.ib-layer / .ib-layer.layer-{color} (×12)
.ib-layer-body (+ p / ul / li / strong / code)
.ib-layer-head (+ .open / b / .ib-chev)
.ib-layer-play (+ span / :hover / .playing)
.ib-layers
.ib-meta (+ span)
.ib-microcopy (+ .left / .right)
.ib-nutshell (+ b / p / .ib-nutshell-label)
.ib-state
.ib-subtitle
.ib-title
.ib-truth
.meta-sep
.v10-icon (+ .core / .facet / .shade / .edge)
.layer-jewel-wrap
.layer-jewel-svg
```
