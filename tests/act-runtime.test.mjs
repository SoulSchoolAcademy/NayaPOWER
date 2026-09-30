import test from "node:test";
import assert from "node:assert/strict";
import { validateAct } from "../supabase/functions/nayanet-act-runtime/act.ts";

const OWNER="adfdf0b8-5558-41d1-9fed-ec51abf4fe2f";
const NAYA="NAYA-NODE-0001";
const NOW=new Date("2026-09-29T20:00:00Z");
const req=(x={})=>({owner_id:OWNER,naya_id:NAYA,law_receipt_id:"law1",action:"naya_node_apply",target:NAYA,door_id:"DOOR-AI",operation:"apply_retained_intelligence",...x});
const law=(x={})=>({
  id:"law1",user_id:OWNER,action:"law_authority_decision",status:"SUCCESS",
  evidence:{
    node_id:"NAYA-KERNEL-LAW",
    law_request:{action:"naya_node_apply",target:NAYA,door:{door_id:"DOOR-AI",operation:"apply_retained_intelligence"}},
    law_decision:{status:"AUTHORIZED",owner_id:OWNER,naya_id:NAYA,action:"naya_node_apply",target:NAYA,authority_refs:["g1"],evaluated_at:"2026-09-29T19:59:00Z",expires_at:null},
  },...x
});
const grant=(x={})=>({grant_id:"g1",issuer_id:OWNER,subject_id:OWNER,scope:{target:NAYA},actions:["naya_node_apply"],status:"ACTIVE",revoked_at:null,expires_at:null,...x});
const door=(x={})=>({door_id:"DOOR-AI",operation:"apply_retained_intelligence",authority_action:"naya_node_apply",target:NAYA,consequential:true,max_law_age_seconds:900,...x});

test("ACT accepts exact fresh authorized LAW receipt",()=>assert.equal(validateAct(req(),law(),grant(),door(),NOW).status,"READY"));
test("ACT revalidates the live grant behind an otherwise authorized LAW receipt",()=>{
  const cases = [
    ["missing", null, "LIVE_AUTHORITY_NOT_FOUND"],
    ["different grant", grant({grant_id:"g2"}), "LIVE_AUTHORITY_NOT_FOUND"],
    ["wrong issuer", grant({issuer_id:"other"}), "LIVE_AUTHORITY_OWNER_MISMATCH"],
    ["wrong subject", grant({subject_id:"other"}), "LIVE_AUTHORITY_OWNER_MISMATCH"],
    ["missing actions", grant({actions:undefined}), "LIVE_AUTHORITY_ACTION_MISMATCH"],
    ["wrong action", grant({actions:["production_deploy"]}), "LIVE_AUTHORITY_ACTION_MISMATCH"],
    ["missing scope", grant({scope:undefined}), "LIVE_AUTHORITY_TARGET_MISMATCH"],
    ["wrong target", grant({scope:{target:"OTHER"}}), "LIVE_AUTHORITY_TARGET_MISMATCH"],
  ];
  for (const [name, liveGrant, reason] of cases) {
    const decision = validateAct(req(),law(),liveGrant,door(),NOW);
    assert.equal(decision.status,"BLOCKED",name);
    assert.equal(decision.reason,reason,name);
    assert.equal(decision.law_receipt_id,"law1",name);
    assert.equal(decision.authority_grant_id,"g1",name);
  }
});

