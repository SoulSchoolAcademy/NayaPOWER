/* YOUR INTELLIGENCE TODAY — THE HIGHLIGHT REEL */
(function(){
  function TodayRoom(){
    const {el}=window.NayaUI, K=window.NayaRoomKit, r=K.room('today');
    const wrap=el('div','room-scene'); wrap.style.setProperty('--room-accent',r.accent);
    const now=new Date();
    const intro=K.board(r.accent,'spark','Your day, distilled',now.toLocaleDateString(undefined,{weekday:'long',year:'numeric',month:'long',day:'numeric'}));
    intro.body.innerHTML='<p style="color:var(--ink-dim);font-size:14px;line-height:1.6;max-width:720px">The highlight reel of the game: what changed, what mattered, what was learned, what remains open, and what should carry forward. Every statement must resolve to evidence.</p>';
    wrap.appendChild(intro);

    const toolbar=el('div','room-toolbar between');
    const modes=K.segmented([
      {value:'summary',label:'HIGHLIGHTS'},
      {value:'collective',label:'COLLECTIVE'},
      {value:'personal',label:'PERSONAL'},
      {value:'activity',label:'ACTIVITY'}
    ],'summary',mode=>refresh(mode));
    const stamp=el('div','room-status-line','<span class="led"></span><span>TODAY · EVIDENCE-BASED</span>');
    toolbar.append(modes,stamp); wrap.appendChild(toolbar);

    const zone=el('section','room-scene'); wrap.appendChild(zone);
    refresh('summary');
    return wrap;

    function refresh(mode){
      K.load(zone,'today',{date:now.toISOString().slice(0,10),mode},(payload,list,out)=>{
        if(mode!=='summary'){
          const listWrap=el('div','intelligence-list');
          list.forEach(x=>listWrap.appendChild(K.intelCard(x,r.accent,{type:x?.type||x?.category||mode.toUpperCase()})));
          out.appendChild(listWrap); return;
        }

        const metrics=payload.metrics||payload.pulse||{};
        const ribbon=el('section','metric-ribbon');
        const defs=[
          ['events','Events'],['discoveries','Discoveries'],['learning','Learning'],['decisions','Decisions'],['creations','Creations']
        ];
        let metricCount=0;
        defs.forEach(([key,label])=>{
          if(metrics[key]!==undefined&&metrics[key]!==null){
            const m=el('div','metric'); m.innerHTML='<b>'+K.safe(metrics[key])+'</b><span>'+K.safe(label)+'</span>'; ribbon.appendChild(m); metricCount++;
          }
        });
        if(metricCount) out.appendChild(ribbon);

        const story=el('div','story-grid');
        const stack=el('div','story-stack');
        const highlights=Array.isArray(payload.highlights)?payload.highlights:list;
        highlights.slice(0,8).forEach((x,i)=>{
          const h=el('article','highlight');
          h.innerHTML='<div class="eyebrow">'+K.safe(x?.type||x?.category||('HIGHLIGHT '+(i+1)))+'</div>'+
            '<h3>'+K.safe(K.title(x,'What changed'))+'</h3>'+
            (K.summary(x)?'<p>'+K.safe(K.summary(x))+'</p>':'')+
            '<div class="meta-row">'+K.meta(x).map(m=>'<span>'+K.safe(m)+'</span>').join('')+'</div>';
          stack.appendChild(h);
        });
        if(!highlights.length){
          const q=el('div','empty-instrument','<strong>A quiet day can stay quiet.</strong><p>No verified highlight was manufactured just to fill the page.</p>');
          stack.appendChild(q);
        }

        const reflection=el('aside','reflection');
        const text=payload.reflection||payload.naya_reflection||payload.summary||'';
        reflection.innerHTML='<div class="intel-type">NAYA\'S REFLECTION</div>'+
          '<div class="quote">'+(text?K.safe(typeof text==='string'?text:(text.text||text.summary||'')):'No evidence-grounded reflection is available yet.')+'</div>'+
          '<small>Interpretation must remain traceable to today\'s canonical intelligence.</small>';
        story.append(stack,reflection); out.appendChild(story);

        const carry=payload.open_loops||payload.carry_forward||payload.tomorrow;
        if(carry){
          const b=K.board(r.accent,'clock','Open loops · carry forward','What should not be lost when today becomes tomorrow');
          const vals=Array.isArray(carry)?carry:[carry];
          b.body.innerHTML='<div class="intelligence-list">'+vals.map(x=>'<div class="intel-row"><div class="intel-title">'+K.safe(typeof x==='string'?x:K.title(x,'Open loop'))+'</div></div>').join('')+'</div>';
          out.appendChild(b);
        }
      },{
        title:'No meaningful highlights yet',
        body:'There is no verified daily intelligence for this date and scope. The room will not manufacture a day.'
      });
    }
  }
  window.NayaRooms=window.NayaRooms||{}; window.NayaRooms.today=TodayRoom;
})();