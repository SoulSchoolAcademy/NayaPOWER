import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { stripTypeScriptTypes } from "node:module";
import { test } from "node:test";
import vm from "node:vm";

import {
  expandBlock,
  expandRanked,
} from "../supabase/functions/nayanet-intelligence-retrieve/retrieve.ts";

// Executed coverage for nayanet-intelligence-retrieve.
// The cold-retrieve handler is an authority-adjacent read surface: it must run,
// authenticate the OIDC workflow identity, preserve retrieval != authority, and
// fail closed when its search substrate fails.

const indexSource = readFileSync(
  new URL("../supabase/functions/nayanet-intelligence-retrieve/index.ts", import.meta.url),
  "utf8",
);
const indexCode = stripTypeScriptTypes(indexSource.replace(/^import .*;\r?\n/gm, ""));

const REPO = "SoulSchoolAcademy/NayaPOWER";
const REF = "refs/heads/main";
const WORKFLOW = ".github/workflows/live-know-proof.yml";
const OWNER = "adfdf0b8-5558-41d1-9fed-ec51abf4fe2f";

function block(id, overrides = {}) {
  return {
    block_id: id,
    status: "DURABLE",
    understanding_state: "VERIFIED",
    owner_scope: "PRIVATE",
    applicable_scope: {},
    content: { lesson: id },
    connections: [],
    superseded_by_block_id: null,
    evidence_refs: [{ receipt_id: `receipt-${id}` }],
    provenance: { source: "test" },
    updated_at: "2026-10-06T00:00:00Z",
    score: 0.8,
    score_breakdown: {},
    why: ["test"],
    ...overrides,
  };
}

function handlerRuntime({
  payload = {
    repository: REPO,
    workflow_ref: `${REPO}/${WORKFLOW}@${REF}`,
    ref: REF,
    jti: "runtime-jti-1",
  },
  ranked = [block("IB-ONE")],
  rpcError = null,
} = {}) {
  let handler;
  let rpcArgs = null;
  let receiptInsert = null;

  const receiptBuilder = {
    insert(value) { receiptInsert = value; return receiptBuilder; },
    select() { return receiptBuilder; },
    async single() { return { data: { id: "receipt-read-1" }, error: null }; },
  };

  const admin = {
    async rpc(name, args) {
      assert.equal(name, "nayanet_retrieve_blocks");
      rpcArgs = args;
      return { data: ranked, error: rpcError };
    },
    from(name) {
      assert.equal(name, "nayanet_execution_receipts");
      return receiptBuilder;
    },
  };

  vm.runInNewContext(indexCode, {
    URL, Request, Response, console, Date,
    Deno: {
      env: {
        get: (key) => ({
          SUPABASE_URL: "https://offline.invalid",
          SUPABASE_SERVICE_ROLE_KEY: "service-role",
        })[key],
      },
      serve: (cb) => { handler = cb; },
    },
    createRemoteJWKSet: () => ({}),
    jwtVerify: async () => ({ payload }),
    createClient: () => admin,
    expandRanked,
  });

  const invoke = (body, headers = {}, method = "POST") =>
    handler(new Request("https://offline.invalid", {
      method,
      headers: { "content-type": "application/json", ...headers },
      body: method === "GET" || method === "HEAD" ? undefined : JSON.stringify(body ?? {}),
    }));

  return {
    invoke,
    getRpcArgs: () => rpcArgs,
    getReceiptInsert: () => receiptInsert,
  };
}

test("cold-retrieve health endpoint executes without runtime identity", async () => {
  const { invoke } = handlerRuntime();
  const res = await invoke(undefined, {}, "GET");
  assert.equal(res.status, 200);
  assert.deepEqual(await res.json(), {
    ok: true,
    service: "nayanet-intelligence-retrieve",
    mode: "health",
  });
});

test("cold-retrieve requires a runtime OIDC bearer identity", async () => {
  const { invoke } = handlerRuntime();
  const res = await invoke({ query: "provenance" });
  assert.equal(res.status, 401);
  assert.equal((await res.json()).error, "RUNTIME_IDENTITY_REQUIRED");
});

test("cold-retrieve rejects a valid token bound to the wrong workflow", async () => {
  const { invoke } = handlerRuntime({
    payload: {
      repository: REPO,
      workflow_ref: `${REPO}/.github/workflows/not-approved.yml@${REF}`,
      ref: REF,
    },
  });
  const res = await invoke(
    { query: "provenance" },
    { authorization: "Bearer token" },
  );
  assert.equal(res.status, 401);
  assert.equal((await res.json()).error, "WORKFLOW_BINDING_MISMATCH");
});

test("cold-retrieve executes ranked retrieval but never mints authority", async () => {
  const { invoke, getRpcArgs, getReceiptInsert } = handlerRuntime();
  const res = await invoke(
    { query: "preserve provenance", limit: 999, include_related: false },
    { authorization: "Bearer token" },
  );
  assert.equal(res.status, 200);
  const body = await res.json();
  assert.equal(body.ok, true);
  assert.equal(body.status, "RETRIEVED");
  assert.equal(body.result_count, 1);
  assert.equal(body.results[0].block_id, "IB-ONE");
  assert.equal(body.retrieval_creates_authority, false);
  assert.equal(body.handoff_to, "NAYA-KERNEL-PROVE");

  assert.equal(getRpcArgs().p_owner_id, OWNER);
  assert.equal(getRpcArgs().p_limit, 50);
  assert.equal(getReceiptInsert().evidence.retrieval_creates_authority, false);
});

