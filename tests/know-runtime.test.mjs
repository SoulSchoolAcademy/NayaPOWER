import assert from "node:assert/strict";
import test from "node:test";
import { selectKnowContext, isEligibleBlock, deriveCapabilities, hasCallerSuppliedIntelligence, validateKnowAuthorization } from "../supabase/functions/nayanet-know-runtime/know.ts";

const OWNER="owner-1";
const req=(overrides={})=>({
  owner_id:OWNER,
  naya_id:"NAYA-NODE-0001",
  task_id:"KNOW-PROVENANCE-HELDOUT-001",
  task_class:"RELATED_HELDOUT",
  required_capability:"provenance_preservation",
  ...overrides
});
const good=(overrides={})=>({
  intelligent_block_id:"IB-VERIFIED-PROVENANCE",
  owner_id:OWNER,
  status:"DURABLE",
  understanding_state:"VERIFIED",
  owner_scope:"PRIVATE",
  applicable_scope:{target:"NAYA-NODE-0001"},
  content:{lesson:"Preserve provenance before applying retained intelligence; retrieval never grants authority."},
  provenance:{source:"AAA-LIVE-BRAIN"},
  evidence_refs:[{receipt:"proof-1"}],
  superseded_by_block_id:null,
  updated_at:"2026-09-29T00:00:00Z",
  ...overrides
});

test("KNOW selects an eligible owner-scoped block from task context without block identity",()=>{
  const out=selectKnowContext(req(),[
    good({intelligent_block_id:"IB-CANDIDATE",understanding_state:"CANDIDATE",updated_at:"2026-09-29T03:00:00Z"}),
    good()
  ]);
  assert.equal(out.status,"HIT");
  assert.equal(out.selected_block_id,"IB-VERIFIED-PROVENANCE");
  assert.equal(out.applicable,true);
  assert.equal(out.retrieval_creates_authority,false);
  assert.equal(out.handoff_to,"NAYA-KERNEL-PROVE");
});

test("KNOW returns a bounded miss for unrelated context",()=>{
  const out=selectKnowContext(req({
    task_id:"KNOW-UNRELATED-ARITHMETIC-001",
    task_class:"UNRELATED_NEGATIVE_TRANSFER",
    required_capability:"arithmetic_only"
  }),[good()]);
  assert.equal(out.status,"MISS");
  assert.equal(out.selected_block_id,null);
  assert.equal(out.applicable,false);
  assert.equal(out.reason,"NO_ELIGIBLE_APPLICABLE_INTELLIGENCE");
});

test("KNOW excludes cross-owner, candidate, deleted, and superseded intelligence",()=>{
  const blocks=[
    good({intelligent_block_id:"IB-CROSS",owner_id:"other-owner"}),
    good({intelligent_block_id:"IB-CANDIDATE",understanding_state:"CANDIDATE"}),
    good({intelligent_block_id:"IB-DELETED",status:"DELETED"}),
    good({intelligent_block_id:"IB-SUPERSEDED",superseded_by_block_id:"block-2"})
  ];
  assert.equal(blocks.some(b=>isEligibleBlock(req(),b)),false);
  assert.equal(selectKnowContext(req(),blocks).status,"MISS");
});

test("KNOW requires provenance and evidence",()=>{
  assert.equal(isEligibleBlock(req(),good({provenance:{}})),false);
  assert.equal(isEligibleBlock(req(),good({evidence_refs:[]})),false);
});

test("KNOW prefers structured applicability capability over bounded legacy derivation",()=>{
  const block=good({
    applicable_scope:{target:"NAYA-NODE-0001",capabilities:["structured_capability"]},
    content:{lesson:"Preserve provenance before applying retained intelligence"}
  });
  assert.deepEqual(deriveCapabilities(block),["structured_capability"]);
  assert.equal(selectKnowContext(req({required_capability:"provenance_preservation"}),[block]).status,"MISS");
  assert.equal(selectKnowContext(req({required_capability:"structured_capability"}),[block]).status,"HIT");
});

test("KNOW deterministically chooses the newest eligible applicable block",()=>{
  const older=good({intelligent_block_id:"IB-OLD",updated_at:"2026-09-28T00:00:00Z"});
  const newer=good({intelligent_block_id:"IB-NEW",updated_at:"2026-09-29T00:00:00Z"});
  assert.equal(selectKnowContext(req(),[older,newer]).selected_block_id,"IB-NEW");
});


