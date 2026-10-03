/* SMART LIST — Room: smart notes saved into lists, groupings, categories.
 *
 * Visual law (director, 2026-10-02): boards flow the natural spectrum —
 *   purple → indigo → cyan → forest → lime → yellow → gold → orange → red → magenta
 * white/silver at rest; the flow color ignites the whole perimeter on hover/focus.
 * Boards share the Your Intelligence Today anatomy: rank + title + when +
 * in-a-nutshell + explicit SAVE TO LIST / VIEW FULL NOTE actions.
 *
 * Contract: window.NayaRooms.smartList(el, ctx)
 *   ctx.notes — note view-models from ListAdapter.parseNotes
 *
 * Store contracts (localStorage):
 *   'naya.smartlist' = { custom: {listName: [noteId,...]} }   (this room owns)
 *   'nayanet.today.smartlist.v1' = [noteId,...]               (the Today room
 *     owns writes — key verified in the Today v8.3 preview; this room reads it
 *     for the "Saved from Today" view and never writes it)
 *
 * Law: every button has a real consequence. No demo content — the 24 real
 * notes are the data. Keyboard: cards are focusable, Enter/Space opens,
 * Escape closes modals.
 */
(function(){
  'use strict';

  var STORE_KEY = 'naya.smartlist';
  var TODAY_KEY = 'nayanet.today.smartlist.v1';

  /* The natural spectrum — the same flow as Living Intel. */
  var FLOW = ['#a855f7','#6366f1','#22d3ee','#16a34a','#a3e635',
              '#facc15','#d4a017','#fb923c','#ef4444','#ec4899'];

  function loadStore(){
    try{
      var s = JSON.parse(localStorage.getItem(STORE_KEY));
      if(s && typeof s === 'object'){
        if(!s.custom || typeof s.custom !== 'object') s.custom = {};
        return s;
      }
    }catch(err){}
    return { custom:{} };
  }
  function saveStore(s){
    try{ localStorage.setItem(STORE_KEY, JSON.stringify(s)); }catch(err){}
  }
  /* Today SAVE writes a flat array of note ids under its own key. Read-only here. */
  function loadTodaySaves(){
    try{
      var a = JSON.parse(localStorage.getItem(TODAY_KEY));
      if(Array.isArray(a)) return a.filter(function(x){ return typeof x === 'string'; });
    }catch(err){}
    return [];
  }

  function esc(s){ return String(s == null ? '' : s); }

  function SmartList(el, ctx){
    ctx = ctx || {};
    var notes = Array.isArray(ctx.notes) ? ctx.notes : [];
    var byId = {};
    notes.forEach(function(n){ byId[n.id] = n; });

    var store = loadStore();
    var state = { view:{type:'all'}, query:'' };

    var stage = el('div','sl-stage');

    /* ---------- header ---------- */
    var head = el('header','sl-head');
    head.appendChild(el('p','sl-kicker','SMART LIST'));
    var h1 = el('h1','sl-title',''); h1.textContent = 'Your intelligence, filed';
    head.appendChild(h1);
    var sub = el('p','sl-sub','');
    sub.textContent = 'Every smart note, grouped by what it teaches. Save notes into your own lists — they persist on this device.';
    head.appendChild(sub);
    stage.appendChild(head);

    var tabs = el('div','sl-tabs');
    stage.appendChild(tabs);

    var main = el('main','sl-main');
    stage.appendChild(main);

    /* ---------- main: search + grid ---------- */
    var toolbar = el('div','sl-toolbar');
    var search = el('input','sl-search');
    search.type = 'search';
    search.placeholder = 'Search notes\u2026';
    search.setAttribute('aria-label','Search smart notes');
    search.addEventListener('input', function(){ state.query = search.value; renderGrid(); });
    toolbar.appendChild(search);
    var count = el('span','sl-count','');
    toolbar.appendChild(count);
    main.appendChild(toolbar);
    var grid = el('div','sl-grid');
    main.appendChild(grid);

    /* ---------- tabs across the top (no sidebar) ---------- */
    function renderTabs(){
      tabs.innerHTML = '';

      /* views row */
      var vrow = el('div','sl-tabrow');
      vrow.appendChild(tabBtn('all', 'ALL NOTES', notes.length, state.view.type==='all'));
      vrow.appendChild(tabBtn('today', 'SAVED FROM TODAY', loadTodaySaves().length, state.view.type==='today'));
      tabs.appendChild(vrow);

      /* categories row */
      var crow = el('div','sl-tabrow');
      crow.appendChild(el('span','sl-tablabel','CATEGORIES'));
      var cscroll = el('div','sl-tabscroll');
      categories().forEach(function(c){
        cscroll.appendChild(tabBtn({type:'cat', name:c.name}, prettyCat(c.name), c.n,
          isView({type:'cat', name:c.name})));
      });
      crow.appendChild(cscroll);
      tabs.appendChild(crow);

      /* my lists row */
      var lrow = el('div','sl-tabrow');
      lrow.appendChild(el('span','sl-tablabel','MY LISTS'));
      var lscroll = el('div','sl-tabscroll');
      var names = Object.keys(store.custom).sort();
      if(!names.length){
        var none = el('span','sl-tabnone',''); none.textContent = 'No custom lists yet';
        lscroll.appendChild(none);
      }
      names.forEach(function(nm){
        var wrap = el('span','sl-ltab');
        var b = el('button','sl-tab'+(isView({type:'list', name:nm})?' on':''));
        b.type = 'button';
        var t = el('span','',''); t.textContent = nm; b.appendChild(t);
        b.appendChild(el('span','sl-tab-n', String(store.custom[nm].length)));
        b.addEventListener('click', function(){
          state.view = {type:'list', name:nm}; state.query=''; search.value=''; renderAll();
        });
        wrap.appendChild(b);
        var del = el('button','sl-tabx','\u00D7');
        del.type = 'button';
        del.setAttribute('aria-label','Delete list '+nm);
        del.setAttribute('title','Delete list');
        del.addEventListener('click', function(ev){
          ev.stopPropagation();
          delete store.custom[nm];
          saveStore(store);
          if(state.view.type==='list' && state.view.name===nm) state.view = {type:'all'};
          renderAll();
        });
        wrap.appendChild(del);
        lscroll.appendChild(wrap);
      });
      var nb = el('button','sl-new','+ NEW LIST');
      nb.type = 'button';
      nb.addEventListener('click', openNewListModal);
      lscroll.appendChild(nb);
      lrow.appendChild(lscroll);
      tabs.appendChild(lrow);
    }

    function tabBtn(view, label, n, on){
      var b = el('button','sl-tab'+(on?' on':''));
      b.type = 'button';
      var key = (typeof view === 'string') ? view : view.type+':'+view.name;
      var t = el('span','',''); t.textContent = label; b.appendChild(t);
      b.appendChild(el('span','sl-tab-n', String(n)));
      b.addEventListener('click', function(){
        state.view = (typeof view === 'string') ? {type:view} : view;
        state.query=''; search.value='';
        renderAll();
      });
      b.setAttribute('data-view', key);
      return b;
    }

    function isView(v){
      if(state.view.type !== v.type) return false;
      if(v.name) return state.view.name === v.name;
      return true;
    }

    function categories(){
      var map = {};
      notes.forEach(function(n){ map[n.category] = (map[n.category]||0)+1; });
      return Object.keys(map).sort().map(function(k){ return {name:k, n:map[k]}; });
    }
    function prettyCat(c){
      return String(c||'').split('/').pop().replace(/-/g,' ').replace(/\b\w/g,function(m){return m.toUpperCase();});
    }

    /* ---------- grid ---------- */
    function currentNotes(){
      var list;
      var v = state.view;
      if(v.type === 'all') list = notes.slice();
      else if(v.type === 'today') list = resolveToday();
      else if(v.type === 'cat') list = notes.filter(function(n){ return n.category === v.name; });
      else if(v.type === 'list'){
        var ids = store.custom[v.name] || [];
        list = ids.map(function(id){ return byId[id]; }).filter(Boolean);
      } else list = [];
      var q = state.query.trim().toLowerCase();
      if(q){
        list = list.filter(function(n){
          return (n.title+' '+n.nutshell+' '+n.category).toLowerCase().indexOf(q) >= 0;
        });
      }
      return list;
    }

    /* Today-saved ids resolve against known notes; anything else renders as an
       honest placeholder that points back at the Today page — never invented. */
    function resolveToday(){
      return loadTodaySaves().map(function(id){
        if(byId[id]) return byId[id];
        return { id:'today:'+id, unresolved:true, title:'Saved from Today',
                 nutshell:'', truth:'', date:'', category:'SAVED FROM TODAY', path:'' };
      });
    }

    function renderGrid(){
      grid.innerHTML = '';
      var list = currentNotes();
      count.textContent = list.length + (list.length===1 ? ' note' : ' notes');
      if(!list.length){
        var empty = el('div','sl-empty','');
        empty.textContent = state.view.type==='today'
          ? 'Nothing saved from Today yet. Use SAVE on the Today page and it lands here.'
          : (state.query ? 'No notes match your search.' : 'No notes here yet.');
        grid.appendChild(empty);
        return;
      }
      list.forEach(function(n, i){
        grid.appendChild(n.unresolved ? unresolvedCard(n, i) : noteCard(n, i));
      });
    }

    function truthClass(t){
      t = String(t||'').toUpperCase();
      if(t === 'RATIFIED') return 'ratified';
      if(t === 'CANDIDATE') return 'candidate';
      return 'other';
    }

    /* The board: Today anatomy (rank + title + when + in-a-nutshell + explicit
       actions) flowing the spectrum — --ic is this board's flow color. */
    function noteCard(n, idx){
      var fc = FLOW[idx % FLOW.length];
      var card = el('article','sl-board');
      card.style.setProperty('--ic', fc);
      card.setAttribute('tabindex','0');
      card.setAttribute('role','button');
      card.setAttribute('aria-label','Open note: '+n.title);

      var inner = el('div','sl-board-inner');

      var top = el('div','sl-board-top');
      var ident = el('div','sl-board-id');
      var glyph = el('div','sl-board-glyph','');
      glyph.textContent = String(idx+1).padStart(2,'0');
      glyph.setAttribute('aria-hidden','true');
      var tw = el('div','');
      var t = el('h3','sl-board-t',''); t.textContent = n.title;
      var meta = el('div','sl-board-meta');
      if(n.date){ var dm = el('span','',''); dm.textContent = n.date; meta.appendChild(dm); }
      var cm = el('span','',''); cm.textContent = prettyCat(n.category); meta.appendChild(cm);
      tw.appendChild(t); tw.appendChild(meta);
      ident.appendChild(glyph); ident.appendChild(tw);
      top.appendChild(ident);
      if(n.truth){
        var pill = el('span','sl-truth '+truthClass(n.truth),''); pill.textContent = n.truth;
        top.appendChild(pill);
      }
      inner.appendChild(top);

      if(n.nutshell){
        var nut = el('div','sl-board-nut');
        var b = el('b','',''); b.textContent = 'IN A NUTSHELL'; nut.appendChild(b);
        var p = el('p','',''); p.textContent = n.nutshell; nut.appendChild(p);
        inner.appendChild(nut);
      }

      var actions = el('div','sl-board-actions');
      var sv = el('button','sl-act','SAVE TO LIST');
      sv.type = 'button';
      sv.addEventListener('click', function(ev){ ev.stopPropagation(); openPickerModal(n); });
      var vw = el('button','sl-act','VIEW FULL NOTE');
      vw.type = 'button';
      vw.addEventListener('click', function(ev){ ev.stopPropagation(); openNoteModal(n, fc); });
      actions.appendChild(sv); actions.appendChild(vw);
      inner.appendChild(actions);

      var foot = el('div','sl-board-foot');
      var fl = el('span','',''); fl.textContent = 'SMART LIST'; foot.appendChild(fl);
      var fr = el('span','',''); fr.textContent = 'NOTE '+String(idx+1).padStart(2,'0'); foot.appendChild(fr);
      inner.appendChild(foot);

      card.appendChild(inner);
      card.addEventListener('click', function(){ openNoteModal(n, fc); });
      card.addEventListener('keydown', function(ev){
        if((ev.key==='Enter'||ev.key===' ') && ev.target===card){ ev.preventDefault(); openNoteModal(n, fc); }
      });
      return card;
    }

    /* A Today save that isn't one of the 24 known notes: honest, minimal,
       points back at the Today page. Never invents a title or nutshell. */
    function unresolvedCard(n, idx){
      var fc = FLOW[idx % FLOW.length];
      var card = el('article','sl-board sl-unresolved');
      card.style.setProperty('--ic', fc);

      var inner = el('div','sl-board-inner');
      var top = el('div','sl-board-top');
      var ident = el('div','sl-board-id');
      var glyph = el('div','sl-board-glyph','');
      glyph.textContent = String(idx+1).padStart(2,'0');
      glyph.setAttribute('aria-hidden','true');
      var tw = el('div','');
      var t = el('h3','sl-board-t',''); t.textContent = 'Saved from Today';
      var meta = el('div','sl-board-meta');
      var m = el('span','',''); m.textContent = 'YOUR INTELLIGENCE TODAY'; meta.appendChild(m);
      tw.appendChild(t); tw.appendChild(meta);
      ident.appendChild(glyph); ident.appendChild(tw);
      top.appendChild(ident);
      inner.appendChild(top);

      var nut = el('div','sl-board-nut');
      var b = el('b','',''); b.textContent = 'SAVED ITEM'; nut.appendChild(b);
      var p = el('p','','');
      p.textContent = 'This save lives on the Today page — open Your Intelligence Today to view the full block.';
      nut.appendChild(p);
      inner.appendChild(nut);

      var foot = el('div','sl-board-foot');
      var fl = el('span','',''); fl.textContent = 'SMART LIST'; foot.appendChild(fl);
      var fr = el('span','',''); fr.textContent = 'NOTE '+String(idx+1).padStart(2,'0'); foot.appendChild(fr);
      inner.appendChild(foot);

      card.appendChild(inner);
      return card;
    }

    /* ---------- modals ---------- */
    var overlay = el('div','sl-overlay'); overlay.style.display = 'none';
    var mbox = el('div','sl-modal');
    overlay.appendChild(mbox);
    overlay.addEventListener('click', function(ev){ if(ev.target === overlay) closeModal(); });
    document.addEventListener('keydown', function(ev){
      if(ev.key === 'Escape' && overlay.style.display !== 'none') closeModal();
    });
    /* Focus trap: Tab cycles inside the open modal, never escapes to the page. */
    function focusables(){
      var out = [];
      (function walk(n){
        if(n.tag==='button' || n.tag==='input') out.push(n);
        (n.children||[]).forEach(walk);
      })(mbox);
      return out;
    }
    overlay.addEventListener('keydown', function(ev){
      if(ev.key !== 'Tab' || overlay.style.display === 'none') return;
      var f = focusables();
      if(!f.length) return;
      var first = f[0], last = f[f.length-1];
      var active = document.activeElement;
      if(ev.shiftKey && active === first){ ev.preventDefault(); last.focus(); }
      else if(!ev.shiftKey && active === last){ ev.preventDefault(); first.focus(); }
    });
    stage.appendChild(overlay);

    function openModal(){
      overlay.style.display = 'flex';
      var f = focusables();
      if(f.length) f[0].focus();
    }
    function closeModal(){ overlay.style.display = 'none'; mbox.innerHTML=''; }

    function modalHead(kicker, title){
      mbox.innerHTML = '';
      mbox.appendChild(el('p','sl-kicker', kicker));
      var h = el('h2','sl-modal-t',''); h.textContent = title; mbox.appendChild(h);
    }
    function modalCloseBtn(){
      var x = el('button','sl-btn','CLOSE'); x.type='button';
      x.addEventListener('click', closeModal);
      return x;
    }

    function openNoteModal(n, fc){
      mbox.style.setProperty('--ic', fc || '#a855f7');
      modalHead('SMART NOTE', n.title);
      var meta = el('div','sl-meta');
      if(n.truth){ var pill = el('span','sl-truth '+truthClass(n.truth),''); pill.textContent=n.truth; meta.appendChild(pill); }
      if(n.date){ var dt = el('span','sl-date',''); dt.textContent=n.date; meta.appendChild(dt); }
      var cat = el('span','sl-cat',''); cat.textContent = prettyCat(n.category); meta.appendChild(cat);
      mbox.appendChild(meta);
      if(n.nutshell){ var p = el('p','sl-nutshell',''); p.textContent = n.nutshell; mbox.appendChild(p); }
      if(n.path){ var ph = el('code','sl-path',''); ph.textContent = n.path; mbox.appendChild(ph); }
      var row = el('div','sl-mrow');
      var sv = el('button','sl-btn','SAVE TO LIST'); sv.type='button';
      sv.addEventListener('click', function(){ openPickerModal(n); });
      row.appendChild(sv);
      row.appendChild(modalCloseBtn());
      mbox.appendChild(row);
      openModal();
    }

    function openPickerModal(n){
      mbox.style.setProperty('--ic', '#a855f7');
      modalHead('SAVE TO LIST', n.title);
      var names = Object.keys(store.custom).sort();
      if(!names.length){
        var p = el('p','sl-none',''); p.textContent = 'No custom lists yet — create one below.';
        mbox.appendChild(p);
      }
      var wrap = el('div','sl-pick');
      names.forEach(function(nm){
        var ids = store.custom[nm];
        var has = ids.indexOf(n.id) >= 0;
        var b = el('button','sl-pickbtn'+(has?' on':''), (has?'\u2713 ':'')+nm);
        b.type = 'button';
        b.setAttribute('aria-pressed', has ? 'true' : 'false');
        b.addEventListener('click', function(){
          var arr = store.custom[nm];
          var i = arr.indexOf(n.id);
          if(i >= 0) arr.splice(i,1); else arr.push(n.id);
          saveStore(store);
          openPickerModal(n); /* re-render picker state */
          renderAll();
        });
        wrap.appendChild(b);
      });
      mbox.appendChild(wrap);
      var row = el('div','sl-mrow');
      var inp = el('input','sl-input'); inp.type='text'; inp.placeholder='New list name\u2026';
      inp.setAttribute('aria-label','New list name');
      row.appendChild(inp);
      var add = el('button','sl-btn','CREATE + SAVE'); add.type='button';
      add.addEventListener('click', function(){
        var nm = inp.value.trim();
        if(!nm) return;
        if(!store.custom[nm]) store.custom[nm] = [];
        if(store.custom[nm].indexOf(n.id) < 0) store.custom[nm].push(n.id);
        saveStore(store);
        openPickerModal(n);
        renderAll();
      });
      row.appendChild(add);
      row.appendChild(modalCloseBtn());
      mbox.appendChild(row);
      openModal();
      inp.focus();
    }

    function openNewListModal(){
      mbox.style.setProperty('--ic', '#a855f7');
      modalHead('NEW LIST', 'Name your list');
      var row = el('div','sl-mrow');
      var inp = el('input','sl-input'); inp.type='text'; inp.placeholder='e.g. Launch research\u2026';
      inp.setAttribute('aria-label','New list name');
      row.appendChild(inp);
      var add = el('button','sl-btn','CREATE LIST'); add.type='button';
      var create = function(){
        var nm = inp.value.trim();
        if(!nm) return;
        if(!store.custom[nm]){ store.custom[nm] = []; saveStore(store); }
        state.view = {type:'list', name:nm};
        closeModal(); renderAll();
      };
      add.addEventListener('click', create);
      inp.addEventListener('keydown', function(ev){ if(ev.key==='Enter'){ ev.preventDefault(); create(); } });
      row.appendChild(add);
      row.appendChild(modalCloseBtn());
      mbox.appendChild(row);
      openModal();
      inp.focus();
    }

    function renderAll(){ renderTabs(); renderGrid(); }
    renderAll();

    var foot = el('footer','sl-foot','');
    foot.textContent = 'stored on this device \u00B7 the Brain stays the source of truth';
    stage.appendChild(foot);
    return stage;
  }

  window.NayaRooms = window.NayaRooms || {};
  window.NayaRooms.smartList = SmartList;
})();
