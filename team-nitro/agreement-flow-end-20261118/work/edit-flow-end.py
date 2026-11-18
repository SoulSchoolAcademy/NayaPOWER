#!/usr/bin/env python3
"""FLOW-END edit driver (2026-11-18) — agreement flow-end round.

Applies the round's edits to:
  - welcome-staged.html (walk-v23-assembly-20261114) — the staged welcome
  - agreement-unfold-fixed.html (agreement-unfold-fix-20261117) — /agreement

Bullseye (Shawn 15:33Z): N ball HOLDS (~0.5s -> 3s, both end paths);
flow ends at the name-entry login, then the Hub; portrait -> NAYA_POWER.jpg
verbatim; play reads the distilled script with stop/pause/play (LAW).
Amendments: 16:07Z one block per viewport, locked; 16:12Z Smart Show
(full screen, one visual per block, split across screens, optimize for
presentation, click to unfold, always go back, 16:9); 16:13Z screenshot
as the visual reference; 16:15Z Smart Block (the presentation unit;
Intelligent Block stays the posting format, untouched).

Every replacement is asserted (exact occurrence counts). Nothing is
written unless every assertion passes. Writes are resilient (chunked,
size+sha verified, retried) for the EPERM flake. Run: python3 edit-flow-end.py
"""
import base64, hashlib, json, os, re, sys, time

HOME = os.path.expanduser('~')
RECORDS = os.path.join(HOME, 'workspace/team-nitro/agreement-flow-end-20261118')
WORK = os.path.join(RECORDS, 'work')
WELCOME_SRC = os.path.join(HOME, 'workspace/team-nitro/walk-v23-assembly-20261114/welcome-staged.html')
UNFOLD_SRC = os.path.join(HOME, 'workspace/team-nitro/agreement-unfold-fix-20261117/agreement-unfold-fixed.html')
PORTRAIT = os.path.join(HOME, 'workspace/user/media_library/image/NAYA_POWER.jpg')
AUDIO = os.path.join(HOME, 'workspace/team-nitro/agreement-audio-20261118/audio-script.md')
WELCOME_OUT = os.path.join(WORK, 'welcome-flow-end.html')
UNFOLD_OUT = os.path.join(WORK, 'unfold-flow-end.html')

BASE_WELCOME_SHA = 'e4fe0d525a7f0a2fcf1b2f739cfe566493e5ad8efd0523733f9fd44f1a7743d5'
BASE_UNFOLD_SHA = '96b18b6f063c88cf4422b915be4bb53808f290364a03be5093c26c9ea3d47983'
PORTRAIT_SHA = '6ee884aa3dacb78e54e246a051455a2b730c391cb9d6fd89b06c0a2f5575c057'

def sha(b): return hashlib.sha256(b).hexdigest()

def read_bytes(p):
    with open(p, 'rb') as f: return f.read()

def write_resilient(path, data):
    """Chunked write + size/sha verify + retry (EPERM flake)."""
    tmp = path + '.tmp-flow-end'
    last = None
    for attempt in range(40):
        try:
            with open(tmp, 'wb') as f:
                for i in range(0, len(data), 8192):
                    f.write(data[i:i+8192])
                f.flush(); os.fsync(f.fileno())
            got = read_bytes(tmp)
            if len(got) != len(data) or sha(got) != sha(data):
                raise IOError('verify failed: tmp %d bytes sha %s' % (len(got), sha(got)[:12]))
            os.replace(tmp, path)
            got2 = read_bytes(path)
            if len(got2) != len(data) or sha(got2) != sha(data):
                raise IOError('verify failed after replace')
            print('wrote %s %d B sha %s (attempt %d)' % (path, len(data), sha(data)[:12], attempt+1))
            return
        except Exception as e:
            last = e
            print('write attempt %d failed: %s' % (attempt+1, e))
            time.sleep(2 + attempt)
    raise IOError('write_resilient gave up on %s: %s' % (path, last))

def rep(text, old, new, count, label):
    n = text.count(old)
    if n != count:
        raise AssertionError('%s: expected %d occurrence(s) of %r, found %d' % (label, count, old[:80], n))
    return text.replace(old, new)

# ---------------------------------------------------------------- portrait
portrait_bytes = read_bytes(PORTRAIT)
assert sha(portrait_bytes) == PORTRAIT_SHA, 'portrait sha mismatch: %s' % sha(portrait_bytes)
PORTRAIT_B64 = base64.b64encode(portrait_bytes).decode('ascii')
print('portrait OK: %d B sha %s' % (len(portrait_bytes), PORTRAIT_SHA[:12]))

# ---------------------------------------------------------------- audio script
audio_raw = read_bytes(AUDIO).decode('utf-8')
audio_body = audio_raw.split('\n---\n')[0].strip()
paras = [p.strip() for p in re.split(r'\n\s*\n', audio_body) if p.strip()]
words = sum(len(p.split()) for p in paras)
print('audio script: %d paragraphs, %d words' % (len(paras), words))
assert len(paras) == 15, 'expected 15 paragraphs, got %d' % len(paras)
assert words == 1482, 'expected 1482 words, got %d' % words
assert paras[-1].endswith('Your world begins here.'), 'last paragraph changed'
assert 'Welcome home.' in paras[-1], 'closing words changed'
SCRIPT_JSON = json.dumps(paras, ensure_ascii=False)

# ---------------------------------------------------------------- shared JS: phase-aware next handler (welcome wireDeck/wireLetterUnfold)
PHASE_NEXT_WELCOME = """    btn.addEventListener('click', function(){
      /* SMART BLOCK (2026-11-18) — one visual per block: a beat with a
         showcase is TWO Smart Blocks. The first tap shows the visual
         alone (16:9, locked to the viewport); the next tap moves on. */
      if (b.querySelector('.lb-showcase') && !b.classList.contains('fp-smart-visual')) {
        b.classList.add('fp-smart-visual');
        b.classList.remove('fp-smart-talk');
        ensureBeatVisible(b);
        return;
      }
      var cur = i + 1;
      if (cur < beats.length) {
        show(cur);
        idx = cur + 1;
        btn.hidden = true;
        if (idx < beats.length) ensureBeatVisible(beats[cur]);
      }
    });"""

PHASE_NEXT_WELCOME_OLD = """    btn.addEventListener('click', function(){
      var cur = i + 1;
      if (cur < beats.length) {
        show(cur);
        idx = cur + 1;
        btn.hidden = true;
        if (idx < beats.length) ensureBeatVisible(beats[cur]);
      }
    });"""

