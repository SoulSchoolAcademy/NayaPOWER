# NAYA SMART BLOCKS — code specimens

The ten canonical blocks, copy-paste ready. Each ships with: its code, its
states, a do/don't, and honest anatomy. Link `TOKENS.css` first — every
specimen builds on `var()` references only. A page with a private color is
drift.

Usage: `<link rel="stylesheet" href="DESIGN/TOKENS.css">` then paste the
block's `<style>` + HTML. Vanilla JS is inline where behavior is required.

---

## 1. INPUT / FORM

**Do:** elevate above context — a labeled field that feels like a raised
control, with a clear kicker label, calm hint, and a quiet, restrained error
state.
**Don't:** float without weight — no ghost inputs, no invisible affordances;
the field must read as a control at rest.
**States:** rest · hover · focus (soul ring) · error · disabled · placeholder.

```html
<style>
  .naya-field {
    --field-bg: var(--obsidian);
    --field-rim: var(--line);
    font-family: "Inter", system-ui, -apple-system, sans-serif;
    color: var(--white);
    max-width: 420px;
    margin: 0;
  }
  .naya-field .naya-field__label {
    display: block;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: .14em;
    text-transform: uppercase;
    color: var(--quiet);
    margin: 0 0 8px 2px;
  }
  .naya-field .naya-field__control {
    position: relative;
  }
  .naya-field .naya-field__input {
    width: 100%;
    box-sizing: border-box;
    appearance: none;
    background: var(--field-bg);
    border: 1.5px solid var(--field-rim);
    border-radius: var(--r-md);
    padding: 13px 14px;
    font-size: 15px;
    line-height: 1.5;
    color: var(--white);
    outline: none;
    transition: border-color .18s var(--ease), box-shadow .18s var(--ease), background .18s var(--ease), opacity .18s var(--ease);
    box-shadow: inset 0 1px 2px rgba(0,0,0,.35);
  }
  .naya-field .naya-field__input::placeholder {
    color: var(--secondary);
  }
  .naya-field .naya-field__input:hover {
    border-color: rgba(255,255,255,.22);
    background: var(--raise);
  }
  .naya-field .naya-field__input:focus-visible,
  .naya-field .naya-field__input:focus {
    border-color: var(--soul);
    background: var(--raise);
    box-shadow: 0 0 0 3px rgba(160,107,255,.28), inset 0 1px 2px rgba(0,0,0,.35);
  }
  .naya-field .naya-field__meta {
    display: flex;
    justify-content: space-between;
    gap: 12px;
    margin: 8px 2px 0;
    font-size: 12px;
    line-height: 1.45;
  }
  .naya-field .naya-field__hint {
    color: var(--secondary);
  }
  .naya-field .naya-field__error {
    color: var(--coral);
    display: none;
    font-weight: 500;
  }
  .naya-field[data-state="error"] .naya-field__input {
    border-color: var(--coral);
    background: var(--obsidian);
  }
  .naya-field[data-state="error"] .naya-field__input:focus,
  .naya-field[data-state="error"] .naya-field__input:focus-visible {
    border-color: var(--coral);
    box-shadow: 0 0 0 3px rgba(255,94,108,.18), inset 0 1px 2px rgba(0,0,0,.35);
  }
  .naya-field[data-state="error"] .naya-field__hint { display: none; }
  .naya-field[data-state="error"] .naya-field__error { display: block; }
  .naya-field[data-state="disabled"] .naya-field__label { color: var(--secondary); }
  .naya-field .naya-field__input:disabled {
    opacity: .45;
    cursor: not-allowed;
    border-color: var(--line);
    background: var(--obsidian);
    box-shadow: none;
  }
  .naya-field[data-state="disabled"] .naya-field__hint { color: var(--secondary); }
  .naya-field[data-state="disabled"] .naya-field__input:hover { background: var(--obsidian); }
</style>

<div class="naya-field" data-state="rest">
  <label class="naya-field__label" for="naya-name">Display name</label>
  <div class="naya-field__control">
    <input class="naya-field__input" id="naya-name" type="text"
           placeholder="What should we call you?"
           aria-describedby="naya-name-hint naya-name-error" />
  </div>
  <div class="naya-field__meta">
    <span class="naya-field__hint" id="naya-name-hint">Visible on your public profile. Letters and spaces only.</span>
    <span class="naya-field__error" id="naya-name-error" role="alert">Name can't be empty — add one to continue.</span>
  </div>
</div>
```

---

## 2. TOGGLE / SETTINGS

**Do:** make on/off unmistakable at a glance — OFF is quiet and honest; ON
speaks the verified language (green ignition) so state is never ambiguous.
**Don't:** use soul-purple for "on" — color has jobs: soul is chrome/identity,
green is verified truth/state. Don't rely on color alone — the knob position
and label carry the meaning.
**States:** off · on · hover · focus-visible ring · disabled.

