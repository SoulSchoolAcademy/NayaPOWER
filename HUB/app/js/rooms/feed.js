/* ═══════════════════════════════════════════════════════════════════
   ROOM 01 — SMART FEED · THE MAIN STAGE
   Rebuilt 2026-10-02 per the director's call. The main stage shows
   "your intelligence today" as intelligent blocks in the V7 language:
   jewel · title · kicker · source · nutshell · deeper layers · trust footer.
   No mode tabs, no spec-speak buttons, no invented content — every layer
   comes from the object's real fields or is honestly derived.
   ═══════════════════════════════════════════════════════════════════ */
(function(){
  'use strict';

  /* The V7 layer order. Nutshell is always visible; the rest live behind
     "Go deeper" and only render when the object actually carries them —
     except MACHINE NOTE, which is honestly derived from provenance facts. */
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

  /* The Smart Feed glyph: white wave-lines, geometric, 40% of diameter,
     centered — set by the specimen V1. The orb itself is CSS anatomy. */
  /* The V7 tone flow: each board takes the next tone in sequence.
     Pink → purple → indigo → blue → green → lime → yellow → orange → red,
     then it cycles. One color, one block — never monochrome wallpaper. */
  const TONES=['#ff4fd8','#9d75ff','#6675ff','#55b9ee','#55e39a','#b8ee57','#f1d75a','#ff9b4a','#ff5e6c'];

  const JEWEL='<svg viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2.2" stroke-linecap="round" aria-hidden="true">'
    +'<path d="M4 8.5c2.6-2.6 5.4-2.6 8 0s5.4 2.6 8 0"/>'
    +'<path d="M4 13.5c2.6-2.6 5.4-2.6 8 0s5.4 2.6 8 0"/>'
    +'<path d="M4 18.5c2.6-2.6 5.4-2.6 8 0s5.4 2.6 8 0"/></svg>';

  function FeedRoom(){
    const {el}=window.NayaUI, K=window.NayaRoomKit;
    const stage=el('section','feed-stage');
    stage.setAttribute('aria-label','Smart Feed — your intelligence today');
    stage.appendChild(greeting(el));
    const zone=el('div','feed-blocks');
    stage.appendChild(zone);
    const foot=el('div','feed-stage-foot');
    const ask=el('button','feed-ask','<span>Ask Naya about today</span>');
    ask.type='button';
    ask.addEventListener('click',()=>{
      window.NayaUI.toast('Ask Naya about today — the governed ask seam lands here. Nothing is answered from thin air.', '#f8f7fb');
    });
    foot.appendChild(ask);
    stage.appendChild(foot);

    K.load(zone,'feed',{limit:25},(payload,list,out)=>{
      out.appendChild(countLine(el,K,list.length));
      list.forEach((o,i)=>out.appendChild(block(el,K,normalize(o,K),i,i===0)));
    },{
      title:'The stage is quiet',
      body:'There is no qualifying intelligence right now. When something matters, it appears here — ordered for you, never manufactured to fill the space.'
    });
    return stage;
  }

  /* ——— Stage header ——— */
  function greeting(el){
    const h=new Date().getHours();
    const part=h<12?'Good morning':h<18?'Good afternoon':'Good evening';
    const who=(window.NayaRuntime&&window.NayaRuntime.user&&window.NayaRuntime.user.name)||'Shawn';
    const date=new Date().toLocaleDateString('en-US',{weekday:'long',month:'long',day:'numeric'});
    const wrap=el('header','feed-stage-head');
    const g=el('h1','feed-greeting',''); g.textContent=part+', '+who;
    const d=el('p','feed-dateline','');
    d.innerHTML='<span>'+esc(date.toUpperCase())+'</span><span class="feed-dot">·</span><span>YOUR INTELLIGENCE TODAY</span>';
    const s=el('p','feed-daystate','');
    s.textContent='Here is what changed, what matters, and what needs you — ordered for you, in the open, with the evidence attached.';
    wrap.appendChild(g); wrap.appendChild(d); wrap.appendChild(s);
    return wrap;
  }

  function countLine(el,K,n){
    const p=el('p','feed-countline','');
    p.innerHTML='<strong>'+K.safe(String(n))+'</strong>&nbsp;&nbsp;INTELLIGENCE BLOCK'+(n===1?'':'S');
    return p;
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
      title:K.title(o,'Untitled intelligence'),
      kicker:[type||'INTELLIGENCE', state||null].filter(Boolean).join(' · '),
      source:srcName,
      layers,
      action:(act&&(act.label||act.verb))?{label:act.label||act.verb,run:act.run||null}:null
    };
  }

  /* MACHINE NOTE is derived from provenance facts, never invented. */
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

  /* ——— Block renderer ——— */
  function block(el,K,b,idx,lead){
    const a=el('article','iblock'+(lead?' iblock-lead':''));
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

    /* Nutshell — always visible. */
    if(b.layers.nutshell) a.appendChild(makeLayer(el,'ilayer-nutshell','nutshell',b.layers.nutshell));

    /* Deeper layers — behind an honest toggle, only if any exist. */
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

    if(b.action){
      const aw=el('div','iblock-action');
      const btn=el('button','feed-btn',''); btn.type='button'; btn.textContent=b.action.label;
      btn.addEventListener('click',()=>{
        if(typeof b.action.run==='function'){ b.action.run(); return; }
        window.NayaUI.toast('This action runs through the governed runtime — never from the feed alone.', '#f8f7fb');
      });
      aw.appendChild(btn); a.appendChild(aw);
    }

    const foot=el('footer','iblock-foot');
    foot.innerHTML='<p>ONE INTELLIGENCE · MANY VIEWS · ONE IDENTITY</p>'
      +'<p>TRUST: <span class="trust">SOURCE / INTERPRETATION SEPARATED</span></p>';
    a.appendChild(foot);
    return a;
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

  function esc(s){
    return String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  }

  window.NayaRooms=window.NayaRooms||{};
  window.NayaRooms.feed=FeedRoom;
})();
