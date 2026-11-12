/* Smart Block: chat/sp-audio-msg
 * Source: Smart Spaces Page Design.html (extracted byte-true, never rewritten)
 * Adapted from renderAudioMsg (~line 1791). App-state calls replaced by params:
 *   s.color     -> opts.accent
 *   m.audioLabel -> opts.label (also seeds the waveform bar heights)
 *   m.audioData -> opts.audioSrc (Data URL or URL; optional)
 *   toast()     -> onPlay callback (no silent failures invented)
 * The specimen must set --sc (via opts.accent), e.g. --sc:#7c3aed.
 */
(function(){
'use strict';

/* ============ helper (from source ~line 724) ============ */
function el(tag, cls, text){
  var e = document.createElement(tag);
  if(cls) e.className = cls;
  if(text !== undefined && text !== null) e.textContent = text;
  return e;
}

/* ---- audio message with waveform ----
 * opts = {label:'0:24', accent:'#7c3aed', bars:24, audioSrc?, onPlay?}
 * opts.onPlay(box) is called on click when no audioSrc is provided.
 */
function spAudioMsg(opts){
  opts = opts || {};
  var label = String(opts.label || '0:00');
  var box = el('div','sp-audio-msg');
  box.style.setProperty('--sc', opts.accent || '#7c3aed');
  var play = el('button','sp-audio-play','▶');
  var wave = el('div','sp-audio-wave');
  var bars = opts.bars || 24;
  var seed = 0;
  for(var i=0;i<label.length;i++) seed += label.charCodeAt(i);
  for(var i=0;i<bars;i++){
    var b = el('i');
    var h = 4 + ((seed * (i+7)) % 20);
    b.style.height = h + 'px';
    wave.appendChild(b);
  }
  var dur = el('span','sp-audio-dur', label);
  var audioEl = null;
  play.addEventListener('click', function(){
    if(!opts.audioSrc){
      if(typeof opts.onPlay === 'function') opts.onPlay(box);
      return;
    }
    if(!audioEl){
      audioEl = new Audio(opts.audioSrc);
      audioEl.onended = function(){ play.textContent = '▶'; };
    }
    if(audioEl.paused){ audioEl.play(); play.textContent = '⏸'; }
    else { audioEl.pause(); play.textContent = '▶'; }
  });
  box.appendChild(play); box.appendChild(wave); box.appendChild(dur);
  return box;
}

/* expose */
window.spAudioMsg = spAudioMsg;

/* Demo:
   var wrap = document.createElement('div');
   wrap.style.setProperty('--sc', '#7c3aed');   // specimen must set --sc
   wrap.appendChild(spAudioMsg({label:'0:24', accent:'#7c3aed'}));
   document.body.appendChild(wrap);
*/
})();
