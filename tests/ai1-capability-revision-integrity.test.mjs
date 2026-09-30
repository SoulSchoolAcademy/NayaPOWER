import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";
import {
  CapabilityValidationError,
  validateCapabilities,
} from "../supabase/functions/nayanet-intelligence-commit-runtime/capability-vocabulary.ts";

const edge = readFileSync(new URL(
  "../supabase/functions/nayanet-intelligence-commit-runtime/index.ts",
  import.meta.url,
), "utf8");
const migration = readFileSync(new URL(
  "../supabase/migrations/20261001000100_ai1_supersede_capability_integrity_v1.sql",
  import.meta.url,
), "utf8");

test("AI1-REV-01: supersede runtime uses the same bounded capability validator", () => {
  assert.match(edge, /const capabilities = coerceCapabilities\(body\.p_capabilities\)/);
  assert.deepEqual(validateCapabilities([" Governance_Triage ", "governance_triage"]), ["governance_triage"]);
  assert.throws(
    () => validateCapabilities(["governance_triagee"]),
    (e) => e instanceof CapabilityValidationError && e.code === "CAPABILITY_UNKNOWN",
  );
});

test("AI1-REV-02: edge threads topic/category/capabilities through supersession", () => {
  assert.match(edge, /p_topic: body\.p_topic/);
  assert.match(edge, /p_category: body\.p_category/);
  assert.match(edge, /p_capabilities: capabilities/);
});

test("AI1-REV-03: SQL keeps legacy successor shape when richer fields are absent", () => {
  assert.match(migration, /v_content := jsonb_build_object\('lesson',p_content\)/);
  assert.match(migration, /if p_topic is not null then v_content := v_content \|\| jsonb_build_object\('topic',p_topic\)/);
  assert.match(migration, /if p_category is not null then v_content := v_content \|\| jsonb_build_object\('category',p_category\)/);
  assert.match(migration, /if v_capabilities is not null then v_content := v_content \|\| jsonb_build_object\('capabilities',to_jsonb\(v_capabilities\)\)/);
});

test("AI1-REV-04: SQL rejects unknown capability names and records declaration provenance", () => {
  assert.match(migration, /CAPABILITY_UNKNOWN:/);
  assert.match(migration, /capability_declaration/);
  assert.match(migration, /declared_capabilities/);
});

test("AI1-REV-05: revision metadata does not change authority or state policy", () => {
  assert.match(migration, /actions @> '\["intelligence_commit"\]'::jsonb/);
  assert.match(migration, /p_understanding_state text default 'CANDIDATE'/);
  assert.doesNotMatch(migration, /LEARNED/);
});
