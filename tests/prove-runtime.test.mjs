import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { assessKnowProof } from "../supabase/functions/nayanet-prove-runtime/prove.ts";

const OWNER="adfdf0b8-5558-41d1-9fed-ec51abf4fe2f";
const NAYA="NAYA-NODE-0001";
const NOW=new Date("2026-09-29T20:30:00Z");

const block=(overrides={})=>({
  intelligent_block_id:"IB-NAYA-NODE-0001-0001",
  owner_id:OWNER,
  status:"ACTIVE",
  understanding_state:"LEARNED",
  applicable_scope:{target:NAYA,capabilities:["provenance_preservation"]},
  content:{lesson:"Preserve provenance before applying retained intelligence; retrieval never grants authority."},
  provenance:{source_event_id:"event-1",method:"canonical"},
  evidence_refs:[{id:"ev-1",source:"execution_receipt"}],
  superseded_by_block_id:null,
  ...overrides
});

const grant=(overrides={})=>({
  grant_id:"grant-1",issuer_id:OWNER,subject_id:OWNER,
  scope:{target:NAYA},actions:["naya_node_apply"],
  status:"ACTIVE",revoked_at:null,expires_at:null,...overrides
});

const knowReceipt=(overrides={})=>({
  id:"know-receipt-1",user_id:OWNER,project_id:"NayaNET",
  action:"know_context_retrieval",status:"SUCCESS",created_at:"2026-09-29T20:29:00Z",
  evidence:{
    schema:"naya.know.receipt.v1",node_id:"NAYA-KERNEL-KNOW",
    request:{owner_id:OWNER,naya_id:NAYA,task_id:"TASK-1",task_class:"RELATED_HELDOUT",required_capability:"provenance_preservation"},
    result:{
      schema:"naya.know.context-result.v1",status:"HIT",task_id:"TASK-1",required_capability:"provenance_preservation",
      selected_block_id:"IB-NAYA-NODE-0001-0001",selected_epistemic_state:"LEARNED",
      selected_provenance:{source_event_id:"event-1",method:"canonical"},
      selected_evidence_refs:[{id:"ev-1",source:"execution_receipt"}],
      applicable:true,reason:"OWNER_SCOPED_CURRENT_BLOCK_MATCHES_REQUIRED_CAPABILITY",
      retrieval_creates_authority:false,handoff_to:"NAYA-KERNEL-PROVE"
    },
    authority_refs:["grant-1"],retrieval_creates_authority:false,handoff_to:"NAYA-KERNEL-PROVE"
  },
  ...overrides
});

test("PROVE derives a bounded SUPPORTED claim without creating authority",()=>{
  const a=assessKnowProof(OWNER,NAYA,knowReceipt(),block(),grant(),[],NOW);
  assert.equal(a.state,"ASSESSED");
  assert.equal(a.epistemic_state,"SUPPORTED");
  assert.equal(a.claim_strength,"MODERATE");
  assert.equal(a.evidence_strength,"STRONG");
  assert.equal(a.selected_block_id,"IB-NAYA-NODE-0001-0001");
  assert.equal(a.proof_creates_authority,false);
  assert.equal(a.handoff_to,"NAYA-KERNEL-CONNECT");
  assert.match(a.claim,/TASK-1/);
  assert.match(a.claim,/provenance_preservation/);
});

test("PROVE refuses to promote a KNOW miss",()=>{
  const r=knowReceipt();
  r.evidence.result={...r.evidence.result,status:"MISS",selected_block_id:null,selected_epistemic_state:null,
    selected_provenance:null,selected_evidence_refs:[],applicable:false,reason:"NO_ELIGIBLE_APPLICABLE_INTELLIGENCE"};
  const a=assessKnowProof(OWNER,NAYA,r,null,grant(),[],NOW);
  assert.equal(a.state,"FAILED");
  assert.equal(a.epistemic_state,"UNVERIFIED");
  assert.equal(a.failure_reason,"KNOW_HIT_REQUIRED");
  assert.equal(a.handoff_to,null);
});

test("PROVE fails closed if current authority is revoked or expired",()=>{
  assert.equal(assessKnowProof(OWNER,NAYA,knowReceipt(),block(),grant({status:"REVOKED",revoked_at:"2026-09-29T20:29:30Z"}),[],NOW).failure_reason,"LIVE_AUTHORITY_NOT_ACTIVE");
  assert.equal(assessKnowProof(OWNER,NAYA,knowReceipt(),block(),grant({expires_at:"2026-09-29T20:29:59Z"}),[],NOW).failure_reason,"LIVE_AUTHORITY_EXPIRED");
});

test("PROVE rejects stale or future KNOW evidence",()=>{
  assert.equal(assessKnowProof(OWNER,NAYA,knowReceipt({created_at:"2026-09-29T20:00:00Z"}),block(),grant(),[],NOW).failure_reason,"KNOW_RECEIPT_STALE");
  assert.equal(assessKnowProof(OWNER,NAYA,knowReceipt({created_at:"2026-09-29T20:31:00Z"}),block(),grant(),[],NOW).failure_reason,"KNOW_RECEIPT_TIME_INVALID");
});

