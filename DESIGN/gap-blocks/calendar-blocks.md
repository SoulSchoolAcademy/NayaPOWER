# CALENDAR BLOCKS — the family

The warehouse had no calendar pieces. Shawn said do it. Five blocks, one
family, one law order. **Laws cited:** ALIVE (Law 1) — every interactive cell
moves and ignites. SPECTRUM (Law 2) — event colors walk the wheel, meaning
never changes between blocks. ELEVATION (Law 3) — boards ride in layers.
TYPE (Law 6) — serif voice on headers, white 99%.

**The event-color walk — fixed forever, across all five blocks:**

| Stop | Hex | Meaning |
|---|---|---|
| magenta | `#e84fff` | Celebrations & milestones — the living edge |
| purple | `#a06bff` | Deep work & focus — choosing intelligence |
| blue | `#3fb8ff` | Meetings & people — knowledge moving |
| green | `#2fe89e` | Health & body — alive and well |
| gold | `#ffbf3d` | Decisions & deadlines — attention, earned |

A sixth type takes orange `#ff9a5a`, a seventh takes red `#ff5e6c` —
continuing the wheel, never reusing a stop while one sits unused. Adjacent
pills in one cell always walk in this order. Gold is reserved: today wears
gold, and only today.

**Family token sheet** (every snippet below assumes these; copy once):

```css
.cal{--ground:#050507;--ink:#fff;--magenta:#e84fff;--purple:#a06bff;
--indigo:#6675ff;--blue:#3fb8ff;--emerald:#35e0a1;--green:#2fe89e;
--lime:#b8ee57;--gold:#ffbf3d;--orange:#ff9a5a;--red:#ff5e6c;--pink:#ed58cd;
--ease:cubic-bezier(.16,.84,.22,1);--serif:Georgia,'Times New Roman',serif;
background:var(--ground);color:var(--ink)}
```

---

## CAL-001 · Month-view board

A full month on black ground: serif weekday headers, day cells with
white-lit edges, today ignited in gold, event pills in wheel order. Law 1:
nothing dead — every in-month cell lifts and ignites; chevrons promise "go
somewhere" and do.

### The code

