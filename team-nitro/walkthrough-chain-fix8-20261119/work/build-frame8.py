#!/usr/bin/env python3
"""FIX8 frame transform (2026-11-19): the agreement shell, fixed at desktop
1920 after the eye's GOES BACK on fix-7 (F1-F9). Takes the fix-7 unfold
bytes (117,636 B, sha e21f08d0) and edits ONLY the shell — every beat's
words, pictures, tones, feet, deck mechanics, end card and agree handler
are untouched (verified by content guards + beat/article counts).

Diagnosis, measured in the VM Chromium render probe at 1920x999 (and read
in the screenshots — t+1.5s strip, t+5.5s blank ornate frame):
  F1 — deckBody is 86px tall: the page header (steplabel + H1 + sub +
    120px play orb + note, ~300px) + dots (97px) + foot-links (58px) eat
    the 579px content box, so the beat's inner scroller is 0px and its
    foot (red seal + buttons) sits below the visible strip. FIX: the
    frame's top bar carries the headline, so the page header goes away
    on every frame; dots + foot-links go slim; the seal scales 120->84.
  F2 — the master frame PNG has an OPAQUE black centre (my first alpha
    read was wrong: I sampled PNG scanlines without unfiltering). The
    .naya-frame layer sits at z-index 60 ABOVE the stage (z 10), so once
    the 1.68MB image loads (~seconds in) it paints over all content.
    FIX: the frame layer goes BEHIND the stage (z-index 0) — its black
    centre becomes the backdrop, the ornament frames the content.
  F3 — Next/Keep reading never visibly advances twice: FIX7's delegated
    handler keys the advance off the beat's fp-smart-visual class, which
    wireDeck never clears on advance, so the second click stays; and the
    Next button double-clicks kr on a 140ms timer. FIX: FIX8 owns
    navigation with its own per-beat phase model (talk/visual), one
    kr.click() per Next, stopPropagation so FIX7's delegated handler
    never double-handles.
  F4 — Play (speech synthesis) produces nothing audible or visible on
    desktop (no voice -> 2.5s watchdog -> idle). FIX: the play orb moves
    into the media frame and drives the verified narration mp3 (F9).
  F5 — all 8 face images + deck-logo + welcome-0 serve HTTP 200 from
    the proof-host (~485-528KB each); the one failed load was transient.
    FIX: an onerror chain (retry once cache-busted, then the filed
    crystal-n.png) so a top-bar picture never shows broken.
  F6 — lives in the WELCOME file, not the unfold: a fresh visitor (no
    saved alias) auto-enters the stage on load, so the agreement bridge
    covers the entrance + nav. Fixed in welcome-staged.html (this
    round's other file); the unfold is untouched by it.
  F7 — the DOM already has three buttons per row (Back hidden on frame
    1); the eye counted two because the foot sat below the strip. FIX:
    frame 1's Back shows disabled (three-button row on every frame);
    the final frame's I-agree button moves into the pinned foot row;
    the red seal is visible once the foot is (F1).
  F8 — no Welcome button or pill is introduced anywhere in this round
    (grep-verified in the transform guards).
  F9 — media frame on frame 1, just below the top bar: AUDIO on top
    (the verified agreement-naya-voice.mp3, 5,976,421 B, 12m27s, filed
    this round), VIDEO below (a slot: no verified anthem video exists
    yet — the Oct-29 mp4 predates the anthem and the NotebookLM m4a
    files must NEVER go on the page — so the button reveals the
    anthem's opening words + a plain note that the captioned video is
    on its way, and takes the captioned file on a one-line swap).
"""
import hashlib

AUDIO_SHA256 = "62bf05e68a036e86b5aa3280c16b9dd810dda711abf1fd34612cda10b2b9261a"
CRYSTAL_CB = "ee4b627c0c254ed9165715308fa282010ce8cf3c"
PH = "https://naya-proof-host.nayapower.workers.dev/?file=team-nitro/agreement-unfold-20261117/"
AUDIO_URL = PH + "agreement-naya-voice.mp3&ref=walkthrough/chain-fix8-20261119&cb=" + AUDIO_SHA256
CRYSTAL_URL = PH + "crystal-n.png&ref=walkthrough/chain-fix8-20261119&cb=" + CRYSTAL_CB

