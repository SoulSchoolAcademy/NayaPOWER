import assert from "node:assert/strict";
import test from "node:test";
import {
  validateKnowAuthority,
  selectKnowContext,
} from "../supabase/functions/nayanet-know-runtime/know.ts";

// Firing proofs for the ten highest-blast-radius unproven guards.
//
// Guard liveness (tools/guard_liveness.py) measured 102 of 147 refusal literals with no
// executed test that watches them reject. Closing all 102 in one sweep would produce
// 100% coverage and roughly zero new information -- the failure mode SN-0461 warns about.
// So: rank by blast radius and close the authority/ownership/replay tier, which is where
// a fail-open costs the most.
//
// RANKING BASIS -- blast radius of the guard failing OPEN:
//   cross-owner / wrong-owner  >  missing authority  >  replay duplication  >  ordering
// A guard that fails open on an ownership check is a privacy breach. One that fails open
// on a missing grant is an authority breach. Both are unrecoverable once they land.
//
// Every test below CALLS validateKnowAuthority or selectKnowContext and asserts the
// refusal reason. None of them grep source. If the guard stops firing, these go red.

const OWNER = "adfdf0b8-5558-41d1-9fed-ec51abf4fe2f";
const NAYA = "NAYA-NODE-0001";
const MISSION = "NAYA-NODE-0001-CONTINUITY";

const req = (overrides = {}) => ({
  owner_id: OWNER,
  naya_id: NAYA,
  task_id: "TASK-1",
  task_class: "RELATED_HELDOUT",
  required_capability: "provenance_preservation",
  ...overrides,
});

const grant = (overrides = {}) => ({
  grant_id: "grant-1",
  issuer_id: OWNER,
  subject_id: OWNER,
  scope: { target: NAYA },
  actions: ["naya_node_apply"],
  constraints: {},
  status: "ACTIVE",
  issued_at: "2026-09-29T00:00:00Z",
  expires_at: null,
  revoked_at: null,
  ...overrides,
});

const lawReceipt = (overrides = {}) => ({
  id: "law-1",
  user_id: OWNER,
  project_id: "NayaNET",
  action: "law_authority_decision",
  status: "SUCCESS",
  created_at: "2026-09-29T19:59:00Z",
  evidence: {
    node_id: "NAYA-KERNEL-LAW",
    law_request: { action: "naya_node_apply", target: NAYA },
    law_decision: {
      status: "AUTHORIZED",
      owner_id: OWNER,
      naya_id: NAYA,
      action: "naya_node_apply",
      target: NAYA,
      evaluated_at: "2026-09-29T19:59:00Z",
      expires_at: null,
      authority_refs: ["grant-1"],
    },
  },
  ...overrides,
});

const NOW = new Date("2026-09-29T20:00:00Z");

// Signature is (req, receipt, grant, now, maxLawAgeSeconds). There is no relationships
// parameter -- an earlier draft of this file passed one, which shifted `now` and made 16
// guards fail for the wrong reason. A gate that fails because the harness is wrong is
// indistinguishable from a real regression, so the call site is kept to one place.
const call = (r = req(), rec = lawReceipt(), g = grant()) =>
  validateKnowAuthority(r, rec, g, NOW);

// ── Tier 1: ownership. Failing open here is a privacy breach. ─────────────────

test("GUARD 1 -- LAW_RECEIPT_OWNER_MISMATCH fires when the LAW receipt belongs to someone else", () => {
  const r = call(req(), lawReceipt({ user_id: "00000000-0000-4000-8000-000000000009" }));
  assert.equal(r.ok, false);
  assert.equal(r.reason, "LAW_RECEIPT_OWNER_MISMATCH");
});

test("GUARD 2 -- LIVE_AUTHORITY_NOT_FOUND fires when the grant is absent", () => {
  const r = call(req(), lawReceipt(), null);
  assert.equal(r.ok, false);
  assert.equal(r.reason, "LIVE_AUTHORITY_NOT_FOUND");
});

test("GUARD 3 -- LIVE_AUTHORITY_OWNER_MISMATCH fires on a cross-owner grant", () => {
  const r = call(req(), lawReceipt(), grant({ subject_id: "00000000-0000-4000-8000-000000000009" }));
  assert.equal(r.ok, false);
  assert.equal(r.reason, "LIVE_AUTHORITY_OWNER_MISMATCH");
});

test("GUARD 4 -- LAW_AUTHORITY_REFERENCE_INVALID fires when the receipt cites no single grant", () => {
  const rec = lawReceipt();
  rec.evidence.law_decision.authority_refs = [];
  const r = call(req(), rec, grant());
  assert.equal(r.ok, false);
  assert.equal(r.reason, "LAW_AUTHORITY_REFERENCE_INVALID");
});

