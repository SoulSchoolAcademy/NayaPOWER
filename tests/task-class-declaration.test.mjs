import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";
import {
  TASK_CLASS_VALUES,
  TaskClassValidationError,
  buildDeclaredProvenance,
  validateTaskClasses,
} from "../supabase/functions/nayanet-intelligence-commit-runtime/task-class-vocabulary.ts";

// H8-7 writer closure (repair/naya4-task-class-writer): contract tests for the
// declared_task_classes writer <-> learning-verify reader seam.
//
// What these tests prove, and what they do NOT prove:
//   - They import the ACTUAL vocabulary module. Nothing is reimplemented;
//     there is no synthetic fallback.
//   - The persisted-shape builder (buildDeclaredProvenance) is the reference
//     implementation the SQL writer mirrors. The SQL itself cannot execute
//     here (no database in this environment); the migration text is asserted
//     separately (mirror-agreement test), and live-SQL execution remains a
//     reviewer-verified step. That limitation is stated, not hidden.
//   - The reader (nayanet-learning-verify deriveGraphApplicability) is a Deno
//     edge function and cannot be imported under node; the reader/writer
//     contract (writer-stamped provenance -> APPLICABLE) is proven in Deno
//     against the pin-exact shipped reader during the repair cycle. Here we
//     assert the structural contract the reader consumes.
//   - No alternate declaration path is exercised: only the governed capture
//     payload channel.

// ---------------------------------------------------------------------------
// 1. Vocabulary validation: valid / unknown / malformed / empty / duplicates /
//    wrong-type / case normalization — all deterministic.
// ---------------------------------------------------------------------------

test("TC-VOCAB-01: the bounded set is exactly the five H8-7 registry classes", () => {
  assert.deepEqual([...TASK_CLASS_VALUES].sort(), [
    "active_intelligence_sensitive",
    "contextual_retrieval",
    "learning_reuse",
    "provenance_sensitive",
    "repository_correction",
  ]);
});

test("TC-VOCAB-02: valid declarations validate to the sorted, deduped array", () => {
  assert.deepEqual(
    validateTaskClasses(["repository_correction", "provenance_sensitive"]),
    ["provenance_sensitive", "repository_correction"],
  );
  assert.deepEqual(
    validateTaskClasses(["learning_reuse", "learning_reuse"]),
    ["learning_reuse"],
  );
});

test("TC-VOCAB-03: normalization trims and lowercases", () => {
  assert.deepEqual(validateTaskClasses(["  Provenance_Sensitive "]), [
    "provenance_sensitive",
  ]);
});

test("TC-VOCAB-04: absent or empty input -> null (persist byte-identical)", () => {
  assert.equal(validateTaskClasses(undefined), null);
  assert.equal(validateTaskClasses(null), null);
  assert.equal(validateTaskClasses([]), null);
});

test("TC-VOCAB-05: unknown class -> TASK_CLASS_UNKNOWN (fail closed)", () => {
  assert.throws(() => validateTaskClasses(["graph_magic"]), (err) => {
    assert.ok(err instanceof TaskClassValidationError);
    assert.equal(err.code, "TASK_CLASS_UNKNOWN");
    return true;
  });
});

test("TC-VOCAB-06: malformed entries -> TASK_CLASS_MALFORMED (fail closed)", () => {
  for (const bad of ["", "   ", "has space", "UPPER-DASH", 42, null, "a".repeat(1) + "!"]) {
    assert.throws(() => validateTaskClasses([bad]), (err) => {
      assert.ok(err instanceof TaskClassValidationError);
      assert.equal(err.code, "TASK_CLASS_MALFORMED");
      return true;
    }, `input ${JSON.stringify(bad)} must be rejected`);
  }
});

test("TC-VOCAB-07: non-array input -> TASK_CLASS_MALFORMED", () => {
  assert.throws(() => validateTaskClasses("provenance_sensitive"), (err) => {
    assert.ok(err instanceof TaskClassValidationError);
    assert.equal(err.code, "TASK_CLASS_MALFORMED");
    return true;
  });
});

test("TC-VOCAB-08: one bad entry rejects the whole declaration", () => {
  assert.throws(
    () => validateTaskClasses(["provenance_sensitive", "nope"]),
    (err) => {
      assert.ok(err instanceof TaskClassValidationError);
      assert.equal(err.code, "TASK_CLASS_UNKNOWN");
      return true;
    },
  );
});

// ---------------------------------------------------------------------------
// 2. Persisted provenance shape: the exact shape the SQL writer stamps.
// ---------------------------------------------------------------------------

const PROV_BASE = {
  stage: "CAPTURE+PERSIST",
  source: "nayanet",
  authority_grant_id: "grant-1",
  source_event_id: "event-1",
};

test("TC-SHAPE-01: null declarations -> byte-identical base provenance", () => {
  assert.deepEqual(buildDeclaredProvenance(PROV_BASE, null), { ...PROV_BASE });
});

