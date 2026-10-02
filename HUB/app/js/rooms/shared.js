/* ROOM KIT — shared mechanics, not a shared composition. */
(function(){
  const {el, StatePanel, Board, toast}=window.NayaUI;
  function safe(v){return String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
  function room(id){return window.NayaRuntime.ROOMS.find(r=>r.id===id);}
  function state(container,id,title,body,actions=[]){
    const r=room(id); container.innerHTML='';
    container.appendChild(StatePanel({accent:r.accent,icon:r.icon,title,body,actions}));
  }
  function unavailable(container,id,detail){
    const c=window.NayaRuntime.NOT_VERIFIED_COPY;
    state(container,id,c.title,detail||c.body,[{label:'System health',icon:'core',ghost:true,onClick:()=>window.NayaRouter.navigate('/hub/settings')}]);
  }
  function empty(container,id,title,body){state(container,id,title,body,[]);}
  function segmented(labels,active,onChange){
    const w=el('div','segmented');
    labels.forEach(x=>{
      const value=typeof x==='string'?x:x.value, label=typeof x==='string'?x:x.label;
      const b=el('button',value===active?'active':'',safe(label)); b.type='button';
      b.setAttribute('aria-pressed',value===active?'true':'false');
      b.addEventListener('click',()=>{
        [...w.children].forEach(n=>{n.classList.remove('active');n.setAttribute('aria-pressed','false')});
        b.classList.add('active'); b.setAttribute('aria-pressed','true'); onChange(value,b);
      });
      w.appendChild(b);
    });
    return w;
  }
  function items(payload){
    if(!payload)return[]; if(Array.isArray(payload))return payload;
    for(const k of ['items','results','data','feed','events','records','messages','connections','lists','spaces','reports']) if(Array.isArray(payload[k])) return payload[k];
    if(payload.data&&typeof payload.data==='object') for(const k of Object.keys(payload.data)) if(Array.isArray(payload.data[k])) return payload.data[k];
    return[];
  }
  function title(x,fallback='Intelligence'){return x?.title||x?.name||x?.subject||x?.label||x?.summary||fallback;}
  function summary(x){return x?.summary||x?.description||x?.human||x?.text||x?.content?.summary||x?.content?.human||'';}
  function meta(x){
    const out=[];
    if(x?.truth_state||x?.state)out.push(x.truth_state||x.state);
    if(x?.created_at||x?.timestamp||x?.time)out.push(x.created_at||x.timestamp||x.time);
    if(x?.source?.name||x?.source)out.push(typeof x.source==='string'?x.source:x.source.name);
    if(x?.intelligent_block_id||x?.id)out.push(x.intelligent_block_id||x.id);
    return out.filter(Boolean).slice(0,4);
  }
  function intelCard(x,accent,opts={}){
    const card=el('article','intel-row'); card.style.setProperty('--room-accent',accent);
    card.innerHTML='<div class="intel-type">'+safe(opts.type||x?.type||x?.category||'INTELLIGENCE')+'</div>'+
      '<div class="intel-title">'+safe(title(x))+'</div>'+
      (summary(x)?'<div class="intel-summary">'+safe(summary(x))+'</div>':'')+
      '<div class="meta-row">'+meta(x).map(m=>'<span>'+safe(m)+'</span>').join('')+'</div><div class="action-row"></div>';
    const actions=card.querySelector('.action-row');
    const open=el('button','btn btn-ghost mini','<span>Open</span>'); open.style.setProperty('--btn-accent',accent);
    open.addEventListener('click',()=>opts.onOpen?opts.onOpen(x):toast('Canonical detail opens when the governed runtime exposes retrieval.',accent));
    actions.appendChild(open);
    if(opts.evidence!==false){
      const ev=el('button','btn btn-ghost mini','<span>Evidence</span>'); ev.style.setProperty('--btn-accent',accent);
      ev.addEventListener('click',()=>opts.onEvidence?opts.onEvidence(x):toast('Evidence is never fabricated; it remains attached to the canonical object.',accent));
      actions.appendChild(ev);
    }
    return card;
  }
  function board(accent,icon,titleText,sub){return Board({accent,icon,title:titleText,sub,lift:false});}
  async function load(container,id,request,render,emptyCopy){
    const r=room(id); container.setAttribute('aria-busy','true'); container.innerHTML='';
    const shimmer=el('div','shimmer-grid');
    for(let i=0;i<3;i++){const s=el('div','shimmer');s.style.setProperty('--room-accent',r.accent);shimmer.appendChild(s)}
    container.appendChild(shimmer);
    let res;
    try{res=await window.NayaRuntime.roomSocket.query(id,request||{});}catch(err){res={ok:false,state:'error',message:err?.message||'The room could not load.'};}
    container.setAttribute('aria-busy','false');
    if(!res?.ok){
      if(res?.state==='empty') empty(container,id,emptyCopy?.title||'Nothing here yet',emptyCopy?.body||'There is no qualifying intelligence in this scope.');
      else if(res?.state==='error') state(container,id,'This room hit an error',res.message||'The governed runtime returned an error.',[{label:'Try again',icon:'arrow',onClick:()=>load(container,id,request,render,emptyCopy)}]);
      else unavailable(container,id,res?.message);
      return;
    }
    const payload=res.data??res, list=items(payload);
    if(!list.length&&!payload?.summary&&!payload?.reflection&&!payload?.metrics){
      empty(container,id,emptyCopy?.title||'Nothing here yet',emptyCopy?.body||'There is no qualifying intelligence in this scope.'); return;
    }
    container.innerHTML=''; render(payload,list,container);
  }
  window.NayaRoomKit={safe,room,state,unavailable,empty,segmented,items,title,summary,meta,intelCard,board,load};
})();