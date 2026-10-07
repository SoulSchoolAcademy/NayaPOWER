import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { stripTypeScriptTypes } from "node:module";
import { test } from "node:test";
import vm from "node:vm";

// Firing proofs for nayanet-learning-verify -- the LOCK-IN path.
//
// This is the last function that can promote a claim from CANDIDATE to ACTIVE and
// simultaneously rewrite canonical brain state (block -> LEARNED, relationship ->
// VERIFIED, checkpoint -> LEARNED). A fail-open here does not return a wrong answer.
// It WRITES a wrong answer into the brain that everything else later reads as
// settled knowledge.
//
// AND two defects found while writing these, which are worse than "missing proof":
//
//   CV-06 -- THE LAW GATE IS ORDERED AFTER THE MUTATIONS IT IS SUPPOSED TO GUARD.
//
//     index.ts:404 promotes learning_evidence to status:ACTIVE / provenance:VERIFICATION.
//     index.ts:453 writes `verified: true` into an execution receipt.
//     index.ts:482 calls resolveLearningLockInLaw().
//
//     So when LAW denies, the runtime correctly answers 403
//     LEARNING_LOCK_IN_LAW_DENIED -- and the two mutations it just performed are
//     already persisted. The refusal is real and the fail-open is real, in the same
//     request. The H13 comment at index.ts:478 states the intent plainly:
//     "every canonical mutation must sit behind the grant gate." Two of them do not.
//
//     The same ordering bug applies to RECEIPT_NOT_FOUND_OR_NOT_OWNED (index.ts:435):
//     the learning row is already ACTIVE before the receipt is looked up.
//
//   CV-07 -- evidence_refs IS NEVER CHECKED TO BE EVIDENCE.
//
//     index.ts:398 takes `body.evidence_refs` as an array of caller-supplied strings and
//     only requires that it be non-empty (index.ts:399). index.ts:552 then derives
//     `causal_verification_id: refs.find(r => r.startsWith("CVO-")) || null`.
//
//     So arbitrary strings promote the learning AND write causal_verification_id:null
//     into the block, relationship and checkpoint provenance while still reporting
//     VERIFIED. The candidate's own verification_method -- set at index.ts:333 -- says
//     "Pending independent causal verification of the persisted Event -> Intelligent
//     Block -> ... chain." The promotion claims to discharge a requirement it never
//     checks. A caller can pass ["lol"] and get a verified lock-in with no verification
//     id recorded anywhere.
//
//   The tests below assert the CURRENT behaviour exactly, including both fail-opens, so
//   both lies are on the record in executable form. Each repair turns a test red, which
//   is the signal that the repair happened and the assertion was updated in the same
//   commit. Fixing these silently would be worse than the defects.

const source = readFileSync(
  new URL("../supabase/functions/nayanet-learning-verify/index.ts", import.meta.url),
  "utf8"
);
const code = stripTypeScriptTypes(
  source
    .replace(/^import .*from "\.\/.*";\r?\n/gm, "")
    .replace(/^import .*;\r?\n/gm, "")
);

const OWNER = "adfdf0b8-5558-41d1-9fed-ec51abf4fe2f";
const FUTURE = "2099-01-01T00:00:00.000Z";

/** Default healthy row set for the verify (lock-in) path. */
function baseTables(overrides = {}) {
  return {
    learning_evidence: [
      {
        id: "L1",
        member_id: OWNER,
        status: "CANDIDATE",
        claim: "lesson text",
        provenance: "OBSERVATION",
        verification_method: "Pending independent causal verification of the persisted chain.",
        observed_value: {
          intelligent_block_id: "IB-1",
          relationship_id: "R1",
          checkpoint_id: "C1",
          lineage_id: "LN1",
          index_id: "I1",
          commit_receipt_id: "RC1",
          checkpoint_provenance: "CURRENT_STATE_MATCH",
        },
      },
    ],
    nayanet_intelligent_blocks: [
      {
        intelligent_block_id: "IB-1",
        owner_id: OWNER,
        understanding_state: "CANDIDATE",
        provenance: {},
        evidence_refs: [],
        content: { lesson: "lesson text" },
      },
    ],
    nayanet_brain_relationships: [
      {
        relationship_id: "R1",
        owner_id: OWNER,
        epistemic_state: "CANDIDATE",
        provenance: {},
        evidence_refs: [],
      },
    ],
    nayanet_project_cognition_state: [
      { id: "C1", user_id: OWNER, project_id: "NayaNET", status: "ACTIVE", revision: 3, updated_at: "2026-01-01T00:00:00.000Z", state: { status: "CANDIDATE" } },
    ],
    nayanet_execution_receipts: [
      { id: "RC1", user_id: OWNER, project_id: "NayaNET", action: "intelligence_commit", learning: [], evidence: {} },
    ],
    nayanet_authority_grants: [
      {
        grant_id: "G1",
        issuer_id: OWNER,
        subject_id: OWNER,
        actions: ["learning_lock_in"],
        status: "ACTIVE",
        revoked_at: null,
        expires_at: FUTURE,
        scope: { target: "IB-1" },
      },
    ],
    ...overrides,
  };
}