# ---------------------------------------------------------------- shared JS: back button builder
BACK_BUILDER = """
  /* SMART BLOCK (2026-11-18) — always go back: every beat carries a
     ‹ Back button beside its Keep reading. It steps back one Smart
     Block: visual -> talk on the same beat, else the previous beat
     (its visual if it has a showcase, else its talk). */
  beats.forEach(function(b, i){
    var next = b.querySelector('.deck-next[data-beat]');
    if (!next || b.querySelector('.deck-back')) return;
    var back = document.createElement('button');
    back.className = 'p3-enter letter-next deck-next deck-back';
    back.type = 'button';
    back.textContent = '\\u2039 Back \\u25C6';
    if (i === 0) back.hidden = true;
    back.addEventListener('click', function(){
      if (b.classList.contains('fp-smart-visual')) {
        b.classList.remove('fp-smart-visual');
        b.classList.add('fp-smart-talk');
        ensureBeatVisible(b);
        return;
      }
      if (i <= 0) return;
      var prev = beats[i - 1];
      prev.hidden = false;
      prev.classList.add('reveal');
      if (prev.querySelector('.lb-showcase')) {
        prev.classList.add('fp-smart-visual');
        prev.classList.remove('fp-smart-talk');
      } else {
        prev.classList.add('fp-smart-talk');
        prev.classList.remove('fp-smart-visual');
      }
      ensureBeatVisible(prev);
    });
    next.parentNode.insertBefore(back, next.nextSibling);
  });
  beats[0].classList.add('fp-smart-talk');"""

# ---------------------------------------------------------------- welcome CSS block
WELCOME_CSS = """
<style id="fpFlowEnd">
/* ============ FLOW-END (2026-11-18) — Smart Block ============
   Every unfolded screen is one Smart Block, locked to exactly one
   viewport (16:07Z); the deck IS the Smart Show, across (16:12Z):
   FULL SCREEN, ONE VISUAL PER BLOCK, oversize boards split, 16:9,
   click to unfold, always go back. The unit is the Smart Block
   (16:15Z). The Intelligent Block stays the posting format — untouched.
   The N HOLD lives here too (the N ball, held 3s at the flow end). */
/* RULE 1 — FULL SCREEN: the 980px narrow column goes. The text board
   band in Shawn's 16:13Z screenshot ran x~305–1576 in a 1867-wide shot
   (a 980px column + gutters); the container is now the full viewport
   width with its 18px gutters. The beats carry no max-width of their
   own, so the text fills the frame with them. */
#fpAgreement .p3-deal-unfold, #fpLegal .p3-deal-unfold{max-width:none}
.lb-showcase{max-width:none}
/* SMART BLOCK — the two phases of one beat. TALK: the face + the words
   (the showcase hidden). VISUAL: the showcase alone, 16:9, locked to
   the frame. The stage's own rules carry !important display on the
   blocktop, so the stage-scoped hides carry !important too. */
#fpAgreement .letter-beat.fp-smart-talk .lb-showcase, #fpLegal .letter-beat.fp-smart-talk .lb-showcase{display:none}
body.fp-stage-on #fpAgreement .fp-now.fp-smart-talk .lb-showcase{display:none}
#fpAgreement .letter-beat.fp-smart-visual .ib-blocktop, #fpAgreement .letter-beat.fp-smart-visual .ib-nutshell, #fpAgreement .letter-beat.fp-smart-visual .ib-foot{display:none}
body.fp-stage-on #fpAgreement .fp-now.fp-smart-visual .ib-blocktop, body.fp-stage-on #fpAgreement .fp-now.fp-smart-visual .ib-nutshell, body.fp-stage-on #fpAgreement .fp-now.fp-smart-visual .ib-foot{display:none!important}
/* VISUAL — the 16:9 slot. width:min(100%, the width that fits the
   frame height) so the slot is exactly 16:9 and never cropped wider:
   at 1919x1080 the stage frame is 914px tall, so the slot is
   1625x914; at 390x844 it is 366x206, centred in the frame. The slide
   art is natively 16:9 (1672x941), so object-fit:cover fills it
   exactly; the zoom still shows the whole picture, one tap away. */
body.fp-stage-on #fpAgreement .fp-now.fp-smart-visual{justify-content:center}
body.fp-stage-on #fpAgreement .fp-now.fp-smart-visual .lb-showcase{flex:0 1 auto;width:min(100%,calc((100svh - 166px) * 16 / 9));height:auto;min-height:0;aspect-ratio:16/9;max-width:100%;max-height:100%;margin-left:auto!important;margin-right:auto!important}
body.fp-stage-on #fpAgreement .fp-now.fp-smart-visual .lb-showcase img{object-fit:cover}
#fpAgreement .letter-beat.fp-smart-visual .lb-showcase{width:min(100%,calc((100svh - 166px) * 16 / 9));aspect-ratio:16/9;max-height:100%;margin-left:auto;margin-right:auto}
#fpAgreement .letter-beat.fp-smart-visual .lb-showcase img{width:100%;height:100%;object-fit:cover;aspect-ratio:auto}
/* SMART SHOW — the >=900px side-by-side grid (talk 42% | showcase)
   IS the double block. In the stage the beat is one flex column in
   both phases; the grid never applies. Equal specificity, later in
   the cascade, so this wins. */
@media (min-width:900px){
  body.fp-stage-on #deckBody .letter-beat.fp-now,
  body.fp-stage-on #letterBody .letter-beat.fp-now,
  body.fp-stage-on #fpLegal [data-legal-beat].fp-now{display:flex;flex-direction:column}
}
/* SECONDARY — 390 hover-tip overflow (12.1px): the tip was centred on
   the play button, white-space:nowrap, 218.5px wide, right edge 402.1
   in a 390 viewport. At <=480px it anchors to the button's right edge
   and wraps at 200px: right edge = the button's right edge (~327 at
   390), left edge ~127. Nothing passes the viewport. */
@media (max-width:480px){
  .p3-play-tip{left:auto;right:0;transform:none;white-space:normal;width:min(200px,calc(100vw - 48px));text-align:center}
}
/* BACK — the in-beat ‹ Back button sits under its Keep reading. */
.letter-beat .deck-back{margin-top:12px}
/* THE N HOLD — full-screen Smart Block (data-smart-block="n-hold") on
   both end paths. The harvested #dealSeal orb, same classes, scaled
   by the hold's own rules (200px, 92px N). z-index 95 sits above the
   stage bars (70) and every overlay (90). Stamp .55s on entry, then
   a slow breathing glow; the hold releases at 3000ms, or on tap. */
#fpNHold{position:fixed;inset:0;z-index:95;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:28px;background:#050607}
#fpNHold[hidden]{display:none}
#fpNHold .deal-seal{width:200px;height:200px;animation:fp-seal-breathe 3.2s ease-in-out .55s infinite}
#fpNHold .deal-seal-mark{font-size:92px}
#fpNHold .fp-nhold-line{font-family:Marcellus,Georgia,serif;font-size:25px;line-height:1.3;color:#fff;margin:0;text-align:center}
#fpNHold .fp-nhold-hint{font-size:17px;line-height:1.4;color:#fff;margin:0;text-align:center}
@keyframes fp-seal-breathe{0%,100%{box-shadow:0 12px 32px rgba(0,0,0,.75),0 0 36px rgba(178,32,56,.5),inset 0 2px 6px rgba(255,255,255,.35),inset 0 -10px 20px rgba(0,0,0,.6),inset 0 0 0 7px rgba(0,0,0,.16),inset 0 0 0 9px rgba(255,200,200,.12)}50%{box-shadow:0 12px 32px rgba(0,0,0,.75),0 0 72px rgba(178,32,56,.9),inset 0 2px 6px rgba(255,255,255,.35),inset 0 -10px 20px rgba(0,0,0,.6),inset 0 0 0 7px rgba(0,0,0,.16),inset 0 0 0 9px rgba(255,200,200,.12)}}
/* THE INTRO SEAL — the N, quiet, in the void below the choice buttons
   (the 1919 empty stretch). It fills the void with the loved object
   and moves nothing: it sits after the choices in the flow, shows
   only in the intro view, and is a real object, breathing slowly. */
.fp-intro-seal{display:none}
body.fp-stage-on #fpAgreement.fp-view-intro .fp-intro-seal{display:block;margin:36px auto 0;text-align:center}
.fp-intro-seal .deal-seal{width:84px;height:84px;margin:0 auto;animation:fp-seal-breathe 3.2s ease-in-out infinite}
.fp-intro-seal .deal-seal-mark{font-size:38px}
@media (max-width:640px){.fp-intro-seal .deal-seal{width:64px;height:64px}.fp-intro-seal .deal-seal-mark{font-size:30px}}
/* THE STOP — a real object on the play button: a 44px obsidian circle,
   bottom-right of the 68px play, visible only while the agreement is
   playing or paused. It is a span (a button cannot nest a button),
   role=button, keyboard-operable. Absolute, out of flow: the intro
   row (0.0/0.0/24-24) does not move. */
#fpIntroStop{position:absolute;right:-10px;bottom:-10px;width:44px;height:44px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:radial-gradient(circle at 35% 30%,#3a0d18,#12060a 60%,#000);border:1.5px solid rgba(255,140,150,.65);box-shadow:0 0 18px rgba(178,32,56,.5),inset 0 1.5px 0 rgba(255,255,255,.3),inset 0 -4px 8px rgba(0,0,0,.7);cursor:pointer}
#fpIntroStop[hidden]{display:none}
#fpIntroStop:active{transform:scale(.94)}
@media (prefers-reduced-motion: reduce){
  #fpNHold .deal-seal, .fp-intro-seal .deal-seal{animation:none}
}
</style>"""

