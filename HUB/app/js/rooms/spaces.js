/* SMART SPACES — contexts as lenses.
   A Space is a context the intelligence is viewed through: Build, Review, Compass.
   Spaces don't own objects — they frame them. Same objects, different rooms of the mind. */

(function () {
  const { el, Board } = window.NayaUI;
  const C = window.NayaCanonical;
  const { KIND_META, OBJECTS } = C;
  const ACC = 'var(--accent-spaces)';

  /* Fixture space assignments — the runtime will govern real spaces */
  const SPACE_OF = {
    'IB-2026-10-01-004': 'build', 'IB-2026-10-01-006': 'build', 'IB-2026-10-01-012': 'build',
    'IB-2026-10-01-011': 'review', 'IB-2026-10-01-009': 'review',
    'IB-2026-10-01-002': 'compass', 'IB-2026-10-01-003': 'compass',
  };
  const SPACES = [
    ['build', 'Build', 'Where the work happens — decisions and build events.'],
    ['review', 'Review', 'Where the work is checked — learnings and proof.'],
    ['compass', 'Compass', 'Where direction is set — discoveries that reframe.'],
  ];

  const CSS = `
  .sp-hero { position:relative; border-radius:22px; padding:36px 36px 30px; overflow:hidden;
    background:linear-gradient(135deg,#0e1608 0%,#0a0e08 60%,#08060d 100%);
    border:1px solid #b8e3562e; box-shadow:0 30px 80px -20px #b8e3562b, inset 0 1px 0 #ffffff14; }
  .sp-title { position:relative; font-size:clamp(30px,4vw,46px); font-weight:800; line-height:1.05;
    background:linear-gradient(115deg,#fff 30%,#e4f5bd 70%,#b8e356); -webkit-background-clip:text; background-clip:text; color:transparent; }
  .space-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:16px; margin-top:20px; }
  .space-card { border-radius:20px; padding:26px; background:#0e120a; border:1px solid var(--line); cursor:pointer; }
  .space-card:hover { border-color:var(--lime); box-shadow:0 18px 44px -18px #b8e35666; }
  .space-card h3 { font-size:22px; margin:0 0 6px; }
  .space-card p { font-size:13px; color:var(--muted); margin-bottom:14px; }
  .space-card .mem { display:flex; gap:8px; flex-wrap:wrap; }
  .space-card .chip { font-size:11.5px; padding:6px 12px; border-radius:999px; background:#ffffff08;
    border:1px solid var(--line-soft); }
  @media (max-width:640px) { .sp-hero { padding:26px 20px 22px; } }`;
  if (!document.getElementById('sp-room-css')) {
    const st = el('style', '', CSS); st.id = 'sp-room-css'; document.head.appendChild(st);
  }

  function SpacesRoom() {
    const wrap = el('div');
    const hero = el('section', 'sp-hero');
    hero.innerHTML = `
      <div class="kicker" style="position:relative">SPACES</div>
      <h1 class="sp-title">Contexts,<br>not containers.</h1>
      <p class="room-desc" style="position:relative;max-width:620px;margin-top:10px">
        A Space frames intelligence without owning it. The same object can be seen from Build,
        Review, or Compass — it never moves, only the lens does.</p>
      ${C.fixtureBanner('Smart Spaces')}`;
    wrap.appendChild(hero);

    const grid = el('div', 'space-grid');
    SPACES.forEach(([id, name, desc]) => {
      const members = OBJECTS.filter(o => SPACE_OF[o.id] === id);
      const card = el('div', 'space-card');
      card.setAttribute('role', 'button'); card.setAttribute('tabindex', '0');
      card.setAttribute('aria-label', `${name} space — ${members.length} objects`);
      card.innerHTML = `<h3>${name}</h3><p>${desc}</p>
        <div class="mem">${members.map(o => `<span class="chip">${o.title.slice(0, 34)}${o.title.length > 34 ? '…' : ''}</span>`).join('')}</div>
        <div style="margin-top:12px;font-size:11px;color:var(--muted);letter-spacing:.1em">${members.length} MEMBER${members.length === 1 ? '' : 'S'} · 0 DUPLICATES</div>`;
      const open = () => {
        if (members[0]) C.openEvidence(members[0]);
      };
      card.addEventListener('click', open);
      card.addEventListener('keydown', e => { if (e.key === 'Enter') open(); });
      grid.appendChild(card);
    });
    wrap.appendChild(grid);

    const note = Board({ accent: ACC, icon: 'spaces', title: 'Space law', sub: 'Framing, not filing', lift: false });
    note.body.innerHTML = `<p style="color:var(--muted);font-size:13.5px;max-width:640px">
      Spaces are assigned by context and consent — an object in Compass is still the same canonical object
      the Feed streams. When the runtime connects, spaces become governed contexts with real membership.</p>`;
    wrap.appendChild(note);
    return wrap;
  }

  SpacesRoom.ownsHead = true;
  window.NayaRooms = window.NayaRooms || {};
  window.NayaRooms.spaces = SpacesRoom;
})();
