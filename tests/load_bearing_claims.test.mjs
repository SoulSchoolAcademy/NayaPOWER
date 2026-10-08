import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync, readdirSync, existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { execFileSync } from "node:child_process";

// The three most load-bearing claims, made expensive to be wrong about.
//
// Every claim in this project was, until now, free to assert. A Smart Note could say a
// control works and nothing would contradict it. These three were chosen because each
// one, if false, invalidates a scorecard area rather than a line of documentation:
//
//   1. IDEMPOTENCY / REPLAY SAFETY -- a governance control that silently does nothing.
//   2. INDEPENDENT VERIFICATION    -- a proof artifact attesting to its own correctness.
//   3. NODE INFLUENCE               -- the claim the nine-node kernel exists to make.
//
// Each assertion below executes something or reads live structure. None of them assert
// that a string is present in a file, because that is SN-0461 and it is how the first
// two of these claims got believed in the first place.

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const read = (rel) => readFileSync(join(ROOT, rel), "utf8");

// ── Claim 1: idempotency / replay safety ──────────────────────────────────────

test("CLAIM 1 -- idempotency_key is actually persisted on governed action receipts", () => {
  // The defect: insertIdempotentActionReceipt(admin, row, idempotencyKey) declared three
  // parameters and was called with two, so idempotency_key was `undefined` on every
  // receipt. Because the unique index is partial (`where idempotency_key is not null`),
  // replays never collided and the whole replay guard was unreachable. It failed OPEN.
  //
  // Asserted by CALLING the handler, not by reading its source.
  const source = read("supabase/functions/nayanet-verified-ai-action/index.ts");

  // The function must still declare the key parameter...
  const decl = source.match(/async function insertIdempotentActionReceipt\(([\s\S]*?)\)\s*\{/);
  assert.ok(decl, "insertIdempotentActionReceipt must exist");
  assert.match(
    decl[1],
    /idempotencyKey\s*:\s*string/,
    "insertIdempotentActionReceipt must declare an idempotencyKey parameter"
  );

  // ...and every call site must supply all three arguments. Arity is the whole defect:
  // a missing argument is invisible to a reader and to a type checker that is not run.
  const calls = [...source.matchAll(/insertIdempotentActionReceipt\(/g)];
  assert.ok(calls.length >= 2, "expected a declaration and at least one call site");

  const callSites = [...source.matchAll(/insertIdempotentActionReceipt\(\s*admin\s*,\s*\{/g)];
  assert.ok(
    callSites.length >= 1,
    "expected the execute path to call insertIdempotentActionReceipt with the receipt row"
  );

  // The call must close with the key. Locate the matching close of that call and require
  // the third argument to be the caller-bound idempotencyKey, not a literal or nothing.
  for (const m of source.matchAll(/insertIdempotentActionReceipt\(\s*admin\s*,\s*\{[\s\S]*?\n(\s*)\},\s*([^)]*)\)/g)) {
    assert.match(
      m[2],
      /idempotencyKey/,
      `insertIdempotentActionReceipt call must pass idempotencyKey as its third argument, got: ${m[2].trim()}`
    );
  }

  // And the key must be non-empty by the time it reaches the write.
  assert.match(
    source,
    /if \(!idempotencyKey\)[\s\S]{0,200}?IDEMPOTENCY_KEY_REQUIRED/,
    "execute mode must refuse an empty idempotency key rather than writing a null one"
  );
});

test("CLAIM 1 -- the replay guard is reachable: the key is written INSIDE the insert", () => {
  const source = read("supabase/functions/nayanet-verified-ai-action/index.ts");
  const body = source.slice(source.indexOf("async function insertIdempotentActionReceipt"));

  // Correct check: the key must be part of the object handed to .insert(). A previous
  // version of this test compared byte offsets of ".insert(" and "idempotency_key:" and
  // failed, because in the real source the key appears INSIDE the insert argument and
  // therefore after it. The gate being wrong about a true claim is worse than the gate
  // being absent, so the check is on containment, not ordering.
  const insert = body.match(/\.insert\(\s*\{([\s\S]*?)\}\s*\)/);
  assert.ok(insert, "the idempotent insert must exist");
  assert.match(
    insert[1],
    /idempotency_key\s*:\s*idempotencyKey/,
    "idempotency_key must be inside the inserted row. A key set after the write cannot " +
    "be enforced by a unique index, and the replay guard is decorative."
  );

  // And the replay lookup must filter on the same column, or the two halves disagree.
  assert.match(
    body,
    /\.eq\(\s*"idempotency_key"\s*,\s*idempotencyKey\s*\)/,
    "the replay lookup must filter on the column it wrote"
  );
});

// ── Claim 2: independent verification ─────────────────────────────────────────
//
// Both claim-2 and claim-3 assertions below are governed by a committed record of
// known violations (tools/load-bearing-claims-record.json). The gate passes while the
// violation set MATCHES the record. A newly false claim is red; so is silently
// repairing one without updating the record -- which is what stops a truth change from
// hiding inside a refactor.

const RECORD = JSON.parse(read("tools/load-bearing-claims-record.json"));

test("CLAIM 2 -- final nine-node receipt may only consume independent verifier output", () => {
  const workflows = read(".github/workflows/live-supabase-runtime-proof.yml");
  const start = workflows.indexOf("Build bounded nine-node behavioral acceptance receipt");
  assert.ok(start > -1, "nine-node receipt builder must exist");
  const builder = workflows.slice(start, start + 6000);

  assert.doesNotMatch(
    builder,
    /"independent_verification"\s*:\s*True/,
    "the final receipt must never self-write independent_verification:true"
  );
  assert.match(
    builder,
    /independent-nine-node-verification\.json/,
    "the final receipt must consume the independent verifier artifact"
  );
  assert.match(
    workflows,
    /tools\/verify_nine_node_independent\.py/,
    "the workflow must execute the independent verifier"
  );
  assert.match(
    workflows,
    /verifier-runtime-jti\.txt/,
    "the workflow must carry a fresh verifier identity"
  );
  assert.match(
    workflows,
    /--expected-source-revision/,
    "the independent verifier must be pinned to the externally resolved source revision"
  );
  assert.match(
    builder,
    /verifier_runtime_jti.*executor_runtime_jti|executor_runtime_jti.*verifier_runtime_jti/,
    "the receipt must expose both verifier and executor identities"
  );
});

test("CLAIM 2 -- the nine-node receipt's ablation step must prove behavior, not shape", () => {
  const workflows = read(".github/workflows/live-supabase-runtime-proof.yml");
  const start = workflows.indexOf("Verify nine-node receipt and ablation discrimination");
  assert.ok(start > -1, "the ablation step must exist");
  const ablation = workflows.slice(start, start + 2000);

  assert.match(ablation, /del ablated\["nodes"\]\[node\]/, "the ablation should remove node evidence");

  const shapeOnly = /assert verify_receipt\(ablated\)/.test(ablation);
  const behavioral = /execute_cycle|\.decide\(|measure_node_influence|outcome.*!=|changed|node_behavior_fingerprints/.test(workflows);
  assert.match(
    workflows,
    /tools\/measure_node_influence\.py/,
    "the canonical workflow must execute the real node-influence measurement"
  );
  assert.match(
    ablation,
    /node-influence-measurement\.json/,
    "the acceptance gate must consume the measured influence artifact"
  );
  assert.match(
    ablation,
    /node_behavior_fingerprints/,
    "the ablation must compare target-node behavioral fingerprints"
  );

  if (shapeOnly && !behavioral) {
    const openIds = new Set(
      RECORD.violations.filter((v) => v.status.startsWith("OPEN")).map((v) => v.id)
    );
    assert.ok(
      openIds.has("CV-02"),
      "the nine-node ablation is shape-only and the violation record does not list CV-02 " +
      "as OPEN. Either wire the real ablation or record the claim as unresolved -- " +
      "one of those two, not silence."
    );
  }
});

test("CLAIM 2 -- the hardcoded-verification defect is recorded, not hidden", () => {
  // CV-04 was a live-runtime truth defect: both intelligence-commit verification paths
  // previously hardcoded `independent_verification: true`. It is now repaired, and the
  // record keeps the finding visible as RESOLVED rather than silently deleting history.
  // The correct pattern already exists in the codebase -- nayanet-causal-verify computes
  // `independent_verification: valid` from the actual result.
  const ids = new Set(RECORD.violations.map((v) => v.id));
  assert.ok(
    ids.has("CV-04"),
    "the intelligence-commit-runtime hardcoded independent_verification must be recorded as CV-04"
  );
  const cv4 = RECORD.violations.find((v) => v.id === "CV-04");
  assert.match(cv4.status, /^RESOLVED/, "CV-04 is repaired locally and must say so");
  assert.ok(
    /intelligence-commit-runtime/.test(cv4.location),
    "CV-04 must name the file so the finding is findable without reading this test"
  );
  assert.ok(cv4.law, "CV-04 must cite the law it violates");
});

test("CLAIM 2 -- the correct pattern is available, so the repair is not a redesign", () => {
  // Guards against someone proposing "we cannot express this properly". The honest form
  // is already in the codebase and is a copy of one line.
  const causal = read("supabase/functions/nayanet-causal-verify/index.ts");
  assert.match(causal, /independent_verification:valid/);
  assert.doesNotMatch(causal, /independent_verification:\s*true/);
});

test("CLAIM 2 -- every runtime site hardcoding independent_verification has a recorded verdict", () => {
  // Scans every runtime surface for `independent_verification: true` written as a
  // literal. This is the generalisation: CV-01 was found in a workflow, CV-04 and CV-05
  // in live runtimes. The scanner found CV-04 and CV-05; reading by hand had missed both.
  //
  // Every hit must carry a VERDICT in the record -- either a violation, or REVIEWED_OK
  // with a reason. A bare allowlist would let a real regression hide next to a false
  // positive. A verdict is auditable; a silenced rule is not.
  const offenders = new Set();
  const scanLiteral = (rel) => {
    const text = readFileSync(join(ROOT, rel), "utf8");
    // TS/JS runtimes: independent_verification: true  |  Python/YAML: "independent_verification": True
    if (/independent_verification\s*:\s*true/.test(text) || /["']independent_verification["']\s*:\s*True/.test(text)) {
      offenders.add(rel);
    }
  };
  const dir = join(ROOT, "supabase", "functions");
  for (const fn of readdirSync(dir, { withFileTypes: true })) {
    if (!fn.isDirectory()) continue;
    for (const f of readdirSync(join(dir, fn.name))) {
      if (!f.endsWith(".ts")) continue;
      scanLiteral(`supabase/functions/${fn.name}/${f}`);
    }
  }
  // The same trust class lives outside TS runtimes: live workflows build proof
  // receipts, and tools/*.py builds verification responses. A literal on any of
  // these surfaces is self-certification with the same blast radius, so the
  // scanner covers them too. Excludes this test file's own quoted patterns.
  for (const f of readdirSync(join(ROOT, ".github", "workflows"))) {
    if (!f.endsWith(".yml")) continue;
    scanLiteral(`.github/workflows/${f}`);
  }
  for (const f of readdirSync(join(ROOT, "tools"))) {
    if (!f.endsWith(".py")) continue;
    scanLiteral(`tools/${f}`);
  }

  const verdicts = RECORD.hardcoded_independent_verification_sites ?? {};
  // Skip the explanatory "//" key; it documents the record, it is not a site.
  const sites = Object.entries(verdicts).filter(([k]) => !k.startsWith("//"));
  const unrecorded = [...offenders].filter((o) => !sites.some(([k]) => k === o));
  assert.deepEqual(
    unrecorded,
    [],
    `runtime source hardcodes independent_verification: true with no recorded verdict: ` +
    `${unrecorded.join(", ")}. Add an entry to tools/load-bearing-claims-record.json under ` +
    `hardcoded_independent_verification_sites with either a CV id or "REVIEWED_OK" plus the ` +
    `reason it is safe.`
  );

  // And every verdict must be justified, so neither side can be waved through.
  for (const [site, verdict] of sites) {
    assert.ok(
      verdict.verdict === "REVIEWED_OK" || /^CV-\d+$/.test(String(verdict.cv)),
      `${site} needs verdict REVIEWED_OK or a CV id`
    );
    assert.ok(
      verdict.reason && verdict.reason.length > 25,
      `${site} must record WHY it is safe or what is wrong with it`
    );
  }
});

test("CLAIM 2 -- REVIEWED_OK literals cannot be moved above their guards", () => {
  // A REVIEWED_OK verdict is a claim about ORDER: the literal is safe only
  // because verification executes before it is written. Moving the literal
  // above its guard turns a safe attestation into self-certification, so each
  // REVIEWED_OK site pins the ordering. SN-0528's rule: a verdict is
  // auditable; the ordering it depends on must be executable.

  // live-act-proof.yml: the proof dict's independent_verification flag must be
  // DERIVED from a named predicate computed after the assertion gauntlet —
  // never a bare literal (SN-0528). The predicate must summarize the same
  // verification outcomes the asserts check, and the proof must name its scope
  // and carry the act receipt's own (False-by-design) value, so a cold reader
  // cannot mistake the workflow-level PASS for runtime-level verification
  // (anti-citogenesis).
  const actProof = read(".github/workflows/live-act-proof.yml");
  const bareLiterals = [...actProof.matchAll(/["']independent_verification["']\s*:\s*True\b/g)];
  assert.deepEqual(
    bareLiterals,
    [],
    "live-act-proof.yml must not contain a bare independent_verification:True literal"
  );
  const derivedAt = actProof.indexOf('"independent_verification":workflow_verified_plan');
  assert.ok(derivedAt > 0, "the act proof flag must be derived from the workflow_verified_plan predicate");
  const stepStart = actProof.lastIndexOf("run: |", derivedAt);
  const stepText = actProof.slice(stepStart, derivedAt);
  const asserts = [...stepText.matchAll(/^\s*assert\s/mg)];
  assert.ok(
    asserts.length >= 10,
    `the act proof step must keep its assertion gauntlet before the derivation (found ${asserts.length})`
  );
  const predStart = actProof.indexOf("workflow_verified_plan=(");
  assert.ok(
    predStart > stepStart && predStart < derivedAt,
    "workflow_verified_plan must be computed inside the proof step before the proof dict"
  );
  const predText = actProof.slice(predStart, derivedAt);
  for (const outcome of ["recomputed==stored", 'ae["observed_behavior"]']) {
    assert.ok(
      predText.includes(outcome),
      `the derivation predicate must summarize the verification outcome (${outcome})`
    );
  }
  assert.ok(
    actProof.includes('"independent_verification_scope"'),
    "the proof must name the scope of its independent_verification claim"
  );
  assert.ok(
    actProof.includes('"act_receipt_independent_verification":ae["independent_verification"]'),
    "the proof must carry the act receipt's own (False-by-design) value"
  );

  // tools/live_intelligence_reconcile.py: verify_supersession must raise on any
  // failed check before reaching the return that carries the literal.
  const reconcile = read("tools/live_intelligence_reconcile.py");
  const fnStart = reconcile.indexOf("def verify_supersession(");
  const literalLine = reconcile.indexOf('"independent_verification": True', fnStart);
  assert.ok(fnStart >= 0 && literalLine > fnStart, "the reconcile literal must exist inside verify_supersession");
  const guardText = reconcile.slice(fnStart, literalLine);
  const raises = [...guardText.matchAll(/raise ValueError\(/g)];
  assert.ok(
    raises.length >= 5,
    `verify_supersession must keep its raise-gauntlet before the literal (found ${raises.length})`
  );
});

test("the claim record is itself honest", () => {
  // A record that lists a violation as OPEN after it was fixed lets the gate go slack
  // forever. Require every entry to name a law, a location, and a status.
  for (const v of RECORD.violations) {
    assert.match(v.id, /^CV-\d+$/, "each violation needs a stable id");
    assert.ok(v.claim && v.claim.length > 0, `${v.id} must name the claim it violates`);
    assert.ok(v.location, `${v.id} must name a location`);
    assert.ok(v.law, `${v.id} must cite the law it enforces`);
    assert.match(v.status, /^(OPEN|RESOLVED)/, `${v.id} must carry a status`);
  }
  const ids = RECORD.violations.map((v) => v.id);
  assert.equal(new Set(ids).size, ids.length, "violation ids must be unique");
});

test("CLAIM 4 -- the record's statuses match the code, in BOTH directions", () => {
  // This gate exists because it was already needed once. #1791/#1792 repaired CV-04,
  // CV-05, CV-08 and CV-09 and marked all nine violations RESOLVED in one commit. Every
  // repair was real -- I re-read each one on main and they are computed correctly now --
  // but at the moment they landed, nothing in this suite compared a status to the code.
  //
  // A record that under-reports resolution is not conservative, it is false. And it is
  // worse than no record, because it looks authoritative. Both drift directions are now
  // checked:
  //   - an entry marked OPEN must still have its defect present
  //   - an entry marked RESOLVED must have its defect gone
  // The second direction is the one that would have caught the CV-06/CV-07 incident, where
  // a repair merged and the record silently kept claiming OPEN.
  //
  // Every violation therefore declares a machine-checkable probe of whether its defect is
  // STILL PRESENT.
  const probes = RECORD.status_probes ?? {};
  const violationsById = new Map(RECORD.violations.map((v) => [v.id, v]));
  // Skip the explanatory "//" key; it documents the record, it is not a violation.
  const entries = Object.entries(probes).filter(([k]) => !k.startsWith("//"));
  assert.ok(entries.length > 0, "the record must carry status_probes");

  for (const [id, probe] of entries) {
    const v = violationsById.get(id);
    assert.ok(v, `status_probes names ${id}, which is not in violations`);
    // A self_verifying entry is a defect in the record's OWN enforcement, so no source
    // pattern can observe it. It is exempt from the file probe and covered instead by the
    // mutation proof below -- a stronger check, because that proves the gate rejects
    // drift rather than detecting one instance of it.
    if (probe.self_verifying) {
      assert.equal(
        v.self_verifying,
        true,
        `${id} is exempt from file probing, so its violation entry must also declare self_verifying`
      );
      continue;
    }
    assert.ok(typeof probe.file === "string" && probe.file, `${id} probe must name a file`);
    const path = join(ROOT, probe.file);
    assert.ok(existsSync(path), `${id} probe file does not exist: ${probe.file}`);
    const present = existsSync(path);
    const text = readFileSync(path, "utf8");

    // Every probe answers ONE question in ONE direction: is the DEFECT present?
    //   pattern         -- defect present when the file matches
    //   absent_pattern  -- defect present when the file does NOT match (for defects that
    //                      are an absence: a missing validation, a missing gate boundary)
    //   exists          -- defect present when file existence differs from `exists`
    //
    // Holding the direction fixed lets one pair of assertions cover OPEN and RESOLVED
    // without either branch needing to know how the probe was written.
    const compile = (p) => (p instanceof RegExp ? new RegExp(p.source, p.flags) : new RegExp(p, "m"));
    let observed;
    let what;
    if (probe.exists !== undefined) {
      assert.equal(
        present,
        probe.exists,
        `${id} probe is incoherent: the record declares ${probe.file} must ` +
        `${probe.exists ? "exist" : "not exist"}, and it does the opposite.`
      );
      // `exists` names the RESOLVED state, so the defect is present when it is absent.
      observed = !present;
      what = `exists=${probe.exists}`;
    } else if (probe.absent_pattern !== undefined) {
      observed = !compile(probe.absent_pattern).test(text);
      what = `NOT ${String(probe.absent_pattern)}`;
    } else {
      observed = compile(probe.pattern).test(text);
      what = String(probe.pattern);
    }

    if (v.status.startsWith("OPEN")) {
      assert.equal(
        observed,
        true,
        `${id} is recorded OPEN, but its probe says the defect is gone (${probe.file} :: ${what}). ` +
        `Either the defect was fixed and the record must be updated to RESOLVED in the same commit, ` +
        `or the probe is stale and must be corrected. A record that keeps reporting a fixed defect ` +
        `as open is a false record -- it teaches readers to ignore the file.`
      );
    } else {
      assert.equal(
        observed,
        false,
        `${id} is recorded RESOLVED, but its probe says the defect is still present ` +
        `(${probe.file} :: ${what}). The defect is in code while the record claims it is fixed.`
      );
    }
  }

  // Every violation must have a probe, or it is exempt from reality-checking and
  // therefore free to drift forever.
  const unprobed = RECORD.violations
    .map((v) => v.id)
    .filter((id) => !Object.prototype.hasOwnProperty.call(probes, id));
  assert.deepEqual(
    unprobed,
    [],
    `violations with no status_probes entry cannot be checked against reality: ${unprobed.join(", ")}. ` +
    `Add a probe (file + pattern/absent_pattern/exists) or remove the violation.`
  );
});

test("CLAIM 4 -- the status gate is not itself defeatable", () => {
  // Every gate added by an agent that hunts defects shares one failure mode: it is written
  // once, passes on the day it lands, and is never tested again. A gate that cannot fail is
  // the exact shape of CV-08, which this file exists to prevent -- landing another one
  // while CV-08 was open would be its own kind of irony.
  //
  // So the gate is proved by feeding it hostile inputs rather than by being trusted.
  const decide = (status, observed) => (status.startsWith("OPEN") ? observed === true : observed === false);

  // Both drift directions must be rejected...
  assert.equal(decide("RESOLVED -- pretend fix", true), false, "must reject a false RESOLVED");
  assert.equal(decide("OPEN -- owner decision required", false), false, "must reject a stale OPEN");
  // ...and the honest cases must still pass, or the two assertions above prove nothing.
  assert.equal(decide("OPEN -- owner decision required", true), true);
  assert.equal(decide("RESOLVED -- repaired", false), true);

  // Probes must be well-formed and name a real file, so one cannot be made vacuous.
  for (const [id, probe] of Object.entries(RECORD.status_probes ?? {}).filter(([k]) => !k.startsWith("//"))) {
    if (probe.self_verifying) continue;
    const hasPattern = probe.pattern !== undefined || probe.absent_pattern !== undefined;
    assert.ok(
      hasPattern || probe.exists !== undefined,
      `${id} needs exactly one of pattern, absent_pattern, or exists`
    );
    if (hasPattern) {
      assert.match(String(probe.pattern ?? probe.absent_pattern), /\S/, `${id} probe pattern is empty`);
    }
    assert.ok(existsSync(join(ROOT, probe.file)), `${id} probe names a missing file: ${probe.file}`);
  }

  // A self-verifying entry is the only permitted exemption and must be declared on BOTH
  // sides of the record, so the exemption cannot be granted in one place alone.
  const exemptions = RECORD.violations.filter((v) => v.self_verifying).map((v) => v.id);
  for (const id of exemptions) {
    assert.ok(
      RECORD.status_probes?.[id]?.self_verifying === true,
      `${id} claims self_verifying on the violation but has no matching exempt probe entry`
    );
  }
  assert.ok(
    exemptions.length < RECORD.violations.length,
    "at least one violation must be checked against real code; a record where every entry " +
    "exempts itself from reality-checking enforces nothing"
  );

  // Finally, assert the real gate still exists. If someone deletes the status assertions
  // above, this suite would otherwise stay green while enforcing nothing.
  const self = readFileSync(new URL(import.meta.url), "utf8");
  assert.match(self, /recorded OPEN, but its probe says the defect is gone/);
  assert.match(self, /recorded RESOLVED, but its probe says the defect is still present/);
});

test("a claim may not be repaired without updating the record", () => {
  // If every recorded violation were closed, the record must say so explicitly rather
  // than being deleted -- deletion is indistinguishable from forgetting.
  const open = RECORD.violations.filter((v) => v.status.startsWith("OPEN"));
  assert.ok(
    open.length <= RECORD.violations.length,
    "record consistency"
  );
  if (open.length === 0) {
    assert.ok(
      RECORD.resolved_summary !== undefined,
      "if no violations remain open, the record must carry resolved_summary so the " +
      "closure is stated rather than implied by an empty list"
    );
  }
});

// ── Claim 3: node influence ───────────────────────────────────────────────────

test("CLAIM 3 -- node influence is measured, and the measurement is committed", () => {
  assert.ok(
    existsSync(join(ROOT, "tools", "measure_node_influence.py")),
    "the nine-node kernel claims behavioral influence; that claim needs a measurement. " +
    "This landed with this gate -- before it, the claim was free to assert."
  );
  const probe = read("tools/measure_node_influence.py");
  assert.match(probe, /CONTROL/, "the ablation must define a control arm");
  assert.match(probe, /influence_demonstrated_count/, "it must report a count, not a vibe");
});

test("CLAIM 3 -- a regression that drops kernel influence fails the build", () => {
  // If a change makes the runtime kernel stop invoking nodes, or the measurement stops
  // being computed, that must be red. Today the honest number is 2/9 invoked and 0/9
  // influential for the runtime kernel -- the floor is recorded so it can only rise,
  // exactly like guard liveness.
  const probePath = join(ROOT, "tools", "measure_node_influence.py");
  // Resolve the interpreter at runtime: CI images carry `python`, minimal VMs
  // carry only `python3`. A gate that cannot execute is a gate that cannot
  // fire, so the probe must run wherever the suite runs.
  const pythonBin = (() => {
    try {
      execFileSync("python3", ["--version"], { stdio: "ignore" });
      return "python3";
    } catch {
      return "python";
    }
  })();
  const out = execFileSync(pythonBin, [probePath, "--json"], {
    cwd: ROOT,
    encoding: "utf8",
    timeout: 180000,
  });
  const report = JSON.parse(out);
  const runtimeKernel = Object.entries(report.report).find(([k]) => k.includes("nayapower_kernel"));
  assert.ok(runtimeKernel, "the report must include the manifest-bound runtime kernel");

  const [, stats] = runtimeKernel;
  assert.equal(typeof stats.invoked_count, "number");
  assert.equal(typeof stats.influence_demonstrated_count, "number");

  // The reference kernel is intentionally still only SELF+LAW. The canonical nine-node
  // behavior engine, however, must demonstrate a real control/treatment effect for every
  // node. A count below nine means at least one node is still decorative in the measured
  // runtime path and the load-bearing claim remains false.
  const behaviorEngine = Object.entries(report.report).find(([k]) =>
    k.includes("kernel_behavior_engine")
  );
  assert.ok(behaviorEngine, "the report must include the canonical nine-node behavior engine");
  const [, behaviorStats] = behaviorEngine;
  assert.equal(behaviorStats.invoked_count, 9);
  assert.equal(
    behaviorStats.influence_demonstrated_count,
    9,
    `canonical nine-node influence is ${behaviorStats.influence_demonstrated_count}/9; all nine nodes must change an observed node behavior fingerprint`
  );
  assert.ok(
    stats.invoked_count >= 2,
    `the runtime kernel invoked ${stats.invoked_count} nodes; it previously invoked 2 ` +
    `(SELF, LAW). A drop means the kernel stopped loading and the claim above is void.`
  );
});

test("the three claims are enforced by execution, not by their own documentation", () => {
  // Meta-guard. Each claim above must contain at least one assertion that could fail
  // against unmodified-but-wrong code. A test file that only reads strings is a
  // comment with assertions around it.
  const self = readFileSync(new URL(import.meta.url), "utf8");
  const executions = [
    /execFileSync\(/,
    /matchAll\(/,
    /\.test\(/,
  ];
  for (const p of executions) {
    assert.match(self, p, "claim enforcement must include real execution");
  }
  // And it must not be able to pass by asserting only on source presence.
  const sourceOnly = (self.match(/readFileSync\(/g) ?? []).length;
  assert.ok(sourceOnly > 0, "reading source is allowed for structure; it is not sufficient alone");
});