```html
<style>
  .naya-toggle {
    font-family: "Inter", system-ui, -apple-system, sans-serif;
    color: var(--white);
  }
  .naya-switch {
    position: relative;
    display: inline-flex;
    align-items: center;
    padding: 0;
    margin: 0;
    border: none;
    background: none;
    cursor: pointer;
  }
  .naya-switch .naya-switch__track {
    width: 52px;
    height: 30px;
    border-radius: var(--r-pill);
    background: var(--obsidian);
    border: 1.5px solid var(--line);
    position: relative;
    transition: background .22s var(--ease), border-color .22s var(--ease), box-shadow .22s var(--ease), opacity .18s var(--ease);
    box-shadow: inset 0 1px 3px rgba(0,0,0,.5);
  }
  .naya-switch .naya-switch__knob {
    position: absolute;
    top: 50%;
    left: 4px;
    transform: translate(0, -50%);
    width: 22px;
    height: 22px;
    border-radius: var(--r-pill);
    background: var(--white);
    opacity: .75;
    box-shadow: 0 2px 6px rgba(0,0,0,.45);
    transition: transform .22s var(--ease), opacity .22s var(--ease), background .22s var(--ease);
  }
  .naya-switch:hover .naya-switch__track {
    border-color: rgba(255,255,255,.22);
  }
  .naya-switch:focus-visible {
    outline: none;
  }
  .naya-switch:focus-visible .naya-switch__track {
    border-color: var(--soul);
    box-shadow: 0 0 0 3px rgba(160,107,255,.28), inset 0 1px 3px rgba(0,0,0,.5);
  }
  .naya-switch[data-on="false"] .naya-switch__track {
    background: var(--obsidian);
    border-color: var(--line);
  }
  .naya-switch[data-on="true"] .naya-switch__track {
    background: var(--verified);
    border-color: var(--verified);
    box-shadow: 0 0 12px rgba(47,232,158,.25), inset 0 1px 2px rgba(0,0,0,.15);
  }
  .naya-switch[data-on="true"] .naya-switch__knob {
    transform: translate(22px, -50%);
    background: var(--white);
    opacity: 1;
  }
  .naya-switch:disabled {
    cursor: not-allowed;
  }
  .naya-switch:disabled .naya-switch__track {
    opacity: .4;
    box-shadow: none;
  }
  .naya-switch:disabled .naya-switch__knob {
    opacity: .5;
  }
  .naya-switch__word {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: .14em;
    text-transform: uppercase;
    margin-left: 12px;
    color: var(--secondary);
    transition: color .22s var(--ease);
    user-select: none;
  }
  .naya-switch[data-on="true"] .naya-switch__word { color: var(--verified); }
  .naya-switch:disabled .naya-switch__word { color: var(--secondary); opacity: .6; }
  .naya-settings {
    max-width: 560px;
    background: var(--card);
    border: 1.5px solid var(--line);
    border-radius: var(--r-lg);
    padding: 8px;
    box-shadow: var(--lift);
  }
  .naya-settings__kicker {
    display: block;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: .14em;
    text-transform: uppercase;
    color: var(--quiet);
    padding: 12px 16px 4px;
  }
  .naya-settings__row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    padding: 14px 16px;
    border-radius: var(--r-md);
    transition: background .18s var(--ease);
  }
  .naya-settings__row + .naya-settings__row {
    border-top: 1px solid var(--line);
    border-radius: 0;
  }
  .naya-settings__row:hover {
    background: var(--raise);
  }
  .naya-settings__text { min-width: 0; }
  .naya-settings__title {
    font-size: 15px;
    font-weight: 600;
    line-height: 1.45;
    margin: 0 0 2px;
  }
  .naya-settings__desc {
    font-size: 13px;
    line-height: 1.5;
    color: var(--secondary);
    margin: 0;
  }
  .naya-settings__row[data-disabled="true"] .naya-settings__title { color: var(--secondary); }
  .naya-settings__row[data-disabled="true"] .naya-settings__desc { opacity: .6; }
  .naya-settings__row[data-disabled="true"]:hover { background: none; }
</style>

<div class="naya-settings">
  <span class="naya-settings__kicker">Notifications</span>
  <div class="naya-settings__row">
    <div class="naya-settings__text">
      <p class="naya-settings__title">Smart Feed alerts</p>
      <p class="naya-settings__desc">Get pinged when a note you follow gets verified.</p>
    </div>
    <button class="naya-switch" data-on="true" role="switch" aria-checked="true"
            aria-label="Smart Feed alerts">
      <span class="naya-switch__track"><span class="naya-switch__knob"></span></span>
      <span class="naya-switch__word">On</span>
    </button>
  </div>
  <div class="naya-settings__row">
    <div class="naya-settings__text">
      <p class="naya-settings__title">Weekly digest</p>
      <p class="naya-settings__desc">One summary email every Monday morning.</p>
    </div>
    <button class="naya-switch" data-on="false" role="switch" aria-checked="false"
            aria-label="Weekly digest">
      <span class="naya-switch__track"><span class="naya-switch__knob"></span></span>
      <span class="naya-switch__word">Off</span>
    </button>
  </div>
  <div class="naya-settings__row" data-disabled="true">
    <div class="naya-settings__text">
      <p class="naya-settings__title">Public profile indexing</p>
      <p class="naya-settings__desc">Unavailable while your profile is private.</p>
    </div>
    <button class="naya-switch" data-on="false" role="switch" aria-checked="false" disabled
            aria-label="Public profile indexing">
      <span class="naya-switch__track"><span class="naya-switch__knob"></span></span>
      <span class="naya-switch__word">Off</span>
    </button>
  </div>
</div>

<script>
  document.querySelectorAll('.naya-switch:not(:disabled)').forEach(function (el) {
    el.addEventListener('click', function () {
      var on = el.getAttribute('data-on') === 'true';
      el.setAttribute('data-on', String(!on));
      el.setAttribute('aria-checked', String(!on));
      el.querySelector('.naya-switch__word').textContent = on ? 'Off' : 'On';
    });
  });
</script>
```

---

## 3. SEARCH INTERFACE

**Do:** show scope + truth state on every result — pills tell the user WHERE we
looked, badges tell them WHAT WE KNOW (✓ verified green, ? claim gold).
**Don't:** return mystery results — a result without a scope and a truth
badge is a guess, and guesses don't ship.
**States:** input rest/hover/focus · pill active/hover/focus-visible · results +
badges · honest empty state.

