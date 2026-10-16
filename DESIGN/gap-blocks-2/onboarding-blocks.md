# ONBOARDING BLOCKS — the family

The warehouse had no onboarding pieces. Shawn said do it. Three blocks, one
family, one law order. **Laws cited:** ALIVE (Law 1) — every reachable node
lifts and ignites; the current step breathes; the welcome board is a warm
front door. SPECTRUM (Law 2) — the 5-stop strip walks the steps in law order,
meaning never changes between blocks. ELEVATION (Law 3) — the welcome board
rides the field, nodes ride above the thread, the ring rides its own board.
TYPE (Law 6) — serif voice on step names and headlines, white 99%.

**The family laws:** each step earns the next — progress is real, never
theater. One job per step, one CTA per card. Honest percentages. Celebration
with restraint: one ignition, then calm.

**The step-color walk — fixed for the whole flow:**

| Stop | Hex | Step job |
|---|---|---|
| magenta | `#e84fff` | 1 · Meet — the living edge, the hello |
| purple | `#a06bff` | 2 · Choose — choosing intelligence |
| blue | `#3fb8ff` | 3 · Connect — knowledge moving |
| green | `#2fe89e` | 4 · Grow — alive and well |
| gold | `#ffbf3d` | 5 · Ignite — attention, earned: the moment it lights up |

A sixth step takes orange `#ff9a5a`, a seventh takes red `#ff5e6c` —
continuing the wheel, never reusing a stop while one sits unused. Gold is
gold, never yellow — the wheel carries gold and gold only.

**Family token sheet** (every snippet below assumes these; copy once):

```css
.onb{--ground:#050507;--ink:#fff;--magenta:#e84fff;--purple:#a06bff;
--indigo:#6675ff;--blue:#3fb8ff;--emerald:#35e0a1;--green:#2fe89e;
--lime:#b8ee57;--gold:#ffbf3d;--orange:#ff9a5a;--red:#ff5e6c;--pink:#ed58cd;
--ease:cubic-bezier(.16,.84,.22,1);--serif:Georgia,'Times New Roman',serif;
background:var(--ground);color:var(--ink)}
```

---

## ONB-001 · Stepper

The multi-step progress rail: five jewel nodes (done / current / locked), a
spectrum thread behind them that fills as you advance, one job named per
step, skippable steps marked honestly "optional." Law 1: reachable nodes
lift and ignite in their own step color; the current node breathes. A locked
step is dim and truly inert — it never fakes being clickable. Never a wall
of forms: the rail shows the journey, each step carries exactly one job.

### The code

