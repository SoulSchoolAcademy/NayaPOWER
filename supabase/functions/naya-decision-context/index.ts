import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
const cors={"Access-Control-Allow-Origin":"*","Access-Control-Allow-Headers":"authorization, x-client-info, apikey, content-type","Access-Control-Allow-Methods":"POST, OPTIONS"};
const json=(body:unknown,status=200)=>new Response(JSON.stringify(body),{status,headers:{...cors,"Content-Type":"application/json"}});
Deno.serve(async(req)=>{
 if(req.method==="OPTIONS")return new Response("ok",{headers:cors});
 if(req.method!=="POST")return json({ok:false,error:"METHOD_NOT_ALLOWED"},405);
 try{
  const url=Deno.env.get("SUPABASE_URL"),anon=Deno.env.get("SUPABASE_ANON_KEY"),authorization=req.headers.get("Authorization");
  if(!url||!anon)return json({ok:false,error:"RUNTIME_NOT_CONFIGURED"},500);
  if(!authorization)return json({ok:false,error:"AUTHORIZATION_REQUIRED"},401);
  const supabase=createClient(url,anon,{global:{headers:{Authorization:authorization}}});
  const {data:au,error:ae}=await supabase.auth.getUser(); if(ae||!au.user)return json({ok:false,error:"AUTHENTICATED_USER_REQUIRED"},401);
  const userId=au.user.id,body=await req.json().catch(()=>({})),targetId=String(body?.target_id||"").trim();
  if(!targetId)return json({ok:false,error:"TARGET_ID_REQUIRED"},400);
  const {data:state,error:se}=await supabase.from("learner_states").select("*").eq("member_id",userId).maybeSingle(); if(se)throw se;
  const pointer=state?.current_evidence_by_target?.[targetId]||null;
  let evidence=null,replay=null;
  if(pointer?.evidence_id){
    const {data:e,error:ee}=await supabase.from("learning_evidence").select("*").eq("id",pointer.evidence_id).eq("member_id",userId).single(); if(!ee)evidence=e;
    if(pointer.replay_id){const {data:r}=await supabase.from("nayanet_dream_replays").select("id,source_event_id,policy_version,status,verification,replay_output,created_at").eq("id",pointer.replay_id).eq("user_id",userId).maybeSingle(); replay=r||null;}
  }
  const influenced=!!(evidence&&evidence.status==="ACTIVE");
  const decision=influenced?"USE_VERIFIED_LEARNING_CONTEXT":"NO_LEARNING_INFLUENCE";
  return json({ok:true,decision:{decision,target_id:targetId,influenced,reason:influenced?"Active learning evidence is present in the canonical learner state.":"No active learner-state evidence was found.",context:{evidence_id:evidence?.id||null,level:evidence?.level||null,claim:evidence?.claim||null,source_event_id:evidence?.source_event_id||null,replay_id:replay?.id||null,policy_version:replay?.policy_version||null},authority:{changed:false,granted:false,source:"existing governance boundary"},verification:{evidence_status:evidence?.status||null,replay_status:replay?.status||null,replay_verification:replay?.verification||null}},learner_state_version:state?.version||0});
 }catch(error){console.error(error);return json({ok:false,error:"DECISION_CONTEXT_FAILED",detail:String(error)},500)}
});