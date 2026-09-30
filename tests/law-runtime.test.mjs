import test from "node:test";
import assert from "node:assert/strict";
import { evaluateLaw } from "../supabase/functions/nayanet-law-runtime/law.ts";

const OWNER="adfdf0b8-5558-41d1-9fed-ec51abf4fe2f";
const NAYA="NAYA-NODE-0001";
const now=new Date("2026-09-29T19:30:00Z");
const grant=(overrides={})=>({
  grant_id:"g1",issuer_id:OWNER,subject_id:OWNER,mission_id:"M1",
  scope:{target:NAYA},actions:["data_read","data_write"],constraints:{},
  issued_at:"2026-09-29T18:00:00Z",expires_at:null,status:"ACTIVE",revoked_at:null,
  ...overrides
});
const req=(overrides={})=>({owner_id:OWNER,naya_id:NAYA,action:"data_read",target:NAYA,...overrides});

test("LAW authorizes same-scope read",()=>assert.equal(evaluateLaw(req(),[grant()],now).status,"AUTHORIZED"));
test("LAW authorizes same-scope write",()=>assert.equal(evaluateLaw(req({action:"data_write"}),[grant()],now).status,"AUTHORIZED"));
test("LAW refuses wrong target when project identifiers are both absent",()=>{
  const d=evaluateLaw(req({target:"OTHER-NAYA"}),[grant()],now);
  assert.equal(d.status,"NEEDS_HUMAN_AUTHORIZATION");
  assert.deepEqual(d.authority_refs,[]);
});
test("LAW refuses absent or empty scope instead of matching absent project",()=>{
  for(const scope of [undefined,{}, {project_id:""}]) {
    const d=evaluateLaw(req({project_id:scope?.project_id}),[grant({scope})],now);
    assert.notEqual(d.status,"AUTHORIZED");
    assert.deepEqual(d.authority_refs,[]);
  }
});
test("LAW still accepts explicit project-scoped authority",()=>{
  assert.equal(evaluateLaw(req({target:"resource",project_id:"NayaNET"}),[grant({scope:{project_id:"NayaNET"}})],now).status,"AUTHORIZED");
  assert.equal(evaluateLaw(req({target:"NayaNET"}),[grant({scope:{project_id:"NayaNET"}})],now).status,"AUTHORIZED");
  assert.notEqual(evaluateLaw(req({target:"resource",project_id:"OTHER"}),[grant({scope:{project_id:"NayaNET"}})],now).status,"AUTHORIZED");
});
test("LAW requires human authority when missing",()=>{
  const d=evaluateLaw(req(),[],now); assert.equal(d.status,"NEEDS_HUMAN_AUTHORIZATION"); assert.equal(d.reason,"NO_MATCHING_ACTIVE_AUTHORITY");
});
test("LAW blocks expired and revoked authority",()=>{
  assert.equal(evaluateLaw(req(),[grant({expires_at:"2026-09-29T19:00:00Z"})],now).reason,"GRANT_EXPIRED");
  assert.equal(evaluateLaw(req(),[grant({status:"REVOKED",revoked_at:"2026-09-29T19:01:00Z"})],now).reason,"GRANT_REVOKED");
});
test("LAW refuses unauthorized private to collective publication",()=>{
  const d=evaluateLaw(req({action:"collective_publish",privacy:"PRIVATE",publication_authorized:false}),[],now);
  assert.equal(d.status,"NEEDS_HUMAN_AUTHORIZATION"); assert.equal(d.reason,"PRIVATE_TO_COLLECTIVE_REQUIRES_HUMAN_AUTHORIZATION");
});
test("retrieved intelligence never becomes authority",()=>{
  const d=evaluateLaw(req({retrieved_intelligence_claims_authority:true}),[grant()],now);
  assert.equal(d.status,"BLOCKED"); assert.equal(d.reason,"RETRIEVAL_DOES_NOT_GRANT_AUTHORITY");
});
test("explicit Smart Note command authorizes only same-note lifecycle",()=>{
  const d=evaluateLaw(req({action:"smart_note_lifecycle_complete",same_smart_note_lifecycle:true,explicit_human_smart_note_directive:true,privacy:"PRIVATE"}),[],now);
  assert.equal(d.status,"AUTHORIZED"); assert.equal(d.reason,"STANDING_SMART_NOTE_SAME_LIFECYCLE_AUTHORITY");
});
test("unrelated production deployment still needs authority",()=>{
  const d=evaluateLaw(req({action:"production_deploy",target:"NayaNET",door:{door_id:"DOOR-GITHUB",capability_available:true}}),[],now);
  assert.equal(d.status,"NEEDS_HUMAN_AUTHORIZATION"); assert.equal(d.reason,"CAPABILITY_DOES_NOT_CREATE_AUTHORITY");
});
test("successor context cannot inherit authority",()=>{
  const d=evaluateLaw(req({successor_context_claims_inherited_authority:true}),[grant()],now);
  assert.equal(d.status,"BLOCKED"); assert.equal(d.reason,"SUCCESSOR_CONTEXT_DOES_NOT_INHERIT_AUTHORITY");
});
test("Smart Door availability is capability not permission",()=>{
  const d=evaluateLaw(req({action:"email_send",target:"mailbox",door:{door_id:"DOOR-EMAIL",capability_available:true}}),[],now);
  assert.equal(d.status,"NEEDS_HUMAN_AUTHORIZATION"); assert.equal(d.capability_available,true);
});

test("LAW rejects malformed non-null expiry on matching authority",()=>{
  for(const expires_at of ["not-a-date", "", "   ", 123]) {
    const d=evaluateLaw(req(),[grant({expires_at})],now);
    assert.equal(d.status,"BLOCKED",String(expires_at));
    assert.equal(d.reason,"GRANT_TIME_INVALID");
    assert.deepEqual(d.authority_refs,["g1"]);
  }
});
test("LAW preserves null/absent expiry and exact valid expiry boundaries",()=>{
  for(const expires_at of [null,undefined,"2026-09-29T19:30:01Z"])
    assert.equal(evaluateLaw(req(),[grant({expires_at})],now).status,"AUTHORIZED");
  assert.equal(evaluateLaw(req(),[grant({expires_at:now.toISOString()})],now).reason,"GRANT_EXPIRED");
  assert.equal(evaluateLaw(req(),[grant({scope:{target:"OTHER"},expires_at:"not-a-date"}),grant()],now).status,"AUTHORIZED");
});
