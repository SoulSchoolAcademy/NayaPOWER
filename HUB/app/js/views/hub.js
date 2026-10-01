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
      <span class="jewel"></span>
      <span><b>NAYANET</b><small>INTELLIGENT HUB</small></span>
    </div>`;
  R.ROOMS.forEach(r => {
    const b = el('button', 'rail-btn' + (r.id === room.id ? ' active' : ''));
    b.style.setProperty('--nav', r.accent);
    b.innerHTML = `<span class="ico">${Icons.icon(r.icon)}</span><span>${r.name}</span>`;
    b.setAttribute('aria-current', r.id === room.id ? 'page' : 'false');
    b.addEventListener('click', () => {
      window.NayaRouter.navigate('/hub/' + r.id);
      shell.classList.remove('rail-open');
    });
    rail.appendChild(b);
  });
  const priv = el('div', 'rail-privacy',
    'PRIVATE BY DEFAULT.<br>SHARED BY CHOICE.<br>COLLECTIVE BY CONSENT.<br>PUBLIC BY DECISION.');
  rail.appendChild(priv);

  /* ——— Topbar ——— */
  const top = el('header', 'topbar');
  const toggle = el('button', 'rail-toggle', Icons.icon('menu'));
  toggle.setAttribute('aria-label', 'Open room navigation');
  toggle.addEventListener('click', () => shell.classList.toggle('rail-open'));
  const search = el('div', 'jewel-search');
  search.innerHTML = `${Icons.icon('search')}<input type="search" placeholder="Ask the intelligence…" aria-label="Search the intelligence">`;
  const input = search.querySelector('input');
  input.addEventListener('keydown', e => {
    if (e.key === 'Enter' && input.value.trim()) {
      const res = R.search(input.value.trim());
      toast(res.message, room.accent);
    }
  });
  const chip = el('div', 'identity-chip',
    `<span class="avatar" role="img" aria-label="Your avatar"></span><span>Shawn</span>`);
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

  shell.append(rail, top, main);
  return shell;

  function roomDesc(id) {
    return {
      feed: 'One stream of everything the collective intelligence wants you to see — newest understanding first.',
      today: 'Your day, answered by the intelligence. What matters, what changed, what deserves you.',
      notes: 'Capture anything. Naya distills it, connects it, and keeps it retrievable — never a black hole.',
      reports: 'Proof, not promises. Every report carries its evidence and its receipts.',
      library: 'Everything retained, organized by what it means — not where it happened to land.',
      connect: 'One brain. Many doors. Choose how you — or your agents, apps, and systems — step into the same intelligence.',
      ledger: 'Every contribution, valued. The accountability layer of the collective mind.',
      connections: 'Humans, AIs, and machines you share intelligence with — each on your terms.',
      lists: 'Living lists that stay current because the intelligence behind them does.',
      mail: 'Your messages, understood — triaged by meaning, not just recency.',
      spaces: 'Rooms inside the Hub for projects, people, and ideas that belong together.',
      settings: 'Your Hub, your rules. Identity, privacy, doors, and preferences.',
      system: 'The Hub knows itself — its spec, its scorecard, its roadmap, live in the open.',
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
        onClick: () => window.NayaRouter.navigate('/hub/system'),
      }],
    });
  }
}
window.HubView = HubView;
