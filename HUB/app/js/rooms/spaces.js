/* SMART SPACES — Room: living rooms inside NayaNET.
 *
 * A Smart Space is a LIVING ROOM, not a directory card: create a space on any
 * topic (free subject, or gathered around an intelligent block), instant chat
 * inside it, mail the whole space at once (lands in the same conversation),
 * anyone can add people. Facebook-group-meets-instant-chat, gathered around
 * intelligence.
 *
 * Registry theme: VIOLET #8b5cf6 (room chrome). Each space carries its OWN
 * identity color (stable identity, never list position).
 *
 * Contract: window.NayaRooms.smartSpaces(el, ctx)
 *   ctx.spaces    — from SpacesAdapter.parseSpaces (normalized)
 *   ctx.contacts  — optional contact list (fallback when window.NayaPeople is absent)
 *   ctx.me        — my person id (author name resolution)
 *   ctx.onMail    — optional fn(space, text) called when a message is posted
 *   ctx.onCompose — optional fn({to, toKind:'space'}) — opens Smart Mail addressed to the space
 *   ctx.initialSpaceId — optional space id to open directly (a chat app opens
 *                        INTO the conversation); otherwise the last-opened space
 *                        is restored from naya.smartspaces.lastOpen
 *
 * Stores (localStorage):
 *   naya.smartspaces.posts   — {spaceId:[{ts: ISO string, text, author, demo?}]}
 *                               SHARED with Smart Mail: a mail addressed to a space
 *                               IS a post here. Same object, two views.
 *   naya.smartspaces.members — {spaceId:[personId]} user-added members
 *   naya.smartspaces.custom  — [user-created spaces] — real, unlabeled
 *
 * Law: seeded spaces/activity are DEMO-labeled; user content is unlabeled and
 * never invented. No faked realtime: no simulated typing, no fake incoming
 * messages. Text chat is real locally; audio is backend-gated future, not built.
 */
