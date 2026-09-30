import assert from "node:assert/strict";
import test from "node:test";
import { selectKnowContext, isEligibleBlock, deriveCapabilities, validateKnowAuthority } from "../supabase/functions/nayanet-know-runtime/know.ts";

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


const NOW=new Date("2026-09-29T20:00:00Z");
const law=(overrides={})=>({
  id:"law-1",user_id:OWNER,action:"law_authority_decision",status:"SUCCESS",
  evidence:{
    node_id:"NAYA-KERNEL-LAW",
    law_request:{action:"naya_node_apply",target:"NAYA-NODE-0001"},
    law_decision:{
      status:"AUTHORIZED",owner_id:OWNER,naya_id:"NAYA-NODE-0001",action:"naya_node_apply",target:"NAYA-NODE-0001",
      authority_refs:["grant-1"],evaluated_at:"2026-09-29T19:59:00Z",expires_at:null
    }
  },
  ...overrides
});
const grant=(overrides={})=>({
  grant_id:"grant-1",issuer_id:OWNER,subject_id:OWNER,scope:{target:"NAYA-NODE-0001"},
  actions:["naya_node_apply"],status:"ACTIVE",revoked_at:null,expires_at:null,...overrides
});

test("KNOW requires live authority, not only an old LAW receipt",()=>{
  assert.equal(validateKnowAuthority(req(),null,grant(),NOW).reason,"LAW_RECEIPT_REQUIRED");
  assert.equal(validateKnowAuthority(req(),law(),grant({status:"REVOKED",revoked_at:"2026-09-29T19:59:30Z"}),NOW).reason,"LIVE_AUTHORITY_NOT_ACTIVE");
  assert.equal(validateKnowAuthority(req(),law(),grant(),NOW).ok,true);
});

test("KNOW rejects malformed or stale LAW time",()=>{
  const malformed=law(); malformed.evidence.law_decision.evaluated_at="not-a-date";
  assert.equal(validateKnowAuthority(req(),malformed,grant(),NOW).reason,"LAW_EVALUATED_AT_INVALID");
  const stale=law(); stale.evidence.law_decision.evaluated_at="2026-09-29T19:00:00Z";
  assert.equal(validateKnowAuthority(req(),stale,grant(),NOW).reason,"LAW_RECEIPT_STALE");
});

test("KNOW rejects wrong live grant target",()=>{
  assert.equal(validateKnowAuthority(req(),law(),grant({scope:{target:"OTHER"}}),NOW).reason,"LIVE_AUTHORITY_TARGET_MISMATCH");
});

test("KNOW excludes capability-matching intelligence scoped to another target",()=>{
  const wrongTarget=good({applicable_scope:{target:"OTHER",capabilities:["provenance_preservation"]}});
  assert.equal(isEligibleBlock(req(),wrongTarget),false);
  assert.equal(selectKnowContext(req(),[wrongTarget]).status,"MISS");
});


test("KNOW refuses missing or future LAW evaluated_at",()=>{
  const missing=law();
  delete missing.evidence.law_decision.evaluated_at;
  assert.equal(validateKnowAuthority(req(),missing,grant(),NOW).reason,"LAW_EVALUATED_AT_INVALID");
  const future=law();
  future.evidence.law_decision.evaluated_at="2026-09-29T20:01:00Z";
  assert.equal(validateKnowAuthority(req(),future,grant(),NOW).reason,"LAW_EVALUATED_AT_INVALID");
});

test("KNOW accepts only the bounded naya_node_apply parent action",()=>{
  const wrong=law();
  wrong.evidence.law_request.action="intelligence_commit";
  wrong.evidence.law_decision.action="intelligence_commit";
  const broadGrant=grant({actions:["naya_node_apply","intelligence_commit"]});
  assert.equal(validateKnowAuthority(req(),wrong,broadGrant,NOW).reason,"LAW_ACTION_MISMATCH");
});
