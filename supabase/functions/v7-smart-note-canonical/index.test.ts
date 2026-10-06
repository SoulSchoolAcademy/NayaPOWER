// Tests for the governed task-class declaration writer repair.
// The canonical capture contract must carry declared_task_classes through
// provenance so deriveGraphApplicability can return APPLICABLE for governed
// declarations. Unknown classes must fail closed (filtered, never applicable).

import { assertEquals } from "https://deno.land/std@0.208.0/assert/mod.ts";

// Mirror of the validation logic in v7-smart-note-canonical/index.ts
const GOVERNED_TASK_CLASSES = new Set([
  "provenance_sensitive",
  "repository_correction",
  "active_intelligence_sensitive",
  "learning_reuse",
  "contextual_retrieval",
]);

function validateDeclaredTaskClasses(raw: unknown): { governed: string[]; rejected: string[] } {
  if (!Array.isArray(raw)) return { governed: [], rejected: [] };
  const seen = new Set<string>();
  const governed: string[] = [];
  const rejected: string[] = [];
  for (const c of raw) {
    if (typeof c !== "string" || !c) continue;
    if (seen.has(c)) continue;
    seen.add(c);
    if (GOVERNED_TASK_CLASSES.has(c)) governed.push(c);
    else rejected.push(c);
  }
  return { governed, rejected };
}

Deno.test("governed declaration passes through", () => {
  const r = validateDeclaredTaskClasses(["provenance_sensitive", "learning_reuse"]);
  assertEquals(r.governed, ["provenance_sensitive", "learning_reuse"]);
  assertEquals(r.rejected, []);
});

Deno.test("unknown class fails closed", () => {
  const r = validateDeclaredTaskClasses(["provenance_sensitive", "evil_class", ""]);
  assertEquals(r.governed, ["provenance_sensitive"]);
  assertEquals(r.rejected, ["evil_class"]);
});

Deno.test("non-array input yields empty", () => {
  const r = validateDeclaredTaskClasses("provenance_sensitive");
  assertEquals(r.governed, []);
  assertEquals(r.rejected, []);
});

Deno.test("duplicates deduplicated", () => {
  const r = validateDeclaredTaskClasses(["learning_reuse", "learning_reuse"]);
  assertEquals(r.governed, ["learning_reuse"]);
  assertEquals(r.rejected, []);
});

Deno.test("empty input yields empty", () => {
  const r = validateDeclaredTaskClasses([]);
  assertEquals(r.governed, []);
  assertEquals(r.rejected, []);
});
