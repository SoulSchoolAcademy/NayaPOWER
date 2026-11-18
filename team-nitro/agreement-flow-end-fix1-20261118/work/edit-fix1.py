#!/usr/bin/env python3
"""FIX1 edit driver (2026-11-18) — agreement flow-end FIX round.

Base: walk-end/agreement-flow-end-20261118 @ 19d8c9ab (welcome 018d488a,
unfold fb0ab19b — the prior round's built files, sha-verified locally).
Fixes the eye's three GOES-BACK failures, all wiring, not missing code:

1. THE N HOLD NEVER APPEARS. Diagnosis, proven in the bytes:
   (a) render() hides the hold on ANY render while S.view!=='agree' — the
       deck-end hold is shown while S.view==='deck', so any render in its
       3s window (including the onStageClick render bubbled from the very
       click that showed it) hides it instantly and drops its release.
       The hold is a full-screen overlay (z-index 95, background #050607):
       nothing beneath it is tappable while it is up, so the render-hide
       is pure hazard with zero benefit — removed.
   (b) The agree button carries TWO handlers: the first block's 2000ms
       scroll-to-login runs INSIDE the hold's 3s window, yanking the
       viewport to the login underneath the hold — guarded to skip while
       the hold is up.
   (c) There was NO visible fill/progress at all — the eye held 3-4s and
       saw no fill ring because none existed. Added a white progress ring
       around the seal, driven to full over exactly 3000ms.
   (d) Deck beat 9's end anchor (a.deck-next[href="#dealUnfold"]) exits
       the stage outright on the talk tap, skipping its visual phase and
       skipping the hold — now talk->visual first, then the hold, like
       deck-end Enter.
2. THE PLAY BUTTON DOES NOT READ ALOUD. Diagnosis, proven in the bytes:
   (a) `.p3-naya-play svg{display:block}` (author rule) defeats the UA
       `[hidden]{display:none}`, so the pause-bars SVG renders alongside
       the play triangle even while hidden — both icons at once. Added
       an author-level `svg[hidden]{display:none}` rule.
   (b) fpSpeakPara never selects a voice (getVoices/voiceschanged: 0 in
       the file). Headless Chromium reports zero voices until they load;
       speak() with no voice fires onerror and the player silently drops
       back to idle. Added voice warm-up + voiceschanged + en-US pick +
       a 2.5s no-start watchdog that says so in the tip instead of
       failing silently.
   (c) The unfold's playBtn advances the deck (its comment admits it
       never plays audio) — rewired to the same speech player; the deck
       advances only via Keep reading now.
3. THE LETTER IS A NARROW CENTRED COLUMN. The checker's Condition 1,
   confirmed live: the stage letter rules keep max-width:640px!important
   on the nutshell and the showcase. Both now say max-width:none; the
   nutshell also gets the unfold's proven bounded scroll
   (max-height:max(160px,calc(100svh-480px)), overflow-y:auto) so its
   last line can no longer slice mid-glyph at the viewport bottom.
   Visuals: the stage slot used object-fit:cover — the letter images are
   4:3 (1448x1086) in a 16:9 slot, so cover crops ~16% top and bottom
   (the NayaNET header cut in half, the caption half cut off). Now
   contain, never cropped. The "Tap the picture" pill sat ON the image's
   bottom caption — now below the frame, with the slot budget grown to
   fit it.
F2: there is NO F2 key handler in the welcome bytes (the only e.key
handlers are Escape x3; "F2" hits are base64 noise) — recorded as
UNVERIFIED in the maker report, honestly, never as passed.

Every replacement is asserted (exact occurrence counts). Nothing is
written unless every assertion passes. Writes are resilient (chunked,
size+sha verified, retried) for the EPERM flake. Run: python3 edit-fix1.py
"""
import base64, hashlib, json, os, re, subprocess, sys, time