```html
<style>
.onb-rail{position:relative;max-width:920px;margin:0 auto;padding:34px 6px 4px}
.onb-thread{position:absolute;top:58px;left:10%;right:10%;height:4px;border-radius:4px;
background:#141318;border:1px solid rgba(255,255,255,.14);box-shadow:inset 0 1px 3px rgba(0,0,0,.7)}
.onb-fill{position:absolute;top:-1px;bottom:-1px;left:-1px;width:50%;border-radius:4px;
background:linear-gradient(90deg,#e84fff,#a06bff,#3fb8ff,#2fe89e,#ffbf3d);
box-shadow:0 0 18px rgba(160,107,255,.6);transition:width .5s cubic-bezier(.16,.84,.22,1)}
.onb-steps{list-style:none;margin:0;padding:0;display:flex;justify-content:space-between;position:relative}
.onb-step{width:20%;text-align:center;transition:transform .18s cubic-bezier(.16,.84,.22,1)}
.onb-node{width:48px;height:48px;transform:rotate(45deg);border-radius:12px;
border:1.5px solid rgba(255,255,255,.85);cursor:pointer;display:grid;place-items:center;margin:0 auto;
background:radial-gradient(circle at 35% 30%,#fff,var(--sc) 45%,#050507 92%);
box-shadow:0 0 14px -4px var(--sc),inset 0 2px 3px rgba(255,255,255,.35);
transition:box-shadow .18s cubic-bezier(.16,.84,.22,1),border-color .18s,filter .18s}
.onb-node .in{transform:rotate(-45deg);display:grid;place-items:center;
font-family:Georgia,serif;font-size:17px;font-weight:700;color:#fff;text-shadow:0 1px 4px rgba(0,0,0,.8)}
.onb-node .in svg{width:20px;height:20px}
.onb-step:hover .onb-node{box-shadow:0 0 34px var(--sc),inset 0 2px 3px rgba(255,255,255,.35);border-color:#fff}
.onb-step:hover{transform:translateY(-2px)}
.onb-node:active{filter:brightness(1.25)}
.onb-node:focus-visible{outline:2px solid #fff;outline-offset:6px}
.onb-step.is-current .onb-node{box-shadow:0 0 40px var(--sc),inset 0 2px 4px rgba(255,255,255,.4);
border-color:#fff;animation:onb-node-breathe 3s ease-in-out infinite}
@keyframes onb-node-breathe{0%,100%{box-shadow:0 0 32px var(--sc)}50%{box-shadow:0 0 52px var(--sc)}}
.onb-step.is-locked .onb-node{background:#0a0a0e;box-shadow:none;cursor:not-allowed;opacity:.34}
.onb-step.is-locked .onb-node .in{color:#fff;opacity:.7}
.onb-step.is-locked:hover{transform:none}
.onb-step.is-locked:hover .onb-node{box-shadow:none;border-color:rgba(255,255,255,.85)}
.onb-label{margin-top:16px;padding:0 6px}
.onb-label .k{display:block;font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:#fff;opacity:.6}
.onb-label .t{display:block;font-family:Georgia,serif;font-size:16px;color:#fff;margin:5px 0 4px;
text-shadow:0 2px 8px rgba(0,0,0,.8)}
.onb-label .s{display:inline-flex;align-items:center;font-size:12px;color:#fff;opacity:.85}
.onb-label .s::before{content:"";width:7px;height:7px;transform:rotate(45deg);background:var(--sc);
box-shadow:0 0 8px var(--sc);margin-right:8px;flex:none}
.onb-step.is-locked .onb-label .s::before{background:#555;box-shadow:none}
.onb-opt{display:inline-block;margin-top:8px;font-size:10px;letter-spacing:.22em;text-transform:uppercase;
color:var(--sc);border:1px solid var(--sc);border-radius:999px;padding:3px 10px;background:rgba(0,0,0,.4)}
.onb-job{display:block;margin-top:8px;font-size:12px;color:#fff;opacity:.6;line-height:1.5}
.onb-no-steps{max-width:520px;margin:0 auto;text-align:center;padding:52px 24px;background:#0a0a0e;
border:1.5px solid rgba(255,255,255,.28);border-radius:18px}
.onb-no-steps .jewel{width:30px;height:30px;margin:0 auto 16px;transform:rotate(45deg);border-radius:8px;
background:#141318;border:1.5px solid rgba(255,255,255,.4)}
.onb-no-steps h3{font-family:Georgia,serif;font-size:19px;color:#fff;margin:0 0 8px}
.onb-no-steps p{font-size:14px;color:#fff;opacity:.8;margin:0}
@media (prefers-reduced-motion:reduce){.onb-step.is-current .onb-node{animation:none}.onb-step,.onb-node,.onb-fill{transition:none}}
</style>
<div class="onb onb-rail" id="onbRail">
  <div class="onb-thread" aria-hidden="true"><div class="onb-fill"></div></div>
  <ol class="onb-steps" aria-label="Setup steps">
    <li class="onb-step is-done" style="--sc:#e84fff">
      <button class="onb-node" aria-label="Step 1 done: Meet Naya"><span class="in"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12.5l5 5L20 6.5" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg></span></button>
      <div class="onb-label"><span class="k">Step 1</span><span class="t">Meet Naya</span><span class="s">Done</span>
        <span class="onb-job">One job: say hello.</span></div>
    </li>
    <li class="onb-step is-done" style="--sc:#a06bff">
      <button class="onb-node" aria-label="Step 2 done: Choose your path"><span class="in"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12.5l5 5L20 6.5" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg></span></button>
      <div class="onb-label"><span class="k">Step 2</span><span class="t">Choose your path</span><span class="s">Done</span>
        <span class="onb-job">One job: pick what this is for.</span></div>
    </li>
    <li class="onb-step is-current" style="--sc:#3fb8ff" aria-current="step">
      <button class="onb-node" aria-label="Step 3 current: Add your team, optional"><span class="in">3</span></button>
      <div class="onb-label"><span class="k">Step 3</span><span class="t">Add your team</span><span class="s">You are here</span><br>
        <span class="onb-opt">Optional</span>
        <span class="onb-job">One job: invite people — or skip it.</span></div>
    </li>
    <li class="onb-step is-locked" style="--sc:#2fe89e">
      <button class="onb-node" disabled aria-disabled="true" aria-label="Step 4 locked: Set your rhythm"><span class="in">4</span></button>
      <div class="onb-label"><span class="k">Step 4</span><span class="t">Set your rhythm</span><span class="s">Locked</span>
        <span class="onb-job">One job: choose your pace.</span></div>
    </li>
    <li class="onb-step is-locked" style="--sc:#ffbf3d">
      <button class="onb-node" disabled aria-disabled="true" aria-label="Step 5 locked: Light the feed"><span class="in">5</span></button>
      <div class="onb-label"><span class="k">Step 5</span><span class="t">Light the feed</span><span class="s">Locked</span>
        <span class="onb-job">One job: send your first note.</span></div>
    </li>
  </ol>
</div>

<div class="onb onb-rail is-empty" aria-label="No steps example" style="margin-top:8px">
  <div class="onb-no-steps">
    <div class="jewel" aria-hidden="true"></div>
    <h3>No steps yet</h3>
    <p>The flow hasn't been built — so there's nothing to walk. This is not step zero of five.</p>
  </div>
</div>
<script>
(function(){
  const rail=document.getElementById('onbRail');
  if(!rail||rail.classList.contains('is-empty'))return;
  const steps=[...rail.querySelectorAll('.onb-step')];
  const fill=rail.querySelector('.onb-fill');
  const check='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12.5l5 5L20 6.5" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  function state(i,cur){return i<cur?'done':(i===cur?'current':'locked');}
  function render(){
    const cur=steps.findIndex(s=>s.classList.contains('is-current'));
    fill.style.width=(cur/(steps.length-1)*100)+'%';
    steps.forEach((s,i)=>{
      const st=state(i,cur),b=s.querySelector('.onb-node'),title=s.querySelector('.t').textContent;
      s.classList.toggle('is-done',st==='done');
      s.classList.toggle('is-current',st==='current');
      s.classList.toggle('is-locked',st==='locked');
      b.disabled=(st==='locked');
      if(st==='locked')b.setAttribute('aria-disabled','true');else b.removeAttribute('aria-disabled');
      b.querySelector('.in').innerHTML=(st==='done')?check:String(i+1);
      b.setAttribute('aria-label','Step '+(i+1)+' '+st+': '+title);
      s.querySelector('.s').textContent=st==='done'?'Done':(st==='current'?'You are here':'Locked');
      if(st==='current')s.setAttribute('aria-current','step');else s.removeAttribute('aria-current');
    });
  }
  steps.forEach((s,i)=>{
    s.querySelector('.onb-node').addEventListener('click',()=>{
      const cur=steps.findIndex(x=>x.classList.contains('is-current'));
      if(i<=cur){steps[cur].classList.remove('is-current');steps[i].classList.add('is-current');render();}
    });
  });
  render();
})();
</script>
```

