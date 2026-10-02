/* YOUR REPORTS — THE FILM ROOM / TIME MACHINE */
(function(){
  function ReportsRoom(){
    const {el}=window.NayaUI, K=window.NayaRoomKit, r=K.room('reports');
    const wrap=el('div','room-scene'); wrap.style.setProperty('--room-accent',r.accent);
    const intro=K.board(r.accent,'report','Understand what your intelligence became','Day, week, month and year are different stories — not one template with a different date.');
    intro.body.innerHTML='<p style="color:var(--ink-dim);font-size:13.5px;line-height:1.6;max-width:760px">Reports synthesize change across time. Meaning comes first; evidence is always one layer away. Charts appear only when they clarify.</p>';
    wrap.appendChild(intro);
    const toolbar=el('div','room-toolbar between');
    const periods=K.segmented(['day','week','month','year'],'week',period=>refresh(period));
    toolbar.append(periods,el('div','room-status-line','<span class="led"></span><span>PERIODIC INTELLIGENCE · SOURCED</span>'));
    wrap.appendChild(toolbar);
    const zone=el('section','room-scene'); wrap.appendChild(zone);
    refresh('week'); return wrap;

    function refresh(period){
      K.load(zone,'reports',{period},(payload,list,out)=>{
        const cover=el('section','highlight');
        cover.innerHTML='<div class="eyebrow">'+K.safe(period.toUpperCase())+' INTELLIGENCE</div>'+
          '<h3>'+K.safe(payload.title||payload.heading||label(period))+'</h3>'+
          '<p>'+K.safe(payload.summary||payload.story||'Evidence-backed synthesis is available for this period.')+'</p>';
        out.appendChild(cover);

        const sections=payload.sections&&Array.isArray(payload.sections)?payload.sections:[];
        if(sections.length){
          const b=K.board(r.accent,'report','The story','Interpretation remains distinct from evidence');
          sections.forEach(s=>{
            const sec=el('section','report-section');
            sec.innerHTML='<h4>'+K.safe(s.title||s.name||'Section')+'</h4><p>'+K.safe(s.summary||s.text||s.content||'')+'</p>';
            b.body.appendChild(sec);
          });
          out.appendChild(b);
        }else if(list.length){
          const b=K.board(r.accent,'report','Evidence & intelligence','Canonical objects supporting this report');
          const l=el('div','intelligence-list');
          list.forEach(x=>l.appendChild(K.intelCard(x,r.accent,{type:x?.type||'REPORT EVIDENCE'})));
          b.body.appendChild(l); out.appendChild(b);
        }

        if(payload.evidence_count!==undefined||payload.verified!==undefined){
          const e=K.board(r.accent,'shield','Proof boundary','What supports this report');
          e.body.innerHTML='<div class="meta-row">'+
            (payload.evidence_count!==undefined?'<span>'+K.safe(payload.evidence_count)+' EVIDENCE OBJECTS</span>':'')+
            (payload.verified!==undefined?'<span>'+(payload.verified?'VERIFIED':'NOT VERIFIED')+'</span>':'')+
            '</div>';
          out.appendChild(e);
        }
      },{
        title:'No report is available for this period',
        body:'The system will not create a report without enough canonical intelligence and evidence.'
      });
    }
    function label(p){return p==='day'?'Today in intelligence':p==='week'?'This week\'s story':p==='month'?'Patterns this month':'Your year in intelligence';}
  }
  window.NayaRooms=window.NayaRooms||{}; window.NayaRooms.reports=ReportsRoom;
})();