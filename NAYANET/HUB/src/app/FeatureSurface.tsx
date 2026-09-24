import { useEffect, useState } from 'react';
import { useIdentity } from '../identity/session';

type Row = Record<string, unknown>;
const text = (value: unknown) => value == null ? '' : String(value);
const short = (value: string, max = 220) => value.length > max ? value.slice(0, max - 1) + '…' : value;

function runtime() {
  const rt = window.NayaAssistantRuntime;
  if (!rt) throw new Error('ASSISTANT_RUNTIME_UNAVAILABLE');
  if (!rt.snapshot?.()?.authenticated) throw new Error('AUTH_REQUIRED');
  return rt;
}
function recordId(row: Row, index: number) { return text(row.ledger_event_id || row.id || row.source_id) || String(index); }
function pick(row: Row, keys: string[]) {
  for (const key of keys) { const value = text(row[key]).trim(); if (value) return value; }
  return '';
}

export function FeatureSurface({ kind }: { kind: 'ledger' | 'mail' | 'spaces' | 'lists' | 'share' | 'connections' | 'reports' | 'today' }) {
  const identity = useIdentity();
  const [rows, setRows] = useState<Row[]>([]);
  const [busy, setBusy] = useState(true);
  const [error, setError] = useState('');
  const [query, setQuery] = useState('');
  const [selected, setSelected] = useState<Row | null>(null);
  const [inspectBusy, setInspectBusy] = useState(false);
  const [inspectStatus, setInspectStatus] = useState('');

  const load = async () => {
    setBusy(true); setError('');
    try {
      const rt: any = runtime();
      if (kind !== 'ledger') throw new Error('CANONICAL_RUNTIME_SURFACE_NOT_BOUND');
      const data = await rt.listSmartLedger();
      setRows(Array.isArray(data) ? data as Row[] : []);
    } catch (e) {
      setRows([]); setError(e instanceof Error ? e.message : 'LEDGER_LOAD_FAILED');
    } finally { setBusy(false); }
  };

  useEffect(() => {
    if (!identity.is_authenticated) { setRows([]); setBusy(false); return; }
    void load();
  }, [identity.is_authenticated, kind]);

  const filtered = rows.filter(row => {
    const q = query.trim().toLowerCase();
    return !q || Object.values(row).some(value => text(value).toLowerCase().includes(q));
  });

  const inspect = async () => {
    if (!selected || inspectBusy) return;
    setInspectBusy(true); setInspectStatus('');
    try {
      const rt = runtime();
      const ledgerEventId = text(selected.ledger_event_id || selected.id);
      if (!ledgerEventId) throw new Error('LEDGER_EVENT_ID_MISSING');
      const result = await rt.record({
        title: 'Smart Ledger evidence inspection',
        content: JSON.stringify({
          ledger_event_id: ledgerEventId,
          source_id: selected.source_id || null,
          verification: selected.verification || null,
          evidence_refs: selected.evidence_refs || null,
        }),
        source: 'nayanet-hub.smart-ledger.inspect',
        project: 'NayaNET',
        status: 'active',
        actor: 'human',
        tags: ['intelligent-hub', 'smart-ledger', 'inspect-evidence'],
        metadata: { action: 'inspect_evidence', ledger_event_id: ledgerEventId, persistence_boundary: 'authenticated-canonical-runtime' },
      });
      const receiptId = text(result?.receipt?.id || result?.receipt?.receipt_id || result?.receipt_id);
      const eventId = text(result?.event_id || result?.event?.event_id);
      setInspectStatus('INSPECT PERSISTED · ' + (receiptId ? 'RECEIPT ' + receiptId : 'RECEIPT NOT RETURNED') + (eventId ? ' · EVENT ' + eventId : ''));
      await load();
    } catch (e) {
      setInspectStatus('INSPECT BLOCKED · ' + (e instanceof Error ? e.message : 'LEDGER_INSPECT_FAILED'));
    } finally { setInspectBusy(false); }
  };

  if (!identity.is_authenticated) {
    return <section className="feature-surface" data-surface="ledger">
      <div className="feature-hero"><div><div className="eyebrow">NAYANET · ACCOUNTABILITY · ACTION · EVIDENCE</div><h1>Smart Ledger</h1><p>See what happened, what was authorized, and what evidence followed.</p></div></div>
      <div className="feature-empty"><b>AUTHENTICATION REQUIRED</b><span>Ledger records are private to the authenticated identity. No browser session is fabricated.</span></div>
    </section>;
  }

  return <section className="feature-surface" data-surface="ledger">
    <div className="feature-hero">
      <div><div className="eyebrow">NAYANET · ACCOUNTABILITY · ACTION · EVIDENCE</div><h1>Smart Ledger</h1><p>Inspect canonical accountability records through the governed runtime. RECEIVED, AUTHORIZED, EXECUTED, VERIFIED, and PROJECTED remain distinct.</p></div>
      <div className="feature-state">AUTHENTICATED · {rows.length} RECORDS</div>
    </div>
    <div className="feature-toolbar">
      <label><span>⌕</span><input value={query} onChange={e => setQuery(e.target.value)} placeholder="Search ledger evidence…" aria-label="Search Smart Ledger" /></label>
      <button onClick={() => void load()} disabled={busy}>↻ REFRESH</button><span>{filtered.length} VISIBLE</span>
    </div>
    {busy ? <div className="feature-empty"><b>READING CANONICAL LEDGER…</b><span>Loading owner-scoped Ledger records through the governed runtime.</span></div>
      : error ? <div className="feature-empty"><b>LEDGER RETRIEVAL BLOCKED</b><span>{error}</span><button onClick={() => void load()}>RETRY WITH NEW INFORMATION</button></div>
      : !filtered.length ? <div className="feature-empty"><b>NO LEDGER RECORDS</b><span>{query ? 'No canonical records match this search.' : 'No Ledger events are visible for this identity yet.'}</span></div>
      : <div className="feature-cards">{filtered.map((row, index) => {
        const title = pick(row, ['event_type', 'title', 'action', 'source_id']) || 'Ledger event';
        const summary = pick(row, ['outcome', 'result', 'description', 'summary', 'verification']);
        const status = pick(row, ['status', 'verification']);
        return <article className="feature-card" key={recordId(row, index)}>
          <div className="feature-card-head"><div><span className="feature-card-kicker">LEDGER · CANONICAL</span><h2>{short(title, 120)}</h2></div>{status && <span className="feature-card-status">{status}</span>}</div>
          {summary && <p>{short(summary)}</p>}
          <div className="feature-card-meta"><span>EVENT · {text(row.ledger_event_id || row.id || 'UNKNOWN')}</span><span>SOURCE · {text(row.source_table || 'UNKNOWN')}</span><span>TIME · {text(row.event_at || row.created_at || 'UNKNOWN')}</span></div>
          <button onClick={() => { setSelected(row); setInspectStatus(''); }}>INSPECT EVIDENCE →</button>
        </article>;
      })}</div>}
    <div className="feature-foot"><span>CANONICAL BOUNDARY</span><b>HUB → GOVERNED RUNTIME → SMART LEDGER</b><span>•</span><span>UNKNOWN ≠ SUCCESS · BLOCKED ≠ PASS</span></div>
    {selected && <div className="feature-modal" role="dialog" aria-modal="true">
      <div className="feature-dialog"><div className="eyebrow">CANONICAL RECORD · SMART LEDGER</div>
        <h2>{short(pick(selected, ['event_type', 'title', 'action', 'source_id']) || 'Ledger event', 140)}</h2>
        <div className="feature-detail-grid">{Object.entries(selected).map(([key, value]) => value == null || value === '' ? null : <div key={key}><b>{key.replaceAll('_', ' ').toUpperCase()}</b><span>{typeof value === 'object' ? JSON.stringify(value) : String(value)}</span></div>)}</div>
        <div className="feature-dialog-actions"><button onClick={() => setSelected(null)}>CLOSE</button><button onClick={() => void inspect()} disabled={inspectBusy}>{inspectBusy ? 'INSPECTING…' : inspectStatus || 'INSPECT EVIDENCE →'}</button></div>
      </div>
    </div>}
  </section>;
}
