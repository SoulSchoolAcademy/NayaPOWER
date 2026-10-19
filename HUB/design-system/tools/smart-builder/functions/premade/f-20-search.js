/* NayaFunction: f-20-search v1.0.0
   What: live search filtering a list inside root, with result count and empty state.
   Activation: <div data-fn="f-20-search" data-fn-config='{"items":[{"id":"a","title":"Hub","sub":"home"}],"placeholder":"Search pieces..."}'></div>
   Config:
     items: [{ id*, title*, sub }] — the searchable list (rendered by the unit).
     placeholder: input placeholder text (default "Search...").
     accent: hex — focus/chrome color (default #a06bff purple).
   Ready behavior: typing filters live (title + sub, case-insensitive); shows "N of M results";
     empty query shows all; no match shows an empty state. Fully client-side.
   Connected behavior: none.
   Backend twin: none.
   Lessons: L-2026-10-16-005 (every visible control works — the input really filters).
*/
(function(){
'use strict';
var NF = window.NayaFunctions = window.NayaFunctions || {};
NF._r = NF._r || {};
NF.register = NF.register || function(id, def){ if (NF._r[id]) return; NF._r[id] = def; };

NF.register('search', {
  version: '1.0.0',
  activate: function(root, config){
    config = config || {};
    var items = Array.isArray(config.items) ? config.items : [];
    var accent = config.accent || '#a06bff';

    root.innerHTML = '';
    var box = document.createElement('div');

    var input = document.createElement('input');
    input.type = 'search';
    input.setAttribute('aria-label', 'Search');
    input.placeholder = config.placeholder || 'Search...';
    input.className = 'nf20-input';
    input.style.cssText = 'width:100%;box-sizing:border-box;padding:13px 16px;font-size:15px;color:#ffffff;' +
      'background:#0b0b10;border:1.5px solid rgba(255,255,255,.55);border-radius:12px;outline:none;';
    input.addEventListener('focus', function(){ input.style.borderColor = accent; input.style.boxShadow = '0 0 16px -6px ' + accent; });
    input.addEventListener('blur', function(){ input.style.borderColor = 'rgba(255,255,255,.55)'; input.style.boxShadow = 'none'; });
    box.appendChild(input);

    var meta = document.createElement('p');
    meta.style.cssText = 'color:#F8F7FB;font-size:13px;margin:10px 2px 0;';
    box.appendChild(meta);

    var list = document.createElement('div');
    list.style.cssText = 'display:flex;flex-direction:column;gap:8px;margin-top:10px;';
    box.appendChild(list);

    function norm(s){ return String(s == null ? '' : s).toLowerCase(); }

    function render(){
      var q = norm(input.value).trim();
      list.innerHTML = '';
      var shown = 0;
      items.forEach(function(it){
        if (q && norm(it.title).indexOf(q) < 0 && norm(it.sub).indexOf(q) < 0) return;
        shown++;
        var card = document.createElement('div');
        card.style.cssText = 'padding:12px 16px;background:#0b0b10;border:1px solid rgba(255,255,255,.28);border-radius:10px;';
        var t = document.createElement('div');
        t.textContent = it.title;
        t.style.cssText = 'color:#ffffff;font-size:15px;font-weight:600;';
        var s = document.createElement('div');
        s.textContent = it.sub || '';
        s.style.cssText = 'color:#F8F7FB;font-size:13px;margin-top:2px;opacity:.85;';
        card.appendChild(t); card.appendChild(s);
        list.appendChild(card);
      });
      meta.textContent = shown + ' of ' + items.length + ' results';
      if (!shown) {
        var empty = document.createElement('div');
        empty.textContent = q ? 'No matches for "' + input.value.trim() + '".' : 'Nothing here yet.';
        empty.style.cssText = 'color:#F8F7FB;font-size:14px;padding:18px;text-align:center;border:1px dashed rgba(255,255,255,.3);border-radius:10px;';
        list.appendChild(empty);
      }
    }

    input.addEventListener('input', render);
    render();
    root.appendChild(box);
    return { destroy: function(){ root.innerHTML = ''; } };
  }
});
})();
