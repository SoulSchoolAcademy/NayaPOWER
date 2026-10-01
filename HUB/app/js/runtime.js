/* ═══════════════════════════════════════════════════════════════════
   RUNTIME — the Hub ↔ intelligence boundary.
   The Hub never touches storage directly. Every room asks the runtime
   for its honest state; the runtime never invents data.
   ═══════════════════════════════════════════════════════════════════ */

const Runtime = (() => {
  // ——— The twelve rooms ———
  const ROOMS = [
    { id: 'feed',        name: 'Smart Feed',          kicker: 'STREAM',       accent: 'var(--accent-feed)',        icon: 'feed' },
    { id: 'today',       name: 'Your Intelligence Today', kicker: 'TODAY',    accent: 'var(--accent-today)',       icon: 'spark' },
    { id: 'notes',       name: 'Smart Notes',         kicker: 'CAPTURE',      accent: 'var(--accent-notes)',       icon: 'note' },
    { id: 'reports',     name: 'Your Reports',        kicker: 'REPORTS',      accent: 'var(--accent-reports)',     icon: 'report' },
    { id: 'library',     name: 'Intelligent Library', kicker: 'LIBRARY',      accent: 'var(--accent-library)',     icon: 'library' },
    { id: 'connect',     name: 'Smart Connect',       kicker: 'CONNECT',      accent: 'var(--accent-connect)',     icon: 'connect' },
    { id: 'ledger',      name: 'Smart Ledger',        kicker: 'ACCOUNTABILITY', accent: 'var(--accent-ledger)',     icon: 'ledger' },
    { id: 'connections', name: 'Your Connections',    kicker: 'CONNECTIONS',  accent: 'var(--accent-connections)', icon: 'nodes' },
    { id: 'lists',       name: 'Smart Lists',         kicker: 'LISTS',        accent: 'var(--accent-lists)',       icon: 'lists' },
    { id: 'mail',        name: 'Smart Mail',          kicker: 'MAIL',         accent: 'var(--accent-mail)',         icon: 'mail' },
    { id: 'spaces',      name: 'Smart Spaces',        kicker: 'SPACES',       accent: 'var(--accent-spaces)',      icon: 'spaces' },
    { id: 'settings',    name: 'Settings',            kicker: 'SETTINGS',     accent: 'var(--accent-settings)',    icon: 'gear' },
    { id: 'system',      name: 'System',              kicker: 'THE HUB KNOWS ITSELF', accent: 'var(--accent-system)', icon: 'core' },
  ];

  // ——— The ten Smart Doors. One brain. Many doors. ———
  // status: live | ready | soon | specialized
  const DOORS = [
    { id: 'mcp',        name: 'MCP',               for: 'AI agents → NayaPOWER tools & context',
      desc: 'Any MCP-capable agent connects, authorizes, and NayaPOWER tools appear inside its own context. The server enforces identity, scopes, and authorization on every request.',
      accent: '#d86cff', icon: 'mcp',     status: 'ready', priority: 1 },
    { id: 'rest',       name: 'REST / OpenAPI',    for: 'Apps & agents → NayaPOWER',
      desc: 'A clean HTTP API for applications and agents that speak REST. Same governance, same intelligence, no special SDK required.',
      accent: '#6675ff', icon: 'api',     status: 'ready', priority: 2 },
    { id: 'github',     name: 'GitHub App',        for: 'Coding & repository agents',
      desc: 'The NayaPOWER GitHub App — coding agents work with the repository and the intelligence together, under governed permissions.',
      accent: '#55b9ee', icon: 'github',  status: 'ready', priority: 3 },
    { id: 'webhooks',   name: 'Webhooks',          for: 'System → NayaPOWER events',
      desc: 'External systems push events into NayaPOWER. Intelligence reacts to the world instead of waiting to be asked.',
      accent: '#9d75ff', icon: 'webhook', status: 'ready', priority: 4 },
    { id: 'sdk',        name: 'SDK',               for: 'Developers embed NayaPOWER',
      desc: 'Embed the intelligence inside your own product. Your app, NayaPOWER\'s memory and judgment underneath.',
      accent: '#55e39a', icon: 'sdk',     status: 'ready', priority: 5 },
    { id: 'a2a',        name: 'Agent to Agent',     for: 'Agent ↔ agent collaboration',
      desc: 'AI agents connect to each other through NayaPOWER — shared context, governed handoffs, collective work.',
      accent: '#b8ee57', icon: 'a2a',     status: 'ready', priority: 6 },
    { id: 'browser',    name: 'Browser / Web Hub', for: 'Humans — the Hub itself is a door',
      desc: 'You are here. The Hub is the human door into the same intelligence every other door reaches.',
      accent: '#f1d75a', icon: 'browser', status: 'live' },
    { id: 'messaging',  name: 'Email / Messaging', for: 'Human & network communication',
      desc: 'Reach NayaPOWER through email and messaging adapters. The intelligence meets people where they already are.',
      accent: '#ff9a5a', icon: 'mail',    status: 'ready' },
    { id: 'enterprise', name: 'Enterprise Identity', for: 'Organization-level authorization',
      desc: 'Organizations connect with their own identity and authorization boundaries. Collective intelligence with corporate-grade control.',
      accent: '#aaa4b1', icon: 'shield',  status: 'soon' },
    { id: 'tunnel',     name: 'Private MCP Tunnel', for: 'Private / on-prem agent access',
      desc: 'A private tunnel for agents that must never touch the public internet. Same doors, your own walls.',
      accent: '#e8c766', icon: 'tunnel',  status: 'specialized' },
  ];

  // ——— Honest state per room.
  // loading | ready | empty | not_verified | blocked | error
  // Nothing is 'ready' with data until the governed runtime is connected.
  function stateFor(roomId) {
    if (roomId === 'connect' || roomId === 'system') return 'ready';
    return 'not_verified';
  }

  const NOT_VERIFIED_COPY = {
    title: 'Not connected to the governed runtime yet',
    body: 'This room is honest about what it cannot show. The intelligence substrate (persistence + nine-node kernel) is still being brought live. When it connects, this room fills with real data — never sample data, never pretend activity.',
  };

  // ——— Actions. Every one is honest about what it can do today. ———
  function connectDoor(doorId) {
    const door = DOORS.find(d => d.id === doorId);
    if (!door) return { ok: false, message: 'Unknown door.' };
    if (door.status === 'live') {
      return { ok: true, message: `${door.name} is already live — you are using it.` };
    }
    if (door.status === 'soon' || door.status === 'specialized') {
      return { ok: false, message: `${door.name} is ${door.status === 'soon' ? 'on the roadmap' : 'a specialized door'} — not connectable from this Hub yet.` };
    }
    // 'ready' doors: the handshake begins, but the backend isn't live —
    // so we say exactly that instead of faking a connection.
    return {
      ok: false,
      message: `${door.name} handshake prepared. The governed endpoint isn't live yet — this door will light up the moment the runtime connects. Nothing was faked.`,
    };
  }

  function search(query) {
    return {
      ok: false,
      state: 'not_verified',
      message: 'Search will query the canonical intelligence substrate. The substrate connection is pending — results arrive when it lands, with provenance attached.',
    };
  }

  function captureNote(text) {
    const kept = (text || '').trim();
    if (!kept) return { ok: false, message: 'Write something first — empty notes are not kept.' };
    try {
      const notes = JSON.parse(localStorage.getItem('nayanet.draftNotes') || '[]');
      notes.unshift({ text: kept, at: new Date().toISOString(), state: 'LOCAL_DRAFT' });
      localStorage.setItem('nayanet.draftNotes', JSON.stringify(notes));
      return {
        ok: true, local: true,
        message: 'Kept as a local draft. It will flow through the governed capture pipeline the moment the runtime connects — nothing stored only in the browser is ever treated as canonical.',
      };
    } catch {
      return { ok: false, message: 'Could not keep the draft on this device.' };
    }
  }

  function draftNotes() {
    try { return JSON.parse(localStorage.getItem('nayanet.draftNotes') || '[]'); }
    catch { return []; }
  }

  return {
    ROOMS, DOORS, stateFor, NOT_VERIFIED_COPY,
    connectDoor, search, captureNote, draftNotes,
    version: '1.0.0',
    specRef: 'HUB/app/SPEC.md',
  };
})();

window.NayaRuntime = Runtime;
