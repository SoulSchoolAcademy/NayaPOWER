# PRICING REBUILD — AMENDMENT 4: THE CODE
## Every piece, with its link, its code, and what it's supposed to say — copy and paste, don't re-derive

**Status:** extends the airtight brief (blob 52aa7543) + Amendment 1 (blob 87e81e5f) + Amendment 2 (blob 000288d7) + Amendment 3 (blob e9c02913). Where this amendment conflicts with any of them, this amendment wins — it is the later word, and it is the most specific.

**Why this amendment exists (Shawn's instruction, 03:34Z):** "you're not giving them the examples, you're not giving them the code... you just give them the URLs or give them the code, tell the pieces, hey you're supposed to use this code in these pieces, this is the links to them, this is where it is and this is what it's supposed to say... you should be doing the work for them, not be like here go create some shit." He is right. The miscommunication chain — one person tells another what they want, the other creates something else, and it goes around over and over — exists because the seat has to INTERPRET. The fix is to remove the interpretation step: **every piece below has (a) the link — where it lives, (b) the code — what to paste, (c) what it's supposed to say and do, (d) what NOT to change.** The seat copies and pastes. It does not re-derive, re-read, re-imagine, or "improve". **Any deviation from the pasted code = build FAILED. Any invented replacement = build FAILED.**

**The rule for this amendment:** if a piece has code pasted below, that code IS the piece — paste it verbatim. If a piece has only a link + line ranges, fetch that exact range and paste it verbatim — do not summarize it, do not rewrite it, do not "adapt" it. If a piece has NO canonical code anywhere, it is named as a GAP below (§5) — the seat uses the spec given, and does NOT invent code to fill it.

---

## §1 THE BUTTON — `.primo` (every button on the page)

**The link — where it lives:**
- Canonical source file (local, on this machine): `~/workspace/team-nitro/smart-builder/scratch/trial1-p2/HUB/design-system/library/buttons/Naya_Beautiful_Button_Set_N4.html` — lines 238–247 (the `.primo` rule block). Also at `~/workspace/user/files/Naya_Beautiful_Button_Set_N4.html`.
- DESIGN-BLOCKS part (filed, GitHub main): `BRAIN/10-INTERFACES/DESIGN-BLOCKS/pricing-round7-fix1/chrome-button-naya-btn-027.md` — raw: https://raw.githubusercontent.com/SoulSchoolAcademy/NayaPOWER/main/BRAIN/10-INTERFACES/DESIGN-BLOCKS/pricing-round7-fix1/chrome-button-naya-btn-027.md
- Catalog entry: `team-nitro/smart-builder/scratch/trial1-p2/HUB/design-system/library/catalog/block-catalog.json` — NAYA-BTN-027 = "04 · Standard — .primo".

**The code — paste this verbatim:**
```css
.primo { display: inline-flex; align-items: center; gap: 10px; cursor: pointer; font-weight: 800; font-size: 15px; letter-spacing: .08em; color: #fff; padding: 14px 26px; border-radius: 999px; border: none;
  background: linear-gradient(180deg, #141419 0%, #050505 60%, #08080c 100%);
  box-shadow: inset 0 0 0 1.7px rgba(255,255,255,.9), inset 0 2px 5px rgba(255,255,255,.2), inset 0 -6px 14px rgba(0,0,0,.7), 0 10px 28px rgba(0,0,0,.55), 0 3px 10px rgba(0,0,0,.45);
  transition: transform .22s var(--ease), box-shadow .22s var(--ease); --glow: var(--soul); }
.primo:hover { transform: translateY(-2px); box-shadow: inset 0 0 0 1.7px var(--glow), inset 0 2px 5px rgba(255,255,255,.25), inset 0 -6px 14px rgba(0,0,0,.65), 0 14px 36px rgba(0,0,0,.6), 0 0 26px -4px var(--glow); }
.primo:active { transform: translateY(1px) scale(.985); }
.primo.theme-magenta { --glow: var(--magenta); } .primo.theme-purple { --glow: var(--purple); }
.primo.theme-blue { --glow: var(--blue); } .primo.theme-green { --glow: var(--green); } .primo.theme-gold { --glow: var(--gold); }
.primo:disabled { opacity: .6; cursor: default; transform: none; }
```

**The markup — paste this verbatim:**
```html
<button class="primo theme-gold">Start free — try her for 9 days</button>
```

**What it's supposed to say and do:** "silver-white at rest, ignites on touch" — a chrome button, a real object. At rest it is silver-white; on touch it lifts 2px and ignites with its theme glow. The gold theme (`theme-gold`) is the Start button. Every button on the page is `.primo` — the Start button, the claim button, every call to action. No other button class exists on this page.

**What it depends on (define these vars, from the button set file's `:root` — do not invent values):** `--ease`, `--soul`, `--magenta`, `--purple`, `--blue`, `--green`, `--gold`. Copy the `:root` vars from the same source file.

**What NOT to change:** the gradient, the shadows, the hover lift, the theme vars, the 999px pill radius, the 14px/26px padding. A flat button is a failed build.

---

## §2 THE CALCULATOR — the kept part (copy the whole working component, don't rebuild it)

**The link — where it lives:**
- The working file (GitHub, branch `pricing/defectfix-v2`, blob af96de70, 335,857B): https://raw.githubusercontent.com/SoulSchoolAcademy/NayaPOWER/pricing/defectfix-v2/PRICING/pricing-round8-fix2.html
- Local copy (on this machine): `/tmp/pricing-fix2.html` (335,857B, 2,857 lines — freshly fetched 03:26Z; /tmp is ephemeral, so re-fetch from the URL above if it is gone).
- DESIGN-BLOCKS part (filed, GitHub main): `BRAIN/10-INTERFACES/DESIGN-BLOCKS/pricing-round7-fix1/epic-speedometer-studio-turbine-face.md` — raw: https://raw.githubusercontent.com/SoulSchoolAcademy/NayaPOWER/main/BRAIN/10-INTERFACES/DESIGN-BLOCKS/pricing-round7-fix1/epic-speedometer-studio-turbine-face.md

**The code — copy these exact ranges, verbatim, from the working file:**
- **HTML:** lines 1301–1345 — the whole `<section class="calc ...">` (pasted below so there is no fetching step for the markup).
- **Calc CSS:** lines 222–260 (`.calc-kicker` through `.calc-pace-num`).
- **Tacho CSS:** lines 511–~600 (`.tn-tacho` — the gauge the calculator mounts into).
- **Config + JS:** line 2556 (`window.NAYA_CALC_CONFIG = {...}`) + lines 2557–2812 (the `NayaCalc` script — the reusable calculator + gauge component).

**The HTML — paste this verbatim (fix-2 lines 1301–1345):**
```html
<section class="calc lit-section doc-sec sec-calc" id="calculator" tabindex="-1" aria-label="Ambassador calculator — pick your package, see your potential">
    <p class="calc-kicker">PICK YOUR PACKAGE — SHOW YOUR POTENTIAL</p>
    <h2>Calculate your income.</h2>
    <p class="calc-sub">Pick your package, see your potential. You&rsquo;re hired — tell everybody how awesome she is; they try her free, they upgrade, and you get paid. End of story.</p>
    <div class="calc-hero-example">
      <div class="calc-ex-hero big"><div class="calc-ex-num">$4 500</div><div class="calc-ex-line">a month, recurring — 3 Max sales a day</div><p>Three sales a day. <b>$50 a sale</b> — 50% of Max — every month they stay. That is <b>$54 000 a year</b>, recurring, not once.</p></div>
      <div class="calc-ex-hero"><div class="calc-ex-num">$750</div><div class="calc-ex-line">a month, recurring — 1 Pro sale a day</div><p>One sale a day. <b>$25 a day</b>, from a single sale a day. That is <b>$9 000 a year</b>.</p></div>
      <div class="calc-ex-hero"><div class="calc-ex-num">$150</div><div class="calc-ex-line">a month, recurring — 3 Max sales a month</div><p>Three sales, all month. <b>$50 a sale</b>, every month they stay. That is <b>$1 800 a year</b>.</p></div>
    </div>
    <figure class="edge-art calc-art"><img src="assets/supercharger-top-layers.webp" alt="Naya inside the turbine ring, light beams reaching the nine systems on pedestals around her." loading="lazy"><figcaption>The nine systems, around her.</figcaption></figure>
    <div class="calc-body">
      <div class="calc-gauge">
        <div id="tn-tacho-mount" role="img" aria-label="Speedometer gauge showing your potential monthly recurring earnings"></div>
        <div class="calc-readout"><span class="calc-tiles" id="calc-tiles" aria-hidden="true"></span><span id="calc-amount" class="visually-hidden" aria-live="polite">$750</span><span class="calc-per">/ month, recurring</span></div>
        <p class="calc-math" id="calc-math">1 Pro sale a day × $25 × 30 days = $750 a month ($9 000 a year)</p>
      </div>
      <div class="calc-controls">
        <p class="calc-label">Your package</p>
        <div class="calc-plans" role="group" aria-label="Pick your package">
          <button type="button" class="calc-plan" data-share="12.5" data-plan="Power" style="--sc:#c9c9d8"><span class="sdot" aria-hidden="true"></span>POWER<span>$25/mo · $12.50 a sale</span></button>
          <button type="button" class="calc-plan is-on" data-share="25" data-plan="Pro" style="--sc:#a06bff"><span class="sdot" aria-hidden="true"></span>PRO<span>$50/mo · $25 a sale</span></button>
          <button type="button" class="calc-plan" data-share="50" data-plan="Max" style="--sc:#ffbf3d"><span class="sdot" aria-hidden="true"></span>MAX<span>$100/mo · $50 a sale</span></button>
        </div>
        <p class="calc-label">Your pace</p>
        <div class="calc-pace">
          <button type="button" class="calc-step" id="calc-minus" aria-label="Fewer sales">−</button>
          <span class="calc-pace-num"><b id="calc-pace">1</b> sale<span id="calc-pace-s"></span> a <span id="calc-pace-unit">day</span></span>
          <button type="button" class="calc-step" id="calc-plus" aria-label="More sales">+</button>
        </div>
        <div class="calc-unit" role="group" aria-label="Per day or per month">
          <button type="button" class="calc-unit-btn is-on" data-unit="day">Per day</button>
          <button type="button" class="calc-unit-btn" data-unit="month">Per month</button>
        </div>
        <p class="calc-label">Play with it — the numbers above move as you do</p>
        <div class="calc-examples">
          <button type="button" class="calc-ex" data-plan="Max" data-share="50" data-pace="3" data-unit="day">3 Max a day → $4 500/mo</button>
          <button type="button" class="calc-ex" data-plan="Pro" data-share="25" data-pace="1" data-unit="day">1 Pro a day → $750/mo</button>
          <button type="button" class="calc-ex" data-plan="Max" data-share="50" data-pace="3" data-unit="month">3 Max a month → $150/mo</button>
        </div>
      </div>
    </div>
    <p class="calc-not">NOT network marketing.</p>
    <p class="calc-lines">No downline, no upline. Just the potential to get paid every day.</p>
    <p class="calc-proof">You know it is solid because you tried her for nine days. You cannot say it is not good — it is good, it is more than good, it is awesome.</p>
    <p class="calc-hired-link" style="text-align:center; margin-top:16px;"><a class="text-link" href="#start">You&rsquo;re hired — see how it works in Start Now &rarr;</a></p>
```

**The gauge — what it is (epic-speedometer-studio-turbine-face.md):** gold bezel object + toothed gear ring + concentric silver rings on the face + purple jewel centre hub + live needle `#calc-needle` — the needle angles are FIXED: `rotate(72deg)` @ $4,500, `rotate(-63deg)` @ $750, `rotate(-84.6deg)` @ $150. Counting readout + auto-demo ($750 → $4,500, no touch). The needle CSS: `#calc-needle{transform-origin:180px 178px; transition:transform .5s cubic-bezier(.2,.8,.2,1);}`. The gauge object: `.speedo-object{position:relative; width:360px; max-width:100%; aspect-ratio:1/1; margin:0 auto; border-radius:50%;...}`.

**What it's supposed to say and do:** "Calculate your income." Pick your package (Power $25/mo · $12.50 a sale / Pro $50/mo · $25 a sale / Max $100/mo · $50 a sale, Max gold-outlined), pick your pace (− / 3 sales a day / +), per day or per month — and the gauge needle, the tiled number, and the math line all move as you do. The presets: "3 Max a day → $4 500/mo", "1 Pro a day → $750/mo", "3 Max a month → $150/mo". The config (line 2556) is the source of truth for the plans: Power 25/12.5, Pro 50/25, Max 100/50; default Pro, pace 1, day; auto-sweep Max 3/day after 1500ms.

**What NOT to change:** the needle angles, the plans and shares, the presets, the math line format, the "NOT network marketing" lines, the "You're hired" link. **DEPLOY-PATH WARNING:** the art image `assets/supercharger-top-layers.webp` is a RELATIVE path — on the proof host it resolves to the host root and 400s (this is exactly how fix-2 shipped six broken images). The image MUST resolve from the served URL (proof-host `?file=` src or a served path where `assets/` exists) AND render naturalWidth > 0 in the browser, or the build FAILED.

---

## §3 THE SMART NOTE BLOCK — `.real-note` (the Top 10 + the detail views)

**The link — where it lives:**
- DESIGN-BLOCKS part (filed, GitHub main): `BRAIN/10-INTERFACES/DESIGN-BLOCKS/pricing-round7-fix1/real-notes-block.md` — raw: https://raw.githubusercontent.com/SoulSchoolAcademy/NayaPOWER/main/BRAIN/10-INTERFACES/DESIGN-BLOCKS/pricing-round7-fix1/real-notes-block.md
- Local copy: `~/workspace/smart-factory/pricing-round7-fix1/real-notes-block.md` (line 10–11).

**The code — paste this verbatim:**
```css
.real-note{background:linear-gradient(180deg,#1a1a26,#0a0a0f 72%); border:1px solid rgba(255,255,255,.16); border-left:3px solid var(--gold); border-radius:12px; padding:14px 16px; margin-bottom:10px; box-shadow:inset 0 1px 0 rgba(255,255,255,.12), 0 8px 18px rgba(0,0,0,.45);}
.cycle-step{background:linear-gradient(180deg,#1a1a26,#0a0a0f 72%); border:1px solid rgba(255,255,255,.16); border-radius:12px; padding:12px; font-size:13px; color:var(--dim); box-shadow:inset 0 1px 0 rgba(255,255,255,.12), 0 8px 18px rgba(0,0,0,.45);}
```

**What it's supposed to say and do:** the Smart Note block — the card IS the object. One intelligence in short layered views: Nutshell, Human, Child, Grandma, Naya. Orb + label + ONE short paragraph + colored glow. Scannable. This is the form for the Top 10 (Amendment 3 §7) and for the chart detail views (Amendment 3 §6). The block contains REAL notes (SN-0831, SN-0883, SN-2076) with verbatim lines — never invented copy.

**What NOT to change:** the gradient, the 1px border, the 3px gold left border, the 12px radius, the inset highlight + the 0 8px 18px shadow. No nested boxes inside a `.real-note`. No meta-text. No four-paragraph essays.

---

## §4 THE ORB — `.ib-card-orb` (the Top 10's orb + the Hub's Smart Note orb)

**The link — where it lives:**
- The Hub file (local, on this machine): `~/workspace/team-nitro/hub/index-2-fixed-v2.html` — lines 2641–2665 (the `.ib-card-orb` rule block). The orb color var `--oc` is set at line 2603.

**The code — paste this verbatim (Hub lines 2641–2665):**
```css
.ib-card-orb {
  width: 42px; height: 42px; flex: none; margin: 1px 0 0 18px;
  background:
    radial-gradient(circle at 34% 26%, #ffffff 0%, rgba(255,255,255,.85) 10%, rgba(255,255,255,.28) 22%, transparent 38%),
    radial-gradient(circle at 50% 60%, rgba(255,255,255,.22) 0%, transparent 48%),
    radial-gradient(circle at 50% 50%, var(--oc) 0%, color-mix(in srgb, var(--oc) 88%, #fff) 28%, color-mix(in srgb, var(--oc) 72%, #000) 68%, #050507 100%);
  box-shadow:
    inset 0 0 0 2px rgba(255,255,255,.55),
    inset 0 8px 16px rgba(255,255,255,.22),
    inset 0 -10px 20px rgba(0,0,0,.55),
    0 0 22px rgba(var(--oc-rgb),.9),
    0 0 55px -8px rgba(var(--oc-rgb),.6),
    0 14px 30px rgba(0,0,0,.6);
}
.ib-card-orb::before {
  inset: -4px; padding: 3px;
  filter: drop-shadow(0 0 20px var(--oc)) drop-shadow(0 0 8px #fff);
}
.ib-card-orb::after { bottom: -18px; height: 16px;
  background: radial-gradient(ellipse, rgba(var(--oc-rgb),.55), transparent 70%); }
.ib-card-orb.playing { animation: ib-orb-flow 1.6s ease-in-out infinite !important; }
.ib-card-orb.reading { animation: ib-orb-flow 2.8s ease-in-out infinite !important; }
```

**What it's supposed to say and do:** the orb IS the object — a real jewel, not a flat circle. The color lives in the `--oc` var (set per card, line 2603) and its `--oc-rgb` twin. The orb glows with its own color. The playback states (`.playing` / `.reading`) are the NayaVoice contract (Shawn 2026-10-20): the orb flows while she prepares her reading and while she speaks.

**What NOT to change:** the gradients, the shadows, the glow, the 42px size, the `--oc` var. A flat circle is a failed build.

---

## §5 THE JEWEL BULLETS + THE ICON SOCKET (one has code, one is a named gap)

**The jewel bullets — the link + what to use:**
- DESIGN-BLOCKS part (filed, GitHub main): `BRAIN/10-INTERFACES/DESIGN-BLOCKS/pricing-round7-fix1/gem-bullets-naya-jwl.md` — raw: https://raw.githubusercontent.com/SoulSchoolAcademy/NayaPOWER/main/BRAIN/10-INTERFACES/DESIGN-BLOCKS/pricing-round7-fix1/gem-bullets-naya-jwl.md
- Canonical source: `team-nitro/smart-builder/PIECES-INVENTORY-v2.json` — NAYA-JWL-016 = `.mini-gem.circle` jewel, source `Naya_Ultimate_Design_System_-_Naya_2.html`.
- **Construction (paste the pattern, don't invent it):** "drawn jewel, not a dot" — a small faceted gem (radial gradient, top-left highlight, glow) used as the bullet for tier list items. Applied: the tier cards' list items carry diamond/gem bullets (per-tier accent). The jewel "i" button for the chart rows is the same jewel form (Amendment 1 §2 — `gem-bullets-naya-jwl.md` + the Hub's jewel spans/NayaJewels, 306 spans proven live).

**The icon socket — A NAMED GAP, not a piece with code:**
- DESIGN-BLOCKS part: `BRAIN/10-INTERFACES/DESIGN-BLOCKS/pricing-round7-fix1/icon-socket-naya-ico-023.md` — raw: https://raw.githubusercontent.com/SoulSchoolAcademy/NayaPOWER/main/BRAIN/10-INTERFACES/DESIGN-BLOCKS/pricing-round7-fix1/icon-socket-naya-ico-023.md
- **Status: SAY SO — no canonical source located.** The inventory (`PIECES-INVENTORY-v2.json`) has the entry "Icon socket" and nothing more; the catalog (`block-catalog.json`) has NO entry for NAYA-ICO-023. No CSS source file was located. **This is not a filed object with a source — it is a named gap.**
- **What the seat does:** use the 40px tinted-tile spec from the inventory entry + the four-page look (the system jewels were sized 48→40px with an 18px glyph). **Do NOT invent CSS for the icon socket.** If a canonical source is located later, it gets appended to the part file — never invented. A gap named honestly beats a fake source every time.

---

## §6 THE DECK SLIDE — the page IS a deck (viewpoint by viewpoint)

**The link — where it lives:**
- DESIGN-BLOCKS part (filed, GitHub main): `BRAIN/10-INTERFACES/DESIGN-BLOCKS/pricing-round7-fix1/deck-slide.md` — raw: https://raw.githubusercontent.com/SoulSchoolAcademy/NayaPOWER/main/BRAIN/10-INTERFACES/DESIGN-BLOCKS/pricing-round7-fix1/deck-slide.md
- Local copy: `~/workspace/smart-factory/pricing-round7-fix1/deck-slide.md`.

**The code — paste this verbatim:**
```css
.slide{height:100vh; height:100svh; overflow-y:auto; scroll-snap-align:start; scroll-snap-stop:always; box-shadow:inset 0 1px 0 rgba(255,255,255,.07);}
.js-deck .slide{opacity:.85; transform:scale(.998); transition:opacity .35s ease, transform .35s ease;}
.js-deck .slide.arrived{opacity:1; transform:none;}
```

**What it's supposed to say and do:** the page IS a deck. Each major section is a full-viewport slide (min-height 100vh; 100svh on phone). Scroll snapping locks each section into view; no straddling, no cut content, nothing hidden under the sticky bar (the bar is in-flow, `position:static`, so it can never cover a locked slide). Long sections (chart, Top 10) scroll INSIDE their slide, then the page snaps on. Reduced motion turns snapping off (the deck unrolls to a normal document); keyboard moves slide to slide; the snap never traps the user or fights the wheel. The arrival settle is 350ms (opacity .85, 0.2% scale — the translateY was REMOVED, it caused +9px snap offsets). Round 7 proved 13 slides, document height at 1920 exactly 14,040px = 13 × 1,080.

**What NOT to change:** the 100vh/100svh, the snap alignment, the in-flow sticky bar, the opacity + scale(.998) arrival (never translateY). This is the viewpoint-by-viewpoint law in code — the premium design algorithm (Shawn 03:33Z): each screen a complete, optimized viewpoint, always mobile optimized.

---

## §7 THE HERO — the beginning (copy the markup, don't rewrite it)

**The link — where it lives:**
- The round-7 fix1 file (local, on this machine): `~/workspace/verify-pricing-v6/pricing-round7-fix1-work.html` (sha256 99514923…, 294,207B, 2,578 lines) — the hero is lines 1291–1317 (`<section class="banner-top slide" aria-label="Meet the Naya Supercharger">`).
- DESIGN-BLOCKS part (filed, GitHub main): `BRAIN/10-INTERFACES/DESIGN-BLOCKS/pricing-round7-fix1/hero-wide-composition-nine-systems-panel.md` — raw: https://raw.githubusercontent.com/SoulSchoolAcademy/NayaPOWER/main/BRAIN/10-INTERFACES/DESIGN-BLOCKS/pricing-round7-fix1/hero-wide-composition-nine-systems-panel.md

**The code — paste this verbatim (round-7 fix1 lines 1291–1317):**
```html
<section class="banner-top slide" aria-label="Meet the Naya Supercharger">
  <div class="banner-map">
  <img class="banner-img" src="banner-assets/ChatGPT_Image_Nov_6__2026__06_06_21_PM.png" alt="Meet the Naya Supercharger — Naya in the gauge, the nine systems as capsules around her: Personality, Brain, Notes, Lead Mode, Law, Scorecarding, Language, Design, Coder.">
  </div>
  <div class="banner-head hero-band">
<div class="kicker">BUILD YOUR WORLD — THE INTERNET, REBUILT</div>
    <h1>The Internet, Rebuilt.</h1>
    <p class="manifesto">We're not building another app — we're rebuilding the internet itself, in a smarter, better way.</p>
    <p class="tech">A new technology, not a new app: <b>Collective Chain Technology</b> — the value and the intelligence, given back to you and shared with everybody.</p>
    <p class="mission">The old internet fails people — dead projects, forgotten chats, AI with amnesia. Something like 99 out of 100 never get what they came for. Our mission is 100% success: everybody who uses her, succeeds.</p>
    <p class="sub">The new internet — intelligent, automated collective intelligence. A network for AIs and humans to collaborate. Plug any AI into her — ChatGPT, Muse, Claude — she is the mothership for all AIs and humans. Put a supercharger on your AI, and connect to the ultimate supercharger: a supercharged network.</p>
    <p class="demo-starter">Three questions. Your world appears.</p>
    <div class="hero-cta">
      <input type="text" class="claim-name" id="claimNameHero" placeholder="Your name" aria-label="Your name — the name you want to claim" maxlength="32" autocomplete="off">
      <a class="btn btn-max" href="https://nayanet.app/yourname" data-claim><span class="btn-inner"><span class="btn-star" aria-hidden="true">★</span>Claim your name</span></a>
      <span class="hero-cta-note">Drive the Bugatti before you buy her — 9 days at Max Power.</span>
    </div>
  </div>
</section>
```

**What it's supposed to say:** the kicker "BUILD YOUR WORLD — THE INTERNET, REBUILT", the headline "The Internet, Rebuilt.", the manifesto, the tech line (Collective Chain Technology), the mission (100% success — everybody who uses her, succeeds), the sub (plug any AI into her — she is the mothership for all AIs and humans), "Three questions. Your world appears.", and the claim-your-name call to action ("Drive the Bugatti before you buy her — 9 days at Max Power."). **Note:** the claim button in this markup is `.btn btn-max` — in the rebuild it becomes `.primo theme-gold` (§1); the words and the link (`https://nayanet.app/yourname`) stay.

**DEPLOY-PATH WARNING:** the banner image `banner-assets/ChatGPT_Image_Nov_6__2026__06_06_21_PM.png` is a RELATIVE path — it MUST resolve from the served URL and render naturalWidth > 0, or the build FAILED (the fix-2 lesson).

**What NOT to change:** the words. The hero's copy is his — the kicker, the headline, the manifesto, the mission, the sub. Content adaptation (the button class, per §1) is allowed; restyling or rewriting the copy is not.

---

## §8 THE CHART FORM — the DRAFT v4 table (the form, not the facts) + the RECORDS (the facts)

**The link — the form (where it lives):**
- The DRAFT v4 table file (local, on this machine): `~/workspace/user/files/pricing-table-DRAFT-v4-2.html` (14,425B, Nov 6 20:42 — "ten times better, at least you could read it": one compact table, one row per feature, four columns, orbs, scannable).
- **The form to copy:** one compact table, one row per feature, four tier columns, orbs. The tier cards: NAYANET $25/mo "The whole living system." ($50 for 3 months · $150 a year — saves you $150 · $300 lifetime, founding only — 1,000 members, then closed forever) · NAYA PRO $50/mo MOST CHOSEN "For builders — box, sites, reach." ($300 a year · Smart Box · 3 membership sites (proposed) · Smart Mail up to 100,000/mo) · NAYANET MAX $100/mo "For sellers — more of everything." ($600 a year · 10 membership sites (proposed) · Affiliate system for your own products · 300 smart apps a month). **The DRAFT v4 numbers are Oct 30 and partly superseded — the rebuild uses its FORM with the settled content of Amendment 3 §5.**

**The link — the facts (where they live):**
- The RECORDS data block: fix-2, line 2506+ — `RECORDS = {"power":…, "pro":…, "max":…, "seats":…, "reason-01"…"reason-10":…, "chart-01"…"chart-36":…}` (same file as §2: https://raw.githubusercontent.com/SoulSchoolAcademy/NayaPOWER/pricing/defectfix-v2/PRICING/pricing-round8-fix2.html).
- **The chart cells are Amendment 3 §5** — all 36 rows in 5 groups, the EXACT cells (≤8 words each). The detail views are Amendment 3 §6 — the 7-part mapping + the full 7 parts written out for the 6 deciding rows. **Do not re-derive the cells from the DRAFT v4 or the chart images — the cells are Amendment 3 §5, verbatim.**

**What it's supposed to say and do:** the chart intro is Amendment 3 §4 (fix-2, harvested verbatim: "What the money buys." + the intro + the tier header + the ladder line + the trial line). Every feature row carries a jewel "i" button (§5 above); click it and the detail view opens IN YOUR VIEWPOINT (overlay, not a new page) with the 7 parts in order (Amendment 1 §2, Amendment 3 §6). Close → back to the chart at the same scroll position. On hover, the boards separate. The chart must show the DIFFERENCE between the tiers at a glance — if every cell says "Included at every level", the chart has failed.

---

## §9 THE IMAGES — the links (every image, where it is, what it's for)

**The ten images (Amendment 2 §6 — all verified on disk at `~/workspace/user/media_library/image/`):**
- Banners (the bookends — top + bottom): `Naya_World.png` (2172×724, 2,361,788B) + `naya_world_2.png` (2172×724, 2,467,741B). One is "Skip the struggle. Start further ahead. — THE NAYA SUPERCHARGER TURNS AI FRICTION INTO FLOW." The other is "Meet the Naya Supercharger. — SAME AI. DIFFERENT OPERATING SYSTEM. One intelligence. Nine activated systems." **Open both files, confirm which is which, and record the mapping in the checkpoint** (the captain could not map filename→banner with certainty).
- Art shots (webp): `media-generation-supercharger-top-cinema-0-0eee6949-f828-4279-b041-86a01b3c6ae3.webp` (2352×1008, 451,844B) · `media-generation-supercharger-top-studio-0-dedbcf4d-7761-46e2-ba60-9d68f9b168ad.webp` (2240×1120, 366,828B) · `media-generation-supercharger-bottom-v2-0-c5e1ce98-6667-4a1b-8b5b-4f6f57802f77.webp` (1920×1280, 489,760B) · `media-generation-supercharger-top-v2-0-e771f629-9f0b-444e-9e4d-be8665d8cb03.webp` (1920×1280, 630,632B) · `media-generation-pricing-banner-bottom-royal-0-cb335ee7-65b9-499a-9994-efd0137685b9.webp` (2352×1008, 540,454B).
- Chart files (the FORM, not the facts — Amendment 2's content warning stands): `Naya_Chart_option.png` (1171×841, 96,053B) · `image_2026-11-07_201421768.png` (1158×322, 34,648B) · `Naya_Chart_option_2.png` (1158×322, 39,183B).

**The Top 10 images (Amendment 3 §7):** `assets/TOP_TEN_NAYANET.png` (items 1–7) + `assets/TOP_TEN_NAYANET_2.png` (items 8–10), from Shawn's dictation. **DEPLOY-PATH LAW (absolute):** every image must render naturalWidth > 0 from the served URL — the asset paths must resolve from the served URL, not from the `?file=` form. Any image 0×0 = build FAILED.

**What to do with them (Amendment 2 §3):** take the best of the best; use whatever ones (NOT all ten required); MODIFY the images — crop, compose, layer, reframe, resize — anything, to make it a work of art (his own words). Record in the checkpoint for every image used: file → slot on the page → what was done to it (as-is / cropped / composed / layered / reframed).

---

## §10 THE LINKS — all of them, in one place (so nothing has to be hunted for)

| Piece | Link (where it is) |
|---|---|
| Calculator + gauge + RECORDS (the working file) | https://raw.githubusercontent.com/SoulSchoolAcademy/NayaPOWER/pricing/defectfix-v2/PRICING/pricing-round8-fix2.html — branch `pricing/defectfix-v2`, blob af96de70, 335,857B; local `/tmp/pricing-fix2.html` |
| `.primo` button (the code) | `~/workspace/team-nitro/smart-builder/scratch/trial1-p2/HUB/design-system/library/buttons/Naya_Beautiful_Button_Set_N4.html` lines 238–247; also `~/workspace/user/files/Naya_Beautiful_Button_Set_N4.html` |
| Chrome button part | https://raw.githubusercontent.com/SoulSchoolAcademy/NayaPOWER/main/BRAIN/10-INTERFACES/DESIGN-BLOCKS/pricing-round7-fix1/chrome-button-naya-btn-027.md |
| Smart Note block part | https://raw.githubusercontent.com/SoulSchoolAcademy/NayaPOWER/main/BRAIN/10-INTERFACES/DESIGN-BLOCKS/pricing-round7-fix1/real-notes-block.md |
| Orb (the Hub file) | `~/workspace/team-nitro/hub/index-2-fixed-v2.html` lines 2641–2665 (orb color var `--oc` at line 2603) |
| Jewel bullets part | https://raw.githubusercontent.com/SoulSchoolAcademy/NayaPOWER/main/BRAIN/10-INTERFACES/DESIGN-BLOCKS/pricing-round7-fix1/gem-bullets-naya-jwl.md |
| Icon socket part (NAMED GAP) | https://raw.githubusercontent.com/SoulSchoolAcademy/NayaPOWER/main/BRAIN/10-INTERFACES/DESIGN-BLOCKS/pricing-round7-fix1/icon-socket-naya-ico-023.md |
| Deck slide part | https://raw.githubusercontent.com/SoulSchoolAcademy/NayaPOWER/main/BRAIN/10-INTERFACES/DESIGN-BLOCKS/pricing-round7-fix1/deck-slide.md |
| Speedometer part | https://raw.githubusercontent.com/SoulSchoolAcademy/NayaPOWER/main/BRAIN/10-INTERFACES/DESIGN-BLOCKS/pricing-round7-fix1/epic-speedometer-studio-turbine-face.md |
| Hero (round-7 fix1 file) | `~/workspace/verify-pricing-v6/pricing-round7-fix1-work.html` lines 1291–1317 (294,207B, 2,578 lines) |
| Hero part | https://raw.githubusercontent.com/SoulSchoolAcademy/NayaPOWER/main/BRAIN/10-INTERFACES/DESIGN-BLOCKS/pricing-round7-fix1/hero-wide-composition-nine-systems-panel.md |
| Chart form (DRAFT v4) | `~/workspace/user/files/pricing-table-DRAFT-v4-2.html` (14,425B) |
| Images (the ten) | `~/workspace/user/media_library/image/` (see §9 for the file names) |
| The words (the page, top to bottom) | Amendment 3 — `TEAM-NITRO/pricing/PRICING-REBUILD-AMENDMENT-3-THE-WORDS.md` (blob e9c02913) |
| The standard (the brief + the gates) | The airtight brief — `TEAM-NITRO/pricing/PRICING-REBUILD-BRIEF-AIRTIGHT.md` (blob 52aa7543) |

---

## §11 THE GATE (extended — the copy-paste gate)

1. **Copy-paste, don't re-derive.** Every piece above has its code pasted in this amendment or its exact line ranges named. The seat pastes the code. It does not summarize it, rewrite it, "adapt" it, or "improve" it. Content adaptation (menu items, the button class per §1, the image treatment per §9) is allowed; restyling the component is not.
2. **Any deviation from the pasted code = build FAILED.** Do not file, do not report.
3. **Any invented replacement = build FAILED.** If a piece has no canonical code, it is named as a GAP (§5, the icon socket) — the seat uses the spec given and does NOT invent code to fill it.
4. **Any word on the page without a named source = build FAILED** (Amendment 3 §11).
5. **Any chart cell over 8 words = FAILED. Any detail-view line stating a fact not in the RECORDS = FAILED. Any image 0×0 from the served URL = FAILED.** Any "every Wednesday" = FAILED. Any "3 / 10 membership sites" = FAILED. Any "Fork" = FAILED.
6. **The checkpoint MUST list, for EVERY element on the page:** the element + its source part + its file + its line (or its pasted section in this amendment). Any element without a source = build FAILED.
7. **Verification (unchanged):** the maker scorecards the EXPERIENCE with rendered screenshots (every image naturalWidth > 0, the calculator's needle + tiles + math line moving, a jewel "i" opening the 7-part detail view and closing back to the same scroll position, the deck slides locking into view, the hero rendering with its banner image); a different seat scores the experience; the captain looks with her own eyes (phone first) before anything reaches Shawn.

**DONE defined first (this amendment's additions):** the seat's checkpoint carries the §10 link list with a ✓ beside every link it actually used; the pasted code is in the file byte-for-byte where the amendment says it is (the captain will diff it); the icon socket is built to the 40px tinted-tile spec and NOTHING invented; every image renders naturalWidth > 0 from the served URL.
