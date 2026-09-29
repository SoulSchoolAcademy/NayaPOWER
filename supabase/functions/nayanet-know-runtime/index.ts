import { createRemoteJWKSet, jwtVerify } from "https://esm.sh/jose@6.0.10";
import { createClient } from "npm:@supabase/supabase-js@2";
import { selectKnow, type KnowCandidate, type KnowRequest } from "./know.ts";

const ISSUER="https://token.actions.githubusercontent.com";
const AUDIENCE="nayanet-runtime";
const REPOSITORY="SoulSchoolAcademy/NayaPOWER";
const WORKFLOW=".github/workflows/live-know-proof.yml";
const REF="refs/heads/main";
const OWNER_ID="adfdf0b8-5558-41d1-9fed-ec51abf4fe2f";
const NAYA_ID="NAYA-NODE-0001";
const PROJECT_ID="NayaNET";
const JWKS=createRemoteJWKSet(new URL("https://token.actions.githubusercontent.com/.well-known/jwks"));

const json=(body:unknown,status=200)=>new Response(JSON.stringify(body),{
  status,
  headers:{"content-type":"application/json","cache-control":"no-store"}
});

async function authenticate(req:Request){
  const h=req.headers.get("authorization")??"";
  if(!h.startsWith("Bearer ")) throw new Error("RUNTIME_IDENTITY_REQUIRED");
  const {payload}=await jwtVerify(h.slice(7),JWKS,{issuer:ISSUER,audience:AUDIENCE});
  const workflowRef=REPOSITORY+"/"+WORKFLOW+"@"+REF;
  if(payload.repository!==REPOSITORY||payload.workflow_ref!==workflowRef||payload.ref!==REF){
    throw new Error("WORKFLOW_BINDING_MISMATCH");
  }
  return {payload,workflowRef};
}

function adminClient(){
  const url=Deno.env.get("SUPABASE_URL");
  const key=Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");
  if(!url||!key) throw new Error("SERVER_AUTH_CONFIG_MISSING");
  return createClient(url,key,{auth:{persistSession:false}});
}

async function readCandidates(admin:ReturnType<typeof adminClient>){
  const {data,error}=await admin
    .from("nayanet_intelligent_blocks")
    .select("block_id,intelligent_block_id,owner_id,subject_id,title,status,understanding_state,owner_scope,evidence_refs,provenance,applicable_scope,content,superseded_by_block_id,updated_at")
    .eq("owner_id",OWNER_ID)
    .in("status",["ACTIVE","DURABLE"])
    .in("understanding_state",["VERIFIED","DISTILLED","APPLIED","LEARNED"])
    .is("superseded_by_block_id",null)
    .order("updated_at",{ascending:false})
    .limit(100);
  if(error) throw error;
  return (data??[]) as KnowCandidate[];
}

async function readReceipt(admin:ReturnType<typeof adminClient>,id:string){
  const {data,error}=await admin.from("nayanet_execution_receipts")
    .select("*")
    .eq("id",id)
    .eq("user_id",OWNER_ID)
    .eq("project_id",PROJECT_ID)
    .maybeSingle();
  if(error) throw error;
  return data;
}

async function insertReceipt(admin:ReturnType<typeof adminClient>,row:Record<string,unknown>){
  for(let attempt=0;attempt<8;attempt++){
    const {data:maxRows,error:maxError}=await admin.from("nayanet_execution_receipts")
      .select("revision").eq("user_id",OWNER_ID).eq("project_id",PROJECT_ID)
      .order("revision",{ascending:false}).limit(1);
    if(maxError) throw maxError;
    const revision=Number(maxRows?.[0]?.revision??0)+1;
    const {data,error}=await admin.from("nayanet_execution_receipts")
      .insert({...row,revision}).select("*").single();
    if(!error) return data;
    if(error.code!=="23505") throw error;
  }
  throw new Error("KNOW_RECEIPT_REVISION_CONFLICT");
}