HOME = os.path.expanduser('~')
RECORDS = os.path.join(HOME, 'workspace/team-nitro/agreement-flow-end-fix1-20261118')
WORK = os.path.join(RECORDS, 'work')
BASE_WORK = os.path.join(HOME, 'workspace/team-nitro/agreement-flow-end-20261118/work')
WELCOME_SRC = os.path.join(BASE_WORK, 'welcome-flow-end.html')
UNFOLD_SRC = os.path.join(BASE_WORK, 'unfold-flow-end.html')
AUDIO = os.path.join(HOME, 'workspace/team-nitro/agreement-audio-20261118/audio-script.md')
WELCOME_OUT = os.path.join(WORK, 'welcome-fix1.html')
UNFOLD_OUT = os.path.join(WORK, 'unfold-fix1.html')

BASE_WELCOME_SHA = '018d488a1a1fb771b8996b655ae0f36bf7435d8337dfd87becd4c61760c16cc1'
BASE_UNFOLD_SHA = 'fb0ab19b4cafe6bc7e92f47980ea551d3cf131dff4bfb135151297db8c7cfe37'

def sha(b): return hashlib.sha256(b).hexdigest()

def read_bytes(p):
    with open(p, 'rb') as f: return f.read()

def write_resilient(path, data):
    tmp = path + '.tmp-fix1'
    last = None
    for attempt in range(40):
        try:
            # python write first; under the EPERM flake it can return 0
            # and land 0 bytes, so ALWAYS verify, then fall back to a
            # shell redirect (proven to land while python writes fail).
            wrote = False
            try:
                with open(tmp, 'wb') as f:
                    for i in range(0, len(data), 8192):
                        f.write(data[i:i+8192])
                    f.flush(); os.fsync(f.fileno())
                got = read_bytes(tmp)
                if len(got) == len(data) and sha(got) == sha(data):
                    wrote = True
            except Exception as e:
                last = e
            if not wrote:
                r = subprocess.run(['/bin/bash', '-c', 'cat > "$1"', 'bash', tmp],
                                   input=data, capture_output=True, timeout=120)
                if r.returncode != 0:
                    raise IOError('shell write failed rc=%d' % r.returncode)
                got = read_bytes(tmp)
                if len(got) != len(data) or sha(got) != sha(data):
                    raise IOError('shell verify failed: tmp %d bytes sha %s' % (len(got), sha(got)[:12]))
            os.replace(tmp, path)
            got2 = read_bytes(path)
            if len(got2) != len(data) or sha(got2) != sha(data):
                raise IOError('verify failed after replace')
            print('wrote %s %d B sha %s (attempt %d)' % (path, len(data), sha(data)[:12], attempt+1), flush=True)
            return
        except Exception as e:
            last = e
            print('write attempt %d failed: %s' % (attempt+1, e), flush=True)
            time.sleep(2 + attempt)
    raise IOError('write_resilient gave up on %s: %s' % (path, last))

def rep(text, old, new, count, label):
    n = text.count(old)
    if n != count:
        raise AssertionError('%s: expected %d occurrence(s) of %r, found %d' % (label, count, old[:100], n))
    return text.replace(old, new)

def brace_body(t, start):
    i = t.find('{', start)
    d = 0
    for j in range(i, len(t)):
        if t[j] == '{': d += 1
        elif t[j] == '}':
            d -= 1
            if d == 0: return t[start:j+1]
    raise AssertionError('unbalanced braces from %d' % start)

# ---------------------------------------------------------------- base inputs
welcome_b = read_bytes(WELCOME_SRC)
unfold_b = read_bytes(UNFOLD_SRC)
assert sha(welcome_b) == BASE_WELCOME_SHA, 'welcome base sha mismatch: %s' % sha(welcome_b)
assert sha(unfold_b) == BASE_UNFOLD_SHA, 'unfold base sha mismatch: %s' % sha(unfold_b)
print('base OK: welcome %d B %s, unfold %d B %s' % (len(welcome_b), BASE_WELCOME_SHA[:8], len(unfold_b), BASE_UNFOLD_SHA[:8]))
w = welcome_b.decode('utf-8')
u = unfold_b.decode('utf-8')

