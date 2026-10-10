import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { stripTypeScriptTypes } from "node:module";
import { test } from "node:test";
import vm from "node:vm";

// EXECUTED coverage for v7-smart-note-canonical, which previously had none.
//
// This is the canonical Smart Note write path: the single seam where a human-authored
// note becomes a persisted intelligent event. It is also the only place governed task
// classes are admitted, and task-class attestation is what confers graph applicability
// downstream. Fail-open here would silently widen authority, so the registry gate is
// executed below rather than grepped.
//
// The handler is loaded into a VM sandbox with stubbed Deno / supabase so the real
// request path runs offline, exactly as it does in Deno.

const source = readFileSync(
  new URL("../supabase/functions/v7-smart-note-canonical/index.ts", import.meta.url),
  "utf8"
);
const code = stripTypeScriptTypes(source.replace(/^import[\s\S]*?;\r?\n/gm, ""));

const USER_ID = "11111111-1111-4111-8111-111111111111";

const GOVERNED = [
  "provenance_sensitive",
  "repository_correction",
  "active_intelligence_sensitive",
  "learning_reuse",
  "contextual_retrieval",
];

/** Load the module's pure helpers by running it with a Deno.serve that never fires. */
function loadHelpers() {
  const sandbox = { URL, Request, Response, console, Date, TextEncoder, Uint8Array, crypto,
    Deno: { env: { get: () => "x" }, serve: () => {} } };
  vm.runInNewContext(code + "\n;globalThis.__h = {validateDeclaredTaskClasses, buildIntelligentBlock, normalizedText, canonicalize, GOVERNED_TASK_CLASSES};", sandbox);
  return sandbox.__h;
}

const helpers = loadHelpers();

/**
 * Arrays/objects created inside a vm context have that realm's prototypes, so
 * assert.deepEqual (strict) fails on identity even when the contents match. Copy
 * across the boundary before comparing.
 */
const plain = (value) => JSON.parse(JSON.stringify(value));

test("governed task-class registry admits exactly the five ratified classes", () => {
  assert.deepEqual(plain([...helpers.GOVERNED_TASK_CLASSES]).sort(), [...GOVERNED].sort());
});

test("unknown task classes are rejected fail-closed and never confer applicability", () => {
  // The whole point of the registry: an unrecognised class must not ride along into
  // the persisted block, because that block is what downstream nodes attest against.
  for (const bogus of ["TASK_CLASS_UNKNOWN", "", "PROVENANCE_SENSITIVE", "provenance sensitive", "provenance_sensitive "]) {
    const { governed, rejected } = plain(helpers.validateDeclaredTaskClasses([bogus]));
    assert.deepEqual(governed, [], `"${bogus}" must not be governed`);
    // Case and whitespace variants are rejected rather than silently normalised:
    // a near-miss class name is a caller bug worth surfacing, and normalising it
    // would let a typo quietly confer applicability.
    assert.deepEqual(rejected, bogus ? [bogus] : [], `"${bogus}" classification`);
  }
  const mixed = plain(helpers.validateDeclaredTaskClasses(["provenance_sensitive", "TASK_CLASS_MALFORMED", "learning_reuse"]));
  assert.deepEqual(mixed.governed, ["provenance_sensitive", "learning_reuse"]);
  assert.deepEqual(mixed.rejected, ["TASK_CLASS_MALFORMED"]);
});

test("task-class validation ignores non-string and duplicate entries", () => {
  const r = plain(helpers.validateDeclaredTaskClasses(["learning_reuse", "learning_reuse", 42, null, {}, ["x"], "", "repository_correction"]));
  assert.deepEqual(r.governed, ["learning_reuse", "repository_correction"]);
  assert.deepEqual(r.rejected, []);
});

test("task-class validation treats a non-array as no declaration", () => {
  for (const bad of [undefined, null, "provenance_sensitive", { a: 1 }, 7]) {
    assert.deepEqual(plain(helpers.validateDeclaredTaskClasses(bad)), { governed: [], rejected: [] });
  }
});

test("task-class validation accepts the full governed set", () => {
  assert.deepEqual(plain(helpers.validateDeclaredTaskClasses(GOVERNED).governed), GOVERNED);
  assert.deepEqual(plain(helpers.validateDeclaredTaskClasses(GOVERNED).rejected), []);
});