```html
<style>
.cal-month{max-width:980px;margin:0 auto;background:linear-gradient(180deg,#1a171f,#09090d 60%,#030304);
border:1.5px solid rgba(255,255,255,.3);border-radius:24px;padding:26px 26px 30px;
box-shadow:inset 0 2px 2px rgba(255,255,255,.12),inset 0 -8px 18px rgba(0,0,0,.55),
0 5px 0 #020203,0 35px 75px rgba(0,0,0,.7),0 0 40px -17px rgba(160,107,255,.35)}
.cal-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:18px}
.cal-title{font-family:Georgia,'Times New Roman',serif;font-size:24px;color:#fff;margin:0;letter-spacing:.02em;
text-shadow:0 2px 8px rgba(0,0,0,.8),0 0 22px rgba(255,255,255,.14)}
.cal-title small{font-size:14px;opacity:.75;font-family:system-ui,sans-serif;letter-spacing:.18em;text-transform:uppercase;margin-left:10px}
.cal-nav{display:flex;gap:10px}
.cal-chev{width:44px;height:44px;border-radius:50%;background:#050505;border:1.5px solid rgba(255,255,255,.85);
color:#fff;cursor:pointer;display:grid;place-items:center;transition:transform .18s cubic-bezier(.16,.84,.22,1),border-color .18s,box-shadow .18s}
.cal-chev i{width:10px;height:10px;border-top:2px solid #fff;border-right:2px solid #fff;transform:rotate(-135deg);margin-left:3px}
.cal-chev.next i{transform:rotate(45deg);margin-left:-3px}
.cal-chev:hover{transform:translateY(-2px);border-color:#a06bff;box-shadow:0 0 26px rgba(160,107,255,.55)}
.cal-chev:active{transform:translateY(1px)}
.cal-chev:focus-visible{outline:2px solid #fff;outline-offset:3px}
.cal-week{display:grid;grid-template-columns:repeat(7,1fr);gap:8px;margin-bottom:8px}
.cal-week span{font-family:Georgia,serif;font-size:14px;color:#fff;opacity:.92;text-align:center;padding:8px 0;letter-spacing:.14em;text-transform:uppercase}
.cal-grid{display:grid;grid-template-columns:repeat(7,1fr);gap:8px}
.cal-day{min-height:104px;background:#0a0a0e;border:1.5px solid rgba(255,255,255,.32);border-radius:14px;
padding:8px 8px 6px;cursor:pointer;position:relative;
transition:transform .18s cubic-bezier(.16,.84,.22,1),border-color .18s,box-shadow .18s}
.cal-day .dnum{font-family:Georgia,serif;font-size:18px;color:#fff}
.cal-day:hover{transform:translateY(-2px);border-color:#a06bff;box-shadow:0 0 26px rgba(160,107,255,.5)}
.cal-day.is-selected{border-color:#a06bff;box-shadow:0 0 32px rgba(160,107,255,.65),inset 0 0 18px rgba(160,107,255,.12);transform:translateY(-2px)}
.cal-day.is-today{border:2px solid #ffbf3d;box-shadow:0 0 34px rgba(255,191,61,.6),inset 0 0 20px rgba(255,191,61,.1);
animation:cal-breathe 4s ease-in-out infinite}
.cal-day.is-today .dnum{color:#ffbf3d}
@keyframes cal-breathe{0%,100%{box-shadow:0 0 30px rgba(255,191,61,.5)}50%{box-shadow:0 0 44px rgba(255,191,61,.75)}}
.cal-day.is-out{opacity:.34;min-height:104px}
.cal-day.is-out:hover{border-color:rgba(255,255,255,.7);box-shadow:none}
.cal-pill{display:flex;align-items:center;gap:6px;margin-top:6px;padding:4px 7px;border-radius:8px;
background:#050507;border:1px solid var(--pc);font-size:12px;color:#fff;white-space:nowrap;overflow:hidden;
transition:transform .18s cubic-bezier(.16,.84,.22,1),box-shadow .18s}
.cal-pill::before{content:"";width:7px;height:7px;transform:rotate(45deg);background:var(--pc);box-shadow:0 0 8px var(--pc);flex:none}
.cal-pill:hover{transform:translateY(-1px);box-shadow:0 0 22px var(--pc)}
.cal-pill .t{opacity:.7;font-size:11px}
.cal-dots{display:flex;gap:5px;margin-top:7px;padding:0 2px}
.cal-dots i{width:7px;height:7px;transform:rotate(45deg);background:var(--pc);box-shadow:0 0 7px var(--pc)}
.cal-more{display:inline-block;margin-top:6px;font-size:11px;letter-spacing:.08em;color:#fff;opacity:.75;
background:none;border:1px solid rgba(255,255,255,.35);border-radius:999px;padding:3px 10px;cursor:pointer;
transition:all .18s cubic-bezier(.16,.84,.22,1)}
.cal-more:hover{border-color:#a06bff;opacity:1;box-shadow:0 0 18px rgba(160,107,255,.5);transform:translateY(-1px)}
@media (prefers-reduced-motion:reduce){.cal-day.is-today{animation:none}.cal-day,.cal-chev,.cal-pill,.cal-more{transition:none}}
</style>
<div class="cal cal-month">
  <div class="cal-head">
    <h2 class="cal-title">October <small>2026</small></h2>
    <div class="cal-nav">
      <button class="cal-chev" aria-label="Previous month"><i></i></button>
      <button class="cal-chev next" aria-label="Next month"><i></i></button>
    </div>
  </div>
  <div class="cal-week" aria-hidden="true"><span>Mon</span><span>Tue</span><span>Wed</span><span>Thu</span><span>Fri</span><span>Sat</span><span>Sun</span></div>
  <div class="cal-grid" role="grid" aria-label="October 2026">
    <div class="cal-day is-out" role="gridcell" tabindex="0"><span class="dnum">28</span></div>
    <div class="cal-day is-out" role="gridcell" tabindex="0"><span class="dnum">29</span></div>
    <div class="cal-day is-out" role="gridcell" tabindex="0"><span class="dnum">30</span></div>
    <div class="cal-day" role="gridcell" tabindex="0"><span class="dnum">1</span>
      <div class="cal-pill" style="--pc:#a06bff"><span class="t">09:00</span>Deep work</div></div>
    <div class="cal-day" role="gridcell" tabindex="0"><span class="dnum">2</span></div>
    <div class="cal-day" role="gridcell" tabindex="0"><span class="dnum">3</span>
      <div class="cal-pill" style="--pc:#e84fff"><span class="t">18:00</span>Mara's party</div></div>
    <div class="cal-day" role="gridcell" tabindex="0"><span class="dnum">4</span></div>
    <div class="cal-day" role="gridcell" tabindex="0"><span class="dnum">5</span></div>
    <div class="cal-day" role="gridcell" tabindex="0"><span class="dnum">6</span>
      <div class="cal-pill" style="--pc:#3fb8ff"><span class="t">10:30</span>Design sync</div></div>
    <div class="cal-day" role="gridcell" tabindex="0"><span class="dnum">7</span></div>
    <div class="cal-day" role="gridcell" tabindex="0"><span class="dnum">8</span>
      <div class="cal-pill" style="--pc:#2fe89e"><span class="t">07:00</span>Run</div></div>
    <div class="cal-day" role="gridcell" tabindex="0"><span class="dnum">9</span></div>
    <div class="cal-day" role="gridcell" tabindex="0"><span class="dnum">10</span>
      <div class="cal-pill" style="--pc:#e84fff"><span class="t">all day</span>Anniversary</div></div>
    <div class="cal-day" role="gridcell" tabindex="0"><span class="dnum">11</span></div>
    <div class="cal-day" role="gridcell" tabindex="0"><span class="dnum">12</span></div>
    <div class="cal-day" role="gridcell" tabindex="0"><span class="dnum">13</span>
      <div class="cal-pill" style="--pc:#ffbf3d"><span class="t">17:00</span>Ship deadline</div></div>
    <div class="cal-day" role="gridcell" tabindex="0"><span class="dnum">14</span></div>
    <div class="cal-day" role="gridcell" tabindex="0"><span class="dnum">15</span>
      <div class="cal-pill" style="--pc:#3fb8ff"><span class="t">14:00</span>1:1 with Sam</div>
      <div class="cal-dots" aria-label="2 more events"><i style="--pc:#a06bff"></i><i style="--pc:#2fe89e"></i></div>
      <button class="cal-more">+2 more</button></div>
    <div class="cal-day is-today is-selected" role="gridcell" tabindex="0" aria-current="date"><span class="dnum">16</span>
      <div class="cal-pill" style="--pc:#a06bff"><span class="t">09:00</span>Deep work</div>
      <div class="cal-pill" style="--pc:#3fb8ff"><span class="t">10:30</span>Standup</div>
      <div class="cal-pill" style="--pc:#ffbf3d"><span class="t">15:00</span>Launch decision</div></div>
    <div class="cal-day" role="gridcell" tabindex="0"><span class="dnum">17</span></div>
    <div class="cal-day" role="gridcell" tabindex="0"><span class="dnum">18</span></div>
    <div class="cal-day" role="gridcell" tabindex="0"><span class="dnum">19</span></div>
    <div class="cal-day" role="gridcell" tabindex="0"><span class="dnum">20</span>
      <div class="cal-pill" style="--pc:#a06bff"><span class="t">3d →</span>Design sprint</div></div>
    <div class="cal-day" role="gridcell" tabindex="0"><span class="dnum">21</span>
      <div class="cal-pill" style="--pc:#a06bff"><span class="t">→</span>Sprint ctd.</div></div>
    <div class="cal-day" role="gridcell" tabindex="0"><span class="dnum">22</span>
      <div class="cal-pill" style="--pc:#a06bff"><span class="t">→ end</span>Sprint ends</div></div>
    <div class="cal-day" role="gridcell" tabindex="0"><span class="dnum">23</span></div>
    <div class="cal-day" role="gridcell" tabindex="0"><span class="dnum">24</span>
      <div class="cal-pill" style="--pc:#2fe89e"><span class="t">08:00</span>Dentist</div></div>
    <div class="cal-day" role="gridcell" tabindex="0"><span class="dnum">25</span></div>
    <div class="cal-day" role="gridcell" tabindex="0"><span class="dnum">26</span></div>
    <div class="cal-day" role="gridcell" tabindex="0"><span class="dnum">27</span>
      <div class="cal-pill" style="--pc:#3fb8ff"><span class="t">11:00</span>Board review</div></div>
    <div class="cal-day" role="gridcell" tabindex="0"><span class="dnum">28</span></div>
    <div class="cal-day" role="gridcell" tabindex="0"><span class="dnum">29</span></div>
    <div class="cal-day" role="gridcell" tabindex="0"><span class="dnum">30</span>
      <div class="cal-pill" style="--pc:#ffbf3d"><span class="t">16:00</span>Q4 planning</div></div>
    <div class="cal-day" role="gridcell" tabindex="0"><span class="dnum">31</span>
      <div class="cal-pill" style="--pc:#e84fff"><span class="t">20:00</span>Halloween</div></div>
    <div class="cal-day is-out" role="gridcell" tabindex="0"><span class="dnum">1</span></div>
  </div>
</div>
<script>
document.querySelectorAll('.cal-month .cal-day').forEach(d=>{
  d.addEventListener('click',()=>{
    document.querySelectorAll('.cal-month .is-selected').forEach(x=>x.classList.remove('is-selected'));
    d.classList.add('is-selected');
  });
  d.addEventListener('keydown',e=>{ if(e.key==='Enter'||e.key===' '){e.preventDefault();d.click();} });
});
</script>
```