/** Row set for the candidate path, which walks a different chain. */
function candidateTables(overrides = {}) {
  return {
    learning_evidence: [],
    nayanet_intelligent_blocks: [
      {
        block_id: "B1",
        intelligent_block_id: "IB-1",
        owner_id: OWNER,
        understanding_state: "CANDIDATE",
        content: { lesson: "persistence alone is memory, not proof of active intelligence" },
        evidence_refs: [{ event_id: "E1", receipt_id: "RC1" }],
        created_at: "2026-01-01T00:00:00.000Z",
      },
    ],
    nayanet_cognition_events: [{ id: "E1", event_id: "EV-1", receipt_id: "RC1", user_id: OWNER, created_at: "2026-01-01T00:00:00.000Z" }],
    nayanet_intelligence_lineage: [{ id: "LN1", source_event_id: "E1", target_event_id: "E2", relation: "derives", created_at: "2026-01-01T00:00:00.000Z" }],
    nayanet_brain_relationships: [{ relationship_id: "R1", owner_id: OWNER, source_id: "E1", target_id: "IB-1", relationship_type: "supports", epistemic_state: "CANDIDATE", provenance: {} }],
    nayanet_intelligence_index: [{ id: "I1", source_id: "B1", owner_id: OWNER, source_table: "nayanet_intelligent_blocks", object_type: "intelligent_block", status: "ACTIVE" }],
    nayanet_project_cognition_state: [
      {
        id: "C1",
        user_id: OWNER,
        project_id: "NayaNET",
        status: "ACTIVE",
        revision: 3,
        updated_at: "2026-01-01T00:00:00.000Z",
        state: { intelligent_block_id: "IB-1", lineage_id: "LN1", relationship_id: "R1", index_id: "I1" },
      },
    ],
    nayanet_execution_receipts: [{ id: "RC1", user_id: OWNER, project_id: "NayaNET", action: "intelligence_commit", learning: [], evidence: { checkpoint_id: "C1", event_row_id: "E1", intelligent_block_id: "IB-1", lineage_id: "LN1", relationship_id: "R1", index_id: "I1", content_hash: "h1", authority_grant_id: "G1" } }],
    nayanet_authority_grants: [],
    ...overrides,
  };
}

/**
 * Drive the real handler over an in-memory table set.
 *
 * Returns the response body, the final rows, and every write that was applied, so a
 * test can distinguish "the guard fired" from "the guard fired but the mutation had
 * already landed".
 */
async function runtime({ mode = "verify", body = {}, tables = {}, auth = {}, method = "POST", authHeader = "Bearer tok", jwtFails = false } = {}) {
  const rows = { ...baseTables(), ...tables };
  const writes = [];
  let nextId = 1000;

  const matches = (row, filters) => filters.every(([col, val]) => row[col] === val);

  const db = {
    from(table) {
      const filters = [];
      let op = "select";
      let payload = null;
      let ordered = false;
      const chain = {
        select() { return chain; },
        eq(col, val) { filters.push([col, val]); return chain; },
        order() { ordered = true; return chain; },
        limit() { return chain; },
        insert(row) { op = "insert"; payload = row; return chain; },
        update(patch) { op = "update"; payload = patch; return chain; },
        maybeSingle: async () => {
          const found = rows[table].filter((r) => matches(r, filters));
          return { data: found[0] ?? null, error: null };
        },
        single: async () => {
          if (op === "insert") {
            const created = { id: `gen-${nextId++}`, ...payload };
            rows[table].push(created);
            writes.push({ op: "insert", table, row: created });
            return { data: created, error: null };
          }
          const found = rows[table].filter((r) => matches(r, filters));
          if (!found.length) return { data: null, error: { message: "no rows returned" } };
          const updated = { ...found[0], ...payload };
          rows[table][rows[table].indexOf(found[0])] = updated;
          writes.push({ op: "update", table, patch: payload, row: updated });
          return { data: updated, error: null };
        },
        then(resolve, reject) {
          let out = rows[table].filter((r) => matches(r, filters));
          if (ordered) out = [...out].sort((a, b) => String(b.updated_at ?? "").localeCompare(String(a.updated_at ?? "")));
          return resolve({ data: out, error: null });
        },
      };
      return chain;
    },
  };

  let handler;
  const context = {
    Deno: {
      serve: (fn) => { handler = fn; },
      env: { get: (k) => ({ SUPABASE_URL: "https://stub.supabase.co", SUPABASE_SERVICE_ROLE_KEY: "sb-secret" })[k] },
    },
    createClient: () => db,
    jwtVerify: async () => {
      if (jwtFails) throw new Error("JWKS signature verification failed");
      return {
        payload: {
          repository: "SoulSchoolAcademy/NayaPOWER",
          workflow_ref: "SoulSchoolAcademy/NayaPOWER/.github/workflows/live-supabase-runtime-proof.yml@refs/heads/main",
          ref: "refs/heads/main",
          jti: "jti-1",
          ...auth,
        },
      };
    },
    createRemoteJWKSet: () => ({}),
    // The handler logs every refusal to stderr. That is correct runtime behaviour, but
    // here it would bury the test report under 30 stack traces that are the EXPECTED
    // outcome. Keep console.error reachable so nothing is hidden; just route it away.
    console: { ...console, error: () => {}, log: () => {}, warn: () => {} },
    URL,
    Request,
    Response,
    Promise,
    Date,
    JSON,
    Boolean,
    Object,
    Array,
    String,
    Number,
    Error,
  };
  vm.createContext(context);
  new vm.Script(code, { filename: "nayanet-learning-verify/index.ts" }).runInContext(context);

  const req = {
    method,
    headers: { get: (h) => (h === "authorization" ? authHeader : null) },
    json: async () => ({ mode, ...body }),
  };
  const res = await handler(req);
  return { status: res.status, body: await res.json(), rows, writes };
}

