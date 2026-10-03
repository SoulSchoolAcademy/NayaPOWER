/* CONNECTIONS — Room: everybody within NayaNET you can communicate with.
 * Registry: "connections", route "/connections", identity ROSE.
 * Contract: window.NayaRooms.connections(el, ctx)
 *   ctx.contacts — from ConnectionsAdapter.parseContacts (real people)
 *   ctx.onCompose — optional fn(contact); WRITE MAIL hands the contact to
 *     Smart Mail's composer (the shell routes it; previews use a handoff key).
 * People spine: contacts resolve through window.NayaPeople, the registry
 * shared with Smart Mail — add someone in Mail and they appear here.
 * Lists persist in localStorage `naya.connections.lists` (seed: "Team Naya").
 * Message drafts persist in `naya.connections.drafts` — honest drafts,
 * never presented as sent.
 * Law: every button has a real consequence. These contacts are REAL.
 */
(function(){
  'use strict';

  var LS_LISTS = 'naya.connections.lists';
  var LS_DRAFTS = 'naya.connections.drafts';

  function loadLists(){
    try{
      var raw = localStorage.getItem(LS_LISTS);
      if(raw){ var l = JSON.parse(raw); if(l && Array.isArray(l.lists)) return l; }
    }catch(e){}
    return null;
  }

  function seedLists(contacts){
    return { lists:[{ id:'team-naya', name:'Team Naya',
                      members: contacts.map(function(c){ return c.id; }) }] };
  }

  function saveLists(state){
    try{ localStorage.setItem(LS_LISTS, JSON.stringify(state)); }catch(e){}
  }

  function loadDrafts(){
    try{ return JSON.parse(localStorage.getItem(LS_DRAFTS) || '{}'); }catch(e){ return {}; }
  }

  function saveDraft(contactId, text){
    var d = loadDrafts();
    d[contactId] = { text:text, savedAt:new Date().toISOString() };
    try{ localStorage.setItem(LS_DRAFTS, JSON.stringify(d)); }catch(e){}
    return d[contactId];
  }

  function Connections(el, ctx){
    ctx = ctx || {};
    /* people spine: the same shared registry Smart Mail reads — seeded from
       ctx.contacts on first run, so both rooms see one truth. */
    var contacts = (window.NayaPeople && window.NayaPeople.ensureSeeded)
      ? window.NayaPeople.ensureSeeded(ctx.contacts)
      : (Array.isArray(ctx.contacts) ? ctx.contacts : []);
    var byId = {};
    contacts.forEach(function(c){ byId[c.id] = c; });

    var store = loadLists() || seedLists(contacts);
    /* repair: drop member ids that no longer exist, keep seed if empty */
    store.lists.forEach(function(l){
      l.members = l.members.filter(function(id){ return byId[id]; });
    });
    if(!store.lists.length) store = seedLists(contacts);
    saveLists(store);

    var state = { filter:'all', draftFor:null };

    var stage = el('div','cx-stage');

    var head = el('header','cx-head');
    head.appendChild(el('p','cx-kicker','CONNECTIONS'));
    var h1 = el('h1','cx-title',''); h1.textContent = 'Everybody you can reach';
    head.appendChild(h1);
    var sub = el('p','cx-sub','');
    sub.textContent = 'The people of your network. Save them into lists, open a card, and start a message — drafts stay yours until you send them.';
    head.appendChild(sub);
    stage.appendChild(head);

    var main = el('div','cx-main');
    var side = el('nav','cx-side'); side.setAttribute('aria-label','Lists');
    var grid = el('div','cx-grid');
    main.appendChild(side); main.appendChild(grid);
    stage.appendChild(main);

    function renderSide(){
      side.innerHTML = '';
      side.appendChild(el('p','cx-side-label','LISTS'));
      var all = chip('All', contacts.length, state.filter==='all', function(){ state.filter='all'; sync(); });
      side.appendChild(all);
      store.lists.forEach(function(l){
        side.appendChild(chip(l.name, l.members.length, state.filter===l.id, function(){
          state.filter = l.id; sync();
        }));
      });
      var nb = el('button','cx-new','+ New list'); nb.type='button';
      nb.addEventListener('click', function(){
        var name = promptName('Name the new list');
        if(!name) return;
        var id = 'list-' + Date.now().toString(36);
        store.lists.push({ id:id, name:name, members:[] });
        saveLists(store); state.filter = id; sync();
      });
      side.appendChild(nb);
    }

    function chip(label, count, on, fn){
      var b = el('button','cx-chip'+(on?' on':''));
      b.type = 'button'; b.setAttribute('aria-pressed', on?'true':'false');
      var t = el('span','',''); t.textContent = label; b.appendChild(t);
      var c = el('span','cx-chip-n',''); c.textContent = count; b.appendChild(c);
      b.addEventListener('click', fn);
      return b;
    }

    function visible(){
      if(state.filter==='all') return contacts;
      var l = store.lists.filter(function(x){ return x.id===state.filter; })[0];
      if(!l) return contacts;
      return l.members.map(function(id){ return byId[id]; }).filter(Boolean);
    }

    function renderGrid(){
      grid.innerHTML = '';
      var list = visible();
      if(!list.length){
        var e = el('p','cx-empty','');
        e.textContent = 'This list is empty. Open a contact and save them here.';
        grid.appendChild(e); return;
      }
      list.forEach(function(c, i){ grid.appendChild(card(c, i)); });
    }

    function card(c, i){
      var a = el('article','cx-card');
      a.style.setProperty('--cc', c.color);
      a.style.setProperty('--i', i);
      a.style.animationDelay = Math.min(i*0.05, 0.6)+'s';
      a.setAttribute('role','button'); a.setAttribute('tabindex','0');
      a.setAttribute('aria-label','Open '+c.name);
      var av = el('span','cx-ava',''); av.textContent = initials(c.name); a.appendChild(av);
      var nm = el('h2','cx-name',''); nm.textContent = c.name; a.appendChild(nm);
      if(c.role){ var r = el('p','cx-role',''); r.textContent = c.role; a.appendChild(r); }
      var lists = store.lists.filter(function(l){ return l.members.indexOf(c.id)>=0; })
                             .map(function(l){ return l.name; });
      if(lists.length){ var m = el('p','cx-in',''); m.textContent = 'In: '+lists.join(', '); a.appendChild(m); }
      var open = function(){ openModal(c); };
      a.addEventListener('click', open);
      a.addEventListener('keydown', function(ev){
        if(ev.key==='Enter'||ev.key===' '){ ev.preventDefault(); open(); }
      });
      return a;
    }

    function initials(name){
      return String(name).split(/\s+/).map(function(w){ return w[0]||''; })
                         .join('').slice(0,2).toUpperCase();
    }

    function promptName(msg){
      var v = null;
      try{ v = window.prompt(msg, ''); }catch(e){}
      return v && v.trim() ? v.trim().slice(0,40) : null;
    }

    /* ---------- detail modal ---------- */
    var overlay = el('div','cx-overlay'); overlay.style.display='none';
    var mcard = el('div','cx-modal');
    overlay.appendChild(mcard);
    overlay.addEventListener('click', function(ev){ if(ev.target===overlay) closeModal(); });
    document.addEventListener('keydown', function(ev){
      if(ev.key==='Escape' && overlay.style.display==='flex') closeModal();
    });
    stage.appendChild(overlay);

    function openModal(c){
      state.draftFor = c.id;
      mcard.innerHTML = '';
      mcard.style.setProperty('--cc', c.color);
      var top = el('div','cx-mtop');
      var av = el('span','cx-ava big',''); av.textContent = initials(c.name); top.appendChild(av);
      var tt = el('div','');
      var nm = el('h2','cx-mname',''); nm.textContent = c.name; tt.appendChild(nm);
      if(c.role){ var r = el('p','cx-mrole',''); r.textContent = c.role; tt.appendChild(r); }
      top.appendChild(tt);
      mcard.appendChild(top);
      if(c.note){ var n = el('p','cx-mnote',''); n.textContent = c.note; mcard.appendChild(n); }

      /* save to list */
      mcard.appendChild(el('p','cx-mlabel','SAVE TO LIST'));
      var lp = el('div','cx-lpick');
      store.lists.forEach(function(l){
        var has = l.members.indexOf(c.id) >= 0;
        var b = el('button','cx-lbtn'+(has?' in':''), (has?'\u2713 ':'+ ')+l.name);
        b.type='button'; b.setAttribute('aria-pressed', has?'true':'false');
        b.addEventListener('click', function(){
          var i = l.members.indexOf(c.id);
          if(i>=0) l.members.splice(i,1); else l.members.push(c.id);
          saveLists(store); openModal(c); renderSide(); renderGrid();
        });
        lp.appendChild(b);
      });
      mcard.appendChild(lp);

      /* message draft */
      mcard.appendChild(el('p','cx-mlabel','MESSAGE'));
      var drafts = loadDrafts();
      var ta = el('textarea','cx-draft','');
      ta.setAttribute('placeholder','Write to '+c.name+'\u2026');
      ta.setAttribute('aria-label','Message draft to '+c.name);
      ta.value = (drafts[c.id] && drafts[c.id].text) || '';
      mcard.appendChild(ta);
      var row = el('div','cx-mrow');
      var sv = el('button','cx-btn','SAVE DRAFT'); sv.type='button';
      var st = el('span','cx-dstatus','');
      sv.addEventListener('click', function(){
        var rec = saveDraft(c.id, ta.value);
        st.textContent = 'Draft saved '+timeAgo(rec.savedAt)+' \u2014 not sent.';
      });
      row.appendChild(sv); row.appendChild(st);
      /* cross-room handoff: WRITE MAIL only exists when the shell (or preview)
         provides the composer route — no dead buttons. */
      if(typeof ctx.onCompose === 'function'){
        var wm = el('button','cx-btn','WRITE MAIL'); wm.type='button';
        wm.addEventListener('click', function(){ ctx.onCompose(c); });
        row.appendChild(wm);
      }
      mcard.appendChild(row);
      var honest = el('p','cx-honest','');
      honest.textContent = 'Drafts stay on this device. Nothing is sent anywhere from here.';
      mcard.appendChild(honest);

      var x = el('button','cx-btn ghost','CLOSE'); x.type='button';
      x.addEventListener('click', closeModal);
      mcard.appendChild(x);
      overlay.style.display='flex';
      var first = mcard.querySelector('.cx-lbtn'); if(first) first.focus();
    }

    function closeModal(){ overlay.style.display='none'; state.draftFor=null; }

    function timeAgo(iso){
      var s = Math.max(0, Math.floor((Date.now()-new Date(iso).getTime())/1000));
      if(s<60) return 'just now';
      var m = Math.floor(s/60); return m<60 ? m+'m ago' : Math.floor(m/60)+'h ago';
    }

    function sync(){ renderSide(); renderGrid(); }
    sync();
    return stage;
  }

  window.NayaRooms = window.NayaRooms || {};
  window.NayaRooms.connections = Connections;
})();
