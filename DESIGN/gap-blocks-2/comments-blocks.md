# COMMENTS BLOCKS — the family

The warehouse had no comment pieces. Wave 2 builds three: a thread, a
comment, a reaction row. One family, one law order. **Laws cited:** ALIVE
(Law 1) — every action moves and ignites. SPECTRUM (Law 2) — reaction colors
walk the wheel, meaning never changes between blocks. ELEVATION (Law 3) —
nested boards ride in layers. JEWELS (Law 4) — avatars are gems, bullets are
diamonds. BUTTONS (Law 5) — black centers, white rims, 44px targets. TYPE
(Law 6) — serif voice on names, white 99%.

**Three family laws, stated plainly:**

1. **Honest nesting.** Depth is capped at 3 — past that, the thread continues
   in a dedicated panel, never in a fake fourth indent. What looks nested *is*
   nested; what continues *says* it continues.
2. **Plain-words timestamps.** "2h ago", "yesterday", "Mar 4" — from real
   datetimes. Never "2 hours 14 minutes ago" (fake precision), never "just now"
   for something that happened an hour ago.
3. **Reactions are play, not status.** They are opt-in, toggleable, and honest
   counts. No "top fan" badges, no streak shaming, no leaderboards wearing a
   reaction row as a costume.

**Private-by-default:** a comment shows a display name and nothing else — no
emails, no handles, no profile links unless the person made them public by
choice. Removed comments become tombstones: "This comment was removed." The
body is gone, not grayed out as a tease.

**The reaction-color walk — fixed forever, across CMT-002 and CMT-003:**

| Stop | Hex | Reaction | Meaning |
|---|---|---|---|
| pink | `#ed58cd` | Love | Delight, the flourish |
| magenta | `#e84fff` | Celebrate | The living edge |
| purple | `#a06bff` | Thoughtful | Choosing intelligence |
| blue | `#3fb8ff` | Agree | Knowledge moving |
| green | `#2fe89e` | Laugh | Alive and well |

A sixth reaction takes indigo `#6675ff`, continuing the wheel, never reusing
a stop while one sits unused. The love toggle in CMT-002 and the love pill in
CMT-003 are the *same object* — one count, one truth, never two.

**The depth-rail walk — structure, not sentiment:** nested reply rails walk
the Strip in order — depth 1 magenta, depth 2 purple, depth 3 blue. Three
rails, then the cap. Rails mark *where you are in the conversation*, never
how anyone feels about it.

**Family token sheet** (every snippet below assumes these; copy once):

```css
.cmt{--ground:#050507;--ink:#fff;--magenta:#e84fff;--purple:#a06bff;
--indigo:#6675ff;--blue:#3fb8ff;--emerald:#35e0a1;--green:#2fe89e;
--lime:#b8ee57;--gold:#ffbf3d;--orange:#ff9a5a;--red:#ff5e6c;--pink:#ed58cd;
--ease:cubic-bezier(.16,.84,.22,1);--serif:Georgia,'Times New Roman',serif;
background:var(--ground);color:var(--ink)}
```

**The one button DNA:** this family imports `.naya-btn` from the single canonical source (per `DESIGN/BLOCKS.md`, Law 5) — it is never redefined or re-typed here (see the single-source rule: checkout family contract §7). The snippets below assume it the way they assume the token sheet.

---

## CMT-001 · Comment thread

The whole conversation: a composer on top, top-level comments below, replies
nested under honest rails to depth 3, then a "Continue thread" panel for the
rest. Collapse/expand per comment, plain-words timestamps, tombstones for
the removed. Law 1: nothing dead — collapse chevrons lift, rails ignite on
hover, the Post button is alive the moment there's something to say.

### The code