// ---------------------------------------------------------------------------
// Authentication / transport guards
// ---------------------------------------------------------------------------

test("METHOD_NOT_ALLOWED -- a GET is refused, not handled", async () => {
  const { status, body } = await runtime({ method: "GET" });
  assert.equal(status, 405);
  assert.equal(body.error, "METHOD_NOT_ALLOWED");
});

test("RUNTIME_IDENTITY_REQUIRED -- no bearer token", async () => {
  const { body } = await runtime({ authHeader: "" });
  assert.equal(body.error, "RUNTIME_IDENTITY_REQUIRED");
});

test("GITHUB_OIDC_INVALID -- a token whose signature cannot be verified", async () => {
  // Executed, not asserted from source. The catch arm at index.ts:33 is what turns a
  // bad token into a refusal, and it is the arm that decides whether an unverifiable
  // caller is rejected or silently treated as authenticated.
  const { body } = await runtime({ jwtFails: true });
  assert.equal(body.error, "GITHUB_OIDC_INVALID");
});

test("WORKFLOW_BINDING_MISMATCH -- a token from the wrong repository", async () => {
  const { body } = await runtime({ auth: { repository: "attacker/NayaPOWER" } });
  assert.equal(body.error, "WORKFLOW_BINDING_MISMATCH");
});

test("WORKFLOW_BINDING_MISMATCH -- a token from the wrong ref", async () => {
  const { body } = await runtime({ auth: { ref: "refs/heads/evil-branch" } });
  assert.equal(body.error, "WORKFLOW_BINDING_MISMATCH");
});

// ---------------------------------------------------------------------------
// candidate mode: the chain must actually exist
// ---------------------------------------------------------------------------

test("INTELLIGENT_BLOCK_ID_REQUIRED -- candidate with no block id", async () => {
  const { status, body } = await runtime({ mode: "candidate", body: {}, tables: candidateTables() });
  assert.equal(status, 400);
  assert.equal(body.error, "INTELLIGENT_BLOCK_ID_REQUIRED");
});

test("INTELLIGENT_BLOCK_NOT_FOUND -- candidate for a block that does not exist", async () => {
  const { status, body } = await runtime({ mode: "candidate", body: { intelligent_block_id: "NOPE" }, tables: candidateTables() });
  assert.equal(status, 404);
  assert.equal(body.error, "INTELLIGENT_BLOCK_NOT_FOUND");
});

test("BLOCK_NOT_REVALIDATABLE -- a block already past the revalidation states", async () => {
  const t = candidateTables();
  t.nayanet_intelligent_blocks[0].understanding_state = "VERIFIED";
  const { status, body } = await runtime({ mode: "candidate", body: { intelligent_block_id: "IB-1" }, tables: t });
  assert.equal(status, 409);
  assert.equal(body.error, "BLOCK_NOT_REVALIDATABLE");
  assert.equal(body.state, "VERIFIED");
});

test("BLOCK_PROVENANCE_INCOMPLETE -- a block whose first evidence ref has no event id", async () => {
  const t = candidateTables();
  t.nayanet_intelligent_blocks[0].evidence_refs = [{ receipt_id: "RC1" }];
  const { status, body } = await runtime({ mode: "candidate", body: { intelligent_block_id: "IB-1" }, tables: t });
  assert.equal(status, 409);
  assert.equal(body.error, "BLOCK_PROVENANCE_INCOMPLETE");
});

