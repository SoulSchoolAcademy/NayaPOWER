# CHECKOUT — the payment block family

*Shipped by the BUILD seat, Team Nitro, 2026-10-16. Status: NEW. Shippable specs — real code, real states, no mock chrome.*

Money is the most trust-sensitive surface in the product. These five blocks carry the checkout: what you're buying, how you pay, what happened next. Every block below ships with its code, its states, a do/don't, and honest anatomy. A block without all four is a draft — these have all four.

Law citations per block: Law 1 (ALIVE — nothing flat, nothing dead), Law 2 (SPECTRUM — one color per object, gold never worn at rest by buttons, purple for chrome), Law 3 (ELEVATION — the board formula), Law 5 (BUTTONS — one `.naya-btn` DNA), Law 6 (TYPE — Georgia voice for headers, white 99%). Spectrum jobs kept clean: **gold = attention, earned** (the total, the final word); **purple = choosing intelligence** (primary actions, selection); **emerald = alive and well** (valid, confirmed); **red = urgency, not alarm** (errors, calm, actionable).

All five blocks are theme-safe: they own no page accent and don't clump — each ignites its own tone, never a shared flood.

---

## PAY-001 — Order summary board

**Law:** Law 3 (board formula, tone spine, corner jewel, 5px lift, own-tone ignition) · Law 1 (the total rests white, ignites gold — gold is attention, earned). Data-table law: labels left, numbers right.

What it is: the board that says "here is what you're paying for" before any money moves. Line items, quantities, one promo code, the three rows that matter, and one honest line so nobody feels tricked at the total.

### The code

```html
<section class="pay-board pay-summary" aria-label="Order summary">
  <span class="pay-corner" aria-hidden="true"><i>◆</i></span>
  <header class="pay-head">
    <p class="pay-kicker">CHECKOUT</p>
    <h3 class="pay-title">Your order</h3>
  </header>

  <ul class="pay-items">
    <li class="pay-item" data-tone="magenta">
      <span class="pay-thumb" aria-hidden="true"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2l2.2 7.8L22 12l-7.8 2.2L12 22l-2.2-7.8L2 12l7.8-2.2z"/></svg></span>
      <div class="pay-item-body">
        <span class="pay-item-name">Naya MAXIS AI Score</span>
        <span class="pay-item-meta">Annual membership · renews Oct 2027</span>
      </div>
      <div class="pay-stepper" role="group" aria-label="Quantity for Naya MAXIS AI Score">
        <button type="button" class="naya-btn icon micro pay-step" aria-label="Decrease quantity">−</button>
        <output class="pay-qty" aria-live="polite">1</output>
        <button type="button" class="naya-btn icon micro pay-step" aria-label="Increase quantity">+</button>
      </div>
      <span class="pay-price">$149.00</span>
    </li>
    <li class="pay-item" data-tone="purple">
      <span class="pay-thumb" aria-hidden="true"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 4l9 16H3z"/></svg></span>
      <div class="pay-item-body">
        <span class="pay-item-name">AI Masterclass seat</span>
        <span class="pay-item-meta">Cohort 12 · starts Nov 3</span>
      </div>
      <div class="pay-stepper" role="group" aria-label="Quantity for AI Masterclass seat">
        <button type="button" class="naya-btn icon micro pay-step" aria-label="Decrease quantity">−</button>
        <output class="pay-qty" aria-live="polite">2</output>
        <button type="button" class="naya-btn icon micro pay-step" aria-label="Increase quantity">+</button>
      </div>
      <span class="pay-price">$298.00</span>
    </li>
    <li class="pay-item" data-tone="blue">
      <span class="pay-thumb" aria-hidden="true"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3l9 9-9 9-9-9z"/></svg></span>
      <div class="pay-item-body">
        <span class="pay-item-name">Powercast bundle</span>
        <span class="pay-item-meta">14 episodes · yours to keep</span>
      </div>
      <div class="pay-stepper" role="group" aria-label="Quantity for Powercast bundle">
        <button type="button" class="naya-btn icon micro pay-step" aria-label="Decrease quantity">−</button>
        <output class="pay-qty" aria-live="polite">1</output>
        <button type="button" class="naya-btn icon micro pay-step" aria-label="Increase quantity">+</button>
      </div>
      <span class="pay-price">$49.00</span>
    </li>
  </ul>

  <form class="pay-promo" action="#" onsubmit="return false">
    <label class="pay-promo-label" for="promo-code">Promo code</label>
    <div class="pay-promo-row">
      <input id="promo-code" class="pay-promo-input" type="text"
             placeholder="Enter code" autocomplete="off" spellcheck="false">
      <button type="submit" class="naya-btn">Apply</button>
    </div>
    <p class="pay-promo-msg" aria-live="polite"></p>
  </form>

  <dl class="pay-totals">
    <div class="pay-total-row"><dt>Subtotal</dt><dd>$496.00</dd></div>
    <div class="pay-total-row"><dt>Estimated tax</dt><dd>$39.68</dd></div>
    <div class="pay-total-row pay-grand"><dt>Total</dt><dd>$535.68</dd></div>
  </dl>

  <p class="pay-honest">Prices confirmed at checkout. The total is the total — no surprises on the next step.</p>
</section>
```

