/* NayaFunction: f-23-save v1.0.0
   What: favorites — toggle save on items within root, persisted to localStorage, with a saved view.
   Activation: <div data-fn="f-23-save" data-fn-config='{"items":[{"id":"p1","title":"Crystal orb","sub":"magenta"}],"storeKey":"naya.fn23.saved.v1"}'></div>
   Config:
     items: [{ id*, title*, sub }] — the items that can be saved.
     storeKey: localStorage key holding an array of saved ids (default "naya.fn23.saved.v1").
     accent: hex — saved-state gold chrome (default #ffbf3d; gold = shown value, Law 2).
   Ready behavior: each item shows Save / Saved; toggling updates the set immediately and persists.
     "Saved only" filter shows just the saved items; empty states say so honestly. Fully client-side.
   Connected behavior: none.
   Backend twin: none.
   Lessons: L-2026-10-16-005 (the toggle really saves and survives reload).
*/
(function(){
'use strict';
var NF = window.NayaFunctions = window.NayaFunctions || {};
NF._r = NF._r || {};
NF.register = NF.register || function(id, def){ if (NF._r[id]) return; NF._r[id] = def; };

NF.register('f-23-save', {
  version: '1.0.0',
  activate: function(root, config){
    config = config || {};
    var items = Array.isArray(config.items) ? config.items : [];
    var key = config.storeKey || 'naya.fn23.saved.v1';
    var accent = config.accent || '#ffbf3d';
    var savedOnly = false;

    function load(){
      try { var v = JSON.parse(localStorage.getItem(key)); return Array.isArray(v) ? v : []; }
      catch (e) { return []; }
    }
    function store(ids){
      try { localStorage.setItem(key, JSON.stringify(ids)); }
      catch (e) { console.warn('[f-23-save] localStorage unavailable — save kept in memory only'); }
    }
    var saved = load();

    root.innerHTML = '';
    var wrap = document.createElement('div');

    var head = document.createElement('div');
    head.style.cssText = 'display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;';
    var t = document.createElement('p');
    t.textContent = 'Favorites';
    t.style.cssText = 'color:#ffffff;font-size:15px;font-weight:600;margin:0;';
    var filter = document.createElement('button');
    filter.type = 'button'; filter.textContent = 'Show: all';
    filter.className = 'nf23-filter';
    filter.style.cssText = 'padding:9px 18px;font-size:13px;font-weight:700;color:#ffffff;background:#0b0b10;' +
      'border:1.5px solid rgba(255,255,255,.55);border-radius:10px;cursor:pointer;';
    head.appendChild(t); head.appendChild(filter);
    wrap.appendChild(head);

    var list = document.createElement('div');
    list.style.cssText = 'display:flex;flex-direction:column;gap:8px;';
    wrap.appendChild(list);

    var meta = document.createElement('p');
    meta.style.cssText = 'color:#F8F7FB;font-size:13px;margin:10px 2px 0;';
    wrap.appendChild(meta);

    function render(){
      list.innerHTML = '';
      var shown = 0;
      items.forEach(function(it){
        var isSaved = saved.indexOf(it.id) >= 0;
        if (savedOnly && !isSaved) return;
        shown++;
        var card = document.createElement('div');
        card.style.cssText = 'display:flex;align-items:center;gap:12px;padding:12px 16px;background:#0b0b10;' +
          'border:1px solid ' + (isSaved ? accent : 'rgba(255,255,255,.28)') + ';border-radius:10px;';
        var dot = document.createElement('span');
        dot.style.cssText = 'width:10px;height:10px;border-radius:50%;flex:none;' +
          'background:' + (isSaved ? accent : 'transparent') +
          ';border:1.5px solid ' + (isSaved ? accent : 'rgba(255,255,255,.4)') + ';';
        var txt = document.createElement('div');
        txt.style.cssText = 'flex:1;min-width:0;';
        var tt = document.createElement('div');
        tt.textContent = it.title; tt.style.cssText = 'color:#ffffff;font-size:15px;font-weight:600;';
        var ss = document.createElement('div');
        ss.textContent = it.sub || ''; ss.style.cssText = 'color:#F8F7FB;font-size:13px;opacity:.85;';
        txt.appendChild(tt); txt.appendChild(ss);
        var b = document.createElement('button');
        b.type = 'button'; b.textContent = isSaved ? 'Saved' : 'Save';
        b.setAttribute('data-save-id', it.id);
        b.className = 'nf23-toggle';
        b.style.cssText = 'flex:none;padding:9px 18px;font-size:13px;font-weight:700;color:#ffffff;background:#0b0b10;' +
          'border:1.5px solid ' + (isSaved ? accent : 'rgba(255,255,255,.55)') + ';border-radius:10px;cursor:pointer;' +
          (isSaved ? 'box-shadow:0 0 14px -6px ' + accent + ';' : '');
        b.addEventListener('click', function(){
          var i = saved.indexOf(it.id);
          if (i >= 0) saved.splice(i, 1); else saved.push(it.id);
          store(saved);
          render();
        });
        card.appendChild(dot); card.appendChild(txt); card.appendChild(b);
        list.appendChild(card);
      });
      meta.textContent = saved.length + ' saved' + (savedOnly ? ' — showing saved only' : '');
      if (!shown) {
        var empty = document.createElement('div');
        empty.textContent = savedOnly ? 'Nothing saved yet — tap Save on anything you like.' : 'Nothing here yet.';
        empty.style.cssText = 'color:#F8F7FB;font-size:14px;padding:18px;text-align:center;border:1px dashed rgba(255,255,255,.3);border-radius:10px;';
        list.appendChild(empty);
      }
    }

    filter.addEventListener('click', function(){
      savedOnly = !savedOnly;
      filter.textContent = savedOnly ? 'Show: saved' : 'Show: all';
      render();
    });

    render();
    root.appendChild(wrap);
    return { destroy: function(){ root.innerHTML = ''; } };
  }
});
})();
