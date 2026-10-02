/* SMART MAIL — how people communicate inside the NayaNET network.
 * Registry: "mail", route "/mail", theme blue.
 * Contract: window.NayaRooms.smartMail(el, ctx)
 *   ctx.threads  — thread view-models from MailAdapter.parseThreads
 *   ctx.contacts  — [{id,name,role,color}] (shared contact contract)
 *   ctx.spaces    — [{id,name,color}] mail can be addressed to a space
 *   ctx.me        — id of the mailbox owner (default 'naya4')
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
    var contacts = Array.isArray(ctx.contacts) ? ctx.contacts : [];
    var spaces = Array.isArray(ctx.spaces) ? ctx.spaces : [];
    var byId = {};
    contacts.forEach(function(c){ byId[c.id]=c; });
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
    var demo = el('p','ml-demo',''); demo.textContent='DEMO THREADS \u00B7 seeded for design review \u00B7 your sent mail persists locally';
    head.appendChild(demo);
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

    function renderRail(){
      rail.innerHTML='';
      var defs = [
        ['inbox','INBOX', unreadCount()],
        ['unread','UNREAD', null],
        ['sent','SENT', null]
      ];
      defs.forEach(function(d){
        var b = el('button','ml-folder'+(state.folder===d[0]?' on':''));
        b.type='button'; b.setAttribute('aria-pressed', state.folder===d[0]?'true':'false');
        var nm = el('span','',''); nm.textContent=d[1]; b.appendChild(nm);
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
    return stage;
  }

  window.NayaRooms = window.NayaRooms || {};
  window.NayaRooms.smartMail = SmartMail;
})();
