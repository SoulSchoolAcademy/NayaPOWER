#!/usr/bin/env python3
"""FIX9 frame transform (2026-11-19): the three measured gaps from the
fix-8 checker (GOES BACK), fixed in the fix-8 bytes, harvest verbatim,
edit never rebuild. Takes the fix-8 unfold bytes (131,797 B, sha
11130770) and edits ONLY the shell — every beat's words, pictures,
tones, feet, deck mechanics, end card and agree handler are untouched
(verified by content guards + beat/article counts).

F1 — frame 1 shows no agreement words at load (checker's measurement at
  1920x999: reading window 219px, media board 183px, first paragraph at
  +227px, all paragraphs vis:false at load). Root cause by the numbers:
  the first paragraph sits inside the .ib-nutshell board, so its top =
  media 183 + collapsed gap 22 + board border 2 + board padding-top 20
  = 227. Fix, all three legs of it, so the first line lifts 56px and
  the window grows 12px: (a) the media board slims ~34px (orb 60->48,
  video pill padding 16->10, board padding 10->8, title margin 4->2,
  video margin-top 10->8, board margin-bottom 12->8); (b) the text
  lifts — the nutshell board's top margin 22->8 and top padding 20->12
  on every frame alike; (c) the window grows — foot pills padding 16->12
  and top bar margin-bottom 8->4. First line "Hi, I'm Naya." whole at
  load, second line starting — no inner scroll to discover.
F3 — no way back from the final frame (final row holds only "I agree";
  the 47 jewel dots are display-only spans). Fix, both legs: (a) a
  working Back on the final frame — a clone of frame 46's Back button
  (same node, same classes; a clone carries no listener), wired to step
  back one frame; (b) the jewel dots become real navigation — tap a dot,
  go to its frame, and the lit dot follows every move (row taps included).
F7 — red seal only on frame 1; final frame 1 button with its seal
  display:none. Fix: frame 1's red seal is cloned into every foot that
  lacks one, just above the button row — the same node, the same 72px
  seal, on all 47 frames. The final frame's row becomes Back + I-agree
  with its seal shown in the foot. NOTE on #dealSeal: the end card's
  seal stays hidden until the citizen clicks "I agree" — it is the
  agree stamp (wireAgree unhides it + stamps it on agree, then
  navigates); unhiding it early would fake the stamp. The frame seal in
  the foot is the seal the brief means by "shown".
"""
import hashlib

CSS9 = """
<style id="fpFrame9">
/* ============ FRAME-9 (2026-11-19) — the fix-8 shell, three gaps closed ============
   F1: the media board slims so the first agreement words show at load.
   Orb 60 -> 48 (the label block beside it is ~50 tall, so the row drops
   to ~50); video pill padding 16 -> 10; board padding 10 -> 8; title
   margin 4 -> 2; video margin-top 10 -> 8; board margin-bottom 12 -> 8. */
.frame-media{padding:8px 16px!important;margin-bottom:8px!important}
.frame-media-title{margin-bottom:2px!important}
.frame-media .play-btn{width:48px!important;height:48px!important}
.frame-media .frame-video-btn{margin-top:8px!important;padding:10px 46px!important}
/* F1: lift the text — the agreement board's top margin 22 -> 8 and its top
   padding 20 -> 12, on every frame alike, so the first line lifts. */
.frame-scroll>.ib-nutshell{margin-top:8px!important;padding-top:12px!important}
/* F1: grow the reading window — the foot pills slim 16 -> 12 padding
   (still real pills, white words, own-colour rims) and the top bar
   closes up 8 -> 4. */
.frame-foot button{padding-top:12px!important;padding-bottom:12px!important}
.frame-topbar{margin-bottom:4px!important}
/* F3: the jewel dots are real navigation now — a pointer, and a lit hover. */
#deckDots .ldot{cursor:pointer}
#deckDots .ldot:hover{filter:brightness(1.35)}
/* F7: the seal on every frame is frame 1's seal cloned (JS9) — no new
   styling; the 72px seal and its mark already read on frame 1. */
</style>
"""

