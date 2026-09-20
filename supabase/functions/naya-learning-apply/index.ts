import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
const cors={"Access-Control-Allow-Origin":"*","Access-Control-Allow-Headers":"authorization, x-client-info, apikey, content-type","Access-Control-Allow-Methods":"POST, OPTIONS"};
const json=(body:unknown,status=200)=>new Response(JSON.stringify(body),{status,headers:{...cors,"Content-Type":"application/json"}});
const rank=(v:string)=>["E0_EXPOSED","E1_UNDERSTANDS","E2_CAN_DO","E3_INDEPENDENT","E4_TRANSFER","E5_CAN_TEACH","E6_RETAINED","E7_MASTERED"].indexOf(v);
Deno.serve(async(req)=>{
 if(req.method==="OPTIONS")return new Response("ok",{headers:cors});
 if(req.method!=="POST")return json({ok:false,error:"METHOD_NOT_ALLOWED"},405);
 try{
  const url=Deno.env.get("SUPABASE_URL"),anon=Deno.env.get("SUPABASE_ANON_KEY"),authorization=req.headers.get("Authorization");
  if(!url||!anon)return json({ok:false,error:"RUNTIME_NOT_CONFIGURED"},500);
  if(!authorization)return json({ok:false,error:"AUTHORIZATION_REQUIRED"},401);
  const supabase=createClient(url,anon,{global:{headers:{Authorization:authorization}}});
  const {data:au,error:ae}=await supabase.auth.getUser();if(ae||!au.user)return json({ok:false,error:"AUTHENTICATED_USER_REQUIRED"},401);
  const userId=au.user.id,body=await req.json().catch(()=>({})),evidenceId=String(body?.evidence_id||"").trim();if(!evidenceId)return json({ok:false,error:"EVIDENCE_ID_REQUIRED"},400);
  const {data:e,error:ee}=await supabase.from("learning_evidence").select("*").eq("id",evidenceId).eq("member_id",userId).single();if(ee||!e)return json({ok:false,error:"LEARNING_EVIDENCE_NOT_FOUND"},404);
  if(e.status!=="ACTIVE")return json({ok:false,error:"LEARNING_EVIDENCE_NOT_ACTIVE"},409);
  if(rank(e.level)<rank("E1_UNDERSTANDS"))return json({ok:false,error:"LEARNING_LEVEL_TOO_LOW"},409);
  let replay=null;
  if(body?.replay_id){
   const {data:r,error:re}=await supabase.from("nayanet_dream_replays").select("*").eq("id",String(body.replay_id)).eq("user_id",userId).single();
   if(re||!r)return json({ok:false,error:"DREAM_REPLAY_NOT_FOUND"},404);
   if(r.status!=="SIMULATED"&&r.status!=="VERIFIED")return json({ok:false,error:"DREAM_REPLAY_NOT_USABLE"},409);
   if(r.source_event_id!==e.source_event_id)return json({ok:false,error:"LEARNING_REPLAY_LINEAGE_MISMATCH"},409);
   replay=r;
  }
  const {data:existing}=await supabase.from("learner_states").select("*").eq("member_id",userId).maybeSingle();
  const prev=existing||{member_id:userId,goals:[],active_target_ids:[],demonstrated_capability_ids:[],current_evidence_by_target:{},unresolved_gap_ids:[],misconception_ids:[],successful_teaching_approach_ids:[],version:0};
  const target=String(e.target_id);
  const current={...(prev.current_evidence_by_target||{}),[target]:{evidence_id:e.id,level:e.level,claim:e.claim,source_event_id:e.source_event_id,verification_method:e.verification_method,updated_at:new Date().toISOString(),replay_id:replay?.id||null}};
  const targets=Array.from(new Set([...(prev.active_target_ids||[]),target]));
  const patch={member_id:userId,goals:prev.goals||[],active_target_ids:targets,demonstrated_capability_ids:prev.demonstrated_capability_ids||[],current_evidence_by_target:current,unresolved_gap_ids:prev.unresolved_gap_ids||[],misconception_ids:prev.misconception_ids||[],successful_teaching_approach_ids:prev.successful_teaching_approach_ids||[],last_meaningful_learning_at:new Date().toISOString(),version:Number(prev.version||0)+1,updated_at:new Date().toISOString()};
  const {data:state,error:se}=await supabase.from("learner_states").upsert(patch,{onConflict:"member_id"}).select("*").single();if(se)throw se;
  const cognition={event_id:"learning-apply:"+e.id,type:"learning_application",classification:"verified_learning",title:"Verified learning applied",content:e.claim,source:"naya-learning-apply",status:"active",actor:"human",confidence:1,tags:["learning","verified","smart-ledger"],source_hash:"learning:"+e.id,schema_version:"1.0.0",metadata:{learning_evidence_id:e.id,target_id:target,learner_state_version:state.version,replay_id:replay?.id||null}};
  const learningPayload=[{target_id:target,level:e.level,status:"APPLIED",learning_evidence_id:e.id,verification_method:e.verification_method,observed_value:e.observed_value}];
  const {data:ce,error:cerr}=await supabase.rpc("nayanet_record_cognition_event",{p_project_id:"NayaNET",p_event:cognition,p_action:"apply_verified_learning",p_expected_result:"Verified learning becomes retrievable Superbrain intelligence",p_observed_result:"Learner state updated and cognition event persisted",p_learning:learningPayload});
  if(cerr)return json({ok:false,error:"SUPERBRAIN_LEARNING_COMMIT_FAILED",detail:cerr.message,learner_state_version:state.version},500);
  return json({ok:true,learning:{evidence_id:e.id,target_id:target,level:e.level,learner_state_version:state.version,replay_id:replay?.id||null,authority_changed:false,production_policy_changed:false},superbrain:{cognition_event_id:ce?.id||ce?.event_id||null},learner_state:state});
 }catch(error){console.error(error);return json({ok:false,error:"LEARNING_APPLY_FAILED",detail:String(error)},500)}
});