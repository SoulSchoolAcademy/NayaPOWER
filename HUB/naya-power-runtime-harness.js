/* ============================================================================
 * naya-power-runtime-harness.js — conformance harness for HUB/naya-power-runtime.js
 * Covers the smartFeed() accessor's graded fallback (build request 6219408880):
 *   L0 ready   — live fetch validates -> {ok:true, state:'ready'}
 *   L0 invalid — wrong room in file -> fails closed to L1/L2
 *   L1 cached  — fetch down + warm localStorage -> {ok:true, state:'cached'}
 *                with _feed_meta.age_seconds visible
 *   L2 empty   — fetch down + cold cache -> {ok:true, state:'empty'}
 *   never throws — every level failing still resolves
 *   write-through — L0 success populates localStorage for L1
 *
 * Run: node HUB/naya-power-runtime-harness.js   (exit 0 = all green)
 * ========================================================================== */
"use strict";

var failures = 0;
function check(name, cond, detail) {
  if (cond) {
    console.log("  PASS " + name);
  } else {
    failures += 1;
    console.log("  FAIL " + name + (detail ? " — " + detail : ""));
  }
}

// ---- Minimal browser stubs ------------------------------------------------
function makeLocalStorage() {
  var store = {};
  return {
    getItem: function (k) { return Object.prototype.hasOwnProperty.call(store, k) ? store[k] : null; },
    setItem: function (k, v) { store[k] = String(v); },
    removeItem: function (k) { delete store[k]; },
    clear: function () { store = {}; },
    _dump: function () { return store; }
  };
}

var FEED_DOC = {
  contract: "room-feed/v1",
  room: "feed",
  emitted_at: "2026-10-16T10:00:00-07:00",
  source_ref: "test",
  items: [{ id: "note-IB-1", title: "T", topics: ["G"], kind: "note", layers: [] }]
};

function fetchOk() {
  return Promise.resolve({ ok: true, json: function () { return Promise.resolve(JSON.parse(JSON.stringify(FEED_DOC))); } });
}
function fetchWrongRoom() {
  var bad = JSON.parse(JSON.stringify(FEED_DOC)); bad.room = "today";
  return Promise.resolve({ ok: true, json: function () { return Promise.resolve(bad); } });
}
function fetchDown() {
  return Promise.reject(new Error("network down"));
}
function fetchHttp500() {
  return Promise.resolve({ ok: false, status: 500, json: function () { return Promise.reject(new Error("no body")); } });
}

function loadRuntime(opts) {
  opts = opts || {};
  delete require.cache[require.resolve("./naya-power-runtime.js")];
  global.localStorage = opts.storage || makeLocalStorage();
  global.fetch = opts.fetch || fetchDown;
  global.window = {};
  var rt = require("./naya-power-runtime.js");
  delete global.window;
  return rt;
}

async function main() {
  console.log("naya-power-runtime harness — smartFeed() graded fallback");

  // 1. L0 ready
  var rt = loadRuntime({ fetch: fetchOk });
  var r = await rt.smartFeed();
  check("L0 ready: ok:true", r.ok === true, JSON.stringify(r).slice(0, 120));
  check("L0 ready: state 'ready'", r.state === "ready", r.state);
  check("L0 ready: items served", r.data && r.data.items && r.data.items.length === 1);
  check("L0 ready: room handshake", r.data && r.data.room === "feed");

  // 2. Write-through: L0 success warms L1
  var stored = JSON.parse(global.localStorage.getItem("nayanet.feed.feed.v1"));
  check("write-through: L1 populated", !!stored && stored.data && stored.data.room === "feed",
    "key nayanet.feed.feed.v1");

  // 3. L1 cached (fetch down, warm cache)
  rt = loadRuntime({ fetch: fetchDown, storage: global.localStorage });
  r = await rt.smartFeed();
  check("L1 cached: ok:true", r.ok === true);
  check("L1 cached: state 'cached'", r.state === "cached", r.state);
  check("L1 cached: items served", r.data && r.data.items && r.data.items.length === 1);
  check("L1 cached: age_seconds visible",
    r.data && r.data._feed_meta && typeof r.data._feed_meta.age_seconds === "number",
    JSON.stringify(r.data && r.data._feed_meta));

  // 4. L2 empty (fetch down, cold cache)
  rt = loadRuntime({ fetch: fetchDown, storage: makeLocalStorage() });
  r = await rt.smartFeed();
  check("L2 empty: ok:true", r.ok === true);
  check("L2 empty: state 'empty'", r.state === "empty", r.state);
  check("L2 empty: valid envelope", r.data && r.data.contract === "room-feed/v1"
    && r.data.room === "feed" && Array.isArray(r.data.items));

  // 5. L0 invalid file (wrong room) fails closed -> L1 (cold here -> L2)
  rt = loadRuntime({ fetch: fetchWrongRoom, storage: makeLocalStorage() });
  r = await rt.smartFeed();
  check("wrong-room file: fails closed (not ready)", r.state !== "ready", r.state);
  check("wrong-room file: lands on empty", r.state === "empty", r.state);

  // 6. HTTP 500 fails closed -> L2
  rt = loadRuntime({ fetch: fetchHttp500, storage: makeLocalStorage() });
  r = await rt.smartFeed();
  check("HTTP 500: fails closed to empty", r.ok === true && r.state === "empty",
    r.state);

  // 7. Never throws: sabotage everything (no fetch, no localStorage)
  delete require.cache[require.resolve("./naya-power-runtime.js")];
  global.localStorage = undefined;
  global.fetch = undefined;
  global.window = {};
  rt = require("./naya-power-runtime.js");
  delete global.window;
  var threw = false, res = null;
  try { res = await rt.smartFeed(); } catch (e) { threw = true; }
  check("never throws", threw === false && res && res.ok === true, threw ? "threw" : res && res.state);

  // 8. ROOM_FEED maps feed -> smart-feed (not feed.json)
  rt = loadRuntime({ fetch: fetchDown });
  check("ROOM_FEED['feed'] === 'smart-feed'", rt.ROOM_FEED.feed === "smart-feed",
    JSON.stringify(rt.ROOM_FEED));

  // 9. validateEnvelope unit checks
  check("validateEnvelope accepts good doc", rt.validateEnvelope("feed", FEED_DOC) === true);
  var badContract = JSON.parse(JSON.stringify(FEED_DOC)); badContract.contract = "x";
  check("validateEnvelope rejects bad contract", rt.validateEnvelope("feed", badContract) === false);
  check("validateEnvelope rejects null", rt.validateEnvelope("feed", null) === false);

  // 10. withMeta shape
  var m = rt.withMeta(true, "ready", { a: 1 }, { age_seconds: 5 });
  check("withMeta shape {ok,state,data}", m.ok === true && m.state === "ready" && m.data.a === 1);
  check("withMeta meta visible", m.data._feed_meta && m.data._feed_meta.age_seconds === 5);

  console.log(failures === 0 ? "\nALL GREEN" : "\n" + failures + " FAILURES");
  process.exit(failures === 0 ? 0 : 1);
}

main().catch(function (e) {
  console.log("HARNESS CRASHED: " + (e && e.stack || e));
  process.exit(2);
});
