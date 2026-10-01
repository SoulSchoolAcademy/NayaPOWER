import test from "node:test";
import assert from "node:assert/strict";
import {
  recomputeActIdempotencyFingerprint,
  assessActIdempotencyReceipt,
} from "../supabase/functions/nayanet-causal-verify/verify-act-idempotency.ts";

const OWNER = "adfdf0b8-5558-41d1-9fed-ec51abf4fe2f";
const NAYA = "NAYA-NODE-0001";

const INPUTS = {
  authority_grant_id: "grant-p7-test-001",
  mission_id: "NAYA-NODE-0001-CONTINUITY",
  action: "naya_node_apply",
  target: NAYA,
  canonical_block_id: "IB-NAYA-NODE-0001-0001",
  canonical_digest: "digest-p7-test-abc123",
};

const evidenceFor = (fingerprint, overrides = {}) => ({
  idempotency_request_fingerprint: fingerprint,
  authority_grant_id: INPUTS.authority_grant_id,
  authority_mission: INPUTS.mission_id,
  requested_action: INPUTS.action,
  requested_target: INPUTS.target,
  canonical_block_id: INPUTS.canonical_block_id,
  canonical_digest: INPUTS.canonical_digest,
  ...overrides,
});

const actReceipt = (evidence) => ({
  id: "receipt-p7-001",
  user_id: OWNER,
  project_id: "NayaNET",
  action: "NAYA-NODE-0001-VERIFIED-AI-ACTION",
  status: "SUCCESS",
  evidence,
});

test("P7 known-answer: canonicalization is pinned byte-exact", async () => {
  // Guards against silent drift in the fingerprint canonical form. If the
  // ACT executor's hashing changes, this fails loudly instead of VERIFY
  // silently agreeing with a new (unreviewed) scheme.
  const fp = await recomputeActIdempotencyFingerprint({
    authority_grant_id: "grant-known-answer-001",
    mission_id: "NAYA-NODE-0001-CONTINUITY",
    action: "naya_node_apply",
    target: "NAYA-NODE-0001",
    canonical_block_id: "IB-NAYA-NODE-0001-0001",
    canonical_digest: "known-digest-abc",
  });
  assert.equal(
    fp,
    "e54c290a4e8ffcefa79937188a42757fda65dc6c8b087f1fd6fbb30311a0f1b2",
  );
});

test("P7 (a): recomputation matches on a valid receipt", async () => {
  const fingerprint = await recomputeActIdempotencyFingerprint(INPUTS);
  const assessment = await assessActIdempotencyReceipt(
    actReceipt(evidenceFor(fingerprint)),
  );
  assert.equal(assessment.ok, true);
  assert.equal(assessment.code, "ACT_IDEMPOTENCY_RECOMPUTED");
  assert.equal(assessment.fingerprint_matches, true);
  assert.equal(assessment.fail_closed, false);
  assert.equal(assessment.recomputed_fingerprint, fingerprint);
  assert.equal(assessment.claimed_fingerprint, fingerprint);
});

test("P7 (b): tampered fingerprint fails closed", async () => {
  const fingerprint = await recomputeActIdempotencyFingerprint(INPUTS);
  const tampered =
    fingerprint.slice(0, 8) +
    (fingerprint[8] === "a" ? "b" : "a") +
    fingerprint.slice(9);
  assert.notEqual(tampered, fingerprint);
  const assessment = await assessActIdempotencyReceipt(
    actReceipt(evidenceFor(tampered)),
  );
  assert.equal(assessment.ok, false);
  assert.equal(assessment.code, "IDEMPOTENCY_FINGERPRINT_MISMATCH");
  assert.equal(assessment.fingerprint_matches, false);
  assert.equal(assessment.fail_closed, true);
});

test("P7 (b2): tampered fingerprint input fails closed", async () => {
  // Attacker changes a persisted input (e.g. swaps the digest) but leaves
  // the fingerprint: recomputation from the tampered inputs must mismatch.
  const fingerprint = await recomputeActIdempotencyFingerprint(INPUTS);
  const assessment = await assessActIdempotencyReceipt(
    actReceipt(evidenceFor(fingerprint, { canonical_digest: "evil-digest" })),
  );
  assert.equal(assessment.ok, false);
  assert.equal(assessment.code, "IDEMPOTENCY_FINGERPRINT_MISMATCH");
  assert.equal(assessment.fail_closed, true);
});

test("P7 (c): missing fingerprint fails closed, not assumed", async () => {
  const { idempotency_request_fingerprint: _dropped, ...rest } =
    evidenceFor("unused");
  const assessment = await assessActIdempotencyReceipt(actReceipt(rest));
  assert.equal(assessment.ok, false);
  assert.equal(assessment.code, "FINGERPRINT_NOT_PERSISTED");
  assert.equal(assessment.fail_closed, true);
});

test("P7 (c2): incomplete fingerprint inputs fail closed, not assumed", async () => {
  const fingerprint = await recomputeActIdempotencyFingerprint(INPUTS);
  const { canonical_digest: _dropped, ...rest } = evidenceFor(fingerprint);
  const assessment = await assessActIdempotencyReceipt(actReceipt(rest));
  assert.equal(assessment.ok, false);
  assert.equal(assessment.code, "FINGERPRINT_INPUTS_INCOMPLETE");
  assert.deepEqual(assessment.missing_inputs, ["canonical_digest"]);
  assert.equal(assessment.fail_closed, true);
});

test("P7: non-ACT receipt fails closed", async () => {
  const assessment = await assessActIdempotencyReceipt({
    id: "receipt-other",
    user_id: OWNER,
    project_id: "NayaNET",
    action: "NAYA-NODE-0001-TREATMENT",
    status: "SUCCESS",
    evidence: {},
  });
  assert.equal(assessment.ok, false);
  assert.equal(assessment.code, "NOT_AN_ACT_EXECUTION_RECEIPT");
  assert.equal(assessment.fail_closed, true);
});

test("P7: null receipt fails closed", async () => {
  const assessment = await assessActIdempotencyReceipt(null);
  assert.equal(assessment.ok, false);
  assert.equal(assessment.code, "RECEIPT_NOT_FOUND");
  assert.equal(assessment.fail_closed, true);
});