The thread fill is derived from the current step's real index — `width`
recomputes on every render, never hardcoded per story. A specimen freezes it;
a live build moves it.

### States

- **Rest:** dark thread, jewel nodes in their step color (white → tone → black
  facet), serif step titles, white 99%.
- **Hover (reachable):** the step lifts 2px, its node ignites in its own step
  color. Done steps are revisit buttons — hovering promises "go back," and
  clicking does.
- **Active/press:** the node brightens (`filter:brightness(1.25)`) — it feels
  held.
- **Current:** held ignition in the step's own color + a slow 3s breathe. The
  "You are here" marker carries a jewel dot in the step color. Only one
  current step ever exists.
- **Locked:** 34% opacity, `disabled` + `aria-disabled`, out of tab order,
  no hover lift, no glow. Dimmed because it *is* unreachable — the next step
  is earned, not previewed.
- **Empty:** no steps configured renders an honest panel — "No steps yet" —
  never a rail of fake placeholder nodes.

### Do / Don't

**Do** mark skippable steps with a plain "Optional" chip and give the step's
own content an honest "Skip this step" control — skipping is a first-class
choice, not a hidden shame. **Don't** unlock all steps "for preview": a
locked step you can peek into teaches the user that locks are theater, and
then nothing in the flow is trusted.

