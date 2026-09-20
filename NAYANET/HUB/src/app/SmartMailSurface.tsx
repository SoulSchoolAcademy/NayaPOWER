import { useEffect, useState } from 'react';
import { useIdentity } from '../identity/session';
type Row = Record<string, unknown>;
type WindowRuntime = {
  snapshot: () => { authenticated?: boolean; user_id?: string };
  listMailThreads: () => Promise<unknown[]>;
  listMailMessages: (threadId?: string) => Promise<unknown[]>;
  listConnections: () => Promise<unknown[]>;
  listAuthorityGrants: (targetId: string) => Promise<unknown[]>;
  sendSmartMail: (input: { receiver_id: string; body: string; subject?: string; kind?: string; idempotency_key?: string; authority_grant_id: string }) => Promise<any>;
  verifySmartMail: (messageId: string) => Promise<any>;
};
const short = (v: unknown) => { const s = String(v || ''); return s.length > 18 ? `${s.slice(0, 8)}…${s.slice(-6)}` : s; };

function runtime(): WindowRuntime {
  const rt = (window as Window & { NayaAssistantRuntime?: WindowRuntime }).NayaAssistantRuntime;
  if (!rt) throw new Error('ASSISTANT_RUNTIME_UNAVAILABLE');
  if (!rt.snapshot()?.authenticated) throw new Error('AUTH_REQUIRED');
  return rt;
}

