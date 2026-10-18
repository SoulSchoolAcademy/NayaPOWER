/* NayaFunction: preview v1.0.0
   What: Real sample preview — a .tcard2 .tview carrying data-href opens the sample page.
   Activation: <div data-fn="preview" data-fn-config='{}'></div>
   Config: { target } — every key documented, all optional unless marked *
   Ready behavior: fully client-side. Binds ONLY .tview elements (or their .tcard2 card)
     that carry a data-href; views without one are left untouched (her select toggle
     keeps working — the unit never fights the host page).
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

NF.register('preview', {
  version: '1.0.0',
  activate: function(root, config){
    config = config || {};
    if (root.dataset.nfBound_preview) return { destroy: function(){} };
    root.dataset.nfBound_preview = '1';

    var target = config.target || '_blank';
    var bound = [];

    // Harvested verbatim from ultimate-intake.html preview wiring
    // (.tmpl .viewbtn → window.open(b.dataset.href,'_blank')),
    // retargeted to her hooks: .tcard2 .tview + data-href.
    // Wire ONLY inside root, and only elements that carry data-href (L-2026-10-17-004).
    Array.prototype.forEach.call(root.querySelectorAll('.tcard2 .tview'), function(v){
      var href = v.getAttribute('data-href') ||
                 (v.closest('.tcard2') || {}).getAttribute &&
                 v.closest('.tcard2').getAttribute('data-href');
      if (!href) return; // no sample href → leave her handler alone (no dead control, no fight)
      if (v.dataset.nfPreview) return; // per-element idempotency
      v.dataset.nfPreview = '1';
      var prev = v.onclick;
      bound.push([v, prev]);
      v.onclick = function(e){
        if (e) e.stopPropagation(); // keep the card's select toggle from also firing
        window.open(href, target);
      };
      v.setAttribute('data-nf-unit', 'preview');
    });

    return { destroy: function(){
      bound.forEach(function(pair){ pair[0].onclick = pair[1]; delete pair[0].dataset.nfPreview; });
      delete root.dataset.nfBound_preview;
    } };
  }
});
})();
