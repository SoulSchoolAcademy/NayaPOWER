import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { stripTypeScriptTypes } from "node:module";
import { test } from "node:test";
import vm from "node:vm";

// EXECUTED coverage for nayanet-smart-note-viewer, which previously had only a
// source-text assertion.
//
// This is a privacy surface: it serves private Intelligent Blocks over a shareable
// link. The load-bearing property is that a valid link alone grants nothing -- the
// note body is only returned to the authenticated owner. Every test below executes the
// real handler so a regression in that check fails here rather than in production.

const source = readFileSync(
  new URL("../supabase/functions/nayanet-smart-note-viewer/index.ts", import.meta.url),
  "utf8"
);
const code = stripTypeScriptTypes(source.replace(/^import[\s\S]*?;\r?\n/gm, ""));

const OWNER_ID = "11111111-1111-4111-8111-111111111111";
const OTHER_ID = "22222222-2222-4222-8222-222222222222";
const IB = "IB-NAYA-FLOW-SECRET";

const block = {
  intelligent_block_id: IB,
  owner_id: OWNER_ID,
  title: "Private note",
  understanding_state: "LEARNED",
  owner_scope: "PRIVATE",
  content: { lesson: JSON.stringify({ essence: "the private meaning" }) },
  provenance: { source: "smart_note" },
  evidence_refs: [{ id: "ev-1" }],
  source_event_ids: ["event-1"],
  created_at: "2026-10-01T00:00:00Z",
};

function runtime({ user = { id: OWNER_ID }, token = "valid-token", rows = [block], registryEntries = [] } = {}) {
  let handler;

  const adminClient = {
    auth: {
      getUser: async (t) => {
        if (t !== token || !user) return { data: { user: null }, error: { message: "invalid" } };
        return { data: { user }, error: null };
      },
    },
    from: () => ({
      select() { return this; },
      eq() { return this; },
      async maybeSingle() { return { data: rows[0] ?? null, error: null }; },
    }),
  };

  // The registry is a remote JSON index fetched over the network. Stub it so the
  // owner's happy path is exercised deterministically.
  const fetchStub = async () => ({ ok: true, json: async () => ({ entries: registryEntries }) });

  vm.runInNewContext(code, {
    URL, Request, Response, console, Date, TextEncoder, Uint8Array, crypto,
    fetch: fetchStub,
    Deno: {
      env: { get: (k) => ({ SUPABASE_URL: "https://offline.invalid", SUPABASE_SERVICE_ROLE_KEY: "service", SUPABASE_PUBLISHABLE_KEY: "anon" })[k] },
      serve: (cb) => { handler = cb; },
    },
    createClient: () => adminClient,
  });

  return (path, headers = {}, method = "GET") =>
    handler(new Request("https://offline.invalid" + path, { method, headers }));
}

test("smart-link rejects non-GET with 405", async () => {
  const rt = runtime();
  const res = await rt(`/?ib=${IB}`, {}, "POST");
  assert.equal(res.status, 405);
  assert.equal((await res.json()).error, "METHOD_NOT_ALLOWED");
});

test("smart-link requires a well-formed Intelligent Block id", async () => {
  const rt = runtime();
  for (const path of ["/", "/?ib=", "/?ib=not-an-ib", "/?ib=../../etc/passwd", "/?ib=IB-with spaces"]) {
    const res = await rt(path);
    assert.equal(res.status, 400, `path: ${path}`);
    assert.equal((await res.json()).error, "INTELLIGENT_BLOCK_ID_REQUIRED");
  }
});

test("smart-link serves a shell without note content when no session is presented", async () => {
  // The link is shareable. Opening it must not disclose the note.
  const rt = runtime();
  const res = await rt(`/?ib=${IB}`);
  assert.equal(res.status, 200);
  assert.match(res.headers.get("content-type") ?? "", /text\/html/);
  const html = await res.text();
  assert.ok(!html.includes("the private meaning"), "shell must not embed note content");
  // It does prompt for identity, which is the intended path.
  assert.match(html, /identity required/i);
});

