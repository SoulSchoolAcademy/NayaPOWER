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
    var s = { custom:{}, cats:{ added:[], renamed:{}, hidden:[] } };
    try{
      var raw = JSON.parse(localStorage.getItem(STORE_KEY));
      if(raw && typeof raw === 'object'){
        if(raw.custom && typeof raw.custom === 'object') s.custom = raw.custom;
        if(raw.cats && typeof raw.cats === 'object'){
          if(Array.isArray(raw.cats.added)) s.cats.added = raw.cats.added.filter(function(x){ return typeof x === 'string'; });
          if(raw.cats.renamed && typeof raw.cats.renamed === 'object') s.cats.renamed = raw.cats.renamed;
          if(Array.isArray(raw.cats.hidden)) s.cats.hidden = raw.cats.hidden.filter(function(x){ return typeof x === 'string'; });
        }
        return s;
      }
    }catch(err){}
    return s;
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

    /* ---------- header: title left, + NEW LIST top-right ---------- */
    var head = el('header','sl-head');
    var htext = el('div','sl-head-text');
    htext.appendChild(el('p','sl-kicker','SMART LIST'));
    var h1 = el('h1','sl-title',''); h1.textContent = 'Your intelligence, filed';
    htext.appendChild(h1);
    var sub = el('p','sl-sub','');
    sub.textContent = 'Every smart note, grouped by what it teaches. Save notes into your own lists — they persist on this device.';
    htext.appendChild(sub);
    head.appendChild(htext);
    var nbHead = el('button','sl-new','+ NEW LIST');
    nbHead.type = 'button';
    nbHead.addEventListener('click', function(){ openNewListModal(); });
    head.appendChild(nbHead);
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
    var clearf = el('button','sl-clearf','\u00D7 CLEAR');
    clearf.type = 'button';
    clearf.style.display = 'none';
    clearf.setAttribute('aria-label','Clear filter');
    clearf.addEventListener('click', function(){
      state.view = {type:'all'}; state.query=''; search.value=''; renderAll();
    });
    toolbar.appendChild(clearf);
    main.appendChild(toolbar);
    var grid = el('div','sl-grid');
    main.appendChild(grid);

    /* ---------- category tabs: derived from notes + user-managed ---------- */
    function setClass(elm, cls, on){
      var cs = (' ' + (elm.className||'') + ' ').replace(/\s+/g,' ');
      var has = cs.indexOf(' ' + cls + ' ') >= 0;
      if(on && !has) elm.className = ((elm.className||'') + ' ' + cls).trim();
      else if(!on && has) elm.className = cs.split(' ' + cls + ' ').join(' ').trim();
    }

    /* Visible tabs: derived categories (minus hidden, plus renames) then added customs. */
    function visibleCategories(){
      var out = [];
      categories().forEach(function(c){
        if(store.cats.hidden.indexOf(c.name) >= 0) return;
        out.push({ key:c.name, label:(store.cats.renamed[c.name] || prettyCat(c.name)), n:c.n, custom:false });
      });
      store.cats.added.forEach(function(name){
        out.push({ key:'custom:'+name, label:name, n:0, custom:true });
      });
      return out;
    }

    /* A horizontally scrolling row done properly: edge fades + chevrons when
       content overflows, instead of buttons accidentally clipped. */
    var scrollUpdaters = [];
    function scrollRow(){
      var w = el('div','sl-scrollwrap');
      var l = el('button','sl-chev sl-chev-l','\u2039'); l.type='button';
      l.setAttribute('aria-label','Scroll tabs left');
      var s = el('div','sl-tabscroll');
      var r = el('button','sl-chev sl-chev-r','\u203A'); r.type='button';
      r.setAttribute('aria-label','Scroll tabs right');
      w.appendChild(l); w.appendChild(s); w.appendChild(r);
      var step = function(){ return Math.max(280, (s.clientWidth||0)*0.7); };
      l.addEventListener('click', function(){ if(s.scrollBy) s.scrollBy({left:-step(), behavior:'smooth'}); });
      r.addEventListener('click', function(){ if(s.scrollBy) s.scrollBy({left: step(), behavior:'smooth'}); });
      var update = function(){
        var can = (s.scrollWidth||0) > (s.clientWidth||0) + 4;
        setClass(w, 'is-scroll', can);
        setClass(s, 'is-scroll', can);
        l.disabled = (s.scrollLeft||0) <= 4;
        r.disabled = (s.scrollLeft||0) + (s.clientWidth||0) >= (s.scrollWidth||0) - 4;
      };
      s.addEventListener('scroll', update);
      scrollUpdaters.push(update);
      return { wrap:w, scroll:s, update:update };
    }
    if(window.addEventListener){
      window.addEventListener('resize', function(){
        scrollUpdaters.forEach(function(u){ u(); });
      });
    }

    /* ---------- tabs: lists row (only when it earns the space) + scrolling category bar ---------- */
    function renderTabs(){
      tabs.innerHTML = '';
      scrollUpdaters = [];

      /* Row 1 — lists: Saved from Today (only when non-empty) + my lists. */
      var todaySaves = loadTodaySaves();
      var names = Object.keys(store.custom).sort();
      if(todaySaves.length || names.length){
        var lrow = el('div','sl-tabrow');
        var lr = scrollRow();
        if(todaySaves.length){
          lr.scroll.appendChild(tabBtn({type:'today'}, 'SAVED FROM TODAY', todaySaves.length,
            state.view.type==='today', null));
        }
        names.forEach(function(nm){
          var wrap = el('span','sl-ltab');
          var v = {type:'list', name:nm};
          var b = el('button','sl-tab'+(isView(v)?' on':''));
          b.type = 'button';
          b.setAttribute('data-view', 'list:'+nm);
          var t = el('span','',''); t.textContent = nm; b.appendChild(t);
          b.appendChild(el('span','sl-tab-n', String(store.custom[nm].length)));
          b.addEventListener('click', function(){
            state.view = isView(v) ? {type:'all'} : v;
            state.query=''; search.value=''; renderAll();
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
          lr.scroll.appendChild(wrap);
        });
        lrow.appendChild(lr.wrap);
        tabs.appendChild(lrow);
      }

      /* Row 2 — the scrolling category bar: one level, toggle to filter,
         each tab lighting in its own spectrum color. Nothing lit by default. */
      var krow = el('div','sl-tabrow');
      var kr = scrollRow();
      visibleCategories().forEach(function(c, i){
        kr.scroll.appendChild(tabBtn({type:'cat', name:c.key}, c.label, c.n,
          isView({type:'cat', name:c.key}), FLOW[i % FLOW.length]));
      });
      krow.appendChild(kr.wrap);
      var mg = el('button','sl-manage','\u2699 TABS');
      mg.type = 'button';
      mg.setAttribute('title','Add, rename, or hide category tabs');
      mg.setAttribute('aria-label','Manage category tabs');
      mg.addEventListener('click', openManageCats);
      krow.appendChild(mg);
      tabs.appendChild(krow);

      scrollUpdaters.forEach(function(u){ u(); });
    }

    function tabBtn(view, label, n, on, color){
      var b = el('button','sl-tab'+(on?' on':''));
      b.type = 'button';
      if(color) b.style.setProperty('--tc', color);
      var key = view.type+':'+(view.name || view.type);
      var t = el('span','',''); t.textContent = label; b.appendChild(t);
      b.appendChild(el('span','sl-tab-n', String(n)));
      b.addEventListener('click', function(){
        state.view = isView(view) ? {type:'all'} : view;
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
      clearf.style.display = (state.view.type!=='all' || state.query) ? '' : 'none';
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

    /* Manage the category tabs: rename, hide, restore, add. Persisted in the
       room store — notes themselves are never touched. */
    function openManageCats(){
      mbox.style.setProperty('--ic', '#a855f7');
      modalHead('MANAGE TABS', 'Rename, hide, or add category tabs');
      var list = el('div','sl-catlist');
      visibleCategories().forEach(function(c){
        var row = el('div','sl-catrow');
        var inp = el('input','sl-input'); inp.type='text'; inp.value = c.label;
        inp.setAttribute('aria-label','Rename tab '+c.label);
        inp.addEventListener('change', function(){
          var v = inp.value.trim();
          if(!v){ inp.value = c.label; return; }
          if(c.custom){
            var i = store.cats.added.indexOf(c.label);
            if(i >= 0) store.cats.added[i] = v;
          } else {
            store.cats.renamed[c.key] = v;
          }
          saveStore(store); state.view = {type:'all'}; renderAll(); openManageCats();
        });
        row.appendChild(inp);
        row.appendChild(el('span','sl-catn', c.n + (c.n===1 ? ' note' : ' notes')));
        var del = el('button','sl-btn sl-btndanger', c.custom ? 'DELETE' : 'HIDE');
        del.type = 'button';
        del.setAttribute('title', c.custom ? 'Delete this tab' : 'Hide this tab (its notes stay under All)');
        del.addEventListener('click', function(){
          if(c.custom){
            store.cats.added = store.cats.added.filter(function(x){ return x !== c.label; });
          } else if(store.cats.hidden.indexOf(c.key) < 0){
            store.cats.hidden.push(c.key);
          }
          saveStore(store); state.view = {type:'all'}; renderAll(); openManageCats();
        });
        row.appendChild(del);
        list.appendChild(row);
      });
      mbox.appendChild(list);

      if(store.cats.hidden.length){
        mbox.appendChild(el('p','sl-msub','HIDDEN'));
        store.cats.hidden.forEach(function(key){
          var row = el('div','sl-catrow');
          var s = el('span','',''); s.textContent = prettyCat(key); row.appendChild(s);
          var rs = el('button','sl-btn','RESTORE'); rs.type = 'button';
          rs.addEventListener('click', function(){
            store.cats.hidden = store.cats.hidden.filter(function(x){ return x !== key; });
            saveStore(store); renderAll(); openManageCats();
          });
          row.appendChild(rs);
          mbox.appendChild(row);
        });
      }

      mbox.appendChild(el('p','sl-msub','ADD NEW TAB'));
      var arow = el('div','sl-catrow');
      var ainp = el('input','sl-input'); ainp.type = 'text'; ainp.placeholder = 'New tab name\u2026';
      ainp.setAttribute('aria-label','New tab name');
      arow.appendChild(ainp);
      var addTab = function(){
        var v = ainp.value.trim();
        if(!v) return;
        var dup = store.cats.added.indexOf(v) >= 0 ||
          categories().some(function(c){ return (store.cats.renamed[c.name] || prettyCat(c.name)) === v; });
        if(!dup){ store.cats.added.push(v); saveStore(store); }
        state.view = {type:'all'}; renderAll(); openManageCats();
      };
      var add = el('button','sl-btn','ADD TAB'); add.type = 'button';
      add.addEventListener('click', addTab);
      ainp.addEventListener('keydown', function(ev){ if(ev.key==='Enter'){ ev.preventDefault(); addTab(); } });
      arow.appendChild(add);
      mbox.appendChild(arow);

      var crow = el('div','sl-mrow');
      crow.appendChild(modalCloseBtn());
      mbox.appendChild(crow);
      openModal();
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
