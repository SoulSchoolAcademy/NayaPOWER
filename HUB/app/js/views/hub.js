/* ═══════════════════════════════════════════════════════════════════
   HUB SHELL v2 — the quiet stage.
   Director's law (2026-10-02): no persistent rail. First paint shows only
   two quiet corner controls. Top-left opens the room drawer (ten rooms —
   Smart Feed is NOT a drawer entry; it IS the Main Show). Top-right opens
   the ecosystem drawer. The Main Show is a full-bleed intelligence feed
   with ONE sticky mode zone (Collective / Personal / Activity) — modes
   live here and nowhere else, never inside rooms.
   Drawer law: exactly one nav surface at a time · backdrop · Escape ·
   scroll lock · focus trap · focus restoration.
   ═══════════════════════════════════════════════════════════════════ */

function HubView(params) {
  const { el, Icons, toast } = window.NayaUI;
  const R = window.NayaRuntime;
  const Jewels = window.NayaJewels;
  const roomId = params.room || 'feed';
  const isMainShow = roomId === 'feed';
  const room = R.ROOMS.find(r => r.id === roomId) || R.ROOMS[0];

  const stage = el('div', 'stage');
  let lastFocus = null;

  /* ——— The two quiet corner controls ——— */
  function cornerBtn(side, glyph, label, drawerId) {
    const b = el('button', 'corner corner-' + side);
    b.innerHTML = Jewels ? Jewels.chip(glyph, 26, '#9d75ff') : Icons.icon('menu');
    b.setAttribute('aria-label', label);
    b.setAttribute('aria-expanded', 'false');
    b.setAttribute('aria-controls', drawerId);
    b.addEventListener('click', () => {
      const d = document.getElementById(drawerId);
      (d && d.classList.contains('open')) ? closeDrawers() : openDrawer(drawerId, b);
    });
    return b;
  }
  const tlCorner = cornerBtn('tl', 'lines', 'Open rooms', 'roomsDrawer');
  const trCorner = cornerBtn('tr', 'grid', 'Open ecosystem navigation', 'ecoDrawer');

  /* ——— Room drawer (left): the ten rooms, never Smart Feed ——— */
  function buildRoomsDrawer() {
    const d = el('nav', 'drawer drawer-left');
    d.id = 'roomsDrawer';
    d.setAttribute('aria-label', 'Hub rooms');
    d.innerHTML = `
      <div class="drawer-head">
        <span class="drawer-emblem"><img src="assets/naya-emblem-192.png" width="32" height="32" alt="Naya"></span>
        <span class="drawer-titles"><b>NAYANET</b><small>INTELLIGENT HUB</small></span>
      </div>
      <div class="drawer-list" role="list"></div>
      <div class="drawer-foot">PRIVATE BY DEFAULT.<br>SHARED BY CHOICE.<br>COLLECTIVE BY CONSENT.</div>`;
    const list = d.querySelector('.drawer-list');
    R.drawerRooms().forEach(r => {
      const b = el('button', 'drawer-btn' + (r.id === room.id && !isMainShow ? ' active' : ''));
      b.setAttribute('role', 'listitem');
      b.innerHTML = `
        <span class="drawer-ico">${Jewels ? Jewels.mark(r.id, 32) : Icons.icon(r.icon)}</span>
        <span class="drawer-label"><span class="drawer-name">${r.name}</span>
        <span class="drawer-kicker">${r.kicker}</span></span>
        <span class="drawer-go">${Icons.icon('arrow')}</span>`;
      if (r.id === room.id && !isMainShow) b.setAttribute('aria-current', 'page');
      b.setAttribute('aria-label', r.name + ' room');
      b.addEventListener('click', () => {
        closeDrawers();
        window.NayaRouter.navigate('/hub/' + r.id);
      });
      list.appendChild(b);
    });
    return d;
  }

  /* ——— Ecosystem drawer (right): the director's eight ——— */
  function buildEcoDrawer() {
    const d = el('nav', 'drawer drawer-right');
    d.id = 'ecoDrawer';
    d.setAttribute('aria-label', 'Ecosystem navigation');
    d.innerHTML = `
      <div class="drawer-head">
        <span class="drawer-titles"><b>ECOSYSTEM</b><small>ONE BRAIN · MANY DOORS</small></span>
      </div>
      <div class="drawer-list" role="list"></div>
      <div class="drawer-foot">EVERY DOOR OPENS ONTO THE SAME INTELLIGENCE.</div>`;
    const list = d.querySelector('.drawer-list');
    R.ECOSYSTEM_LINKS.forEach(link => {
      const live = link.kind === 'internal' || !!link.url;
      const b = el('button', 'drawer-btn' + (live ? '' : ' pending'));
      b.setAttribute('role', 'listitem');
      b.innerHTML = `
        <span class="drawer-ico">${Jewels ? Jewels.chip(link.icon, 26, '#9d75ff') : Icons.icon(link.icon)}</span>
        <span class="drawer-label"><span class="drawer-name">${link.name}</span>
        <span class="drawer-kicker">${live ? link.desc : 'LINK PENDING'}</span></span>
        <span class="drawer-go">${Icons.icon(live ? 'arrow' : 'clock')}</span>`;
      if (live) {
        b.setAttribute('aria-label', link.name + (link.kind === 'internal' ? '' : ', opens in a new tab'));
        b.addEventListener('click', () => {
          closeDrawers();
          if (link.kind === 'internal') window.NayaRouter.navigate(link.route);
          else window.open(link.url, '_blank', 'noopener');
        });
      } else {
        // Honest state, never a dead button pretending: the door exists,
        // its canonical address is being linked. One tap says so, plainly.
        b.setAttribute('aria-disabled', 'true');
        b.setAttribute('aria-label', link.name + ' — canonical link pending');
        b.addEventListener('click', () => {
          toast(`${link.name} opens here — the canonical address is being linked. Nothing was faked.`, '#9d75ff');
        });
      }
      list.appendChild(b);
    });
    return d;
  }

  const roomsDrawer = buildRoomsDrawer();
  const ecoDrawer = buildEcoDrawer();

  /* ——— Backdrop: one nav surface at a time ——— */
  const backdrop = el('div', 'backdrop');
  backdrop.setAttribute('aria-hidden', 'true');
  backdrop.addEventListener('click', closeDrawers);

  function openDrawer(id, opener) {
    closeDrawers(true);
    lastFocus = opener || document.activeElement;
    const d = document.getElementById(id);
    if (!d) return;
    d.classList.add('open');
    backdrop.classList.add('show');
    document.body.classList.add('drawer-open');
    const corner = stage.querySelector(`[aria-controls="${id}"]`);
    if (corner) corner.setAttribute('aria-expanded', 'true');
    const first = d.querySelector('.drawer-btn');
    if (first) first.focus();
  }
  function closeDrawers(silent) {
    let wasOpen = false;
    stage.querySelectorAll('.drawer.open').forEach(d => { d.classList.remove('open'); wasOpen = true; });
    if (!wasOpen && !silent) return;
    backdrop.classList.remove('show');
    document.body.classList.remove('drawer-open');
    stage.querySelectorAll('.corner[aria-expanded="true"]').forEach(c => c.setAttribute('aria-expanded', 'false'));
    if (!silent && lastFocus && document.contains(lastFocus)) lastFocus.focus();
    lastFocus = null;
  }

  /* ——— Focus trap: Tab never escapes an open drawer ——— */
  if (!window.__nayaDrawerTrap) {
    window.__nayaDrawerTrap = function (e) {
      if (e.key !== 'Tab') return;
      const open = document.querySelector('.stage .drawer.open');
      if (!open) return;
      const items = Array.from(open.querySelectorAll('button:not([disabled])'));
      if (!items.length) return;
      const first = items[0], last = items[items.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    };
    document.addEventListener('keydown', window.__nayaDrawerTrap);
  }

  /* ——— Escape: one global handler, closes whatever drawer is open ——— */
  if (!window.__nayaDrawerEsc) {
    window.__nayaDrawerEsc = function (e) {
      if (e.key !== 'Escape') return;
      const open = document.querySelector('.stage .drawer.open');
      if (!open) return;
      const cornerId = open.id;
      open.classList.remove('open');
      const bd = document.querySelector('.stage .backdrop');
      if (bd) bd.classList.remove('show');
      document.body.classList.remove('drawer-open');
      const corner = document.querySelector(`.corner[aria-controls="${cornerId}"]`);
      if (corner) { corner.setAttribute('aria-expanded', 'false'); corner.focus(); }
    };
    document.addEventListener('keydown', window.__nayaDrawerEsc);
  }

  /* ——— The Main Show: full-bleed feed + ONE sticky mode zone ——— */
  function modeZone() {
    const z = el('div', 'mode-zone');
    z.setAttribute('role', 'tablist');
    z.setAttribute('aria-label', 'Intelligence mode');
    const label = el('span', 'mode-zone-label', 'MODE');
    z.appendChild(label);
    R.MODES.forEach(m => {
      const active = R.mode === m.id;
      const b = el('button', 'mode-btn' + (active ? ' active' : ''));
      b.setAttribute('role', 'tab');
      b.setAttribute('aria-selected', active ? 'true' : 'false');
      b.style.setProperty('--mode-accent', m.accent);
      b.innerHTML = `<span class="mode-name">${m.name}</span><span class="mode-hint">${m.hint}</span>`;
      b.setAttribute('aria-label', `${m.name} mode — ${m.desc}`);
      b.addEventListener('click', () => {
        if (R.mode === m.id) return;
        R.setMode(m.id);
        window.NayaRouter.render();
        requestAnimationFrame(() => {
          const cur = document.querySelector('.mode-btn.active');
          if (cur) cur.focus({ preventScroll: true });
        });
      });
      z.appendChild(b);
    });
    return z;
  }

  function roomDesc(id) {
    return {
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

  function notVerifiedPanel(room) {
    const { StatePanel } = window.NayaUI;
    const c = R.NOT_VERIFIED_COPY;
    return StatePanel({
      accent: room.accent, icon: 'lock',
      title: c.title, body: c.body,
      actions: [{
        label: 'How this connects', icon: 'core',
        onClick: () => window.NayaRouter.navigate('/hub/settings'),
      }],
    });
  }

  const main = el('main', isMainShow ? 'main-show' : 'main');
  if (isMainShow) {
    // No dashboard grid, no navigation wall, no title block before the
    // content: the feed IS the arrival.
    main.appendChild(modeZone());
    const mount = el('div', 'feed-mount');
    mount.setAttribute('data-mode', R.mode);
    const renderer = window.NayaRooms && window.NayaRooms.feed;
    mount.appendChild(renderer ? renderer() : notVerifiedPanel(room));
    main.appendChild(mount);
  } else {
    const head = el('div', 'room-head');
    head.style.setProperty('--room-accent', room.accent);
    head.innerHTML = `
      <div class="kicker">${room.kicker}</div>
      <h2 class="room-title">${room.name}</h2>
      <p class="room-desc">${roomDesc(room.id)}</p>`;
    main.appendChild(head);
    const body = el('div', 'room-body');
    body.style.setProperty('--room-accent', room.accent);
    const renderer = window.NayaRooms && window.NayaRooms[room.id];
    body.appendChild(renderer ? renderer() : notVerifiedPanel(room));
    main.appendChild(body);
  }

  stage.append(tlCorner, trCorner, roomsDrawer, ecoDrawer, backdrop, main);
  return stage;
}
window.HubView = HubView;