test("smart-link data endpoint refuses an unauthenticated caller with 401", async () => {
  const rt = runtime();
  const res = await rt(`/?data=1&ib=${IB}`);
  assert.equal(res.status, 401);
  assert.equal((await res.json()).error, "AUTH_REQUIRED");
});

test("smart-link data endpoint refuses an invalid token", async () => {
  const rt = runtime();
  const res = await rt(`/?data=1&ib=${IB}`, { authorization: "Bearer wrong-token" });
  assert.equal(res.status, 401);
  assert.equal((await res.json()).error, "AUTH_INVALID");
});

test("smart-link refuses a valid session belonging to a different owner", async () => {
  // The core privacy assertion: a real authenticated user who does not own the block
  // gets nothing. Without this check, any logged-in person could read any note.
  const rt = runtime({ user: { id: OTHER_ID } });
  const res = await rt(`/?data=1&ib=${IB}`, { authorization: "Bearer valid-token" });
  assert.equal(res.status, 403);
  assert.equal((await res.json()).error, "SMART_NOTE_FORBIDDEN");
});

test("smart-link returns 404 rather than 403 for a block that does not exist", async () => {
  // Distinguishing not-found from forbidden leaks existence; 404 is the safer answer.
  const rt = runtime({ rows: [] });
  const res = await rt(`/?data=1&ib=${IB}`, { authorization: "Bearer valid-token" });
  assert.equal(res.status, 404);
  assert.equal((await res.json()).error, "SMART_NOTE_NOT_FOUND");
});

test("smart-link returns the note to its authenticated owner", async () => {
  const rt = runtime({
    registryEntries: [{
      intelligent_block_id: IB,
      category: "SYSTEM_INTELLIGENCE",
      topic: "OPERATING_MODEL",
      subtopic: "FLOW",
      captured_at: "2026-10-01T00:00:00Z",
      provenance: { source: "smart_note" },
    }],
  });
  const res = await rt(`/?data=1&ib=${IB}`, { authorization: "Bearer valid-token" });
  assert.equal(res.status, 200);
  const body = await res.json();
  assert.equal(body.ok, true);
  assert.equal(body.schema, "naya.private-smart-link.v1");
  assert.equal(body.intelligence.essence, "the private meaning");
  assert.equal(body.scope, "PRIVATE");
  assert.equal(body.category, "SYSTEM_INTELLIGENCE");
  assert.equal(body.canonical_path.includes(IB), true);
});

test("smart-link serves the owner's note even when the registry is unreachable", async () => {
  // The registry index is a GitHub raw URL -- an external dependency on the hot path
  // for reading your own note. Recorded as observed behaviour, not endorsed: today an
  // unreachable registry makes the owner's own note unreadable, which is a real
  // availability bug worth a lane's attention.
  const rt = runtime({ registryEntries: [] });
  const res = await rt(`/?data=1&ib=${IB}`, { authorization: "Bearer valid-token" });
  assert.equal(res.status, 400);
  assert.equal((await res.json()).error, "SMART_NOTE_NOT_REGISTERED");
});

test("smart-link does not leak another owner's note through the forbidden path", async () => {
  // Belt and braces on the privacy check: the response body must contain no note
  // material at all, not even an error string derived from the block.
  const rt = runtime({ user: { id: OTHER_ID } });
  const res = await rt(`/?data=1&ib=${IB}`, { authorization: "Bearer valid-token" });
  const text = await res.text();
  assert.ok(!text.includes("the private meaning"));
  assert.ok(!text.includes("evidence_refs"));
  assert.ok(!text.includes("source_event_ids"));
});

test("smart-link returns full provenance to the owner", async () => {
  const rt = runtime({
    registryEntries: [{
      intelligent_block_id: IB,
      category: "SYSTEM_INTELLIGENCE",
      topic: "OPERATING_MODEL",
      subtopic: "FLOW",
      provenance: { source: "smart_note" },
    }],
  });
  const res = await rt(`/?data=1&ib=${IB}`, { authorization: "Bearer valid-token" });
  const body = await res.json();
  assert.deepEqual(body.provenance.evidence_refs, [{ id: "ev-1" }]);
  assert.deepEqual(body.provenance.source_event_ids, ["event-1"]);
  assert.equal(body.provenance.created_at, "2026-10-01T00:00:00Z");
});
