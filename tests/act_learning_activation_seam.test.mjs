import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { stripTypeScriptTypes } from "node:module";
import vm from "node:vm";
import {
  buildActPlan,
  canonicalEqual,
  validateAct,
  ACT_RETRIEVAL_SELECTOR,
  ACT_BASELINE_BEHAVIOR,
  ACT_PROVENANCE_BEHAVIOR,
} from "../supabase/functions/nayanet-act-runtime/act.ts";
import { selectKnowContext } from "../supabase/functions/nayanet-know-runtime/know.ts";

const OWNER="adfdf0b8-5558-41d1-9fed-ec51abf4fe2f";
const NAYA="NAYA-NODE-0001";
const ACTION="naya_node_apply";
const DOOR_ID="DOOR-AI";
const OPERATION="apply_retained_intelligence";
const TASK={
  owner_id:OWNER,
  naya_id:NAYA,
  task_id:"TASK-P0-LEARNING-ACTIVATION-001",
  task_class:"governed_action_planning",
  required_capability:"provenance_preservation",
};
const BLOCK_ID="IB-NAYA-P0-LEARNING-001";
const NOW=new Date();
const EVALUATED_AT=new Date(NOW.getTime()-60_000).toISOString();

const law=()=>({
  id:"law-1",
  user_id:OWNER,
  project_id:"NayaNET",
  action:"law_authority_decision",
  status:"SUCCESS",
  evidence:{
    node_id:"NAYA-KERNEL-LAW",
    law_request:{action:ACTION,target:NAYA},
    law_decision:{
      status:"AUTHORIZED",owner_id:OWNER,naya_id:NAYA,action:ACTION,target:NAYA,
      authority_refs:["grant-1"],evaluated_at:EVALUATED_AT,expires_at:null,
    },
  },
});
const grant=(overrides={})=>({
  grant_id:"grant-1",issuer_id:OWNER,subject_id:OWNER,scope:{target:NAYA},
  actions:[ACTION],status:"ACTIVE",revoked_at:null,expires_at:null,...overrides,
});
const door=()=>({
  door_id:DOOR_ID,operation:OPERATION,authority_action:ACTION,target:NAYA,
  consequential:true,max_law_age_seconds:900,
});
const actRequest=()=>({
  owner_id:OWNER,naya_id:NAYA,law_receipt_id:"law-1",action:ACTION,target:NAYA,
  door_id:DOOR_ID,operation:OPERATION,
});

const learnedBlock=(overrides={})=>({
  intelligent_block_id:BLOCK_ID,
  owner_id:OWNER,
  status:"ACTIVE",
  understanding_state:"LEARNED",
  owner_scope:"PRIVATE",
  applicable_scope:{target:NAYA,capabilities:["provenance_preservation"]},
  value_context:{},
  content:{
    lesson:"Preserve provenance before applying retained intelligence.",
    capabilities:["provenance_preservation"],
  },
  provenance:{source_event_id:"event-p0-1",method:"canonical-test"},
  evidence_refs:[{type:"receipt",id:"evidence-p0-1"}],
  superseded_by_block_id:null,
  updated_at:new Date(NOW.getTime()-10_000).toISOString(),
  connections:[],
  ...overrides,
});

function knowReceipt(id,result){
  return {
    id,user_id:OWNER,project_id:"NayaNET",action:"know_context_retrieval",status:"SUCCESS",
    evidence:{
      schema:"naya.know.receipt.v1",
      node_id:"NAYA-KERNEL-KNOW",
      request:{...TASK},
      result,
      law_receipt_id:"law-1",
      authority_refs:["grant-1"],
      caller_selected_block:false,
      retrieval_creates_authority:false,
      candidate_count:result.status==="HIT"?1:0,
      selection_now:NOW.toISOString(),
      handoff_to:"NAYA-KERNEL-PROVE",
    },
  };
}

