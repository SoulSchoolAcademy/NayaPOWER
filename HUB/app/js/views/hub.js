/* ═══════════════════════════════════════════════════════════════════
   HUB SHELL v2.1 — the quiet stage, enhanced.
   Director's law (2026-10-02): no persistent rail. First paint shows only
   two quiet "+" corner controls. Top-left opens rooms (drawer on desktop,
   popup menu on mobile). Top-right opens the ecosystem popup menu — never
   a pill nav across the top. The Main Show is a full-bleed intelligence
   feed with ONE sticky mode zone (Collective / Personal / Activity) —
   modes live here and nowhere else, never inside rooms.
   Nav law: exactly one nav surface at a time · backdrop · Escape ·
   scroll lock · focus trap · focus restoration.
   Director's enhancement (2026-10-02): enhance, don't redesign. Plus
   buttons open popup menus; the feed IS the presentation — scroll, clean,
   premium, nothing overlapping.
   ═══════════════════════════════════════════════════════════════════ */

function HubView(params) {
  const { el, Icons, toast } = window.NayaUI;
  const R = window.NayaRuntime;
  const Jewels = window.NayaJewels;
  const roomId = params.room || 'feed';
  const isMainShow = roomId === 'feed';
  const room = R.ROOMS.find(r => r.id === roomId) || R.ROOMS[0];
  const isMobile = () => window.matchMedia('(max-width: 768px)').matches;

  const stage = el('div', 'stage');
  let lastFocus = null;

  /* ——— The two quiet "+" corner controls ——— */
  function cornerBtn(side, label, controls, toggle) {
    const b = el('button', 'corner corner-' + side);
    b.innerHTML = Jewels ? Jewels.chip('add', 26, '#9d75ff') : Icons.icon('add');
    b.setAttribute('aria-label', label);
    b.setAttribute('aria-expanded', 'false');
    b.setAttribute('aria-controls', controls);
    b.addEventListener('click', () => toggle(b));
    return b;
  }
  const tlCorner = cornerBtn('tl', 'Rooms', 'roomsDrawer roomsMenu', () => {
    if (navOpen()) return closeNav();
    openNav(isMobile() ? 'roomsMenu' : 'roomsDrawer');
  });
  const trCorner = cornerBtn('tr', 'Ecosystem menu', 'ecoMenu', () => {
    if (navOpen()) return closeNav();
    openNav('ecoMenu');
  });

  /* ——— Nav surfaces: drawers and popup menus share one law ——— */
  function navOpen() { return !!stage.querySelector('.nav-surface.open'); }
  function openNav(id, opener) {
    closeNav(true);
    lastFocus = opener || document.activeElement;
    const s = document.getElementById(id);
    if (!s) return;
    s.classList.add('open');
    backdrop.classList.add('show');
    document.body.classList.add('drawer-open');
    const corner = stage.querySelector('[aria-controls~="' + id + '"]');
    if (corner) corner.setAttribute('aria-expanded', 'true');
    const first = s.querySelector('button');
    if (first) first.focus();
  }
  function closeNav(silent) {
    let wasOpen = false;
    stage.querySelectorAll('.nav-surface.open').forEach(s => { s.classList.remove('open'); wasOpen = true; });
    if (!wasOpen && !silent) return;
    backdrop.classList.remove('show');
    document.body.classList.remove('drawer-open');
    stage.querySelectorAll('.corner[aria-expanded="true"]').forEach(c => c.setAttribute('aria-expanded', 'false'));
    if (!silent && lastFocus && document.contains(lastFocus)) lastFocus.focus();
    lastFocus = null;
  }

  /* ——— Popup menu: anchored to its "+" corner, premium, compact ——— */
  function buildPopupMenu(id, side, title, sub) {
    const m = el('div', 'popup-menu nav-surface popup-' + side);
    m.id = id;
    m.setAttribute('role', 'menu');
    m.setAttribute('aria-label', title);
    m.innerHTML =
      '<div class="popup-head"><b>' + title + '</b><small>' + sub + '</small></div>' +
      '<div class="popup-list" role="none"></div>';
    return m;
  }
  function popupItem(menu, opts) {
    const b = el('button', 'popup-item' + (opts.pending ? ' pending' : '') + (opts.active ? ' active' : ''));
    b.setAttribute('role', 'menuitem');
    b.innerHTML =
      '<span class="popup-ico">' + (opts.iconHTML || (Jewels ? Jewels.chip(opts.icon, 24, '#9d75ff') : Icons.icon(opts.icon))) + '</span>' +
      '<span class="popup-label"><span class="popup-name">' + opts.name + '</span>' +
      '<span class="popup-kicker">' + (opts.pending ? 'LINK PENDING' : opts.kicker) + '</span></span>' +
      '<span class="popup-go">' + Icons.icon(opts.pending ? 'clock' : 'arrow') + '</span>';
    b.setAttribute('aria-label', opts.ariaLabel || opts.name);
    if (opts.pending) b.setAttribute('aria-disabled', 'true');
    if (opts.active) b.setAttribute('aria-current', 'page');
    b.addEventListener('click', () => opts.onSelect(b));
    menu.querySelector('.popup-list').appendChild(b);
    return b;
  }

  /* ——— Ecosystem popup menu (top-right "+"): the director's eight ——— */
  function buildEcoMenu() {
    const m = buildPopupMenu('ecoMenu', 'right', 'ECOSYSTEM', 'ONE BRAIN · MANY DOORS');
    R.ECOSYSTEM_LINKS.forEach(link => {
      const live = link.kind === 'internal' || !!link.url;
      popupItem(m, {
        icon: link.icon, name: link.name, kicker: link.desc, pending: !live,
        ariaLabel: link.name + (!live ? ' — canonical link pending' : (link.kind === 'internal' ? '' : ', opens in a new tab')),
        onSelect: () => {
          closeNav();
          if (!live) {
            // Honest state, never a dead button pretending: the door exists,
            // its canonical address is being linked. One tap says so, plainly.
            toast(link.name + ' opens here — the canonical address is being linked. Nothing was faked.', '#9d75ff');
            return;
          }
          if (link.kind === 'internal') window.NayaRouter.navigate(link.route);
          else window.open(link.url, '_blank', 'noopener');
        }
      });
    });
    return m;
  }

  /* ——— Rooms popup menu (mobile, top-left "+"): the ten rooms ——— */
  function buildRoomsMenu() {
    const m = buildPopupMenu('roomsMenu', 'left', 'ROOMS', 'TEN DESTINATIONS');
    R.drawerRooms().forEach(r => {
      const active = r.id === room.id && !isMainShow;
      popupItem(m, {
        iconHTML: Jewels ? Jewels.mark(r.id, 30) : Icons.icon(r.icon),
        name: r.name, kicker: r.kicker, active,
        ariaLabel: r.name + ' room',
        onSelect: () => { closeNav(); window.NayaRouter.navigate('/hub/' + r.id); }
      });
    });
    return m;
  }

  /* ——— Room drawer (desktop, left): the ten rooms, never Smart Feed ——— */
  function buildRoomsDrawer() {
    const d = el('nav', 'drawer drawer-left nav-surface');
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
        closeNav();
        window.NayaRouter.navigate('/hub/' + r.id);
      });
      list.appendChild(b);
    });
    return d;
  }

  const roomsDrawer = buildRoomsDrawer();
  const roomsMenu = buildRoomsMenu();
  const ecoMenu = buildEcoMenu();

  /* ——— Backdrop: one nav surface at a time ——— */
  const backdrop = el('div', 'backdrop');
  backdrop.setAttribute('aria-hidden', 'true');
  backdrop.addEventListener('click', closeNav);

  /* ——— Focus trap: Tab never escapes an open nav surface ——— */
  if (!window.__nayaNavTrap) {
    window.__nayaNavTrap = function (e) {
      if (e.key !== 'Tab') return;
      const open = document.querySelector('.stage .nav-surface.open');
      if (!open) return;
      const items = Array.from(open.querySelectorAll('button:not([disabled])'));
      if (!items.length) return;
      const first = items[0], last = items[items.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    };
    document.addEventListener('keydown', window.__nayaNavTrap);
  }

  /* ——— Escape: one global handler, closes whatever nav surface is open.
     Attached once, so it must work from live document queries — never from
     this render's closures, which go stale on the next route render. ——— */
  if (!window.__nayaNavEsc) {
    window.__nayaNavEsc = function (e) {
      if (e.key !== 'Escape') return;
      const open = document.querySelector('.stage .nav-surface.open');
      if (!open) return;
      const surfaceId = open.id;
      open.classList.remove('open');
      const stageEl = open.closest('.stage');
      if (stageEl) {
        const bd = stageEl.querySelector('.backdrop');
        if (bd) bd.classList.remove('show');
        stageEl.querySelectorAll('.corner[aria-expanded="true"]').forEach(c => c.setAttribute('aria-expanded', 'false'));
      }
      document.body.classList.remove('drawer-open');
      const corner = document.querySelector('.corner[aria-controls~="' + surfaceId + '"]');
      if (corner) corner.focus();
    };
    document.addEventListener('keydown', window.__nayaNavEsc);
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

  stage.append(tlCorner, trCorner, roomsDrawer, roomsMenu, ecoMenu, backdrop, main);
  return stage;
}
window.HubView = HubView;
