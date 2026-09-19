import { useEffect, useMemo, useState } from 'react';
import { SUPABASE_URL } from '../config/supabase';
import { supabase, useIdentity } from '../identity/session';

type MailMessage = {
  id: string;
  thread_id: string;
  sender_id: string;
  body: string;
  created_at: string;
  metadata: Record<string, unknown> | null;
};
type MailThread = { id: string; subject: string; kind: string; created_at: string };
type Recipient = { id: string; name: string };
type AuthorityGrant = {
  grant_id: string;
  actions: unknown;
  scope: unknown;
  status: string;
  expires_at: string | null;
};

const mailEndpoint = () => `${SUPABASE_URL}/functions/v1/nayanet-smart-mail`;
const shortId = (value: string) => value.length > 18 ? `${value.slice(0, 8)}…${value.slice(-6)}` : value;

function hasMailAuthority(actions: unknown) {
  if (Array.isArray(actions)) return actions.some(value => String(value) === 'smart_mail_send');
  if (actions && typeof actions === 'object') {
    const record = actions as Record<string, unknown>;
    return record.smart_mail_send === true || record.smart_mail_send === 'AUTHORIZED';
  }
  return false;
}

function displayMetadata(message: MailMessage) {
  const metadata = message.metadata || {};
  const receipt = typeof metadata.execution_receipt_id === 'string' ? metadata.execution_receipt_id : '';
  const verifiedAt = typeof metadata.receiver_verified_at === 'string' ? metadata.receiver_verified_at : '';
  return { receipt, verifiedAt };
}