# ---------------------------------------------------------------- welcome edits
def edit_welcome(text):
    orig = text
    # W1 — portrait swap (verbatim NAYA_POWER.jpg, data-URI; deck beats keep /agmt-b06.png)
    old_img = '<img class="fp-naya-portrait" src="/agmt-b06.png" alt="Naya">'
    new_img = '<img class="fp-naya-portrait" src="data:image/jpeg;base64,' + PORTRAIT_B64 + '" alt="Naya">'
    text = rep(text, old_img, new_img, 1, 'W1 portrait')
    assert text.count('/agmt-b06.png') == orig.count('/agmt-b06.png') - 1, 'W1: another /agmt-b06.png moved'
    # W2 — Smart Block naming on the two containers
    text = rep(text, '<div id="deckBody">', '<div id="deckBody" data-smart-block="deck">', 1, 'W2 deckBody')
    text = rep(text, '<div id="letterBody">', '<div id="letterBody" data-smart-block="letter">', 1, 'W2 letterBody')
    # W3 — intro N seal (fills the 1919 void; after the choices, in the flow, intro view only)
    seal = ('<div class="fp-intro-seal" aria-hidden="true"><div class="deal-seal">'
            '<span class="deal-seal-mark" aria-hidden="true">N</span></div></div>')
    text = rep(text, '<div class="letter-controls" id="deckControls">', seal + ' <div class="letter-controls" id="deckControls">', 1, 'W3 intro seal')
    # W4 — play button: pause icon + stop control (span: a button cannot nest a button)
    old_play = ('<button class="p3-naya-play" id="fpIntroPlay" type="button" aria-label="Naya will talk you through this page">'
                '<svg viewBox="0 0 24 24" width="24" height="24" fill="#fff" aria-hidden="true"><path d="M7 4l13 8-13 8z"/></svg>'
                '<span class="p3-play-tip">Naya will talk you through this page</span></button>')
    new_play = ('<button class="p3-naya-play" id="fpIntroPlay" type="button" aria-label="Naya will talk you through this page">'
                '<svg class="fp-play-ic" viewBox="0 0 24 24" width="24" height="24" fill="#fff" aria-hidden="true"><path d="M7 4l13 8-13 8z"/></svg>'
                '<svg class="fp-pause-ic" hidden viewBox="0 0 24 24" width="24" height="24" fill="#fff" aria-hidden="true"><path d="M6 4h4v16H6zM14 4h4v16h-4z"/></svg>'
                '<span class="p3-play-tip">Naya will talk you through this page</span>'
                '<span class="fp-intro-stop" id="fpIntroStop" role="button" tabindex="0" hidden aria-label="Stop — stop reading the agreement">'
                '<svg viewBox="0 0 24 24" width="18" height="18" fill="#fff" aria-hidden="true"><path d="M6 6h12v12H6z"/></svg></span></button>')
    text = rep(text, old_play, new_play, 1, 'W4 play button')
    # W5 — N hold overlay (body child, before the legal footer)
    hold = ('<div id="fpNHold" data-smart-block="n-hold" hidden><div class="deal-seal">'
            '<span class="deal-seal-mark" aria-hidden="true">N</span></div>'
            '<p class="fp-nhold-line">Welcome home.</p>'
            '<p class="fp-nhold-hint">Tap to continue &#9670;</p></div>')
    text = rep(text, '<footer id="fpLegal">', hold + '<footer id="fpLegal">', 1, 'W5 N hold')
    # W6 — new CSS block after the LAST </style>
    idx = text.rfind('</style>')
    assert idx > 0, 'W6: no </style>'
    text = text[:idx + len('</style>')] + '\n' + WELCOME_CSS + text[idx + len('</style>'):]
    # W7 — viewport lock: 'nearest' -> 'start' in all three ensureBeatVisible copies
    text = rep(text, "b.scrollIntoView({ behavior: scrollBehavior(), block: 'nearest', inline: 'nearest' });",
               "b.scrollIntoView({ behavior: scrollBehavior(), block: 'start', inline: 'nearest' });", 3, 'W7 ensureBeatVisible')
    # W7b — same lock in the legal pages' next-group handler (L2866): the
    # last revealed legal beat was scrolled 'nearest' too — halfway down
    # a tall beat. Same law, same one-word fix.
    text = rep(text, "last.scrollIntoView({ behavior: 'smooth', block: 'nearest' });",
               "last.scrollIntoView({ behavior: 'smooth', block: 'start' });", 1, 'W7b legal next')
    # W8 — phase-aware next buttons (wireDeck + wireLetterUnfold share the body)
    text = rep(text, PHASE_NEXT_WELCOME_OLD, PHASE_NEXT_WELCOME, 2, 'W8 phase next')
    # W9 — show() sets the talk phase (three IIFEs, three anchors)
    text = rep(text, "b.classList.add('reveal');\n    if (dots[n]) dots[n].classList.add('on');",
               "b.classList.add('reveal');\n    b.classList.add('fp-smart-talk');b.classList.remove('fp-smart-visual');\n    if (dots[n]) dots[n].classList.add('on');", 1, 'W9a wireDeck show')
    text = rep(text, "b.classList.add('reveal');\n    var official = parseInt(b.getAttribute('data-beat'), 10);",
               "b.classList.add('reveal');\n    b.classList.add('fp-smart-talk');b.classList.remove('fp-smart-visual');\n    var official = parseInt(b.getAttribute('data-beat'), 10);", 1, 'W9b wireLetterUnfold show')
    text = rep(text, "b.classList.add('reveal');\n    /* SPLIT (2026-11-16)",
               "b.classList.add('reveal');\n    b.classList.add('fp-smart-talk');b.classList.remove('fp-smart-visual');\n    /* SPLIT (2026-11-16)", 1, 'W9c wireLetter show')
    # W10 — back buttons + first-beat talk phase (wireDeck + wireLetterUnfold)
    text = rep(text, 'glowFor(beats[0]);', 'glowFor(beats[0]);' + BACK_BUILDER, 2, 'W10 back buttons')
    # W11 — wireLetter #letterNext control: phase check before advancing
    old_next = """  next.addEventListener('click', function(){
    if (idx < beats.length) {
      var cur = idx;
      show(cur);
      idx++;
      update();
      if (idx >= beats.length) finish();
      else ensureBeatVisible(beats[cur]);
    }
  });"""
    new_next = """  next.addEventListener('click', function(){
    /* SMART BLOCK (2026-11-18) — one visual per block (see wireDeck). */
    var curBeat = beats[idx - 1];
    if (curBeat && curBeat.querySelector('.lb-showcase') && !curBeat.classList.contains('fp-smart-visual')) {
      curBeat.classList.add('fp-smart-visual');
      curBeat.classList.remove('fp-smart-talk');
      ensureBeatVisible(curBeat);
      return;
    }
    if (idx < beats.length) {
      var cur = idx;
      show(cur);
      idx++;
      update();
      if (idx >= beats.length) finish();
      else ensureBeatVisible(beats[cur]);
    }
  });"""
    text = rep(text, old_next, new_next, 1, 'W11 letterNext phase')
    # W12 — rail jump lands its beat in talk phase
    text = rep(text, "beats[target].scrollIntoView({ behavior: scrollBehavior(), block: 'start', inline: 'nearest' });",
               "beats[target].classList.add('fp-smart-talk');beats[target].classList.remove('fp-smart-visual');\n      beats[target].scrollIntoView({ behavior: scrollBehavior(), block: 'start', inline: 'nearest' });", 1, 'W12 rail phase')
    # W13 — plain-text "take me to signing" shows all beats: read-all clears phases
    text = rep(text, 'for (var k = 1; k < beats.length; k++) show(k);',
               'for (var k = 1; k < beats.length; k++) { show(k); beats[k].classList.remove(\'fp-smart-talk\'); beats[k].classList.remove(\'fp-smart-visual\'); }', 1, 'W13 read-all clear')
    # W14 — legal-row clip: intro + bridge rows wrap and centre (was nowrap + horizontal scroll)
    text = rep(text, 'flex-wrap:nowrap;justify-content:flex-start;gap:2px 20px;max-width:none;margin:0;overflow-x:auto;padding:0 4px',
               'flex-wrap:wrap;justify-content:center;gap:2px 20px;max-width:none;margin:0;padding:0 4px', 2, 'W14 legal wrap')
    # W15 — stage state gains a phase
    text = rep(text, "var S={view:'intro',deck:0,letter:0,legalId:null,legal:0,all:null,letterDone:false,letterPageTop:0};",
               "var S={view:'intro',deck:0,letter:0,legalId:null,legal:0,all:null,letterDone:false,letterPageTop:0,phase:'talk'};", 1, 'W15 S.phase')
    # W16 — end-of-walk helpers (before the EYE FOLLOW-ON F3 comment)
    helpers = """  /* FLOW-END (2026-11-18) — Smart Block phases: one beat is two Smart
     Blocks when it carries a showcase (talk, then visual). The end of
     a walk is the last beat in its visual phase (or its talk, when it
     has no showcase). Progress stays beat-based (dots, jewel); the
     Smart Block totals are deck 18 (9+9), letter 38 (34+4). */
  function hasShowcase(b){return !!b&&!!b.querySelector('.lb-showcase');}
  function deckEnd(){return S.deck>=deckBeats.length-1&&(!hasShowcase(deckBeats[S.deck])||S.phase==='visual');}
  function letterEnd(){return S.letter>=letterBeats.length-1&&(!hasShowcase(letterBeats[S.letter])||S.phase==='visual');}
"""
    text = rep(text, "/* EYE FOLLOW-ON F3 (2026-11-17) - the eye's verdict settles the", helpers + "/* EYE FOLLOW-ON F3 (2026-11-17) - the eye's verdict settles the", 1, 'W16 helpers')
    # W17 — deck end is phase-aware
    text = rep(text, "if(S.deck<deckBeats.length-1){setNext('Keep reading \\u25C6',tone,'deckNext');if(deckBack)deckBack.hidden=false;}",
               "if(!deckEnd()){setNext('Keep reading \\u25C6',tone,'deckNext');if(deckBack)deckBack.hidden=false;}", 1, 'W17 deck end')
    # W18 — letter end is phase-aware (letter + letterPage branches)
    text = rep(text, "if(S.letter>=letterBeats.length-1){setNext('I agree \\u25C6','#07925f','letterPageAgree');}",
               "if(letterEnd()){setNext('I agree \\u25C6','#07925f','letterPageAgree');}", 2, 'W18 letter end')
    # W19 — letter-end toggle is phase-aware
    text = rep(text, "agreeSec.classList.toggle('fp-letter-end',S.letter>=letterBeats.length-1);",
               "agreeSec.classList.toggle('fp-letter-end',letterEnd());", 1, 'W19 letter-end toggle')
    # W20 — render() deck branch: viewport lock + phase classes
    old_deck_render = """    if(S.view==='deck'){
      for(i=0;i<deckBeats.length;i++){
        b=deckBeats[i];var sd=i===S.deck;
        b.hidden=!sd;b.classList.toggle('fp-now',sd);
        b.classList.toggle('fp-noslide',!q('.lb-showcase',b));
        b.classList.toggle('fp-notop',!q('.ib-blocktop',b));
      }
    }"""
    new_deck_render = """    if(S.view==='deck'){
      /* SMART BLOCK (2026-11-18) — the viewport lock: the layer never
         scrolls in the deck view (the beat fills the frame by flex),
         and the current beat carries its phase (talk or visual). */
      agreeSec.scrollTop=0;
      for(i=0;i<deckBeats.length;i++){
        b=deckBeats[i];var sd=i===S.deck;
        b.hidden=!sd;b.classList.toggle('fp-now',sd);
        b.classList.toggle('fp-noslide',!q('.lb-showcase',b));
        b.classList.toggle('fp-notop',!q('.ib-blocktop',b));
        b.classList.toggle('fp-smart-visual',sd&&S.phase==='visual');
        b.classList.toggle('fp-smart-talk',sd&&S.phase==='talk');
      }
    }"""
    text = rep(text, old_deck_render, new_deck_render, 1, 'W20 render deck')
    # W21 — render() letter branch: same lock; read-all clears phases and keeps its scroll
    old_letter_render = """    if(S.view==='letter'){
      for(i=0;i<letterBeats.length;i++){
        b=letterBeats[i];var sl=(S.all==='letter')||i===S.letter;
        b.hidden=!sl;b.classList.toggle('fp-now',sl);
        b.classList.toggle('fp-noslide',!q('.lb-showcase',b));
        b.classList.toggle('fp-notop',!q('.ib-blocktop',b));
      }
    }"""
    new_letter_render = """    if(S.view==='letter'){
      /* SMART BLOCK (2026-11-18) — same lock as the deck. In read-it-all
         mode (S.all==='letter') the phases are OFF: every showcase
         shows, stacked, as the citizen chose — and the layer keeps its
         scroll position. */
      if(S.all!=='letter')agreeSec.scrollTop=0;
      for(i=0;i<letterBeats.length;i++){
        b=letterBeats[i];var sl=(S.all==='letter')||i===S.letter;
        b.hidden=!sl;b.classList.toggle('fp-now',sl);
        b.classList.toggle('fp-noslide',!q('.lb-showcase',b));
        b.classList.toggle('fp-notop',!q('.ib-blocktop',b));
        if(S.all==='letter'){b.classList.remove('fp-smart-visual');b.classList.remove('fp-smart-talk');}
        else{b.classList.toggle('fp-smart-visual',sl&&S.phase==='visual');b.classList.toggle('fp-smart-talk',sl&&S.phase==='talk');}
      }
    }"""
    text = rep(text, old_letter_render, new_letter_render, 1, 'W21 render letter')
    # W22 — render() letterPage branch: phase classes (scroll restore untouched — fix-4 stands)
    old_lp_render = """      /* ITEM 10 CORRECTED — the 86-beat stacked scroll is GONE: letterPage
         steps the distilled beats one at a time, like the letter view. */
      for(i=0;i<letterBeats.length;i++){
        b=letterBeats[i];var slp=i===S.letter;
        b.hidden=!slp;b.classList.toggle('fp-now',slp);
        b.classList.toggle('fp-noslide',!q('.lb-showcase',b));
        b.classList.toggle('fp-notop',!q('.ib-blocktop',b));
      }"""
    new_lp_render = """      /* ITEM 10 CORRECTED — the 86-beat stacked scroll is GONE: letterPage
         steps the distilled beats one at a time, like the letter view. */
      for(i=0;i<letterBeats.length;i++){
        b=letterBeats[i];var slp=i===S.letter;
        b.hidden=!slp;b.classList.toggle('fp-now',slp);
        b.classList.toggle('fp-noslide',!q('.lb-showcase',b));
        b.classList.toggle('fp-notop',!q('.ib-blocktop',b));
        b.classList.toggle('fp-smart-visual',slp&&S.phase==='visual');
        b.classList.toggle('fp-smart-talk',slp&&S.phase==='talk');
      }"""
    text = rep(text, old_lp_render, new_lp_render, 1, 'W22 render letterPage')
    # W23-25 — derive() syncs S.phase from the DOM class (the in-beat handler runs first)
    text = rep(text, 'var d=lastShown(deckBeats);if(d>=0)S.deck=d;',
               "var d=lastShown(deckBeats);if(d>=0){S.deck=d;var db=deckBeats[d];S.phase=(db&&db.classList.contains('fp-smart-visual'))?'visual':'talk';}", 1, 'W23 derive deck')
    text = rep(text, 'var l=lastShown(letterBeats);if(l>=0)S.letter=l;',
               "var l=lastShown(letterBeats);if(l>=0){S.letter=l;var lbv=letterBeats[l];S.phase=(lbv&&lbv.classList.contains('fp-smart-visual'))?'visual':'talk';}", 1, 'W24 derive letter')
    text = rep(text, 'var lp=lastShown(letterBeats);if(lp>=0)S.letter=lp;',
               "var lp=lastShown(letterBeats);if(lp>=0){S.letter=lp;var lpv=letterBeats[lp];S.phase=(lpv&&lpv.classList.contains('fp-smart-visual'))?'visual':'talk';}", 1, 'W25 derive letterPage')
    # W26-28 — resumes and returns start at the talk phase
    text = rep(text, "else{S.view='deck';S.deck=rt.deck;}\n    S.all=null;render();",
               "else{S.view='deck';S.deck=rt.deck;}\n    S.phase='talk';S.all=null;render();", 1, 'W26 goResume')
    text = rep(text, "function enterLetterPage(){S.view='letterPage';S.all=null;render();}",
               "function enterLetterPage(){S.view='letterPage';S.phase='talk';S.all=null;render();}", 1, 'W27 enterLetterPage')
    text = rep(text, "if(linkDeckBack)linkDeckBack.addEventListener('click',function(){cancelAgreeExit();S.view='deck';S.deck=deckBeats.length-1;S.all=null;render();});",
               "if(linkDeckBack)linkDeckBack.addEventListener('click',function(){cancelAgreeExit();S.view='deck';S.deck=deckBeats.length-1;S.phase='talk';S.all=null;render();});", 1, 'W28 linkDeckBack')
    # W29 — deck-end Enter shows the N hold, then exits to the login
    text = rep(text, "else if(action==='deckJoin'){window.__fpDeckEndReturn=true;exitStage();}",
               "else if(action==='deckJoin'){window.__fpDeckEndReturn=true;showNHold(function(){exitStage();});}", 1, 'W29 deckJoin hold')
    # W30 — stage agree: arm the 10s fallback, then show the N hold (primary)
    old_agree_stage = """  agreeBtn.addEventListener('click',function(){
    if(!body.classList.contains('fp-stage-on'))return;
    cancelAgreeExit();
    agreeExitTimer=setTimeout(function(){agreeExitTimer=null;stopAgreeCount();exitStage();},10000);
    startAgreeCount();
  });"""
    new_agree_stage = """  agreeBtn.addEventListener('click',function(){
    if(!body.classList.contains('fp-stage-on'))return;
    cancelAgreeExit();
    agreeExitTimer=setTimeout(function(){agreeExitTimer=null;stopAgreeCount();exitStage();},10000);
    startAgreeCount();
    /* FLOW-END (2026-11-18) — the N HOLDS on agree too: the hold is the
       primary exit (3s, or a tap); the 10s timer above is the fallback,
       cancelled by the hold's release. */
    showNHold(function(){cancelAgreeExit();exitStage();});
  });"""
    text = rep(text, old_agree_stage, new_agree_stage, 1, 'W30 agree hold')
    # W31 — N hold functions (before exitStage)
    hold_js = """  /* FLOW-END (2026-11-18) — the N HOLDS (Shawn 15:33Z): the beautiful N
     ball showed ~0.5s (the deal-stamp .55s) and must HOLD. The hold is
     a full-screen Smart Block (data-smart-block="n-hold") on BOTH end
     paths — deck-end Enter and I agree — reusing the harvested
     #dealSeal orb (same classes, scaled by the hold's own rules).
     Stamp .55s + hold 3000ms from first paint, then release to the
     name-entry login. Tap anywhere to continue at once — the 3s never
     traps. */
  var nHold=q('#fpNHold'), nHoldTimer=null, nHoldRelease=null;
  function showNHold(release){
    if(!nHold)return;
    nHoldRelease=(typeof release==='function')?release:null;
    nHold.hidden=false;
    var s=nHold.querySelector('.deal-seal');
    if(s){s.classList.remove('stamp');void s.offsetWidth;s.classList.add('stamp');}
    if(nHoldTimer)clearTimeout(nHoldTimer);
    nHoldTimer=setTimeout(function(){releaseNHold();},3000);
  }
  function releaseNHold(){
    if(!nHold||nHold.hidden)return;
    if(nHoldTimer){clearTimeout(nHoldTimer);nHoldTimer=null;}
    nHold.hidden=true;
    var r=nHoldRelease;nHoldRelease=null;
    if(r)r();
  }
  if(nHold)nHold.addEventListener('click',function(){releaseNHold();});
"""
    text = rep(text, '  function exitStage(){', hold_js + '  function exitStage(){', 1, 'W31 hold JS')
    # W32 — exitStage cleans the hold and stops the voice
    text = rep(text, "  function exitStage(){\n    closeZoom();",
               "  function exitStage(){\n    closeZoom();\n    if(nHold){nHold.hidden=true;}\n    if(nHoldTimer){clearTimeout(nHoldTimer);nHoldTimer=null;}\n    nHoldRelease=null;\n    fpSpeechStop();", 1, 'W32 exitStage cleanup')
    # W33 — render() hides the hold on any view change away from agree
    text = rep(text, "  function render(){\n    var i,j,b;\n    var onLegal=(S.view==='footer'||S.view==='legal');",
               "  function render(){\n    var i,j,b;\n    var onLegal=(S.view==='footer'||S.view==='legal');\n    /* FLOW-END (2026-11-18) — the N hold is an agree-view moment: any\n       render away from the agree view hides it and drops its release,\n       so a tap on \"The whole deal\" (or any other agree-view control)\n       never leaves the citizen staring at the N. */\n    if(nHold&&!nHold.hidden&&S.view!=='agree'){nHold.hidden=true;if(nHoldTimer){clearTimeout(nHoldTimer);nHoldTimer=null;}nHoldRelease=null;}", 1, 'W33 render hold guard')
    # W34 — the play button READS the distilled script (stop/pause/play)
    player = """  /* FLOW-END (2026-11-18) — the play button READS the agreement (Shawn
     15:53Z, LAW): the distilled script (agreement-audio-20261118,
     1,482 words, ~10 min) spoken by the Web Speech API, one utterance
     per paragraph so a long read never clips. STOP / PAUSE / PLAY are
     the controls. No harvested speech path existed — speechSynthesis
     count 0 in the welcome, unfold and walk files — so the player is
     built on the platform API, and this comment says so. The voice
     keeps reading if the citizen walks on into the deck (they started
     it deliberately); it stops on exitStage, on Stop, and at the end. */
  var FP_DISTILLED_SCRIPT=""" + SCRIPT_JSON + """;
  var fpSpeechIdx=0, fpSpeechState='idle';
  function fpSpeechEls(){return{play:q('.fp-play-ic',wPlay),pause:q('.fp-pause-ic',wPlay),tip:q('.p3-play-tip',wPlay),stop:q('#fpIntroStop')};} 
  function fpSpeechSetState(st){
    fpSpeechState=st;
    var e=fpSpeechEls();
    if(e.play)e.play.hidden=(st==='playing');
    if(e.pause)e.pause.hidden=(st!=='playing');
    if(e.stop)e.stop.hidden=(st==='idle');
    if(st==='playing'){wPlay.classList.add('show');if(e.tip)e.tip.textContent='Playing the agreement \\u2014 tap to pause';wPlay.setAttribute('aria-label','Pause \\u2014 Naya is reading the agreement');}
    else if(st==='paused'){wPlay.classList.add('show');if(e.tip)e.tip.textContent='Paused \\u2014 tap to play';wPlay.setAttribute('aria-label','Play \\u2014 resume the agreement');}
    else{wPlay.classList.remove('show');if(e.tip)e.tip.textContent='Naya will talk you through this page';wPlay.setAttribute('aria-label','Naya will talk you through this page');}
  }
  function fpSpeakPara(i){
    if(!('speechSynthesis' in window))return;
    if(i>=FP_DISTILLED_SCRIPT.length){fpSpeechSetState('idle');var e2=fpSpeechEls();if(e2.tip)e2.tip.textContent='Finished \\u2014 tap to hear it again';wPlay.classList.add('show');return;}
    fpSpeechIdx=i;
    var u=new SpeechSynthesisUtterance(FP_DISTILLED_SCRIPT[i]);
    u.lang='en-US';u.rate=1;
    u.onend=function(){if(fpSpeechState!=='playing')return;fpSpeakPara(i+1);};
    u.onerror=function(){if(fpSpeechState==='playing')fpSpeechSetState('idle');};
    try{window.speechSynthesis.speak(u);}catch(err){fpSpeechSetState('idle');}
  }
  function fpPlayToggle(){
    if(!('speechSynthesis' in window)){
      var e=fpSpeechEls();
      if(e.tip){e.tip.textContent='Voice not available on this device \\u2014 read below';wPlay.classList.add('show');setTimeout(function(){wPlay.classList.remove('show');},3000);}
      return;
    }
    if(fpSpeechState==='playing'){try{window.speechSynthesis.pause();}catch(err){}fpSpeechSetState('paused');}
    else if(fpSpeechState==='paused'){try{window.speechSynthesis.resume();}catch(err){}fpSpeechSetState('playing');}
    else{try{window.speechSynthesis.cancel();}catch(err){}fpSpeechSetState('playing');fpSpeakPara(0);}
  }
  function fpSpeechStop(){
    if('speechSynthesis' in window){try{window.speechSynthesis.cancel();}catch(err){}}
    fpSpeechState='idle';
    if(wPlay)fpSpeechSetState('idle');
  }
  if(wPlay){var _fpStop=q('#fpIntroStop');if(_fpStop){_fpStop.addEventListener('click',function(ev){ev.stopPropagation();fpSpeechStop();});_fpStop.addEventListener('keydown',function(ev){if(ev.key==='Enter'||ev.key===' '){ev.preventDefault();ev.stopPropagation();fpSpeechStop();}});}}
"""
    old_wplay = "if(wPlay){wPlay.addEventListener('click',function(){wPlay.classList.toggle('show');wPlay.classList.add('pending-glow');setTimeout(function(){wPlay.classList.remove('pending-glow');},900);});}"
    text = rep(text, old_wplay, player + "  if(wPlay){wPlay.addEventListener('click',function(){fpPlayToggle();});}", 1, 'W34 speech player')
    return text