```css
/* ---------- PAY tokens ---------- */
.pay-board{
  --ground:#050507; --ink:#fbfbfd;
  --magenta:#e84fff; --purple:#a06bff; --indigo:#6675ff; --blue:#3fb8ff;
  --emerald:#35e0a1; --green:#2fe89e; --lime:#b8ee57; --gold:#ffbf3d;
  --orange:#ff9a5a; --red:#ff5e6c;
  --ease:cubic-bezier(.16,.84,.22,1);
  --tone:#a06bff; --tone-rgb:160,107,255; /* default: choosing intelligence */
  background:linear-gradient(160deg,#1a171f 0%,#09090d 55%,#030304 100%);
  border:1.5px solid rgba(160,107,255,.38);
  border-radius:24px;
  box-shadow:
    inset 0 2px 2px rgba(255,255,255,.12),
    inset 0 -8px 18px rgba(0,0,0,.55),
    0 5px 0 #020203,
    0 17px 0 -8px rgba(160,107,255,.16),
    0 35px 75px rgba(0,0,0,.7),
    0 0 40px -17px rgba(160,107,255,.5);
  padding:28px 30px 26px;
  position:relative;
  transition:border-color .28s var(--ease), box-shadow .28s var(--ease), transform .28s var(--ease);
}
.pay-board:hover{
  transform:translateY(-5px);
  border-color:rgba(160,107,255,.8);
  box-shadow:
    inset 0 2px 2px rgba(255,255,255,.14),
    inset 0 -8px 18px rgba(0,0,0,.55),
    0 5px 0 #020203,
    0 17px 0 -8px rgba(160,107,255,.2),
    0 35px 75px rgba(0,0,0,.7),
    0 0 46px -14px rgba(160,107,255,.85);
}
.pay-corner{
  position:absolute; top:14px; right:16px; font-size:22px; color:#fff;
  text-shadow:0 0 14px rgba(160,107,255,.9); opacity:.9;
}
.pay-head{ margin:0 0 20px; }
.pay-kicker{
  margin:0 0 6px; font-size:12px; letter-spacing:.32em; color:rgba(255,255,255,.72);
}
.pay-title{
  margin:0; font-family:Georgia,'Times New Roman',serif; font-size:24px;
  font-weight:600; color:var(--ink);
  text-shadow:0 2px 8px rgba(0,0,0,.6), 0 0 22px rgba(160,107,255,.35);
}

/* line items */
.pay-items{ list-style:none; margin:0 0 8px; padding:0; }
.pay-item{
  --jc:#a06bff; --jc-rgb:160,107,255;
  display:flex; align-items:center; gap:14px;
  padding:13px 14px; border-radius:16px;
  border:1.5px solid rgba(255,255,255,.14);
  background:rgba(255,255,255,.03);
  margin-bottom:10px;
  transition:border-color .18s var(--ease), box-shadow .18s var(--ease), transform .18s var(--ease);
}
.pay-item[data-tone="magenta"]{ --jc:#e84fff; --jc-rgb:232,79,255; }
.pay-item[data-tone="purple"]{ --jc:#a06bff; --jc-rgb:160,107,255; }
.pay-item[data-tone="blue"]{ --jc:#3fb8ff; --jc-rgb:63,184,255; }
.pay-item[data-tone="green"]{ --jc:#2fe89e; --jc-rgb:47,232,158; }
.pay-item[data-tone="gold"]{ --jc:#ffbf3d; --jc-rgb:255,191,61; }
.pay-item:hover{
  transform:translateY(-2px);
  border-color:rgba(var(--jc-rgb),.75);
  box-shadow:0 0 26px -6px rgba(var(--jc-rgb),.65);
}
.pay-thumb{
  flex:0 0 44px; width:44px; height:44px; display:grid; place-items:center;
  font-size:17px; color:#fff;
  transform:rotate(45deg); border-radius:9px;
  border:1px solid rgba(255,255,255,.85);
  background:radial-gradient(circle at 32% 28%, #fff 0%, var(--jc) 42%, #050507 100%);
  box-shadow:0 0 18px rgba(var(--jc-rgb),.55);
}
/* thumb glyphs are drawn SVG (Law 4: icons are drawn) — the diamond frame is CSS
   geometry, the glyph inside is vector; no unicode symbols anywhere */
.pay-thumb svg{
  width:16px; height:16px; fill:#fff; flex:none;
  transform:rotate(-45deg); /* glyph stays upright inside the diamond */
}
.pay-item-body{ flex:1 1 auto; min-width:0; }
.pay-item-name{ display:block; font-size:15px; font-weight:600; color:#fbfbfd; }
.pay-item-meta{ display:block; font-size:13px; color:rgba(255,255,255,.72); margin-top:2px; }

/* qty stepper — the buttons ARE .naya-btn.icon.micro: the one DNA, no bespoke
   button system. .pay-step carries only the stepper's glyph sizing; every
   button visual — gradient heart, white-ish idle border, insets, lift,
   flowing conic ring, press — comes from .naya-btn. The 44px circle is
   Law 5's minimum touch target. */
.pay-stepper{ display:flex; align-items:center; gap:8px; }
.pay-step{ font-size:17px; line-height:1; flex:none; }
.pay-qty{ min-width:22px; text-align:center; font-size:15px; font-weight:700; color:#fbfbfd; }
.pay-price{ font-size:15px; font-weight:700; color:#fbfbfd; min-width:78px; text-align:right; font-variant-numeric:tabular-nums; }

/* promo */
.pay-promo{ margin:16px 0 4px; }
.pay-promo-label{ display:block; font-size:12px; letter-spacing:.24em; color:rgba(255,255,255,.72); margin-bottom:8px; }
.pay-promo-row{ display:flex; gap:10px; }
.pay-promo-input{
  flex:1 1 auto; height:50px; padding:0 16px; border-radius:14px;
  background:#0a0a0e; color:#fbfbfd; font-size:15px;
  border:1.5px solid rgba(255,255,255,.55);
  transition:border-color .18s var(--ease), box-shadow .18s var(--ease);
}
.pay-promo-input::placeholder{ color:rgba(255,255,255,.45); }
.pay-promo-input:focus{ outline:none; border-color:#a06bff; box-shadow:0 0 26px -4px rgba(160,107,255,.8); }
.pay-promo-msg{ min-height:20px; font-size:14px; margin:8px 0 0; color:rgba(255,255,255,.72); }
.pay-promo.is-applied .pay-promo-input{ border-color:#35e0a1; box-shadow:0 0 26px -6px rgba(53,224,161,.6); }
.pay-promo.is-applied .pay-promo-msg{ color:#35e0a1; }
.pay-promo.is-invalid .pay-promo-input{ border-color:#ff5e6c; box-shadow:0 0 26px -6px rgba(255,94,108,.6); }
.pay-promo.is-invalid .pay-promo-msg{ color:#ff8a96; }

/* ---------- .naya-btn — the one button DNA (canonical, per DESIGN/BLOCKS.md) ----------
   54px min-height, 999px radius, black gradient heart, 1.5px white-ish idle
   border, inset top-light + inset bottom-shadow + drop shadow. Hover lifts
   with a flowing conic ring; press compresses. No flat buttons — ever.
   The icon variant is glyph-only: 58px circle, .micro 44px.
   Ships from one canonical source (family contract §7) — import, never re-type. */
.naya-btn{
  --nb-accent:#a06bff; --nb-accent-rgb:160,107,255;
  position:relative;
  display:inline-flex; align-items:center; justify-content:center; gap:10px;
  min-height:54px; padding:0 26px; border-radius:999px; cursor:pointer;
  background:linear-gradient(180deg,#101014 0%,#050505 60%,#020203 100%);
  color:#fbfbfd; font-size:14px; font-weight:700; letter-spacing:.08em; text-transform:uppercase;
  border:1.5px solid rgba(255,255,255,.85);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.22), inset 0 -6px 12px rgba(0,0,0,.6), 0 10px 24px rgba(0,0,0,.6);
  transition:border-color .18s cubic-bezier(.16,.84,.22,1), box-shadow .18s cubic-bezier(.16,.84,.22,1), transform .18s cubic-bezier(.16,.84,.22,1);
}
/* the flowing conic ring — ignition you can watch travel */
.naya-btn::after{
  content:""; position:absolute; inset:-3px; border-radius:inherit; pointer-events:none;
  background:conic-gradient(from 0deg, transparent 0deg, rgba(var(--nb-accent-rgb),.95) 50deg, transparent 100deg);
  -webkit-mask:radial-gradient(farthest-side, transparent calc(100% - 3px), #000 calc(100% - 2px));
  mask:radial-gradient(farthest-side, transparent calc(100% - 3px), #000 calc(100% - 2px));
  opacity:0; transition:opacity .18s cubic-bezier(.16,.84,.22,1);
}
.naya-btn:hover{
  transform:translateY(-2px);
  border-color:var(--nb-accent);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.25), inset 0 -6px 12px rgba(0,0,0,.6), 0 10px 24px rgba(0,0,0,.6), 0 0 32px -4px rgba(var(--nb-accent-rgb),.8);
}
.naya-btn:hover::after{ opacity:1; animation:nb-ring 1.5s linear infinite; }
.naya-btn:active{ transform:translateY(1px) scale(.98); }
.naya-btn:focus-visible{ outline:2px solid #fff; outline-offset:4px; }
.naya-btn:disabled{ opacity:.45; cursor:not-allowed; transform:none; box-shadow:inset 0 -6px 12px rgba(0,0,0,.6); }
.naya-btn:disabled:hover{ border-color:rgba(255,255,255,.85); }
.naya-btn:disabled::after{ display:none; }
@keyframes nb-ring{ to{ transform:rotate(360deg); } }
/* icon variant — glyph-only actions */
.naya-btn.icon{ width:58px; height:58px; min-height:0; padding:0; border-radius:50%; }
.naya-btn.icon.micro{ width:44px; height:44px; }

/* totals: labels left, numbers right — the table law */
.pay-totals{ margin:14px 0 0; }
.pay-total-row{
  display:flex; justify-content:space-between; align-items:baseline;
  padding:9px 2px; font-size:15px;
  border-bottom:1px solid rgba(255,255,255,.1);
}
.pay-total-row dt{ color:rgba(255,255,255,.88); }
.pay-total-row dd{ margin:0; color:#fbfbfd; font-weight:600; font-variant-numeric:tabular-nums; }
.pay-grand{ border-bottom:none; margin-top:6px; padding:12px 10px 4px; border-radius:14px;
  border:1.5px solid rgba(255,255,255,.2);
  transition:border-color .28s var(--ease), box-shadow .28s var(--ease), transform .28s var(--ease);
}
.pay-grand dt{
  font-family:Georgia,'Times New Roman',serif; font-size:18px; font-weight:600; color:#fbfbfd;
}
.pay-grand dd{
  font-family:Georgia,'Times New Roman',serif; font-size:26px; font-weight:700; color:#fbfbfd;
  text-shadow:0 2px 10px rgba(0,0,0,.6);
}
.pay-grand:hover{
  transform:translateY(-2px);
  border-color:#ffbf3d;
  box-shadow:0 0 38px -8px rgba(255,191,61,.75);
}
.pay-grand:hover dd{
  color:#fff4dd;
  text-shadow:0 0 18px rgba(255,191,61,.85), 0 2px 10px rgba(0,0,0,.6);
}
.pay-honest{ margin:16px 2px 0; font-size:13px; color:rgba(255,255,255,.68); }

/* honest empty state — quiet, but never dead */
.pay-summary.is-empty .pay-items,
.pay-summary.is-empty .pay-promo,
.pay-summary.is-empty .pay-totals{ display:none; }
.pay-empty{ display:none; text-align:center; padding:34px 10px 26px; }
.pay-summary.is-empty .pay-empty{ display:block; }
.pay-empty .pay-title{ margin-bottom:8px; }
.pay-empty p{ color:rgba(255,255,255,.72); font-size:15px; margin:0 0 18px; }

@media (prefers-reduced-motion:reduce){
  .pay-board,.pay-item,.pay-step,.naya-btn,.pay-grand{ transition:none; }
  .pay-board:hover,.pay-item:hover,.pay-step:hover,.naya-btn:hover,.pay-grand:hover{ transform:none; }
  .naya-btn:hover::after{ opacity:0; animation:none; } /* the conic ring never shows */
}
```

