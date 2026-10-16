# CHAT BLOCKS — the family

The warehouse had no chat pieces. Shawn said do it. Three blocks, one
family, one law order. **Laws cited:** ALIVE (Law 1) — living but calm:
motion breathes, never jitters. TYPE (Law 6) — serif voice on day dividers,
white 99%. ELEVATION (Law 3) — bubbles ride above the field, the scroll pill
rides above the list. JEWELS (Law 4) — avatars are lit orbs, read ticks are
drawn, never emoji.

The family law, stated once and binding on all three blocks: **truth-states
only.** A typing indicator exists only while a live signal says someone is
typing. A read receipt turns only after the other side actually rendered the
message. Motion breathes at 72bpm — slow enough to be calm, alive enough to
be awake. Nothing in this family ever performs liveness it does not have.

**In/out language — fixed forever, across all three blocks:**

| Side | Hex | Meaning |
|---|---|---|
| incoming | white-lit edge `#fff` | Someone else's words — the world speaking in |
| outgoing | purple `#a06bff` | My voice — choosing intelligence, going out |
| read | gold `#ffbf3d` | Attention, earned — the moment was seen |

Outgoing bubbles rest dark with a held purple edge — the edge is the
identity mark, not a flood. Incoming bubbles rest dark with a 1.5px white-lit
edge. Color earns its meaning: purple says "mine," gold says "seen." Message
content never renders into logs, previews, or anywhere beyond the bubble —
private by default, everywhere.

**Family token sheet** (every snippet below assumes these; copy once):

```css
.chat{--ground:#050507;--ink:#fff;--bubble-in:#0e0e13;--bubble-out:#0d0a16;
--purple:#a06bff;--gold:#ffbf3d;--magenta:#e84fff;--blue:#3fb8ff;--green:#2fe89e;
--red:#ff5e6c;--serif:Georgia,'Times New Roman',serif;
--ease:cubic-bezier(.16,.84,.22,1);--bpm:0.833s;
background:var(--ground);color:var(--ink)}
```

`--bpm` is the 72-beats-per-minute heartbeat: `60/72 = 0.833s`. Every ambient
loop in this family is a multiple of it. Calm timing is not a feeling — it
is a number.

---

## CHT-003 · Chat bubbles (in/out)

The atomic message object: incoming on the left (dark board, white-lit
edge), outgoing on the right (purple-ignited edge), a tail that points the
way the words came from. Consecutive messages from one sender collapse into
a group — one avatar, one timestamp, no repeated faces. Read receipts are
honest truth-states: sent, delivered, read — and "read" is never shown
before the other side renders.

### The code