# ---------------------------------------------------------------- unfold CSS block
UNFOLD_CSS = """
<style id="fpFlowEnd">
/* ============ FLOW-END (2026-11-18) — Smart Block ============
   Same law as the welcome file. THIS page is the stacked view Shawn
   screenshotted at 16:13Z: the narrow column (980px) and the 640px
   showcase are gone — the container and the showcase are full screen
   now (see the edits above); this block carries the phases.
   Every Smart Block is exactly one viewport tall, its content
   centred in it. The talk text is capped so a long beat never
   overflows its viewport — it scrolls inside its own panel instead
   (the cap is load-bearing: blocktop + capped text + foot + buttons
   always fit 100svh). */
.letter-beat.fp-smart-talk .lb-showcase{display:none}
.letter-beat.fp-smart-visual .ib-blocktop, .letter-beat.fp-smart-visual .ib-nutshell, .letter-beat.fp-smart-visual .ib-foot{display:none}
.letter-beat.fp-smart-talk{display:flex;flex-direction:column;justify-content:center;min-height:100svh;min-height:100dvh}
.letter-beat.fp-smart-talk .ib-nutshell{max-height:max(160px,calc(100svh - 480px));overflow-y:auto}
.letter-beat.fp-smart-talk .deck-next, .letter-beat.fp-smart-visual .deck-next{align-self:center}
.letter-beat.fp-smart-visual{display:flex;flex-direction:column;justify-content:center;align-items:center;min-height:100svh;min-height:100dvh;gap:18px}
.letter-beat.fp-smart-visual .lb-showcase{display:block;width:min(100%,calc((100svh - 160px) * 16 / 9));aspect-ratio:16/9;max-height:calc(100svh - 160px);margin:0 auto}
.letter-beat.fp-smart-visual .lb-showcase img{width:100%;height:100%;object-fit:cover;aspect-ratio:auto}
.letter-beat .deck-back{margin-top:12px}
</style>"""