```html
<style>
  .naya-search {
    font-family: "Inter", system-ui, -apple-system, sans-serif;
    color: var(--white);
    max-width: 560px;
  }
  .naya-search__box {
    position: relative;
  }
  .naya-search__icon {
    position: absolute;
    left: 15px;
    top: 50%;
    transform: translateY(-50%);
    width: 17px;
    height: 17px;
    color: var(--secondary);
    pointer-events: none;
  }
  .naya-search__input {
    width: 100%;
    box-sizing: border-box;
    appearance: none;
    background: var(--obsidian);
    border: 1.5px solid var(--line);
    border-radius: var(--r-pill);
    padding: 13px 18px 13px 44px;
    font-size: 15px;
    line-height: 1.5;
    color: var(--white);
    outline: none;
    transition: border-color .18s var(--ease), box-shadow .18s var(--ease), background .18s var(--ease);
    box-shadow: inset 0 1px 2px rgba(0,0,0,.35);
  }
  .naya-search__input::placeholder { color: var(--secondary); }
  .naya-search__input:hover {
    border-color: rgba(255,255,255,.22);
    background: var(--raise);
  }
  .naya-search__input:focus-visible,
  .naya-search__input:focus {
    border-color: var(--soul);
    background: var(--raise);
    box-shadow: 0 0 0 3px rgba(160,107,255,.28), inset 0 1px 2px rgba(0,0,0,.35);
  }
  .naya-search__scopes {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin: 12px 2px 0;
  }
  .naya-pill {
    appearance: none;
    border: 1.5px solid var(--line);
    background: var(--obsidian);
    color: var(--quiet);
    border-radius: var(--r-pill);
    padding: 7px 15px;
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    transition: all .18s var(--ease);
  }
  .naya-pill:hover {
    border-color: rgba(255,255,255,.22);
    color: var(--white);
  }
  .naya-pill[data-active="true"] {
    background: var(--white);
    border-color: var(--white);
    color: var(--field);
    font-weight: 600;
  }
  .naya-pill:focus-visible {
    outline: none;
    box-shadow: 0 0 0 3px rgba(160,107,255,.28);
  }
  .naya-search__results {
    margin: 16px 0 0;
    padding: 0;
    list-style: none;
    display: grid;
    gap: 8px;
  }
  .naya-result {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    background: var(--card);
    border: 1.5px solid var(--line);
    border-radius: var(--r-md);
    padding: 14px 16px;
    box-shadow: var(--lift);
    transition: border-color .18s var(--ease), transform .18s var(--ease);
    cursor: pointer;
  }
  .naya-result:hover {
    border-color: rgba(255,255,255,.22);
    transform: translateY(-1px);
  }
  .naya-result__scope {
    flex: none;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: .1em;
    text-transform: uppercase;
    color: var(--soul);
    border: 1px solid rgba(160,107,255,.4);
    border-radius: var(--r-pill);
    padding: 3px 9px;
    margin-top: 1px;
  }
  .naya-result__body { min-width: 0; flex: 1; }
  .naya-result__title {
    font-size: 15px;
    font-weight: 600;
    line-height: 1.45;
    margin: 0 0 2px;
  }
  .naya-result__snippet {
    font-size: 13px;
    line-height: 1.5;
    color: var(--secondary);
    margin: 0;
  }
  .naya-badge {
    flex: none;
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: .08em;
    text-transform: uppercase;
    border-radius: var(--r-pill);
    padding: 4px 10px;
    margin-top: 1px;
    border: 1px solid transparent;
  }
  .naya-badge--verified {
    color: var(--verified);
    border-color: rgba(47,232,158,.4);
    background: rgba(47,232,158,.08);
  }
  .naya-badge--claim {
    color: var(--claim);
    border-color: rgba(255,191,61,.4);
    background: rgba(255,191,61,.08);
  }
  .naya-search__empty {
    margin: 16px 0 0;
    background: var(--card);
    border: 1.5px dashed var(--line);
    border-radius: var(--r-md);
    padding: 28px 24px;
    text-align: center;
    box-shadow: none;
  }
  .naya-search__empty[hidden] { display: none; }
  .naya-search__empty-title {
    font-size: 17px;
    font-weight: 600;
    margin: 0 0 6px;
  }
  .naya-search__empty-title .naya-search__query { color: var(--soul); }
  .naya-search__empty-sub {
    font-size: 13px;
    line-height: 1.55;
    color: var(--secondary);
    margin: 0 0 14px;
  }
  .naya-search__empty-try {
    display: inline-flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 8px;
  }
</style>

<div class="naya-search">
  <div class="naya-search__box">
    <svg class="naya-search__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor"
         stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
      <circle cx="11" cy="11" r="7"></circle>
      <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
    </svg>
    <input class="naya-search__input" id="naya-q" type="search" role="searchbox"
           placeholder="Search notes, people, rooms…" autocomplete="off" />
  </div>
  <div class="naya-search__scopes" role="group" aria-label="Search scope">
    <button class="naya-pill" data-active="true"  data-scope="all">All</button>
    <button class="naya-pill" data-active="false" data-scope="notes">Notes</button>
    <button class="naya-pill" data-active="false" data-scope="people">People</button>
    <button class="naya-pill" data-active="false" data-scope="rooms">Rooms</button>
  </div>
  <ul class="naya-search__results" id="naya-results">
    <li class="naya-result" data-scope="notes">
      <span class="naya-result__scope">Note</span>
      <div class="naya-result__body">
        <p class="naya-result__title">Morning pages compound over 90 days</p>
        <p class="naya-result__snippet">12 sessions logged · last updated Oct 14 · matches "morning"</p>
      </div>
      <span class="naya-badge naya-badge--verified">✓ Verified</span>
    </li>
    <li class="naya-result" data-scope="people">
      <span class="naya-result__scope">Person</span>
      <div class="naya-result__body">
        <p class="naya-result__title">Jordan Blake</p>
        <p class="naya-result__snippet">Mutual contact · 3 shared notes · matched on name</p>
      </div>
      <span class="naya-badge naya-badge--claim">? Claim</span>
    </li>
    <li class="naya-result" data-scope="rooms">
      <span class="naya-result__scope">Room</span>
      <div class="naya-result__body">
        <p class="naya-result__title">/hub/library — Design language shelf</p>
        <p class="naya-result__snippet">Shelf of 14 blocks · pinned by you · matched on "design"</p>
      </div>
      <span class="naya-badge naya-badge--verified">✓ Verified</span>
    </li>
  </ul>
  <div class="naya-search__empty" id="naya-empty" hidden>
    <p class="naya-search__empty-title">No results for <span class="naya-search__query">"x"</span></p>
    <p class="naya-search__empty-sub">Nothing in <span id="naya-empty-scope">All</span> matched. Try one of these:</p>
    <div class="naya-search__empty-try">
      <button class="naya-pill" data-try="morning">"morning"</button>
      <button class="naya-pill" data-try="design">"design"</button>
      <button class="naya-pill" data-try="jordan">"jordan"</button>
    </div>
  </div>
</div>

<script>
  (function () {
    var input   = document.getElementById('naya-q');
    var list    = document.getElementById('naya-results');
    var empty   = document.getElementById('naya-empty');
    var queryEl = empty.querySelector('.naya-search__query');
    var scopeEl = document.getElementById('naya-empty-scope');
    var pills   = Array.prototype.slice.call(document.querySelectorAll('.naya-search__scopes .naya-pill'));
    function activeScope() {
      var p = pills.find(function (x) { return x.getAttribute('data-active') === 'true'; });
      return p ? p.getAttribute('data-scope') : 'all';
    }
    function scopeLabel(s) {
      return s === 'all' ? 'All' : s.charAt(0).toUpperCase() + s.slice(1);
    }
    pills.forEach(function (pill) {
      pill.addEventListener('click', function () {
        pills.forEach(function (p) { p.setAttribute('data-active', 'false'); });
        pill.setAttribute('data-active', 'true');
        apply();
      });
    });
    function apply() {
      var q = input.value.trim().toLowerCase();
      var scope = activeScope();
      var shown = 0;
      Array.prototype.forEach.call(list.children, function (li) {
        var inScope = scope === 'all' || li.getAttribute('data-scope') === scope;
        var hay = li.textContent.toLowerCase();
        var hit = inScope && (!q || hay.indexOf(q) !== -1);
        li.style.display = hit ? '' : 'none';
        if (hit) shown++;
      });
      var isEmpty = q && shown === 0;
      empty.hidden = !isEmpty;
      list.style.display = isEmpty ? 'none' : '';
      if (isEmpty) {
        queryEl.textContent = '"' + input.value.trim() + '"';
        scopeEl.textContent = scopeLabel(scope);
      }
    }
    empty.querySelectorAll('[data-try]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        input.value = btn.getAttribute('data-try');
        apply();
        input.focus();
      });
    });
    input.addEventListener('input', apply);
    apply();
  })();
</script>
```

---

## 4. MODAL / DIALOG

**Do:** one clear action — the primary button says exactly what happens.
**Don't:** trap without escape — ✕, backdrop click, and Escape all close it.
**States:** buttons rest/hover/active/focus-visible · overlay fades, dialog
rises on var(--ease) · focus moves in on open, returns on close.

