import test from "node:test";
import assert from "node:assert/strict";
import { selectKnow } from "../supabase/functions/nayanet-know-runtime/know.ts";

const OWNER="adfdf0b8-5558-41d1-9fed-ec51abf4fe2f";
const NAYA="NAYA-NODE-0001";

const req=(task_context,overrides={})=>({
  owner_id:OWNER,
  naya_id:NAYA,
  target:NAYA,
  task_context,
  ...overrides
});

const learned=(overrides={})=>({
  block_id:"b1",
  intelligent_block_id:"IB-PROVENANCE-LESSON",
  owner_id:OWNER,
  subject_id:NAYA,
  title:"Preserve provenance before use",
  status:"DURABLE",
  understanding_state:"LEARNED",
  owner_scope:"PRIVATE",
  evidence_refs:[{receipt_id:"r1"}],
  provenance:{source:"verified-learning",source_event_id:"e1"},
  applicable_scope:{target:NAYA,capability:"provenance_preservation"},
  content:{
    lesson:"Preserve provenance before applying retained intelligence.",
    topic:"provenance preservation",
    category:"governed intelligence"
  },
  superseded_by_block_id:null,
  ...overrides
});

test("KNOW selects applicable retained intelligence from task context without caller block id",()=>{
  const d=selectKnow(req("Preserve exact provenance and source lineage before using a learned record."),[learned()]);
  assert.equal(d.status,"SELECTED");
  assert.equal(d.selected.intelligent_block_id,"IB-PROVENANCE-LESSON");
  assert.ok(d.score>=2);
});

test("KNOW returns bounded miss for unrelated context",()=>{
  const d=selectKnow(req("Compute arithmetic total seven plus five."),[learned()]);
  assert.equal(d.status,"MISS");
  assert.equal(d.reason,"NO_APPLICABLE_CANONICAL_INTELLIGENCE");
});

test("caller cannot force a block or supply the answer",()=>{
  for(const injected of [
    {intelligent_block_id:"IB-PROVENANCE-LESSON"},
    {block_id:"b1"},
    {lesson:"Preserve provenance"},
    {answer:"PRESERVE_PROVENANCE_BEFORE_APPLY"},
    {intelligence:{id:"IB-PROVENANCE-LESSON"}},
    {intelligence_content:"Preserve provenance"}
  ]){
    const d=selectKnow(req("Preserve provenance source lineage.",injected),[learned()]);
    assert.equal(d.status,"BLOCKED");
    assert.equal(d.reason,"CALLER_SUPPLIED_INTELLIGENCE_FORBIDDEN");
  }
});

test("cross-owner private intelligence cannot enter selection",()=>{
  const d=selectKnow(req("Preserve provenance and source lineage."),[learned({owner_id:"00000000-0000-0000-0000-000000000000"})]);
  assert.equal(d.status,"MISS");
});

test("superseded or unverified intelligence is excluded",()=>{
  assert.equal(selectKnow(req("Preserve provenance source lineage."),[learned({superseded_by_block_id:"b2"})]).status,"MISS");
  assert.equal(selectKnow(req("Preserve provenance source lineage."),[learned({understanding_state:"CANDIDATE"})]).status,"MISS");
  assert.equal(selectKnow(req("Preserve provenance source lineage."),[learned({evidence_refs:[]})]).status,"MISS");
  assert.equal(selectKnow(req("Preserve provenance source lineage."),[learned({provenance:{}})]).status,"MISS");
});

test("scope mismatch excludes otherwise relevant intelligence",()=>{
  const d=selectKnow(req("Preserve provenance source lineage."),[learned({applicable_scope:{target:"OTHER-NAYA"}})]);
  assert.equal(d.status,"MISS");
});

test("ambiguous equal contextual matches fail closed",()=>{
  const a=learned({intelligent_block_id:"IB-A"});
  const b=learned({block_id:"b2",intelligent_block_id:"IB-B"});
  const d=selectKnow(req("Preserve provenance and source lineage."),[a,b]);
  assert.equal(d.status,"BLOCKED");
  assert.equal(d.reason,"AMBIGUOUS_CONTEXTUAL_INTELLIGENCE");
});

test("missing context fails closed",()=>{
  const d=selectKnow(req(""),[learned()]);
  assert.equal(d.status,"BLOCKED");
  assert.equal(d.reason,"KNOW_CONTEXT_REQUIRED");
});
