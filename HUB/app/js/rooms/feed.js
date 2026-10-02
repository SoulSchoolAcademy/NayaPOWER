/* SMART FEED — the canonical live intelligence stream.
   The raw/current layer that Today later synthesizes. Three source streams
   (Personal · Collective · Activity), smart views over them, no duplicate stores.
   Projects the SAME canonical objects as every other room — one object, many lenses.

   Input/output law: no capture surface. CAPTURE_SMART_NOTE from the old spec
   is intentionally not implemented. */

(function () {
  const { el, Board, toast } = window.NayaUI;
  const C = window.NayaCanonical;
  const { KIND_META, OBJECTS } = C;
  const ACC = 'var(--accent-feed)';

  const STREAMS = [
    ['personal', 'Personal', 'Your Smart Notes, reports, learning, decisions, discoveries.'],
    ['collective', 'Collective', 'Consented, anonymized intelligence. The intelligence is shared — never the contributor.'],
    ['activity', 'Activity', 'What is happening now: current state, change, process.'],
  ];
  const VIEWS = [
    ['all', 'All'], ['highlights', 'Highlights'], ['decisions', 'Decisions'],
    ['learning', 'Learning'], ['discoveries', 'Discoveries'],
    ['smart_notes', 'Smart Notes'], ['activity', 'Activity'], ['reports', 'Reports'],
  ];

  const CSS = `
  .feed-hero { position:relative; border-radius:22px; padding:36px 36px 30px; overflow:hidden;
    background:linear-gradient(135deg,#08140f 0%,#0a0f0c 60%,#08060d 100%);
    border:1px solid #55e39a2e; box-shadow:0 30px 80px -20px #55e39a33, inset 0 1px 0 #ffffff14; }
  .feed-hero::before { content:""; position:absolute; inset:-40%; pointer-events:none;
    background:radial-gradient(ellipse 55% 45% at 85% 0%, #55e39a1f, transparent 70%); }
  .feed-title { position:relative; font-size:clamp(30px,4vw,46px); font-weight:800; line-height:1.05;
    background:linear-gradient(115deg,#fff 30%,#b8ffd9 70%,#55e39a); -webkit-background-clip:text; background-clip:text; color:transparent; }
  .stream-tabs { position:relative; display:flex; gap:8px; margin-top:20px; flex-wrap:wrap; }
  .stream-tab { padding:12px 22px; border-radius:16px; border:1px solid var(--line); background:#ffffff06;
    color:var(--muted); cursor:pointer; text-align:left; min-width:150px; }
  .stream-tab .st-name { font-weight:800; font-size:14px; color:var(--ink); }
  .stream-tab .st-count { font-size:22px; font-weight:800; margin-top:2px; }
  .stream-tab[aria-pressed="true"] { border-color:var(--green); background:#55e39a14; box-shadow:0 0 20px #55e39a33; }
  .stream-tab[aria-pressed="true"] .st-name { color:var(--green); }
  .view-row { display:flex; gap:8px; flex-wrap:wrap; margin:20px 0 4px; }
  .view-chip { padding:8px 16px; border-radius:999px; border:1px solid var(--line-soft); background:transparent;
    color:var(--muted); font-size:12.5px; font-weight:700; cursor:pointer; letter-spacing:.03em; }
  .view-chip[aria-pressed="true"] { color:#fff; border-color:var(--green); background:#55e39a1c; }
  .feed-card { border-radius:18px; padding:22px 24px; background:linear-gradient(150deg,#101711,#0b0d0a);
    border:1px solid var(--line); margin-bottom:14px; position:relative; overflow:hidden; }
  .feed-card::before { content:""; position:absolute; left:0; top:0; bottom:0; width:3px;
    background:var(--fc-accent); box-shadow:0 0 12px var(--fc-accent); }
  .feed-card-top { display:flex; gap:10px; align-items:center; flex-wrap:wrap; font-size:11px;
    letter-spacing:.14em; font-weight:800; color:var(--fc-accent); }
  .feed-card-title { font-size:19px; font-weight:800; margin:8px 0 6px; line-height:1.3; }
  .feed-card-body { color:#c9d2c9; font-size:14px; line-height:1.6; }
  .feed-why { margin-top:12px; font-size:12.5px; color:var(--muted); border-top:1px dashed var(--line-soft); padding-top:10px; }
  .feed-why b { color:var(--green); font-size:10.5px; letter-spacing:.14em; display:block; margin-bottom:3px; }
  .feed-actions { display:flex; gap:8px; flex-wrap:wrap; margin-top:14px; }
  .feed-meta { margin-top:10px; font-size:11px; color:var(--muted); font-family:ui-monospace,monospace; }
  .new-pill { display:inline-flex; align-items:center; gap:8px; padding:8px 16px; border-radius:999px;
    background:#55e39a14; border:1px solid #55e39a55; color:var(--green); font-size:12.5px; font-weight:700; }
  @media (max-width:640px) { .feed-hero { padding:26px 20px 22px; } .stream-tab { min-width:0; flex:1; } }`;
  if (!document.getElementById('feed-room-css')) {
    const st = el('style', '', CSS); st.id = 'feed-room-css'; document.head.appendChild(st);
  }

  function FeedRoom() {
    const wrap = el('div');
    let stream = 'personal';
    let view = 'all';

    /* ——— ORIENTATION ——— */
    const hero = el('section', 'feed-hero');
    hero.innerHTML = `
      <div class="kicker" style="position:relative">STREAM</div>
      <h1 class="feed-title">One stream.<br>Three sources. Zero copies.</h1>
      <p class="room-desc" style="position:relative;max-width:620px;margin-top:10px">
        Everything the collective intelligence wants you to see — newest understanding first.
        Views filter the lens; the objects stay canonical.</p>
      ${C.fixtureBanner('Smart Feed')}
      <div class="stream-tabs" role="group" aria-label="Source streams"></div>`;
    const tabsEl = hero.querySelector('.stream-tabs');
    const tabBtns = {};
    STREAMS.forEach(([id, name, desc]) => {
      const n = OBJECTS.filter(o => o.stream === id).length;
      const b = el('button', 'stream-tab');
      b.setAttribute('aria-pressed', id === stream ? 'true' : 'false');
      b.title = desc;
      b.innerHTML = `<div class="st-name">${name}</div><div class="st-count">${n}</div>`;
      b.addEventListener('click', () => {
        stream = id;
        Object.entries(tabBtns).forEach(([k, btn]) => btn.setAttribute('aria-pressed', k === id ? 'true' : 'false'));
        render();
        toast(`${name} stream — ${n} object${n === 1 ? '' : 's'}. Same objects Today synthesizes.`, 'var(--green)');
      });
      tabBtns[id] = b; tabsEl.appendChild(b);
    });
    wrap.appendChild(hero);

    /* ——— Smart views ——— */
    const viewRow = el('div', 'view-row');
    viewRow.setAttribute('role', 'group');
    viewRow.setAttribute('aria-label', 'Smart views');
    const viewBtns = {};
    VIEWS.forEach(([id, label]) => {
      const b = el('button', 'view-chip', label);
      b.setAttribute('aria-pressed', id === view ? 'true' : 'false');
      b.addEventListener('click', () => {
        view = id;
        Object.entries(viewBtns).forEach(([k, btn]) => btn.setAttribute('aria-pressed', k === id ? 'true' : 'false'));
        render();
      });
      viewBtns[id] = b; viewRow.appendChild(b);
    });
    wrap.appendChild(viewRow);

    /* ——— New since last visit (honest: this device) ——— */
    const lastVisit = (() => {
      try {
        const v = localStorage.getItem('naya.feed.lastvisit');
        localStorage.setItem('naya.feed.lastvisit', new Date().toISOString());
        return v ? new Date(v) : null;
      } catch { return null; }
    })();
    const newCount = lastVisit ? OBJECTS.filter(o => new Date(o.ts) > lastVisit).length : OBJECTS.length;
    const newRow = el('div', '', `<div style="margin:14px 0 6px"><span class="new-pill">
      <span aria-hidden="true">✦</span> ${newCount} new since your last visit ${lastVisit ? '(this device)' : '(first visit on this device)'}</span></div>`);
    wrap.appendChild(newRow);

    /* ——— Intelligence stream ——— */
    const list = el('div');
    list.id = 'feed-stream';
    wrap.appendChild(list);

    function matchView(o) {
      switch (view) {
        case 'all': return true;
        case 'highlights': return o.kind !== 'activity';
        case 'decisions': return o.kind === 'decision';
        case 'learning': return o.kind === 'learning';
        case 'discoveries': return o.kind === 'discovery';
        case 'smart_notes': return o.kind === 'smart_note';
        case 'activity': return o.kind === 'activity';
        case 'reports': return o.kind === 'report';
        default: return true;
      }
    }
    function whyText(o) {
      if (o.stream !== stream) return '';
      const reasons = {
        personal: 'It is yours — your decisions, learning, and discoveries, newest first.',
        collective: 'Consented and anonymized — the intelligence is shared, never the contributor.',
        activity: 'It is happening now — current state and change in the substrate.',
      };
      return reasons[o.stream] || '';
    }

    function render() {
      list.innerHTML = '';
      const items = OBJECTS.filter(o => o.stream === stream && matchView(o))
        .sort((a, b) => new Date(b.ts) - new Date(a.ts));
      if (!items.length) {
        const empty = Board({ accent: ACC, icon: 'feed', title: 'Quiet stream', sub: 'Nothing here right now', lift: false });
        empty.body.innerHTML = `<p style="color:var(--muted);font-size:14px">This stream is quiet. The Feed does not manufacture content to fill silence — when the runtime connects, new intelligence lands here first.</p>`;
        list.appendChild(empty);
        return;
      }
      items.forEach(o => {
        const km = KIND_META[o.kind];
        const t = new Date(o.ts).toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', timeZone: 'America/Los_Angeles' });
        const card = el('article', 'feed-card');
        card.style.setProperty('--fc-accent', km.accent);
        card.innerHTML = `
          <div class="feed-card-top"><span>${km.label.toUpperCase()}</span><span style="color:var(--muted)">·</span>
            <span style="color:var(--muted)">${o.stream.toUpperCase()}</span><span style="color:var(--muted)">·</span>
            <span style="color:var(--muted)">${t}</span></div>
          <h3 class="feed-card-title">${o.title}</h3>
          <p class="feed-card-body">${o.body}</p>
          <div class="feed-why"><b>WHY AM I SEEING THIS</b>${whyText(o)}</div>
          <div class="feed-actions">
            <button class="btn" data-act="ev"><span>Evidence</span></button>
            <button class="btn btn-ghost" data-act="fav"><span>Save</span></button>
            <button class="btn btn-ghost" data-act="list"><span>List</span></button>
            <button class="btn btn-ghost" data-act="ask"><span>Ask Naya</span></button>
          </div>
          <div class="feed-meta">${o.id} · truth: FIXTURE · also in: ${o.id === 'IB-2026-10-01-004' || o.id === 'IB-2026-10-01-006' ? 'Today highlight reel' : 'Today stream'}</div>`;
        card.querySelector('[data-act="ev"]').addEventListener('click', () => C.openEvidence(o));
        card.querySelector('[data-act="fav"]').addEventListener('click', () => C.saveFavorite(o));
        card.querySelector('[data-act="list"]').addEventListener('click', () => C.addToList(o));
        card.querySelector('[data-act="ask"]').addEventListener('click', () => {
          const s = document.querySelector('.jewel-search input');
          if (s) { s.focus(); s.value = o.title; toast('Ask Naya about this object — retrieval over the brain.', 'var(--magenta)'); }
        });
        list.appendChild(card);
      });
    }
    render();

    /* ——— Continuity note ——— */
    const cont = Board({ accent: ACC, icon: 'nodes', title: 'One object, many lenses', sub: 'The continuity proof', lift: false });
    cont.body.innerHTML = `<p style="color:var(--muted);font-size:14px;max-width:640px">
      Every card above is the <b style="color:var(--ink)">same canonical object</b> that <i>Your Intelligence Today</i> synthesizes —
      same ID, same provenance, same truth state. Open any card\u2019s evidence here and in Today: identical.
      Feed streams it raw; Today tells its story; the Library will shelve it. Nothing is copied.</p>
      <div style="margin-top:12px"><button class="btn btn-ghost" id="f-today"><span>See it in Today</span></button></div>`;
    cont.querySelector('#f-today').addEventListener('click', () => window.NayaRouter.navigate('/hub/today'));
    wrap.appendChild(cont);

    return wrap;
  }

  window.NayaRooms = window.NayaRooms || {};
  FeedRoom.ownsHead = true;
  window.NayaRooms.feed = FeedRoom;
})();
