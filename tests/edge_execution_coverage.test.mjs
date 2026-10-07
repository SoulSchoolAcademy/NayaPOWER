import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync, readdirSync, existsSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { join, dirname, relative, sep } from "node:path";
import { fileURLToPath } from "node:url";

// Coverage-shape gate: no edge function may regress to "grep only".
//
// The failure mode this exists to stop is specific and has already happened here.
// nayanet-prove-runtime shipped an un-imported identifier that became an opaque HTTP
// 400 in production (live-prove-proof run 37384065800) while 13/13 tests were green,
// because every assertion on the failing branch regex-matched the handler's source
// text instead of running it.
//
// A source-text assertion is not worthless -- it can pin a workflow step, a migration,
// or a contract string -- but it is NOT evidence that a handler runs. This gate makes
// the distinction explicit and machine-checked rather than a matter of reviewer memory.

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const FUNCTIONS = join(ROOT, "supabase", "functions");
const TESTS = join(ROOT, "tests");

const nodeTests = readdirSync(TESTS).filter((f) => f.endsWith(".test.mjs"));
const suites = nodeTests.map((f) => ({ file: f, text: readFileSync(join(TESTS, f), "utf8") }));

function walk(dir) {
  const out = [];
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    const p = join(dir, entry.name);
    if (entry.isDirectory()) out.push(...walk(p));
    else if (entry.name.endsWith(".ts")) out.push(p);
  }
  return out;
}

/**
 * Repo-relative, forward-slash path.
 *
 * Platform-independent on purpose. An earlier version did
 * `p.replace(ROOT + "\\", "")`, which silently produces an absolute path on Linux, so
 * the gate matched nothing there and reported 0/14 executed -- a false "everything is
 * unproven" verdict in CI while passing locally. path.relative + sep normalisation is
 * the only form that behaves the same on every runner.
 */
const rel = (p) => relative(ROOT, p).split(sep).join("/");

/**
 * Decide whether any test genuinely executes a function's code.
 *
 * Two execution routes are recognised:
 *   1. direct import of the function's own module
 *   2. VM sandbox load (vm.runInNewContext over stripTypeScriptTypes(source)) with
 *      stubbed Deno/jose/supabase -- this runs the real handler body offline
 *
 * A python test is never counted: it cannot execute TS, so any reference it makes is
 * text matching. It may still assert useful things (workflow wiring, migration
 * contents, contract strings) -- it is simply not execution evidence.
 */
function executionEvidenceFor(paths) {
  const evidence = [];
  for (const s of suites) {
    const referenced = paths.filter((p) => s.text.includes(p));
    if (!referenced.length) continue;
    const tsReferenced = referenced.filter((p) => p.endsWith(".ts"));

    const importsModule = tsReferenced.some((p) => {
      const esc = p.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
      return new RegExp(`import[^;]*from\\s+["'][^"']*${esc}["']`).test(s.text);
    });
    const vmExecutes = /vm\.runIn(New)?Context/.test(s.text) && /stripTypeScriptTypes|readFileSync/.test(s.text);

    if (importsModule || vmExecutes) evidence.push(s.file);
  }
  return [...new Set(evidence)];
}

test("no edge function is left without executed test coverage", () => {
  const uncovered = [];
  const details = [];

  for (const fn of readdirSync(FUNCTIONS, { withFileTypes: true })) {
    if (!fn.isDirectory()) continue;
    const paths = walk(join(FUNCTIONS, fn.name)).map(rel);
    const evidence = executionEvidenceFor(paths);
    if (!evidence.length) uncovered.push(fn.name);
    details.push(`${fn.name}: ${evidence.length ? evidence.join(", ") : "NONE"}`);
  }

  assert.deepEqual(
    uncovered,
    [],
    `edge function(s) with no executed test coverage:\n  ${uncovered.join("\n  ")}\n\n` +
    `All functions:\n  ${details.join("\n  ")}\n\n` +
    "A handler with only source-text assertions is unproven: it may not even run. " +
    "Add a test that imports the module or loads it into a VM sandbox."
  );
});

test("the coverage audit tool reports the same verdicts as this gate", () => {
  // Two implementations of the same judgement will drift. Rather than string-match the
  // audit's source, run it and compare its verdicts to what this gate computed. If they
  // disagree, one of them is wrong and the disagreement is the finding.
  const audit = join(ROOT, "tools", "edge-typecheck", "audit-execution-coverage.mjs");
  assert.ok(existsSync(audit), "the audit tool must exist; the gate is derived from it");

  const output = execFileSync(process.execPath, [audit], { encoding: "utf8", cwd: ROOT, timeout: 120000 });
  const auditExecuted = new Set();
  for (const line of output.split("\n")) {
    const m = line.match(/^(\S+)\s+EXECUTED\s/);
    if (m) auditExecuted.add(m[1]);
  }

  const gateExecuted = readdirSync(FUNCTIONS, { withFileTypes: true })
    .filter((e) => e.isDirectory())
    .filter((e) => executionEvidenceFor(walk(join(FUNCTIONS, e.name)).map(rel)).length > 0)
    .map((e) => e.name);

  assert.deepEqual(
    [...auditExecuted].sort(),
    [...gateExecuted].sort(),
    "the standalone audit and this gate disagree about which functions are executed"
  );
  assert.equal(auditExecuted.size, gateExecuted.length);
});

test("every edge function has executed coverage, not just a grep", () => {
  // The concrete number, asserted so a silent regression cannot hide behind the
  // generic message above.
  const total = readdirSync(FUNCTIONS, { withFileTypes: true }).filter((e) => e.isDirectory()).length;
  const covered = readdirSync(FUNCTIONS, { withFileTypes: true })
    .filter((e) => e.isDirectory())
    .filter((e) => executionEvidenceFor(walk(join(FUNCTIONS, e.name)).map(rel)).length > 0)
    .map((e) => e.name);

  assert.equal(covered.length, total, `only ${covered.length}/${total} edge functions are executed by a test`);
});

test("the coverage gate names the defect class it prevents", () => {
  // Keeps the reason attached to the check. A gate whose purpose is undocumented
  // tends to be deleted by someone who thinks it is redundant.
  const self = readFileSync(new URL(import.meta.url), "utf8");
  assert.match(self, /live-prove-proof run 37384065800/);
  assert.match(self, /opaque HTTP 400/);
});