test("1 missing LAW receipt fails closed",()=>assert.equal(validateAct(req({law_receipt_id:""}),null,grant(),door(),NOW).reason,"LAW_RECEIPT_REQUIRED"));
test("2 non-authorized LAW receipt fails closed",()=>assert.equal(validateAct(req(),law({status:"BLOCKED"}),grant(),door(),NOW).reason,"LAW_NOT_AUTHORIZED"));
test("3 wrong owner or Naya fails closed",()=>{
  assert.equal(validateAct(req(),law({user_id:"other"}),grant(),door(),NOW).reason,"LAW_RECEIPT_OWNER_MISMATCH");
  const l=law(); l.evidence.law_decision.naya_id="OTHER"; assert.equal(validateAct(req(),l,grant(),door(),NOW).reason,"LAW_IDENTITY_MISMATCH");
});
test("4 requested action mismatch fails closed",()=>{
  const l=law(); l.evidence.law_request.action="other"; assert.equal(validateAct(req(),l,grant(),door(),NOW).reason,"AUTHORIZED_ACTION_MISMATCH");
});
test("5 target mismatch fails closed",()=>{
  const l=law(); l.evidence.law_decision.target="OTHER"; assert.equal(validateAct(req(),l,grant(),door(),NOW).reason,"AUTHORIZED_TARGET_MISMATCH");
});
test("6 stale LAW receipt fails where freshness matters",()=>{
  const l=law(); l.evidence.law_decision.evaluated_at="2026-09-29T19:00:00Z"; assert.equal(validateAct(req(),l,grant(),door(),NOW).reason,"LAW_RECEIPT_STALE");
});
test("7 broader Door authority than LAW fails closed",()=>assert.equal(validateAct(req(),law(),grant(),door({authority_action:"production_deploy"}),NOW).reason,"DOOR_AUTHORITY_BROADER_THAN_LAW"));
test("8 retrieved intelligence cannot stand in for authority",()=>assert.equal(validateAct(req({retrieved_intelligence_claims_authority:true}),law(),grant(),door(),NOW).reason,"RETRIEVAL_DOES_NOT_GRANT_AUTHORITY"));
test("9 successor context cannot reuse authority",()=>assert.equal(validateAct(req({successor_context_claims_inherited_authority:true}),law(),grant(),door(),NOW).reason,"SUCCESSOR_CONTEXT_DOES_NOT_INHERIT_AUTHORITY"));
test("10 unregistered/unobservable path fails before effect",()=>assert.equal(validateAct(req(),law(),grant(),null,NOW).reason,"SMART_DOOR_OPERATION_NOT_REGISTERED"));
test("revoked live grant invalidates previously authorized LAW receipt",()=>assert.equal(validateAct(req(),law(),grant({status:"REVOKED",revoked_at:"2026-09-29T19:59:30Z"}),door(),NOW).reason,"LIVE_AUTHORITY_NOT_ACTIVE"));

test("freshness cannot be established from missing, malformed or future LAW evaluation time",()=>{
  for (const value of [undefined, null, "", "not-a-date", "2026-09-29T20:00:01Z"]) {
    const l=law(); l.evidence.law_decision.evaluated_at=value;
    assert.equal(validateAct(req(),l,grant(),door(),NOW).reason,"LAW_RECEIPT_TIME_INVALID",String(value));
  }
});
test("malformed expiry on LAW decision or live grant fails closed",()=>{
  const l=law(); l.evidence.law_decision.expires_at="not-a-date";
  assert.equal(validateAct(req(),l,grant(),door(),NOW).reason,"LAW_AUTHORITY_TIME_INVALID");
  assert.equal(validateAct(req(),law(),grant({expires_at:"not-a-date"}),door(),NOW).reason,"LIVE_AUTHORITY_TIME_INVALID");
});
test("freshness and expiry boundaries are inclusive and unbounded expiry remains valid",()=>{
  const l=law(); l.evidence.law_decision.evaluated_at="2026-09-29T19:45:00Z";
  assert.equal(validateAct(req(),l,grant(),door(),NOW).status,"READY");
  l.evidence.law_decision.evaluated_at="2026-09-29T19:44:59Z";
  assert.equal(validateAct(req(),l,grant(),door(),NOW).reason,"LAW_RECEIPT_STALE");
  const expired=law(); expired.evidence.law_decision.expires_at=NOW.toISOString();
  assert.equal(validateAct(req(),expired,grant(),door(),NOW).reason,"LAW_AUTHORITY_EXPIRED");
  assert.equal(validateAct(req(),law(),grant({expires_at:NOW.toISOString()}),door(),NOW).reason,"LIVE_AUTHORITY_EXPIRED");
  assert.equal(validateAct(req(),law(),grant(),door(),NOW).status,"READY");
});