CSS8 = """
<style id="fpFrame8">
/* ============ FRAME-8 (2026-11-19) — the fix-7 shell, fixed at desktop ============
   F2: the frame goes BEHIND the stage. The master-frame PNG's centre is
   opaque black (not transparent), and at z-index 60 it painted over all
   content once loaded. At z-index 0 its black centre is the backdrop and
   the silver ornament frames the content. */
.naya-frame{z-index:0}
/* F1: the page header goes away on every frame — the per-frame top bar
   carries the headline (frame 1: "Hi, I'm Naya"). The play orb is not
   deleted: it moves into the media frame (F4/F9), so .play-wrap hides
   with the rest of the header. */
main.fp-frame8 .letter-steplabel,main.fp-frame8 .deal-title,main.fp-frame8 .deck-sub,
main.fp-frame8 .play-wrap,main.fp-frame8 .play-note{display:none!important}
/* F1: dots + read-it-all on one slim row; foot-links slim. This hands the
   freed ~200px back to #deckBody, so the beat's inner scroller is a real
   reading window and the pinned foot is in view. */
#deckControls{flex-direction:row!important;align-items:center!important;justify-content:center!important;gap:16px!important;margin-top:6px!important}
#deckControls .letter-dots{gap:6px}
#deckControls .ldot{width:10px;height:10px}
#deckControls .letter-all{padding:6px 10px;min-height:44px}
.foot-links{margin:8px 0 0!important}
/* F1+F7: the foot tightens; the red seal scales 120 -> 84 (still the big
   red piece, still just above the three buttons — now visible). */
.frame-foot{gap:8px;padding-top:8px}
.frame-red-n{width:84px!important;height:84px!important}
.frame-red-n .deal-seal-mark{font-size:38px!important}
/* F7: frame 1's Back is present but disabled — three buttons on every
   frame. Disabled is a state (opacity), never gray text. */
.frame-back-off{opacity:.55;cursor:default}
/* F9: the media frame — an obsidian board, just below the top bar on
   frame 1. AUDIO on top, VIDEO below. Same board anatomy as the beats. */
.frame-media{margin:0 0 16px;padding:18px 20px;border:1.5px solid rgba(255,255,255,.32);border-radius:22px;background:#050607;box-shadow:0 18px 40px rgba(0,0,0,.65),inset 0 1px 0 rgba(255,255,255,.14)}
.frame-media-title{font-family:Marcellus,Georgia,serif;font-size:25px;line-height:1.15;color:#fff;margin:0 0 6px;text-align:center}
.frame-media-sub{font-size:17px;line-height:1.5;color:#fff;text-align:center;margin:0 0 14px}
.frame-media-audio{display:flex;align-items:center;gap:16px;justify-content:center}
.frame-media .play-btn{width:72px;height:72px;flex:none}
.frame-media .play-btn .play-name{display:none}
.frame-media .play-btn.is-playing{border-color:#8e24aa;box-shadow:inset 0 1.5px 0 rgba(255,255,255,.55),inset 0 -4px 8px rgba(0,0,0,.5),0 0 38px -2px #8e24aa,0 12px 26px rgba(0,0,0,.6)}
.frame-media-audio-name{font-size:17px;font-weight:700;color:#fff}
.frame-media-audio-state{font-size:17px;line-height:1.5;color:#fff;margin-top:4px}
.frame-media .frame-video-btn{width:100%;justify-content:center;margin-top:14px}
.frame-anthem-note{font-size:17px;line-height:1.6;color:#fff;margin:14px 0 0;text-align:left}
.frame-anthem-note[hidden]{display:none}
.frame-anthem-note p{margin:0 0 12px}
.frame-anthem-note p:last-child{margin-bottom:0}
#fpAgreeAudio{display:none}
</style>
"""

