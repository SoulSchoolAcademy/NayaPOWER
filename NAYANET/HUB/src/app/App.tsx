import { useEffect, useMemo, useState } from 'react';
import type { ReactNode } from 'react';
import { IdentityProvider, useIdentity } from '../identity/session';
import { AuthPanel } from '../identity/AuthPanel';
import type { IntelligentEvent, Lens } from '../intelligence/types';
import { SmartFeedBoard } from '../intelligence/SmartFeedBoard';
import { initializeCognition, rememberIntelligence } from '../intelligence/cognition';
import { loadPrimaryIntelligence, sortPrimaryIntelligence } from '../data/pis';
import { loadSmartFeed } from '../intelligence/smartFeedProjection';
import type { PISFeed } from '../data/pis';
import { SparklingShapeShell } from './SparklingShapeShell';
import { routes } from './routes';
import { FeatureSurface } from './FeatureSurface';
import { ActivityBoard } from '../activity/ActivityBoard';

type LensTab = { key: Lens; label: string; detail: string; icon: string };
const lensTabs: LensTab[] = [
  { key: 'personal', label: 'PERSONAL', detail: 'Your private intelligence and saves', icon: '◉' },
  { key: 'activity', label: 'ACTIVITY', detail: 'What Naya and the system are doing', icon: '◷' },
  { key: 'collective', label: 'COLLECTIVE', detail: 'Shared intelligence worth discovering', icon: '◎' },
];
const routeLens = (path: string): Lens => path === routes.today || path === routes.reports ? 'activity' : path === routes.collective || path === routes.share ? 'collective' : 'personal';
const compact = (value: string | undefined, fallback: string) => value?.trim() || fallback;

function IntelligenceCard({ event, onOpen }: { event: IntelligentEvent; onOpen: () => void }) {
  const summary = compact(event.weaver_synthesis.summary, event.source.label);
  const nutshell = compact(event.naya_interpretation.observation, event.human_input.raw);
  const meaning = compact(event.meaning.text || event.meaning.significance, 'Meaning is not yet recorded.');
  const value = compact(event.whats_in_it_for_you, 'Human value is not yet recorded.');
  const evidence = event.machine_evidence.verification_state || event.status;
  return <button className="intel-card block" onClick={onOpen} aria-label={`Open ${event.source.label}`}>
    <div className="intel-card-top"><span className="intel-source">{event.source.type.replaceAll('_', ' ').toUpperCase()} · INTELLIGENCE</span><span className="intel-state">{evidence.toUpperCase()}</span></div>
    <h3>{summary}</h3><p className="intel-nutshell">{nutshell}</p>
    <div className="intel-meta"><span className="intel-chip">{event.context.topic || 'NayaNET'}</span>{(event.context.tags || []).slice(0, 3).map(tag => <span className="intel-chip" key={tag}>{tag}</span>)}<span className="intel-chip">{new Date(event.created_at).toLocaleDateString()}</span></div>
    <div className="intel-footer"><div className="intel-mini"><span>WHY IT MATTERS</span><p>{meaning}</p></div><div className="intel-mini"><span>WHAT'S IN IT FOR YOU</span><p>{value}</p></div><div className="intel-mini"><span>NAYA / NEXT</span><p>{compact(event.action.text, 'Open the intelligence to inspect the next action.')}</p></div></div>
  </button>;
}

function SmartNoteCapture({ onCaptured }: { onCaptured: () => void }) {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [status, setStatus] = useState('');
  const [busy, setBusy] = useState(false);
  const capture = async () => {
    if (!content.trim() || busy) return;
    setBusy(true); setStatus('PERSISTING INTELLIGENCE…');
    try {
      const result = await rememberIntelligence({
        event_id: 'hub-smart-note-' + Date.now(),
        title: title.trim() || content.trim().slice(0, 100),
        content: content.trim(),
        source: 'nayanet-hub.smart-note-capture',
        project: 'NayaNET',
        status: 'active', actor: 'human',
        tags: ['smart-note', 'intelligent-hub', 'captured'],
        metadata: { capture_surface: 'NayaNET Intelligent Hub', continuity: 'conversation-to-compounding-intelligence' },
      });
      setStatus(result.persisted ? '✓ CAPTURED • PERSISTED • READY TO COMPOUND' : 'CAPTURED • ' + result.persistence.status.toUpperCase());
      setTitle(''); setContent(''); onCaptured();
    } catch (error) { setStatus(error instanceof Error ? error.message : 'CAPTURE_FAILED'); }
    finally { setBusy(false); }
  };
  return <section className="smart-note-capture">
    <div><div className="hub-rail-label">CAPTURE WHAT MATTERS</div><h2>Turn an aha into durable intelligence.</h2><p>Capture a decision, lesson, mistake, discovery, or mission update. NayaNET records it so it can be retrieved and compounded later.</p></div>
    <input value={title} onChange={e => setTitle(e.target.value)} placeholder="Title (optional)" aria-label="Smart Note title" />
    <textarea value={content} onChange={e => setContent(e.target.value)} placeholder="What should Naya remember?" aria-label="Smart Note content" rows={4} />
    <div className="capture-actions"><button className="powerBtn" disabled={!content.trim() || busy} onClick={() => void capture()}>{busy ? 'PERSISTING…' : '✦ CAPTURE SMART NOTE'}</button>{status && <span>{status}</span>}</div>
  </section>;
}