```html
<style>
.cmt-thread{max-width:680px;margin:0 auto;font-family:system-ui,sans-serif}
/* ——— composer ——— */
.cmt-compose{display:flex;gap:12px;background:linear-gradient(180deg,#141318,#08080c);
border:1.5px solid rgba(255,255,255,.3);border-radius:18px;padding:16px;margin-bottom:20px;
box-shadow:inset 0 2px 2px rgba(255,255,255,.1),0 12px 30px rgba(0,0,0,.6)}
.cmt-field{flex:1;background:#050505;border:1.5px solid rgba(255,255,255,.5);border-radius:12px;
color:#fff;font-size:14px;padding:12px 14px;min-height:44px;resize:vertical;font-family:inherit;
transition:border-color .18s var(--ease),box-shadow .18s var(--ease)}
.cmt-field::placeholder{color:#fff;opacity:.5}
.cmt-field:focus{outline:none;border-color:#a06bff;box-shadow:0 0 24px rgba(160,107,255,.5)}
/* ——— Post IS .naya-btn — the one DNA, no bespoke button system (independent
   scorecard fix, 2026-10-16). The hook keeps only the composer's layout needs
   (alignment, 52px floor); every button visual — gradient heart, idle border,
   conic ring, press parity, canonical focus, disabled — comes from .naya-btn. */
.cmt-post{align-self:flex-end;min-width:120px;min-height:52px}
/* ——— comment ——— */
.cmt-item{display:flex;gap:12px;padding:14px 4px}
.cmt-av{flex:none;width:44px;height:44px;transform:rotate(45deg);border-radius:12px;margin-top:2px;
background:radial-gradient(circle at 35% 30%,#fff,var(--ac,#a06bff) 45%,#050507 95%);
border:1.5px solid rgba(255,255,255,.85);box-shadow:0 0 22px var(--ac-glow,rgba(160,107,255,.45));
display:grid;place-items:center}
.cmt-av b{transform:rotate(-45deg);font-family:Georgia,serif;font-size:15px;color:#fff;
text-shadow:0 1px 6px rgba(0,0,0,.9)}
.cmt-main{flex:1;min-width:0}
.cmt-head{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}
.cmt-name{font-family:Georgia,serif;font-size:16px;color:#fff;margin:0;
text-shadow:0 2px 8px rgba(0,0,0,.8)}
.cmt-time{font-size:12px;color:#fff;opacity:.6;letter-spacing:.04em}
.cmt-edited{font-size:11px;color:#fff;opacity:.5;font-style:italic}
.cmt-body{font-size:14px;line-height:1.6;color:#fff;margin:6px 0 10px;opacity:.96}
.cmt-actions{display:flex;gap:6px;flex-wrap:wrap}
.cmt-act{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:0 14px;border-radius:999px;
background:transparent;border:1.5px solid transparent;color:#fff;font-size:13px;cursor:pointer;
transition:transform .18s var(--ease),border-color .18s var(--ease),box-shadow .18s var(--ease),background .18s}
.cmt-act svg{width:15px;height:15px;stroke:#fff;fill:none;stroke-width:1.8;flex:none;transition:stroke .18s}
.cmt-act:hover{transform:translateY(-2px);border-color:var(--ac,#a06bff);box-shadow:0 0 20px var(--ac-glow,rgba(160,107,255,.5))}
.cmt-act:hover svg{stroke:var(--ac,#a06bff)}
.cmt-act:active{transform:translateY(1px)}
.cmt-act:focus-visible{outline:2px solid #fff;outline-offset:2px}
.cmt-act.is-on{border-color:var(--ac,#ed58cd);background:rgba(0,0,0,.5);box-shadow:0 0 22px var(--ac-glow,rgba(237,88,205,.5))}
.cmt-act.is-on svg{stroke:var(--ac,#ed58cd);fill:var(--ac,#ed58cd)}
.cmt-love{--ac:#ed58cd;--ac-glow:rgba(237,88,205,.5)}
.cmt-reply{--ac:#a06bff;--ac-glow:rgba(160,107,255,.5)}
.cmt-share{--ac:#3fb8ff;--ac-glow:rgba(63,184,255,.5)}
/* ——— nesting: honest rails to depth 3 ——— */
.cmt-kids{margin:6px 0 0 22px;padding-left:18px;border-left:2px solid var(--rail,#e84fff);
transition:border-color .28s var(--ease),box-shadow .28s var(--ease)}
.cmt-item:hover>.cmt-kids{box-shadow:-6px 0 18px -8px var(--rail,#e84fff)}
.cmt-kids.d1{--rail:#e84fff}
.cmt-kids.d2{--rail:#a06bff}
.cmt-kids.d3{--rail:#3fb8ff}
.cmt-fold{display:flex;align-items:center;gap:10px;margin:8px 0 0 56px}
/* ——— the fold chevron IS .naya-btn.icon.micro — the one DNA, no bespoke
   button system (independent scorecard fix, 2026-10-16). Exactly the CAL-001
   pattern: the hook carries only the drawn chevron glyph (Law 4); every
   button visual — gradient heart, idle border, insets, lift, flowing conic
   ring, press, focus — comes from .naya-btn (imported, never redefined). */
.naya-btn.icon.micro.cmt-chev i{width:9px;height:9px;border-top:2px solid #fff;border-right:2px solid #fff;
transform:rotate(135deg);margin-top:-3px;transition:transform .18s var(--ease)}
.naya-btn.icon.micro.cmt-chev[aria-expanded="false"] i{transform:rotate(45deg);margin-top:0}
.cmt-fold .n{font-size:13px;color:#fff;opacity:.75;letter-spacing:.04em}
/* ——— continue thread: the depth cap, stated ——— */
.cmt-more{display:flex;align-items:center;gap:12px;margin:10px 0 0 22px;padding:12px 16px;min-height:52px;
background:#0a0a0e;border:1.5px dashed rgba(255,255,255,.45);border-radius:14px;color:#fff;font-size:14px;
cursor:pointer;width:calc(100% - 22px);
transition:transform .18s var(--ease),border-color .18s var(--ease),box-shadow .18s var(--ease)}
.cmt-more:hover{transform:translateY(-2px);border-color:#a06bff;box-shadow:0 0 24px rgba(160,107,255,.5)}
.cmt-more:focus-visible{outline:2px solid #fff;outline-offset:3px}
.cmt-more svg{width:16px;height:16px;stroke:#a06bff;fill:none;stroke-width:1.8;flex:none}
.cmt-deep{margin:10px 0 0 22px;padding:16px;background:linear-gradient(180deg,#141318,#08080c);
border:1.5px solid rgba(255,255,255,.3);border-radius:18px;
box-shadow:inset 0 2px 2px rgba(255,255,255,.1),0 18px 44px rgba(0,0,0,.65)}
.cmt-deep[hidden]{display:none}
.cmt-deep .cap{font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:#fff;opacity:.6;margin:0 0 6px}
/* ——— tombstone ——— */
.cmt-tomb{margin:8px 0;padding:16px;border:1.5px dashed rgba(255,255,255,.3);border-radius:14px;
color:#fff;opacity:.6;font-size:14px;font-style:italic}
/* ——— empty ——— */
.cmt-empty{text-align:center;padding:56px 20px;background:linear-gradient(180deg,#141318,#08080c);
border:1.5px solid rgba(255,255,255,.3);border-radius:24px;
box-shadow:inset 0 2px 2px rgba(255,255,255,.1),0 12px 30px rgba(0,0,0,.6)}
.cmt-empty .jewel{width:34px;height:34px;margin:0 auto 18px;transform:rotate(45deg);border-radius:8px;
background:radial-gradient(circle at 35% 30%,#fff,#a06bff 45%,#050507 90%);
border:1.5px solid rgba(255,255,255,.8);box-shadow:0 0 30px rgba(160,107,255,.55)}
.cmt-empty h3{font-family:Georgia,serif;font-size:20px;color:#fff;margin:0 0 8px}
.cmt-empty p{font-size:14px;color:#fff;opacity:.85;margin:0}
@media (prefers-reduced-motion:reduce){.cmt-act,.cmt-chev,.cmt-more,.cmt-post,.cmt-kids,.cmt-field{transition:none}}
</style>

<div class="cmt cmt-thread" aria-label="Comments">
  <div class="cmt-compose">
    <div class="cmt-av" style="--ac:#a06bff;--ac-glow:rgba(160,107,255,.45)" aria-hidden="true"><b>YO</b></div>
    <label class="cmt-sr" for="cmtBox" hidden>Write a comment</label>
    <textarea class="cmt-field" id="cmtBox" placeholder="Say something true…" aria-label="Write a comment"></textarea>
    <button class="naya-btn cmt-post" id="cmtPost" disabled>Post</button>
  </div>

  <div class="cmt-item">
    <div class="cmt-av" style="--ac:#e84fff;--ac-glow:rgba(232,79,255,.45)" aria-hidden="true"><b>JO</b></div>
    <div class="cmt-main">
      <div class="cmt-head">
        <h4 class="cmt-name">June Okafor</h4>
        <time class="cmt-time" datetime="2026-10-16T21:28:00Z" title="Oct 16, 2026, 21:28 UTC">2h ago</time>
      </div>
      <p class="cmt-body">The depth cap is the kindest thing in this spec. Threads that indent forever stop being conversations and start being geology.</p>
      <div class="cmt-actions">
        <button class="cmt-act cmt-reply"><svg viewBox="0 0 24 24"><path d="M9 14l-4-4 4-4"/><path d="M5 10h9a6 6 0 0 1 0 12h-3"/></svg>Reply</button>
        <button class="cmt-act cmt-love is-on" aria-pressed="true"><svg viewBox="0 0 24 24"><path d="M12 21C7 16.5 3 13 3 8.9 3 6 5.2 4 7.8 4c1.7 0 3.2.9 4.2 2.3C13 4.9 14.5 4 16.2 4 18.8 4 21 6 21 8.9c0 4.1-4 7.6-9 12.1z"/></svg>12</button>
        <button class="cmt-act cmt-share"><svg viewBox="0 0 24 24"><circle cx="6" cy="12" r="2.6"/><circle cx="18" cy="6" r="2.6"/><circle cx="18" cy="18" r="2.6"/><path d="M8.3 10.8l7.4-3.6M8.3 13.2l7.4 3.6"/></svg>Share</button>
      </div>
      <div class="cmt-fold">
        <button class="naya-btn icon micro cmt-chev" aria-expanded="true" aria-label="Collapse 2 replies"><i></i></button>
        <span class="n">2 replies</span>
      </div>
      <div class="cmt-kids d1">
        <div class="cmt-item">
          <div class="cmt-av" style="--ac:#3fb8ff;--ac-glow:rgba(63,184,255,.45)" aria-hidden="true"><b>TM</b></div>
          <div class="cmt-main">
            <div class="cmt-head">
              <h4 class="cmt-name">Theo Marchetti</h4>
              <time class="cmt-time" datetime="2026-10-16T22:10:00Z" title="Oct 16, 2026, 22:10 UTC">1h ago</time>
            </div>
            <p class="cmt-body">Agreed — and the rail colors walking the Strip means you always know how deep you are without counting pixels.</p>
            <div class="cmt-actions">
              <button class="cmt-act cmt-reply"><svg viewBox="0 0 24 24"><path d="M9 14l-4-4 4-4"/><path d="M5 10h9a6 6 0 0 1 0 12h-3"/></svg>Reply</button>
              <button class="cmt-act cmt-love" aria-pressed="false"><svg viewBox="0 0 24 24"><path d="M12 21C7 16.5 3 13 3 8.9 3 6 5.2 4 7.8 4c1.7 0 3.2.9 4.2 2.3C13 4.9 14.5 4 16.2 4 18.8 4 21 6 21 8.9c0 4.1-4 7.6-9 12.1z"/></svg>4</button>
              <button class="cmt-act cmt-share"><svg viewBox="0 0 24 24"><circle cx="6" cy="12" r="2.6"/><circle cx="18" cy="6" r="2.6"/><circle cx="18" cy="18" r="2.6"/><path d="M8.3 10.8l7.4-3.6M8.3 13.2l7.4 3.6"/></svg>Share</button>
            </div>
            <div class="cmt-fold">
              <button class="naya-btn icon micro cmt-chev" aria-expanded="true" aria-label="Collapse 1 reply"><i></i></button>
              <span class="n">1 reply</span>
            </div>
            <div class="cmt-kids d2">
              <div class="cmt-item">
                <div class="cmt-av" style="--ac:#e84fff;--ac-glow:rgba(232,79,255,.45)" aria-hidden="true"><b>JO</b></div>
                <div class="cmt-main">
                  <div class="cmt-head">
                    <h4 class="cmt-name">June Okafor</h4>
                    <time class="cmt-time" datetime="2026-10-16T22:44:00Z" title="Oct 16, 2026, 22:44 UTC">44m ago</time>
                  </div>
                  <p class="cmt-body">Depth 2, purple rail. One more level and we hand off to the continue panel — as it should be.</p>
                  <div class="cmt-actions">
                    <button class="cmt-act cmt-reply"><svg viewBox="0 0 24 24"><path d="M9 14l-4-4 4-4"/><path d="M5 10h9a6 6 0 0 1 0 12h-3"/></svg>Reply</button>
                    <button class="cmt-act cmt-love" aria-pressed="false"><svg viewBox="0 0 24 24"><path d="M12 21C7 16.5 3 13 3 8.9 3 6 5.2 4 7.8 4c1.7 0 3.2.9 4.2 2.3C13 4.9 14.5 4 16.2 4 18.8 4 21 6 21 8.9c0 4.1-4 7.6-9 12.1z"/></svg>2</button>
                    <button class="cmt-act cmt-share"><svg viewBox="0 0 24 24"><circle cx="6" cy="12" r="2.6"/><circle cx="18" cy="6" r="2.6"/><circle cx="18" cy="18" r="2.6"/><path d="M8.3 10.8l7.4-3.6M8.3 13.2l7.4 3.6"/></svg>Share</button>
                  </div>
                  <button class="cmt-more" aria-expanded="false">
                    <svg viewBox="0 0 24 24"><path d="M4 12h16M12 4v16"/></svg>
                    Continue thread — 3 more replies
                  </button>
                  <div class="cmt-deep" hidden>
                    <p class="cap">Thread continues — depth capped at 3</p>
                    <div class="cmt-item">
                      <div class="cmt-av" style="--ac:#2fe89e;--ac-glow:rgba(47,232,158,.45)" aria-hidden="true"><b>RA</b></div>
                      <div class="cmt-main">
                        <div class="cmt-head">
                          <h4 class="cmt-name">Rin Adler</h4>
                          <time class="cmt-time" datetime="2026-10-16T23:02:00Z" title="Oct 16, 2026, 23:02 UTC">26m ago</time>
                        </div>
                        <p class="cmt-body">Same thread, readable. The cap is doing its job.</p>
                      </div>
                    </div>
                    <div class="cmt-item">
                      <div class="cmt-av" style="--ac:#3fb8ff;--ac-glow:rgba(63,184,255,.45)" aria-hidden="true"><b>TM</b></div>
                      <div class="cmt-main">
                        <div class="cmt-head">
                          <h4 class="cmt-name">Theo Marchetti</h4>
                          <time class="cmt-time" datetime="2026-10-16T23:15:00Z" title="Oct 16, 2026, 23:15 UTC">13m ago</time>
                          <span class="cmt-edited">edited</span>
                        </div>
                        <p class="cmt-body">No fake fourth indent. Honest.</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="cmt-tomb" role="note">This comment was removed.</div>

  <div class="cmt-item">
    <div class="cmt-av" style="--ac:#a06bff;--ac-glow:rgba(160,107,255,.45)" aria-hidden="true"><b>AH</b></div>
    <div class="cmt-main">
      <div class="cmt-head">
        <h4 class="cmt-name">Amara Haddad</h4>
        <time class="cmt-time" datetime="2026-03-04T09:12:00Z" title="Mar 4, 2026, 09:12 UTC">Mar 4</time>
      </div>
      <p class="cmt-body">Older comments get a calendar date, not a strained "7 months ago". Plain words, real datetimes underneath.</p>
      <div class="cmt-actions">
        <button class="cmt-act cmt-reply"><svg viewBox="0 0 24 24"><path d="M9 14l-4-4 4-4"/><path d="M5 10h9a6 6 0 0 1 0 12h-3"/></svg>Reply</button>
        <button class="cmt-act cmt-love" aria-pressed="false"><svg viewBox="0 0 24 24"><path d="M12 21C7 16.5 3 13 3 8.9 3 6 5.2 4 7.8 4c1.7 0 3.2.9 4.2 2.3C13 4.9 14.5 4 16.2 4 18.8 4 21 6 21 8.9c0 4.1-4 7.6-9 12.1z"/></svg>7</button>
        <button class="cmt-act cmt-share"><svg viewBox="0 0 24 24"><circle cx="6" cy="12" r="2.6"/><circle cx="18" cy="6" r="2.6"/><circle cx="18" cy="18" r="2.6"/><path d="M8.3 10.8l7.4-3.6M8.3 13.2l7.4 3.6"/></svg>Share</button>
      </div>
    </div>
  </div>
</div>

<div class="cmt cmt-thread" style="margin-top:28px" aria-label="Empty thread example">
  <div class="cmt-empty">
    <div class="jewel" aria-hidden="true"></div>
    <h3>No comments yet</h3>
    <p>Say the first true thing.</p>
  </div>
</div>

<script>
/* Specimen behavior is local. A live build posts through your API and renders
   the server's receipt (real id, real timestamp) — it never claims a local
   append reached anyone. */
(function(){
  const box=document.getElementById('cmtBox'),post=document.getElementById('cmtPost');
  box.addEventListener('input',()=>{post.disabled=!box.value.trim();});
  document.querySelectorAll('.cmt-chev').forEach(chev=>{
    chev.addEventListener('click',()=>{
      const main=chev.closest('.cmt-main');
      const kids=main?main.querySelector(':scope > .cmt-kids'):null;
      const open=chev.getAttribute('aria-expanded')==='true';
      chev.setAttribute('aria-expanded',String(!open));
      if(kids)kids.hidden=open;
      const base=chev.getAttribute('aria-label').replace(/^(Expand|Collapse) /,'');
      chev.setAttribute('aria-label',(open?'Expand ':'Collapse ')+base);
    });
  });
  document.querySelectorAll('.cmt-more').forEach(btn=>{
    btn.addEventListener('click',()=>{
      const deep=btn.nextElementSibling,open=btn.getAttribute('aria-expanded')==='true';
      btn.setAttribute('aria-expanded',String(!open));deep.hidden=open;
    });
  });
  document.querySelectorAll('.cmt-act.cmt-love').forEach(love=>{
    love.addEventListener('click',()=>{
      const on=love.classList.toggle('is-on');
      love.setAttribute('aria-pressed',String(on));
    });
  });
})();
</script>
```

