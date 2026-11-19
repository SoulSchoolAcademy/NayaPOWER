import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { stripTypeScriptTypes } from "node:module";
import { test } from "node:test";
import vm from "node:vm";

// EXECUTED coverage for nayanet-smart-mail, the Smart Mail send door, which
// shipped with no test executing its handler -- caught by
// tests/edge_execution_coverage.test.mjs ("nayanet-smart-mail: NONE",
// "only 16/17 edge functions are executed by a test").
//
// This function is the write path for Smart Mail: the sender's identity
// comes from the JWT (never the body), the recipient must exist, and the
// message id is a deterministic UUIDv5 of (sender, recipient, body,
// idempotency_key), so a replayed send returns REPLAY instead of writing a
// duplicate. Every test below executes the real handler in a VM sandbox with
// a stubbed fetch, so a regression in auth, validation, recipient lookup,
// idempotency, or the write path fails here rather than in production. The
// stub records every outbound call, so the write-path tests prove the thread
// and message rows are actually written (and NOT written on replay).

const source = readFileSync(
  new URL("../supabase/functions/nayanet-smart-mail/index.ts", import.meta.url),
  "utf8"
);
// The handler is a module now (see the `export {};` marker in index.ts) but
// the VM sandbox loads it as a script, so drop the marker here — same
// preprocessing idea as the import strip in github_intake_execution.test.mjs.
// The marker itself is still type-checked by the edge type-check gate on the
// real file.
const code = stripTypeScriptTypes(
  source
    .replace(/^import .*;\r?\n/gm, "")
    .replace(/^export \{\};?\r?\n/m, ""),
);