function controlAndTreatment(){
  const block=learnedBlock();
  const controlResult=selectKnowContext(TASK,[],NOW);
  const treatmentResult=selectKnowContext(TASK,[block],NOW);
  return {
    block,
    controlUniverse:[],
    treatmentUniverse:[block],
    control:knowReceipt("know-control",controlResult),
    treatment:knowReceipt("know-treatment",treatmentResult),
  };
}

test("CONTROL/TREATMENT: normal KNOW+CONNECT retrieval changes ACT plan under identical task and authority",()=>{
  const {block,control,treatment,controlUniverse,treatmentUniverse}=controlAndTreatment();
  const req=actRequest();
  const c=buildActPlan(req,law(),grant(),door(),control,null,controlUniverse,NOW);
  const t=buildActPlan(req,law(),grant(),door(),treatment,block,treatmentUniverse,NOW);

  assert.equal(control.evidence.result.status,"MISS");
  assert.equal(treatment.evidence.result.status,"HIT");
  assert.deepEqual(c.task_identity,t.task_identity);
  assert.deepEqual(c.guard,t.guard);
  assert.deepEqual(c.pre_learning_plan,t.pre_learning_plan);
  assert.equal(c.post_retrieval_plan.behavior,ACT_BASELINE_BEHAVIOR);
  assert.equal(t.post_retrieval_plan.behavior,ACT_PROVENANCE_BEHAVIOR);
  assert.equal(c.intelligence_applied_to_plan,false);
  assert.equal(t.intelligence_applied_to_plan,true);
  assert.equal(t.selected_intelligence.intelligent_block_id,BLOCK_ID);
  assert.equal(t.selected_intelligence.truth_state,"LEARNED");
  assert.equal(t.selected_intelligence.lifecycle_state,"ACTIVE");
  assert.equal(t.selector.version,"naya.know.context-result.v1/connect-selector-v2");
  assert.equal(t.law_reresolution_required,false);

  const taskWire=JSON.stringify(TASK);
  assert.equal(taskWire.includes("Preserve provenance"),false,"lesson content must not be hand-fed in task");
  assert.equal(taskWire.includes(BLOCK_ID),false,"selected block id must not be hand-fed in task");
});

test("falsifier: removing the activation seam makes the treatment delta disappear",()=>{
  const {block,control,treatment,controlUniverse,treatmentUniverse}=controlAndTreatment();
  const withSeam=buildActPlan(actRequest(),law(),grant(),door(),treatment,block,treatmentUniverse,NOW);
  const seamRemoved=buildActPlan(actRequest(),law(),grant(),door(),control,null,controlUniverse,NOW);
  assert.equal(withSeam.post_retrieval_plan.behavior,ACT_PROVENANCE_BEHAVIOR);
  assert.equal(seamRemoved.post_retrieval_plan.behavior,ACT_BASELINE_BEHAVIOR);
  assert.notEqual(withSeam.post_retrieval_plan.behavior,seamRemoved.post_retrieval_plan.behavior);
});

test("unrelated, superseded, contradicted, and inapplicable intelligence do not steer",()=>{
  const variants=[
    learnedBlock({
      applicable_scope:{target:NAYA,capabilities:["unrelated_capability"]},
      content:{lesson:"Unrelated retained lesson.",capabilities:["unrelated_capability"]},
    }),
    learnedBlock({superseded_by_block_id:"IB-NEWER"}),
    learnedBlock({understanding_state:"CONTRADICTED"}),
    learnedBlock({applicable_scope:{target:"OTHER",capabilities:["provenance_preservation"]}}),
    learnedBlock({status:"ARCHIVED"}),
    learnedBlock({status:"STALE"}),
  ];
  for(const block of variants){
    const result=selectKnowContext(TASK,[block],NOW);
    assert.equal(result.status,"MISS");
    const plan=buildActPlan(actRequest(),law(),grant(),door(),knowReceipt("know-negative",result),null,[block],NOW);
    assert.equal(plan.status,"READY");
    assert.equal(plan.post_retrieval_plan.behavior,ACT_BASELINE_BEHAVIOR);
    assert.equal(plan.intelligence_applied_to_plan,false);
  }
});