```html
<style>
.chat-row{display:flex;gap:10px;margin:4px 0;align-items:flex-end;max-width:760px}
.chat-row.out{flex-direction:row-reverse;margin-left:auto}
.chat-ava{flex:none;width:36px;height:36px;border-radius:50%;
background:radial-gradient(circle at 35% 30%,#fff,var(--purple) 42%,#050507 92%);
border:1.5px solid rgba(255,255,255,.85);box-shadow:0 0 18px rgba(160,107,255,.5)}
.chat-ava.in{--purple:#3fb8ff}
.chat-bub{position:relative;max-width:min(70%,480px);padding:11px 15px;font-size:15px;line-height:1.5;color:#fff;
box-shadow:inset 0 2px 2px rgba(255,255,255,.1),0 8px 22px rgba(0,0,0,.55);
transition:transform .28s cubic-bezier(.16,.84,.22,1),box-shadow .28s,border-color .28s}
.chat-bub.in{background:linear-gradient(180deg,#121218,#0a0a0f);border:1.5px solid rgba(255,255,255,.85);border-radius:18px 18px 18px 6px}
.chat-bub.out{background:linear-gradient(180deg,#141021,#0b0812);border:1.5px solid #a06bff;border-radius:18px 18px 6px 18px;
box-shadow:inset 0 2px 2px rgba(255,255,255,.1),0 8px 22px rgba(0,0,0,.55),0 0 24px -6px rgba(160,107,255,.55)}
.chat-bub.in::after,.chat-bub.out::after{content:"";position:absolute;bottom:-1px;width:14px;height:14px;background:inherit;transform:rotate(45deg)}
.chat-bub.in::after{left:-8px;border-left:1.5px solid rgba(255,255,255,.85);border-bottom:1.5px solid rgba(255,255,255,.85);border-bottom-left-radius:4px}
.chat-bub.out::after{right:-8px;border-right:1.5px solid #a06bff;border-bottom:1.5px solid #a06bff;border-bottom-right-radius:4px}
.chat-row:hover .chat-bub.in{transform:translateY(-2px);box-shadow:inset 0 2px 2px rgba(255,255,255,.1),0 12px 26px rgba(0,0,0,.6),0 0 26px rgba(255,255,255,.25)}
.chat-row:hover .chat-bub.out{transform:translateY(-2px);box-shadow:inset 0 2px 2px rgba(255,255,255,.1),0 12px 26px rgba(0,0,0,.6),0 0 34px rgba(160,107,255,.75)}
.chat-bub:active{transform:translateY(1px)}
/* grouped: collapse repeats, tighten adjoining corners */
.chat-row.grp{margin:2px 0}
.chat-row.grp .chat-ava{visibility:hidden}
.chat-row.grp .chat-bub.in{border-radius:18px 18px 18px 6px}
.chat-row.grp-first .chat-bub.in{border-bottom-left-radius:6px}
.chat-row.grp-first .chat-bub.out{border-bottom-right-radius:6px}
.chat-row.grp .chat-bub.in::after,.chat-row.grp .chat-bub.out::after{display:none}
.chat-meta{display:flex;align-items:center;gap:8px;margin-top:5px;font-size:12px;color:#fff;opacity:.75;min-height:18px}
.chat-row.out .chat-meta{flex-direction:row-reverse}
.chat-name{font-size:13px;letter-spacing:.04em;opacity:.9}
.chat-time{font-size:12px;opacity:.7}
/* receipts: drawn ticks, truth-states */
.chat-ticks{display:inline-flex;align-items:center;gap:0;min-width:44px;min-height:18px;justify-content:flex-end}
.chat-ticks svg{width:17px;height:17px;fill:none;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round}
.chat-ticks[data-state="sending"] svg{stroke:rgba(255,255,255,.55)}
.chat-ticks[data-state="sent"] svg{stroke:rgba(255,255,255,.85)}
.chat-ticks[data-state="delivered"] svg{stroke:#fff;filter:drop-shadow(0 0 5px rgba(255,255,255,.6))}
.chat-ticks[data-state="read"] svg{stroke:#ffbf3d;filter:drop-shadow(0 0 6px rgba(255,191,61,.8))}
.chat-ticks[data-state="read"]::after{content:"Seen";font-size:11px;letter-spacing:.1em;color:#ffbf3d;margin-left:5px;text-transform:uppercase}
.chat-ticks .sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
/* one bubble, edited: the honesty tag */
.chat-edited{font-size:11px;opacity:.55;font-style:italic;margin-left:2px}
@media (prefers-reduced-motion:reduce){.chat-bub{transition:none}}
</style>
<div class="chat" aria-label="Conversation">
  <div class="chat-row grp-first">
    <div class="chat-ava in" aria-hidden="true"></div>
    <div>
      <div class="chat-bub in">The Hub is live. Watch the feed.</div>
      <div class="chat-meta"><span class="chat-name">Sam</span><span class="chat-time">21:02</span></div>
    </div>
  </div>
  <div class="chat-row grp">
    <div class="chat-ava in" aria-hidden="true"></div>
    <div><div class="chat-bub in">Compiler ticked green on the hour.</div></div>
  </div>
  <div class="chat-row out grp-first">
    <div class="chat-ava" aria-hidden="true"></div>
    <div>
      <div class="chat-bub out">Seeing it. Smart Note landed in seconds.</div>
      <div class="chat-meta">
        <span class="chat-time">21:04</span>
        <span class="chat-ticks" data-state="read" role="img" aria-label="Read">
          <span class="sr">Read</span>
          <svg viewBox="0 0 24 24"><path d="M2.5 12.5l4.5 4.5L14 9.5"/><path d="M10 15.5l1.8 1.8L21 8"/></svg>
        </span>
      </div>
    </div>
  </div>
  <div class="chat-row out grp">
    <div class="chat-ava" aria-hidden="true"></div>
    <div><div class="chat-bub out">Ship it.<span class="chat-edited">edited</span></div>
      <div class="chat-meta">
        <span class="chat-time">21:05</span>
        <span class="chat-ticks" data-state="delivered" role="img" aria-label="Delivered">
          <span class="sr">Delivered</span>
          <svg viewBox="0 0 24 24"><path d="M2.5 12.5l4.5 4.5L14 9.5"/><path d="M10 15.5l1.8 1.8L21 8"/></svg>
        </span>
      </div>
    </div>
  </div>
  <div class="chat-row out">
    <div class="chat-ava" aria-hidden="true"></div>
    <div><div class="chat-bub out">One more thing — check the now-line on the agenda.</div>
      <div class="chat-meta">
        <span class="chat-time">21:06</span>
        <span class="chat-ticks" data-state="sent" role="img" aria-label="Sent">
          <span class="sr">Sent</span>
          <svg viewBox="0 0 24 24"><path d="M3 12.5l4.5 4.5L15 9"/></svg>
        </span>
      </div>
    </div>
  </div>
</div>
<script>
/* The receipt contract. Your transport owns the truth; this is how the block
   displays it. setReceipt(el, state) is the ONLY writer of data-state. */
(function(){
  const ORDER=['sending','sent','delivered','read'];
  window.chatReceipt=function(el,state){
    if(!ORDER.includes(state))return;
    el.setAttribute('data-state',state);
    const sr=el.querySelector('.sr');if(sr)sr.textContent=state[0].toUpperCase()+state.slice(1);
    el.setAttribute('aria-label',state[0].toUpperCase()+state.slice(1));
  };
  /* Grouping rule, enforced by the renderer: same sender AND <5 min apart
     gets .grp; the first of the run gets .grp-first. A renderer that can't
     decide groups renders every row ungrouped — never a wrong group. */
})();
</script>
```

