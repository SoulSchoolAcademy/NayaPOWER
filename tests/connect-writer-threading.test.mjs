import assert from "node:assert/strict";
import { readFileSync, readdirSync } from "node:fs";
import test from "node:test";

// CONNECT writer threading (migration 20260930050000 + edge-function
// modes): the R1 connections contract is exposed through the governed
// runtime bridges so the CONNECT live proof can write edges through the
// runtime. Structural tests -- the established repo pattern for
// SQL/edge changes that cannot run against a live DB from here
// (see tests/test_r1_writer_connections.py).

const MIGRATION_PATH = new URL(
  "../supabase/migrations/20260930050000_thread_connections_through_commit_bridge.sql",
  import.meta.url
);
const COMMIT_RUNTIME_PATH = new URL(
  "../supabase/functions/nayanet-intelligence-commit-runtime/index.ts",
  import.meta.url
);

const migration = readFileSync(MIGRATION_PATH, "utf8");
const commitRuntime = readFileSync(COMMIT_RUNTIME_PATH, "utf8");

test("CONNECT: migration file sorts after the R1 writer contract migration", () => {
  const files = readdirSync(new URL("../supabase/migrations/", import.meta.url));
  const r1 = files.find((f) => f.endsWith("_r1_writer_connections_v1.sql"));
  assert.ok(r1, "R1 writer contract migration must exist");
  assert.ok(
    "20260930050000_thread_connections_through_commit_bridge.sql" > r1,
    "threading migration must sort after the R1 writer contract"
  );
});

test("CONNECT: commit bridge signature gains trailing p_connections", () => {
  assert.match(
    migration,
    /create function public\.nayanet_intelligence_commit_runtime\([\s\S]*?p_connections jsonb default null/
  );
  // CREATE OR REPLACE cannot change an argument list, so the old signature
  // must be dropped first (same pattern as the R1 migration itself).
  assert.match(
    migration,
    /drop function if exists public\.nayanet_intelligence_commit_runtime\(text,uuid,text,text,text,text,text,text,text,uuid,text\)/
  );
});

test("CONNECT: commit bridge threads p_connections into the R1 commit writer", () => {
  assert.match(
    migration,
    /public\.nayanet_intelligence_commit\(p_event_id,p_title,p_content,p_category,p_topic,p_target_id,p_authority_grant_id,p_project_id,p_connections\)/
  );
});

test("CONNECT: supersede bridge exists with p_connections and authority checks", () => {
  assert.match(
    migration,
    /create function public\.nayanet_supersede_intelligent_block_runtime\([\s\S]*?p_connections jsonb default null/
  );
  assert.ok(migration.includes("NAYA_ID_NOT_AUTHORIZED"), "naya_id check kept");
  assert.ok(migration.includes("RUNTIME_JTI_REQUIRED"), "jti check kept");
  assert.ok(migration.includes("AUTHORITY_BLOCKED"), "authority grant check kept");
  assert.ok(
    migration.includes(`actions @> '["intelligence_commit"]'::jsonb`),
    "supersede bridge requires the intelligence_commit grant action"
  );
  assert.ok(
    migration.includes("set_config('request.jwt.claim.sub',p_owner_id::text,true)"),
    "jwt claim propagation kept"
  );
});

test("CONNECT: supersede bridge calls the promoted supersession writer with eligible defaults", () => {
  assert.match(migration, /public\.nayanet_supersede_intelligent_block\(/);
  // evidence_refs must be non-empty or the new row is ineligible for
  // retrieval (know.ts isEligibleBlock) and the positive proof cannot pass.
  assert.ok(migration.includes("idempotency_key"), "evidence envelope carries the idempotency key");
  assert.ok(
    migration.includes("jsonb_build_object('lesson',p_content)"),
    "content uses the governed lesson shape"
  );
});

test("CONNECT: bridges stay service_role-only (edge functions invoke, never direct client SQL)", () => {
  assert.match(
    migration,
    /revoke all on function public\.nayanet_intelligence_commit_runtime\(text,uuid,text,text,text,text,text,text,text,uuid,text,jsonb\) from public,anon,authenticated/
  );
  assert.match(
    migration,
    /grant execute on function public\.nayanet_intelligence_commit_runtime\(text,uuid,text,text,text,text,text,text,text,uuid,text,jsonb\) to service_role/
  );
  assert.match(
    migration,
    /revoke all on function public\.nayanet_supersede_intelligent_block_runtime\(text,uuid,text,uuid,text,uuid,text,text,text,text,text,text,jsonb\) from public,anon,authenticated/
  );
  assert.match(
    migration,
    /grant execute on function public\.nayanet_supersede_intelligent_block_runtime\(text,uuid,text,uuid,text,uuid,text,text,text,text,text,text,jsonb\) to service_role/
  );
});

test("CONNECT: commit-runtime validates and passes p_connections in execute mode", () => {
  assert.ok(commitRuntime.includes("function coerceConnections"), "edge validates candidate shape before RPC");
  assert.ok(commitRuntime.includes("P_CONNECTIONS_MUST_BE_ARRAY"), "non-array candidates fail before RPC");
  assert.match(commitRuntime, /p_connections:\s*coerceConnections\(body\.p_connections\)/);
});

test("CONNECT: commit-runtime edge function exposes a supersede mode threading p_connections", () => {
  assert.ok(commitRuntime.includes("nayanet_supersede_intelligent_block_runtime"), "supersede bridge RPC called");
  assert.match(commitRuntime, /async function callSupersede\(body: Json, jti: string\)/);
  assert.match(commitRuntime, /mode === "supersede"/);
  assert.ok(commitRuntime.includes("SUPERSEDE_FIELDS_REQUIRED"), "supersede mode fails closed on missing fields");
});

test("CONNECT: commit-runtime edge function allowlists both proof workflows", () => {
  assert.ok(
    commitRuntime.includes('".github/workflows/live-intelligence-commit-proof.yml"'),
    "existing commit-proof workflow still bound"
  );
  assert.ok(
    commitRuntime.includes('".github/workflows/live-connect-proof.yml"'),
    "new connect-proof workflow bound"
  );
  // The old single-WORKFLOW binding is gone; the allowlist drives authenticate().
  assert.ok(!commitRuntime.match(/const WORKFLOW = /), "single-workflow binding removed");
});

test("CONNECT: LAW and KNOW runtimes allowlist the connect proof workflow", () => {
  for (const fn of ["nayanet-law-runtime", "nayanet-know-runtime"]) {
    const src = readFileSync(
      new URL(`../supabase/functions/${fn}/index.ts`, import.meta.url),
      "utf8"
    );
    assert.ok(
      src.includes('".github/workflows/live-connect-proof.yml"'),
      `${fn} must allowlist live-connect-proof.yml`
    );
  }
});