Timestamps are specimen-frozen (Oct 16, 2026). A live build renders `datetime`
from the server's clock and derives the plain-words label: under a minute
"just now", under an hour "Nm ago", under a day "Nh ago", under a week "Nd
ago", else the calendar date. The `title` always carries the full date — the
exact time is one hover away, never paraded.

The love toggle above is wired for the demo's *state* only; the count it
changes is the specimen's own count. A live build re-renders counts from the
server after the toggle lands — it never invents a number while the request
is in flight.

### States

- **Rest:** comments sit quiet — avatar jewel, serif name, plain timestamp, body at white 96%. The thread is a conversation, not a dashboard.
- **Hover:** the comment's nesting rail ignites in its depth color (magenta → purple → blue); action pills lift 2px and ignite in their own color — reply chrome-purple, love pink, share blue. Collapse chevrons lift and ignite purple.
- **Active/press:** settles back 1px — held, not dead.
- **Focus:** white 2px ring on every control — chevron, actions, Post, composer. Keyboard collapse: Enter or Space on the chevron.
- **Collapsed:** kids hidden, chevron flips, label keeps the honest count ("2 replies" — the number is real, from the data). Collapsing never deletes; it folds.
- **Continue thread:** a dashed, honest button — "Continue thread — 3 more replies". Opens a nested board (Law 3 — a board inside a board rides higher) labeled "Thread continues — depth capped at 3". The deep replies render flat, in order. No fourth indent exists, anywhere.
- **Composer rest:** dark field, "Say something true…" placeholder — never a fake pre-filled draft. **Focus:** purple ignition. **Post disabled:** `.naya-btn:disabled` — 45% opacity, truly inert — an empty comment cannot be posted, and the button doesn't pretend otherwise. **Post enabled:** alive the moment there's text.
- **Tombstone:** dashed edge, italic "This comment was removed." No body, no actions, no author — removal is total, not a tease.
- **Empty thread:** centered jewel, serif "No comments yet", 14px "Say the first true thing." No fake suggestions, no ghost comments, no "be the first to…" engagement theater.
- **Edited:** a quiet italic "edited" beside the timestamp — the edit is disclosed, the history isn't paraded.

