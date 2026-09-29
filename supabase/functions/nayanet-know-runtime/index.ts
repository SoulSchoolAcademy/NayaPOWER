import { createRemoteJWKSet, jwtVerify } from "https://esm.sh/jose@6.0.10";
import { createClient } from "npm:@supabase/supabase-js@2";
import { hasCallerSuppliedIntelligence, selectKnowContext, validateKnowAuthorization, type KnowAuthorityGrant, type KnowRequest } from "./know.ts";

const ISSUER="https://token.actions.githubusercontent.com";
const AUDIENCE="nayanet-runtime";
const REPOSITORY="SoulSchoolAcademy/NayaPOWER";
const WORKFLOW=".github/workflows/live-know-proof.yml";
const REF="refs/heads/main";
const OWNER_ID="adfdf0b8-5558-41d1-9fed-ec51abf4fe2f";
const NAYA_ID="NAYA-NODE-0001";
const PROJECT_ID="NayaNET";
const MAX_LAW_AGE_SECONDS=900;
const JWKS=createRemoteJWKSet(new URL("https://token.actions.githubusercontent.com/.well-known/jwks"));

const json=(body:unknown,status=200)=>new Response(JSON.stringify(body),{status,headers:{"content-type":"application/json","cache-control":"no-store"}});

async function authenticate(req:Request){
  const h=req.headers.get("authorization")??"";
  if(!h.startsWith("Bearer ")) throw new Error("RUNTIME_IDENTITY_REQUIRED");
  const {payload}=await jwtVerify(h.slice(7),JWKS,{issuer:ISSUER,audience:AUDIENCE});
  const expected=REPOSITORY+"/"+WORKFLOW+"@"+REF;
  if(payload.repository!==REPOSITORY || payload.workflow_ref!==expected || payload.ref!==REF) throw new Error("WORKFLOW_BINDING_MISMATCH");
  return {payload,workflowRef:expected};
}

function adminClient(){
  const url=Deno.env.get("SUPABASE_URL"),key=Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");
  if(!url||!key) throw new Error("SERVER_AUTH_CONFIG_MISSING");
  return createClient(url,key,{auth:{persistSession:false}});
}

async function readLawReceipt(admin:ReturnType<typeof adminClient>,id:string){
  if(!id) return null;
  const {data,error}=await admin.from("nayanet_execution_receipts").select("*").eq("id",id).eq("user_id",OWNER_ID).eq("project_id",PROJECT_ID).maybeSingle();
  if(error) throw error;
  return data;
}

async function readAuthorityGrant(admin:ReturnType<typeof adminClient>,id:string){
  if(!id) return null;
  const {data,error}=await admin.from("nayanet_authority_grants").select("*").eq("grant_id",id).maybeSingle();
  if(error) throw error;
  return data as KnowAuthorityGrant|null;
}

async function resolveKnowAuthorization(admin:ReturnType<typeof adminClient>,receipt:any,now=new Date()){
  const refs=Array.isArray(receipt?.evidence?.law_decision?.authority_refs)?receipt.evidence.law_decision.authority_refs.map(String):[];
  const grant=refs.length===1?await readAuthorityGrant(admin,refs[0]):null;
  return validateKnowAuthorization(receipt,grant,OWNER_ID,NAYA_ID,now,MAX_LAW_AGE_SECONDS);
}

async function readEligibleUniverse(admin:ReturnType<typeof adminClient>){
  const {data,error}=await admin.from("nayanet_intelligent_blocks")
    .select("intelligent_block_id,owner_id,status,understanding_state,owner_scope,applicable_scope,value_context,content,provenance,evidence_refs,superseded_by_block_id,updated_at")
    .eq("owner_id",OWNER_ID);
  if(error) throw error;
  return data??[];
}

async function readReceipt(admin:ReturnType<typeof adminClient>,id:string){
  if(!id) return null;
  const {data,error}=await admin.from("nayanet_execution_receipts").select("*").eq("id",id).eq("user_id",OWNER_ID).eq("project_id",PROJECT_ID).maybeSingle();
  if(error) throw error;
  return data;
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
  throw new Error("KNOW_RECEIPT_REVISION_CONFLICT");
}

