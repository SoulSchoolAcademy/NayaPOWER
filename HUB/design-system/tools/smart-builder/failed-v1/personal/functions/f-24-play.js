/* NayaFunction: f-24-play v1.0.0
   What: real audio player — play / pause / seek for a configured URL (HTMLAudioElement).
   Activation: <div data-fn="f-24-play" data-fn-config='{"url":"./demo-assets/tone.wav","title":"Welcome tone"}'></div>
   Config:
     url*: audio URL. If absent the unit says so (fail-soft) instead of rendering dead controls.
     title: label shown above the player (default "Audio").
     accent: hex — player chrome color (default #40d3bb teal).
   Ready behavior: play/pause toggles a real HTMLAudioElement; the seek bar scrubs currentTime;
     time reads current / duration; load errors show an inline message, never a dead play button.
   Connected behavior: none.
   Backend twin: none.
   Lessons: L-2026-10-16-005 (no staged play button — the button plays real audio), L-2026-10-17-004.
*/
(function(){
'use strict';
var NF = window.NayaFunctions = window.NayaFunctions || {};
NF._r = NF._r || {};
NF.register = NF.register || function(id, def){ if (NF._r[id]) return; NF._r[id] = def; };

function fmt(s){
  if (!isFinite(s) || s < 0) s = 0;
  var m = Math.floor(s / 60), sec = Math.floor(s % 60);
  return m + ':' + (sec < 10 ? '0' : '') + sec;
}

NF.register('f-24-play', {
  version: '1.0.0',
  activate: function(root, config){
    config = config || {};
    var url = String(config.url || '').trim();
    var title = config.title || 'Audio';
    var accent = config.accent || '#40d3bb';

    root.innerHTML = '';
    var wrap = document.createElement('div');

    var t = document.createElement('p');
    t.textContent = title;
    t.style.cssText = 'color:#ffffff;font-size:15px;font-weight:600;margin:0 0 12px;';
    wrap.appendChild(t);

    if (!url) {
      var note = document.createElement('p');
      note.textContent = 'No audio URL configured — nothing to play.';
      note.style.cssText = 'color:#F8F7FB;font-size:14px;margin:0;';
      wrap.appendChild(note);
      root.appendChild(wrap);
      return { destroy: function(){} }; // fail-soft: no fake controls
    }

    var audio = document.createElement('audio');
    audio.preload = 'metadata';
    audio.src = url;

    var row = document.createElement('div');
    row.style.cssText = 'display:flex;align-items:center;gap:12px;';

    var playBtn = document.createElement('button');
    playBtn.type = 'button'; playBtn.textContent = 'Play';
    playBtn.className = 'nf24-play';
    playBtn.style.cssText = 'flex:none;width:88px;padding:12px 0;font-size:15px;font-weight:700;color:#ffffff;' +
      'background:#0b0b10;border:1.5px solid rgba(255,255,255,.55);border-radius:12px;cursor:pointer;';

    var seek = document.createElement('input');
    seek.type = 'range'; seek.min = '0'; seek.max = '100'; seek.value = '0'; seek.step = '0.1';
    seek.setAttribute('aria-label', 'Seek');
    seek.className = 'nf24-seek';
    seek.style.cssText = 'flex:1;accent-color:' + accent + ';';

    var time = document.createElement('span');
    time.textContent = '0:00 / 0:00';
    time.style.cssText = 'flex:none;color:#F8F7FB;font-size:13px;min-width:104px;text-align:right;';
    row.appendChild(playBtn); row.appendChild(seek); row.appendChild(time);
    wrap.appendChild(row);

    wrap.appendChild(audio); // in-DOM so host pages and tests can reach it; no controls shown

    var err = document.createElement('p');
    err.setAttribute('role', 'alert');
    err.style.cssText = 'color:#F8F7FB;font-size:13px;margin:10px 0 0;display:none;';
    wrap.appendChild(err);

    var dragging = false;
    function paint(){
      var d = audio.duration || 0, c = audio.currentTime || 0;
      if (!dragging && d > 0) seek.value = String((c / d) * 100);
      time.textContent = fmt(c) + ' / ' + fmt(d);
    }
    playBtn.addEventListener('click', function(){
      if (audio.paused) {
        var p = audio.play();
        if (p && typeof p.then === 'function') {
          p.then(function(){}, function(e){
            err.textContent = '! Playback was blocked or failed: ' + (e && e.message ? e.message : e);
            err.style.display = 'block';
          });
        }
      } else { audio.pause(); }
    });
    audio.addEventListener('play', function(){ playBtn.textContent = 'Pause'; playBtn.style.borderColor = accent; playBtn.style.boxShadow = '0 0 18px -4px ' + accent; });
    audio.addEventListener('pause', function(){ playBtn.textContent = 'Play'; playBtn.style.borderColor = 'rgba(255,255,255,.55)'; playBtn.style.boxShadow = 'none'; });
    audio.addEventListener('timeupdate', paint);
    audio.addEventListener('loadedmetadata', paint);
    audio.addEventListener('error', function(){
      err.textContent = '! Could not load the audio at the configured URL.';
      err.style.display = 'block';
      playBtn.disabled = true; playBtn.style.opacity = '0.4';
    });
    seek.addEventListener('pointerdown', function(){ dragging = true; });
    seek.addEventListener('pointerup', function(){ dragging = false; });
    seek.addEventListener('input', function(){
      var d = audio.duration || 0;
      if (d > 0) audio.currentTime = (parseFloat(seek.value) / 100) * d;
      paint();
    });
    paint();

    root.appendChild(wrap);
    return { destroy: function(){ try { audio.pause(); } catch (e) {} root.innerHTML = ''; } };
  }
});
})();