function blockArgs(overrides = {}) {
  return {
    eventId: "aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee",
    now: "2026-10-01T00:00:00.000Z",
    userId: USER_ID,
    subject: "Test Note",
    humanText: "Human meaning",
    nayaText: "Naya interpretation",
    nutshell: "A nutshell",
    simpleText: "Simple words",
    machine: { event_id: "aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee", schema_version: "NAYANET_INTELLIGENT_BLOCK_V1" },
    source: "naya_conversation",
    idempotencyKey: "key-1",
    childText: "Child perspective",
    grandmaText: "Grandma perspective",
    learningText: "Learning lesson",
    meaningText: "What it means",
    connectsText: "How it connects",
    applyText: "How to apply",
    valueText: "Value",
    declaredTaskClasses: [],
    ...overrides,
  };
}

test("persisted block carries only the governed task classes into its provenance attestation", () => {
  const block = helpers.buildIntelligentBlock(blockArgs({ declaredTaskClasses: ["provenance_sensitive"] }));
  assert.deepEqual(plain(block.provenance.declared_task_classes), ["provenance_sensitive"]);
});

test("persisted block records the transport version and idempotency key", () => {
  const block = helpers.buildIntelligentBlock(blockArgs());
  assert.equal(block.metadata.transport_version, "NAYANET_INTELLIGENT_BLOCK_V1");
  assert.equal(block.metadata.source_idempotency_key, "key-1");
  // The projection fields are declared by the builder, not bolted on untyped.
  assert.ok("projection_category" in block.metadata);
  assert.ok("projection_topic" in block.metadata);
});

test("persisted block preserves every required perspective rather than dropping unknowns", () => {
  const block = helpers.buildIntelligentBlock(blockArgs());
  for (const key of ["human", "naya", "machine", "simple", "hub", "api"]) {
    assert.ok(block.projections[key], `missing projection: ${key}`);
  }
  assert.equal(block.identity.event_id, "aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee");
  assert.equal(block.identity.object_id, "event:aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee");
});

test("normalizedText collapses whitespace so idempotency comparison is stable", () => {
  assert.equal(helpers.normalizedText("  a   b \n c  "), "a b c");
  assert.equal(helpers.normalizedText(undefined), "");
  assert.equal(helpers.normalizedText(null), "");
});

test("canonicalize is deterministic across key order", () => {
  const a = helpers.canonicalize({ b: 1, a: { d: 2, c: [3, { f: 4, e: 5 }] } });
  const b = helpers.canonicalize({ a: { c: [3, { e: 5, f: 4 }], d: 2 }, b: 1 });
  assert.equal(JSON.stringify(a), JSON.stringify(b));
});

function runtime({ user = { id: USER_ID }, rpcResult, rpcError = null, idempotencyKeyInRpc = null } = {}) {
  let handler;
  const captured = { rpc: null };

  const supabase = {
    auth: {
      getUser: async () => (user ? { data: { user }, error: null } : { data: { user: null }, error: {} }),
    },
    rpc: async (name, args) => {
      captured.rpc = { name, args };
      if (rpcError) return { data: null, error: rpcError };
      if (rpcResult) return { data: rpcResult, error: null };
      return { data: {}, error: null };
    },
    from: () => ({
      select() { return this; },
      eq() { return this; },
      limit() { return this; },
      maybeSingle: async () => ({ data: null, error: null }),
      insert() { return { select: () => ({ single: async () => ({ data: null, error: null }) }) }; },
    }),
  };

  vm.runInNewContext(code, {
    URL, Request, Response, console, Date, TextEncoder, Uint8Array, crypto,
    Deno: {
      env: { get: (k) => ({ SUPABASE_URL: "https://offline.invalid", SUPABASE_ANON_KEY: "anon" })[k] },
      serve: (cb) => { handler = cb; },
    },
    createClient: () => supabase,
  });

  return {
    get captured() { return captured; },
    invoke: (body, headers = {}, method = "POST") =>
      handler(new Request("https://offline.invalid", {
        method,
        headers: { "content-type": "application/json", authorization: "Bearer t", ...headers },
        body: method === "GET" || method === "HEAD" ? undefined : JSON.stringify(body ?? {}),
      })),
  };
}

const validBody = {
  idempotency_key: "key-1",
  human_note: { text: "Human meaning", subject: "Test Note" },
  naya_note: { text: "Naya interpretation" },
};

test("smart-note requires authorization and an authenticated user", async () => {
  const anon = runtime({ user: null });
  const res = await anon.invoke(validBody);
  assert.equal(res.status, 401);
  assert.equal((await res.json()).error, "AUTHENTICATED_USER_REQUIRED");
});