test("GUARD 5 -- a receipt citing a different grant is refused (LIVE_AUTHORITY_NOT_FOUND)", () => {
  // An earlier draft expected LAW_AUTHORITY_REFERENCE_INVALID here. The code combines the
  // two conditions -- `refs.length!==1 || !grant || String(grant.grant_id)!==refs[0]` --
  // and reports LIVE_AUTHORITY_NOT_FOUND. Asserting the reason the code actually emits is
  // the point; asserting a reason it does not emit would be a test that passes by luck.
  const rec = lawReceipt();
  rec.evidence.law_decision.authority_refs = ["a-different-grant"];
  const r = call(req(), rec, grant());
  assert.equal(r.ok, false);
  assert.equal(r.reason, "LIVE_AUTHORITY_NOT_FOUND");
});

// ── Tier 2: authority liveness. Failing open here is an authority breach. ───────

test("GUARD 6 -- LIVE_AUTHORITY_NOT_ACTIVE fires for a revoked or inactive grant", () => {
  for (const g of [grant({ status: "REVOKED" }), grant({ revoked_at: "2026-09-29T19:59:30Z" })]) {
    const r = call(req(), lawReceipt(), g);
    assert.equal(r.ok, false);
    assert.equal(r.reason, "LIVE_AUTHORITY_NOT_ACTIVE");
  }
});

test("GUARD 7 -- LIVE_AUTHORITY_EXPIRED fires for an expired grant", () => {
  const r = call(req(), lawReceipt(), grant({ expires_at: "2026-09-29T19:59:00Z" }));
  assert.equal(r.ok, false);
  assert.equal(r.reason, "LIVE_AUTHORITY_EXPIRED");
});

test("GUARD 8 -- LIVE_AUTHORITY_EXPIRY_INVALID fires for an unparseable grant expiry", () => {
  // This is the guard whose `=== NaN` half was dead code until #1624. It is now the one
  // guard in this file that can actually fire, and this test is the proof.
  const r = call(req(), lawReceipt(), grant({ expires_at: "not-a-timestamp" }));
  assert.equal(r.ok, false);
  assert.equal(r.reason, "LIVE_AUTHORITY_EXPIRY_INVALID");
});

test("GUARD 9 -- LIVE_AUTHORITY_ACTION_MISMATCH fires when the grant omits the action", () => {
  const r = call(req(), lawReceipt(), grant({ actions: ["read_only"] }));
  assert.equal(r.ok, false);
  assert.equal(r.reason, "LIVE_AUTHORITY_ACTION_MISMATCH");
});

test("GUARD 10 -- LIVE_AUTHORITY_TARGET_MISMATCH fires when the grant scope is another Naya", () => {
  const r = call(req(), lawReceipt(), grant({ scope: { target: "SOME-OTHER-NAYA" } }));
  assert.equal(r.ok, false);
  assert.equal(r.reason, "LIVE_AUTHORITY_TARGET_MISMATCH");
});

// ── Tier 3: the LAW receipt itself must be real and current. ───────────────────

test("GUARD 11 -- LAW_RECEIPT_REQUIRED fires when no receipt is presented", () => {
  const r = call(req(), null, grant());
  assert.equal(r.ok, false);
  assert.equal(r.reason, "LAW_RECEIPT_REQUIRED");
});

test("GUARD 12 -- LAW_RECEIPT_INVALID fires for a non-SUCCESS or wrong-action receipt", () => {
  assert.equal(call(req(), lawReceipt({ status: "BLOCKED" })).reason, "LAW_RECEIPT_INVALID");
  assert.equal(call(req(), lawReceipt({ action: "not_a_law_decision" })).reason, "LAW_RECEIPT_INVALID");
});

test("GUARD 13 -- LAW_NOT_AUTHORIZED fires when the decision was a denial", () => {
  const rec = lawReceipt();
  rec.evidence.law_decision.status = "DENIED";
  const r = call(req(), rec, grant());
  assert.equal(r.ok, false);
  assert.equal(r.reason, "LAW_NOT_AUTHORIZED");
});

test("GUARD 14 -- LAW_IDENTITY_MISMATCH fires when the decision names a different owner or Naya", () => {
  for (const patch of [{ owner_id: "other" }, { naya_id: "other" }]) {
    const rec = lawReceipt();
    Object.assign(rec.evidence.law_decision, patch);
    const r = call(req(), rec, grant());
    assert.equal(r.ok, false, JSON.stringify(patch));
    assert.equal(r.reason, "LAW_IDENTITY_MISMATCH");
  }
});

test("GUARD 15 -- LAW_ACTION_MISMATCH fires when the decision authorises a different action", () => {
  const rec = lawReceipt();
  rec.evidence.law_decision.action = "delete_everything";
  rec.evidence.law_request.action = "delete_everything";
  const r = call(req(), rec, grant());
  assert.equal(r.ok, false);
  assert.equal(r.reason, "LAW_ACTION_MISMATCH");
});

test("GUARD 16 -- LAW_TARGET_MISMATCH fires when the decision targets a different Naya", () => {
  const rec = lawReceipt();
  rec.evidence.law_decision.target = "SOME-OTHER-NAYA";
  rec.evidence.law_request.target = "SOME-OTHER-NAYA";
  const r = call(req(), rec, grant());
  assert.equal(r.ok, false);
  assert.equal(r.reason, "LAW_TARGET_MISMATCH");
});