Empty-state HTML (toggled by the integrator with `.is-empty` when the cart has no items):

```html
<div class="pay-empty">
  <h3 class="pay-title">Your cart is empty</h3>
  <p>Nothing to total up yet. When you add something, it'll land here.</p>
  <button type="button" class="naya-btn">Browse the catalog</button>
</div>
```

### The states

- **Rest:** black ground, white-lit 1.5px edges, corner jewel ◆ in the board's tone. Items rest dark; thumb jewels carry each item's own color (law order, never twice in a row).
- **Hover (board):** lifts 5px, border and glow ignite in the board's tone (choosing purple). **Hover (item):** lifts 2px, border ignites in that item's own jewel color. **Hover (grand total):** the serif total ignites **gold** — the only place gold appears, and only on touch. Gold is attention, earned.
- **Active/press:** steppers press in like every `.naya-btn` (down 1px, scale .98); the Apply button presses in the same way.
- **Focus:** `:focus-visible` gives a 2px white ring on every stepper, input, and button. Focus is not optional — Law 5.
- **Disabled:** the Apply button drops to 45% opacity, no motion, no ignition. Disabled never ignites.
- **Empty:** `.is-empty` hides items/promo/totals and shows the quiet empty panel with a live "Browse the catalog" button — the board is idle, not dead.
- **Promo applied:** `.is-applied` — emerald edge, "✓ Code NAYA10 applied — $49.60 off." **Promo invalid:** `.is-invalid` — red edge, plain-words message ("That code didn't land — check the spelling and try again."). Never "Invalid code. Try again." without the human sentence.

### Do / Don't

**DO** let the grand total be the one gold moment on the board — serif, earned, only on hover. The total is the final word of the page; it should feel like it.
**DON'T** show a strike-through "original price" theater next to numbers you never charged. The honest microcopy line — *"Prices confirmed at checkout"* — is a promise, not decoration. If the backend can't confirm a price yet, say "Price loads at the next step" instead.

### Honest anatomy

- **Corner jewel ◆:** the board's identity mark — purple, choosing intelligence. It says "this board belongs to the checkout."
- **Thumb jewels:** rotated diamonds, one spectrum step per item in law order. They are *identity*, not decoration — in a cart of five lookalike items, the jewel is how your eye finds the one you're editing.
- **Qty stepper:** real `<button>`s wearing `.naya-btn.icon.micro` — 44px
  circles, Law 5's minimum touch target, the one DNA (gradient heart,
  white-ish idle border, flowing conic ring on hover, press compresses).
  `<output aria-live>` so screen readers hear the count change. It will not
  fake — when quantity hits 0, the item leaves the list; no phantom rows.
- **Promo row:** one code, one button, one message line. It applies a discount only when the backend accepts the code — `.is-applied` is set by a real response, never by the front end guessing.
- **Totals:** labels left, numbers right, tabular figures so columns stay honest. Tax says "estimated" until the backend confirms it — the word *estimated* is the honesty.
- **What it will NOT fake:** this board never shows a price the page can't prove. If prices arrive asynchronously, the totals area shows a quiet "Loading your total…" state rather than a zero or a guess. Fake totals are a trust violation (Law 75).
- **Backend gate:** every number on this board — line prices, the promo discount, tax, the total — renders only from backend-confirmed values. The specimen's figures ($535.68 and friends) are illustrative; a live build binds all three renderings of the total (PAY-001's board, PAY-002's Pay button label, PAY-003's hologram) to the same confirmed source (family contract §1). Nothing here computes money client-side.

---

## PAY-002 — Payment form

**Law:** Law 1 (fields rest dark with white-lit edges; focus ignites purple — purple is chrome) · Law 5 (Pay is the flagship CTA: ≥52px, one per view) · Law 6 (Georgia voice on the header). Validation law: valid = emerald edge, invalid = red edge + a plain-words message. Never blame the user.

What it is: the four fields where money changes hands. Card number, expiry, CVC, name — floating labels, white-lit edges at rest, purple ignition on focus. Validation speaks like a person, not a parser.

### The code

```html
<form class="pay-board pay-form" action="/checkout/pay" method="post" autocomplete="on" novalidate>
  <span class="pay-corner" aria-hidden="true"><i>◆</i></span>
  <header class="pay-head">
    <p class="pay-kicker">PAYMENT</p>
    <h3 class="pay-title">Card details</h3>
  </header>

  <div class="pay-field">
    <input id="pay-name" class="pay-input" type="text" name="cardholder_name"
           placeholder=" " autocomplete="cc-name" required>
    <label class="pay-label" for="pay-name">Name on card</label>
    <p class="pay-err" id="err-name" hidden>Name helps us match the card — how does it read on the front?</p>
  </div>

  <div class="pay-field">
    <input id="pay-number" class="pay-input pay-input--card" type="text" name="card_number"
           placeholder=" " inputmode="numeric" autocomplete="cc-number"
           pattern="[0-9\s]{13,23}" required aria-describedby="err-number">
    <label class="pay-label" for="pay-number">Card number</label>
    <span class="pay-brand" aria-hidden="true"></span>
    <p class="pay-err" id="err-number" hidden>That number looks short — card numbers are usually 16 digits. Take another look.</p>
  </div>

  <div class="pay-field-row">
    <div class="pay-field">
      <input id="pay-expiry" class="pay-input" type="text" name="card_expiry"
             placeholder=" " inputmode="numeric" autocomplete="cc-exp"
             pattern="(0[1-9]|1[0-2])\s?\/\s?\d{2}" required aria-describedby="err-expiry">
      <label class="pay-label" for="pay-expiry">Expiry · MM / YY</label>
      <p class="pay-err" id="err-expiry" hidden>Expiry reads month, then year — like 04 / 28.</p>
    </div>
    <div class="pay-field">
      <input id="pay-cvc" class="pay-input" type="password" name="card_cvc"
             placeholder=" " inputmode="numeric" autocomplete="cc-csc"
             pattern="\d{3,4}" required aria-describedby="err-cvc">
      <label class="pay-label" for="pay-cvc">CVC</label>
      <p class="pay-err" id="err-cvc" hidden>The 3 digits on the back — 4 on the front for Amex.</p>
    </div>
  </div>

  <button type="submit" class="naya-btn pay-submit" disabled>Pay $535.68</button>
  <p class="pay-secure">Locked in transit. We never see your full card number — only the payment processor does.</p>
</form>
<script>
/* The enable contract, as code (independent scorecard fix, 2026-10-16) — the
   money-moving button's enable logic is pinned here, not left to integrator
   improvisation. */
(function(){
  const form=document.querySelector('.pay-form');
  const pay=form.querySelector('.pay-submit');
  const fields=[...form.querySelectorAll('.pay-input')]; /* the four: name, number, expiry, cvc */
  /* the rule: the Pay button enables iff ALL four fields carry .is-valid */
  function refresh(){pay.disabled=!fields.every(f=>f.classList.contains('is-valid'));}
  function validateField(f){
    /* specimen-grade validation; a live build runs the processor's real rules */
    const ok=f.checkValidity()&&f.value.trim().length>0;
    f.classList.toggle('is-valid',ok);
    f.classList.toggle('is-invalid',!ok&&f.value.length>0);
    const err=document.getElementById(f.getAttribute('aria-describedby'));
    if(err)err.hidden=(ok||f.value.length===0);
  }
  fields.forEach(f=>{
    /* which class, on which event: .is-valid/.is-invalid on blur AND input */
    f.addEventListener('blur',()=>{validateField(f);refresh();});
    f.addEventListener('input',()=>{validateField(f);refresh();});
  });
  /* a failed payment NEVER clears the form — retry re-submits this same
     validated data (see PAY-004's retry contract); the user never re-types */
  form.addEventListener('submit',e=>{
    e.preventDefault();
    if(pay.disabled)return;
    /* hand the validated fields to the processor; keep every value
       regardless of the answer */
  });
  refresh();
})();
</script>
```

