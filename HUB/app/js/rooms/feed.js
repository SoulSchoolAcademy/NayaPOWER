/* SMART FEED — THE GAME (Room 01, living contract HUB/ROOMS/01-FEED.md)
   Composition grammar: mode control → focused orientation → intelligence river → why-now per object.
   Truth rules: never fabricate liveness, counts, or personalization. The "new" seam is driven by a
   real client seen-set (localStorage); UNKNOWN/BLOCKED states are shown distinctly, never as success. */
(function(){
  function FeedRoom(){
    const {el}=window.NayaUI, K=window.NayaRoomKit, r=K.room('feed');
    const wrap=el('div','room-scene'); wrap.style.setProperty('--room-accent',r.accent);

    /* 1 — Mode + room identity (sticky, thumb-reachable). Switching modes re-queries the runtime. */
    const top=el('div','room-toolbar between feed-toolbar');
    const modes=K.segmented([
      {value:'personal',label:'PERSONAL'},
      {value:'collective',label:'COLLECTIVE'},
      {value:'activity',label:'ACTIVITY'}
    ],'personal',mode=>refresh(mode));
    const status=el('div','room-status-line','<span class="led"></span><span>LIVE INTELLIGENCE · PROVENANCE PRESERVED</span>');
    top.append(modes,status); wrap.appendChild(top);

    /* 2 — Focused orientation: slim Naya narration line (real state only) + one-line orientation. */
    const nayaLine=el('div','feed-naya-line'); nayaLine.setAttribute('aria-live','polite'); wrap.appendChild(nayaLine);
    const orient=el('div','room-orient','Personal shows intelligence scoped to you · Collective shows consented network intelligence · Activity shows operational change. Switching streams changes the underlying runtime query — never just the color.');
    wrap.appendChild(orient);

    /* 3 — The river owns the canvas. */
    const zone=el('section','intelligence-list'); zone.setAttribute('aria-label','Intelligence river'); wrap.appendChild(zone);
    refresh('personal');
    return wrap;

    /* ---- seen-set: the only "new" signal. Real client state, never fake liveness. ---- */
    function seenKey(stream){return 'nayanet.feed.seen.'+stream;}
    function getSeen(stream){try{return new Set(JSON.parse(localStorage.getItem(seenKey(stream))||'[]'));}catch(e){return new Set();}}
    function putSeen(stream,ids){try{localStorage.setItem(seenKey(stream),JSON.stringify(Array.from(ids).slice(-300)));}catch(e){}}
    function itemId(x){return x?.intelligent_block_id||x?.id||null;}

    function normTruth(x){
      const t=String(x?.truth_state||x?.state||'').toUpperCase().trim();
      if(!t) return 'UNKNOWN';
      if(t==='VERIFIED') return 'VERIFIED';
      if(t.indexOf('NOT_VERIFIED')>=0||t.indexOf('UNVERIFIED')>=0) return 'NOT_VERIFIED';
      return t;
    }
    function truthLabel(t){
      if(t==='VERIFIED') return 'Verified';
      if(t==='NOT_VERIFIED') return 'Not verified';
      if(t==='UNKNOWN') return 'Unknown';
      return t.charAt(0)+t.slice(1).toLowerCase().replace(/_/g,' ');
    }
    function sourceName(x){
      const s=x?.source; if(!s) return '';
      return typeof s==='string'?s:(s.name||'');
    }
    /* Why-now: explicit rationale when the object carries one; otherwise the true,
       inspectable facts (source · truth · time). Never invented. */
    function whyNowText(x){
      const explicit=x?.why_now||x?.why||x?.relevance_reason||x?.surfacing_reason;
      if(explicit) return String(explicit);
      const parts=[];
      const src=sourceName(x); if(src) parts.push('via '+src);
      parts.push(truthLabel(normTruth(x)).toLowerCase());
      const when=x?.created_at||x?.timestamp||x?.time; if(when) parts.push(String(when));
      return parts.length?parts.join(' · '):'rationale on request';
    }

    function refresh(stream){
      K.load(zone,'feed',{stream,limit:50},(payload,list,out)=>{
        const seen=getSeen(stream);
        const ids=list.map(itemId).filter(Boolean);
        const fresh=list.filter(x=>{const id=itemId(x);return id&&!seen.has(id);});
        const freshVerified=fresh.filter(x=>normTruth(x)==='VERIFIED');

        /* Naya narration — computed from real diff, nothing fabricated. */
        nayaLine.innerHTML='';
        if(list.length){
          const jewel=el('span','feed-naya-jewel','✦');
          const msg=fresh.length
            ? (freshVerified.length
                ? freshVerified.length+' new verified item'+(freshVerified.length===1?'':'s')+' since your last visit'+(fresh.length>freshVerified.length?' · '+(fresh.length-freshVerified.length)+' more awaiting verification':'')
                : fresh.length+' new item'+(fresh.length===1?'':'s')+' since your last visit · none verified yet')
            : 'You are caught up on this stream.';
          nayaLine.append(jewel,el('span','',K.safe(msg)));
        }

        const head=el('div','room-toolbar between');
        const count=el('div','room-status-line','<span class="led"></span><span>'+K.safe(list.length)+' QUALIFYING OBJECT'+(list.length===1?'':'S')+'</span>');
        const why=el('button','btn btn-ghost mini','<span>How ranking works</span>');
        why.style.setProperty('--btn-accent',r.accent);
        why.addEventListener('click',()=>window.NayaUI.toast('Ranking is explainable from relevance, recency, context, relationships and verified learning — never mystery engagement logic.',r.accent));
        head.append(count,why); out.appendChild(head);

        const listWrap=el('div','intelligence-list');
        list.forEach((x,i)=>{
          const card=buildCard(x,stream,i===0,fresh.indexOf(x)>=0);
          listWrap.appendChild(card);
        });
        out.appendChild(listWrap);

        /* Record the seen-set AFTER a truthful render — return visits distinguish new. */
        if(ids.length) putSeen(stream,new Set([...seen,...ids]));
      },{
        title:stream==='activity'?'No activity in this scope':stream==='personal'?'Your stream is quiet':'The collective stream is quiet',
        body:'There is no qualifying canonical intelligence for this stream and current context.'
      });
    }

    function buildCard(x,stream,isFocus,isFresh){
      const truth=normTruth(x);
      const card=el('article','intel-row'+(isFocus?' intel-focus':'')+(isFresh?' intel-new':''));
      card.style.setProperty('--room-accent',r.accent);
      card.setAttribute('data-truth',truth);
      if(isFresh) card.setAttribute('data-fresh','true');

      const type=el('div','intel-type',K.safe(x?.category||x?.type||stream.toUpperCase()));
      const title=el('div','intel-title',K.safe(K.title(x)));
      card.append(type,title);

      const nutshell=K.summary(x);
      if(nutshell) card.appendChild(el('div','intel-summary',K.safe(nutshell)));

      /* Why-now: discoverable as text, never hover-only (a11y contract). */
      const why=el('div','intel-why');
      why.appendChild(el('span','intel-why-label','Why now'));
      why.appendChild(el('span','intel-why-text',K.safe(whyNowText(x))));
      card.appendChild(why);

      const meta=el('div','meta-row');
      const badge=el('span','truth-badge truth-'+truth.toLowerCase(),K.safe(truthLabel(truth)));
      meta.appendChild(badge);
      const when=x?.created_at||x?.timestamp||x?.time;
      if(when) meta.appendChild(el('span','',K.safe(String(when))));
      const src=sourceName(x);
      if(src) meta.appendChild(el('span','',K.safe(src)));
      card.appendChild(meta);

      const actions=el('div','action-row');
      const open=el('button','btn btn-ghost mini','<span>Open</span>');
      open.style.setProperty('--btn-accent',r.accent);
      open.addEventListener('click',()=>openObject(x));
      actions.appendChild(open);

      /* Progressive evidence: inline, from the object's real fields only. */
      const evBtn=el('button','btn btn-ghost mini','<span>Evidence</span>');
      evBtn.style.setProperty('--btn-accent',r.accent);
      evBtn.setAttribute('aria-expanded','false');
      const evPanel=el('div','intel-evidence'); evPanel.hidden=true;
      evBtn.addEventListener('click',()=>{
        const showing=evPanel.hidden;
        if(showing) renderEvidence(evPanel,x);
        evPanel.hidden=!showing;
        evBtn.setAttribute('aria-expanded',String(showing));
        evBtn.querySelector('span').textContent=showing?'Hide evidence':'Evidence';
      });
      actions.appendChild(evBtn);
      card.append(actions,evPanel);
      return card;
    }

    function renderEvidence(panel,x){
      panel.innerHTML='';
      const rows=[
        ['Canonical ID', x?.intelligent_block_id||x?.id || 'not exposed'],
        ['Truth state', truthLabel(normTruth(x))],
        ['Source', sourceName(x)||'not exposed'],
        ['Time', x?.created_at||x?.timestamp||x?.time || 'not exposed'],
        ['Lineage', x?.lineage||x?.provenance||'attached to the canonical object']
      ];
      rows.forEach(([k,v])=>{
        const row=el('div','intel-evidence-row');
        row.appendChild(el('span','intel-evidence-key',K.safe(k)));
        row.appendChild(el('span','intel-evidence-val',K.safe(String(v))));
        panel.appendChild(row);
      });
    }

    async function openObject(x){
      const id=itemId(x);
      if(!id){window.NayaUI.toast('This item did not expose a canonical intelligence ID.',r.accent);return;}
      const res=await window.NayaRuntime.retrieve(id);
      if(!res.ok){window.NayaUI.toast(res.message||'Canonical detail is unavailable.',r.accent);return;}
      window.NayaUI.toast('Canonical intelligence retrieved. Detail-view projection is the next seam.',r.accent);
    }
  }
  window.NayaRooms=window.NayaRooms||{}; window.NayaRooms.feed=FeedRoom;
})();
