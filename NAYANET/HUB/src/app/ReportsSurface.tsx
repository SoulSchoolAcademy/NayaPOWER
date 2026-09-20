import { useEffect, useMemo, useState } from 'react';
import { useIdentity } from '../identity/session';
type ReportEvent = { event_id: string; title?: string; content?: string; created_at: string; status?: string; metadata?: Record<string, unknown> };

type Period = 'today' | 'week' | 'month' | 'year';

const periods: Array<{ key: Period; label: string; duration: number; description: string }> = [
  { key: 'today', label: 'TODAY', duration: 86_400_000, description: 'What happened and what matters today.' },
  { key: 'week', label: '7 DAYS', duration: 604_800_000, description: 'Patterns, learning, and movement across the last seven days.' },
  { key: 'month', label: '30 DAYS', duration: 2_592_000_000, description: 'Recurring signals and durable lessons across the last month.' },
  { key: 'year', label: 'YEAR', duration: 31_536_000_000, description: 'Long-horizon intelligence accumulated across the last year.' },
];

function asText(value: unknown) {
  return value == null ? '' : String(value);
}

function eventTitle(event: ReportEvent) {
  return event.source.label || event.human_input.raw || 'Untitled intelligence';
}

function isVerified(event: ReportEvent) {
  const state = event.status || ''.toLowerCase();
  return state.includes('verified') || event.status || ''.toLowerCase().includes('verified');
}

function within(event: ReportEvent, duration: number, now: number) {
  const time = new Date(event.created_at).getTime();
  return Number.isFinite(time) && now - time >= 0 && now - time <= duration;
}

function periodRows(events: ReportEvent[], duration: number, now: number) {
  return events.filter(event => within(event, duration, now));
}

function ReportCard({ period, events, now }: { period: typeof periods[number]; events: ReportEvent[]; now: number }) {
  const rows = periodRows(events, period.duration, now);
  const verified = rows.filter(isVerified).length;
  const learned = rows.filter(event => Boolean(Boolean(asText(event.metadata?.lesson).trim()))).length;
  const actions = rows.filter(event => Boolean(Boolean(asText(event.metadata?.action).trim()))).length;
  const uniqueTopics = new Set(rows.flatMap(event => Array.isArray(event.metadata?.tags) ? event.metadata.tags.filter((tag): tag is string => typeof tag === 'string') : [])).size;
  const latest = rows.slice(0, 5);

  return (
    <article className="report-card" data-period={period.key}>
      <div className="report-card-head">
        <div>
          <span className="feature-card-kicker">AUTO REPORT · {period.label}</span>
          <h2>{rows.length} CANONICAL EVENTS</h2>
        </div>
        <span className="report-card-status">{verified} VERIFIED</span>
      </div>
      <p>{period.description}</p>
      <div className="report-metrics">
        <div><b>{learned}</b><span>LESSONS</span></div>
        <div><b>{actions}</b><span>ACTIONS</span></div>
        <div><b>{uniqueTopics}</b><span>TAG SIGNALS</span></div>
      </div>
      {latest.length ? (
        <div className="report-latest">
          <span className="report-section-label">LATEST SIGNAL</span>
          {latest.map(event => (
            <div className="report-signal" key={event.event_id}>
              <b>{eventTitle(event)}</b>
              <span>{asText(event.metadata?.lesson) || asText(event.metadata?.meaning) || event.content || event.title || event.event_id}</span>
            </div>
          ))}
        </div>
      ) : (
        <div className="report-empty">No canonical events fall inside this period. The report is empty because the source is empty, not because synthetic data was created.</div>
      )}
    </article>
  );
}

export function ReportsSurface() {
  const identity = useIdentity();
  const [events, setEvents] = useState<IntelligentEvent[]>([]);
  const [busy, setBusy] = useState(true);
  const [error, setError] = useState('');
  const [query, setQuery] = useState('');
  const [now, setNow] = useState(() => Date.now());

  const load = async () => {
    setBusy(true);
    setError('');
    try {
      const runtime = window.NayaAssistantRuntime;
      if (!runtime) throw new Error('ASSISTANT_RUNTIME_UNAVAILABLE');
      if (!runtime.snapshot()?.authenticated) throw new Error('AUTH_REQUIRED');
      const rows = await runtime.retrieve();
      setEvents(Array.isArray(rows) ? rows as ReportEvent[] : []);
      setNow(Date.now());
    } catch (error) {
      setError(error instanceof Error ? error.message : 'REPORTS_LOAD_FAILED');
      setEvents([]);
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
    return events.filter(event =>
      [eventTitle(event), event.human_input.raw, event.context.topic || '', ...(Array.isArray(event.metadata?.tags) ? event.metadata.tags.filter((tag): tag is string => typeof tag === 'string') : []), event.lesson.text || '', event.meaning.text || '']
        .join(' ')
        .toLowerCase()
        .includes(q),
    );
  }, [events, query]);

  if (!identity.is_authenticated) {
    return <section className="feature-surface" data-surface="reports"><div className="feature-hero"><div><div className="eyebrow">NAYANET · REPORTS · COMPRESSION · LEARNING · TIME</div><h1>Your Reports</h1><p>Automatic time-horizon projections from canonical intelligence.</p></div></div><div className="feature-empty"><b>AUTHENTICATION REQUIRED</b><span>Reports read the authenticated canonical intelligence boundary. No preview data is substituted.</span></div></section>;
  }

  return (
    <section className="feature-surface" data-surface="reports">
      <div className="feature-hero">
        <div><div className="eyebrow">NAYANET · REPORTS · COMPRESSION · LEARNING · TIME</div><h1>Your Reports</h1><p>Automatic time-horizon projections from the intelligence you have actually captured.</p></div>
        <div className="feature-state">AUTHENTICATED · {events.length} CANONICAL EVENTS</div>
      </div>
      <div className="feature-toolbar">
        <label><span>⌕</span><input value={query} onChange={event => setQuery(event.target.value)} placeholder="Search report signals…" aria-label="Search report signals" /></label>
        <button onClick={() => void load()} disabled={busy}>{busy ? 'READING…' : '↻ REFRESH'}</button>
        <span>{filtered.length} MATCHING EVENTS</span>
      </div>
      {error ? <div className="feature-empty"><b>REPORT SOURCE BLOCKED</b><span>{error}</span></div> : busy ? <div className="feature-empty"><b>BUILDING REPORT PROJECTIONS…</b><span>Reading the canonical event stream. No report table is required and no synthetic report records are created.</span></div> : <div className="report-grid">{periods.map(period => <ReportCard key={period.key} period={period} events={filtered} now={now} />)}</div>}
      <div className="feature-foot"><span>CANONICAL SOURCE</span><b>nayanet_cognition_events</b><span>•</span><span>CAPTURE → LEARN → RETAIN → COMPOUND</span></div>
    </section>
  );
}
