import { createRemoteJWKSet, jwtVerify } from "https://esm.sh/jose@6.0.10";
import { createClient } from "npm:@supabase/supabase-js@2";
import { assessKnowProof, sameAssessment, type ProveKnowReceipt, type ProveBlock, type ProveGrant, type ProveRelationship } from "./prove.ts";

const ISSUER="https://token.actions.githubusercontent.com";
const AUDIENCE="nayanet-runtime";
const REPOSITORY="SoulSchoolAcademy/NayaPOWER";
const WORKFLOW=".github/workflows/live-prove-proof.yml";
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
  const expected=REPOSITORY+"/"+WORKFLOW+"@"+REF;
  if(payload.repository!==REPOSITORY || payload.workflow_ref!==expected || payload.ref!==REF) throw new Error("WORKFLOW_BINDING_MISMATCH");
  return {payload,workflowRef:expected};
}

function adminClient(){
  const url=Deno.env.get("SUPABASE_URL"),key=Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");
  if(!url||!key) throw new Error("SERVER_AUTH_CONFIG_MISSING");
  return createClient(url,key,{auth:{persistSession:false}});
}

async function readReceipt(admin:ReturnType<typeof adminClient>,id:string){
  if(!id) return null;
  const {data,error}=await admin.from("nayanet_execution_receipts").select("*")
    .eq("id",id).eq("user_id",OWNER_ID).eq("project_id",PROJECT_ID).maybeSingle();
  if(error) throw error;
  return data;
}

async function readGrant(admin:ReturnType<typeof adminClient>,id:string){
  if(!id) return null;
  const {data,error}=await admin.from("nayanet_authority_grants").select("*").eq("grant_id",id).maybeSingle();
  if(error) throw error;
  return data as ProveGrant|null;
}

async function readBlock(admin:ReturnType<typeof adminClient>,id:string){
  if(!id) return null;
  const {data,error}=await admin.from("nayanet_intelligent_blocks")
    .select("intelligent_block_id,owner_id,status,understanding_state,applicable_scope,content,provenance,evidence_refs,superseded_by_block_id")
    .eq("intelligent_block_id",id).eq("owner_id",OWNER_ID).maybeSingle();
  if(error) throw error;
  return data as ProveBlock|null;
}

async function readRelationships(admin:ReturnType<typeof adminClient>,id:string){
  if(!id) return [] as ProveRelationship[];
  const safe=id.replaceAll(",", "");
  const {data,error}=await admin.from("nayanet_brain_relationships")
    .select("relationship_id,source_id,target_id,relationship_type,epistemic_state,provenance")
    .eq("owner_id",OWNER_ID)
    .or("source_id.eq."+safe+",target_id.eq."+safe);
  if(error) throw error;
  return (data??[]) as ProveRelationship[];
}

async function insertReceipt(admin:ReturnType<typeof adminClient>,row:Record<string,unknown>){
  for(let attempt=0;attempt<8;attempt++){
    const {data:maxRows,error:maxError}=await admin.from("nayanet_execution_receipts").select("revision")
      .eq("user_id",OWNER_ID).eq("project_id",PROJECT_ID).order("revision",{ascending:false}).limit(1);
    if(maxError) throw maxError;
    const revision=Number(maxRows?.[0]?.revision??0)+1;
    const {data,error}=await admin.from("nayanet_execution_receipts").insert({...row,revision}).select("*").single();
    if(!error) return data;
    if(error.code!=="23505") throw error;
  }
  throw new Error("PROVE_RECEIPT_REVISION_CONFLICT");
}

function rejectCallerProofContent(body:Record<string,unknown>){
  const forbidden=["claim","evidence","provenance","block_id","intelligent_block_id","epistemic_state","proof","answer","lesson","intelligence","intelligence_content"];
  if(forbidden.some(k=>k in body)) throw new Error("CALLER_SUPPLIED_PROOF_CONTENT_FORBIDDEN");
}

async function inputsFromKnow(admin:ReturnType<typeof adminClient>,knowReceipt:any){
  const refs=Array.isArray(knowReceipt?.evidence?.authority_refs)?knowReceipt.evidence.authority_refs.map(String):[];
  const grant=refs.length===1?await readGrant(admin,refs[0]):null;
  const selectedId=String(knowReceipt?.evidence?.result?.selected_block_id??"");
  const block=selectedId?await readBlock(admin,selectedId):null;
  const relationships=selectedId?await readRelationships(admin,selectedId):[];
  return {grant,block,relationships};
}

