/* ═══════════════════════════════════════════════════════════════════
   YOUR INTELLIGENCE TODAY — THE HIGHLIGHT REEL · v2
   Director ruling (2026-10-02): the sidebar's "Your Intelligence Today"
   is its own page — the day's hockey highlights. Scroll and see
   everything going on in your world, in-a-nutshells, quick view.
   No modes. No builder-world. No manufactured noise.

   10-star thinking — the page's real job isn't showing highlights,
   it's building tomorrow's starting lineup:
   - THE SCORELINE: the day at a glance, one quiet line.
   - THE TOP PLAYS: ranked by what changed the game. Each play: rank,
     time anchor, the announcer's call, the nutshell. Tap → the play
     opens into its full Smart Note depth.
   - CARRY FORWARD: mark the plays that deserve to survive. They
     collect into tomorrow's lineup — continuity you can touch.
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

  const carried=[];
  let allPlays=[];
  let openPlayId=null;

  function TodayRoom(){
    const {el}=window.NayaUI, K=window.NayaRoomKit;
    const stage=el('section','today-stage');
    stage.setAttribute('aria-label','Your Intelligence Today — the highlight reel');
    const line=el('div','score-line'); stage.appendChild(line);
    const river=el('div','plays-river'); stage.appendChild(river);
    const lineup=el('div','lineup'); stage.appendChild(lineup);
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
    renderScoreline(el,stage);
    renderRiver(el,stage);
    renderLineup(el,stage);
  }

  /* ——— THE SCORELINE: the day at a glance ——— */
  function renderScoreline(el,stage){
    const line=stage.querySelector('.score-line');
    line.innerHTML='';
    const n=allPlays.length;
    const tp=allPlays.filter(p=>p.turning).length;
    const s=el('p','');
    s.innerHTML='<strong>'+n+'</strong> PLAYS&nbsp;&nbsp;·&nbsp;&nbsp;<strong>'+tp+'</strong> TURNING POINT'+(tp===1?'':'S')
      +'&nbsp;&nbsp;·&nbsp;&nbsp;<strong>'+carried.length+'</strong> CARRIED FORWARD';
    line.appendChild(s);
  }

  /* ——— THE TOP PLAYS ——— */
  function renderRiver(el,stage){
    const river=stage.querySelector('.plays-river');
    river.innerHTML='';
    allPlays.forEach((p,i)=>river.appendChild(play(el,p,i)));
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

    /* The play opens into its full Smart Note depth. */
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
    carry.setAttribute('aria-label',(isOn?'Remove from tomorrow’s lineup: ':'Carry into tomorrow: ')+p.title);
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

  /* ——— TOMORROW'S LINEUP: continuity you can touch ——— */
  function renderLineup(el,stage){
    const box=stage.querySelector('.lineup');
    box.innerHTML='';
    if(!carried.length)return;
    const h=el('h3','',''); h.textContent='Tomorrow’s lineup';
    const sub=el('p','lineup-sub','');
    sub.textContent='Tomorrow’s briefing starts here — '+carried.length+' play'+(carried.length===1?'':'s')+' you chose to carry forward.';
    box.appendChild(h); box.appendChild(sub);
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
        renderAll(el,stage);
      });
      li.appendChild(dot); li.appendChild(span); li.appendChild(rm); ul.appendChild(li);
    });
    box.appendChild(ul);
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
    return {
      id:String(o.intelligent_block_id||o.id||('play-'+Math.abs(hashCode(o.title||'')))),
      title:K.title(o,'Untitled play'),
      source:srcName,
      truth_state:state,
      created_at:o.created_at||o.timestamp||o.time||'',
      when:(o.when||'').toString().toUpperCase(),
      call:o.call||'',
      turning:!!o.turning_point||!!o.turning,
      layers,
      related:Array.isArray(o.related)?o.related:[]
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
    return bits.length?bits.join(' — ')
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
    const k=el('p','ev-kicker',''); k.textContent='EVIDENCE · '+(b.truth_state||'STATE UNSTATED');
    const h=el('h3','',''); h.textContent=b.title;
    dr.appendChild(k); dr.appendChild(h);
    const ul=el('ul','ev-chain');
    [
      ['SOURCE',(b.source||'Unnamed source')+' — origin of this intelligence. Source and interpretation stay separate.'],
      ['EVENT','Recorded '+(b.created_at||'at an unstated time')+'. Object ID: '+b.id+'.'],
      ['STATE',(b.truth_state||'UNSTATED')+' — '+(b.truth_state==='VERIFIED'||b.truth_state==='CANONICAL'?'backed by evidence.':'not yet verified; treat accordingly.')]
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