test("CONNECT conflict is visible but non-steering",()=>{
  const block=learnedBlock({
    connections:[{target_block_id:"IB-CONFLICT",relationship_type:"CONTRADICTS"}],
  });
  const conflictBlock=learnedBlock({
    intelligent_block_id:"IB-CONFLICT",
    updated_at:new Date(NOW.getTime()-20_000).toISOString(),
    provenance:{source_event_id:"event-conflict",method:"canonical-test"},
    evidence_refs:[{type:"receipt",id:"evidence-conflict"}],
  });
  const universe=[block,conflictBlock];
  const result=selectKnowContext(TASK,universe,NOW);
  assert.equal(result.conflict_detected,true);
  const plan=buildActPlan(actRequest(),law(),grant(),door(),knowReceipt("know-conflict",result),block,universe,NOW);
  assert.equal(plan.status,"READY");
  assert.equal(plan.reason,"CONFLICTED_INTELLIGENCE_NON_STEERING");
  assert.equal(plan.post_retrieval_plan.behavior,ACT_BASELINE_BEHAVIOR);
  assert.equal(plan.intelligence_applied_to_plan,false);
});

test("missing or revoked authority blocks before learning can steer",()=>{
  const {block,treatment,treatmentUniverse}=controlAndTreatment();
  const missing=buildActPlan(actRequest(),null,null,door(),treatment,block,treatmentUniverse,NOW);
  assert.equal(missing.status,"BLOCKED");
  assert.equal(missing.reason,"LAW_RECEIPT_REQUIRED");

  const revoked=buildActPlan(actRequest(),law(),grant({status:"REVOKED",revoked_at:NOW.toISOString()}),door(),treatment,block,treatmentUniverse,NOW);
  assert.equal(revoked.status,"BLOCKED");
  assert.equal(revoked.reason,"LIVE_AUTHORITY_NOT_ACTIVE");

  const expired=buildActPlan(
    actRequest(),law(),grant({expires_at:new Date(NOW.getTime()-1_000).toISOString()}),door(),treatment,block,treatmentUniverse,NOW
  );
  assert.equal(expired.status,"BLOCKED");
  assert.equal(expired.reason,"LIVE_AUTHORITY_EXPIRED");
});

test("scope-changing learning cannot use the old LAW receipt",()=>{
  const block=learnedBlock({
    content:{
      lesson:"Preserve provenance before applying retained intelligence.",
      capabilities:["provenance_preservation"],
      act_plan_patch:{target:"OTHER-TARGET"},
    },
  });
  const result=selectKnowContext(TASK,[block],NOW);
  const plan=buildActPlan(actRequest(),law(),grant(),door(),knowReceipt("know-scope-change",result),block,[block],NOW);
  assert.equal(plan.status,"LAW_RERESOLUTION_REQUIRED");
  assert.equal(plan.authority_scope_changed,true);
  assert.equal(plan.law_reresolution_required,true);
  assert.equal(plan.intelligence_applied_to_plan,false);
  assert.equal(plan.effect_executed,false);
  assert.equal(plan.post_retrieval_plan.target,"OTHER-TARGET");
});

test("forged retrieval provenance fails closed",()=>{
  const {block,treatment,treatmentUniverse}=controlAndTreatment();
  const forged=structuredClone(treatment);
  forged.evidence.result.selected_provenance={source_event_id:"forged"};
  const plan=buildActPlan(actRequest(),law(),grant(),door(),forged,block,treatmentUniverse,NOW);
  assert.equal(plan.status,"BLOCKED");
  assert.equal(plan.reason,"KNOW_SELECTION_REPLAY_MISMATCH");
  assert.equal(plan.intelligence_applied_to_plan,false);
});