test("SOURCE_EVENT_NOT_FOUND -- the evidence ref points at a missing event", async () => {
  const t = candidateTables();
  t.nayanet_cognition_events = [];
  const { status, body } = await runtime({ mode: "candidate", body: { intelligent_block_id: "IB-1" }, tables: t });
  assert.equal(status, 409);
  assert.equal(body.error, "SOURCE_EVENT_NOT_FOUND");
});

test("LINEAGE_NOT_FOUND -- event exists but nothing derives from it", async () => {
  const t = candidateTables();
  t.nayanet_intelligence_lineage = [];
  const { status, body } = await runtime({ mode: "candidate", body: { intelligent_block_id: "IB-1" }, tables: t });
  assert.equal(status, 409);
  assert.equal(body.error, "LINEAGE_NOT_FOUND");
});

test("RELATIONSHIP_NOT_FOUND -- no relationship targets the block", async () => {
  const t = candidateTables();
  t.nayanet_brain_relationships = [];
  const { status, body } = await runtime({ mode: "candidate", body: { intelligent_block_id: "IB-1" }, tables: t });
  assert.equal(status, 409);
  assert.equal(body.error, "RELATIONSHIP_NOT_FOUND");
});

test("INDEX_NOT_FOUND -- the block was never indexed", async () => {
  const t = candidateTables();
  t.nayanet_intelligence_index = [];
  const { status, body } = await runtime({ mode: "candidate", body: { intelligent_block_id: "IB-1" }, tables: t });
  assert.equal(status, 409);
  assert.equal(body.error, "INDEX_NOT_FOUND");
});

test("CHECKPOINT_PROVENANCE_MISMATCH -- a named checkpoint that does not exist", async () => {
  const { status, body } = await runtime({ mode: "candidate", body: { intelligent_block_id: "IB-1", checkpoint_id: "NOPE" }, tables: candidateTables() });
  assert.equal(status, 409);
  assert.equal(body.error, "CHECKPOINT_PROVENANCE_MISMATCH");
  assert.equal(body.reason, "CHECKPOINT_NOT_FOUND");
});

test("CHECKPOINT_PROVENANCE_MISMATCH -- a rebuilt chain disagrees AND no immutable receipt backs it", async () => {
  const t = candidateTables();
  t.nayanet_project_cognition_state[0].state.relationship_id = "WRONG";
  t.nayanet_execution_receipts[0].evidence = {};
  const { status, body } = await runtime({ mode: "candidate", body: { intelligent_block_id: "IB-1" }, tables: t });
  assert.equal(status, 409);
  assert.equal(body.error, "CHECKPOINT_PROVENANCE_MISMATCH");
  assert.equal(body.immutable_receipt_reconstruction, false);
  // The guard must NAME which link disagrees, or it reproduces the SUPABASE_READ_400
  // observability dead end.
  assert.ok([...body.mismatched].some((m) => m.field === "relationship_id"));
});

test("LESSON_CONTENT_REQUIRED -- a block with no lesson text", async () => {
  const t = candidateTables();
  t.nayanet_intelligent_blocks[0].content = { lesson: "   " };
  const { status, body } = await runtime({ mode: "candidate", body: { intelligent_block_id: "IB-1" }, tables: t });
  assert.equal(status, 409);
  assert.equal(body.error, "LESSON_CONTENT_REQUIRED");
});

test("AMBIGUOUS_EXISTING_LEARNING_CANDIDATES -- two candidates match, so neither is trusted", async () => {
  const t = candidateTables();
  t.learning_evidence = [
    { id: "LC1", member_id: OWNER, target_id: "NAYA-NODE-0001", status: "CANDIDATE", claim: "x", observed_value: { intelligent_block_id: "IB-1" } },
    { id: "LC2", member_id: OWNER, target_id: "NAYA-NODE-0001", status: "CANDIDATE", claim: "y", observed_value: { intelligent_block_id: "IB-1" } },
  ];
  const { status, body } = await runtime({ mode: "candidate", body: { intelligent_block_id: "IB-1" }, tables: t });
  assert.equal(status, 409);
  assert.equal(body.error, "AMBIGUOUS_EXISTING_LEARNING_CANDIDATES");
  assert.deepEqual([...body.candidate_ids].sort(), ["LC1", "LC2"]);
});