```html
<style>
  .naya-btn {
    display: inline-flex; align-items: center; justify-content: center;
    min-height: 54px; padding: 0 28px;
    border-radius: var(--r-pill);
    border: 1.5px solid var(--line);
    background: linear-gradient(180deg, var(--card), var(--field));
    color: var(--white);
    font-family: Inter, system-ui, -apple-system, sans-serif;
    font-size: 15px; font-weight: 600; letter-spacing: .01em; line-height: 1;
    cursor: pointer;
    box-shadow: inset 0 1px 0 var(--line), var(--lift);
    transition: transform .22s var(--ease), box-shadow .22s var(--ease), border-color .22s var(--ease);
  }
  .naya-btn:hover {
    transform: translateY(-2px);
    border-color: var(--quiet);
    box-shadow: inset 0 1px 0 var(--line), var(--lift), 0 12px 32px rgba(160,107,255,.42);
  }
  .naya-btn:active { transform: translateY(0) scale(.98); }
  .naya-btn:focus-visible { outline: 2.5px solid var(--soul); outline-offset: 3px; }
  .naya-btn--quiet {
    display: inline-flex; align-items: center; justify-content: center;
    min-height: 54px; padding: 0 24px;
    border-radius: var(--r-pill);
    border: 1px solid transparent;
    background: transparent;
    color: var(--secondary);
    font-family: Inter, system-ui, -apple-system, sans-serif;
    font-size: 15px; font-weight: 500; line-height: 1;
    cursor: pointer;
    transition: transform .2s var(--ease), color .2s var(--ease), background-color .2s var(--ease);
  }
  .naya-btn--quiet:hover {
    color: var(--white);
    background: rgba(255,255,255,.06);
    transform: translateY(-1px);
  }
  .naya-btn--quiet:active { transform: translateY(0) scale(.97); }
  .naya-btn--quiet:focus-visible { outline: 2.5px solid var(--secondary); outline-offset: 3px; }
  .naya-modal-overlay {
    position: fixed; inset: 0; z-index: 100;
    display: flex; align-items: center; justify-content: center;
    padding: 24px;
    background: rgba(5,5,7,.72);
    -webkit-backdrop-filter: blur(8px); backdrop-filter: blur(8px);
    opacity: 0; visibility: hidden; pointer-events: none;
    transition: opacity .28s var(--ease), visibility 0s linear .28s;
  }
  .naya-modal-overlay.is-open {
    opacity: 1; visibility: visible; pointer-events: auto;
    transition: opacity .28s var(--ease);
  }
  .naya-dialog {
    position: relative;
    width: min(440px, 100%);
    padding: 28px;
    border-radius: var(--r-lg);
    border: 1.5px solid var(--line);
    background: linear-gradient(180deg, var(--card), var(--obsidian));
    box-shadow: var(--lift), 0 48px 96px rgba(5,5,7,.65);
    opacity: 0; transform: translateY(16px) scale(.97);
  }
  .naya-modal-overlay.is-open .naya-dialog { animation: naya-dialog-in .42s var(--ease) forwards; }
  @keyframes naya-dialog-in {
    from { opacity: 0; transform: translateY(16px) scale(.97); }
    to   { opacity: 1; transform: translateY(0) scale(1); }
  }
  .naya-dialog__close {
    position: absolute; top: 14px; right: 14px;
    width: 34px; height: 34px; border-radius: 50%;
    display: inline-flex; align-items: center; justify-content: center;
    border: 1px solid transparent; background: transparent;
    color: var(--secondary); font-size: 15px; line-height: 1;
    cursor: pointer;
    transition: color .18s var(--ease), background-color .18s var(--ease), transform .18s var(--ease);
  }
  .naya-dialog__close:hover { color: var(--white); background: rgba(255,255,255,.08); }
  .naya-dialog__close:active { transform: scale(.92); }
  .naya-dialog__close:focus-visible { outline: 2px solid var(--secondary); outline-offset: 2px; }
  .naya-dialog__kicker {
    margin: 0 0 10px;
    font-family: Inter, system-ui, -apple-system, sans-serif;
    font-size: 11px; font-weight: 600; line-height: 1.2;
    letter-spacing: .14em; text-transform: uppercase;
    color: var(--secondary);
  }
  .naya-dialog__title {
    margin: 0 0 12px;
    font-family: Inter, system-ui, -apple-system, sans-serif;
    font-size: 24px; font-weight: 700; line-height: 1.25; letter-spacing: -.01em;
    color: var(--white);
  }
  .naya-dialog__body {
    margin: 0;
    font-family: Inter, system-ui, -apple-system, sans-serif;
    font-size: 15px; font-weight: 400; line-height: 1.6;
    color: var(--quiet);
  }
  .naya-dialog__actions {
    display: flex; flex-direction: column; align-items: stretch; gap: 10px;
    margin-top: 26px;
  }
  .naya-dialog__actions .naya-btn { width: 100%; }
  @media (prefers-reduced-motion: reduce) {
    .naya-modal-overlay, .naya-dialog, .naya-btn, .naya-btn--quiet, .naya-dialog__close { transition: none; animation: none; }
    .naya-modal-overlay.is-open .naya-dialog { opacity: 1; transform: none; }
  }
</style>

<button type="button" class="naya-btn" data-modal-open="save-dialog">Save smart note</button>

<div class="naya-modal-overlay" id="save-dialog-overlay" aria-hidden="true">
  <div class="naya-dialog" id="save-dialog" role="dialog" aria-modal="true"
       aria-labelledby="save-dialog-title" aria-describedby="save-dialog-body" tabindex="-1">
    <button type="button" class="naya-dialog__close" data-modal-close aria-label="Close dialog">✕</button>
    <p class="naya-dialog__kicker">Smart Note</p>
    <h2 class="naya-dialog__title" id="save-dialog-title">Save this note to your feed?</h2>
    <p class="naya-dialog__body" id="save-dialog-body">This writes the note to your shared feed where the team can read it. Saving is the one thing this dialog does — everything else stays exactly where it is.</p>
    <div class="naya-dialog__actions">
      <button type="button" class="naya-btn" data-modal-close>Save note</button>
      <button type="button" class="naya-btn--quiet" data-modal-close>Not now</button>
    </div>
  </div>
</div>

<script>
(function () {
  var overlay = document.getElementById('save-dialog-overlay');
  var dialog = document.getElementById('save-dialog');
  var lastFocus = null;
  function openModal() {
    lastFocus = document.activeElement;
    overlay.classList.add('is-open');
    overlay.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
    requestAnimationFrame(function () { dialog.focus({ preventScroll: true }); });
  }
  function closeModal() {
    overlay.classList.remove('is-open');
    overlay.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
    if (lastFocus && typeof lastFocus.focus === 'function') lastFocus.focus({ preventScroll: true });
  }
  document.querySelectorAll('[data-modal-open="save-dialog"]').forEach(function (btn) {
    btn.addEventListener('click', openModal);
  });
  overlay.querySelectorAll('[data-modal-close]').forEach(function (el) {
    el.addEventListener('click', closeModal);
  });
  overlay.addEventListener('click', function (e) {
    if (e.target === overlay) closeModal();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && overlay.classList.contains('is-open')) closeModal();
  });
})();
</script>
```

---

## 5. TOAST / NOTIFICATION

**Do:** report truthfully and briefly — one line, one truth color.
**Don't:** fake success — CLAIM never wears a ✓; DEMO never glows verified.
**States:** slide-in on var(--ease) · rest · ✕ dismiss · auto-dismiss 6s
(hover pauses the timer so it can be read) · slide-out on leave.