const source=readFileSync(new URL("../supabase/functions/nayanet-act-runtime/index.ts",import.meta.url),"utf8");
const code=stripTypeScriptTypes(source.replace(/^import .*;\r?\n/gm,""));
const claims={
  repository:"SoulSchoolAcademy/NayaPOWER",
  ref:"refs/heads/main",
  workflow_ref:"SoulSchoolAcademy/NayaPOWER/.github/workflows/live-act-proof.yml@refs/heads/main",
  jti:"p0-learning-activation-test",
};

function handlerRuntime({useTreatment=true,blockOverride=null}={}){
  let handler;
  let receiptSeq=100;
  const {block,control,treatment}=controlAndTreatment();
  const chosenBlock=blockOverride??block;
  const chosenKnow=useTreatment
    ? knowReceipt("know-treatment",selectKnowContext(TASK,[chosenBlock],NOW))
    : control;
  const rows={
    nayanet_execution_receipts:[law(),chosenKnow],
    nayanet_authority_grants:[grant()],
    nayanet_intelligent_blocks:useTreatment?[chosenBlock]:[],
  };

  const executeQuery=(query)=>{
    const table=rows[query.table];
    if(!table) throw new Error("UNKNOWN_TABLE_"+query.table);
    if(query.op==="insert"){
      const row={...query.insertRow,id:"receipt-"+receiptSeq++};
      table.push(row);
      return {data:{...row},error:null};
    }
    let matches=table.filter(row=>query.filters.every(([k,v])=>row[k]===v));
    if(query.orderBy){
      const {column,ascending}=query.orderBy;
      matches.sort((a,b)=>(ascending?1:-1)*(Number(a[column]??0)-Number(b[column]??0)));
    }
    if(query.limitCount!=null) matches=matches.slice(0,query.limitCount);
    if(query.singleRequired){
      return matches.length===1?{data:{...matches[0]},error:null}:{data:null,error:{code:"PGRST116"}};
    }
    return {data:matches,error:null};
  };

  class Query{
    constructor(table){this.table=table;this.op="select";this.filters=[];this.orderBy=null;this.limitCount=null;this.insertRow=null;this.singleRequired=false;}
    select(){return this;}
    eq(k,v){this.filters.push([k,v]);return this;}
    order(column,options={}){this.orderBy={column,ascending:options.ascending!==false};return this;}
    limit(n){this.limitCount=n;return this;}
    maybeSingle(){const r=executeQuery(this);return Promise.resolve({data:r.data?.[0]??r.data??null,error:r.error});}
    single(){this.singleRequired=true;const r=executeQuery(this);return Promise.resolve(r);}
    insert(row){this.op="insert";this.insertRow=row;return this;}
    then(resolve,reject){return Promise.resolve(executeQuery(this)).then(resolve,reject);}
  }
  const client={from:(table)=>new Query(table)};
  vm.runInNewContext(code,{
    URL,Request,Response,Date,TextEncoder,Uint8Array,console,crypto,
    validateAct,buildActPlan,canonicalEqual,ACT_RETRIEVAL_SELECTOR,
    Deno:{
      env:{get:key=>({SUPABASE_URL:"https://offline.invalid",SUPABASE_SERVICE_ROLE_KEY:"offline-key"})[key]},
      serve:cb=>{handler=cb;},
    },
    createRemoteJWKSet:()=>({}),
    jwtVerify:async()=>({payload:claims}),
    createClient:()=>client,
  });
  const post=async(body)=>{
    const response=await handler(new Request("https://offline.invalid",{
      method:"POST",
      headers:{authorization:"Bearer offline","content-type":"application/json"},
      body:JSON.stringify(body),
    }));
    return {status:response.status,body:await response.json()};
  };
  return {rows,post};
}

const planBody=(retrieval_receipt_id)=>({
  mode:"plan",
  law_receipt_id:"law-1",
  retrieval_receipt_id,
  action:ACTION,
  target:NAYA,
  door_id:DOOR_ID,
  operation:OPERATION,
});

