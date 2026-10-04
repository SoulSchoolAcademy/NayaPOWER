/* YOUR INTELLIGENCE TODAY — the reference masterpiece room.
   Metaphor: THE HIGHLIGHT REEL. Theme: magenta — human significance, daily synthesis.
   Five layers: ORIENTATION → CURRENT STATE → INTELLIGENCE → ACTION → PROOF.
   Room grammar: Hero → Intelligence Wall → Action Deck → Evidence Layer → Naya Layer.

   This room projects the shared canonical substrate (window.NayaCanonical) —
   the SAME objects Feed, Library, Lists, Spaces, and Reports project.
   One intelligence object → many projections. */

(function () {
  const { el, Board, toast } = window.NayaUI;
  const C = window.NayaCanonical;
  const { KIND_META, OBJECTS } = C;
  const ACC = 'var(--accent-today)';

  /* Today-specific: open loops + carry-forward (the room's action layer) */
  const LOOPS = [
    { id: 'LOOP-01', title: 'Today needs its independent re-score', state: 'open', note: 'Producer build is done; the independent seat has not scored it.' },
    { id: 'LOOP-02', title: 'Door registry re-fetch before Connect renders', state: 'open', note: 'Registry is canonical; the room must never render a stale copy.' },
    { id: 'LOOP-03', title: 'SN-127 collision re-scan (commit graph)', state: 'open', note: 'PR heads checked; the full graph scan is still owed.' },
  ];
  const CARRY = [
    { id: 'CF-01', title: 'Compound Today\u2019s architecture into Feed', note: 'Same object shape, same evidence drawer, Feed\u2019s three streams.' },
    { id: 'CF-02', title: 'Rendered QA for the next room', note: 'The shell matrix becomes the per-room matrix.' },
  ];

  /* ——— Pulse: derived from the objects, never hardcoded ——— */
  function pulse() {
    const byKind = {};
    OBJECTS.forEach(it => { byKind[it.kind] = (byKind[it.kind] || 0) + 1; });
    return { total: OBJECTS.length, byKind, loops: LOOPS.filter(l => l.state === 'open').length };
  }
  function nutshell() {
    const p = pulse(), parts = [];
    if (p.byKind.decision) parts.push(`${p.byKind.decision} decision${p.byKind.decision > 1 ? 's' : ''} locked`);
    if (p.byKind.learning) parts.push(`${p.byKind.learning} learning${p.byKind.learning > 1 ? 's' : ''} banked`);
    if (p.byKind.discovery) parts.push(`${p.byKind.discovery} ${p.byKind.discovery > 1 ? 'discoveries' : 'discovery'}`);
    if (p.loops) parts.push(`${p.loops} loop${p.loops > 1 ? 's' : ''} still open`);
    return parts.join(' · ') + '.';
  }
  function greeting() {
    const h = new Date().getHours();
    return h < 5 ? 'Night' : h < 12 ? 'Morning' : h < 18 ? 'Afternoon' : 'Evening';
  }
  function fmtDate(d) {
    return d.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric', timeZone: 'America/Los_Angeles' });
  }

  /* ——— Room-scoped styles: Today is its own world ——— */
  const CSS = `
  .today-hero { position:relative; overflow:hidden; border-radius:22px; padding:44px 40px 36px;
    background:linear-gradient(135deg,#160a20 0%,#0d0716 55%,#08060d 100%);
    border:1px solid #d86cff33; box-shadow:0 30px 80px -20px #d86cff44, inset 0 1px 0 #ffffff14; }
  .today-hero::before { content:""; position:absolute; inset:-40%; pointer-events:none;
    background:radial-gradient(ellipse 60% 50% at 20% 0%, #d86cff26, transparent 70%); }
  .today-date { position:relative; font-size:13px; letter-spacing:.22em; color:var(--magenta); font-weight:700; }
  .today-greet { position:relative; font-size:clamp(34px,5vw,58px); font-weight:800; line-height:1.04; margin:10px 0 14px;
    background:linear-gradient(115deg,#fff 30%,#e9b8ff 70%,#d86cff); -webkit-background-clip:text; background-clip:text; color:transparent; }
  .today-nutshell { position:relative; font-size:clamp(17px,2.2vw,22px); color:#e8e2f2; max-width:640px; line-height:1.5; }
  .today-nutshell b { color:#fff; }
  .pulse-ribbon { display:flex; gap:0; margin:26px 0 8px; border-radius:18px; overflow:hidden;
    border:1px solid var(--line); background:#0d0a14; }
  .pulse-seg { flex:1; padding:18px 20px; position:relative; cursor:pointer; border:0; background:transparent; color:var(--ink); text-align:left; }
  .pulse-seg + .pulse-seg { border-left:1px solid var(--line-soft); }
  .pulse-seg:hover { background:#ffffff08; }
  .pulse-num { font-size:30px; font-weight:800; }
  .pulse-lab { font-size:11px; letter-spacing:.16em; color:var(--muted); margin-top:4px; }
  .pulse-seg::after { content:""; position:absolute; left:0; top:0; bottom:0; width:3px; background:var(--seg-accent); box-shadow:0 0 12px var(--seg-accent); opacity:.85; }
  .pulse-src { font-size:11px; color:var(--muted); margin:8px 2px 0; }
  .mode-row { display:flex; gap:8px; margin:22px 0 4px; flex-wrap:wrap; }
  .mode-btn { padding:10px 20px; border-radius:999px; border:1px solid var(--line); background:transparent; color:var(--muted);
    font-weight:700; font-size:13px; cursor:pointer; letter-spacing:.04em; }
  .mode-btn[aria-pressed="true"] { color:#fff; border-color:var(--magenta); background:#d86cff22; box-shadow:0 0 18px #d86cff44; }
  .narrative { font-size:17px; line-height:1.75; color:#ddd6ea; max-width:720px; }
  .narrative .cite { color:var(--magenta); font-weight:700; cursor:pointer; font-size:.85em; vertical-align:super; }
  .narrative .cite:hover { text-decoration:underline; }
  .hl-reel { display:grid; gap:18px; margin-top:6px; }
  .hl-card { position:relative; border-radius:20px; padding:26px 28px; background:linear-gradient(150deg,#141021,#0c0913);
    border:1px solid var(--hl-accent); box-shadow:0 24px 60px -24px var(--hl-glow); overflow:hidden; }
  .hl-card::before { content:""; position:absolute; inset:0; pointer-events:none;
    background:radial-gradient(ellipse 50% 60% at 100% 0%, var(--hl-glow), transparent 70%); }
  .hl-kind { display:inline-flex; align-items:center; gap:8px; font-size:11px; letter-spacing:.2em; font-weight:800; color:var(--hl-accent); }
  .hl-title { position:relative; font-size:24px; font-weight:800; margin:10px 0 8px; line-height:1.2; }
  .hl-body { position:relative; color:#cfc8de; font-size:15px; line-height:1.65; max-width:640px; }
  .hl-why { position:relative; margin-top:14px; padding:12px 16px; border-left:3px solid var(--hl-accent);
    background:#ffffff06; border-radius:0 12px 12px 0; font-size:13.5px; color:#e6e0f2; }
  .hl-why b { color:var(--hl-accent); letter-spacing:.1em; font-size:11px; display:block; margin-bottom:4px; }
  .hl-actions { position:relative; display:flex; flex-wrap:wrap; gap:8px; margin-top:16px; }
  .hl-id { position:relative; margin-top:12px; font-size:11px; color:var(--muted); font-family:ui-monospace,monospace; }
  .stream-item { display:grid; grid-template-columns:86px 1fr; gap:16px; padding:16px 4px; border-bottom:1px solid var(--line-soft); cursor:pointer; border-radius:10px; }
  .stream-item:hover { background:#ffffff05; }
  .stream-time { font-size:12px; color:var(--muted); font-variant-numeric:tabular-nums; padding-top:3px; }
  .stream-title { font-weight:700; font-size:15px; }
  .stream-meta { font-size:12px; color:var(--muted); margin-top:4px; display:flex; gap:10px; flex-wrap:wrap; }
  .reflect { font-size:16.5px; line-height:1.8; color:#d9d2e8; max-width:720px; }
  .reflect p { margin:0 0 16px; }
  .reflect .cite { color:var(--magenta); font-weight:700; cursor:pointer; font-size:.85em; vertical-align:super; }
  .loop-row { display:flex; gap:14px; align-items:flex-start; padding:14px 4px; border-bottom:1px solid var(--line-soft); }
  .loop-dot { width:10px; height:10px; border-radius:50%; background:var(--orange); box-shadow:0 0 10px var(--orange); margin-top:6px; flex:none; }
  .loop-title { font-weight:700; font-size:14.5px; }
  .loop-note { font-size:12.5px; color:var(--muted); margin-top:3px; }
  .today-act-grid { display:grid; grid-template-columns:1fr 1fr; gap:18px; margin-top:26px; }
  .tour-glow { outline:2px solid var(--magenta) !important; outline-offset:4px; box-shadow:0 0 40px #d86cff88 !important; }
  @media (max-width:760px) { .today-act-grid { grid-template-columns:1fr; } }
  @media (max-width:640px) {
    .today-hero { padding:30px 22px 26px; }
    .pulse-ribbon { flex-wrap:wrap; }
    .pulse-seg { flex:1 1 40%; }
    .pulse-seg + .pulse-seg { border-left:0; border-top:1px solid var(--line-soft); }
    .stream-item { grid-template-columns:1fr; gap:6px; }
    .stream-time { padding-top:0; }
  }
  @media (prefers-reduced-motion: reduce) { .today-hero::before, .hl-card::before { display:none; } }`;
  if (!document.getElementById('today-room-css')) {
    const st = el('style', '', CSS); st.id = 'today-room-css'; document.head.appendChild(st);
  }

  /* ═══════════════ THE ROOM — five layers ═══════════════ */
  function TodayRoom() {
    const wrap = el('div');
    const now = new Date();
    let mode = 'brief';

    /* ——— LAYER 1 · ORIENTATION — DayOpeningFrame ——— */
    const hero = el('section', 'today-hero');
    hero.innerHTML = `
      <div class="today-date">${fmtDate(now).toUpperCase()}</div>
      <h1 class="today-greet">Good ${greeting()}.<br>Here is what today knows.</h1>
      <p class="today-nutshell" id="today-nutshell"></p>
      ${C.fixtureBanner('Your Intelligence Today')}
      <div style="position:relative;display:flex;gap:10px;flex-wrap:wrap;margin-top:22px">
        <button class="btn" id="t-explore"><span>Explore Today</span></button>
        <button class="btn btn-ghost" id="t-ask"><span>Ask Naya</span></button>
      </div>`;
    hero.querySelector('#today-nutshell').innerHTML =
      `Today so far: <b>${nutshell()}</b> Each one opens to its evidence.`;
    wrap.appendChild(hero);

    /* ——— LAYER 2 · CURRENT STATE — TodayPulse (computed ribbon) ——— */
    const p = pulse();
    const segs = [
      ['Highlights', p.total, 'var(--magenta)', 'every highlight below'],
      ['Decisions', p.byKind.decision || 0, 'var(--magenta)', 'locked today'],
      ['Learnings', p.byKind.learning || 0, 'var(--blue)', 'banked today'],
      ['Discoveries', p.byKind.discovery || 0, 'var(--green)', 'surfaced today'],
      ['Open loops', p.loops, 'var(--orange)', 'carried, not hidden'],
    ];
    const pulseSec = el('section');
    pulseSec.innerHTML = `<div class="pulse-ribbon" role="list" aria-label="Today's pulse, computed from today's intelligence"></div>
      <p class="pulse-src">Computed live from the ${p.total} intelligence objects on this page — not a score, not a rating. Counts support the story; they never are the story.</p>`;
    const ribbon = pulseSec.querySelector('.pulse-ribbon');
    segs.forEach(([label, n, accent, title]) => {
      const b = el('button', 'pulse-seg');
      b.style.setProperty('--seg-accent', accent);
      b.setAttribute('role', 'listitem');
      b.title = title;
      b.innerHTML = `<div class="pulse-num">${n}</div><div class="pulse-lab">${label.toUpperCase()}</div>`;
      b.addEventListener('click', () => {
        document.getElementById('today-highlights').scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
      ribbon.appendChild(b);
    });
    wrap.appendChild(pulseSec);

    /* ——— Mode selector (Brief / Deep / Review) ——— */
    const modeRow = el('div', 'mode-row');
    modeRow.setAttribute('role', 'group');
    modeRow.setAttribute('aria-label', 'Today view mode');
    const MODES = [['brief', 'Brief'], ['deep', 'Deep'], ['review', 'Review']];
    const modeBtns = {};
    MODES.forEach(([m, label]) => {
      const b = el('button', 'mode-btn', label);
      b.setAttribute('aria-pressed', m === mode ? 'true' : 'false');
      b.addEventListener('click', () => {
        mode = m;
        Object.entries(modeBtns).forEach(([k, btn]) => btn.setAttribute('aria-pressed', k === m ? 'true' : 'false'));
        renderStream();
        toast(`Today view: ${label} — the stream re-filters; nothing is duplicated.`, 'var(--magenta)');
      });
      modeBtns[m] = b; modeRow.appendChild(b);
    });

    /* ——— LAYER 3 · INTELLIGENCE ——— */
    const intelHead = Board({ accent: ACC, icon: 'spark', title: 'What changed', sub: 'The day as a story, not a pile of records', lift: false });

    const narrative = el('div', 'narrative');
    const cite = id => `<span class="cite" data-ev="${id}" role="link" tabindex="0" aria-label="Open evidence">[${OBJECTS.findIndex(i => i.id === id) + 1}]</span>`;
    narrative.innerHTML = `
      This morning the Hub\u2019s architecture locked into place: the Hub is <b>output, not input</b> ${cite('IB-2026-10-01-004')},
      and the rail settled at <b>eleven rooms</b> ${cite('IB-2026-10-01-006')}.
      Rendered QA caught a real defect class — off-canvas drawers inflating scroll width — and proved the fix ${cite('IB-2026-10-01-011')},
      while the scorecard stopped flattering itself ${cite('IB-2026-10-01-009')}.
      Underneath it all, the three-pipeline model now governs every pixel the Hub may show ${cite('IB-2026-10-01-002')}.`;
    narrative.querySelectorAll('.cite').forEach(c => {
      const open = () => C.openEvidence(OBJECTS.find(i => i.id === c.dataset.ev));
      c.addEventListener('click', open);
      c.addEventListener('keydown', e => { if (e.key === 'Enter') open(); });
    });
    intelHead.body.appendChild(narrative);
    wrap.appendChild(intelHead);

    /* HighlightScene — the signature instrument */
    const hlSec = el('section');
    hlSec.id = 'today-highlights';
    hlSec.innerHTML = `<div class="kicker">HIGHLIGHT REEL</div>
      <h2 class="room-title" style="margin-bottom:6px">Moments that matter</h2>
      <p class="room-desc" style="margin-bottom:18px">Each highlight explains <i>why</i> it was selected. Open any of them to its evidence.</p>
      <div class="hl-reel"></div>`;
    const reel = hlSec.querySelector('.hl-reel');
    const highlights = OBJECTS.filter(i => i.kind !== 'activity');
    highlights.forEach((item, idx) => {
      const km = KIND_META[item.kind];
      const card = el('article', 'hl-card');
      card.style.setProperty('--hl-accent', km.accent);
      card.style.setProperty('--hl-glow', item.kind === 'decision' ? '#d86cff33' : '#ffffff11');
      card.id = 'hl-' + idx;
      card.innerHTML = `
        <span class="hl-kind">${km.label.toUpperCase()} · ${item.stream.toUpperCase()}</span>
        <h3 class="hl-title">${item.title}</h3>
        <p class="hl-body">${item.body}</p>
        <div class="hl-why"><b>WHY THIS WAS SELECTED</b>${item.why_selected}</div>
        <div class="hl-actions">
          <button class="btn" data-act="ev"><span>Evidence</span></button>
          <button class="btn btn-ghost" data-act="fav"><span>Save favorite</span></button>
          <button class="btn btn-ghost" data-act="list"><span>Add to list</span></button>
        </div>
        <div class="hl-id">${item.id} · truth: FIXTURE · consent: ${item.consent}</div>`;
      card.querySelector('[data-act="ev"]').addEventListener('click', () => C.openEvidence(item));
      card.querySelector('[data-act="fav"]').addEventListener('click', () => C.saveFavorite(item));
      card.querySelector('[data-act="list"]').addEventListener('click', () => C.addToList(item));
      reel.appendChild(card);
    });
    wrap.appendChild(hlSec);

    /* DailyIntelligenceStream — three modes, one stream */
    const streamSec = el('section');
    streamSec.innerHTML = `<div class="kicker">INTELLIGENCE STREAM</div>
      <h2 class="room-title" style="margin-bottom:6px">The day underneath</h2>
      <p class="room-desc" style="margin-bottom:6px">One stream, three modes. Modes filter the lens — they never duplicate the objects.</p>`;
    streamSec.appendChild(modeRow);
    const streamList = el('div');
    streamList.id = 'today-stream';
    streamSec.appendChild(streamList);
    wrap.appendChild(streamSec);

    function renderStream() {
      streamList.innerHTML = '';
      const items = OBJECTS.filter(i => i.modes.includes(mode))
        .sort((a, b) => new Date(b.ts) - new Date(a.ts));
      if (!items.length) {
        streamList.appendChild(el('p', 'room-desc', 'A quiet mode. The day stays quiet rather than manufacturing content.'));
        return;
      }
      items.forEach(item => {
        const km = KIND_META[item.kind];
        const t = new Date(item.ts).toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', timeZone: 'America/Los_Angeles' });
        const row = el('div', 'stream-item');
        row.setAttribute('role', 'button');
        row.setAttribute('tabindex', '0');
        row.setAttribute('aria-label', `${item.title} — open evidence`);
        row.innerHTML = `
          <div class="stream-time">${t}</div>
          <div><div class="stream-title">${item.title}</div>
          <div class="stream-meta"><span style="color:${km.accent};font-weight:700">${km.label}</span>
          <span>${item.stream}</span><span style="font-family:ui-monospace,monospace">${item.id}</span></div></div>`;
        const open = () => C.openEvidence(item);
        row.addEventListener('click', open);
        row.addEventListener('keydown', e => { if (e.key === 'Enter') open(); });
        streamList.appendChild(row);
      });
    }
    renderStream();

    /* ——— LAYER 4 · ACTION — Open loops + carry-forward ——— */
    const actGrid = el('div', 'today-act-grid');
    const loops = Board({ accent: 'var(--orange)', icon: 'report', title: 'Open loops', sub: 'Carried in the open — never silently dropped', lift: false });
    loops.body.innerHTML = LOOPS.map(l => `
      <div class="loop-row"><span class="loop-dot"></span>
        <div><div class="loop-title">${l.title}</div><div class="loop-note">${l.id} · ${l.note}</div></div>
      </div>`).join('');
    const carry = Board({ accent: 'var(--green)', icon: 'arrow', title: 'Tomorrow carry-forward', sub: 'What the day hands to tomorrow', lift: false });
    carry.body.innerHTML = CARRY.map(c => `
      <div class="loop-row"><span class="loop-dot" style="background:var(--green);box-shadow:0 0 10px var(--green)"></span>
        <div><div class="loop-title">${c.title}</div><div class="loop-note">${c.id} · ${c.note}</div></div>
      </div>`).join('') + `
      <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:16px">
        <button class="btn btn-ghost" id="t-ledger"><span>Day ledger</span></button>
        <button class="btn btn-ghost" id="t-report"><span>Week report</span></button>
      </div>`;
    actGrid.append(loops, carry);
    wrap.appendChild(actGrid);
    carry.querySelector('#t-ledger').addEventListener('click', () => window.NayaRouter.navigate('/hub/ledger'));
    carry.querySelector('#t-report').addEventListener('click', () => window.NayaRouter.navigate('/hub/reports'));

    /* ——— LAYER 5 · PROOF — Naya Reflection ——— */
    const refl = Board({ accent: ACC, icon: 'core', title: 'Naya\u2019s reflection', sub: 'Grounded in today\u2019s evidence — every claim cites its source', lift: false });
    const rdiv = el('div', 'reflect');
    const rcite = id => `<span class="cite" data-ev="${id}" role="link" tabindex="0">[${OBJECTS.findIndex(i => i.id === id) + 1}]</span>`;
    rdiv.innerHTML = `
      <p>The most load-bearing thing that happened today was architectural, not visual: the Hub committed to being <b>output</b> ${rcite('IB-2026-10-01-004')}.
      That single ruling deleted an entire room, removed capture code, and forced the rail down to its contracted eleven ${rcite('IB-2026-10-01-006')} —
      which is what a real decision looks like: it destroys as much as it creates.</p>
      <p>The day also got more honest. The scorecard stopped reporting the builder\u2019s hopes and started reporting the auditor\u2019s findings ${rcite('IB-2026-10-01-009')},
      and a genuine defect — the kind users actually feel on their phones — was found by rendering, not by reading ${rcite('IB-2026-10-01-011')}.
      Nineteen checks, nineteen passes, one real fix. That is the whole method in miniature.</p>
      <p>What remains open is exactly what should remain open: the independent re-score, the registry re-fetch, the collision re-scan.
      Loops carried in the open are not debt — they are the proof the system knows what it hasn\u2019t proven yet.</p>`;
    rdiv.querySelectorAll('.cite').forEach(c => {
      const open = () => C.openEvidence(OBJECTS.find(i => i.id === c.dataset.ev));
      c.addEventListener('click', open);
      c.addEventListener('keydown', e => { if (e.key === 'Enter') open(); });
    });
    refl.body.appendChild(rdiv);
    wrap.appendChild(refl);

    /* ——— Guided tour: EXPLORE_TODAY ——— */
    let tourIdx = -1;
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    function tourStep() {
      document.querySelectorAll('.hl-card').forEach(c => c.classList.remove('tour-glow'));
      tourIdx++;
      if (tourIdx >= highlights.length) {
        tourIdx = -1;
        toast('Tour complete — the reel is yours to explore.', 'var(--magenta)');
        return;
      }
      const card = document.getElementById('hl-' + tourIdx);
      card.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'center' });
      card.classList.add('tour-glow');
      toast(`Highlight ${tourIdx + 1} of ${highlights.length}: ${highlights[tourIdx].title} — tap to continue the tour.`, 'var(--magenta)', 6000);
    }
    hero.querySelector('#t-explore').addEventListener('click', tourStep);
    hero.querySelector('#t-ask').addEventListener('click', () => {
      const s = document.querySelector('.jewel-search input');
      if (s) { s.focus(); toast('Ask Naya — retrieval over the brain. Type your question.', 'var(--magenta)'); }
    });

    return wrap;
  }

  TodayRoom.ownsHead = true;
  window.NayaRooms = window.NayaRooms || {};
  window.NayaRooms.today = TodayRoom;
})();