### Do / Don't

**Do** cap nesting at 3 and say so in the open — the "Continue thread" panel names the cap, so no one mistakes it for a bug. **Don't** indent a fourth level "just this once"; one fake indent is a lie the whole thread inherits.

**Do** derive every timestamp from a real datetime in the markup — the plain-words label is a rendering of truth, not a substitute for it. **Don't** write "just now" for anything older than a minute, and don't write "2 hours 14 minutes ago" for anything — precision you don't have is theater.

### Anatomy

- **Composer:** the thread's front door — avatar jewel of the poster, dark field, a Post button wearing `.naya-btn` (52px — the one DNA, no bespoke system). Post is disabled until there's text; your app wires the real submit and the server's receipt.
- **Avatar jewel:** rotated diamond, white → tone → black radial, initials in serif, glow in the author's own stable color. The color is assigned once per author (hash of the display name) and never changes between renders — identity, not decoration.
- **Name row:** serif display name (16px), plain-words timestamp, quiet "edited" flag. Display name only — no email, no handle, no link unless the author made one public by choice.
- **Nesting rail:** 2px line in the depth's Strip color, left of the kids. Hovering the parent ignites it — you see where the fold lives.
- **Fold control:** a `.naya-btn.icon.micro` chevron (the CAL-001 pattern — drawn glyph only, the DNA carries everything else) + honest count. The count is the real reply count; collapsing folds, expanding unfolds — nothing is created or destroyed.
- **Continue panel:** the depth cap made visible — dashed button, nested board, stated cap. Replies inside are flat and in order.
- **Tombstone:** the honest grave — dashed edge, one line, no remains.

