import { useEffect, useMemo, useState } from 'react';
import { useIdentity } from '../identity/session';
import { loadPrimaryIntelligence } from '../data/pis';
import type { IntelligentEvent } from '../intelligence/types';

export function SmartShareSurface() {
  const identity = useIdentity();
  const [events, setEvents] = useState<IntelligentEvent[]>([]);
  const [selected, setSelected] = useState('');
  const [query, setQuery] = useState('');
  const [busy, setBusy] = useState(true);
  const [publishing, setPublishing] = useState(false);
  const [status, setStatus] = useState('');

  const load = async () => {
    setBusy(true);
    setStatus('');
    try {
      const runtime = window.NayaAssistantRuntime;
      if (!runtime) throw new Error('ASSISTANT_RUNTIME_UNAVAILABLE');
      if (!runtime.snapshot()?.authenticated) throw new Error('AUTH_REQUIRED');
      const feed = await loadPrimaryIntelligence();
      const owned = feed.events.filter(event => event.user_id === runtime.snapshot()?.user_id);
      setEvents(owned);
      setSelected(current => current && owned.some(event => event.event_id === current) ? current : owned[0]?.event_id || '');
    } catch (error) {
      setEvents([]);
      setStatus(error instanceof Error ? error.message : 'SMART_SHARE_LOAD_FAILED');
    } finally {
      setBusy(false);
    }
  };

  useEffect(() => {
    if (!identity.is_authenticated) {
      setEvents([]);
      setBusy(false);
      return;
    }
    void load();
  }, [identity.is_authenticated]);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return events;
    return events.filter(event => [event.source.label, event.human_input.raw, event.context.topic || '', ...(event.context.tags || [])].join(' ').toLowerCase().includes(q));
  }, [events, query]);

  const selectedEvent = filtered.find(event => event.event_id === selected) || events.find(event => event.event_id === selected);

  const publish = async () => {
    if (!selectedEvent) return;
    setPublishing(true);
    setStatus('PUBLISHING THROUGH THE CANONICAL CONSENT BOUNDARY…');
    try {
      const runtime = window.NayaAssistantRuntime;
      if (!runtime) throw new Error('ASSISTANT_RUNTIME_UNAVAILABLE');
      if (!runtime.snapshot()?.authenticated) throw new Error('AUTH_REQUIRED');
      const result = await runtime.publishSmartFeed({ sourceEventId: selectedEvent.event_id }) as { publication?: { id?: string; status?: string; consent_state?: string }; receipt?: { id?: string; receipt_id?: string } };
      const publicationId = result.publication?.id || '';
      if (!publicationId) throw new Error('CANONICAL_PUBLICATION_ID_NOT_RETURNED');
      setStatus('PUBLISHED · PUBLICATION ' + publicationId + ' · CONSENT ' + (result.publication?.consent_state || 'CANONICAL'));
      await load();
    } catch (error) {
      setStatus('SHARE BLOCKED · ' + (error instanceof Error ? error.message : 'CANONICAL_PUBLICATION_FAILED'));
    } finally {
      setPublishing(false);
    }
  };

  if (!identity.is_authenticated) {
    return <section className="feature-surface" data-surface="share"><div className="feature-hero"><div><div className="eyebrow">NAYANET · CONSENT · PROVENANCE · SHARING</div><h1>Smart Share</h1><p>Share intelligence by choice while preserving provenance and privacy.</p></div></div><div className="feature-empty"><b>AUTHENTICATION REQUIRED</b><span>Private intelligence cannot be published from a preview session.</span></div></section>;
  }

  return (
    <section className="feature-surface" data-surface="share">
      <div className="feature-hero"><div><div className="eyebrow">NAYANET · CONSENT · PROVENANCE · SHARING</div><h1>Smart Share</h1><p>Choose exactly which intelligence you want to publish. Nothing is silently selected for you.</p></div><div className="feature-state">AUTHENTICATED · {events.length} OWNED</div></div>
      <div className="feature-toolbar"><label><span>⌕</span><input value={query} onChange={event => setQuery(event.target.value)} placeholder="Find intelligence to share…" aria-label="Find intelligence to share" /></label><button onClick={() => void load()} disabled={busy || publishing}>{busy ? 'READING…' : '↻ REFRESH'}</button><span>{filtered.length} AVAILABLE</span></div>
      <div className="share-layout">
        <div className="share-events">{filtered.map(event => <button key={event.event_id} className={'share-event ' + (selected === event.event_id ? 'selected' : '')} onClick={() => setSelected(event.event_id)}><b>{event.source.label}</b><span>{event.human_input.raw}</span><small>{event.privacy.visibility} · {event.trust.level}</small></button>)}</div>
        <div className="share-panel">
          {selectedEvent ? <><span className="feature-card-kicker">SELECTED INTELLIGENCE</span><h2>{selectedEvent.source.label}</h2><p>{selectedEvent.human_input.raw}</p><div className="share-consent"><b>CONSENT BOUNDARY</b><span>Publishing crosses from your private intelligence into the collective publication path. The governed runtime remains the authority for the publication.</span></div><button className="share-publish" onClick={() => void publish()} disabled={publishing}>{publishing ? 'PUBLISHING…' : 'PUBLISH THIS INTELLIGENCE'}</button></> : <div className="feature-empty"><b>SELECT INTELLIGENCE</b><span>Choose an owned intelligence object before publishing.</span></div>}
        </div>
      </div>
      {status && <div className="feature-status" role="status">{status}</div>}
      <div className="feature-foot"><span>GOVERNED PATH</span><b>PRIVATE → EXPLICIT SHARE → COLLECTIVE</b><span>•</span><span>SHARE THE WISDOM · NOT THE PERSON</span></div>
    </section>
  );
}