# ---------------------------------------------------------------- unfold edits
def edit_unfold(text):
    # U1 — full screen container (was max-width:980px, the narrow column)
    text = rep(text, '.p3-deal-unfold{position:relative;border:1.5px solid rgba(255,255,255,.32);border-radius:22px;padding:28px 18px 30px;margin:0 auto;max-width:980px;',
               '.p3-deal-unfold{position:relative;border:1.5px solid rgba(255,255,255,.32);border-radius:22px;padding:28px 18px 30px;margin:0 auto;max-width:none;', 1, 'U1 container')
    # U2 — full screen showcase (was max-width:min(640px,100%))
    text = rep(text, '.lb-showcase{margin:18px auto 4px;max-width:min(640px,100%);',
               '.lb-showcase{margin:18px auto 4px;max-width:none;', 1, 'U2 showcase')
    # U3 — Smart Block naming
    text = rep(text, '<div id="deckBody">', '<div id="deckBody" data-smart-block="deck">', 1, 'U3 deckBody')
    # U4 — viewport lock in ensureBeatVisible
    text = rep(text, "b.scrollIntoView({ behavior: scrollBehavior(), block: 'nearest', inline: 'nearest' });",
               "b.scrollIntoView({ behavior: scrollBehavior(), block: 'start', inline: 'nearest' });", 1, 'U4 ensureBeatVisible')
    # U5 — wirePlay fallback scrolls to the block top, never nearest
    text = rep(text, "last.scrollIntoView({ behavior: 'smooth', block: 'nearest' });",
               "last.scrollIntoView({ behavior: 'smooth', block: 'start' });", 1, 'U5 wirePlay')
    # U6 — show() sets the talk phase
    text = rep(text, "b.classList.add('reveal');\n    if (dots[n]) dots[n].classList.add('on');",
               "b.classList.add('reveal');\n    b.classList.add('fp-smart-talk');b.classList.remove('fp-smart-visual');\n    if (dots[n]) dots[n].classList.add('on');", 1, 'U6 show')
    # U7 — phase-aware next button (this file's handler carries finish())
    old_next = """    btn.addEventListener('click', function(){
      var cur = i + 1;
      if (cur < beats.length) {
        show(cur);
        idx = cur + 1;
        btn.hidden = true;
        if (idx >= beats.length) finish();
        else ensureBeatVisible(beats[cur]);
      }
    });"""
    new_next = """    btn.addEventListener('click', function(){
      /* SMART BLOCK (2026-11-18) — one visual per block: a beat with a
         showcase is TWO Smart Blocks. The first tap shows the visual
         alone (16:9, locked to the viewport); the next tap moves on. */
      if (b.querySelector('.lb-showcase') && !b.classList.contains('fp-smart-visual')) {
        b.classList.add('fp-smart-visual');
        b.classList.remove('fp-smart-talk');
        ensureBeatVisible(b);
        return;
      }
      var cur = i + 1;
      if (cur < beats.length) {
        show(cur);
        idx = cur + 1;
        btn.hidden = true;
        if (idx >= beats.length) finish();
        else ensureBeatVisible(beats[cur]);
      }
    });"""
    text = rep(text, old_next, new_next, 1, 'U7 phase next')
    # U8 — back buttons + first-beat talk phase
    text = rep(text, 'glowFor(beats[0]);', 'glowFor(beats[0]);' + BACK_BUILDER, 1, 'U8 back buttons')
    # U9 — read-it-all clears phases (showcases show, stacked, as chosen)
    text = rep(text, 'for (var n = 1; n < beats.length; n++) show(n);',
               'for (var n = 1; n < beats.length; n++) { show(n); beats[n].classList.remove(\'fp-smart-talk\'); beats[n].classList.remove(\'fp-smart-visual\'); }', 1, 'U9 read-all clear')
    # U10 — new CSS block after the LAST </style>
    idx = text.rfind('</style>')
    assert idx > 0, 'U10: no </style>'
    text = text[:idx + len('</style>')] + '\n' + UNFOLD_CSS + text[idx + len('</style>'):]
    return text