const UUID_V5_RE =
  /^[0-9a-f]{8}-[0-9a-f]{4}-5[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

// A fake JWT: the handler only base64-decodes the claims segment and reads
// role + smart_alias from it (no signature verification — the gateway owns
// that, verify_jwt: true). No real credentials anywhere in this file.
function jwt(alias, role = "authenticated") {
  const b64 = (o) => Buffer.from(JSON.stringify(o)).toString("base64url");
  return `${b64({ alg: "none", typ: "JWT" })}.${b64({
    role,
    user_metadata: { smart_alias: alias },
  })}.sig`;
}

// Offline fetch stub: answers the Supabase REST + Auth Admin calls the
// handler makes, and records every call so write-path tests can prove what
// was (and was not) written.
function makeFetch({
  aliasFound = true,
  adminAliases = [],
  messageExists = false,
  threadExists = false,
  failThreadPost = false,
  failMessagePost = false,
} = {}) {
  const calls = [];
  const stub = async (url, init = {}) => {
    const method = (init.method ?? "GET").toUpperCase();
    const u = new URL(url);
    calls.push({ method, path: u.pathname + u.search, body: init.body });
    const ok = (status, payload) =>
      new Response(JSON.stringify(payload), { status });
    if (u.pathname === "/rest/v1/smart_mail_aliases" && method === "GET") {
      const alias = (u.searchParams.get("alias") ?? "").replace(/^eq\./, "");
      return ok(200, aliasFound && alias ? [{ alias }] : []);
    }
    if (u.pathname === "/auth/v1/admin/users" && method === "GET") {
      return ok(200, {
        users: adminAliases.map((a) => ({ user_metadata: { smart_alias: a } })),
      });
    }
    if (u.pathname === "/rest/v1/smart_mail_messages" && method === "GET") {
      return ok(200, messageExists ? [{ id: "x", thread_id: "y" }] : []);
    }
    if (u.pathname === "/rest/v1/smart_mail_threads" && method === "GET") {
      return ok(200, threadExists ? [{ id: "x" }] : []);
    }
    if (u.pathname === "/rest/v1/smart_mail_threads" && method === "POST") {
      return failThreadPost
        ? ok(500, { message: "boom" })
        : ok(201, JSON.parse(init.body ?? "{}"));
    }
    if (u.pathname === "/rest/v1/smart_mail_messages" && method === "POST") {
      return failMessagePost
        ? ok(500, { message: "boom" })
        : ok(201, JSON.parse(init.body ?? "{}"));
    }
    return ok(404, { message: "not found" });
  };
  stub.calls = calls;
  return stub;
}

function runtime(
  env = {
    SUPABASE_URL: "https://offline.invalid",
    SUPABASE_SERVICE_ROLE_KEY: "test-service-key-not-a-real-one",
  },
  fetchImpl = makeFetch(),
) {
  let handler;

  vm.runInNewContext(code, {
    URL, Request, Response, console, Date, TextEncoder, Uint8Array, atob, crypto,
    fetch: fetchImpl,
    Deno: {
      env: { get: (k) => env[k] ?? "" },
      serve: (cb) => { handler = cb; },
    },
  });

  return {
    fetch: fetchImpl,
    call: (body, { auth, method = "POST" } = {}) =>
      handler(new Request("https://offline.invalid/", {
        method,
        headers: {
          "content-type": "application/json",
          ...(auth ? { Authorization: `Bearer ${auth}` } : {}),
        },
        body: method === "GET" || method === "OPTIONS" ? undefined : body,
      })),
  };
}

function sendBody(overrides = {}) {
  return JSON.stringify({
    recipient: "bob",
    subject: "Hello",
    body: "Hi Bob, this is a test.",
    idempotency_key: "test-key-1",
    ...overrides,
  });
}

test("smart-mail answers OPTIONS with 204", async () => {
  const rt = runtime();
  const res = await rt.call(undefined, { method: "OPTIONS" });
  assert.equal(res.status, 204);
});

test("smart-mail rejects non-POST methods with 405", async () => {
  const rt = runtime();
  const res = await rt.call(undefined, { method: "GET" });
  assert.equal(res.status, 405);
  assert.equal((await res.json()).error, "METHOD_NOT_ALLOWED");
});

test("smart-mail rejects a body that is not JSON with 400", async () => {
  const rt = runtime();
  const res = await rt.call("this is not json", { auth: jwt("alice") });
  assert.equal(res.status, 400);
  assert.equal((await res.json()).error, "INVALID_JSON");
});

test("smart-mail rejects a send with no JWT with 401", async () => {
  const rt = runtime();
  const res = await rt.call(sendBody());
  assert.equal(res.status, 401);
  assert.equal((await res.json()).error, "AUTH_INVALID");
});

test("smart-mail rejects a JWT whose role is not authenticated with 401", async () => {
  const rt = runtime();
  const res = await rt.call(sendBody(), { auth: jwt("alice", "anon") });
  assert.equal(res.status, 401);
  assert.equal((await res.json()).error, "AUTH_INVALID");
});

test("smart-mail rejects a send missing recipient, body, or idempotency key with 400", async () => {
  const rt = runtime();
  const auth = jwt("alice");
  for (const overrides of [
    { recipient: undefined },
    { body: undefined },
    { idempotency_key: undefined },
  ]) {
    const payload = JSON.parse(sendBody());
    for (const [k, v] of Object.entries(overrides)) {
      if (v === undefined) delete payload[k];
      else payload[k] = v;
    }
    const res = await rt.call(JSON.stringify(payload), { auth });
    assert.equal(res.status, 400);
    assert.equal((await res.json()).error, "RECIPIENT_BODY_IDEMPOTENCY_REQUIRED");
  }
});

test("smart-mail rejects a body over 10,000 characters with 400", async () => {
  const rt = runtime();
  const res = await rt.call(sendBody({ body: "x".repeat(10_001) }), {
    auth: jwt("alice"),
  });
  assert.equal(res.status, 400);
  assert.equal((await res.json()).error, "BODY_TOO_LONG");
});

test("smart-mail rejects sending to yourself with 400", async () => {
  const rt = runtime();
  const res = await rt.call(sendBody({ recipient: "alice" }), {
    auth: jwt("alice"),
  });
  assert.equal(res.status, 400);
  assert.equal((await res.json()).error, "SENDER_IS_RECIPIENT");
});

test("smart-mail returns 404 when the recipient does not exist", async () => {
  const rt = runtime(
    undefined,
    makeFetch({ aliasFound: false, adminAliases: [] }),
  );
  const res = await rt.call(sendBody(), { auth: jwt("alice") });
  assert.equal(res.status, 404);
  assert.equal((await res.json()).error, "RECIPIENT_NOT_FOUND");
});

test("smart-mail sends a valid message and writes the thread and message rows", async () => {
  const rt = runtime();
  const res = await rt.call(sendBody(), { auth: jwt("alice") });
  assert.equal(res.status, 200);
  const body = await res.json();
  assert.equal(body.ok, true);
  assert.equal(body.status, "SENT");
  assert.match(body.thread_id, UUID_V5_RE);
  assert.match(body.message_id, UUID_V5_RE);

  // The write path actually ran: one thread insert, one message insert.
  const posts = rt.fetch.calls.filter((c) => c.method === "POST");
  assert.deepEqual(
    posts.map((c) => c.path),
    ["/rest/v1/smart_mail_threads", "/rest/v1/smart_mail_messages"],
  );
  const threadRow = JSON.parse(posts[0].body);
  assert.equal(threadRow.id, body.thread_id);
  assert.equal(threadRow.from_alias, "alice");
  assert.equal(threadRow.to_alias, "bob");
  const messageRow = JSON.parse(posts[1].body);
  assert.equal(messageRow.id, body.message_id);
  assert.equal(messageRow.thread_id, body.thread_id);
  assert.equal(messageRow.from_alias, "alice");
});

test("smart-mail ids are deterministic for the same send", async () => {
  const first = await (async () => {
    const rt = runtime();
    const res = await rt.call(sendBody(), { auth: jwt("alice") });
    return res.json();
  })();
  const second = await (async () => {
    const rt = runtime();
    const res = await rt.call(sendBody(), { auth: jwt("alice") });
    return res.json();
  })();
  assert.equal(second.thread_id, first.thread_id);
  assert.equal(second.message_id, first.message_id);
});

test("smart-mail replays an already-landed send instead of duplicating it", async () => {
  const rt = runtime(undefined, makeFetch({ messageExists: true }));
  const res = await rt.call(sendBody(), { auth: jwt("alice") });
  assert.equal(res.status, 200);
  const body = await res.json();
  assert.equal(body.ok, true);
  assert.equal(body.status, "REPLAY");
  assert.match(body.thread_id, UUID_V5_RE);
  assert.match(body.message_id, UUID_V5_RE);

  // No message insert on replay — the duplicate was not written.
  const posts = rt.fetch.calls.filter((c) => c.method === "POST");
  assert.deepEqual(posts, []);
});

test("smart-mail fails closed with 502 when the service env is not configured", async () => {
  const rt = runtime({});
  const res = await rt.call(sendBody(), { auth: jwt("alice") });
  assert.equal(res.status, 502);
  assert.equal((await res.json()).error, "MAIL_WRITE_FAILED");
});

test("smart-mail finds a recipient through the Auth Admin fallback", async () => {
  // Alias table has no row; the recipient carries the alias in user metadata.
  const rt = runtime(
    undefined,
    makeFetch({ aliasFound: false, adminAliases: ["bob"] }),
  );
  const res = await rt.call(sendBody(), { auth: jwt("alice") });
  assert.equal(res.status, 200);
  assert.equal((await res.json()).status, "SENT");
});

test("smart-mail reuses an existing thread instead of creating one", async () => {
  const rt = runtime(undefined, makeFetch({ threadExists: true }));
  const res = await rt.call(sendBody(), { auth: jwt("alice") });
  assert.equal(res.status, 200);
  assert.equal((await res.json()).status, "SENT");
  const posts = rt.fetch.calls.filter((c) => c.method === "POST");
  assert.deepEqual(
    posts.map((c) => c.path),
    ["/rest/v1/smart_mail_messages"],
  );
});

test("smart-mail returns 502 when the message write fails", async () => {
  const rt = runtime(undefined, makeFetch({ failMessagePost: true }));
  const res = await rt.call(sendBody(), { auth: jwt("alice") });
  assert.equal(res.status, 502);
  assert.equal((await res.json()).error, "MAIL_WRITE_FAILED");
});
