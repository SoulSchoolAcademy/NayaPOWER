// verification redeploy: source synchronized with live Edge Function v8
import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2.57.0";
type SendBody={operation?: "send"|"verify";recipient_user_id?:string;message_id?:string;body?:string;subject?:string;kind?:"direct"|"room"|"group"|"list";idempotency_key?:string;project_id?:string;policy_id?:string;experiment_case_id?:string;policy_input_hash?:string;policy_decision_hash?:string;authority_grant_id?:string;request_id?:string};
const cors={"access-control-allow-origin":"https://sparkling-shape-7ae5.smartnetpodcast.workers.dev","access-control-allow-methods":"POST, OPTIONS","access-control-allow-headers":"authorization, apikey, content-type, x-idempotency-key","vary":"Origin"};
const json=(payload:unknown,status=200)=>new Response(JSON.stringify(payload),{status,headers:{"content-type":"application/json","cache-control":"no-store",...cors}});
const inputRequestId=(req:Request)=>req.headers.get("x-request-id")||crypto.randomUUID();
Deno.serve(async(req)=>{
 if(req.method==="OPTIONS")return new Response(null,{status:204,headers:cors});
 if(req.method!=="POST")return json({ok:false,error:"METHOD_NOT_ALLOWED"},405);
 const authHeader=req.headers.get("authorization"); if(!authHeader?.startsWith("Bearer "))return json({ok:false,error:"AUTH_REQUIRED"},401);
 const url=Deno.env.get("SUPABASE_URL")!,anon=Deno.env.get("SUPABASE_ANON_KEY")!,service=Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
 const userClient=createClient(url,anon,{global:{headers:{Authorization:authHeader}}}),admin=createClient(url,service);
 const {data:userData,error:userError}=await userClient.auth.getUser(); if(userError||!userData.user)return json({ok:false,error:"AUTH_INVALID"},401);
 const actorId=userData.user.id;
 let input:SendBody; try{input=await req.json()}catch{return json({ok:false,error:"INVALID_JSON"},400)}
 const requestId=inputRequestId(req);
 if(input.operation==="verify"){
   if(!input.message_id)return json({ok:false,error:"MESSAGE_ID_REQUIRED"},400);
   const {data:message,error:messageError}=await admin.from("v7_mail_messages").select("id,thread_id,sender_id,metadata").eq("id",input.message_id).maybeSingle();
   if(messageError)return json({ok:false,error:"MESSAGE_LOOKUP_FAILED",detail:messageError.message},500);
   if(!message)return json({ok:false,error:"MESSAGE_NOT_FOUND"},404);
   const {data:membership}=await admin.from("v7_mail_members").select("user_id").eq("thread_id",message.thread_id).eq("user_id",actorId).maybeSingle();
   if(!membership)return json({ok:false,error:"RECEIVER_NOT_AUTHORIZED"},403);
   const receiptId=message.metadata?.execution_receipt_id;
   if(!receiptId)return json({ok:false,error:"RECEIPT_NOT_LINKED"},409);
   const {data:receipt,error:receiptError}=await admin.from("nayanet_execution_receipts").select("id,status,evidence,value,learning,experiment_case_id").eq("id",receiptId).maybeSingle();
   if(receiptError||!receipt)return json({ok:false,error:"RECEIPT_NOT_FOUND"},404);
   const {data:outcome,error:outcomeError}=await userClient.rpc("nayanet_record_smart_mail_outcome",{p_receipt_id:receiptId,p_message_id:message.id,p_experiment_case_id:receipt.experiment_case_id??null});
   if(outcomeError)return json({ok:false,error:"OUTCOME_RECORD_FAILED",detail:outcomeError.message},409);
   const {data:sourceCognition}=await admin.from("nayanet_cognition_events").select("id,event_id").eq("receipt_id",receiptId).eq("user_id",message.sender_id).order("created_at",{ascending:false}).limit(1).maybeSingle();
   const sourceEventId=sourceCognition?.event_id??receiptId;
   const {data:existingLearning,error:existingLearningError}=await admin.from("learning_evidence").select("id").eq("member_id",message.sender_id).eq("source_event_id",sourceEventId).limit(1).maybeSingle();
   if(existingLearningError)return json({ok:false,error:"LEARNING_EVIDENCE_LOOKUP_FAILED",detail:existingLearningError.message},500);
   let learningEvidenceId=existingLearning?.id??null;
   if(!learningEvidenceId){
     const learningStatement=Array.isArray(receipt.learning)&&receipt.learning[0]?.statement?String(receipt.learning[0].statement):"Verified Smart Mail execution produced an independently receiver-verified outcome that is reusable intelligence.";
     const {data:learningEvidence,error:learningError}=await admin.from("learning_evidence").insert({
       member_id:message.sender_id,target_id:receipt.experiment_case_id??("smart-mail:"+receiptId),level:"E1_UNDERSTANDS",
       provenance:"authenticated receiver verification + execution receipt + cognition/Ledger lineage",status:"ACTIVE",claim:learningStatement,
       observed_value:{receipt_id:receiptId,outcome_id:outcome?.outcome_id??null,message_id:message.id,thread_id:message.thread_id,receiver_id:actorId,verified_value:outcome?.verified_value??null},
       verification_method:"authenticated receiver verification",source_event_id:sourceEventId
     }).select("id").single();
     if(learningError)return json({ok:false,error:"LEARNING_EVIDENCE_CREATE_FAILED",detail:learningError.message},500);
     learningEvidenceId=learningEvidence.id;
   }
   await admin.from("v7_mail_messages").update({metadata:{...message.metadata,receiver_verified_at:new Date().toISOString(),receiver_verified_by:actorId,outcome_id:outcome?.outcome_id??null,learning_evidence_id:learningEvidenceId}}).eq("id",message.id);
   return json({ok:true,status:"VERIFIED",message_id:message.id,thread_id:message.thread_id,execution_receipt_id:receiptId,receiver_id:actorId,authority_changed:false,outcome,learning_evidence_id:learningEvidenceId});
 }
 if(!input?.recipient_user_id||!input?.body||!input?.idempotency_key)return json({ok:false,error:"RECIPIENT_BODY_IDEMPOTENCY_REQUIRED"},400);
 if(input.recipient_user_id===actorId)return json({ok:false,error:"SELF_RECIPIENT_NOT_ALLOWED"},400);
 if(input.body.length>10000)return json({ok:false,error:"BODY_TOO_LARGE"},400);
 const {data:recipient}=await admin.auth.admin.getUserById(input.recipient_user_id); if(!recipient?.user)return json({ok:false,error:"RECIPIENT_NOT_FOUND"},404);
 if(!input.authority_grant_id)return json({ok:false,error:"AUTHORITY_GRANT_ID_REQUIRED"},403);
 const {data:validated,error:validationError}=await userClient.rpc("nayanet_validate_authority_grant",{p_grant_id:input.authority_grant_id,p_action:"smart_mail_send",p_target:input.recipient_user_id});
 if(validationError||validated?.status!=="AUTHORIZED")return json({ok:false,error:"AUTHORITY_GRANT_VALIDATION_FAILED",detail:validationError?.message??validated},403);
 const inputRequestId=(req:Request)=>req.headers.get("x-request-id")||crypto.randomUUID();
 const rpcName=(input.policy_id||input.experiment_case_id||input.policy_input_hash||input.policy_decision_hash)?"nayanet_send_smart_mail_policy_authorized":"nayanet_send_smart_mail_authorized";
 const rpcArgs=(input.policy_id||input.experiment_case_id||input.policy_input_hash||input.policy_decision_hash)
   ? {p_sender_id:actorId,p_receiver_id:input.recipient_user_id,p_body:input.body,p_subject:input.subject??"NayaNET P0 communication proof",p_kind:input.kind??"direct",p_idempotency_key:input.idempotency_key,p_project_id:input.project_id??"NayaNET",p_request_id:requestId,p_policy_id:input.policy_id,p_experiment_case_id:input.experiment_case_id,p_policy_input_hash:input.policy_input_hash,p_policy_decision_hash:input.policy_decision_hash,p_authority_grant_id:input.authority_grant_id}
   : {p_sender_id:actorId,p_receiver_id:input.recipient_user_id,p_body:input.body,p_subject:input.subject??"NayaNET P0 communication proof",p_kind:input.kind??"direct",p_idempotency_key:input.idempotency_key,p_project_id:input.project_id??"NayaNET",p_request_id:requestId,p_authority_grant_id:input.authority_grant_id};
 const {data:result,error}=await userClient.rpc(rpcName,rpcArgs);
 if(error)return json({ok:false,error:"SMART_MAIL_TRANSACTION_FAILED",detail:error.message},500);
 if(result?.status==="CREATED" && result?.execution_receipt_id){
   const receiptId=String(result.execution_receipt_id);
   const eventId="SE-"+new Date().toISOString().replace(/[-:TZ.]/g,"").slice(0,14)+"-"+crypto.randomUUID().slice(0,12);
   const {error:activityError}=await admin.from("nayanet_team_activity").insert({
     event_id:eventId,effective_at:new Date().toISOString(),session_id:"SMART-MAIL-"+receiptId,claim_id:"SMART-MAIL-"+receiptId,action_id:"smart_mail_send",
     decision_id:input.policy_decision_hash?"POLICY-"+input.policy_decision_hash:"AUTHORITY-"+input.authority_grant_id,authority_id:input.authority_grant_id,actor_id:actorId,run_id:receiptId,
     subject:"Consequential Smart Mail execution",summary:"Smart Mail execution completed and produced a durable Team Naya Activity receipt.",
     evidence:[receiptId,input.policy_input_hash??"policy-input-hash-not-supplied",input.policy_decision_hash??"policy-decision-hash-not-supplied"],
     next_action:"Continue from the verified execution receipt.",successor:"NEXT-NAYA-FROM-"+receiptId,execution_receipt_id:receiptId
   });
   if(activityError)return json({ok:false,error:"ACTIVITY_WRITE_FAILED",detail:activityError.message,execution_receipt_id:receiptId},500);
 }
 return json({ok:true,...result,authority_grant_id:input.authority_grant_id});
});