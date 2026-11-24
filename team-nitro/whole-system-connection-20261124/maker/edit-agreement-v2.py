#!/usr/bin/env python3
"""Whole-system connection round — AGREEMENT fix v2 (checker FAIL -> fix).

Input: maker/agreement.html (v1 output, sha 1a726235). Output: same file,
in place. Every edit asserts its anchor; a failed assert stops the build.

Fixes (checker verdict 2026-11-24):
 3. Load-time JS error + dead Close (item 53 / G.4): the appended init block
    attached fpFinalClose's handler BEFORE the <div id="fpFinalReader">
    existed (script ends ~22949963, div at ~22950003) — every load threw and
    the handler never attached. Guard it + wire on DOMContentLoaded + re-wire
    inside openFinal (the only path that opens the reader).
 4. "I agree" must exist and sink (item 11): a reachable agree control at
    the deck-end (in the final row, next to The Invitation links) and at the
    letter-end (revealed by finishLegalPanel when the last beat lands), both
    class .fp-agree-btn sinking to scale .94 + dim + shadow collapse while
    held, both onward in place via goToPortal() (N ball 2s, then
    /?from=agreement#userName). The play disc gets a real press-in too
    (scale .94 + dim on :active).
 7. Item 7 amplitude: audioPlaying was declared false and NEVER set true, so
    the analyser branch in drawWave was unreachable. The anthem element
    (#welcomeAudio, src EMBED.audio) has native controls — wire its real
    play/pause/ended events to the flag, so the analyser reads live
    frequency data whenever the recording actually plays.
 10. Tidies: choice pills the same width on desktop (280px fixed) and the
    claimed 64px min-height real (was height:48px overriding it); daybar
    title stops truncating on phone (the <=640px nowrap+ellipsis rule
    becomes wrapping 19px).

Out of scope (kept, not rebuilt): the choice screen stays the merge-law
shape (items 48/50 — the video-left/audio-right frame EXISTS on the cover
screen, proven by render; items stay PARTIAL pending the coordinator).
Slide 11 + boards untouched (asserted).
"""
import hashlib
import re

P = "/home/hatch/workspace/team-nitro/whole-system-connection-20261124/maker/agreement.html"

text = open(P, encoding="utf-8", errors="ignore").read()
print("v2 input:", len(text.encode("utf-8")), hashlib.sha256(text.encode("utf-8")).hexdigest()[:12])
assert hashlib.sha256(text.encode("utf-8")).hexdigest().startswith("1a726235"), "v1 base moved"
intel_board_rules_before = len(re.findall(r"\.intel-board", text))
m = re.search(r"var SLIDES = \[(.*?)\];", text, re.S)
slides = re.findall(r'\{t:"(.*?)"\s*,\s*x:"(.*?)"\s*,\s*a:"(.*?)"\}', m.group(1), re.S)
assert len(slides) == 27
slide11_before = hashlib.sha256(slides[10][1].encode()).hexdigest()


def replace_once(s, old, new, name):
    assert s.count(old) == 1, f"{name}: anchor count {s.count(old)} != 1: {old[:90]!r}"
    return s.replace(old, new, 1)


# ---------------------------------------------------------------- F3 item 53
old = """document.getElementById('fpFinalClose').addEventListener('click', function(){
  document.getElementById('fpFinalReader').hidden = true;
});"""
new = """/* WHOLE-SYSTEM CONNECTION 2026-11-24 v2 (item 53): this block runs BEFORE
   the <div id="fpFinalReader"> exists (it sits after this script), so the
   bare getElementById threw on EVERY load and the Close handler never
   attached — the reader trapped the user. Wire it once the DOM exists, and
   re-wire inside openFinal, the only path that opens the reader. */
function wireFinalClose(){
  var c = document.getElementById('fpFinalClose');
  if (c && !c.__fpWired){
    c.__fpWired = true;
    c.addEventListener('click', function(){
      document.getElementById('fpFinalReader').hidden = true;
    });
  }
}
if (document.readyState === 'loading'){
  document.addEventListener('DOMContentLoaded', wireFinalClose);
} else {
  wireFinalClose();
}"""
text = replace_once(text, old, new, "item53-wireFinalClose")
old = "  document.getElementById('fpFinalReader').hidden = false;\n}"
new = "  document.getElementById('fpFinalReader').hidden = false;\n  wireFinalClose();\n}"
text = replace_once(text, old, new, "item53-rewire-in-openFinal")
print("item53: Close wired after the DOM exists + re-wired on open")

