import { createRemoteJWKSet, jwtVerify } from "https://esm.sh/jose@6.0.10";
import { createClient } from "npm:@supabase/supabase-js@2";
import { validateAct, buildActPlan, canonicalEqual, measureLearningInfluence, ACT_RETRIEVAL_SELECTOR, type ActRequest, type LawReceipt, type Grant, type DoorOperation, type KnowReceipt, type SelectedBlock } from "./act.ts";
import { readDecisionContext, type DecisionContext } from "./decision-context.ts";

const ISSUER="https://token.actions.githubusercontent.com";
const AUDIENCE="nayanet-runtime";
const REPOSITORY="SoulSchoolAcademy/NayaPOWER";
const WORKFLOW=".github/workflows/live-act-proof.yml";
const REF="refs/heads/main";
const OWNER_ID="adfdf0b8-5558-41d1-9fed-ec51abf4fe2f";
const NAYA_ID="NAYA-NODE-0001";
const PROJECT_ID="NayaNET";
const LEGACY_BLOCK_ID="IB-NAYA-NODE-0001-0001";
const JWKS=createRemoteJWKSet(new URL("https://token.actions.githubusercontent.com/.well-known/jwks"));

const DOOR:DoorOperation={
  door_id:"DOOR-AI",
  operation:"apply_retained_intelligence",
  authority_action:"naya_node_apply",
  target:NAYA_ID,
  consequential:true,
  max_law_age_seconds:900
};

const json=(body:unknown,status=200)=>new Response(JSON.stringify(body),{status,headers:{"content-type":"application/json","cache-control":"no-store"}});

async function authenticate(req:Request){
  const h=req.headers.get("authorization")??"";
  if(!h.startsWith("Bearer ")) throw new Error("RUNTIME_IDENTITY_REQUIRED");
  const {payload}=await jwtVerify(h.slice(7),JWKS,{issuer:ISSUER,audience:AUDIENCE});
  const workflowRef=REPOSITORY+"/"+WORKFLOW+"@"+REF;
  if(payload.repository!==REPOSITORY || payload.workflow_ref!==workflowRef || payload.ref!==REF) throw new Error("WORKFLOW_BINDING_MISMATCH");
  return {payload,workflowRef};
}
function adminClient(){
  const url=Deno.env.get("SUPABASE_URL"),key=Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");
  if(!url||!key) throw new Error("SERVER_AUTH_CONFIG_MISSING");
  return createClient(url,key,{auth:{persistSession:false}});
}
async function readReceipt(admin:ReturnType<typeof adminClient>,id:string){
  if(!id) return null;
  const {data,error}=await admin.from("nayanet_execution_receipts").select("*").eq("id",id).eq("user_id",OWNER_ID).eq("project_id",PROJECT_ID).maybeSingle();
  if(error) throw error;
  return data as LawReceipt|KnowReceipt|null;
}
async function readGrant(admin:ReturnType<typeof adminClient>,id:string){
  if(!id) return null;
  const {data,error}=await admin.from("nayanet_authority_grants").select("*").eq("grant_id",id).maybeSingle();
  if(error) throw error;
  return data as Grant|null;
}
async function readBlock(admin:ReturnType<typeof adminClient>,blockId:string){
  if(!blockId) return null;
  const {data,error}=await admin.from("nayanet_intelligent_blocks")
    .select("intelligent_block_id,owner_id,status,understanding_state,owner_scope,applicable_scope,value_context,content,evidence_refs,provenance,superseded_by_block_id,updated_at,connections")
    .eq("intelligent_block_id",blockId).eq("owner_id",OWNER_ID).maybeSingle();
  if(error) throw error;
  return data as SelectedBlock|null;
}
async function readEligibleUniverse(admin:ReturnType<typeof adminClient>){
  const {data,error}=await admin.from("nayanet_intelligent_blocks")
    .select("intelligent_block_id,owner_id,status,understanding_state,owner_scope,applicable_scope,value_context,content,provenance,evidence_refs,superseded_by_block_id,updated_at,connections")
    .eq("owner_id",OWNER_ID);
  if(error) throw error;
  return (data??[]) as SelectedBlock[];
}
async function digestValue(value:unknown){
  const bytes=new TextEncoder().encode(JSON.stringify(value??null));
  const hash=await crypto.subtle.digest("SHA-256",bytes);
  return Array.from(new Uint8Array(hash)).map(b=>b.toString(16).padStart(2,"0")).join("");
}
async function legacyDigest(lesson:string,refs:unknown){
  const bytes=new TextEncoder().encode(lesson+"|"+JSON.stringify(refs??null));
  const hash=await crypto.subtle.digest("SHA-256",bytes);
  return Array.from(new Uint8Array(hash)).map(b=>b.toString(16).padStart(2,"0")).join("");
}
async function insertReceipt(admin:ReturnType<typeof adminClient>,row:Record<string,unknown>){
  for(let attempt=0;attempt<8;attempt++){
    const {data:maxRows,error:maxError}=await admin.from("nayanet_execution_receipts").select("revision").eq("user_id",OWNER_ID).eq("project_id",PROJECT_ID).order("revision",{ascending:false}).limit(1);
    if(maxError) throw maxError;
    const revision=Number(maxRows?.[0]?.revision??0)+1;
    const {data,error}=await admin.from("nayanet_execution_receipts").insert({...row,revision}).select("*").single();
    if(!error) return data;
    if(error.code!=="23505") throw error;
  }
  throw new Error("ACT_RECEIPT_REVISION_CONFLICT");
}