test("candidate POSITIVE CONTROL -- a whole intact chain produces a CANDIDATE, never ACTIVE", async () => {
  const { status, body, writes } = await runtime({ mode: "candidate", body: { intelligent_block_id: "IB-1" }, tables: candidateTables() });
  assert.equal(status, 200);
  assert.equal(body.ok, true);
  assert.equal(body.created, true);
  assert.equal(body.learning.status, "CANDIDATE");
  // The lesson text contains a task-class trigger, but text may only PROPOSE.
  // APPLICABLE requires a provenance-attested declaration (H8-7).
  const rel = writes.find((w) => w.op === "insert" && w.table === "learning_evidence");
  assert.ok(rel);
  assert.match(rel.row.observed_value.checkpoint_provenance, /CURRENT_STATE_MATCH/);
});

// ---------------------------------------------------------------------------
// reread mode
// ---------------------------------------------------------------------------

test("LEARNING_ID_REQUIRED -- no learning id", async () => {
  const { status, body } = await runtime({ body: {} });
  assert.equal(status, 400);
  assert.equal(body.error, "LEARNING_ID_REQUIRED");
});

test("LEARNING_NOT_FOUND -- reread of a learning row that does not exist", async () => {
  const { status, body } = await runtime({ mode: "reread", body: { learning_id: "NOPE" } });
  assert.equal(status, 404);
  assert.equal(body.error, "LEARNING_NOT_FOUND");
});

test("reread POSITIVE CONTROL -- reports the real integration state, including when lock-in never happened", async () => {
  const { body } = await runtime({ mode: "reread", body: { learning_id: "L1" } });
  assert.equal(body.ok, true);
  assert.equal(body.independent_reread, true);
  assert.equal(body.integration.core_intelligence_updated, false);
  assert.equal(body.integration.progressive_intelligence_lock_in, false);
});

// ---------------------------------------------------------------------------
// verify mode -- the lock-in
// ---------------------------------------------------------------------------

test("LEARNING_NOT_FOUND -- verify of a learning row that does not exist", async () => {
  const { status, body } = await runtime({ body: { learning_id: "NOPE", evidence_refs: ["CVO-1"] } });
  assert.equal(status, 404);
  assert.equal(body.error, "LEARNING_NOT_FOUND");
});

test("EVIDENCE_REQUIRED -- an empty evidence_refs array does not verify anything", async () => {
  const { body } = await runtime({ body: { learning_id: "L1", evidence_refs: [] } });
  assert.equal(body.verified, false);
  assert.equal(body.reason, "EVIDENCE_REQUIRED");
});

test("RECEIPT_NOT_FOUND_OR_NOT_OWNED -- a receipt that is not the owner's", async () => {
  const { status, body } = await runtime({ body: { learning_id: "L1", evidence_refs: ["CVO-1"], receipt_id: "RC-NOT-MINE" } });
  assert.equal(status, 404);
  assert.equal(body.error, "RECEIPT_NOT_FOUND_OR_NOT_OWNED");
});

test("LEARNING_PROVENANCE_LINKS_REQUIRED -- a learning row missing its chain links", async () => {
  const t = baseTables();
  t.learning_evidence[0].observed_value = { intelligent_block_id: "IB-1" };
  const { status, body } = await runtime({ body: { learning_id: "L1", evidence_refs: ["CVO-1"] }, tables: t });
  assert.equal(status, 409);
  assert.equal(body.error, "LEARNING_PROVENANCE_LINKS_REQUIRED");
});

test("LEARNING_LOCK_IN_LAW_DENIED -- no authority grant at all", async () => {
  const { status, body } = await runtime({ body: { learning_id: "L1", evidence_refs: ["CVO-1"] }, tables: baseTables({ nayanet_authority_grants: [] }) });
  assert.equal(status, 403);
  assert.equal(body.error, "LEARNING_LOCK_IN_LAW_DENIED");
  assert.equal(body.reason, "NO_MATCHING_ACTIVE_AUTHORITY");
});

test("LEARNING_LOCK_IN_LAW_DENIED -- a revoked grant names itself as the reason", async () => {
  const t = baseTables();
  t.nayanet_authority_grants[0].status = "REVOKED";
  const { status, body } = await runtime({ body: { learning_id: "L1", evidence_refs: ["CVO-1"] }, tables: t });
  assert.equal(status, 403);
  assert.equal(body.reason, "GRANT_REVOKED");
  assert.equal(body.authority_refs.length, 1);
  assert.equal(body.authority_refs[0], "G1");
});

test("LEARNING_LOCK_IN_LAW_DENIED -- an expired grant, and the expiry comparison is real", async () => {
  const t = baseTables();
  t.nayanet_authority_grants[0].expires_at = "2020-01-01T00:00:00.000Z";
  const { status, body } = await runtime({ body: { learning_id: "L1", evidence_refs: ["CVO-1"] }, tables: t });
  assert.equal(status, 403);
  assert.equal(body.reason, "GRANT_EXPIRED");
});