Selection is local — your app wires what a selected day *does* (opens CAL-004,
filters, navigates). The specimen above freezes Oct 16 as today for teaching;
a live build sets `is-today` from the viewer's clock.

### States

- **Rest:** black cell `#0a0a0e`, 1.5px white-lit edge, serif day number. Pills rest dark with a 1px tinted border — color is earned by interaction, per Law 1.
- **Hover:** lifts 2px, edge ignites purple (chrome), glow `0 0 26px`. Pills ignite in their *own* event color — the pill is themed, the cell is chrome.
- **Selected:** held purple edge + purple glow + 2px lift. One selected day at a time; clicking moves it, never stacks it.
- **Today:** 2px gold edge, gold glow, slow 4s breathe. Gold belongs to today and to nothing else — a selected day that is not today wears purple.
- **Out-of-month:** 34% opacity, no ignition on hover — clicking one jumps the board to that month (the cell keeps its promise).
- **Overflow:** two pills render, then jewel dots in wheel order, then an honest `+N more` chip. The chip opens the day's agenda (CAL-004) — it never pretends the cell showed everything.

### Do / Don't

**Do** walk the wheel down each cell — magenta → purple → blue → green → gold, adjacent pills always in law order, never adjacent duplicates. **Don't** paint event types by mood of the day; the meaning of each color is fixed across the whole family, or the wheel becomes decoration.

### Anatomy

- **Board chrome:** 5-layer board shadow, 24px radius, tone under-glow. The board is the world; cells live inside it.
- **Title:** serif voice, month in 24px, year as an uppercase letterspaced kicker. White 99%.
- **Chevrons:** drawn CSS chevrons (Law 4 — icons are drawn), 44px targets, chrome-purple ignition. A chevron promises "go somewhere."
- **Weekday row:** serif, uppercase, letterspaced — the voice of the calendar.
- **Day cell:** the unit. Number (serif) + pills + dots + more-chip, in that order.
- **Event pill:** diamond jewel + time + title. The diamond is the bullet law at calendar scale.

**What it will NOT fake:** it never invents events to fill empty cells — an empty cell is honestly empty. It never guesses today: `is-today` comes from the viewer's clock or an explicit `data-today`; the specimen above is a frozen teaching state and a live build says so. The `+N more` count is the real count of hidden events, never a decoration.

---

## CAL-002 · Event card

One event, fully dressed: time rail, serif title, type tag in its fixed
spectrum color, location/attendees row. Hover lifts 6px and ignites in the
event's own color — the card is themed, so it burns its own hue.

### The code

