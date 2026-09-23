import { useEffect, useMemo, useState } from 'react';
import { useIdentity } from '../../../identity/session';

type Connection = { id: string; connected_member_id: string; status: string };
type SmartList = { id: string; name: string; members: Array<{ connection_id: string }> };

export function SmartListsSurface() {
  const identity = useIdentity();
  const [lists, setLists] = useState<SmartList[]>([]);
  const [connections, setConnections] = useState<Connection[]>([]);
  const [selected, setSelected] = useState('');
  const [name, setName] = useState('');
  const [busy, setBusy] = useState(true);
  const [actionBusy, setActionBusy] = useState(false);
  const [status, setStatus] = useState('');
  const [query, setQuery] = useState('');

  const load = async () => {
    setBusy(true);
    setStatus('');
    try {
      const runtime = window.NayaAssistantRuntime;
      if (!runtime) throw new Error('ASSISTANT_RUNTIME_UNAVAILABLE');
      if (!runtime.snapshot()?.authenticated) throw new Error('AUTH_REQUIRED');
      const [nextLists, nextConnections] = await Promise.all([runtime.listSmartLists(), runtime.listConnections()]);
      const typedLists = (nextLists || []) as SmartList[];
      setLists(typedLists);
      setConnections((nextConnections || []) as Connection[]);
      setSelected(current => current && typedLists.some(item => item.id === current) ? current : typedLists[0]?.id || '');
    } catch (error) {
      setLists([]);
      setConnections([]);
      setStatus(error instanceof Error ? error.message : 'SMART_LISTS_LOAD_FAILED');
    } finally {
      setBusy(false);
    }
  };

  useEffect(() => {
    if (!identity.is_authenticated) {
      setLists([]);
      setConnections([]);
      setBusy(false);
      return;
    }
    void load();
  }, [identity.is_authenticated]);

  const current = lists.find(list => list.id === selected);
  const visibleConnections = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return connections;
    return connections.filter(connection => connection.connected_member_id.toLowerCase().includes(q));
  }, [connections, query]);

  const create = async () => {
    const trimmed = name.trim();
    if (!trimmed) return;
    setActionBusy(true);
    setStatus('CREATING CANONICAL SMART LIST…');
    try {
      const runtime = window.NayaAssistantRuntime;
      if (!runtime?.createSmartList) throw new Error('SMART_LIST_RUNTIME_UNAVAILABLE');
      const result = await runtime.createSmartList(trimmed) as any;
      setName('');
      setStatus('SMART LIST CREATED · ' + (result?.id || result?.list_id || trimmed));
      await load();
    } catch (error) {
      setStatus('SMART LIST CREATE BLOCKED · ' + (error instanceof Error ? error.message : 'CREATE_FAILED'));
    } finally {
      setActionBusy(false);
    }
  };

  const toggleConnection = async (connection: Connection) => {
    if (!current) return;
    const member = current.members.find(item => item.connection_id === connection.id);
    setActionBusy(true);
    setStatus((member ? 'REMOVING ' : 'ADDING ') + 'CONNECTION THROUGH CANONICAL LIST BOUNDARY…');
    try {
      const runtime = window.NayaAssistantRuntime;
      if (!runtime) throw new Error('ASSISTANT_RUNTIME_UNAVAILABLE');
      if (member) await runtime.removeConnectionFromList(current.id, connection.id);
      else await runtime.addConnectionToList(current.id, connection.id);
      setStatus((member ? 'REMOVED FROM ' : 'ADDED TO ') + current.name + ' · PERSISTED');
      await load();
    } catch (error) {
      setStatus('SMART LIST MEMBERSHIP BLOCKED · ' + (error instanceof Error ? error.message : 'MEMBERSHIP_FAILED'));
    } finally {
      setActionBusy(false);
    }
  };

  if (!identity.is_authenticated) {
    return <section className="feature-surface" data-surface="lists"><div className="feature-hero"><div><div className="eyebrow">NAYANET · ACTION · FOLLOW-THROUGH</div><h1>Smart Lists</h1><p>Organize trusted Connections into reusable action groups.</p></div></div><div className="feature-empty"><b>AUTHENTICATION REQUIRED</b><span>Smart Lists are private owner-scoped structures.</span></div></section>;
  }

  return (
    <section className="feature-surface" data-surface="lists">
      <div className="feature-hero"><div><div className="eyebrow">NAYANET · ACTION · FOLLOW-THROUGH</div><h1>Smart Lists</h1><p>Create a list, choose its Connections, and carry that organization forward.</p></div><div className="feature-state">AUTHENTICATED · {lists.length} LISTS</div></div>
      <div className="feature-toolbar"><label><span>LIST NAME</span><input value={name} onChange={event => setName(event.target.value)} placeholder="Name a new Smart List…" aria-label="New Smart List name" /></label><button onClick={() => void create()} disabled={actionBusy || !name.trim()}>＋ CREATE SMART LIST</button><button onClick={() => void load()} disabled={busy || actionBusy}>↻ REFRESH</button></div>
      {status && <div className="feature-status" role="status">{status}</div>}
      {busy ? <div className="feature-empty"><b>READING CANONICAL LISTS…</b><span>Loading owner-scoped lists and Connections.</span></div> : <div className="lists-layout"><div className="list-index">{lists.map(list => <button key={list.id} className={selected === list.id ? 'selected' : ''} onClick={() => setSelected(list.id)}><b>{list.name}</b><span>{list.members.length} Connections</span></button>)}{!lists.length && <div className="feature-empty"><b>NO SMART LISTS YET</b><span>Create your first list above.</span></div>}</div><div className="list-members">{current ? <><div className="list-members-head"><div><span className="feature-card-kicker">SMART LIST · {current.members.length} CONNECTIONS</span><h2>{current.name}</h2></div><label><span>⌕</span><input value={query} onChange={event => setQuery(event.target.value)} placeholder="Find a Connection…" aria-label="Find a Connection" /></label></div><div className="connection-members">{visibleConnections.map(connection => { const inList = current.members.some(member => member.connection_id === connection.id); return <button key={connection.id} className={inList ? 'in-list' : ''} onClick={() => void toggleConnection(connection)} disabled={actionBusy}><b>{inList ? '✓ ' : '＋ '}{connection.connected_member_id}</b><span>{connection.status} · canonical Connection</span></button>; })}</div>{!visibleConnections.length && <div className="feature-empty"><b>NO MATCHING CONNECTIONS</b><span>Only Connections available to this identity can be organized.</span></div>}</> : <div className="feature-empty"><b>SELECT A SMART LIST</b><span>The membership editor appears after a list exists.</span></div>}</div></div>}
      <div className="feature-foot"><span>CANONICAL BOUNDARY</span><b>SMART LISTS → CONNECTIONS</b><span>•</span><span>CAPABILITY DOES NOT CREATE AUTHORITY</span></div>
    </section>
  );
}