function requestFromBody(body:Record<string,unknown>):ActRequest{
  return {
    owner_id:OWNER_ID,
    naya_id:NAYA_ID,
    law_receipt_id:String(body.law_receipt_id??""),
    action:String(body.action??""),
    target:String(body.target??""),
    door_id:String(body.door_id??""),
    operation:String(body.operation??""),
    retrieved_intelligence_claims_authority:body.retrieved_intelligence_claims_authority===true,
    successor_context_claims_inherited_authority:body.successor_context_claims_inherited_authority===true
  };
}

function doorFor(request:ActRequest){
  return request.door_id===DOOR.door_id && request.operation===DOOR.operation ? DOOR : null;
}

async function authorityFor(admin:ReturnType<typeof adminClient>,request:ActRequest){
  const lawReceipt=await readReceipt(admin,request.law_receipt_id??"") as LawReceipt|null;
  const refs=Array.isArray((lawReceipt as any)?.evidence?.law_decision?.authority_refs)
    ?(lawReceipt as any).evidence.law_decision.authority_refs:[];
  const liveGrant=refs.length===1?await readGrant(admin,String(refs[0])):null;
  const door=doorFor(request);
  const guard=validateAct(request,lawReceipt,liveGrant,door,new Date());
  return {lawReceipt,liveGrant,door,guard};
}

async function persistRefusal(
  admin:ReturnType<typeof adminClient>,
  payload:any,
  workflowRef:string,
  tokenJti:unknown,
  stage:string,
  reason:string,
){
  return insertReceipt(admin,{
    user_id:OWNER_ID,project_id:PROJECT_ID,action:"act_node_refusal",status:"BLOCKED",
    expected_result:"ACT must refuse before execution when authority, retrieval lineage, plan integrity, or observation cannot be established.",
    observed_result:"REFUSED:"+reason,
    evidence:{
      schema:"naya.act.receipt.v1",node_id:"NAYA-KERNEL-ACT",stage,
      ...payload,
      action_executed:false,observed:false,
      independent_verification:false,
      verification_status:"NOT_EXECUTED",
      runtime_identity:"naya-node-oidc",runtime_jti:tokenJti??null,workflow_ref:workflowRef
    },
    learning:[]
  });
}

