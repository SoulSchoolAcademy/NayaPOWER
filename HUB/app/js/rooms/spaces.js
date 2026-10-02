/* SMART SPACES — THE WORLDS */
(function(){
  function SpacesRoom(){
    const {el}=window.NayaUI,K=window.NayaRoomKit,r=K.room('spaces');
    const wrap=el('div','room-scene');wrap.style.setProperty('--room-accent',r.accent);
    const intro=K.board(r.accent,'spaces','Context worlds','A Space changes context across the Hub; it never becomes a duplicate memory store.');
    intro.body.innerHTML='<p style="color:var(--ink-dim);font-size:13.5px;line-height:1.6;max-width:760px">Projects, people and areas of life become governed contexts for retrieval, interpretation and sharing. Switching Space must materially change scoped intelligence.</p>';
    wrap.appendChild(intro);
    const zone=el('section','room-scene');wrap.appendChild(zone);
    K.load(zone,'spaces',{view:'all'},render,{title:'No Spaces in this scope',body:'Create/manage Spaces through the governed context service. The Hub will not fabricate context worlds.'});
    return wrap;

    function render(payload,list,out){
      const grid=el('div','space-grid');
      list.forEach(x=>{
        const card=el('article','space-card');
        card.innerHTML='<div class="intel-type">'+K.safe(x.privacy||x.scope||'SPACE')+'</div>'+
          '<h3>'+K.safe(K.title(x,'Space'))+'</h3>'+
          '<p>'+K.safe(K.summary(x)||x.purpose||'Governed context')+'</p>'+
          '<div class="meta-row">'+
            (x.member_count!==undefined?'<span>'+K.safe(x.member_count)+' MEMBERS</span>':'')+
            (x.intelligence_count!==undefined?'<span>'+K.safe(x.intelligence_count)+' INTELLIGENCE</span>':'')+
            (x.updated_at?'<span>'+K.safe(x.updated_at)+'</span>':'')+
          '</div><div class="action-row"><button class="btn btn-ghost mini"><span>Enter Space</span></button></div>';
        const btn=card.querySelector('button');btn.style.setProperty('--btn-accent',r.accent);
        btn.addEventListener('click',()=>enter(x,out));
        grid.appendChild(card);
      });
      out.appendChild(grid);
      if(payload.active_space){
        const active=K.board(r.accent,'spaces','Active context',K.safe(payload.active_space.name||payload.active_space));
        active.body.innerHTML='<p style="color:var(--ink-dim);font-size:13px">This context should follow you into Feed, Today, Reports, Library, Lists, Mail, Connections and Ledger.</p>';
        out.appendChild(active);
      }
    }

    function enter(space,out){
      const id=space.id||space.space_id||space.name;
      K.load(out,'spaces',{view:'space',space:id},(payload,list,target)=>{
        const head=K.board(r.accent,'spaces',space.name||space.title||'Space',payload.purpose||space.purpose||'Active governed context');
        const metrics=el('div','metric-ribbon');
        const defs=[['intelligence_count','Intelligence'],['people_count','People'],['project_count','Projects'],['open_loops','Open loops']];
        let n=0;defs.forEach(([k,l])=>{if(payload[k]!==undefined){metrics.insertAdjacentHTML('beforeend','<div class="metric"><b>'+K.safe(payload[k])+'</b><span>'+l+'</span></div>');n++;}});
        if(n)head.body.appendChild(metrics);
        if(list.length){const l=el('div','intelligence-list');list.forEach(x=>l.appendChild(K.intelCard(x,r.accent)));head.body.appendChild(l);}
        target.appendChild(head);
      },{title:'Space is empty',body:'This context contains no qualifying intelligence yet.'});
    }
  }
  window.NayaRooms=window.NayaRooms||{};window.NayaRooms.spaces=SpacesRoom;
})();