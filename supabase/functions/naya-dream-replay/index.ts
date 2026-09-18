import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
const cors={"Access-Control-Allow-Origin":"*","Access-Control-Allow-Headers":"authorization, x-client-info, apikey, content-type, x-idempotency-key","Access-Control-Allow-Methods":"POST, OPTIONS"};
const json=(body:unknown,status=200)=>new Response(JSON.stringify(body),{status,headers:{...cors,"Content-Type":"application/json"}});
Deno.serve(async(req)=>{
 if(req.method==="OPTIONS")return new Response("ok",{headers:cors});
 if(req.method!=="POST")return json({ok:false,error:"METHOD_NOT_ALLOWED"},405);
 try{
  const url=Deno.env.get("SUPABASE_URL"),anon=Deno.env.get("SUPABASE_ANON_KEY");
  if(!url||!anon)throw new Error("SUPABASE_RUNTIME_NOT_CONFIGURED");
  const authorization=req.headers.get("Authorization"); if(!authorization)return json({ok:false,error:"AUTHORIZATION_REQUIRED"},401);
  const supabase=createClient(url,anon,{global:{headers:{Authorization:authorization}}});
  const {data:authData,error:authError}=await supabase.auth.getUser();
  if(authError||!authData.user)return json({ok:false,error:"AUTHENTICATED_USER_REQUIRED"},401);
  const body=await req.json().catch(()=>({})),userId=authData.user.id;
  const projectId=typeof body?.project_id==="string"&&body.project_id.trim()?body.project_id.trim():"NayaNET";
  const idempotencyKey=(typeof body?.idempotency_key==="string"&&body.idempotency_key.trim()?body.idempotency_key.trim():null)||req.headers.get("x-idempotency-key");
  if(!idempotencyKey)return json({ok:false,error:"DREAM_IDEMPOTENCY_KEY_REQUIRED"},400);
  let eventQuery=supabase.from("nayanet_cognition_events").select("id,user_id,project_id,event_id,type,classification,title,content,source,status,actor,confidence,tags,parent_event_id,source_hash,schema_version,receipt_id,metadata,created_at").eq("user_id",userId).eq("project_id",projectId).order("created_at",{ascending:false}).limit(1);
  if(typeof body?.event_id==="string"&&body.event_id.trim())eventQuery=eventQuery.eq("event_id",body.event_id.trim());
  const {data:events,error:eventError}=await eventQuery; if(eventError)throw eventError;
  const event=events?.[0]; if(!event)return json({ok:false,error:"DREAM_SOURCE_EVENT_NOT_FOUND"},404);
  const {data:receipts,error:receiptError}=await supabase.from("nayanet_execution_receipts").select("id,user_id,project_id,revision,action,expected_result,observed_result,status,evidence,learning,created_at").eq("user_id",userId).eq("project_id",projectId).order("created_at",{ascending:false}).limit(20);
  if(receiptError)throw receiptError;
  const sourceReceipt=(receipts||[]).find(r=>r.evidence?.event_id===event.event_id)||(event.receipt_id?(receipts||[]).find(r=>r.id===event.receipt_id):null)||null;
  const valueInputs=sourceReceipt?.value&&typeof sourceReceipt.value==='object'?sourceReceipt.value:null;
  const n=(x)=>typeof x==='number'&&Number.isFinite(x)?x:null;
  const benefit=n(valueInputs?.benefit),harm=n(valueInputs?.harm),cost=n(valueInputs?.cost),risk=n(valueInputs?.risk_adjusted_loss);
  const valueComplete=[benefit,harm,cost,risk].every(x=>x!==null);
  const responsibleValue=valueComplete?benefit-harm-cost-risk:null;
  const verifiedValue=valueComplete&&valueInputs?.verified===true?responsibleValue:null;
  const taskScore=sourceReceipt?.status==='SUCCESS'&&sourceReceipt?.evidence?.some(x=>x?.receiver_retrieved_by)?1:sourceReceipt?.status==='SUCCESS'?0.5:0;
  const history=[{event_id:event.event_id,classification:event.classification,title:event.title,content:event.content,source:event.source,status:event.status,confidence:event.confidence,tags:event.tags,parent_event_id:event.parent_event_id,source_hash:event.source_hash,schema_version:event.schema_version,metadata:event.metadata,created_at:event.created_at},...(sourceReceipt?[{receipt_id:sourceReceipt.id,action:sourceReceipt.action,expected_result:sourceReceipt.expected_result,observed_result:sourceReceipt.observed_result,status:sourceReceipt.status,evidence:sourceReceipt.evidence,learning:sourceReceipt.learning,created_at:sourceReceipt.created_at}]:[])];
  const worldSnapshot={schema:"nayanet.dream.world.p0.v1",source:"nayanet_cognition_events + nayanet_execution_receipts",source_event_id:event.event_id,source_receipt_id:sourceReceipt?.id??null,captured_at:new Date().toISOString(),immutable_source_projection:history};
  const baseline={strategy:"HISTORY_ONLY_V1",source_event_count:1,source_receipt_count:sourceReceipt?1:0,context_items:history.length,authority_changed:false,execution_performed:false};
  const counterfactual={strategy:"HISTORY_PLUS_VERIFIED_RECEIPT_V1",source_event_count:1,source_receipt_count:sourceReceipt?1:0,context_items:history.length,authority_changed:false,execution_performed:false,additional_context:sourceReceipt?["verified_execution_receipt"]:[]};
  const replayOutput={schema:"nayanet.dream.replay.p0.v1",disposition:"SIMULATED",baseline,counterfactual,delta:{context_items:counterfactual.context_items-baseline.context_items,receipt_recovered:Boolean(sourceReceipt)},score_contract:{schema:"NAYANET_DREAM_SCORE_V1",task_score:{baseline:taskScore,counterfactual:taskScore,delta:0,method:"SUCCESS=1; SUCCESS without verified receiver observation=0.5; otherwise=0"},responsible_value:{inputs:{benefit,harm,cost,risk_adjusted_loss:risk},baseline:responsibleValue,counterfactual:responsibleValue,delta:0,formula:"benefit - harm - cost - risk_adjusted_loss",verified_value:verifiedValue,verification:valueComplete&&valueInputs?.verified===true?"VERIFIED":"NOT_VERIFIED"},policy_improvement:"NOT_PROVEN"},score_separation:{task_score:taskScore,responsible_value:verifiedValue,authority:"unchanged",truth:"not_inferred",verification:valueComplete&&valueInputs?.verified===true?"source_receipt_value_verified":"source_receipt_only"}};
  const {data:inserted,error:insertError}=await supabase.from("nayanet_dream_replays").insert({user_id:userId,project_id:projectId,source_event_id:event.event_id,source_receipt_id:sourceReceipt?.id??null,policy_version:"DREAM-P0-V1",world_snapshot:worldSnapshot,replay_input:{requested_event_id:body?.event_id??null,strategy:"HISTORY_PLUS_VERIFIED_RECEIPT_V1"},replay_output:replayOutput,status:"SIMULATED",verification:{source_history_read:true,source_history_mutated:false,execution_performed:false,authority_granted:false,production_policy_changed:false,deterministic:true},idempotency_key:idempotencyKey}).select("id,project_id,source_event_id,source_receipt_id,policy_version,status,replay_output,verification,created_at").single();
  if(insertError){if(insertError.code==="23505"){const {data:existing}=await supabase.from("nayanet_dream_replays").select("id,project_id,source_event_id,source_receipt_id,policy_version,status,replay_output,verification,created_at").eq("user_id",userId).eq("idempotency_key",idempotencyKey).single();return json({ok:true,replay:existing,idempotent:true});}throw insertError;}
  return json({ok:true,replay:inserted,idempotent:false});
 }catch(error){console.error(error);return json({ok:false,error:"DREAM_REPLAY_FAILED",detail:String(error)},500)}
});