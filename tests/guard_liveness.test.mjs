import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync, existsSync, mkdtempSync, writeFileSync, rmSync, mkdirSync, cpSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { tmpdir } from "node:os";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

// Guard liveness gate.
//
// The rule: a refusal that cannot be observed to fire is not a guard. SN-0468 says
// fail closed; this makes "closed" mean something measurable. Two guards in this repo
// looked correct and could never fire -- `idempotency_key` was undefined because a
// 3-param function was called with 2 args, and `x === NaN` can never be true for a
// `number | null`. Neither was findable by reading. Both are findable by asking
// whether a test can watch the thing reject.
//
// Design decision: RATCHET, not cliff. The honest starting coverage is 30.6%. A gate
// that fails at 30.6% blocks every merge forever and trains people to bypass it, which
// is worse than no gate. The floor is committed and may only rise.

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const TOOL = join(ROOT, "tools", "guard_liveness.py");
const FLOOR = join(ROOT, "tools", "guard-liveness-floor.json");

function runTool(cwd = ROOT, args = [], toolPath = TOOL) {
  // toolPath is explicit because the fixture test copies the tool into a temp repo.
  // ROOT inside the script derives from __file__, so running the real script with a
  // temp cwd would silently scan the REAL repository -- which is exactly the kind of
  // false green this project keeps learning about.
  try {
    const stdout = execFileSync("python", [toolPath, ...args], {
      cwd,
      encoding: "utf8",
      timeout: 180000,
    });
    return { code: 0, stdout };
  } catch (e) {
    return {
      code: typeof e.status === "number" ? e.status : 1,
      stdout: `${e.stdout ?? ""}${e.stderr ?? ""}`,
    };
  }
}

function report() {
  const r = runTool(ROOT, ["--json"]);
  assert.equal(r.code, 0, `guard_liveness.py failed:\n${r.stdout}`);
  return JSON.parse(r.stdout);
}

test("guard liveness tool exists and emits a machine-readable report", () => {
  assert.ok(existsSync(TOOL));
  assert.ok(existsSync(FLOOR));
  const r = report();
  assert.equal(typeof r.total_guards, "number");
  assert.equal(typeof r.with_firing_proof, "number");
  assert.equal(typeof r.pct_with_firing_proof, "number");
  assert.equal(
    r.with_firing_proof + r.without_firing_proof,
    r.total_guards,
    "every guard must be classified as proven or unproven"
  );
});

test("guard coverage has not fallen below the committed floor (ratchet)", () => {
  const floor = JSON.parse(readFileSync(FLOOR, "utf8"));
  const r = report();
  assert.ok(
    r.pct_with_firing_proof >= floor.floor_pct_with_firing_proof,
    `guard firing-proof coverage fell from the committed floor ` +
    `${floor.floor_pct_with_firing_proof}% to ${r.pct_with_firing_proof}%. ` +
    `A guard that loses its firing proof is a silent-failure regression (SN-0468).`
  );
});

test("the floor is honest: it records the measured baseline, not an aspiration", () => {
  const floor = JSON.parse(readFileSync(FLOOR, "utf8"));
  const r = report();
  // The floor must not be above reality, or the gate is theatre that always fails, and
  // must not be far below, or it lets a real regression through.
  assert.ok(
    floor.floor_pct_with_firing_proof <= r.pct_with_firing_proof + 0.2,
    `floor ${floor.floor_pct_with_firing_proof}% exceeds measured ${r.pct_with_firing_proof}%; ` +
    `the gate would be permanently red`
  );
  assert.ok(
    r.pct_with_firing_proof - floor.floor_pct_with_firing_proof < 15,
    `floor is more than 15 points below measured coverage; it is not holding anything`
  );
});