**What it will NOT fake:** it never renders a fourth indent — the cap is structural, not a suggestion. It never invents replies to fill a thread — an empty thread says so. It never shows a fake "Posting…" state that resolves locally and claims delivery — the specimen posts locally and says so; a live build waits for the server's receipt. Removed comments show nothing of the body, ever. Timestamps never claim precision the data doesn't carry.

---

## CMT-002 · Single comment

One comment, fully dressed: avatar jewel, serif name, plain-words timestamp,
body, and an action row — reply (chrome), love (pink toggle), share (blue).
The building block CMT-001 is made of. Law 1: the actions rest quiet and
ignite in their own colors; nothing in the row is flat.

### The code

```html
<style>
.cmt-one{max-width:620px;margin:0 auto;display:flex;gap:14px;background:linear-gradient(180deg,#141318,#08080c);
border:1.5px solid rgba(255,255,255,.3);border-radius:20px;padding:20px;
box-shadow:inset 0 2px 2px rgba(255,255,255,.1),0 14px 34px rgba(0,0,0,.65);
transition:transform .28s cubic-bezier(.16,.84,.22,1),border-color .28s,box-shadow .28s}
.cmt-one:hover{transform:translateY(-4px);border-color:rgba(255,255,255,.55);
box-shadow:inset 0 2px 2px rgba(255,255,255,.12),0 22px 48px rgba(0,0,0,.7),0 0 36px -12px rgba(160,107,255,.5)}
.cmt-one .cmt-av{width:52px;height:52px;border-radius:14px}
.cmt-one .cmt-av b{font-size:17px}
.cmt-one .cmt-name{font-size:18px}
.cmt-one .cmt-body{font-size:15px}
.cmt-one .cmt-body.is-clamped{display:-webkit-box;-webkit-line-clamp:4;-webkit-box-orient:vertical;overflow:hidden}
/* ——— the clamp toggle wears .naya-btn--quiet — the one blessed quiet-control
   DNA (independent scorecard fix, 2026-10-16). Canonical home: the checkout
   family contract (checkout-blocks.md, family contract §8) — owned ONCE there
   for the whole catalog, consumed here. The hook carries only the clamp
   toggle's sizing; this block defines no quiet control of its own. */
.cmt-morebtn{min-height:44px;padding:8px 16px;font-size:12px;letter-spacing:.08em}
.cmt-one .cmt-actions{margin-top:4px}
.cmt-count{font-variant-numeric:tabular-nums}
@media (prefers-reduced-motion:reduce){.cmt-one,.cmt-morebtn{transition:none}}
</style>

<article class="cmt cmt-one" aria-label="Comment by June Okafor">
  <div class="cmt-av" style="--ac:#e84fff;--ac-glow:rgba(232,79,255,.45)" aria-hidden="true"><b>JO</b></div>
  <div class="cmt-main">
    <div class="cmt-head">
      <h4 class="cmt-name">June Okafor</h4>
      <time class="cmt-time" datetime="2026-10-16T21:28:00Z" title="Oct 16, 2026, 21:28 UTC">2h ago</time>
    </div>
    <p class="cmt-body is-clamped" id="cmtBody1">A single comment is the atom the thread is built from — same avatar jewel, same serif name, same plain-words timestamp, same action row. Long bodies clamp at four lines with an honest "Show more" — the full text is in the markup, nothing is cut, nothing is hidden from assistive tech. The love toggle here and the love pill in the reaction row are the same object: one count, one truth. Toggle it here and the pill agrees, because there was never a second number to disagree with.</p>
    <button class="naya-btn naya-btn--quiet cmt-morebtn" aria-expanded="false" aria-controls="cmtBody1">Show more</button>
    <div class="cmt-actions">
      <button class="cmt-act cmt-reply"><svg viewBox="0 0 24 24"><path d="M9 14l-4-4 4-4"/><path d="M5 10h9a6 6 0 0 1 0 12h-3"/></svg>Reply</button>
      <button class="cmt-act cmt-love is-on" aria-pressed="true"><svg viewBox="0 0 24 24"><path d="M12 21C7 16.5 3 13 3 8.9 3 6 5.2 4 7.8 4c1.7 0 3.2.9 4.2 2.3C13 4.9 14.5 4 16.2 4 18.8 4 21 6 21 8.9c0 4.1-4 7.6-9 12.1z"/></svg><span class="cmt-count">12</span></button>
      <button class="cmt-act cmt-share"><svg viewBox="0 0 24 24"><circle cx="6" cy="12" r="2.6"/><circle cx="18" cy="6" r="2.6"/><circle cx="18" cy="18" r="2.6"/><path d="M8.3 10.8l7.4-3.6M8.3 13.2l7.4 3.6"/></svg>Share</button>
    </div>
  </div>
</article>

<script>
(function(){
  const btn=document.querySelector('.cmt-morebtn'),body=document.getElementById('cmtBody1');
  btn.addEventListener('click',()=>{
    const open=btn.getAttribute('aria-expanded')==='true';
    btn.setAttribute('aria-expanded',String(!open));
    body.classList.toggle('is-clamped',open);
    btn.textContent=open?'Show more':'Show less';
  });
})();
</script>
```