```html
<style>
.cal-event{display:flex;gap:0;max-width:560px;background:linear-gradient(180deg,#141318,#08080c);
border:1.5px solid rgba(255,255,255,.3);border-radius:18px;overflow:hidden;cursor:pointer;
box-shadow:inset 0 2px 2px rgba(255,255,255,.1),0 12px 30px rgba(0,0,0,.6);
transition:transform .28s cubic-bezier(.16,.84,.22,1),border-color .28s,box-shadow .28s}
.cal-event:hover{transform:translateY(-6px);border-color:var(--ec);box-shadow:0 0 40px var(--ec-glow),0 22px 44px rgba(0,0,0,.7)}
.cal-event:active{transform:translateY(-2px)}
.cal-event:focus-visible{outline:2px solid #fff;outline-offset:3px}
.cal-rail{flex:none;width:86px;padding:18px 0 18px 18px;border-right:1px solid rgba(255,255,255,.12);
display:flex;flex-direction:column;gap:2px}
.cal-rail .t{font-family:Georgia,serif;font-size:18px;color:#fff}
.cal-rail .dur{font-size:11px;letter-spacing:.1em;color:#fff;opacity:.6;text-transform:uppercase}
.cal-body{flex:1;padding:16px 18px;position:relative}
.cal-body::before{content:"";position:absolute;left:0;top:14px;bottom:14px;width:3px;border-radius:3px;
background:var(--ec);box-shadow:0 0 12px var(--ec)}
.cal-type{display:inline-block;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--ec);
border:1px solid var(--ec);border-radius:999px;padding:3px 11px;margin-bottom:9px;background:rgba(0,0,0,.4)}
.cal-title{font-family:Georgia,serif;font-size:18px;color:#fff;margin:0 0 8px;text-shadow:0 2px 8px rgba(0,0,0,.8)}
.cal-meta{display:flex;flex-wrap:wrap;gap:14px;font-size:13px;color:#fff}
.cal-meta span{display:inline-flex;align-items:center;gap:7px;opacity:.92}
.cal-meta svg{width:14px;height:14px;stroke:var(--ec);fill:none;stroke-width:1.8;flex:none}
/* all-day: the rail becomes a band */
.cal-event.is-allday .cal-rail{width:10px;padding:0;background:var(--ec);border-right:none;box-shadow:0 0 16px var(--ec)}
.cal-event.is-allday .cal-rail .t,.cal-event.is-allday .cal-rail .dur{display:none}
.cal-event.is-allday .cal-body{padding-left:22px}
.cal-allday-flag{font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--ec);margin-bottom:6px}
/* multi-day: the rail carries the span */
.cal-event.is-span .cal-rail .t{font-size:15px}
.cal-span-note{font-size:12px;color:#fff;opacity:.75;margin-top:8px;letter-spacing:.04em}
/* tentative: dashed edge = honest uncertainty */
.cal-event.is-tentative{border-style:dashed}
.cal-event.is-tentative .cal-rail .t::after{content:" ~";color:var(--ec)}
</style>

<article class="cal-event" style="--ec:#3fb8ff;--ec-glow:rgba(63,184,255,.45)" tabindex="0">
  <div class="cal-rail"><span class="t">10:30</span><span class="dur">45 min</span></div>
  <div class="cal-body">
    <span class="cal-type">Meeting</span>
    <h3 class="cal-title">Design sync — Studio walk</h3>
    <div class="cal-meta">
      <span><svg viewBox="0 0 24 24"><path d="M12 21s-7-5.6-7-11a7 7 0 0 1 14 0c0 5.4-7 11-7 11z"/><circle cx="12" cy="10" r="2.6"/></svg>Studio B, Naya House</span>
      <span><svg viewBox="0 0 24 24"><circle cx="9" cy="8" r="3.4"/><path d="M2.8 20c.7-3.4 3.2-5.2 6.2-5.2s5.5 1.8 6.2 5.2"/><circle cx="17" cy="9" r="2.6"/><path d="M15.5 14.6c2.9.2 5 1.9 5.7 5.4"/></svg>4 attending</span>
    </div>
  </div>
</article>

<article class="cal-event is-allday" style="--ec:#e84fff;--ec-glow:rgba(232,79,255,.45)" tabindex="0" aria-label="All day: Anniversary">
  <div class="cal-rail" aria-hidden="true"></div>
  <div class="cal-body">
    <div class="cal-allday-flag">All day</div>
    <span class="cal-type">Celebration</span>
    <h3 class="cal-title">Anniversary</h3>
  </div>
</article>

<article class="cal-event is-span" style="--ec:#a06bff;--ec-glow:rgba(160,107,255,.45)" tabindex="0">
  <div class="cal-rail"><span class="t">Oct 20 → 22</span><span class="dur">3 days</span></div>
  <div class="cal-body">
    <span class="cal-type">Deep work</span>
    <h3 class="cal-title">Design sprint</h3>
    <p class="cal-span-note">Continues through Thursday — one event, three days, shown where it lives.</p>
  </div>
</article>

<article class="cal-event is-tentative" style="--ec:#2fe89e;--ec-glow:rgba(47,232,158,.45)" tabindex="0">
  <div class="cal-rail"><span class="t">07:00</span><span class="dur">30 min</span></div>
  <div class="cal-body">
    <span class="cal-type">Health · tentative</span>
    <h3 class="cal-title">Morning run with Jo</h3>
    <p class="cal-span-note">Not confirmed yet — the dashed edge says so before you have to ask.</p>
  </div>
</article>
```

### States

- **Rest:** dark card, white-lit edge, color present only as the spine, tag, and glyph strokes — never as a flood.
- **Hover:** lifts 6px (card weight), edge + glow ignite in the event's own color. Light moves first, words follow.
- **Active/press:** settles back 4px — it feels held.
- **Focus:** white 2px ring — keyboard users get the same ignition promise.
- **All-day:** the time rail collapses into a glowing color band; an "ALL DAY" flag replaces the time. It never shows a fake `00:00–23:59`.
- **Multi-day span:** the rail carries the range (`Oct 20 → 22`); the note says where the event continues. In CAL-001 the same event renders one pill per day with `→` honesty markers.
- **Tentative:** dashed 1.5px edge + `~` after the time + "tentative" in the tag. Uncertainty is styled, never hidden.

### Do / Don't

**Do** let the card ignite in the event's own spectrum color — purple for deep work, blue for meetings, gold for deadlines. **Don't** rest the card in its color; a card that wears its hue at rest is a flood, and floods are forbidden.

### Anatomy

- **Time rail:** the left column — serif time, uppercase duration. Time is the rail the card hangs on.
- **Spine:** 3px glowing line in the event color — the card's identity mark, shared with CAL-004's timeline.
- **Type tag:** pill in the event color, letterspaced. The tag's color is the fixed meaning from the family table — never improvised per card.
- **Title:** serif voice, 18px. The human name of the event.
- **Meta row:** drawn SVG glyphs (pin, people), never emoji — Law 4. Glyphs inherit the event color via `stroke`.
- **Tentative styling:** the honesty layer — dashed edge, tilde time, plain-words note.

