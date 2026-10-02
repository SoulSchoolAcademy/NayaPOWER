/* SMART LIST — Room: smart notes saved into lists, groupings, categories.
 * Room identity: EMERALD #10b981 (stable; color is identity, never position).
 * Contract: window.NayaRooms.smartList(el, ctx)
 *   ctx.notes — note view-models from ListAdapter.parseNotes
 *
 * Store contract (localStorage):
 *   'naya.smartlist' = { custom: {listName: [noteId,...]}, today: [...] }
 * NOTE: the Today room's SAVE implementation lives on another branch
 * (naya4/room-01-main-stage-v2) and its exact key could not be verified
 * here. This key is the proposed shared contract: Today SAVE should append
 * note ids (or {title, nutshell} objects) into store.today; this room reads
 * it under "Saved from Today". Flagged in LIST-SCORECARD.md.
 *
 * Law: every button has a real consequence. No demo content — the 24 real
 * notes are the data. Keyboard: cards are focusable, Enter opens,
 * Escape closes modals.
 */
(function(){
  'use strict';

  var STORE_KEY = 'naya.smartlist';

  function loadStore(){
    try{
      var s = JSON.parse(localStorage.getItem(STORE_KEY));
      if(s && typeof s === 'object'){
        if(!s.custom || typeof s.custom !== 'object') s.custom = {};
        if(!Array.isArray(s.today)) s.today = [];
        return s;
      }
    }catch(err){}
    return { custom:{}, today:[] };
  }
  function saveStore(s){
    try{ localStorage.setItem(STORE_KEY, JSON.stringify(s)); }catch(err){}
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

    var body = el('div','sl-body');
    var side = el('aside','sl-side');
    var main = el('main','sl-main');
    body.appendChild(side); body.appendChild(main);
    stage.appendChild(body);

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

    /* ---------- sidebar ---------- */
    function renderSide(){
      side.innerHTML = '';

      var views = el('div','sl-sec');
      views.appendChild(sideBtn('all', 'ALL NOTES', notes.length, state.view.type==='all'));
      views.appendChild(sideBtn('today', 'SAVED FROM TODAY', store.today.length, state.view.type==='today'));
      side.appendChild(views);

      var cats = categories();
      var csec = el('div','sl-sec');
      csec.appendChild(el('h2','sl-sec-h','CATEGORIES'));
      cats.forEach(function(c){
        csec.appendChild(sideBtn({type:'cat', name:c.name}, prettyCat(c.name), c.n, isView({type:'cat', name:c.name})));
      });
      side.appendChild(csec);

      var lsec = el('div','sl-sec');
      lsec.appendChild(el('h2','sl-sec-h','MY LISTS'));
      var names = Object.keys(store.custom).sort();
      if(!names.length){
        var none = el('p','sl-none',''); none.textContent = 'No custom lists yet.';
        lsec.appendChild(none);
      }
      names.forEach(function(nm){
        var row = el('div','sl-listrow');
        var b = el('button','sl-sidebtn'+(isView({type:'list', name:nm})?' on':''));
        b.type = 'button';
        var t = el('span','',''); t.textContent = nm; b.appendChild(t);
        b.appendChild(el('span','sl-sidebtn-n', String(store.custom[nm].length)));
        b.addEventListener('click', function(){ state.view = {type:'list', name:nm}; state.query=''; search.value=''; renderAll(); });
        row.appendChild(b);
        var del = el('button','sl-del','\u00D7');
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
        row.appendChild(del);
        lsec.appendChild(row);
      });
      var nb = el('button','sl-new','+ NEW LIST');
      nb.type = 'button';
      nb.addEventListener('click', openNewListModal);
      lsec.appendChild(nb);
      side.appendChild(lsec);
    }

    function sideBtn(view, label, n, on){
      var b = el('button','sl-sidebtn'+(on?' on':''));
      b.type = 'button';
      var key = (typeof view === 'string') ? view : view.type+':'+view.name;
      var t = el('span','',''); t.textContent = label; b.appendChild(t);
      b.appendChild(el('span','sl-sidebtn-n', String(n)));
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
      return c.split('/').pop().replace(/-/g,' ').replace(/\b\w/g,function(m){return m.toUpperCase();});
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

    /* Today-saved entries: note ids OR {title, nutshell} objects (defensive). */
    function resolveToday(){
      return store.today.map(function(e){
        if(typeof e === 'string' && byId[e]) return byId[e];
        if(e && typeof e === 'object' && e.title){
          return { id:'today:'+e.title, title:e.title, nutshell:e.nutshell||'',
                   truth:e.truth||'', date:e.date||'', category:'SAVED FROM TODAY', path:'' };
        }
        return null;
      }).filter(Boolean);
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
      list.forEach(function(n){ grid.appendChild(noteCard(n)); });
    }

    function truthClass(t){
      t = String(t||'').toUpperCase();
      if(t === 'RATIFIED') return 'ratified';
      if(t === 'CANDIDATE') return 'candidate';
      return 'other';
    }

    function noteCard(n){
      var card = el('article','sl-card');
      card.setAttribute('tabindex','0');
      card.setAttribute('role','button');
      card.setAttribute('aria-label','Open note: '+n.title);
      var t = el('h2','sl-card-t',''); t.textContent = n.title; card.appendChild(t);
      if(n.nutshell){
        var p = el('p','sl-card-n',''); p.textContent = n.nutshell; card.appendChild(p);
      }
      var foot = el('div','sl-card-f');
      if(n.truth){
        var pill = el('span','sl-truth '+truthClass(n.truth),''); pill.textContent = n.truth;
        foot.appendChild(pill);
      }
      if(n.date){ var dt = el('span','sl-date',''); dt.textContent = n.date; foot.appendChild(dt); }
      card.appendChild(foot);
      var actions = el('div','sl-card-a');
      var sv = el('button','sl-btn','SAVE TO LIST');
      sv.type = 'button';
      sv.addEventListener('click', function(ev){ ev.stopPropagation(); openPickerModal(n); });
      actions.appendChild(sv);
      card.appendChild(actions);
      card.addEventListener('click', function(){ openNoteModal(n); });
      card.addEventListener('keydown', function(ev){
        if(ev.key === 'Enter' && ev.target === card){ ev.preventDefault(); openNoteModal(n); }
      });
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
    stage.appendChild(overlay);

    function openModal(){ overlay.style.display = 'flex'; }
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

    function openNoteModal(n){
      modalHead('SMART NOTE', n.title);
      var meta = el('div','sl-meta');
      if(n.truth){ var pill = el('span','sl-truth '+truthClass(n.truth),''); pill.textContent=n.truth; meta.appendChild(pill); }
      if(n.date){ var dt = el('span','sl-date',''); dt.textContent=n.date; meta.appendChild(dt); }
      var cat = el('span','sl-cat',''); cat.textContent = n.category; meta.appendChild(cat);
      mbox.appendChild(meta);
      if(n.nutshell){ var p = el('p','sl-nutshell',''); p.textContent = n.nutshell; mbox.appendChild(p); }
      if(n.path){ var ph = el('code','sl-path',''); ph.textContent = n.path; mbox.appendChild(ph); }
      var row = el('div','sl-mrow');
      if(String(n.id).indexOf('today:') !== 0){
        var sv = el('button','sl-btn','SAVE TO LIST'); sv.type='button';
        sv.addEventListener('click', function(){ openPickerModal(n); });
        row.appendChild(sv);
      }
      row.appendChild(modalCloseBtn());
      mbox.appendChild(row);
      openModal();
    }

    function openPickerModal(n){
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

    function renderAll(){ renderSide(); renderGrid(); }
    renderAll();

    var foot = el('footer','sl-foot','');
    foot.textContent = 'stored on this device \u00B7 the Brain stays the source of truth';
    stage.appendChild(foot);
    return stage;
  }

  window.NayaRooms = window.NayaRooms || {};
  window.NayaRooms.smartList = SmartList;
})();
