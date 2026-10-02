/* YOUR INTELLIGENCE TODAY — THE HIGHLIGHT REEL
   Canonical room contract: HUB/ROOMS/02-TODAY.md
   NOW → NEXT → WATCH → LEARNED → WAITING → RECENT PROOF.
   This room projects governed intelligence; it never fabricates a daily story. */
(function(){
  function TodayRoom(){
    const UI=window.NayaUI, K=window.NayaRoomKit, R=window.NayaRuntime;
    const el=UI.el, Icons=UI.Icons, r=K.room('today');
    const wrap=el('div','room-scene today-room');
    wrap.style.setProperty('--room-accent',r.accent);

    const now=new Date();
    const dateKey=now.toISOString().slice(0,10);
    const intro=K.board(
      r.accent,
      'spark',
      'Your intelligence, distilled',
      now.toLocaleDateString(undefined,{weekday:'long',year:'numeric',month:'long',day:'numeric'})
    );
    intro.classList.add('today-intro');
    intro.body.innerHTML=
      '<p class="today-intro-copy">Naya sorts the day before asking you to sort it. '+
      'Start with what matters now, take the next useful move, and open evidence only when you need depth.</p>';
    wrap.appendChild(intro);

    const status=el('div','room-toolbar between today-toolbar');
    const stamp=el('div','room-status-line',
      '<span class="led" aria-hidden="true"></span><span>TODAY · CANONICAL INTELLIGENCE ONLY</span>');
    const refresh=el('button','btn btn-ghost today-refresh',Icons.icon('arrow')+'<span>Refresh</span>');
    refresh.type='button';
    refresh.style.setProperty('--btn-accent',r.accent);
    refresh.addEventListener('click',load);
    status.append(stamp,refresh);
    wrap.appendChild(status);

    const zone=el('section','room-scene today-zone');
    zone.setAttribute('aria-label','Your intelligence today');
    wrap.appendChild(zone);

    let detailHost=null;
    load();
    return wrap;

    async function load(){
      zone.setAttribute('aria-busy','true');
      zone.innerHTML='';
      const shimmer=el('div','shimmer-grid today-loading');
      for(let i=0;i<3;i++){
        const s=el('div','shimmer');
        s.style.setProperty('--room-accent',r.accent);
        shimmer.appendChild(s);
      }
      zone.appendChild(shimmer);

      let res;
      try{
        res=await R.roomData('today',{date:dateKey,mode:'canonical_today'});
      }catch(err){
        res={ok:false,state:'error',message:err&&err.message?err.message:'Your Intelligence Today could not load.'};
      }
      zone.setAttribute('aria-busy','false');

      if(!res||!res.ok){
        if(res&&res.state==='empty'){
          K.empty(zone,'today','A quiet day can stay quiet',
            'No qualifying intelligence exists for this date and scope. Naya will not manufacture a highlight reel.');
        }else if(res&&res.state==='error'){
          K.state(zone,'today','Today could not load',res.message||'The governed runtime returned an error.',[
            {label:'Try again',icon:'arrow',onClick:load}
          ]);
        }else{
          K.unavailable(zone,'today',res&&res.message?res.message:undefined);
        }
        return;
      }

      const payload=res.data!==undefined?res.data:res;
      const model=buildModel(payload);
      if(!model.hasAny){
        K.empty(zone,'today','Nothing meaningful needs your attention',
          'The runtime is connected, but it returned no canonical NOW, NEXT, WATCH, LEARNED, WAITING or proof intelligence for this date.');
        return;
      }
      renderModel(model,payload);
    }

    function buildModel(payload){
      const root=(payload&&payload.data&&typeof payload.data==='object'&&!Array.isArray(payload.data))?payload.data:(payload||{});
      const sections=(root.sections&&typeof root.sections==='object')?root.sections:{};
      const list=unique([].concat(
        toArray(root.items),
        toArray(root.highlights),
        toArray(root.intelligence),
        K.items(root)
      ));

      const tagged={now:[],next:[],watch:[],learned:[],waiting:[],proof:[],other:[]};
      list.forEach(item=>{
        const tag=String(item&&(
          item.section||item.bucket||item.type||item.category||item.kind||item.status_type
        )||'').toLowerCase();
        if(/(^|\b)(now|current|focus|priority)(\b|$)/.test(tag)) tagged.now.push(item);
        else if(/(^|\b)(next|action|move|todo)(\b|$)/.test(tag)) tagged.next.push(item);
        else if(/(^|\b)(watch|risk|blocker|warning)(\b|$)/.test(tag)) tagged.watch.push(item);
        else if(/learn|lesson|change/.test(tag)) tagged.learned.push(item);
        else if(/wait|depend|pending|open[_ -]?loop/.test(tag)) tagged.waiting.push(item);
        else if(/proof|evidence|receipt|verif/.test(tag)) tagged.proof.push(item);
        else tagged.other.push(item);
      });

      const nowItems=firstNonEmpty(
        values(root,sections,['now','current','focus','priority','top']),
        tagged.now
      );
      const next=firstNonEmpty(
        values(root,sections,['next','next_moves','moves','actions']),
        tagged.next
      );
      const watch=firstNonEmpty(
        values(root,sections,['watch','risks','risk','blockers','warnings']),
        tagged.watch
      );
      const learned=firstNonEmpty(
        values(root,sections,['learned','learning','learnings','lessons','changes']),
        tagged.learned
      );
      const waiting=firstNonEmpty(
        values(root,sections,['waiting','dependencies','pending','open_loops','carry_forward']),
        tagged.waiting
      );
      const proof=firstNonEmpty(
        values(root,sections,['recent_proof','proof','receipts','evidence','verified']),
        tagged.proof
      );

      let current=nowItems[0]||null;
      const synthesis=textValue(root.summary||root.synthesis||root.briefing);
      if(!current&&synthesis){
        current={
          title:'Today, distilled',
          summary:synthesis,
          truth_state:root.truth_state||root.state||'SYNTHESIS'
        };
      }

      const unclassified=tagged.other.filter(item=>
        !containsItem(nowItems,item)&&!containsItem(next,item)&&!containsItem(watch,item)&&
        !containsItem(learned,item)&&!containsItem(waiting,item)&&!containsItem(proof,item)
      );

      const reflection=textValue(root.reflection||root.naya_reflection);
      return {
        current:current,
        next:next,
        watch:watch,
        learned:learned,
        waiting:waiting,
        proof:proof,
        unclassified:unclassified,
        reflection:reflection,
        hasAny:!!current||next.length>0||watch.length>0||learned.length>0||
          waiting.length>0||proof.length>0||unclassified.length>0||!!reflection
      };
    }

    function renderModel(model,payload){
      zone.innerHTML='';

      const arc=el('nav','today-arc');
      arc.setAttribute('aria-label',"Today's intelligence arc");
      const arcItems=[
        ['now','NOW',model.current?1:0],
        ['next','NEXT',model.next.length],
        ['watch','WATCH',model.watch.length],
        ['learned','LEARNED',model.learned.length],
        ['waiting','WAITING',model.waiting.length],
        ['proof','RECENT PROOF',model.proof.length]
      ];
      arcItems.forEach(([id,label,count])=>{
        const b=el('button','today-arc-step');
        b.type='button';
        b.disabled=count===0;
        b.setAttribute('aria-label',label+(count?': '+count+' item'+(count===1?'':'s'):': no verified items'));
        b.innerHTML='<span class="today-arc-dot" aria-hidden="true"></span><span>'+K.safe(label)+'</span>'+
          '<strong>'+K.safe(count)+'</strong>';
        b.addEventListener('click',()=>{
          const target=zone.querySelector('#today-'+id);
          if(target) target.scrollIntoView({behavior:reducedMotion()?'auto':'smooth',block:'start'});
        });
        arc.appendChild(b);
      });
      zone.appendChild(arc);

      const hero=el('section','today-now');
      hero.id='today-now';
      hero.setAttribute('aria-labelledby','today-now-heading');
      if(model.current){
        const item=model.current;
        hero.innerHTML=
          '<div class="today-now-glow" aria-hidden="true"></div>'+
          '<div class="today-kicker">NOW</div>'+
          '<h3 id="today-now-heading">'+K.safe(K.title(item,'What matters now'))+'</h3>'+
          (K.summary(item)?'<p class="today-now-summary">'+K.safe(K.summary(item))+'</p>':'')+
          '<div class="today-meta">'+metaHtml(item)+'</div>'+
          '<div class="today-actions"></div>';
        const actions=hero.querySelector('.today-actions');
        actions.appendChild(inspectButton(item,'Inspect context'));
        const evidence=evidenceButton(item);
        if(evidence) actions.appendChild(evidence);
      }else{
        hero.innerHTML=
          '<div class="today-kicker">NOW</div>'+
          '<h3 id="today-now-heading">No verified NOW item</h3>'+
          '<p class="today-now-summary">The runtime returned useful intelligence for today, but did not identify one canonical current priority. Naya will not invent one.</p>';
      }
      zone.appendChild(hero);

      const primary=el('div','today-primary-grid');
      primary.appendChild(sectionBlock('next','NEXT','What should move now',model.next,{
        empty:'No verified next move was returned.',
        action:'ask'
      }));
      primary.appendChild(sectionBlock('watch','WATCH','Risks, blockers and changes worth attention',model.watch,{
        empty:'No verified watch item was returned.'
      }));
      zone.appendChild(primary);

      const secondary=el('div','today-secondary-grid');
      secondary.appendChild(sectionBlock('learned','LEARNED','What changed because of experience',model.learned,{
        empty:'No verified learning item was returned.'
      }));
      secondary.appendChild(sectionBlock('waiting','WAITING','Dependencies that should not disappear',model.waiting,{
        empty:'Nothing is currently marked as a verified waiting dependency.'
      }));
      zone.appendChild(secondary);

      zone.appendChild(sectionBlock('proof','RECENT PROOF','Receipts and evidence behind recent consequential claims',model.proof,{
        empty:'No recent proof object was returned for this view.',
        compact:true,
        evidenceOnly:true
      }));

      if(model.reflection){
        const reflection=el('aside','today-reflection');
        reflection.innerHTML=
          '<div class="today-kicker">NAYA · INTERPRETATION</div>'+
          '<blockquote>'+K.safe(model.reflection)+'</blockquote>'+
          '<p>Interpretation is subordinate to the canonical intelligence above. Open evidence before treating it as proof.</p>';
        zone.appendChild(reflection);
      }

      if(model.unclassified.length){
        const notice=el('section','today-unclassified');
        notice.innerHTML=
          '<div class="today-kicker">RUNTIME CONTRACT NOTICE</div>'+
          '<h3>Returned intelligence needs section classification</h3>'+
          '<p>The governed runtime returned '+K.safe(model.unclassified.length)+
          ' item'+(model.unclassified.length===1?'':'s')+
          ' without a canonical NOW / NEXT / WATCH / LEARNED / WAITING / PROOF label. They are shown below without guessing their meaning.</p>';
        const listWrap=el('div','today-unclassified-list');
        model.unclassified.slice(0,8).forEach(item=>listWrap.appendChild(itemCard(item,{label:'UNCLASSIFIED'})));
        notice.appendChild(listWrap);
        zone.appendChild(notice);
      }

      detailHost=el('section','today-inspector');
      detailHost.setAttribute('aria-live','polite');
      detailHost.hidden=true;
      zone.appendChild(detailHost);

      const sourceState=payload&&(
        payload.truth_state||payload.state||payload.verification_state||payload.epistemic_state
      );
      if(sourceState){
        const footer=el('div','today-truth-footer',
          '<span>Projection state</span><strong>'+K.safe(sourceState)+'</strong>');
        zone.appendChild(footer);
      }
    }

    function sectionBlock(id,label,description,items,opts){
      const section=el('section','today-section'+(opts&&opts.compact?' compact':''));
      section.id='today-'+id;
      section.setAttribute('aria-labelledby','today-'+id+'-heading');
      section.innerHTML=
        '<div class="today-section-head">'+
          '<div><div class="today-kicker">'+K.safe(label)+'</div>'+
          '<h3 id="today-'+id+'-heading">'+K.safe(description)+'</h3></div>'+
          '<span class="today-count" aria-label="'+K.safe(items.length)+' items">'+K.safe(items.length)+'</span>'+
        '</div>';
      const listWrap=el('div','today-section-list');
      if(items.length){
        items.slice(0,8).forEach((item,index)=>{
          listWrap.appendChild(itemCard(item,{
            label:label,
            primary:index===0&&id==='next',
            action:opts&&opts.action,
            evidenceOnly:opts&&opts.evidenceOnly
          }));
        });
      }else{
        listWrap.appendChild(el('div','today-section-empty',
          '<span class="today-empty-mark" aria-hidden="true">—</span><span>'+K.safe(opts&&opts.empty?opts.empty:'No verified items returned.')+'</span>'));
      }
      section.appendChild(listWrap);
      return section;
    }

    function itemCard(item,opts){
      const card=el('article','today-item'+(opts&&opts.primary?' primary':''));
      const title=K.title(item,opts&&opts.label?opts.label:'Intelligence');
      card.innerHTML=
        '<div class="today-item-copy">'+
          '<div class="today-item-label">'+K.safe(opts&&opts.label?opts.label:'INTELLIGENCE')+'</div>'+
          '<h4>'+K.safe(title)+'</h4>'+
          (K.summary(item)?'<p>'+K.safe(K.summary(item))+'</p>':'')+
          '<div class="today-meta">'+metaHtml(item)+'</div>'+
        '</div>'+
        '<div class="today-item-actions"></div>';
      const actions=card.querySelector('.today-item-actions');
      if(!(opts&&opts.evidenceOnly)) actions.appendChild(inspectButton(item,'Inspect'));
      const ev=evidenceButton(item);
      if(ev) actions.appendChild(ev);
      if(opts&&opts.action==='ask'){
        const ask=el('button','btn today-action');
        ask.type='button';
        ask.style.setProperty('--btn-accent',r.accent);
        ask.innerHTML=Icons.icon('spark')+'<span>Ask Naya to help</span>';
        ask.addEventListener('click',()=>askNaya(item,ask));
        actions.appendChild(ask);
      }
      return card;
    }

    function inspectButton(item,label){
      const b=el('button','btn btn-ghost today-action');
      b.type='button';
      b.style.setProperty('--btn-accent',r.accent);
      b.innerHTML=Icons.icon('search')+'<span>'+K.safe(label)+'</span>';
      b.addEventListener('click',()=>inspectItem(item,b));
      return b;
    }

    function evidenceButton(item){
      const id=canonicalId(item);
      const evidence=item&&(
        item.evidence_ref||item.evidence_id||item.receipt_id||item.proof_id||
        item.provenance_ref||item.provenance_id
      );
      if(!id&&!evidence) return null;
      const b=el('button','btn btn-ghost today-action');
      b.type='button';
      b.style.setProperty('--btn-accent',r.accent);
      b.innerHTML=Icons.icon('shield')+'<span>Evidence</span>';
      b.addEventListener('click',()=>inspectItem(item,b,true));
      return b;
    }

    async function inspectItem(item,button,evidenceOnly){
      const id=(evidenceOnly&&item&&(
        item.evidence_ref||item.evidence_id||item.receipt_id||item.proof_id||item.provenance_ref||item.provenance_id
      ))||canonicalId(item);
      if(!id){
        presentInspector('Context is not retrievable yet',
          'This projected item has no canonical retrieval identifier. The Hub will not pretend an evidence path exists.',
          'NOT_VERIFIED');
        return;
      }
      setBusy(button,true);
      const res=await R.retrieve(id);
      setBusy(button,false);
      if(!res||!res.ok){
        presentInspector(evidenceOnly?'Evidence is not available':'Canonical context is not available',
          res&&res.message?res.message:'The governed runtime did not return a retrievable object.',
          res&&res.state?res.state:'NOT_VERIFIED');
        return;
      }
      const data=res.data!==undefined?res.data:res;
      const object=(data&&data.data&&typeof data.data==='object')?data.data:data;
      presentInspector(
        K.title(object,evidenceOnly?'Evidence':'Canonical intelligence'),
        K.summary(object)||'The canonical object was retrieved. No additional human-readable summary was returned.',
        object&&(
          object.truth_state||object.verification_state||object.epistemic_state||object.state
        )||'RETRIEVED',
        object
      );
    }

    async function askNaya(item,button){
      const title=K.title(item,'this next move');
      setBusy(button,true);
      const res=await R.search(
        'Help me take the next useful step on: '+title,
        {room:'today',context_id:canonicalId(item)||undefined,intent:'HELP_ACT_ON_NEXT_MOVE'}
      );
      setBusy(button,false);
      if(!res||!res.ok){
        presentInspector('Naya cannot help with this move yet',
          res&&res.message?res.message:'The governed Naya runtime is not available for this action.',
          res&&res.state?res.state:'NOT_VERIFIED');
        return;
      }
      const data=res.data!==undefined?res.data:res;
      const message=textValue(data&&(
        data.answer||data.summary||data.text||data.message
      ))||'Naya returned a result without a human-readable response.';
      presentInspector('Naya · next move support',message,
        data&&(
          data.truth_state||data.verification_state||data.epistemic_state||data.state
        )||'READY',
        data
      );
    }

    function presentInspector(title,body,state,obj){
      if(!detailHost) return;
      detailHost.hidden=false;
      detailHost.innerHTML=
        '<div class="today-inspector-head">'+
          '<div><div class="today-kicker">CONTEXT / PROOF</div><h3>'+K.safe(title)+'</h3></div>'+
          '<span class="today-truth-chip">'+K.safe(String(state||'UNKNOWN').toUpperCase())+'</span>'+
        '</div>'+
        '<p>'+K.safe(body)+'</p>'+
        (obj?'<div class="today-meta">'+metaHtml(obj)+'</div>':'');
      detailHost.scrollIntoView({behavior:reducedMotion()?'auto':'smooth',block:'nearest'});
    }

    function metaHtml(item){
      const parts=K.meta(item);
      if(!parts.length) return '<span>NO EXTRA METADATA</span>';
      return parts.map(x=>'<span>'+K.safe(x)+'</span>').join('');
    }

    function canonicalId(item){
      if(!item||typeof item!=='object') return null;
      return item.intelligent_block_id||item.canonical_id||item.object_id||item.id||null;
    }

    function values(root,sections,keys){
      for(const key of keys){
        if(root&&root[key]!=null) return toArray(root[key]);
        if(sections&&sections[key]!=null) return toArray(sections[key]);
      }
      return [];
    }

    function toArray(v){
      if(v==null||v===false) return [];
      if(Array.isArray(v)) return v.filter(Boolean);
      if(typeof v==='object') return [v];
      if(typeof v==='string'&&v.trim()) return [{title:v}];
      return [];
    }

    function firstNonEmpty(a,b){ return a&&a.length?a:(b||[]); }

    function unique(items){
      const out=[], seen=new Set();
      items.filter(Boolean).forEach(item=>{
        const key=(item&&typeof item==='object')?
          (canonicalId(item)||JSON.stringify([item.title,item.name,item.subject,item.type,item.category,item.created_at])):String(item);
        if(!seen.has(key)){seen.add(key);out.push(item);}
      });
      return out;
    }

    function containsItem(list,item){
      const id=canonicalId(item);
      return list.some(x=>x===item||(id&&canonicalId(x)===id));
    }

    function textValue(v){
      if(v==null) return '';
      if(typeof v==='string') return v;
      if(typeof v==='number'||typeof v==='boolean') return String(v);
      if(typeof v==='object') return v.text||v.summary||v.description||v.human||'';
      return '';
    }

    function setBusy(button,busy){
      if(!button) return;
      button.disabled=!!busy;
      button.setAttribute('aria-busy',busy?'true':'false');
    }

    function reducedMotion(){
      return !!(window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches);
    }
  }

  window.NayaRooms=window.NayaRooms||{};
  window.NayaRooms.today=TodayRoom;
})();