**What it will NOT fake:** the time rail renders the time it was given — if no timezone is known, none is shown (no invented "PST", no silent conversion). All-day never renders a fake time range. Tentative never renders as confirmed. The attendee count is the real count or the row is omitted — never "4 attending" as decoration.

---

## CAL-003 · Date picker

A compact picker for embedding in forms: an input-styled trigger showing the
chosen date, a dropdown mini month grid, keyboard-honest focus states, past
dates visibly dimmed and truly inert. Law 1: the trigger lifts and ignites
chrome-purple like any control; the days ignite purple on hover and hold it
when chosen.

### The code

```html
<style>
.cal-pick{position:relative;display:inline-block;font-family:system-ui,sans-serif}
.cal-trigger{display:flex;align-items:center;gap:12px;min-width:240px;background:#050505;color:#fff;
border:1.5px solid rgba(255,255,255,.85);border-radius:14px;padding:13px 16px;cursor:pointer;font-size:15px;
box-shadow:inset 0 2px 2px rgba(255,255,255,.1),0 10px 24px rgba(0,0,0,.6);
transition:transform .18s cubic-bezier(.16,.84,.22,1),border-color .18s,box-shadow .18s}
.cal-trigger:hover{transform:translateY(-2px);border-color:#a06bff;box-shadow:0 0 26px rgba(160,107,255,.5),0 12px 26px rgba(0,0,0,.6)}
.cal-trigger:active{transform:translateY(1px)}
.cal-trigger:focus-visible{outline:2px solid #fff;outline-offset:3px}
.cal-trigger svg{width:18px;height:18px;stroke:#fff;fill:none;stroke-width:1.8;flex:none}
.cal-trigger .ph{opacity:.55}
.cal-drop{position:absolute;top:calc(100% + 10px);left:0;z-index:40;width:308px;background:linear-gradient(180deg,#16141b,#08080c);
border:1.5px solid rgba(255,255,255,.35);border-radius:18px;padding:18px;
box-shadow:inset 0 2px 2px rgba(255,255,255,.12),0 24px 60px rgba(0,0,0,.75),0 0 40px -14px rgba(160,107,255,.4)}
.cal-drop[hidden]{display:none}
.cal-drop-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:10px}
.cal-drop-head h3{font-family:Georgia,serif;font-size:16px;color:#fff;margin:0}
.cal-mini{display:grid;grid-template-columns:repeat(7,1fr);gap:4px}
.cal-mini .wd{font-size:10px;letter-spacing:.1em;color:#fff;opacity:.6;text-align:center;padding:4px 0;text-transform:uppercase}
.cal-mini button{aspect-ratio:1;border-radius:10px;background:transparent;border:1px solid transparent;color:#fff;
font-size:13px;cursor:pointer;transition:all .18s cubic-bezier(.16,.84,.22,1)}
.cal-mini button:hover:not(:disabled){transform:translateY(-2px);border-color:#a06bff;box-shadow:0 0 18px rgba(160,107,255,.55);background:rgba(160,107,255,.12)}
.cal-mini button:focus-visible{outline:2px solid #fff;outline-offset:2px}
.cal-mini button.is-chosen{background:rgba(160,107,255,.2);border-color:#a06bff;box-shadow:0 0 20px rgba(160,107,255,.6);font-weight:700}
.cal-mini button.is-todayd{border-color:#ffbf3d;color:#ffbf3d}
.cal-mini button:disabled{opacity:.32;cursor:not-allowed;text-decoration:line-through;text-decoration-color:rgba(255,255,255,.4)}
.cal-mini button:disabled:hover{transform:none;box-shadow:none;border-color:transparent;background:transparent}
.cal-tz{margin-top:12px;font-size:11px;color:#fff;opacity:.55;letter-spacing:.04em}
@media (prefers-reduced-motion:reduce){.cal-trigger,.cal-mini button{transition:none}}
</style>
<div class="cal cal-pick">
  <button class="cal-trigger" id="dpTrig" aria-haspopup="dialog" aria-expanded="false">
    <svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3.5" y="5" width="17" height="15.5" rx="2.5"/><path d="M3.5 9.5h17M8 3v4M16 3v4"/></svg>
    <span class="ph" id="dpLabel">Choose a date</span>
  </button>
  <div class="cal-drop" id="dpDrop" role="dialog" aria-label="Choose a date" hidden>
    <div class="cal-drop-head">
      <h3>October 2026</h3>
    </div>
    <div class="cal-mini" id="dpGrid" role="grid" aria-label="October 2026">
      <span class="wd">M</span><span class="wd">T</span><span class="wd">W</span><span class="wd">T</span><span class="wd">F</span><span class="wd">S</span><span class="wd">S</span>
    </div>
    <p class="cal-tz">Calendar date only — no timezone is assumed or stored.</p>
  </div>
</div>
<script>
(function(){
  const trig=document.getElementById('dpTrig'),drop=document.getElementById('dpDrop'),
        grid=document.getElementById('dpGrid'),label=document.getElementById('dpLabel');
  const YEAR=2026,MONTH=9,TODAY=16; /* October 2026; live build derives from the clock */
  const firstDow=(new Date(YEAR,MONTH,1).getDay()+6)%7; /* Monday-first */
  for(let i=0;i<firstDow;i++){const s=document.createElement('span');grid.appendChild(s);}
  let focusIdx=-1;const btns=[];
  for(let d=1;d<=31;d++){
    const b=document.createElement('button');
    b.textContent=d;b.setAttribute('role','gridcell');
    const iso=`${YEAR}-${String(MONTH+1).padStart(2,'0')}-${String(d).padStart(2,'0')}`;
    b.dataset.iso=iso;
    if(d===TODAY){b.classList.add('is-todayd');b.setAttribute('aria-label',`October ${d}, today`);}
    if(d<TODAY){b.disabled=true;b.setAttribute('aria-disabled','true');b.tabIndex=-1;
      b.setAttribute('aria-label',`October ${d}, in the past`);}
    b.addEventListener('click',()=>choose(b));
    grid.appendChild(b);btns.push(b);
  }
  function choose(b){
    btns.forEach(x=>x.classList.remove('is-chosen'));b.classList.add('is-chosen');
    const d=+b.textContent;
    label.textContent=`${['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][MONTH]} ${d}, ${YEAR}`;
    label.classList.remove('ph');trig.dataset.value=b.dataset.iso;close();
    trig.focus();
  }
  function open(){drop.hidden=false;trig.setAttribute('aria-expanded','true');
    const t=btns.find(b=>b.classList.contains('is-chosen'))||btns.find(b=>!b.disabled);if(t)t.focus();}
  function close(){drop.hidden=true;trig.setAttribute('aria-expanded','false');}
  trig.addEventListener('click',()=>drop.hidden?open():close());
  document.addEventListener('click',e=>{if(!drop.hidden&&!e.target.closest('.cal-pick'))close();});
  document.addEventListener('keydown',e=>{
    if(drop.hidden)return;
    const live=btns.filter(b=>!b.disabled);
    const cur=live.indexOf(document.activeElement);
    if(e.key==='Escape'){close();trig.focus();}
    else if(e.key==='ArrowRight'){e.preventDefault();(live[cur+1]||live[0]).focus();}
    else if(e.key==='ArrowLeft'){e.preventDefault();(live[cur-1]||live[live.length-1]).focus();}
    else if(e.key==='ArrowDown'){e.preventDefault();(live[cur+7]||live[live.length-1]).focus();}
    else if(e.key==='ArrowUp'){e.preventDefault();(live[cur-7]||live[0]).focus();}
    else if(e.key==='Enter'&&document.activeElement.dataset.iso){choose(document.activeElement);}
  });
})();
</script>
```

### States

- **Trigger rest:** input-styled — black body, 1.5px white edge, drawn calendar glyph, placeholder at 55% opacity ("Choose a date" — never a fake pre-filled date).
- **Trigger hover:** lifts 2px, ignites chrome-purple. It is chrome; it burns chrome's color.
- **Dropdown open:** elevated panel (Law 3 — overlay rides highest), tone under-glow. `aria-expanded` tells the truth.
- **Day hover:** lifts, purple edge + glow. Day focus (keyboard): white 2px ring — arrow keys move, Enter chooses, Esc closes and returns focus to the trigger.
- **Chosen:** held purple edge + glow + bold number. One chosen day; choosing moves it.
- **Today in the mini-grid:** gold edge + gold number — the family rule, at 36px scale.
- **Past dates:** 32% opacity, strikethrough, `cursor:not-allowed`, `disabled`, removed from tab order. Dimmed *and* inert — never the fake-disabled look that still clicks.

### Do / Don't

**Do** make past dates visibly dimmed and keyboard-unreachable — a disabled date that still takes focus is a lie with styling. **Don't** pre-fill the trigger with "today" to look alive; an unchosen picker says "Choose a date" until a human chooses.

### Anatomy

- **Trigger:** the form-facing face — reads as an input, behaves as a button. Glyph is drawn SVG, never emoji.
- **Dropdown panel:** the mini month — weekday initials, 36px day buttons, the month title in serif voice.
- **Day button:** the unit — number, hover ignition, chosen hold, today gold, past inert.
- **Timezone footnote:** the honesty line — "Calendar date only — no timezone is assumed or stored." It is part of the block, not documentation.

**What it will NOT fake:** it never pretends to know the user's timezone — the value is a calendar date (`YYYY-MM-DD`), stored noon-neutral, displayed as-is. It never converts, never appends a zone abbreviation it doesn't know, and never disables dates by guessing. Past-ness is computed against the viewer's clock or an explicit `data-today`; the frozen October 16 in the specimen is labeled as a specimen.

---

## CAL-004 · Agenda list

The day's events as a vertical timeline: time gutter, glowing spectrum
spine per event type, cards in CAL-002's language. A day with nothing on it
says so honestly — "Nothing scheduled — the day is yours."

### The code

```html
<style>
.cal-agenda{max-width:640px;margin:0 auto;background:linear-gradient(180deg,#141318,#08080c);
border:1.5px solid rgba(255,255,255,.3);border-radius:24px;padding:26px;
box-shadow:inset 0 2px 2px rgba(255,255,255,.12),inset 0 -8px 18px rgba(0,0,0,.55),0 5px 0 #020203,0 35px 75px rgba(0,0,0,.7)}
.cal-agenda h2{font-family:Georgia,serif;font-size:24px;color:#fff;margin:0 0 4px}
.cal-agenda .sub{font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:#fff;opacity:.6;margin-bottom:20px}
.cal-tl{list-style:none;margin:0;padding:0;position:relative}
.cal-tl li{position:relative;display:grid;grid-template-columns:64px 1fr;gap:0 0;padding-bottom:18px}
.cal-tl li:last-child{padding-bottom:0}
.cal-gutter{font-family:Georgia,serif;font-size:15px;color:#fff;text-align:right;padding:14px 16px 0 0;opacity:.9}
.cal-spine{position:absolute;left:64px;top:0;bottom:0;width:3px;border-radius:3px;background:var(--ec);box-shadow:0 0 12px var(--ec)}
.cal-tl li::before{content:"";position:absolute;left:64px;top:20px;width:11px;height:11px;transform:translateX(-4px) rotate(45deg);
background:var(--ec);box-shadow:0 0 10px var(--ec);z-index:1}
.cal-ev{background:#0a0a0e;border:1.5px solid rgba(255,255,255,.28);border-radius:14px;padding:14px 16px;margin-left:22px;cursor:pointer;
transition:transform .28s cubic-bezier(.16,.84,.22,1),border-color .28s,box-shadow .28s}
.cal-ev:hover{transform:translateY(-4px);border-color:var(--ec);box-shadow:0 0 32px var(--ec-glow)}
.cal-ev:focus-visible{outline:2px solid #fff;outline-offset:3px}
.cal-ev h3{font-family:Georgia,serif;font-size:17px;color:#fff;margin:6px 0 6px}
.cal-ev .tag{display:inline-block;font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:var(--ec);
border:1px solid var(--ec);border-radius:999px;padding:2px 10px}
.cal-ev .meta{font-size:13px;color:#fff;opacity:.8;margin-top:6px}
.cal-now{position:relative;height:0;z-index:2}
.cal-now i{position:absolute;left:58px;right:0;top:0;height:2px;border-radius:2px;
background:linear-gradient(90deg,#ffbf3d,rgba(255,191,61,0));box-shadow:0 0 14px rgba(255,191,61,.7)}
.cal-now b{position:absolute;left:60px;top:-16px;font-size:10px;letter-spacing:.18em;color:#ffbf3d;font-weight:400;text-transform:uppercase}
.cal-empty{text-align:center;padding:56px 20px}
.cal-empty .jewel{width:34px;height:34px;margin:0 auto 18px;transform:rotate(45deg);border-radius:8px;
background:radial-gradient(circle at 35% 30%,#fff,var(--gold,#ffbf3d) 45%,#050507 90%);
border:1.5px solid rgba(255,255,255,.8);box-shadow:0 0 30px rgba(255,191,61,.55)}
.cal-empty h3{font-family:Georgia,serif;font-size:20px;color:#fff;margin:0 0 8px}
.cal-empty p{font-size:14px;color:#fff;opacity:.85;margin:0}
@media (prefers-reduced-motion:reduce){.cal-ev{transition:none}}
</style>
<div class="cal cal-agenda">
  <h2>Friday, October 16</h2>
  <p class="sub">3 events · today</p>
  <ol class="cal-tl">
    <li style="--ec:#a06bff;--ec-glow:rgba(160,107,255,.5)">
      <span class="cal-gutter">09:00</span><span class="cal-spine" aria-hidden="true"></span>
      <div class="cal-ev" tabindex="0"><span class="tag">Deep work</span><h3>Ship the calendar spec</h3><p class="meta">2 h · Studio</p></div>
    </li>
    <li style="--ec:#3fb8ff;--ec-glow:rgba(63,184,255,.5)">
      <span class="cal-gutter">10:30</span><span class="cal-spine" aria-hidden="true"></span>
      <div class="cal-ev" tabindex="0"><span class="tag">Meeting</span><h3>Standup</h3><p class="meta">15 min · 6 attending</p></div>
    </li>
    <div class="cal-now" aria-hidden="true"><i></i><b>now</b></div>
    <li style="--ec:#ffbf3d;--ec-glow:rgba(255,191,61,.5)">
      <span class="cal-gutter">15:00</span><span class="cal-spine" aria-hidden="true"></span>
      <div class="cal-ev" tabindex="0"><span class="tag">Decision</span><h3>Launch decision</h3><p class="meta">1 h · The call Shawn takes</p></div>
    </li>
  </ol>
</div>

<div class="cal cal-agenda" style="margin-top:28px" aria-label="Empty day example">
  <h2>Saturday, October 17</h2>
  <p class="sub">tomorrow</p>
  <div class="cal-empty">
    <div class="jewel" aria-hidden="true"></div>
    <h3>Nothing scheduled</h3>
    <p>The day is yours.</p>
  </div>
</div>
```

The now-line is positioned by your app from the clock at render time — it is
only ever rendered when the viewed day *is* today. A specimen freezes it; a
live build computes it or omits it.

### States

- **Rest:** gutter times in serif, spines glowing quietly in each event's color, cards dark with white-lit edges.
- **Hover:** the card lifts 4px and ignites in the event's own color — same language as CAL-002, one family.
- **Now-line:** gold gradient line with a "now" flag. Gold = attention, earned; the current moment is the one thing that deserves it.
- **Empty:** centered gold jewel, serif "Nothing scheduled", 14px "The day is yours." No fake suggestions, no "maybe add…" nudges, no grayed-out ghost events.
- **Past events (viewing today):** the card keeps its colors but the spine dims to 40% and the title takes no hover lift — the past is readable, not clickable-theater. (Your app sets `aria-disabled` where the event can't be acted on.)

### Do / Don't

**Do** give every event one glowing spine in its fixed type color, in wheel order down the day — the timeline should read as a walked spectrum. **Don't** render a now-line on any day that isn't today; a fake "now" on last Tuesday is a trust violation with styling.

### Anatomy

- **Time gutter:** serif times, right-aligned — the rail the day hangs on.
- **Spine:** 3px glowing line per event in its type color — the same identity mark as CAL-002's card spine, so the two blocks read as one object.
- **Node jewel:** the rotated diamond where gutter meets spine — Law 4, bullets are jewels, at timeline scale.
- **Event card:** CAL-002's language compressed — tag, serif title, one meta line. One idea per card.
- **Now-line:** the honest present — gold, labeled, clock-driven.
- **Empty state:** jewel + two lines. Emptiness is a state with dignity, not a hole to fill with suggestions.

**What it will NOT fake:** it never invents events — an empty day renders the empty state, never placeholder cards. The now-line never renders for a non-today view. Past events never pretend to be upcoming: no hover theater on what can't be acted on. The "3 events" count is the real count.

---

## CAL-005 · Day-cell state system

The seven honest states of a calendar day, specified once so CAL-001 and
CAL-003 never drift apart. A state is visual truth: if it looks clickable it
is clickable; if it looks dead it is dead.

### The code

```html
<style>
.cal-states{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;max-width:900px;margin:0 auto}
.cal-st{border-radius:14px;padding:16px 14px;min-height:120px;background:#0a0a0e;position:relative;
border:1.5px solid rgba(255,255,255,.32);transition:transform .18s cubic-bezier(.16,.84,.22,1),border-color .18s,box-shadow .18s}
.cal-st .dnum{font-family:Georgia,serif;font-size:20px;color:#fff}
.cal-st .lbl{position:absolute;left:14px;bottom:12px;font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:#fff;opacity:.65}
.cal-st .why{font-size:11px;color:#fff;opacity:.55;margin-top:8px;line-height:1.5}
.cal-st.s-hover{transform:translateY(-2px);border-color:#a06bff;box-shadow:0 0 26px rgba(160,107,255,.5)}
.cal-st.s-selected{transform:translateY(-2px);border-color:#a06bff;box-shadow:0 0 32px rgba(160,107,255,.65),inset 0 0 18px rgba(160,107,255,.12)}
.cal-st.s-today{border:2px solid #ffbf3d;box-shadow:0 0 34px rgba(255,191,61,.6);animation:cal-breathe 4s ease-in-out infinite}
.cal-st.s-today .dnum{color:#ffbf3d}
.cal-st.s-events{border-color:rgba(255,255,255,.5)}
.cal-st.s-events .dots{display:flex;gap:5px;margin-top:10px}
.cal-st.s-events .dots i{width:7px;height:7px;transform:rotate(45deg);background:var(--pc);box-shadow:0 0 7px var(--pc)}
.cal-st.s-disabled{opacity:.32;cursor:not-allowed}
.cal-st.s-disabled .dnum{text-decoration:line-through;text-decoration-color:rgba(255,255,255,.4)}
.cal-st.s-out{opacity:.34}
.cal-st.s-out .lbl::after{content:" · jumps month"}
@media (prefers-reduced-motion:reduce){.cal-st.s-today{animation:none}.cal-st{transition:none}}
</style>
<div class="cal cal-states">
  <div class="cal-st"><span class="dnum">12</span><p class="why">Dark cell, white-lit edge. Waiting.</p><span class="lbl">Rest</span></div>
  <div class="cal-st s-hover"><span class="dnum">13</span><p class="why">Lifts 2px, ignites chrome-purple. Clickable.</p><span class="lbl">Hover</span></div>
  <div class="cal-st s-selected"><span class="dnum">14</span><p class="why">Held purple edge + glow. One at a time.</p><span class="lbl">Selected</span></div>
  <div class="cal-st s-today"><span class="dnum">16</span><p class="why">Gold edge, gold glow, slow breathe. Only today.</p><span class="lbl">Today</span></div>
  <div class="cal-st s-events"><span class="dnum">15</span><div class="dots"><i style="--pc:#a06bff"></i><i style="--pc:#3fb8ff"></i><i style="--pc:#ffbf3d"></i></div><p class="why">Jewel dots in wheel order. Never adjacent duplicates.</p><span class="lbl">Has events</span></div>
  <div class="cal-st s-disabled"><span class="dnum">9</span><p class="why">Dimmed, struck, inert — and out of tab order.</p><span class="lbl">Disabled</span></div>
  <div class="cal-st s-out"><span class="dnum">30</span><p class="why">Belongs to another month. Click jumps there.</p><span class="lbl">Out of month</span></div>
</div>
```

### States

The seven, each frozen above so a builder can implement without running anything:

- **Rest:** the baseline — black, white-lit, serif number. All other states are deltas from this.
- **Hover:** lift + chrome-purple ignition. Frozen here with the class so the state is visible statically.
- **Selected:** the hover ignition *held* — edge, glow, lift persist. Moving selection moves the hold; it is never stacked on two days.
- **Today:** gold 2px edge, gold glow, 4s breathe. If today is also selected, gold wins — today outranks selection, always.
- **Has-events:** jewel dots (or pills in CAL-001) in wheel order. The dots are information, not decoration — their colors are the event types.
- **Disabled:** 32% opacity, strikethrough number, `cursor:not-allowed`, `disabled` + `tabindex="-1"` in real markup. Looks dead because it *is* dead.
- **Out-of-month:** 34% opacity, no ignition — but still clickable, jumping the board to its month. Dimmed is not dead here; the label says what it does.

### Do / Don't

**Do** freeze today above selection in the precedence order — when both apply, the day wears gold, because today is the fact and selection is the choice. **Don't** invent an eighth state for "weekend" or "holiday" tinting; tinting days by category is a flood by another name — holidays are events, and events already have colors.

### Anatomy

- **The cell:** one class per state (`.s-hover`, `.s-selected`, `.s-today`, `.s-events`, `.s-disabled`, `.s-out`) — states compose by class, never by inline-style improvisation.
- **Precedence order:** today > selected > hover > has-events > rest; disabled and out-of-month modify the base independently. Written down so two builders never disagree.
- **The label:** every specimen carries its state name — teaching statically, per the state-strip pattern.
- **Reduced motion:** the today-breathe stops, transitions drop. Motion is earned by meaning; the meaning survives without it.

**What it will NOT fake:** disabled never merely *looks* disabled — it is removed from keyboard reach and ignores clicks. Out-of-month never pretends to belong; its label names its behavior. Selected never renders on two days at once. Today is computed, never guessed — a frozen specimen says it's a specimen.

---

## Family notes

- **One meaning per color, everywhere:** the family table at the top is the contract. A purple pill in CAL-001, a purple spine in CAL-004, and a purple tag in CAL-002 all mean deep work. If a sixth event type appears, it takes orange — the wheel continues, it never restarts.
- **Gold's two jobs are one job:** today (CAL-001, CAL-003, CAL-005) and the now-line (CAL-004) are both "attention, earned" — the present moment, marked. That is a single meaning, not a reuse.
- **What the family does not cover:** week-view grids, drag-to-reschedule, and recurring-event editors are real needs and are *not* specified here — they are future blocks (CAL-006+), not implied features of these five. Nothing in these specs pretends they exist.