# ---------------------------------------------------------------- audio script
audio_raw = read_bytes(AUDIO).decode('utf-8')
audio_body = audio_raw.split('\n---\n')[0].strip()
paras = [p.strip() for p in re.split(r'\n\s*\n', audio_body) if p.strip()]
words = sum(len(p.split()) for p in paras)
print('audio script: %d paragraphs, %d words' % (len(paras), words))
assert len(paras) == 15 and words == 1482, 'audio script changed'
assert paras[-1].endswith('Your world begins here.')
SCRIPT_JSON = json.dumps(paras, ensure_ascii=False)

# ================================================================ WELCOME
# --- H1. render() must never kill a shown hold ---------------------
OLD_HOLD_HIDE = """    /* FLOW-END (2026-11-18) — the N hold is an agree-view moment: any
       render away from the agree view hides it and drops its release,
       so a tap on "The whole deal" (or any other agree-view control)
       never leaves the citizen staring at the N. */
    if(nHold&&!nHold.hidden&&S.view!=='agree'){nHold.hidden=true;if(nHoldTimer){clearTimeout(nHoldTimer);nHoldTimer=null;}nHoldRelease=null;}"""
NEW_HOLD_HIDE = """    /* FIX1 (2026-11-18) — the hold is NEVER hidden by render(). The
       old line hid it on any render while S.view!=='agree' — and the
       deck-end hold is shown while S.view==='deck', so the render
       bubbled from the very click that showed it killed the hold in the
       same task, before one frame painted. The hold is a full-screen
       overlay (z-index 95, background #050607): nothing beneath it is
       tappable while it is up, so there is no stale-hold case for
       render() to guard. Only the hold itself hides it (its 3s timer,
       a tap) and exitStage(). */
    void 0;"""
w = rep(w, OLD_HOLD_HIDE, NEW_HOLD_HIDE, 1, 'H1 render hold-hide')

# --- H2. Hold markup: progress ring around the seal ---------------
OLD_HOLD_HTML = """<div id="fpNHold" data-smart-block="n-hold" hidden><div class="deal-seal"><span class="deal-seal-mark" aria-hidden="true">N</span></div><p class="fp-nhold-line">Welcome home.</p><p class="fp-nhold-hint">Tap to continue &#9670;</p></div>"""
NEW_HOLD_HTML = """<div id="fpNHold" data-smart-block="n-hold" hidden><div class="fp-nhold-sealwrap"><svg class="fp-nhold-ring" viewBox="0 0 220 220" aria-hidden="true"><circle class="fp-nhold-track" cx="110" cy="110" r="104"></circle><circle class="fp-nhold-fill" id="fpNHoldFill" cx="110" cy="110" r="104"></circle></svg><div class="deal-seal"><span class="deal-seal-mark" aria-hidden="true">N</span></div></div><p class="fp-nhold-line">Welcome home.</p><p class="fp-nhold-hint">Tap to continue &#9670;</p></div>"""
w = rep(w, OLD_HOLD_HTML, NEW_HOLD_HTML, 1, 'H2 hold ring markup')

# --- H3. Hold CSS: the ring ---------------------------------------
OLD_HOLD_CSS = """#fpNHold .fp-nhold-hint{font-size:17px;line-height:1.4;color:#fff;margin:0;text-align:center}"""
NEW_HOLD_CSS = """#fpNHold .fp-nhold-hint{font-size:17px;line-height:1.4;color:#fff;margin:0;text-align:center}
#fpNHold .fp-nhold-sealwrap{position:relative;width:200px;height:200px;flex:0 0 auto}
#fpNHold .fp-nhold-ring{position:absolute;left:-10px;top:-10px;width:220px;height:220px;transform:rotate(-90deg);pointer-events:none}
#fpNHold .fp-nhold-track{fill:none;stroke:rgba(255,255,255,.18);stroke-width:5}
#fpNHold .fp-nhold-fill{fill:none;stroke:#fff;stroke-width:5;stroke-linecap:round;stroke-dasharray:653.45;stroke-dashoffset:653.45}"""
w = rep(w, OLD_HOLD_CSS, NEW_HOLD_CSS, 1, 'H3 hold ring CSS')