Deno.serve(async(req)=>{
 try{
  if(req.method!=="POST") return json({ok:false,error:"METHOD_NOT_ALLOWED"},405);
  const {payload,workflowRef}=await authenticate(req);
  const body=await req.json().catch(()=>({})) as Record<string,unknown>;
  const mode=String(body.mode??"");
  const admin=adminClient();

  if(mode==="plan"){
    const request=requestFromBody(body);
    const authority=await authorityFor(admin,request);

    // LAW preflight must close before ACT reads the owner-scoped KNOW receipt or selected block.
    if(authority.guard.status!=="READY"){
      const refusal=await persistRefusal(admin,{request,guard:authority.guard},workflowRef,payload.jti,"PLAN_PREAUTH",authority.guard.reason);
      return json({ok:false,status:"BLOCKED",guard:authority.guard,refusal_receipt:refusal},403);
    }

    const retrievalReceiptId=String(body.retrieval_receipt_id??"");
    const knowReceipt=await readReceipt(admin,retrievalReceiptId) as KnowReceipt|null;
    const selectedId=String((knowReceipt as any)?.evidence?.result?.selected_block_id??"");
    const selectedBlock=selectedId?await readBlock(admin,selectedId):null;
    const selectionUniverse=await readEligibleUniverse(admin);

    // WO4 — verified-lesson → decision seam. The decision context reports what
    // verified learning is AVAILABLE for the action's target; it never claims
    // influence (PR #1733: availability ≠ causal influence). The plan is built
    // twice — a control arm without the lesson and a treatment arm with it —
    // and influenced is true ONLY when the treatment observably differs from
    // the control. A read failure here fails closed: no plan is produced.
    const decisionContext: DecisionContext = await readDecisionContext(admin,OWNER_ID,request.target);
    const plan=buildActPlan(
      request,
      authority.lawReceipt,
      authority.liveGrant,
      authority.door,
      knowReceipt,
      selectedBlock,
      selectionUniverse,
      new Date(),
      decisionContext,
    );
    const controlPlan=buildActPlan(
      request,
      authority.lawReceipt,
      authority.liveGrant,
      authority.door,
      knowReceipt,
      selectedBlock,
      selectionUniverse,
      new Date(),
      null,
    );
    const learningInfluence=measureLearningInfluence(decisionContext,controlPlan,plan);

    const planHash=await digestValue({
      request,
      task_identity:plan.task_identity,
      selector:plan.selector,
      pre_learning_plan:plan.pre_learning_plan,
      post_retrieval_plan:plan.post_retrieval_plan,
      selected_intelligence:plan.selected_intelligence,
      retrieval_receipt_id:plan.retrieval_receipt_id,
      law_receipt_id:plan.guard.law_receipt_id,
      authority_grant_id:plan.guard.authority_grant_id,
      decision_context_evidence_id:plan.decision_context?.context?.evidence_id??null,
      learning_context_applied:plan.learning_context_applied,
      learning_influenced:learningInfluence.influenced,
    });

    if(plan.status==="BLOCKED"){
      const refusal=await persistRefusal(
        admin,
        {request,guard:authority.guard,plan,retrieval_receipt_id:retrievalReceiptId,plan_hash:planHash},
        workflowRef,payload.jti,"PLAN_GUARD",plan.reason
      );
      return json({ok:false,status:"BLOCKED",plan,refusal_receipt:refusal},409);
    }

    const planReceipt=await insertReceipt(admin,{
      user_id:OWNER_ID,project_id:PROJECT_ID,action:"act_node_plan",
      status:plan.status==="READY"?"SUCCESS":"BLOCKED",
      expected_result:"ACT.PLAN consumes only persisted KNOW/CONNECT selection evidence; retrieved intelligence may change planning but never creates authority.",
      observed_result:plan.status+":"+plan.post_retrieval_plan.behavior,
      evidence:{
        schema:"naya.act.plan.receipt.v1",
        node_id:"NAYA-KERNEL-ACT",
        stage:plan.status==="READY"?"PLAN_READY":"LAW_RERESOLUTION_REQUIRED",
        request,
        plan,
        plan_hash:planHash,
        law_receipt_id:plan.guard.law_receipt_id,
        authority_grant_id:plan.guard.authority_grant_id,
        retrieval_receipt_id:plan.retrieval_receipt_id,
        selector:ACT_RETRIEVAL_SELECTOR,
        decision_context:decisionContext,
        learning_influence:learningInfluence,
        control_plan_behavior:controlPlan.post_retrieval_plan.behavior,
        action_executed:false,
        independent_verification:false,
        verification_status:"PENDING_EXECUTION_AND_INDEPENDENT_VERIFY",
        runtime_identity:"naya-node-oidc",runtime_jti:payload.jti??null,workflow_ref:workflowRef
      },
      learning:[]
    });

    if(plan.status==="LAW_RERESOLUTION_REQUIRED"){
      return json({
        ok:false,status:"LAW_RERESOLUTION_REQUIRED",
        reason:"OLD_LAW_RECEIPT_CANNOT_AUTHORIZE_CHANGED_SCOPE",
        plan,plan_receipt:planReceipt,
        action_executed:false
      },409);
    }

    return json({
      ok:true,status:"PLANNED",node_id:"NAYA-KERNEL-ACT",
      plan,plan_receipt:planReceipt,
      decision_context:decisionContext,
      learning_influence:learningInfluence,
      action_executed:false,
      handoff_to:"NAYA-KERNEL-ACT/EXECUTE"
    });
  }

  if(mode==="execute" && String(body.plan_receipt_id??"")){
    const planReceiptId=String(body.plan_receipt_id??"");
    const planReceipt=await readReceipt(admin,planReceiptId) as any;
    if(
      !planReceipt ||
      planReceipt.action!=="act_node_plan" ||
      planReceipt.status!=="SUCCESS" ||
      planReceipt.evidence?.schema!=="naya.act.plan.receipt.v1" ||
      planReceipt.evidence?.stage!=="PLAN_READY"
    ){
      const refusal=await persistRefusal(admin,{plan_receipt_id:planReceiptId},workflowRef,payload.jti,"EXECUTE_PLAN_GUARD","PLAN_RECEIPT_INVALID");
      return json({ok:false,status:"BLOCKED",error:"PLAN_RECEIPT_INVALID",refusal_receipt:refusal},409);
    }

    const request=planReceipt.evidence.request as ActRequest;
    const storedPlan=planReceipt.evidence.plan;
    const authority=await authorityFor(admin,request);
    if(authority.guard.status!=="READY"){
      const refusal=await persistRefusal(admin,{request,guard:authority.guard,plan_receipt_id:planReceiptId},workflowRef,payload.jti,"EXECUTE_PREAUTH",authority.guard.reason);
      return json({ok:false,status:"BLOCKED",guard:authority.guard,refusal_receipt:refusal},403);
    }

    const retrievalReceiptId=String(planReceipt.evidence.retrieval_receipt_id??"");
    const knowReceipt=await readReceipt(admin,retrievalReceiptId) as KnowReceipt|null;
    const selectedId=String((knowReceipt as any)?.evidence?.result?.selected_block_id??"");
    const selectedBlock=selectedId?await readBlock(admin,selectedId):null;
    const selectionUniverse=await readEligibleUniverse(admin);
    // WO4: replay the treatment arm with the decision context pinned in the
    // stored plan, and re-measure the control-vs-treatment delta so the
    // influence claim is re-verified, not trusted from the receipt.
    const storedDecisionContext=(storedPlan as any)?.decision_context as DecisionContext | null ?? null;
    const recomputed=buildActPlan(
      request,
      authority.lawReceipt,
      authority.liveGrant,
      authority.door,
      knowReceipt,
      selectedBlock,
      selectionUniverse,
      new Date(),
      storedDecisionContext,
    );
    const recomputedControl=buildActPlan(
      request,
      authority.lawReceipt,
      authority.liveGrant,
      authority.door,
      knowReceipt,
      selectedBlock,
      selectionUniverse,
      new Date(),
      null,
    );
    const recomputedInfluence=measureLearningInfluence(storedDecisionContext,recomputedControl,recomputed);
    const recomputedHash=await digestValue({
      request,
      task_identity:recomputed.task_identity,
      selector:recomputed.selector,
      pre_learning_plan:recomputed.pre_learning_plan,
      post_retrieval_plan:recomputed.post_retrieval_plan,
      selected_intelligence:recomputed.selected_intelligence,
      retrieval_receipt_id:recomputed.retrieval_receipt_id,
      law_receipt_id:recomputed.guard.law_receipt_id,
      authority_grant_id:recomputed.guard.authority_grant_id,
      decision_context_evidence_id:recomputed.decision_context?.context?.evidence_id??null,
      learning_context_applied:recomputed.learning_context_applied,
      learning_influenced:recomputedInfluence.influenced,
    });

    if(
      recomputed.status!=="READY" ||
      !canonicalEqual(storedPlan,recomputed) ||
      String(planReceipt.evidence.plan_hash??"")!==recomputedHash
    ){
      const refusal=await persistRefusal(
        admin,
        {request,guard:authority.guard,stored_plan:storedPlan,recomputed_plan:recomputed,plan_receipt_id:planReceiptId,recomputed_hash:recomputedHash},
        workflowRef,payload.jti,"EXECUTE_REPLAY_GUARD","PLAN_STATE_CHANGED_OR_FORGED"
      );
      return json({ok:false,status:"BLOCKED",error:"PLAN_STATE_CHANGED_OR_FORGED",recomputed_plan:recomputed,refusal_receipt:refusal},409);
    }

    const selectedFingerprint=selectedBlock?await digestValue({
      intelligent_block_id:selectedBlock.intelligent_block_id,
      status:selectedBlock.status,
      understanding_state:selectedBlock.understanding_state,
      provenance:selectedBlock.provenance,
      evidence_refs:selectedBlock.evidence_refs,
      content:selectedBlock.content,
    }):null;
    const observed=String(recomputed.post_retrieval_plan.behavior);

    const receipt=await insertReceipt(admin,{
      user_id:OWNER_ID,project_id:PROJECT_ID,action:"act_node_execute",status:"SUCCESS",
      expected_result:"ACT.EXECUTE crosses the bounded effect boundary only from an exact durable ACT.PLAN plus fresh independently governed LAW/live authority.",
      observed_result:observed,
      evidence:{
        schema:"naya.act.receipt.v1",node_id:"NAYA-KERNEL-ACT",stage:"EXECUTED",
        planning_mode:"TWO_PHASE_KNOW_CONNECT_BOUND",
        plan_receipt_id:planReceiptId,
        retrieval_receipt_id:retrievalReceiptId,
        request,
        guard:authority.guard,
        plan_hash:recomputedHash,
        task_identity:recomputed.task_identity,
        selector:recomputed.selector,
        pre_learning_plan:recomputed.pre_learning_plan,
        post_retrieval_plan:recomputed.post_retrieval_plan,
        intelligence_applied_to_plan:recomputed.intelligence_applied_to_plan,
        selected_intelligence:recomputed.selected_intelligence,
        selected_intelligence_fingerprint:selectedFingerprint,
        observed_behavior:observed,
        observed:true,action_executed:true,
        independent_verification:false,
        verification_status:"PENDING_INDEPENDENT_RUNTIME_VERIFICATION",
        handoff_to:"NAYA-KERNEL-VERIFY",
        runtime_identity:"naya-node-oidc",runtime_jti:payload.jti??null,workflow_ref:workflowRef
      },
      learning:[]
    });
    return json({
      ok:true,status:"EXECUTED",node_id:"NAYA-KERNEL-ACT",
      planning_mode:"TWO_PHASE_KNOW_CONNECT_BOUND",
      guard:authority.guard,receipt,
      observation:{
        behavior:observed,
        selected_intelligence_id:recomputed.selected_intelligence?.intelligent_block_id??null,
        selected_intelligence_fingerprint:selectedFingerprint,
      },
      independent_verification:false,
      verification_status:"PENDING_INDEPENDENT_RUNTIME_VERIFICATION",
      handoff_to:"NAYA-KERNEL-VERIFY"
    });
  }

  if(mode==="execute"){
    // Historical bounded ACT specimen. Retained only so the previous live ACT proof remains reproducible.
    // It is NOT the learning-activation seam and MUST NOT be used to claim normal retrieval changed planning.
    const request=requestFromBody(body);
    const authority=await authorityFor(admin,request);

    if(authority.guard.status!=="READY"){
      const refusal=await persistRefusal(admin,{request,guard:authority.guard},workflowRef,payload.jti,"PRE_EXECUTION_GUARD",authority.guard.reason);
      return json({ok:false,status:"BLOCKED",guard:authority.guard,refusal_receipt:refusal},403);
    }

    const block=await readBlock(admin,LEGACY_BLOCK_ID);
    const lesson=String((block?.content as any)?.lesson??"");
    if(!lesson){
      const refusal=await persistRefusal(admin,{request,guard:authority.guard},workflowRef,payload.jti,"OBSERVATION_GUARD","OBSERVATION_UNAVAILABLE");
      return json({ok:false,status:"BLOCKED",guard:{...authority.guard,status:"BLOCKED",reason:"OBSERVATION_UNAVAILABLE"},refusal_receipt:refusal},409);
    }
    const canonicalDigest=await legacyDigest(lesson,block?.evidence_refs);
    const observed=lesson.includes("Preserve provenance before applying retained intelligence")
      ?"PRESERVE_PROVENANCE_BEFORE_APPLY"
      :"RETAINED_INTELLIGENCE_APPLIED";

    const receipt=await insertReceipt(admin,{
      user_id:OWNER_ID,project_id:PROJECT_ID,action:"act_node_execute",status:"SUCCESS",
      expected_result:"Historical ACT specimen executes exactly the LAW-authorized bounded Smart Door operation and records an observable result.",
      observed_result:observed,
      evidence:{
        schema:"naya.act.receipt.v1",node_id:"NAYA-KERNEL-ACT",stage:"EXECUTED",
        planning_mode:"LEGACY_DIRECT_SPECIMEN_NOT_LEARNING_ACTIVATION",
        request,guard:authority.guard,law_receipt_id:authority.guard.law_receipt_id,authority_grant_id:authority.guard.authority_grant_id,
        door:{door_id:DOOR.door_id,operation:DOOR.operation,authority_action:DOOR.authority_action},
        canonical_block_id:block?.intelligent_block_id,canonical_digest:canonicalDigest,
        observed_behavior:observed,observed:true,action_executed:true,
        independent_verification:false,
        verification_status:"PENDING_INDEPENDENT_RUNTIME_VERIFICATION",
        handoff_to:"NAYA-KERNEL-VERIFY",
        runtime_identity:"naya-node-oidc",runtime_jti:payload.jti??null,workflow_ref:workflowRef
      },
      learning:[]
    });
    return json({ok:true,status:"EXECUTED",node_id:"NAYA-KERNEL-ACT",planning_mode:"LEGACY_DIRECT_SPECIMEN_NOT_LEARNING_ACTIVATION",guard:authority.guard,receipt,observation:{behavior:observed,canonical_block_id:block?.intelligent_block_id,canonical_digest:canonicalDigest},handoff_to:"NAYA-KERNEL-VERIFY"});
  }

  if(mode==="inspect-plan"){
    const planReceiptId=String(body.plan_receipt_id??"");
    const planReceipt=await readReceipt(admin,planReceiptId) as any;
    if(!planReceipt || planReceipt.action!=="act_node_plan") return json({ok:false,error:"PLAN_RECEIPT_NOT_FOUND"},404);
    const request=planReceipt.evidence?.request as ActRequest;
    const authority=await authorityFor(admin,request);
    const retrievalReceiptId=String(planReceipt.evidence?.retrieval_receipt_id??"");
    const knowReceipt=await readReceipt(admin,retrievalReceiptId) as KnowReceipt|null;
    const selectedId=String((knowReceipt as any)?.evidence?.result?.selected_block_id??"");
    const selectedBlock=selectedId?await readBlock(admin,selectedId):null;
    const selectionUniverse=await readEligibleUniverse(admin);
    const recomputed=buildActPlan(request,authority.lawReceipt,authority.liveGrant,authority.door,knowReceipt,selectedBlock,selectionUniverse,new Date());
    return json({
      ok:true,
      status:"CANONICAL_PLAN_REREAD",
      plan_receipt:planReceipt,
      retrieval_receipt:knowReceipt,
      law_receipt:authority.lawReceipt,
      live_grant:authority.liveGrant,
      selected_block:selectedBlock,
      recomputed_plan:recomputed,
      cold_reconstruction:true,
      independent_verification:false,
      executor_claim_trusted_as_verification:false,
      runtime_identity:"naya-node-oidc",workflow_ref:workflowRef,token_jti:payload.jti??null
    });
  }

  if(mode==="inspect"){
    const actionId=String(body.action_receipt_id??"");
    const refusalId=String(body.refusal_receipt_id??"");
    const actionReceipt=await readReceipt(admin,actionId);
    const refusalReceipt=refusalId?await readReceipt(admin,refusalId):null;
    if(!actionReceipt) return json({ok:false,error:"ACTION_RECEIPT_NOT_FOUND"},404);
    const lawId=String((actionReceipt as any)?.evidence?.law_receipt_id??(actionReceipt as any)?.evidence?.guard?.law_receipt_id??"");
    const lawReceipt=await readReceipt(admin,lawId);
    const refs=Array.isArray((lawReceipt as any)?.evidence?.law_decision?.authority_refs)?(lawReceipt as any).evidence.law_decision.authority_refs:[];
    const liveGrant=refs.length===1?await readGrant(admin,String(refs[0])):null;
    const blockId=String((actionReceipt as any)?.evidence?.selected_intelligence?.intelligent_block_id??(actionReceipt as any)?.evidence?.canonical_block_id??LEGACY_BLOCK_ID);
    const block=await readBlock(admin,blockId);
    return json({ok:true,status:"AUTHORITATIVE_STATE_REREAD",action_receipt:actionReceipt,refusal_receipt:refusalReceipt,law_receipt:lawReceipt,live_grant:liveGrant,canonical_block:block,door_contract:DOOR,runtime_identity:"naya-node-oidc",workflow_ref:workflowRef,token_jti:payload.jti??null});
  }
  return json({ok:false,error:"UNSUPPORTED_MODE"},400);
 }catch(e){return json({ok:false,error:String((e as Error)?.message??e)},400)}
});
