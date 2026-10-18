/* NayaFunction: contract-draft v1.0.0
   What: Drafts the design-build contract from vision + template + feature toggles + cart.
   Activation: <div data-fn="contract-draft" data-fn-config='{}'></div>
   Config: { } — every key documented, all optional unless marked *
   Ready behavior: fully client-side. #buildBtn drafts text into #contract and reveals
     #contractWrap. NayaFunctions.get('contract-draft').collect() returns structured
     state { vision, template, functions[], pieces[] } for the host review step.
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

function selTemplate(root){
  var t = root.querySelector('.tcard2.sel');
  if (!t) return null;
  var brand = t.querySelector('.tbrand');
  return { key: t.dataset.t || '', name: brand ? brand.textContent.trim() : (t.dataset.t || '') };
}

function featsOn(root){
  var on = [];
  Array.prototype.forEach.call(root.querySelectorAll('.frow .tog.on'), function(tog){
    var row = tog.closest('.frow');
    var b = row ? row.querySelector('b') : null;
    on.push(b ? b.textContent.trim() : tog.textContent.trim());
  });
  return on;
}

function piecesOf(){
  var cartDef = NF.get('cart');
  if (cartDef && typeof cartDef.items === 'function') return cartDef.items();
  return [];
}

NF.register('contract-draft', {
  version: '1.0.0',
  // Structured state for the host review step (her openSummary()) — live reads.
  collect: function(root){
    root = root || document;
    var visionEl = root.querySelector('#visionText');
    return {
      vision: visionEl ? visionEl.value.trim() : '',
      template: selTemplate(root),
      functions: featsOn(root),
      pieces: piecesOf().map(function(i){
        return { model: i.model, name: i.name, size: i.size, qty: i.qty, note: i.note || '' };
      })
    };
  },
  activate: function(root, config){
    config = config || {};
    if (root.dataset.nfBound_contractDraft) return { destroy: function(){} };
    root.dataset.nfBound_contractDraft = '1';

    var buildBtn = root.querySelector('#buildBtn');
    var contract = root.querySelector('#contract');
    var wrap = root.querySelector('#contractWrap');
    // Fail soft: without the draft surface there is nothing to wire (L-2026-10-17-004).
    if (!buildBtn || !contract || !wrap) return { destroy: function(){} };

    var prev = buildBtn.onclick;

    // Contract text shape harvested from ultimate-intake.html's buildBtn block,
    // retargeted to her hooks: #doForYou/#behaviorText do not exist on her page
    // (verified by grep), so those lines are dropped; features come from her
    // .frow .tog.on toggles and the template from .tcard2.sel.
    buildBtn.onclick = function(){
      var st = NF.get('contract-draft').collect(root);
      var lines = st.pieces.map(function(i){
        return '  - ' + i.model + ' \u00b7 ' + i.name + ' \u00b7 size ' + i.size +
               ' \u00d7' + i.qty + (i.note ? ' \u00b7 note: ' + i.note : '');
      });
      var c = 'DESIGN BUILD CONTRACT \u2014 SMART FACTORY\n' +
        'vision: ' + (st.vision || '[no vision typed yet]') + '\n' +
        'template: ' + (st.template ? (st.template.name || st.template.key) : '[no template chosen]') + '\n' +
        'functions on (' + st.functions.length + '): ' + (st.functions.join(', ') || 'none') + '\n' +
        'pieces (' + st.pieces.length + ' kinds):\n' +
        (lines.join('\n') || '  (none selected)') + '\n' +
        'rules: the 16 Naya design laws \u2014 white text always, white at rest / own color on touch, ' +
        'one board one color, rectangles, elevation everywhere, mobile-first. ' +
        'AUTO-sized pieces are sized by Naya for the app.';
      contract.textContent = c;
      wrap.style.display = 'block';
      if (wrap.scrollIntoView) wrap.scrollIntoView({behavior: 'smooth'});
    };
    buildBtn.setAttribute('data-nf-unit', 'contract-draft');

    return { destroy: function(){
      buildBtn.onclick = prev;
      delete root.dataset.nfBound_contractDraft;
    } };
  }
});
})();
