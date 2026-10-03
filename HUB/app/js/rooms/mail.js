/* SMART MAIL — how people communicate inside the NayaNET network.
 * Registry: "mail", route "/mail", theme blue.
 * Contract: window.NayaRooms.smartMail(el, ctx)
 *   ctx.threads  — conversation view-models from MailAdapter.parseThreads:
 *     {id, subject, messages:[{id,from,to,toKind,subject,body,ts,unread,demo}],
 *      count, ts, unread, demo}
 *   ctx.contacts  — [{id,name,role,color}]; seeds window.NayaPeople, the
 *     people spine shared with Connections (one registry, not four copies)
 *   ctx.spaces    — [{id,name,color}] mail can be addressed to a space
 *   ctx.me        — id of the mailbox owner (default 'naya4')
 *   ctx.composeRequest — optional {to, toKind, subject, body}; opens the
 *     composer pre-addressed (cross-room handoff, e.g. from Connections)
 * People spine: ADD TO CONNECTIONS files an unknown sender into the shared
 * registry, so they appear in Connections and in the next compose.
 * Law: every button has a real consequence. Search searches, delete deletes
 * (two-tap), reply appends to the conversation, Send persists user messages
 * to localStorage (naya.smartmail.sent). All seeded messages carry DEMO.
 */