test("cold-retrieve surfaces an RPC failure instead of returning a false clean miss", async () => {
  const { invoke } = handlerRuntime({ rpcError: { message: "database unavailable" } });
  const res = await invoke(
    { query: "anything" },
    { authorization: "Bearer token" },
  );
  assert.equal(res.status, 400);
  assert.match((await res.json()).error, /RETRIEVE_RPC_FAILED/);
});

test("Graph V2 gates consent, applicability, temporal state, and target servability", async () => {
  const now = new Date("2026-10-07T00:00:00Z");
  const successor = block("IB-NEW", {
    connections: [
      {
        relationship_id: "rel-support",
        target_block_id: "IB-SUPPORT",
        relationship_type: "SUPPORTS",
        status: "ACTIVE",
        epistemic_state: "VERIFIED",
        visibility: "PRIVATE",
        applicability: { state: "UNKNOWN" },
      },
      {
        relationship_id: "rel-conflict",
        target_block_id: "IB-CONFLICT",
        relationship_type: "CONTRADICTS",
        status: "ACTIVE",
        epistemic_state: "CONTRADICTED",
        visibility: "PRIVATE",
      },
      {
        relationship_id: "rel-no-consent",
        target_block_id: "IB-NO-CONSENT",
        relationship_type: "SUPPORTS",
        status: "ACTIVE",
        visibility: "DERIVED_SHARED",
      },
      {
        relationship_id: "rel-not-applicable",
        target_block_id: "IB-NOT-APPLICABLE",
        relationship_type: "SUPPORTS",
        status: "ACTIVE",
        visibility: "PRIVATE",
        applicability: { state: "NOT_APPLICABLE" },
      },
      {
        relationship_id: "rel-expired",
        target_block_id: "IB-EXPIRED",
        relationship_type: "SUPPORTS",
        status: "ACTIVE",
        visibility: "PRIVATE",
        valid_until: "2026-10-06T23:59:59Z",
      },
      {
        relationship_id: "rel-candidate-target",
        target_block_id: "IB-CANDIDATE",
        relationship_type: "SUPPORTS",
        status: "ACTIVE",
        visibility: "PRIVATE",
      },
    ],
  });

  const rows = new Map([
    ["IB-NEW", successor],
    ["IB-SUPPORT", block("IB-SUPPORT")],
    ["IB-CONFLICT", block("IB-CONFLICT")],
    ["IB-NO-CONSENT", block("IB-NO-CONSENT")],
    ["IB-NOT-APPLICABLE", block("IB-NOT-APPLICABLE")],
    ["IB-EXPIRED", block("IB-EXPIRED")],
    ["IB-CANDIDATE", block("IB-CANDIDATE", { understanding_state: "CANDIDATE" })],
  ]);
  const fetchBlock = async (id) => rows.get(id) ?? null;

  const out = await expandBlock(
    block("IB-OLD", { superseded_by_block_id: "IB-NEW" }),
    fetchBlock,
    now,
  );

  assert.equal(out.block_id, "IB-NEW");
  assert.equal(out.via_lineage, "SUPERSEDED_BY:IB-NEW");
  assert.deepEqual(out.related_context.map((x) => x.block_id), ["IB-SUPPORT"]);
  assert.deepEqual(out.conflicts.map((x) => x.block_id), ["IB-CONFLICT"]);
});

test("include_related=false still resolves known supersession", async () => {
  const rows = new Map([
    ["IB-NEW", block("IB-NEW", {
      connections: [{
        target_block_id: "IB-SUPPORT",
        relationship_type: "SUPPORTS",
        status: "ACTIVE",
        visibility: "PRIVATE",
      }],
    })],
    ["IB-SUPPORT", block("IB-SUPPORT")],
  ]);
  const out = await expandBlock(
    block("IB-OLD", { superseded_by_block_id: "IB-NEW" }),
    async (id) => rows.get(id) ?? null,
    new Date("2026-10-07T00:00:00Z"),
    false,
  );
  assert.equal(out.block_id, "IB-NEW");
  assert.equal(out.via_lineage, "SUPERSEDED_BY:IB-NEW");
  assert.deepEqual(out.related_context, []);
  assert.deepEqual(out.conflicts, []);
});

test("supersession is cycle-safe and stops at the last non-cyclic servable block", async () => {
  const old = block("IB-A", { superseded_by_block_id: "IB-B" });
  const next = block("IB-B", { superseded_by_block_id: "IB-A" });
  const rows = new Map([["IB-A", old], ["IB-B", next]]);
  const out = await expandBlock(
    old,
    async (id) => rows.get(id) ?? null,
    new Date("2026-10-07T00:00:00Z"),
  );
  assert.equal(out.block_id, "IB-B");
  assert.equal(out.via_lineage, "SUPERSEDED_BY:IB-B");
});