# --- H4. Hold JS: ring driver + stop on release/exit --------------
OLD_SHOW = """  function showNHold(release){
    if(!nHold)return;
    nHoldRelease=(typeof release==='function')?release:null;
    nHold.hidden=false;
    var s=nHold.querySelector('.deal-seal');
    if(s){s.classList.remove('stamp');void s.offsetWidth;s.classList.add('stamp');}
    if(nHoldTimer)clearTimeout(nHoldTimer);
    nHoldTimer=setTimeout(function(){releaseNHold();},3000);
  }"""
NEW_SHOW = """  var nHoldRingTimer=null;
  function fpNHoldRingSet(p){var f=document.getElementById('fpNHoldFill');if(f)f.style.strokeDashoffset=String(653.45*(1-p));}
  function fpNHoldRingStop(){if(nHoldRingTimer){clearInterval(nHoldRingTimer);nHoldRingTimer=null;}}
  function showNHold(release){
    if(!nHold)return;
    nHoldRelease=(typeof release==='function')?release:null;
    nHold.hidden=false;
    var s=nHold.querySelector('.deal-seal');
    if(s){s.classList.remove('stamp');void s.offsetWidth;s.classList.add('stamp');}
    if(nHoldTimer)clearTimeout(nHoldTimer);
    /* FIX1 (2026-11-18) — the VISIBLE fill: a white ring that fills
       around the seal over exactly the 3000ms hold, so the citizen can
       SEE the hold working. The eye held 3-4s and saw no fill ring
       because none existed. */
    fpNHoldRingStop();fpNHoldRingSet(0);
    var _t0=Date.now();
    nHoldRingTimer=setInterval(function(){var p=(Date.now()-_t0)/3000;if(p>=1){p=1;fpNHoldRingStop();}fpNHoldRingSet(p);},100);
    nHoldTimer=setTimeout(function(){releaseNHold();},3000);
  }"""
w = rep(w, OLD_SHOW, NEW_SHOW, 1, 'H4 showNHold ring')
OLD_RELEASE = """  function releaseNHold(){
    if(!nHold||nHold.hidden)return;
    if(nHoldTimer){clearTimeout(nHoldTimer);nHoldTimer=null;}"""
NEW_RELEASE = """  function releaseNHold(){
    if(!nHold||nHold.hidden)return;
    fpNHoldRingStop();fpNHoldRingSet(0);
    if(nHoldTimer){clearTimeout(nHoldTimer);nHoldTimer=null;}"""
w = rep(w, OLD_RELEASE, NEW_RELEASE, 1, 'H4 releaseNHold ring')
OLD_EXIT = """  function exitStage(){
    closeZoom();
    if(nHold){nHold.hidden=true;}"""
NEW_EXIT = """  function exitStage(){
    closeZoom();
    fpNHoldRingStop();
    if(nHold){nHold.hidden=true;}"""
w = rep(w, OLD_EXIT, NEW_EXIT, 1, 'H4 exitStage ring')

# --- H5. Agree handler 1: never scroll under the hold ------------
OLD_AGREE_SCROLL = """    setTimeout(function(){
      var form = document.getElementById('entryForm');"""
NEW_AGREE_SCROLL = """    setTimeout(function(){
      /* FIX1 (2026-11-18) — never scroll the login into view UNDER the
         N hold: this 2000ms scroll ran inside the hold's 3s window and
         yanked the viewport beneath it. While the hold is up, stay. */
      var _nh=document.getElementById('fpNHold');
      if(_nh&&!_nh.hidden)return;
      var form = document.getElementById('entryForm');"""