test("handler persists ACT.PLAN then executes exact plan; executor does not self-certify VERIFY",async()=>{
  const rt=handlerRuntime({useTreatment:true});
  const planned=await rt.post(planBody("know-treatment"));
  assert.equal(planned.status,200);
  assert.equal(planned.body.status,"PLANNED");
  assert.equal(planned.body.plan.post_retrieval_plan.behavior,ACT_PROVENANCE_BEHAVIOR);
  assert.equal(planned.body.plan_receipt.action,"act_node_plan");
  assert.equal(planned.body.plan_receipt.evidence.selector.version,"naya.know.context-result.v1/connect-selector-v2");

  const executed=await rt.post({mode:"execute",plan_receipt_id:planned.body.plan_receipt.id});
  assert.equal(executed.status,200);
  assert.equal(executed.body.status,"EXECUTED");
  assert.equal(executed.body.planning_mode,"TWO_PHASE_KNOW_CONNECT_BOUND");
  assert.equal(executed.body.observation.behavior,ACT_PROVENANCE_BEHAVIOR);
  assert.equal(executed.body.receipt.evidence.retrieval_receipt_id,"know-treatment");
  assert.equal(executed.body.receipt.evidence.independent_verification,false);
  assert.equal(executed.body.receipt.evidence.verification_status,"PENDING_INDEPENDENT_RUNTIME_VERIFICATION");
  assert.equal(executed.body.receipt.evidence.handoff_to,"NAYA-KERNEL-VERIFY");
});

test("cold successor reconstructs selected lesson and plan from plan receipt id only",async()=>{
  const rt=handlerRuntime({useTreatment:true});
  const planned=await rt.post(planBody("know-treatment"));
  const reconstructed=await rt.post({mode:"inspect-plan",plan_receipt_id:planned.body.plan_receipt.id});
  assert.equal(reconstructed.status,200);
  assert.equal(reconstructed.body.status,"CANONICAL_PLAN_REREAD");
  assert.equal(reconstructed.body.cold_reconstruction,true);
  assert.equal(reconstructed.body.selected_block.intelligent_block_id,BLOCK_ID);
  assert.equal(reconstructed.body.selected_block.content.lesson,"Preserve provenance before applying retained intelligence.");
  assert.equal(reconstructed.body.recomputed_plan.post_retrieval_plan.behavior,ACT_PROVENANCE_BEHAVIOR);
  assert.equal(reconstructed.body.executor_claim_trusted_as_verification,false);
});

test("handler refuses scope-changing treatment under old LAW receipt and never executes it",async()=>{
  const scopeBlock=learnedBlock({
    content:{
      lesson:"Preserve provenance before applying retained intelligence.",
      capabilities:["provenance_preservation"],
      act_plan_patch:{target:"OTHER-TARGET"},
    },
  });
  const rt=handlerRuntime({useTreatment:true,blockOverride:scopeBlock});
  const planned=await rt.post(planBody("know-treatment"));
  assert.equal(planned.status,409);
  assert.equal(planned.body.status,"LAW_RERESOLUTION_REQUIRED");
  assert.equal(planned.body.action_executed,false);
  assert.equal(planned.body.plan_receipt.status,"BLOCKED");
  assert.equal(rt.rows.nayanet_execution_receipts.some(r=>r.action==="act_node_execute"),false);
});

test("handler CONTROL executes baseline using same action and authority with no selected learning",async()=>{
  const rt=handlerRuntime({useTreatment:false});
  const planned=await rt.post(planBody("know-control"));
  assert.equal(planned.status,200);
  assert.equal(planned.body.plan.post_retrieval_plan.behavior,ACT_BASELINE_BEHAVIOR);
  assert.equal(planned.body.plan.selected_intelligence,null);
  const executed=await rt.post({mode:"execute",plan_receipt_id:planned.body.plan_receipt.id});
  assert.equal(executed.status,200);
  assert.equal(executed.body.observation.behavior,ACT_BASELINE_BEHAVIOR);
  assert.equal(executed.body.observation.selected_intelligence_id,null);
});