function sanitizeRequest(body:Record<string,unknown>):KnowRequest{
  return {
    owner_id:OWNER_ID,
    naya_id:NAYA_ID,
    target:String(body.target??NAYA_ID),
    task_context:String(body.task_context??""),
    intelligent_block_id:body.intelligent_block_id===undefined?undefined:String(body.intelligent_block_id),
    block_id:body.block_id===undefined?undefined:String(body.block_id),
    lesson:body.lesson===undefined?undefined:String(body.lesson),
    answer:body.answer===undefined?undefined:String(body.answer),
    intelligence:body.intelligence,
    intelligence_content:body.intelligence_content
  };
}

Deno.serve(async(req)=>{
  try{
    if(req.method!=="POST") return json({ok:false,error:"METHOD_NOT_ALLOWED"},405);
    const {payload,workflowRef}=await authenticate(req);
    const body=await req.json().catch(()=>({})) as Record<string,unknown>;
    const mode=String(body.mode??"");
    const admin=adminClient();

    if(mode==="retrieve"){
      const request=sanitizeRequest(body);
      const candidates=await readCandidates(admin);
      const decision=selectKnow(request,candidates);

      const status=decision.status==="SELECTED"?"SUCCESS":decision.status==="MISS"?"MISS":"BLOCKED";
      const receipt=await insertReceipt(admin,{
        user_id:OWNER_ID,
        project_id:PROJECT_ID,
        action:decision.status==="SELECTED"?"know_node_retrieval":decision.status==="MISS"?"know_node_miss":"know_node_refusal",
        status,
        expected_result:"KNOW selects only current canonical intelligence applicable to task/context without caller-supplied answer or authority.",
        observed_result:decision.reason,
        evidence:{
          schema:"naya.know.receipt.v1",
          node_id:"NAYA-KERNEL-KNOW",
          request:{target:request.target,task_context:request.task_context},
          candidate_count:candidates.length,
          decision:{
            status:decision.status,
            reason:decision.reason,
            score:decision.score,
            matched_terms:decision.matched_terms,
            selected_intelligent_block_id:decision.selected?.intelligent_block_id??null
          },
          selected:decision.selected?{
            intelligent_block_id:decision.selected.intelligent_block_id,
            block_id:decision.selected.block_id??null,
            owner_id:decision.selected.owner_id,
            owner_scope:decision.selected.owner_scope??null,
            status:decision.selected.status??null,
            understanding_state:decision.selected.understanding_state??null,
            provenance:decision.selected.provenance??null,
            evidence_refs:decision.selected.evidence_refs??null,
            applicable_scope:decision.selected.applicable_scope??null
          }:null,
          retrieval_grants_authority:false,
          handoff_to:"NAYA-KERNEL-PROVE",
          runtime_identity:"naya-node-oidc",
          runtime_jti:payload.jti??null,
          workflow_ref:workflowRef
        },
        learning:[]
      });

      const code=decision.status==="BLOCKED"?409:200;
      return json({
        ok:decision.status!=="BLOCKED",
        status:decision.status,
        node_id:"NAYA-KERNEL-KNOW",
        decision,
        receipt,
        authority_created:false,
        handoff_to:"NAYA-KERNEL-PROVE"
      },code);
    }

    if(mode==="inspect"){
      const selectedReceiptId=String(body.selected_receipt_id??"");
      const missReceiptId=String(body.miss_receipt_id??"");
      if(!selectedReceiptId||!missReceiptId) return json({ok:false,error:"KNOW_RECEIPT_IDS_REQUIRED"},400);
      const [selectedReceipt,missReceipt,candidates]=await Promise.all([
        readReceipt(admin,selectedReceiptId),
        readReceipt(admin,missReceiptId),
        readCandidates(admin)
      ]);
      if(!selectedReceipt||!missReceipt) return json({ok:false,error:"KNOW_RECEIPT_NOT_FOUND"},404);
      return json({
        ok:true,
        status:"AUTHORITATIVE_STATE_REREAD",
        selected_receipt:selectedReceipt,
        miss_receipt:missReceipt,
        candidates,
        runtime_identity:"naya-node-oidc",
        workflow_ref:workflowRef,
        token_jti:payload.jti??null
      });
    }

    return json({ok:false,error:"UNSUPPORTED_MODE"},400);
  }catch(e){
    return json({ok:false,error:String((e as Error)?.message??e)},400);
  }
});