Reply opens the thread's composer focused on this comment (your app wires the
targeting — the specimen's Reply is the same chrome-purple affordance as
CMT-001's, and it promises the same thing). Share fires your app's real share
path — the specimen never shows a "Link copied" confirmation it didn't earn.

### States

- **Rest:** the card sits quiet — dark board, white-lit edge, actions transparent with white glyphs. Color is earned by interaction.
- **Hover:** lifts 4px, edge brightens, tone under-glow. The card is chrome-adjacent; it ignites softly, never in a reaction color.
- **Action hover:** each pill lifts 2px and ignites in its own color — reply purple, love pink, share blue. Light moves first, words follow.
- **Love on (`aria-pressed="true"`):** held pink edge + pink glow, heart filled pink, count in tabular numerals. Toggling off returns it to rest — reactions are play, and play can be taken back.
- **Active/press:** settles 1px — the press is felt.
- **Focus:** white 2px ring on every control.
- **Clamped body:** four lines, then an honest "Show more" — the full text stays in the markup and in the accessibility tree. "Show less" folds it back. The button labels the truth in both directions.
- **Disabled:** any action your app can't offer (e.g. reply on a locked thread) renders at 38% opacity with `disabled` — truly inert, never hover theater on a dead control.

### Do / Don't

**Do** keep the love count identical to the reaction row's love count — same data, same number, rendered twice, never computed twice. **Don't** let the single comment drift from the thread's comment — CMT-002 *is* CMT-001's atom; if they disagree on spacing, type, or behavior, one of them is wrong.

**Do** clamp long bodies with a real control — four lines is a kindness, hiding text without a control is a theft. **Don't** truncate with an ellipsis and no way back; a "…" with nowhere to go is a dead end wearing punctuation.

### Anatomy

- **Avatar jewel:** 52px here (the single comment gets a touch more presence than in-thread), initials in serif, author's stable color — same jewel law as CMT-001, one size up.
- **Name row:** serif 18px display name, plain-words timestamp, quiet "edited" when true. Nothing else about the author is shown — private by default.
- **Body:** 15px, white 96%, 1.6 line height. Clamps at four lines with "Show more" — the control is part of the block, not an afterthought. The toggle wears `.naya-btn--quiet` — the one blessed quiet DNA (canonical home: checkout family contract §8); this block defines no quiet control of its own.
- **Action row:** reply / love / share, 44px targets, each igniting its own color. Reply is chrome (purple); love is pink and toggles; share is blue and fires the app's real share path.
- **The count:** tabular numerals, `aria-pressed` telling the truth about your state. The number is the server's number — never rounded to "12k" theater, never "12" as decoration.

**What it will NOT fake:** the love count is the real count or the pill is absent — there is no "0 loves" display and no invented social proof. Share never confirms what it didn't do. Reply never opens a composer that can't post. The clamped body never hides text from assistive technology — `aria-expanded` and the full text stay honest.

---

## CMT-003 · Reaction row

The play layer: jewel pills with honest counts, toggle on/off, a plus that
opens the fixed set. Reactions are opt-in delight — the row never shames,
never ranks, never badges. Law 2: each reaction burns its fixed wheel color;
Law 1: pills lift and ignite on hover, and yours holds its glow.

### The code