```html
<style>
  .naya-toasts {
    position: fixed; right: 20px; bottom: 20px; z-index: 200;
    display: flex; flex-direction: column; gap: 12px;
    width: min(360px, calc(100vw - 40px));
  }
  .naya-toast {
    position: relative; overflow: hidden;
    display: flex; align-items: flex-start; gap: 12px;
    padding: 14px 12px 14px 18px;
    border-radius: var(--r-md);
    border: 1.5px solid var(--line);
    background: linear-gradient(180deg, var(--raise), var(--obsidian));
    box-shadow: var(--lift);
    animation: naya-toast-in .45s var(--ease) both;
  }
  .naya-toast.is-leaving { animation: naya-toast-out .35s var(--ease) both; }
  @keyframes naya-toast-in {
    from { opacity: 0; transform: translateX(32px); }
    to   { opacity: 1; transform: translateX(0); }
  }
  @keyframes naya-toast-out {
    from { opacity: 1; transform: translateX(0); }
    to   { opacity: 0; transform: translateX(32px); }
  }
  .naya-toast::before {
    content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 3px;
    background: var(--line);
  }
  .naya-toast__icon {
    flex: 0 0 auto;
    width: 30px; height: 30px; border-radius: 50%;
    display: inline-flex; align-items: center; justify-content: center;
    border: 1.5px solid var(--line);
    background: var(--field);
    font-family: Inter, system-ui, -apple-system, sans-serif;
    font-size: 14px; font-weight: 700; line-height: 1;
  }
  .naya-toast__body { flex: 1 1 auto; min-width: 0; padding-top: 1px; }
  .naya-toast__title {
    margin: 0;
    font-family: Inter, system-ui, -apple-system, sans-serif;
    font-size: 15px; font-weight: 600; line-height: 1.35;
    color: var(--white);
  }
  .naya-toast__detail {
    margin: 3px 0 0;
    font-family: Inter, system-ui, -apple-system, sans-serif;
    font-size: 13px; font-weight: 400; line-height: 1.45;
    color: var(--secondary);
  }
  .naya-toast__close {
    flex: 0 0 auto;
    width: 28px; height: 28px; border-radius: 50%;
    display: inline-flex; align-items: center; justify-content: center;
    border: 1px solid transparent; background: transparent;
    color: var(--secondary); font-size: 12px; line-height: 1;
    cursor: pointer;
    transition: color .18s var(--ease), background-color .18s var(--ease), transform .18s var(--ease);
  }
  .naya-toast__close:hover { color: var(--white); background: rgba(255,255,255,.08); }
  .naya-toast__close:active { transform: scale(.92); }
  .naya-toast__close:focus-visible { outline: 2px solid var(--secondary); outline-offset: 2px; }
  .naya-toast--verified { border-color: rgba(47,232,158,.38); }
  .naya-toast--verified::before { background: var(--verified); }
  .naya-toast--verified .naya-toast__icon {
    color: var(--verified);
    border-color: rgba(47,232,158,.55);
    box-shadow: 0 0 16px rgba(47,232,158,.28);
  }
  .naya-toast--claim { border-color: rgba(255,191,61,.38); }
  .naya-toast--claim::before { background: var(--claim); }
  .naya-toast--claim .naya-toast__icon {
    color: var(--claim);
    border-color: rgba(255,191,61,.55);
    border-style: dashed;
  }
  .naya-toast--demo { border-color: rgba(232,79,255,.38); }
  .naya-toast--demo::before { background: var(--demo); }
  .naya-toast--demo .naya-toast__icon {
    color: var(--demo);
    border-color: rgba(232,79,255,.55);
    box-shadow: 0 0 16px rgba(232,79,255,.28);
  }
  .naya-toast-demo-row { display: flex; flex-wrap: wrap; gap: 8px; }
  .naya-toast-demo-btn {
    display: inline-flex; align-items: center; justify-content: center;
    min-height: 44px; padding: 0 20px;
    border-radius: var(--r-pill);
    border: 1.5px solid var(--line);
    background: linear-gradient(180deg, var(--card), var(--obsidian));
    box-shadow: var(--lift);
    color: var(--quiet);
    font-family: Inter, system-ui, -apple-system, sans-serif;
    font-size: 13px; font-weight: 600; line-height: 1;
    cursor: pointer;
    transition: transform .2s var(--ease), color .2s var(--ease), border-color .2s var(--ease);
  }
  .naya-toast-demo-btn:hover { transform: translateY(-2px); color: var(--white); border-color: var(--quiet); }
  .naya-toast-demo-btn:active { transform: translateY(0) scale(.97); }
  .naya-toast-demo-btn:focus-visible { outline: 2.5px solid var(--secondary); outline-offset: 3px; }
  @media (prefers-reduced-motion: reduce) {
    .naya-toast, .naya-toast.is-leaving, .naya-toast-demo-btn { animation: none; transition: none; }
  }
</style>

<div class="naya-toast-demo-row">
  <button type="button" class="naya-toast-demo-btn" data-toast-demo="verified">Show verified</button>
  <button type="button" class="naya-toast-demo-btn" data-toast-demo="claim">Show claim</button>
  <button type="button" class="naya-toast-demo-btn" data-toast-demo="demo">Show demonstration</button>
</div>
<div class="naya-toasts" id="naya-toasts" aria-live="polite"></div>

<script>
(function () {
  var stack = document.getElementById('naya-toasts');
  var AUTO_MS = 6000;
  function receiptNo() { return 'SN-' + Math.floor(1000 + Math.random() * 9000); }
  var CONFIG = {
    verified: { glyph: '✓', title: 'Smart Note saved', detail: function () { return 'Receipt #' + receiptNo(); } },
    claim:    { glyph: '?', title: 'Sync pending', detail: function () { return 'Will confirm — nothing confirmed yet.'; } },
    demo:     { glyph: '◈', title: 'Preview', detail: function () { return 'Not live — demo data only.'; } }
  };
  function showToast(kind) {
    var cfg = CONFIG[kind];
    if (!cfg) return;
    var el = document.createElement('div');
    el.className = 'naya-toast naya-toast--' + kind;
    el.setAttribute('role', 'status');
    var icon = document.createElement('span');
    icon.className = 'naya-toast__icon';
    icon.setAttribute('aria-hidden', 'true');
    icon.textContent = cfg.glyph;
    var body = document.createElement('div');
    body.className = 'naya-toast__body';
    var title = document.createElement('p');
    title.className = 'naya-toast__title';
    title.textContent = cfg.title;
    var detail = document.createElement('p');
    detail.className = 'naya-toast__detail';
    detail.textContent = cfg.detail();
    body.appendChild(title);
    body.appendChild(detail);
    var close = document.createElement('button');
    close.type = 'button';
    close.className = 'naya-toast__close';
    close.setAttribute('aria-label', 'Dismiss notification');
    close.textContent = '✕';
    el.appendChild(icon);
    el.appendChild(body);
    el.appendChild(close);
    stack.appendChild(el);
    var timer = null;
    function dismiss() {
      if (el.classList.contains('is-leaving')) return;
      clearTimeout(timer);
      el.classList.add('is-leaving');
      el.addEventListener('animationend', function () { el.remove(); }, { once: true });
      setTimeout(function () { el.remove(); }, 450);
    }
    timer = setTimeout(dismiss, AUTO_MS);
    close.addEventListener('click', dismiss);
    el.addEventListener('mouseenter', function () { clearTimeout(timer); });
    el.addEventListener('mouseleave', function () { timer = setTimeout(dismiss, AUTO_MS); });
  }
  document.querySelectorAll('[data-toast-demo]').forEach(function (btn) {
    btn.addEventListener('click', function () { showToast(btn.getAttribute('data-toast-demo')); });
  });
})();
</script>
```

---

## 6. DATA TABLE

**Do:** labels left, numbers right. Header row in kicker type. Row hover lifts
to --raise. One selected row carries the soul edge. Truth badges inline.
**Don't:** center every column. Never use color without a job.
**States:** header · row hover · selected row · truth badges (verified/claim/demo).

```html
<style>
  .naya-table-block{
    background:linear-gradient(180deg,var(--card),var(--obsidian));
    border:1.5px solid var(--line);
    border-radius:var(--r-lg);
    padding:22px;
    max-width:760px;
    font-family:Inter,-apple-system,"Segoe UI",sans-serif;
  }
  .naya-kicker{
    font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.14em;
    color:var(--secondary);margin:0 0 12px;
  }
  .naya-table{width:100%;border-collapse:collapse;}
  .naya-table th{
    font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.12em;
    color:var(--secondary);text-align:left;
    padding:10px 12px;border-bottom:1.5px solid var(--line);
  }
  .naya-table td{
    padding:13px 12px;border-bottom:1px solid var(--line);
    font-size:15px;line-height:1.5;color:var(--white);
    vertical-align:middle;
  }
  .naya-table tbody tr{transition:background .25s var(--ease);}
  .naya-table tbody tr:hover{background:var(--raise);}
  .naya-table tbody tr:last-child td{border-bottom:none;}
  .naya-table tr.selected{background:var(--raise);box-shadow:inset 2px 0 0 var(--soul);}
  .naya-table .num{text-align:right;font-variant-numeric:tabular-nums;}
  .naya-title{font-weight:600;color:var(--white);}
  .naya-detail{font-size:12.5px;color:var(--secondary);white-space:nowrap;}
  .truth{
    display:inline-flex;align-items:center;gap:6px;
    font-size:12px;font-weight:600;white-space:nowrap;
    color:var(--t);
    padding:4px 11px;border:1.5px solid var(--line);border-radius:var(--r-pill);
    transition:box-shadow .25s var(--ease),border-color .25s var(--ease);
  }
  .truth:hover{box-shadow:0 0 14px -3px var(--t);border-color:var(--t);}
  .truth.verified{--t:var(--verified);}
  .truth.claim{--t:var(--claim);}
  .truth.demo{--t:var(--demo);}
  .truth .mark{font-size:11px;line-height:1;}
</style>

<div class="naya-table-block">
  <p class="naya-kicker">Recent Smart Notes</p>
  <table class="naya-table">
    <thead>
      <tr>
        <th scope="col">Title</th>
        <th scope="col">Room</th>
        <th scope="col" class="num">Notes</th>
        <th scope="col">Updated</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="naya-title">First Light acceptance checklist</td>
        <td><span class="truth verified"><span class="mark">✓</span>Feed</span></td>
        <td class="num">42</td>
        <td class="naya-detail">2h ago</td>
      </tr>
      <tr>
        <td class="naya-title">Hub contract v1 — the 7 hops</td>
        <td><span class="truth verified"><span class="mark">✓</span>Today</span></td>
        <td class="num">35</td>
        <td class="naya-detail">5h ago</td>
      </tr>
      <tr class="selected">
        <td class="naya-title">Emitter D4 doctrine note</td>
        <td><span class="truth claim"><span class="mark">?</span>Ledger</span></td>
        <td class="num">28</td>
        <td class="naya-detail">Yesterday</td>
      </tr>
      <tr>
        <td class="naya-title">Compiler v2 direction</td>
        <td><span class="truth claim"><span class="mark">?</span>Reports</span></td>
        <td class="num">18</td>
        <td class="naya-detail">2 days ago</td>
      </tr>
      <tr>
        <td class="naya-title">Design library seed list</td>
        <td><span class="truth demo"><span class="mark">~</span>Lists</span></td>
        <td class="num">12</td>
        <td class="naya-detail">3 days ago</td>
      </tr>
    </tbody>
  </table>
</div>
```