export function SmartMailSurface() {
  const id = useIdentity();
  const [messages, setMessages] = useState<Row[]>([]);
  const [threads, setThreads] = useState<Row[]>([]);
  const [recipients, setRecipients] = useState<Row[]>([]);
  const [grants, setGrants] = useState<Row[]>([]);
  const [recipient, setRecipient] = useState('');
  const [grant, setGrant] = useState('');
  const [subject, setSubject] = useState('NayaNET communication');
  const [body, setBody] = useState('');
  const [status, setStatus] = useState('');
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);

  const load = async () => {
    if (!id.is_authenticated) {
      setMessages([]); setThreads([]); setRecipients([]); setGrants([]); return;
    }
    setError('');
    const rt = runtime();
    const [threadRows, connectionRows] = await Promise.all([rt.listMailThreads(), rt.listConnections()]);
    setThreads((threadRows || []) as Row[]);
    setRecipients((connectionRows || [])
      .filter((x: Row) => String(x.status || '') === 'active')
      .map((x: Row) => ({ id: String(x.connected_member_id || ''), display_name: `Connected member · ${short(x.connected_member_id)}` })));
    const latest = (threadRows || [])[0] as Row | undefined;
    setMessages(latest?.id ? ((await rt.listMailMessages(String(latest.id))) as Row[]) : []);
  };

  const loadGrants = async (targetId: string) => {
    setGrant('');
    setGrants([]);
    if (!targetId || !id.is_authenticated) return;
    try {
      const rows = await runtime().listAuthorityGrants(targetId);
      setGrants((rows || []).filter((g: Row) => String(g.status || '').toUpperCase() === 'ACTIVE'
        && JSON.stringify(g.actions || '').includes('smart_mail_send')) as Row[]);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'SMART_MAIL_AUTHORITY_LOAD_FAILED');
    }
  };

  useEffect(() => {
    setBusy(true);
    void load().catch(e => setError(e instanceof Error ? e.message : 'SMART_MAIL_LOAD_FAILED')).finally(() => setBusy(false));
  }, [id.is_authenticated, id.user_id]);

  const send = async () => {
    if (!recipient || !grant || !body.trim() || busy) return;
    setBusy(true); setError(''); setStatus('EXECUTING THROUGH NAYAPOWER…');
    try {
      const data = await runtime().sendSmartMail({
        receiver_id: recipient,
        subject: subject.trim() || 'NayaNET communication',
        body: body.trim(),
        kind: 'direct',
        idempotency_key: crypto.randomUUID(),
        authority_grant_id: grant,
      });
      const receipt = data?.execution_receipt_id || data?.receipt?.id || data?.receipt_id || 'NOT_RETURNED';
      setStatus(`✓ SENT · RECEIPT ${short(receipt)}`);
      setBody('');
      await load();
    } catch (e) {
      setError(e instanceof Error ? e.message : 'SMART_MAIL_SEND_FAILED'); setStatus('');
    } finally { setBusy(false); }
  };

  const verify = async (messageId: string) => {
    if (busy) return;
    setBusy(true); setError(''); setStatus('VERIFYING RECEIVER OUTCOME…');
    try {
      const data = await runtime().verifySmartMail(messageId);
      setStatus(`✓ RECEIVER VERIFIED · VALUE ${String(data?.outcome?.verified_value ?? 'recorded')}`);
      await load();
    } catch (e) {
      setError(e instanceof Error ? e.message : 'SMART_MAIL_VERIFY_FAILED'); setStatus('');
    } finally { setBusy(false); }
  };

  if (!id.is_authenticated) {
    return <section className="naya-mail-page"><div className="hero"><div className="eyebrow">NAYANET · COMMUNICATION</div><h1>Smart Mail</h1><p>Private, governed communication through the NayaNET intelligence engine.</p></div><div className="naya-mail-card"><b>AUTHENTICATION REQUIRED</b><p>Sign in through the NayaNET identity surface to use Smart Mail. No browser session is fabricated.</p></div></section>;
  }

  const latest = threads[0];
  return <section className="naya-mail-page">
    <div className="hero"><div className="eyebrow">NAYANET · SMART MAIL</div><h1>Smart Mail</h1><p>Real communication through the same governed engine that protects every consequential NayaPOWER action.</p></div>
    <div className="naya-mail-layout">
      <aside className="naya-mail-panel">
        <div className="naya-mail-label">NEW MESSAGE</div>
        <label>CONNECTED PERSON<select value={recipient} onChange={e => { setRecipient(e.target.value); void loadGrants(e.target.value); }}><option value="">Choose recipient…</option>{recipients.map(r => <option key={String(r.id)} value={String(r.id)}>{String(r.display_name || 'NayaNET Member')}</option>)}</select></label>
        <label>AUTHORITY<select value={grant} onChange={e => setGrant(e.target.value)} disabled={!recipient}><option value="">{recipient ? 'Choose active Smart Mail authority…' : 'Choose a connected person first…'}</option>{grants.map(g => <option key={String(g.grant_id)} value={String(g.grant_id)}>{short(g.grant_id)} · {String(g.expires_at || 'no expiry')}</option>)}</select></label>
        <label>SUBJECT<input value={subject} onChange={e => setSubject(e.target.value)} /></label>
        <label>MESSAGE<textarea value={body} onChange={e => setBody(e.target.value)} rows={8} placeholder="Write what NayaPOWER is authorized to send…" /></label>
        <button className="powerBtn" disabled={!recipient || !grant || !body.trim() || busy} onClick={() => void send()}>{busy ? 'EXECUTING…' : '✦ SEND THROUGH NAYAPOWER'}</button>
        {status && <div className="naya-mail-status" role="status">{status}</div>}
        {error && <div className="naya-mail-error"><b>EXECUTION STOPPED</b><span>{error}</span></div>}
      </aside>
      <main className="naya-mail-panel">
        <div className="naya-mail-label">MAIL · LIVE RECORDS</div>
        <h2>{latest ? String(latest.subject || 'Current thread') : 'Your Smart Mail'}</h2>
        {messages.length ? messages.map(m => {
          const mine = String(m.sender_id) === String(id.user_id);
          const meta = (m.metadata || {}) as Row;
          const receipt = meta.execution_receipt_id;
          const verified = meta.receiver_verified_at;
          return <article className="naya-mail-message" key={String(m.id)}>
            <div><b>{mine ? 'YOU' : 'CONNECTED MEMBER'}</b><time>{new Date(String(m.created_at)).toLocaleString()}</time></div>
            <p>{String(m.body || '')}</p>
            <footer><span>RECEIPT · {receipt ? short(receipt) : 'NOT LINKED'}</span>{verified ? <em>RECEIVER VERIFIED</em> : !mine && <button onClick={() => void verify(String(m.id))} disabled={busy}>VERIFY OUTCOME</button>}</footer>
          </article>;
        }) : <div className="naya-mail-empty"><b>NO MESSAGES YET</b><span>Smart Mail is connected to the governed runtime and canonical Mail records.</span></div>}
      </main>
    </div>
  </section>;
}