function HubHome({ onExplore }: { onExplore: (event?: IntelligentEvent) => void }) {
  const identity = useIdentity();
  const [events, setEvents] = useState<IntelligentEvent[]>([]);
  const [feed, setFeed] = useState<PISFeed | undefined>();
  const [error, setError] = useState('');
  const [selected, setSelected] = useState<IntelligentEvent | undefined>();
  useEffect(() => { let alive = true; loadPrimaryIntelligence().then(value => { if (!alive) return; setFeed(value); setEvents(sortPrimaryIntelligence(value.events)); }).catch(reason => { if (alive) setError(reason instanceof Error ? reason.message : 'PIS_FEED_UNAVAILABLE'); }); return () => { alive = false; }; }, [identity.is_authenticated]);
  if (selected) return <div className="hub-home-restored"><button className="hub-back" onClick={() => setSelected(undefined)}>← BACK TO INTELLIGENCE</button><SmartFeedBoard event={selected} /></div>;
  const open = (event?: IntelligentEvent) => event ? setSelected(event) : onExplore();
  return <div className="hub-home-restored">
        <section className="hero"><div className="eyebrow">NAYANET · LIVING INTELLIGENCE NETWORK</div><h1>Your Intelligence Today</h1><p>NayaNET is where intelligence becomes visible, understandable, useful, and reusable — so what you learn today can compound into what Naya and you can do tomorrow.</p></section>
    <SmartNoteCapture onCaptured={() => { loadPrimaryIntelligence().then(value => { setFeed(value); setEvents(sortPrimaryIntelligence(value.events)); }).catch(() => undefined); }} />
    <div className="feedNav">{lensTabs.map(tab => <button key={tab.key} onClick={() => open()}>{tab.icon} {tab.label} FEED</button>)}</div>
    <div className="feedHead"><div><h2>Living Intelligence</h2><p>{feed?.source === 'supabase:nayanet_intelligence_index' ? 'Persistent intelligence is connected.' : 'The Hub is ready for canonical intelligence.'}</p></div><span className="feedCount">{events.length} OBJECTS</span></div>
    {error ? <div className="hub-empty"><b>INTELLIGENCE FEED UNAVAILABLE</b><span>{error}</span></div> : events.length ? <div className="blocks">{events.slice(0, 3).map(event => <IntelligenceCard key={event.event_id} event={event} onOpen={() => open(event)} />)}</div> : <div className="hub-empty"><b>NO INTELLIGENCE YET</b><span>Capture a canonical intelligence event and it will appear here.</span></div>}
  </div>;
}

