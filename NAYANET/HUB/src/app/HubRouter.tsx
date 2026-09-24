import { useEffect, useMemo, useState } from 'react';
import { AuthPanel } from '../identity/AuthPanel';
import { SmartMailSurface } from './SmartMailSurface';
import { FeatureSurface } from './FeatureSurface';
import { SmartFeedBoard } from '../intelligence/SmartFeedBoard';
import { loadPrimaryIntelligence, searchPrimaryIntelligence, sortPrimaryIntelligence } from '../data/pis';
import type { IntelligentEvent } from '../intelligence/types';
import { routes } from './routes';
import { useIdentity } from '../identity/session';
import { DreamSurface } from './DreamSurface';
import { ReportsSurface } from './ReportsSurface';
import { SmartConnectSurface } from './SmartConnectSurface';
import { SmartListsSurface } from './SmartListsSurface';
import { ConnectionsSurface } from './ConnectionsSurface';
import { NayaPlaySurface } from './NayaPlaySurface';
import { SmartSpacesSurface } from './SmartSpacesSurface';
import { SettingsSurface } from './SettingsSurface';
import { SmartNoteSurface } from './SmartNoteSurface';
import { IntelligenceTodaySurface } from './IntelligenceTodaySurface';

function FeedView({ title, subtitle, library = false }: { title: string; subtitle: string; library?: boolean }) {
  const identity = useIdentity();
  const [events, setEvents] = useState<IntelligentEvent[]>([]);
  const [selected, setSelected] = useState(0);
  const [query, setQuery] = useState('');
  const [state, setState] = useState<'loading' | 'ready' | 'error'>('loading');
  const [deepSearching, setDeepSearching] = useState(false);

  useEffect(() => {
    let alive = true;
    const targetEventId = new URLSearchParams(window.location.search).get('event_id') || '';
    if (!identity.is_authenticated) {
      setEvents([]);
      setState('loading');
      return () => { alive = false; };
    }
    setState('loading');
    (async () => {
      try {
        let feed: Awaited<ReturnType<typeof loadPrimaryIntelligence>> | null = null;
        for (let attempt = 0; attempt < 20; attempt += 1) {
          feed = await loadPrimaryIntelligence();
          if (!targetEventId || feed.events.some(event => event.event_id === targetEventId) || attempt === 19) break;
          await new Promise(resolve => setTimeout(resolve, 500));
        }
        if (!alive || !feed) return;
        const ordered = sortPrimaryIntelligence(feed.events);
        setEvents(ordered);
        const targetIndex = targetEventId ? ordered.findIndex(event => event.event_id === targetEventId) : -1;
        setSelected(targetIndex >= 0 ? targetIndex : 0);
        setState('ready');
      } catch {
        if (alive) setState('error');
      }
    })();
    return () => { alive = false; };
  }, [identity.is_authenticated, window.location.search]);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return events;
    return events.filter(event => [
      event.source.label,
      event.human_input.raw,
      event.context.topic || '',
      ...(event.context.tags || []),
      event.lesson.text || '',
      event.meaning.text || '',
      event.action.text || '',
    ].join(' ').toLowerCase().includes(q));
  }, [events, query]);

  if (state === 'loading') return <section className="feed-loading"><div className="loading-orbit" /><b>LOADING CANONICAL INTELLIGENCE</b><p>Reading the existing intelligence source. No synthetic feed is created.</p></section>;
  if (state === 'error') return <section className="feature-empty"><b>INTELLIGENCE LOAD FAILED</b><span>The Hub could not retrieve canonical intelligence. Nothing has been fabricated to fill the gap.</span></section>;

  const current = filtered[selected] || filtered[0];
  const index = current ? Math.max(0, filtered.findIndex(event => event.event_id === current.event_id)) : 0;

  return <section className="hub-route">
    <div className="orientation">
      <div><span className="eyebrow">NAYANET · LIVING INTELLIGENCE</span><h1>{title}</h1><p className="sub">{subtitle}</p></div>
      <div className="nayaMark"><span>✦</span><b>NAYA</b><small>INTELLIGENCE MADE VISIBLE</small></div>
    </div>
    <div className="searchRow">
      <label className="searchWrap"><span>⌕</span><input value={query} onChange={e => { setQuery(e.target.value); setSelected(0); }} onKeyDown={async e => { if(e.key !== 'Enter' || !query.trim()) return; setDeepSearching(true); try { const result = await searchPrimaryIntelligence(query, { schema_version:'PIS-1.1', generated_at:new Date().toISOString(), source:'github:smart_feed_content', event_count:events.length, events }); setEvents(sortPrimaryIntelligence(result.events)); setSelected(0); } finally { setDeepSearching(false); } }} placeholder={library ? 'Search your intelligence library… Press Enter for deep retrieval' : 'Search intelligence — what, why, source, learning, meaning… Press Enter for deep retrieval'} aria-label="Search intelligence" /></label>
      <button className="ask" disabled={deepSearching} onClick={() => document.querySelector<HTMLInputElement>('.universal-search input')?.focus()}>{deepSearching ? '⌁ SEARCHING CANONICAL INTELLIGENCE…' : '✦ TALK TO NAYA'}</button>
    </div>
    <div className="feedHead"><div><span className="eyebrow">{library ? 'INTELLIGENCE LIBRARY' : 'YOUR INTELLIGENCE TODAY'}</span><h2>{filtered.length} INTELLIGENT {filtered.length === 1 ? 'BLOCK' : 'BLOCKS'}</h2><p className="feedSub">One canonical intelligence object can be understood, applied, verified, and reused without creating a second source of truth.</p></div><div className="lens"><button className="selected">INTELLIGENCE</button><button onClick={() => window.dispatchEvent(new CustomEvent('nayanet:navigate', { detail: { path: routes.mail } }))}>SMART MAIL</button></div></div>
    {!current ? <section className="feature-empty"><b>NO MATCHING INTELLIGENCE</b><span>No verified intelligence matches this search.</span></section> :
      <><div className="feed-selector">{filtered.slice(0, 12).map((event, i) => <button key={event.event_id} className={i === index ? 'selected' : ''} onClick={() => setSelected(i)}>{event.source.label}</button>)}</div><SmartFeedBoard event={current} /></>}
  </section>;
}

export function HubRouter({ path }: { path: string }) {
  switch (path) {
    case routes.home:
    case routes.today:
      return <IntelligenceTodaySurface />;
    case routes.feed:
      return <FeedView title="Intelligence" subtitle="Living intelligence made visible, useful, and reusable." />;
    case routes.notes:
      return <SmartNoteSurface />;
    case routes.library:
      return <FeedView title="Intelligence Library" subtitle="Find the intelligence that exists, understand it, and reuse it without losing provenance." library />;
    case routes.reports:
      return <ReportsSurface />;
    case routes.lists:
      return <SmartListsSurface />;
    case routes.connect:
      return <SmartConnectSurface />;
    case routes.spaces:
      return <SmartSpacesSurface />;
    case routes.connections:
      return <ConnectionsSurface />;
    case routes.mail:
      return <SmartMailSurface />;
    case routes.ledger:
    case routes.evidence:
      return <FeatureSurface kind="ledger" />;
    case routes.settings:
      return <SettingsSurface />;
    case routes.dream:
      return <DreamSurface />;
    case routes.play:
      return <NayaPlaySurface />;
    default:
      return <FeedView title="Your Intelligence Today" subtitle="What matters now — the intelligence you can understand, use, verify, and carry forward." />;
  }
}
