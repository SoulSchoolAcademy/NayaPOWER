/* ═══════════════════════════════════════════════════════════════════
   YOUR INTELLIGENCE TODAY — v3 · built against the Master Directive v1
   (INTELLIGENCE-TODAY-MASTER-DIRECTIVE-V1.md, repo root).

   Composition per the contract hierarchy:
   ORIENT → NOW → NEXT → WATCH → LEARNED → WAITING → REMEMBER → PROOF.

   - ORIENT: date, time-aware line (morning/midday/evening — clock-true,
     never faked personalization), the day at a glance.
   - NOW: what changed — ranked plays, biggest first. Each play: rank,
     time anchor, the announcer's call, the nutshell. Tap → full Smart
     Note depth (GLANCE → UNDERSTAND → INSPECT → PROVE).
   - NEXT: the top next move — THE primary action, verb-first, purple.
     State-driven around what the human has carried forward.
   - WATCH: plays not yet opened — derived from real interaction state,
     never manufactured.
   - LEARNED: where today climbed the ladder
     INFORMATION → UNDERSTANDING → CHANGE → DECISION → KNOWLEDGE.
   - WAITING: open loops — honest empty state when there are none.
   - REMEMBER: tomorrow's lineup — continuity the human can touch.
   - PROOF: evidence drawer per play (SOURCE → EVENT → STATE).

   Color jobs (every pixel named): magenta #d86cff signs the ROOM
   (human significance — eyebrows, scoreline, header edge); per-play
   edge tone = the object's stable identity; gold = turning points and
   carried-forward (consequence/value); purple = the primary action
   (Naya's signature). No modes. No builder-world. No manufactured noise.
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

  const RUNGS=['INFORMATION','UNDERSTANDING','CHANGE','DECISION','KNOWLEDGE'];

  const TONES=['#ff4fd8','#9d75ff','#6675ff','#55b9ee','#55e39a','#b8ee57','#f1d75a','#ff9b4a','#ff5e6c'];

  const carried=[];
  const seenPlays=new Set();
  let allPlays=[];
  let openPlayId=null;

  function TodayRoom(){
    const {el}=window.NayaUI, K=window.NayaRoomKit;
    const stage=el('section','today-stage');
    stage.setAttribute('aria-label','Your Intelligence Today — the highlight reel');
    stage.appendChild(evDrawer(el));

    K.load(stage,'today',{date:new Date().toISOString().slice(0,10)},(payload,list,out)=>{
      const hl=payload&&Array.isArray(payload.highlights)?payload.highlights:[];
      const raw=hl.length?hl:list;
      allPlays=(raw||[]).map(o=>normalize(o,K));
      renderAll(el,out);
    },{
      title:'A quiet day can stay quiet',
      body:'No verified highlight was manufactured just to fill the page.'
    });
    return stage;
  }

  function renderAll(el,stage){
    const drawer=stage.querySelector('.ev-wrap');
    stage.innerHTML='';
    if(drawer)stage.appendChild(drawer);
    stage.appendChild(orient(el));
    stage.appendChild(section(el,'NOW','What changed',nowRiver(el)));
    stage.appendChild(section(el,'NEXT','Your top next move',nextCard(el)));
    stage.appendChild(section(el,'WATCH','Still unopened',watchList(el)));
    stage.appendChild(section(el,'LEARNED','What today taught',learnedList(el)));
    stage.appendChild(section(el,'WAITING','Open loops',waitingList(el)));
    const lineup=rememberLineup(el);
    if(lineup)stage.appendChild(section(el,'REMEMBER','Tomorrow\u2019s lineup',lineup));
  }

  function section(el,eyebrow,title,body){
    const s=el('section','tsection');
    const h=el('div','tsection-head');
    const e=el('p','tsection-eyebrow',''); e.textContent=eyebrow;
    const t=el('h2','tsection-title',''); t.textContent=title;
    h.appendChild(e); h.appendChild(t);
    s.appendChild(h); s.appendChild(body);
    return s;
  }

  /* ——— ORIENT: the day at a glance ——— */
  function orient(el){
    const o=el('div','orient');
    const now=new Date(), h=now.getHours();
    const line=h>=5&&h<11
      ?'Good morning. Today\u2019s intelligence is still arriving \u2014 here\u2019s what\u2019s here so far.'
      :h>=11&&h<17
      ?'Good afternoon. Here\u2019s what today holds so far.'
      :h>=17&&h<22
      ?'Good evening. Here\u2019s what today became.'
      :'Late night. Here\u2019s today, distilled.';
    const d=el('p','orient-date','');
    d.textContent=now.toLocaleDateString(undefined,{weekday:'long',year:'numeric',month:'long',day:'numeric'});
    const l=el('p','orient-line',''); l.textContent=line;
    o.appendChild(d); o.appendChild(l);

    const n=allPlays.length;
    const tp=allPlays.filter(p=>p.turning).length;
    const s=el('p','score-line');
    s.innerHTML='<strong>'+n+'</strong> PLAYS&nbsp;&nbsp;\u00B7&nbsp;&nbsp;<strong>'+tp+'</strong> TURNING POINT'+(tp===1?'':'S')
      +'&nbsp;&nbsp;\u00B7&nbsp;&nbsp;<strong>'+carried.length+'</strong> CARRIED FORWARD';
    o.appendChild(s);
    return o;
  }

  /* ——— NOW: what changed ——— */
  function nowRiver(el){
    const river=el('div','plays-river');
    allPlays.forEach((p,i)=>river.appendChild(play(el,p,i)));
    return river;
  }

  function play(el,p,rank){
    const a=el('article','play'+(p.turning?' play-turning':''));
    a.id='play-'+p.id;
    a.style.setProperty('--tone',toneFor(p));

    const brow=el('div','play-brow');
    const rankEl=el('span','play-rank',''); rankEl.textContent=String(rank+1).padStart(2,'0');
    const when=el('span','play-when',''); when.textContent=p.when||'TODAY';
    brow.appendChild(rankEl); brow.appendChild(when);
    if(p.turning){
      const tag=el('span','play-turning-tag',''); tag.textContent='TURNING POINT';
      brow.appendChild(tag);
    }
    a.appendChild(brow);

    const t=el('h2','play-title',''); t.textContent=p.title;
    a.appendChild(t);
    if(p.call){
      const c=el('p','play-call',''); c.textContent=p.call;
      a.appendChild(c);
    }
    if(p.layers.nutshell){
      const n=el('p','play-nut',''); n.textContent=p.layers.nutshell;
      a.appendChild(n);
    }

    const opened=p.id===openPlayId;
    if(opened){
      const deep=el('div','play-depth');
      LAYERS.forEach(([key])=>{
        if(key!=='nutshell'&&p.layers[key]) deep.appendChild(makeLayer(el,key,p.layers[key]));
      });
      const tools=el('div','play-tools');
      const ev=el('button','play-tool','Evidence'); ev.type='button';
      ev.addEventListener('click',e2=>{e2.stopPropagation();openEvidence(p);});
      tools.appendChild(ev);
      deep.appendChild(tools);
      a.appendChild(deep);
    }

    const foot=el('div','play-foot');
    const isOn=carried.includes(p.id);
    const carry=el('button','carry-toggle'+(isOn?' on':''),'');
    carry.type='button';
    carry.setAttribute('aria-pressed',isOn?'true':'false');
    carry.setAttribute('aria-label',(isOn?'Remove from tomorrow\u2019s lineup: ':'Carry into tomorrow: ')+p.title);
    const dot=el('span','carry-dot',''); carry.appendChild(dot);
    const clab=el('span','',''); clab.textContent=isOn?'Carried forward':'Carry forward';
    carry.appendChild(clab);
    carry.addEventListener('click',e2=>{
      e2.stopPropagation();
      const ix=carried.indexOf(p.id);
      if(ix>=0)carried.splice(ix,1); else carried.push(p.id);
      const stage=a.closest('.today-stage');
      renderAll(el,stage);
    });
    foot.appendChild(carry);
    const hint=el('span','play-hint',''); hint.textContent=opened?'Close':'Open the note';
    foot.appendChild(hint);
    a.appendChild(foot);

    const toggle=()=>{
      openPlayId=opened?null:p.id;
      if(!opened)seenPlays.add(p.id);
      const stage=a.closest('.today-stage');
      renderAll(el,stage);
      if(!opened){
        const t2=document.getElementById('play-'+CSS.escape(p.id));
        if(t2)t2.scrollIntoView({block:'nearest',behavior:'smooth'});
      }
    };
    a.setAttribute('tabindex','0'); a.setAttribute('role','button');
    a.setAttribute('aria-expanded',opened?'true':'false');
    a.setAttribute('aria-label',(opened?'Close ':'Open ')+p.title);
    a.addEventListener('click',toggle);
    a.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();toggle();}});
    return a;
  }

  /* ——— NEXT: the top next move — the primary action ——— */
  function nextCard(el){
    const card=el('div','next-card');
    const n=carried.length;
    const t=el('h3','');
    const b=el('p','next-body','');
    const btn=el('button','next-action',''); btn.type='button';
    if(n===0){
      t.textContent='Decide what today means';
      b.textContent='Nothing is carried forward yet. Mark the plays worth remembering \u2014 tomorrow\u2019s briefing starts with your call.';
      btn.textContent='Choose the first play';
      btn.addEventListener('click',()=>{
        const first=document.getElementById('play-'+CSS.escape(allPlays[0].id));
        if(first){first.scrollIntoView({block:'center',behavior:'smooth'});first.focus({preventScroll:true});}
      });
    }else{
      t.textContent='Tomorrow\u2019s briefing is taking shape';
      b.textContent=n+' play'+(n===1?'':'s')+' carried forward. Review the lineup before the day ends.';
      btn.textContent='Review tomorrow\u2019s lineup';
      btn.addEventListener('click',()=>{
        const lu=document.querySelector('.lineup');
        if(lu)lu.scrollIntoView({block:'center',behavior:'smooth'});
      });
    }
    card.appendChild(t); card.appendChild(b); card.appendChild(btn);
    return card;
  }

  /* ——— WATCH: still unopened — derived from real state ——— */
  function watchList(el){
    const wrap=el('div','watch-list');
    const unseen=allPlays.filter(p=>!seenPlays.has(p.id));
    if(!unseen.length){
      const q=el('p','quiet-note','');
      q.textContent='You\u2019ve opened every play. Nothing is waiting on your attention.';
      wrap.appendChild(q); return wrap;
    }
    const ul=el('ul','');
    unseen.forEach(p=>{
      const li=el('li','');
      const dot=el('span','watch-dot',''); dot.style.setProperty('--tone',toneFor(p));
      const span=el('span','',''); span.textContent=p.title;
      const open=el('button','','Open'); open.type='button';
      open.setAttribute('aria-label','Open: '+p.title);
      open.addEventListener('click',()=>{
        openPlayId=p.id; seenPlays.add(p.id);
        const stage=wrap.closest('.today-stage');
        renderAll(el,stage);
        const t2=document.getElementById('play-'+CSS.escape(p.id));
        if(t2)t2.scrollIntoView({block:'center',behavior:'smooth'});
      });
      li.appendChild(dot); li.appendChild(span); li.appendChild(open); ul.appendChild(li);
    });
    wrap.appendChild(ul);
    return wrap;
  }

  /* ——— LEARNED: where today climbed the ladder ——— */
  function learnedList(el){
    const wrap=el('div','learned-list');
    const items=allPlays.filter(p=>p.rung);
    if(!items.length){
      const q=el('p','quiet-note','');
      q.textContent='Nothing has been marked as learned yet today.';
      wrap.appendChild(q); return wrap;
    }
    const ul=el('ul','');
    items.forEach(p=>{
      const li=el('li','');
      const rung=el('span','rung-tag',''); rung.textContent=p.rung;
      const span=el('span','',''); span.textContent=p.title;
      li.appendChild(rung); li.appendChild(span); ul.appendChild(li);
    });
    wrap.appendChild(ul);
    return wrap;
  }

  /* ——— WAITING: open loops — honest when empty ——— */
  function waitingList(el){
    const wrap=el('div','waiting-list');
    const items=allPlays.filter(p=>Array.isArray(p.waiting)&&p.waiting.length);
    if(!items.length){
      const q=el('p','quiet-note','');
      q.textContent='Nothing is waiting on you. A quiet day can stay quiet.';
      wrap.appendChild(q); return wrap;
    }
    const ul=el('ul','');
    items.forEach(p=>p.waiting.forEach(w=>{
      const li=el('li','');
      const span=el('span','',''); span.textContent=w;
      const src=el('span','waiting-src',''); src.textContent=p.title;
      li.appendChild(span); li.appendChild(src); ul.appendChild(li);
    }));
    wrap.appendChild(ul);
    return wrap;
  }

  /* ——— REMEMBER: tomorrow's lineup ——— */
  function rememberLineup(el){
    if(!carried.length)return null;
    const box=el('div','lineup');
    const sub=el('p','lineup-sub','');
    sub.textContent='Tomorrow\u2019s briefing starts here \u2014 '+carried.length+' play'+(carried.length===1?'':'s')+' you chose to carry forward.';
    box.appendChild(sub);
    const ul=el('ul','');
    carried.forEach(id=>{
      const p=allPlays.find(x=>x.id===id); if(!p)return;
      const li=el('li','');
      const dot=el('span','lineup-dot',''); dot.style.setProperty('--tone',toneFor(p));
      const span=el('span','',''); span.textContent=p.title;
      const rm=el('button','','Remove'); rm.type='button';
      rm.setAttribute('aria-label','Remove from lineup: '+p.title);
      rm.addEventListener('click',()=>{
        const ix=carried.indexOf(id); if(ix>=0)carried.splice(ix,1);
        const stage=box.closest('.today-stage');
        renderAll(el,stage);
      });
      li.appendChild(dot); li.appendChild(span); li.appendChild(rm); ul.appendChild(li);
    });
    box.appendChild(ul);
    return box;
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
    const state=(o.truth_state||o.state||'').toString().toUpperCase();
    const srcName=typeof o.source==='string'?o.source:(o.source&&o.source.name)||'';
    const rung=(o.rung||'').toString().toUpperCase();
    return {
      id:String(o.intelligent_block_id||o.id||('play-'+Math.abs(hashCode(o.title||'')))),
      title:K.title(o,'Untitled play'),
      source:srcName,
      truth_state:state,
      created_at:o.created_at||o.timestamp||o.time||'',
      when:(o.when||'').toString().toUpperCase(),
      call:o.call||'',
      turning:!!o.turning_point||!!o.turning,
      rung:RUNGS.includes(rung)?rung:'',
      waiting:Array.isArray(o.waiting)?o.waiting.filter(w=>typeof w==='string'&&w.trim()):[],
      layers
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
    return bits.length?bits.join(' \u2014 ')
      :'No provenance is attached to this object, so no evidence boundary can be stated.';
  }

  function evDrawer(el){
    const wrap=el('div','ev-wrap','');
    const bd=el('div','ev-backdrop',''); bd.id='ev-backdrop-today';
    const dr=el('aside','ev-drawer',''); dr.id='ev-drawer-today';
    dr.setAttribute('aria-label','Evidence'); dr.setAttribute('role','dialog'); dr.setAttribute('aria-modal','true');
    bd.addEventListener('click',closeEvidence);
    wrap.appendChild(bd); wrap.appendChild(dr);
    return wrap;
  }
  function openEvidence(b){
    const {el}=window.NayaUI;
    const dr=document.getElementById('ev-drawer-today'), bd=document.getElementById('ev-backdrop-today');
    if(!dr||!bd)return;
    dr.innerHTML='';
    const k=el('p','ev-kicker',''); k.textContent='EVIDENCE \u00B7 '+(b.truth_state||'STATE UNSTATED');
    const h=el('h3','',''); h.textContent=b.title;
    dr.appendChild(k); dr.appendChild(h);
    const ul=el('ul','ev-chain');
    [
      ['SOURCE',(b.source||'Unnamed source')+' \u2014 origin of this intelligence. Source and interpretation stay separate.'],
      ['EVENT','Recorded '+(b.created_at||'at an unstated time')+'. Object ID: '+b.id+'.'],
      ['STATE',(b.truth_state||'UNSTATED')+' \u2014 '+(b.truth_state==='VERIFIED'||b.truth_state==='CANONICAL'?'backed by evidence.':'not yet verified; treat accordingly.')]
    ].forEach(r=>{
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
    const dr=document.getElementById('ev-drawer-today'), bd=document.getElementById('ev-backdrop-today');
    if(dr)dr.classList.remove('open');
    if(bd)bd.classList.remove('open');
  }

  function esc(s){
    return String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  }

  window.NayaRooms=window.NayaRooms||{};
  window.NayaRooms.today=TodayRoom;
})();
