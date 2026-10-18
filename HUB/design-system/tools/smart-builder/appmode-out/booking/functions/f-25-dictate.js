/* NayaFunction: dictate v1.0.0
   What: SpeechRecognition dictation into #visionText via #dictBtn.
   Activation: <div data-fn="dictate" data-fn-config='{}'></div>
   Config: { idleLabel, listeningLabel, noSRMessage } — every key documented, all optional unless marked *
   Ready behavior: fully client-side; without SpeechRecognition the button shows an inline
     message (never alert()) telling the user to type/paste instead.
   Connected behavior: none
   Backend twin: none
*/
(function(){
'use strict';
var NF = window.NayaFunctions = window.NayaFunctions || {};
NF._r = NF._r || {};
NF.register = NF.register || function(id, def){
  if (NF._r[id]) return; // one function, one implementation — never double-register
  NF._r[id] = def;
};
NF.get = NF.get || function(id){ return NF._r[id] || null; };

NF.register('dictate', {
  version: '1.0.0',
  activate: function(root, config){
    config = config || {};
    // 1. Idempotent: activating twice on the same root binds once (L-2026-10-17-004).
    //    Key is namespaced per unit so multiple intake units can share one page root.
    if (root.dataset.nfBound_dictate) return { destroy: function(){} };
    root.dataset.nfBound_dictate = '1';

    var btn = root.querySelector('#dictBtn');
    var vision = root.querySelector('#visionText');
    // 2. Fail soft: if required DOM is absent, do nothing harmful.
    if (!btn || !vision) return { destroy: function(){} };

    var IDLE = config.idleLabel || btn.textContent.trim() || 'START DICTATING';
    var LISTENING = config.listeningLabel || 'LISTENING — tap to stop';
    var NO_SR = config.noSRMessage || 'Dictation needs Chrome or Edge — type or paste instead.';
    var prev = btn.onclick;
    var rec = null;
    var msg = null;

    function showNoSR(){
      // Inline fail-soft message, never alert() — white text per Law 1.
      if (msg) msg.remove();
      msg = document.createElement('span');
      msg.setAttribute('data-nf', 'dictate-nosr');
      msg.style.cssText = 'color:#fff;font-size:13px;margin-left:10px;';
      msg.textContent = NO_SR;
      btn.insertAdjacentElement('afterend', msg);
      setTimeout(function(){ if (msg){ msg.remove(); msg = null; } }, 5000);
    }

    // Harvested verbatim from ultimate-intake.html dictation block;
    // selectors retargeted to the unit root; alert() replaced by inline message.
    btn.onclick = function(){
      var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (!SR){ showNoSR(); return; }
      if (rec){ rec.stop(); rec = null; btn.textContent = IDLE; return; }
      rec = new SR(); rec.continuous = true; rec.interimResults = true;
      rec.onresult = function(e){ var t=''; for (var i=0;i<e.results.length;i++) t += e.results[i][0].transcript; vision.value = t; };
      rec.onend = function(){ btn.textContent = IDLE; rec = null; };
      rec.onerror = function(){ btn.textContent = IDLE; rec = null; }; // fail-soft: mic denied etc.
      rec.start(); btn.textContent = LISTENING;
    };
    btn.setAttribute('data-nf-unit', 'dictate');

    return { destroy: function(){
      if (rec){ try{ rec.stop(); }catch(e){} rec = null; }
      if (msg){ msg.remove(); msg = null; }
      if (btn) btn.onclick = prev;
      delete root.dataset.nfBound_dictate;
    } };
  }
});
})();
