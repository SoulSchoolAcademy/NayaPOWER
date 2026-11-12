/*
 * Tests for the notification-sound toggle (hub-notification-sounds-toggle-20261027).
 * Run: node --test HUB/app/js/test-notification-sound.cjs
 *
 * The toggle + sound live inline in HUB/app/index.html (the Settings room §6
 * board and the window.NayaNotif bar object — there is no separate rooms/
 * source file in the repo). These tests read that file, extract the real
 * NayaNotif object literal, and exercise it in a sandbox with stubbed
 * localStorage / AudioContext / document — no synthetic copy of the logic.
 */
"use strict";

const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const INDEX_HTML = path.join(__dirname, "..", "index.html");

function readIndex() {
  return fs.readFileSync(INDEX_HTML, "utf8");
}

/* Extract a brace-balanced object literal starting at the first `{` at or
 * after `from`. Skips braces inside strings, template literals and comments. */
function extractBraced(src, from) {
  const start = src.indexOf("{", from);
  assert.notEqual(start, -1, "no opening brace found");
  let depth = 0;
  let i = start;
  let quote = null;
  let escaped = false;
  let lineComment = false;
  let blockComment = false;
  for (; i < src.length; i++) {
    const ch = src[i];
    const next = src[i + 1] || "";
    if (lineComment) {
      if (ch === "\n") lineComment = false;
      continue;
    }
    if (blockComment) {
      if (ch === "*" && next === "/") {
        blockComment = false;
        i++;
      }
      continue;
    }
    if (quote) {
      if (escaped) {
        escaped = false;
      } else if (ch === "\\") {
        escaped = true;
      } else if (ch === quote) {
        quote = null;
      }
      continue;
    }
    if (ch === "/" && next === "/") {
      lineComment = true;
      continue;
    }
    if (ch === "/" && next === "*") {
      blockComment = true;
      continue;
    }
    if (ch === "'" || ch === '"' || ch === "`") {
      quote = ch;
      continue;
    }
    if (ch === "{") depth++;
    if (ch === "}") {
      depth--;
      if (depth === 0) return src.slice(start, i + 1);
    }
  }
  throw new Error("unbalanced braces in NayaNotif literal");
}

function makeStorage(init) {
  const m = new Map(Object.entries(init || {}));
  return {
    getItem: (k) => (m.has(k) ? m.get(k) : null),
    setItem: (k, v) => m.set(k, String(v)),
    removeItem: (k) => m.delete(k),
    _map: m,
  };
}

/* Fake WebAudio: records every oscillator + gain envelope, never sounds. */
function makeFakeAudio(state) {
  const contexts = [];
  class FakeParam {
    constructor() {
      this.calls = [];
    }
    setValueAtTime(v, t) {
      this.calls.push(["set", v, t]);
    }
    exponentialRampToValueAtTime(v, t) {
      this.calls.push(["ramp", v, t]);
    }
  }
  class FakeGain {
    constructor() {
      this.gain = new FakeParam();
    }
    connect() {}
  }
  class FakeOsc {
    constructor() {
      this.type = "";
      this.frequency = { value: 0 };
      this.started = null;
      this.stopped = null;
    }
    connect() {}
    start(t) {
      this.started = t;
    }
    stop(t) {
      this.stopped = t;
    }
  }
  class FakeAC {
    constructor() {
      this.state = state || "running";
      this.currentTime = 0;
      this.destination = {};
      this.resumed = false;
      this.oscs = [];
      this.gains = [];
      contexts.push(this);
    }
    resume() {
      this.resumed = true;
      if (this.state === "suspended") this.state = "running";
      return Promise.resolve();
    }
    createOscillator() {
      const o = new FakeOsc();
      this.oscs.push(o);
      return o;
    }
    createGain() {
      const g = new FakeGain();
      this.gains.push(g);
      return g;
    }
  }
  return { FakeAC, contexts };
}

function loadNotif(html, opts) {
  const o = opts || {};
  const marker = html.indexOf("window.NayaNotif = window.NayaNotif || {");
  assert.notEqual(marker, -1, "NayaNotif literal not found in index.html");
  const literal = extractBraced(html, marker);
  const audio = makeFakeAudio(o.audioState);
  const storage = makeStorage(o.storage);
  const sandbox = {
    localStorage: storage,
    window: { AudioContext: o.noAudio ? undefined : audio.FakeAC },
    document: { getElementById: () => null },
    console,
  };
  sandbox.window.window = sandbox.window;
  vm.createContext(sandbox);
  const notif = vm.runInContext("(" + literal + ")", sandbox);
  return { notif, storage, audio, sandbox };
}