test("selected-block reread guards all fire fail-closed against forged or changed canonical state",()=>{
  const {block,treatment,treatmentUniverse}=controlAndTreatment();
  const cases=[
    ["SELECTED_INTELLIGENCE_NOT_FOUND", null],
    ["SELECTED_INTELLIGENCE_ID_MISMATCH", {...block,intelligent_block_id:"IB-FORGED"}],
    ["SELECTED_INTELLIGENCE_OWNER_MISMATCH", {...block,owner_id:"other-owner"}],
    ["SELECTED_INTELLIGENCE_LIFECYCLE_NOT_SERVABLE", {...block,status:"ARCHIVED"}],
    ["SELECTED_INTELLIGENCE_TRUTH_NOT_SERVABLE", {...block,understanding_state:"CANDIDATE"}],
    ["SELECTED_INTELLIGENCE_SUPERSEDED", {...block,superseded_by_block_id:"IB-NEWER"}],
    ["SELECTED_INTELLIGENCE_TRUTH_MISMATCH", {...block,understanding_state:"VERIFIED"}],
    ["SELECTED_INTELLIGENCE_PROVENANCE_MISSING", {...block,provenance:{}}],
    ["SELECTED_INTELLIGENCE_EVIDENCE_MISSING", {...block,evidence_refs:[]}],
    ["SELECTED_INTELLIGENCE_EVIDENCE_MISMATCH", {...block,evidence_refs:[{type:"receipt",id:"other-evidence"}]}],
    ["SELECTED_INTELLIGENCE_APPLICABILITY_MISMATCH", {...block,applicable_scope:{target:"OTHER",capabilities:["provenance_preservation"]}}],
  ];
  for(const [reason,changedBlock] of cases){
    const plan=buildActPlan(actRequest(),law(),grant(),door(),treatment,changedBlock,treatmentUniverse,NOW);
    assert.equal(plan.status,"BLOCKED",reason);
    assert.equal(plan.reason,reason,reason);
    assert.equal(plan.effect_executed,false,reason);
  }
});

test("handler exposes OLD_LAW_RECEIPT_CANNOT_AUTHORIZE_CHANGED_SCOPE on scope-changing plan",async()=>{
  const scopeBlock=learnedBlock({
    content:{
      lesson:"Preserve provenance before applying retained intelligence.",
      capabilities:["provenance_preservation"],
      act_plan_patch:{target:"OTHER-TARGET"},
    },
  });
  const rt=handlerRuntime({useTreatment:true,blockOverride:scopeBlock});
  const planned=await rt.post(planBody("know-treatment"));
  assert.equal(planned.status,409);
  assert.equal(planned.body.reason,"OLD_LAW_RECEIPT_CANNOT_AUTHORIZE_CHANGED_SCOPE");
});

test("PLAN_RECEIPT_INVALID fires before execution for missing/invalid plan receipt",async()=>{
  const rt=handlerRuntime({useTreatment:true});
  const result=await rt.post({mode:"execute",plan_receipt_id:"missing-plan"});
  assert.equal(result.status,409);
  assert.equal(result.body.error,"PLAN_RECEIPT_INVALID");
  assert.equal(rt.rows.nayanet_execution_receipts.some(r=>r.action==="act_node_execute"),false);
});

test("PLAN_RECEIPT_NOT_FOUND fires on cold reconstruction of an unknown plan id",async()=>{
  const rt=handlerRuntime({useTreatment:true});
  const result=await rt.post({mode:"inspect-plan",plan_receipt_id:"missing-plan"});
  assert.equal(result.status,404);
  assert.equal(result.body.error,"PLAN_RECEIPT_NOT_FOUND");
});

