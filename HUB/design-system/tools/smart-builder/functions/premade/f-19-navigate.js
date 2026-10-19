/* NayaFunction: f-19-navigate v1.0.0
   What: room/page navigation rendered from config; active state; every href verified (no dead links).
   Activation: <div data-fn="f-19-navigate" data-fn-config='{"rooms":[{"label":"Hub","href":"#hub"}],"active":"auto"}'></div>
   Config:
     rooms: [{ label*, href* }] — nav entries. Rooms with empty href are skipped with a console.warn.
     active: index | "auto" (default) — explicit active index, or match location.hash to href.
     accent: hex — board accent color (default #e84fff magenta). Verbatim token recommended (Law 9).
   Ready behavior: renders nav, active state, click updates state. #-hrefs verified against real DOM
     targets; missing targets are warned about and disabled (never a dead click).
   Connected behavior: none.
   Backend twin: none.
   Lessons: L-2026-10-17-002 (all hrefs verified, no dead links), L-2026-10-17-004 (fail-soft).
*/
(function(){
'use strict';
var NF = window.NayaFunctions = window.NayaFunctions || {};
NF._r = NF._r || {};
NF.register = NF.register || function(id, def){ if (NF._r[id]) return; NF._r[id] = def; };

NF.register('navigate', {
  version: '1.0.0',
  activate: function(root, config){
    config = config || {};
    var rooms = Array.isArray(config.rooms) ? config.rooms : [];
    var accent = config.accent || '#e84fff';
    var listeners = [];

    root.innerHTML = '';
    var nav = document.createElement('nav');
    nav.setAttribute('aria-label', 'Room navigation');
    nav.style.cssText = 'display:flex;flex-wrap:wrap;gap:10px;';
    var links = [];

    function resolveActive(){
      var idx = -1;
      if (typeof config.active === 'number' && config.active >= 0 && config.active < links.length) {
        idx = config.active;
      } else {
        var h = window.location.hash;
        for (var i = 0; i < links.length; i++) {
          if (links[i].getAttribute('href') === h) { idx = i; break; }
        }
        if (idx < 0 && links.length) idx = 0;
      }
      for (var j = 0; j < links.length; j++) {
        links[j].classList.toggle('nf19-active', j === idx);
      }
    }

    rooms.forEach(function(room){
      var label = String(room && room.label || '').trim();
      var href = String(room && room.href || '').trim();
      if (!label || !href) {
        console.warn('[f-19-navigate] skipped room with empty label/href:', JSON.stringify(room));
        return; // fail-soft — no dead entry rendered
      }
      var a = document.createElement('a');
      a.textContent = label;
      a.className = 'nf19-link';
      var live = true;
      if (href.charAt(0) === '#') {
        // L-2026-10-17-002: verify the in-page target really exists — no dead links
        if (!document.getElementById(href.slice(1)) && !document.querySelector(href)) {
          console.warn('[f-19-navigate] dead in-page link "' + href + '" — target not found; link disabled');
          live = false;
        }
      }
      if (live) { a.setAttribute('href', href); }
      else {
        a.setAttribute('href', '#');
        a.setAttribute('aria-disabled', 'true');
        a.dataset.nf19Disabled = '1';
        a.addEventListener('click', function(ev){
          ev.preventDefault();
          console.warn('[f-19-navigate] disabled dead link "' + label + '" — no navigation');
        });
      }
      a.style.cssText = 'color:#ffffff;text-decoration:none;font-size:15px;font-weight:600;' +
        'padding:12px 22px;border:1.5px solid rgba(255,255,255,.55);border-radius:12px;' +
        'background:#0b0b10;transition:border-color .18s,box-shadow .18s,background .18s;' +
        (a.dataset.nf19Disabled ? 'opacity:0.35;' : '');
      a.addEventListener('mouseover', function(){ a.style.borderColor = accent; a.style.boxShadow = '0 0 18px -4px ' + accent; });
      a.addEventListener('mouseout', function(){ if (!a.classList.contains('nf19-active')) { a.style.borderColor = 'rgba(255,255,255,.55)'; a.style.boxShadow = 'none'; } });
      nav.appendChild(a);
      links.push(a);
    });

    if (!links.length) {
      root.innerHTML = '';
      var note = document.createElement('p');
      note.textContent = 'Navigation: no rooms configured.';
      note.style.cssText = 'color:#F8F7FB;font-size:14px;margin:0;';
      root.appendChild(note);
      return { destroy: function(){} }; // fail-soft — nothing harmful
    }

    // active style applied by class
    var st = document.createElement('style');
    st.textContent = '.nf19-active{border-color:' + accent + '!important;box-shadow:0 0 22px -6px ' + accent + '!important;background:rgba(255,255,255,.04)!important;}';
    document.head.appendChild(st);

    root.appendChild(nav);
    var onHash = function(){ resolveActive(); };
    window.addEventListener('hashchange', onHash);
    listeners.push(function(){ window.removeEventListener('hashchange', onHash); if (st.parentNode) st.parentNode.removeChild(st); });
    resolveActive();

    return { destroy: function(){ listeners.forEach(function(fn){ fn(); }); root.innerHTML = ''; } };
  }
});
})();