# ---------------------------------------------------------------- verification
def check_scripts(path, label):
    import subprocess
    data = read_bytes(path).decode('utf-8')
    blocks = re.findall(r'<script[^>]*>(.*?)</script>', data, re.S)
    print('%s: %d script blocks' % (label, len(blocks)))
    for i, b in enumerate(blocks):
        if not b.strip():
            continue
        tmp = os.path.join(WORK, 'script-check-%s-%d.js' % (label, i))
        write_resilient(tmp, b.encode('utf-8'))
        r = subprocess.run(['node', '--check', tmp], capture_output=True, text=True)
        if r.returncode != 0:
            raise AssertionError('%s script %d failed node --check: %s' % (label, i, r.stderr[:500]))
        print('%s script %d: node --check OK (%d chars)' % (label, i, len(b)))
        os.remove(tmp)

def count_beats(path, label):
    data = read_bytes(path).decode('utf-8')
    out = {}
    di = data.find('<div id="deckBody"')
    if di >= 0:
        end = data.find('<section', di)
        seg = data[di:end if end > 0 else di+600000]
        a = list(re.finditer(r'<article[^>]*data-beat=[^>]*>(.*?)</article>', seg, re.S))
        out['deck'] = (len(a), sum(1 for x in a if 'lb-showcase' in x.group(1)))
    li = data.find('<div id="letterBody"')
    if li >= 0:
        end = data.find('</section>', li)
        seg = data[li:end if end > 0 else li+900000]
        a = [x for x in re.finditer(r'<article[^>]*data-distilled[^>]*>(.*?)</article>', seg, re.S)]
        out['letter_distilled'] = (len(a), sum(1 for x in a if 'lb-showcase' in x.group(1)))
    print('%s beats: %s' % (label, out))
    return out

