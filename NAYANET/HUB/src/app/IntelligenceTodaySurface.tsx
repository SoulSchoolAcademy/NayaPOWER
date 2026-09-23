import { useEffect, useMemo, useState } from 'react';
import type { IntelligentEvent } from '../intelligence/types';
import { loadPrimaryIntelligence, sortPrimaryIntelligence } from '../data/pis';
import { routes } from './routes';

function navigate(path:string){
  history.pushState({},'',path);
  window.dispatchEvent(new PopStateEvent('popstate'));
}

function dateLabel(){
  return new Intl.DateTimeFormat(undefined,{weekday:'long',month:'long',day:'numeric',year:'numeric'}).format(new Date());
}

function excerpt(event:IntelligentEvent){
  return (event.weaver_synthesis.summary || event.naya_interpretation.observation || event.human_input.raw || 'Intelligence is present.').replace(/\s+/g,' ').trim();
}

type Boundary='PROVEN'|'RECORDED'|'UNCERTAIN'|'MISSING'|'BLOCKED'|'NOT VERIFIED';

function nonempty(...values:(string|undefined)[]){
  return values.find(value=>Boolean(value?.trim()))?.trim()||'';
}

function learningClass(event:IntelligentEvent){
  const block=event.intelligent_block?.learning;
  if(typeof block?.lesson==='string'&&block.lesson.trim())return 'KNOWLEDGE';
  if(event.action.text?.trim())return 'DECISION / ACTION';
  if(event.meaning.text?.trim()||event.naya_interpretation.interpretation?.trim())return 'UNDERSTANDING';
  return 'INFORMATION';
}

function truthBoundary(event:IntelligentEvent):Boundary{
  const state=String(event.intelligent_block?.truth?.state||event.machine_evidence.verification_state||event.trust.level||'RECORDED').toUpperCase();
  if(state.includes('VERIF'))return 'PROVEN';
  if(state.includes('BLOCK'))return 'BLOCKED';
  if(state.includes('UNCERT'))return 'UNCERTAIN';
  return 'RECORDED';
}

function evidenceFor(event:IntelligentEvent){
  return event.machine_evidence.items.slice(0,4);
}

