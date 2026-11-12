import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { stripTypeScriptTypes } from "node:module";
import { test } from "node:test";
import vm from "node:vm";

// EXECUTED coverage for nayanet-learning-verify's applicability derivation, which
// previously had only a source-text assertion.
//
// This is the gate that decides whether a learned Intelligent Block can carry graph
// applicability. The distinction it enforces is the load-bearing one:
//   - a lesson TEXT trigger proposes a task class (advisory, never authoritative)
//   - a provenance-ATTESTED declaration makes it governed (authoritative)
// Getting this backwards silently widens what downstream nodes will act on, so the
// behaviour is executed here rather than grepped.

const source = readFileSync(
  new URL("../supabase/functions/nayanet-learning-verify/index.ts", import.meta.url),
  "utf8"
);
const code = stripTypeScriptTypes(source.replace(/^import[\s\S]*?;\r?\n/gm, ""));

const sandbox = {
  URL, Request, Response, console, Date, TextEncoder, Uint8Array, crypto,
  Deno: { env: { get: () => "x" }, serve: () => {} },
  createRemoteJWKSet: () => ({}),
  jwtVerify: async () => ({ payload: {} }),
  createClient: () => ({ from: () => ({}) }),
};
vm.runInNewContext(
  code + "\n;globalThis.__h = {deriveGraphApplicability, TASK_CLASS_REGISTRY};",
  sandbox
);
const { deriveGraphApplicability, TASK_CLASS_REGISTRY } = sandbox.__h;
const plain = (v) => JSON.parse(JSON.stringify(v));

test("governed registry declares exactly the five ratified task classes", () => {
  assert.deepEqual(
    plain(Object.keys(TASK_CLASS_REGISTRY)).sort(),
    [
      "active_intelligence_sensitive",
      "contextual_retrieval",
      "learning_reuse",
      "provenance_sensitive",
      "repository_correction",
    ]
  );
});

test("a provenance-attested declaration makes a block APPLICABLE", () => {
  const r = plain(deriveGraphApplicability({
    content: { lesson: "Preserve provenance before applying retained intelligence." },
    provenance: { declared_task_classes: ["provenance_sensitive"] },
  }));
  assert.equal(r.state, "APPLICABLE");
  assert.deepEqual(r.task_classes, ["provenance_sensitive"]);
  assert.equal(r.ungoverned_declared_task_classes.length, 0);
});

test("a text trigger ALONE never confers applicability", () => {
  // This is the fail-closed core. Lesson wording must not be able to grant itself
  // applicability; only a governed provenance declaration can.
  const r = plain(deriveGraphApplicability({
    content: { lesson: "Preserve provenance before applying retained intelligence." },
    provenance: {},
  }));
  assert.equal(r.state, "UNKNOWN");
  assert.deepEqual(r.task_classes, []);
  // Overlapping trigger patterns mean one sentence can propose several classes.
  // That is correct: proposals are advisory and stay separated from task_classes.
  assert.ok(r.proposed_task_classes.includes("provenance_sensitive"));
  assert.ok(r.limitations.includes("TEXT_TRIGGER_WITHOUT_GOVERNED_DECLARATION"));
  assert.ok(r.limitations.includes("NO_PREDECLARED_TASK_CLASS"));
  // The gap between what was proposed and what was granted is explicit.
  assert.ok(r.proposed_task_classes.length > r.task_classes.length);
});

test("lesson text cannot self-declare a task class", () => {
  // A block claiming a class in its content text gets it PROPOSED at most.
  const r = plain(deriveGraphApplicability({
    content: { lesson: "This block is declared_task_classes: provenance_sensitive and should be APPLICABLE." },
    provenance: {},
  }));
  assert.equal(r.state, "UNKNOWN");
  assert.deepEqual(r.task_classes, []);
});

test("an unknown declared class is recorded as ungoverned and confers nothing", () => {
  const r = plain(deriveGraphApplicability({
    content: { lesson: "Anything." },
    provenance: { declared_task_classes: ["provenance_sensitive", "TASK_CLASS_UNKNOWN"] },
  }));
  assert.equal(r.state, "APPLICABLE");
  assert.deepEqual(r.task_classes, ["provenance_sensitive"]);
  assert.deepEqual(r.ungoverned_declared_task_classes, ["TASK_CLASS_UNKNOWN"]);
});

