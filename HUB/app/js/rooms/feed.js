/* ═══════════════════════════════════════════════════════════════════
   ROOM 01 — SMART FEED · THE MAIN SHOW · v4
   Per the binding design law (Ultimate Contract, PR #1331, §8.2 / §14B.2):
   Presence → recognition → the river (ONE hero region, the rest
   subordinate) → the mode dock (Collective / Personal / Activity, ONE
   sticky zone) → Ask Naya. Full-bleed scroll. Distilled content. No KPI
   wall. No dashboard grid. No navigation wall before the intelligence.
   The river shows snapshots — the in-a-nutshell of each smart node for
   the day. Depth (why-now, layers, action, refs, evidence) opens on tap.
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

  const JEWEL='<svg viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2.2" stroke-linecap="round" aria-hidden="true">'
    +'<path d="M4 8.5c2.6-2.6 5.4-2.6 8 0s5.4 2.6 8 0"/>'
    +'<path d="M4 13.5c2.6-2.6 5.4-2.6 8 0s5.4 2.6 8 0"/>'
    +'<path d="M4 18.5c2.6-2.6 5.4-2.6 8 0s5.4 2.6 8 0"/></svg>';

  const MODES=[
    {id:'personal',label:'Personal'},
    {id:'collective',label:'Collective'},
    {id:'activity',label:'Activity'}
  ];

  const savedList=[];
  const decisions={};
  let allItems=[];
  let currentMode='personal';
  let expandedId=null;

  function FeedRoom(){
    const {el}=window.NayaUI, K=window.NayaRoomKit;
    const stage=el('section','feed-stage');
    stage.setAttribute('aria-label','Smart Feed — the Main Show');
    stage.appendChild(greeting(el));
    const heroZone=el('div','feed-hero'); stage.appendChild(heroZone);
    stage.appendChild(modeDock(el));
    const river=el('div','feed-river'); stage.appendChild(river);
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
      renderShow(el,stage);
    },{
      title:'The stage is quiet',
      body:'There is no qualifying intelligence right now. When something matters, it appears here — ordered for you, never manufactured to fill the space.'
    });
    return stage;
  }

  /* ——— Presence → recognition. Quiet. No navigation wall. ——— */
  function greeting(el){
    const h=new Date().getHours();
    const part=h<12?'Good morning':h<18?'Good afternoon':'Good evening';
    const who=(window.NayaRuntime&&window.NayaRuntime.user&&window.NayaRuntime.user.name)||'';
    const date=new Date().toLocaleDateString('en-US',{weekday:'long',month:'long',day:'numeric'});
    const wrap=el('header','feed-stage-head');
    const g=el('h1','feed-greeting',''); g.textContent=who?part+', '+who:part;
    const d=el('p','feed-dateline','');
    d.innerHTML='<span>'+esc(date.toUpperCase())+'</span><span class="feed-dot">·</span><span>YOUR INTELLIGENCE TODAY</span>';
    wrap.appendChild(g); wrap.appendChild(d);
    return wrap;
  }

  /* ——— ONE sticky mode zone, under the top bar ——— */
  function modeDock(el){
    const dock=el('div','feed-modedock');
    dock.setAttribute('role','tablist'); dock.setAttribute('aria-label','Feed mode');
    MODES.forEach((m,i)=>{
      const b=el('button','feed-mode',''); b.type='button'; b.textContent=m.label;
      b.setAttribute('role','tab'); b.setAttribute('aria-selected',i===0?'true':'false');
      b.dataset.mode=m.id;
      b.addEventListener('click',()=>{
        dock.querySelectorAll('.feed-mode').forEach(x=>x.setAttribute('aria-selected','false'));
        b.setAttribute('aria-selected','true');
        currentMode=m.id; expandedId=null;
        const stage=dock.closest('.feed-stage');
        renderShow(el,stage);
        stage.scrollIntoView({block:'start'});
      });
      dock.appendChild(b);
    });
    return dock;
  }

  /* ——— The show: one hero, the rest subordinate snapshots ——— */
  function renderShow(el,stage){
    const items=allItems.filter(o=>modeOf(o)===currentMode);
    const heroZone=stage.querySelector('.feed-hero');
    const river=stage.querySelector('.feed-river');
    heroZone.innerHTML=''; river.innerHTML='';
    if(!items.length){
      const p=el('p','feed-daystate','');
      p.textContent='Nothing in this stream right now. When something matters, it appears here — never manufactured to fill the space.';
      river.appendChild(p); return;
    }
    const [hero,...rest]=items;
    heroZone.appendChild(block(el,hero,0,true));
    if(rest.length){
      const k=el('p','river-kicker','');
      k.innerHTML='<span>'+rest.length+'</span>&nbsp;&nbsp;MORE TODAY';
      river.appendChild(k);
      rest.forEach((b,i)=>{
        if(b.id===expandedId) river.appendChild(expandedBlock(el,b,i+1));
        else river.appendChild(snapshot(el,b,i+1));
      });
    }
  }

  /* Subordinate snapshot: the in-a-nutshell of the node. One calm line. */
  function snapshot(el,b,idx){
    const s=el('button','snap',''); s.type='button';
    s.style.setProperty('--tone',TONES[idx%TONES.length]);
    s.setAttribute('aria-expanded','false');
    s.innerHTML='<span class="snap-dot" aria-hidden="true"></span>'
      +'<span class="snap-main"><span class="snap-title">'+esc(b.title)+'</span>'
      +'<span class="snap-nut">'+esc(b.layers.nutshell||'')+'</span></span>'
      +'<span class="snap-chev" aria-hidden="true">▾</span>';
    s.setAttribute('aria-label','Open: '+b.title);
    s.addEventListener('click',()=>{
      expandedId=b.id;
      const stage=s.closest('.feed-stage');
      renderShow(el,stage);
      const t=stage.querySelector('#block-'+CSS.escape(b.id));
      if(t){t.scrollIntoView({behavior:'smooth',block:'center'});}
    });
    return s;
  }

  function expandedBlock(el,b,idx){
    const wrap=el('div','snap-open');
    wrap.appendChild(block(el,b,idx,false));
    const less=el('button','snap-less',''); less.type='button';
    less.innerHTML='<span>Show less</span><span class="chev">▴</span>';
    less.addEventListener('click',()=>{
      expandedId=null;
      const stage=wrap.closest('.feed-stage');
      renderShow(el,stage);
    });
    wrap.appendChild(less);
    return wrap;
  }

  function modeOf(b){
    const m=(b.mode||'personal').toLowerCase();
    return MODES.some(x=>x.id===m)?m:'personal';
  }

  /* ——— Object → block. Only real fields; nothing invented. ——— */
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
    const act=o.action||o.primary_action||null;
    return {
      id:String(o.intelligent_block_id||o.id||type+'-'+Math.abs(hashCode(o.title||''))),
      mode:o.mode||o.stream||'personal',
      title:K.title(o,'Untitled intelligence'),
      kicker:[type||'INTELLIGENCE', state||null].filter(Boolean).join(' · '),
      source:srcName,
      truth_state:state,
      created_at:o.created_at||o.timestamp||o.time||'',
      whyNow:o.why_now||o.whyNow||'',
      layers,
      related:Array.isArray(o.related)?o.related:[],
      people:Array.isArray(o.people)?o.people:[],
      context:o.context||null,
      action:(act&&(act.label||act.verb))?{label:act.label||act.verb,kind:act.kind||'evidence',run:act.run||null}:null
    };
  }

  function hashCode(s){let h=0;for(let i=0;i<s.length;i++){h=(h*31+s.charCodeAt(i))|0;}return h;}

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

  /* ——— Full block: hero or expanded snapshot. Depth lives here, on demand. ——— */
  function block(el,b,idx,lead){
    const a=el('article','iblock'+(lead?' iblock-lead':''));
    a.id='block-'+b.id;
    a.style.setProperty('--tone', TONES[idx % TONES.length]);
    const head=el('div','iblock-head');
    const jewel=el('div','iblock-jewel'); jewel.innerHTML=JEWEL;
    const htext=el('div','iblock-htext');
    const t=el('h2','iblock-title',''); t.textContent=b.title;
    const k=el('p','iblock-kicker','');
    const kickerParts=b.kicker.split(' · ');
    k.innerHTML='<span>'+esc(kickerParts[0]||'INTELLIGENCE')+'</span>'
      +(kickerParts[1]?' <span class="k-accent">· '+esc(kickerParts[1])+'</span>':'');
    htext.appendChild(t); htext.appendChild(k);
    if(b.source){
      const s=el('p','iblock-source','');
      s.innerHTML='<span class="led"></span><span>SOURCE SEPARATED — '+esc(b.source.toUpperCase())+'</span>';
      htext.appendChild(s);
    }
    head.appendChild(jewel); head.appendChild(htext);
    a.appendChild(head);

    if(b.whyNow){
      const w=el('p','iblock-whynow','');
      w.innerHTML='<strong>WHY NOW</strong><span>'+esc(b.whyNow)+'</span>';
      a.appendChild(w);
    }

    if(b.layers.nutshell) a.appendChild(makeLayer(el,'ilayer-nutshell','nutshell',b.layers.nutshell));

    const deepKeys=LAYERS.map(l=>l[0]).filter(k2=>k2!=='nutshell'&&b.layers[k2]);
    if(deepKeys.length){
      const deeper=el('button','feed-deeper','');
      deeper.type='button';
      deeper.setAttribute('aria-expanded','false');
      deeper.innerHTML='<span>Go deeper</span><span class="chev">▾</span>';
      const layersEl=el('div','iblock-layers');
      deepKeys.forEach(k2=>layersEl.appendChild(makeLayer(el,'',k2,b.layers[k2])));
      deeper.addEventListener('click',()=>{
        const open=layersEl.classList.toggle('open');
        deeper.setAttribute('aria-expanded',open?'true':'false');
        deeper.querySelector('span').textContent=open?'Go shallower':'Go deeper';
      });
      a.appendChild(deeper);
      a.appendChild(layersEl);
    }

    /* The one obvious action — real behavior, never a toast. */
    const aw=el('div','iblock-actionrow');
    const acted=decisions[b.id];
    const btn=el('button','feed-btn primary',''); btn.type='button';
    const label=(b.action&&b.action.label)||'Open the proof';
    btn.textContent=acted?('Decided: '+acted.choice):label;
    if(acted) btn.disabled=true;
    btn.addEventListener('click',()=>runAction(el,b,btn,aw));
    aw.appendChild(btn);
    const note=el('span','iblock-decision','');
    if(acted) note.textContent='Recorded '+acted.at+' — preview-local receipt.';
    aw.appendChild(note);
    a.appendChild(aw);

    /* Cross-references — the identity becomes navigable. */
    const refs=el('div','iblock-refs');
    refs.appendChild(refBtn(el,'Source note',()=>openEvidence(b)));
    refs.appendChild(refBtn(el,'Evidence',()=>openEvidence(b)));
    b.related.forEach(rid=>{
      const target=allItems.find(x=>x.id===String(rid));
      if(target) refs.appendChild(refBtn(el,'Related: '+shortTitle(target.title),()=>{
        const prev=currentMode, pm=modeOf(target);
        const finish=()=>jumpTo(target.id);
        if(pm!==prev){
          currentMode=pm; expandedId=target.id;
          const stage=a.closest('.feed-stage');
          stage.querySelectorAll('.feed-mode').forEach(x=>x.setAttribute('aria-selected',x.dataset.mode===pm?'true':'false'));
          renderShow(el,stage); finish();
        }else{ expandedId=target.id; const stage=a.closest('.feed-stage'); renderShow(el,stage); finish(); }
      }));
    });
    b.people.forEach(pn=>{
      const c=el('span','iblock-ref','');
      c.innerHTML='Person: <span class="who">'+esc(pn)+'</span>';
      c.title='Named in this intelligence. Profiles are not fabricated.';
      refs.appendChild(c);
    });
    const ctx=b.context||{};
    ['list','space','report'].forEach(kk=>{
      if(ctx[kk]){
        const c2=el('span','iblock-ref','');
        c2.innerHTML=esc(kk.charAt(0).toUpperCase()+kk.slice(1))+': <span class="who">'+esc(ctx[kk])+'</span>';
        c2.title='Canonical '+kk+' — resolves to the real object in production.';
        refs.appendChild(c2);
      }
    });
    if(ctx.prior){const pr=el('span','iblock-ref','');pr.innerHTML='Prior: <span class="who">'+esc(ctx.prior)+'</span>';refs.appendChild(pr);}
    if(ctx.next){const nx=el('span','iblock-ref','');nx.innerHTML='Next: <span class="who">'+esc(ctx.next)+'</span>';refs.appendChild(nx);}
    a.appendChild(refs);

    const foot=el('footer','iblock-foot');
    foot.innerHTML='<p>ONE INTELLIGENCE · MANY VIEWS · ONE IDENTITY</p>'
      +'<p>TRUST: <span class="trust">SOURCE / INTERPRETATION SEPARATED</span></p>';
    a.appendChild(foot);
    return a;
  }

  function shortTitle(t){t=String(t||'');return t.length>26?t.slice(0,26)+'…':t;}
  function refBtn(el,label,fn){const b=el('button','iblock-ref','');b.type='button';b.textContent=label;b.addEventListener('click',fn);return b;}
  function jumpTo(rid){
    const sel='#block-'+CSS.escape(rid);
    const t=document.querySelector(sel);
    if(t){t.scrollIntoView({behavior:'smooth',block:'center'});t.classList.remove('flash');void t.offsetWidth;t.classList.add('flash');}
  }

  function makeLayer(el,cls,key,text){
    const found=LAYERS.find(l=>l[0]===key);
    const label=found?found[1]:key.toUpperCase();
    const sub=found?found[2]:'';
    const d=el('div','ilayer '+cls);
    const lab=el('p','ilayer-label','');
    lab.innerHTML='<strong>'+esc(label)+'</strong>'+(sub?'<span>'+esc(sub)+'</span>':'');
    const txt=el('p','ilayer-text',''); txt.textContent=text;
    d.appendChild(lab); d.appendChild(txt);
    return d;
  }

  function runAction(el,b,btn,row){
    const kind=(b.action&&b.action.kind)||'evidence';
    if(typeof (b.action&&b.action.run)==='function'){ b.action.run(); return; }
    if(kind==='decide'){
      decisions[b.id]={choice:'APPROVED',at:new Date().toLocaleTimeString('en-US',{hour:'numeric',minute:'2-digit'})};
      btn.textContent='Decided: APPROVED'; btn.disabled=true;
      const note=row.querySelector('.iblock-decision');
      if(note)note.textContent='Recorded '+decisions[b.id].at+' — preview-local receipt. Production writes a governed ledger receipt.';
    }else if(kind==='ask'){
      const panel=document.querySelector('.ask-panel');
      if(panel){panel.classList.add('open');
        const i=panel.querySelector('.ask-input');
        if(i){i.value='About "'+b.title+'": ';i.focus();}}
      const foot=document.querySelector('.feed-stage-foot');
      if(foot)foot.scrollIntoView({behavior:'smooth',block:'center'});
    }else if(kind==='save'){
      if(!savedList.includes(b.id))savedList.push(b.id);
      btn.textContent='Saved to Today’s list'; btn.disabled=true;
      renderTodayList();
    }else{
      openEvidence(b);
    }
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
      const hk=el('p','ask-k',''); hk.textContent='RETRIEVAL — '+hits.length+' relevant block'+(hits.length===1?'':'s');
      hv.appendChild(hk);
      if(!hits.length){
        const none=el('p','ask-v',''); none.textContent='Nothing loaded on this stage matches. Naya will not invent an answer — try different words, or switch mode.';
        hv.appendChild(none);
      }
      hits.forEach(hit=>{
        const line=el('div','ask-hit','');
        const bb=el('button','',''); bb.type='button'; bb.textContent=hit.b.title;
        bb.addEventListener('click',()=>{
          const pm=modeOf(hit.b);
          if(pm!==currentMode){
            currentMode=pm; expandedId=hit.b.id;
            const stage=p.closest('.feed-stage');
            stage.querySelectorAll('.feed-mode').forEach(x=>x.setAttribute('aria-selected',x.dataset.mode===pm?'true':'false'));
            renderShow(el,stage);
          }else{ expandedId=hit.b.id; renderShow(el,p.closest('.feed-stage')); }
          jumpTo(hit.b.id);
        });
        line.appendChild(bb);
        const why=el('span','',''); why.textContent=' — '+(hit.b.whyNow||'on this stage');
        line.appendChild(why); hv.appendChild(line);
      });
      res.appendChild(hv);
      if(hits.length){
        const synth=hits.slice(0,3).map(hit=>hit.b.layers.nutshell||'').filter(Boolean).join(' ');
        res.appendChild(askStep(el,'SYNTHESIS — assembled only from the blocks above',synth.slice(0,420)+(synth.length>420?'…':'')));
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