test("LEARNING_LOCK_IN_LAW_DENIED -- a grant scoped to a different block", async () => {
  const t = baseTables();
  t.nayanet_authority_grants[0].scope = { target: "IB-SOMETHING-ELSE" };
  const { status, body } = await runtime({ body: { learning_id: "L1", evidence_refs: ["CVO-1"] }, tables: t });
  assert.equal(status, 403);
  assert.equal(body.reason, "NO_MATCHING_ACTIVE_AUTHORITY");
});

test("LEARNING_LOCK_IN_LAW_DENIED -- a grant that does not name the learning_lock_in action", async () => {
  const t = baseTables();
  t.nayanet_authority_grants[0].actions = ["something_else"];
  const { status, body } = await runtime({ body: { learning_id: "L1", evidence_refs: ["CVO-1"] }, tables: t });
  assert.equal(status, 403);
  assert.equal(body.reason, "NO_MATCHING_ACTIVE_AUTHORITY");
});

test("HISTORICAL_COMMIT_RECEIPT_REQUIRED -- historical provenance with no receipt id", async () => {
  const t = baseTables();
  t.learning_evidence[0].observed_value.checkpoint_provenance = "IMMUTABLE_COMMIT_RECEIPT_SNAPSHOT";
  delete t.learning_evidence[0].observed_value.commit_receipt_id;
  const { status, body } = await runtime({ body: { learning_id: "L1", evidence_refs: ["CVO-1"] }, tables: t });
  assert.equal(status, 409);
  assert.equal(body.error, "HISTORICAL_COMMIT_RECEIPT_REQUIRED");
});

test("HISTORICAL_COMMIT_RECEIPT_NOT_FOUND -- the immutable receipt is missing", async () => {
  const t = baseTables();
  t.learning_evidence[0].observed_value.checkpoint_provenance = "IMMUTABLE_COMMIT_RECEIPT_SNAPSHOT";
  t.nayanet_execution_receipts = [];
  const { status, body } = await runtime({ body: { learning_id: "L1", evidence_refs: ["CVO-1"] }, tables: t });
  assert.equal(status, 409);
  assert.equal(body.error, "HISTORICAL_COMMIT_RECEIPT_NOT_FOUND");
});

test("INTELLIGENT_BLOCK_NOT_FOUND_FOR_LOCK_IN -- the block vanished between candidate and verify", async () => {
  const { status, body } = await runtime({ body: { learning_id: "L1", evidence_refs: ["CVO-1"] }, tables: baseTables({ nayanet_intelligent_blocks: [] }) });
  assert.equal(status, 404);
  assert.equal(body.error, "INTELLIGENT_BLOCK_NOT_FOUND_FOR_LOCK_IN");
});

test("INTELLIGENT_BLOCK_LOCK_IN_STATE_INVALID -- the block is no longer lockable", async () => {
  const t = baseTables();
  t.nayanet_intelligent_blocks[0].understanding_state = "SUPERSEDED";
  const { status, body } = await runtime({ body: { learning_id: "L1", evidence_refs: ["CVO-1"] }, tables: t });
  assert.equal(status, 409);
  assert.equal(body.error, "INTELLIGENT_BLOCK_LOCK_IN_STATE_INVALID");
  assert.equal(body.state, "SUPERSEDED");
});

test("RELATIONSHIP_NOT_FOUND_FOR_LOCK_IN -- the relationship vanished", async () => {
  const { status, body } = await runtime({ body: { learning_id: "L1", evidence_refs: ["CVO-1"] }, tables: baseTables({ nayanet_brain_relationships: [] }) });
  assert.equal(status, 404);
  assert.equal(body.error, "RELATIONSHIP_NOT_FOUND_FOR_LOCK_IN");
});

test("CHECKPOINT_NOT_FOUND_FOR_LOCK_IN -- the checkpoint vanished", async () => {
  const { status, body } = await runtime({ body: { learning_id: "L1", evidence_refs: ["CVO-1"] }, tables: baseTables({ nayanet_project_cognition_state: [] }) });
  assert.equal(status, 404);
  assert.equal(body.error, "CHECKPOINT_NOT_FOUND_FOR_LOCK_IN");
});

// ---------------------------------------------------------------------------
// POSITIVE CONTROL for the lock-in: all three canonical mutations, with the
// grant recorded. Without this the guards above could all fire and the happy
// path could still be broken.
// ---------------------------------------------------------------------------

