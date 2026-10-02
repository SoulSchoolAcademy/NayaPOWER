(function(){

  'use strict';

  function ReportsRoom(el, ctx){
    const stage=el('div','reports-stage');
    let activePeriod='daily';
    let openReportId=null;
    let openDay=null;
    let query='';
    /* Adapter output wins when provided; fixtures are the fallback. */
    let ALL_REPORTS=(ctx&&ctx.reports&&ctx.reports.length)?ctx.reports:null;

    /* Jewel palette — cycles through sections */
    const JEWELS=['#ffd45a','#35e39b','#3ca8ff','#8a5cff','#ed42c4'];
    const JEWEL_GLYPHS=['\u25C6','\u2726','\u25B3','\u2727','\u25C6'];
    /* Rainbow week — each weekday owns a color (Shawn, 2026-10-02) */
    const DAY_COLORS=['#ffd45a','#ff9f43','#ff5c5c','#ed42c4','#8a5cff','#3ca8ff','#35e39b'];
    const DAY_NAMES=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
    function dayOf(dstr){
      const d=new Date(dstr+'T12:00:00');
      return isNaN(d)?null:d.getDay();
    }
    function dayColor(r){
      const d=dayOf(r.date);
      return d===null?null:DAY_COLORS[d];
    }
    function fullDateLabel(r){
      const d=dayOf(r.date);
      return d===null?r.dateLabel:DAY_NAMES[d]+', '+r.dateLabel;
    }
    function keyOf(r){ return r.dateKey||r.date||''; }
    /* ——— THE WEEK: seven day tiles, rainbow week, mocks stay inert ——— */
    const WEEK_META=[
      {name:'SUNDAY',color:'#ffd45a'},{name:'MONDAY',color:'#ff9f43'},
      {name:'TUESDAY',color:'#ff5c5c'},{name:'WEDNESDAY',color:'#ed42c4'},
      {name:'THURSDAY',color:'#8a5cff'},{name:'FRIDAY',color:'#3ca8ff'},
      {name:'SATURDAY',color:'#35e39b'}];
    const MONTHS_S=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    const MONTHS=['January','February','March','April','May','June','July','August','September','October','November','December'];
    function weekOf(anchorKey){
      const a=new Date(anchorKey+'T12:00:00');
      const sun=new Date(a); sun.setDate(a.getDate()-a.getDay());
      const days=[];
      for(let i=0;i<7;i++){
        const d=new Date(sun); d.setDate(sun.getDate()+i);
        const key=d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');
        days.push({key:key, dow:d.getDay(), label:MONTHS_S[d.getMonth()]+' '+d.getDate(),
          long:DAY_NAMES[d.getDay()]+', '+MONTHS[d.getMonth()]+' '+d.getDate()+', '+d.getFullYear()});
      }
      return days;
    }
    function todayKey(){
      const n=new Date();
      return n.getFullYear()+'-'+String(n.getMonth()+1).padStart(2,'0')+'-'+String(n.getDate()).padStart(2,'0');
    }
    function newestKey(list){
      let best='';
      list.forEach(r=>{ const k=keyOf(r); if(/^\d{4}-\d{2}-\d{2}$/.test(k)&&k>best) best=k; });
      return best||todayKey();
    }
    function weekRangeLabel(days){
      const f=days[0].label.split(' '), l=days[6].label.split(' ');
      return (f[0]+' '+f[1]+' \u2013 '+l[0]+' '+l[1]).toUpperCase();
    }
    function dayTile(d,rep,today){
      const meta=WEEK_META[d.dow];
      /* live: report filed · open: past/today, ready and clickable · todo: future, dimmed */
      const st=rep?'live':(d.key>today?'todo':'open');
      const t=el('article','day-tile '+st);
      t.style.setProperty('--day',meta.color);
      const kick=el('p','tile-kicker',''); kick.textContent=meta.name; t.appendChild(kick);
      const dt=el('p','tile-date',''); dt.textContent=d.label; t.appendChild(dt);
      const lab=el('p','tile-label',''); lab.textContent=(rep&&rep.subtitle)||'Daily Intelligence Briefing'; t.appendChild(lab);
      if(st==='live'){
        const b=el('button','tile-open','READ \u2192'); b.type='button';
        b.setAttribute('aria-label','Read the '+d.label+' report');
        b.addEventListener('click',()=>{ openReportId=rep.id; openDay=null; renderAll(); });
        t.appendChild(b);
      }else if(st==='open'){
        const b=el('button','tile-view','VIEW \u2192'); b.type='button';
        b.setAttribute('aria-label','View '+d.long+' — no report filed yet');
        b.addEventListener('click',()=>{ openDay=d; openReportId=null; renderAll(); });
        t.appendChild(b);
      }else{
        const pill=el('p','tile-pill',''); pill.textContent='AWAITING REPORT'; t.appendChild(pill);
      }
      return t;
    }
    function weekStrip(){
      const reps=ALL_REPORTS.filter(r=>r.period==='daily');
      const days=weekOf(newestKey(reps));
      const today=todayKey();
      const sec=el('section','week-sec');
      const h=el('p','list-head',''); h.textContent='THIS WEEK \u00B7 '+weekRangeLabel(days);
      sec.appendChild(h);
      const strip=el('div','week-strip');
      days.forEach(d=>{
        const rep=reps.find(r=>keyOf(r)===d.key);
        strip.appendChild(dayTile(d,rep,today));
      });
      sec.appendChild(strip);
      return sec;
    }

    /* ——— DAY BOARD: a past/today tile with no report yet ——— */
    function dayBoard(d){
      const meta=WEEK_META[d.dow];
      const wrap=el('div','full-report');
      const back=el('button','report-back','\u2190 ALL DAILY REPORTS');
      back.type='button';
      back.addEventListener('click',()=>{ openDay=null; renderAll(); });
      wrap.appendChild(back);
      wrap.appendChild(weekRail(d.key));
      const board=el('article','report-board');
      const hero=el('header','rb-hero');
      const kick=el('p','rb-kicker',''); kick.textContent='NO REPORT FILED';
      kick.style.color=meta.color;
      const title=el('h1','rb-title',''); title.textContent='NayaPOWER Daily Intelligence Briefing';
      const date=el('p','rb-date',''); date.textContent=d.long;
      hero.appendChild(kick); hero.appendChild(title); hero.appendChild(date);
      board.appendChild(hero);
      board.appendChild(el('div','rb-beam'));
      const sec=el('section','rb-section');
      sec.style.setProperty('--sec',meta.color);
      const head=el('div','rb-sec-head');
      head.appendChild(jewel(meta.color,'\u25C6'));
      const lab=el('h2','rb-sec-label',''); lab.textContent='AWAITING THIS DAY\u2019S REPORT';
      head.appendChild(lab); sec.appendChild(head);
      const nut=el('p','rb-nutshell','');
      nut.textContent='There is no raw report for this day yet \u2014 this board is ready and waiting.';
      sec.appendChild(nut);
      const ul=el('ul','rb-points');
      ['When this day\u2019s markdown is added, the adapter distills it automatically \u2014 nutshell, jewel highlights, scorecard dials, the copyable prompt block. The same beautiful board, no hand-typing.',
       'Expected folder: BRAIN/05-MEMORY/INTELLIGENCE-REPORTS/DAILY/'+d.key.slice(0,4)+'/'+d.key.slice(5,7)+'/'+d.key.slice(8)+'/'
      ].forEach((pt,bi)=>{
        const li=el('li','rb-point');
        li.appendChild(jewel(JEWELS[bi%JEWELS.length],JEWEL_GLYPHS[bi%JEWEL_GLYPHS.length],'11px'));
        const tx=el('span','',''); tx.textContent=pt;
        li.appendChild(tx); ul.appendChild(li);
      });
      sec.appendChild(ul);
      board.appendChild(sec);
      const prov=el('footer','rb-prov');
      prov.innerHTML='<span>AWAITING REPORT</span><span>'+d.key+'</span>';
      board.appendChild(prov);
      wrap.appendChild(board);
      wrap.appendChild(keepReading(d.key));
      return wrap;
    }

    const SAMPLE_REPORTS=[
      {id:'DIR-NAYAPOWER-2026-10-01', ib:'IB-DIR-NAYAPOWER-20261001-001',
       period:'daily', date:'2026-10-01', dateLabel:'October 1, 2026',
       scope:'NayaPOWER / System Intelligence', status:'CANONICAL',
       title:'Daily Intelligence Briefing',
       bigPicture:'We have moved from \u201cdesigning the brain\u201d into the much harder stage of proving that the organs actually behave like one brain.',
       sections:[
        {label:'WHAT WE HAVE ACHIEVED',
         nutshell:'In a nutshell: today we proved several trust seams are real — the flaws were found precisely, the repairs were adversarially tested, and the round trip closed.',
         points:[
          'Coda 1 found and precisely isolated the LEARN trust flaw \u2014 proved the design/runtime mismatch, refused to overclaim.',
          'Naya 4 implemented the repair: resolver-based intake, 19 adversarial tests, two red guards turned green.',
          'Naya 2 closed the Demo-1 persistence round trip \u2014 receipt survived termination, recomputed byte-identically.',
          'EVOLVE is further along than the narrative suggested \u2014 we compose it, not build it.']},
        {label:'WHERE WE ACTUALLY ARE',
         nutshell:'In a nutshell: the architecture is real code and the trust boundaries genuinely work — the organism is not yet production-proven.',
         points:[
          'Nine-node organism: not yet fully production-proven. The remaining problem is composition.',
          'Trust boundaries are genuinely working through real code \u2014 no longer guessing at the seams.',
          'The question moved from \u201ccan callers manufacture verification?\u201d to \u201cdoes the runtime wire the boundary?\u201d']},
        {label:'WHAT MATTERS MOST RIGHT NOW',
         nutshell:'In a nutshell: stop building organs, start composing the brain — through the real runtime, with live evidence for every handoff.',
         points:[
          'Composition over construction. The organs exist.',
          'Make them behave like one brain through the real default runtime \u2014 no fixture shortcuts.',
          'Prove each handoff with live evidence.']},
        {label:'THE NEXT 10 HIGHEST-VALUE MOVES',
         nutshell:'In a nutshell: wire, prove, close, promote — in that order, scored by the calculus.',
         points:[
          'Wire the LEARN intake boundary through the default runtime.',
          'Prove the VERIFY handoff live.',
          'Close the CONNECT public path.',
          'Promote the persistence proof to production.',
          'Score every move by the decision calculus \u2014 highest verified value per moment first.']},
        {label:'PRIORITY + WHY',
         nutshell:'In a nutshell: the runtime wiring comes first, because nothing compounds until the ordinary path uses the trustworthy boundaries.',
         points:[
          'The runtime wiring is the priority.',
          'Everything else only compounds if the ordinary path uses the trustworthy boundaries.',
          'A boundary nobody traverses is a decoration.']},
        {label:'SCORECARD RIGHT NOW',
         nutshell:'In a nutshell: strong on architecture and trust boundaries, honest about composition — the score moves only on live evidence.',
         points:[
          'Architecture: real code.',
          'Trust boundaries: genuinely working.',
          'Composition: in progress.',
          'Production proof: not yet \u2014 the honest score moves only on live evidence.']},
        {label:'ONE NEXT ACTION',
         nutshell:'In a nutshell: run the LEARN intake through the default Kernel runtime and prove it with receipts.',
         points:[
          'Run the LEARN intake through the default Kernel runtime \u2014 the real path, not a test harness.',
          'Prove the receipt resolves, binds, and rejects exactly as the repair specifies.']},
        {label:'EXACT READY-TO-USE PROMPT',
         nutshell:'In a nutshell: copy this prompt into any Naya and the wiring proof starts immediately.',
         points:[
          '\u201cTake the LEARN intake repair and execute it through the default runtime. Did the resolver fire? Did subject/task/owner/scope bind? Did superseded evidence reject? Show the receipts.\u201d']},
        {label:'PROOF CRITERIA',
         nutshell:'In a nutshell: the proof is behavioral — resolver fires, bindings hold, superseded evidence rejects, cold successor recomputes.',
         points:[
          'Resolver fires on the real path.',
          'Bindings hold under adversarial input.',
          'Superseded evidence is rejected; fixture mode cannot be smuggled in.',
          'A cold successor recomputes the same result from receipts alone.']},
        {label:'TORCH FOR NEXT NAYA',
         nutshell:'In a nutshell: don’t rebuild what exists — compose it, and follow the receipts, not the narrative.',
         points:[
          'The LEARN boundary is repaired and tested. What is not yet proven is the runtime wiring \u2014 start there.',
          'Do not rebuild what exists. Compose it.',
          'The receipts are the map; follow them, do not trust the narrative.']}
       ]},
      {id:'DIR-NAYAPOWER-2026-09-30', ib:'IB-DIR-NAYAPOWER-20260930-001',
       period:'daily', date:'2026-09-30', dateLabel:'September 30, 2026',
       scope:'NayaPOWER / System Intelligence', status:'CANONICAL',
       title:'Daily Intelligence Briefing',
       bigPicture:'The nine master nodes are specified. The brain has a map. Today was about making the map match the territory.',
       sections:[]},
      {id:'DIR-NAYAPOWER-2026-W40', ib:'IB-DIR-NAYAPOWER-2026W40-001',
       period:'weekly', date:'2026-W40', dateLabel:'Week of September 28, 2026',
       scope:'NayaPOWER / System Intelligence', status:'CANONICAL',
       title:'Weekly Intelligence Briefing',
       bigPicture:'This week the project moved from specification to composition.',
       sections:[]}
    ];
    if(!ALL_REPORTS) ALL_REPORTS=SAMPLE_REPORTS;

    const PERIODS=[
      {key:'daily', label:'DAILY', searchPh:'Search daily reports\u2026'},
      {key:'weekly', label:'WEEKLY', searchPh:'Search weekly reports\u2026'},
      {key:'monthly', label:'MONTHLY', searchPh:'Search monthly reports\u2026'},
      {key:'yearly', label:'YEARLY', searchPh:'Search yearly reports\u2026'}
    ];

    function periodDef(){ return PERIODS.find(p=>p.key===activePeriod); }
    function periodReports(){
      let list=ALL_REPORTS.filter(r=>r.period===activePeriod);
      /* newest first, mechanical */
      list=list.slice().sort((a,b)=>String(b.dateKey||'').localeCompare(String(a.dateKey||'')));
      if(query){
        const q=query.toLowerCase();
        const hay=r=>((r.title+' '+r.dateLabel+' '+r.bigPicture+' '+r.id+' '+
          (r.sections||[]).map(s=>s.label+' '+(s.nutshell||'')+' '+(s.points||[]).join(' ')).join(' ')
        ).toLowerCase());
        list=list.filter(r=>hay(r).includes(q));
      }
      return list;
    }

    /* ——— ORIENT ——— */
    function orient(){
      const o=el('div','orient');
      const d=el('p','orient-date',''); d.textContent='Friday, October 2, 2026';
      const l=el('p','orient-line','');
      l.textContent='Your intelligence, collected across time. Each report \u2014 one beautiful board.';
      o.appendChild(d); o.appendChild(l);
      const sc=el('p','score-line');
      const n=ALL_REPORTS.filter(r=>r.period===activePeriod).length;
      sc.innerHTML='<strong>'+n+'</strong> '+periodDef().label+' REPORTS';
      o.appendChild(sc);
      return o;
    }

    function periodTabs(){
      const wrap=el('div','report-tabs');
      wrap.setAttribute('role','tablist');
      PERIODS.forEach(p=>{
        const t=el('button','report-tab'+(p.key===activePeriod?' active':''),p.label);
        t.type='button'; t.setAttribute('role','tab');
        t.setAttribute('aria-selected',p.key===activePeriod?'true':'false');
        t.addEventListener('click',()=>{ activePeriod=p.key; openReportId=null; openDay=null; query=''; renderAll(); });
        wrap.appendChild(t);
      });
      return wrap;
    }

    function searchBar(){
      const wrap=el('div','search-wrap');
      const input=el('input','search-input','');
      input.type='search'; input.placeholder=periodDef().searchPh;
      input.setAttribute('aria-label','Search reports'); input.value=query;
      input.addEventListener('input',()=>{ query=input.value; renderList(); });
      wrap.appendChild(input);
      return wrap;
    }

    /* ——— REPORT CARD ——— */
    function reportCard(r){
      const card=el('article','report-card');
      const dc=dayColor(r);
      if(dc)card.style.setProperty('--day',dc);
      const kick=el('p','card-kicker',''); kick.textContent=r.status+' \u00B7 '+fullDateLabel(r).toUpperCase();
      const title=el('h3','card-title',''); title.textContent=r.title;
      card.appendChild(kick); card.appendChild(title);
      if(r.subtitle){ const theme=el('p','card-theme',''); theme.textContent=r.subtitle; card.appendChild(theme); }
      const big=el('p','card-big',''); big.textContent=r.bigPicture;
      const open=el('button','card-open','READ THE REPORT \u2192'); open.type='button';
      open.setAttribute('aria-label','Read the full report: '+r.title+' '+r.dateLabel);
      open.addEventListener('click',()=>{ openReportId=r.id; renderAll(); });
      card.appendChild(big); card.appendChild(open);
      return card;
    }

    function renderList(){
      const zone=stage.querySelector('.reports-list');
      if(!zone)return;
      zone.innerHTML='';
      if(activePeriod==='daily'&&!query){
        zone.appendChild(weekStrip());
        const ah=el('p','list-head',''); ah.textContent='REPORT ARCHIVE';
        zone.appendChild(ah);
      }
      const list=periodReports();
      if(!list.length){
        const q=el('p','quiet-note','');
        q.textContent=query
          ? 'No reports match \u201C'+query+'\u201D in '+periodDef().label.toLowerCase()+'.'
          : 'No '+periodDef().label.toLowerCase()+' reports yet. The system will not invent one.';
        zone.appendChild(q);
        return;
      }
      list.forEach(r=>zone.appendChild(reportCard(r)));
    }

    /* ——— special sections ——— */
    /* chain pill strip — shared by scorecard and standard sections */
    function chainStrip(s,i){
      const ch=el('div','sc-chain');
      s.chain.forEach((link,li)=>{
        if(li){ const ar=el('span','sc-arrow','\u2192'); ch.appendChild(ar); }
        const lk=el('span','sc-link',''); lk.textContent=link;
        lk.style.setProperty('--sec',JEWELS[(li+i)%JEWELS.length]);
        ch.appendChild(lk);
      });
      return ch;
    }

    function scorecardSection(s,i){
      const color=JEWELS[i%JEWELS.length];
      const sec=el('section','rb-section rb-scorecard');
      sec.style.setProperty('--sec',color);
      const head=el('div','rb-sec-head');
      head.appendChild(jewel(color,JEWEL_GLYPHS[i%JEWEL_GLYPHS.length]));
      const lab=el('h2','rb-sec-label',''); lab.textContent=s.label;
      head.appendChild(lab); sec.appendChild(head);
      if(s.nutshell){ const nut=el('p','rb-nutshell',''); nut.textContent=s.nutshell; sec.appendChild(nut); }
      /* score dials */
      if(s.scores && s.scores.length){
        const dials=el('div','sc-dials');
        s.scores.forEach((sc,di)=>{
          const dcol=JEWELS[(di+i)%JEWELS.length];
          const d=el('div','sc-dial'); d.style.setProperty('--sec',dcol);
          const v=el('div','sc-value',''); v.textContent=sc.value;
          const l=el('div','sc-label',''); l.textContent=sc.label;
          d.appendChild(v); d.appendChild(l); dials.appendChild(d);
        });
        sec.appendChild(dials);
      }
      /* the chain */
      if(s.chain && s.chain.length) sec.appendChild(chainStrip(s,i));
      /* remaining bullets */
      if(s.points && s.points.length){
        const ul=el('ul','rb-points');
        s.points.forEach((pt,bi)=>{
          const bcol=JEWELS[(bi+i)%JEWELS.length];
          const li=el('li','rb-point');
          li.appendChild(jewel(bcol,JEWEL_GLYPHS[(bi+i)%JEWEL_GLYPHS.length],'11px'));
          const tx=el('span','',''); tx.textContent=pt;
          li.appendChild(tx); ul.appendChild(li);
        });
        sec.appendChild(ul);
      }
      return sec;
    }

    function promptSection(s,i){
      const color=JEWELS[i%JEWELS.length];
      const sec=el('section','rb-section');
      sec.style.setProperty('--sec',color);
      const head=el('div','rb-sec-head');
      head.appendChild(jewel(color,JEWEL_GLYPHS[i%JEWEL_GLYPHS.length]));
      const lab=el('h2','rb-sec-label',''); lab.textContent=s.label;
      head.appendChild(lab); sec.appendChild(head);
      const box=el('div','prompt-box');
      const pre=el('pre','prompt-text',''); pre.textContent=s.prompt||s.points.join('\n');
      box.appendChild(pre);
      const copy=el('button','prompt-copy','COPY PROMPT'); copy.type='button';
      copy.addEventListener('click',()=>{
        const done=()=>{ copy.textContent='COPIED \u2713'; setTimeout(()=>copy.textContent='COPY PROMPT',1600); };
        if(navigator.clipboard&&navigator.clipboard.writeText){
          navigator.clipboard.writeText(pre.textContent).then(done,done);
        } else {
          const ta=document.createElement('textarea'); ta.value=pre.textContent;
          document.body.appendChild(ta); ta.select();
          try{document.execCommand('copy');}catch(e){} document.body.removeChild(ta); done();
        }
      });
      box.appendChild(copy);
      sec.appendChild(box);
      return sec;
    }

    /* ——— WEEK RAIL + KEEP READING: move across days from inside a report ——— */
    function dayState(d,rep,today){ return rep?'live':(d.key>today?'todo':'open'); }
    function weekDays(){
      const reps=ALL_REPORTS.filter(r=>r.period==='daily');
      return {reps:reps, days:weekOf(newestKey(reps)), today:todayKey()};
    }
    function goDay(d,rep){
      if(rep){ openReportId=rep.id; openDay=null; }
      else{ openDay=d; openReportId=null; }
      renderAll(); window.scrollTo(0,0);
    }
    function weekRail(currentKey){
      const w=weekDays();
      const nav=el('nav','week-rail');
      nav.setAttribute('aria-label','Days of this week');
      w.days.forEach(d=>{
        const meta=WEEK_META[d.dow];
        const rep=w.reps.find(r=>keyOf(r)===d.key);
        const st=dayState(d,rep,w.today);
        const chip=el('button','rail-chip '+st+(d.key===currentKey?' current':''));
        chip.type='button';
        chip.style.setProperty('--day',meta.color);
        chip.appendChild(el('span','rail-dot',''));
        const tx=el('span','',''); tx.textContent=meta.name.slice(0,3)+' '+d.label.split(' ')[1];
        chip.appendChild(tx);
        if(st==='todo'){ chip.disabled=true; }
        else{
          chip.setAttribute('aria-label',(rep?'Read ':'View ')+d.long);
          chip.addEventListener('click',()=>goDay(d,rep));
        }
        nav.appendChild(chip);
      });
      return nav;
    }
    function keepReading(currentKey){
      const w=weekDays();
      const sec=el('section','keep-reading');
      const h=el('p','list-head',''); h.textContent='MORE FROM THIS WEEK';
      sec.appendChild(h);
      w.days.forEach(d=>{
        if(d.key===currentKey) return;
        const meta=WEEK_META[d.dow];
        const rep=w.reps.find(r=>keyOf(r)===d.key);
        const st=dayState(d,rep,w.today);
        const row=el(st==='todo'?'div':'button','kr-row '+st);
        if(st!=='todo') row.type='button';
        row.style.setProperty('--day',meta.color);
        row.appendChild(el('span','kr-dot',''));
        const nm=el('span','kr-name',''); nm.textContent=meta.name+' \u00B7 '+d.long;
        row.appendChild(nm);
        const act=el('span','kr-act','');
        act.textContent=st==='live'?'READ \u2192':st==='open'?'VIEW \u2192':'SOON';
        row.appendChild(act);
        if(st!=='todo') row.addEventListener('click',()=>goDay(d,rep));
        sec.appendChild(row);
      });
      return sec;
    }

    /* ——— FULL REPORT — ONE board, sectionized inside ——— */
    function jewel(color, glyph, size){
      const j=el('span','jewel',''); j.textContent=glyph;
      j.style.setProperty('--jewel',color);
      if(size)j.style.fontSize=size;
      return j;
    }

    function fullReport(r){
      const wrap=el('div','full-report');

      const back=el('button','report-back','\u2190 ALL '+periodDef().label+' REPORTS');
      back.type='button';
      back.addEventListener('click',()=>{ openReportId=null; openDay=null; renderAll(); });
      wrap.appendChild(back);
      if(r.period==='daily') wrap.appendChild(weekRail(keyOf(r)));

      /* THE board */
      const board=el('article','report-board');

      /* hero */
      const hero=el('header','rb-hero');
      const kick=el('p','rb-kicker',''); kick.textContent=r.status+' \u00B7 '+r.scope.toUpperCase();
      const title=el('h1','rb-title',''); title.textContent=r.title;
      const date=el('p','rb-date',''); date.textContent=r.dateLabel;
      hero.appendChild(kick); hero.appendChild(title);
      if(r.subtitle){ const theme=el('p','rb-theme',''); theme.textContent=r.subtitle; hero.appendChild(theme); }
      hero.appendChild(date);
      board.appendChild(hero);

      /* divider */
      board.appendChild(el('div','rb-beam'));

      /* the big picture */
      const big=el('section','rb-big');
      const bigKick=el('p','rb-kicker',''); bigKick.textContent='THE BIG PICTURE';
      const bigTxt=el('p','rb-bigtext',''); bigTxt.textContent=r.bigPicture;
      big.appendChild(bigKick); big.appendChild(bigTxt);
      board.appendChild(big);

      /* sections — each a sub-block with its jewel color */
      if(r.sections && r.sections.length){
        r.sections.forEach((s,i)=>{
          if(s.kind==='scorecard'){ board.appendChild(scorecardSection(s,i)); return; }
          if(s.kind==='prompt'){ board.appendChild(promptSection(s,i)); return; }
          const color=JEWELS[i%JEWELS.length];
          const glyph=JEWEL_GLYPHS[i%JEWEL_GLYPHS.length];
          const sec=el('section','rb-section');
          sec.style.setProperty('--sec',color);

          const head=el('div','rb-sec-head');
          head.appendChild(jewel(color,glyph));
          const lab=el('h2','rb-sec-label',''); lab.textContent=s.label;
          head.appendChild(lab);
          sec.appendChild(head);

          /* nutshell line */
          if(s.nutshell){
            const nut=el('p','rb-nutshell',''); nut.textContent=s.nutshell;
            sec.appendChild(nut);
          }
          /* chain strip when the section carries one */
          if(s.chain && s.chain.length) sec.appendChild(chainStrip(s,i));
          /* jewel bullets — mixed palette for contrast, never all-matching */
          const ul=el('ul','rb-points');
          const numbered=/MOVE/.test(s.label);
          s.points.forEach((pt,bi)=>{
            const bcol=JEWELS[(bi+i)%JEWELS.length];
            const li=el('li','rb-point');
            if(numbered){
              const nj=el('span','jewel jewel-num',''); nj.textContent=String(bi+1);
              nj.style.setProperty('--jewel',bcol); li.appendChild(nj);
            } else {
              const bgly=JEWEL_GLYPHS[(bi+i)%JEWEL_GLYPHS.length];
              li.appendChild(jewel(bcol,bgly,'11px'));
            }
            const tx=el('span','',''); tx.textContent=pt;
            li.appendChild(tx);
            ul.appendChild(li);
          });
          sec.appendChild(ul);
          board.appendChild(sec);
        });
      }

      /* provenance */
      const prov=el('footer','rb-prov');
      prov.innerHTML='<span>'+r.ib+'</span><span>SNAPSHOT \u00B7 TRUE AS OF '+r.date+'</span>';
      board.appendChild(prov);

      wrap.appendChild(board);
      if(r.period==='daily') wrap.appendChild(keepReading(keyOf(r)));
      return wrap;
    }

    function renderAll(){
      stage.innerHTML='';
      if(openReportId){
        const r=ALL_REPORTS.find(x=>x.id===openReportId);
        if(r){ stage.appendChild(fullReport(r)); return; }
        openReportId=null;
      }
      if(openDay){ stage.appendChild(dayBoard(openDay)); return; }
      stage.appendChild(orient());
      stage.appendChild(periodTabs());
      stage.appendChild(searchBar());
      const list=el('div','reports-list');
      stage.appendChild(list);
      renderList();
    }

    renderAll();
    return stage;
  }

  window.NayaRooms=window.NayaRooms||{};
  window.NayaRooms.reports=ReportsRoom;
})();
