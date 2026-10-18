/* NayaFunction: copy v1.0.0
   What: Clipboard copy of #contract text via #copyBtn (or a BUTTON #btnCopy).
   Activation: <div data-fn="copy" data-fn-config='{}'></div>
   Config: { copiedLabel, manualLabel, failedLabel } — every key documented, all optional unless marked *
   Ready behavior: fully client-side. navigator.clipboard when available; inline fallback
     label when clipboard is unavailable or the write rejects (never alert()).
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

NF.register('copy', {
  version: '1.0.0',
  activate: function(root, config){
    config = config || {};
    if (root.dataset.nfBound_copy) return { destroy: function(){} };
    root.dataset.nfBound_copy = '1';

    var contract = root.querySelector('#contract');
    // Fail soft: nothing to copy without the contract node.
    if (!contract) return { destroy: function(){} };

    // Bind #copyBtn and #btnCopy — but only real BUTTON controls. In Verity's
    // factory file #btnCopy is a <pre> code sample (copied by her copyCode()),
    // so the tag guard keeps that behavior untouched.
    var targets = [];
    ['#copyBtn', '#btnCopy'].forEach(function(sel){
      var el = root.querySelector(sel);
      if (el && el.tagName === 'BUTTON' && targets.indexOf(el) === -1) targets.push(el);
    });
    if (!targets.length) return { destroy: function(){} };

    var COPIED = config.copiedLabel || 'COPIED \u2713';
    var MANUAL = config.manualLabel || 'SELECT + COPY MANUALLY';
    var FAILED = config.failedLabel || 'COPY FAILED — SELECT MANUALLY';
    var prev = targets.map(function(el){ return el.onclick; });

    // Harvested verbatim from ultimate-intake.html copy block;
    // selectors retargeted to the unit root; promise rejection now fails soft.
    targets.forEach(function(el){
      el.onclick = function(){
        var t = contract.textContent;
        if (navigator.clipboard){
          navigator.clipboard.writeText(t).then(
            function(){ el.textContent = COPIED; },
            function(){ el.textContent = FAILED; }
          );
        } else { el.textContent = MANUAL; }
      };
      el.setAttribute('data-nf-unit', 'copy');
    });

    return { destroy: function(){
      targets.forEach(function(el, i){ el.onclick = prev[i]; });
      delete root.dataset.nfBound_copy;
    } };
  }
});
})();