```css
/* ---------- PAY-002 payment form ---------- */
.pay-form{ --tone:#a06bff; --tone-rgb:160,107,255; }
.pay-form .pay-corner{ text-shadow:0 0 14px rgba(160,107,255,.9); }

.pay-field{ position:relative; margin-bottom:20px; }
.pay-field-row{ display:flex; gap:14px; }
.pay-field-row .pay-field{ flex:1 1 0; }

.pay-input{
  width:100%; height:58px; padding:22px 16px 8px; border-radius:14px;
  background:#0a0a0e; color:#fbfbfd; font-size:16px;
  border:1.5px solid rgba(255,255,255,.55);
  transition:border-color .18s cubic-bezier(.16,.84,.22,1), box-shadow .18s cubic-bezier(.16,.84,.22,1);
}
.pay-input--card{ letter-spacing:.12em; font-variant-numeric:tabular-nums; }
.pay-input:focus{ outline:none; border-color:#a06bff; box-shadow:0 0 26px -4px rgba(160,107,255,.85); }

/* floating label — rests inside the field, lifts on focus or content */
.pay-label{
  position:absolute; left:16px; top:19px; font-size:15px; color:rgba(255,255,255,.55);
  pointer-events:none; transition:all .18s cubic-bezier(.16,.84,.22,1);
}
.pay-input:focus + .pay-label,
.pay-input:not(:placeholder-shown) + .pay-label{
  top:8px; font-size:11px; letter-spacing:.18em; text-transform:uppercase; color:rgba(255,255,255,.8);
}

/* validation — emerald for alive-and-well, red for urgency */
.pay-input.is-valid{ border-color:#35e0a1; box-shadow:0 0 26px -6px rgba(53,224,161,.6); }
.pay-input.is-invalid{ border-color:#ff5e6c; box-shadow:0 0 26px -6px rgba(255,94,108,.6); }
.pay-input.is-invalid + .pay-label{ color:#ff8a96; }
.pay-err{ margin:8px 2px 0; font-size:14px; color:#ff9aa3; }
.pay-err[hidden]{ display:none; }

/* brand jewel — a small orb that lights when a brand is recognized */
.pay-brand{
  position:absolute; right:14px; top:50%; transform:translateY(-50%);
  width:30px; height:30px; border-radius:50%;
  background:radial-gradient(circle at 35% 30%, rgba(255,255,255,.9) 0%, transparent 45%),
             radial-gradient(circle at 50% 50%, var(--bc,#333) 0%, #050507 100%);
  border:1.5px solid rgba(255,255,255,.5);
  opacity:0; transition:opacity .28s cubic-bezier(.16,.84,.22,1), box-shadow .28s cubic-bezier(.16,.84,.22,1);
}
.pay-brand.is-known{ opacity:1; box-shadow:0 0 22px -2px var(--bc,#333); }
.pay-brand.is-visa{ --bc:#3fb8ff; }
.pay-brand.is-mastercard{ --bc:#ff9a5a; }
.pay-brand.is-amex{ --bc:#35e0a1; }

.pay-submit{
  width:100%; min-height:56px; font-size:15px; margin-top:6px;
  --nb-accent:#a06bff; --nb-accent-rgb:160,107,255;
}
.pay-submit:not(:disabled):hover{ transform:translateY(-2px); }
.pay-secure{ margin:14px 2px 0; font-size:13px; color:rgba(255,255,255,.68); text-align:center; }

@media (prefers-reduced-motion:reduce){
  .pay-input,.pay-label,.pay-brand{ transition:none; }
}
```

The submit button starts **disabled** (45% opacity, no ignition — disabled never ignites) and enables only when all four fields pass validation. The integrator's validation script adds `.is-valid` / `.is-invalid` and unhides the matching `.pay-err`; the button label always carries the real total from PAY-001 — never a hardcoded number the page can't prove. The enable rule is pinned in the script above, as code: the button enables iff all four fields carry `.is-valid`, evaluated on `blur` **and** `input` — never on submit-attempt alone.

### The states

- **Rest:** fields dark (`#0a0a0e`), white-lit 1.5px edges, labels sitting inside like a placeholder. Everything readable, nothing shouting.
- **Focus:** border ignites **purple** with a held glow — purple is chrome, and a payment form is chrome. The label lifts, shrinks, and letterspaces into a kicker.
- **Active:** the Pay button presses in (down 1px, scale .98) on click.
- **Valid:** emerald edge + emerald glow — "alive and well," the color of a thing that checked out.
- **Invalid:** red edge + red glow + one plain-words sentence underneath. Red is urgency, not alarm: no shaking, no exclamation icons, no red flood — just an edge and a sentence that helps. Messages never blame: "That number looks short" instead of "Invalid input"; "Expiry reads month, then year" instead of "Wrong format."
- **Disabled:** Pay button at 45% opacity until the form validates. It does not pulse, glow, or beg — a disabled button is quiet.
- **Empty:** all fields blank is the natural rest state — labels in place, button disabled, no error text anywhere. A form with nothing typed is not an error.

### Do / Don't

