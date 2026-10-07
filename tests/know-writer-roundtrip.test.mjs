import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";
import { selectKnowContext } from "../supabase/functions/nayanet-know-runtime/know.ts";

// R1 writer contract round-trip: rows shaped EXACTLY as the SQL writers stamp
// them (migration 20260930040000_r1_writer_connections_v1.sql) must be
// consumable by the edge-aware retrieval seam (know.ts, PR #1094).
//
// Writer-stamped row shape for `connections`:
//   [{"target_block_id": "<intelligent_block_id IB-*>", "relationship_type": "<22-type>"}]
// produced by nayanet_normalize_block_connections(): vocabulary-checked,
// owner-scoped target resolution, deduplicated. The guard trigger rejects
// anything else at write time.

const OWNER = "owner-1";
const req = (overrides = {}) => ({
  owner_id: OWNER,
  naya_id: "NAYA-NODE-0001",
  task_id: "KNOW-R1-001",
  task_class: "WRITER_ROUNDTRIP",
  required_capability: "provenance_preservation",
  ...overrides,
});

// A block row as the writers persist it (post-migration column set).
const row = (overrides = {}) => ({
  intelligent_block_id: "IB-000101",
  owner_id: OWNER,
  status: "DURABLE",
  understanding_state: "VERIFIED",
  owner_scope: "PRIVATE",
  applicable_scope: { target: "NAYA-NODE-0001" },
  content: { lesson: "Preserve provenance before applying retained intelligence; retrieval never grants authority." },
  provenance: { source: "R1-TEST" },
  evidence_refs: [{ receipt: "r1-receipt-1" }],
  superseded_by_block_id: null,
  updated_at: "2026-09-29T00:00:00Z",
  connections: [],
  ...overrides,
});

test("R1: supersession writer output — old row carries SUPERSEDES edge, new row is selected", () => {
  // As stamped by nayanet_supersede_intelligent_block(PROMOTED_V1):
  // old row flipped to SUPERSEDED + edge appended; new row minted with a
  // fresh IB id, version+1, and the uuid chain link.
  const oldRow = row({
    intelligent_block_id: "IB-000101",
    status: "SUPERSEDED",
    superseded_by_block_id: "11111111-1111-1111-1111-111111111111",
    updated_at: "2026-09-30T00:00:00Z", // touched by the supersession update
    connections: [{ target_block_id: "IB-000102", relationship_type: "SUPERSEDES" }],
  });
  const newRow = row({
    intelligent_block_id: "IB-000102",
    status: "ACTIVE",
    updated_at: "2026-09-29T12:00:00Z",
    connections: [],
  });
  const out = selectKnowContext(req(), [oldRow, newRow]);
  assert.equal(out.status, "HIT");
  // The superseded row is ineligible; the successor is selected directly.
  // The stamped edge is well-formed and causes no adverse behavior.
  assert.equal(out.selected_block_id, "IB-000102");
  assert.equal(out.conflict_detected, false);
});

test("R1: SUPERSEDES edge in writer shape is chase-consumable", () => {
  // The edge the supersession writer stamps must be in the exact shape
  // chaseSupersession consumes: when an eligible block carries it, the
  // graph overrides flat recency toward the current truth.
  const successor = row({ intelligent_block_id: "IB-000202", updated_at: "2026-09-28T00:00:00Z" });
  const predecessor = row({
    intelligent_block_id: "IB-000201",
    updated_at: "2026-09-29T00:00:00Z",
    connections: [{ target_block_id: "IB-000202", relationship_type: "SUPERSEDES" }],
  });
  const out = selectKnowContext(req(), [predecessor, successor]);
  assert.equal(out.status, "HIT");
  assert.equal(out.selected_block_id, "IB-000202");
  assert.match(out.reason, /SUPERSEDES_EDGE_FOLLOWED:IB-000202/);
});

