/* ═══════════════════════════════════════════════════════════════════
   ROOM 01 — SMART FEED · THE MAIN SHOW · v7
   Learned from the live V7 page (deep dive 2026-10-02):
   - The feed is a RIVER of quiet snapshots. The full intelligent block
     lives on its own Smart Note surface — the two are never mashed
     together.
   - Restraint: orb · title · nutshell · why-now. No buttons, no modes,
     no chrome shouting over the intelligence.
   - USER-WORLD ONLY. Builder-world (PRs, contracts, lanes, ratify) is
     back-end lane work and never appears as a user feed action.
   - Tap a snapshot → the Smart Note: full layers in the live page's
     calm language, with only working tools (Evidence, Save, Ask).
   ═══════════════════════════════════════════════════════════════════ */
(function(){
  'use strict';

  const LAYERS=[
    ['nutshell','IN A NUTSHELL',''],
    ['human','HUMAN NOTE','HUMAN INPUT'],
    ['child','CHILD','SIMPLIFIED'],
    ['grandma','GRANDMA NOTE','WHY NOTICE?'],
    ['naya','NAYA NOTE','INTERPRETATION'],
    ['machine','MACHINE NOTE','EVIDENCE BOUNDARY'],
    ['learning','ADAPTIVE LEARNING','LEARNING'],
    ['means','WHAT IT MEANS','SIGNIFICANCE'],
    ['value',"WHAT'S IN IT FOR YOU?",'HUMAN VALUE']
  ];

  const TONES=['#ff4fd8','#9d75ff','#6675ff','#55b9ee','#55e39a','#b8ee57','#f1d75a','#ff9b4a','#ff5e6c'];

  const GLYPHS={
    decision:'<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 12.5l5 5L20 6.5"/></svg>',
    intelligence:'<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M4 8.5c2.6-2.6 5.4-2.6 8 0s5.4 2.6 8 0"/><path d="M4 13.5c2.6-2.6 5.4-2.6 8 0s5.4 2.6 8 0"/><path d="M4 18.5c2.6-2.6 5.4-2.6 8 0s5.4 2.6 8 0"/></svg>',
    signal:'<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.2" aria-hidden="true"><circle cx="12" cy="12" r="3.2" fill="#fff" stroke="none"/><circle cx="12" cy="12" r="7.5"/></svg>',
    event:'<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.2" stroke-linejoin="round" aria-hidden="true"><path d="M13 3L5 13.5h6L11 21l8-10.5h-6L13 3z"/></svg>'
  };

  const savedList=[];
  let allItems=[];
  let openNoteId=null;

  function FeedRoom(){
    const {el}=window.NayaUI, K=window.NayaRoomKit;
    const stage=el('section','feed-stage');
    stage.setAttribute('aria-label','Smart Feed — the Main Show');
    stage.appendChild(greeting(el));
    const river=el('div','feed-river');
    stage.appendChild(river);
    const note=el('div','note-view'); note.hidden=true;
    stage.appendChild(note);
    stage.appendChild(todayListBox(el));
    const foot=el('div','feed-stage-foot');
    const ask=el('button','feed-ask','<span>Ask Naya about today</span>');
    ask.type='button';
    const panel=askPanel(el);
    ask.addEventListener('click',()=>{
      panel.classList.toggle('open');
      if(panel.classList.contains('open')){const i=panel.querySelector('.ask-input'); if(i)i.focus();}
    });
    foot.appendChild(ask); foot.appendChild(panel); stage.appendChild(foot);
    stage.appendChild(evDrawer(el));

    K.load(stage,'feed',{limit:25},(payload,list)=>{
      allItems=(list||[]).map(o=>normalize(o,K));
      renderRiver(el,stage);
    },{
      title:'The stage is quiet',
      body:'There is no qualifying intelligence right now. When something matters, it appears here — ordered for you, never manufactured to fill the space.'
    });
    return stage;
  }

  function greeting(el){
    const h=new Date().getHours();
    const part=h<12?'Good morning':h<18?'Good afternoon':'Good evening';
    const who=(window.NayaRuntime&&window.NayaRuntime.user&&window.NayaRuntime.user.name)||'';
    const date=new Date().toLocaleDateString('en-US',{weekday:'long',month:'long',day:'numeric'});
    const wrap=el('header','feed-stage-head');
    const g=el('h1','feed-greeting',''); g.textContent=who?part+', '+who:part;
    const d=el('p','feed-dateline','');
    d.innerHTML='<span>'+esc(date.toUpperCase())+'</span><span class="feed-dot">·</span><span>YOUR INTELLIGENCE TODAY</span>';
    const s=el('p','feed-daystate','');
    s.textContent='Your intelligence has a place to be understood, explored, remembered, and acted on — without making you manage the architecture.';
    wrap.appendChild(g); wrap.appendChild(d); wrap.appendChild(s);
    return wrap;
  }

  /* ——— THE RIVER: quiet snapshots. Tap → the Smart Note. ——— */
  function renderRiver(el,stage){
    const river=stage.querySelector('.feed-river');
    const note=stage.querySelector('.note-view');
    note.hidden=true; river.hidden=false;
    river.innerHTML='';
    if(!allItems.length){
      const p=el('p','feed-daystate','');
      p.textContent='Nothing today yet. When something matters, it appears here — never manufactured to fill the space.';
      river.appendChild(p); return;
    }
    const k=el('p','river-kicker','');
    k.innerHTML='<span>'+allItems.length+'</span>&nbsp;&nbsp;INTELLIGENCE BLOCK'+(allItems.length===1?'':'S')+' · TODAY';
    river.appendChild(k);
    allItems.forEach(b=>river.appendChild(snapshot(el,b)));
  }

  function snapshot(el,b){
    const a=el('article','snap-board');
    a.style.setProperty('--tone',toneFor(b));
    a.setAttribute('tabindex','0');
    a.setAttribute('role','button');
    a.setAttribute('aria-label','Open: '+b.title);
    const orb=el('div','sb-orb'); orb.innerHTML=glyphFor(b); orb.setAttribute('aria-hidden','true');
    const main=el('div','sb-main');
    const th=el('p','sb-theme',''); th.textContent=themeFor(b);
    const t=el('h2','sb-title',''); t.textContent=b.title;
    const n=el('p','sb-nut',''); n.textContent=b.layers.nutshell||'';
    main.appendChild(th); main.appendChild(t); main.appendChild(n);
    if(b.whyNow){
      const w=el('p','sb-why','');
      w.innerHTML='<strong>WHY NOW</strong><span>'+esc(b.whyNow)+'</span>';
      main.appendChild(w);
    }
    a.appendChild(orb); a.appendChild(main);
    const open=()=>{
      openNoteId=b.id;
      const stage=a.closest('.feed-stage');
      renderNote(el,stage,b);
      stage.scrollIntoView({block:'start'});
    };
    a.addEventListener('click',open);
    a.addEventListener('keydown',e=>{ if(e.key==='Enter'||e.key===' '){ e.preventDefault(); open(); }});
    return a;
  }

  function themeFor(b){
    const t=(b.kicker.split(' · ')[0]||'INTELLIGENCE').toUpperCase();
    return t;
  }
  function glyphFor(b){
    const t=(b.kicker.split(' · ')[0]||'').toLowerCase();
    return GLYPHS[t]||GLYPHS.intelligence;
  }

  /* ——— THE SMART NOTE: the full block, live-page language ——— */
  function renderNote(el,stage,b){
    const river=stage.querySelector('.feed-river');
    const note=stage.querySelector('.note-view');
    river.hidden=true; note.hidden=false; note.innerHTML='';
    note.style.setProperty('--tone',toneFor(b));

    const back=el('button','note-back',''); back.type='button';
    back.innerHTML='<span>←</span><span>Today</span>';
    back.setAttribute('aria-label','Back to today’s river');
    back.addEventListener('click',()=>renderRiver(el,stage));
    note.appendChild(back);

    const head=el('div','note-head');
    const orb=el('div','note-orb'); orb.innerHTML=glyphFor(b); orb.setAttribute('aria-hidden','true');
    const t=el('h2','note-title',''); t.textContent=b.title;
    head.appendChild(orb); head.appendChild(t);
    note.appendChild(head);

    const canon=el('p','note-canon',''); canon.textContent='CANONICAL INTELLIGENCE';
    const src=el('p','note-source',''); src.textContent='SOURCE SEPARATED';
    note.appendChild(canon); note.appendChild(src);

    const layers=el('div','note-layers');
    LAYERS.forEach(([key])=>{
      if(b.layers[key]) layers.appendChild(makeLayer(el,key,b.layers[key]));
    });
    note.appendChild(layers);

    /* Only working tools. Everything here does something real. */
    const tools=el('div','note-tools');
    tools.appendChild(toolBtn(el,'Evidence',()=>openEvidence(b)));
    tools.appendChild(toolBtn(el,savedList.includes(b.id)?'Saved ✓':'Save to Today',()=>{
      if(!savedList.includes(b.id))savedList.push(b.id);
      renderTodayList(); renderNote(el,stage,b);
    }));
    tools.appendChild(toolBtn(el,'Ask Naya',()=>{
      const panel=document.querySelector('.ask-panel');
      if(panel){panel.classList.add('open');
        const i=panel.querySelector('.ask-input');
        if(i){i.value='About "'+b.title+'": ';}}
      renderRiver(el,stage);
      const foot=document.querySelector('.feed-stage-foot');
      if(foot)foot.scrollIntoView({behavior:'smooth',block:'center'});
      const inp=document.querySelector('.ask-input'); if(inp)inp.focus();
    }));
    note.appendChild(tools);

    const foot=el('footer','note-foot');
    foot.innerHTML='<p>ONE INTELLIGENCE · MANY VIEWS · ONE IDENTITY</p><p>TRUST: SOURCE / INTERPRETATION SEPARATED</p>';
    note.appendChild(foot);
  }

  function toolBtn(el,label,fn){
    const x=el('button','note-tool',''); x.type='button'; x.textContent=label;
    x.addEventListener('click',fn); return x;
  }

  function makeLayer(el,key,text){
    const found=LAYERS.find(l=>l[0]===key);
    const label=found?found[1]:key.toUpperCase();
    const sub=found?found[2]:'';
    const d=el('div','nlayer');
    const lab=el('p','nlayer-label','');
    lab.innerHTML='<strong>'+esc(label)+'</strong>'+(sub?'<span>'+esc(sub)+'</span>':'');
    const txt=el('p','nlayer-text',''); txt.textContent=text;
    d.appendChild(lab); d.appendChild(txt);
    return d;
  }

  /* ——— Object → snapshot. Only real fields; nothing invented. ——— */
  function normalize(o,K){
    const src=o.layers||o.intelligent_block||o.content||{};
    const layers={};
    LAYERS.forEach(([key])=>{
      const v=o[key]??src[key];
      if(typeof v==='string'&&v.trim()) layers[key]=v.trim();
    });
    if(!layers.nutshell){
      const s=K.summary(o);
      if(s) layers.nutshell=s;
    }
    if(!layers.machine) layers.machine=evidenceLine(o);
    const type=(o.category||o.type||o.kind||'').toString().toUpperCase();
    const state=(o.truth_state||o.state||'').toString().toUpperCase();
    const srcName=typeof o.source==='string'?o.source:(o.source&&o.source.name)||'';
    return {
      id:String(o.intelligent_block_id||o.id||type+'-'+Math.abs(hashCode(o.title||''))),
      title:K.title(o,'Untitled intelligence'),
      kicker:[type||'INTELLIGENCE', state||null].filter(Boolean).join(' · '),
      source:srcName,
      truth_state:state,
      created_at:o.created_at||o.timestamp||o.time||'',
      whyNow:o.why_now||o.whyNow||'',
      layers,
      related:Array.isArray(o.related)?o.related:[],
      people:Array.isArray(o.people)?o.people:[],
      context:o.context||null
    };
  }

  function hashCode(s){let h=0;for(let i=0;i<s.length;i++){h=(h*31+s.charCodeAt(i))|0;}return h;}
  function toneFor(b){ return TONES[Math.abs(hashCode('tone:'+b.id)) % TONES.length]; }

  function evidenceLine(o){
    const bits=[];
    const src=typeof o.source==='string'?o.source:(o.source&&o.source.name);
    if(src) bits.push('Source: '+src);
    const st=o.truth_state||o.state;
    if(st) bits.push('State: '+String(st).toUpperCase());
    const t=o.created_at||o.timestamp||o.time;
    if(t) bits.push('Time: '+t);
    const id=o.intelligent_block_id||o.id;
    if(id) bits.push('ID: '+id);
    return bits.length
      ? bits.join(' — ')
      : 'No provenance is attached to this object, so no evidence boundary can be stated.';
  }

  function todayListBox(el){
    const box=el('div','today-list'); box.id='today-list';
    renderTodayList(); return box;
  }
  function renderTodayList(){
    const box=document.getElementById('today-list'); if(!box)return;
    box.innerHTML='';
    if(!savedList.length){box.classList.remove('show');return;}
    box.classList.add('show');
    const {el}=window.NayaUI;
    const h=el('h3','','Today’s list'); box.appendChild(h);
    const sub=el('p','tl-sub',''); sub.textContent=savedList.length+' saved — preview-local working list.'; box.appendChild(sub);
    const ul=el('ul','');
    savedList.forEach(id=>{
      const o=allItems.find(x=>x.id===id); if(!o)return;
      const li=el('li','');
      const span=el('span','',''); span.textContent=o.title;
      const rm=el('button','','Remove'); rm.type='button';
      rm.addEventListener('click',()=>{
        const ix=savedList.indexOf(id); if(ix>=0)savedList.splice(ix,1);
        renderTodayList();
      });
      li.appendChild(span); li.appendChild(rm); ul.appendChild(li);
    });
    box.appendChild(ul);
  }

  function evDrawer(el){
    const wrap=el('div','ev-wrap','');
    const bd=el('div','ev-backdrop',''); bd.id='ev-backdrop';
    const dr=el('aside','ev-drawer',''); dr.id='ev-drawer';
    dr.setAttribute('aria-label','Evidence'); dr.setAttribute('role','dialog'); dr.setAttribute('aria-modal','true');
    bd.addEventListener('click',closeEvidence);
    wrap.appendChild(bd); wrap.appendChild(dr);
    if(!window.__nayaCloseEvidence) window.__nayaCloseEvidence=closeEvidence;
    return wrap;
  }
  function openEvidence(b){
    const {el}=window.NayaUI;
    const dr=document.getElementById('ev-drawer'), bd=document.getElementById('ev-backdrop');
    if(!dr||!bd)return;
    dr.innerHTML='';
    const k=el('p','ev-kicker',''); k.textContent='EVIDENCE · '+(b.truth_state||'STATE UNSTATED');
    const h=el('h3','',''); h.textContent=b.title;
    dr.appendChild(k); dr.appendChild(h);
    const ul=el('ul','ev-chain');
    const rows=[
      ['SOURCE',(b.source||'Unnamed source')+' — origin of this intelligence. Source and interpretation stay separate.'],
      ['EVENT','Recorded '+(b.created_at||'at an unstated time')+'. Object ID: '+b.id+'.'],
      ['BLOCK','Rendered with '+Object.keys(b.layers).length+' layers. '+(b.whyNow?('Ranked because: '+b.whyNow):'No ranking reason attached.')],
      ['STATE',(b.truth_state||'UNSTATED')+' — '+(b.truth_state==='VERIFIED'?'backed by evidence.':'not yet verified; treat accordingly.')]
    ];
    rows.forEach(r=>{
      const li=el('li',''); li.innerHTML='<strong>'+esc(r[0])+'</strong>';
      const sp=el('span','',''); sp.textContent=r[1]; li.appendChild(sp); ul.appendChild(li);
    });
    dr.appendChild(ul);
    const c=el('button','ev-close','Close evidence'); c.type='button';
    c.addEventListener('click',closeEvidence);
    dr.appendChild(c);
    bd.classList.add('open'); dr.classList.add('open'); c.focus();
  }
  function closeEvidence(){
    const dr=document.getElementById('ev-drawer'), bd=document.getElementById('ev-backdrop');
    if(dr)dr.classList.remove('open');
    if(bd)bd.classList.remove('open');
  }

  function askPanel(el){
    const p=el('div','ask-panel');
    const h=el('h3','','Ask Naya about today');
    const sub=el('p','ask-sub',''); sub.textContent='Ask in plain words. Naya searches what is actually loaded on this stage and answers only from it — nothing invented.';
    const row=el('div','ask-row');
    const input=el('input','ask-input'); input.type='text';
    input.setAttribute('aria-label','Ask Naya'); input.placeholder='What needs my attention today?';
    const go=el('button','ask-go','Ask'); go.type='button';
    const res=el('div','ask-result');
    const answer=()=>{
      const q=input.value.trim(); if(!q)return;
      res.innerHTML=''; res.classList.add('show');
      res.appendChild(askStep(el,'INTENT','You asked: “'+q+'”'));
      const hits=retrieve(q);
      const hv=el('div','ask-step');
      const hk=el('p','ask-k',''); hk.textContent='RETRIEVAL — '+hits.length+' relevant'+(hits.length===1?'':'s');
      hv.appendChild(hk);
      if(!hits.length){
        const none=el('p','ask-v',''); none.textContent='Nothing loaded on this stage matches. Naya will not invent an answer — try different words.';
        hv.appendChild(none);
      }
      hits.forEach(hit=>{
        const line=el('div','ask-hit','');
        const bb=el('button','',''); bb.type='button'; bb.textContent=hit.b.title;
        bb.addEventListener('click',()=>{ const stage=p.closest('.feed-stage'); renderNote(el,stage,hit.b); stage.scrollIntoView({block:'start'}); });
        line.appendChild(bb);
        const why=el('span','',''); why.textContent=' — '+(hit.b.whyNow||'on this stage');
        line.appendChild(why); hv.appendChild(line);
      });
      res.appendChild(hv);
      if(hits.length){
        const synth=hits.slice(0,3).map(hit=>hit.b.layers.nutshell||'').filter(Boolean).join(' ');
        res.appendChild(askStep(el,'SYNTHESIS — assembled only from the above',synth.slice(0,420)+(synth.length>420?'…':'')));
      }
      const bound=el('p','ask-boundary','');
      bound.textContent='Boundary, stated plainly: this answers from what is loaded on this stage. In production the same surface queries the governed runtime. Nothing here is sent anywhere.';
      res.appendChild(bound);
    };
    go.addEventListener('click',answer);
    input.addEventListener('keydown',e=>{if(e.key==='Enter')answer();});
    row.appendChild(input); row.appendChild(go);
    p.appendChild(h); p.appendChild(sub); p.appendChild(row); p.appendChild(res);
    return p;
  }
  function askStep(el,k,v){
    const d=el('div','ask-step');
    const kk=el('p','ask-k',''); kk.textContent=k;
    const vv=el('p','ask-v',''); vv.textContent=v;
    d.appendChild(kk); d.appendChild(vv); return d;
  }
  function retrieve(q){
    const words=q.toLowerCase().split(/[^a-z0-9]+/).filter(w=>w.length>2);
    return allItems.map(o=>{
      const hay=((o.title||'')+' '+(o.kicker||'')+' '+(o.whyNow||'')+' '+Object.keys(o.layers).map(k=>o.layers[k]).join(' ')).toLowerCase();
      let score=0; words.forEach(w=>{if(hay.includes(w))score++;});
      return {b:o,score};
    }).filter(h=>h.score>0).sort((a,b2)=>b2.score-a.score);
  }

  function esc(s){
    return String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  }

  window.NayaRooms=window.NayaRooms||{};
  window.NayaRooms.feed=FeedRoom;
})();