test("PROVE independently recomputes canonical applicability instead of trusting KNOW",()=>{
  const a=assessKnowProof(OWNER,NAYA,knowReceipt(),block({applicable_scope:{target:NAYA},content:{lesson:"Arithmetic only"}}),grant(),[],NOW);
  assert.equal(a.failure_reason,"CANONICAL_BLOCK_CAPABILITY_MISMATCH");
  assert.equal(a.handoff_to,null);
});

test("PROVE refuses missing or mismatched canonical evidence",()=>{
  assert.equal(assessKnowProof(OWNER,NAYA,knowReceipt(),block({provenance:{}}),grant(),[],NOW).failure_reason,"PROVENANCE_REQUIRED");
  assert.equal(assessKnowProof(OWNER,NAYA,knowReceipt(),block({evidence_refs:[]}),grant(),[],NOW).failure_reason,"EVIDENCE_REQUIRED");
  assert.equal(assessKnowProof(OWNER,NAYA,knowReceipt(),block({provenance:{source_event_id:"other"}}),grant(),[],NOW).failure_reason,"PROVENANCE_MISMATCH");
});

test("PROVE surfaces verified contradictions rather than resolving them by fiat",()=>{
  const rel=[{relationship_id:"rel-1",source_id:"OTHER",target_id:"IB-NAYA-NODE-0001-0001",
    relationship_type:"CONTRADICTS",epistemic_state:"VERIFIED",provenance:{receipt_id:"contradiction-proof"}}];
  const a=assessKnowProof(OWNER,NAYA,knowReceipt(),block(),grant(),rel,NOW);
  assert.equal(a.state,"CONFLICTED");
  assert.equal(a.epistemic_state,"CONTRADICTED");
  assert.equal(a.failure_reason,"VERIFIED_CONTRADICTION_PRESENT");
  assert.equal(a.handoff_to,null);
  assert.equal(a.conflicts.length,1);
});

test("PROVE preserves supported unresolved conflict as UNVERIFIED",()=>{
  const rel=[{relationship_id:"rel-2",source_id:"IB-NAYA-NODE-0001-0001",target_id:"OTHER",
    relationship_type:"INVALIDATES",epistemic_state:"SUPPORTED",provenance:{source:"review"}}];
  const a=assessKnowProof(OWNER,NAYA,knowReceipt(),block(),grant(),rel,NOW);
  assert.equal(a.state,"CONFLICTED");
  assert.equal(a.epistemic_state,"UNVERIFIED");
  assert.equal(a.failure_reason,"UNRESOLVED_CONFLICT_PRESENT");
});

test("runtime forbids caller-supplied claim, evidence, block identity, and answer content",()=>{
  const source=readFileSync(new URL("../supabase/functions/nayanet-prove-runtime/index.ts",import.meta.url),"utf8");
  for(const key of ["claim","evidence","provenance","block_id","intelligent_block_id","answer","lesson","intelligence","intelligence_content"])
    assert.match(source,new RegExp('"'+key+'"'));
  assert.match(source,/CALLER_SUPPLIED_PROOF_CONTENT_FORBIDDEN/);
  assert.match(source,/executor_claim_trusted_as_verification:false/);
  assert.match(source,/proof_creates_authority:false/);
});

test("runtime persists PROVE assessments in existing execution receipt ledger and hands only supported claims to CONNECT",()=>{
  const source=readFileSync(new URL("../supabase/functions/nayanet-prove-runtime/index.ts",import.meta.url),"utf8");
  assert.match(source,/action:"prove_claim_assessment"/);
  assert.match(source,/nayanet_execution_receipts/);
  assert.match(source,/NAYA-KERNEL-CONNECT/);
  assert.doesNotMatch(source,/nayanet_proof_receipts/);
});


test("PROVE independent verifier compares persisted JSONB semantically, not object key order",()=>{
  const source=readFileSync(new URL("../supabase/functions/nayanet-prove-runtime/index.ts",import.meta.url),"utf8");
  assert.match(source,/stableJson\(recorded\.evidence\?\?\[\]\)===stableJson\(recomputed\.evidence\?\?\[\]\)/);
  assert.match(source,/stableJson\(recorded\.provenance_chain\?\?\[\]\)===stableJson\(recomputed\.provenance_chain\?\?\[\]\)/);
  assert.match(source,/stableJson\(recorded\.conflicts\?\?\[\]\)===stableJson\(recomputed\.conflicts\?\?\[\]\)/);
  assert.doesNotMatch(source,/JSON\.stringify\(recorded\.evidence/);
  assert.doesNotMatch(source,/JSON\.stringify\(recorded\.provenance_chain/);
  assert.doesNotMatch(source,/JSON\.stringify\(recorded\.conflicts/);
});
