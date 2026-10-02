/* HUB — the intelligent cockpit. Rail + topbar + room outlet. */

function HubView(params) {
  const { el, Icons, toast } = window.NayaUI;
  const R = window.NayaRuntime;
  const activeRoom = params.room || 'feed';
  const room = R.ROOMS.find(r => r.id === activeRoom) || R.ROOMS[0];

  const shell = el('div', 'shell');

  /* ——— Rail ——— */
  const rail = el('nav', 'rail');
  rail.setAttribute('aria-label', 'Hub rooms');
  rail.innerHTML = `
    <div class="rail-mark">
      <span class="rail-emblem">${window.NayaJewels ? window.NayaJewels.emblem(40) : '<span class="jewel"></span>'}</span>
      <span><b>NAYANET</b><small>INTELLIGENT HUB</small></span>
    </div>`;
  R.ROOMS.forEach(r => {
    const b = el('button', 'rail-btn' + (r.id === room.id ? ' active' : ''));
    b.style.setProperty('--nav', r.accent);
    b.innerHTML = `<span class="ico jewel-ico">${window.NayaJewels ? window.NayaJewels.mark(r.id, 32) : Icons.icon(r.icon)}</span><span>${r.name}</span>`;
    b.setAttribute('aria-current', r.id === room.id ? 'page' : 'false');
    b.addEventListener('click', () => {
      closeDrawer();
      window.NayaRouter.navigate('/hub/' + r.id);
    });
    rail.appendChild(b);
  });
  const priv = el('div', 'rail-privacy',
    'PRIVATE BY DEFAULT.<br>SHARED BY CHOICE.<br>COLLECTIVE BY CONSENT.');
  rail.appendChild(priv);

  /* ——— Topbar ——— */
  const top = el('header', 'topbar');
  const toggle = el('button', 'rail-toggle', Icons.icon('menu'));
  toggle.setAttribute('aria-label', 'Open room navigation');
  toggle.setAttribute('aria-expanded', 'false');
  toggle.addEventListener('click', () => (shell.classList.contains('rail-open') ? closeDrawer() : openDrawer()));
  const search = el('div', 'jewel-search');
  search.innerHTML = `${Icons.icon('search')}<input type="search" placeholder="Ask the intelligence…" aria-label="Search the intelligence">`;
  const input = search.querySelector('input');
  input.addEventListener('keydown', async e => {
    if (e.key === 'Enter' && input.value.trim()) {
      input.setAttribute('aria-busy','true');
      const res = await R.search(input.value.trim(), { room: room.id });
      input.removeAttribute('aria-busy');
      if (!res.ok) toast(res.message || 'No verified answer is available.', room.accent);
      else showSearchResult(res);
    }
  });
  const identity = R.identitySnapshot ? R.identitySnapshot() : { display_name: 'You', state: 'not_verified' };
  const chip = el('div', 'identity-chip',
    `<span class="avatar" role="img" aria-label="Identity avatar"></span><span>${escapeHtml(identity.display_name || 'You')}</span>`);
  top.append(toggle, search, chip);

  /* ——— Room outlet ——— */
  const main = el('main', 'main');
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
  if (renderer) body.appendChild(renderer());
  else body.appendChild(notVerifiedPanel(room));
  main.appendChild(body);

  /* ——— Drawer law: exactly one nav surface. Backdrop, Escape, scroll lock. ——— */
  const backdrop = el('div', 'rail-backdrop');
  backdrop.setAttribute('aria-hidden', 'true');
  backdrop.addEventListener('click', closeDrawer);
  shell.appendChild(backdrop);
  function closeDrawer() {
    shell.classList.remove('rail-open');
    document.body.classList.remove('drawer-open');
    toggle.setAttribute('aria-expanded', 'false');
  }
  function openDrawer() {
    shell.classList.add('rail-open');
    document.body.classList.add('drawer-open');
    toggle.setAttribute('aria-expanded', 'true');
    const first = rail.querySelector('.rail-btn');
    if (first) first.focus();
  }
  if (!window.__nayaDrawerEsc) {
    window.__nayaDrawerEsc = function (e) {
      const open = document.querySelector('.shell.rail-open');
      if (e.key === 'Escape' && open) {
        open.classList.remove('rail-open');
        document.body.classList.remove('drawer-open');
        const t = open.querySelector('.rail-toggle');
        if (t) { t.setAttribute('aria-expanded', 'false'); t.focus(); }
      }
    };
    document.addEventListener('keydown', window.__nayaDrawerEsc);
  }

  shell.append(rail, top, main);
  return shell;

  function showSearchResult(res) {
    const payload = res.data ?? res;
    const list = window.NayaRoomKit ? window.NayaRoomKit.items(payload) : [];
    const existing = main.querySelector('.global-search-result');
    if (existing) existing.remove();
    const panel = el('section', 'board global-search-result');
    panel.style.setProperty('--room-accent', room.accent);
    const summary = payload.summary || payload.answer || payload.text || '';
    panel.innerHTML = `<div class="board-head"><div class="board-icon">${Icons.icon('search')}</div><div><div class="board-title">Ask the intelligence</div><div class="board-sub">Sourced retrieval · current room context</div></div></div><div class="board-body"></div>`;
    const body = panel.querySelector('.board-body');
    if (summary) body.insertAdjacentHTML('beforeend', `<p style="color:var(--ink-dim);font-size:14px;line-height:1.6">${escapeHtml(summary)}</p>`);
    if (list.length && window.NayaRoomKit) {
      const listWrap = el('div','intelligence-list');
      list.slice(0,8).forEach(x=>listWrap.appendChild(window.NayaRoomKit.intelCard(x,room.accent)));
      body.appendChild(listWrap);
    }
    if (!summary && !list.length) body.innerHTML='<div class="empty-instrument"><strong>No verified answer returned.</strong><p>The runtime connected, but returned no displayable intelligence.</p></div>';
    main.insertBefore(panel, bodyAnchor());
  }
  function bodyAnchor(){ return main.querySelector('.room-body'); }
  function escapeHtml(x){return String(x??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}

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
