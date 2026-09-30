import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "npm:@supabase/supabase-js@2";

const U = Deno.env.get("SUPABASE_URL")!;
const A = Deno.env.get("SUPABASE_ANON_KEY")!;
const cors = {"Access-Control-Allow-Origin":"*","Access-Control-Allow-Headers":"authorization, x-client-info, apikey, content-type","Access-Control-Allow-Methods":"POST, OPTIONS"};
const json=(body:unknown,status=200)=>new Response(JSON.stringify(body),{status,headers:{...cors,"Content-Type":"application/json","Cache-Control":"no-store"}});

Deno.serve(async(req)=>{
  if(req.method==="OPTIONS") return json({ok:true});
  if(req.method!=="POST") return json({ok:false,error:"METHOD_NOT_ALLOWED"},405);
  try{
    const authorization=req.headers.get("Authorization");
    if(!authorization) return json({ok:false,error:"AUTHORIZATION_REQUIRED"},401);
    const supabase=createClient(U,A,{global:{headers:{Authorization:authorization}}});
    const {data:auth,error:authError}=await supabase.auth.getUser();
    if(authError||!auth.user) return json({ok:false,error:"AUTHENTICATED_USER_REQUIRED"},401);
    const body=await req.json().catch(()=>({}));
    const targetId=String(body?.target_id||"").trim();
    if(!targetId) return json({ok:false,error:"TARGET_ID_REQUIRED"},400);
    const {data:evidence,error:evidenceError}=await supabase
      .from("learning_evidence")
      .select("id,target_id,level,status,claim,observed_value,source_event_id,verification_method,provenance,created_at")
      .eq("member_id",auth.user.id).eq("target_id",targetId).eq("status","ACTIVE")
      .order("created_at",{ascending:false}).limit(1).maybeSingle();
    if(evidenceError) throw evidenceError;
    const influenced=!!evidence;
    const decision=influenced?"USE_VERIFIED_LEARNING_CONTEXT":"NO_LEARNING_INFLUENCE";
    return json({ok:true,decision:{
      decision,target_id:targetId,influenced,
      reason:influenced?"Active learning evidence is present in the canonical learner evidence boundary.":"No active learning evidence was found for this target.",
      context:{evidence_id:evidence?.id||null,level:evidence?.level||null,claim:evidence?.claim||null,source_event_id:evidence?.source_event_id||null,observed_value:evidence?.observed_value||null,verification_method:evidence?.verification_method||null,provenance:evidence?.provenance||null},
      authority:{changed:false,granted:false,source:"existing governance boundary"},
      verification:{evidence_status:evidence?.status||null},
      continuity:{grounded:influenced,source:influenced?"learning_evidence":"no_learning_evidence",next_step:influenced?"APPLY_VERIFIED_LEARNING_CONTEXT":"RETRIEVE_VERIFIED_LEARNING_BEFORE_CONTINUATION"}
    }});
  }catch(error){return json({ok:false,error:"DECISION_CONTEXT_FAILED",detail:String(error)},500);}
});