test("the tool does not count success reasons as guards", () => {
  // Inflating the denominator with pass-path reasons would flatter the coverage number
  // and hide the real gap. Regression guard for a mistake this tool actually made in
  // its first draft, where LAW_AND_LIVE_AUTHORITY_MATCH was counted as a guard.
  const r = report();
  for (const literal of ["LAW_AND_LIVE_AUTHORITY_MATCH", "ACTIVE_IN_SCOPE_GRANT"]) {
    const hit = r.unproven.find((g) => g.literal === literal);
    assert.equal(
      hit,
      undefined,
      `${literal} names a successful outcome and must not appear in the guard report`
    );
  }
});

test("a guard with no executed firing proof is reported, not hidden", () => {
  const r = report();
  assert.ok(r.without_firing_proof > 0, "expected a real number of unproven guards at baseline");
  for (const g of r.unproven) {
    assert.ok(g.literal && g.literal.length > 0);
    assert.ok(Array.isArray(g.sites) && g.sites.length > 0, `${g.literal} has no code site`);
    assert.equal(g.firing_observed, false);
  }
});

test("the tool detects a guard that cannot fire (mutation proof)", () => {
  // Prove the gate has teeth against the exact defect class it exists to catch.
  //
  // Built in an isolated copy of the repo so the real tree is never mutated and an
  // interrupted run cannot leave a dirty working tree. The synthetic code contains a
  // refusal literal whose only "test" is a source grep -- exactly the shape that let
  // PROVE's stableJson ship -- and the tool must classify it unproven.
  const dir = mkdtempSync(join(tmpdir(), "guard-liveness-teeth-"));
  try {
    mkdirSync(join(dir, "tools"), { recursive: true });
    mkdirSync(join(dir, "supabase", "functions", "synthetic"), { recursive: true });
    mkdirSync(join(dir, "tests"), { recursive: true });

    cpSync(TOOL, join(dir, "tools", "guard_liveness.py"));

    // A refusal literal emitted only on an ok:false path.
    writeFileSync(
      join(dir, "supabase", "functions", "synthetic", "index.ts"),
      'const json=(b,s=200)=>new Response(JSON.stringify(b),{status:s});\n' +
        'export function handler(req){\n' +
        '  if(!req.tenant) return json({ok:false,error:"SYNTHETIC_TENANT_REQUIRED"},400);\n' +
        '  return json({ok:true});\n' +
        '}\n'
    );
    // The only "test": greps the source. No execution. This is the defect shape.
    writeFileSync(
      join(dir, "tests", "synthetic.test.mjs"),
      'import test from "node:test";\n' +
        'import assert from "node:assert/strict";\n' +
        'import { readFileSync } from "node:fs";\n' +
        'test("synthetic guard present", () => {\n' +
        '  const s = readFileSync(new URL("../supabase/functions/synthetic/index.ts", import.meta.url), "utf8");\n' +
        '  assert.match(s, /SYNTHETIC_TENANT_REQUIRED/);\n' +
        '});\n'
    );

    const r = runTool(dir, ["--json"], join(dir, "tools", "guard_liveness.py"));
    let parsed;
    try {
      parsed = JSON.parse(r.stdout);
    } catch {
      throw new Error(`guard_liveness.py did not emit JSON in the isolated fixture (exit ${r.code}):\n${r.stdout}`);
    }
    const guard = parsed.unproven.find((g) => g.literal === "SYNTHETIC_TENANT_REQUIRED");
    assert.ok(
      guard,
      `the tool must classify a source-grep-only guard as unproven; that is the whole point.\n` +
      `report was: ${JSON.stringify(parsed, null, 2)}`
    );
    assert.equal(guard.firing_observed, false);
    assert.deepEqual(
      guard.grep_only,
      ["synthetic.test.mjs"],
      "it must record that a grep reference exists and explicitly not count it"
    );
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("guard liveness keeps its own name attached to its purpose", () => {
  // A gate nobody can explain gets deleted by someone who thinks it is redundant.
  const src = readFileSync(TOOL, "utf8");
  assert.match(src, /SN-0468/, "must cite the law it enforces");
  assert.match(src, /idempotency_key/, "must cite the concrete defect it was built from");
});