### Anatomy

- **Thread:** the journey line — dark track, spectrum-strip fill in the
  5-stop law order. The fill is the walked spectrum; it never runs backward.
- **Node jewel:** the rotated diamond, white → step-color → black, own-color
  glow. Done shows a drawn check (Law 4 — icons are drawn); current shows the
  number and breathes; locked shows the number at 34%.
- **Label stack:** kicker (Step N, letterspaced), serif title, status with a
  jewel dot in the step color — the dot is information, not decoration.
- **Optional chip:** letterspaced, in the step's own color. Optional is a
  promise: this step can be skipped and the flow still completes.
- **One job:** each step names its single job in one line. A step with two
  jobs is two steps — split it.

**What it will NOT fake:** it never fills the thread past the current step —
a full thread on step 2 of 5 is a lie. Locked steps never respond to hover;
the rail never renders more nodes than the flow has; the "You are here"
marker sits on exactly one step. Skipping is real: an optional step skipped
advances the flow honestly, it is not silently "completed."

---
## ONB-002 · Welcome card

The first-run greeting board: Naya's face and her energy — light with a
face, drawn, never a stock avatar — one warm line in her voice, and exactly
one clear next action. Law 3: the board rides the field with the full
5-layer shadow; it is a warm front door. Personal without creepy: the card
knows only what the user gave it. No name known, no name used — the
specimen below shows the honest nameless state.

### The code