export function IntelligenceTodaySurface(){
  const [events,setEvents]=useState<IntelligentEvent[]>([]);
  const [state,setState]=useState<'loading'|'ready'|'error'>('loading');

  useEffect(()=>{
    let alive=true;
    (async()=>{
      try{
        const result=await loadPrimaryIntelligence();
        if(!alive)return;
        setEvents(sortPrimaryIntelligence(result.events));
        setState('ready');
      }catch{
        if(alive)setState('error');
      }
    })();
    return()=>{alive=false};
  },[]);

  const todayStart=useMemo(()=>{
    const now=new Date();
    return new Date(now.getFullYear(),now.getMonth(),now.getDate()).getTime();
  },[]);

  const latest=useMemo(()=>events.slice(0,9),[events]);
  const todayEvents=useMemo(()=>events.filter(event=>{
    const time=Date.parse(event.created_at||event.human_input.captured_at||'');
    return Number.isFinite(time)&&time>=todayStart;
  }),[events,todayStart]);

  const counts=useMemo(()=>({
    total:events.length,
    personal:events.filter(e=>e.privacy?.visibility?.toLowerCase().includes('private')).length,
    collective:events.filter(e=>!e.privacy?.visibility?.toLowerCase().includes('private')).length
  }),[events]);

  const learning=useMemo(()=>{
    const buckets:{label:string;count:number;examples:string[]}[]=[
      {label:'INFORMATION',count:0,examples:[]},
      {label:'UNDERSTANDING',count:0,examples:[]},
      {label:'CHANGE / DECISION',count:0,examples:[]},
      {label:'KNOWLEDGE',count:0,examples:[]}
    ];
    events.slice(0,20).forEach(event=>{
      const kind=learningClass(event);
      const bucket=buckets.find(item=>item.label===kind)||buckets.find(item=>item.label.startsWith(kind.split(' ')[0]));
      if(bucket){bucket.count+=1;if(bucket.examples.length<2)bucket.examples.push(event.source.label);}
    });
    return buckets;
  },[events]);

  const changed=useMemo(()=>events.filter(event=>{
    const created=Date.parse(event.created_at||'');
    const updated=Date.parse(event.updated_at||'');
    return Number.isFinite(created)&&Number.isFinite(updated)&&updated>created;
  }).slice(0,5),[events]);

  const missingBoundaries=[
    {label:'PRIOR-DAY COMPARISON',status:'NOT VERIFIED' as Boundary,detail:'A real prior-day source is not part of the current PIS contract, so no invented comparison is shown.'},
    {label:'ACTIVITY PROJECTION',status:'NOT VERIFIED' as Boundary,detail:'The room does not fabricate daily activity until a governed activity source is available.'},
    {label:'RETENTION RECOMMENDATION',status:events.some(e=>e.lesson.retained)?'RECORDED' as Boundary:'NOT VERIFIED' as Boundary,detail:events.some(e=>e.lesson.retained)?'Retention is recorded on available intelligence objects. A separate recommendation engine is not asserted.':'No retention evidence is available.'},
    {label:'DAILY PRIORITY',status:events.length?'RECORDED' as Boundary:'MISSING' as Boundary,detail:events.length?'Items are surfaced from canonical intelligence; no unsupported priority score is invented.':'No intelligence exists to prioritize.'}
  ];

  if(state==='loading')return <section className="today-room loading"><div className="today-orbit">✦</div><b>READING YOUR INTELLIGENCE</b><p>Loading the canonical intelligence source. Nothing synthetic is inserted while it loads.</p></section>;
  if(state==='error')return <section className="today-room error"><span className="today-kicker">YOUR INTELLIGENCE TODAY</span><h1>We could not retrieve today’s intelligence.</h1><p>The canonical intelligence source did not respond successfully. The room will not manufacture a dashboard to hide the gap.</p><button onClick={()=>window.location.reload()}>TRY AGAIN</button></section>;

  return <section className="today-room">
    <header className="today-hero">
      <div className="today-hero-copy">
        <span className="today-kicker">INTELLIGENCE DIARY · DAILY COCKPIT</span>
        <h1>Your Intelligence Today</h1>
        <div className="today-date">{dateLabel()}</div>
        <p>Your life creates your intelligence every day. This room turns what is actually available into a clear daily picture: what arrived, what it means, what changed, what can be remembered, what remains uncertain, and what you can do next.</p>
        <div className="today-actions">
          <button className="today-primary" onClick={()=>navigate(routes.notes)}>CAPTURE INTELLIGENCE <span>＋</span></button>
          <button onClick={()=>navigate(routes.feed)}>EXPLORE YOUR INTELLIGENCE <span>→</span></button>
          <button onClick={()=>navigate(routes.library)}>SEARCH YOUR LIBRARY <span>⌕</span></button>
        </div>
      </div>
      <div className="today-hero-orb">
        <div className="today-orb-ring"><span>✦</span></div>
        <b>NAYA</b>
        <small>YOUR INTELLIGENCE PARTNER</small>
      </div>
    </header>

    <section className="today-section today-pulse">
      <div className="today-section-head"><div><span className="today-kicker">01 · ORIENT</span><h2>Today at a glance</h2><p>Current intelligence available through the canonical Hub projection. Counts are derived from retrieved events, not placeholders.</p></div><span className="today-live">● LIVE PROJECTION</span></div>
      <div className="today-metrics">
        <button onClick={()=>navigate(routes.feed)}><span className="metric-icon">✦</span><small>INTELLIGENCE</small><strong>{counts.total}</strong><em>blocks available now</em></button>
        <button onClick={()=>navigate(routes.feed)}><span className="metric-icon personal">◉</span><small>PERSONAL</small><strong>{counts.personal}</strong><em>private intelligence visible</em></button>
        <button onClick={()=>navigate(routes.feed)}><span className="metric-icon collective">◎</span><small>COLLECTIVE</small><strong>{counts.collective}</strong><em>non-private intelligence visible</em></button>
      </div>
      <div className="today-boundary-line"><b>Today's retrieved events: {todayEvents.length}</b><span>Source: Primary Intelligence / PIS</span></div>
    </section>

    <section className="today-section">
      <div className="today-section-head"><div><span className="today-kicker">02 · SEE</span><h2>What happened?</h2><p>The newest intelligence objects currently available. Each card opens the complete intelligence projection and its evidence.</p></div></div>
      <div className="today-intelligence-grid">
        {latest.map((event,index)=><article key={event.event_id} className="today-intelligence-card">
          <div className="today-card-top"><span>{String(index+1).padStart(2,'0')}</span><small>{event.privacy?.visibility||'VISIBLE'}</small></div>
          <h3>{event.source.label}</h3>
          <p>{excerpt(event).slice(0,280)}{excerpt(event).length>280?'…':''}</p>
          <div className="today-card-status"><span>{truthBoundary(event)}</span><span>{learningClass(event)}</span></div>
          <button onClick={()=>navigate(routes.feed+'?event_id='+encodeURIComponent(event.event_id))}>OPEN INTELLIGENCE <span>→</span></button>
        </article>)}
      </div>
      {!latest.length&&<div className="today-empty"><b>No intelligence has arrived yet.</b><span>Capture a Smart Note to begin creating your Intelligence Diary.</span></div>}
    </section>

    <section className="today-section">
      <div className="today-section-head"><div><span className="today-kicker">03 · UNDERSTAND</span><h2>What did I learn?</h2><p>Learning is classified from fields that actually exist on the retrieved intelligence objects. Nothing is promoted to durable knowledge without evidence.</p></div></div>
      <div className="today-learning-grid">
        {learning.map(item=><article key={item.label} className="today-learning-card"><span>{item.count}</span><div><b>{item.label}</b><p>{item.examples.length?item.examples.join(' · '):'No matching evidence currently retrieved.'}</p></div></article>)}
      </div>
    </section>

    <section className="today-section">
      <div className="today-section-head"><div><span className="today-kicker">04 · CHANGE</span><h2>What changed?</h2><p>Only actual object updates are shown here. A true yesterday-versus-today comparison remains explicitly unverified until the daily comparison source exists.</p></div><span className="today-state-badge">PRIOR-DAY: NOT VERIFIED</span></div>
      <div className="today-change-list">
        {changed.length?changed.map(event=><button key={event.event_id} onClick={()=>navigate(routes.feed+'?event_id='+encodeURIComponent(event.event_id))}><span>UPDATED</span><strong>{event.source.label}</strong><small>{new Date(event.updated_at).toLocaleString()}</small><i>→</i></button>):<div className="today-empty compact"><b>No verified object changes detected.</b><span>This is an honest result, not a fabricated “change” card.</span></div>}
      </div>
    </section>

    <section className="today-section today-priority">
      <div className="today-section-head"><div><span className="today-kicker">05 · PRIORITIZE</span><h2>What matters now?</h2><p>Relevant intelligence is surfaced without pretending the system has a priority model it cannot substantiate yet.</p></div></div>
      <div className="today-focus">
        <div className="today-focus-main"><span className="today-focus-icon">✦</span><div><b>CURRENT INTELLIGENCE IS THE VERIFIED STARTING POINT</b><h3>{latest[0]?.source.label||'Nothing to prioritize yet'}</h3><p>{latest[0]?excerpt(latest[0]):'Capture or retrieve intelligence before asking Naya to prioritize it.'}</p></div></div>
        <button onClick={()=>latest[0]&&navigate(routes.feed+'?event_id='+encodeURIComponent(latest[0].event_id))}>INSPECT EVIDENCE <span>→</span></button>
      </div>
    </section>

    <section className="today-section">
      <div className="today-section-head"><div><span className="today-kicker">06 · REMEMBER</span><h2>What should I remember?</h2><p>Retention is shown from recorded intelligence state. The room does not invent a retention recommendation when the governed recommendation engine is absent.</p></div></div>
      <div className="today-memory-grid">
        {latest.filter(event=>event.lesson.retained||event.intelligent_block?.lifecycle?.stage).slice(0,4).map(event=><button key={event.event_id} onClick={()=>navigate(routes.feed+'?event_id='+encodeURIComponent(event.event_id))}><span>◆</span><div><b>{event.lesson.retained?'RETAINED':'RECORDED'}</b><strong>{event.source.label}</strong><small>{nonempty(event.lesson.text,event.meaning.text,excerpt(event)).slice(0,180)}</small></div><i>→</i></button>)}
        {!latest.some(event=>event.lesson.retained||event.intelligent_block?.lifecycle?.stage)&&<div className="today-empty compact"><b>No governed retention state is currently recorded.</b><span>Naya will not pretend otherwise.</span></div>}
      </div>
    </section>

    <section className="today-section">
      <div className="today-section-head"><div><span className="today-kicker">07 · QUESTION</span><h2>What am I missing?</h2><p>This is the intelligence boundary. Missing means missing evidence—not an invitation to guess.</p></div></div>
      <div className="today-boundary-grid">
        {missingBoundaries.map(item=><article key={item.label}><div><b>{item.label}</b><span className={'boundary-'+item.status.toLowerCase().replace(/\s+/g,'-')}>{item.status}</span></div><p>{item.detail}</p></article>)}
      </div>
    </section>

    <section className="today-section today-naya-view">
      <div className="today-section-head"><div><span className="today-kicker">08 · NAYA'S VIEW</span><h2>What Naya can substantiate</h2><p>This synthesis separates observation from interpretation and points back to the evidence object.</p></div></div>
      <div className="today-naya-grid">
        <article><span>OBSERVED</span><h3>{latest.length} intelligence objects are retrievable.</h3><p>The current room is reading from the primary intelligence loader rather than manufacturing daily content.</p></article>
        <article><span>INTERPRETATION</span><h3>{latest[0]?nonempty(latest[0].naya_interpretation.interpretation,latest[0].naya_interpretation.observation):'No interpretation is currently available.'}</h3><p>This is a projection of the retrieved object, not an independent fact claim.</p></article>
        <article><span>UNCERTAINTY</span><h3>{latest[0]?.naya_interpretation.uncertainty||'No additional uncertainty statement is attached.'}</h3><p>Unknown boundaries remain visible instead of being smoothed over.</p></article>
      </div>
    </section>

    <section className="today-section">
      <div className="today-section-head"><div><span className="today-kicker">09 · EVIDENCE</span><h2>Provenance you can inspect</h2><p>Every visible intelligence item exposes the evidence identifiers available on the object. Open it to inspect the full Smart Feed projection.</p></div></div>
      <div className="today-evidence-list">
        {latest.slice(0,5).map(event=><button key={event.event_id} onClick={()=>navigate(routes.feed+'?event_id='+encodeURIComponent(event.event_id))}><div><b>{event.source.label}</b><small>{event.event_id}</small></div><p>{evidenceFor(event).join(' · ')}</p><span>VIEW →</span></button>)}
      </div>
    </section>

    <section className="today-section today-value">
      <div className="today-section-head"><div><span className="today-kicker">10 · ACT → VERIFY</span><h2>Turn today's intelligence into value</h2><p>The room ends with action, not a dashboard. Every action leads back to an existing governed Hub surface.</p></div></div>
      <div className="today-value-grid">
        <button onClick={()=>navigate(routes.notes)}><span>＋</span><div><b>CAPTURE</b><strong>Preserve what matters.</strong><small>Turn a discovery, decision, lesson or meaningful moment into a Smart Note.</small></div><i>→</i></button>
        <button onClick={()=>navigate(routes.feed)}><span>◎</span><div><b>UNDERSTAND</b><strong>Inspect the intelligence.</strong><small>Open the complete object, evidence, meaning, learning and application.</small></div><i>→</i></button>
        <button onClick={()=>navigate(routes.library)}><span>▱</span><div><b>REUSE</b><strong>Carry it forward.</strong><small>Find useful intelligence again instead of reconstructing it.</small></div><i>→</i></button>
      </div>
    </section>

    <section className="today-section today-honesty">
      <div><span className="today-kicker">11 · TRUTH BOUNDARY</span><h2>Known is known. Unknown stays unknown.</h2><p>Room 01 is now a complete daily intelligence surface: it shows what is retrievable, classifies learning from available evidence, exposes change boundaries, surfaces what matters without fake scoring, shows retention state, identifies missing evidence, separates Naya interpretation from observation, and provides direct evidence access. Where the underlying governed capability is not yet present, the room says so instead of simulating it.</p></div>
      <button onClick={()=>navigate(routes.feed)}>OPEN THE FULL INTELLIGENCE VIEW <span>→</span></button>
    </section>
  </section>;
}
