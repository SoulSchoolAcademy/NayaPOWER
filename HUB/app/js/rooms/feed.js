/* SMART FEED — THE GAME.
   Director ruling 2026-10-02: the mode zone (Collective / Personal / Activity)
   lives in the shell and ONLY in the shell. This room is the river — it reads
   the shell's mode and never renders its own mode control.
   Director's enhancement 2026-10-02: the feed IS the presentation. No title
   wall, no explanatory board before the content — scroll, clean, premium. */
(function(){
  function FeedRoom(){
    const {el}=window.NayaUI, K=window.NayaRoomKit, r=K.room('feed');
    const R=window.NayaRuntime;
    const wrap=el('div','room-scene'); wrap.style.setProperty('--room-accent',r.accent);
    const top=el('div','room-toolbar between');
    const status=el('div','room-status-line','<span class="led"></span><span>LIVE INTELLIGENCE · PROVENANCE PRESERVED</span>');
    top.appendChild(status); wrap.appendChild(top);

    const zone=el('section','intelligence-list'); wrap.appendChild(zone);
    refresh();
    return wrap;

    function refresh(){
      const stream=R.mode||'collective';
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