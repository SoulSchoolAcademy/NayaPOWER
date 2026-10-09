// WO3 acceptance proofs — through the REAL gate code, not mocks.
// Case A: pre-registered BAD candidate -> rejected with reason codes.
// Case B: verifiable candidate -> passes.
// Case C: forced gate error -> FAIL CLOSED (rejected), never open.
import {
  ADMISSION_SCHEMA,
  admit_candidate,
  canonicalJson,
  inputHash,
  rejection_log,
  GATE_EVALUATION_ERROR,
} from "../supabase/functions/nayanet-learning-verify/admission_gate.ts";

function validDesign(overrides = {}) {
  return {
    schema: ADMISSION_SCHEMA,
    claim: "Applying the retry-with-backoff lesson reduces failed capture writes on flaky networks.",
    falsification_condition: "If treatment and control show identical failure rates over 30 flaky-network trials, the claim is wrong.",
    task: "capture-write-retry",
    success_criterion: "Treatment arm shows >=20% fewer failed writes than control over 30 trials.",
    criterion_independent_of_lesson: true,
    criterion_registered_at: "2026-10-09T09:00:00Z",
    doer: "naya-5",
    scorer: "naya-2",
    measurement: { method: "machine", detail: "write-failure counter" },
    arms: {
      treatment: { observable: "retries each failed write up to 3x with backoff", measured_at: "2026-10-09T10:00:00Z" },
      control: { observable: "fails the write immediately, no retry", measured_at: "2026-10-09T10:05:00Z" },
    },
    asserts_behavioral_change: true,
    behavioral_measure: "failed-write count per 30-trial run",
    outcome: "pending",
    ...overrides,
  };
}

// The EXACT fail-closed wrapper pattern from index.ts (mode==='candidate' write site).
function gatedWrite(admissionInput, candidateId) {
  const gateHash = inputHash(canonicalJson(admissionInput));
  let gateResult;
  try {
    gateResult = admit_candidate(admissionInput);
  } catch (gateErr) {
    console.log(`ADMISSION_GATE_ERROR input_hash=${gateHash} error=${gateErr instanceof Error ? gateErr.message : String(gateErr)}`);
    return { http: 500, body: { ok: false, error: "ADMISSION_GATE_ERROR", reason: GATE_EVALUATION_ERROR }, wrote: false };
  }
  console.log(`ADMISSION_GATE input_hash=${gateHash} admitted_as=${gateResult.admitted_as} reasons=${gateResult.reasons.join(",") || "-"}`);
  if (gateResult.admitted_as === "REJECTED") {
    console.log(rejection_log(candidateId, gateResult));
    return { http: 422, body: { ok: false, error: "ADMISSION_REJECTED", reasons: gateResult.reasons }, wrote: false };
  }
  const status = gateResult.admitted_as === "NOT_VERIFIED" ? "NOT_VERIFIED" : "CANDIDATE";
  return { http: 200, body: { ok: true, admitted_as: gateResult.admitted_as }, wrote: true, status };
}

let failures = 0;
function check(name, cond, detail) {
  console.log(`${cond ? "PASS" : "FAIL"} ${name}${detail ? " — " + detail : ""}`);
  if (!cond) failures++;
}

// --- Case A: pre-registered BAD candidate (unverifiable) -> rejected with reason codes
const bad = validDesign({
  claim: "Applying the lesson changes behavior.",
  falsification_condition: "if applying the lesson did not change behavior", // tautology in costume
  doer: "Naya-5",
  scorer: "naya-5 ", // same seat, case/whitespace variant
});
const ra = gatedWrite(bad, "block-BAD-001");
check("A1 bad candidate rejected (http 422)", ra.http === 422);
check("A2 reason TAUTOLOGICAL_FALSIFICATION", ra.body.reasons.includes("TAUTOLOGICAL_FALSIFICATION"), ra.body.reasons.join(","));
check("A3 reason DOER_EQUALS_SCORER", ra.body.reasons.includes("DOER_EQUALS_SCORER"));
check("A4 nothing written", ra.wrote === false);

// --- Case B: verifiable candidate -> passes
const good = validDesign();
const rb = gatedWrite(good, "block-GOOD-001");
check("B1 good candidate passes (http 200)", rb.http === 200);
check("B2 admitted as CANDIDATE", rb.body.admitted_as === "CANDIDATE");
check("B3 row would be written", rb.wrote === true && rb.status === "CANDIDATE");

// --- Case C: forced gate error -> FAIL CLOSED
// A Proxy whose property access throws simulates ANY unexpected gate failure
// (corrupt input, runtime fault) through the real code path.
const poisoned = new Proxy({}, { get() { throw new Error("FORCED_GATE_FAULT"); } });
const rc = gatedWrite(poisoned, "block-POISON-001");
check("C1 forced error -> rejected (http 500)", rc.http === 500);
check("C2 reason GATE_EVALUATION_ERROR", rc.body.reason === GATE_EVALUATION_ERROR);
check("C3 nothing written (door stayed closed)", rc.wrote === false);

console.log(failures === 0 ? "ALL WO3 PROOFS GREEN" : `${failures} PROOF(S) FAILED`);
process.exit(failures === 0 ? 0 : 1);
