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

  /* Store: custom lists + the SmartTabs ribbon.
     tabs[] follows Shawn's SmartTabs v9 data shape {id,label,heart,star},
     plus key = the category binding (his `route` becomes our filter key)
     and custom = user-added tab. hiddenTabs = removed derived tabs. */
  function loadStore(){
    var s = { custom:{}, tabs:[], hiddenTabs:[] };
    try{
      var raw = JSON.parse(localStorage.getItem(STORE_KEY)) || {};
      if(raw.custom && typeof raw.custom === 'object') s.custom = raw.custom;
      if(Array.isArray(raw.tabs)) s.tabs = raw.tabs;
      if(Array.isArray(raw.hiddenTabs)) s.hiddenTabs = raw.hiddenTabs;
      if(raw.cats && !raw.tabs){
        /* migrate the v5 cats model */
        var renamed = raw.cats.renamed || {};
        (raw.cats.added || []).forEach(function(nm){
          s.tabs.push({ id:'tab-custom-'+nm, key:'custom:'+nm, label:nm, heart:false, star:false, custom:true });
        });
        s._renamed = renamed;
        s.hiddenTabs = (raw.cats.hidden || []).slice();
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

    /* ============ Shawn's SmartTabs v9, ported as the category ribbon ============
       His component: pill ribbon, click = navigate, right-click / ⋯ =
       Edit / Set Purple Heart / Set Gold Star / Remove, ＋Add pill, popover
       editor with 💜/⭐ toggles, heart-first sort, localStorage persistence.
       Ported here: click = filter the Smart List (the list's "navigation"),
       his `route` binding becomes our category `key`. Same pill language,
       same menu, same popover, same sort. */

    function setClass(elm, cls, on){
      var cs = (' ' + (elm.className||'') + ' ').replace(/\s+/g,' ');
      var has = cs.indexOf(' ' + cls + ' ') >= 0;
      if(on && !has) elm.className = ((elm.className||'') + ' ' + cls).trim();
      else if(!on && has) elm.className = cs.split(' ' + cls + ' ').join(' ').trim();
    }
    function hasClass(elm, cls){
      return ((' '+(elm.className||'')+' ').replace(/\s+/g,' ').indexOf(' '+cls+' ') >= 0);
    }

    /* Stable spectrum color per tab: color is the tab's identity, so it must
       not shift when 💜/⭐ re-sort the ribbon. */
    function tabColor(key){
      var h = 0, s = String(key);
      for(var i=0;i<s.length;i++){ h = ((h*31) + s.charCodeAt(i)) | 0; }
      return FLOW[Math.abs(h) % FLOW.length];
    }

    /* Keep the ribbon grounded in the real notes: every derived category gets
       a tab unless hidden; vanished categories drop off; customs persist. */
    function syncTabs(){
      var have = {}, changed = false;
      store.tabs.forEach(function(t){ have[t.key]=true; });
      categories().forEach(function(c){
        if(have[c.name] || store.hiddenTabs.indexOf(c.name)>=0) return;
        store.tabs.push({ id:'tab-'+String(c.name).replace(/[^a-z0-9]+/gi,'-').toLowerCase(),
          key:c.name, label:prettyCat(c.name), heart:false, star:false, custom:false });
        changed = true;
      });
      if(store._renamed){
        Object.keys(store._renamed).forEach(function(k){
          store.tabs.forEach(function(t){ if(t.key===k) t.label = store._renamed[k]; });
        });
        delete store._renamed; changed = true;
      }
      var cats = {};
      categories().forEach(function(c){ cats[c.name]=true; });
      var before = store.tabs.length;
      store.tabs = store.tabs.filter(function(t){ return t.custom || !!cats[t.key]; });
      if(store.tabs.length!==before) changed = true;
      var hb = store.hiddenTabs.length;
      store.hiddenTabs = store.hiddenTabs.filter(function(k){ return !!cats[k]; });
      if(store.hiddenTabs.length!==hb) changed = true;
      if(changed) saveStore(store);
    }

    /* His sortLit: 💜 first, then ⭐, the rest keep insertion order. */
    function sortedTabs(){
      return store.tabs.slice().sort(function(a,b){
        var pa = (a.heart?2:0)+(a.star?1:0), pb = (b.heart?2:0)+(b.star?1:0);
        return pb - pa;
      });
    }
    /* What the ribbon shows: everything except hidden tabs. Hidden tabs keep
       their objects, so rename/💜/⭐ survive a remove → restore round-trip. */
    function visibleTabs(){
      return sortedTabs().filter(function(t){ return store.hiddenTabs.indexOf(t.key)<0; });
    }

    /* A horizontally scrolling row done properly: edge fades + chevrons when
       content overflows, instead of buttons accidentally clipped — plus the
       slow ambient drift from his SmartNET ribbon (pauses on touch). */
    var scrollUpdaters = [];
    var scrollRows = [];
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

      /* Ambient drift: slow ping-pong across the ribbon, like his SmartNET
         page. Any touch, hover, focus, or menu pauses it for a while. */
      var lastPoke = 0, dir = 1, timer = null;
      var row = { wrap:w, scroll:s, update:update, timer:null };
      function reduced(){
        return !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
      }
      function poke(){ lastPoke = Date.now(); }
      function tick(){
        if(document.hidden) return;
        if(reduced()) return;
        if(Date.now() - lastPoke < 4000) return;
        var max = (s.scrollWidth||0) - (s.clientWidth||0);
        if(max <= 4) return;
        var next = (s.scrollLeft||0) + dir * 1.1;
        if(next >= max){ next = max; dir = -1; }
        else if(next <= 0){ next = 0; dir = 1; }
        s.scrollLeft = next;
      }
      function arm(){
        if(row.timer || reduced()) return;
        if((s.scrollWidth||0) <= (s.clientWidth||0) + 4) return;
        row.timer = setInterval(tick, 32);
      }
      function disarm(){ if(row.timer){ clearInterval(row.timer); row.timer = null; } }
      ['pointerenter','pointerdown','focusin'].forEach(function(t){ w.addEventListener(t, poke); });
      w.addEventListener('wheel', poke, {passive:true});
      w.addEventListener('touchstart', poke, {passive:true});
      w.addEventListener('keydown', poke);
      row.poke = poke; row.tick = tick; row.arm = arm; row.disarm = disarm;
      w._row = row;
      /* Re-measure when layout actually happens: the room renders detached,
         so first-paint widths are 0 until the stage is mounted. */
      if(window.ResizeObserver){
        try{
          var ro = new ResizeObserver(function(){ update(); arm(); });
          ro.observe(s);
          row._ro = ro;
        }catch(e){}
      }
      scrollRows.push(row);
      return { wrap:w, scroll:s, update:update, row:row };
    }
    function pokeScrollers(){ scrollRows.forEach(function(r){ r.poke(); }); }
    if(window.addEventListener){
      window.addEventListener('resize', function(){
        scrollUpdaters.forEach(function(u){ u(); });
      });
    }

    function placeNear(anchor, panel){
      if(!anchor || !anchor.getBoundingClientRect) return;
      try{
        var r = anchor.getBoundingClientRect();
        var W = panel.offsetWidth||280, H = panel.offsetHeight||180;
        var vw = window.innerWidth||1024, vh = window.innerHeight||768;
        panel.style.left = Math.min(vw-W-8, Math.max(8, r.left))+'px';
        panel.style.top = Math.min(vh-H-8, (r.bottom||r.top||0)+8)+'px';
      }catch(e){}
    }

    /* ---------- the ribbon ---------- */
    function renderTabs(){
      tabs.innerHTML = '';
      scrollUpdaters = [];
      scrollRows.forEach(function(r){ r.disarm(); if(r._ro){ try{ r._ro.disconnect(); }catch(e){} } });
      scrollRows = [];
      syncTabs();

      /* Row 1 — lists row (only when it earns the space), same pill language. */
      var todaySaves = loadTodaySaves();
      var names = Object.keys(store.custom).sort();
      if(todaySaves.length || names.length){
        var lrow = el('div','sl-tabrow');
        var lr = scrollRow();
        if(todaySaves.length){
          lr.scroll.appendChild(listPill('SAVED FROM TODAY', todaySaves.length, {type:'today'}, null));
        }
        names.forEach(function(nm){
          var v = {type:'list', name:nm};
          lr.scroll.appendChild(listPill(nm, store.custom[nm].length, v, function(){
            delete store.custom[nm];
            saveStore(store);
            if(state.view.type==='list' && state.view.name===nm) state.view = {type:'all'};
            renderAll();
          }));
        });
        lrow.appendChild(lr.wrap);
        tabs.appendChild(lrow);
      }

      /* Row 2 — the SmartTabs ribbon. Click a pill = filter (toggle). */
      var krow = el('div','sl-tabrow');
      var kr = scrollRow();
      visibleTabs().forEach(function(t){
        kr.scroll.appendChild(snPill(t));
      });
      var addPill = el('div','sn-pill add');
      addPill.setAttribute('tabindex','0');
      addPill.setAttribute('role','button');
      addPill.setAttribute('aria-label','Add a tab');
      var alab = el('span','sn-label',''); alab.textContent = '\uFF0B Add'; addPill.appendChild(alab);
      var addGo = function(){ openTabEditor(null, true, addPill); };
      addPill.addEventListener('click', addGo);
      wirePillKeys(addPill, addGo);
      kr.scroll.appendChild(addPill);
      krow.appendChild(kr.wrap);
      tabs.appendChild(krow);

      refreshRows();
      /* Fallback for no-ResizeObserver: re-measure after mount + first paint. */
      if(!window.ResizeObserver){
        if(window.requestAnimationFrame){
          window.requestAnimationFrame(function(){ window.requestAnimationFrame(refreshRows); });
        } else {
          setTimeout(refreshRows, 60);
        }
      }
    }
    function refreshRows(){
      scrollUpdaters.forEach(function(u){ u(); });
      scrollRows.forEach(function(r){ r.arm(); });
    }

    /* Roving keyboard travel across a pill ribbon: ←/→ move, Home/End jump. */
    function wirePillKeys(p, go){
      p.addEventListener('keydown', function(ev){
        if(ev.key==='Enter'||ev.key===' '){ ev.preventDefault(); go(); return; }
        if(ev.key!=='ArrowRight'&&ev.key!=='ArrowLeft'&&ev.key!=='Home'&&ev.key!=='End') return;
        ev.preventDefault();
        var kids = (p.parentNode && p.parentNode.children) || [];
        var ps = [];
        for(var i=0;i<kids.length;i++){ if(hasClass(kids[i],'sn-pill')) ps.push(kids[i]); }
        var ix = ps.indexOf(p), n = ix;
        if(ev.key==='ArrowRight') n = Math.min(ps.length-1, ix+1);
        else if(ev.key==='ArrowLeft') n = Math.max(0, ix-1);
        else if(ev.key==='Home') n = 0;
        else n = ps.length-1;
        if(ps[n] && ps[n].focus) ps[n].focus();
      });
    }

    /* One SmartTab pill: label + 💜/⭐ marker + ⋯ menu. */
    function snPill(t){
      var p = el('div','sn-pill'+(t.heart?' heart':'')+(t.star?' star':'')+
        (isView({type:'cat',name:t.key})?' on':''));
      p.style.setProperty('--tc', tabColor(t.key));
      p.setAttribute('data-id', t.id);
      p.setAttribute('tabindex','0');
      p.setAttribute('role','button');
      p.setAttribute('aria-label','Filter by '+t.label);
      var lab = el('span','sn-label',''); lab.textContent = t.label; p.appendChild(lab);
      if(t.heart || t.star){
        var mk = el('span','sn-mark',''); mk.textContent = t.heart ? '\uD83D\uDC9C' : '\u2B50'; p.appendChild(mk);
      }
      var more = el('button','sn-more','\u22EF');
      more.type='button';
      more.setAttribute('aria-label','Tab options for '+t.label);
      more.addEventListener('click', function(ev){ ev.stopPropagation(); openTabMenu(t, p); });
      p.appendChild(more);
      var go = function(){
        var v = {type:'cat', name:t.key};
        state.view = isView(v) ? {type:'all'} : v;
        state.query=''; search.value=''; renderAll();
      };
      p.addEventListener('click', go);
      wirePillKeys(p, go);
      p.addEventListener('contextmenu', function(ev){ ev.preventDefault(); openTabMenu(t, p); });
      return p;
    }

    /* A saved-collection pill in the same language (× instead of ⋯). */
    function listPill(label, count, view, onDelete){
      var p = el('div','sn-pill'+(isView(view)?' on':''));
      p.style.setProperty('--tc', '#ffffff');
      p.setAttribute('data-view', view.type+':'+(view.name||view.type));
      p.setAttribute('tabindex','0');
      p.setAttribute('role','button');
      p.setAttribute('aria-label', label);
      var lab = el('span','sn-label',''); lab.textContent = label; p.appendChild(lab);
      p.appendChild(el('span','sn-count', String(count)));
      if(onDelete){
        var x = el('button','sn-more sn-x','\u00D7'); x.type='button';
        x.setAttribute('aria-label','Delete '+label);
        x.addEventListener('click', function(ev){ ev.stopPropagation(); onDelete(); });
        p.appendChild(x);
      }
      var go = function(){
        state.view = isView(view) ? {type:'all'} : view;
        state.query=''; search.value=''; renderAll();
      };
      p.addEventListener('click', go);
      wirePillKeys(p, go);
      return p;
    }

    /* ---------- the ⋯ menu: his Edit / 💜 / ⭐ / Remove ---------- */
    var tabMenu = el('div','sn-menu'); tabMenu.style.display='none'; stage.appendChild(tabMenu);
    var menuTab = null;
    function openTabMenu(t, anchor){
      menuTab = t;
      pokeScrollers();
      tabMenu.innerHTML = '';
      var items = [['edit','\u270F\uFE0F Edit'],['heart','\uD83D\uDC9C Set Purple Heart'],
                   ['star','\u2B50 Set Gold Star'],['remove','\u2715 Remove']];
      items.forEach(function(it){
        var mi = el('div','mi',''); mi.textContent = it[1]; mi.setAttribute('data-act', it[0]);
        (function(act){ mi.addEventListener('click', function(){ tabMenuAction(act); }); })(it[0]);
        tabMenu.appendChild(mi);
      });
      tabMenu.style.display='block';
      placeNear(anchor, tabMenu);
    }
    function tabMenuAction(act){
      tabMenu.style.display='none';
      var t = menuTab; if(!t) return;
      if(act==='edit'){ openTabEditor(t, false, null); }
      else if(act==='heart' || act==='star'){
        store.tabs.forEach(function(x){
          if(x.id===t.id){ x.heart = (act==='heart'); x.star = (act==='star'); }
        });
        saveStore(store); renderAll();
      }
      else if(act==='remove'){
        if(t.custom){
          store.tabs = store.tabs.filter(function(x){ return x.id!==t.id; });
        } else if(store.hiddenTabs.indexOf(t.key)<0){
          /* derived: hide the tab, keep its object — rename/💜/⭐ survive restore */
          store.hiddenTabs.push(t.key);
        }
        saveStore(store);
        if(state.view.type==='cat' && state.view.name===t.key) state.view = {type:'all'};
        renderAll();
      }
    }

    /* ---------- the popover editor: his Label + 💜/⭐ toggles ---------- */
    var tabPop = el('div','sn-pop'); tabPop.style.display='none'; stage.appendChild(tabPop);
    function openTabEditor(t, isCreate, anchor){
      tabPop.innerHTML = '';
      pokeScrollers();
      tabPop.appendChild(el('h3','sn-pop-title', isCreate ? 'Add Tab' : 'Edit Tab'));
      var r1 = el('div','row');
      var l1 = el('label','','Label');
      var inLabel = el('input','sn-in-label'); inLabel.type='text';
      inLabel.value = isCreate ? '' : t.label;
      inLabel.placeholder = 'e.g. Design';
      inLabel.setAttribute('aria-label','Tab label');
      l1.appendChild(inLabel); r1.appendChild(l1); tabPop.appendChild(r1);
      var tg = el('div','toggles');
      var tH = el('div','tgl sn-tgl-heart'+((!isCreate && t.heart)?' on':''), '\uD83D\uDC9C Purple Heart');
      var tS = el('div','tgl sn-tgl-star'+((!isCreate && t.star)?' on':''), '\u2B50 Gold Star');
      tH.addEventListener('click', function(){ setClass(tH,'on',!hasClass(tH,'on')); setClass(tS,'on',false); });
      tS.addEventListener('click', function(){ setClass(tS,'on',!hasClass(tS,'on')); setClass(tH,'on',false); });
      tg.appendChild(tH); tg.appendChild(tS); tabPop.appendChild(tg);
      if(isCreate && store.hiddenTabs.length){
        tabPop.appendChild(el('p','sn-msub','HIDDEN — TAP TO RESTORE'));
        store.hiddenTabs.forEach(function(key){
          var rb = el('button','sn-btn sn-restore',''); rb.type='button';
          rb.textContent = prettyCat(key);
          rb.addEventListener('click', function(){
            store.hiddenTabs = store.hiddenTabs.filter(function(x){ return x!==key; });
            saveStore(store); renderAll(); openTabEditor(null, true, anchor);
          });
          tabPop.appendChild(rb);
        });
      }
      var ft = el('div','ft');
      var cancel = el('button','sn-btn sn-cancel','Cancel'); cancel.type='button';
      cancel.addEventListener('click', function(){ tabPop.style.display='none'; });
      var save = el('button','sn-btn primary sn-save','Save'); save.type='button';
      save.addEventListener('click', function(){
        var label = inLabel.value.trim() || (isCreate ? 'New Tab' : t.label);
        var heart = hasClass(tH,'on'), star = hasClass(tS,'on');
        if(isCreate){
          var dup = store.tabs.some(function(x){ return x.label.toLowerCase()===label.toLowerCase(); });
          if(!dup) store.tabs.push({ id:'tab-'+Date.now(), key:'custom:'+label,
            label:label, heart:heart, star:star, custom:true });
        } else {
          store.tabs.forEach(function(x){
            if(x.id===t.id){ x.label=label; x.heart=heart; x.star=star; }
          });
        }
        saveStore(store); tabPop.style.display='none'; renderAll();
      });
      ft.appendChild(cancel); ft.appendChild(save); tabPop.appendChild(ft);
      tabPop.style.display='block';
      placeNear(anchor, tabPop);
      if(inLabel.focus) inLabel.focus();
    }

    /* His global close: click outside, or Escape, dismisses menu + popover. */
    document.addEventListener('click', function(ev){
      var t = ev.target, inside = false;
      try{
        inside = !!(t && ((tabs.contains && tabs.contains(t)) ||
          (tabMenu.contains && tabMenu.contains(t)) || (tabPop.contains && tabPop.contains(t))));
      }catch(e){}
      if(!inside){ tabMenu.style.display='none'; tabPop.style.display='none'; }
    });

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
      if(ev.key === 'Escape'){ tabMenu.style.display='none'; tabPop.style.display='none'; }
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
      if(n.body){
        mbox.appendChild(el('p','sl-msub','FULL NOTE'));
        var full = el('div','sl-fullnote',''); full.textContent = n.body; mbox.appendChild(full);
      }
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
    stage._refreshRows = refreshRows;

    var foot = el('footer','sl-foot','');
    foot.textContent = 'stored on this device \u00B7 the Brain stays the source of truth';
    stage.appendChild(foot);
    return stage;
  }

  window.NayaRooms = window.NayaRooms || {};
  window.NayaRooms.smartList = SmartList;
})();