function peakGain(gain) {
  return Math.max(...gain.gain.calls.map((c) => c[1]));
}

test("sound defaults OFF: no context, no oscillators", () => {
  const { notif, audio } = loadNotif(readIndex());
  assert.equal(notif.soundOn(), false);
  assert.equal(notif.playSound(), false);
  assert.equal(audio.contexts.length, 0);
});

test("sound ON plays exactly one calm chime: two sine notes, 880 + 659.25 Hz", () => {
  const { notif, audio } = loadNotif(readIndex(), {
    storage: { "nayanet.notif.sound": "1" },
  });
  assert.equal(notif.soundOn(), true);
  assert.equal(notif.playSound(), true);
  assert.equal(audio.contexts.length, 1);
  const ctx = audio.contexts[0];
  assert.equal(ctx.oscs.length, 2);
  assert.deepEqual(
    ctx.oscs.map((o) => o.type),
    ["sine", "sine"]
  );
  assert.deepEqual(
    ctx.oscs.map((o) => o.frequency.value),
    [880, 659.25]
  );
  assert.deepEqual(
    ctx.oscs.map((o) => o.started),
    [0, 0.18]
  );
  // Gentle: peak gain 0.12, fades to silence — never a blast.
  assert.deepEqual(
    ctx.gains.map((g) => peakGain(g)),
    [0.12, 0.12]
  );
  assert.ok(ctx.gains.every((g) => g.gain.calls.some((c) => c[0] === "ramp" && c[1] === 0.0001)));
});

test("arrival fires the sound; same count, clear, and non-channel sets stay silent", () => {
  const { notif, audio } = loadNotif(readIndex(), {
    storage: { "nayanet.notif.sound": "1", "nayanet.notif.mail": "2" },
  });
  notif.bump("mail"); // 2 -> 3: a new notification arrives
  assert.equal(audio.contexts[0].oscs.length, 2);
  const before = audio.contexts[0].oscs.length;
  notif.set("mail", 3); // same count: no new arrival
  notif.set("mail", 0); // cleared by tapping the bar: not an arrival
  notif.set("seen.activity", 5); // bookkeeping key, not a channel
  assert.equal(audio.contexts[0].oscs.length, before);
});

test("sound OFF: an arrival stays silent", () => {
  const { notif, audio } = loadNotif(readIndex(), {
    storage: { "nayanet.notif.mail": "0" },
  });
  assert.equal(notif.soundOn(), false);
  notif.bump("mail");
  assert.equal(audio.contexts.length, 0);
});

test("no AudioContext: playSound fails soft, never throws", () => {
  const { notif } = loadNotif(readIndex(), {
    storage: { "nayanet.notif.sound": "1" },
    noAudio: true,
  });
  assert.equal(notif.playSound(), false);
});

test("suspended AudioContext: resume is attempted, no throw", () => {
  const { notif, audio } = loadNotif(readIndex(), {
    storage: { "nayanet.notif.sound": "1" },
    audioState: "suspended",
  });
  assert.equal(notif.playSound(), true);
  assert.equal(audio.contexts[0].resumed, true);
});

test("settings toggle wiring is present in the Notifications board", () => {
  const html = readIndex();
  // Pref key + OFF default, read through the same pref()/setPref() helpers
  // the channel rows use.
  assert.ok(html.includes("pref('nayanet.notif.sound','0')"), "toggle reads pref with OFF default");
  assert.ok(html.includes("setPref('nayanet.notif.sound'"), "toggle writes the pref");
  assert.ok(html.includes("Notification sound"), "toggle label present");
  assert.ok(html.includes("One calm chime when a new notification arrives"), "toggle subline present");
  // Same segmented On/Off control as the channel rows.
  assert.ok(
    html.includes("seg([{label:'On',value:'1'},{label:'Off',value:'0'}],sndOn?'1':'0'"),
    "toggle uses the shared seg On/Off control"
  );
  // Turning it ON previews the one sound, so the citizen hears what they chose.
  assert.ok(html.includes("window.NayaNotif.playSound()"), "toggle previews the sound on ON");
});

test("exactly one notification sound exists: no library, no asset", () => {
  const html = readIndex();
  const oscCount = (html.match(/createOscillator/g) || []).length;
  assert.equal(oscCount, 1, "one chime only, not a library of noises");
  assert.ok(!html.includes("nayanet.notif.sound.url"), "no per-sound asset URL");
});
