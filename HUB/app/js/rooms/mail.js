/* SMART MAIL — THE SIGNAL ROOM */
(function(){
  function MailRoom(){
    const {el}=window.NayaUI,K=window.NayaRoomKit,r=K.room('mail');
    const wrap=el('div','room-scene');wrap.style.setProperty('--room-accent',r.accent);
    const intro=K.board(r.accent,'mail','Communication intelligence','Meaning and context first. No fake mailbox, ever.');
    intro.body.innerHTML='<p style="color:var(--ink-dim);font-size:13.5px;line-height:1.6;max-width:760px">The room separates what needs attention from noise and attaches relationship/project context. Drafting is assistance; sending remains a governed consequential action.</p>';
    wrap.appendChild(intro);
    const toolbar=el('div','room-toolbar between');
    const tabs=K.segmented([
      {value:'important',label:'IMPORTANT'},{value:'respond',label:'RESPOND'},{value:'follow_up',label:'FOLLOW UP'},
      {value:'drafts',label:'DRAFTS'},{value:'sent',label:'SENT'}
    ],'important',x=>refresh(x));
    toolbar.append(tabs,el('div','room-status-line','<span class="led"></span><span>REAL MESSAGES ONLY</span>'));wrap.appendChild(toolbar);
    const zone=el('section','room-scene');wrap.appendChild(zone);refresh('important');return wrap;

    function refresh(view){
      K.load(zone,'mail',{view},(payload,list,out)=>{
        const layout=el('div','mail-layout');
        const left=el('section','signal-list');
        const reader=K.board(r.accent,'mail','Message + context','Who · why it matters · related intelligence · response state');
        if(!list.length){
          left.innerHTML='<div class="empty-instrument"><strong>No messages in this view.</strong><p>The runtime returned no qualifying communication.</p></div>';
          reader.body.innerHTML='<div class="empty-instrument"><strong>No message selected.</strong><p>Select a real message when one is available.</p></div>';
        }else{
          list.slice(0,40).forEach((x,i)=>{
            const row=el('button','signal'+(i===0?' active':''));row.type='button';row.style.color='inherit';row.style.textAlign='left';row.style.cursor='pointer';
            row.innerHTML='<b>'+K.safe(K.title(x,'Message'))+'</b><span>'+K.safe(x.sender||x.from||x.reason||x.preview||'')+'</span>';
            row.addEventListener('click',()=>{[...left.children].forEach(n=>n.classList.remove('active'));row.classList.add('active');show(x,reader);});
            left.appendChild(row);
          });
          show(list[0],reader);
        }
        layout.append(left,reader);out.appendChild(layout);
      },{
        title:view==='drafts'?'No drafts':'No mail in this view',
        body:'The governed messaging runtime returned no qualifying messages. No sample inbox is shown.'
      });
    }
    function show(x,reader){
      const body=x.body||x.text||x.content||x.preview||'';
      reader.body.innerHTML='<div class="intel-type">'+K.safe(x.sender||x.from||'MESSAGE')+'</div>'+
        '<div class="intel-title">'+K.safe(K.title(x,'Message'))+'</div>'+
        '<div class="meta-row">'+K.meta(x).map(m=>'<span>'+K.safe(m)+'</span>').join('')+'</div>'+
        (body?'<div class="message-body" style="margin-top:16px">'+K.safe(typeof body==='string'?body:JSON.stringify(body))+'</div>':'')+
        '<div class="context-box"><div class="intel-type">CONTEXT</div><div class="intel-summary">'+
          K.safe(x.context||x.why_it_matters||x.relationship_context||'No verified contextual summary was supplied by the runtime.')+
        '</div></div>'+
        '<div class="action-row"><button class="btn btn-ghost mini" disabled><span>Draft response · runtime required</span></button></div>';
    }
  }
  window.NayaRooms=window.NayaRooms||{};window.NayaRooms.mail=MailRoom;
})();