(function(){
  'use strict';

  var BLUE = '#3b82f6';
  var SENT_KEY = 'naya.smartmail.sent';
  var DEL_KEY  = 'naya.smartmail.deleted'; /* tombstoned threadIds — a deleted
     seeded thread stays deleted across reloads instead of resurrecting */

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

  function refreshThread(t){
    t.messages.sort(function(a,b){ return a.ts - b.ts; });
    var last = t.messages[t.messages.length-1];
    t.count = t.messages.length;
    t.ts = last ? last.ts : 0;
    t.unread = t.messages.some(function(m){ return m.unread; });
    t.demo = t.messages.every(function(m){ return m.demo; });
  }

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

    /* threads: seeded (demo) + user messages restored from persistence */
    var threads = Array.isArray(ctx.threads) ? ctx.threads.slice() : [];
    loadSent().forEach(function(rec){
      var t = findThread(rec.id);
      if(t){
        (rec.messages||[]).forEach(function(m){
          if(!t.messages.some(function(x){ return x.id===m.id; })) t.messages.push(m);
        });
        refreshThread(t);
      }else if(rec.messages && rec.messages.length){
        var nt = { id:rec.id, subject:rec.subject || '(no subject)', messages:rec.messages.slice() };
        refreshThread(nt);
        threads.push(nt);
      }
    });
    threads.sort(function(a,b){ return b.ts - a.ts; });
    /* the dead stay dead: tombstoned threads never resurrect on reload */
    (function(){
      var gone = {};
      loadDeleted().forEach(function(id){ gone[id]=1; });
      threads = threads.filter(function(t){ return !gone[t.id]; });
    })();

    var state = { folder:'inbox', selectedId:null, q:'' };

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

    var listCol = el('div','ml-listcol');
    var searchBar = el('div','ml-searchbar');
    var searchIcon = el('span','ml-searchicon','');
    searchIcon.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg>';
    searchBar.appendChild(searchIcon);
    var searchIn = el('input','ml-searchin');
    searchIn.type='search';
    searchIn.setAttribute('placeholder','Search mail\u2026');
    searchIn.setAttribute('aria-label','Search mail');
    searchIn.addEventListener('input', function(){
      state.q = searchIn.value.trim().toLowerCase();
      renderList();
    });
    searchBar.appendChild(searchIn);
    listCol.appendChild(searchBar);

    var list = el('div','ml-list'); list.setAttribute('role','listbox'); list.setAttribute('aria-label','Threads');
    listCol.appendChild(list);
    panes.appendChild(listCol);

    var read = el('article','ml-read'); read.setAttribute('aria-live','polite');
    panes.appendChild(read);

    stage.appendChild(panes);

    /* compose button */
    var composeBtn = el('button','ml-compose','+ COMPOSE');
    composeBtn.type='button';
    composeBtn.addEventListener('click', function(){ openCompose({}); });
    stage.appendChild(composeBtn);

    /* ---------- folders ---------- */
    function isSent(t){ return t.messages.length && t.messages[0].from===me; }
    function inboxThreads(){ return threads.filter(function(t){ return !isSent(t); }); }
    function sentThreads(){ return threads.filter(function(t){ return isSent(t); }); }
    function unreadCount(){ return inboxThreads().filter(function(t){ return t.unread; }).length; }

    /* folder identity: each folder owns a stable color + icon (Shawn, 2026-10-02).
       inbox stays blue, unread is green, sent is purple when lit.
       The unread count lives on UNREAD (green on green) — never a green
       badge inside the blue box. */
    var F_INBOX  = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-6l-2 3h-4l-2-3H2"/><path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/></svg>';
    var F_UNREAD = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z"/><path d="m22 6-10 7L2 6"/><circle cx="18.5" cy="5.5" r="2.8" fill="currentColor" stroke="#0b0b0e" stroke-width="1.6"/></svg>';
    var F_SENT   = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="m22 2-7 20-4-9-9-4z"/><path d="M22 2 11 13"/></svg>';

    function renderRail(){
      rail.innerHTML='';
      var defs = [
        ['inbox','INBOX', null,          '#3b82f6', '#93c5fd', F_INBOX],
        ['unread','UNREAD', unreadCount(), '#34d399', '#a7f3d0', F_UNREAD],
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
      var ts;
      if(state.folder==='sent') ts = sentThreads();
      else if(state.folder==='unread') ts = inboxThreads().filter(function(t){ return t.unread; });
      else ts = inboxThreads();
      if(state.q){
        var q = state.q;
        ts = ts.filter(function(t){
          var hay = (t.subject+' '+t.messages.map(function(m){
            return m.subject+' '+m.snippet+' '+m.body+' '+partyName(m.from,'person');
          }).join(' ')).toLowerCase();
          return hay.indexOf(q)>=0;
        });
      }
      return ts;
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
    /* the human face of a thread: the first participant who isn't me,
       else the last message's recipient. */
    function otherParty(t){
      for(var i=0;i<t.messages.length;i++){
        if(t.messages[i].from!==me) return {id:t.messages[i].from, kind:'person'};
      }
      var l = t.messages[t.messages.length-1];
      return l ? {id:l.to, kind:l.toKind} : {id:'?', kind:'person'};
    }

    function renderList(){
      list.innerHTML='';
      var ts = folderThreads();
      if(!ts.length){
        var empty = el('p','ml-empty','');
        empty.textContent = state.q ? 'No threads match your search.'
          : state.folder==='sent' ? 'Nothing sent yet. Compose your first network mail.'
          : 'All caught up. No threads here.';
        list.appendChild(empty);
        return;
      }
      ts.forEach(function(t){
        var op = otherParty(t);
        var last = t.messages[t.messages.length-1];
        var item = el('button','ml-thread'+(t.unread?' unread':'')+(state.selectedId===t.id?' sel':''));
        item.type='button'; item.setAttribute('role','option');
        item.setAttribute('aria-selected', state.selectedId===t.id?'true':'false');
        item.setAttribute('aria-label',(t.unread?'Unread: ':'')+t.subject+
          (t.count>1 ? ' ('+t.count+' messages)' : ''));

        var av = el('span','ml-avatar','');
        var nm = partyName(op.id, op.kind);
        av.textContent = nm.charAt(0).toUpperCase();
        av.style.setProperty('--pc', partyColor(op.id, op.kind));
        item.appendChild(av);

        var mid = el('span','ml-thread-mid');
        var top = el('span','ml-thread-top');
        var fromEl = el('span','ml-thread-from',''); fromEl.textContent=nm; top.appendChild(fromEl);
        var time = el('span','ml-thread-time',''); time.textContent=timeAgo(t.ts); top.appendChild(time);
        mid.appendChild(top);
        var sj = el('span','ml-thread-subj',''); sj.textContent=t.subject; mid.appendChild(sj);
        var sn = el('span','ml-thread-snip',''); sn.textContent=last.snippet; mid.appendChild(sn);
        item.appendChild(mid);

        if(t.count>1){
          var cnt = el('span','ml-count',''); cnt.textContent=t.count; item.appendChild(cnt);
        }
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
      if(t.unread){ t.messages.forEach(function(m){ m.unread=false; }); refreshThread(t); }
      renderRail(); renderList(); renderRead();
      var pane = read.querySelector('.ml-read-subj');
      if(pane) pane.focus();
    }

    /* ---------- reading pane: the conversation ---------- */
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
      var op = otherParty(t);

      var sj = el('h2','ml-read-subj',''); sj.textContent=t.subject; sj.tabIndex=-1; read.appendChild(sj);

      var meta = el('div','ml-read-meta');
      var names = [];
      t.messages.forEach(function(m){
        var n = partyName(m.from,'person');
        if(names.indexOf(n)<0) names.push(n);
      });
      var mm = el('span','ml-read-to','');
      mm.textContent = t.count+' message'+(t.count>1?'s':'')+' · '+names.join(', ');
      meta.appendChild(mm);
      if(t.demo){ var chip=el('span','ml-chip',''); chip.textContent='DEMO'; meta.appendChild(chip); }
      read.appendChild(meta);

      t.messages.forEach(function(m){
        var mine = m.from===me;
        var mc = el('div','ml-msg'+(mine?' mine':''));
        var mhead = el('div','ml-msg-head');
        var fav = el('span','ml-avatar sm','');
        fav.textContent=partyName(m.from,'person').charAt(0).toUpperCase();
        fav.style.setProperty('--pc', partyColor(m.from,'person'));
        mhead.appendChild(fav);
        var who = el('div','ml-msg-who');
        var fn = el('span','ml-msg-from',''); fn.textContent=partyName(m.from,'person'); who.appendChild(fn);
        var fd = el('span','ml-msg-date',''); fd.textContent=fmtFull(m.ts); who.appendChild(fd);
        mhead.appendChild(who);
        mc.appendChild(mhead);
        var mb = el('div','ml-msg-body');
        String(m.body||'').split(/\n\s*\n/).forEach(function(para){
          var p = el('p','',''); p.textContent=para.trim(); mb.appendChild(p);
        });
        mc.appendChild(mb);
        read.appendChild(mc);
      });

      var actions = el('div','ml-read-actions');
      var reply = el('button','ml-btn','REPLY'); reply.type='button';
      reply.addEventListener('click', function(){
        openCompose({ threadId:t.id, to:op.id, toKind:op.kind,
          subject:'Re: '+t.subject.replace(/^Re:\s*/i,'') });
      });
      actions.appendChild(reply);
      var toggle = el('button','ml-btn ghost','MARK UNREAD'); toggle.type='button';
      toggle.addEventListener('click', function(){
        t.messages.forEach(function(m){ m.unread=true; });
        refreshThread(t);
        renderRail(); renderList();
      });
      actions.appendChild(toggle);
      /* people spine: file the other party as a connection in one tap. */
      if(window.NayaPeople && window.NayaPeople.get && !window.NayaPeople.get(op.id)){
        var addP = el('button','ml-btn ghost','ADD TO CONNECTIONS'); addP.type='button';
        addP.addEventListener('click', function(){
          window.NayaPeople.add({ id:op.id, name:partyName(op.id,op.kind),
            role:'via Smart Mail', color:partyColor(op.id,op.kind) });
          reloadPeople();
          addP.textContent='IN CONNECTIONS \u2713'; addP.disabled=true;
        });
        actions.appendChild(addP);
      }
      var del = el('button','ml-btn ghost danger','DELETE'); del.type='button';
      del.addEventListener('click', function(){
        if(del.getAttribute('data-arm')==='1'){ deleteThread(t.id); return; }
        del.setAttribute('data-arm','1'); del.textContent='CONFIRM DELETE';
        setTimeout(function(){
          if(del.parentNode){ del.removeAttribute('data-arm'); del.textContent='DELETE'; }
        }, 3000);
      });
      actions.appendChild(del);
      read.appendChild(actions);
    }

    function deleteThread(id){
      for(var i=0;i<threads.length;i++){
        if(threads[i].id===id){ threads.splice(i,1); break; }
      }
      tombstone(id);
      try{
        var arr = loadSent().filter(function(r){ return r.id!==id; });
        localStorage.setItem(SENT_KEY, JSON.stringify(arr));
      }catch(e){}
      if(state.selectedId===id) state.selectedId=null;
      renderRail(); renderList(); renderRead();
    }

    /* ---------- compose ---------- */
    var overlay=null;
    function openCompose(preset){
      preset = preset || {};
      closeCompose();
      overlay = el('div','ml-overlay');
      var card = el('div','ml-modal'); card.setAttribute('role','dialog'); card.setAttribute('aria-label','Compose mail');
      overlay.appendChild(card);

      card.appendChild(el('h2','ml-modal-title', preset.threadId ? 'REPLY' : 'COMPOSE'));

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
        var thread = preset.threadId ? findThread(preset.threadId) : null;
        var msg={
          id:'m-'+Date.now().toString(36)+Math.floor(Math.random()*1e4).toString(36),
          from:me, to:parts[1]||'', toKind:parts[0]==='space'?'space':'person',
          subject: thread ? thread.subject : subject,
          snippet:body.slice(0,120), body:body,
          ts:Date.now(), unread:false, demo:false
        };
        if(thread){
          /* reply appends to the conversation — threads actually thread now */
          thread.messages.push(msg);
          refreshThread(thread);
          persistThread(thread);
          state.selectedId=thread.id;
        }else{
          var nt={ id:'thread-'+Date.now().toString(36), subject:subject, messages:[msg] };
          refreshThread(nt);
          threads.unshift(nt);
          persistThread(nt);
          state.folder = nt.messages[0].from===me ? 'sent' : 'inbox';
          state.selectedId=nt.id;
        }
        /* the organism loop (Shawn, 2026-10-02): a mail addressed to a space
           IS a post in that space — same object, two views. Spaces reads
           naya.smartspaces.posts, so the post lands in the space feed with
           no changes needed on the spaces side. */
        if(msg.toKind==='space' && msg.to){
          try{
            var SP_KEY='naya.smartspaces.posts';
            var sraw=localStorage.getItem(SP_KEY);
            var sall=sraw?JSON.parse(sraw):{};
            if(!sall || typeof sall!=='object') sall={};
            var slist=Array.isArray(sall[msg.to])?sall[msg.to]:[];
            slist.push({ts:new Date(msg.ts).toISOString(), text:msg.body,
                        author:partyName(me,'person')});
            sall[msg.to]=slist.slice(-100);
            localStorage.setItem(SP_KEY, JSON.stringify(sall));
          }catch(e){ /* space feed unavailable — the mail itself still sent */ }
        }
        closeCompose();
        renderRail(); renderList(); renderRead();
      });
      row.appendChild(send);
      var cancel = el('button','ml-btn ghost','CANCEL'); cancel.type='button';
      cancel.addEventListener('click', closeCompose);
      row.appendChild(cancel);
      card.appendChild(row);

      /* focus trap: Tab cycles inside the dialog */
      card.addEventListener('keydown', function(ev){
        if(ev.key!=='Tab') return;
        var all = card.querySelectorAll('button, input, textarea, select');
        var vis = [];
        for(var i=0;i<all.length;i++){ if(!all[i].disabled) vis.push(all[i]); }
        if(!vis.length) return;
        var first=vis[0], last=vis[vis.length-1];
        if(ev.shiftKey && document.activeElement===first){ ev.preventDefault(); last.focus(); }
        else if(!ev.shiftKey && document.activeElement===last){ ev.preventDefault(); first.focus(); }
      });

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

    /* ---------- persistence: user-authored messages only ---------- */
    function loadDeleted(){
      try{
        var raw = localStorage.getItem(DEL_KEY);
        var arr = raw ? JSON.parse(raw) : [];
        return Array.isArray(arr) ? arr.filter(function(x){ return typeof x==='string'; }) : [];
      }catch(e){ return []; }
    }
    function tombstone(id){
      try{
        var arr = loadDeleted();
        if(arr.indexOf(id)<0){ arr.push(id); localStorage.setItem(DEL_KEY, JSON.stringify(arr.slice(0,200))); }
      }catch(e){}
    }
    function loadSent(){
      try{
        var raw = localStorage.getItem(SENT_KEY);
        var arr = raw ? JSON.parse(raw) : [];
        return Array.isArray(arr) ? arr.filter(function(r){ return r && r.id && Array.isArray(r.messages); }) : [];
      }catch(e){ return []; }
    }
    function persistThread(t){
      try{
        var mine = t.messages.filter(function(m){ return !m.demo; });
        if(!mine.length) return;
        var arr = loadSent();
        var rec = { id:t.id, subject:t.subject, messages:mine };
        var ix=-1;
        for(var i=0;i<arr.length;i++){ if(arr[i].id===t.id){ ix=i; break; } }
        if(ix>=0) arr[ix]=rec; else arr.unshift(rec);
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