**DO** validate inline, per field, the moment the user leaves it — and let the emerald edge be the reward. Fast feedback is kindness; a surprise error at the bottom of a submitted form is not.
**DON'T** clear the whole form on a failed payment, and don't red-ring every field when one card number is the problem. Mark the one field that's wrong, keep everything else, and keep the user's typing. Wiping their work is the fastest way to lose the sale *and* the trust. (PAY-004's retry re-submits this same validated data — the contract is two-sided.)

### Honest anatomy — including the privacy boundary

- **Floating labels:** rest inside the field, lift to kicker on focus or content. The field's purpose never disappears.
- **Card number field:** `inputmode="numeric"` for the right mobile keyboard, `autocomplete="cc-number"` so the browser can fill it safely, `letter-spacing` + tabular figures so a 16-digit number reads in groups. The `pattern` is a courtesy, not a contract — real validation runs against the payment processor's rules.
- **Brand jewel:** lights in the brand's own color once the leading digits identify it (Visa blue, Mastercard orange, Amex emerald). It is *identity*, not decoration — and it only ever confirms the brand, never echoes digits.
- **CVC field:** `type="password"` + `autocomplete="cc-csc"` — masked at rest, like it should be.
- **The Pay button:** one per view, ≥52px, carries the real total. It stays disabled until validation passes — a pay button that fires on a broken form is unfinished.
- **The secure line:** "Locked in transit. We never see your full card number — only the payment processor does." A promise in plain words. It must be *true* for the build that ships this block.
- **PRIVACY BOUNDARY (this is part of the spec):** card data lives **only** in the input fields, bound for the payment backend on submit. This block **never** renders a card number back as text — not in a summary, not in an error message, not in a receipt preview. It **never** logs card fields to console, analytics, or error reporters (strip them before any capture). The display layer shows **at most the last-4 plus the brand** ("Visa ···· 4242"), and only when the backend returns that masked form. No full number ever touches the DOM as text. This is not a guideline — a build that echoes a PAN violates the block.
Enforced mechanically: `DESIGN/gap-blocks/validate-checkout-privacy.sh`
fails the build on any PAN-shaped string in the spec, any card identifier
outside an input attribute, any logging call, or any display-layer number
beyond last-4 + brand. Run it in CI; the boundary is structural, not
aspirational.
- **What it will NOT fake:** the form never shows a "processing" success before the processor answers, never pre-fills test card numbers, and the brand jewel never lights for a brand the digits don't prove. A specimen may show the layout with placeholder-shaped fields — it must never show a plausible real card number (Law 75: fake success is a trust violation; fake data is its cousin).

---

## PAY-003 — Confirmation state

**Law:** Law 1 (maximum life, minimum noise — one ignition, then a soft breathe) · Law 2 (emerald/green: alive and well) · the truth language (green ✓ = proven by the backend, gold ? = claimed, awaiting its stamp).

What it is: the moment after money moves. The paid amount as a hologram number — layered light you look *into* — receipt rows for what, where, when, and an honest receipt line that only claims "sent" when the backend confirms it.

### The code

```html
<section class="pay-board pay-confirm" aria-label="Payment confirmed">
  <span class="pay-corner" aria-hidden="true"><i>◆</i></span>
  <header class="pay-head">
    <p class="pay-kicker">CONFIRMED</p>
    <h3 class="pay-title">Payment complete</h3>
  </header>

  <div class="pay-holo" aria-label="Amount paid: $535.68">
    <span class="pay-holo-amount">$535.68</span>
    <span class="pay-holo-sub">charged to Visa ···· 4242</span>
  </div>

  <ul class="pay-receipt">
    <li class="pay-receipt-row">
      <span class="pay-receipt-jewel" data-tone="magenta" aria-hidden="true"><i>◆</i></span>
      <span class="pay-receipt-k">What</span>
      <span class="pay-receipt-v">Naya MAXIS AI Score, AI Masterclass ×2, Powercast bundle</span>
    </li>
    <li class="pay-receipt-row">
      <span class="pay-receipt-jewel" data-tone="blue" aria-hidden="true"><i>◆</i></span>
      <span class="pay-receipt-k">When</span>
      <span class="pay-receipt-v">Oct 16, 2026 · 10:52 PM UTC</span>
    </li>
    <li class="pay-receipt-row">
      <span class="pay-receipt-jewel" data-tone="green" aria-hidden="true"><i>◆</i></span>
      <span class="pay-receipt-k">Receipt</span>
      <span class="pay-receipt-v pay-receipt-sent">✓ Sent to you@nayanet.live</span>
    </li>
  </ul>

  <div class="pay-confirm-actions">
    <button type="button" class="naya-btn">Back to the Hub</button>
    <button type="button" class="naya-btn naya-btn--quiet">Download receipt</button>
  </div>
</section>
```

```css
/* ---------- PAY-003 confirmation ---------- */
.pay-confirm{ --tone:#2fe89e; --tone-rgb:47,232,158;
  border-color:rgba(47,232,158,.4);
  box-shadow:
    inset 0 2px 2px rgba(255,255,255,.12),
    inset 0 -8px 18px rgba(0,0,0,.55),
    0 5px 0 #020203,
    0 17px 0 -8px rgba(47,232,158,.16),
    0 35px 75px rgba(0,0,0,.7),
    0 0 40px -17px rgba(47,232,158,.5);
}
.pay-confirm:hover{ border-color:rgba(47,232,158,.8);
  box-shadow:
    inset 0 2px 2px rgba(255,255,255,.14),
    inset 0 -8px 18px rgba(0,0,0,.55),
    0 5px 0 #020203,
    0 17px 0 -8px rgba(47,232,158,.2),
    0 35px 75px rgba(0,0,0,.7),
    0 0 46px -14px rgba(47,232,158,.85);
  transform:translateY(-5px);
}
.pay-confirm .pay-corner{ text-shadow:0 0 14px rgba(47,232,158,.9); }

/* the hologram number — layered depth, looked INTO not AT */
.pay-holo{ text-align:center; padding:26px 10px 22px; position:relative; }
.pay-holo-amount{
  display:block; font-family:Georgia,'Times New Roman',serif; font-size:56px; font-weight:700;
  color:#fbfbfd; letter-spacing:.01em;
  text-shadow:
    0 1px 0 rgba(255,255,255,.35),
    0 3px 14px rgba(0,0,0,.7),
    0 0 34px rgba(47,232,158,.65),
    0 0 90px rgba(47,232,158,.28);
  animation:pay-breathe 5s cubic-bezier(.16,.84,.22,1) infinite;
}
/* ONE ignition: the integrator adds .is-ignited when the backend confirms.
   It fires once — maximum life, minimum noise — then settles into the breathe. */
.pay-holo.is-ignited .pay-holo-amount{ animation:pay-ignite 1.1s cubic-bezier(.16,.84,.22,1) 1, pay-breathe 5s cubic-bezier(.16,.84,.22,1) 1.2s infinite; }
@keyframes pay-ignite{
  0%{ transform:scale(.94); text-shadow:0 1px 0 rgba(255,255,255,.35), 0 3px 14px rgba(0,0,0,.7), 0 0 12px rgba(47,232,158,.3); }
  45%{ transform:scale(1.02); text-shadow:0 1px 0 rgba(255,255,255,.5), 0 3px 14px rgba(0,0,0,.7), 0 0 70px rgba(47,232,158,.95), 0 0 140px rgba(47,232,158,.4); }
  100%{ transform:scale(1); }
}
@keyframes pay-breathe{
  0%,100%{ text-shadow:0 1px 0 rgba(255,255,255,.35), 0 3px 14px rgba(0,0,0,.7), 0 0 34px rgba(47,232,158,.6), 0 0 90px rgba(47,232,158,.25); }
  50%{ text-shadow:0 1px 0 rgba(255,255,255,.4), 0 3px 14px rgba(0,0,0,.7), 0 0 40px rgba(47,232,158,.75), 0 0 100px rgba(47,232,158,.32); }
}
.pay-holo-sub{ display:block; margin-top:10px; font-size:14px; color:rgba(255,255,255,.72); }

/* receipt rows */
.pay-receipt{ list-style:none; margin:6px 0 0; padding:0; }
.pay-receipt-row{
  display:flex; align-items:center; gap:12px; padding:11px 4px;
  border-bottom:1px solid rgba(255,255,255,.1); font-size:15px;
}
.pay-receipt-row:last-child{ border-bottom:none; }
.pay-receipt-jewel{
  flex:0 0 20px; font-size:13px; color:#fff; transform:rotate(45deg); text-align:center;
  --jc:#a06bff; --jc-rgb:160,107,255;
  text-shadow:0 0 12px rgba(var(--jc-rgb),.9);
}
.pay-receipt-jewel[data-tone="magenta"]{ --jc:#e84fff; --jc-rgb:232,79,255; }
.pay-receipt-jewel[data-tone="blue"]{ --jc:#3fb8ff; --jc-rgb:63,184,255; }
.pay-receipt-jewel[data-tone="green"]{ --jc:#2fe89e; --jc-rgb:47,232,158; }
.pay-receipt-jewel i{ font-style:normal; display:inline-block; transform:rotate(-45deg); } /* glyph stays upright inside the diamond */
.pay-receipt-k{ flex:0 0 74px; font-size:12px; letter-spacing:.24em; color:rgba(255,255,255,.6); }
.pay-receipt-v{ flex:1 1 auto; color:#fbfbfd; }
.pay-receipt-sent{ color:#35e0a1; }
.pay-receipt-pending{ color:#ffbf3d; } /* gold = claimed, awaiting its stamp */

.pay-confirm-actions{ display:flex; gap:12px; margin-top:22px; }
.pay-confirm-actions .naya-btn{ flex:1 1 auto; }
/* .naya-btn--quiet is owned ONCE by the shared family contract (§8) —
   referenced here and by PAY-004, never redefined. No block defines what
   another block consumes (independent scorecard fix, 2026-10-16). */

@media (prefers-reduced-motion:reduce){
  .pay-holo-amount,.pay-holo.is-ignited .pay-holo-amount{ animation:none; }
  .pay-confirm,.pay-confirm:hover{ transition:none; transform:none; }
}
```

The honest receipt line has two variants — only one ships per render:

```html
<!-- backend confirmed the email: -->
<span class="pay-receipt-v pay-receipt-sent">✓ Sent to you@nayanet.live</span>
<!-- backend has NOT confirmed yet (gold = claimed, awaiting its stamp): -->
<span class="pay-receipt-v pay-receipt-pending">? Receipt is on its way — we'll confirm here when it lands</span>
```

### The states

- **Rest:** emerald-tone board, the hologram amount breathing on a slow 5s loop — "maximum life, minimum noise." Restrained, alive, not a party.
- **The one ignition:** when the payment processor answers success, the integrator adds `.is-ignited` to `.pay-holo`. The amount flares once — scale, light, settle — then returns to the breathe. One ignition. Not confetti, not fireworks, not a modal parade. The restraint *is* the celebration.
- **Hover:** the board lifts 5px and ignites emerald. Receipt rows stay still — they're records, not controls; nothing fake-interactive.
- **Receipt sent:** emerald ✓ — the backend confirmed the email. **Receipt pending:** gold ? — claimed, awaiting its stamp. The gold line never upgrades itself; only a confirmed delivery flips it.
- **Error (inside confirmation):** if the receipt email fails *after* a successful charge, the receipt row says so in plain words: "Charged ✓ — receipt email failed, retrying. Your money is safe." Red is reserved for the charge failing (PAY-004), not for a delayed email. Never let a mail hiccup read as a payment failure.

### Do / Don't

**DO** make the paid amount the most beautiful number on the page — Georgia, hologram layers, one ignition, then breathe. This is the moment the user trusted you with money; the number should feel *held*, not just displayed.
**DON'T** add confetti, coin bursts, or a "YOU DID IT!!!" modal. Maximum life, minimum noise. A payment confirmation is a receipt, not a birthday party — restraint is what makes the one ignition feel like something.

### Honest anatomy

- **Hologram amount:** Georgia 56px, four layers of shadow — top light, grounding, glow, far glow. "You look *into* the data, not *at* it." It breathes because numbers breathe (Law 1); it never blinks, spins, or dances.
- **Charged-to line:** brand + last-4 only ("Visa ···· 4242") — the full number never appears here, per the PAY-002 privacy boundary. Last-4 arrives from the backend's masked response; the front end never truncates a PAN it shouldn't have.
- **Receipt rows:** what / where (the charge destination is the *merchant of record*, stated plainly) / when in UTC, so there's no timezone argument later. Jewel bullets in law order carry the rows; the jewels are identity, not buttons.
- **Receipt-sent line:** two truth states, and the spec chooses between them — green ✓ only when the backend confirms delivery, gold ? while it's claimed. The line is a *claim* until the mailer says otherwise.
- **Backend gate:** this block renders ONLY on a confirmed charge response from the payment processor. The fields it may consume: charge id, confirmed amount, masked brand + last-4, receipt-email delivery status. It never renders on a timeout, a guess, or an optimistic local state — the specimen's charge is illustrative, and `.is-ignited` fires only on the confirmed response. No processor, no confirmation block.
- **Actions:** "Back to the Hub" (primary, one per view) and "Download receipt" (quiet — same DNA, speaks softly). Download serves the receipt *the backend already generated*; it never fabricates a PDF client-side from page text.
- **What it will NOT fake:** this block never claims the charge succeeded before the processor answers (Law 75 — fake success is a trust violation). The `.is-ignited` class is added by a confirmed success response, never by a timeout, a guess, or an optimistic render. The receipt email is never claimed as sent until the mailer confirms it. And it never shows a total the page can't prove — the amount comes from the confirmed charge, not from PAY-001's estimate.

---

## PAY-004 — Error state

**Law:** Law 1 (calm surfaces can still be alive — the retry button ignites, the panel breathes) · Law 2 (red = urgency, not alarm — an edge and a glow, never a flood, never flashing) · the plain-words law from PAY-002 validation (never blame the user).

What it is: the panel for when the payment doesn't go through. Declined card, failed processor, expired session — the panel explains what happened in plain words, what to try next, and gives retry the primary seat. Calm, honest, actionable. Nobody is shamed for a declined card.

### The code

```html
<section class="pay-board pay-error" role="alert" aria-label="Payment didn't go through">
  <span class="pay-corner" aria-hidden="true"><i>◆</i></span>
  <header class="pay-head">
    <p class="pay-kicker">PAYMENT</p>
    <h3 class="pay-title">That didn't go through</h3>
  </header>

  <p class="pay-error-what">Your card was declined — no money moved. This happens, and it's usually one of three things.</p>

  <ul class="pay-error-next">
    <li><span class="pay-receipt-jewel" data-tone="blue" aria-hidden="true"><i>◆</i></span>
      <span><strong>Check the card details.</strong> One mistyped digit is the most common cause — take another look.</span></li>
    <li><span class="pay-receipt-jewel" data-tone="purple" aria-hidden="true"><i>◆</i></span>
      <span><strong>Try a different card.</strong> Some cards block certain purchase types by default.</span></li>
    <li><span class="pay-receipt-jewel" data-tone="green" aria-hidden="true"><i>◆</i></span>
      <span><strong>Ask your bank.</strong> A quick call clears most declines — mention the amount, $535.68.</span></li>
  </ul>

  <!-- specimen: the integrator renders the real reference from the failed
       attempt's processor response — never a hardcoded string -->
  <p class="pay-error-code">Reference: <code>ch_3P2k_402_declined</code> — keep this if you call your bank.</p>

  <div class="pay-error-actions">
    <button type="button" class="naya-btn pay-retry">Try again</button>
    <button type="button" class="naya-btn naya-btn--quiet">Use a different card</button>
  </div>
</section>
```

```css
/* ---------- PAY-004 error state ---------- */
.pay-error{ --tone:#ff5e6c; --tone-rgb:255,94,108;
  border-color:rgba(255,94,108,.45);
  box-shadow:
    inset 0 2px 2px rgba(255,255,255,.12),
    inset 0 -8px 18px rgba(0,0,0,.55),
    0 5px 0 #020203,
    0 17px 0 -8px rgba(255,94,108,.18),
    0 35px 75px rgba(0,0,0,.7),
    0 0 40px -17px rgba(255,94,108,.55);
  animation:pay-calm 6s cubic-bezier(.16,.84,.22,1) infinite;
}
/* red breathes slowly — urgency that stays calm, never an alarm */
@keyframes pay-calm{
  0%,100%{ box-shadow:
    inset 0 2px 2px rgba(255,255,255,.12),
    inset 0 -8px 18px rgba(0,0,0,.55),
    0 5px 0 #020203,
    0 17px 0 -8px rgba(255,94,108,.18),
    0 35px 75px rgba(0,0,0,.7),
    0 0 40px -17px rgba(255,94,108,.5); }
  50%{ box-shadow:
    inset 0 2px 2px rgba(255,255,255,.12),
    inset 0 -8px 18px rgba(0,0,0,.55),
    0 5px 0 #020203,
    0 17px 0 -8px rgba(255,94,108,.22),
    0 35px 75px rgba(0,0,0,.7),
    0 0 48px -14px rgba(255,94,108,.7); }
}
.pay-error:hover{ border-color:rgba(255,94,108,.8); transform:translateY(-5px); }
.pay-error .pay-corner{ text-shadow:0 0 14px rgba(255,94,108,.9); }

.pay-error-what{ font-size:16px; color:#fbfbfd; margin:0 0 18px; line-height:1.55; }
.pay-error-next{ list-style:none; margin:0 0 18px; padding:0; }
.pay-error-next li{
  display:flex; gap:12px; align-items:flex-start; padding:10px 4px;
  font-size:15px; color:rgba(255,255,255,.88); line-height:1.5;
  border-bottom:1px solid rgba(255,255,255,.08);
}
.pay-error-next li:last-child{ border-bottom:none; }
.pay-error-next strong{ color:#fbfbfd; font-weight:700; }
.pay-error-code{ font-size:13px; color:rgba(255,255,255,.6); margin:0 0 20px; }
.pay-error-code code{
  font-family:ui-monospace,Menlo,monospace; color:rgba(255,255,255,.85);
  background:rgba(255,255,255,.06); padding:3px 8px; border-radius:8px;
  border:1px solid rgba(255,255,255,.16);
}
/* "Use a different card" wears .naya-btn--quiet — the family's shared quiet
   variant, owned once in the family contract (§8). This block defines no quiet
   control of its own; the reference is the whole dependency (independent
   scorecard fix, 2026-10-16). */
.pay-error-actions{ display:flex; gap:12px; }
.pay-error-actions .naya-btn{ flex:1 1 auto; }
.pay-retry{ --nb-accent:#a06bff; --nb-accent-rgb:160,107,255; } /* retry is the primary action: chrome purple */

@media (prefers-reduced-motion:reduce){
  .pay-error{ animation:none; }
  .pay-error,.pay-error:hover{ transition:none; transform:none; }
}
```

### The states

- **Rest:** red-tone board breathing on a slow 6s loop — the glow swells and settles, like a held breath. Urgency you can feel, not an alarm you flinch from. `role="alert"` so assistive tech announces it once, immediately.
- **Hover:** the board lifts 5px and the red edge brightens. The "Try again" button is chrome-purple — retry is *the* primary action, and primary actions wear chrome.
- **Active:** retry presses in like every `.naya-btn`.
- **Declined vs. failed:** the headline and first line change with the cause, and the cause is always named honestly —
  - *Declined:* "Your card was declined — no money moved."
  - *Processor failed:* "The payment processor didn't answer — no money moved."
  - *Session expired:* "This checkout timed out before anything was charged — no money moved."
  
  "No money moved" appears in all three. That sentence is the whole job of the panel.
- **Empty:** never empty — an error panel without a cause is a bug. If the cause is unknown, the panel says "Something went wrong on our side — no money moved" and the reference code becomes the primary artifact. Unknown is stated, never hidden.
- **Disabled:** the retry button disables while a retry is in flight ("Trying again…" label swap), re-enabling on the next response. No double-charges from double-clicks.

### Do / Don't

**DO** say "no money moved" before anything else. The user's first fear is the double-charge; kill it in the first sentence, then explain.
**DON'T** show the raw processor code as the headline ("Error 402: card_declined") or paste a stack trace anywhere near the user. The reference code exists — small, monospace, at the bottom, for the bank call — but the panel speaks human first. And never, ever imply the user did something wrong: no "you entered," no "your fault," no red ✕ stamped over their card.

### Honest anatomy

- **The red:** an edge and a glow, at ~45% border strength, breathing. Red is urgency — "look at this" — not alarm. No flashing, no pulsing icons, no red flood. A panel that screams at a declined card teaches users to fear the checkout.
- **"No money moved":** the load-bearing sentence. It is only rendered when the backend confirms no charge was created — the block never assumes it. If the charge state is genuinely unknown (timeout with no confirmation), the line reads "We're confirming with the processor whether anything was charged — nothing is final yet," and the panel offers "Check status" instead of "Try again." Guessing here is how double-charges happen.
- **The three next-steps:** jewel bullets in law order, each one a *concrete action*, ordered by likelihood. "Check the details" first because it's the most common cause and the cheapest fix. "Ask your bank" names the amount — because the bank will ask.
- **Reference code:** real, from the failed attempt, monospace, copyable. It's for the bank call and for support — the one piece of machine truth the user can carry elsewhere.
- **Retry as primary:** one primary action per view (Law 5). "Try again" re-submits the *same* validated form data — it never clears the fields (see PAY-002's don't). "Use a different card" is the quiet secondary.
- **What it will NOT fake:** this block never claims "no money moved" on a guess, never auto-retries without the user's hand on the button (a retry is a new charge attempt — it needs consent, every time), and never hides the failure behind a success-looking state. A failed payment that *looks* fine is the worst lie a checkout can tell.

---

## PAY-005 — Payment method picker

**Law:** Law 2 (purple = choosing intelligence — the selected row ignites purple) · Law 1 (rows rest dark, lift 2px, ignite their own tone) · the PAY-002 privacy boundary (last-4 + brand only, never full numbers).

What it is: the "which card?" moment. Saved methods as rows — brand jewel, last-4, expiry, one marked default — plus a "new card" row that hands off to PAY-002. Selecting a row is a choice, and choices ignite purple.

### The code

```html
<div class="pay-board pay-methods" role="radiogroup" aria-label="Choose a payment method">
  <span class="pay-corner" aria-hidden="true"><i>◆</i></span>
  <header class="pay-head">
    <p class="pay-kicker">PAYMENT METHOD</p>
    <h3 class="pay-title">Which card?</h3>
  </header>

  <label class="pay-method is-selected">
    <input type="radio" name="pay-method" value="pm_visa_4242" checked>
    <span class="pay-mbrand is-visa" aria-hidden="true"></span>
    <span class="pay-mbody">
      <span class="pay-mname">Visa ···· 4242 <em class="pay-mdefault">Default</em></span>
      <span class="pay-mmeta">Expires 08 / 28</span>
    </span>
    <span class="pay-mcheck" aria-hidden="true">✓</span>
  </label>

  <label class="pay-method">
    <input type="radio" name="pay-method" value="pm_mc_5555">
    <span class="pay-mbrand is-mastercard" aria-hidden="true"></span>
    <span class="pay-mbody">
      <span class="pay-mname">Mastercard ···· 5555</span>
      <span class="pay-mmeta">Expires 03 / 27</span>
    </span>
    <span class="pay-mcheck" aria-hidden="true">✓</span>
  </label>

  <button type="button" class="pay-method pay-method--new">
    <span class="pay-mbrand pay-mbrand--plus" aria-hidden="true">+</span>
    <span class="pay-mbody">
      <span class="pay-mname">Use a new card</span>
      <span class="pay-mmeta">Enter details on the next step</span>
    </span>
    <span class="pay-mgo" aria-hidden="true">→</span>
  </button>

  <p class="pay-methods-note">Full numbers are never shown here — and never leave the payment processor.</p>
</div>
```

```css
/* ---------- PAY-005 method picker ---------- */
.pay-methods{ --tone:#a06bff; --tone-rgb:160,107,255; }
.pay-method{
  --jc:#a06bff; --jc-rgb:160,107,255;
  display:flex; align-items:center; gap:14px; width:100%;
  padding:14px 16px; margin-bottom:10px; border-radius:16px; cursor:pointer;
  background:rgba(255,255,255,.03);
  border:1.5px solid rgba(255,255,255,.55);
  color:#fbfbfd; font:inherit; text-align:left;
  transition:border-color .18s cubic-bezier(.16,.84,.22,1), box-shadow .18s cubic-bezier(.16,.84,.22,1), transform .18s cubic-bezier(.16,.84,.22,1);
}
.pay-method input[type="radio"]{
  position:absolute; opacity:0; width:1px; height:1px; /* the row IS the control */
}
.pay-method:hover{
  transform:translateY(-2px);
  border-color:rgba(var(--jc-rgb),.8);
  box-shadow:0 0 26px -6px rgba(var(--jc-rgb),.7);
}
.pay-method:active{ transform:translateY(1px); }
.pay-method:focus-within{ outline:2px solid #fff; outline-offset:3px; }

/* selected: the choice ignites purple — choosing intelligence */
.pay-method.is-selected{
  border-color:#a06bff;
  background:linear-gradient(160deg, rgba(160,107,255,.14) 0%, rgba(255,255,255,.03) 70%);
  box-shadow:0 0 32px -6px rgba(160,107,255,.8), inset 0 1px 0 rgba(255,255,255,.12);
}
.pay-method.is-selected:hover{ transform:translateY(-2px); box-shadow:0 0 38px -4px rgba(160,107,255,.9), inset 0 1px 0 rgba(255,255,255,.12); }
.pay-mcheck{
  margin-left:auto; width:30px; height:30px; border-radius:50%;
  display:grid; place-items:center; font-size:15px; color:#fff;
  border:1.5px solid rgba(255,255,255,.4);
  opacity:0; transform:scale(.7);
  transition:opacity .18s cubic-bezier(.16,.84,.22,1), transform .18s cubic-bezier(.16,.84,.22,1), box-shadow .18s cubic-bezier(.16,.84,.22,1);
}
.pay-method.is-selected .pay-mcheck{
  opacity:1; transform:scale(1);
  border-color:#a06bff; box-shadow:0 0 20px -2px rgba(160,107,255,.9);
}

/* brand jewels — identity in the brand's own color */
.pay-mbrand{
  flex:0 0 40px; width:40px; height:40px; border-radius:50%;
  border:1.5px solid rgba(255,255,255,.6);
  background:radial-gradient(circle at 35% 30%, rgba(255,255,255,.85) 0%, transparent 45%),
             radial-gradient(circle at 50% 50%, var(--bc,#444) 0%, #050507 100%);
  box-shadow:0 0 16px -2px var(--bc,#444);
}
.pay-mbrand.is-visa{ --bc:#3fb8ff; }
.pay-mbrand.is-mastercard{ --bc:#ff9a5a; }
.pay-mbrand.is-amex{ --bc:#35e0a1; }
.pay-mbrand--plus{
  --bc:#a06bff; display:grid; place-items:center;
  font-size:20px; color:#fff; font-weight:300;
}
.pay-mbody{ flex:1 1 auto; min-width:0; }
.pay-mname{ display:block; font-size:15px; font-weight:700; color:#fbfbfd; font-variant-numeric:tabular-nums; }
/* the default chip: purple "choosing intelligence" — the default is a choice.
   Gold stays sacred to the total (the family's own law); it never marks a card
   (independent scorecard fix, 2026-10-16). */
.pay-mdefault{
  font-style:normal; font-size:11px; letter-spacing:.18em; text-transform:uppercase;
  color:#cfaeff; border:1px solid rgba(160,107,255,.55); border-radius:999px;
  padding:2px 9px; margin-left:8px; vertical-align:2px;
  background:rgba(160,107,255,.1); box-shadow:0 0 14px -4px rgba(160,107,255,.6);
}
.pay-mmeta{ display:block; font-size:13px; color:rgba(255,255,255,.68); margin-top:3px; }
.pay-method--new{ --jc:#a06bff; --jc-rgb:160,107,255; background:transparent; border-style:dashed; }
.pay-method--new:hover{ border-style:solid; }
.pay-mgo{ margin-left:auto; font-size:18px; color:rgba(255,255,255,.7); transition:transform .18s cubic-bezier(.16,.84,.22,1), color .18s; }
.pay-method--new:hover .pay-mgo{ transform:translateX(4px); color:#a06bff; }
.pay-methods-note{ margin:14px 2px 0; font-size:13px; color:rgba(255,255,255,.68); text-align:center; }

@media (prefers-reduced-motion:reduce){
  .pay-method,.pay-mcheck,.pay-mgo{ transition:none; }
  .pay-method:hover{ transform:none; }
}
```

Rows are real `<label>`s wrapping real radio inputs — keyboard, screen reader, and click all work with no JS. The integrator toggles `.is-selected` to match `:checked` (or styles `:has(:checked)` where supported — the class is the contract).

### The states

- **Rest:** dark rows, white-lit 1.5px edges, brand jewels glowing in their brand colors. The default card wears a purple "Default" chip — choosing intelligence, because the default is the card already chosen. Gold is attention, earned — and on this board gold is sacred to the total; it never marks a card.
- **Hover:** the row lifts 2px and ignites in choosing-purple. The "new card" row's dashed border goes solid and its → nudges 4px — a chevron promises "go somewhere" (Law 4: the glyph promises its behavior).
- **Selected:** purple edge, purple wash, purple glow, and the ✓ check orb fades in at full scale. One selected at a time — it's a radiogroup, and the visual obeys the semantics.
- **Focus:** `:focus-within` gives the white ring — keyboard users get the same certainty as pointer users.
- **Active:** press compresses 1px. The row is a real control; it feels like one.
- **Empty (no saved methods):** the saved rows don't render at all — no "no cards saved" apology panel. The "Use a new card" row becomes the whole picker, pre-highlighted, heading to PAY-002. An empty picker is a one-row picker, not an error.

### Do / Don't

**DO** mark exactly one default and let the user change it where the row lives — a "make default" that only exists in settings is a scavenger hunt. The chip is purple — choosing intelligence — because the default is the card the user already chose.
**DON'T** show the expiry as a countdown ("expires in 4 months!!") or nudge the user toward any particular card. The picker is neutral ground — it presents, it never persuades. And never add a "delete" affordance inline on the row; removing a payment method is destructive and deserves its own confirmed moment elsewhere.

### Honest anatomy — including the privacy boundary

- **Brand jewels:** orbs in the brand's own color — Visa blue, Mastercard orange, Amex emerald. Identity, not decoration: at a glance you know which card is which without reading a digit.
- **Last-4 + expiry:** the only numbers on the row, and both arrive from the backend already masked. The row *names* the card ("Visa ···· 4242") the way a person would.
- **Backend gate:** the method list renders only from the processor's saved-method response, already masked. An empty response renders the one-row picker (PAY-005's empty state) — never specimen cards, never guessed rows.
- **Default chip:** purple outline, letterspaced, quiet. One per picker.
- **New-card row:** dashed border at rest (it *promises* a different kind of action — "go somewhere," Law 4), solid on hover, hands off to PAY-002. The handoff carries nothing sensitive — no partial numbers, no session card data.
- **PRIVACY BOUNDARY (this is part of the spec):** this block shows **at most the last-4 and the brand**, exactly as the payment backend returns them masked. It **never** renders, stores, or transmits a full card number — the full PAN exists only inside the processor's vault and inside PAY-002's transient input fields. Removing a saved method, if offered anywhere, goes through the processor's delete — the front end holds no card data to delete. Same rule as PAY-002: no card fields in console, analytics, or error reports, ever.
- **What it will NOT fake:** the picker never invents a saved method for the demo — an account with no saved cards shows the one-row picker, not two handsome fake Visas. The default chip is set by the user's stored preference, never by recency or by the block guessing. And the selected row is the *actually submitted* method — the visual selection and the form value are the same truth, never two truths.