Deno.serve(async(req)=>{
  try{
    if(req.method!=="POST") return json({ok:false,error:"METHOD_NOT_ALLOWED"},405);
    const {payload,workflowRef}=await authenticate(req);
    const body=await req.json().catch(()=>({})) as Record<string,unknown>;
    rejectCallerProofContent(body);
    const mode=String(body.mode??"");
    const admin=adminClient();

    if(mode==="assess"){
      const knowReceiptId=String(body.know_receipt_id??"").trim();
      if(!knowReceiptId) return json({ok:false,error:"KNOW_RECEIPT_ID_REQUIRED"},400);
      const knowReceipt=await readReceipt(admin,knowReceiptId) as ProveKnowReceipt|null;
      const {grant,block,relationships}=await inputsFromKnow(admin,knowReceipt);
      const assessment=assessKnowProof(OWNER_ID,NAYA_ID,knowReceipt,block,grant,relationships,new Date());
      const allowed=assessment.state==="ASSESSED" && assessment.epistemic_state==="SUPPORTED" && assessment.handoff_to==="NAYA-KERNEL-CONNECT";
      const receipt=await insertReceipt(admin,{
        user_id:OWNER_ID,project_id:PROJECT_ID,action:"prove_claim_assessment",status:allowed?"SUCCESS":"BLOCKED",
        expected_result:"PROVE derives a context-bound evidence claim from persisted KNOW output and canonical evidence without caller-supplied proof content or authority creation.",
        observed_result:assessment.epistemic_state+":"+(assessment.selected_block_id??"NONE"),
        evidence:{
          schema:"naya.prove.receipt.v1",node_id:"NAYA-KERNEL-PROVE",know_receipt_id:knowReceiptId,assessment,
          authority_ref:grant?.grant_id??null,caller_supplied_proof_content:false,proof_creates_authority:false,
          handoff_to:assessment.handoff_to,runtime_identity:"naya-node-oidc",runtime_jti:payload.jti??null,workflow_ref:workflowRef
        },
        learning:[]
      });
      return json({ok:true,status:allowed?"PROVE_SUPPORTED":"PROVE_NOT_PROMOTED",node_id:"NAYA-KERNEL-PROVE",assessment,receipt,
        handoff_to:assessment.handoff_to,proof_creates_authority:false});
    }

    if(mode==="inspect"){
      const proveReceiptId=String(body.prove_receipt_id??"").trim();
      if(!proveReceiptId) return json({ok:false,error:"PROVE_RECEIPT_ID_REQUIRED"},400);
      const proveReceipt=await readReceipt(admin,proveReceiptId);
      if(!proveReceipt || proveReceipt.action!=="prove_claim_assessment") return json({ok:false,error:"PROVE_RECEIPT_NOT_FOUND"},404);
      const knowReceiptId=String(proveReceipt.evidence?.know_receipt_id??"");
      const knowReceipt=await readReceipt(admin,knowReceiptId) as ProveKnowReceipt|null;
      const {grant,block,relationships}=await inputsFromKnow(admin,knowReceipt);
      // Recompute as-of the original assessment time so independent verification is
      // time-stable: it answers "was the assessment correct when made?", not "is the
      // KNOW receipt still fresh now?". Using wall-clock now here turns the 900s KNOW
      // freshness check into a time-bomb for any workflow that takes >15 min between
      // assess and inspect.
      const assessTime=proveReceipt.created_at?new Date(proveReceipt.created_at):new Date();
      const recomputed=assessKnowProof(OWNER_ID,NAYA_ID,knowReceipt,block,grant,relationships,assessTime);
      const recorded=proveReceipt.evidence?.assessment??{};
      const same=sameAssessment(recorded,recomputed);

      return json({
        ok:same,
        status:same?"PROVE_ASSESSMENT_VERIFIED":"PROVE_ASSESSMENT_MISMATCH",
        independent_verification:same,
        executor_claim_trusted_as_verification:false,
        assessment_integrity_state:same?"VERIFIED":"CONTRADICTED",
        claim_epistemic_state:recomputed.epistemic_state,
        node_id:"NAYA-KERNEL-PROVE",
        prove_receipt_id:proveReceiptId,
        know_receipt_id:knowReceiptId,
        recorded,
        recomputed,
        proof_creates_authority:false,
        verifier_identity:"fresh_github_actions_oidc",
        workflow_ref:workflowRef,
        token_jti:payload.jti??null,
        limitation:"Independent PROVE assessment recomputation is not outcome/causal verification; VERIFY remains a separate Node responsibility."
      },same?200:409);
    }

    return json({ok:false,error:"UNSUPPORTED_MODE"},400);
  }catch(e){
    return json({ok:false,error:String((e as Error)?.message??e)},400);
  }
});
