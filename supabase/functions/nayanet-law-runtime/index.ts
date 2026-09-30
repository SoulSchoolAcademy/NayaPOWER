import { createRemoteJWKSet, jwtVerify } from "https://esm.sh/jose@6.0.10";
import { createClient } from "npm:@supabase/supabase-js@2";
import { evaluateLaw, type LawRequest, type AuthorityGrant } from "./law.ts";

const ISSUER="https://token.actions.githubusercontent.com";
const AUDIENCE="nayanet-runtime";
const REPOSITORY="SoulSchoolAcademy/NayaPOWER";
const WORKFLOWS=new Set([".github/workflows/live-law-proof.yml",".github/workflows/live-act-proof.yml",".github/workflows/live-know-proof.yml",".github/workflows/live-prove-proof.yml",".github/workflows/live-connect-proof.yml"]);
const REF="refs/heads/main";
const OWNER_ID="adfdf0b8-5558-41d1-9fed-ec51abf4fe2f";
const NAYA_ID="NAYA-NODE-0001";
const PROJECT_ID="NayaNET";
const JWKS=createRemoteJWKSet(new URL("https://token.actions.githubusercontent.com/.well-known/jwks"));

const json=(body:unknown,status=200)=>new Response(JSON.stringify(body),{status,headers:{"content-type":"application/json","cache-control":"no-store"}});

async function authenticate(req:Request){
  const h=req.headers.get("authorization")??"";
  if(!h.startsWith("Bearer ")) throw new Error("RUNTIME_IDENTITY_REQUIRED");
  const {payload}=await jwtVerify(h.slice(7),JWKS,{issuer:ISSUER,audience:AUDIENCE});
  const workflowRef=String(payload.workflow_ref??"");
  const expectedRefs=Array.from(WORKFLOWS).map(w=>REPOSITORY+"/"+w+"@"+REF);
  if(payload.repository!==REPOSITORY || !expectedRefs.includes(workflowRef) || payload.ref!==REF) throw new Error("WORKFLOW_BINDING_MISMATCH");
  return {payload,workflowRef};
}
function adminClient(){
  const url=Deno.env.get("SUPABASE_URL"), key=Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");
  if(!url||!key) throw new Error("SERVER_AUTH_CONFIG_MISSING");
  return createClient(url,key,{auth:{persistSession:false}});
}
async function loadGrants(admin:ReturnType<typeof adminClient>){
  const {data,error}=await admin.from("nayanet_authority_grants").select("*").eq("issuer_id",OWNER_ID).eq("subject_id",OWNER_ID);
  if(error) throw error;
  return (data??[]) as AuthorityGrant[];
}
async function persistDecision(admin:ReturnType<typeof adminClient>, request:LawRequest, decision:ReturnType<typeof evaluateLaw>, jti:string){
  for(let attempt=0;attempt<4;attempt++){
    const {data:maxRows,error:maxError}=await admin.from("nayanet_execution_receipts").select("revision").eq("user_id",OWNER_ID).eq("project_id",PROJECT_ID).order("revision",{ascending:false}).limit(1);
    if(maxError) throw maxError;
    const revision=Number(maxRows?.[0]?.revision??0)+1;
    const evidence={
      schema:"naya.law.receipt.v1",
      node_id:"NAYA-KERNEL-LAW",
      law_request:request,
      law_decision:decision,
      runtime_identity:"naya-node-oidc",
      runtime_jti:jti,
      execution_boundary:"LAW_DECIDES_ONLY_DOES_NOT_EXECUTE"
    };
    const {data,error}=await admin.from("nayanet_execution_receipts").insert({
      user_id:OWNER_ID,project_id:PROJECT_ID,revision,
      action:"law_authority_decision",
      expected_result:"LAW returns and persists a bounded authority decision without executing the requested action.",
      observed_result:decision.status+":"+decision.reason,
      status:decision.status==="AUTHORIZED"?"SUCCESS":"BLOCKED",
      evidence,learning:[]
    }).select("id,revision,action,status,evidence,created_at").single();
    if(!error) return data;
    if(!String(error.message??"").toLowerCase().includes("duplicate")) throw error;
  }
  throw new Error("LAW_RECEIPT_REVISION_CONFLICT");
}
async function getReceipt(admin:ReturnType<typeof adminClient>,id:string){
  const {data,error}=await admin.from("nayanet_execution_receipts").select("*").eq("id",id).eq("user_id",OWNER_ID).maybeSingle();
  if(error) throw error;
  return data;
}

Deno.serve(async(req)=>{
 try{
  if(req.method!=="POST") return json({ok:false,error:"METHOD_NOT_ALLOWED"},405);
  const {payload,workflowRef}=await authenticate(req);
  const body=await req.json().catch(()=>({})) as Record<string,unknown>;
  const mode=String(body.mode??"");
  const admin=adminClient();
  if(mode==="evaluate"){
    const request={...(body.request as LawRequest),owner_id:OWNER_ID,naya_id:NAYA_ID};
    const grants=await loadGrants(admin);
    const decision=evaluateLaw(request,grants,new Date());
    const receipt=await persistDecision(admin,request,decision,String(payload.jti??""));
    return json({ok:true,status:"LAW_EVALUATED",node_id:"NAYA-KERNEL-LAW",runtime_identity:"naya-node-oidc",workflow_ref:workflowRef,request,decision,receipt});
  }
  if(mode==="verify"){
    const receiptId=String(body.receipt_id??"");
    if(!receiptId) return json({ok:false,error:"RECEIPT_ID_REQUIRED"},400);
    const receipt=await getReceipt(admin,receiptId);
    if(!receipt || receipt.action!=="law_authority_decision") return json({ok:false,error:"LAW_RECEIPT_NOT_FOUND"},404);
    const request=receipt.evidence?.law_request as LawRequest;
    const recorded=receipt.evidence?.law_decision;
    const grants=await loadGrants(admin);
    const recomputed=evaluateLaw(request,grants,new Date());
    const same=recorded?.status===recomputed.status && recorded?.reason===recomputed.reason &&
      JSON.stringify(recorded?.authority_refs??[])===JSON.stringify(recomputed.authority_refs??[]);
    return json({ok:same,status:same?"LAW_DECISION_VERIFIED":"LAW_DECISION_MISMATCH",independent_verification:true,node_id:"NAYA-KERNEL-LAW",receipt,recorded,recomputed});
  }
  if(mode==="verify_existing_action"){
    const receiptId=String(body.receipt_id??"");
    const receipt=await getReceipt(admin,receiptId);
    if(!receipt) return json({ok:false,error:"ACTION_RECEIPT_NOT_FOUND"},404);
    const authority=receipt.evidence?.authority;
    const request:LawRequest={owner_id:OWNER_ID,naya_id:NAYA_ID,action:String(receipt.action??""),target:String(receipt.evidence?.target_id??NAYA_ID)};
    const grants=await loadGrants(admin);
    const decision=evaluateLaw(request,grants,new Date());
    const matches=decision.status==="AUTHORIZED" && authority?.status==="AUTHORIZED" &&
      decision.authority_refs.includes(String(receipt.evidence?.resolved_authority_grant_id??authority?.grant_id??""));
    return json({ok:matches,status:matches?"EXISTING_ACTION_AUTHORITY_VERIFIED":"EXISTING_ACTION_AUTHORITY_MISMATCH",receipt_id:receiptId,decision,action_receipt:receipt});
  }
  return json({ok:false,error:"UNSUPPORTED_MODE"},400);
 }catch(e){return json({ok:false,error:String((e as Error)?.message??e)},400)}
});
