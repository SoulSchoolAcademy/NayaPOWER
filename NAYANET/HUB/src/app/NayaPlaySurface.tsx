import { useEffect, useMemo, useState } from 'react';
import { useIdentity } from '../identity/session';

type EventRow = Record<string, any>;

function playbackText(event: EventRow) {
  return [
    event.title || event.source?.label,
    event.human_input?.raw,
    event.naya_interpretation?.interpretation,
    event.lesson?.text,
    event.meaning?.text,
    event.action?.text,
    event.whats_in_it_for_you,
  ].map(value => String(value || '').trim()).filter(Boolean).join('. ');
}

export function NayaPlaySurface() {
  const identity = useIdentity();
  const [events, setEvents] = useState<EventRow[]>([]);
  const [selected, setSelected] = useState('');
  const [status, setStatus] = useState('');
  const [busy, setBusy] = useState(false);
  const [speaking, setSpeaking] = useState(false);
  const [lastReceipt, setLastReceipt] = useState('');

  const selectedEvent = useMemo(() => events.find(event => event.event_id === selected) || null, [events, selected]);

  useEffect(() => {
    let live = true;
    (async () => {
      if (!identity.is_authenticated) return;
      try {
        const runtime = window.NayaAssistantRuntime;
        if (!runtime?.retrieve) throw new Error('ASSISTANT_RUNTIME_UNAVAILABLE');
        const rows = await runtime.retrieve();
        const usable = (Array.isArray(rows) ? rows : []).filter((event: EventRow) => !String(event.source || '').includes('nayanet-hub.naya-play'));
        if (live) {
          setEvents(usable);
          setSelected(usable[0]?.event_id || '');
        }
      } catch (error) {
        if (live) setStatus(error instanceof Error ? error.message : 'NAYA_PLAY_LOAD_FAILED');
      }
    })();
    return () => { live = false; };
  }, [identity.is_authenticated]);

  const stop = () => {
    window.speechSynthesis?.cancel();
    setSpeaking(false);
    setBusy(false);
  };

  const play = async () => {
    if (!selectedEvent) return;
    const runtime = window.NayaAssistantRuntime;
    if (!runtime?.record || !runtime?.retrieve) throw new Error('ASSISTANT_RUNTIME_UNAVAILABLE');
    if (!window.speechSynthesis) throw new Error('SPEECH_SYNTHESIS_UNAVAILABLE');
    const text = playbackText(selectedEvent);
    if (!text) throw new Error('PLAYBACK_SOURCE_EMPTY');

    setBusy(true);
    setSpeaking(true);
    setStatus('PLAYING CANONICAL INTELLIGENCE…');
    setLastReceipt('');

    try {
      await new Promise<void>((resolve, reject) => {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 0.96;
        utterance.pitch = 1;
        utterance.onend = () => resolve();
        utterance.onerror = event => reject(new Error(`SPEECH_SYNTHESIS_${event.error || 'FAILED'}`));
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(utterance);
      });

      const result: any = await runtime.record({
        title: 'Naya Play session',
        content: `Played canonical intelligence event ${selectedEvent.event_id}.`,
        source: 'nayanet-hub.naya-play',
        project: 'NayaNET',
        status: 'active',
        actor: 'human',
        tags: ['intelligent-hub', 'naya-play', 'human-action'],
        metadata: {
          action: 'play_naya',
          source_event_id: selectedEvent.event_id,
          playback_transport: 'speechSynthesis',
          playback_source: 'canonical_event_content',
          persistence_boundary: 'authenticated-canonical-runtime',
        },
      });
      const eventId = String(result?.event_id || result?.event?.event_id || '');
      const receiptId = String(result?.receipt?.id || result?.receipt?.receipt_id || result?.receipt_id || '');
      if (!eventId || !receiptId) throw new Error('NAYA_PLAY_RECEIPT_INCOMPLETE');
      const verified = await runtime.retrieve(eventId);
      const found = Array.isArray(verified) && verified.some((event: EventRow) => event.event_id === eventId);
      if (!found) throw new Error('NAYA_PLAY_RETRIEVAL_FAILED');
      setLastReceipt(receiptId);
      setStatus(`PLAY VERIFIED · EVENT ${eventId} · RECEIPT ${receiptId}`);
    } catch (error) {
      setStatus(error instanceof Error ? error.message : 'NAYA_PLAY_FAILED');
    } finally {
      setSpeaking(false);
      setBusy(false);
    }
  };

  if (!identity.is_authenticated) {
    return <section className="feature-surface" data-surface="naya-play">
      <div className="feature-hero"><div><div className="eyebrow">NAYANET · PLAY NAYA · HUMAN EXPERIENCE</div><h1>Naya Play</h1><p>Listen to the intelligence that already exists, without inventing a second source.</p></div><div className="feature-state">AUTHENTICATION REQUIRED</div></div>
      <div className="feature-empty"><b>AUTHENTICATION REQUIRED</b><span>Naya Play reads private intelligence only inside the authenticated Hub boundary.</span></div>
    </section>;
  }

  return <section className="feature-surface" data-surface="naya-play">
    <div className="feature-hero"><div><div className="eyebrow">NAYANET · PLAY NAYA · HUMAN EXPERIENCE</div><h1>Naya Play</h1><p>Hear the actual canonical intelligence event through the existing governed Hub runtime.</p></div><div className="feature-state">AUTHENTICATED · {events.length} SOURCES</div></div>
    <div className="feature-toolbar">
      <label><span>⌕</span><select value={selected} onChange={event => setSelected(event.target.value)} aria-label="Naya Play source">{events.map(event => <option key={event.event_id} value={event.event_id}>{event.title || event.source?.label || event.event_id}</option>)}</select></label>
      <button onClick={() => void play()} disabled={busy || !selected}>{speaking ? 'Ⅱ PLAYING…' : busy ? 'VERIFYING…' : '▶ PLAY NAYA'}</button>
      {speaking && <button onClick={stop}>■ STOP</button>}
    </div>
    {status && <div className="feature-status" role="status">{status}</div>}
    {lastReceipt && <div className="feature-status">CANONICAL RECEIPT · {lastReceipt}</div>}
    {!selectedEvent ? <div className="feature-empty"><b>NAYA PLAY IS READY</b><span>No canonical intelligence is available for playback yet.</span></div> : <div className="feature-cards">
      <article className="feature-card">
        <div className="feature-card-head"><div><span className="feature-card-kicker">PLAYBACK SOURCE</span><h2>{String(selectedEvent.title || selectedEvent.source?.label || selectedEvent.event_id)}</h2></div><span className="feature-card-status">CANONICAL</span></div>
        <p>{String(selectedEvent.human_input?.raw || selectedEvent.naya_interpretation?.interpretation || 'Canonical event content is available.')}</p>
        <div className="feature-card-meta"><span>EVENT · {selectedEvent.event_id}</span><span>SOURCE · {String(selectedEvent.source?.label || selectedEvent.source || 'canonical')}</span></div>
      </article>
    </div>}
    <div className="feature-foot"><span>TRUTH</span><b>PLAYBACK USES EXISTING CANONICAL EVENT CONTENT</b><span>•</span><span>NO SECOND MEMORY · NO SYNTHETIC INTELLIGENCE</span></div>
  </section>;
}