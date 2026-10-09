# `wb-entrance`

The NayaNET sovereign entrance: full-viewport treatment — topbar with brand crystal + inline ecosystem dots + Auto-Login, intro headline, portal stage with the 108-jewel orbital ring and white unity light, the silver-vault portal with name-entry form (or welcome-back state), footer, and the `body.entering` fly-through animation.

- **Type:** layout
- **Source:** `Welcome Page Design.html` (verbatim body markup; long inline styles and jewel spans shortened with `…`; brand logo replaced with `{{logo}}` placeholder — source embeds a base64 PNG)
- **Files:** `wb-entrance.css`, `wb-entrance.js`, `specimen.html`
- **States:** `body.entering` (portal zoom + orbit speed-up + main fly-forward `wholeForward`), `#welcomeBack` remembered-identity state, `:hover`/`:active` on `.auto`/`.enter`/`.input:focus`, `@media(max-height:760px)`, `@media(max-height:700px)`, `@media(max-width:380px)`, `@media(min-width:700px)`, `prefers-reduced-motion`
- **Dependencies:** `tokens.css` (block defines its own `:root` vars: `--bg --white --muted --purple --purple2 --green --dark`), `eco-inline` (the topbar dots' hover/active CSS lives there), `navigation-stack` (the nav below the portal)
- **JS:** `wb-entrance.js` is the source script verbatim: 108-jewel orbital generator (12 color families × 3 shades × 3 passes), entry-flow submit → `body.entering` → identity handoff, `checkAutoLogin()`, and the welcome-back renderer (`#welcomeBack`, `.wb-name`, `.wb-switch`)
- **Overlap notes:**
  - The task brief said `#intro` — the source actually uses `section.intro` (class, not id). The `.intro`/`.intro h1` rules are included.
  - Welcome's `.stage` vs indexed `stage` (`.stage, .stage-label, .stage:before` — demo showcase container): NOT a duplicate. Welcome `.stage` is a 3D portal stage (`perspective:1200px`, `container-type:size`, flex centering for the orbit + portal). Different purpose, different rules. Its single rule is included here rather than as a standalone block.
  - The `.topbar` chrome differs from indexed `nav` (`.naya-nav` sticky top bar): this one centers an inline ecosystem nav and carries an Auto-Login button. Extracted as part of the entrance, not skipped.

## Use it

```html
<body>
  <header class="topbar">
    <div class="brand"><img src="{{logo}}" alt="NayaNET" …></div>
    <nav class="eco-inline" aria-label="NayaNET destinations" style="…">… .eco-dot links …</nav>
    <button class="auto" type="button">Auto-Login</button>
  </header>
  <main>
    <section class="intro">
      <h1>Welcome to NayaNET</h1>
      <p class="tag">Create. Connect. Grow <strong>with US.</strong></p>
    </section>
    <section class="stage">
      <div class="naya-orbit" aria-hidden="true">
        <div class="naya-color-orbit" id="nayaColorOrbit"><!-- .naya-jewel × 108 (JS) --></div>
        <div class="naya-white-orbit"><span class="naya-white-light"></span></div>
      </div>
      <div class="portal">
        <div class="core">
          <div class="content">
            <div class="presence" id="presence">Naya Listening</div>
            <form id="entryForm">
              <input id="userName" class="input" type="text" placeholder="Enter Your Name" autocomplete="name" autocapitalize="words" required>
              <button class="enter" type="submit">Enter NayaNET →</button>
            </form>
          </div>
        </div>
      </div>
    </section>
  </main>
  <footer class="footer">Create. Connect. Grow with US.</footer>
  <script src="wb-entrance.js"></script>
</body>
```

## Selectors

```css
*, :root, html, body, body:before
.topbar, .brand, .brand span, .crystal, .auto, .auto:hover, .auto:active
main, .intro, .intro h1, .tag, .tag strong
.stage
.naya-orbit, .naya-color-orbit, .naya-jewel, .naya-jewel:before, .naya-jewel:after
.naya-white-orbit, .naya-white-light, .naya-white-light:after
.portal, .portal:before, .core, .core:after, .content
.presence, .presence:before
.input, .input::placeholder, .input:focus
.enter, .enter:hover, .enter:active
.footer
body.entering .naya-color-orbit, body.entering .naya-white-orbit, body.entering .naya-jewel,
body.entering .naya-white-light, body.entering .portal, body.entering .portal:before,
body.entering main, body.entering .presence
#welcomeBack, .wb-name, .wb-name strong, .wb-switch, .wb-switch:hover
@keyframes ambient, nayaSpectrum, nayaWhite, pulse, wholeForward
@media(max-height:760px), @media(max-height:700px), @media(max-width:380px),
@media(min-width:700px), @media(prefers-reduced-motion:reduce)
```