w = rep(w, OLD_AGREE_SCROLL, NEW_AGREE_SCROLL, 1, 'H5 agree scroll guard')

# --- H6. Deck beat 9: visual first, then the hold -----------------
OLD_ANCHOR = """    var a=(t&&t.closest)?t.closest('a.deck-next[href="#dealUnfold"]'):null;
    if(a){e.preventDefault();exitStage();return;}"""
NEW_ANCHOR = """    var a=(t&&t.closest)?t.closest('a.deck-next[href="#dealUnfold"]'):null;
    if(a){e.preventDefault();
      /* FIX1 (2026-11-18) — deck beat 9 HAS a showcase like beats 1-8,
         so its end button must show the visual first (talk, then
         visual), not exit on the talk tap; and the exit goes through
         the N hold, like deck-end Enter. S.phase is still 'talk' on the
         first tap (derive has not run since the phase handler added the
         visual class), 'visual' on the second — that is the tell. */
      if(S.view==='deck'&&S.phase!=='visual'){var _cb=currentBeatEl();if(_cb&&_cb.querySelector('.lb-showcase')){if(!_cb.classList.contains('fp-smart-visual')){_cb.classList.add('fp-smart-visual');_cb.classList.remove('fp-smart-talk');}derive(false);render();return;}}
      showNHold(function(){exitStage();});return;}"""
w = rep(w, OLD_ANCHOR, NEW_ANCHOR, 1, 'H6 beat-9 anchor')

# --- H7. Play icons: author rule must not defeat [hidden] ----------
OLD_PLAY_SVG = """.p3-naya-play svg{margin-left:2px;display:block;position:relative;z-index:1}"""
NEW_PLAY_SVG = """.p3-naya-play svg{margin-left:2px;display:block;position:relative;z-index:1} .p3-naya-play svg[hidden]{display:none}"""
w = rep(w, OLD_PLAY_SVG, NEW_PLAY_SVG, 1, 'H7 play svg hidden')

# --- H8. Play voices: warm-up, pick, watchdog ----------------------
OLD_ELS = """function fpSpeechEls(){return{play:q('.fp-play-ic',wPlay),pause:q('.fp-pause-ic',wPlay),tip:q('.p3-play-tip',wPlay),stop:q('#fpIntroStop')};}"""
NEW_ELS = OLD_ELS + """
  /* FIX1 (2026-11-18) — VOICES. The player never selected a voice
     (getVoices/voiceschanged: 0 in the file). Headless Chromium
     reports zero voices until they load, so speak() with no voice
     fires onerror and the player silently drops back to idle — the
     eye clicked three times and nothing sounded, no state changed.
     Warm the voices up at load, re-pick on voiceschanged, prefer
     en-US, fall back to any English voice. */
  function fpSpeechVoice(){try{var vs=window.speechSynthesis?window.speechSynthesis.getVoices():[];if(vs&&vs.length){var p=null,k;for(k=0;k<vs.length;k++){if(vs[k].lang&&vs[k].lang.toLowerCase().indexOf('en-us')===0){p=vs[k];break;}}if(!p){for(k=0;k<vs.length;k++){if(vs[k].lang&&vs[k].lang.toLowerCase().indexOf('en')===0){p=vs[k];break;}}}if(p)return p;}}catch(err){}return null;}
  try{if(window.speechSynthesis){window.speechSynthesis.getVoices();if(window.speechSynthesis.addEventListener)window.speechSynthesis.addEventListener('voiceschanged',function(){fpSpeechVoice();});}}catch(err){}"""
w = rep(w, OLD_ELS, NEW_ELS, 1, 'H8 voice loader')
OLD_SPEAK = """    var u=new SpeechSynthesisUtterance(FP_DISTILLED_SCRIPT[i]);
    u.lang='en-US';u.rate=1;
    u.onend=function(){if(fpSpeechState!=='playing')return;fpSpeakPara(i+1);};
    u.onerror=function(){if(fpSpeechState==='playing')fpSpeechSetState('idle');};"""
