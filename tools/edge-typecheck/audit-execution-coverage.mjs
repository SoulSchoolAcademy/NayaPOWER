// Audit: which edge functions are actually EXECUTED by the test suite, and which are
// only source-text-matched?
//
// A green check that greps handler source proves the code looks right, not that it
// runs. That is the exact blind spot that let nayanet-prove-runtime ship an
// un-imported identifier as an opaque HTTP 400 (live-prove-proof run 37384065800)
// while 13/13 tests were green.
//
// Runs both suites: tests/*.test.mjs (node) and tests/*.py (pytest).
import { readFileSync, readdirSync } from "node:fs";
import { join, dirname, relative, sep } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..", "..");
const FUNCTIONS = join(ROOT, "supabase", "functions");
const TESTS = join(ROOT, "tests");

const nodeTests = readdirSync(TESTS).filter((f) => f.endsWith(".test.mjs"));
const pyTests = readdirSync(TESTS).filter((f) => f.endsWith(".py"));
const suites = [
  ...nodeTests.map((f) => ({ file: f, text: readFileSync(join(TESTS, f), "utf8"), lang: "node" })),
  ...pyTests.map((f) => ({ file: f, text: readFileSync(join(TESTS, f), "utf8"), lang: "py" })),
];

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
 * Platform-independent on purpose. A previous version stripped ROOT + "\\", which
 * yields an absolute path on Linux and therefore matched nothing on the CI runner.
 * That made the audit report every function as UNCOVERED there while passing on
 * Windows -- a false negative in the tool people would trust for a coverage claim.
 */
const rel = (p) => relative(ROOT, p).split(sep).join("/");

// Two ways a node test can genuinely EXECUTE handler code:
//   1. imports the module            -> `import { x } from "../supabase/..."`
//   2. loads it into a VM sandbox    -> `vm.runInNewContext(code, ...)` where code
//      came from stripTypeScriptTypes(readFileSync(handler))
// Method 2 executes the handler body with stubbed Deno/jose/supabase, which is real
// execution. An audit that only recognises method 1 reports false negatives, and a
// false "UNCOVERED" claim is worse than no audit -- so detect both.
//
// A python test can never execute a TS handler; every reference it makes is a
// source-text match. It may still be a *useful* test (it can assert contract shape,
// workflow wiring, migration contents); it is simply not execution evidence.
const rows = [];
for (const fn of readdirSync(FUNCTIONS, { withFileTypes: true })) {
  if (!fn.isDirectory()) continue;
    if (fn.name.startsWith("_")) continue; // shared modules are not deployable edge functions
  const name = fn.name;
  const sources = walk(join(FUNCTIONS, name));
  const paths = sources.map(rel);

  let executed = false;
  let grepped = false;
  let execTests = [];
  let grepTests = [];

  for (const s of suites) {
    const references = paths.filter((p) => s.text.includes(p));
    if (!references.length) continue;

    let isExecution = false;
    if (s.lang === "node") {
      // 1. direct import of the function's own module
      if (references.some((p) => new RegExp(`import[^;]*from\\s+["'][^"']*${p.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}["']`).test(s.text))) {
        isExecution = true;
      }
      // 2. VM sandbox execution of the handler source
      if (!isExecution && /vm\.runIn(New)?Context/.test(s.text) && /stripTypeScriptTypes|readFileSync/.test(s.text)) {
        isExecution = true;
      }
    }

    if (isExecution) {
      executed = true;
      execTests.push(s.file);
    } else {
      grepped = true;
      grepTests.push(s.file);
    }
  }

  rows.push({
    function: name,
    verdict: executed ? "EXECUTED" : grepped ? "GREP ONLY" : "UNCOVERED",
    exec: execTests.length,
    grep: grepTests.length,
  });
}

rows.sort((a, b) => a.verdict.localeCompare(b.verdict) || a.function.localeCompare(b.function));

const w = (s, n) => String(s).padEnd(n);
console.log(w("FUNCTION", 40), w("VERDICT", 11), w("EXEC-TESTS", 11), "GREP-TESTS");
console.log("-".repeat(110));
for (const r of rows) {
  console.log(w(r.function, 40), w(r.verdict, 11), w(r.exec, 11), r.grep || "");
}
const counts = rows.reduce((a, r) => ((a[r.verdict] = (a[r.verdict] ?? 0) + 1), a), {});
console.log("-".repeat(110));
console.log("TOTAL:", JSON.stringify(counts));
