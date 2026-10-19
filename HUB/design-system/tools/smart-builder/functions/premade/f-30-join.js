/* NayaFunction: f-30-join v1.0.0
   What: join / leave a space or community — member count updates live, membership persists.
   Activation: <div data-fn="f-30-join" data-fn-config='{"spaces":[{"id":"sp1","name":"Makers","topic":"Build things","members":128}]}'></div>
   Config:
     spaces: [{ id*, name*, topic, members (base count, default 0), color (accent hex) }]
       — colors fall back to the spectrum in law order (magenta -> purple -> blue -> green -> gold).
     storeKey: localStorage key for joined ids (default "naya.spaces.mine.v1" — harvest-compatible).
   Ready behavior: each space shows name, topic, live member count and a Join button.
     Joining adds +1 to the count, shows "Joined" in the space's own color, and persists;
     leaving reverses it. Survives reload via localStorage. Fail-soft if storage is blocked.
   Connected behavior: none.
   Backend twin: spaces service (membership feed).
   Harvest: adapted from Smart_Spaces_Page_Design.html — same localStorage shape
     (array of joined space ids), same join/leave toggle, live member count, welcome note.
     Rebuilt as a NayaFunction: scoped to root, fail-soft, one color per space (Laws 5/6).
*/
(function(){
'use strict';
var NF = window.NayaFunctions = window.NayaFunctions || {};
NF._r = NF._r || {};
NF.register = NF.register || function(id, def){ if (NF._r[id]) return; NF._r[id] = def; };

var SPECTRUM = ['#e84fff', '#a06bff', '#3fb8ff', '#2fe89e', '#ffbf3d'];

NF.register('join', {
  version: '1.0.0',
  activate: function(root, config){
    config = config || {};
    var spaces = Array.isArray(config.spaces) ? config.spaces : [];
    var key = config.storeKey || 'naya.spaces.mine.v1';

    function load(){
      try { var v = JSON.parse(localStorage.getItem(key)); return Array.isArray(v) ? v : []; }
      catch (e) { return []; }
    }
    function store(ids){
      try { localStorage.setItem(key, JSON.stringify(ids)); }
      catch (e) { console.warn('[f-30-join] localStorage unavailable — membership kept in memory only'); }
    }
    var mine = load();

    root.innerHTML = '';
    var wrap = document.createElement('div');
    wrap.style.cssText = 'display:flex;flex-direction:column;gap:10px;';

    var note = document.createElement('p');
    note.style.cssText = 'color:#F8F7FB;font-size:14px;margin:0 0 4px;min-height:20px;';
    wrap.appendChild(note);

    if (!spaces.length) {
      var empty = document.createElement('p');
      empty.textContent = 'No spaces configured.';
      empty.style.cssText = 'color:#F8F7FB;font-size:14px;margin:0;';
      wrap.appendChild(empty);
      root.appendChild(wrap);
      return { destroy: function(){} }; // fail-soft
    }

    function render(){
      // clear cards but keep the note
      while (wrap.children.length > 1) wrap.removeChild(wrap.lastChild);
      spaces.forEach(function(sp, idx){
        if (!sp || !sp.id || !sp.name) return; // fail-soft on malformed entries
        var color = sp.color || SPECTRUM[idx % SPECTRUM.length];
        var joined = mine.indexOf(sp.id) >= 0;
        var count = (parseInt(sp.members, 10) || 0) + (joined ? 1 : 0);

        var card = document.createElement('div');
        card.style.cssText = 'display:flex;align-items:center;gap:14px;padding:14px 18px;' +
          'background:#0b0b10;border:1px solid ' + (joined ? color : 'rgba(255,255,255,.28)') + ';' +
          'border-left:4px solid ' + color + ';border-radius:10px;' +
          (joined ? 'box-shadow:0 0 18px -8px ' + color + ';' : '');
        var txt = document.createElement('div');
        txt.style.cssText = 'flex:1;min-width:0;';
        var nm = document.createElement('div');
        nm.textContent = sp.name; nm.style.cssText = 'color:#ffffff;font-size:16px;font-weight:700;';
        var tp = document.createElement('div');
        tp.textContent = (sp.topic || '') + ' · ' + count + (count === 1 ? ' member' : ' members');
        tp.style.cssText = 'color:#F8F7FB;font-size:13px;margin-top:2px;opacity:.85;';
        txt.appendChild(nm); txt.appendChild(tp);

        var b = document.createElement('button');
        b.type = 'button';
        b.textContent = joined ? 'Joined' : 'Join';
        b.setAttribute('data-join-id', sp.id);
        b.className = 'nf30-join';
        b.style.cssText = 'flex:none;padding:11px 22px;font-size:14px;font-weight:700;color:#ffffff;background:#0b0b10;' +
          'border:1.5px solid ' + (joined ? color : 'rgba(255,255,255,.55)') + ';border-radius:12px;cursor:pointer;' +
          'transition:border-color .18s,box-shadow .18s;';
        if (joined) b.style.boxShadow = '0 0 16px -6px ' + color;
        b.addEventListener('mouseover', function(){ b.style.borderColor = color; b.style.boxShadow = '0 0 18px -4px ' + color; });
        b.addEventListener('mouseout', function(){
          if (joined) { b.style.borderColor = color; b.style.boxShadow = '0 0 16px -6px ' + color; }
          else { b.style.borderColor = 'rgba(255,255,255,.55)'; b.style.boxShadow = 'none'; }
        });
        b.addEventListener('click', function(){
          var i = mine.indexOf(sp.id);
          if (i >= 0) { mine.splice(i, 1); note.textContent = 'You left ' + sp.name + '.'; }
          else { mine.push(sp.id); note.textContent = 'Welcome to ' + sp.name + '.'; } // harvest greeting
          store(mine);
          render();
        });

        card.appendChild(txt); card.appendChild(b);
        wrap.appendChild(card);
      });
    }

    render();
    root.appendChild(wrap);
    return { destroy: function(){ root.innerHTML = ''; } };
  }
});
})();