test("smart-note requires an idempotency key, from body or header", async () => {
  const rt = runtime();
  const res = await rt.invoke({ ...validBody, idempotency_key: undefined });
  assert.equal(res.status, 400);
  assert.equal((await res.json()).error, "SMART_NOTE_IDEMPOTENCY_KEY_REQUIRED");
});

test("smart-note requires both a human and a Naya note", async () => {
  const rt = runtime();
  for (const body of [{ idempotency_key: "k" }, { idempotency_key: "k", human_note: { text: "a" } }, { idempotency_key: "k", naya_note: { text: "a" } }]) {
    const res = await rt.invoke(body);
    assert.equal(res.status, 400);
    assert.equal((await res.json()).error, "HUMAN_AND_NAYA_NOTES_REQUIRED");
  }
});

test("smart-note rejects non-POST with 405 and answers OPTIONS", async () => {
  const rt = runtime();
  const preflight = await rt.invoke(undefined, {}, "OPTIONS");
  assert.equal(preflight.status, 200);
  const wrong = await rt.invoke(undefined, {}, "GET");
  assert.equal(wrong.status, 405);
});

test("smart-note passes the idempotency key through to the canonical rpc", async () => {
  const rt = runtime();
  // The rpc stub returns no event id, so the handler stops at the lineage check --
  // but the request must have reached the canonical seam with the right key.
  await rt.invoke(validBody).catch(() => {});
  assert.equal(rt.captured.rpc?.name, "v7_create_smart_note");
  assert.equal(rt.captured.rpc?.args.p_idempotency_key, "key-1");
});

test("smart-note refuses to proceed when the canonical transaction has no event id", async () => {
  // Without this the function would invent an event identity, and the receipt would
  // point at nothing durable.
  const rt = runtime({ rpcResult: { id: "txn-1" } });
  const res = await rt.invoke(validBody);
  const body = await res.json();
  assert.notEqual(body.ok, true);
  assert.match(JSON.stringify(body), /SMART_NOTE_CANONICAL_EVENT_ID_MISSING/);
});

test("smart-note reports a pipeline failure and never claims the note was captured", async () => {
  const rt = runtime({ rpcError: { message: "deadlock detected", code: "40001" } });
  const res = await rt.invoke(validBody);
  const body = await res.json();
  assert.equal(body.ok, false);
  assert.equal(body.pipeline, "failed");
  assert.equal(body.transaction_id, null);
  // The failure must be legible. String(error) on a driver error object produced
  // "[object Object]", so the real cause never reached the caller; the handler now
  // extracts the driver's code and message.
  assert.equal(body.detail, "40001: deadlock detected");
});

test("smart-note still reports a reason when the thrown value is not an object", async () => {
  const rt = runtime({ rpcError: "plain string failure" });
  const res = await rt.invoke(validBody);
  const body = await res.json();
  assert.equal(body.ok, false);
  assert.equal(body.detail, "plain string failure");
});

test("smart-note rejects a replayed canonical event id that is not a UUID", async () => {
  // Regression anchor for the validation added in the edge-typecheck sweep. Before it,
  // a malformed persisted event id propagated straight into the canonical receipt.
  const rt = runtime({
    rpcResult: {
      id: "txn-1",
      evidence: { event_id: "not-a-uuid" },
      hub_state: { event_id: "not-a-uuid" },
      human_note: { text: "Human meaning", subject: "Test Note" },
      naya_note: { text: "Naya interpretation" },
    },
  });
  const res = await rt.invoke(validBody);
  const body = await res.json();
  assert.notEqual(body.ok, true);
  assert.match(JSON.stringify(body), /SMART_NOTE_CANONICAL_EVENT_ID_MALFORMED/);
});

test("smart-note rejects a replay whose persisted text disagrees with the request", async () => {
  // Same idempotency key, different content: this is the conflict case, and silently
  // returning the older note would misrepresent what the human just wrote.
  const persistedEventId = "aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee";
  const rt = runtime({
    rpcResult: {
      id: "txn-1",
      evidence: { event_id: persistedEventId },
      hub_state: { event_id: persistedEventId },
      human_note: { text: "Something entirely different", subject: "Test Note" },
      naya_note: { text: "Naya interpretation" },
    },
  });
  const res = await rt.invoke(validBody);
  const body = await res.json();
  assert.notEqual(body.ok, true);
  assert.match(JSON.stringify(body), /SMART_NOTE_IDEMPOTENCY_CONFLICT/);
});