test("KNOW excludes intelligence scoped to another target",()=>{
  const other=good({applicable_scope:{target:"OTHER-NAYA",capabilities:["provenance_preservation"]}});
  assert.equal(isEligibleBlock(req(),other),false);
  assert.equal(selectKnowContext(req(),[other]).status,"MISS");
});

test("KNOW rejects every caller-supplied intelligence or answer alias",()=>{
  for(const body of [
    {block_id:"b1"},
    {intelligent_block_id:"IB-X"},
    {answer:"PRESERVE"},
    {intelligence_content:"lesson"},
    {lesson:"Preserve provenance"},
    {intelligence:{id:"IB-X"}}
  ]) assert.equal(hasCallerSuppliedIntelligence(body),true);
  assert.equal(hasCallerSuppliedIntelligence({task_id:"t",task_class:"c",required_capability:"x"}),false);
});

const OWNER_ID="adfdf0b8-5558-41d1-9fed-ec51abf4fe2f";
const NAYA_ID="NAYA-NODE-0001";
const NOW=new Date("2026-09-29T20:00:00Z");
const law=(overrides={})=>({
  id:"law-1",user_id:OWNER_ID,action:"law_authority_decision",status:"SUCCESS",
  evidence:{node_id:"NAYA-KERNEL-LAW",law_request:{action:"naya_node_apply",target:NAYA_ID},
    law_decision:{status:"AUTHORIZED",owner_id:OWNER_ID,naya_id:NAYA_ID,action:"naya_node_apply",target:NAYA_ID,
      evaluated_at:"2026-09-29T19:59:00Z",authority_refs:["grant-1"]}},
  ...overrides
});
const grant=(overrides={})=>({
  grant_id:"grant-1",issuer_id:OWNER_ID,subject_id:OWNER_ID,scope:{target:NAYA_ID},
  actions:["naya_node_apply"],status:"ACTIVE",revoked_at:null,expires_at:"2026-09-29T21:00:00Z",...overrides
});

test("KNOW requires current live authority in addition to the LAW receipt",()=>{
  assert.equal(validateKnowAuthorization(law(),grant(),OWNER_ID,NAYA_ID,NOW).ok,true);
  assert.equal(validateKnowAuthorization(law(),null,OWNER_ID,NAYA_ID,NOW).reason,"LIVE_AUTHORITY_NOT_FOUND");
  assert.equal(validateKnowAuthorization(law(),grant({status:"REVOKED",revoked_at:"2026-09-29T19:59:30Z"}),OWNER_ID,NAYA_ID,NOW).reason,"LIVE_AUTHORITY_NOT_ACTIVE");
  assert.equal(validateKnowAuthorization(law(),grant({expires_at:"2026-09-29T19:59:30Z"}),OWNER_ID,NAYA_ID,NOW).reason,"LIVE_AUTHORITY_EXPIRED");
  assert.equal(validateKnowAuthorization(law(),grant({scope:{target:"OTHER-NAYA"}}),OWNER_ID,NAYA_ID,NOW).reason,"LIVE_AUTHORITY_TARGET_MISMATCH");
});

test("KNOW refuses missing, malformed, or stale LAW freshness",()=>{
  const missing=law();
  delete missing.evidence.law_decision.evaluated_at;
  assert.equal(validateKnowAuthorization(missing,grant(),OWNER_ID,NAYA_ID,NOW).reason,"LAW_FRESHNESS_MISSING_OR_INVALID");
  const malformed=law();
  malformed.evidence.law_decision.evaluated_at="not-a-date";
  assert.equal(validateKnowAuthorization(malformed,grant(),OWNER_ID,NAYA_ID,NOW).reason,"LAW_FRESHNESS_MISSING_OR_INVALID");
  const stale=law();
  stale.evidence.law_decision.evaluated_at="2026-09-29T19:30:00Z";
  assert.equal(validateKnowAuthorization(stale,grant(),OWNER_ID,NAYA_ID,NOW).reason,"LAW_RECEIPT_STALE");
});
