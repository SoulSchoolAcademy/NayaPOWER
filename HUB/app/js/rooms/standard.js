/* STANDARD ROOMS — the honest renderer for every room whose
   governed backend isn't connected yet. One shared path, so no room
   can ever drift into faking data. */

(function () {
  const HONEST = {
    feed:        { icon: 'feed',    title: 'The stream is quiet — honestly',
                   body: 'The Smart Feed will show the freshest collective understanding here. Until the runtime connects, there is no stream to show — and this room will not invent one.' },
    today:       { icon: 'spark',   title: 'Today, unanswered — for now',
                   body: 'Your Intelligence Today will answer from real data: what matters, what changed, what deserves you. The answering engine is still being connected.' },
    reports:     { icon: 'report',  title: 'No reports yet',
                   body: 'Reports carry proof, not promises. When the verification layer connects, your reports will appear here with their evidence attached.' },
    library:     { icon: 'library', title: 'The shelves are empty — truthfully',
                   body: 'The Intelligent Library will hold everything retained, organized by meaning. Nothing is retained yet, so nothing is shown.' },
    ledger:      { icon: 'ledger',  title: 'The ledger opens with the first contribution',
                   body: 'The Smart Ledger values every contribution to the collective mind. The valuation layer connects with the governed runtime.' },
    connections: { icon: 'nodes',   title: 'No connections yet',
                   body: 'Humans, AIs, and machines you share intelligence with will live here — each on your terms, each with consent recorded.' },
    lists:       { icon: 'lists',   title: 'No lists yet',
                   body: 'Smart Lists stay current because the intelligence behind them does. Create your first list the day the runtime connects.' },
    mail:        { icon: 'mail',    title: 'The mailbox is honest, too',
                   body: 'Smart Mail triages by meaning, not recency. The messaging door opens with the runtime — until then, no pretend inbox.' },
    spaces:      { icon: 'spaces',  title: 'No spaces yet',
                   body: 'Spaces are rooms inside the Hub for projects, people, and ideas that belong together. They open with the runtime.' },
    settings:    { icon: 'gear',   title: 'Settings, minimal and true',
                   body: 'Identity, privacy, and door preferences live here. Today the only true settings are the ones this device can keep — everything governed arrives with the runtime.' },
  };

  function standardRoom(id) {
    return function () {
      const { el, StatePanel } = window.NayaUI;
      const R = window.NayaRuntime;
      const room = R.ROOMS.find(r => r.id === id);
      const h = HONEST[id] || HONEST.feed;
      const wrap = el('div');
      const c = R.NOT_VERIFIED_COPY;
      wrap.appendChild(StatePanel({
        accent: room.accent, icon: 'lock',
        title: c.title, body: c.body,
        actions: [
          { label: 'What this room becomes', icon: h.icon, onClick: () => showVision(wrap, room, h) },
          { label: 'How it connects', icon: 'core', ghost: true, onClick: () => window.NayaRouter.navigate('/hub/settings') },
        ],
      }));
      return wrap;
    };
  }

  function showVision(wrap, room, h) {
    const { el, Board } = window.NayaUI;
    wrap.innerHTML = '';
    const b = Board({ accent: room.accent, icon: h.icon, title: h.title, sub: 'What this room becomes', lift: false });
    b.body.innerHTML = `<p style="color:var(--ink-dim);font-size:14px;max-width:600px">${h.body}</p>`;
    wrap.appendChild(b);
  }

  window.NayaRooms = window.NayaRooms || {};
  Object.keys(HONEST).forEach(id => { window.NayaRooms[id] = standardRoom(id); });
})();