# ---------------------------------------------------------------- F4 item 11
# Shared agree-button CSS + the play-disc press-in, appended before </style>
# (the file has exactly one </style>).
agree_css = """
/* WHOLE-SYSTEM CONNECTION 2026-11-24 v2 (item 11) — the agree control is
   LIVE: deck-end and letter-end, sinking to scale .94 + dim + shadow
   collapse while held, onward in place to the portal name box. The play
   disc gets a real press-in too (was transform:none on hold). */
.fp-agree-btn{display:inline-block;min-width:200px;min-height:64px;padding:12px 28px;border-radius:30px;border:1.5px solid rgba(47,232,158,.65);color:#fff;background:radial-gradient(circle at 50% 0%,#0b2e21,#05060a);font:inherit;font-size:17px;font-weight:800;cursor:pointer;box-shadow:0 0 18px rgba(47,232,158,.22);margin-top:16px}
.fp-agree-btn:active{transform:translateY(1px) scale(.94);filter:brightness(.72);box-shadow:0 0 2px 0 rgba(255,255,255,.08)}
#screen-choice .choice-play .pm-play-disc{transition:transform .15s ease,filter .15s ease,box-shadow .15s ease}
#screen-choice .choice-play:active{transform:translateY(1px)}
#screen-choice .choice-play:active .pm-play-disc{transform:scale(.94);filter:brightness(.72);box-shadow:0 0 2px 0 rgba(255,255,255,.08)}"""
assert text.count("</style>") == 1
text = text.replace("</style>", agree_css + "\n</style>", 1)

# Deck-end: the agree button joins the final row (The Invitation + 8 links).
old = """<button class="fp-final-link" type="button" data-final="oath">Our Oath</button></nav>';"""
new = """<button class="fp-final-link" type="button" data-final="oath">Our Oath</button></nav>' +
      '<button class="fp-agree-btn" type="button" data-fp-agree>I agree &#9670;</button>';"""
text = replace_once(text, old, new, "item11-deck-agree-button")
old = """    _row.querySelectorAll('[data-final]').forEach(function(b){
      b.addEventListener('click', function(){ openFinal(b.getAttribute('data-final')); });
    });"""
new = """    _row.querySelectorAll('[data-final]').forEach(function(b){
      b.addEventListener('click', function(){ openFinal(b.getAttribute('data-final')); });
    });
    _row.querySelectorAll('[data-fp-agree]').forEach(function(b){
      b.addEventListener('click', function(){ goToPortal(); });
    });"""
text = replace_once(text, old, new, "item11-deck-agree-wire")
print("item11: deck-end agree button added (goToPortal)")

# Letter-end: finishLegalPanel reveals the agree button when the last beat
# lands; resetLegalPanel hides it again for a fresh read.
old = """function finishLegalPanel(panel){
  var next = panel.querySelector('[data-legal-next]');
  var all = panel.querySelector('[data-legal-all]');
  if (next) next.hidden = true;
  if (all) all.hidden = true;
}"""
new = """function finishLegalPanel(panel){
  var next = panel.querySelector('[data-legal-next]');
  var all = panel.querySelector('[data-legal-all]');
  if (next) next.hidden = true;
  if (all) all.hidden = true;
  /* WHOLE-SYSTEM CONNECTION 2026-11-24 v2 (item 11): the letter-end agree
     control — reachable, sinks to .94 while held, onward in place to the
     portal name box. Created once per panel, revealed at the end. */
  var agree = panel.querySelector('[data-legal-agree]');
  if (!agree){
    agree = document.createElement('button');
    agree.className = 'fp-agree-btn';
    agree.type = 'button';
    agree.setAttribute('data-legal-agree', '');
    agree.innerHTML = 'I agree &#9670;';
    agree.addEventListener('click', function(){ goToPortal(); });
    var ctl = panel.querySelector('.letter-controls');
    if (ctl) ctl.appendChild(agree); else panel.appendChild(agree);
  }
  agree.hidden = false;
  try { agree.scrollIntoView({block:'nearest'}); } catch(e){}
}"""
text = replace_once(text, old, new, "item11-letter-agree-finish")
old = "  if (next) next.hidden = false;\n  if (all) all.hidden = false;"
new = ("  if (next) next.hidden = false;\n  if (all) all.hidden = false;\n"
       "  var _ag = panel.querySelector('[data-legal-agree]'); if (_ag) _ag.hidden = true;")