JS9 = """
<script>
/* ============ FRAME-9 (2026-11-19) — seal on every frame, a way back, dots that go ============
   Runs after wireFrame8. It does NOT touch the deck mechanics' outcomes:
   Keep reading / Back / read-it-all / the agree stamp all run exactly as
   before — FIX9 only adds the seal to the feet that lack one, adds a Back
   to the final row, and wires the jewel dots to the frame they name. */
(function wireFrame9(){
  var main = document.getElementById('deckUnfold');
  var deckBody = document.getElementById('deckBody');
  var beats = Array.prototype.slice.call(document.querySelectorAll('#deckBody .letter-beat'));
  var dots = Array.prototype.slice.call(document.querySelectorAll('#deckDots .ldot'));
  function syncDots(n){
    dots.forEach(function(d, j){ d.classList.toggle('on', j === n); });
  }
  function syncDotsNow(){
    var cur = -1;
    beats.forEach(function(b, j){ if (b.classList.contains('frame-now')) cur = j; });
    if (cur >= 0) syncDots(cur);
  }
  /* F3 — one frame function, the frame-8 one verbatim: one tap = one frame,
     the shown beat unhidden, the scroll windows reset, the lit dot follows. */
  function showFrame9(n){
    if (n < 0) n = 0;
    if (n > beats.length - 1) n = beats.length - 1;
    beats.forEach(function(b, j){
      var on = (j === n);
      b.classList.toggle('frame-now', on);
      if (on) b.hidden = false;
    });
    if (main) main.classList.toggle('frame-past-1', n > 0);
    if (deckBody) deckBody.scrollTop = 0;
    var sc = beats[n] ? beats[n].querySelector('.frame-scroll') : null;
    if (sc) sc.scrollTop = 0;
    syncDots(n);
  }
  /* F7 — the red seal on every frame: clone frame 1's seal (the same node,
     the same classes, nothing new) into each foot that lacks one, just
     above the button row. Frame 1 keeps its own. */
  var seal0 = beats[0] && beats[0].querySelector('.frame-foot .frame-red-n');
  beats.forEach(function(b, i){
    if (i === 0) return;
    var foot = b.querySelector('.frame-foot');
    var row = b.querySelector('.frame-btnrow');
    if (!foot || !row || !seal0) return;
    if (foot.querySelector('.frame-red-n')) return;
    foot.insertBefore(seal0.cloneNode(true), row);
  });
  /* F3 — the jewel dots are real navigation now: tap a dot, go to its
     frame. They were display-only spans; they keep their look, their
     colours, their lit state — they only gain the tap. */
  var dotsBox = document.getElementById('deckDots');
  if (dotsBox) dotsBox.removeAttribute('aria-hidden');
  dots.forEach(function(d, j){
    d.setAttribute('role', 'button');
    d.setAttribute('tabindex', '0');
    d.setAttribute('title', 'Go to frame ' + (j + 1) + ' of ' + dots.length);
    d.setAttribute('aria-label', 'Go to frame ' + (j + 1));
    var go = function(ev){ if (ev) ev.stopPropagation(); showFrame9(j); };
    d.addEventListener('click', go);
    d.addEventListener('keydown', function(ev){
      if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); go(ev); }
    });
  });
  /* F3 — Back on the final frame: clone frame 46's Back button (the same
     node, the same classes; a clone carries no listener) into the final
     row, first, beside the I-agree action. It steps back one frame. A
     Next on the last frame would be a dead control pointing nowhere, so
     the row is complete at Back + I-agree. */
  var last = beats[beats.length - 1];
  var lastRow = last && last.querySelector('.frame-btnrow');
  var backSrc = beats.length > 1 ? beats[beats.length - 2].querySelector('.frame-btnrow .deck-back') : null;
  if (lastRow && backSrc && !lastRow.querySelector('.deck-back')) {
    var back = backSrc.cloneNode(true);
    back.hidden = false;
    back.disabled = false;
    back.classList.remove('frame-back-off');
    back.removeAttribute('aria-disabled');
    back.addEventListener('click', function(ev){
      ev.stopPropagation();
      showFrame9(beats.length - 2);
    });
    lastRow.insertBefore(back, lastRow.firstChild);
  }
  /* Keep the lit dot honest on every path: the frame-8 Next/Back buttons
     move the frame without passing through here, so sync after any row
     tap, and after read-it-all. */
  beats.forEach(function(b){
    var row = b.querySelector('.frame-btnrow');
    if (!row) return;
    Array.prototype.slice.call(row.querySelectorAll('button')).forEach(function(btn){
      btn.addEventListener('click', function(){ setTimeout(syncDotsNow, 0); });
    });
  });
  var all = document.getElementById('deckAll');
  if (all) all.addEventListener('click', function(){ setTimeout(syncDotsNow, 0); });
  syncDotsNow();
})();
</script>
"""
