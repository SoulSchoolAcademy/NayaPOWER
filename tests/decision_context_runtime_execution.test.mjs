import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { stripTypeScriptTypes } from "node:module";
import { test } from "node:test";
import vm from "node:vm";

// EXECUTED coverage for naya-decision-context, which previously had none at all.
//
// This function is on the hot path for "does retained learning influence this
// decision?". Its whole job is to say whether the caller is grounded in verified
// learning, and to be explicit that looking up context grants no authority. Both
// properties are asserted by executing the handler, not by grepping its source.

const source = readFileSync(
  new URL("../supabase/functions/naya-decision-context/index.ts", import.meta.url),
  "utf8"
);
const code = stripTypeScriptTypes(source.replace(/^import .*;\r?\n/gm, ""));

const USER_ID = "11111111-1111-4111-8111-111111111111";

const evidenceRow = {
  id: "evidence-1",
  target_id: "TARGET-1",
  level: "APPLIED",
  status: "ACTIVE",
  claim: "Provenance precedes application.",
  observed_value: "PROVENANCE_PRESERVED",
  source_event_id: "event-1",
  verification_method: "CONTROLLED_INTERVENTION",
  provenance: { receipt_id: "receipt-1" },
  created_at: "2026-10-01T00:00:00Z",
};

function runtime({ user = { id: USER_ID }, evidence = evidenceRow, evidenceError = null } = {}) {
  let handler;
  const filters = {};

  const builder = {
    select() { return builder; },
    eq(key, value) { filters[key] = value; return builder; },
    order() { return builder; },
    limit() { return builder; },
    async maybeSingle() { return { data: evidence ?? null, error: evidenceError }; },
  };

  const supabase = {
    auth: {
      getUser: async () => (user ? { data: { user }, error: null } : { data: { user: null }, error: { message: "no session" } }),
    },
    from: () => builder,
  };

  vm.runInNewContext(code, {
    URL, Request, Response, console, Date,
    Deno: {
      env: { get: (k) => ({ SUPABASE_URL: "https://offline.invalid", SUPABASE_ANON_KEY: "anon" })[k] },
      serve: (cb) => { handler = cb; },
    },
    createClient: () => supabase,
  });

  return (body, headers = {}, method = "POST") =>
    handler(new Request("https://offline.invalid", {
      method,
      headers: { "content-type": "application/json", ...headers },
      body: method === "GET" || method === "HEAD" ? undefined : (typeof body === "string" ? body : JSON.stringify(body)),
    }));
}

test("decision-context answers OPTIONS for CORS preflight", async () => {
  const invoke = runtime();
  const res = await invoke(undefined, {}, "OPTIONS");
  assert.equal(res.status, 200);
  assert.equal((await res.json()).ok, true);
});

test("decision-context rejects non-POST with 405", async () => {
  const invoke = runtime();
  const res = await invoke(undefined, { authorization: "Bearer t" }, "GET");
  assert.equal(res.status, 405);
  assert.equal((await res.json()).error, "METHOD_NOT_ALLOWED");
});

test("decision-context requires an Authorization header", async () => {
  const invoke = runtime();
  const res = await invoke({ target_id: "TARGET-1" });
  assert.equal(res.status, 401);
  assert.equal((await res.json()).error, "AUTHORIZATION_REQUIRED");
});

test("decision-context requires an authenticated user, not just a bearer token", async () => {
  const invoke = runtime({ user: null });
  const res = await invoke({ target_id: "TARGET-1" }, { authorization: "Bearer not-a-real-session" });
  assert.equal(res.status, 401);
  assert.equal((await res.json()).error, "AUTHENTICATED_USER_REQUIRED");
});

test("decision-context requires a target_id", async () => {
  const invoke = runtime();
  for (const body of [{}, { target_id: "" }, { target_id: "   " }]) {
    const res = await invoke(body, { authorization: "Bearer t" });
    assert.equal(res.status, 400);
    assert.equal((await res.json()).error, "TARGET_ID_REQUIRED");
  }
});