text = replace_once(text, old, new, "item11-letter-agree-reset")
print("item11: letter-end agree button added (finishLegalPanel)")

# ---------------------------------------------------------------- F9 item 7
# The analyser follows the REAL anthem: #welcomeAudio (src EMBED.audio) has
# native controls, so a citizen can press play on the recording. Its real
# play/pause/ended events drive audioPlaying — the flag drawWave's analyser
# branch reads. (Before: declared false, never set true — unreachable.)
old = """dPlay.addEventListener('click', function(){
  if (videoPlaying) ytCommand('pause'); else ytCommand('play');
});"""
new = """dPlay.addEventListener('click', function(){
  if (videoPlaying) ytCommand('pause'); else ytCommand('play');
});
/* WHOLE-SYSTEM CONNECTION 2026-11-24 v2 (item 7): the analyser follows the
   REAL anthem, not the play-state flag. The recording has its own native
   controls; when it actually plays, audioPlaying goes true and drawWave
   reads live frequency data; pause/end rests it. */
audio.addEventListener('play', function(){ audioPlaying = true; });
audio.addEventListener('pause', function(){ audioPlaying = false; });
audio.addEventListener('ended', function(){ audioPlaying = false; });"""
text = replace_once(text, old, new, "item7-real-audio-flag")
print("item7: audioPlaying follows the real anthem element")

# ---------------------------------------------------------------- F10 tidies
# Choice pills: same width on desktop + the claimed 64px min-height real
# (height:48px was overriding it).
old = "min-width:179px;height:48px;padding:0 24px;"
new = "width:280px;min-width:280px;height:auto;min-height:64px;padding:12px 24px;"
text = replace_once(text, old, new, "tidy-choice-pills-size")
# Daybar title: the <=640px nowrap+ellipsis rule truncated "The Collective
# Agreement" on phone. Let it wrap at 19px instead.
old = ".tb-title{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}"
new = ".tb-title{white-space:normal;overflow:visible;text-overflow:clip;font-size:19px;line-height:1.25}"
text = replace_once(text, old, new, "tidy-daybar-title")
print("tidies: choice pills 280x64, daybar title wraps")

# ---------------------------------------------------------------- verify
assert text.count("document.getElementById('fpFinalClose').addEventListener") == 0, "bare pre-DOM attach left"
assert "function wireFinalClose()" in text and "c.addEventListener('click'" in text
assert text.count("data-fp-agree") == 2, text.count("data-fp-agree")
assert text.count("data-legal-agree") == 3, text.count("data-legal-agree")
assert text.count("fp-agree-btn") >= 4
assert "audio.addEventListener('play'" in text
assert "width:280px;min-width:280px;height:auto;min-height:64px" in text
assert "white-space:normal;overflow:visible;text-overflow:clip;font-size:19px" in text
# slide 11 byte-identical + boards untouched (items 3, 74)
m2 = re.search(r"var SLIDES = \[(.*?)\];", text, re.S)
slides2 = re.findall(r'\{t:"(.*?)"\s*,\s*x:"(.*?)"\s*,\s*a:"(.*?)"\}', m2.group(1), re.S)
assert len(slides2) == 27
assert hashlib.sha256(slides2[10][1].encode()).hexdigest() == slide11_before, "slide 11 changed!"
assert hashlib.sha256(slides2[10][1].encode()).hexdigest().startswith("33b0590cfb9f811a")
assert len(re.findall(r"\.intel-board", text)) == intel_board_rules_before, "intel-board changed"
assert text.count("welcome-staged") == 0
assert text.count('of 27') == 0
open(P, "w", encoding="utf-8").write(text)
b = len(text.encode("utf-8"))
print("V2 written:", P, b, "sha:", hashlib.sha256(text.encode("utf-8")).hexdigest()[:12])
scripts = re.findall(r"<script>(.*?)</script>", text, re.S)
print("script blocks:", len(scripts))
for i, sc in enumerate(scripts):
    open(f"/tmp/wsc-ag2-{i}.js", "w").write(sc)