---

## 7. CHART / DATA-VIZ

**Do:** axes labeled. Baseline pinned at a true zero — bars drawn to true
scale, never truncated. Spectrum order: magenta→purple→blue→green→gold.
Value on every bar; hover lifts with its own color.
**Don't:** truncate the axis or stretch bars to deceive. No fake depth.
**States:** rest · per-bar hover (lifts, own-color glow).

```html
<style>
  .naya-chart-block{
    background:linear-gradient(180deg,var(--card),var(--obsidian));
    border:1.5px solid var(--line);
    border-radius:var(--r-lg);
    padding:22px;
    max-width:760px;
    font-family:Inter,-apple-system,"Segoe UI",sans-serif;
  }
  .naya-chart{display:flex;gap:12px;margin-top:4px;}
  .naya-yaxis{
    display:flex;flex-direction:column;justify-content:space-between;
    height:230px;min-width:30px;text-align:right;
    font-size:11px;color:var(--secondary);font-variant-numeric:tabular-nums;
  }
  .naya-plot{position:relative;flex:1;height:230px;}
  .naya-grid{
    position:absolute;left:0;right:0;height:1px;
    background:var(--line);opacity:.55;
  }
  .naya-baseline{
    position:absolute;left:0;right:0;bottom:0;height:1.5px;background:var(--line);
  }
  .naya-bars{
    position:absolute;inset:0;display:flex;align-items:stretch;gap:10px;
  }
  .naya-barcol{
    flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;
  }
  .naya-barval{
    font-size:13px;font-weight:700;color:var(--white);
    font-variant-numeric:tabular-nums;margin-bottom:8px;line-height:1;
  }
  .naya-bar{
    width:min(64px,72%);height:var(--h);
    border-radius:var(--r-sm) var(--r-sm) 0 0;
    background:var(--bar);
    box-shadow:inset 0 1px 0 rgba(255,255,255,.25);
    transition:transform .3s var(--ease),box-shadow .3s var(--ease);
  }
  .naya-barcol:hover .naya-bar{
    transform:translateY(-4px);
    box-shadow:0 12px 28px -8px var(--bar), inset 0 1px 0 rgba(255,255,255,.25);
  }
  .naya-xlabels{display:flex;margin-left:42px;}
  .naya-xlabels span{
    flex:1;text-align:center;font-size:12px;color:var(--secondary);padding-top:10px;
  }
  .naya-honest{
    margin:14px 0 0;font-size:12px;color:var(--secondary);line-height:1.5;
  }
  .naya-honest strong{color:var(--verified);font-weight:700;}
</style>

<div class="naya-chart-block">
  <p class="naya-kicker">Notes per room — last 7 days</p>
  <div class="naya-chart">
    <div class="naya-yaxis" aria-hidden="true">
      <span>50</span><span>40</span><span>30</span><span>20</span><span>10</span><span>0</span>
    </div>
    <div class="naya-plot" role="img" aria-label="Bar chart of notes per room over the last 7 days. Feed 42, Today 35, Ledger 28, Reports 18, Lists 12. Baseline at zero.">
      <div class="naya-grid" style="top:0%"></div>
      <div class="naya-grid" style="top:20%"></div>
      <div class="naya-grid" style="top:40%"></div>
      <div class="naya-grid" style="top:60%"></div>
      <div class="naya-grid" style="top:80%"></div>
      <div class="naya-baseline"></div>
      <div class="naya-bars">
        <div class="naya-barcol" style="--bar:var(--magenta);--h:84%">
          <span class="naya-barval">42</span><div class="naya-bar"></div>
        </div>
        <div class="naya-barcol" style="--bar:var(--purple);--h:70%">
          <span class="naya-barval">35</span><div class="naya-bar"></div>
        </div>
        <div class="naya-barcol" style="--bar:var(--blue);--h:56%">
          <span class="naya-barval">28</span><div class="naya-bar"></div>
        </div>
        <div class="naya-barcol" style="--bar:var(--green);--h:36%">
          <span class="naya-barval">18</span><div class="naya-bar"></div>
        </div>
        <div class="naya-barcol" style="--bar:var(--gold);--h:24%">
          <span class="naya-barval">12</span><div class="naya-bar"></div>
        </div>
      </div>
    </div>
  </div>
  <div class="naya-xlabels" aria-hidden="true">
    <span>Feed</span><span>Today</span><span>Ledger</span><span>Reports</span><span>Lists</span>
  </div>
  <p class="naya-honest"><strong>✓ Honest scale</strong> — baseline pinned at 0, bars drawn to true scale. No truncation, no stretch.</p>
</div>
```

---

## 8. CONTENT CARD

**Do:** one idea per card — kicker + headline + 2-line body + one quiet action.
**Don't:** overload — no spectrum spine, no second actions, no extra metadata.
Distinct from boards: smaller, single idea.
**States:** rest · hover (lifts -3px, border-light) · focus-visible.

```html
<style>
  .nb-card {
    background: var(--card);
    border: 1.5px solid var(--line);
    border-radius: var(--r-lg);
    padding: 22px 24px;
    box-shadow: var(--lift);
    transition: transform .35s var(--ease), border-color .35s var(--ease), box-shadow .35s var(--ease);
    max-width: 380px;
    cursor: default;
    outline: none;
  }
  .nb-card:hover {
    transform: translateY(-3px);
    border-color: rgba(255,255,255,.28);
    box-shadow: 0 14px 44px rgba(0,0,0,.55), 0 0 0 1px rgba(255,255,255,.08);
  }
  .nb-card:focus-visible {
    border-color: var(--soul);
    box-shadow: 0 0 0 3px rgba(160,107,255,.35), var(--lift);
  }
  .nb-card__kicker {
    display: flex;
    align-items: center;
    gap: 8px;
    font-family: Inter, sans-serif;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: .14em;
    text-transform: uppercase;
    color: var(--quiet);
    margin: 0 0 10px;
  }
  .nb-card__kicker::before {
    content: "◆";
    color: var(--magenta);
    font-size: 10px;
  }
  .nb-card__headline {
    font-family: Inter, sans-serif;
    font-size: 22px;
    line-height: 1.3;
    color: var(--white);
    margin: 0 0 8px;
  }
  .nb-card__body {
    font-family: Inter, sans-serif;
    font-size: 15px;
    line-height: 1.6;
    color: var(--secondary);
    margin: 0 0 16px;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
  .nb-card__action {
    font-family: Inter, sans-serif;
    font-size: 13px;
    font-weight: 600;
    color: var(--quiet);
    text-decoration: none;
    border-bottom: 1px solid var(--line);
    padding-bottom: 2px;
    transition: color .25s var(--ease), border-color .25s var(--ease);
  }
  .nb-card__action:hover { color: var(--white); border-color: var(--white); }
  .nb-card__action:focus-visible {
    outline: none;
    color: var(--white);
    box-shadow: 0 0 0 3px rgba(160,107,255,.35);
    border-radius: var(--r-sm);
  }
</style>

<article class="nb-card" tabindex="0" aria-label="Smart Note: Trust is a ledger">
  <p class="nb-card__kicker">Smart Note</p>
  <h3 class="nb-card__headline">Trust is a ledger, not a feeling.</h3>
  <p class="nb-card__body">Every promise kept is a deposit. Every receipt shared is compound interest. The balance is always visible.</p>
  <a class="nb-card__action" href="#">Read the note →</a>
</article>
```

