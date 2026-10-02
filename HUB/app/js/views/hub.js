/* ═══════════════════════════════════════════════════════════════════
   HUB CHASSIS — the 509 structure. One shell, one nav model, one room
   outlet. Enhances the 509 laboratory structure per the Human Director's
   2026-10-02 ruling: fixed left rail, plus-button ecosystem menu (no pill
   bar), mobile plus-button room drawer, the feed as the main show.

   The chassis never invents intelligence. Rooms render through it.
   A room may own one lens at shell level via NayaChassis.setLens(node)
   (the Main Show's Collective/Personal/Activity lens lives here, never
   duplicated inside the room).
   ═══════════════════════════════════════════════════════════════════ */

function HubView(params) {
  const { el, Icons, toast, StatePanel } = window.NayaUI;
  const R = window.NayaRuntime;
  const C = window.NayaContent || null;
  const activeRoom = params.room || 'feed';
  const room = R.ROOMS.find(r => r.id === activeRoom) || R.ROOMS[0];

  const shell = el('div', 'shell');

  /* ——— LEFT RAIL · fixed room navigation ——— */
  const rail = el('aside', 'rail left');
  rail.setAttribute('aria-label', 'Hub rooms');
  const brand = el('div', 'brand');
  brand.innerHTML = '<img src="../icon-192.png" alt="NayaNET mark"><div><b>NAYANET</b><small>INTELLIGENT HUB</small></div>';
  const nav = el('nav', 'nav');
  nav.setAttribute('aria-label', 'Intelligence rooms');
  R.ROOMS.forEach(r => {
    const b = el('button', 'nav-btn' + (r.id === room.id ? ' active' : ''));
    b.style.setProperty('--nav', r.accent);
    b.innerHTML = '<span class="ico">' + Icons.icon(r.icon) + '</span><span class="lbl">' + esc(r.name) + '</span>';
    b.setAttribute('aria-current', r.id === room.id ? 'page' : 'false');
    b.addEventListener('click', () => { closeDrawer(); window.NayaRouter.navigate('/hub/' + r.id); });
    nav.appendChild(b);
  });
  const priv = el('div', 'private', 'PRIVATE BY DEFAULT<br>SHARED BY CHOICE<br>COLLECTIVE BY CONSENT');
  rail.append(brand, nav, priv);

  /* ——— MAIN ——— */
  const main = el('main', 'main');
  main.setAttribute('aria-label', room.name);

  /* Topbar: rooms-plus (mobile) · title · source status · ecosystem plus menu */
  const top = el('header', 'top');
  const roomsPlus = el('button', 'rooms-plus', Icons.icon('plus'));
  roomsPlus.setAttribute('aria-label', 'Open room navigation');
  roomsPlus.setAttribute('aria-expanded', 'false');
  roomsPlus.addEventListener('click', () => (shell.classList.contains('drawer-open') ? closeDrawer() : openDrawer()));
  const title = el('div', 'top-title', '<b>INTELLIGENT HUB</b>');
  const status = el('div', 'top-status', '<span class="led" aria-hidden="true"></span><span>SOURCE · VISIBLE</span>');
  status.setAttribute('role', 'status');
  const pluswrap = el('div', 'pluswrap');
  const plusBtn = el('button', 'plus-btn', Icons.icon('plus'));
  plusBtn.setAttribute('aria-label', 'Ecosystem destinations');
  plusBtn.setAttribute('aria-expanded', 'false');
  plusBtn.setAttribute('aria-haspopup', 'true');
  const plusMenu = el('div', 'plusmenu');
  plusMenu.hidden = true;
  plusMenu.setAttribute('role', 'menu');
  plusMenu.innerHTML = '<div class="pm-head">DESTINATIONS</div>';
  ECOSYSTEM.forEach(([label, href]) => {
    const a = el('a', 'pluslink');
    a.href = href; a.target = '_blank'; a.rel = 'noopener'; a.setAttribute('role', 'menuitem');
    a.innerHTML = '<span>' + esc(label) + '</span><span class="ext" aria-hidden="true">↗</span>';
    plusMenu.appendChild(a);
  });
  plusBtn.addEventListener('click', e => { e.stopPropagation(); toggleMenu(); });
  pluswrap.append(plusBtn, plusMenu);
  top.append(roomsPlus, title, status, pluswrap);

  /* Ask Naya — chassis-level retrieval. One contextual-Naya interface. */
  const searchWrap = el('section', 'searchWrap');
  searchWrap.innerHTML =
    '<div class="searchRow" role="search">' +
    '<span class="search-ico" aria-hidden="true">' + Icons.icon('search') + '</span>' +
    '<input type="search" id="chassisSearch" placeholder="Ask the intelligence…" aria-label="Ask the intelligence" autocomplete="off">' +
    '</div><div class="searchHint">Ask Naya — retrieval across retained intelligence. Answers carry their sources.</div>';
  const searchInput = searchWrap.querySelector('input');
  searchInput.addEventListener('keydown', async e => {
    if (e.key === 'Enter' && searchInput.value.trim()) {
      searchInput.setAttribute('aria-busy', 'true');
      try {
        const res = await R.search(searchInput.value.trim(), { room: room.id });
        if (!res.ok) toast(res.message || 'No verified answer is available.', room.accent);
        else showSearchResult(res);
      } finally { searchInput.removeAttribute('aria-busy'); }
    }
  });

  /* Shell lens slot — owned by the room, positioned by the chassis. */
  const lensSlot = el('div', 'shell-lens');
  lensSlot.hidden = true;

  /* Room outlet */
  const outlet = el('div', 'room-outlet');
  if (room.id === 'feed') outlet.appendChild(mainShowHero(room, C));
  else {
    const head = el('div', 'room-head');
    head.style.setProperty('--room-accent', room.accent);
    head.innerHTML =
      '<div class="kicker">' + esc(room.kicker) + '</div>' +
      '<h2>' + esc(room.name) + '</h2>' +
      '<p>' + esc(roomDesc(room.id)) + '</p>';
    outlet.appendChild(head);
  }
  const body = el('div', 'room-body');
  body.style.setProperty('--room-accent', room.accent);
  body.setAttribute('aria-live', 'polite');
  const renderer = window.NayaRooms && window.NayaRooms[room.id];
  if (renderer) {
    try { body.appendChild(renderer()); }
    catch (err) { body.appendChild(roomError(room, err)); }
  } else body.appendChild(notVerified(room));
  outlet.appendChild(body);

  main.append(top, searchWrap, lensSlot, outlet);

  /* ——— RIGHT RAIL · Naya presence (wide screens) ——— */
  const right = el('aside', 'rail right');
  right.setAttribute('aria-label', 'Naya');
  right.appendChild(nayaCard());

  /* ——— Mobile drawer backdrop ——— */
  const backdrop = el('div', 'drawer-backdrop');
  backdrop.setAttribute('aria-hidden', 'true');
  backdrop.addEventListener('click', closeDrawer);

  shell.append(rail, main, right, backdrop);

  /* Chassis API — exactly one shell-level lens. */
  window.NayaChassis = window.NayaChassis || {};
  window.NayaChassis.setLens = node => {
    lensSlot.innerHTML = '';
    if (node) { lensSlot.appendChild(node); lensSlot.hidden = false; }
    else lensSlot.hidden = true;
  };
  window.NayaChassis.room = room;
  window.NayaChassis.closeDrawer = closeDrawer;

  ensureGlobalKeys();
  return shell;

  /* ——— internals ——— */
  function openDrawer() {
    shell.classList.add('drawer-open');
    document.body.classList.add('drawer-open');
    roomsPlus.setAttribute('aria-expanded', 'true');
    const f = nav.querySelector('.nav-btn');
    if (f) f.focus();
  }
  function closeDrawer() {
    shell.classList.remove('drawer-open');
    document.body.classList.remove('drawer-open');
    roomsPlus.setAttribute('aria-expanded', 'false');
  }
  function toggleMenu() {
    const willOpen = plusMenu.hidden;
    plusMenu.hidden = !willOpen;
    plusBtn.setAttribute('aria-expanded', String(willOpen));
    if (willOpen) { const f = plusMenu.querySelector('.pluslink'); if (f) f.focus(); }
  }
  function closeMenu() {
    if (!plusMenu.hidden) { plusMenu.hidden = true; plusBtn.setAttribute('aria-expanded', 'false'); }
  }
  function ensureGlobalKeys() {
    if (window.__nayaChassisKeys) return;
    window.__nayaChassisKeys = true;
    document.addEventListener('click', e => {
      if (!e.target.closest('.pluswrap')) {
        document.querySelectorAll('.plusmenu').forEach(m => { m.hidden = true; });
        document.querySelectorAll('.plus-btn').forEach(b => b.setAttribute('aria-expanded', 'false'));
      }
    });
    document.addEventListener('keydown', e => {
      if (e.key !== 'Escape') return;
      document.querySelectorAll('.plusmenu').forEach(m => { m.hidden = true; });
      const open = document.querySelector('.shell.drawer-open');
      if (open) {
        open.classList.remove('drawer-open');
        document.body.classList.remove('drawer-open');
        const t = open.querySelector('.rooms-plus');
        if (t) { t.setAttribute('aria-expanded', 'false'); t.focus(); }
      }
    });
  }

  function mainShowHero(rm, content) {
    const hour = new Date().getHours();
    const greet = hour < 12 ? 'Good morning' : hour < 18 ? 'Good afternoon' : 'Good evening';
    // Identity comes from the canonical chassis identity model — never a hardcoded name.
    // When the governed runtime is not connected, no name is claimed.
    let who = '';
    try {
      const id = R.identitySnapshot && R.identitySnapshot();
      if (id && id.display_name && id.display_name !== 'You') who = ', ' + id.display_name;
    } catch (e) { /* identity unavailable — fall back to neutral greeting */ }
    const now = content && content.today && content.today.now && content.today.now[0]
      ? content.today.now[0]
      : 'Your intelligence, as it exists now.';
    const h = el('section', 'hero');
    h.style.setProperty('--room-accent', rm.accent);
    h.innerHTML =
      '<div class="eyebrow">NAYANET · HUMAN-FACING INTELLIGENCE</div>' +
      '<h1>' + greet + esc(who) + '.</h1>' +
      '<p class="hero-sub">' + esc(now) + '</p>' +
      '<p class="hero-prov">Repository snapshot · main 10190133 · captured 2026-10-02 · nothing fabricated</p>';
    return h;
  }

  function nayaCard() {
    const wrap = el('div');
    const card = el('div', 'naya-card');
    card.innerHTML =
      '<div class="naya-face" aria-hidden="true"><span>N</span></div>' +
      '<h2>Naya</h2><div class="naya-sub">TRUSTED THINKING PARTNER</div>' +
      '<div class="naya-block"><b>WHAT NAYA IS DOING</b>' +
      '<p>Surfacing the highest-signal intelligence from the repository snapshot — newest understanding first.</p></div>' +
      '<div class="naya-block"><b>WHY THIS MATTERS</b>' +
      '<p>The Hub should reduce the work required to understand intelligence — not add another place to manage.</p></div>' +
      '<div class="naya-actions">' +
      '<button class="btn" data-act="ask"><span>ASK NAYA</span></button>' +
      '<button class="btn btn-ghost" data-act="today"><span>WHAT SHOULD I KNOW?</span></button>' +
      '</div>';
    card.querySelector('[data-act="ask"]').addEventListener('click', () => {
      const s = document.getElementById('chassisSearch');
      if (s) { s.scrollIntoView({ block: 'nearest', behavior: 'smooth' }); s.focus(); }
    });
    card.querySelector('[data-act="today"]').addEventListener('click', () => window.NayaRouter.navigate('/hub/today'));
    const trust = el('div', 'rail-card');
    trust.innerHTML = '<b>TRUST STATE</b><p>Source content is marked separately from interpretation. Snapshot-pinned; no remote result is fabricated in this package.</p>';
    wrap.append(card, trust);
    return wrap;
  }

  function showSearchResult(res) {
    const payload = res.data ?? res;
    const list = window.NayaRoomKit ? window.NayaRoomKit.items(payload) : [];
    const prev = outlet.querySelector('.global-search-result');
    if (prev) prev.remove();
    const panel = el('section', 'board global-search-result');
    panel.style.setProperty('--room-accent', room.accent);
    panel.innerHTML =
      '<div class="board-head"><div class="board-icon">' + Icons.icon('search') + '</div>' +
      '<div><div class="board-title">Ask the intelligence</div>' +
      '<div class="board-sub">Sourced retrieval · ' + esc(room.name) + ' context</div></div></div>' +
      '<div class="board-body"></div>';
    const pb = panel.querySelector('.board-body');
    const summary = payload.summary || payload.answer || payload.text || '';
    if (summary) {
      const p = el('p', 'search-answer', esc(summary));
      pb.appendChild(p);
    }
    if (list.length && window.NayaRoomKit) {
      const lw = el('div', 'intelligence-list');
      list.slice(0, 8).forEach(x => lw.appendChild(window.NayaRoomKit.intelCard(x, room.accent)));
      pb.appendChild(lw);
    }
    if (!summary && !list.length) {
      pb.appendChild(el('div', 'empty-instrument', '<strong>No verified answer returned.</strong><p>The runtime connected, but returned no displayable intelligence.</p>'));
    }
    const dismiss = el('button', 'btn btn-ghost mini', '<span>Dismiss</span>');
    dismiss.style.setProperty('--btn-accent', room.accent);
    dismiss.addEventListener('click', () => panel.remove());
    pb.appendChild(dismiss);
    outlet.insertBefore(panel, body);
    panel.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
  }

  function notVerified(rm) {
    const c = R.NOT_VERIFIED_COPY || { title: 'Not verified', body: 'This surface is not connected to verified intelligence.' };
    return StatePanel({
      accent: rm.accent, icon: 'lock', title: c.title, body: c.body,
      actions: [{ label: 'System health', icon: 'core', ghost: true,
        onClick: () => window.NayaRouter.navigate('/hub/settings') }],
    });
  }
  function roomError(rm, err) {
    return StatePanel({
      accent: rm.accent, icon: 'alert',
      title: 'This room failed to render',
      body: 'The room renderer threw an error. Nothing was fabricated in its place. ' +
            'Technical detail: ' + esc(err && err.message ? err.message : String(err)),
      actions: [{ label: 'Reload the Hub', icon: 'core',
        onClick: () => window.NayaRouter.navigate('/hub/' + rm.id) }],
    });
  }
  function esc(x) {
    return String(x ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  }
  function roomDesc(id) {
    return {
      feed: 'One stream of everything the collective intelligence wants you to see — newest understanding first.',
      today: 'Your day, answered by the intelligence. What matters, what changed, what deserves you.',
      reports: 'Proof, not promises. Every report carries its evidence and its receipts.',
      library: 'Everything retained, organized by what it means — not where it happened to land.',
      connect: 'One brain. Many doors. Choose how you — or your agents, apps, and systems — step into the same intelligence.',
      ledger: 'Every contribution, valued. The accountability layer of the collective mind.',
      connections: 'Humans, AIs, and machines you share intelligence with — each on your terms.',
      lists: 'Living lists that stay current because the intelligence behind them does.',
      mail: 'Your messages, understood — triaged by meaning, not just recency.',
      spaces: 'Rooms inside the Hub for projects, people, and ideas that belong together.',
      settings: 'Your Hub, your rules. Identity, privacy, doors, preferences — and System Health.'
    }[id] || '';
  }
}

/* Ecosystem destinations — real addresses. The pill bar is gone;
   the plus button is the only ecosystem surface. */
const ECOSYSTEM = [
  ['HOME', 'https://hmclibrary.groovemember.net/home'],
  ['NAYA POWER', 'https://academy.nayanet.app/'],
  ['“5” DAY CHALLENGE', 'https://academy.nayanet.app/'],
  ['ENTER FREE', 'https://humanmaximuscodex.groovesell.com/checkout/08fba2cbd6488ef4d2cc82b52d361dab'],
  ['POWERCAST', 'https://nayanet.groovepages.com/powerplayer'],
  ['WHITE PAPER', 'https://nayanet.groovepages.com/whitepaper'],
  ['ABOUT US', 'https://nayanet.groovepages.com/aboutus'],
  ['HMC LOGIN', 'https://hmclibrary.groovemember.net/login'],
];

window.HubView = HubView;