```html
<style>
.onb-welcome{max-width:640px;margin:0 auto;text-align:center;padding:44px 38px 34px;
background:linear-gradient(180deg,#1a171f,#09090d 60%,#030304);
border:1.5px solid rgba(255,255,255,.3);border-radius:24px;
box-shadow:inset 0 2px 2px rgba(255,255,255,.12),inset 0 -8px 18px rgba(0,0,0,.55),
0 5px 0 #020203,0 35px 75px rgba(0,0,0,.7),0 0 40px -17px rgba(160,107,255,.35);
transition:transform .28s cubic-bezier(.16,.84,.22,1),border-color .28s,box-shadow .28s}
.onb-welcome:hover{transform:translateY(-5px);border-color:#a06bff;
box-shadow:inset 0 2px 2px rgba(255,255,255,.12),inset 0 -8px 18px rgba(0,0,0,.55),
0 5px 0 #020203,0 40px 80px rgba(0,0,0,.7),0 0 52px -14px rgba(160,107,255,.55)}
.onb-face{width:104px;height:104px;margin:0 auto 22px;position:relative}
.onb-face svg{width:100%;height:100%;display:block;filter:drop-shadow(0 0 22px rgba(160,107,255,.65))}
.onb-face::after{content:"";position:absolute;inset:-16px;border-radius:50%;pointer-events:none;
background:radial-gradient(circle,rgba(160,107,255,.22),transparent 70%);
animation:onb-halo 5s ease-in-out infinite}
@keyframes onb-halo{0%,100%{opacity:.6;transform:scale(1)}50%{opacity:1;transform:scale(1.06)}}
.onb-kicker{font-size:12px;letter-spacing:.24em;text-transform:uppercase;color:#fff;opacity:.65}
.onb-hello{font-family:Georgia,'Times New Roman',serif;font-size:32px;color:#fff;margin:12px 0 10px;
text-shadow:0 2px 8px rgba(0,0,0,.8),0 0 22px rgba(255,255,255,.14)}
.onb-line{font-size:15px;line-height:1.7;color:#fff;opacity:.92;max-width:44ch;margin:0 auto 28px}
.onb-cta{min-height:52px;padding:0 36px;font-size:16px;font-weight:600;border-radius:14px;
background:#050505;color:#fff;border:1.5px solid rgba(255,255,255,.85);cursor:pointer;
display:inline-flex;align-items:center;gap:10px;
box-shadow:inset 0 2px 2px rgba(255,255,255,.12),0 12px 28px rgba(0,0,0,.6);
transition:transform .18s cubic-bezier(.16,.84,.22,1),border-color .18s,box-shadow .18s}
.onb-cta svg{width:18px;height:18px;stroke:#fff;fill:none;stroke-width:2;flex:none}
.onb-cta:hover{transform:translateY(-2px);border-color:#a06bff;box-shadow:0 0 32px rgba(160,107,255,.6),0 14px 30px rgba(0,0,0,.6)}
.onb-cta:active{transform:translateY(1px)}
.onb-cta:focus-visible{outline:2px solid #fff;outline-offset:3px}
.onb-quiet{display:inline-block;margin-top:18px;font-size:13px;color:#fff;opacity:.65;text-decoration:none;
border-bottom:1px solid rgba(255,255,255,.25);padding-bottom:2px;transition:opacity .18s,border-color .18s}
.onb-quiet:hover{opacity:1;border-color:#a06bff}
.onb-knows{margin:24px 0 0;font-size:11px;letter-spacing:.06em;color:#fff;opacity:.5}
@media (prefers-reduced-motion:reduce){.onb-face::after{animation:none}.onb-welcome,.onb-cta{transition:none}}
</style>
<article class="onb onb-welcome" id="onbWelcome" aria-label="Welcome">
  <div class="onb-face" aria-hidden="true">
    <svg viewBox="0 0 120 120">
      <defs>
        <radialGradient id="onbFaceGlow" cx="50%" cy="38%" r="65%">
          <stop offset="0%" stop-color="#ffffff"/>
          <stop offset="45%" stop-color="#a06bff"/>
          <stop offset="100%" stop-color="#050507"/>
        </radialGradient>
      </defs>
      <circle cx="60" cy="60" r="46" fill="url(#onbFaceGlow)" stroke="rgba(255,255,255,.8)" stroke-width="1.5"/>
      <circle cx="45" cy="54" r="5" fill="#0a0a0e"/>
      <circle cx="75" cy="54" r="5" fill="#0a0a0e"/>
      <circle cx="46.5" cy="52.5" r="1.6" fill="#fff" opacity=".9"/>
      <circle cx="76.5" cy="52.5" r="1.6" fill="#fff" opacity=".9"/>
      <path d="M46 74 Q60 84 74 74" stroke="#0a0a0e" stroke-width="4" fill="none" stroke-linecap="round"/>
    </svg>
  </div>
  <p class="onb-kicker">First run</p>
  <h2 class="onb-hello">Welcome<span data-onb-name></span>.</h2>
  <p class="onb-line">I'm Naya — your intelligence, at your side. Give me five
  small steps and I'll learn how you work. No forms wall, no maze.</p>
  <button class="onb-cta" type="button">
    <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
    Begin the tour
  </button><br>
  <a class="onb-quiet" href="#">I'll explore on my own</a>
  <p class="onb-knows">This card knows only what you've told it — nothing more.</p>
</article>
<script>
(function(){
  const card=document.getElementById('onbWelcome');
  const name=(card.dataset.name||'').trim();
  if(name){card.querySelector('[data-onb-name]').textContent=', '+name;}
})();
</script>
```

Set `data-name` on the article when the app knows the user's name — the
script fills the greeting from it and from nothing else. The specimen above
carries no `data-name`, so it greets without one: the honest default.

### States

- **Rest:** the board on its 5-layer shadow; Naya's face lit from within with
  a slow 5s halo breathe — presence, not decoration.
