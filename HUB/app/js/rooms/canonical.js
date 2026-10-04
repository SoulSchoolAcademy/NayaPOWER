/* NAYA CANONICAL SUBSTRATE (client projection)
   One intelligence object → many projections. Feed, Today, Library, Lists,
   Spaces, and Reports render THE SAME objects — never copies. Every object
   carries identity, provenance, truth state, consent, supersession, and the
   four node questions: WHO ALLOWS? WHY BELIEVE? WHAT CONNECTS? WHAT NEXT?

   TRUTH CONTRACT: the objects below are DESIGN FIXTURES. They demonstrate the
   canonical shape the governed runtime will project. None is live, verified,
   or canonical data. */

(function () {
  const { el, Pill, toast } = window.NayaUI;

  const KIND_META = {
    decision:   { label: 'Decision',   accent: 'var(--magenta)', icon: 'spark' },
    learning:   { label: 'Learning',   accent: 'var(--blue)',    icon: 'nodes' },
    discovery:  { label: 'Discovery',  accent: 'var(--green)',   icon: 'feed' },
    activity:   { label: 'Activity',   accent: 'var(--orange)',  icon: 'report' },
    smart_note: { label: 'Smart Note', accent: 'var(--purple)',  icon: 'note' },
    report:     { label: 'Report',     accent: 'var(--indigo)',  icon: 'report' },
  };

  /* ——— The canonical objects. One set. Every room projects from here. ——— */
  const OBJECTS = [
    {
      id: 'IB-2026-10-01-004', kind: 'decision', stream: 'personal',
      title: 'The Hub is output, not input',
      body: 'No intelligence capture, generation, or command surface belongs in the Hub. Retrieval, navigation, filters, categorization, and read-back are the valid consumption controls. Room contracts listing capture actions must be amended.',
      truth_state: 'FIXTURE', consent: 'personal', superseded_by: null,
      provenance: { source: 'Design fixture — mirrors session decision', captured: '2026-10-01', by: 'Naya 2 (builder)' },
      why_selected: 'Locks the input/output architecture. Every room contract that lists a capture action must reconcile against it.',
      next: 'Amend the room contracts that still list capture actions (lane #1290).',
      connects: ['IB-2026-10-01-006', 'IB-2026-10-01-003'],
      modes: ['brief', 'deep', 'review'], ts: '2026-10-01T09:40:00-07:00',
    },
    {
      id: 'IB-2026-10-01-006', kind: 'decision', stream: 'personal',
      title: 'Eleven rooms. No more, no fewer.',
      body: 'The primary rail holds exactly eleven rooms. Smart Notes was removed as a Hub room (capture is input); System diagnostics moved under Settings → System Health. The rail is a contract, not a wishlist.',
      truth_state: 'FIXTURE', consent: 'personal', superseded_by: null,
      provenance: { source: 'Design fixture — mirrors session decision', captured: '2026-10-01', by: 'Naya 2 (builder)' },
      why_selected: 'Resolves the 13-vs-11 conflict between the app foundation and the canonical rail.',
      next: 'Verify the rail matches the contract byte-for-byte in the per-room QA matrix.',
      connects: ['IB-2026-10-01-004'],
      modes: ['brief', 'deep', 'review'], ts: '2026-10-01T10:15:00-07:00',
    },
    {
      id: 'IB-2026-10-01-011', kind: 'learning', stream: 'personal',
      title: 'Off-canvas drawers inflate document scroll width',
      body: 'A fixed drawer translated off-canvas still extends the document\u2019s scrollable overflow region in Chromium (476px vs 390px viewport). Fix: overflow-x: clip containment on the shell — the drawer is intentionally off-screen, so its overflow must not be scrollable.',
      truth_state: 'FIXTURE', consent: 'personal', superseded_by: null,
      provenance: { source: 'Design fixture — mirrors rendered QA finding', captured: '2026-10-01', by: 'Naya 2 (builder)' },
      why_selected: 'Found by rendered QA, not by reading code. The exact defect class reported against the Hub — now with a proven fix and a 19/19 pass.',
      next: 'Extend the containment check to every room\u2019s QA matrix.',
      connects: ['IB-2026-10-01-012'],
      modes: ['deep', 'review'], ts: '2026-10-01T14:20:00-07:00',
    },
    {
      id: 'IB-2026-10-01-009', kind: 'learning', stream: 'personal',
      title: 'Producer self-scores never close a gate',
      body: 'The old System room carried self-authored scores (Visual 9.0, Honesty 9.0) with no evidence behind them. Replaced with the attributed independent audit: composite 5.7/10. Scores move when the evidence moves — up or down.',
      truth_state: 'FIXTURE', consent: 'personal', superseded_by: null,
      provenance: { source: 'Design fixture — mirrors session decision', captured: '2026-10-01', by: 'Naya 2 (builder)' },
      why_selected: 'A standing law for the whole build: flattering numbers are a defect. The honest scorecard lets the score earn its way up.',
      next: 'Independent re-score of the Today room.',
      connects: ['IB-2026-10-01-012'],
      modes: ['deep', 'review'], ts: '2026-10-01T13:05:00-07:00',
    },
    {
      id: 'IB-2026-10-01-002', kind: 'discovery', stream: 'collective',
      title: 'Three pipelines feed the Hub — nothing else',
      body: 'Smart Notes (captured intelligence), Activity (current state and change), Reports (periodic synthesis). Every pixel in the Hub must trace to one of these three governed streams.',
      truth_state: 'FIXTURE', consent: 'collective', superseded_by: null,
      provenance: { source: 'Design fixture — consented, anonymized', captured: '2026-10-01', by: 'Naya 2 (builder)' },
      why_selected: 'Gives the Feed its architecture: three source streams, smart views over them, no duplicate stores.',
      next: 'Map each Feed smart view to its source stream; reject any view that needs a fourth.',
      connects: ['IB-2026-10-01-003', 'IB-2026-10-01-004'],
      modes: ['brief', 'deep', 'review'], ts: '2026-10-01T09:05:00-07:00',
    },
    {
      id: 'IB-2026-10-01-003', kind: 'discovery', stream: 'personal',
      title: '\u201CAsk Naya\u201D means ask the brain',
      body: 'The Hub\u2019s prominent search is retrieval over the NayaPOWER knowledge base — not a chatbot, not a command surface. It answers from canonical intelligence with provenance. Voice read-back is output, so it belongs.',
      truth_state: 'FIXTURE', consent: 'personal', superseded_by: null,
      provenance: { source: 'Design fixture — mirrors session ruling', captured: '2026-10-01', by: 'Naya 2 (builder)' },
      why_selected: 'Ends the ambiguity: the search box is a lens on the brain, not another AI to talk to. Retrieval only.',
      next: 'Bind search to governed retrieval with provenance when the runtime connects.',
      connects: ['IB-2026-10-01-002'],
      modes: ['brief', 'deep'], ts: '2026-10-01T09:25:00-07:00',
    },
    {
      id: 'IB-2026-10-01-012', kind: 'activity', stream: 'activity',
      title: '#1278 foundation reconciled to main',
      body: 'Eleven rooms, drawer law proven 19/19, rail accents matched to the design contract, search held as the retrieval surface. The foundation the rooms compound onto.',
      truth_state: 'FIXTURE', consent: 'personal', superseded_by: null,
      provenance: { source: 'Design fixture — mirrors build event', captured: '2026-10-01', by: 'Naya 2 (builder)' },
      why_selected: 'The day\u2019s load-bearing build event. Everything after this compounds on a reconciled foundation.',
      next: 'Compound this architecture into Feed, then Library — same objects, new lenses.',
      connects: ['IB-2026-10-01-011', 'IB-2026-10-01-009'],
      modes: ['brief', 'review'], ts: '2026-10-01T15:45:00-07:00',
    },
  ];

  const byId = id => OBJECTS.find(o => o.id === id);

  const CSS = `
  .ev-backdrop { position:fixed; inset:0; z-index:80; background:rgba(3,3,6,.7); backdrop-filter:blur(3px);
    opacity:0; pointer-events:none; transition:opacity .25s ease; }
  .ev-backdrop.open { opacity:1; pointer-events:auto; }
  .ev-sheet { position:fixed; top:0; right:0; bottom:0; width:min(440px,94vw); z-index:81;
    background:linear-gradient(160deg,#151021,#0b0812); border-left:1px solid var(--line);
    box-shadow:-30px 0 80px #000; transform:translateX(103%); transition:transform .3s cubic-bezier(.2,.8,.25,1);
    overflow-y:auto; padding:28px 26px; }
  .ev-sheet.open { transform:none; }
  .ev-q { margin:18px 0 6px; font-size:11px; letter-spacing:.2em; font-weight:800; color:var(--magenta); }
  .ev-field { margin:10px 0; }
  .ev-field .k { font-size:10.5px; letter-spacing:.16em; color:var(--muted); font-weight:700; }
  .ev-field .v { font-size:14px; margin-top:4px; color:var(--ink); line-height:1.55; }
  .ev-field .v.mono { font-family:ui-monospace,monospace; font-size:12.5px; color:#cfc8de; word-break:break-all; }
  .ev-link { color:var(--magenta); cursor:pointer; font-weight:700; }
  .ev-link:hover { text-decoration:underline; }
  .fixture-banner { display:flex; gap:10px; align-items:flex-start; padding:12px 16px; border-radius:14px;
    background:#f5c51814; border:1px solid #f5c51855; font-size:12.5px; color:#e8dfc9; max-width:720px; }
  .fixture-banner b { color:#f5c518; letter-spacing:.08em; }
  @media (prefers-reduced-motion: reduce) { .ev-backdrop, .ev-sheet { transition:none; } }`;
  if (!document.getElementById('naya-canonical-css')) {
    const st = el('style', '', CSS); st.id = 'naya-canonical-css'; document.head.appendChild(st);
  }

  /* ——— Evidence: the four node questions, answered from the object ——— */
  let evBackdrop, evSheet;
  function ensureEvidence() {
    if (evSheet) return;
    evBackdrop = el('div', 'ev-backdrop');
    evSheet = el('aside', 'ev-sheet');
    evSheet.setAttribute('role', 'dialog');
    evSheet.setAttribute('aria-label', 'Evidence: canonical intelligence object');
    evBackdrop.addEventListener('click', closeEvidence);
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape' && evSheet.classList.contains('open')) closeEvidence();
    });
    document.body.append(evBackdrop, evSheet);
  }
  function openEvidence(item) {
    ensureEvidence();
    const km = KIND_META[item.kind];
    const linked = (item.connects || []).map(byId).filter(Boolean);
    evSheet.innerHTML = `
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">
        <span style="font-size:11px;letter-spacing:.2em;font-weight:800;color:${km.accent}">${km.label.toUpperCase()} · EVIDENCE</span>
        <button class="btn btn-ghost" id="ev-close" aria-label="Close evidence"><span>Close</span></button>
      </div>
      <h2 style="font-size:22px;line-height:1.25;margin:8px 0 4px">${item.title}</h2>
      <div style="margin:10px 0">${Pill('soon')}<span style="font-size:11px;color:var(--muted);margin-left:8px">truth state: FIXTURE — design fixture, not canonical data</span></div>
      <p style="color:#cfc8de;font-size:14.5px;line-height:1.65">${item.body}</p>
      <div class="ev-q">WHO ALLOWS?</div>
      <div class="ev-field"><div class="k">CONSENT SCOPE</div><div class="v">${item.consent} · stream: ${item.stream}</div></div>
      <div class="ev-q">WHY BELIEVE?</div>
      <div class="ev-field"><div class="k">PROVENANCE</div><div class="v mono">${item.provenance.source}<br>captured ${item.provenance.captured} · ${item.provenance.by}</div></div>
      <div class="ev-field"><div class="k">CANONICAL ID</div><div class="v mono">${item.id}</div></div>
      <div class="ev-field"><div class="k">SUPERSESSION</div><div class="v mono">${item.superseded_by ? 'superseded by ' + item.superseded_by : 'current — supersedes nothing, superseded by nothing'}</div></div>
      <div class="ev-q">WHAT CONNECTS?</div>
      <div class="ev-field"><div class="v">${linked.length
        ? linked.map(l => `<div style="margin:6px 0"><span class="ev-link" data-ev="${l.id}">${l.title}</span> <span style="color:var(--muted);font-size:12px">· ${KIND_META[l.kind].label}</span></div>`).join('')
        : '<span style="color:var(--muted)">No recorded connections yet.</span>'}</div></div>
      <div class="ev-q">WHAT NEXT?</div>
      <div class="ev-field"><div class="v">${item.next || '<span style="color:var(--muted)">No responsible next action recorded.</span>'}</div></div>
      ${item.why_selected ? `<div class="ev-q">WHY SELECTED</div><div class="ev-field"><div class="v">${item.why_selected}</div></div>` : ''}
      <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:20px">
        <button class="btn" id="ev-feed"><span>Open in Feed</span></button>
        <button class="btn btn-ghost" id="ev-fav"><span>Save favorite</span></button>
      </div>
      <p style="font-size:11px;color:var(--muted);margin-top:14px">When the governed runtime connects, this sheet shows the live canonical object — same identity, same fields, verified provenance.</p>`;
    evSheet.querySelector('#ev-close').addEventListener('click', closeEvidence);
    evSheet.querySelector('#ev-feed').addEventListener('click', () => { closeEvidence(); window.NayaRouter.navigate('/hub/feed'); });
    evSheet.querySelector('#ev-fav').addEventListener('click', () => saveFavorite(item));
    evSheet.querySelectorAll('.ev-link').forEach(a =>
      a.addEventListener('click', () => openEvidence(byId(a.dataset.ev))));
    evBackdrop.classList.add('open'); evSheet.classList.add('open');
    document.body.style.overflow = 'hidden';
    evSheet.querySelector('#ev-close').focus();
  }
  function closeEvidence() {
    if (!evSheet) return;
    evBackdrop.classList.remove('open'); evSheet.classList.remove('open');
    document.body.style.overflow = '';
  }

  /* ——— Local-only consumption actions (honest: this device only) ——— */
  function localSet(key) {
    try { return new Set(JSON.parse(localStorage.getItem(key) || '[]')); }
    catch { return new Set(); }
  }
  function saveFavorite(item) {
    const s = localSet('naya.favorites'); s.add(item.id);
    localStorage.setItem('naya.favorites', JSON.stringify([...s]));
    toast('Saved to favorites — on this device only, until the runtime syncs.', 'var(--magenta)');
  }
  function addToList(item, list = 'inbox') {
    const s = localSet('naya.list.' + list); s.add(item.id);
    localStorage.setItem('naya.list.' + list, JSON.stringify([...s]));
    toast(`Added to your ${list} list — on this device only, until the runtime syncs.`, 'var(--purple)');
  }
  function fixtureBanner(roomName) {
    return `<div class="fixture-banner" role="note"><span aria-hidden="true">◈</span>
      <span><b>DESIGN FIXTURES.</b> This room shows what <i>${roomName}</i> will look like when the governed runtime connects. Every card below is a labeled fixture — none of it is live, verified, or canonical data.</span></div>`;
  }

  window.NayaCanonical = {
    KIND_META, OBJECTS, byId,
    openEvidence, closeEvidence,
    saveFavorite, addToList, fixtureBanner,
  };
})();
