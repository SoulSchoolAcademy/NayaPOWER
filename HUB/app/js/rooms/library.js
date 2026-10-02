/* INTELLIGENT LIBRARY — THE VAULT / YOUR MIND */
(function(){
  function LibraryRoom(){
    const {el,Icons}=window.NayaUI, K=window.NayaRoomKit, r=K.room('library');
    const wrap=el('div','room-scene'); wrap.style.setProperty('--room-accent',r.accent);

    const hero=el('section','library-hero');
    const b=K.board(r.accent,'library','Everything retained, organized by meaning','Search what NayaPOWER knows — with provenance, uncertainty and relationships.');
    const search=el('form','library-search');
    search.innerHTML=Icons.icon('search')+'<input type="search" aria-label="Search your intelligence" placeholder="Search your intelligence — what, why, source, learning, meaning…"><button class="btn mini" type="submit"><span>Search</span></button>';
    search.querySelector('.btn').style.setProperty('--btn-accent',r.accent);
    b.body.appendChild(search); hero.appendChild(b); wrap.appendChild(hero);

    const zone=el('section','room-scene'); wrap.appendChild(zone);
    search.addEventListener('submit',e=>{e.preventDefault();const q=search.querySelector('input').value.trim();if(q)runSearch(q);});
    refresh(); return wrap;

    function refresh(){
      K.load(zone,'library',{view:'featured'},(payload,list,out)=>{
        const featured=el('div','story-grid');
        const left=el('div','story-stack');
        const groups=[
          ['MOST RELEVANT',payload.most_relevant],
          ['RECENTLY DEVELOPED',payload.recently_developed],
          ['NEEDS ATTENTION',payload.needs_attention]
        ];
        let added=0;
        groups.forEach(([label,data])=>{
          if(!data)return;
          const vals=Array.isArray(data)?data:[data];
          vals.slice(0,3).forEach(x=>{
            const h=el('article','highlight');
            h.innerHTML='<div class="eyebrow">'+label+'</div><h3>'+K.safe(K.title(x))+'</h3>'+
              (K.summary(x)?'<p>'+K.safe(K.summary(x))+'</p>':'');
            left.appendChild(h);added++;
          });
        });
        if(!added&&list.length){list.slice(0,6).forEach(x=>left.appendChild(K.intelCard(x,r.accent)));}
        featured.appendChild(left);

        const side=el('aside','reflection');
        side.innerHTML='<div class="intel-type">KNOWLEDGE HEALTH</div><div class="quote">'+
          K.safe(payload.health_summary||payload.gap_summary||'The Library exposes what is known, what is developing, and what remains uncertain.')+
          '</div><small>Uncertainty is a feature of truthful intelligence, not a defect to hide.</small>';
        featured.appendChild(side); out.appendChild(featured);

        const domains=Array.isArray(payload.domains)?payload.domains:[];
        if(domains.length){
          const db=K.board(r.accent,'library','Your knowledge','Domains are navigational lenses — never separate stores.');
          const grid=el('div','domain-grid');
          domains.forEach(d=>{
            const x=el('button','domain');
            x.type='button'; x.style.color='inherit'; x.style.textAlign='left'; x.style.cursor='pointer';
            x.innerHTML='<strong>'+K.safe(d.name||d.title||'Domain')+'</strong><p>'+
              K.safe(d.summary||((d.count??'—')+' intelligence objects · '+(d.unresolved??'—')+' unresolved'))+'</p>';
            x.addEventListener('click',()=>loadDomain(d));
            grid.appendChild(x);
          });
          db.body.appendChild(grid);out.appendChild(db);
        }
      },{
        title:'The Library has no retrievable intelligence in this scope',
        body:'Nothing is shown until the canonical retrieval layer can return retained intelligence.'
      });
    }

    async function runSearch(query){
      zone.innerHTML=''; const res=await window.NayaRuntime.search(query,{scope:'library'});
      if(!res.ok){K.unavailable(zone,'library',res.message);return;}
      const list=K.items(res.data??res);
      if(!list.length){K.empty(zone,'library','No verified match','The knowledge base returned no qualifying intelligence for this search.');return;}
      const head=K.board(r.accent,'search','Search results','Why each result matched should remain explainable.');
      const l=el('div','intelligence-list');list.forEach(x=>l.appendChild(K.intelCard(x,r.accent)));
      head.body.appendChild(l);zone.appendChild(head);
    }

    function loadDomain(domain){
      const name=domain.name||domain.title||'Domain';
      K.load(zone,'library',{view:'domain',domain:domain.id||name},(payload,list,out)=>{
        const head=K.board(r.accent,'library',name,'What I know · What I learned · What I am uncertain about');
        const l=el('div','intelligence-list');list.forEach(x=>l.appendChild(K.intelCard(x,r.accent)));
        if(list.length)head.body.appendChild(l);
        else head.body.innerHTML='<div class="empty-instrument"><strong>No canonical objects returned.</strong><p>This domain exists, but the current runtime returned no intelligence for it.</p></div>';
        out.appendChild(head);
      },{title:'No intelligence in this domain',body:'This domain has no qualifying canonical objects yet.'});
    }
  }
  window.NayaRooms=window.NayaRooms||{};window.NayaRooms.library=LibraryRoom;
})();