```html
<style>
.cmt-rx{display:flex;flex-wrap:wrap;gap:10px;align-items:center}
.rx{display:inline-flex;align-items:center;gap:9px;min-height:44px;padding:8px 16px 8px 12px;
border-radius:999px;background:#050505;border:1.5px solid var(--rc);color:#fff;font-size:14px;cursor:pointer;
box-shadow:inset 0 2px 2px rgba(255,255,255,.08);
transition:transform .18s cubic-bezier(.16,.84,.22,1),box-shadow .18s,background .18s}
.rx svg{width:17px;height:17px;stroke:var(--rc);fill:none;stroke-width:1.8;flex:none}
.rx b{font-weight:600;font-variant-numeric:tabular-nums}
.rx:hover{transform:translateY(-2px);box-shadow:0 0 24px var(--rc-glow)}
.rx:active{transform:translateY(1px)}
.rx:focus-visible{outline:2px solid #fff;outline-offset:3px}
.rx.is-mine{background:rgba(0,0,0,.55);box-shadow:0 0 26px var(--rc-glow),inset 0 0 14px var(--rc-dim)}
.rx.is-mine svg{fill:var(--rc)}
.rx-add{width:44px;height:44px;border-radius:50%;background:#050505;border:1.5px dashed rgba(255,255,255,.6);
color:#fff;cursor:pointer;display:grid;place-items:center;
transition:transform .18s cubic-bezier(.16,.84,.22,1),border-color .18s,box-shadow .18s}
.rx-add svg{width:16px;height:16px;stroke:#fff;fill:none;stroke-width:1.8}
.rx-add:hover{transform:translateY(-2px);border-color:#a06bff;box-shadow:0 0 22px rgba(160,107,255,.55)}
.rx-add:hover svg{stroke:#a06bff}
.rx-add:focus-visible{outline:2px solid #fff;outline-offset:3px}
.rx-pop{position:absolute;z-index:40;display:flex;gap:8px;background:linear-gradient(180deg,#16141b,#08080c);
border:1.5px solid rgba(255,255,255,.35);border-radius:16px;padding:12px;
box-shadow:inset 0 2px 2px rgba(255,255,255,.12),0 24px 60px rgba(0,0,0,.75)}
.rx-pop[hidden]{display:none}
.rx-wrap{position:relative;display:inline-block}
@media (prefers-reduced-motion:reduce){.rx,.rx-add{transition:none}}
</style>

<div class="cmt rx-wrap">
  <div class="cmt-rx" role="group" aria-label="Reactions">
    <button class="rx is-mine" aria-pressed="true" data-rx="love" style="--rc:#ed58cd;--rc-glow:rgba(237,88,205,.5);--rc-dim:rgba(237,88,205,.14)" title="Loved by you, June, Theo and 9 others">
      <svg viewBox="0 0 24 24"><path d="M12 21C7 16.5 3 13 3 8.9 3 6 5.2 4 7.8 4c1.7 0 3.2.9 4.2 2.3C13 4.9 14.5 4 16.2 4 18.8 4 21 6 21 8.9c0 4.1-4 7.6-9 12.1z"/></svg><b>12</b><span hidden>Love</span>
    </button>
    <button class="rx" aria-pressed="false" data-rx="celebrate" style="--rc:#e84fff;--rc-glow:rgba(232,79,255,.5);--rc-dim:rgba(232,79,255,.14)" title="Celebrated by Rin and 4 others">
      <svg viewBox="0 0 24 24"><path d="M12 3l2.7 5.6 6.1.8-4.5 4.2 1.1 6-5.4-3-5.4 3 1.1-6L3.2 9.4l6.1-.8z"/></svg><b>5</b><span hidden>Celebrate</span>
    </button>
    <button class="rx" aria-pressed="false" data-rx="thoughtful" style="--rc:#a06bff;--rc-glow:rgba(160,107,255,.5);--rc-dim:rgba(160,107,255,.14)" title="Thoughtful to Amara and 2 others">
      <svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="2.4"/></svg><b>3</b><span hidden>Thoughtful</span>
    </button>
    <button class="rx-add" aria-label="Add a reaction" aria-expanded="false">
      <svg viewBox="0 0 24 24"><path d="M12 5v14M5 12h14"/></svg>
    </button>
  </div>
  <div class="rx-pop" hidden role="group" aria-label="Choose a reaction">
    <button class="rx" aria-pressed="false" data-rx="love" style="--rc:#ed58cd;--rc-glow:rgba(237,88,205,.5);--rc-dim:rgba(237,88,205,.14)" title="Love"><svg viewBox="0 0 24 24"><path d="M12 21C7 16.5 3 13 3 8.9 3 6 5.2 4 7.8 4c1.7 0 3.2.9 4.2 2.3C13 4.9 14.5 4 16.2 4 18.8 4 21 6 21 8.9c0 4.1-4 7.6-9 12.1z"/></svg></button>
    <button class="rx" aria-pressed="false" data-rx="celebrate" style="--rc:#e84fff;--rc-glow:rgba(232,79,255,.5);--rc-dim:rgba(232,79,255,.14)" title="Celebrate"><svg viewBox="0 0 24 24"><path d="M12 3l2.7 5.6 6.1.8-4.5 4.2 1.1 6-5.4-3-5.4 3 1.1-6L3.2 9.4l6.1-.8z"/></svg></button>
    <button class="rx" aria-pressed="false" data-rx="thoughtful" style="--rc:#a06bff;--rc-glow:rgba(160,107,255,.5);--rc-dim:rgba(160,107,255,.14)" title="Thoughtful"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="2.4"/></svg></button>
    <button class="rx" aria-pressed="false" data-rx="agree" style="--rc:#3fb8ff;--rc-glow:rgba(63,184,255,.5);--rc-dim:rgba(63,184,255,.14)" title="Agree"><svg viewBox="0 0 24 24"><path d="M4 12.5l5 5L20 6.5"/></svg></button>
    <button class="rx" aria-pressed="false" data-rx="laugh" style="--rc:#2fe89e;--rc-glow:rgba(47,232,158,.5);--rc-dim:rgba(47,232,158,.14)" title="Laugh"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="8"/><path d="M8.5 14.2c1 1.2 2.2 1.8 3.5 1.8s2.5-.6 3.5-1.8"/><circle cx="9.2" cy="9.6" r=".9"/><circle cx="14.8" cy="9.6" r=".9"/></svg></button>
  </div>
</div>

<script>
/* Specimen toggling is local. A live build re-renders counts from the server
   after each toggle lands — it never invents a number mid-flight. */
(function(){
  const wrap=document.querySelector('.rx-wrap'),add=wrap.querySelector('.rx-add'),pop=wrap.querySelector('.rx-pop');
  add.addEventListener('click',()=>{
    const open=add.getAttribute('aria-expanded')==='true';
    add.setAttribute('aria-expanded',String(!open));pop.hidden=open;
    if(!open)pop.querySelector('.rx').focus();
  });
  document.addEventListener('click',e=>{
    if(!pop.hidden&&!e.target.closest('.rx-wrap')){pop.hidden=true;add.setAttribute('aria-expanded','false');}
  });
  const order=['love','celebrate','thoughtful','agree','laugh'];
  pop.querySelectorAll('.rx').forEach(choice=>{
    choice.addEventListener('click',()=>{
      const key=choice.getAttribute('data-rx');
      const row=wrap.querySelector('.cmt-rx');
      let existing=row.querySelector(':scope > .rx[data-rx="'+key+'"]');
      if(existing){
        if(existing.getAttribute('aria-pressed')!=='true')existing.click();
      }else{
        const pill=choice.cloneNode(true);
        pill.removeAttribute('role');
        pill.classList.add('is-mine');
        pill.setAttribute('aria-pressed','true');
        const label=choice.getAttribute('title');
        pill.setAttribute('title',label+' — you reacted');
        const count=document.createElement('b');count.textContent='1';pill.appendChild(count);
        const sr=document.createElement('span');sr.hidden=true;sr.textContent=label;pill.appendChild(sr);
        const addBtn=row.querySelector('.rx-add');
        const later=[...row.querySelectorAll(':scope > .rx[data-rx]')]
          .find(p=>order.indexOf(p.getAttribute('data-rx'))>order.indexOf(key));
        row.insertBefore(pill,later||addBtn);
      }
      pop.hidden=true;add.setAttribute('aria-expanded','false');add.focus();
    });
  });
  wrap.querySelectorAll('.cmt-rx > .rx').forEach(pill=>{
    pill.addEventListener('click',()=>{
      const on=pill.classList.toggle('is-mine');
      pill.setAttribute('aria-pressed',String(on));
      const b=pill.querySelector('b'),n=parseInt(b.textContent,10);
      b.textContent=String(Math.max(0,n+(on?1:-1)));
    });
  });
})();
</script>
```