test("PLAN_STATE_CHANGED_OR_FORGED fires when canonical selected intelligence changes after planning",async()=>{
  const rt=handlerRuntime({useTreatment:true});
  const planned=await rt.post(planBody("know-treatment"));
  assert.equal(planned.status,200);
  rt.rows.nayanet_intelligent_blocks[0].content={
    lesson:"Changed after planning.",
    capabilities:["provenance_preservation"],
  };
  const executed=await rt.post({mode:"execute",plan_receipt_id:planned.body.plan_receipt.id});
  assert.equal(executed.status,409);
  assert.equal(executed.body.error,"PLAN_STATE_CHANGED_OR_FORGED");
  assert.equal(rt.rows.nayanet_execution_receipts.some(r=>r.action==="act_node_execute"),false);
});


test("retained intelligence cannot smuggle arbitrary behavior through act_plan_patch",()=>{
  const block=learnedBlock({
    content:{
      lesson:"Preserve provenance before applying retained intelligence.",
      capabilities:["provenance_preservation"],
      act_plan_patch:{behavior:"UNAUTHORIZED_ARBITRARY_BEHAVIOR"},
    },
  });
  const result=selectKnowContext(TASK,[block],NOW);
  const plan=buildActPlan(actRequest(),law(),grant(),door(),knowReceipt("know-behavior-injection",result),block,[block],NOW);
  assert.equal(plan.status,"READY");
  assert.equal(plan.post_retrieval_plan.behavior,ACT_PROVENANCE_BEHAVIOR);
  assert.notEqual(plan.post_retrieval_plan.behavior,"UNAUTHORIZED_ARBITRARY_BEHAVIOR");
});


test("coherently forged KNOW selected ID fails canonical selector replay",()=>{
  const newest=learnedBlock({
    intelligent_block_id:"IB-NEWEST",
    updated_at:new Date(NOW.getTime()-1_000).toISOString(),
    provenance:{source_event_id:"event-newest",method:"canonical-test"},
    evidence_refs:[{type:"receipt",id:"evidence-newest"}],
  });
  const older=learnedBlock({
    intelligent_block_id:"IB-OLDER",
    updated_at:new Date(NOW.getTime()-60_000).toISOString(),
    provenance:{source_event_id:"event-older",method:"canonical-test"},
    evidence_refs:[{type:"receipt",id:"evidence-older"}],
  });
  const universe=[older,newest];
  const canonical=selectKnowContext(TASK,universe,NOW);
  assert.equal(canonical.selected_block_id,"IB-NEWEST");

  const forged=knowReceipt("know-forged-coherent",{
    ...canonical,
    selected_block_id:"IB-OLDER",
    selected_epistemic_state:older.understanding_state,
    selected_provenance:older.provenance,
    selected_evidence_refs:older.evidence_refs,
  });
  const plan=buildActPlan(actRequest(),law(),grant(),door(),forged,older,universe,NOW);
  assert.equal(plan.status,"BLOCKED");
  assert.equal(plan.reason,"KNOW_SELECTION_REPLAY_MISMATCH");
  assert.equal(plan.intelligence_applied_to_plan,false);
});

test("missing selector replay universe or pinned selection time fails closed",()=>{
  const {block,treatment,treatmentUniverse}=controlAndTreatment();
  const noUniverse=buildActPlan(actRequest(),law(),grant(),door(),treatment,block,null,NOW);
  assert.equal(noUniverse.status,"BLOCKED");
  assert.equal(noUniverse.reason,"KNOW_SELECTION_UNIVERSE_REQUIRED");

  const noTime=structuredClone(treatment);
  delete noTime.evidence.selection_now;
  const missingTime=buildActPlan(actRequest(),law(),grant(),door(),noTime,block,treatmentUniverse,NOW);
  assert.equal(missingTime.status,"BLOCKED");
  assert.equal(missingTime.reason,"KNOW_SELECTION_TIME_INVALID");
});