---

## The family contract

The five blocks share one contract, so a checkout built from them behaves like one intelligence:

1. **One total, one truth.** PAY-001's total, PAY-002's button label, and PAY-003's hologram all render the same confirmed number. Three renderings, one source.
2. **Privacy is structural.** PAY-002 and PAY-005 carry the boundary in their specs — card data lives in transient inputs bound for the processor, and the display layer never sees more than last-4 + brand.
3. **No fake success anywhere.** Confirmation ignites on a confirmed response. The receipt email is claimed only when confirmed. "No money moved" is stated only when confirmed. Law 75, everywhere.
4. **Every interactive thing is alive.** Steppers, rows, fields, buttons — rest dark with white-lit edges, ignite in their own color on touch. Nothing flat, nothing dead.
5. **Plain words under pressure.** Validation messages, error panels, and microcopy never blame the user. The checkout is the moment trust is thinnest; the words carry it.
6. **Backend-gated money states (director review fix, 2026-10-16).** Nothing here implements a payment processor — every money state is a rendering of a backend response, never a client-side decision. PAY-003 renders only on a confirmed charge; "no money moved" (PAY-004) only on a confirmed no-charge; totals and promo (PAY-001) only from confirmed prices; the method list (PAY-005) only from the processor's masked saved-method response. Specimen numbers are illustrative — a live build binds them to real responses, and a state with no backend answer behind it does not render.
7. **One button DNA, one source (independent scorecard fix, 2026-10-16).** `.naya-btn` ships from a single canonical source (import/include) — never copy-pasted per block file. The DNA rendered in PAY-001's stylesheet is the *reference rendering* for the specimen; builders import the canonical file, they don't re-type it. A pasted canonical is a drift risk: a fix to the DNA lands once, in the source, and every block inherits it.
8. **One quiet control (independent scorecard fix, 2026-10-16).** `.naya-btn--quiet` — same DNA, speaks softly — is defined ONCE, here in the shared contract, and referenced by PAY-003 and PAY-004. No block defines what another block consumes:

   ```css
   /* the quiet variant — the family's shared quiet control, owned once here */
   .naya-btn--quiet{ background:transparent; border:1.5px solid rgba(255,255,255,.4); box-shadow:none; }
   .naya-btn--quiet:hover{ border-color:#a06bff; box-shadow:0 0 26px -6px rgba(160,107,255,.7); }
   ```

*End of the checkout block family. Five blocks, all four parts each. Shipped, not drafted.*
