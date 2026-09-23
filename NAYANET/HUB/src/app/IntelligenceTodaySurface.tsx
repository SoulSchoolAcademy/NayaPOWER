import { useEffect, useMemo, useState } from 'react';
import type { CSSProperties } from 'react';
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

  const latest=useMemo(()=>events.slice(0,9),[events]);
  const counts=useMemo(()=>({
    total:events.length,
    personal:events.filter(e=>e.privacy?.visibility==='private'||e.privacy?.visibility==='private').length,
    collective:events.filter(e=>e.privacy?.visibility!=='private'&&e.privacy?.visibility!=='private').length
  }),[events]);

  if(state==='loading')return <section className="today-room loading"><div className="today-orbit">✦</div><b>READING YOUR INTELLIGENCE</b><p>Loading the canonical intelligence source. Nothing synthetic is inserted while it loads.</p></section>;
  if(state==='error')return <section className="today-room error"><span className="today-kicker">YOUR INTELLIGENCE TODAY</span><h1>We could not retrieve today’s intelligence.</h1><p>The canonical intelligence source did not respond successfully. The room will not manufacture a dashboard to hide the gap.</p><button onClick={()=>window.location.reload()}>TRY AGAIN</button></section>;

  return <section className="today-room">
    <header className="today-hero">
      <div className="today-hero-copy">
        <span className="today-kicker">INTELLIGENCE DIARY · DAILY COCKPIT</span>
        <h1>Your Intelligence Today</h1>
        <div className="today-date">{dateLabel()}</div>
        <p>Your life creates your intelligence every day. This is the place to see what has arrived, understand what is here, preserve what matters, and move useful intelligence forward.</p>
        <div className="today-actions">
          <button className="today-primary" onClick={()=>navigate(routes.feed)}>EXPLORE YOUR INTELLIGENCE <span>→</span></button>
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
      <div className="today-section-head"><div><span className="today-kicker">01 · SEE</span><h2>Today at a glance</h2><p>The intelligence currently available through the canonical Hub projection.</p></div><span className="today-live">● LIVE PROJECTION</span></div>
      <div className="today-metrics">
        <button onClick={()=>navigate(routes.feed)}><span className="metric-icon">✦</span><small>INTELLIGENCE</small><strong>{counts.total}</strong><em>blocks available now</em></button>
        <button onClick={()=>navigate(routes.feed)}><span className="metric-icon personal">◉</span><small>PERSONAL</small><strong>{counts.personal}</strong><em>private intelligence visible</em></button>
        <button onClick={()=>navigate(routes.feed)}><span className="metric-icon collective">◎</span><small>COLLECTIVE</small><strong>{counts.collective}</strong><em>shared intelligence visible</em></button>
      </div>
    </section>

    <section className="today-section">
      <div className="today-section-head"><div><span className="today-kicker">02 · UNDERSTAND</span><h2>What is here today?</h2><p>Open any intelligence item for the complete Smart Feed experience: meaning, learning, evidence, provenance, application and action.</p></div></div>
      <div className="today-intelligence-grid">
        {latest.map((event,index)=><article key={event.event_id} className="today-intelligence-card" style={{'--today-tone':(['#9d75ff','#6675ff','#55b9ee','#55e39a','#d86cff','#e8c766'][index%6])} as CSSProperties}>
          <div className="today-card-top"><span>{String(index+1).padStart(2,'0')}</span><small>{event.privacy?.visibility||'VISIBLE'}</small></div>
          <h3>{event.source.label}</h3>
          <p>{excerpt(event).slice(0,280)}{excerpt(event).length>280?'…':''}</p>
          <button onClick={()=>navigate(routes.feed+'?event_id='+encodeURIComponent(event.event_id))}>OPEN INTELLIGENCE <span>→</span></button>
        </article>)}
      </div>
      {!latest.length&&<div className="today-empty"><b>No intelligence has arrived yet.</b><span>Capture a Smart Note to begin creating your Intelligence Diary.</span></div>}
    </section>

    <section className="today-section today-value">
      <div className="today-section-head"><div><span className="today-kicker">03 · MAKE IT USEFUL</span><h2>From intelligence to value</h2><p>The room exists to help a person do something useful with what they know—not simply admire a dashboard.</p></div></div>
      <div className="today-value-grid">
        <button onClick={()=>navigate(routes.notes)}><span>＋</span><div><b>CAPTURE</b><strong>Preserve what matters.</strong><small>Turn a discovery, decision, lesson or meaningful moment into a Smart Note.</small></div><i>→</i></button>
        <button onClick={()=>navigate(routes.feed)}><span>◎</span><div><b>UNDERSTAND</b><strong>Go deeper.</strong><small>Open the complete intelligence object with evidence, meaning, learning and application.</small></div><i>→</i></button>
        <button onClick={()=>navigate(routes.library)}><span>▱</span><div><b>REUSE</b><strong>Find it again.</strong><small>Search your intelligence and carry useful knowledge into future work.</small></div><i>→</i></button>
      </div>
    </section>

    <section className="today-section today-honesty">
      <div><span className="today-kicker">04 · NAYA'S INTELLIGENCE LAW</span><h2>Known is known. Unknown stays unknown.</h2><p>This room shows verified intelligence that exists in the current projection. It does not invent “what changed,” priorities, learning, or activity merely to make the interface look complete. Those become first-class daily capabilities when their governed evidence boundaries are available.</p></div>
      <button onClick={()=>navigate(routes.feed)}>OPEN THE FULL INTELLIGENCE VIEW <span>→</span></button>
    </section>
  </section>;
}