export function SmartMailSurface() {
  const id = useIdentity();
  const [messages, setMessages] = useState<MailMessage[]>([]);
  const [threads, setThreads] = useState<MailThread[]>([]);
  const [recipients, setRecipients] = useState<Recipient[]>([]);
  const [grants, setGrants] = useState<AuthorityGrant[]>([]);
  const [selectedThread, setSelectedThread] = useState<string>('');
  const [selectedRecipient, setSelectedRecipient] = useState('');
  const [selectedGrant, setSelectedGrant] = useState('');
  const [subject, setSubject] = useState('NayaNET communication');
  const [body, setBody] = useState('');
  const [status, setStatus] = useState('');
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);

  const load = async () => {
    if (!id.is_authenticated) {
      setMessages([]); setThreads([]); setRecipients([]); setGrants([]);
      return;
    }
    setError('');
    const membership = await supabase.from('v7_mail_members').select('thread_id').eq('user_id', id.user_id);
    if (membership.error) throw new Error(membership.error.message);
    const threadIds = [...new Set((membership.data || []).map(row => row.thread_id as string))];
    if (threadIds.length) {
      const [messageResult, threadResult] = await Promise.all([
        supabase.from('v7_mail_messages').select('id,thread_id,sender_id,body,created_at,metadata').in('thread_id', threadIds).order('created_at', { ascending: false }).limit(100),
        supabase.from('v7_mail_threads').select('id,subject,kind,created_at').in('id', threadIds).order('created_at', { ascending: false }),
      ]);
      if (messageResult.error) throw new Error(messageResult.error.message);
      if (threadResult.error) throw new Error(threadResult.error.message);
      setMessages((messageResult.data || []) as MailMessage[]);
      setThreads((threadResult.data || []) as MailThread[]);
      if (!selectedThread && threadResult.data?.[0]?.id) setSelectedThread(threadResult.data[0].id);
    } else {
      setMessages([]); setThreads([]);
    }

    const connections = await supabase.from('nayanet_connections').select('connected_member_id').eq('owner_member_id', id.user_id).eq('status', 'active');
    if (!connections.error) {
      const memberIds = [...new Set((connections.data || []).map(row => row.connected_member_id as string))];
      if (memberIds.length) {
        const members = await supabase.from('members').select('id,display_name').in('id', memberIds);
        if (!members.error) setRecipients((members.data || []).map(row => ({ id: row.id as string, name: String(row.display_name || 'NayaNET Member') })));
      }
    }

    const authority = await supabase.from('nayanet_authority_grants').select('grant_id,actions,scope,status,expires_at').eq('subject_id', id.user_id).eq('status', 'ACTIVE').order('created_at', { ascending: false }).limit(50);
    if (!authority.error) setGrants(((authority.data || []) as AuthorityGrant[]).filter(grant => hasMailAuthority(grant.actions)));
  };

  useEffect(() => {
    let alive = true;
    setBusy(true);
    load().catch(reason => { if (alive) setError(reason instanceof Error ? reason.message : 'SMART_MAIL_LOAD_FAILED'); }).finally(() => { if (alive) setBusy(false); });
    return () => { alive = false; };
  }, [id.is_authenticated, id.user_id]);

  const visibleMessages = useMemo(
    () => selectedThread ? messages.filter(message => message.thread_id === selectedThread) : messages,
    [messages, selectedThread],
  );
  const selectedThreadMeta = threads.find(thread => thread.id === selectedThread);
  const selectedGrantMeta = grants.find(grant => grant.grant_id === selectedGrant);

  const send = async () => {
    if (!id.is_authenticated || !selectedRecipient || !selectedGrant || !body.trim() || busy) return;
    setBusy(true); setError(''); setStatus('AUTHORIZING SMART MAIL…');
    try {
      const { data: sessionData } = await supabase.auth.getSession();
      const token = sessionData.session?.access_token;
      if (!token) throw new Error('AUTHENTICATION_REQUIRED');
      const response = await fetch(mailEndpoint(), {
        method: 'POST',
        headers: { 'content-type': 'application/json', authorization: `Bearer ${token}` },
        body: JSON.stringify({
          operation: 'send',
          recipient_user_id: selectedRecipient,
          subject: subject.trim() || 'NayaNET communication',
          body: body.trim(),
          kind: 'direct',
          idempotency_key: crypto.randomUUID(),
          project_id: 'NayaNET',
          authority_grant_id: selectedGrant,
        }),
      });
      const result = await response.json().catch(() => ({}));
      if (!response.ok || result?.ok === false) throw new Error(String(result?.error || `SMART_MAIL_HTTP_${response.status}`));
      setStatus(`✓ SENT · RECEIPT ${shortId(String(result.execution_receipt_id || 'not-returned'))}`);
      setBody('');
      await load();
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : 'SMART_MAIL_SEND_FAILED');
      setStatus('');
    } finally { setBusy(false); }
  };

  const verify = async (messageId: string) => {
    if (!id.is_authenticated || busy) return;
    setBusy(true); setError(''); setStatus('VERIFYING RECEIVER OUTCOME…');
    try {
      const { data: sessionData } = await supabase.auth.getSession();
      const token = sessionData.session?.access_token;
      if (!token) throw new Error('AUTHENTICATION_REQUIRED');
      const response = await fetch(mailEndpoint(), {
        method: 'POST',
        headers: { 'content-type': 'application/json', authorization: `Bearer ${token}` },
        body: JSON.stringify({ operation: 'verify', message_id: messageId }),
      });
      const result = await response.json().catch(() => ({}));
      if (!response.ok || result?.ok === false) throw new Error(String(result?.error || `SMART_MAIL_VERIFY_HTTP_${response.status}`));
      setStatus(`✓ RECEIVER VERIFIED · VALUE ${String(result.outcome?.verified_value ?? 'recorded')}`);
      await load();
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : 'SMART_MAIL_VERIFY_FAILED');
      setStatus('');
    } finally { setBusy(false); }
  };

  if (!id.is_authenticated) {
    return <section className="mail-surface"><div className="feature-hero"><div><div className="eyebrow">NAYANET · SMART MAIL</div><h1>Smart Mail</h1><p>Authorized intelligence moving between people through the canonical Mail path.</p></div><div className="feature-state">AUTHENTICATION REQUIRED</div></div><div className="mail-empty"><b>SIGN IN TO OPEN SMART MAIL</b><span>Smart Mail is private and uses the authenticated NayaNET identity, authority grant, live execution boundary, receipt, and receiver verification path.</span></div></section>;
  }

  return <section className="mail-surface">
    <div className="feature-hero">
      <div><div className="eyebrow">NAYANET · CONSEQUENT SMART MAIL</div><h1>Smart Mail</h1><p>Real communication through the governed execution engine — not a mock inbox.</p></div>
      <div className="feature-state">{busy ? 'WORKING…' : 'AUTHENTICATED'} · {messages.length} MESSAGES</div>
    </div>

    <div className="mail-grid">
      <aside className="mail-sidebar">
        <div className="mail-section-label">THREADS</div>
        {threads.length ? threads.map(thread => <button key={thread.id} className={selectedThread === thread.id ? 'mail-thread active' : 'mail-thread'} onClick={() => setSelectedThread(thread.id)}><b>{thread.subject || 'Untitled thread'}</b><span>{thread.kind} · {new Date(thread.created_at).toLocaleString()}</span></button>) : <div className="mail-muted">No threads yet.</div>}
        <div className="mail-proof-card"><b>ENGINE PATH</b><span>AUTH → AUTHORITY → SMART MAIL → RECEIPT → ACTIVITY</span></div>
      </aside>

      <main className="mail-compose">
        <div className="mail-compose-head"><div><div className="mail-section-label">NEW CONSEQUENT MESSAGE</div><h2>Send through NayaPOWER</h2></div><span className="mail-lock">PRIVATE BY DEFAULT</span></div>
        <div className="mail-form">
          <label>CONNECTED RECIPIENT<select value={selectedRecipient} onChange={event => setSelectedRecipient(event.target.value)}><option value="">Choose a connected person…</option>{recipients.map(recipient => <option key={recipient.id} value={recipient.id}>{recipient.name} · {shortId(recipient.id)}</option>)}</select></label>
          <label>AUTHORIZED GRANT<select value={selectedGrant} onChange={event => setSelectedGrant(event.target.value)}><option value="">Choose an active Smart Mail authority…</option>{grants.map(grant => <option key={grant.grant_id} value={grant.grant_id}>{shortId(grant.grant_id)} · {new Date(grant.expires_at || Date.now()).toLocaleDateString()}</option>)}</select></label>
          {selectedGrantMeta && <div className="mail-authority"><b>AUTHORITY VERIFIED AT UI BOUNDARY</b><span>{shortId(selectedGrantMeta.grant_id)} · status {selectedGrantMeta.status}</span></div>}
          <label>SUBJECT<input value={subject} onChange={event => setSubject(event.target.value)} /></label>
          <label>MESSAGE<textarea value={body} onChange={event => setBody(event.target.value)} placeholder="Write the message NayaPOWER is authorized to send…" rows={8} /></label>
          <div className="mail-actions"><button className="powerBtn" disabled={!selectedRecipient || !selectedGrant || !body.trim() || busy} onClick={() => void send()}>{busy ? 'EXECUTING…' : '✦ SEND THROUGH NAYAPOWER'}</button>{status && <span className="mail-status">{status}</span>}</div>
          {error && <div className="mail-error"><b>EXECUTION STOPPED</b><span>{error}</span></div>}
        </div>
      </main>

      <aside className="mail-reading">
        <div className="mail-section-label">CURRENT THREAD</div>
        <h2>{selectedThreadMeta?.subject || 'Select a thread'}</h2>
        {visibleMessages.length ? visibleMessages.map(message => {
          const meta = displayMetadata(message);
          const mine = message.sender_id === id.user_id;
          return <article key={message.id} className={mine ? 'mail-message mine' : 'mail-message'}>
            <div className="mail-message-head"><span>{mine ? 'YOU' : 'CONNECTED MEMBER'}</span><time>{new Date(message.created_at).toLocaleString()}</time></div>
            <p>{message.body}</p>
            <div className="mail-receipt"><span>RECEIPT</span><b>{meta.receipt ? shortId(meta.receipt) : 'NOT LINKED'}</b>{meta.verifiedAt ? <em>RECEIVER VERIFIED</em> : !mine ? <button onClick={() => void verify(message.id)} disabled={busy}>VERIFY OUTCOME</button> : <em>PENDING RECEIVER VERIFICATION</em>}</div>
          </article>;
        }) : <div className="mail-empty"><b>NO MESSAGES IN THIS THREAD</b><span>Send a governed message or select another thread.</span></div>}
      </aside>
    </div>
  </section>;
}
