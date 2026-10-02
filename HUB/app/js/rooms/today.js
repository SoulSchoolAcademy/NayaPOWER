/* ═══════════════════════════════════════════════════════════════════
   YOUR INTELLIGENCE TODAY — v8 · smart tabs
   Director's ruling (2026-10-02): "the same visual language, the same
   style, the same look. If you're going to change it, then you have to
   change everything."

   Every play is a .block.naya509-board — the reference board anatomy,
   quoted verbatim and scoped to this room: blockTop (glyph + title +
   meta) → the nutshell box →
   the full ten-layer intelligent block (on open) → actions →
   blockFoot. Opening a play renders the SAME intelligent-block
   language as the main page — not a second presentation.

   Composition: ORIENT → TABS → SEARCH → NOW → WATCH → WAITING → REMEMBER.
   The ranking IS the intelligence (#1 wears TOP INTELLIGENCE).
   Actions: SAVE keeps it (the Smart List), SHARE sends it (native
   sheet, clipboard fallback). Proof lives in the opened layers.
   No manufactured actions. No modes.
   ═══════════════════════════════════════════════════════════════════ */
(function(){
  'use strict';

  /* The intelligent-block layers, in reference order. The nutshell is
     shown in its own box above; the open state renders the rest. */
  const LAYERS=[
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

  /* The Smart List — what the human chose to keep. Persisted locally;
     the Smart Lists room reads the same store. */
  const SMARTLIST_KEY='nayanet.today.smartlist.v1';
  let smartList=[];
  try{
    const raw=localStorage.getItem(SMARTLIST_KEY);
    if(raw) smartList=JSON.parse(raw).filter(x=>typeof x==='string');
  }catch(err){ smartList=[]; }
  function persistSmartList(){
    try{ localStorage.setItem(SMARTLIST_KEY, JSON.stringify(smartList)); }catch(err){}
  }
  const SEEN_KEY='nayanet.today.seen.v1';
  let seenPlays=new Set();
  try{
    const rawSeen=localStorage.getItem(SEEN_KEY);
    if(rawSeen)seenPlays=new Set(JSON.parse(rawSeen).filter(x=>typeof x==='string'));
  }catch(err){ seenPlays=new Set(); }
  function persistSeen(){
    try{ localStorage.setItem(SEEN_KEY, JSON.stringify(Array.from(seenPlays))); }catch(err){}
  }
  let allPlays=[];
  let query='';
  let activeTab='today';
  const TABS=[
    {id:'today',label:'TODAY',title:'What changed',searchPh:'Search today\u2019s intelligence\u2026'},
    {id:'yesterday',label:'YESTERDAY',title:'What changed yesterday',searchPh:'Search yesterday\u2019s intelligence\u2026'},
    {id:'week',label:'LAST WEEK',title:'What changed last week',searchPh:'Search last week\u2019s intelligence\u2026'}
  ];
  function tabDef(){ return TABS.find(t=>t.id===activeTab)||TABS[0]; }
  function tabPlays(){ return allPlays.filter(p=>(p.period||'today')===activeTab); }

  function TodayRoom(){
    const {el}=window.NayaUI, K=window.NayaRoomKit;
    const stage=el('section','today-stage');
    stage.setAttribute('aria-label','Your Intelligence Today — the highlight reel');

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
    stage.innerHTML='';
    stage.appendChild(orient(el));
    stage.appendChild(smartTabs(el,stage));
    stage.appendChild(searchBar(el));
    const secs=el('div','today-sections');
    secs.appendChild(section(el,'NOW',tabDef().title,nowBlock(el)));
    secs.appendChild(section(el,'WATCH','Still unopened',watchList(el),'watch-sec'));
    secs.appendChild(section(el,'WAITING','Open loops',waitingList(el)));
    const lineup=rememberLineup(el);
    if(lineup)secs.appendChild(section(el,'REMEMBER','Your Smart List',lineup,'remember-sec'));
    stage.appendChild(secs);
  }

  function section(el,eyebrow,title,body,extra){
    const s=el('section','tsection'+(extra?' '+extra:''));
    const h=el('div','tsection-head');
    const e=el('p','tsection-eyebrow',''); e.textContent=eyebrow;
    const t=el('h2','tsection-title',''); t.textContent=title;
    h.appendChild(e); h.appendChild(t);
    s.appendChild(h); s.appendChild(body);
    return s;
  }

  /* ——— SMART TABS: the diary you can flip back through.
         Today / Yesterday / Last Week. Time is the first axis of
         intelligent organization; topic is the second (needs the runtime). ——— */
  function smartTabs(el,stage){
    const wrap=el('div','smart-tabs');
    wrap.setAttribute('role','tablist');
    wrap.setAttribute('aria-label','Time period');
    TABS.forEach(t=>{
      const b=el('button','smart-tab'+(t.id===activeTab?' on':''),'');
      b.type='button';
      b.textContent=t.label;
      b.setAttribute('role','tab');
      b.setAttribute('aria-selected',t.id===activeTab?'true':'false');
      b.addEventListener('click',()=>{
        if(activeTab===t.id)return;
        activeTab=t.id;
        query='';
        renderAll(el,stage);
        const nt=stage.querySelector('.smart-tab.on');
        if(nt)nt.focus();
      });
      wrap.appendChild(b);
    });
    return wrap;
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

    const sc=el('p','score-line');
    sc.innerHTML=scoreHTML();
    o.appendChild(sc);
    return o;
  }

  function scoreHTML(){
    const n=tabPlays().length;
    return '<strong>'+n+'</strong> PLAYS&nbsp;&nbsp;\u00B7&nbsp;&nbsp;<strong>'+smartList.length+'</strong> SAVED';
  }

  /* ——— SEARCH: filter the day's plays ——— */
  function searchBar(el){
    const wrap=el('div','search-wrap');
    const input=el('input','search-input','');
    input.type='search';
    input.setAttribute('aria-label',tabDef().searchPh.replace('\u2026',''));
    input.placeholder=tabDef().searchPh;
    input.value=query;
    input.addEventListener('input',()=>{
      query=input.value;
      const stage=input.closest('.today-stage');
      renderRiver(el,stage);
    });
    wrap.appendChild(input);
    return wrap;
  }

  function matches(p){
    const q=query.trim().toLowerCase();
    if(!q)return true;
    return (p.title+' '+(p.layers.nutshell||'')).toLowerCase().includes(q);
  }

  /* ——— NOW: what changed — ranked boards, reference language ——— */
  function nowBlock(el){
    const block=el('div','now-block');
    const matchLine=el('p','match-line',''); matchLine.id='today-match-line';
    const river=el('div','plays-river'); river.id='today-river';
    block.appendChild(matchLine); block.appendChild(river);
    renderRiverInto(el,matchLine,river);
    return block;
  }

  function renderRiver(el,stage){
    const matchLine=stage.querySelector('#today-match-line');
    const river=stage.querySelector('#today-river');
    if(matchLine&&river)renderRiverInto(el,matchLine,river);
  }

  function renderRiverInto(el,matchLine,river){
    river.innerHTML='';
    const plays=tabPlays();
    const hits=plays.map((p,i)=>({p,i})).filter(x=>matches(x.p));
    const q=query.trim();
    if(q){
      if(hits.length){
        matchLine.textContent=hits.length+' of '+plays.length+' plays match \u201C'+q+'\u201D';
      }else{
        matchLine.textContent='';
        const note=el('p','quiet-note','');
        note.textContent='No intelligence matches \u201C'+q+'\u201D in '+tabDef().label.toLowerCase()+'.';
        river.appendChild(note);
        return;
      }
    }else{
      matchLine.textContent='';
    }
    hits.forEach(x=>river.appendChild(play(el,x.p,x.i)));
  }

  /* ——— THE BOARD — reference anatomy, quoted verbatim ——— */
  /* ——— THE HIGHLIGHT — a snapshot, not the full note.
         Rank + title + when + call + nutshell + SAVE/SHARE.
         No pills (rank IS the priority; the call IS the significance).
         Tap opens the full intelligent block in its own view. ——— */
  function play(el,p,rank){
    const tone=toneFor(p);
    const nn=String(rank+1).padStart(2,'0');
    const a=el('article','block naya509-board today-highlight');
    a.id='play-'+p.id;
    a.style.setProperty('--tone',tone);

    const inner=el('div','blockInner');

    /* blockTop: identity (rank glyph + title + meta) */
    const top=el('div','blockTop');
    const ident=el('div','identity');
    const glyph=el('div','glyph',''); glyph.textContent=nn;
    glyph.setAttribute('aria-hidden','true');
    const titleWrap=el('div','');
    const h3=el('h3',''); h3.textContent=p.title;
    const meta=el('div','meta');
    const mWhen=el('span',''); mWhen.textContent=p.when||'TODAY';
    const mPlay=el('span',''); mPlay.textContent='PLAY '+nn;
    meta.appendChild(mWhen); meta.appendChild(mPlay);
    titleWrap.appendChild(h3); titleWrap.appendChild(meta);
    ident.appendChild(glyph); ident.appendChild(titleWrap);
    top.appendChild(ident);
    inner.appendChild(top);

    /* the nutshell — the snapshot, and the whole snapshot */
    if(p.layers.nutshell){
      const nut=el('div','nutshell');
      const b=el('b',''); b.textContent='IN A NUTSHELL';
      const par=el('p',''); par.textContent=p.layers.nutshell;
      nut.appendChild(b); nut.appendChild(par);
      inner.appendChild(nut);
    }

    /* actions — SAVE keeps it, SHARE sends it, VIEW FULL NOTE opens it */
    inner.appendChild(actionRow(el,p,()=>openNote(el,p,rank)));

    const foot=el('div','blockFoot');
    const fL=el('span',''); fL.textContent='YOUR INTELLIGENCE TODAY';
    const fR=el('span',''); fR.textContent='INTELLIGENCE EVENT \u00B7 PLAY '+nn;
    foot.appendChild(fL); foot.appendChild(fR);
    inner.appendChild(foot);

    a.appendChild(inner);
    return a;
  }

  /* ——— shared SAVE/SHARE/VIEW row (highlights and the full-note view) ——— */
  function actionRow(el,p,onView){
    const actions=el('div','actions');
    const isOn=smartList.includes(p.id);
    const save=el('button','action'+(isOn?' carry-on':''),'');
    save.type='button';
    save.dataset.saveFor=p.id;
    save.textContent=isOn?'\u2605 SAVED':'SAVE';
    save.setAttribute('aria-pressed',isOn?'true':'false');
    save.setAttribute('aria-label',(isOn?'Remove from your Smart List: ':'Save to your Smart List: ')+p.title);
    if(isOn)save.style.setProperty('--action-color','#e8b64c');
    save.addEventListener('click',e2=>{
      e2.stopPropagation();
      toggleSave(el,p.id,p.title);
    });
    const share=el('button','action','SHARE'); share.type='button';
    share.setAttribute('aria-label','Share: '+p.title);
    share.addEventListener('click',e2=>{
      e2.stopPropagation();
      sharePlay(p,share);
    });
    actions.appendChild(save); actions.appendChild(share);
    if(onView){
      const view=el('button','action','VIEW FULL NOTE'); view.type='button';
      view.setAttribute('aria-label','View the full smart note: '+p.title);
      view.addEventListener('click',e2=>{
        e2.stopPropagation();
        onView();
      });
      actions.appendChild(view);
    }
    return actions;
  }

  function toggleSave(el,playId,title){
    const ix=smartList.indexOf(playId);
    if(ix>=0)smartList.splice(ix,1); else smartList.push(playId);
    persistSmartList();
    const isOn=smartList.includes(playId);
    /* surgical update — no full re-render, no scroll jump */
    document.querySelectorAll('[data-save-for="'+CSS.escape(playId)+'"]').forEach(btn=>{
      btn.textContent=isOn?'\u2605 SAVED':'SAVE';
      btn.setAttribute('aria-pressed',isOn?'true':'false');
      btn.setAttribute('aria-label',(isOn?'Remove from your Smart List: ':'Save to your Smart List: ')+title);
      btn.classList.toggle('carry-on',isOn);
      btn.style.setProperty('--action-color',isOn?'#e8b64c':'');
    });
    const stage=document.querySelector('.today-stage');
    if(stage){
      const sc=stage.querySelector('.score-line');
      if(sc)sc.innerHTML=scoreHTML();
      const sec=stage.querySelector('.remember-sec');
      if(sec){
        const fresh=rememberLineup(el);
        if(fresh){ sec.replaceChildren(fresh); }
        else{ sec.remove(); }
      }else if(smartList.length){
        const wrap=stage.querySelector('.today-sections');
        if(wrap)wrap.appendChild(section(el,'REMEMBER','Your Smart List',rememberLineup(el),'remember-sec'));
      }
    }
  }

  function sharePlay(p,btn){
    const url=location.origin+location.pathname+'#/today/'+p.id;
    const data={title:p.title, text:p.layers.nutshell||p.title, url:url};
    const copied=()=>{ btn.textContent='COPIED \u2713'; setTimeout(()=>{ btn.textContent='SHARE'; },2000); };
    const copyFallback=()=>{
      const ta=document.createElement('textarea');
      ta.value=url; ta.style.position='fixed'; ta.style.opacity='0';
      document.body.appendChild(ta); ta.select();
      try{ document.execCommand('copy'); copied(); }
      catch(err){ btn.textContent='SHARE FAILED'; setTimeout(()=>{ btn.textContent='SHARE'; },2000); }
      document.body.removeChild(ta);
    };
    if(navigator.share){
      navigator.share(data).then(
        ()=>{ btn.textContent='SHARED \u2713'; setTimeout(()=>{ btn.textContent='SHARE'; },2000); },
        ()=>{}
      );
    }else if(navigator.clipboard&&navigator.clipboard.writeText){
      navigator.clipboard.writeText(url).then(copied).catch(copyFallback);
    }else copyFallback();
  }

  /* ——— THE FULL NOTE — one home for the intelligent block.
         The highlight points here; this is not a second presentation. ——— */
  function openNote(el,p,rank){
    closeNote();
    seenPlays.add(p.id); persistSeen();
    const stage=document.querySelector('.today-stage');
    if(stage)renderWatchOnly(el,stage);

    const tone=toneFor(p);
    const nn=String(rank+1).padStart(2,'0');
    const overlay=el('div','note-overlay'); overlay.id='today-note-overlay';
    const dialog=el('div','note-dialog block naya509-board');
    dialog.style.setProperty('--tone',tone);
    dialog.setAttribute('role','dialog');
    dialog.setAttribute('aria-modal','true');
    dialog.setAttribute('aria-label','Full note: '+p.title);

    const inner=el('div','blockInner');
    const close=el('button','note-close','\u00D7'); close.type='button';
    close.setAttribute('aria-label','Close the full note');
    close.addEventListener('click',closeNote);
    inner.appendChild(close);

    const top=el('div','blockTop');
    const ident=el('div','identity');
    const glyph=el('div','glyph',''); glyph.textContent=nn; glyph.setAttribute('aria-hidden','true');
    const titleWrap=el('div','');
    const h3=el('h3',''); h3.textContent=p.title;
    const meta=el('div','meta');
    const mWhen=el('span',''); mWhen.textContent=p.when||'TODAY';
    const mPlay=el('span',''); mPlay.textContent='PLAY '+nn;
    meta.appendChild(mWhen); meta.appendChild(mPlay);
    titleWrap.appendChild(h3); titleWrap.appendChild(meta);
    ident.appendChild(glyph); ident.appendChild(titleWrap);
    top.appendChild(ident); inner.appendChild(top);

    if(p.call){ const c=el('p','call',''); c.textContent=p.call; inner.appendChild(c); }
    if(p.layers.nutshell){
      const nut=el('div','nutshell');
      const b=el('b',''); b.textContent='IN A NUTSHELL';
      const par=el('p',''); par.textContent=p.layers.nutshell;
      nut.appendChild(b); nut.appendChild(par); inner.appendChild(nut);
    }
    const layers=el('div','layers');
    LAYERS.forEach(([key,label,sub])=>{
      if(p.layers[key])layers.appendChild(makeLayer(el,key,label,sub,p.layers[key],tone));
    });
    inner.appendChild(layers);
    inner.appendChild(actionRow(el,p));
    const foot=el('div','blockFoot');
    const fL=el('span',''); fL.textContent='YOUR INTELLIGENCE TODAY';
    const fR=el('span',''); fR.textContent='INTELLIGENCE EVENT \u00B7 PLAY '+nn;
    foot.appendChild(fL); foot.appendChild(fR); inner.appendChild(foot);

    dialog.appendChild(inner);
    overlay.appendChild(dialog);
    overlay.addEventListener('click',e=>{ if(e.target===overlay)closeNote(); });
    const host=document.querySelector('.today-stage')||document.body;
    host.appendChild(overlay);
    document.body.style.overflow='hidden';
    close.focus();
  }

  function closeNote(){
    const ov=document.getElementById('today-note-overlay');
    if(ov)ov.remove();
    document.body.style.overflow='';
  }
  document.addEventListener('keydown',e=>{
    if(e.key==='Escape')closeNote();
  });

  function renderWatchOnly(el,stage){
    const w=stage.querySelector('.watch-sec .watch-list');
    if(!w)return;
    const fresh=watchList(el);
    w.replaceWith(fresh);
  }

  function makeLayer(el,key,label,sub,text,tone){
    const a=el('article','layer');
    a.style.setProperty('--layer',tone);
    const head=el('div','layerHead');
    const dot=el('span','dot',''); dot.setAttribute('aria-hidden','true');
    const b=el('b',''); b.textContent=label;
    const st=el('span','state',''); st.textContent=sub;
    head.appendChild(dot); head.appendChild(b); head.appendChild(st);
    const body=el('div','layerBody',''); body.textContent=text;
    a.appendChild(head); a.appendChild(body);
    return a;
  }

  /* ——— WATCH: still unopened — derived from real state ——— */
  function watchList(el){
    const wrap=el('div','watch-list');
    const plays=tabPlays();
    const unseen=plays.filter(p=>!seenPlays.has(p.id));
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
        const rank=plays.findIndex(x=>x.id===p.id);
        openNote(el,p,rank);
      });
      li.appendChild(dot); li.appendChild(span); li.appendChild(open); ul.appendChild(li);
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

  /* ——— REMEMBER: your Smart List ——— */
  function rememberLineup(el){
    if(!smartList.length)return null;
    const box=el('div','lineup');
    const sub=el('p','lineup-sub','');
    sub.textContent='You saved '+smartList.length+' to your Smart List.';
    box.appendChild(sub);
    const ul=el('ul','');
    smartList.forEach(id=>{
      const p=allPlays.find(x=>x.id===id); if(!p)return;
      const li=el('li','');
      const dot=el('span','lineup-dot',''); dot.style.setProperty('--tone',toneFor(p));
      const span=el('span','',''); span.textContent=p.title;
      const rm=el('button','','Remove'); rm.type='button';
      rm.setAttribute('aria-label','Remove from Smart List: '+p.title);
      rm.addEventListener('click',()=>{ toggleSave(el,id,p.title); });
      li.appendChild(dot); li.appendChild(span); li.appendChild(rm); ul.appendChild(li);
    });
    box.appendChild(ul);
    return box;
  }

  function normalize(o,K){
    const src=o.layers||o.intelligent_block||o.content||{};
    const keys=['nutshell','human','child','grandma','naya','machine','learning','means','value'];
    const layers={};
    keys.forEach(key=>{
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
      waiting:Array.isArray(o.waiting)?o.waiting.filter(w=>typeof w==='string'&&w.trim()):[],
      period:o.period||'today',
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


  function esc(s){
    return String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  }

  window.NayaRooms=window.NayaRooms||{};
  window.NayaRooms.today=TodayRoom;
})();
