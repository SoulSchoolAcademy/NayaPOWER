/* INTELLIGENT LIBRARY — the shelves, not the store.
   The Library does not hold copies. It shelves references to the same canonical
   objects Feed streams and Today synthesizes. Shelved, not stored. */

(function () {
  const { el, Board } = window.NayaUI;
  const C = window.NayaCanonical;
  const { KIND_META, OBJECTS } = C;
  const ACC = 'var(--accent-library)';

  const CSS = `
  .lib-hero { position:relative; border-radius:22px; padding:36px 36px 30px; overflow:hidden;
    background:linear-gradient(135deg,#0a1020 0%,#0a0d14 60%,#08060d 100%);
    border:1px solid #55b9ee2e; box-shadow:0 30px 80px -20px #55b9ee33, inset 0 1px 0 #ffffff14; }
  .lib-hero::before { content:""; position:absolute; inset:-40%; pointer-events:none;
    background:radial-gradient(ellipse 55% 45% at 15% 0%, #55b9ee1f, transparent 70%); }
  .lib-title { position:relative; font-size:clamp(30px,4vw,46px); font-weight:800; line-height:1.05;
    background:linear-gradient(115deg,#fff 30%,#bfe6ff 70%,#55b9ee); -webkit-background-clip:text; background-clip:text; color:transparent; }
  .shelf { margin-top:26px; }
  .shelf-head { display:flex; align-items:baseline; gap:12px; margin-bottom:12px; }
  .shelf-name { font-size:20px; font-weight:800; }
  .shelf-count { font-size:12px; color:var(--muted); letter-spacing:.1em; }
  .shelf-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(260px,1fr)); gap:14px; }
  .shelf-card { border-radius:16px; padding:18px 20px; background:#0d1119; border:1px solid var(--line);
    cursor:pointer; position:relative; overflow:hidden; }
  .shelf-card:hover { border-color:var(--sc-accent); box-shadow:0 12px 30px -12px var(--sc-accent); }
  .shelf-card::before { content:""; position:absolute; left:0; top:0; bottom:0; width:3px; background:var(--sc-accent); }
  .shelf-card h4 { font-size:15px; font-weight:700; margin:6px 0; line-height:1.35; }
  .shelf-card p { font-size:12.5px; color:var(--muted); line-height:1.55; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; }
  .shelf-id { margin-top:10px; font-size:10.5px; color:var(--muted); font-family:ui-monospace,monospace; }
  .lib-search { position:relative; margin-top:18px; max-width:480px; }
  .lib-search input { width:100%; padding:13px 18px 13px 44px; border-radius:14px; border:1px solid var(--line);
    background:#0d0a14; color:var(--ink); font-size:14px; }
  .lib-search input:focus { outline:none; border-color:var(--blue); box-shadow:0 0 0 3px #55b9ee33; }
  .lib-search .mag { position:absolute; left:16px; top:50%; transform:translateY(-50%); color:var(--muted); }
  @media (max-width:640px) { .lib-hero { padding:26px 20px 22px; } }`;
  if (!document.getElementById('lib-room-css')) {
    const st = el('style', '', CSS); st.id = 'lib-room-css'; document.head.appendChild(st);
  }

  function LibraryRoom() {
    const wrap = el('div');
    let query = '';

    const hero = el('section', 'lib-hero');
    hero.innerHTML = `
      <div class="kicker" style="position:relative">LIBRARY</div>
      <h1 class="lib-title">Shelved,<br>not stored.</h1>
      <p class="room-desc" style="position:relative;max-width:620px;margin-top:10px">
        The Library shelves <b>references</b> to canonical intelligence — the same objects the Feed streams
        and Today synthesizes. Nothing here is a copy. Move the object, and every shelf updates.</p>
      ${C.fixtureBanner('Intelligent Library')}
      <div class="lib-search" style="position:relative">
        <span class="mag" aria-hidden="true">⌕</span>
        <input type="search" id="lib-q" placeholder="Search the shelves… (retrieval, not capture)" aria-label="Search the library">
      </div>`;
    wrap.appendChild(hero);

    const shelvesEl = el('div');
    wrap.appendChild(shelvesEl);

    function render() {
      shelvesEl.innerHTML = '';
      const kinds = Object.keys(KIND_META).filter(k => OBJECTS.some(o => o.kind === k));
      let total = 0;
      kinds.forEach(kind => {
        const km = KIND_META[kind];
        const items = OBJECTS.filter(o => o.kind === kind &&
          (!query || (o.title + ' ' + o.body).toLowerCase().includes(query)));
        if (!items.length) return;
        total += items.length;
        const shelf = el('section', 'shelf');
        shelf.innerHTML = `<div class="shelf-head">
          <span class="shelf-name" style="color:${km.accent}">${km.label}s</span>
          <span class="shelf-count">${items.length} REFERENCE${items.length > 1 ? 'S' : ''} · 0 COPIES</span></div>
          <div class="shelf-grid"></div>`;
        const grid = shelf.querySelector('.shelf-grid');
        items.forEach(o => {
          const card = el('article', 'shelf-card');
          card.style.setProperty('--sc-accent', km.accent);
          card.setAttribute('role', 'button');
          card.setAttribute('tabindex', '0');
          card.setAttribute('aria-label', `${o.title} — open evidence`);
          card.innerHTML = `
            <div style="font-size:10.5px;letter-spacing:.16em;font-weight:800;color:${km.accent}">${o.stream.toUpperCase()}</div>
            <h4>${o.title}</h4><p>${o.body}</p>
            <div class="shelf-id">${o.id} · truth: FIXTURE</div>`;
          const open = () => C.openEvidence(o);
          card.addEventListener('click', open);
          card.addEventListener('keydown', e => { if (e.key === 'Enter') open(); });
          grid.appendChild(card);
        });
        shelvesEl.appendChild(shelf);
      });
      if (!total) {
        shelvesEl.innerHTML = `<p class="room-desc" style="margin-top:20px">No references match \u201C${query}\u201D. The shelves stay honest — no results invented.</p>`;
      }
    }
    render();
    hero.querySelector('#lib-q').addEventListener('input', e => {
      query = e.target.value.trim().toLowerCase();
      render();
    });

    /* Continuity proof */
    const cont = Board({ accent: ACC, icon: 'library', title: 'The same objects, shelved', sub: 'Reference integrity', lift: false });
    cont.body.innerHTML = `<p style="color:var(--muted);font-size:14px;max-width:640px">
      Pick any shelf card and open its evidence — the canonical ID matches the Feed card and the Today highlight
      <b style="color:var(--ink)">exactly</b>. Three rooms, one object. That is the whole architecture in one gesture.</p>`;
    wrap.appendChild(cont);

    return wrap;
  }

  window.NayaRooms = window.NayaRooms || {};
  LibraryRoom.ownsHead = true;
  window.NayaRooms.library = LibraryRoom;
})();
