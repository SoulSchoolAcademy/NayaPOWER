import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { stripTypeScriptTypes } from "node:module";
import { test } from "node:test";
import vm from "node:vm";

// EXECUTED coverage for the 2026-10-07 production repair of the capture chain:
// GitHub projection is best-effort and NON-BLOCKING. A dispatch failure must
// never 500 a successfully captured Smart Note; the projection outcome is
// recorded in the completion receipt so it stays observable.
//
// The full shipped handler runs offline in a VM sandbox with stubbed
// Deno/supabase/fetch, exactly as it does in Deno. Two scenarios:
//   - dispatch 500s        -> HTTP 200, ok:true, pipeline=SMART_NOTE_CAPTURED_PROJECTION_DEFERRED,
//                            repository_projection.status=PROJECTION_FAILED, smart_link=null
//   - dispatch verifies    -> HTTP 200, ok:true, pipeline=PROJECTION_VERIFIED with a real smart_link

const source = readFileSync(
  new URL("../supabase/functions/v7-smart-note-canonical/index.ts", import.meta.url),
  "utf8"
);
const code = stripTypeScriptTypes(source.replace(/^import[\s\S]*?;\r?\n/gm, ""));

const USER_ID = "11111111-1111-4111-8111-111111111111";
const EV_ID = "aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee";
const TX_ID = "bbbbbbbb-cccc-4ddd-8eee-ffffffffffff";
const GRANT_ID = "99999999-8888-4777-8666-555555555555";
const IB_ID = "IB-000042";
const CHECKPOINT_ID = "smart-note-checkpoint:" + EV_ID;
const LINK_RE = /^https:\/\/github\.com\/SoulSchoolAcademy\/NayaPOWER\/blob\/main\/.+\/IB-\d{6}\/smart-note\.md$/;

const TX_DATA = {
  id: TX_ID,
  intelligent_block: {
    identity: { intelligent_block_id: IB_ID, event_id: EV_ID },
    meaning: { subject: "Test Note", in_a_nutshell: "The nutshell." },
    integrity: { content_hash: "blockhash123" },
  },
  evidence: { event_id: EV_ID, receipt_id: "receipt-ev-1" },
  human_note: { subject: "Test Note", text: "Human meaning" },
  naya_note: { text: "Naya interpretation", summary: "The nutshell." },
};

const EVIDENCE_REFS = [
  { kind: "smart_note_receipt", receipt_id: "receipt-ev-1" },
  { kind: "source_event", event_id: EV_ID },
  { kind: "intelligent_block_hash", sha256: "blockhash123" },
  { kind: "learning_evidence", evidence_id: "learning-1" },
];

function runtime({ dispatchMode, sourceEvent = "present" }) {
  let handler;

  const query = (name) => {
    const q = {
      _eqs: [],
      _insert: null,
      select() { return q; },
      eq(col, val) { q._eqs.push([col, val]); return q; },
      order() { return q; },
      limit() { return q; },
      insert(row) { q._insert = row; return q; },
      maybeSingle: async () => resolveQuery(name, q),
      single: async () => resolveQuery(name, q),
    };
    return q;
  };

  async function resolveQuery(name, q) {
    if (name === "learning_evidence") {
      if (q._insert) {
        return {
          data: { id: "learning-1", status: "CANDIDATE", claim: q._insert.claim, target_id: q._insert.target_id },
          error: null,
        };
      }
      return { data: null, error: null };
    }
    if (name === "smart_note_events") {
      // Canonical source event lives here (production repair): id is the uuid PK.
      if (sourceEvent === "missing") return { data: null, error: null };
      const hasId = q._eqs.some(([c, v]) => c === "id" && v === EV_ID);
      const hasMember = q._eqs.some(([c, v]) => c === "member_id" && v === USER_ID);
      return { data: hasId && hasMember ? { id: EV_ID } : null, error: null };
    }
    if (name === "nayanet_cognition_events") {
      // Only the CHECKPOINT event is verified here (production repair).
      const checkpointed = q._eqs.some(([c, v]) => c === "event_id" && v === CHECKPOINT_ID);
      return {
        data: checkpointed
          ? { id: "cog-1", event_id: CHECKPOINT_ID, user_id: USER_ID, project_id: "NayaNET", status: "active", created_at: "2026-10-07T22:00:00.000Z" }
          : null,
        error: null,
      };
    }
    if (name === "nayanet_authority_grants") return { data: [], error: null };
    throw new Error("unexpected table " + name);
  }

  async function rpc(name) {
    if (name === "v7_create_smart_note") return { data: TX_DATA, error: null };
    if (name === "nayanet_record_cognition_event") {
      return {
        data: {
          event: { event_id: CHECKPOINT_ID, metadata: { evidence_refs: EVIDENCE_REFS } },
          receipt: { id: "receipt-1" },
        },
        error: null,
      };
    }
    if (name === "nayanet_issue_authority_grant") return { data: { grant_id: GRANT_ID }, error: null };
    throw new Error("unexpected rpc " + name);
  }

  // crypto.subtle is a getter that requires a real Crypto as `this`; intercept
  // only randomUUID through a Proxy bound to the real instance.
  const realCrypto = crypto;
  const fixedCrypto = new Proxy(realCrypto, {
    get(target, prop) {
      if (prop === "randomUUID") return () => EV_ID;
      return Reflect.get(target, prop, target);
    },
  });

  const context = {
    URL, Request, Response, console, Date, TextEncoder, Uint8Array,
    crypto: fixedCrypto,
    Deno: {
      env: {
        get: (key) => ({
          SUPABASE_URL: "https://offline.invalid",
          SUPABASE_ANON_KEY: "anon-key",
        }[key] || ""),
      },
      serve: (cb) => { handler = cb; },
    },
    createClient: () => ({
      auth: { getUser: async () => ({ data: { user: { id: USER_ID } }, error: null }) },
      from: query,
      rpc,
    }),
    fetch: async (url) => {
      assert.ok(String(url).endsWith("/functions/v1/nayanet-github-dispatch"), "only dispatch is fetched");
      if (dispatchMode === "failure") {
        return { ok: false, status: 500, json: async () => ({ ok: false, error: "GITHUB_DISPATCH_FAILED", pipeline: "failed" }) };
      }
      return {
        ok: true,
        status: 200,
        json: async () => ({
          ok: true,
          pipeline: "PROJECTION_VERIFIED",
          smart_link: "https://github.com/SoulSchoolAcademy/NayaPOWER/blob/main/BRAIN/05-MEMORY/SMART-NOTES/2026/10/07/system/test-topic/IB-000042/smart-note.md",
          receipt: { id: "r-1" },
          projection_verification: { completed_at: "2026-10-07T22:00:00.000Z", run_url: null },
        }),
      };
    },
  };
  vm.runInNewContext(code, context);
  assert.ok(handler, "Deno.serve handler registered");

  const post = (bodyObj) => {
    const req = new Request("https://offline.invalid/", {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: "Bearer user-jwt" },
      body: JSON.stringify(bodyObj),
    });
    return handler(req).then(async (res) => ({ status: res.status, body: await res.json() }));
  };
  return { post };
}

