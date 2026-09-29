import { createRemoteJWKSet, jwtVerify } from "https://esm.sh/jose@6.0.10";
import { createClient } from "npm:@supabase/supabase-js@2";
import { validateAct, type ActRequest, type LawReceipt, type Grant, type DoorOperation } from "./act.ts";

const ISSUER="https://token.actions.githubusercontent.com";
const AUDIENCE="nayanet-runtime";
const REPOSITORY="SoulSchoolAcademy/NayaPOWER";
const WORKFLOW=".github/workflows/live-act-proof.yml";
const REF="refs/heads/main";
const OWNER_ID="adfdf0b8-5558-41d1-9fed-ec51abf4fe2f";
const NAYA_ID="NAYA-NODE-0001";
const PROJECT_ID="NayaNET";
const BLOCK_ID="IB-NAYA-NODE-0001-0001";
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
  return data as LawReceipt|null;
}
async function readGrant(admin:ReturnType<typeof adminClient>,id:string){
  if(!id) return null;
  const {data,error}=await admin.from("nayanet_authority_grants").select("*").eq("grant_id",id).maybeSingle();
  if(error) throw error;
  return data as Grant|null;
}
async function readBlock(admin:ReturnType<typeof adminClient>){
  const {data,error}=await admin.from("nayanet_intelligent_blocks").select("intelligent_block_id,owner_id,understanding_state,content,evidence_refs,provenance").eq("intelligent_block_id",BLOCK_ID).eq("owner_id",OWNER_ID).maybeSingle();
  if(error) throw error;
  if(!data) throw new Error("CANONICAL_BLOCK_NOT_FOUND");
  return data;
}
async function digest(lesson:string,refs:unknown){
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

Deno.serve(async(req)=>{
 try{
  if(req.method!=="POST") return json({ok:false,error:"METHOD_NOT_ALLOWED"},405);
  const {payload,workflowRef}=await authenticate(req);
  const body=await req.json().catch(()=>({})) as Record<string,unknown>;
  const mode=String(body.mode??"");
  const admin=adminClient();

  if(mode==="execute"){
    const request:ActRequest={
      owner_id:OWNER_ID,naya_id:NAYA_ID,
      law_receipt_id:String(body.law_receipt_id??""),
      action:String(body.action??""),
      target:String(body.target??""),
      door_id:String(body.door_id??""),
      operation:String(body.operation??""),
      retrieved_intelligence_claims_authority:body.retrieved_intelligence_claims_authority===true,
      successor_context_claims_inherited_authority:body.successor_context_claims_inherited_authority===true
    };
    const lawReceipt=await readReceipt(admin,request.law_receipt_id??"");
    const refs=Array.isArray((lawReceipt as any)?.evidence?.law_decision?.authority_refs)?(lawReceipt as any).evidence.law_decision.authority_refs:[];
    const liveGrant=refs.length===1?await readGrant(admin,String(refs[0])):null;
    const door=(request.door_id===DOOR.door_id && request.operation===DOOR.operation)?DOOR:null;
    const guard=validateAct(request,lawReceipt,liveGrant,door,new Date());

    if(guard.status!=="READY"){
      const refusal=await insertReceipt(admin,{
        user_id:OWNER_ID,project_id:PROJECT_ID,action:"act_node_refusal",status:"BLOCKED",
        expected_result:"ACT must refuse before execution unless a fresh AUTHORIZED LAW receipt exactly covers the requested Smart Door action and target.",
        observed_result:"REFUSED:"+guard.reason,
        evidence:{schema:"naya.act.receipt.v1",node_id:"NAYA-KERNEL-ACT",stage:"PRE_EXECUTION_GUARD",request,guard,door_capability_available:request.door_id==="DOOR-AI",action_executed:false,observed:false,runtime_identity:"naya-node-oidc",runtime_jti:payload.jti??null,workflow_ref:workflowRef},
        learning:[]
      });
      return json({ok:false,status:"BLOCKED",guard,refusal_receipt:refusal},403);
    }

    const block=await readBlock(admin);
    const lesson=String((block.content as any)?.lesson??"");
    if(!lesson){
      const refusal=await insertReceipt(admin,{
        user_id:OWNER_ID,project_id:PROJECT_ID,action:"act_node_refusal",status:"BLOCKED",
        expected_result:"ACT must not claim execution when the bounded operation cannot produce an observable result.",
        observed_result:"REFUSED:OBSERVATION_UNAVAILABLE",
        evidence:{schema:"naya.act.receipt.v1",node_id:"NAYA-KERNEL-ACT",stage:"OBSERVATION_GUARD",request,guard,action_executed:false,observed:false,runtime_identity:"naya-node-oidc",runtime_jti:payload.jti??null,workflow_ref:workflowRef},
        learning:[]
      });
      return json({ok:false,status:"BLOCKED",guard:{...guard,status:"BLOCKED",reason:"OBSERVATION_UNAVAILABLE"},refusal_receipt:refusal},409);
    }
    const canonicalDigest=await digest(lesson,block.evidence_refs);
    const observed=lesson.includes("Preserve provenance before applying retained intelligence")
      ?"PRESERVE_PROVENANCE_BEFORE_APPLY"
      :"RETAINED_INTELLIGENCE_APPLIED";

    const receipt=await insertReceipt(admin,{
      user_id:OWNER_ID,project_id:PROJECT_ID,action:"act_node_execute",status:"SUCCESS",
      expected_result:"ACT executes exactly the LAW-authorized bounded Smart Door operation and records an observable result.",
      observed_result:observed,
      evidence:{
        schema:"naya.act.receipt.v1",node_id:"NAYA-KERNEL-ACT",stage:"EXECUTED",
        request,guard,law_receipt_id:guard.law_receipt_id,authority_grant_id:guard.authority_grant_id,
        door:{door_id:DOOR.door_id,operation:DOOR.operation,authority_action:DOOR.authority_action},
        canonical_block_id:block.intelligent_block_id,canonical_digest:canonicalDigest,
        observed_behavior:observed,observed:true,action_executed:true,
        handoff_to:"NAYA-KERNEL-VERIFY",
        runtime_identity:"naya-node-oidc",runtime_jti:payload.jti??null,workflow_ref:workflowRef
      },
      learning:[]
    });
    return json({ok:true,status:"EXECUTED",node_id:"NAYA-KERNEL-ACT",guard,receipt,observation:{behavior:observed,canonical_block_id:block.intelligent_block_id,canonical_digest:canonicalDigest},handoff_to:"NAYA-KERNEL-VERIFY"});
  }

  if(mode==="inspect"){
    const actionId=String(body.action_receipt_id??"");
    const refusalId=String(body.refusal_receipt_id??"");
    const actionReceipt=await readReceipt(admin,actionId);
    const refusalReceipt=refusalId?await readReceipt(admin,refusalId):null;
    if(!actionReceipt) return json({ok:false,error:"ACTION_RECEIPT_NOT_FOUND"},404);
    const lawId=String((actionReceipt as any)?.evidence?.law_receipt_id??"");
    const lawReceipt=await readReceipt(admin,lawId);
    const refs=Array.isArray((lawReceipt as any)?.evidence?.law_decision?.authority_refs)?(lawReceipt as any).evidence.law_decision.authority_refs:[];
    const liveGrant=refs.length===1?await readGrant(admin,String(refs[0])):null;
    const block=await readBlock(admin);
    return json({ok:true,status:"AUTHORITATIVE_STATE_REREAD",action_receipt:actionReceipt,refusal_receipt:refusalReceipt,law_receipt:lawReceipt,live_grant:liveGrant,canonical_block:block,door_contract:DOOR,runtime_identity:"naya-node-oidc",workflow_ref:workflowRef,token_jti:payload.jti??null});
  }
  return json({ok:false,error:"UNSUPPORTED_MODE"},400);
 }catch(e){return json({ok:false,error:String((e as Error)?.message??e)},400)}
});
