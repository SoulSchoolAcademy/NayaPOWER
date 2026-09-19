import { useEffect, useMemo, useState } from 'react';
import { groupActivity, loadFeatureActivity, type FeatureActivity } from './activityProjection';

const dateKey = (record: FeatureActivity) => new Date(record.effective_at).toISOString().slice(0, 10);

export function ActivityBoard() {
  const [records, setRecords] = useState<FeatureActivity[]>([]);
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(true);
  const [year, setYear] = useState('');
  const [month, setMonth] = useState('');
  const [day, setDay] = useState('');
  const [session, setSession] = useState('');

  useEffect(() => {
    let live = true;
    setBusy(true);
    setError('');
    loadFeatureActivity().then(value => {
      if (!live) return;
      setRecords(value);
      const first = value[0];
      if (first) {
        const date = new Date(first.effective_at);
        setYear(String(date.getFullYear()));
        setMonth(String(date.getMonth() + 1).padStart(2, '0'));
        setDay(date.toISOString().slice(0, 10));
      }
    }).catch(reason => { if (live) setError(reason instanceof Error ? reason.message : 'ACTIVITY_LOAD_FAILED'); })
      .finally(() => { if (live) setBusy(false); });
    return () => { live = false; };
  }, []);

  const grouped = useMemo(() => groupActivity(records), [records]);
  const years = [...grouped.keys()].sort().reverse();
  const months = year ? [...(grouped.get(year)?.keys() || [])].sort().reverse() : [];
  const days = year && month ? [...(grouped.get(year)?.get(month)?.keys() || [])].sort().reverse() : [];
  const selectedSessions = year && month && day ? grouped.get(year)?.get(month)?.get(day) : undefined;
  const sessions = selectedSessions ? [...selectedSessions.keys()] : [];
  const visible = selectedSessions
    ? [...selectedSessions.entries()].flatMap(([sessionId, items]) => session && sessionId !== session ? [] : items)
    : records;

  const selectYear = (value: string) => { setYear(value); setMonth(''); setDay(''); setSession(''); };
  const selectMonth = (value: string) => { setMonth(value); setDay(''); setSession(''); };
  const selectDay = (value: string) => { setDay(value); setSession(''); };

  return <div className="hub-command">
    <header className="hub-command-head">
      <div className="hub-command-title">
        <div className="eyebrow">NAYANET · ENGINEERING ACTIVITY</div>
        <h1>Engineering Activity</h1>
        <p>Canonical team activity projected as YEAR → MONTH → DAY → SESSION. Activity is a review surface, not a second event store.</p>
      </div>
      <div className="hub-live">{records.length} ACTIVITY EVENTS</div>
    </header>

    <div className="hub-lensbar" role="navigation" aria-label="Engineering activity hierarchy">
      <button className="hub-lens" onClick={() => { setYear(''); setMonth(''); setDay(''); setSession(''); }}><b>ALL</b><span>{records.length} events</span></button>
      {years.map(value => <button key={value} className={year === value ? 'hub-lens active' : 'hub-lens'} onClick={() => selectYear(value)}><b>{value}</b><span>YEAR</span></button>)}
    </div>

    {year && <div className="hub-lensbar" role="navigation" aria-label="Activity months">
      {months.map(value => <button key={value} className={month === value ? 'hub-lens active' : 'hub-lens'} onClick={() => selectMonth(value)}><b>{value}</b><span>MONTH</span></button>)}
    </div>}

    {year && month && <div className="hub-lensbar" role="navigation" aria-label="Activity days">
      {days.map(value => {
        const key = year + '-' + month + '-' + value;
        return <button key={key} className={day === key ? 'hub-lens active' : 'hub-lens'} onClick={() => selectDay(key)}><b>{value}</b><span>DAY</span></button>;
      })}
    </div>}

    {day && selectedSessions && <div className="hub-lensbar" role="navigation" aria-label="Activity sessions">
      {sessions.map(value => <button key={value} className={session === value ? 'hub-lens active' : 'hub-lens'} onClick={() => setSession(value)}><b>{value}</b><span>SESSION</span></button>)}
    </div>}

    <section className="hub-stream">
      <div className="hub-stream-head"><h2>{day || year || 'All Activity'}</h2><span>{visible.length} entries</span></div>
      {error ? <div className="hub-empty"><b>ACTIVITY FEED UNAVAILABLE</b><span>{error}</span></div> :
       busy ? <div className="hub-empty"><b>RETRIEVING CANONICAL ACTIVITY…</b></div> :
       visible.length ? <div className="hub-results">{visible.map(record =>
        <article className="intel-card block" key={record.event_id}>
          <div className="intel-card-top"><span className="intel-source">{record.subject || 'NAYANET ENGINEERING'}</span><span className="intel-state">{dateKey(record)}</span></div>
          <h3>{record.summary}</h3>
          <p className="intel-nutshell">{record.next_action || 'No successor action recorded.'}</p>
          <div className="intel-meta">
            <span className="intel-chip">SESSION · {record.session_id || '—'}</span>
            <span className="intel-chip">RUN · {record.run_id || '—'}</span>
            <span className="intel-chip">EVENT · {record.event_id}</span>
          </div>
          <div className="intel-footer">
            <div className="intel-mini"><span>EVIDENCE</span><p>{record.evidence?.length ? JSON.stringify(record.evidence) : 'No evidence references recorded.'}</p></div>
            <div className="intel-mini"><span>SUCCESSOR</span><p>{record.successor || '—'}</p></div>
            <div className="intel-mini"><span>RECEIPT</span><p>{record.execution_receipt_id || '—'}</p></div>
          </div>
        </article>
       )}</div> :
       <div className="hub-empty"><b>NO ACTIVITY FOR THIS SELECTION</b><span>The system will not fabricate activity when the canonical activity source is empty.</span></div>}
    </section>
  </div>;
}