test("R1: upsert writer output — normalized SUPPORTS edge attaches related context", () => {
  // As stamped by nayanet_upsert_intelligent_block_from_smart_note after
  // nayanet_normalize_block_connections(): capture {type,target} pairs that
  // resolve become row-shape edges; prose targets and forged types are gone.
  const main = row({
    intelligent_block_id: "IB-000301",
    connections: [{ target_block_id: "IB-000302", relationship_type: "SUPPORTS" }],
  });
  const support = row({ intelligent_block_id: "IB-000302", understanding_state: "LEARNED" });
  const out = selectKnowContext(req(), [main, support]);
  assert.equal(out.status, "HIT");
  assert.equal(out.selected_block_id, "IB-000301");
  assert.equal(out.related_context.length, 1);
  assert.equal(out.related_context[0].block_id, "IB-000302");
  assert.equal(out.related_context[0].relationship_type, "SUPPORTS");
});

test("R1: writer output with empty connections preserves flat behavior", () => {
  // Fresh commit rows (nayanet_intelligence_commit with no p_connections)
  // stamp connections=[] — retrieval must be byte-identical to flat.
  const a = row({ intelligent_block_id: "IB-000401", updated_at: "2026-09-29T00:00:00Z", connections: [] });
  const b = row({ intelligent_block_id: "IB-000402", updated_at: "2026-09-28T00:00:00Z", connections: [] });
  const out = selectKnowContext(req(), [a, b]);
  assert.equal(out.status, "HIT");
  assert.equal(out.selected_block_id, "IB-000401");
  assert.equal(out.reason, "OWNER_SCOPED_CURRENT_BLOCK_MATCHES_REQUIRED_CAPABILITY");
  assert.deepEqual(out.related_context, []);
  assert.equal(out.conflict_detected, false);
});

test("R1: CONTRADICTS edge stamped by writer surfaces conflict", () => {
  const main = row({
    intelligent_block_id: "IB-000501",
    connections: [{ target_block_id: "IB-000502", relationship_type: "CONTRADICTS" }],
  });
  const rival = row({ intelligent_block_id: "IB-000502" });
  const out = selectKnowContext(req(), [main, rival]);
  assert.equal(out.status, "HIT");
  assert.equal(out.selected_block_id, "IB-000501");
  assert.equal(out.conflict_detected, true);
  assert.equal(out.related_context[0].relationship_type, "CONTRADICTS");
});

test("R1: migration vocabulary matches the canonical 22-type contract", () => {
  // The SQL writers, the guard trigger, and know.ts must all enforce the
  // SAME vocabulary, sourced from the canonical contract. If this test
  // fails, a writer and the retrieval disagree on what a real edge is.
  const schema = JSON.parse(readFileSync(new URL("../BRAIN/00-SPEC/BRAIN-MACHINE-CONTRACT-V1.schema.json", import.meta.url), "utf8"));
  const canonical = schema.$defs.relationshipType.enum;
  assert.equal(canonical.length, 22);
  const migration = readFileSync(new URL("../supabase/migrations/20260930040000_r1_writer_connections_v1.sql", import.meta.url), "utf8");
  for (const t of canonical) {
    assert.ok(migration.includes(`'${t}'`), `migration must list vocabulary type ${t}`);
  }
  // CONNECT-owned selector seam (2026-10-07): the vocabulary moved verbatim from
  // know.ts to supabase/functions/_shared/connect_selector.ts. know.ts imports
  // the gate; the invariant is unchanged — one vocabulary, matching canonical.
  const selector = readFileSync(new URL("../supabase/functions/_shared/connect_selector.ts", import.meta.url), "utf8");
  for (const t of canonical) {
    assert.ok(selector.includes(`"${t}"`), `connect_selector.ts must list vocabulary type ${t}`);
  }
});

test("R1: know-runtime fetch selects the connections column", () => {
  // Without this, writers stamp edges the runtime never reads and the
  // round-trip is silently broken.
  const index = readFileSync(new URL("../supabase/functions/nayanet-know-runtime/index.ts", import.meta.url), "utf8");
  assert.match(index, /\.select\("[^"]*connections[^"]*"\)/);
});