NEW_SPEAK = """    var u=new SpeechSynthesisUtterance(FP_DISTILLED_SCRIPT[i]);
    u.lang='en-US';u.rate=1;
    var _v=fpSpeechVoice();if(_v)u.voice=_v;
    /* FIX1 (2026-11-18) — the no-start watchdog: if the voice never
       starts within 2.5s (no voices on the device, silent failure),
       say so in the tip instead of sitting on 'playing' for ever. */
    var _wd=setTimeout(function(){if(fpSpeechState==='playing'&&fpSpeechIdx===i){fpSpeechSetState('idle');var _e=fpSpeechEls();if(_e.tip)_e.tip.textContent='Voice not available on this device \\u2014 read below';wPlay.classList.add('show');}},2500);
    u.onstart=function(){clearTimeout(_wd);};
    u.onend=function(){clearTimeout(_wd);if(fpSpeechState!=='playing')return;fpSpeakPara(i+1);};
    u.onerror=function(){clearTimeout(_wd);if(fpSpeechState==='playing')fpSpeechSetState('idle');};"""
w = rep(w, OLD_SPEAK, NEW_SPEAK, 1, 'H8 speak voice+watchdog')

# --- H9. Letter full-screen: the two !important caps go -----------
OLD_NUT = """max-width:640px!important;margin:0 auto 10px!important;overflow-y:visible!important"""
NEW_NUT = """max-width:none!important;margin:0 auto 10px!important;overflow-y:auto!important;max-height:max(160px,calc(100svh - 480px))!important"""
w = rep(w, OLD_NUT, NEW_NUT, 1, 'H9 letter nutshell cap')
OLD_SHOWCASE_CAP = """width:100%!important;max-width:640px!important;margin:0 auto 8px!important"""
NEW_SHOWCASE_CAP = """width:100%!important;max-width:none!important;margin:0 auto 8px!important"""
w = rep(w, OLD_SHOWCASE_CAP, NEW_SHOWCASE_CAP, 1, 'H9 letter showcase cap')

# --- H10. Visuals: contain, never cropped; pill below the frame ----
OLD_COVER1 = """body.fp-stage-on #fpAgreement .fp-now.fp-smart-visual .lb-showcase img{object-fit:cover}"""
NEW_COVER1 = """body.fp-stage-on #fpAgreement .fp-now.fp-smart-visual .lb-showcase img{object-fit:contain}"""
w = rep(w, OLD_COVER1, NEW_COVER1, 1, 'H10 cover->contain stage')
OLD_COVER2 = """#fpAgreement .letter-beat.fp-smart-visual .lb-showcase img{width:100%;height:100%;object-fit:cover;aspect-ratio:auto}"""
NEW_COVER2 = """#fpAgreement .letter-beat.fp-smart-visual .lb-showcase img{width:100%;height:100%;object-fit:contain;aspect-ratio:auto}"""
w = rep(w, OLD_COVER2, NEW_COVER2, 1, 'H10 cover->contain plain')
# slot budget grows 166 -> 212 so the pill below the frame fits
w = rep(w, "calc((100svh - 166px) * 16 / 9)", "calc((100svh - 212px) * 16 / 9)", 2, 'H10 slot budget')
OLD_PILL = """left:50%;bottom:6px;transform:translateX(-50%);font-size:12px;"""
NEW_PILL = """left:50%;top:calc(100% + 8px);bottom:auto;transform:translateX(-50%);font-size:12px;"""
w = rep(w, OLD_PILL, NEW_PILL, 1, 'H10 pill below frame')
OLD_VIS_MARGIN = """margin-left:auto!important;margin-right:auto!important}"""
NEW_VIS_MARGIN = """margin-left:auto!important;margin-right:auto!important;margin-bottom:36px}"""
w = rep(w, OLD_VIS_MARGIN, NEW_VIS_MARGIN, 1, 'H10 visual margin for pill')