def main():
    w0 = read_bytes(WELCOME_SRC)
    assert sha(w0) == BASE_WELCOME_SHA, 'welcome base sha mismatch: %s' % sha(w0)
    u0 = read_bytes(UNFOLD_SRC)
    assert sha(u0) == BASE_UNFOLD_SHA, 'unfold base sha mismatch: %s' % sha(u0)
    print('bases OK: welcome %d B, unfold %d B' % (len(w0), len(u0)))
    print('base counts:'); count_beats(WELCOME_SRC, 'welcome-base'); count_beats(UNFOLD_SRC, 'unfold-base')
    w = edit_welcome(w0.decode('utf-8'))
    u = edit_unfold(u0.decode('utf-8'))
    # --- welcome invariants (must-not-move) ---
    assert w.count('/agmt-b06.png') == w0.decode('utf-8').count('/agmt-b06.png') - 1, 'portrait: wrong /agmt-b06.png count'
    assert 'agreeSec.scrollTop=S.letterPageTop||0;' in w, 'fix-4 letterPage restore moved!'
    assert '#fpWelcomeHero' in w and 'fpIntroPlay' in w, 'intro row markers lost'
    assert '.deal-seal{width:120px' in w, 'harvested deal-seal rule moved!'
    assert 'speechSynthesis' in w and 'FP_DISTILLED_SCRIPT' in w, 'player missing'
    assert "block: 'start', inline: 'nearest'" in w, 'viewport lock missing'
    assert w.count("block: 'nearest'") == 1, 'nearest should survive only in the note-eye handler, found %d' % w.count("block: 'nearest'")
    # portrait data-URI decodes to the exact JPEG
    m = re.search(r'src="data:image/jpeg;base64,([A-Za-z0-9+/=]+)"', w)
    assert m, 'portrait data-URI not found'
    assert sha(base64.b64decode(m.group(1))) == PORTRAIT_SHA, 'portrait data-URI does not decode to NAYA_POWER.jpg'
    # --- unfold invariants ---
    assert "block: 'nearest'" not in u, 'unfold still has nearest'
    assert 'max-width:980px' not in u, 'unfold still has the 980px column'
    assert 'max-width:min(640px,100%)' not in u, 'unfold still has the 640px showcase'
    assert u.count('fp-smart-visual') >= 10, 'unfold phase wiring thin'
    print('new counts:'); count_beats(WELCOME_OUT if False else WELCOME_SRC, 'welcome-base(again)')
    write_resilient(WELCOME_OUT, w.encode('utf-8'))
    write_resilient(UNFOLD_OUT, u.encode('utf-8'))
    print('welcome new: %d B sha %s' % (len(w.encode('utf-8')), sha(w.encode('utf-8'))))
    print('unfold new: %d B sha %s' % (len(u.encode('utf-8')), sha(u.encode('utf-8'))))
    check_scripts(WELCOME_OUT, 'welcome')
    check_scripts(UNFOLD_OUT, 'unfold')
    print('ALL EDITS APPLIED + VERIFIED')

if __name__ == '__main__':
    main()