test("TC-SHAPE-02: declared classes stamp the reader contract + attestation", () => {
  const prov = buildDeclaredProvenance(
    PROV_BASE,
    validateTaskClasses(["provenance_sensitive"]),
  );
  assert.deepEqual(prov.declared_task_classes, ["provenance_sensitive"]);
  assert.deepEqual(prov.task_class_declaration, {
    source: "intelligence_commit_capture",
    values: ["provenance_sensitive"],
  });
  // Base keys preserved.
  assert.equal(prov.stage, "CAPTURE+PERSIST");
});

// ---------------------------------------------------------------------------
// 3. Reader-consumption contract (structural): what deriveGraphApplicability
//    reads from a writer-stamped block.
// ---------------------------------------------------------------------------

test("TC-READER-CONTRACT-01: stamped provenance satisfies the reader's input contract", () => {
  // The reader (nayanet-learning-verify/index.ts) does:
  //   const declaredRaw = block?.provenance?.declared_task_classes;
  //   const declared = Array.isArray(declaredRaw)
  //     ? declaredRaw.filter((c) => typeof c === "string") : [];
  //   const governed = declared.filter((c) => c in TASK_CLASS_REGISTRY);
  //   APPLICABLE iff governed.length > 0.
  const block = { provenance: buildDeclaredProvenance(PROV_BASE, validateTaskClasses(["learning_reuse", "contextual_retrieval"])) };
  const declaredRaw = block.provenance.declared_task_classes;
  assert.ok(Array.isArray(declaredRaw));
  const declared = declaredRaw.filter((c) => typeof c === "string");
  assert.deepEqual(declared, ["contextual_retrieval", "learning_reuse"]);
  // Every declared string is a registry member (writer-side enforcement).
  const registry = new Set(TASK_CLASS_VALUES);
  assert.ok(declared.every((c) => registry.has(c)));
  assert.ok(declared.length > 0, "reader would return APPLICABLE");
});

test("TC-READER-CONTRACT-02: undeclared block -> reader sees empty declaration", () => {
  const block = { provenance: buildDeclaredProvenance(PROV_BASE, null) };
  assert.equal(block.provenance.declared_task_classes, undefined);
});

// ---------------------------------------------------------------------------
// 4. SQL mirror agreement: the migration mirrors the canonical vocabulary.
// ---------------------------------------------------------------------------

const MIGRATION_PATH = "../supabase/migrations/20261006021500_declared_task_classes_commit_writer_v1.sql";

test("TC-MIRROR-01: SQL mirror agrees with the canonical vocabulary (no second taxonomy)", () => {
  const migration = readFileSync(new URL(MIGRATION_PATH, import.meta.url), "utf8");
  assert.match(migration, /task-class-vocabulary\.ts/, "migration must name its canonical owner");
  for (const v of TASK_CLASS_VALUES) {
    assert.ok(migration.includes(`'${v}'`), `migration must mirror vocabulary value ${v}`);
  }
  // The mirror must be exactly the bounded set: the literals in the
  // task-class validation array (anchored on v_tc_norm) must equal the
  // vocabulary size.
  const mirror = migration.match(/v_tc_norm <> all \(array\[([^\]]*)\]\)/);
  assert.ok(mirror, "validation array literal must be present");
  const literals = mirror[1].split(",").map((s) => s.trim().replace(/^'|'$/g, ""));
  assert.deepEqual(literals.sort(), [...TASK_CLASS_VALUES].sort());
});

test("TC-MIRROR-02: migration stamps the reader contract and fails closed", () => {
  const migration = readFileSync(new URL(MIGRATION_PATH, import.meta.url), "utf8");
  assert.match(migration, /TASK_CLASS_MALFORMED/);
  assert.match(migration, /TASK_CLASS_UNKNOWN/);
  assert.match(migration, /'declared_task_classes', to_jsonb\(v_task_classes\)/);
  assert.match(migration, /EVENT_ID_REPLAY_PAYLOAD_MISMATCH/);
  // Wrapper threads the new parameter through the runtime bridge.
  assert.match(migration, /p_declared_task_classes text\[\] default null/);
  assert.match(
    migration,
    /nayanet_intelligence_commit\(p_event_id,p_title,p_content,p_category,p_topic,p_target_id,p_authority_grant_id,p_project_id,p_connections,p_capabilities,p_declared_task_classes\)/,
  );
});

// ---------------------------------------------------------------------------
// 5. Edge function wiring: validate + forward on commit; explicit reject on
//    supersede (no silent drop).
// ---------------------------------------------------------------------------

test("TC-EDGE-01: edge function validates and forwards declared_task_classes on commit", () => {
  const index = readFileSync(
    new URL("../supabase/functions/nayanet-intelligence-commit-runtime/index.ts", import.meta.url),
    "utf8",
  );
  assert.match(index, /from "\.\/task-class-vocabulary\.ts"/);
  assert.match(index, /validateTaskClasses\(body\.declared_task_classes\)/);
  assert.match(index, /p_declared_task_classes: declaredTaskClasses/);
});

test("TC-EDGE-02: supersede explicitly rejects task-class declarations (no silent drop)", () => {
  const index = readFileSync(
    new URL("../supabase/functions/nayanet-intelligence-commit-runtime/index.ts", import.meta.url),
    "utf8",
  );
  assert.match(index, /TASK_CLASS_DECLARATION_NOT_SUPPORTED_ON_SUPERSEDE/);
});