---

## 9. MEDIA PLAYER

**Do:** portal-style play (66px black field, white triangle, jewel ring),
honest progress.
**Don't:** fake the buffer — buffering is pulsing, labeled "Buffering…", and
never moves progress.
**States:** ready · buffering (pulsing, labeled) · playing · paused ·
finished · portal rest/hover/active/focus-visible.

```html
<style>
  .nb-player {
    background: var(--card);
    border: 1.5px solid var(--line);
    border-radius: var(--r-lg);
    padding: 18px 20px;
    box-shadow: var(--lift);
    max-width: 520px;
    display: flex;
    align-items: center;
    gap: 18px;
    transition: border-color .35s var(--ease);
  }
  .nb-player:hover { border-color: rgba(255,255,255,.22); }
  .nb-portal {
    flex: 0 0 auto;
    width: 66px;
    height: 66px;
    border-radius: 50%;
    background: var(--field);
    border: 1.5px solid rgba(255,255,255,.45);
    box-shadow: 0 0 0 3px rgba(160,107,255,.55), 0 8px 24px rgba(0,0,0,.5), inset 0 2px 6px rgba(255,255,255,.12);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: transform .3s var(--ease), box-shadow .3s var(--ease);
    padding: 0;
  }
  .nb-portal:hover { transform: scale(1.06); }
  .nb-portal:active { transform: scale(.97); }
  .nb-portal:focus-visible { outline: none; box-shadow: 0 0 0 5px rgba(160,107,255,.45), var(--lift); }
  .nb-portal svg { width: 24px; height: 24px; fill: var(--white); margin-left: 3px; }
  .nb-portal.is-paused svg { margin-left: 0; }
  .nb-player__meta { flex: 1 1 auto; min-width: 0; }
  .nb-player__kicker {
    font-family: Inter, sans-serif;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: .14em;
    text-transform: uppercase;
    color: var(--quiet);
    margin: 0 0 4px;
  }
  .nb-player__title {
    font-family: Inter, sans-serif;
    font-size: 16px;
    color: var(--white);
    margin: 0 0 12px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .nb-player__track {
    position: relative;
    height: 6px;
    border-radius: var(--r-pill);
    background: var(--raise);
    border: 1px solid var(--line);
    overflow: hidden;
    cursor: pointer;
  }
  .nb-player__buffer {
    position: absolute;
    inset: 0 auto 0 0;
    width: 0%;
    background: rgba(248,247,251,.18);
    border-radius: var(--r-pill);
  }
  .nb-player__fill {
    position: absolute;
    inset: 0 auto 0 0;
    width: 0%;
    background: var(--soul);
    border-radius: var(--r-pill);
    box-shadow: 0 0 8px rgba(160,107,255,.8);
    transition: width .25s linear;
  }
  .nb-player__row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 8px;
  }
  .nb-player__time {
    font-family: Inter, sans-serif;
    font-size: 12px;
    color: var(--secondary);
    font-variant-numeric: tabular-nums;
  }
  .nb-player__state {
    font-family: Inter, sans-serif;
    font-size: 12px;
    font-weight: 600;
    color: var(--secondary);
  }
  .nb-player__state.is-buffering {
    color: var(--quiet);
    animation: nb-pulse 1.1s ease-in-out infinite;
  }
  @keyframes nb-pulse {
    0%, 100% { opacity: .45; }
    50% { opacity: 1; }
  }
</style>

<div class="nb-player" id="nbPlayer">
  <button class="nb-portal" id="nbPortalBtn" aria-label="Play Powercast" aria-pressed="false">
    <svg viewBox="0 0 24 24" id="nbPortalIcon" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>
  </button>
  <div class="nb-player__meta">
    <p class="nb-player__kicker">Powercast</p>
    <p class="nb-player__title">The Smart Note: proof before promise</p>
    <div class="nb-player__track" id="nbTrack" role="slider" aria-label="Playback progress" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0" tabindex="0">
      <div class="nb-player__buffer" id="nbBuffer"></div>
      <div class="nb-player__fill" id="nbFill"></div>
    </div>
    <div class="nb-player__row">
      <span class="nb-player__time" id="nbTime">0:00 / 12:47</span>
      <span class="nb-player__state" id="nbState">Ready</span>
    </div>
  </div>
</div>

<script>
(function () {
  var DURATION = 767;
  var current = 0, playing = false, buffering = false, tick = null;
  var btn = document.getElementById('nbPortalBtn');
  var icon = document.getElementById('nbPortalIcon');
  var fill = document.getElementById('nbFill');
  var buffer = document.getElementById('nbBuffer');
  var timeEl = document.getElementById('nbTime');
  var stateEl = document.getElementById('nbState');
  var track = document.getElementById('nbTrack');
  var PLAY_PATH = 'M8 5v14l11-7z';
  var PAUSE_PATH = 'M6 5h4v14H6zM14 5h4v14h-4z';
  function fmt(s) {
    s = Math.floor(s);
    return Math.floor(s / 60) + ':' + String(s % 60).padStart(2, '0');
  }
  function render() {
    var pct = (current / DURATION) * 100;
    fill.style.width = pct + '%';
    track.setAttribute('aria-valuenow', Math.round(pct));
    timeEl.textContent = fmt(current) + ' / ' + fmt(DURATION);
  }
  function setIcon(path, paused) {
    icon.querySelector('path').setAttribute('d', path);
    btn.classList.toggle('is-paused', paused);
    btn.setAttribute('aria-pressed', String(!paused));
    btn.setAttribute('aria-label', paused ? 'Play Powercast' : 'Pause Powercast');
  }
  function setState(text, isBuffering) {
    stateEl.textContent = text;
    stateEl.classList.toggle('is-buffering', !!isBuffering);
  }
  function startPlayback() {
    buffering = true;
    setState('Buffering…', true);
    setTimeout(function () {
      buffering = false;
      playing = true;
      setIcon(PAUSE_PATH, false);
      setState('Playing', false);
      tick = setInterval(function () {
        if (current < DURATION) { current += 1; render(); }
        else { pausePlayback(true); }
      }, 1000);
    }, 1200);
  }
  function pausePlayback(ended) {
    playing = false;
    clearInterval(tick);
    setIcon(PLAY_PATH, true);
    setState(ended ? 'Finished' : 'Paused', false);
  }
  btn.addEventListener('click', function () {
    if (buffering) return;
    if (playing) pausePlayback(false);
    else { if (current >= DURATION) current = 0; startPlayback(); }
  });
  var prefetch = 0;
  setInterval(function () {
    if (prefetch < 100) {
      prefetch = Math.min(100, prefetch + (playing ? 4 : 1.2));
      buffer.style.width = prefetch + '%';
    }
  }, 500);
  track.addEventListener('click', function (e) {
    var rect = track.getBoundingClientRect();
    var ratio = Math.min(1, Math.max(0, (e.clientX - rect.left) / rect.width));
    current = Math.floor(ratio * DURATION);
    if (prefetch < ratio * 100) prefetch = ratio * 100;
    render();
  });
  track.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
      e.preventDefault();
      current = Math.min(DURATION, Math.max(0, current + (e.key === 'ArrowRight' ? 10 : -10)));
      render();
    }
  });
  render();
})();
</script>
```