test("verify POSITIVE CONTROL -- an authorized, intact chain performs the full lock-in", async () => {
  const { status, body, rows, writes } = await runtime({
    body: { learning_id: "L1", evidence_refs: ["CVO-777"], receipt_id: "RC1", verification_method: "Independent runtime verification." },
  });
  assert.equal(status, 200);
  assert.equal(body.ok, true);
  assert.equal(body.result.verified, true);

  assert.equal(rows.learning_evidence[0].status, "ACTIVE");
  assert.equal(rows.learning_evidence[0].provenance, "VERIFICATION");
  assert.equal(rows.nayanet_intelligent_blocks[0].understanding_state, "LEARNED");
  assert.equal(rows.nayanet_brain_relationships[0].epistemic_state, "VERIFIED");
  assert.equal(rows.nayanet_project_cognition_state[0].state.status, "LEARNED");

  // LAW must be recorded in the provenance of every canonical mutation, not merely
  // consulted. A decision nobody can audit is not a decision.
  assert.equal(rows.nayanet_intelligent_blocks[0].provenance.law_authority_refs.length, 1);
  assert.equal(rows.nayanet_intelligent_blocks[0].provenance.law_authority_refs[0], "G1");
  assert.equal(rows.nayanet_intelligent_blocks[0].provenance.law_decision_reason, "ACTIVE_IN_SCOPE_GRANT");
  assert.equal(rows.nayanet_brain_relationships[0].provenance.law_decision_reason, "ACTIVE_IN_SCOPE_GRANT");
  assert.equal(rows.nayanet_project_cognition_state[0].state.law_authority_refs[0], "G1");

  // The causal verification id must be carried through, not dropped.
  assert.equal(rows.nayanet_intelligent_blocks[0].provenance.learning_id, "L1");
  assert.equal(rows.nayanet_brain_relationships[0].provenance.causal_verification_id, "CVO-777");

  // The receipt must carry the verification record.
  assert.ok([...rows.nayanet_execution_receipts[0].learning].some((e) => e.learning_id === "L1" && e.verified === true));

  assert.ok(writes.length >= 5);
});

test("verify POSITIVE CONTROL -- the causal verification id reaches EVERY canonical provenance", async () => {
  // The three mutations each embed a causal_verification_id. If one of them drops it,
  // the graph carries a verified lock-in with no trace of the verification that caused
  // it, and no later reader can tell. That is the shape of an unfalsifiable receipt.
  const { rows } = await runtime({ body: { learning_id: "L1", evidence_refs: ["CVO-777"], receipt_id: "RC1" } });
  assert.equal(rows.nayanet_brain_relationships[0].provenance.causal_verification_id, "CVO-777");
  assert.equal(rows.nayanet_project_cognition_state[0].state.causal_verification_id, "CVO-777");
  assert.equal(rows.learning_evidence[0].observed_value.checkpoint_id, "C1");
});

test("verify is idempotent for one token -- the same verification is not double-recorded", async () => {
  const { rows } = await runtime({ body: { learning_id: "L1", evidence_refs: ["CVO-777"], receipt_id: "RC1" } });
  const recorded = rows.nayanet_execution_receipts[0].learning.filter((e) => e.learning_id === "L1" && e.verified === true);
  assert.equal(recorded.length, 1);
});

// ---------------------------------------------------------------------------
// CV-06 -- the LAW gate is ordered AFTER the mutations it guards
// ---------------------------------------------------------------------------

test("CV-06 -- LAW denies, the 403 is returned, AND the learning row is already promoted", async () => {
  const { status, body, rows, writes } = await runtime({
    body: { learning_id: "L1", evidence_refs: ["CVO-777"], receipt_id: "RC1" },
    tables: baseTables({ nayanet_authority_grants: [] }),
  });

  // The refusal is real.
  assert.equal(status, 403);
  assert.equal(body.error, "LEARNING_LOCK_IN_LAW_DENIED");

  // And so is the fail-open it was supposed to prevent. This is the defect.
  assert.equal(rows.learning_evidence[0].status, "ACTIVE");
  assert.equal(rows.learning_evidence[0].provenance, "VERIFICATION");
  assert.ok(
    writes.some((w) => w.op === "update" && w.table === "learning_evidence"),
    "learning_evidence was promoted despite the LAW denial"
  );

  // The receipt has also been written with verified: true.
  assert.ok(
    rows.nayanet_execution_receipts[0].learning.some((e) => e.learning_id === "L1" && e.verified === true),
    "an execution receipt records verified:true for a lock-in LAW denied"
  );
});

test("CV-06 -- the block/relationship/checkpoint ARE correctly untouched on denial", async () => {
  const { rows } = await runtime({
    body: { learning_id: "L1", evidence_refs: ["CVO-777"] },
    tables: baseTables({ nayanet_authority_grants: [] }),
  });
  // Worth stating explicitly: the graph mutations DO sit behind the gate. The leak is
  // scoped to learning_evidence and the receipt, which is exactly the sort of partial
  // fail-open that a review of "does the LAW gate work?" would wave through.
  assert.equal(rows.nayanet_intelligent_blocks[0].understanding_state, "CANDIDATE");
  assert.equal(rows.nayanet_brain_relationships[0].epistemic_state, "CANDIDATE");
  assert.equal(rows.nayanet_project_cognition_state[0].state.status, "CANDIDATE");
});