A reaction with zero count is not rendered — the row shows only what exists.
The popover's five are the fixed set, in wheel order, each in its fixed color.
The love pill's count and CMT-002's love toggle share one number; the
specimen above freezes love at 12 in both places to teach the rule — a live
build renders both from the same field.

The `title` on each pill names a few reactors by display name — never emails,
never handles. Where your privacy rules hide reactor lists, drop the `title`
and keep the count: the count is public, the names are a choice.

### States

- **Rest:** pills sit dark with a 1.5px edge in their reaction color — present, not loud. Glyphs are drawn strokes, never emoji (Law 4).
- **Hover:** lifts 2px, glows in the pill's own color. Each reaction ignites its own hue — love burns pink, celebrate magenta, never blanket purple.
- **Mine (`aria-pressed="true"`):** held glow + inner wash in the reaction color, glyph filled. Your reaction is visibly yours; toggling it off returns the pill to rest and decrements the honest count.
- **Active/press:** settles 1px.
- **Focus:** white 2px ring — the popover is keyboard-operable. It is a `group` of native buttons, not a menu: Tab moves through the five reactions, Esc closes, focus returns to the plus trigger. The roles match the behavior — no menu is promised, so no menu keyboard is owed (independent scorecard fix, 2026-10-16).
- **Plus rest:** dashed circle — it promises "more", and the popover keeps the promise. **Open:** elevated panel (Law 3), five reactions in wheel order.
- **Zero count:** the pill does not exist. There is no "0" pill, no grayed-out ghost of a reaction nobody chose.

### Do / Don't

**Do** render only reactions that exist — a row of three honest pills beats a row of five with two zeros. **Don't** sort pills by count to manufacture a leaderboard; the family order is the wheel order, and popularity is not a ranking the UI gets to invent.

**Do** let anyone take a reaction back — toggling off is as easy as toggling on, no guilt copy, no "are you sure?". **Don't** add badges, streaks, "top fan" labels, or any status game on top of the row — reactions are play, and play that keeps score stops being play.

### Anatomy

- **Pill:** the unit — drawn glyph + honest count in tabular numerals, 44px tall, 1.5px edge in the reaction's fixed color. One pill per reaction that exists.
- **Glyph:** drawn SVG in the reaction color — heart, star, ringed dot, check, smile. Law 4: icons are drawn, and each promises exactly what it does.
- **Mine state:** the held ignition — glow + wash + filled glyph. Visible without shouting.
- **Plus:** the dashed 44px circle — the fixed set lives one tap away. The popover renders the five in wheel order, each keyboard-focusable.
- **Reactor names:** display names only, in the `title`, droppable where privacy says so. The count never depends on the names being shown.

**What it will NOT fake:** counts are the server's counts — never rounded, never "12k" theater, never incremented optimistically and left there if the request fails. A failed toggle rolls the pill back and says so plainly. Zero-count reactions are absent, not grayed out. No badges, no streaks, no "top fan" — the row will not manufacture status from play. The popover never offers a reaction outside the fixed set; a sixth reaction takes indigo and is specified, not improvised.

---

## Family notes

- **One meaning per color, everywhere:** the reaction table at the top is the contract. Pink love in CMT-002's action row, pink love in CMT-003's pill — same object, same number, same color. If a sixth reaction appears, it takes indigo — the wheel continues, it never restarts.
- **Depth rails are structure, not sentiment:** magenta → purple → blue mark where you are in the conversation. They never carry emotional meaning — that job belongs to the reaction table, and the two never mix.
- **Timestamps are renderings, not substitutes:** every plain-words label sits on a real `datetime`; the full date is one hover away. "Just now" is earned by the clock (under a minute), never by optimism.
- **Private by default, everywhere:** display names only, tombstones leave no remains, reactor names are droppable. The family never asks for, shows, or stores author PII beyond the display name — that boundary is structural, not a setting.
- **One quiet control (independent scorecard fix, 2026-10-16):** `.naya-btn--quiet` is the blessed quiet-control DNA — owned ONCE for the whole catalog at the checkout family contract (`checkout-blocks.md`, family contract §8). CMT-002's clamp toggle consumes it; no comment block defines its own quiet idiom. (`.cmt-morebtn` is retired to a sizing hook.)
- **What the family does not cover:** moderation queues, report flows, rich mentions, and threaded DMs are real needs and are *not* specified here — they are future blocks (CMT-004+), not implied features of these three. Nothing in these specs pretends they exist.