function requestFrom(body:Record<string,unknown>):KnowRequest{
  if(hasCallerSuppliedIntelligence(body)) throw new Error("CALLER_SELECTED_INTELLIGENCE_FORBIDDEN");
  const task_id=String(body.task_id??"").trim();
  const task_class=String(body.task_class??"").trim();
  const required_capability=String(body.required_capability??"").trim();
  if(!task_id || !task_class || !required_capability) throw new Error("TASK_CONTEXT_REQUIRED");
  return {owner_id:OWNER_ID,naya_id:NAYA_ID,task_id,task_class,required_capability};
}

Deno.serve(async(req)=>{
  try{
    if(req.method!=="POST") return json({ok:false,error:"METHOD_NOT_ALLOWED"},405);
    const {payload,workflowRef}=await authenticate(req);
    const body=await req.json().catch(()=>({})) as Record<string,unknown>;
    const mode=String(body.mode??"");
    const admin=adminClient();

    if(mode==="retrieve"){
      const request=requestFrom(body);
      const lawReceipt=await readLawReceipt(admin,String(body.law_receipt_id??""));
      const authority=await resolveKnowAuthorization(admin,lawReceipt);
      if(!authority.ok) return json({ok:false,status:"BLOCKED",error:authority.reason,retrieval_creates_authority:false},403);
      const universe=await readEligibleUniverse(admin);
      const result=selectKnowContext(request,universe);
      const receipt=await insertReceipt(admin,{
        user_id:OWNER_ID,project_id:PROJECT_ID,action:"know_context_retrieval",status:"SUCCESS",
        expected_result:"KNOW selects only owner-scoped current intelligence applicable to caller task context without caller-supplied answer/block identity.",
        observed_result:result.status+":"+(result.selected_block_id??"NONE"),
        evidence:{schema:"naya.know.receipt.v1",node_id:"NAYA-KERNEL-KNOW",request,result,law_receipt_id:authority.law_receipt_id,
          authority_refs:authority.authority_refs,caller_selected_block:false,retrieval_creates_authority:false,candidate_count:universe.length,
          handoff_to:"NAYA-KERNEL-PROVE",runtime_identity:"naya-node-oidc",runtime_jti:payload.jti??null,workflow_ref:workflowRef},
        learning:[]
      });
      return json({ok:true,status:"KNOW_RETRIEVED",node_id:"NAYA-KERNEL-KNOW",request,result,receipt,handoff_to:"NAYA-KERNEL-PROVE",retrieval_creates_authority:false});
    }

    if(mode==="inspect"){
      const receiptId=String(body.retrieval_receipt_id??"");
      const request=requestFrom(body);
      const receipt=await readReceipt(admin,receiptId);
      if(!receipt || receipt.action!=="know_context_retrieval") return json({ok:false,error:"KNOW_RECEIPT_NOT_FOUND"},404);
      const lawReceipt=await readLawReceipt(admin,String(receipt.evidence?.law_receipt_id??""));
      const authority=await resolveKnowAuthorization(admin,lawReceipt);
      if(!authority.ok) return json({ok:false,status:"BLOCKED",error:authority.reason},403);
      const universe=await readEligibleUniverse(admin);
      const recomputed=selectKnowContext(request,universe);
      const recorded=receipt.evidence?.result??{};
      const sameTask=receipt.evidence?.request?.task_id===request.task_id &&
        receipt.evidence?.request?.task_class===request.task_class &&
        receipt.evidence?.request?.required_capability===request.required_capability;
      const same=sameTask && recorded.status===recomputed.status &&
        (recorded.selected_block_id??null)===(recomputed.selected_block_id??null) &&
        recorded.applicable===recomputed.applicable && recorded.reason===recomputed.reason &&
        recorded.retrieval_creates_authority===false;
      return json({ok:same,status:same?"KNOW_SELECTION_VERIFIED":"KNOW_SELECTION_MISMATCH",independent_verification:same,
        executor_claim_trusted_as_verification:false,node_id:"NAYA-KERNEL-KNOW",request,recorded,recomputed,
        authority_basis:{law_receipt_id:lawReceipt.id,retrieval_creates_authority:false},persisted_universe_reread:true,
        handoff_to:"NAYA-KERNEL-PROVE",runtime_identity:"naya-node-oidc",workflow_ref:workflowRef,token_jti:payload.jti??null},same?200:409);
    }

    return json({ok:false,error:"UNSUPPORTED_MODE"},400);
  }catch(e){return json({ok:false,error:String((e as Error)?.message??e)},400);}
});