---

## 10. SMART LINK / SHARE SHEET

**Do:** destination clear (icon + name each), confirm step before sending.
**Don't:** one-tap surprise sends — every send passes the confirm gate.
**States:** rest · hover · selected · focus-visible · confirm-open · sent.

```html
<style>
  .nb-share {
    background: var(--card);
    border: 1.5px solid var(--line);
    border-radius: var(--r-lg);
    padding: 22px 24px;
    box-shadow: var(--lift);
    max-width: 420px;
  }
  .nb-share__kicker {
    font-family: Inter, sans-serif;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: .14em;
    text-transform: uppercase;
    color: var(--quiet);
    margin: 0 0 4px;
  }
  .nb-share__title {
    font-family: Inter, sans-serif;
    font-size: 18px;
    color: var(--white);
    margin: 0 0 16px;
  }
  .nb-share__dest {
    display: flex;
    align-items: center;
    gap: 14px;
    width: 100%;
    background: var(--raise);
    border: 1.5px solid var(--line);
    border-radius: var(--r-md);
    padding: 14px 16px;
    margin-bottom: 10px;
    cursor: pointer;
    color: var(--white);
    font-family: Inter, sans-serif;
    text-align: left;
    transition: border-color .3s var(--ease), transform .3s var(--ease), background .3s var(--ease);
  }
  .nb-share__dest:hover { border-color: rgba(255,255,255,.3); transform: translateX(4px); }
  .nb-share__dest:focus-visible { outline: none; border-color: var(--soul); box-shadow: 0 0 0 3px rgba(160,107,255,.35); }
  .nb-share__dest.is-selected { border-color: var(--soul); background: var(--obsidian); }
  .nb-share__icon {
    flex: 0 0 auto;
    width: 38px;
    height: 38px;
    border-radius: var(--r-sm);
    background: var(--field);
    border: 1px solid var(--line);
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .nb-share__icon svg { width: 18px; height: 18px; fill: none; stroke: var(--soul); stroke-width: 1.8; }
  .nb-share__name { font-size: 15px; font-weight: 600; }
  .nb-share__hint { font-size: 12px; color: var(--secondary); display: block; margin-top: 2px; }
  .nb-share__confirm {
    display: none;
    border-top: 1px solid var(--line);
    margin-top: 16px;
    padding-top: 18px;
  }
  .nb-share__confirm.is-open { display: block; }
  .nb-share__question {
    font-family: Inter, sans-serif;
    font-size: 16px;
    color: var(--white);
    margin: 0 0 16px;
  }
  .nb-share__question strong { color: var(--soul); }
  .nb-share__actions { display: flex; gap: 10px; }
  .nb-btn {
    font-family: Inter, sans-serif;
    font-size: 14px;
    font-weight: 600;
    border-radius: var(--r-pill);
    padding: 11px 22px;
    cursor: pointer;
    border: 1.5px solid transparent;
    transition: transform .25s var(--ease), box-shadow .25s var(--ease), background .25s var(--ease);
  }
  .nb-btn:focus-visible { outline: none; box-shadow: 0 0 0 3px rgba(160,107,255,.4); }
  .nb-btn--send {
    background: var(--white);
    color: var(--field);
    box-shadow: 0 4px 18px rgba(0,0,0,.45);
  }
  .nb-btn--send:hover { transform: translateY(-2px); box-shadow: 0 8px 26px rgba(0,0,0,.55); }
  .nb-btn--cancel {
    background: transparent;
    color: var(--quiet);
    border-color: var(--line);
  }
  .nb-btn--cancel:hover { color: var(--white); border-color: rgba(255,255,255,.3); }
  .nb-share__sent {
    display: none;
    border-top: 1px solid var(--line);
    margin-top: 16px;
    padding-top: 18px;
    align-items: center;
    gap: 12px;
    font-family: Inter, sans-serif;
    font-size: 15px;
    color: var(--verified);
  }
  .nb-share__sent.is-open { display: flex; }
  .nb-share__sent .nb-share__actions { margin-left: auto; }
</style>

<div class="nb-share" id="nbShare">
  <p class="nb-share__kicker">Share</p>
  <h3 class="nb-share__title">Share this Smart Note</h3>
  <div id="nbDestList" role="listbox" aria-label="Choose a destination">
    <button class="nb-share__dest" role="option" aria-selected="false" data-dest="Hub Feed">
      <span class="nb-share__icon" aria-hidden="true">
        <svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 3v18M3 12h18"/></svg>
      </span>
      <span><span class="nb-share__name">Hub Feed</span>
        <span class="nb-share__hint">Public lane — visible to the network</span></span>
    </button>
    <button class="nb-share__dest" role="option" aria-selected="false" data-dest="Room">
      <span class="nb-share__icon" aria-hidden="true">
        <svg viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" rx="3"/><path d="M4 10h16M10 10v10"/></svg>
      </span>
      <span><span class="nb-share__name">Room</span>
        <span class="nb-share__hint">A space you belong to</span></span>
    </button>
    <button class="nb-share__dest" role="option" aria-selected="false" data-dest="Person">
      <span class="nb-share__icon" aria-hidden="true">
        <svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="4"/><path d="M4 20c1.5-4 5-6 8-6s6.5 2 8 6"/></svg>
      </span>
      <span><span class="nb-share__name">Person</span>
        <span class="nb-share__hint">Direct — only they see it</span></span>
    </button>
  </div>
  <div class="nb-share__confirm" id="nbConfirm" aria-live="polite">
    <p class="nb-share__question">Send to <strong id="nbConfirmDest">Hub Feed</strong>?</p>
    <div class="nb-share__actions">
      <button class="nb-btn nb-btn--send" id="nbSendBtn">Send</button>
      <button class="nb-btn nb-btn--cancel" id="nbCancelBtn">Cancel</button>
    </div>
  </div>
  <div class="nb-share__sent" id="nbSent" aria-live="polite">
    <span id="nbSentMsg">✓ Shared to Hub Feed</span>
    <div class="nb-share__actions">
      <button class="nb-btn nb-btn--cancel" id="nbResetBtn">Done</button>
    </div>
  </div>
</div>

<script>
(function () {
  var destList = document.getElementById('nbDestList');
  var confirmEl = document.getElementById('nbConfirm');
  var confirmDest = document.getElementById('nbConfirmDest');
  var sentEl = document.getElementById('nbSent');
  var sentMsg = document.getElementById('nbSentMsg');
  var sendBtn = document.getElementById('nbSendBtn');
  var cancelBtn = document.getElementById('nbCancelBtn');
  var resetBtn = document.getElementById('nbResetBtn');
  var destBtns = destList.querySelectorAll('.nb-share__dest');
  var selected = null;
  function clearSelection() {
    selected = null;
    destBtns.forEach(function (b) {
      b.classList.remove('is-selected');
      b.setAttribute('aria-selected', 'false');
    });
    confirmEl.classList.remove('is-open');
  }
  destBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      sentEl.classList.remove('is-open');
      clearSelection();
      selected = btn.getAttribute('data-dest');
      btn.classList.add('is-selected');
      btn.setAttribute('aria-selected', 'true');
      confirmDest.textContent = selected;
      confirmEl.classList.add('is-open');
      sendBtn.focus();
    });
  });
  sendBtn.addEventListener('click', function () {
    if (!selected) return;
    sentMsg.textContent = '✓ Shared to ' + selected;
    confirmEl.classList.remove('is-open');
    sentEl.classList.add('is-open');
  });
  cancelBtn.addEventListener('click', clearSelection);
  resetBtn.addEventListener('click', function () {
    sentEl.classList.remove('is-open');
    clearSelection();
  });
})();
</script>
```
