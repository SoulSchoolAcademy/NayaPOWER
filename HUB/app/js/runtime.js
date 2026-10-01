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

  // ——— The Smart Doors. One brain. Many doors. ———
  // Source of truth: BRAIN/10-INTERFACES/0002-SMART-DOOR-REGISTRY-V1.json
  // (canonical registry). This array mirrors it; `registry` carries the
  // registry's own state so the Hub never invents door liveness.
  // status: live | contract   (contract = REGISTERED_CONTRACT_ONLY)
  const DOORS = [
    { id: 'browser', name: 'Browser / Web Hub', for: 'Humans — the Hub itself is a door',
      desc: 'You are here. The Hub is the human door into the same intelligence every other door reaches.',
      accent: '#e8c766', icon: 'browser', status: 'live', priority: 0,
      registry: 'SESSION_DOOR' },
    { id: 'ai', name: 'AI Connect', for: 'Reasoning over retained intelligence',
      desc: 'Model inference over what Naya retains — the registry marks this door live and bounded.',
      accent: '#9d75ff', icon: 'spark', status: 'live', priority: 1,
      registry: 'LIVE_BOUNDED_EXISTING_CAPABILITY' },
    { id: 'data', name: 'Supabase / Data Connect', for: 'The governed data substrate',
      desc: 'Reads and writes against the data layer pass through governance. Live and bounded, per the registry.',
      accent: '#55e39a', icon: 'db', status: 'live', priority: 2,
      registry: 'LIVE_BOUNDED' },
    { id: 'github', name: 'GitHub Connect', for: 'Coding & repository agents',
      desc: 'The governed channel for repository work — code, issues, pull requests. Writes are consequential: LAW decides, VERIFY checks.',
      accent: '#55b9ee', icon: 'github', status: 'contract', priority: 3,
      registry: 'REGISTERED_CONTRACT_ONLY' },
    { id: 'mcp', name: 'MCP Connect', for: 'AI agents → provider tools',
      desc: 'Any MCP-capable agent reaches provider tools through one governed door. Invocation is consequential and receipted.',
      accent: '#d86cff', icon: 'mcp', status: 'contract', priority: 4,
      registry: 'REGISTERED_CONTRACT_ONLY' },
    { id: 'naya', name: 'Naya-to-Naya Connect', for: 'Seat ↔ seat collaboration',
      desc: 'Nayas reach each other through governed doors — shared context, receipts on every crossing.',
      accent: '#b8ee57', icon: 'a2a', status: 'contract', priority: 5,
      registry: 'REGISTERED_CONTRACT_ONLY' },
    { id: 'email', name: 'Email Connect', for: 'Human & network communication',
      desc: 'Reach NayaPOWER through email adapters. The intelligence meets people where they already are.',
      accent: '#ff9a5a', icon: 'mail', status: 'contract', priority: 6,
      registry: 'REGISTERED_CONTRACT_ONLY' },
    { id: 'calendar', name: 'Calendar Connect', for: 'Schedules & time',
      desc: 'Calendars connect as a governed door — time becomes something the intelligence can reason about.',
      accent: '#f1d75a', icon: 'cal', status: 'contract', priority: 7,
      registry: 'REGISTERED_CONTRACT_ONLY' },
    { id: 'voice', name: 'Voice Connect', for: 'Spoken interaction',
      desc: 'Voice in and voice out, through the same governed intelligence.',
      accent: '#ff5e6c', icon: 'mic', status: 'contract', priority: 8,
      registry: 'REGISTERED_CONTRACT_ONLY' },
    { id: 'web', name: 'Web Connect', for: 'The open web, governed',
      desc: 'Web sources and actions through one door — retrieval with provenance, never silent browsing.',
      accent: '#6675ff', icon: 'connect', status: 'contract', priority: 9,
      registry: 'REGISTERED_CONTRACT_ONLY' },
  ];

  // Future door ideas with working agreements forming — NOT in the canonical
  // registry. Shown on the roadmap, never as live or contracted doors.
  const DOOR_ROADMAP = [
    { name: 'REST / OpenAPI', desc: 'A clean HTTP API for applications and agents that speak REST.' },
    { name: 'Webhooks',      desc: 'External systems push events in — intelligence reacts instead of waiting to be asked.' },
    { name: 'SDK',           desc: 'Embed the intelligence inside your own product.' },
    { name: 'Agent-to-Agent protocol', desc: 'A standing protocol for agent ↔ agent collaboration.' },
    { name: 'Enterprise Identity',      desc: 'Organization-level identity and authorization boundaries.' },
    { name: 'Private MCP Tunnel',      desc: 'On-prem agent access that never touches the public internet.' },
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
    // 'contract' doors: the canonical registry holds the contract, but the
    // door is not live. We say exactly that instead of faking a handshake.
    return {
      ok: false,
      message: `${door.name}: contract registered (${door.registry}), not live yet. Connection never silently creates permission — this door lights up when the runtime opens it. Nothing was faked.`,
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
    ROOMS, DOORS, DOOR_ROADMAP, stateFor, NOT_VERIFIED_COPY,
    connectDoor, search, captureNote, draftNotes,
    version: '1.0.0',
    doorRegistryRef: 'BRAIN/10-INTERFACES/0002-SMART-DOOR-REGISTRY-V1.json',
  };
})();

window.NayaRuntime = Runtime;
