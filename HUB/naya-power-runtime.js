/* naya-power-runtime.js — window.NayaPowerRuntime (Seam C implementation, tick t0480)
 *
 * The runtime bridge object the hub's per-room accessor map resolves against.
 * Discovered live in the hub (index-8.html, js/runtime-live.js @ baf1221d9):
 *   bridge() tries [window.NayaAssistantRuntime, window.NayaPowerRuntime,
 *                   window.NayaRuntimeBridge] and invoke() calls the first
 *   METHOD_MAP candidate that is a function on the bridge, passing (payload),
 *   then normalizes: {ok:true, state: out?.state||'ready', data: out?.data ?? out}.
 *
 * Accessor map re-derived from the live bytes (molded to the rooms, not the reverse):
 *   feed:['smartFeed']
 *   today:['intelligenceToday','dailyIntelligence','today']
 *   reports:['smartReports','reports','intelligenceReports']
 *   library:['intelligentLibrary','library','knowledgeLibrary']
 *   ledger:['smartLedger','ledger','executionLedger']
 *   connections:['smartConnections','connections','relationshipIntelligence']
 *   lists:['smartLists','lists','intelligenceLists']
 *   mail:['smartMail','mail','messages']
 *   spaces:['smartSpaces','spaces','contextSpaces']
 *   settings:['settingsSnapshot','runtimeSnapshot']
 *   search:['searchIntelligence','askNaya','search','retrieveIntelligence']
 *   retrieve:['retrieveIntelligentBlock','getIntelligentBlock','retrieve']
 *   identity: bridge.identity | bridge.currentIdentity | bridge.sessionIdentity
 *
 * Transport (room-feed contract §1): fetch(FEED_URL,{cache:'no-store'}) →
 * validate the room-feed/v1 handshake → on ANY failure graded fallback:
 *   L0 fresh fetch → L1 last-good snapshot in localStorage ('nayanet.<room>.feed.v1',
 *   write-through on success) → L2 an empty-but-valid envelope.
 * Never throws; staleness is visible via _feed_meta on every returned object.
 *
 * NOTES (honest limits):
 * - smartFeed() does NOT hijack the Smart Feed's proven markdown wire; it returns
 *   a not_verified signal so the room keeps its own transport.
 * - Rooms without emitted feeds yet (reports, library, ledger, mail, connections,
 *   settings) correctly degrade to L1/L2 until the emitters land (t0479 merged
 *   only today/lists/spaces).
 */