const noteBody = () => ({
  human_note: { subject: "Test Note", text: "Human meaning" },
  naya_note: { text: "Naya interpretation", summary: "The nutshell." },
  idempotency_key: "idem-1",
});

test("dispatch failure does not fail the capture: 200 with PROJECTION_FAILED recorded", async () => {
  const { post } = runtime({ dispatchMode: "failure" });
  const { status, body } = await post(noteBody());
  assert.equal(status, 200, "core capture stays 200 when projection fails: " + JSON.stringify(body).slice(0, 300));
  assert.equal(body.ok, true);
  assert.equal(body.pipeline, "SMART_NOTE_CAPTURED_PROJECTION_DEFERRED");
  assert.equal(body.smart_link, null);
  assert.equal(body.repository_projection.status, "PROJECTION_FAILED");
  assert.equal(body.repository_projection.smart_link, null);
  assert.equal(body.projection_verification.status, "PROJECTION_FAILED");
  assert.ok(body.projection_verification.error.includes("SMART_NOTE_GITHUB_PROJECTION_FAILED"));
  assert.equal(body.completion_receipt.repository_projection.status, "PROJECTION_FAILED");
  // The canonical capture evidence itself is intact.
  assert.equal(body.intelligent_block_id, IB_ID);
  assert.equal(body.transaction_id, TX_ID);
  assert.equal(body.feed_verification.verified, true);
  assert.equal(body.feed_verification.event_id, CHECKPOINT_ID, "feed verification covers the checkpoint event");
});

test("dispatch success still yields PROJECTION_VERIFIED with a real smart_link", async () => {
  const { post } = runtime({ dispatchMode: "success" });
  const { status, body } = await post(noteBody());
  assert.equal(status, 200);
  assert.equal(body.ok, true);
  assert.equal(body.pipeline, "PROJECTION_VERIFIED");
  assert.ok(LINK_RE.test(body.smart_link), "smart_link is a real GitHub link: " + body.smart_link);
  assert.equal(body.repository_projection.status, "PROJECTION_VERIFIED");
  assert.equal(body.projection_verification.status, "PROJECTION_VERIFIED");
});

test("missing canonical source event in smart_note_events fails closed", async () => {
  // Negative control for the corrected source lookup: when the Smart Note event
  // is absent from smart_note_events, the checkpoint throws
  // CHECKPOINT_SOURCE_EVENT_NOT_FOUND instead of proceeding on unproven state.
  const { post } = runtime({ dispatchMode: "success", sourceEvent: "missing" });
  const { status, body } = await post(noteBody());
  assert.equal(status, 500);
  assert.equal(body.ok, false);
  assert.ok(body.detail.includes("CHECKPOINT_SOURCE_EVENT_NOT_FOUND"), "fails on the source lookup: " + body.detail.slice(0, 120));
});
