/* ============================================================================
 * NayaPowerRuntime — the Hub's data bridge (Goal #1, Smart Feed loader)
 * ----------------------------------------------------------------------------
 * NOTES
 *   This is the bridge's room-feed accessor layer. The bridge owns all four
 *   room feeds — today, lists, spaces, feed — and serves each through the
 *   same graded-fallback machinery. There is no per-room refusal: smartFeed()
 *   serves the Smart Feed exactly like every other room.
 *
 *   Graded fallback (never throws):
 *     L0  live    — fetch(FEED_BASE + file, {cache:'no-store'}), validated
 *                   against the room-feed/v1 handshake. Write-through to L1.
 *     L1  cached  — last-good envelope from localStorage (per-room key).
 *     L2  empty   — empty-but-valid envelope. The honest "nothing yet" state.
 *
 *   Handshake (fail-closed): validateEnvelope(roomKey, data) requires
 *   data.contract === 'room-feed/v1' AND data.room === roomKey. A file that
 *   says anything else fails L0 closed into L1/L2 — which is correct behavior.
 *
 *   Room key -> file stem mapping lives in ROOM_FEED. The emitter writes
 *   smart-feed.json (not feed.json); the bridge maps room key 'feed' to it.
 * ========================================================================== */
(function (root, factory) {
  if (typeof module !== "undefined" && module.exports) {
    module.exports = factory();
  } else {
    root.NayaPowerRuntime = factory();
  }
}(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  var CONTRACT = "room-feed/v1";

  // Base URL for feed files. Override with window.NayaPowerFeedBase before
  // load (e.g. the CDN origin); defaults to the FEEDS/ sibling directory.
  var FEED_BASE = (function () {
    try {
      if (typeof window !== "undefined" && window.NayaPowerFeedBase) {
        return String(window.NayaPowerFeedBase);
      }
    } catch (e) { /* ignore */ }
    return "./FEEDS/";
  }());

  // Room key -> feed file stem (".json" appended at fetch time).
  var ROOM_FEED = {
    today: "today",
    lists: "lists",
    spaces: "spaces",
    feed: "smart-feed"
  };

  function storageKey(roomKey) {
    return "nayanet." + roomKey + ".feed.v1";
  }

  function validateEnvelope(roomKey, data) {
    if (!data || typeof data !== "object") return false;
    if (data.contract !== CONTRACT) return false;
    if (data.room !== roomKey) return false;
    if (!Array.isArray(data.items)) return false;
    return true;
  }

  function emptyEnvelope(roomKey) {
    return {
      contract: CONTRACT,
      room: roomKey,
      emitted_at: null,
      source_ref: "bridge:L2-empty",
      items: []
    };
  }

  // Canonical return shape: {ok, state, data}. Meta (e.g. cache age) rides
  // on data._feed_meta so it stays visible without changing the shape.
  function withMeta(ok, state, data, meta) {
    var out = { ok: !!ok, state: state, data: data || null };
    if (meta && out.data && typeof out.data === "object") {
      try { out.data._feed_meta = meta; } catch (e) { /* ignore */ }
    }
    return out;
  }

  function readCache(roomKey) {
    try {
      if (typeof localStorage === "undefined") return null;
      var raw = localStorage.getItem(storageKey(roomKey));
      if (!raw) return null;
      var parsed = JSON.parse(raw);
      if (!parsed || !validateEnvelope(roomKey, parsed.data)) return null;
      return parsed;
    } catch (e) {
      return null;
    }
  }

  function writeCache(roomKey, data) {
    try {
      if (typeof localStorage === "undefined") return;
      localStorage.setItem(storageKey(roomKey), JSON.stringify({
        saved_at: new Date().toISOString(),
        data: data
      }));
    } catch (e) { /* quota or privacy mode: L1 simply stays cold */ }
  }

  function cacheAgeSeconds(cached) {
    try {
      var then = Date.parse(cached.saved_at);
      if (isNaN(then)) return null;
      return Math.max(0, Math.round((Date.now() - then) / 1000));
    } catch (e) {
      return null;
    }
  }

  // The one accessor every room uses. Never throws: any failure at any
  // level falls through to the next, ending at the L2 empty envelope.
  function roomAccessor(roomKey) {
    var file = ROOM_FEED[roomKey];
    if (!file) {
      return Promise.resolve(withMeta(true, "empty", emptyEnvelope(roomKey)));
    }
    var url = FEED_BASE + file + ".json";
    return Promise.resolve()
      .then(function () {
        // L0 — live fetch, no-store so the 60-second proof sees fresh bytes.
        return fetch(url, { cache: "no-store" });
      })
      .then(function (resp) {
        if (!resp || !resp.ok) throw new Error("L0 bad response");
        return resp.json();
      })
      .then(function (data) {
        if (!validateEnvelope(roomKey, data)) throw new Error("L0 handshake failed");
        writeCache(roomKey, data); // write-through to L1
        return withMeta(true, "ready", data);
      })
      .catch(function () {
        // L1 — last-good from localStorage.
        var cached = readCache(roomKey);
        if (cached) {
          return withMeta(true, "cached", cached.data,
            { age_seconds: cacheAgeSeconds(cached) });
        }
        // L2 — empty-but-valid envelope. Never throws.
        return withMeta(true, "empty", emptyEnvelope(roomKey));
      });
  }

  // Public room accessors. smartFeed() is a first-class room: the bridge
  // owns the feed, so it resolves ready/cached/empty like every other room.
  function smartFeed() { return roomAccessor("feed"); }
  function todayFeed() { return roomAccessor("today"); }
  function listsFeed() { return roomAccessor("lists"); }
  function spacesFeed() { return roomAccessor("spaces"); }

  return {
    CONTRACT: CONTRACT,
    FEED_BASE: FEED_BASE,
    ROOM_FEED: ROOM_FEED,
    validateEnvelope: validateEnvelope,
    withMeta: withMeta,
    roomAccessor: roomAccessor,
    smartFeed: smartFeed,
    todayFeed: todayFeed,
    listsFeed: listsFeed,
    spacesFeed: spacesFeed,
    _storageKey: storageKey,
    _emptyEnvelope: emptyEnvelope
  };
}));