(function(){
  'use strict';

  var ROOM = '#8b5cf6';
  var STORE_KEY  = 'naya.smartspaces.posts';
  var MEMBER_KEY = 'naya.smartspaces.members';
  var CUSTOM_KEY = 'naya.smartspaces.custom';
  var LASTOPEN_KEY = 'naya.smartspaces.lastOpen'; /* return to your conversation */
  var PALETTE = ['#8b5cf6','#22d3ee','#ec4899','#a3e635','#facc15','#38bdf8','#fb923c'];

  function fmtTime(ts){
    if(!ts) return '';
    var d = new Date(ts);
    if(isNaN(d)) return '';
    var diff = Date.now() - d.getTime();
    var m = Math.floor(diff/60000);
    if(m < 1) return 'just now';
    if(m < 60) return m + 'm ago';
    var h = Math.floor(m/60);
    if(h < 24) return h + 'h ago';
    return Math.floor(h/24) + 'd ago';
  }
  function esc(s){ return String(s == null ? '' : s); }

  function loadJSON(key, fallback){
    try{
      var raw = localStorage.getItem(key);
      var v = raw ? JSON.parse(raw) : fallback;
      return v === undefined ? fallback : v;
    }catch(e){ return fallback; }
  }
  function saveJSON(key, val){
    try{ localStorage.setItem(key, JSON.stringify(val)); }catch(e){}
  }
  function loadPosts(){ var p = loadJSON(STORE_KEY, {}); return (p && typeof p === 'object') ? p : {}; }

  function initials(name){
    return String(name || '').split(/\s+/).map(function(w){ return w[0]; })
      .join('').slice(0,2).toUpperCase();
  }
  function colorFor(id){
    var h = 0, s = String(id || '');
    for(var i=0;i<s.length;i++){ h = (h*31 + s.charCodeAt(i)) % 997; }
    return PALETTE[h % PALETTE.length];
  }

  function SmartSpaces(el, ctx){
    ctx = ctx || {};
    var seeded = Array.isArray(ctx.spaces) ? ctx.spaces : [];
    var ctxContacts = Array.isArray(ctx.contacts) ? ctx.contacts : [];
    var me = ctx.me || null;
    var onMail = (typeof ctx.onMail === 'function') ? ctx.onMail : null;
    var onCompose = (typeof ctx.onCompose === 'function') ? ctx.onCompose : null;
    var posts = loadPosts();

    /* ---------- people: shared spine first, ctx.contacts as fallback ---------- */
    function allPeople(){
      var out = [], seen = {};
      function push(p){
        if(!p || !p.id || seen[p.id]) return;
        seen[p.id] = 1;
        out.push({id:p.id, name:p.name || p.id, role:p.role || '', color:p.color || '#888888'});
      }
      try{
        if(window.NayaPeople && typeof window.NayaPeople.load === 'function'){
          (window.NayaPeople.load() || []).forEach(push);
        }
      }catch(e){}
      ctxContacts.forEach(push);
      seeded.forEach(function(s){
        (s.members || []).forEach(push);
      });
      return out;
    }
    function personById(id){
      var found = null;
      allPeople().forEach(function(p){ if(p.id === id) found = p; });
      return found;
    }
    function myName(){
      if(me){ var p = personById(me); if(p) return p.name; }
      return 'You';
    }

    /* ---------- spaces: seeded + user-created ---------- */
    function customSpaces(){ return loadJSON(CUSTOM_KEY, []); }
    function effectiveSpaces(){
      var out = seeded.slice();
      customSpaces().forEach(function(c){
        if(!c || !c.id) return;
        out.push({
          id: c.id, name: c.name || 'Untitled space',
          color: c.color || colorFor(c.id),
          desc: c.topic || '',
          topic: c.topic || '', block: c.block || null,
          memberIds: c.memberIds || [],
          custom: true, demo: false
        });
      });
      return out;
    }
    function spaceById(id){
      var found = null;
      effectiveSpaces().forEach(function(s){ if(s.id === id) found = s; });
      return found;
    }
    function memberOverrides(){ return loadJSON(MEMBER_KEY, {}); }
    function effectiveMembers(space){
      var out = [], seen = {};
      function push(p){
        if(!p || !p.id || seen[p.id]) return;
        seen[p.id] = 1;
        out.push({id:p.id, name:p.name || p.id, role:p.role || '', color:p.color || '#888888'});
      }
      (space.members || []).forEach(push);                    /* seeded members */
      (space.memberIds || []).forEach(function(id){ push(personById(id)); }); /* custom space members */
      ((memberOverrides()[space.id]) || []).forEach(function(id){ push(personById(id)); }); /* added later */
      return out;
    }
    function addMember(spaceId, personId){
      var ov = memberOverrides();
      var arr = Array.isArray(ov[spaceId]) ? ov[spaceId] : [];
      if(arr.indexOf(personId) < 0) arr.push(personId);
      ov[spaceId] = arr;
      saveJSON(MEMBER_KEY, ov);
    }

    /* ---------- conversation: one unified thread, oldest first ----------
       Space posts AND mailed-to-space messages live in the same store:
       a mail addressed to a space IS a post here. */
    function conversation(space){
      var seededActs = (space.activity || []).map(function(a){
        return {ts:a.ts || '', text:String(a.text || ''), author:a.author || '',
                demo:true, mine:false};
      });
      var posted = (posts[space.id] || []).map(function(p){
        return {ts:p.ts || '', text:String(p.text || ''), author:p.author || 'You',
                demo:!!p.demo, mine:!p.demo};
      });
      var all = seededActs.concat(posted);
      all.sort(function(a,b){ return String(a.ts).localeCompare(String(b.ts)); });
      return all;
    }

    var stage = el('div','sp-stage');
    var state = { view:'grid', spaceId:null };
    /* a chat app opens INTO the conversation: preview can force one via
       ctx.initialSpaceId; otherwise return to the last-opened space. */
    (function(){
      var startId = ctx.initialSpaceId || loadJSON(LASTOPEN_KEY, null);
      if(startId && spaceById(startId)){ state.view = 'detail'; state.spaceId = startId; }
    })();
    var modalStack = [];

    /* header */
    var head = el('header','sp-head');
    head.appendChild(el('p','sp-kicker','SMART SPACES'));
    var h1 = el('h1','sp-title',''); h1.textContent = 'Rooms where people talk';
    head.appendChild(h1);
    var sub = el('p','sp-sub','');
    sub.textContent = 'Create a space on any topic, gather around a block of intelligence, and talk — instant chat here, or mail the whole space at once. Anyone can add people.';
    head.appendChild(sub);
    var demo = el('p','sp-demo','');
    demo.textContent = 'DEMO SPACES \u00B7 illustrative groups for design review \u00B7 your spaces and posts are yours';
    head.appendChild(demo);
    stage.appendChild(head);

    var body = el('div','sp-body');
    stage.appendChild(body);

    var foot = el('footer','sp-foot','');
    foot.textContent = 'no canonical group store yet \u00B7 your spaces and posts are saved on this device';
    stage.appendChild(foot);

    function render(){
      body.innerHTML = '';
      if(state.view === 'grid') body.appendChild(gridView());
      else {
        var s = spaceById(state.spaceId);
        if(!s){ state.view = 'grid'; body.appendChild(gridView()); return; }
        body.appendChild(detailView(s));
      }
    }
    function openSpace(id){ state.view = 'detail'; state.spaceId = id; saveJSON(LASTOPEN_KEY, id); render(); }
    function goGrid(){ state.view = 'grid'; state.spaceId = null; render(); }

    /* ---------- focus trap ---------- */
    function trapFocus(container){
      container.addEventListener('keydown', function(ev){
        if(ev.key !== 'Tab') return;
        var all = container.querySelectorAll('button, input, textarea, select');
        var vis = [];
        for(var i=0;i<all.length;i++){ if(!all[i].disabled) vis.push(all[i]); }
        if(!vis.length) return;
        var first = vis[0], last = vis[vis.length-1];
        if(ev.shiftKey && document.activeElement === first){ ev.preventDefault(); last.focus(); }
        else if(!ev.shiftKey && document.activeElement === last){ ev.preventDefault(); first.focus(); }
      });
    }
    function openModal(card){
      var overlay = el('div','sp-overlay');
      overlay.appendChild(card);
      overlay.addEventListener('click', function(ev){ if(ev.target === overlay) closeModal(); });
      stage.appendChild(overlay);
      modalStack.push(overlay);
      trapFocus(card);
      var first = card.querySelector('input, textarea, select, button');
      if(first) first.focus();
      return overlay;
    }
    function closeModal(){
      var ov = modalStack.pop();
      if(ov && ov.parentNode) ov.parentNode.removeChild(ov);
    }

    /* ---------------- GRID ---------------- */
    function gridView(){
      var wrap = el('div','sp-gridwrap');
      var headrow = el('div','sp-gridhead');
      var create = el('button','sp-create','+ CREATE A SPACE');
      create.type = 'button';
      create.addEventListener('click', createSpaceModal);
      headrow.appendChild(create);
      var hint = el('span','sp-gridhint','');
      hint.textContent = 'a space for any topic \u00B7 any group of people';
      headrow.appendChild(hint);
      wrap.appendChild(headrow);

      var grid = el('div','sp-grid');
      var spaces = effectiveSpaces();
      if(!spaces.length){
        grid.appendChild(el('p','sp-empty','No spaces yet. Create the first one.'));
      }
      spaces.forEach(function(s, i){
        var card = el('article','sp-card');
        card.style.setProperty('--sc', s.color);
        card.style.setProperty('--i', i);
        card.setAttribute('role','button');
        card.setAttribute('tabindex','0');
        card.setAttribute('aria-label','Open space: ' + s.name);
        var top = el('div','sp-card-top');
        var jewel = el('span','sp-jewel',''); jewel.textContent = '\u25C9';
        top.appendChild(jewel);
        var nm = el('h2','sp-card-name',''); nm.textContent = s.name;
        top.appendChild(nm);
        if(s.demo) top.appendChild(el('span','sp-demo-chip','DEMO'));
        card.appendChild(top);
        var topic = s.topic || s.desc;
        if(topic){ var dc = el('p','sp-card-desc',''); dc.textContent = topic; card.appendChild(dc); }
        var row = el('div','sp-card-members');
        effectiveMembers(s).slice(0,5).forEach(function(m){
          var dot = el('span','sp-mdot','');
          dot.style.setProperty('--mc', m.color || '#888888');
          dot.title = m.name;
          row.appendChild(dot);
        });
        var cnt = el('span','sp-card-count',''); 
        var n = effectiveMembers(s).length;
        cnt.textContent = n + (n === 1 ? ' person' : ' people') + ' \u00B7 ' + conversation(s).length + ' messages';
        row.appendChild(cnt);
        card.appendChild(row);
        /* the grid shows life: the latest message, so a space reads as a
           conversation at a glance — like every chat app. */
        var conv = conversation(s);
        if(conv.length){
          var lastM = conv[conv.length-1];
          var prev = el('p','sp-card-preview','');
          var who = el('b','sp-card-preview-who','');
          who.textContent = (lastM.author || 'You') + ' \u00B7 ' + fmtTime(lastM.ts);
          prev.appendChild(who);
          var rest = el('span','','');
          rest.textContent = ' \u2014 ' + String(lastM.text || '').slice(0, 90);
          prev.appendChild(rest);
          card.appendChild(prev);
        }
        var open = function(){ openSpace(s.id); };
        card.addEventListener('click', open);
        card.addEventListener('keydown', function(ev){
          if(ev.key === 'Enter' || ev.key === ' '){ ev.preventDefault(); open(); }
        });
        grid.appendChild(card);
      });
      wrap.appendChild(grid);
      return wrap;
    }

    /* ---------------- DETAIL (the living room) ---------------- */
    /* Research notes (2026-10-02, Discord + WhatsApp references):
       a group feed feels alive through DENSITY (6-10 messages/viewport,
       <=8px between rows), NO card chrome on messages (avatar+name+time+text
       in one tight row), a SLIM header (name+topic+count in 3 lines), a
       STICKY composer, and thin date dividers. Author color = stable identity
       via colorFor(). */
    function dayLabel(ts){
      var d = new Date(ts);
      if(isNaN(d)) return '';
      var now = new Date();
      var a = d.toDateString(), b = now.toDateString();
      if(a === b) return 'Today';
      var y = new Date(now.getTime() - 86400000).toDateString();
      if(a === y) return 'Yesterday';
      return d.toLocaleDateString(undefined, {month:'short', day:'numeric', year:'numeric'});
    }
    function firstName(n){ return String(n||'').split(/\s+/)[0] || ''; }
    function detailView(s){
      var d = el('div','sp-detail');
      d.style.setProperty('--sc', s.color);

      /* ---- slim header bar: back | ball + name + meta | actions ---- */
      var bar = el('div','sp-dbar');
      var back = el('button','sp-dback','\u2190');
      back.type = 'button';
      back.setAttribute('aria-label','Back to all spaces');
      back.addEventListener('click', goGrid);
      bar.appendChild(back);
      var sball = el('span','sp-avatar xs','');
      sball.textContent = initials(s.name);
      sball.style.setProperty('--av', s.color || '#8b5cf6');
      sball.setAttribute('aria-hidden','true');
      bar.appendChild(sball);
      var bt = el('div','sp-dbar-t');
      var bn = el('div','sp-dbar-n',''); bn.textContent = s.name;
      if(s.demo){ var dc = el('span','sp-fdemo','DEMO'); bn.appendChild(dc); }
      bt.appendChild(bn);
      var meta = el('div','sp-dbar-m','');
      (function(){
        var ms = effectiveMembers(s);
        var names = ms.slice(0,3).map(function(m){ return firstName(m.name); }).join(', ');
        var more = ms.length > 3 ? ' +' + (ms.length - 3) : '';
        meta.textContent = ms.length + (ms.length === 1 ? ' person' : ' people') +
          (names ? ' \u00B7 ' + names + more : '');
      })();
      bt.appendChild(meta);
      bar.appendChild(bt);
      var acts = el('div','sp-dbar-a');
      if(onCompose){
        var mailBtn = el('button','sp-dact','MAIL');
        mailBtn.type = 'button';
        mailBtn.setAttribute('aria-label','Mail the whole space');
        mailBtn.addEventListener('click', function(){
          try { onCompose({to:s.id, toKind:'space'}); } catch(e){}
        });
        acts.appendChild(mailBtn);
      }
      var addBtn = el('button','sp-dact','+ ADD');
      addBtn.type = 'button';
      addBtn.setAttribute('aria-label','Add people to ' + s.name);
      addBtn.addEventListener('click', function(){ addPeopleModal(s); });
      acts.appendChild(addBtn);
      bar.appendChild(acts);
      d.appendChild(bar);

      /* topic: one quiet line, not a billboard */
      var topic = s.topic || s.desc;
      if(topic){
        var tl = el('p','sp-dtopic',''); tl.textContent = topic;
        if(s.block){ var bl = el('span','sp-dtopic-b',''); bl.textContent = ' \u00B7 gathered around ' + s.block; tl.appendChild(bl); }
        d.appendChild(tl);
      }

      /* author color: the person's stable identity color when known, hash fallback */
      var colorByName = {};
      allPeople().forEach(function(p){ colorByName[p.name] = p.color || colorFor(p.id); });
      effectiveMembers(s).forEach(function(m){ colorByName[m.name] = m.color || colorFor(m.id); });
      function authorColor(name){ return colorByName[name] || colorFor(name || '?'); }

      /* ---- dense conversation feed ---- */
      var feed = el('div','sp-feed');
      feed.setAttribute('aria-live','polite');
      function paintFeed(scroll){
        feed.innerHTML = '';
        var msgs = conversation(s);
        if(!msgs.length) feed.appendChild(el('p','sp-fempty','Nothing said yet. Start the conversation.'));
        var prev = null;
        msgs.forEach(function(m){
          var day = dayLabel(m.ts);
          if(day && (!prev || dayLabel(prev.ts) !== day)){
            var dv = el('div','sp-fdiv');
            dv.appendChild(el('span','sp-fdiv-l',''));
            var dl = el('span','sp-fdiv-t',''); dl.textContent = day; dv.appendChild(dl);
            dv.appendChild(el('span','sp-fdiv-l',''));
            feed.appendChild(dv);
          }
          var sameDay = prev && dayLabel(prev.ts) === day;
          var dt = new Date(m.ts).getTime(), pt = prev ? new Date(prev.ts).getTime() : 0;
          var grouped = !!(prev && sameDay && prev.author === m.author && !isNaN(dt) && !isNaN(pt) && (dt - pt) < 5*60000);
          var row = el('div','sp-frow' + (grouped ? ' cont' : '') + (m.mine ? ' mine' : ''));
          var main = el('div','sp-fmain');
          if(!grouped){
            var av = el('span','sp-avatar xs','');
            av.textContent = initials(m.author || '?');
            av.style.setProperty('--av', authorColor(m.author));
            av.setAttribute('aria-hidden','true');
            row.appendChild(av);
            var mh = el('div','sp-fmeta');
            var au = el('span','sp-fauthor',''); au.textContent = m.author || 'You';
            au.style.color = authorColor(m.author);
            mh.appendChild(au);
            var t = el('span','sp-ftime',''); t.textContent = fmtTime(m.ts); mh.appendChild(t);
            if(m.demo) mh.appendChild(el('span','sp-fdemo','DEMO'));
            main.appendChild(mh);
          }
          var tx = el('p','sp-ftext',''); tx.textContent = m.text; main.appendChild(tx);
          row.appendChild(main);
          feed.appendChild(row);
          prev = m;
        });
        if(scroll) feed.scrollTop = feed.scrollHeight;
      }
      paintFeed(false);
      d.appendChild(feed);

      /* ---- sticky composer ---- */
      var box = el('div','sp-composer');
      var ta = el('textarea','sp-ta','');
      ta.placeholder = 'Message ' + s.name + '\u2026';
      ta.setAttribute('aria-label','Message to ' + s.name);
      ta.rows = 1;
      box.appendChild(ta);
      var send = el('button','sp-send','SEND');
      send.type = 'button';
      send.disabled = true;
      ta.addEventListener('input', function(){ send.disabled = !ta.value.trim(); });
      function doSend(){
        var text = ta.value.trim();
        if(!text) return;
        var entry = {ts:new Date().toISOString(), text:text, author:myName()};
        posts[s.id] = posts[s.id] || [];
        posts[s.id].push(entry);
        saveJSON(STORE_KEY, posts);
        ta.value = '';
        send.disabled = true;
        paintFeed(true);
        if(onMail){ try { onMail(s, text); } catch(e){} }
      }
      send.addEventListener('click', doSend);
      ta.addEventListener('keydown', function(ev){
        if(ev.key === 'Enter' && !ev.shiftKey){ ev.preventDefault(); doSend(); }
      });
      box.appendChild(send);
      d.appendChild(box);

      return d;
    }

    /* ---------------- CREATE SPACE ---------------- */
    var DEMO_BLOCKS = [
      'IB-004 \u2014 14 NayaPOWER blueprint images',
      'IB-006 \u2014 freeze-and-extend protocol',
      'IB-OP-001 \u2014 the 6-to-10 doctrine'
    ];
    function createSpaceModal(prefill){
      prefill = prefill || {};
      var card = el('div','sp-modal');
      card.setAttribute('role','dialog');
      card.setAttribute('aria-label','Create a space');
      card.appendChild(el('h2','sp-modal-title','CREATE A SPACE'));
      if(prefill.aroundLabel){
        var al = el('p','sp-modal-sub','');
        al.textContent = 'Gathered around: ' + prefill.aroundLabel;
        card.appendChild(al);
      }

      var nameF = field('Space name', 'text', 'e.g. Launch crew');
      var topicF = field('Topic \u2014 what is this space about?', 'text', 'e.g. everything about the Hub launch');
      if(prefill.name){ nameF.input.value = prefill.name; }
      if(prefill.topic){ topicF.input.value = prefill.topic; }
      card.appendChild(nameF.wrap); card.appendChild(topicF.wrap);

      var bw = el('label','sp-field');
      bw.appendChild(el('span','sp-flabel','Gather around an intelligent block (optional)'));
      var sel = el('select','sp-input'); sel.name = 'block';
      var opt0 = document.createElement('option'); opt0.value = ''; opt0.textContent = 'Just a subject \u2014 no block';
      sel.appendChild(opt0);
      DEMO_BLOCKS.forEach(function(b){
        var o = document.createElement('option'); o.value = b; o.textContent = b + '  [DEMO]';
        sel.appendChild(o);
      });
      if(prefill.block){
        // pre-select the block if it matches a known option, else add it
        var found = false;
        Array.prototype.forEach.call(sel.options, function(o){ if(o.value === prefill.block){ sel.value = prefill.block; found = true; } });
        if(!found){
          var extra = document.createElement('option');
          extra.value = prefill.block; extra.textContent = prefill.block;
          sel.appendChild(extra); sel.value = prefill.block;
        }
      }
      bw.appendChild(sel);
      card.appendChild(bw);

      var row = el('div','sp-modal-row');
      var cancel = el('button','sp-btn','CANCEL'); cancel.type = 'button';
      var create = el('button','sp-btn primary','CREATE SPACE'); create.type = 'button';
      function valid(){ create.disabled = !(nameF.input.value.trim() && topicF.input.value.trim()); }
      valid();
      nameF.input.addEventListener('input', valid);
      topicF.input.addEventListener('input', valid);
      cancel.addEventListener('click', closeModal);
      create.addEventListener('click', function(){
        var name = nameF.input.value.trim(), topic = topicF.input.value.trim();
        if(!name || !topic) return;
        var id = 'sp-' + Date.now().toString(36);
        var memberIds = [];
        if(me && personById(me)) memberIds.push(me);
        var list = customSpaces();
        list.push({id:id, name:name, topic:topic, block:sel.value || null,
                   color:colorFor(id), memberIds:memberIds});
        saveJSON(CUSTOM_KEY, list);
        closeModal();
        openSpace(id);
      });
      row.appendChild(cancel); row.appendChild(create);
      card.appendChild(row);
      openModal(card);
    }
    function field(label, type, placeholder){
      var wrap = el('label','sp-field');
      wrap.appendChild(el('span','sp-flabel',label));
      var input = el('input','sp-input','');
      input.type = type; input.placeholder = placeholder;
      wrap.appendChild(input);
      return {wrap:wrap, input:input};
    }

    /* ---------------- ADD PEOPLE ---------------- */
    function addPeopleModal(s){
      var card = el('div','sp-modal');
      card.setAttribute('role','dialog');
      card.setAttribute('aria-label','Add people to ' + s.name);
      card.appendChild(el('h2','sp-modal-title','ADD PEOPLE'));
      var sub = el('p','sp-modal-sub','');
      sub.textContent = 'Anyone in your network can join the conversation.';
      card.appendChild(sub);
      var list = el('div','sp-plist');
      function paintList(){
        list.innerHTML = '';
        var have = {};
        effectiveMembers(s).forEach(function(m){ have[m.id] = 1; });
        var cands = allPeople().filter(function(p){ return !have[p.id]; });
        if(!cands.length) list.appendChild(el('p','sp-empty','Everyone is already here.'));
        cands.forEach(function(p){
          var row = el('div','sp-prow');
          var av = el('span','sp-avatar sm','');
          av.textContent = initials(p.name);
          av.style.setProperty('--av', p.color || '#888888');
          row.appendChild(av);
          var tx = el('div','sp-ptx');
          var pn = el('span','sp-pname',''); pn.textContent = p.name; tx.appendChild(pn);
          if(p.role){ var pr = el('span','sp-prole',''); pr.textContent = p.role; tx.appendChild(pr); }
          row.appendChild(tx);
          var add = el('button','sp-padd','ADD');
          add.type = 'button';
          add.addEventListener('click', function(){
            addMember(s.id, p.id);
            closeModal();  /* remove this overlay from the DOM + stack */
            render();      /* refresh the detail members row */
            addPeopleModal(s); /* reopen fresh */
          });
          row.appendChild(add);
          list.appendChild(row);
        });
      }
      paintList();
      card.appendChild(list);
      var row = el('div','sp-modal-row');
      var done = el('button','sp-btn primary','DONE'); done.type = 'button';
      done.addEventListener('click', closeModal);
      row.appendChild(done);
      card.appendChild(row);
      openModal(card);
    }

    render();

    /* ---- "Create a Space around this intelligence" entry contract ----
     * Any room can launch space creation pre-filled from a block, note,
     * or feed item:
     *   window.NayaRooms.smartSpaces.createAround({kind:'block'|'note'|'feed'|'subject', id:'IB-006', title:'Freeze protocol'})
     * The spec is consumed on the next room render (or immediately if the
     * room is already mounted). Standalone page also honors ?around=ID.
     * Prefill is a suggestion — the human still names the space and taps CREATE.
     */
    function consumeAround(){
      var spec = null;
      try{
        if(window.__nayaCreateAround){ spec = window.__nayaCreateAround; window.__nayaCreateAround = null; }
        else {
          var m = /[?&]around=([^&#]*)/.exec(location.search || '');
          if(m) spec = {kind:'subject', id:decodeURIComponent(m[1]), title:decodeURIComponent(m[1])};
        }
      }catch(e){}
      if(!spec) return;
      var label = (spec.kind || 'subject') + ' ' + (spec.id || '');
      createSpaceModal({
        name: spec.title ? spec.title.slice(0, 60) : '',
        topic: spec.title ? ('Conversation around ' + spec.title) : '',
        block: spec.kind === 'block' ? (spec.id || '') : '',
        aroundLabel: label.trim()
      });
    }
    // consume after first paint so the modal opens over the grid
    setTimeout(consumeAround, 60);
    // if another room calls createAround while we're mounted, open it live
    stage.addEventListener('naya:create-around', consumeAround);
    document.addEventListener('naya:create-around', consumeAround);

    /* Escape: close modal first, else back to grid from detail */
    stage.addEventListener('keydown', function(ev){
      if(ev.key !== 'Escape') return;
      if(modalStack.length){ closeModal(); return; }
      if(state.view === 'detail') goGrid();
    });

    return stage;
  }

  window.NayaRooms = window.NayaRooms || {};
  window.NayaRooms.smartSpaces = SmartSpaces;
  /* Entry contract for other rooms: queue a "create around this" spec.
   * If the spaces room is already mounted, the pending spec is consumed
   * on a custom event; otherwise it waits for the next render. */
  window.NayaRooms.smartSpaces.createAround = function(spec){
    window.__nayaCreateAround = spec || null;
    try{ document.dispatchEvent(new CustomEvent('naya:create-around')); }catch(e){}
  };
})();