JS8 = """
<script>
/* ============ FRAME-8 (2026-11-19) — own the navigation, the media, the faces ============
   Runs after wireFrame7. It does NOT touch the deck mechanics' outcomes:
   Keep reading / Back / read-it-all / the dots / the agree stamp all run
   exactly as before — FIX8 only decides WHICH frame shows, and drives the
   deck's own buttons to get there (one kr.click() per move, never two). */
(function wireFrame8(){
  var main = document.getElementById('deckUnfold');
  var deckBody = document.getElementById('deckBody');
  if (main) main.classList.add('fp-frame8');
  var beats = Array.prototype.slice.call(document.querySelectorAll('#deckBody .letter-beat'));
  var CRYSTAL = '__CRYSTAL_URL__';
  var AUDIO_URL = '__AUDIO_URL__';
  function hasShowcase(b){ return !!b.querySelector('.lb-showcase'); }
  /* F5 — a top-bar picture never shows broken: retry once cache-busted,
     then the filed crystal N (a real asset, always served). */
  beats.forEach(function(b){
    var img = b.querySelector('.frame-face');
    if (!img) return;
    img.setAttribute('decoding', 'async');
    img.addEventListener('error', function(){
      var n = parseInt(img.getAttribute('data-fx8fb') || '0', 10);
      if (n === 0) { img.setAttribute('data-fx8fb', '1'); img.src = img.src + '&fx8=1'; }
      else if (n === 1) { img.setAttribute('data-fx8fb', '2'); img.src = CRYSTAL; }
    });
  });
  /* F3 — FIX8 owns the frame. One phase per beat (talk/visual), tracked
     here — never read back off the deck's fp-smart-visual class, which
     wireDeck leaves set after an advance (that stale read is why the
     second Next click stayed on frame 1). stopPropagation keeps FIX7's
     delegated deckBody handler from double-handling the same click. */
  var phase = beats.map(function(){ return 'talk'; });
  function showFrame8(n){
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
  }
  beats.forEach(function(b, i){
    var row = b.querySelector('.frame-btnrow');
    if (!row) return;
    var kr = row.querySelector('.deck-next:not(.deck-back):not(.frame-next)');
    var back = row.querySelector('.deck-back');
    var nx = row.querySelector('.frame-next');
    if (kr) kr.addEventListener('click', function(ev){
      ev.stopPropagation();
      if (hasShowcase(b) && phase[i] === 'talk') { phase[i] = 'visual'; return; }
      phase[i] = 'talk';
      showFrame8(i + 1);
    });
    if (back) back.addEventListener('click', function(ev){
      ev.stopPropagation();
      if (phase[i] === 'visual') { phase[i] = 'talk'; return; }
      showFrame8(i - 1);
      var p = beats[i - 1];
      if (p) phase[i - 1] = hasShowcase(p) ? 'visual' : 'talk';
    });
    /* F3 — the Next button clicks Keep reading ONCE. FIX7's 140ms second
       click is gone (its listener dies with the cloned node). */
    if (nx && kr) {
      var nx2 = nx.cloneNode(true);
      nx.parentNode.replaceChild(nx2, nx);
      nx2.addEventListener('click', function(ev){
        ev.stopPropagation();
        kr.click();
      });
    }
  });
  /* F7 — frame 1's Back shows, disabled: three buttons on every frame. */
  var back0 = beats[0] && beats[0].querySelector('.frame-btnrow .deck-back');
  if (back0) {
    back0.hidden = false;
    back0.disabled = true;
    back0.classList.add('frame-back-off');
    back0.setAttribute('aria-disabled', 'true');
  }
  /* F7 — the final frame's I-agree button moves into the pinned foot row,
     beside Back, so the climax action is never below the fold. Its own
     agree listener travels with the node, untouched. */
  var last = beats[beats.length - 1];
  var agreeBtn = document.getElementById('dealAgreeBtn');
  var lastRow = last && last.querySelector('.frame-btnrow');
  if (agreeBtn && lastRow) lastRow.appendChild(agreeBtn);
  /* F4+F9 — the media frame on frame 1, just below the top bar. The play
     orb moves here (its node is cloned, so wirePlay's speech listener —
     attached to the original node — never fires; the original leaves the
     DOM). The orb now drives the verified narration mp3, visibly:
     triangle <-> pause bars, rim lit while playing, elapsed / total in
     words beside it. The video button is a slot, not a wire-up: no
     verified anthem video exists yet, so it reveals the anthem's opening
     words + a plain note, and takes the captioned file on a one-line
     swap (see the data-anthem-slot hook below). The Oct-29 mp4 and the
     NotebookLM m4a files are NEVER wired here. */
  var playBtn = document.getElementById('playBtn');
  var sc0 = beats[0] && beats[0].querySelector('.frame-scroll');
  if (playBtn && sc0) {
    var audio = document.createElement('audio');
    audio.id = 'fpAgreeAudio';
    audio.preload = 'none';
    audio.src = AUDIO_URL;
    var media = document.createElement('div');
    media.className = 'frame-media';
    media.id = 'fpMediaFrame';
    var ttl = document.createElement('div');
    ttl.className = 'frame-media-title';
    ttl.textContent = 'Hello. I\u2019m Naya.';
    var sub = document.createElement('p');
    sub.className = 'frame-media-sub';
    sub.textContent = 'Listen to the agreement, or watch the anthem.';
    var arow = document.createElement('div');
    arow.className = 'frame-media-audio';
    var orb = playBtn.cloneNode(true);
    playBtn.parentNode.removeChild(playBtn);
    var lab = document.createElement('div');
    var labT = document.createElement('div');
    labT.className = 'frame-media-audio-name';
    labT.textContent = 'Play \u2014 listen to the agreement';
    var labS = document.createElement('div');
    labS.className = 'frame-media-audio-state';
    labS.id = 'fpAudioState';
    labS.textContent = '12:27 \u00b7 Naya reads the agreement';
    lab.appendChild(labT);
    lab.appendChild(labS);
    arow.appendChild(orb);
    arow.appendChild(lab);
    var vbtn = document.createElement('button');
    vbtn.type = 'button';
    vbtn.className = 'p3-enter frame-video-btn';
    vbtn.id = 'fpAnthemVideoBtn';
    vbtn.setAttribute('data-anthem-slot', 'anthem-video-slot');
    vbtn.textContent = '\u25B6 Watch the anthem \u25C6';
    var note = document.createElement('div');
    note.className = 'frame-anthem-note';
    note.id = 'fpAnthemNote';
    note.hidden = true;
    var n1 = document.createElement('p');
    n1.textContent = 'How much of your digital life feels scattered? Your notes, your bookmarks, your plans \u2014 they live in different places, across disconnected tools that don\u2019t speak to one another.';
    var n2 = document.createElement('p');
    n2.textContent = 'The captioned anthem video arrives soon. These are its opening words, while the video is on its way.';
    note.appendChild(n1);
    note.appendChild(n2);
    media.appendChild(ttl);
    media.appendChild(sub);
    media.appendChild(arow);
    media.appendChild(vbtn);
    media.appendChild(note);
    media.appendChild(audio);
    sc0.insertBefore(media, sc0.firstChild);
    function fmt(s){
      s = Math.max(0, Math.floor(s || 0));
      var m = Math.floor(s / 60), r = s % 60;
      return m + ':' + (r < 10 ? '0' : '') + r;
    }
    function setState(){
      var playing = !audio.paused && !audio.ended;
      orb.classList.toggle('is-playing', playing);
      var tri = orb.querySelector('.play-tri');
      if (tri) tri.textContent = playing ? '\u275A\u275A' : '\u25B6';
      if (playing) labS.textContent = 'Playing \u00b7 ' + fmt(audio.currentTime) + ' / 12:27 \u2014 Naya reads the agreement';
      else if (audio.currentTime > 0) labS.textContent = 'Paused \u00b7 ' + fmt(audio.currentTime) + ' / 12:27 \u2014 tap to keep listening';
      else labS.textContent = '12:27 \u00b7 Naya reads the agreement';
    }
    orb.addEventListener('click', function(ev){
      ev.stopPropagation();
      if (audio.paused) {
        var pr = audio.play();
        if (pr && pr.catch) pr.catch(function(){ labS.textContent = 'The audio didn\u2019t load \u2014 tap to try again.'; });
      } else audio.pause();
    });
    audio.addEventListener('play', setState);
    audio.addEventListener('pause', setState);
    audio.addEventListener('ended', function(){ audio.currentTime = 0; setState(); });
    audio.addEventListener('timeupdate', setState);
    audio.addEventListener('error', function(){ labS.textContent = 'The audio didn\u2019t load \u2014 tap to try again.'; });
    vbtn.addEventListener('click', function(ev){
      ev.stopPropagation();
      note.hidden = !note.hidden;
    });
    setState();
  }
  showFrame8(0);
})();
</script>
"""
