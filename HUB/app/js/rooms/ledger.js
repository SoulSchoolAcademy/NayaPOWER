/* SMART LEDGER — THE BLACK BOX / PROOF ROOM */
(function(){
  function LedgerRoom(){
    const {el}=window.NayaUI,K=window.NayaRoomKit,r=K.room('ledger');
    const wrap=el('div','room-scene');wrap.style.setProperty('--room-accent',r.accent);
    const intro=K.board(r.accent,'ledger','The durable record of what happened','Requested, authorized, executed, observed and verified are different states.');
    intro.body.innerHTML='<p style="color:var(--ink-dim);font-size:13.5px;line-height:1.6;max-width:760px">This is the human proof surface — not accounting and not a raw log dump. Executor success never silently becomes verification.</p>';
    wrap.appendChild(intro);
    const toolbar=el('div','room-toolbar between');
    const filters=K.segmented(['all','actions','decisions','shares','connections','system'],'all',f=>refresh(f));
    toolbar.append(filters,el('div','room-status-line','<span class="led"></span><span>PROVENANCE · AUTHORITY · OUTCOME</span>'));wrap.appendChild(toolbar);
    const zone=el('section','room-scene');wrap.appendChild(zone);refresh('all');return wrap;

    function refresh(filter){
      K.load(zone,'ledger',{filter,limit:100},(payload,list,out)=>{
        const health=K.board(r.accent,'shield','Trust state',payload.summary||'Every consequential chain remains inspectable.');
        health.body.innerHTML='<div class="metric-ribbon">'+
          metric('Receipts',payload.receipt_count??list.length)+
          (payload.verified_count!==undefined?metric('Verified',payload.verified_count):'')+
          (payload.needs_attention!==undefined?metric('Needs attention',payload.needs_attention):'')+
          '</div>';
        out.appendChild(health);
        const timeline=el('div','timeline');
        list.forEach(x=>{
          const item=el('article','timeline-item');
          const stages=x.stages||x.stage_chain||['RECEIVED',x.authorized!==false?'AUTHORIZED':null,x.executed?'EXECUTED':null,x.observed?'OBSERVED':null,x.verified?'VERIFIED':null].filter(Boolean);
          item.innerHTML='<div class="intel-type">'+K.safe(x.type||x.action||'EVENT')+'</div>'+
            '<div class="intel-title">'+K.safe(K.title(x,x.action||'Ledger event'))+'</div>'+
            (K.summary(x)?'<div class="intel-summary">'+K.safe(K.summary(x))+'</div>':'')+
            '<div class="meta-row">'+K.meta(x).map(m=>'<span>'+K.safe(m)+'</span>').join('')+'</div>'+
            '<div class="stage-chain">'+stages.map(s=>'<span>'+K.safe(s)+'</span>').join('')+'</div>';
          timeline.appendChild(item);
        });
        out.appendChild(timeline);
      },{title:'No receipted activity in this scope',body:'There are no canonical ledger events to show for this filter.'});
    }
    function metric(label,value){return '<div class="metric"><b>'+K.safe(value)+'</b><span>'+K.safe(label)+'</span></div>';}
  }
  window.NayaRooms=window.NayaRooms||{};window.NayaRooms.ledger=LedgerRoom;
})();