/* ═══════════════════════════════════════════════════════════════════
   HUB SHELL — v4, per the binding design law (Ultimate Contract, PR #1331)
   14B.1: Top-left → room drawer. Top-right → product/navigation drawer.
   No persistent rail. The rooms drawer NEVER lists Smart Feed — the feed
   is the Main Show, not a room. The brand mark returns to the Main Show.
   Drawer law preserved: exactly one nav surface, backdrop, Escape,
   scroll lock, focus restore.
   ═══════════════════════════════════════════════════════════════════ */

function HubView(params) {
  const { el, Icons, toast } = window.NayaUI;
  const R = window.NayaRuntime;
  const activeRoom = params.room || 'feed';
  const room = R.ROOMS.find(r => r.id === activeRoom) || R.ROOMS[0];
  const isMainShow = room.id === 'feed';

  const shell = el('div', 'shell');

  /* ——— Top bar: two corner controls, nothing else competing ——— */
  const top = el('header', 'topbar');
  const leftBtn = el('button', 'corner-btn corner-left', Icons.icon('menu'));
  leftBtn.setAttribute('aria-label', 'Open room navigation');
  leftBtn.setAttribute('aria-expanded', 'false');
  const brand = el('button', 'brand-mark', '<span class="brand-jewel"></span><span><b>NAYANET</b><small>INTELLIGENT HUB</small></span>');
  brand.setAttribute('aria-label', 'NayaNET — back to the Main Show');
  brand.addEventListener('click', () => { closeDrawers(); window.NayaRouter.navigate('/hub/feed'); });
  const rightBtn = el('button', 'corner-btn corner-right', Icons.icon('grid'));
  rightBtn.setAttribute('aria-label', 'Open product navigation');
  rightBtn.setAttribute('aria-expanded', 'false');
  leftBtn.addEventListener('click', () => toggleDrawer('left'));
  rightBtn.addEventListener('click', () => toggleDrawer('right'));
  top.append(leftBtn, brand, rightBtn);

  /* ——— Left drawer: rooms. Smart Feed is NOT listed — it is the Main Show. ——— */
  const leftDrawer = el('nav', 'drawer drawer-left');
  leftDrawer.setAttribute('aria-label', 'Hub rooms');
  const lh = el('p', 'drawer-kicker', 'ROOMS');
  leftDrawer.appendChild(lh);
  R.ROOMS.filter(r => r.id !== 'feed').forEach(r => {
    const b = el('button', 'drawer-btn' + (r.id === room.id ? ' active' : ''));
    b.style.setProperty('--nav', r.accent);
    b.innerHTML = `<span class="ico">${Icons.icon(r.icon)}</span><span>${r.name}</span>`;
    b.setAttribute('aria-current', r.id === room.id ? 'page' : 'false');
    b.addEventListener('click', () => {
      closeDrawers();
      window.NayaRouter.navigate('/hub/' + r.id);
    });
    leftDrawer.appendChild(b);
  });
  const priv = el('div', 'drawer-privacy',
    'PRIVATE BY DEFAULT.<br>SHARED BY CHOICE.<br>COLLECTIVE BY CONSENT.');
  leftDrawer.appendChild(priv);

  /* ——— Right drawer: product / navigation ——— */
  const PRODUCT_LINKS = ['HOME','NAYA POWER','5-DAY CHALLENGE','ENTER FREE','POWERCAST','WHITE PAPER','ABOUT US','LOGIN'];
  const rightDrawer = el('nav', 'drawer drawer-right');
  rightDrawer.setAttribute('aria-label', 'Product navigation');
  const rh = el('p', 'drawer-kicker', 'NAYANET');
  rightDrawer.appendChild(rh);
  PRODUCT_LINKS.forEach(name => {
    const b = el('button', 'drawer-btn product-btn', '');
    b.innerHTML = `<span>${name}</span>`;
    b.addEventListener('click', () => {
      closeDrawers();
      toast(name + ' — the product surface this opens is outside this preview shell.', 'var(--ink-dim)');
    });
    rightDrawer.appendChild(b);
  });

  /* ——— Drawer law: exactly one nav surface ——— */
  const backdrop = el('div', 'drawer-backdrop');
  backdrop.setAttribute('aria-hidden', 'true');
  backdrop.addEventListener('click', closeDrawers);
  shell.appendChild(backdrop);

  let lastFocus = null;
  function toggleDrawer(which) {
    const open = shell.dataset.drawer;
    if (open === which) { closeDrawers(); return; }
    openDrawer(which);
  }
  function openDrawer(which) {
    lastFocus = document.activeElement;
    shell.dataset.drawer = which;
    document.body.classList.add('drawer-open');
    leftBtn.setAttribute('aria-expanded', which === 'left' ? 'true' : 'false');
    rightBtn.setAttribute('aria-expanded', which === 'right' ? 'true' : 'false');
    const first = (which === 'left' ? leftDrawer : rightDrawer).querySelector('.drawer-btn');
    if (first) first.focus();
  }
  function closeDrawers() {
    delete shell.dataset.drawer;
    document.body.classList.remove('drawer-open');
    leftBtn.setAttribute('aria-expanded', 'false');
    rightBtn.setAttribute('aria-expanded', 'false');
    if (lastFocus && lastFocus.focus) { try { lastFocus.focus(); } catch (e) {} lastFocus = null; }
  }
  if (!window.__nayaDrawerEsc) {
    window.__nayaDrawerEsc = function (e) {
      if (e.key !== 'Escape') return;
      const s = document.querySelector('.shell[data-drawer]');
      if (s) {
        delete s.dataset.drawer;
        document.body.classList.remove('drawer-open');
        s.querySelectorAll('.corner-btn').forEach(b => b.setAttribute('aria-expanded', 'false'));
      }
      if (typeof window.__nayaCloseEvidence === 'function') window.__nayaCloseEvidence();
    };
    document.addEventListener('keydown', window.__nayaDrawerEsc);
  }

  /* ——— Room outlet ——— */
  const main = el('main', 'main');
  if (!isMainShow) {
    /* Rooms get orientation: one line on what the room is for. The Main Show
       has its own presence → recognition grammar and needs no header wall. */
    const head = el('div', 'room-head');
    head.style.setProperty('--room-accent', room.accent);
    head.innerHTML = `
      <div class="kicker">${room.kicker}</div>
      <h2 class="room-title">${room.name}</h2>
      <p class="room-desc">${roomDesc(room.id)}</p>`;
    main.appendChild(head);
  }
  const body = el('div', 'room-body' + (isMainShow ? ' mainshow-body' : ''));
  body.style.setProperty('--room-accent', room.accent);
  const renderer = window.NayaRooms && window.NayaRooms[room.id];
  if (renderer) body.appendChild(renderer());
  else body.appendChild(notVerifiedPanel(room));
  main.appendChild(body);

  shell.append(top, leftDrawer, rightDrawer, main);
  return shell;

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
}
window.HubView = HubView;