function CommandCenter({ initialLens = 'personal' }: { initialLens?: Lens }) {
  if (initialLens === 'activity') return <ActivityBoard />;
  const identity = useIdentity();
  const [events, setEvents] = useState<IntelligentEvent[]>([]);
  const [feed, setFeed] = useState<PISFeed | undefined>();
  const [error, setError] = useState('');
  const [lens, setLens] = useState<Lens>(initialLens);
  const [query, setQuery] = useState('');
  const [selected, setSelected] = useState<IntelligentEvent | undefined>();
  useEffect(() => setLens(initialLens), [initialLens]);
  useEffect(() => { let alive = true; setError(''); const load = identity.is_authenticated ? loadSmartFeed(lens, 30).then(value => ({ schema_version:'SMART-FEED-1', generated_at:new Date().toISOString(), source:'supabase:nayanet_intelligence_index' as const, event_count:value.events.length, events:value.events })) : loadPrimaryIntelligence(); load.then(value => { if (!alive) return; setFeed(value); setEvents(sortPrimaryIntelligence(value.events)); }).catch(reason => { if (alive) setError(reason instanceof Error ? reason.message : 'SMART_FEED_UNAVAILABLE'); }); return () => { alive = false; }; }, [identity.is_authenticated, lens]);
  useEffect(() => { const handler = (event: Event) => { const q = (event as CustomEvent<{ query?: string }>).detail?.query || ''; setQuery(q); setSelected(undefined); }; addEventListener('nayanet:search', handler); return () => removeEventListener('nayanet:search', handler); }, []);
  const filtered = useMemo(() => { const q = query.trim().toLowerCase(); if (!q) return events; return events.filter(event => [event.source.label, event.human_input.raw, event.context.topic, ...(event.context.tags || []), event.naya_interpretation.observation || '', event.naya_interpretation.interpretation || '', event.meaning.text || '', event.action.text || '', event.whats_in_it_for_you || ''].join(' ').toLowerCase().includes(q)); }, [events, query]);
  const counts = { collective: events.length, activity: events.length, personal: events.length };
  const activeTab = lensTabs.find(tab => tab.key === lens) || lensTabs[0];
  if (selected) return <div className="hub-command"><button className="hub-back" onClick={() => setSelected(undefined)}>← BACK TO {activeTab.label}</button><div className="hub-detail"><SmartFeedBoard event={selected} /></div></div>;
  return <div className="hub-command">
    <header className="hub-command-head"><div className="hub-command-title"><div className="eyebrow">NAYANET · LIVING INTELLIGENCE NETWORK</div><h1>{activeTab.label.charAt(0) + activeTab.label.slice(1).toLowerCase()} Intelligence</h1><p>{activeTab.detail}. Discover the signal first, then open one intelligence object at full depth.</p></div><div className="hub-live">{feed?.source === 'supabase:nayanet_intelligence_index' ? 'PERSISTENT' : 'CANONICAL'} · {events.length} OBJECTS</div></header>
    <div className="hub-lensbar" role="tablist" aria-label="Smart feeds">{lensTabs.map(tab => <button key={tab.key} role="tab" aria-selected={lens === tab.key} className={`hub-lens ${lens === tab.key ? 'active' : ''}`} onClick={() => setLens(tab.key)}><b>{tab.icon} {tab.label} FEED</b><span>{tab.detail} · {counts[tab.key]}</span></button>)}</div>
    <div className="hub-search"><span>⌕</span><input value={query} onChange={event => setQuery(event.target.value)} placeholder="Search intelligence, people, topics, meaning, evidence…" aria-label="Search NayaNET intelligence"/><kbd>⌘ K</kbd></div>
    <div className="hub-workspace"><section className="hub-stream"><div className="hub-stream-head"><h2>{query ? `Search results for “${query}”` : 'Living intelligence'}</h2><span>{filtered.length} {filtered.length === 1 ? 'object' : 'objects'} · open any block for the full intelligence board</span></div>{error ? <div className="hub-empty"><b>INTELLIGENCE FEED UNAVAILABLE</b>{error}</div> : filtered.length ? <div className="hub-results">{filtered.map(event => <IntelligenceCard key={event.event_id} event={event} onOpen={() => setSelected(event)} />)}</div> : <div className="hub-empty"><b>{query ? 'NO INTELLIGENCE MATCHES' : 'NO INTELLIGENCE YET'}</b><span>{query ? 'Try a different word or topic.' : 'The Hub is waiting for a canonical intelligence event.'}</span></div>}</section>
      <aside className="hub-rail"><section className="hub-rail-card"><div className="hub-rail-label">NAYA · NOW</div><h3>{events[0] ? compact(events[0].source.label, 'Intelligence is flowing.') : 'Waiting for intelligence.'}</h3><p>{events[0] ? compact(events[0].naya_interpretation.observation, 'A canonical event is available to explore.') : 'The Hub will not fabricate a feed when the upstream intelligence source is empty.'}</p><div className="hub-next"><i>✦</i><span>{events[0] ? compact(events[0].action.text, 'Open the newest board and inspect what happens next.') : 'Next: capture a canonical intelligence event.'}</span></div></section><section className="hub-rail-card"><div className="hub-rail-label">INTELLIGENCE LOOP</div><div className="hub-rail-value">CAPTURE → COMPOUND</div><p>Discover → understand → connect → act → verify → learn. The feed is the living projection of that loop.</p></section><section className="hub-rail-card"><div className="hub-rail-label">TRUST SURFACE</div><h3>{events.filter(event => event.machine_evidence.verification_state === 'VERIFIED').length} verified</h3><p>Verification is a truth state. Open a board for source, evidence, uncertainty and provenance.</p></section></aside>
    </div>
  </div>;
}

function Workspace({ path }: { path: string }): ReactNode {
  if (path === routes.settings) return <AuthPanel />;
  if (path === routes.home) return <HubHome onExplore={() => { history.pushState({}, '', routes.feed); dispatchEvent(new PopStateEvent('popstate')); }} />;
  const surfaces: Record<string, Parameters<typeof FeatureSurface>[0]['kind']> = { [routes.today]:'today', [routes.reports]:'reports', [routes.share]:'share', [routes.connections]:'connections', [routes.lists]:'lists', [routes.mail]:'mail', [routes.spaces]:'spaces', [routes.ledger]:'ledger' };
  const surface = surfaces[path];
  if (surface) return <FeatureSurface kind={surface} />;
  return <CommandCenter initialLens={routeLens(path)} />;
}

export default function App() {
  useEffect(() => { initializeCognition().catch(() => {}); }, []);
  return <IdentityProvider><SparklingShapeShell>{path => <Workspace path={path} />}</SparklingShapeShell></IdentityProvider>;
}