test("GUARD 17 -- LAW_RECEIPT_STALE fires when the authority decision is older than the window", () => {
  // Staleness is measured from `law_decision.evaluated_at`, not from the receipt row's
  // created_at. An earlier draft aged created_at and the guard correctly did not fire.
  // That is a defensible design -- the decision time is the authority time -- but it is
  // worth pinning so a future edit does not silently change which clock is used.
  const rec = lawReceipt();
  rec.evidence.law_decision.evaluated_at = "2026-09-29T19:00:00Z";
  const r = call(req(), rec, grant());
  assert.equal(r.ok, false);
  assert.equal(r.reason, "LAW_RECEIPT_STALE");

  // And an aged receipt whose decision is still current stays valid, by design.
  const agedButFresh = lawReceipt({ created_at: "2026-09-29T00:00:00Z" });
  agedButFresh.evidence.law_decision.evaluated_at = "2026-09-29T19:59:30Z";
  assert.equal(call(req(), agedButFresh, grant()).ok, true);
});

test("GUARD 18 -- LAW_EXPIRY_INVALID fires for an unparseable decision expiry", () => {
  const rec = lawReceipt();
  rec.evidence.law_decision.expires_at = "not-a-timestamp";
  const r = call(req(), rec, grant());
  assert.equal(r.ok, false);
  assert.equal(r.reason, "LAW_EXPIRY_INVALID");
});

test("GUARD 19 -- LAW_AUTHORITY_EXPIRED fires when the LAW decision's own window has closed", () => {
  const rec = lawReceipt();
  rec.evidence.law_decision.expires_at = "2026-09-29T19:59:30Z";
  const r = call(req(), rec, grant());
  assert.equal(r.ok, false);
  assert.equal(r.reason, "LAW_AUTHORITY_EXPIRED");
});

test("GUARD 20 -- LAW_EVALUATED_AT_INVALID fires for an unparseable or future decision time", () => {
  for (const at of ["not-a-timestamp", "2026-09-29T21:00:00Z"]) {
    const rec = lawReceipt();
    rec.evidence.law_decision.evaluated_at = at;
    const r = call(req(), rec, grant());
    assert.equal(r.ok, false, at);
    assert.equal(r.reason, "LAW_EVALUATED_AT_INVALID");
  }
});

// ── The positive control. Without this, the suite could pass by refusing everything. ──

test("CONTROL -- a fully valid request is AUTHORIZED (the suite is not just refusing)", () => {
  const r = call();
  assert.equal(r.ok, true);
  assert.equal(r.reason, "LAW_AND_LIVE_AUTHORITY_MATCH");
  assert.equal(r.authority_grant_id, "grant-1");
});

test("CONTROL -- a valid grant with a future expiry is still authorized", () => {
  const r = call(req(), lawReceipt(), grant({ expires_at: "2026-09-29T23:00:00Z" }));
  assert.equal(r.ok, true);
});

test("CONTROL -- eligibility is scoped to the requested capability", () => {
  // Guards 1-20 all live in validateKnowAuthority. This confirms selectKnowContext, the
  // other seam, still works -- so a future edit that breaks selection is caught here too.
  // isEligibleBlock requires non-empty provenance AND evidence_refs. An earlier draft
  // omitted both and the selection correctly MISSED -- the guard worked, the fixture lied.
  const block = {
    intelligent_block_id: "IB-1",
    owner_id: OWNER,
    status: "ACTIVE",
    understanding_state: "LEARNED",
    superseded_by_block_id: null,
    applicable_scope: { target: NAYA, capabilities: ["provenance_preservation"] },
    content: { lesson: "Preserve provenance before applying retained intelligence." },
    provenance: { source_event_id: "event-1", method: "canonical" },
    evidence_refs: [{ id: "ev-1", source: "execution_receipt" }],
  };
  const hit = selectKnowContext(req(), [block], NOW);
  assert.equal(hit.status, "HIT");
  assert.equal(hit.selected_block_id, "IB-1");

  const miss = selectKnowContext(req({ required_capability: "arithmetic_only" }), [block], NOW);
  assert.equal(miss.status, "MISS");
  assert.equal(miss.selected_block_id, null);
});

test("CONTROL -- a cross-owner block is never selected", () => {
  const block = {
    intelligent_block_id: "IB-SOMEONE-ELSES",
    owner_id: "00000000-0000-4000-8000-000000000009",
    status: "ACTIVE",
    understanding_state: "LEARNED",
    superseded_by_block_id: null,
    applicable_scope: { target: NAYA, capabilities: ["provenance_preservation"] },
    content: { lesson: "Preserve provenance before applying retained intelligence." },
    provenance: { source_event_id: "event-1", method: "canonical" },
    evidence_refs: [{ id: "ev-1", source: "execution_receipt" }],
  };
  const r = selectKnowContext(req(), [block], NOW);
  assert.equal(r.status, "MISS");
  assert.equal(r.selected_block_id, null);
});