- **Hover:** the board lifts 5px and ignites chrome-purple (it is chrome, so
  it burns chrome's color). The CTA lifts 2px and ignites purple with it.
- **Active/press:** the CTA settles 1px — it feels held.
- **Focus:** white 2px ring on the CTA — keyboard users get the same
  ignition promise.
- **Quiet exit:** "I'll explore on my own" — 65% opacity, underline only on
  intent. It is an exit, not a competing CTA: no lift, no glow, no color.
- **Nameless (default):** "Welcome." — full sentence, no placeholder, no
  "there," no invented name. Named state only ever renders a name the user
  gave.

### Do / Don't

**Do** keep exactly one primary CTA — the card has one job: get the user to
the first step. **Don't** add a second bright button "just in case," and
never three competing CTAs; every extra button halves the chance the user
presses any of them.

### Anatomy

- **Naya's face:** drawn SVG — lit orb (white → purple → black), two eyes
  with catchlights, one calm arc. A face *and* energy: the halo breathe is
  the energy. Never an emoji, never a stock avatar, never just a logo.
- **Kicker:** "First run," letterspaced — it names the moment honestly.
- **Headline:** serif voice, 32px. The name slot fills only from
  `data-name`; the template never invents one.
- **One line:** 15px, 1.7 line-height, max 44ch — warm, plain words, one
  promise. Not a paragraph of features.
- **The one CTA:** 52px, black center, white rim, drawn arrow glyph — the
  canonical button DNA. It says where it goes ("Begin the tour"), not "Get
  started."
- **The quiet exit:** a text link for the explorer. Present but never
  competing.
- **The honesty footnote:** "This card knows only what you've told it."
  Part of the block, not documentation — it is the personal-without-creepy
  contract, stated where the user can see it.

**What it will NOT fake:** it never greets by a name it wasn't given — no
"Welcome, friend," no mail-merged guess from an email local-part. It never
claims the tour is "quick" unless the flow really is five small steps. The
face is drawn geometry, not a photo of a person who doesn't exist.

---

## ONB-003 · Progress indicator

Progress as honest truth: a linear bar and a ring variant, the percent as a
real number from real work, and a celebration state that fires exactly one
ignition and then goes calm. Law 1: numbers breathe — no static numbers on
screen. The specimen freezes 62%; a live build binds the number to the
work and nothing else.

### The code

```html
<style>
.onb-prog{max-width:520px;margin:0 auto;background:linear-gradient(180deg,#141318,#08080c);
border:1.5px solid rgba(255,255,255,.3);border-radius:20px;padding:26px 28px;
box-shadow:inset 0 2px 2px rgba(255,255,255,.1),0 12px 30px rgba(0,0,0,.6);
transition:transform .28s cubic-bezier(.16,.84,.22,1),border-color .28s,box-shadow .28s}
.onb-prog:hover{transform:translateY(-3px);border-color:rgba(255,255,255,.55);
box-shadow:inset 0 2px 2px rgba(255,255,255,.1),0 16px 36px rgba(0,0,0,.65),0 0 30px -10px rgba(160,107,255,.5)}
.onb-prog-top{display:flex;align-items:baseline;justify-content:space-between;margin-bottom:14px}
.onb-prog-top .lbl{font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:#fff;opacity:.7}
.onb-pct{font-family:Georgia,serif;font-size:30px;color:#fff;text-shadow:0 2px 8px rgba(0,0,0,.8);
animation:onb-num-breathe 4s ease-in-out infinite}
.onb-pct small{font-size:15px;opacity:.7}
@keyframes onb-num-breathe{0%,100%{opacity:1}50%{opacity:.82}}
.onb-bar{height:12px;border-radius:999px;background:#0a0a0e;border:1px solid rgba(255,255,255,.18);
box-shadow:inset 0 2px 5px rgba(0,0,0,.8);overflow:hidden}
.onb-fillbar{height:100%;width:62%;border-radius:999px;
background:linear-gradient(90deg,#e84fff,#a06bff,#3fb8ff,#2fe89e,#ffbf3d);
box-shadow:0 0 16px rgba(160,107,255,.55);transition:width .6s cubic-bezier(.16,.84,.22,1)}
.onb-sub{font-size:13px;color:#fff;opacity:.75;margin:12px 0 0;letter-spacing:.03em}
/* ring variant */
.onb-ringwrap{position:relative;width:168px;height:168px;margin:0 auto}
.onb-ring{width:100%;height:100%;transform:rotate(0deg);transition:transform .28s cubic-bezier(.16,.84,.22,1)}
.onb-ringwrap:hover .onb-ring{filter:drop-shadow(0 0 14px rgba(160,107,255,.55))}
.ring-track{fill:none;stroke:#0a0a0e;stroke-width:11}
.ring-prog{fill:none;stroke:url(#onbRingGrad);stroke-width:11;stroke-linecap:round;
transition:stroke-dashoffset .6s cubic-bezier(.16,.84,.22,1);filter:drop-shadow(0 0 6px rgba(160,107,255,.6))}
.onb-ring-num{position:absolute;inset:0;display:grid;place-content:center;text-align:center}
.onb-ring-num b{font-family:Georgia,serif;font-size:34px;font-weight:400;color:#fff;
text-shadow:0 2px 8px rgba(0,0,0,.8);animation:onb-num-breathe 4s ease-in-out infinite}
.onb-ring-num b small{font-size:16px;opacity:.7}
.onb-ring-num span{display:block;font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:#fff;opacity:.6;margin-top:4px}
/* complete: one ignition, then calm */
.onb-prog.is-complete{border-color:#ffbf3d;animation:onb-celebrate 1.1s cubic-bezier(.16,.84,.22,1) 1}
.onb-prog.is-complete .onb-fillbar{width:100%;background:#ffbf3d;box-shadow:0 0 22px rgba(255,191,61,.7)}
.onb-prog.is-complete .onb-pct{animation:none;color:#ffbf3d}
.onb-ringwrap.is-complete .ring-prog{stroke:#ffbf3d;stroke-dashoffset:0;filter:drop-shadow(0 0 10px rgba(255,191,61,.8))}
.onb-ringwrap.is-complete .onb-ring-num b{animation:none;color:#ffbf3d}
.onb-ringwrap.is-complete{animation:onb-celebrate 1.1s cubic-bezier(.16,.84,.22,1) 1}
@keyframes onb-celebrate{0%{box-shadow:0 0 0 rgba(255,191,61,0)}30%{box-shadow:0 0 80px rgba(255,191,61,.9)}100%{box-shadow:0 0 26px rgba(255,191,61,.4)}}
/* indeterminate: honest about not knowing */
.onb-prog.is-ind .onb-fillbar{width:34%;background:linear-gradient(90deg,transparent,#a06bff,transparent);
box-shadow:0 0 16px rgba(160,107,255,.6);animation:onb-drift 2.2s ease-in-out infinite}
@keyframes onb-drift{0%{margin-left:-34%}100%{margin-left:100%}}
.onb-prog.is-ind .onb-pct{animation:none;font-size:20px}
@media (prefers-reduced-motion:reduce){.onb-pct,.onb-ring-num b{animation:none}.onb-prog.is-complete,.onb-ringwrap.is-complete{animation:none}.onb-prog.is-ind .onb-fillbar{animation:none}.onb-prog,.onb-fillbar,.ring-prog{transition:none}}
</style>
<div class="onb onb-prog">
  <div class="onb-prog-top"><span class="lbl">Getting set up</span><span class="onb-pct">62<small>%</small></span></div>
  <div class="onb-bar" role="progressbar" aria-valuenow="62" aria-valuemin="0" aria-valuemax="100" aria-label="Setup progress"><div class="onb-fillbar"></div></div>
  <p class="onb-sub">5 of 8 done — the count is real.</p>
</div>

<div class="onb onb-ringwrap" style="margin-top:28px" role="progressbar" aria-valuenow="62" aria-valuemin="0" aria-valuemax="100" aria-label="Setup progress, ring">
  <svg class="onb-ring" viewBox="0 0 120 120" aria-hidden="true">
    <defs>
      <linearGradient id="onbRingGrad" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#e84fff"/><stop offset="28%" stop-color="#a06bff"/>
        <stop offset="52%" stop-color="#3fb8ff"/><stop offset="76%" stop-color="#2fe89e"/>
        <stop offset="100%" stop-color="#ffbf3d"/>
      </linearGradient>
    </defs>
    <circle class="ring-track" cx="60" cy="60" r="54"/>
    <circle class="ring-prog" cx="60" cy="60" r="54" stroke-dasharray="339.29" stroke-dashoffset="128.93" transform="rotate(-90 60 60)"/>
  </svg>
  <div class="onb-ring-num"><b>62<small>%</small></b><span>complete</span></div>
</div>

<div class="onb onb-prog is-complete" style="margin-top:28px">
  <div class="onb-prog-top"><span class="lbl">Getting set up</span><span class="onb-pct">100<small>%</small></span></div>
  <div class="onb-bar" role="progressbar" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100" aria-label="Setup progress, complete"><div class="onb-fillbar"></div></div>
  <p class="onb-sub">All 8 done. You're in.</p>
</div>

<div class="onb onb-prog is-ind" style="margin-top:28px">
  <div class="onb-prog-top"><span class="lbl">Syncing your world</span><span class="onb-pct">No number yet</span></div>
  <div class="onb-bar"><div class="onb-fillbar"></div></div>
  <p class="onb-sub">Progress arrives as the work reports it — this bar won't invent a percent.</p>
</div>
```

The 62% is a frozen teaching state: the linear bar's `.onb-fillbar` width,
the ring's `stroke-dashoffset` (`339.29 × (1 − 0.62) = 128.93`), the serif
number, and `aria-valuenow` all say the same number. A live build sets all
four from the same source of truth — or it doesn't render the block.

### States

- **Rest:** dark board, serif percent breathing on a 4s loop (numbers
  breathe — no static numbers), strip-gradient fill, honest sub-count.
- **Hover:** the board lifts 3px; the ring answers with a soft glow (no
  lift — it is a readout, not a button; secondary elements may glow without
  lifting).
- **Zero:** 0%, empty bar, "Ready when you are." Zero is a real state, not a
  hidden one.
- **Complete:** `.is-complete` fires exactly one 1.1s gold ignition on the
  board/ring, then settles: gold edge, gold 100%, number stops breathing.
  Gold = attention, earned — the finish line wears gold, and only the finish
  line.
- **Indeterminate (honest):** when the work genuinely can't report a number,
  a soft spectrum drift crosses the bar and the label says "No number yet"
  in plain words. It never parks at 99% and never invents 47%.
- **Reduced motion:** ignition, breathe, and drift all stop. 100% still
  reads 100% — the meaning survives without the motion.

### Do / Don't

**Do** derive the number, the fill width, the ring offset, and
`aria-valuenow` from one source — four mouths, one truth. **Don't** stall at
99% while work finishes (theater), don't ease a fake 0→100 on load (the
number must mean completed work), and don't celebrate twice: re-adding
`.is-complete` to re-fire the ignition is confetti with extra steps.

