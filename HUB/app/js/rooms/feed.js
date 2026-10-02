/* SMART FEED — THE GAME */
(function(){
  function FeedRoom(){
    const {el}=window.NayaUI, K=window.NayaRoomKit, r=K.room('feed');
    const wrap=el('div','room-scene'); wrap.style.setProperty('--room-accent',r.accent);
    const top=el('div','room-toolbar between');
    const modes=K.segmented([
      {value:'collective',label:'COLLECTIVE'},
      {value:'personal',label:'PERSONAL'},
      {value:'activity',label:'ACTIVITY'}
    ],'collective',mode=>refresh(mode));
    const status=el('div','room-status-line','<span class="led"></span><span>LIVE INTELLIGENCE · PROVENANCE PRESERVED</span>');
    top.append(modes,status); wrap.appendChild(top);

    const intro=K.board(r.accent,'feed','The game','The living intelligence stream. Streams are sources; smart views are lenses.');
    intro.body.innerHTML='<p style="color:var(--ink-dim);font-size:13.5px;max-width:720px;line-height:1.55">Collective shows consented network intelligence, Personal shows intelligence scoped to you, and Activity shows operational change. Switching streams must change the underlying runtime query — never just the color.</p>';
    wrap.appendChild(intro);

    const zone=el('section','intelligence-list'); wrap.appendChild(zone);
    refresh('collective');
    return wrap;

    function refresh(stream){
      K.load(zone,'feed',{stream,limit:50},(payload,list,out)=>{
        const head=el('div','room-toolbar between');
        const count=el('div','room-status-line','<span class="led"></span><span>'+K.safe(list.length)+' QUALIFYING OBJECT'+(list.length===1?'':'S')+'</span>');
        const why=el('button','btn btn-ghost mini','<span>How ranking works</span>');
        why.style.setProperty('--btn-accent',r.accent);
        why.addEventListener('click',()=>window.NayaUI.toast('Ranking must be explainable from relevance, recency, context, relationships and verified learning — never mystery engagement logic.',r.accent));
        head.append(count,why); out.appendChild(head);
        const listWrap=el('div','intelligence-list');
        list.forEach(x=>listWrap.appendChild(K.intelCard(x,r.accent,{type:x?.category||x?.type||stream.toUpperCase(),onOpen:obj=>openObject(obj)})));
        out.appendChild(listWrap);
      },{
        title:stream==='activity'?'No activity in this scope':stream==='personal'?'Your stream is quiet':'The collective stream is quiet',
        body:'There is no qualifying canonical intelligence for this stream and current context.'
      });
    }

    async function openObject(obj){
      const id=obj?.intelligent_block_id||obj?.id;
      if(!id){window.NayaUI.toast('This item did not expose a canonical intelligence ID.',r.accent);return;}
      const res=await window.NayaRuntime.retrieve(id);
      if(!res.ok){window.NayaUI.toast(res.message||'Canonical detail is unavailable.',r.accent);return;}
      window.NayaUI.toast('Canonical intelligence retrieved. Detail-view projection is the next seam.',r.accent);
    }
  }
  window.NayaRooms=window.NayaRooms||{}; window.NayaRooms.feed=FeedRoom;
})();