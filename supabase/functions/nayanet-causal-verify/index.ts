import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "npm:@supabase/supabase-js@2";

const U=Deno.env.get("SUPABASE_URL")!, A=Deno.env.get("SUPABASE_ANON_KEY")!, S=Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const admin=createClient(U,S);
const cors={"Access-Control-Allow-Origin":"*","Access-Control-Allow-Headers":"authorization,apikey,content-type","Access-Control-Allow-Methods":"POST,OPTIONS"};
const out=(x:unknown,s=200)=>new Response(JSON.stringify(x),{status:s,headers:{...cors,"content-type":"application/json","cache-control":"no-store"}});

const METHODS=new Set(["CONTROLLED_INTERVENTION","COUNTERFACTUAL_COMPARISON","MECHANISTIC_EVIDENCE","QUASI_EXPERIMENTAL","OBSERVATIONAL_ONLY"]);
const ASSESSMENTS=new Set(["CAUSAL_SUPPORTED","CAUSAL_INSUFFICIENT","CAUSAL_CONFLICTED"]);

Deno.serve(async req=>{
  if(req.method==="OPTIONS") return out({ok:true});
  if(req.method!=="POST") return out({ok:false,error:"METHOD_NOT_ALLOWED"},405);
  try{
    const auth=req.headers.get("authorization");
    if(!auth?.startsWith("Bearer ")) return out({ok:false,error:"AUTH_REQUIRED"},401);
    const client=createClient(U,A,{global:{headers:{Authorization:auth}}});
    const {data:userData}=await client.auth.getUser();
    if(!userData.user) return out({ok:false,error:"AUTH_INVALID"},401);
    const b=await req.json().catch(()=>({}));
    const receiptId=String(b.receipt_id||"");
    const intended=String(b.intended_change||"").trim();
    const observed=String(b.observed_change||"").trim();
    const method=String(b.causal_method||"").trim();
    const assessment=String(b.assessment||"").trim();
    const evidenceRefs=Array.isArray(b.evidence_refs)?b.evidence_refs.map(String):[];
    const limitations=Array.isArray(b.limitations)?b.limitations.map(String):[];
    const alternatives=Array.isArray(b.alternative_explanations)?b.alternative_explanations.map(String):[];
    if(!receiptId||!intended||!observed||!method||!assessment) return out({ok:false,error:"CAUSAL_REQUEST_INCOMPLETE"},400);
    if(!METHODS.has(method)) return out({ok:false,error:"CAUSAL_METHOD_INVALID"},400);
    if(!ASSESSMENTS.has(assessment)) return out({ok:false,error:"CAUSAL_ASSESSMENT_INVALID"},400);
    if(!evidenceRefs.length) return out({ok:false,error:"CAUSAL_EVIDENCE_REQUIRED"},400);
    if(assessment==="CAUSAL_SUPPORTED" && method==="OBSERVATIONAL_ONLY") return out({ok:false,error:"OBSERVATIONAL_EVIDENCE_CANNOT_ASSERT_CAUSATION"},400);
    if(assessment==="CAUSAL_SUPPORTED" && alternatives.length===0) return out({ok:false,error:"ALTERNATIVE_EXPLANATIONS_REQUIRED"},400);
    if(limitations.length===0) return out({ok:false,error:"CAUSAL_LIMITATIONS_REQUIRED"},400);
    const {data:receipt,error:re}=await admin.from("nayanet_execution_receipts").select("*").eq("id",receiptId).eq("user_id",userData.user.id).eq("project_id","NayaNET").maybeSingle();
    if(re) throw re;
    if(!receipt) return out({ok:false,error:"RECEIPT_NOT_FOUND_OR_NOT_OWNED"},404);
    const causal={
      schema:"NAYANET_CAUSAL_VERIFICATION_V1",
      receipt_id:receiptId,
      intended_change:intended,
      preconditions:Array.isArray(b.preconditions)?b.preconditions.map(String):[],
      action_ref:String(b.action_ref||receiptId),
      observed_change:observed,
      evidence_refs:evidenceRefs,
      causal_method:method,
      causal_assessment:assessment,
      alternative_explanations:alternatives,
      limitations,
      verified_at:new Date().toISOString()
    };
    const {data:op,error:oe}=await admin.from("nayanet_intelligence_operations").insert({
      user_id:userData.user.id,project_id:"NayaNET",operation:"causal_verify",status:"SUCCESS",
      input:b,output:causal,source_ref:receiptId,source_event_ids:evidenceRefs
    }).select("id").single();
    if(oe) throw oe;
    const ev=Array.isArray(receipt.evidence)?receipt.evidence:[];
    const evidence=[...ev,{causal_verification:causal,causal_operation_id:op.id}];
    const {data:updated,error:ue}=await admin.from("nayanet_execution_receipts").update({evidence}).eq("id",receiptId).eq("user_id",userData.user.id).select("*").single();
    if(ue) throw ue;
    return out({ok:true,schema:"NAYANET_CAUSAL_VERIFY_V1",operation_id:op.id,causal_verification:causal,receipt:updated});
  }catch(e){return out({ok:false,error:String(e?.message||e)},400)}
});