(function (global) {
  'use strict';

  var VERSION = '1.0.0-t0480';
  var CONTRACT = 'room-feed/v1';
  var FEED_BASE = global.__NPR_FEED_BASE__ ||
    'https://raw.githubusercontent.com/SoulSchoolAcademy/NayaPOWER/main/HUB/FEEDS/';
  var L1_PREFIX = 'nayanet.';

  // room -> feed filename. 'feed' intentionally absent (see note above).
  var ROOM_FEED = {
    today: 'today', lists: 'lists', spaces: 'spaces',
    reports: 'reports', library: 'library', ledger: 'ledger',
    mail: 'mail', connections: 'connections', settings: 'settings',
  };

  function nowIso() { return new Date().toISOString(); }

  function l1Key(room) { return L1_PREFIX + room + '.feed.v1'; }

  function l1Get(room) {
    try {
      var ls = global.localStorage;
      if (!ls) return null;
      var raw = ls.getItem(l1Key(room));
      return raw ? JSON.parse(raw) : null;
    } catch (e) { return null; }
  }

  function l1Set(room, envelope) {
    try {
      var ls = global.localStorage;
      if (ls) ls.setItem(l1Key(room), JSON.stringify(envelope));
    } catch (e) { /* write-through is best-effort */ }
  }

  function ageSeconds(emittedAt) {
    if (!emittedAt) return null;
    var t = Date.parse(emittedAt);
    if (isNaN(t)) return null;
    return Math.max(0, Math.round((Date.now() - t) / 1000));
  }

  // Room-feed/v1 envelope handshake (mirrors the contract's receiver validator).
  function validateEnvelope(room, data) {
    if (data == null || typeof data !== 'object') throw new Error('feed body is not an object');
    if (data.contract !== CONTRACT) throw new Error('contract mismatch: ' + String(data.contract));
    if (data.room !== room) throw new Error('room mismatch: ' + String(data.room));
    if (!Array.isArray(data.items)) throw new Error('items is not an array');
    for (var i = 0; i < data.items.length; i++) {
      var it = data.items[i];
      if (!it || typeof it.id !== 'string' || it.id === '') throw new Error('item ' + i + ' missing id');
      if (typeof it.title !== 'string') throw new Error('item ' + it.id + ' missing title');
      if (!Array.isArray(it.topics) || it.topics.length < 1) throw new Error('item ' + it.id + ' topics < 1');
      if (typeof it.kind !== 'string' || it.kind === '') throw new Error('item ' + it.id + ' missing kind');
    }
    return data;
  }

  function withMeta(envelope, source) {
    return {
      ok: true,
      state: source === 'live' ? 'ready' : (source === 'cache' ? 'cached' : 'empty'),
      data: {
        contract: envelope.contract,
        room: envelope.room,
        emitted_at: envelope.emitted_at,
        source_ref: envelope.source_ref,
        items: envelope.items,
        _feed_meta: {
          source: source,
          age_seconds: ageSeconds(envelope.emitted_at),
          emitted_at: envelope.emitted_at || null,
          bridge_version: VERSION,
        },
      },
    };
  }

  function emptyEnvelope(room) {
    return { contract: CONTRACT, room: room, emitted_at: null, source_ref: null, items: [] };
  }

  async function loadRoom(room) {
    var filename = ROOM_FEED[room];
    if (!filename) {
      return { ok: false, state: 'not_verified', message: 'no feed mapped for room "' + room + '"' };
    }
    // L0 — live fetch.
    try {
      var res = await global.fetch(FEED_BASE + filename + '.json', { cache: 'no-store' });
      if (!res.ok) throw new Error('HTTP ' + res.status);
      var data = validateEnvelope(room, await res.json());
      l1Set(room, data);
      return withMeta(data, 'live');
    } catch (e) { /* fall through to L1 */ }
    // L1 — last-good snapshot from device-local localStorage.
    try {
      var cached = l1Get(room);
      if (cached) return withMeta(validateEnvelope(room, cached), 'cache');
    } catch (e) { /* fall through to L2 */ }
    // L2 — empty-but-valid envelope. Never blank, never throw.
    return withMeta(emptyEnvelope(room), 'empty');
  }

  function roomAccessor(room) {
    return function (payload) { return loadRoom(room); };
  }

  var Runtime = {
    version: VERSION,

    // ---- METHOD_MAP-preferred names (what the live adapters actually call) ----
    smartFeed: function () {
      // The Smart Feed keeps its own proven markdown transport — do not touch it.
      return Promise.resolve({
        ok: false, state: 'not_verified',
        message: 'Smart Feed reads the canonical markdown wire; this bridge does not own it.',
        runtime_connected: true,
      });
    },
    intelligenceToday: roomAccessor('today'),
    dailyIntelligence: roomAccessor('today'),
    smartReports: roomAccessor('reports'),
    intelligenceReports: roomAccessor('reports'),
    intelligentLibrary: roomAccessor('library'),
    knowledgeLibrary: roomAccessor('library'),
    smartLedger: roomAccessor('ledger'),
    executionLedger: roomAccessor('ledger'),
    smartConnections: roomAccessor('connections'),
    relationshipIntelligence: roomAccessor('connections'),
    smartLists: roomAccessor('lists'),
    intelligenceLists: roomAccessor('lists'),
    smartMail: roomAccessor('mail'),
    messages: roomAccessor('mail'),
    smartSpaces: roomAccessor('spaces'),
    contextSpaces: roomAccessor('spaces'),
    settingsSnapshot: roomAccessor('settings'),
    runtimeSnapshot: roomAccessor('settings'),

    // ---- brief's short names (aliases; the schematic's call shape) ----
    today: roomAccessor('today'),
    reports: roomAccessor('reports'),
    library: roomAccessor('library'),
    ledger: roomAccessor('ledger'),
    connections: roomAccessor('connections'),
    lists: roomAccessor('lists'),
    mail: roomAccessor('mail'),
    spaces: roomAccessor('spaces'),
    settings: roomAccessor('settings'),

    connect: function () {
      return Promise.resolve({
        ok: true, state: 'ready',
        data: {
          doors: [],
          roadmap: [],
          note: 'Door registry renders from the governed runtime (NayaRuntime.DOORS); this bridge feeds room data, not the registry.',
          _feed_meta: { source: 'static', age_seconds: 0, bridge_version: VERSION },
        },
      });
    },
    manifest: function () {
      return Promise.resolve({
        ok: true, state: 'ready',
        data: {
          contract: 'room-feed/v1', bridge_version: VERSION, feed_base: FEED_BASE,
          rooms: Object.keys(ROOM_FEED),
          _feed_meta: { source: 'static', age_seconds: 0, bridge_version: VERSION },
        },
      });
    },

    // ---- search / retrieve (adapter search candidates) ----
    searchIntelligence: function (payload) {
      return Promise.resolve({
        ok: false, state: 'not_verified',
        message: 'Intelligent search queries the canonical substrate; it is not wired through the feed bridge yet.',
        runtime_connected: true,
      });
    },
    askNaya: function (p) { return Runtime.searchIntelligence(p); },
    search: function (p) { return Runtime.searchIntelligence(p); },
    retrieveIntelligence: function (p) { return Runtime.searchIntelligence(p); },
    retrieveIntelligentBlock: function (payload) {
      var id = payload && payload.id;
      return Promise.resolve({
        ok: false, state: 'not_verified',
        message: 'Block retrieval is not wired through the feed bridge yet.',
        id: id || null, runtime_connected: true,
      });
    },
    getIntelligentBlock: function (p) { return Runtime.retrieveIntelligentBlock(p); },
    retrieve: function (p) { return Runtime.retrieveIntelligentBlock(p); },

    // ---- identity (adapter reads bridge.identity first) ----
    identity: { state: 'ready', display_name: 'You', detail: 'NayaPowerRuntime feed bridge ' + VERSION },
    currentIdentity: null,
    sessionIdentity: null,

    // ---- self-describing status (mirrors runtimeStatus shape) ----
    runtimeStatus: function () {
      var names = Object.keys(Runtime).filter(function (k) { return typeof Runtime[k] === 'function'; });
      return { connected: true, available_methods: names, bridge_version: VERSION };
    },
  };

  global.NayaPowerRuntime = Runtime;

  // Node/CommonJS export for the harness (does not affect the browser).
  if (typeof module !== 'undefined' && module.exports) module.exports = Runtime;
})(typeof window !== 'undefined' ? window : globalThis);
