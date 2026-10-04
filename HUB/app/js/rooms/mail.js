/* SMART MAIL — triage as a lens.
   Mail is where intelligence that needs a human decision lands. Not email —
   the triage surface: what needs you, what can wait, what's FYI. Each thread
   is a canonical object with a decision attached. */

(function () {
  const { el, Board } = window.NayaUI;
  const C = window.NayaCanonical;
  const { KIND_META, OBJECTS } = C;
  const ACC = 'var(--accent-mail)';

  /* Fixture triage assignments */
  const TRIAGE = {
    'IB-2026-10-01-004': ['needs-you', 'Ratify the output-only law across room contracts'],
    'IB-2026-10-01-009': ['needs-you', 'Commission the independent re-score'],
    'IB-2026-10-01-011': ['waiting', 'Containment check queued for every room'],
    'IB-2026-10-01-006': ['waiting', 'Rail audit against the contract'],
    'IB-2026-10-01-002': ['fyi', 'Three-pipeline model recorded'],
    'IB-2026-10-01-003': ['fyi', 'Ask-Naya retrieval definition recorded'],
    'IB-2026-10-01-012': ['fyi', 'Foundation reconciliation logged'],
  };
  const LANES = [
    ['needs-you', 'Needs you', 'var(--magenta)', 'Decisions only you can make.'],
    ['waiting', 'Waiting', 'var(--orange)', 'In motion — nothing needed yet.'],
    ['fyi', 'FYI', 'var(--blue)', 'Recorded. Read when you want.'],
  ];

  const CSS = `
  .mail-hero { position:relative; border-radius:22px; padding:36px 36px 30px; overflow:hidden;
    background:linear-gradient(135deg,#0a1220 0%,#0a0d14 60%,#08060d 100%);
    border:1px solid #55b9ee2e; box-shadow:0 30px 80px -20px #55b9ee33, inset 0 1px 0 #ffffff14; }
  .mail-title { position:relative; font-size:clamp(30px,4vw,46px); font-weight:800; line-height:1.05;
    background:linear-gradient(115deg,#fff 30%,#cfeaff 70%,#55b9ee); -webkit-background-clip:text; background-clip:text; color:transparent; }
  .lane { margin-top:24px; }
  .lane-head { display:flex; align-items:center; gap:10px; margin-bottom:12px; }
  .lane-dot { width:10px; height:10px; border-radius:50%; background:var(--lane-c); box-shadow:0 0 10px var(--lane-c); }
  .lane-name { font-size:17px; font-weight:800; }
  .lane-sub { font-size:12px; color:var(--muted); }
  .thread { display:flex; gap:14px; align-items:flex-start; padding:16px 18px; border-radius:14px;
    background:#0c1018; border:1px solid var(--line); margin-bottom:10px; cursor:pointer; }
  .thread:hover { border-color:var(--lane-c); }
  .thread .t { font-weight:700; font-size:14.5px; }
  .thread .a { font-size:12.5px; color:var(--muted); margin-top:4px; }
  .thread .id { font-size:10.5px; color:var(--muted); font-family:ui-monospace,monospace; margin-top:6px; }
  @media (max-width:640px) { .mail-hero { padding:26px 20px 22px; } }`;
  if (!document.getElementById('mail-room-css')) {
    const st = el('style', '', CSS); st.id = 'mail-room-css'; document.head.appendChild(st);
  }

  function MailRoom() {
    const wrap = el('div');
    const hero = el('section', 'mail-hero');
    const needy = OBJECTS.filter(o => (TRIAGE[o.id] || [])[0] === 'needs-you').length;
    hero.innerHTML = `
      <div class="kicker" style="position:relative">MAIL</div>
      <h1 class="mail-title">Triage,<br>not inbox zero.</h1>
      <p class="room-desc" style="position:relative;max-width:620px;margin-top:10px">
        ${needy} thread${needy === 1 ? '' : 's'} need${needy === 1 ? 's' : ''} you. Everything else can wait or is FYI.
        Each thread is a canonical object — decide, and the object records it.</p>
      ${C.fixtureBanner('Smart Mail')}`;
    wrap.appendChild(hero);

    LANES.forEach(([laneId, name, color, sub]) => {
      const items = OBJECTS.filter(o => (TRIAGE[o.id] || [])[0] === laneId);
      const lane = el('section', 'lane');
      lane.style.setProperty('--lane-c', color);
      lane.innerHTML = `<div class="lane-head"><span class="lane-dot"></span>
        <span class="lane-name">${name}</span><span class="lane-sub">${sub} · ${items.length}</span></div>`;
      items.forEach(o => {
        const [_, action] = TRIAGE[o.id];
        const th = el('div', 'thread');
        th.setAttribute('role', 'button'); th.setAttribute('tabindex', '0');
        th.setAttribute('aria-label', `${o.title} — open evidence`);
        th.innerHTML = `<div><div class="t">${o.title}</div><div class="a">${action}</div>
          <div class="id">${o.id} · truth: FIXTURE</div></div>`;
        const open = () => C.openEvidence(o);
        th.addEventListener('click', open);
        th.addEventListener('keydown', e => { if (e.key === 'Enter') open(); });
        lane.appendChild(th);
      });
      wrap.appendChild(lane);
    });

    const note = Board({ accent: ACC, icon: 'mail', title: 'Mail is not email', sub: 'The distinction', lift: false });
    note.body.innerHTML = `<p style="color:var(--muted);font-size:13.5px;max-width:640px">
      Smart Mail triages intelligence that needs a human — it is not an email client.
      When the runtime connects, real threads arrive here with their decisions attached to the objects.</p>`;
    wrap.appendChild(note);
    return wrap;
  }

  MailRoom.ownsHead = true;
  window.NayaRooms = window.NayaRooms || {};
  window.NayaRooms.mail = MailRoom;
})();