# ================================================================ UNFOLD
# --- U1. Unfold play: speech, not navigation ----------------------
# stop button beside Play
OLD_PLAYBTN_HTML = """<span class="play-orbit" aria-hidden="true"></span></button>
</div>"""
NEW_PLAYBTN_HTML = """<span class="play-orbit" aria-hidden="true"></span></button> <button class="play-stop" id="playStop" type="button" hidden aria-label="Stop — stop reading the agreement">&#9632;</button>
</div>"""
u = rep(u, OLD_PLAYBTN_HTML, NEW_PLAYBTN_HTML, 1, 'U1 unfold stop button')
# stop button CSS, appended to the deck style block
OLD_DECK_CSS_END = """.letter-beat .deck-back{margin-top:12px}
</style>"""
NEW_DECK_CSS_END = """.letter-beat .deck-back{margin-top:12px}
.play-stop{width:44px;height:44px;border-radius:50%;flex:0 0 auto;cursor:pointer;border:1.5px solid rgba(255,140,150,.65);background:radial-gradient(circle at 35% 30%,#3a0d18,#12060a 60%,#000);color:#fff;font-size:17px;line-height:1;display:flex;align-items:center;justify-content:center;box-shadow:0 0 18px rgba(178,32,56,.5),inset 0 1.5px 0 rgba(255,255,255,.3),inset 0 -4px 8px rgba(0,0,0,.7)}
.play-stop[hidden]{display:none}
.play-stop:active{transform:scale(.94)}
.play-wrap{display:flex;align-items:center;justify-content:center;gap:14px}
#deckBody{scroll-snap-type:y proximity}
#deckBody .letter-beat{scroll-snap-align:start} </style>"""
u = rep(u, OLD_DECK_CSS_END, NEW_DECK_CSS_END, 1, 'U1/U2 unfold CSS')
# replace the whole wirePlay IIFE (advance) with the speech player
wp_start = u.find('(function wirePlay(){')
assert wp_start >= 0, 'wirePlay not found'
wp_body = brace_body(u, wp_start)
# brace_body stops at the body's closing } — the IIFE's call tail )(); follows it
_wp_tail = u[wp_start + len(wp_body):wp_start + len(wp_body) + 4]
assert _wp_tail == ')();', 'wirePlay IIFE tail unexpected: %r' % _wp_tail
wp_body += _wp_tail
assert "playBtn" in wp_body and "deck-next[data-beat]" in wp_body, 'wirePlay body unexpected'
NEW_WIREPLAY = """(function wirePlay(){
    /* FIX1 (2026-11-18) — Play controls SPEECH ONLY now. The old
       wirePlay advanced the deck on every tap (its own comment: no
       voice was recorded, so it never pretended to play audio) — the
       eye's entanglement: Play advanced the deck ~1,100-2,500px a tap.
       The deck advances only via Keep reading now. The player is the
       same Web Speech player as the welcome intro, reading the same
       distilled script (15 paragraphs, 1,482 words), with the same
       voice warm-up + pick + no-start watchdog. Triangle = play,
       bars = pause, square = stop. */
    var SCRIPT = %s;
    var btn = document.getElementById('playBtn');
    var stopBtn = document.getElementById('playStop');
    var tri = btn ? btn.querySelector('.play-tri') : null;
    var state = 'idle', idx = 0;
    function voices(){ try { return window.speechSynthesis ? window.speechSynthesis.getVoices() : []; } catch (e) { return []; } }
    function pickVoice(){ var vs = voices(), p = null, k; for (k = 0; k < vs.length; k++) { if (vs[k].lang && vs[k].lang.toLowerCase().indexOf('en-us') === 0) { p = vs[k]; break; } } if (!p) { for (k = 0; k < vs.length; k++) { if (vs[k].lang && vs[k].lang.toLowerCase().indexOf('en') === 0) { p = vs[k]; break; } } } return p; }
    function setState(st){ state = st; if (tri) tri.textContent = (st === 'playing') ? '\\u275A\\u275A' : '\\u25B6'; if (stopBtn) stopBtn.hidden = (st === 'idle'); if (btn) btn.setAttribute('aria-label', st === 'playing' ? 'Pause \\u2014 Naya is reading the agreement' : st === 'paused' ? 'Play \\u2014 resume the agreement' : 'Play \\u2014 read the agreement with Naya'); }
    function speak(i){
      if (!('speechSynthesis' in window)) return;
      if (i >= SCRIPT.length) { setState('idle'); return; }
      idx = i;
      var ut = new SpeechSynthesisUtterance(SCRIPT[i]);
      ut.lang = 'en-US'; ut.rate = 1;
      var v = pickVoice(); if (v) ut.voice = v;
      var wd = setTimeout(function(){ if (state === 'playing' && idx === i) setState('idle'); }, 2500);
      ut.onstart = function(){ clearTimeout(wd); };
      ut.onend = function(){ clearTimeout(wd); if (state !== 'playing') return; speak(i + 1); };
      ut.onerror = function(){ clearTimeout(wd); if (state === 'playing') setState('idle'); };
      try { window.speechSynthesis.speak(ut); } catch (e) { clearTimeout(wd); setState('idle'); }
    }
    function stop(){ if ('speechSynthesis' in window) { try { window.speechSynthesis.cancel(); } catch (e) {} } setState('idle'); }
    if (!btn) return;
    try { if (window.speechSynthesis) { window.speechSynthesis.getVoices(); if (window.speechSynthesis.addEventListener) window.speechSynthesis.addEventListener('voiceschanged', function(){ pickVoice(); }); } } catch (e) {}
    btn.addEventListener('click', function(){
      if (!('speechSynthesis' in window)) return;
      if (state === 'playing') { try { window.speechSynthesis.pause(); } catch (e) {} setState('paused'); }
      else if (state === 'paused') { try { window.speechSynthesis.resume(); } catch (e) {} setState('playing'); }
      else { try { window.speechSynthesis.cancel(); } catch (e) {} setState('playing'); speak(0); }
    });
    if (stopBtn) stopBtn.addEventListener('click', function(ev){ ev.stopPropagation(); stop(); });
  })();""" % SCRIPT_JSON
