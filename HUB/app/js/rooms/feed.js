/* ═══════════════════════════════════════════════════════════════════
   SMART FEED — THE MAIN SHOW
   Projection, not input. Canonical intelligence remains in NayaPOWER.
   Human experience:
   PRESENCE → RECOGNITION → DISTILLATION → INVITATION → FLOW.
   The river stays quiet. A snapshot opens one complete intelligence
   object. Evidence and action remain truthful and governed.
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


  const GLYPHS={
    decision:'<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 12.5l5 5L20 6.5"/></svg>',
    intelligence:'<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M4 8.5c2.6-2.6 5.4-2.6 8 0s5.4 2.6 8 0"/><path d="M4 13.5c2.6-2.6 5.4-2.6 8 0s5.4 2.6 8 0"/><path d="M4 18.5c2.6-2.6 5.4-2.6 8 0s5.4 2.6 8 0"/></svg>',
    signal:'<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.2" aria-hidden="true"><circle cx="12" cy="12" r="3.2" fill="#fff" stroke="none"/><circle cx="12" cy="12" r="7.5"/></svg>',
    event:'<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.2" stroke-linejoin="round" aria-hidden="true"><path d="M13 3L5 13.5h6L11 21l8-10.5h-6L13 3z"/></svg>'
  };

  let allItems=[];
  let currentMode=normalizeMode(window.NayaRuntime?.mode||'collective');
  let evidenceReturnFocus=null;
  let riverReturnContext=null;
  let activeAskContext=null;

  function FeedRoom(){
    const {el}=window.NayaUI;
    const K=window.NayaRoomKit;
    const stage=el('section','feed-stage');
    stage.setAttribute('aria-label','Smart Feed — the Main Show');

    stage.appendChild(greeting(el));


    const loadZone=el('div','feed-load-zone');
    stage.appendChild(loadZone);

    const river=el('div','feed-river');
    stage.appendChild(river);

    const note=el('div','note-view');
    note.hidden=true;
    stage.appendChild(note);

    const foot=el('div','feed-stage-foot');
    const ask=el('button','feed-ask','<span>Ask Naya about today</span>');
    ask.type='button';
    const panel=askPanel(el);
    ask.addEventListener('click',()=>{
      if(!panel.classList.contains('open')) activeAskContext=null;
      panel.classList.toggle('open');
      if(panel.classList.contains('open')){
        const input=panel.querySelector('.ask-input');
        if(input) input.focus();
      }
    });
    foot.append(ask,panel);
    stage.appendChild(foot);

    stage.appendChild(evDrawer(el));

    K.load(loadZone,'feed',{limit:25},(payload,list)=>{
      allItems=(list||[]).map(o=>normalize(o,K));
      loadZone.remove();
      renderRiver(el,stage);
    },{
      title:'The stage is quiet',
      body:'There is no qualifying intelligence right now. When something matters, it appears here — ordered for you, never manufactured to fill the space.'
    });

    return stage;
  }

  function greeting(el){
    const hour=new Date().getHours();
    const part=hour<12?'Good morning':hour<18?'Good afternoon':'Good evening';
    const identity=window.NayaRuntime?.identitySnapshot?.();
    const known=identity&&/^(ready|verified|current)$/i.test(identity.state||'')&&identity.display_name&&identity.display_name!=='You';
    const who=known?identity.display_name:'';
    const date=new Date().toLocaleDateString('en-US',{weekday:'long',month:'long',day:'numeric'});

    const wrap=el('header','feed-stage-head');
    const title=el('h1','feed-greeting','');
    title.textContent=who?part+', '+who:part;

    const dateline=el('p','feed-dateline','');
    dateline.innerHTML='<span>'+esc(date.toUpperCase())+'</span><span class="feed-dot">·</span><span>YOUR INTELLIGENCE TODAY</span>';

    const promise=el('p','feed-daystate','');
    promise.textContent='What matters now, distilled first. Open anything to understand it, inspect its evidence, or act through the governed runtime.';

    wrap.append(title,dateline,promise);
    return wrap;
  }

  function renderRiver(el,stage){
    const river=stage.querySelector('.feed-river');
    const note=stage.querySelector('.note-view');
    currentMode=normalizeMode(window.NayaRuntime?.mode||currentMode);
    if(!river||!note) return;

    note.hidden=true;
    river.hidden=false;
    setModeVisibility(false);
    river.innerHTML='';

    const items=allItems.filter(item=>modeOf(item)===currentMode);

    if(!items.length){
      const empty=el('div','feed-empty');
      const h=el('strong','','Nothing in '+currentMode+' right now.');
      const p=el('span','','When qualifying intelligence arrives, it appears here. NayaNET never manufactures activity to make the screen feel busy.');
      empty.append(h,p);
      river.appendChild(empty);
      return;
    }

    const kicker=el('p','river-kicker','');
    kicker.innerHTML='<span>'+items.length+'</span>&nbsp;&nbsp;INTELLIGENCE BLOCK'+(items.length===1?'':'S')+' · '+esc(currentMode.toUpperCase());
    river.appendChild(kicker);

    items.forEach((item,index)=>river.appendChild(snapshot(el,item,index)));
  }

  function snapshot(el,b,index){
    const hero=index===0;
    const board=el('article','snap-board'+(hero?' snap-hero':''));
    board.style.setProperty('--tone',toneFor(b));
    board.style.setProperty('--state-tone',stateTone(b.truth_state));
    board.setAttribute('tabindex','0');
    board.setAttribute('role','button');
    board.dataset.intelligenceId=b.id;
    board.setAttribute('aria-label','Open intelligence: '+b.title);

    const orb=el('div','sb-orb');
    orb.innerHTML=glyphFor(b);
    orb.setAttribute('aria-hidden','true');

    const main=el('div','sb-main');
    const meta=el('div','sb-meta');
    if(hero){
      const priority=el('span','sb-priority','RIGHT NOW');
      meta.appendChild(priority);
    }
    const theme=el('p','sb-theme','');
    theme.textContent=b.type;
    const state=el('span','sb-state','');
    state.textContent=shortState(b.truth_state);
    meta.append(theme,state);

    const title=el('h2','sb-title','');
    title.textContent=b.title;

    const nutshell=el('p','sb-nut','');
    nutshell.textContent=b.layers.nutshell||'No nutshell was supplied for this intelligence object.';

    main.append(meta,title,nutshell);

    if(hero){
      const enter=el('span','sb-enter','Open intelligence <span aria-hidden="true">→</span>');
      main.appendChild(enter);
    }

    if(b.whyNow){
      const why=el('p','sb-why','');
      why.innerHTML='<strong>WHY NOW</strong><span>'+esc(b.whyNow)+'</span>';
      main.appendChild(why);
    }

    board.append(orb,main);

    const open=()=>{
      const stage=board.closest('.feed-stage');
      riverReturnContext={id:b.id,scrollY:window.scrollY};
      renderNote(el,stage,b);
      stage.scrollIntoView({block:'start',behavior:'auto'});
      requestAnimationFrame(()=>{
        stage.querySelector('.note-back')?.focus({preventScroll:true});
      });
    };
    board.addEventListener('click',open);
    board.addEventListener('keydown',event=>{
      if(event.key==='Enter'||event.key===' '){
        event.preventDefault();
        open();
      }
    });

    return board;
  }

  function renderNote(el,stage,b){
    const river=stage.querySelector('.feed-river');
    const note=stage.querySelector('.note-view');
    river.hidden=true;
    note.hidden=false;
    setModeVisibility(true);
    note.innerHTML='';
    note.style.setProperty('--tone',toneFor(b));
    note.style.setProperty('--state-tone',stateTone(b.truth_state));

    const back=el('button','note-back','<span aria-hidden="true">←</span><span>Back to '+currentMode+'</span>');
    back.type='button';
    back.setAttribute('aria-label','Back to the '+currentMode+' intelligence river');
    back.addEventListener('click',()=>{
      const restore=riverReturnContext;
      renderRiver(el,stage);
      requestAnimationFrame(()=>{
        if(restore){
          window.scrollTo({top:restore.scrollY,left:0,behavior:'auto'});
          const target=[...stage.querySelectorAll('.snap-board')]
            .find(node=>node.dataset.intelligenceId===restore.id);
          target?.focus({preventScroll:true});
        }
        riverReturnContext=null;
      });
    });
    note.appendChild(back);

    const head=el('div','note-head');
    const orb=el('div','note-orb');
    orb.innerHTML=glyphFor(b);
    orb.setAttribute('aria-hidden','true');
    const hgroup=el('div','note-hgroup');
    const type=el('p','note-canon','');
    type.textContent=b.type+' · '+shortState(b.truth_state);
    const title=el('h2','note-title','');
    title.textContent=b.title;
    hgroup.append(type,title);
    head.append(orb,hgroup);
    note.appendChild(head);

    if(b.source){
      const source=el('p','note-source','');
      source.textContent='SOURCE · '+b.source;
      note.appendChild(source);
    }

    if(b.whyNow){
      const why=el('div','note-why','');
      why.innerHTML='<strong>WHY NOW</strong><span>'+esc(b.whyNow)+'</span>';
      note.appendChild(why);
    }

    const layers=el('div','note-layers');
    LAYERS.forEach(([key])=>{
      if(b.layers[key]) layers.appendChild(makeLayer(el,key,b.layers[key]));
    });
    note.appendChild(layers);

    const tools=el('div','note-tools');
    tools.appendChild(toolBtn(el,'Inspect evidence',()=>openEvidence(b)));

    if(b.action){
      const action=toolBtn(el,b.action.label,()=>runGovernedAction(b,action,actionStatus));
      action.classList.add('note-tool-primary');
      tools.appendChild(action);
      var actionStatus=el('span','note-action-status','');
      actionStatus.setAttribute('role','status');
      actionStatus.setAttribute('aria-live','polite');
      tools.appendChild(actionStatus);
    }

    tools.appendChild(toolBtn(el,'Ask Naya',()=>openAskForBlock(stage,b)));
    note.appendChild(tools);

    const refs=buildRelationships(el,stage,b);
    if(refs.childElementCount) note.appendChild(refs);

    const foot=el('footer','note-foot');
    foot.innerHTML='<p>ONE INTELLIGENCE · MANY VIEWS · ONE IDENTITY</p><p>TRUST: SOURCE / INTERPRETATION SEPARATED</p>';
    note.appendChild(foot);
  }

  function buildRelationships(el,stage,b){
    const wrap=el('section','note-related');
    const links=el('div','note-related-links');

    b.related.forEach(id=>{
      const target=allItems.find(item=>item.id===String(id));
      if(!target) return;
      links.appendChild(toolBtn(el,'Related · '+shortTitle(target.title),()=>{
        renderNote(el,stage,target);
        stage.scrollIntoView({block:'start'});
      }));
    });

    const roomMap={list:'lists',space:'spaces',report:'reports'};
    Object.keys(roomMap).forEach(key=>{
      if(!b.context?.[key]) return;
      links.appendChild(toolBtn(el,key.charAt(0).toUpperCase()+key.slice(1)+' · '+shortTitle(b.context[key]),()=>{
        window.NayaRouter.navigate('/hub/'+roomMap[key]);
      }));
    });

    if(b.people.length){
      const people=el('p','note-people','');
      people.textContent='Related people · '+b.people.join(', ');
      links.appendChild(people);
    }

    if(links.childElementCount){
      const label=el('p','note-related-label','RELATIONSHIPS');
      wrap.append(label,links);
    }

    return wrap;
  }

  async function runGovernedAction(b,button,status){
    if(!window.NayaRuntime.roomSocket?.act){
      setStatus(status,'not_verified','The governed action seam is not available. Nothing changed.');
      return;
    }

    button.disabled=true;
    button.dataset.state='processing';
    const original=button.textContent;
    button.textContent='Working…';
    setStatus(status,'processing','Checking runtime capability and authority…');

    let out;
    try{
      out=await window.NayaRuntime.roomSocket.act('feed',{
        id:b.id,
        intelligent_block_id:b.id,
        action:b.action.kind,
        label:b.action.label,
        mode:modeOf(b)
      });
    }catch(err){
      out={ok:false,state:'error',message:err?.message||'The action failed.'};
    }

    if(!out?.ok){
      button.disabled=false;
      button.dataset.state=out?.state||'not_verified';
      button.textContent=original;
      setStatus(status,out?.state||'not_verified',out?.message||'The runtime did not confirm this action. Nothing changed.');
      return;
    }

    const data=out.data??out;
    const receipt=data?.receipt?.receipt_id||data?.receipt_id||out?.raw?.receipt?.receipt_id||'';
    button.dataset.state='success';
    button.textContent='Completed';
    setStatus(
      status,
      'success',
      receipt?'Receipt · '+receipt:'Runtime confirmed the action, but no receipt ID was returned.'
    );
  }

  function setStatus(node,state,text){
    if(!node) return;
    node.dataset.state=state;
    node.textContent=text;
  }

  function toolBtn(el,label,fn){
    const b=el('button','note-tool','');
    b.type='button';
    b.textContent=label;
    b.addEventListener('click',fn);
    return b;
  }

  function makeLayer(el,key,text){
    const found=LAYERS.find(layer=>layer[0]===key);
    const block=el('section','nlayer');
    const label=el('p','nlayer-label','');
    label.innerHTML='<strong>'+esc(found?found[1]:key.toUpperCase())+'</strong>'+
      (found&&found[2]?'<span>'+esc(found[2])+'</span>':'');
    const body=el('p','nlayer-text','');
    body.textContent=text;
    block.append(label,body);
    return block;
  }

  function normalize(o,K){
    const src=o.layers||o.intelligent_block||o.content||{};
    const layers={};

    LAYERS.forEach(([key])=>{
      const value=o[key]??src[key];
      if(typeof value==='string'&&value.trim()) layers[key]=value.trim();
    });

    if(!layers.nutshell){
      const summary=K.summary(o);
      if(summary) layers.nutshell=summary;
    }
    if(!layers.machine) layers.machine=evidenceLine(o);

    const type=String(o.category||o.type||o.kind||'INTELLIGENCE').toUpperCase();
    const state=String(o.truth_state||o.state||'UNKNOWN').toUpperCase();
    const sourceObject=o.source&&typeof o.source==='object'?o.source:null;
    const source=typeof o.source==='string'?o.source:(sourceObject?.name||sourceObject?.title||'');
    const action=o.action||o.primary_action||null;

    return {
      id:String(o.intelligent_block_id||o.id||type+'-'+Math.abs(hashCode(o.title||''))),
      mode:normalizeMode(o.mode||o.stream||o.feed_scope||o.projection),
      type,
      title:K.title(o,'Untitled intelligence'),
      source,
      truth_state:state,
      created_at:o.created_at||o.timestamp||o.time||'',
      whyNow:o.why_now||o.whyNow||o.rank_reason||'',
      layers,
      related:Array.isArray(o.related)?o.related:[],
      people:Array.isArray(o.people)?o.people:[],
      context:o.context||{},
      action:(action&&(action.label||action.verb))?{
        label:action.label||action.verb,
        kind:String(action.kind||action.action||action.verb||'act').toLowerCase()
      }:null
    };
  }

  function evDrawer(el){
    const wrap=el('div','ev-wrap','');
    const backdrop=el('div','ev-backdrop','');
    backdrop.id='ev-backdrop';
    const drawer=el('aside','ev-drawer','');
    drawer.id='ev-drawer';
    drawer.setAttribute('aria-label','Evidence');
    drawer.setAttribute('role','dialog');
    drawer.setAttribute('aria-modal','true');
    backdrop.addEventListener('click',closeEvidence);
    wrap.append(backdrop,drawer);
    window.__nayaCloseEvidence=closeEvidence;
    return wrap;
  }

  function openEvidence(b){
    const {el}=window.NayaUI;
    const drawer=document.getElementById('ev-drawer');
    const backdrop=document.getElementById('ev-backdrop');
    if(!drawer||!backdrop) return;

    evidenceReturnFocus=document.activeElement;
    drawer.innerHTML='';

    const kicker=el('p','ev-kicker','');
    kicker.textContent='EVIDENCE · '+shortState(b.truth_state);
    const title=el('h3','','');
    title.textContent=b.title;
    const intro=el('p','ev-intro','');
    intro.textContent='What this projection can state now, plus a direct retrieval check against the canonical runtime.';
    drawer.append(kicker,title,intro);

    const chain=el('ul','ev-chain');
    [
      ['SOURCE',b.source||'No source name was supplied.'],
      ['TIME',b.created_at||'No event time was supplied.'],
      ['OBJECT','Canonical ID: '+b.id+'.'],
      ['WHY NOW',b.whyNow||'No separate ranking reason was supplied.'],
      ['STATE',shortState(b.truth_state)+'. Presentation does not upgrade truth.']
    ].forEach(([label,value])=>{
      const li=el('li','');
      li.innerHTML='<strong>'+esc(label)+'</strong>';
      const span=el('span','','');
      span.textContent=value;
      li.appendChild(span);
      chain.appendChild(li);
    });
    drawer.appendChild(chain);

    const retrieve=el('button','ev-retrieve','Retrieve canonical record');
    retrieve.type='button';
    const result=el('div','ev-runtime-result','');
    result.setAttribute('role','status');
    result.setAttribute('aria-live','polite');

    retrieve.addEventListener('click',async()=>{
      retrieve.disabled=true;
      retrieve.textContent='Retrieving…';
      let out;
      try{
        out=await window.NayaRuntime.roomSocket.retrieve('feed',b.id);
      }catch(err){
        out={ok:false,state:'error',message:err?.message||'Canonical retrieval failed.'};
      }
      retrieve.disabled=false;
      retrieve.textContent='Retrieve canonical record';

      if(!out?.ok){
        result.dataset.state=out?.state||'not_verified';
        result.textContent=out?.message||'The canonical record is not available from the governed runtime.';
        return;
      }

      const data=out.data??out;
      const name=data?.title||data?.name||b.title;
      const state=data?.truth_state||data?.state||'state not returned';
      result.dataset.state='success';
      result.textContent='Canonical runtime returned “'+name+'” · '+state+'.';
    });

    const close=el('button','ev-close','Close evidence');
    close.type='button';
    close.addEventListener('click',closeEvidence);
    drawer.append(retrieve,result,close);

    backdrop.classList.add('open');
    drawer.classList.add('open');
    close.focus();
  }

  function closeEvidence(){
    const drawer=document.getElementById('ev-drawer');
    const backdrop=document.getElementById('ev-backdrop');
    if(drawer) drawer.classList.remove('open');
    if(backdrop) backdrop.classList.remove('open');
    if(evidenceReturnFocus&&evidenceReturnFocus.focus){
      try{ evidenceReturnFocus.focus(); }catch(_){}
    }
    evidenceReturnFocus=null;
  }

  function askPanel(el){
    const panel=el('section','ask-panel');
    const title=el('h3','','Ask Naya about today');
    const sub=el('p','ask-sub','');
    sub.textContent='Ask in plain words. Naya uses the governed retrieval seam first and clearly labels any on-screen fallback.';

    const row=el('div','ask-row');
    const input=el('input','ask-input');
    input.type='text';
    input.setAttribute('aria-label','Ask Naya about today');
    input.placeholder='What needs my attention today?';

    const go=el('button','ask-go','Ask Naya');
    go.type='button';

    const result=el('div','ask-result');
    result.setAttribute('aria-live','polite');

    const answer=async()=>{
      const question=input.value.trim();
      if(!question) return;

      go.disabled=true;
      go.textContent='Thinking…';
      result.innerHTML='';
      result.classList.add('show');
      result.appendChild(askStep(el,'QUESTION',question));

      let runtime;
      try{
        runtime=await window.NayaRuntime.roomSocket.search('feed',question,{
          room:'feed',
          mode:currentMode,
          intelligent_block_id:activeAskContext?.id||null,
          context:activeAskContext?{
            intelligent_block_id:activeAskContext.id,
            title:activeAskContext.title,
            mode:activeAskContext.mode
          }:null
        });
      }catch(err){
        runtime={ok:false,state:'error',message:err?.message||'Runtime search failed.'};
      }

      if(runtime?.ok) renderRuntimeAnswer(el,result,runtime);
      else renderStageFallback(el,result,question,runtime);

      go.disabled=false;
      go.textContent='Ask Naya';
    };

    go.addEventListener('click',answer);
    input.addEventListener('keydown',event=>{if(event.key==='Enter') answer();});

    row.append(input,go);
    panel.append(title,sub,row,result);
    return panel;
  }

  function renderRuntimeAnswer(el,result,runtime){
    const data=runtime.data??runtime;
    const answerText=typeof data==='string'?data:(data?.answer||data?.summary||data?.message||'');

    if(answerText) result.appendChild(askStep(el,'NAYA',answerText));

    const rawItems=window.NayaRoomKit.items(data);
    if(rawItems.length){
      const group=el('div','ask-step');
      const label=el('p','ask-k','');
      label.textContent='RELATED INTELLIGENCE · '+rawItems.length;
      group.appendChild(label);

      rawItems.slice(0,5).forEach(raw=>{
        const normalized=normalize(raw,window.NayaRoomKit);
        const line=el('div','ask-hit','');
        const local=allItems.find(item=>item.id===normalized.id);
        if(local){
          const button=el('button','','');
          button.type='button';
          button.textContent=local.title;
          button.addEventListener('click',()=>{
            const stage=result.closest('.feed-stage');
            renderNote(el,stage,local);
            stage.scrollIntoView({block:'start'});
          });
          line.appendChild(button);
        }else{
          const text=el('span','','');
          text.textContent=normalized.title;
          line.appendChild(text);
        }
        group.appendChild(line);
      });

      result.appendChild(group);
    }

    const boundary=el('p','ask-boundary','');
    boundary.textContent='Source: governed runtime'+(runtime.method?' · '+runtime.method:'')+
      (activeAskContext?' · Canonical context: '+activeAskContext.id:'')+
      '. The interface does not upgrade the returned truth state.';
    result.appendChild(boundary);
  }

  function renderStageFallback(el,result,question,runtime){
    const localHits=localRetrieve(question);
    const focused=activeAskContext&&allItems.find(item=>item.id===activeAskContext.id);
    const hits=focused
      ? [{b:focused,score:Number.MAX_SAFE_INTEGER},...localHits.filter(hit=>hit.b.id!==focused.id)]
      : localHits;
    const group=el('div','ask-step');
    const label=el('p','ask-k','');
    label.textContent='ON-SCREEN RETRIEVAL · '+hits.length;
    group.appendChild(label);

    if(!hits.length){
      const none=el('p','ask-v','');
      none.textContent='Nothing currently loaded on this stage matches. Naya will not invent an answer.';
      group.appendChild(none);
    }else{
      hits.slice(0,5).forEach(hit=>{
        const line=el('div','ask-hit','');
        const button=el('button','','');
        button.type='button';
        button.textContent=hit.b.title;
        button.addEventListener('click',()=>{
          const stage=result.closest('.feed-stage');
          renderNote(el,stage,hit.b);
          stage.scrollIntoView({block:'start'});
        });
        line.appendChild(button);
        group.appendChild(line);
      });

      const synthesis=hits.slice(0,3).map(hit=>hit.b.layers.nutshell||'').filter(Boolean).join(' ');
      if(synthesis){
        result.appendChild(askStep(
          el,
          'WHAT THE LOADED STAGE SAYS',
          synthesis.slice(0,520)+(synthesis.length>520?'…':'')
        ));
      }
    }

    result.appendChild(group);

    const boundary=el('p','ask-boundary','');
    boundary.textContent='Governed retrieval was unavailable'+(runtime?.message?' — '+runtime.message:'')+
      (activeAskContext?' Canonical context requested: '+activeAskContext.id+'.':'')+
      ' This fallback searches only intelligence already visible to this browser session. Nothing was invented or written.';
    result.appendChild(boundary);
  }

  function openAskForBlock(stage,b){
    const panel=stage.querySelector('.ask-panel');
    if(!panel) return;
    activeAskContext={id:b.id,title:b.title,mode:modeOf(b)};
    panel.dataset.intelligenceId=b.id;
    panel.classList.add('open');
    const input=panel.querySelector('.ask-input');
    if(input){
      input.value='What should I understand or do next about this?';
      input.focus({preventScroll:true});
      input.select();
    }
    panel.scrollIntoView({behavior:prefersReduced()?'auto':'smooth',block:'center'});
  }

  function askStep(el,label,value){
    const block=el('div','ask-step');
    const key=el('p','ask-k','');
    key.textContent=label;
    const body=el('p','ask-v','');
    body.textContent=value;
    block.append(key,body);
    return block;
  }

  function localRetrieve(query){
    const words=query.toLowerCase().split(/[^a-z0-9]+/).filter(word=>word.length>2);
    return allItems.map(item=>{
      const haystack=(
        item.title+' '+item.type+' '+(item.whyNow||'')+' '+Object.values(item.layers).join(' ')
      ).toLowerCase();
      let score=0;
      words.forEach(word=>{if(haystack.includes(word)) score++;});
      return {b:item,score};
    }).filter(result=>result.score>0).sort((a,b)=>b.score-a.score);
  }

  function modeOf(item){
    return normalizeMode(item.mode);
  }

  function normalizeMode(value){
    const raw=String(value||'personal').toLowerCase();
    if(raw.includes('collective')||raw.includes('shared')||raw.includes('public')) return 'collective';
    if(raw.includes('activity')||raw.includes('event')) return 'activity';
    return 'personal';
  }

  function toneFor(b){
    const state=String(b.truth_state||'').toUpperCase();
    const type=String(b.type||'').toUpperCase();
    const mode=modeOf(b);

    if(/BLOCKED|FAILED|ERROR|DENIED|REVOKED|CONTRADICTED/.test(state)) return 'var(--red)';
    if(/NAYA|AI|INTERPRET/.test(type)) return 'var(--purple)';
    if(/CONNECT|CONNECTION|NETWORK|COLLECTIVE|SHARED/.test(type)||mode==='collective') return 'var(--teal)';
    if(/ACTIVITY|EVENT|CURRENT|EXECUTION|UPDATE/.test(type)||mode==='activity') return 'var(--green)';
    if(/KNOWLEDGE|REPORT|EVIDENCE|LIBRARY|LEARNING|INSIGHT|PATTERN/.test(type)) return 'var(--blue)';
    if(/HUMAN|PERSONAL|NOTE|DECISION|IDEA|GOAL|QUESTION|OPPORTUNITY|BREAKTHROUGH/.test(type)||mode==='personal') return 'var(--magenta)';
    return 'var(--sapphire)';
  }

  function stateTone(state){
    const value=String(state||'').toUpperCase();
    if(/BLOCKED|FAILED|ERROR|DENIED|REVOKED|CONTRADICTED/.test(value)) return 'var(--red)';
    if(/VERIFIED|CURRENT|READY|ACTIVE|SUCCESS|LIVE|COMPLETE/.test(value)) return 'var(--green)';
    return 'var(--muted)';
  }

  function themeFor(b){ return b.type||'INTELLIGENCE'; }

  function glyphFor(b){
    const type=String(b.type||'').toLowerCase();
    if(type.includes('decision')) return GLYPHS.decision;
    if(type.includes('event')||type.includes('activity')) return GLYPHS.event;
    if(type.includes('signal')||type.includes('connection')) return GLYPHS.signal;
    return GLYPHS.intelligence;
  }

  function evidenceLine(o){
    const bits=[];
    const source=typeof o.source==='string'?o.source:(o.source&&o.source.name);
    if(source) bits.push('Source: '+source);
    const state=o.truth_state||o.state;
    if(state) bits.push('State: '+String(state).toUpperCase());
    const time=o.created_at||o.timestamp||o.time;
    if(time) bits.push('Time: '+time);
    const id=o.intelligent_block_id||o.id;
    if(id) bits.push('ID: '+id);
    return bits.length?bits.join(' — '):'No provenance is attached to this object.';
  }


  function setModeVisibility(hidden){
    const zone=document.querySelector('.mode-zone');
    if(zone) zone.hidden=!!hidden;
  }

  function prefersReduced(){
    return !!window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
  }

  function hashCode(text){
    let hash=0;
    const value=String(text||'');
    for(let i=0;i<value.length;i++) hash=(hash*31+value.charCodeAt(i))|0;
    return hash;
  }

  function shortState(state){
    return String(state||'UNKNOWN').replaceAll('_',' ');
  }

  function shortTitle(title){
    const value=String(title||'');
    return value.length>36?value.slice(0,36)+'…':value;
  }

  function esc(value){
    return String(value??'').replace(/[&<>"']/g,char=>({
      '&':'&amp;',
      '<':'&lt;',
      '>':'&gt;',
      '"':'&quot;',
      "'":'&#39;'
    }[char]));
  }

  window.NayaRooms=window.NayaRooms||{};
  window.NayaRooms.feed=FeedRoom;
})();