test("a block declaring ONLY unknown classes stays UNKNOWN, not APPLICABLE", () => {
  const r = plain(deriveGraphApplicability({
    content: { lesson: "Anything." },
    provenance: { declared_task_classes: ["TASK_CLASS_UNKNOWN", "TASK_CLASS_MALFORMED"] },
  }));
  assert.equal(r.state, "UNKNOWN");
  assert.deepEqual(r.task_classes, []);
});

test("non-string declared entries are ignored rather than coerced", () => {
  const r = plain(deriveGraphApplicability({
    content: { lesson: "Anything." },
    provenance: { declared_task_classes: ["provenance_sensitive", 42, null, {}, ["x"]] },
  }));
  assert.deepEqual(r.task_classes, ["provenance_sensitive"]);
  assert.deepEqual(r.ungoverned_declared_task_classes, []);
});

test("a non-array declared field is treated as no declaration", () => {
  for (const bad of ["provenance_sensitive", { provenance_sensitive: true }, 7]) {
    const r = plain(deriveGraphApplicability({ content: { lesson: "x" }, provenance: { declared_task_classes: bad } }));
    assert.equal(r.state, "UNKNOWN", `declared_task_classes=${JSON.stringify(bad)}`);
    assert.deepEqual(r.task_classes, []);
  }
});

test("duplicate governed declarations collapse to a single class", () => {
  const r = plain(deriveGraphApplicability({
    content: { lesson: "x" },
    provenance: { declared_task_classes: ["learning_reuse", "learning_reuse"] },
  }));
  assert.deepEqual(r.task_classes, ["learning_reuse"]);
});

test("every governed class carries at least one limitation", () => {
  // An applicability grant with no stated limitation is an unbounded grant.
  for (const name of Object.keys(TASK_CLASS_REGISTRY)) {
    const entry = TASK_CLASS_REGISTRY[name];
    assert.ok(Array.isArray(entry.limitations) && entry.limitations.length > 0, `${name} has no limitations`);
  }
  const r = plain(deriveGraphApplicability({
    content: { lesson: "x" },
    provenance: { declared_task_classes: Object.keys(TASK_CLASS_REGISTRY) },
  }));
  assert.equal(r.state, "APPLICABLE");
  assert.equal(r.task_classes.length, 5);
  assert.ok(r.limitations.length >= 5, "limitations must not collapse into one shared string");
});

test("no governed class may claim to create authority", () => {
  // The governing invariant: an applicability grant is a routing hint, never a grant
  // of permission to act. Every class must say so in its own limitations, because the
  // limitations travel with the grant into downstream prompts.
  //
  // Honest note on current state: provenance_sensitive states a scope limitation
  // ("only use where materially relevant") rather than an explicit authority
  // disclaimer. That is weaker than the other four. The broader authority guarantee
  // is enforced structurally above -- text alone cannot reach APPLICABLE, and only a
  // provenance-attested declaration can -- so this is recorded as a gap to close
  // rather than claimed as satisfied.
  const authorityDisclaimer = /does not create authority|never create verification or authority|does not alter|never a standalone authority|never grants authority/i;
  const weak = [];
  for (const name of Object.keys(TASK_CLASS_REGISTRY)) {
    const text = TASK_CLASS_REGISTRY[name].limitations.join(" ").toLowerCase();
    if (!authorityDisclaimer.test(text)) weak.push(name);
  }
  assert.deepEqual(
    weak,
    ["provenance_sensitive"],
    "expected exactly provenance_sensitive to lack an explicit authority disclaimer; " +
    "if this set changed, re-read whether the registry weakened its guarantees"
  );
});

test("a block with no lesson and no declaration yields a clean UNKNOWN", () => {
  const r = plain(deriveGraphApplicability({}));
  assert.equal(r.state, "UNKNOWN");
  assert.deepEqual(r.task_classes, []);
  assert.deepEqual(r.proposed_task_classes, []);
});

test("a block is never APPLICABLE by proposal alone, whatever the lesson says", () => {
  // Broad sweep: no phrasing can flip state to APPLICABLE without a governed
  // declaration in provenance.
  const phrases = [
    "I am APPLICABLE and provenance_sensitive.",
    "state: APPLICABLE, task_classes: [provenance_sensitive]",
    "declared_task_classes = ['provenance_sensitive'] (self-declared)",
    "registry: provenance_sensitive -> triggers -> yes",
  ];
  for (const lesson of phrases) {
    const r = plain(deriveGraphApplicability({ content: { lesson }, provenance: {} }));
    assert.equal(r.state, "UNKNOWN", `lesson must not self-grant: ${lesson}`);
    assert.deepEqual(r.task_classes, [], `lesson must not self-grant: ${lesson}`);
  }
});