u = u[:wp_start] + NEW_WIREPLAY + u[wp_start + len(wp_body):]
print('unfold wirePlay replaced (%d -> %d chars)' % (len(wp_body), len(NEW_WIREPLAY)))

# ---------------------------------------------------------------- write
write_resilient(WELCOME_OUT, w.encode('utf-8'))
write_resilient(UNFOLD_OUT, u.encode('utf-8'))
print('EDIT-RESULT ' + json.dumps({
    'welcome_bytes': len(w.encode('utf-8')), 'welcome_sha': sha(w.encode('utf-8')),
    'unfold_bytes': len(u.encode('utf-8')), 'unfold_sha': sha(u.encode('utf-8')),
}, indent=1))

# node --check every script block in both files
def node_check_file(path, label):
    txt = read_bytes(path).decode('utf-8')
    blocks = re.findall(r'<script>(.*?)</script>', txt, re.S)
    print('%s: %d script blocks' % (label, len(blocks)))
    for n, b in enumerate(blocks):
        tmp = os.path.join(WORK, 'nodecheck-%s-%d.js' % (label, n))
        write_resilient(tmp, b.encode('utf-8'))
        r = subprocess.run(['node', '--check', tmp], capture_output=True, text=True)
        assert r.returncode == 0, 'node --check failed %s block %d: %s' % (label, n, r.stderr[:400])
        print('  node --check OK block %d (%d chars)' % (n, len(b)))
        os.remove(tmp)

node_check_file(WELCOME_OUT, 'welcome')
node_check_file(UNFOLD_OUT, 'unfold')
print('EDIT DONE')
