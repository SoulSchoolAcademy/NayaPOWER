/* SMART MAIL — how people communicate inside the NayaNET network.
 * Registry: "mail", route "/mail", theme blue.
 * Contract: window.NayaRooms.smartMail(el, ctx)
 *   ctx.threads  — thread view-models from MailAdapter.parseThreads
 *   ctx.contacts  — [{id,name,role,color}]; seeds window.NayaPeople, the
 *     people spine shared with Connections (one registry, not four copies)
 *   ctx.spaces    — [{id,name,color}] mail can be addressed to a space
 *   ctx.me        — id of the mailbox owner (default 'naya4')
 *   ctx.composeRequest — optional {to, toKind, subject, body}; opens the
 *     composer pre-addressed (cross-room handoff, e.g. from Connections)
 * People spine: ADD TO CONNECTIONS files an unknown sender into the shared
 * registry, so they appear in Connections and in the next compose.
 * Law: every button has a real consequence. Filters filter, opening a
 * thread marks it read, Send really appends to Sent and persists to
 * localStorage (naya.smartmail.sent). All seeded threads carry DEMO.
 */
(function(){
  'use strict';

  var BLUE = '#3b82f6';
  var SENT_KEY = 'naya.smartmail.sent';

  function timeAgo(ts){
    var s = Math.max(0, Math.floor((Date.now()-ts)/1000));
    if(s < 60) return 'just now';
    var m = Math.floor(s/60); if(m < 60) return m+'m ago';
    var h = Math.floor(m/60); if(h < 24) return h+'h ago';
    var d = Math.floor(h/24); if(d < 7) return d+'d ago';
    return Math.floor(d/7)+'w ago';
  }

  function fmtFull(ts){
    var d = new Date(ts);
    return d.toLocaleDateString('en-US',{month:'long',day:'numeric'}) + ' · ' +
           d.toLocaleTimeString('en-US',{hour:'numeric',minute:'2-digit'});
  }

  function esc(s){ return String(s==null?'':s); }

  function SmartMail(el, ctx){
    ctx = ctx || {};
    var me = ctx.me || 'naya4';
    /* people spine: one shared registry across rooms; seeds from ctx.contacts
       on first run, then every room reads the same truth. */
    var contacts = (window.NayaPeople && window.NayaPeople.ensureSeeded)
      ? window.NayaPeople.ensureSeeded(ctx.contacts)
      : (Array.isArray(ctx.contacts) ? ctx.contacts : []);
    var spaces = Array.isArray(ctx.spaces) ? ctx.spaces : [];
    var byId = {};
    function reloadPeople(){
      if(window.NayaPeople && window.NayaPeople.load){
        var p = window.NayaPeople.load();
        if(p) contacts = p;
      }
      byId = {};
      contacts.forEach(function(c){ byId[c.id]=c; });
    }
    reloadPeople();
    var spaceById = {};
    spaces.forEach(function(s){ spaceById[s.id]=s; });

    /* threads: seeded (demo) + previously sent (persisted) */
    var threads = Array.isArray(ctx.threads) ? ctx.threads.slice() : [];
    loadSent().forEach(function(s){
      if(!threads.some(function(t){ return t.id===s.id; })) threads.push(s);
    });
    threads.sort(function(a,b){ return b.ts - a.ts; });

    var state = { folder:'inbox', selectedId:null };

    var stage = el('div','mail-stage');

    /* header */
    var head = el('header','ml-head');
    head.appendChild(el('p','ml-kicker','SMART MAIL'));
    var h1 = el('h1','ml-title',''); h1.textContent='See what you need to act on'; head.appendChild(h1);
    var sub = el('p','ml-sub','');
    sub.textContent='Mail inside the NayaNET network \u2014 write to a person or straight to a space. Nothing leaves the network; everything stays inspectable.';
    head.appendChild(sub);
    stage.appendChild(head);

    /* three panes */
    var panes = el('div','ml-panes');

    var rail = el('nav','ml-rail'); rail.setAttribute('aria-label','Mail folders');
    panes.appendChild(rail);

    var list = el('div','ml-list'); list.setAttribute('role','listbox'); list.setAttribute('aria-label','Threads');
    panes.appendChild(list);

    var read = el('article','ml-read'); read.setAttribute('aria-live','polite');
    panes.appendChild(read);

    stage.appendChild(panes);

    /* compose button */
    var composeBtn = el('button','ml-compose','+ COMPOSE');
    composeBtn.type='button';
    composeBtn.addEventListener('click', function(){ openCompose({}); });
    stage.appendChild(composeBtn);

    /* ---------- folders ---------- */
    function inboxThreads(){ return threads.filter(function(t){ return t.from!==me; }); }
    function sentThreads(){ return threads.filter(function(t){ return t.from===me; }); }
    function unreadCount(){ return inboxThreads().filter(function(t){ return t.unread; }).length; }

    /* folder identity: each folder owns a stable color + icon (Shawn, 2026-10-02).
       inbox stays blue, unread is green, sent is purple when lit. */
    var F_INBOX  = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-6l-2 3h-4l-2-3H2"/><path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/></svg>';
    var F_UNREAD = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z"/><path d="m22 6-10 7L2 6"/><circle cx="18.5" cy="5.5" r="2.6" fill="currentColor" stroke="#0b0e16" stroke-width="1.4"/></svg>';
    var F_SENT   = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m22 2-7 20-4-9-9-4z"/><path d="M22 2 11 13"/></svg>';

    function renderRail(){
      rail.innerHTML='';
      var defs = [
        ['inbox','INBOX', unreadCount(), '#3b82f6', '#93c5fd', F_INBOX],
        ['unread','UNREAD', null,        '#34d399', '#a7f3d0', F_UNREAD],
        ['sent','SENT',   null,          '#a855f7', '#d8b4fe', F_SENT]
      ];
      defs.forEach(function(d){
        var b = el('button','ml-folder'+(state.folder===d[0]?' on':''));
        b.type='button'; b.setAttribute('aria-pressed', state.folder===d[0]?'true':'false');
        b.style.setProperty('--fc', d[3]);
        b.style.setProperty('--fcl', d[4]);
        var ic = el('span','ml-ficon',''); ic.innerHTML = d[5]; b.appendChild(ic);
        var nm = el('span','ml-fname',''); nm.textContent=d[1]; b.appendChild(nm);
        if(d[2]){
          var badge = el('span','ml-badge',''); badge.textContent=d[2]; b.appendChild(badge);
        }
        b.addEventListener('click', function(){
          state.folder=d[0]; state.selectedId=null;
          renderRail(); renderList(); renderRead();
        });
        rail.appendChild(b);
      });
    }

    function folderThreads(){
      if(state.folder==='sent') return sentThreads();
      if(state.folder==='unread') return inboxThreads().filter(function(t){ return t.unread; });
      return inboxThreads();
    }

    /* ---------- thread list ---------- */
    function partyName(id, kind){
      if(kind==='space' && spaceById[id]) return spaceById[id].name;
      if(byId[id]) return byId[id].name;
      return id;
    }
    function partyColor(id, kind){
      if(kind==='space' && spaceById[id]) return spaceById[id].color;
      if(byId[id]) return byId[id].color;
      return '#8b93a3';
    }

    function renderList(){
      list.innerHTML='';
      var ts = folderThreads();
      if(!ts.length){
        var empty = el('p','ml-empty','');
        empty.textContent = state.folder==='sent'
          ? 'Nothing sent yet. Compose your first network mail.'
          : 'All caught up. No threads here.';
        list.appendChild(empty);
        return;
      }
      ts.forEach(function(t){
        var item = el('button','ml-thread'+(t.unread?' unread':'')+(state.selectedId===t.id?' sel':''));
        item.type='button'; item.setAttribute('role','option');
        item.setAttribute('aria-selected', state.selectedId===t.id?'true':'false');
        item.setAttribute('aria-label',(t.unread?'Unread: ':'')+t.subject);

        var av = el('span','ml-avatar','');
        var nm = partyName(t.from,'person');
        av.textContent = nm.charAt(0).toUpperCase();
        av.style.setProperty('--pc', partyColor(t.from,'person'));
        item.appendChild(av);

        var mid = el('span','ml-thread-mid');
        var top = el('span','ml-thread-top');
        var fromEl = el('span','ml-thread-from',''); fromEl.textContent=nm; top.appendChild(fromEl);
        var time = el('span','ml-thread-time',''); time.textContent=timeAgo(t.ts); top.appendChild(time);
        mid.appendChild(top);
        var sj = el('span','ml-thread-subj',''); sj.textContent=t.subject; mid.appendChild(sj);
        var sn = el('span','ml-thread-snip',''); sn.textContent=t.snippet; mid.appendChild(sn);
        item.appendChild(mid);

        if(t.unread){ item.appendChild(el('span','ml-dot','')); }
        if(t.demo){
          var chip = el('span','ml-chip',''); chip.textContent='DEMO'; item.appendChild(chip);
        }
        item.addEventListener('click', function(){ selectThread(t.id); });
        item.addEventListener('keydown', function(ev){
          if(ev.key==='Enter'||ev.key===' '){ ev.preventDefault(); selectThread(t.id); }
        });
        list.appendChild(item);
      });
    }

    function findThread(id){
      for(var i=0;i<threads.length;i++) if(threads[i].id===id) return threads[i];
      return null;
    }

    function selectThread(id){
      var t = findThread(id);
      if(!t) return;
      state.selectedId = id;
      if(t.unread){ t.unread=false; }
      renderRail(); renderList(); renderRead();
      var pane = read.querySelector('.ml-read-subj');
      if(pane) pane.focus();
    }

    /* ---------- reading pane ---------- */
    function renderRead(){
      read.innerHTML='';
      var t = findThread(state.selectedId);
      if(!t){
        var none = el('div','ml-read-empty');
        var p1 = el('p','',''); p1.textContent='Select a thread to read it.';
        none.appendChild(p1);
        read.appendChild(none);
        return;
      }
      var toKind = t.toKind==='space' ? 'space' : 'person';

      var sj = el('h2','ml-read-subj',''); sj.textContent=t.subject; sj.tabIndex=-1; read.appendChild(sj);

      var meta = el('div','ml-read-meta');
      var fav = el('span','ml-avatar sm','');
      fav.textContent=partyName(t.from,'person').charAt(0).toUpperCase();
      fav.style.setProperty('--pc', partyColor(t.from,'person'));
      meta.appendChild(fav);
      var who = el('div','ml-read-who');
      var fl = el('span','ml-read-from',''); fl.textContent=partyName(t.from,'person'); who.appendChild(fl);
      var tl = el('span','ml-read-to','');
      tl.textContent='to '+partyName(t.to,toKind)+(toKind==='space'?' (space)':'');
      who.appendChild(tl);
      meta.appendChild(who);
      var dt = el('span','ml-read-date',''); dt.textContent=fmtFull(t.ts); meta.appendChild(dt);
      if(t.demo){ var chip=el('span','ml-chip',''); chip.textContent='DEMO'; meta.appendChild(chip); }
      read.appendChild(meta);

      var body = el('div','ml-read-body');
      String(t.body||'').split(/\n\s*\n/).forEach(function(para){
        var p = el('p','',''); p.textContent=para.trim(); body.appendChild(p);
      });
      read.appendChild(body);

      var actions = el('div','ml-read-actions');
      var reply = el('button','ml-btn','REPLY'); reply.type='button';
      reply.addEventListener('click', function(){
        openCompose({ to:t.from, toKind:'person', subject:'Re: '+t.subject.replace(/^Re:\s*/i,'') });
      });
      actions.appendChild(reply);
      var toggle = el('button','ml-btn ghost','MARK UNREAD'); toggle.type='button';
      toggle.addEventListener('click', function(){
        t.unread=true; renderRail(); renderList();
      });
      actions.appendChild(toggle);
      /* people spine: a sender who isn't a connection yet can be filed
         in one tap — the registry is shared, so Connections sees them too. */
      if(window.NayaPeople && window.NayaPeople.get && !window.NayaPeople.get(t.from)){
        var addP = el('button','ml-btn ghost','ADD TO CONNECTIONS'); addP.type='button';
        addP.addEventListener('click', function(){
          window.NayaPeople.add({ id:t.from, name:partyName(t.from,'person'),
            role:'via Smart Mail', color:partyColor(t.from,'person') });
          reloadPeople();
          addP.textContent='IN CONNECTIONS \u2713'; addP.disabled=true;
        });
        actions.appendChild(addP);
      }
      read.appendChild(actions);
    }

    /* ---------- compose ---------- */
    var overlay=null;
    function openCompose(preset){
      closeCompose();
      overlay = el('div','ml-overlay');
      var card = el('div','ml-modal'); card.setAttribute('role','dialog'); card.setAttribute('aria-label','Compose mail');
      overlay.appendChild(card);

      card.appendChild(el('h2','ml-modal-title','COMPOSE'));

      var toRow = el('label','ml-field');
      toRow.appendChild(el('span','ml-field-l','TO'));
      var sel = el('select','ml-input'); sel.name='to';
      var pg = document.createElement('optgroup'); pg.label='People';
      contacts.forEach(function(c){
        var o=document.createElement('option'); o.value='person:'+c.id; o.textContent=c.name+' — '+c.role; pg.appendChild(o);
      });
      sel.appendChild(pg);
      var sg = document.createElement('optgroup'); sg.label='Spaces';
      spaces.forEach(function(s){
        var o=document.createElement('option'); o.value='space:'+s.id; o.textContent=s.name+' (space)'; sg.appendChild(o);
      });
      sel.appendChild(sg);
      if(preset.to) sel.value=(preset.toKind||'person')+':'+preset.to;
      toRow.appendChild(sel);
      card.appendChild(toRow);

      var sjRow = el('label','ml-field');
      sjRow.appendChild(el('span','ml-field-l','SUBJECT'));
      var sjIn = el('input','ml-input'); sjIn.type='text'; sjIn.name='subject';
      sjIn.value=preset.subject||''; sjIn.maxLength=140;
      sjIn.setAttribute('placeholder','Subject');
      sjRow.appendChild(sjIn);
      card.appendChild(sjRow);

      var bdRow = el('label','ml-field');
      bdRow.appendChild(el('span','ml-field-l','MESSAGE'));
      var bdIn = el('textarea','ml-input'); bdIn.name='body'; bdIn.rows=6;
      bdIn.setAttribute('placeholder','Write to the network…');
      bdIn.value = preset.body || '';
      bdRow.appendChild(bdIn);
      card.appendChild(bdRow);

      var err = el('p','ml-err',''); err.style.display='none'; card.appendChild(err);

      var row = el('div','ml-modal-row');
      var send = el('button','ml-btn primary','SEND'); send.type='button';
      send.addEventListener('click', function(){
        var parts=String(sel.value||'').split(':');
        var subject=sjIn.value.trim(), body=bdIn.value.trim();
        if(!subject || !body){
          err.textContent='Subject and message both need words before sending.';
          err.style.display='block';
          return;
        }
        var thread={
          id:'sent-'+Date.now().toString(36),
          from:me, to:parts[1]||'', toKind:parts[0]==='space'?'space':'person',
          subject:subject, snippet:body.slice(0,120), body:body,
          ts:Date.now(), unread:false, demo:false
        };
        threads.unshift(thread);
        persistSent(thread);
        state.folder='sent'; state.selectedId=thread.id;
        closeCompose();
        renderRail(); renderList(); renderRead();
      });
      row.appendChild(send);
      var cancel = el('button','ml-btn ghost','CANCEL'); cancel.type='button';
      cancel.addEventListener('click', closeCompose);
      row.appendChild(cancel);
      card.appendChild(row);

      overlay.addEventListener('click', function(ev){ if(ev.target===overlay) closeCompose(); });
      stage.appendChild(overlay);
      sel.focus();
    }
    function closeCompose(){
      if(overlay && overlay.parentNode) overlay.parentNode.removeChild(overlay);
      overlay=null;
    }
    document.addEventListener('keydown', function esc(ev){
      if(ev.key==='Escape' && overlay) closeCompose();
    });

    /* ---------- persistence ---------- */
    function loadSent(){
      try{
        var raw = localStorage.getItem(SENT_KEY);
        var arr = raw ? JSON.parse(raw) : [];
        return Array.isArray(arr) ? arr.filter(function(t){ return t && t.id && t.subject; }) : [];
      }catch(e){ return []; }
    }
    function persistSent(thread){
      try{
        var arr = loadSent();
        arr.unshift(thread);
        localStorage.setItem(SENT_KEY, JSON.stringify(arr.slice(0,50)));
      }catch(e){ /* storage unavailable — mail still sends in-memory */ }
    }

    renderRail(); renderList(); renderRead();

    /* cross-room handoff: the shell (or a sibling room) can open the composer
       pre-addressed — e.g. "write mail" from a connection card. */
    if(ctx.composeRequest && ctx.composeRequest.to){
      var cr = ctx.composeRequest;
      openCompose({ to:cr.to, toKind:cr.toKind || 'person',
                    subject:cr.subject || '', body:cr.body || '' });
    }

    return stage;
  }

  window.NayaRooms = window.NayaRooms || {};
  window.NayaRooms.smartMail = SmartMail;
})();
