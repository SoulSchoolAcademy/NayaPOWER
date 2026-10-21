import assert from "node:assert/strict";
import { createHmac } from "node:crypto";
import { readFileSync } from "node:fs";
import { stripTypeScriptTypes } from "node:module";
import { test } from "node:test";
import vm from "node:vm";

// EXECUTED coverage for nayanet-github-intake, the GitHub webhook receiving
// door, which shipped with no test executing its handler -- caught by
// tests/edge_execution_coverage.test.mjs ("only 15/16 edge functions are
// executed by a test").
//
// This function is the trust boundary for everything GitHub tells the brain:
// the HMAC check over the RAW body is the only thing standing between a real
// GitHub delivery and anyone on the internet. Every test below executes the
// real handler so a regression in signature verification -- or in the
// fail-closed posture when the secret is unset -- fails here rather than in
// production. Expected signatures are computed with Node's HMAC, the way
// GitHub computes them, independently of the handler's own WebCrypto path.

const source = readFileSync(
  new URL("../supabase/functions/nayanet-github-intake/index.ts", import.meta.url),
  "utf8"
);
const code = stripTypeScriptTypes(source.replace(/^import .*;\r?\n/gm, ""));

const SECRET = "whsec_test_secret_not_a_real_one";
const DELIVERY = "72d3162e-0000-4000-8000-000000000000";

function sign(secret, rawBody) {
  return "sha256=" + createHmac("sha256", secret).update(rawBody, "utf8").digest("hex");
}

function runtime(env = { GITHUB_WEBHOOK_SECRET: SECRET }) {
  let handler;

  vm.runInNewContext(code, {
    URL, Request, Response, console, Date, TextEncoder, Uint8Array, crypto,
    Deno: {
      env: { get: (k) => env[k] },
      serve: (cb) => { handler = cb; },
    },
  });

  return (rawBody, headers = {}, method = "POST") =>
    handler(new Request("https://offline.invalid/", {
      method,
      headers: method === "POST" || rawBody !== undefined
        ? { "content-type": "application/json", ...headers }
        : headers,
      body: method === "GET" || method === "OPTIONS" ? undefined : rawBody,
    }));
}

function delivery(rawBody, { secret = SECRET, event = "issues", signature } = {}) {
  return {
    sig: signature ?? sign(secret, rawBody),
    headers: (s) => ({
      "x-hub-signature-256": s,
      "x-github-event": event,
      "x-github-delivery": DELIVERY,
    }),
  };
}

test("intake accepts a delivery whose signature is valid for the raw body", async () => {
  const rt = runtime();
  const rawBody = JSON.stringify({ action: "opened", issue: { number: 2825 } });
  const d = delivery(rawBody);
  const res = await rt(rawBody, d.headers(d.sig));
  assert.equal(res.status, 200);
  const body = await res.json();
  assert.equal(body.ok, true);
  assert.equal(body.received, true);
  assert.equal(body.event, "issues");
  assert.equal(body.action, "opened");
  assert.equal(body.delivery, DELIVERY);
});

test("intake answers a validly signed ping with pong", async () => {
  const rt = runtime();
  const rawBody = JSON.stringify({ zen: "Keep it logically awesome." });
  const d = delivery(rawBody, { event: "ping" });
  const res = await rt(rawBody, d.headers(d.sig));
  assert.equal(res.status, 200);
  const body = await res.json();
  assert.equal(body.ok, true);
  assert.equal(body.pong, true);
  assert.equal(body.delivery, DELIVERY);
});

test("intake rejects a signature that does not match the body", async () => {
  const rt = runtime();
  const rawBody = JSON.stringify({ action: "opened" });
  const forged = sign(SECRET, JSON.stringify({ action: "closed" }));
  const d = delivery(rawBody);
  const res = await rt(rawBody, d.headers(forged));
  assert.equal(res.status, 401);
  assert.equal((await res.json()).error, "SIGNATURE_INVALID");
});

test("intake rejects a signature made with the wrong secret", async () => {
  const rt = runtime();
  const rawBody = JSON.stringify({ action: "opened" });
  const d = delivery(rawBody, { secret: "some-other-secret" });
  const res = await rt(rawBody, d.headers(d.sig));
  assert.equal(res.status, 401);
  assert.equal((await res.json()).error, "SIGNATURE_INVALID");
});

test("intake rejects a delivery with no signature header", async () => {
  const rt = runtime();
  const rawBody = JSON.stringify({ action: "opened" });
  const res = await rt(rawBody, {
    "x-github-event": "issues",
    "x-github-delivery": DELIVERY,
  });
  assert.equal(res.status, 401);
  assert.equal((await res.json()).error, "SIGNATURE_MISSING");
});

test("intake verifies the raw body, not a re-serialisation of it", async () => {
  // The signature contract is over the exact bytes GitHub sent. A handler that
  // parsed and re-serialised the JSON before verifying would accept this
  // delivery; the real handler must not, because the bytes differ.
  const rt = runtime();
  const sent = '{ "action": "opened",  "spacing": "is part of the bytes" }';
  const reserialised = JSON.stringify(JSON.parse(sent));
  const d = delivery(sent);
  const res = await rt(reserialised, d.headers(d.sig));
  assert.equal(res.status, 401);
  assert.equal((await res.json()).error, "SIGNATURE_INVALID");
});

test("intake fails closed with 503 when the webhook secret is not configured", async () => {
  // An unconfigured intake accepts nothing, from anyone -- even a delivery
  // that would be validly signed if a secret were set.
  const rt = runtime({});
  const rawBody = JSON.stringify({ action: "opened" });
  const d = delivery(rawBody);
  const res = await rt(rawBody, d.headers(d.sig));
  assert.equal(res.status, 503);
  assert.equal((await res.json()).error, "INTAKE_NOT_CONFIGURED");
});

test("intake rejects non-POST methods with 405", async () => {
  const rt = runtime();
  const res = await rt(undefined, {}, "GET");
  assert.equal(res.status, 405);
  assert.equal((await res.json()).error, "METHOD_NOT_ALLOWED");
});

test("intake acknowledges a signed body it cannot parse as JSON", async () => {
  // GitHub delivered it and the signature proves it; retrying will not fix the
  // payload's shape, so the door acknowledges rather than erroring.
  const rt = runtime();
  const rawBody = "this is not json";
  const d = delivery(rawBody, { event: "push" });
  const res = await rt(rawBody, d.headers(d.sig));
  assert.equal(res.status, 200);
  const body = await res.json();
  assert.equal(body.ok, true);
  assert.equal(body.received, true);
  assert.equal(body.action, "");
});