### States

- **Rest (in):** dark board bubble, 1.5px white-lit edge, tail pointing left toward the speaker. Color at rest is white — the world's words wear the world's light.
- **Rest (out):** dark bubble, held 1.5px purple edge + soft purple under-glow, tail pointing right. The purple edge is the identity mark of "my voice" — a spine, not a flood. Never rest-purple as a fill.
- **Hover:** lifts 2px; incoming ignites white (`0 0 26px rgba(255,255,255,.25)`), outgoing ignites purple. Light moves first, words follow.
- **Press:** settles 1px — it feels held.
- **Grouped:** avatar hidden (space kept so the column doesn't jump), margins tighten 4px → 2px, adjoining corners square off, tails suppressed inside the group. The group reads as one breath of speech. Only name + time on the first row.
- **Receipts — the truth-states:** `sending` (single dim tick — my client hasn't handed it off yet), `sent` (single white tick — the server has it), `delivered` (double white tick, glow — their device has it), `read` (double gold tick + gold "SEEN" — their client *rendered* it, reported back through the transport). States move forward only, never backward. A screen reader hears "Sending / Sent / Delivered / Read" — the words are the contract.
- **Edited:** an italic "edited" tag inside the bubble. Edits are labeled; the block never shows an edit history (that is a thread feature, CHT-004+), it only refuses to pretend the first draft was final.
- **Long messages:** the bubble caps at 480px / 70% and the words wrap. A 2,000-word message is a document problem — the block wraps it honestly, never truncates it into "…".

### Do / Don't

**Do** render receipts only from the transport's truth — the block displays states, it never invents them; `setReceipt` is the single writer of `data-state`. **Don't** ever show "read" because the message is old, because the app was backgrounded, or because it looks better — a fake read is a trust violation with styling, and this family has exactly one unforgivable sin.

### Anatomy

- **Row:** flex line, avatar + bubble, `align-items:flex-end`. Outgoing rows reverse; the column edge is the speaker's edge.
- **Avatar orb:** 36px lit jewel orb in Law 4's language — white-hot crown fading through the speaker's tone to black. Incoming orbs wear blue, outgoing wear purple: the tone follows the speaker's edge. In grouped rows the orb hides but keeps its space.
- **Bubble:** the unit. 15px/1.5 line-height text (never smaller — chat is read at a glance, in motion), 11px × 15px padding, 18px radius with the speaker-side bottom corner squared to 6px where the tail grows.
- **Tail:** a rotated 14px square in the bubble's own background, edged in the bubble's edge color — geometry, not an image. It points the way the words came from: left for incoming, right for outgoing. Suppressed inside groups; a group speaks with one tail on its last breath.
- **Meta line:** name + time for incoming, time + receipt ticks for outgoing. 12px, 75% opacity — information, never decoration.
- **Ticks:** drawn SVG strokes (Law 4 — icons are drawn), never emoji, never characters. Single for sent, double for delivered, double-gold + "SEEN" for read. Gold = attention, earned.

**What it will NOT fake:** it never marks read before the other side renders — the `read` state arrives through the transport (a render receipt from their client), never from a timer, a guess, or the app being in the foreground. It never groups messages from different senders, or messages more than 5 minutes apart, or messages across a date divider (CHT-005 owns that boundary). It never logs, previews, or echoes message content anywhere outside the bubble — the block renders the text it is given and nothing else. It never shows an avatar for a speaker the renderer doesn't know — unknown senders get the orb in chrome-white, never a fake face.

---

## CHT-004 · Typing indicator

Three living dots in a bubble shell: the calm heartbeat of someone about to
speak. It pulses at 72bpm, staggers softly, and — this is the whole point —
it exists **only while a live signal says someone is typing**. No signal, no
dots. And it carries a contract: 30 seconds with no keep-alive and no message,
and it dismisses itself honestly — replaced by the message that arrived, or
simply gone.

### The code

```html
<style>
.chat-typing{display:flex;gap:10px;align-items:flex-end;margin:4px 0;max-width:760px}
.chat-typing .chat-ava{flex:none;width:36px;height:36px;border-radius:50%;
background:radial-gradient(circle at 35% 30%,#fff,#3fb8ff 42%,#050507 92%);
border:1.5px solid rgba(255,255,255,.85);box-shadow:0 0 18px rgba(63,184,255,.5)}
.chat-dots{display:flex;align-items:center;gap:8px;padding:16px 20px;border-radius:18px 18px 18px 6px;
background:linear-gradient(180deg,#121218,#0a0a0f);border:1.5px solid rgba(255,255,255,.85);
box-shadow:inset 0 2px 2px rgba(255,255,255,.1),0 8px 22px rgba(0,0,0,.55)}
.chat-dots i{width:9px;height:9px;border-radius:50%;background:#fff;flex:none;
box-shadow:0 0 10px rgba(255,255,255,.8);animation:chat-breathe .833s ease-in-out infinite}
.chat-dots i:nth-child(2){animation-delay:.208s}
.chat-dots i:nth-child(3){animation-delay:.416s}
@keyframes chat-breathe{0%,100%{transform:scale(.72);opacity:.45}50%{transform:scale(1.12);opacity:1}}
.chat-typing .who{font-size:12px;color:#fff;opacity:.7;margin-top:5px;letter-spacing:.04em}
.chat-typing[hidden]{display:none}
@media (prefers-reduced-motion:reduce){.chat-dots i{animation:none;opacity:.85;transform:none}}
</style>
<div class="chat chat-typing" id="typingSam" role="status" aria-live="polite" aria-label="Sam is typing">
  <div class="chat-ava" aria-hidden="true"></div>
  <div>
    <div class="chat-dots" aria-hidden="true"><i></i><i></i><i></i></div>
    <p class="who">Sam is typing</p>
  </div>
</div>
<script>
/* The typing contract. Your transport owns the truth; this module owns the
   honesty. show() requires a signal id; the 30s watchdog is non-negotiable. */
(function(){
  const WATCHDOG_MS=30000, KEEPALIVE_MS=20000;
  const live=new Map(); /* signalId -> {el, timer} */
  function dismiss(id,silent){
    const s=live.get(id);if(!s)return;
    clearTimeout(s.timer);live.delete(id);
    s.el.hidden=true;
    if(!silent)s.el.dispatchEvent(new CustomEvent('chat:typing-expired',{bubbles:true,detail:{id}}));
  }
  window.chatTyping={
    /* show(el, signalId): render the dots. The signal id is the transport's
       live typing event; there is no show() without one. */
    show(el,signalId){
      if(!signalId)throw new Error('chatTyping.show requires a live signal id — no fake typing');
      el.hidden=false;
      if(live.has(signalId))clearTimeout(live.get(signalId).timer);
      /* watchdog: 30s with no keep-alive and no message => honest dismissal */
      const timer=setTimeout(()=>dismiss(signalId),WATCHDOG_MS);
      live.set(signalId,{el,timer});
    },
    /* keepalive(signalId): the transport re-asserts while the user still types */
    keepalive(signalId){
      const s=live.get(signalId);if(!s)return;
      clearTimeout(s.timer);
      s.timer=setTimeout(()=>dismiss(signalId),WATCHDOG_MS);
    },
    /* arrived(signalId): the message landed — the dots are replaced by truth */
    arrived(signalId){dismiss(signalId,true);}
  };
  /* The transport calls keepalive at most every 20s; a signal older than that
     without re-assertion is stale and the next keepalive is ignored. */
})();
</script>
```

The specimen renders the indicator statically so a builder can see it; a
live build renders it **only** through `chatTyping.show(el, signalId)` with a
real signal id. The dots on screen with no signal behind them are a specimen,
and the code says so.

### States

- **Rest:** the bubble shell in incoming language (dark, white-lit edge, left
tail geometry) with three white dots breathing at 72bpm, staggered at
quarter-beat intervals (0 / .208s / .416s). White — the speaker is the world
speaking in.
- **Live:** the pulse itself — each dot scales .72 → 1.12 and breathes
.45 → 1 opacity. One beat per 0.833s. Calm is a number: the easing is
`ease-in-out`, never linear, never snappy.
- **Keep-alive:** invisible as a state — the dots simply continue. The
transport re-asserts every ≤20s while the human types; each re-assertion
resets the 30s watchdog. Your eye sees nothing change; the contract sees
everything.
- **Watchdog expiry:** the dots fade and the row unmounts. No message, no
dots, no explanation owed — the honest end of an unfinished thought. The
block fires `chat:typing-expired` so the app can log it, never to fake the
message that didn't come.
- **Message arrival:** the indicator unmounts the instant the real message
renders (`arrived`). The dots are replaced by the words — never shown
alongside them, never lingering "for effect."
- **Reduced motion:** the pulse stops; three steady dots at 85% opacity. The
meaning — *someone is here* — survives without the motion.

### Do / Don't

**Do** require a live signal id for every render — the `throw` in `show()`
is the law in code: no signal, no dots, no exceptions. **Don't** keep the
indicator alive to look responsive while the other side went quiet; after
30 seconds the honest answer is absence, not persistence. A typing indicator
that outlives the typist is a ghost with styling.

### Anatomy

- **Shell:** the incoming bubble's geometry — same dark gradient, same
white-lit edge, same left tail — so the dots read as *Sam's* unfinished
sentence, in Sam's place.
- **Dots:** three 9px white orbs, Law-4 glow. The stagger is a quarter-beat
walk — 0, .208s, .416s — so the pulse travels left to right like a breath,
never a flicker.
- **The heartbeat:** `--bpm:0.833s` — 72 beats per minute, the resting human
pulse. Frantic is forbidden: nothing in this block animates faster than one
beat.
- **The "who" line:** 12px plain words — "Sam is typing." The dots are felt;
the line is the fallback for eyes that miss motion and for screen readers
(`role="status"`, `aria-live="polite"`).
- **The watchdog:** 30s, non-negotiable, in code. Not a guideline — a timer.

**What it will NOT fake:** it never renders on a schedule, on a timer "to
look alive," or because the conversation went quiet and the screen felt dead
— those are the three classic forgeries and the `throw` exists to stop all
three. It never converts an expired indicator into a message ("Sam sent
something") — absence stays absence. It never shows two typing indicators
for one signal id. The aria announcement fires only for real signals; a
screen-reader user is lied to exactly as badly by a fake announcement as a
sighted user is by fake dots.

---

## CHT-005 · Message list

The conversation as a room: bubbles (CHT-003) day-grouped under serif date
dividers, in a board that scrolls with an honest contract — it sticks to the
bottom only if the reader is already there, and it never yanks a reading
user. An empty room says so plainly: "No messages yet — say the first word."

### The code

```html
<style>
.chat-list{max-width:820px;margin:0 auto;background:linear-gradient(180deg,#1a171f,#09090d 60%,#030304);
border:1.5px solid rgba(255,255,255,.3);border-radius:24px;
box-shadow:inset 0 2px 2px rgba(255,255,255,.12),inset 0 -8px 18px rgba(0,0,0,.55),
0 5px 0 #020203,0 35px 75px rgba(0,0,0,.7),0 0 40px -17px rgba(160,107,255,.35);
display:flex;flex-direction:column;overflow:hidden}
.chat-head{display:flex;align-items:center;gap:14px;padding:20px 24px;border-bottom:1px solid rgba(255,255,255,.14)}
.chat-head .chat-ava{width:44px;height:44px}
.chat-head h2{font-family:Georgia,'Times New Roman',serif;font-size:20px;color:#fff;margin:0;letter-spacing:.02em;
text-shadow:0 2px 8px rgba(0,0,0,.8),0 0 22px rgba(255,255,255,.14)}
.chat-head .presence{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:#2fe89e}
.chat-scroll{position:relative;height:480px;overflow-y:auto;padding:22px 24px;scrollbar-width:thin;scrollbar-color:rgba(160,107,255,.6) transparent}
.chat-scroll::-webkit-scrollbar{width:8px}
.chat-scroll::-webkit-scrollbar-thumb{background:rgba(160,107,255,.5);border-radius:8px}
/* the date divider: serif voice, the room's chapter marks */
.chat-day{display:flex;align-items:center;gap:14px;margin:22px 0 14px}
.chat-day::before,.chat-day::after{content:"";flex:1;height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.35),transparent)}
.chat-day span{font-family:Georgia,'Times New Roman',serif;font-size:13px;letter-spacing:.22em;text-transform:uppercase;color:#fff;opacity:.92;white-space:nowrap}
.chat-day:first-child{margin-top:2px}
/* the scroll pill: a real button, a kept promise */
.chat-new{position:sticky;bottom:12px;margin:0 auto;transform:translateX(0);display:flex;align-items:center;gap:8px;
min-height:44px;padding:10px 20px;border-radius:999px;background:#050505;color:#fff;font-size:14px;cursor:pointer;
border:1.5px solid rgba(255,255,255,.85);box-shadow:0 10px 30px rgba(0,0,0,.7);
transition:transform .18s cubic-bezier(.16,.84,.22,1),border-color .18s,box-shadow .18s;z-index:5}
.chat-new[hidden]{display:none}
.chat-new:hover{transform:translateY(-2px);border-color:#a06bff;box-shadow:0 0 26px rgba(160,107,255,.55),0 12px 30px rgba(0,0,0,.7)}
.chat-new:active{transform:translateY(1px)}
.chat-new:focus-visible{outline:2px solid #fff;outline-offset:3px}
.chat-new svg{width:14px;height:14px;stroke:#fff;fill:none;stroke-width:2.2}
.chat-new .n{display:grid;place-items:center;min-width:22px;height:22px;border-radius:999px;background:#a06bff;
font-size:12px;font-weight:700;padding:0 6px;box-shadow:0 0 12px rgba(160,107,255,.8)}
/* honest empty room */
.chat-empty{text-align:center;padding:72px 24px}
.chat-empty .jewel{width:38px;height:38px;margin:0 auto 20px;transform:rotate(45deg);border-radius:9px;
background:radial-gradient(circle at 35% 30%,#fff,#a06bff 45%,#050507 92%);
border:1.5px solid rgba(255,255,255,.85);box-shadow:0 0 34px rgba(160,107,255,.6)}
.chat-empty h3{font-family:Georgia,'Times New Roman',serif;font-size:22px;color:#fff;margin:0 0 10px}
.chat-empty p{font-size:15px;color:#fff;opacity:.9;margin:0}
/* honest loading: words, not fake bubbles */
.chat-loading{text-align:center;padding:40px 20px;font-size:14px;color:#fff;opacity:.75;letter-spacing:.06em}
.chat-loading i{display:inline-block;width:10px;height:10px;margin-right:10px;border-radius:50%;background:#a06bff;
box-shadow:0 0 12px rgba(160,107,255,.9);animation:chat-breathe .833s ease-in-out infinite;vertical-align:baseline}
@media (prefers-reduced-motion:reduce){.chat-new,.chat-loading i{transition:none;animation:none}}
</style>
<div class="chat chat-list">
  <div class="chat-head">
    <div class="chat-ava" aria-hidden="true"></div>
    <div>
      <h2>Studio channel</h2>
      <p class="presence" style="margin:4px 0 0">3 here now</p>
    </div>
  </div>
  <div class="chat-scroll" id="chatScroll" tabindex="0" aria-label="Messages">
    <div class="chat-day" role="separator"><span>Yesterday · Oct 15</span></div>
    <div class="chat-row grp-first">
      <div class="chat-ava in" aria-hidden="true"></div>
      <div><div class="chat-bub in">The Hub is live. Watch the feed.</div>
      <div class="chat-meta"><span class="chat-name">Sam</span><span class="chat-time">21:02</span></div></div>
    </div>
    <div class="chat-day" role="separator"><span>Today · Oct 16</span></div>
    <div class="chat-row out">
      <div class="chat-ava" aria-hidden="true"></div>
      <div><div class="chat-bub out">Seeing it. Smart Note landed in seconds.</div>
      <div class="chat-meta"><span class="chat-time">09:14</span>
        <span class="chat-ticks" data-state="read" role="img" aria-label="Read"><span class="sr">Read</span>
        <svg viewBox="0 0 24 24"><path d="M2.5 12.5l4.5 4.5L14 9.5" fill="none" stroke="#ffbf3d" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/><path d="M10 15.5l1.8 1.8L21 8" fill="none" stroke="#ffbf3d" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </span></div></div>
    </div>
    <button class="chat-new" id="chatNew" hidden>
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 4v16m0 0l-6-6m6 6l6-6"/></svg>
      <span>New messages</span><span class="n" id="chatNewN">2</span>
    </button>
  </div>
</div>

<div class="chat chat-list" style="margin-top:28px" aria-label="Empty conversation example">
  <div class="chat-head">
    <div class="chat-ava" aria-hidden="true"></div>
    <div><h2>New channel</h2><p class="presence" style="margin:4px 0 0;color:#fff;opacity:.6">just you</p></div>
  </div>
  <div class="chat-empty">
    <div class="jewel" aria-hidden="true"></div>
    <h3>No messages yet</h3>
    <p>Say the first word.</p>
  </div>
</div>
<script>
/* The scroll contract. appendBubble() is the ONLY writer of new rows.
   Rule: stick to bottom only if already there (within 64px). Otherwise the
   pill counts honestly and the reader is never yanked. */
(function(){
  const sc=document.getElementById('chatScroll'),pill=document.getElementById('chatNew'),
        n=document.getElementById('chatNewN');
  const EDGE=64;let unread=0;
  function atBottom(){return sc.scrollHeight-sc.scrollTop-sc.clientHeight<=EDGE;}
  function render(){pill.hidden=unread===0;n.textContent=unread;}
  sc.addEventListener('scroll',()=>{if(atBottom()&&unread>0){unread=0;render();}},{passive:true});
  pill.addEventListener('click',()=>{sc.scrollTop=sc.scrollHeight;unread=0;render();pill.blur();});
  window.chatAppend=function(rowEl){
    const wasDown=atBottom();
    sc.insertBefore(rowEl,pill);
    if(wasDown){sc.scrollTop=sc.scrollHeight;}
    else{unread++;render();}
  };
  /* Presence line contract: "N here now" renders only from a live presence
     feed. No feed, no line — the head shows the name alone. Never a guess. */
})();
</script>
```

The scroll pill is `position:sticky` at the list's bottom so it floats over
the latest rows without covering the composer's future home below the list.
The specimen freezes October 16 as today for teaching; a live build renders
dividers from the viewer's clock.

### States

- **Rest:** board with 5-layer shadow, header (avatar orb + serif room name +
presence line), the scroll region, day dividers in serif voice. Bubbles rest
per CHT-003.
- **Day divider:** a serif, letterspaced, uppercase chapter mark —
"Today · Oct 16" — hairline rules fading both ways. Groups never cross a
divider (CHT-003's grouping rule stops at midnight); the divider is the
hard boundary.
- **New message, reader at bottom:** the row appends and the list glides to
it. One smooth motion — the reader was already there, so nothing is taken
from them.
- **New message, reader up-list:** the list does not move. The pill appears —
"New messages" with the honest count — chrome-purple badge, 44px target. It
is a real button and it keeps its promise: one tap, bottom reached, count
clears.
- **Reader scrolls home:** touching the bottom edge clears the pill. The
contract resolves itself; no button needed.
- **Empty:** centered purple jewel, serif "No messages yet", 15px "Say the
first word." No fake suggestions, no grayed ghost bubbles, no "start with
hi 👋" — an empty room is a state with dignity.
- **Loading history:** one line — "Loading your messages…" with a single
breathing orb. Words, never fake bubbles. Skeleton screens shaped like
messages are messages that lie; this block refuses them.
- **Presence:** "3 here now" in green, uppercase, letterspaced — rendered
only from a live presence feed. No feed, no line. A guessed headcount is a
forgery of company.

### Do / Don't

**Do** measure `atBottom()` *before* the row lands — the decision to move
belongs to the moment before the world changed, not after. **Don't** smooth-
scroll a reading user to the bottom "because something arrived"; yanking a
reader mid-sentence is the chat equivalent of grabbing their book. The pill
is the polite knock; the yank is the shove.

### Anatomy

- **Board:** the room — 5-layer board shadow, 24px radius, tone under-glow.
The room is the world; bubbles live inside it.
- **Header:** the warm front door — 44px avatar orb, serif room name (20px),
presence line. Full width of the board.
- **Scroll region:** 480px tall, thin purple scrollbar. `tabindex="0"` so
keyboard users can enter the list; the region is the conversation's body.
- **Date divider:** serif voice chapter marks. The family's TYPE law at chat
scale — the one place the calendar family's serif weekday row has a cousin.
- **Scroll pill:** the contract made visible — sticky, 44px, chrome ignition,
honest count badge. A pill that promises "new messages" and delivers them.
- **Empty state:** jewel + two lines, verbatim: "No messages yet — say the
first word." The em dash and the invitation are both specified; the words
do not improvise.
- **Loading state:** one breathing orb + one honest sentence. Loading is a
state with words, not shapes.

**What it will NOT fake:** it never auto-scrolls a reader who isn't at the
bottom — the 64px edge is measured, not assumed. The "N new messages" count
is the real count of rows appended while away, never a badge for decoration.
It never renders divider labels for days with no messages on either side —
a divider marks a boundary between real rows, never an empty chapter. It
never shows a presence count without a live feed, never shows "online" from
a last-seen timestamp, and never renders fake message-shaped skeletons while
loading. The empty state never suggests what to say — "say the first word"
is an invitation, not a prompt.

---

## Family notes

- **One meaning per color, everywhere:** the family table at the top is the contract. Purple is "my voice" on an outgoing bubble, in an outgoing avatar orb, and on the scroll pill's badge — choosing intelligence, going out. Gold is "seen" on a read receipt and nowhere else. White-lit edges are the world speaking in. If a new signal needs a color, it takes the next wheel stop — the wheel continues, it never restarts.
- **Truth-states are the family spine:** CHT-003's receipts, CHT-004's signal-gated dots, CHT-005's measured scroll edge and live-only presence — every block in this family refuses to perform a state it does not have. That refusal is the design.
- **Private by default:** message content renders inside bubbles and nowhere else — no log lines, no notification previews in this spec's scope, no search-index snippets. The block is given text and renders text; what leaves the bubble is the app's decision, documented as the app's, never the block's.
- **What the family does not cover:** message composers, voice notes, reactions, threads/replies, and search are real needs and are *not* specified here — they are future blocks (CHT-004+), not implied features of these three. Nothing in these specs pretends they exist.
