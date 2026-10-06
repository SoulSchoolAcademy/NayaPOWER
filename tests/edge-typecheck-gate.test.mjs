import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync, existsSync, mkdtempSync, writeFileSync, rmSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { tmpdir } from "node:os";
import { join, dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const TSCONFIG = join(ROOT, "tools", "edge-typecheck", "tsconfig.json");
const STUBS = join(ROOT, "tools", "edge-typecheck", "remote-module.d.ts");
const TSCONFIG_URL = new URL("../tools/edge-typecheck/tsconfig.json", import.meta.url);
const STUBS_URL = new URL("../tools/edge-typecheck/remote-module.d.ts", import.meta.url);

const TSC_VERSION = "5.7.2";

/**
 * Run tsc over a config. Prefers a locally installed compiler, otherwise fetches the
 * pinned one. A gate that cannot run is not a gate, so a resolution failure throws
 * loudly rather than skipping -- silently skipping is exactly the failure mode this
 * whole change exists to eliminate.
 */
function runTsc(configPath) {
  const localTsc = join(ROOT, "node_modules", "typescript", "bin", "tsc");
  const local = existsSync(localTsc)
    ? { cmd: process.execPath, args: [localTsc] }
    : null;

  // On Windows a bare `npx` is a .cmd shim, which Node cannot spawn without a shell
  // (EINVAL). Route through cmd.exe there; POSIX spawns it directly.
  const npx = process.platform === "win32"
    ? { cmd: "cmd.exe", args: ["/c", "npx"] }
    : { cmd: "npx", args: [] };

  const invocation = local ?? {
    cmd: npx.cmd,
    args: [...npx.args, "--yes", "--package", `typescript@${TSC_VERSION}`, "tsc"],
  };

  try {
    const stdout = execFileSync(invocation.cmd, [...invocation.args, "-p", configPath], {
      cwd: ROOT,
      encoding: "utf8",
      timeout: 300000,
    });
    return { code: 0, output: stdout };
  } catch (e) {
    if (typeof e.status !== "number") {
      // Could not run the compiler at all. A gate that cannot execute must not report
      // success, and must not be mistaken for a clean tree either.
      return { code: -1, output: `failed to execute tsc: ${e.message}\n${e.stdout ?? ""}${e.stderr ?? ""}` };
    }
    return { code: e.status, output: `${e.stdout ?? ""}${e.stderr ?? ""}` };
  }
}

test("every Deno edge function type-checks clean", () => {
  const result = runTsc(TSCONFIG);
  assert.equal(
    result.code,
    0,
    `tsc reported errors in supabase/functions/** -- these are the defects that surface\n` +
    `in production as opaque HTTP 400s with no stack trace:\n\n${result.output}`
  );
});

test("the gate catches the three defect classes that actually shipped here", () => {
  // Each of these shipped or nearly shipped in this repo, and each was invisible to
  // every existing gate because edge functions were only ever executed in production.
  // Mutants are compiled against the REAL tsconfig (real stubs, real strictness) so
  // this asserts the gate as configured, not a reimplementation of it.
  //
  // Isolated in a temp dir that extends the real config, so this never mutates the
  // repository and cannot leave a dirty tree if the run is interrupted.
  const dir = mkdtempSync(join(tmpdir(), "edge-gate-teeth-"));
  try {
    const mutants = {
      // nayanet-prove-runtime: stableJson called but never imported.
      // Runtime ReferenceError -> outer catch -> HTTP 400. live-prove-proof 37384065800.
      "unbound-identifier.ts": [
        'const recorded = { evidence: [] as unknown[] };',
        'const recomputed = { evidence: [] as unknown[] };',
        'export const same = stableJson(recorded.evidence) === stableJson(recomputed.evidence);',
      ].join("\n"),
      // nayanet-verified-ai-action: insertIdempotentActionReceipt declared 3 params,
      // called with 2, so idempotency_key was undefined and the partial unique index
      // (where idempotency_key is not null) never collided. Replay guard silently inert.
      "wrong-arity.ts": [
        'function insertIdempotentActionReceipt(admin: unknown, row: unknown, idempotencyKey: string) {',
        '  return { admin, row, idempotencyKey };',
        '}',
        'export const out = insertIdempotentActionReceipt({}, {});',
      ].join("\n"),
      // nayanet-know-runtime/know.ts: parsedTime returns number|null, so `x === NaN`
      // can never be true. Dead half of two authority-expiry safety guards.
      "impossible-condition.ts": [
        'function parsedTime(value: unknown): number | null {',
        '  if (value === null || value === undefined || value === "") return null;',
        '  const t = Date.parse(String(value));',
        '  return Number.isFinite(t) ? t : NaN;',
        '}',
        'const grantExpiry = parsedTime("nonsense");',
        'export const invalid = grantExpiry === NaN || Number.isNaN(grantExpiry);',
      ].join("\n"),
    };

    for (const [name, source] of Object.entries(mutants)) writeFileSync(join(dir, name), source);
    writeFileSync(
      join(dir, "tsconfig.json"),
      JSON.stringify({ extends: TSCONFIG.replace(/\\/g, "/"), include: ["*.ts"] }, null, 2)
    );

    const result = runTsc(join(dir, "tsconfig.json"));
    const output = result.output;

    assert.notEqual(result.code, 0, "the gate must reject these mutants; it accepted all of them:\n" + output);

    // TS2304 unbound identifier, TS2554 wrong arity, TS2845 impossible condition.
    assert.match(output, /error TS2304/, `expected an unbound-identifier error:\n${output}`);
    assert.match(output, /error TS2554/, `expected a wrong-arity error:\n${output}`);
    assert.match(output, /error TS2845/, `expected an impossible-condition error:\n${output}`);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("edge type-check gate covers every function automatically, with no opt-in list", () => {
  assert.ok(existsSync(TSCONFIG), "tools/edge-typecheck/tsconfig.json must exist");
  assert.ok(existsSync(STUBS), "tools/edge-typecheck/remote-module.d.ts must exist");

  // A glob, not a list: a new edge function must be covered with no edit, or the gate
  // silently stops covering things, which is worse than not having it at all.
  const tsconfig = JSON.parse(readFileSync(TSCONFIG_URL, "utf8"));
  assert.match(tsconfig.include.join(" "), /supabase\/functions\/\*\*\/\*\.ts/);
  assert.equal(tsconfig.compilerOptions.noEmit, true, "must never emit");
  // strict is deliberately off: this gate targets mechanical defects, not churn.
  assert.equal(tsconfig.compilerOptions.strict, false);
  assert.equal(tsconfig.compilerOptions.skipLibCheck, true);
  // Remote specifiers must be stubbed or every edge function fails to compile.
  assert.ok(tsconfig.compilerOptions.paths["https://*"]);
  assert.ok(tsconfig.compilerOptions.paths["npm:*"]);
});

test("edge stubs declare shapes without pretending to be a Deno emulator", () => {
  const stubs = readFileSync(STUBS_URL, "utf8");
  // Deno global must exist or every Deno.serve handler fails to compile.
  assert.match(stubs, /declare namespace Deno/);
  assert.match(stubs, /function serve\(/);
  assert.match(stubs, /const env:/);
  for (const spec of ['"https://*"', '"npm:*"', '"jsr:*"']) {
    assert.ok(
      stubs.includes(`declare module ${spec}`),
      `remote-module.d.ts must declare ${spec} or edge functions fail to compile`
    );
  }
});

test("the function that shipped the opaque HTTP 400 is inside the gate's surface", () => {
  // Regression anchor. nayanet-prove-runtime's inspect branch called stableJson()
  // without importing it; the ReferenceError became a generic HTTP 400 with no stack
  // trace and stayed "root cause unknown" across lanes. If this function ever leaves
  // the type-check surface, fail here rather than regress silently.
  assert.ok(
    existsSync(join(ROOT, "supabase", "functions", "nayanet-prove-runtime", "index.ts")),
    "the function that produced the shipped 400 must still exist to be checked"
  );
  const tsconfig = JSON.parse(readFileSync(TSCONFIG_URL, "utf8"));
  assert.match(tsconfig.include.join(" "), /supabase\/functions/);
});