### Anatomy

- **Label row:** uppercase letterspaced job ("Getting set up") + serif
  percent. The percent is the headline of this block — set it in the voice.
- **Linear bar:** 12px track, inset shadow, strip-gradient fill in law
  order. The fill *is* the walked spectrum; at 100% it resolves to gold.
- **Ring:** 168px SVG, 11px stroke, gradient walked around the path,
  round cap, start at twelve o'clock. The number sits in the middle in
  serif — the ring frames the truth, it doesn't decorate it.
- **Sub-count:** "5 of 8 done" — the percent's receipt. If the count isn't
  known, the sub-line says so instead of inventing one.
- **Celebration:** one ignition (`onb-celebrate`, 1.1s, once), then calm.
  Restraint is the whole design: the moment lands, the glow settles, and the
  user gets on with their day. No confetti, no particle spam, no encore.

**What it will NOT fake:** the percent is completed work over total work —
never time elapsed, never a guess, never "almost there" parked at 99%.
The ring's `stroke-dashoffset` is computed from the same number the label
shows; a mismatch is a bug, not a style choice. The indeterminate state is
only for genuinely unmeasurable work — a measurable job shown as
indeterminate is honesty theater. `.is-complete` is added once, when the
backend confirms 100% — the animation firing is the receipt that the work
is done.

---

## Family notes

- **One meaning per color, everywhere:** the family table at the top is the
  contract. A magenta node in ONB-001, the magenta end of ONB-003's strip,
  and ONB-002's chrome-purple ignition all draw from the same wheel. Step 5
  and the finish line both wear gold — "attention, earned" is a single
  meaning, not a reuse.
- **Progress is the family's only special effect:** the stepper's thread,
  the welcome board's halo, the indicator's breathe and single ignition.
  Nothing else moves. A family that animates everything celebrates nothing.
- **What the family does not cover:** branching conditional flows
  (step 3a vs 3b), skip-to-end fast paths, streak rewards, and gamified
  badges are real needs and are *not* specified here — they are future
  blocks (ONB-004+), not implied features of these three. Nothing in these
  specs pretends they exist.