test("CV-06 -- RECEIPT_NOT_FOUND_OR_NOT_OWNED has the same leak: the row is already ACTIVE", async () => {
  const { status, body, rows } = await runtime({
    body: { learning_id: "L1", evidence_refs: ["CVO-777"], receipt_id: "RC-NOT-MINE" },
  });
  assert.equal(status, 404);
  assert.equal(body.error, "RECEIPT_NOT_FOUND_OR_NOT_OWNED");
  assert.equal(rows.learning_evidence[0].status, "ACTIVE");
});

// ---------------------------------------------------------------------------
// CV-07 -- evidence_refs is never checked to be evidence
// ---------------------------------------------------------------------------

test("CV-07 -- arbitrary strings promote the learning and are recorded as verification", async () => {
  const { status, body, rows } = await runtime({
    body: { learning_id: "L1", evidence_refs: ["not-a-verification", "", "0"] },
  });
  assert.equal(status, 200);
  assert.equal(body.ok, true);
  assert.equal(rows.learning_evidence[0].status, "ACTIVE");
  assert.equal(rows.nayanet_intelligent_blocks[0].understanding_state, "LEARNED");
  assert.equal(rows.nayanet_brain_relationships[0].epistemic_state, "VERIFIED");
});

test("CV-07 -- the causal_verification_id is silently null in the canonical provenance", async () => {
  const { status, body, rows } = await runtime({ body: { learning_id: "L1", evidence_refs: ["not-a-verification"] } });
  assert.equal(status, 200);
  assert.equal(body.ok, true);
  // The runtime performed a verified lock-in and recorded that NO causal verification
  // exists. Nothing in the response says so -- ok:true, verified:true, LEARNED, and a
  // provenance object that quietly contains causal_verification_id: null.
  assert.equal(rows.nayanet_brain_relationships[0].provenance.causal_verification_id, null);
  assert.equal(rows.nayanet_project_cognition_state[0].state.causal_verification_id, null);
});

test("CV-07 -- a single valid-looking prefix among junk is accepted as the verification id", async () => {
  const { rows } = await runtime({ body: { learning_id: "L1", evidence_refs: ["junk", "CVO-forged"] } });
  assert.equal(rows.nayanet_brain_relationships[0].provenance.causal_verification_id, "CVO-forged");
});

// ---------------------------------------------------------------------------
// H8-7: applicability is a governed assertion, never text-derived
// ---------------------------------------------------------------------------

test("H8-7 -- lesson text alone may never yield APPLICABLE", async () => {
  const t = baseTables();
  t.nayanet_intelligent_blocks[0].content = { lesson: "preserve provenance before applying retained intelligence" };
  t.nayanet_intelligent_blocks[0].provenance = {};
  const { rows } = await runtime({ body: { learning_id: "L1", evidence_refs: ["CVO-777"] }, tables: t });
  const rel = rows.nayanet_brain_relationships[0];
  assert.equal(rel.applicability.state, "UNKNOWN");
  assert.ok([...rel.applicability.proposed_task_classes].includes("provenance_sensitive"));
  assert.ok([...rel.applicability.limitations].includes("TEXT_TRIGGER_WITHOUT_GOVERNED_DECLARATION"));
  assert.ok([...rel.reason_codes].includes("APPLICABILITY_UNCLASSIFIED"));
});

test("H8-7 -- a provenance-attested declaration DOES yield APPLICABLE, and is limited", async () => {
  const t = baseTables();
  t.nayanet_intelligent_blocks[0].provenance = { declared_task_classes: ["provenance_sensitive"] };
  const { rows } = await runtime({ body: { learning_id: "L1", evidence_refs: ["CVO-777"] }, tables: t });
  const rel = rows.nayanet_brain_relationships[0];
  assert.equal(rel.applicability.state, "APPLICABLE");
  assert.deepEqual([...rel.applicability.task_classes], ["provenance_sensitive"]);
  assert.ok(rel.applicability.limitations.length > 0);
  assert.ok([...rel.reason_codes].includes("TASK_APPLICABILITY_GOVERNED_DECLARATION"));
});

test("H8-7 -- an ungoverned class in the declaration is quarantined, not dropped", async () => {
  const t = baseTables();
  t.nayanet_intelligent_blocks[0].provenance = { declared_task_classes: ["provenance_sensitive", "invented_authority"] };
  const { rows } = await runtime({ body: { learning_id: "L1", evidence_refs: ["CVO-777"] }, tables: t });
  const rel = rows.nayanet_brain_relationships[0];
  assert.deepEqual([...rel.applicability.task_classes], ["provenance_sensitive"]);
  assert.deepEqual([...rel.applicability.ungoverned_declared_task_classes], ["invented_authority"]);
});
