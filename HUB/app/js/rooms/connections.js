/* YOUR CONNECTIONS — THE CONSTELLATION */
(function(){
  function ConnectionsRoom(){
    const {el}=window.NayaUI,K=window.NayaRoomKit,r=K.room('connections');
    const wrap=el('div','room-scene');wrap.style.setProperty('--room-accent',r.accent);
    const intro=K.board(r.accent,'nodes','Relationship intelligence','The graph supports understanding; it is never the product by itself.');
    intro.body.innerHTML='<p style="color:var(--ink-dim);font-size:13.5px;line-height:1.6;max-width:760px">People, Nayas, organizations and shared contexts are shown with explicit relationship and consent state. Connection never equals authority.</p>';
    wrap.appendChild(intro);
    const toolbar=el('div','room-toolbar between');
    const tabs=K.segmented([
      {value:'people',label:'PEOPLE'},{value:'agents',label:'AGENTS'},{value:'systems',label:'SYSTEMS'},
      {value:'organizations',label:'ORGS'},{value:'spaces',label:'SPACES'},{value:'pending',label:'PENDING'}
    ],'people',x=>refresh(x));
    toolbar.append(tabs,el('div','room-status-line','<span class="led"></span><span>GOVERNED RELATIONSHIPS</span>'));wrap.appendChild(toolbar);
    const zone=el('section','room-scene');wrap.appendChild(zone);refresh('people');return wrap;

    function refresh(category){
      K.load(zone,'connections',{category},(payload,list,out)=>{
        const layout=el('div','connection-layout');
        const map=el('div','constellation');
        const core=el('div','constellation-core',K.safe(payload.self_name||'YOU'));
        map.appendChild(core);
        const panel=K.board(r.accent,'nodes','Selected connection','Relationship · shared intelligence · recent context · consent');
        if(list.length){
          const selected=list[0];
          panel.body.innerHTML=detail(selected);
          const l=el('div','intelligence-list');
          list.slice(0,12).forEach((x,i)=>{
            const row=el('button','intel-row');row.type='button';row.style.color='inherit';row.style.textAlign='left';row.style.cursor='pointer';
            row.innerHTML='<div class="intel-type">'+K.safe(x.type||category)+'</div><div class="intel-title">'+K.safe(K.title(x,'Connection'))+'</div>'+
              '<div class="meta-row">'+K.meta(x).map(m=>'<span>'+K.safe(m)+'</span>').join('')+'</div>';
            row.addEventListener('click',()=>panel.body.innerHTML=detail(x));
            l.appendChild(row);
          });
          map.appendChild(l);
        }else panel.body.innerHTML='<div class="empty-instrument"><strong>No selected relationship.</strong><p>The runtime returned no governed connection in this category.</p></div>';
        layout.append(map,panel);out.appendChild(layout);
      },{title:'No governed connections in this category',body:'Nothing is invented. A relationship appears only when the canonical relationship/consent layer returns it.'});
    }
    function detail(x){
      const shared=x.shared_intelligence_count??x.shared_count;
      return '<div class="intel-title">'+K.safe(K.title(x,'Connection'))+'</div>'+
        '<div class="intel-summary">'+K.safe(K.summary(x)||x.relationship||'Governed relationship')+'</div>'+
        '<div class="meta-row">'+
          (x.relationship?'<span>'+K.safe(x.relationship)+'</span>':'')+
          (x.consent_state?'<span>'+K.safe(x.consent_state)+'</span>':'')+
          (shared!==undefined?'<span>'+K.safe(shared)+' SHARED OBJECTS</span>':'')+
          (x.last_activity?'<span>'+K.safe(x.last_activity)+'</span>':'')+
        '</div>'+
        (x.next_action?'<div class="context-box"><div class="intel-type">NEXT RELEVANT ACTION</div><div class="intel-summary">'+K.safe(x.next_action)+'</div></div>':'');
    }
  }
  window.NayaRooms=window.NayaRooms||{};window.NayaRooms.connections=ConnectionsRoom;
})();