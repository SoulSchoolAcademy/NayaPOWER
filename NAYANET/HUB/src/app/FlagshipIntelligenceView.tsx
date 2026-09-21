import { useEffect, useMemo, useState } from 'react';
import { SmartFeedBoard } from '../intelligence/SmartFeedBoard';
import { loadPrimaryIntelligence, searchPrimaryIntelligence, sortPrimaryIntelligence } from '../data/pis';
import type { IntelligentEvent } from '../intelligence/types';
import { useIdentity } from '../identity/session';
import { routes } from './routes';

type Props = { title: string; subtitle: string; library?: boolean };

const lensCopy = {
  personal: 'Private intelligence captured for this identity.',
  collective: 'Shared intelligence visible only by governed consent.',
  activity: 'A living operational record of meaningful events.',
};

export function FlagshipIntelligenceView({ title, subtitle, library = false }: Props) {
  const identity = useIdentity();
  const [events, setEvents] = useState<IntelligentEvent[]>([]);
  const [selected, setSelected] = useState(0);
  const [query, setQuery] = useState('');
  const [lens, setLens] = useState<keyof typeof lensCopy>('personal');
  const [state, setState] = useState<'loading' | 'ready' | 'error'>('loading');
  const [deepSearching, setDeepSearching] = useState(false);
  useEffect(() => {
    let alive = true;
    const target = new URLSearchParams(window.location.search).get('event_id') || '';
    if (!identity.is_authenticated) { setEvents([]); setState('ready'); return () => { alive = false; }; }
    (async () => {
      try {
        let feed: Awaited<ReturnType<typeof loadPrimaryIntelligence>> | null = null;
        for (let attempt = 0; attempt < 20; attempt += 1) {
          feed = await loadPrimaryIntelligence();
          if (!target || feed.events.some(e => e.event_id === target) || attempt === 19) break;
          await new Promise(r => setTimeout(r, 500));
        }
        if (!alive || !feed) return;
        const ordered = sortPrimaryIntelligence(feed.events);
        const targetIndex = target ? ordered.findIndex(e => e.event_id === target) : -1;
        setEvents(ordered); setSelected(targetIndex >= 0 ? targetIndex : 0); setState('ready');
      } catch { if (alive) setState('error'); }
    })();
    return () => { alive = false; };
  }, [identity.is_authenticated]);
  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return events;
    return events.filter(event => [
      event.source.label, event.human_input.raw, event.context.topic || '',
      ...(event.context.tags || []), event.lesson.text || '', event.meaning.text || '',
      event.action.text || '', event.whats_in_it_for_you || '',
    ].join(' ').toLowerCase().includes(q));
  }, [events, query]);

  const current = filtered[selected] || filtered[0];
  const index = current ? Math.max(0, filtered.findIndex(e => e.event_id === current.event_id)) : 0;
  const proofState = current ? current.machine_evidence.verification_state : 'WAITING';
  const nextAction = current?.action.text || 'No verified next action is recorded yet.';
  const continuity = current ? ['SOURCE', 'EVIDENCE', 'LEARNING', 'MEANING', 'ACTION', 'VERIFY'] : [];
  const deepSearch = async () => {
    if (!query.trim()) return;
    setDeepSearching(true);
    try {
      const result = await searchPrimaryIntelligence(query, {
        schema_version: 'PIS-1.1', generated_at: new Date().toISOString(),
        source: 'github:smart_feed_content', event_count: events.length, events,
      });
      setEvents(sortPrimaryIntelligence(result.events)); setSelected(0);
    } finally { setDeepSearching(false); }
  };

  if (state === 'error') return <section className="state-panel"><div className="state-orb">✦</div><b>CANONICAL INTELLIGENCE UNAVAILABLE</b><span>The Hub will not invent a feed when the source cannot be verified.</span></section>;
  if (state === 'loading') return <section className="state-panel"><div className="state-orb">◌</div><b>READING CANONICAL INTELLIGENCE</b><span>Retrieving the existing Project Intelligence source…</span></section>;

  return <section className="hub-experience" data-surface={library ? 'library' : 'intelligence-today'}>
    <div className="hub-commandline">
      <div><span className="command-kicker">NAYANET · PROJECT INTELLIGENCE</span><h1>{title}</h1></div>
      <div className="field-status"><i className="field-led" /> {identity.smart_name} · {events.length} OBJECTS · {proofState}</div>
    </div>
    <div className="hub-core">
      <aside className="lens-rail">
        <div className="lens-rail-head"><span>INTELLIGENCE</span><i>LIVE</i></div>
        <div className="lens-rail-orbit"><span /><span /><span /></div>
        {(Object.keys(lensCopy) as Array<keyof typeof lensCopy>).map(x => <button key={x} className={`lens-tab ${lens === x ? 'active' : ''}`} onClick={() => setLens(x)}><span className="lens-glyph">{x === 'personal' ? '◉' : x === 'collective' ? '◎' : '◷'}</span><span className="lens-copy"><b>{x.toUpperCase()}</b><small>{lensCopy[x]}</small></span><em>{x === lens ? '●' : '○'}</em></button>)}
        <div className="lens-divider" />
        <button className="rail-tool" onClick={() => window.dispatchEvent(new CustomEvent('nayanet:navigate', { detail: { path: routes.library } }))}><span>▱</span><b>LIBRARY</b></button>
        <button className="rail-tool" onClick={() => window.dispatchEvent(new CustomEvent('nayanet:navigate', { detail: { path: routes.reports } }))}><span>◫</span><b>REPORTS</b></button>
        <button className="rail-tool" onClick={() => window.dispatchEvent(new CustomEvent('nayanet:navigate', { detail: { path: routes.ledger } }))}><span>◇</span><b>LEDGER</b></button>
      </aside>
      <main className="intelligence-stage">
        <div className="signal-bar">
          <div className="signal-main"><span className="signal-kicker">{library ? 'INTELLIGENCE LIBRARY' : 'INTELLIGENCE TODAY'} · {lens.toUpperCase()}</span><strong>{current?.source.label || 'Your intelligence is ready.'}</strong><span>{current ? (current.weaver_synthesis.summary || current.human_input.raw) : subtitle}</span></div>
          <div className="signal-stats"><div><b>{filtered.length}</b><small>VISIBLE</small></div><div><b>{proofState}</b><small>TRUTH STATE</small></div><div><b>{lens.toUpperCase()}</b><small>LENS</small></div></div>
        </div>
        <div className="loop-panel"><span className="panel-eyebrow">COMPOUNDING LOOP</span><span className="loop-title">TRUTH → HUMAN USE</span><div className="loop-track">{continuity.map((x,i) => <span key={x} className={current && i < 4 ? 'lit' : ''}>{x}</span>)}</div><div className="loop-foot"><span>NO SECOND SOURCE OF TRUTH</span><b>Experience → Evidence → Learning → Meaning → Action → Verification</b></div></div>
        <div className="stage-head"><div><span>SMART FEED · CANONICAL PIS</span><h2>Living intelligence, made visible.</h2></div><p>{subtitle}</p></div>
        <div className="searchRow"><label className="searchWrap"><span>⌕</span><input value={query} onChange={e => { setQuery(e.target.value); setSelected(0); }} onKeyDown={e => { if (e.key === 'Enter') void deepSearch(); }} placeholder="Search intelligence — what, why, source, learning, meaning…" aria-label="Search intelligence" /></label><button className="ask" disabled={deepSearching} onClick={() => void deepSearch()}>{deepSearching ? '⌁ SEARCHING…' : '✦ TALK TO NAYA'}</button></div>
        {!current ? <section className="state-panel"><div className="state-orb">◌</div><b>NO VERIFIED INTELLIGENCE YET</b><span>Capture a Smart Note or wait for canonical PIS data. Nothing is fabricated to fill the space.</span></section> : <SmartFeedBoard event={current} />}
      </main>
      <aside className="intelligence-aside">
        {current ? <section className="naya-panel"><div className="naya-panel-top"><div className="naya-orb"><span>✦</span></div><div><span className="naya-eyebrow">NAYA · LIVE</span><b>EVIDENCE-AWARE GUIDE</b></div><i className="naya-live">READY</i></div><h2>{current.naya_interpretation.interpretation || 'Naya is reading the verified intelligence object.'}</h2><p className="naya-observation">{current.naya_interpretation.observation || current.human_input.raw}</p><div className="naya-sections"><div><span>WHAT IT MEANS</span><p>{current.meaning.text || 'Meaning has not been recorded yet.'}</p></div><div><span>WHAT TO DO</span><p>{nextAction}</p></div></div><div className="naya-proof"><div><span>SOURCE</span><b>BOUND</b></div><div><span>EVIDENCE</span><b>{proofState}</b></div><div><span>PRIVACY</span><b>{current.privacy.visibility}</b></div></div></section> : <section className="naya-panel empty"><div className="naya-orb"><span>✦</span></div><h2>Naya is ready.</h2><p>Capture or retrieve intelligence and the verified context will appear here.</p></section>}
        <section className="aside-panel"><span className="command-kicker">CONTINUITY</span><h3>The intelligence stays with you.</h3><div className="continuity"><div><b>{events.length}</b><span>OBJECTS</span></div><div><b>{filtered.length}</b><span>VISIBLE</span></div><div><b>{current ? '1' : '0'}</b><span>FOCUS</span></div></div><p>One canonical object. One visible truth. Reusable by the next Naya.</p></section>
        <section className="aside-panel next-panel"><span className="command-kicker">NEXT RESPONSIBLE ACTION</span><h3>{nextAction}</h3><button onClick={() => window.dispatchEvent(new CustomEvent('nayanet:navigate', { detail: { path: routes.feed } }))}>OPEN SMART FEED <span>→</span></button></section>
      </aside>
    </div>
  </section>;
}