test("decision-context reports available learning context without claiming causal influence", async () => {
  const invoke = runtime();
  const res = await invoke({ target_id: "TARGET-1" }, { authorization: "Bearer t" });
  assert.equal(res.status, 200);
  const body = await res.json();
  assert.equal(body.ok, true);
  assert.equal(body.decision.decision, "LEARNING_CONTEXT_AVAILABLE");
  assert.equal(body.decision.learning_context_available, true);
  assert.equal(body.decision.influenced, false);
  assert.equal(body.decision.target_id, "TARGET-1");
  assert.equal(body.decision.context.evidence_id, "evidence-1");
  assert.equal(body.decision.context.level, "APPLIED");
  assert.equal(body.decision.context.observed_value, "PROVENANCE_PRESERVED");
  assert.equal(body.decision.continuity.grounded, false);
  assert.equal(body.decision.continuity.next_step, "EVALUATE_LEARNING_APPLICABILITY_BEFORE_APPLY");
});

test("decision-context grants no authority even when learning is present", async () => {
  // The critical boundary: retrieving context is not authorization. A response that
  // lets this lookup mint or imply authority would turn a read into a grant.
  const invoke = runtime();
  const res = await invoke({ target_id: "TARGET-1" }, { authorization: "Bearer t" });
  const body = await res.json();
  assert.equal(body.decision.authority.changed, false);
  assert.equal(body.decision.authority.granted, false);
  assert.equal(typeof body.decision.authority.source, "string");
});

test("decision-context says NO_LEARNING_INFLUENCE and stays ungrounded when no evidence exists", async () => {
  const invoke = runtime({ evidence: null });
  const res = await invoke({ target_id: "TARGET-1" }, { authorization: "Bearer t" });
  assert.equal(res.status, 200);
  const body = await res.json();
  assert.equal(body.decision.decision, "NO_VERIFIED_LEARNING_CONTEXT");
  assert.equal(body.decision.influenced, false);
  assert.equal(body.decision.continuity.grounded, false);
  assert.equal(body.decision.continuity.next_step, "RETRIEVE_VERIFIED_LEARNING_BEFORE_CONTINUATION");
  assert.equal(body.decision.context.evidence_id, null);
  assert.equal(body.decision.context.level, null);
});

test("decision-context does not leak provenance detail when ungrounded", async () => {
  const invoke = runtime({ evidence: null });
  const res = await invoke({ target_id: "TARGET-1" }, { authorization: "Bearer t" });
  const body = await res.json();
  for (const key of ["claim", "source_event_id", "observed_value", "verification_method", "provenance"]) {
    assert.equal(body.decision.context[key], null, `${key} must be null when there is no evidence`);
  }
});

test("decision-context surfaces a query failure as 500 rather than a false negative", async () => {
  // Silently returning NO_LEARNING_INFLUENCE on a database error would be the worst
  // possible failure: it looks like a clean "no context" answer to the human.
  const invoke = runtime({ evidenceError: { message: "connection reset" } });
  const res = await invoke({ target_id: "TARGET-1" }, { authorization: "Bearer t" });
  assert.equal(res.status, 500);
  const body = await res.json();
  assert.equal(body.ok, false);
  assert.equal(body.error, "DECISION_CONTEXT_FAILED");
});

test("decision-context tolerates a malformed request body instead of crashing", async () => {
  const invoke = runtime();
  const res = await invoke("not json at all", { authorization: "Bearer t" });
  assert.equal(res.status, 400);
  assert.equal((await res.json()).error, "TARGET_ID_REQUIRED");
});

test("decision-context sets CORS headers so the Hub can read it", async () => {
  const invoke = runtime();
  const res = await invoke({ target_id: "TARGET-1" }, { authorization: "Bearer t" });
  assert.equal(res.headers.get("access-control-allow-origin"), "*");
  assert.match(res.headers.get("content-type") ?? "", /application\/json/);
});


test("decision-context keeps causal influence false on context lookup", async () => {
  const invoke = runtime();
  const res = await invoke({ target_id: "TARGET-1" }, { authorization: "Bearer t" });
  const body = await res.json();
  assert.equal(body.decision.learning_context_available, true);
  assert.equal(body.decision.influenced, false, "availability alone is not causal influence");
});
