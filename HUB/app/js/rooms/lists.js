/* SMART LISTS — THE MISSION TABLE */
(function(){
  function ListsRoom(){
    const {el}=window.NayaUI,K=window.NayaRoomKit,r=K.room('lists');
    const wrap=el('div','room-scene');wrap.style.setProperty('--room-accent',r.accent);
    const intro=K.board(r.accent,'lists','Action intelligence','Not a generic task manager. Every intelligent item should explain why it is here.');
    intro.body.innerHTML='<p style="color:var(--ink-dim);font-size:13.5px;line-height:1.6;max-width:760px">NOW · NEXT · WAITING · QUESTIONS · IDEAS · OPPORTUNITIES · COMPLETED organize references to canonical intelligence. The list never becomes another intelligence store.</p>';
    wrap.appendChild(intro);
    const zone=el('section','room-scene');wrap.appendChild(zone);
    K.load(zone,'lists',{view:'mission'},render,{title:'No intelligent lists yet',body:'Lists appear when the governed list service returns canonical references.'});
    return wrap;

    function render(payload,list,out){
      const lanes=['now','next','waiting','questions','ideas','opportunities','completed'];
      const byLane={};
      lanes.forEach(k=>byLane[k]=[]);
      list.forEach(x=>{const key=String(x.lane||x.status||x.bucket||'next').toLowerCase().replace(/\s+/g,'_');(byLane[key]||byLane.next).push(x);});
      if(payload.lanes&&typeof payload.lanes==='object'){
        Object.keys(payload.lanes).forEach(k=>{if(Array.isArray(payload.lanes[k]))byLane[k.toLowerCase()]=payload.lanes[k];});
      }
      const board=el('div','lane-board');
      lanes.forEach(lane=>{
        const col=el('section','lane');
        const items=byLane[lane]||[];
        col.innerHTML='<div class="lane-head"><span>'+K.safe(lane.toUpperCase())+'</span><span class="lane-count">'+K.safe(items.length)+'</span></div>';
        if(!items.length){
          col.insertAdjacentHTML('beforeend','<div class="why">Nothing qualifying here.</div>');
        }else items.forEach(x=>{
          const card=el('article','list-card');
          card.innerHTML='<b>'+K.safe(K.title(x,'Intelligence item'))+'</b>'+
            '<div class="why">'+K.safe(x.why||x.reason||x.why_here||'The runtime has not supplied an explanation yet.')+'</div>'+
            '<div class="meta-row">'+K.meta(x).map(m=>'<span>'+K.safe(m)+'</span>').join('')+'</div>';
          col.appendChild(card);
        });
        board.appendChild(col);
      });
      out.appendChild(board);
      const law=K.board(r.accent,'shield','Canonical-reference law','Lists organize intelligence; they do not copy it.');
      law.body.innerHTML='<p style="color:var(--muted);font-size:12.5px;line-height:1.55">Every list item must retain its canonical intelligence ID, provenance and supersession state. Smart membership must be explainable.</p>';
      out.appendChild(law);
    }
  }
  window.NayaRooms=window.NayaRooms||{};window.NayaRooms.lists=ListsRoom;
})();