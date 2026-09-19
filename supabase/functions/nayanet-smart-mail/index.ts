// verification redeploy: source synchronized with live Edge Function v8
import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2.57.0";
type SendBody={operation?: "send"|"verify";recipient_user_id?:string;message_id?:string;body?:string;subject?:string;kind?:"direct"|"room"|"group"|"list";idempotency_key?:string;project_id?:string;policy_id?:string;experiment_case_id?:string;policy_input_hash?:string;policy_decision_hash?:string};
const json=(payload:unknown,status=200)=>new Response(JSON.stringify(payload),{status,headers:{"content-type":"application/json","cache-control":"no-store"}});
Deno.serve(async(req)=>{
 if(req.method!=="POST")return json({ok:false,error:"METHOD_NOT_ALLOWED"},405);
 const authHeader=req.headers.get("authorization"); if(!authHeader?.startsWith("Bearer "))return json({ok:false,error:"AUTH_REQUIRED"},401);
 const url=Deno.env.get("SUPABASE_URL")!,anon=Deno.env.get("SUPABASE_ANON_KEY")!,service=Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
 const userClient=createClient(url,anon,{global:{headers:{Authorization:authHeader}}}),admin=createClient(url,service);
 const {data:userData,error:userError}=await userClient.auth.getUser(); if(userError||!userData.user)return json({ok:false,error:"AUTH_INVALID"},401);
 const actorId=userData.user.id;
 let input:SendBody; try{input=await req.json()}catch{return json({ok:false,error:"INVALID_JSON"},400)}
 if(input.operation==="verify"){
   if(!input.message_id)return json({ok:false,error:"MESSAGE_ID_REQUIRED"},400);
   const {data:message,error:messageError}=await admin.from("v7_mail_messages").select("id,thread_id,sender_id,metadata").eq("id",input.message_id).maybeSingle();
   if(messageError)return json({ok:false,error:"MESSAGE_LOOKUP_FAILED",detail:messageError.message},500);
   if(!message)return json({ok:false,error:"MESSAGE_NOT_FOUND"},404);
   const {data:membership}=await admin.from("v7_mail_members").select("user_id").eq("thread_id",message.thread_id).eq("user_id",actorId).maybeSingle();
   if(!membership)return json({ok:false,error:"RECEIVER_NOT_AUTHORIZED"},403);
   const receiptId=message.metadata?.execution_receipt_id;
   if(!receiptId)return json({ok:false,error:"RECEIPT_NOT_LINKED"},409);
   const {data:receipt,error:receiptError}=await admin.from("nayanet_execution_receipts").select("id,status,evidence,value").eq("id",receiptId).maybeSingle();
   if(receiptError||!receipt)return json({ok:false,error:"RECEIPT_NOT_FOUND"},404);
   const evidence=[...(receipt.evidence||[])];
   const already=evidence.some((x:any)=>x?.receiver_retrieved_by===actorId&&x?.message_id===message.id);
   if(!already)evidence.push({receiver_retrieved_by:actorId,message_id:message.id,receiver_retrieved_at:new Date().toISOString()});
   const priorValue=receipt.value&&typeof receipt.value==="object"?receipt.value:{};
   const benefit=typeof priorValue.benefit==="number"?priorValue.benefit:0;
   const harm=typeof priorValue.harm==="number"?priorValue.harm:0;
   const cost=typeof priorValue.cost==="number"?priorValue.cost:0;
   const risk=typeof priorValue.risk_adjusted_loss==="number"?priorValue.risk_adjusted_loss:0;
   const verifiedValue=benefit-harm-cost-risk;
   const {error:updateError}=await admin.from("nayanet_execution_receipts").update({evidence,value:{...priorValue,verified:true,verification_method:"authenticated receiver retrieval",verified_value:verifiedValue}}).eq("id",receiptId);
   if(updateError)return json({ok:false,error:"RECEIPT_UPDATE_FAILED",detail:updateError.message},500);
   await admin.from("v7_mail_messages").update({metadata:{...message.metadata,receiver_verified_at:new Date().toISOString(),receiver_verified_by:actorId}}).eq("id",message.id);
   return json({ok:true,status:"VERIFIED",message_id:message.id,thread_id:message.thread_id,execution_receipt_id:receiptId,receiver_id:actorId,authority_changed:false});
 }
 if(!input?.recipient_user_id||!input?.body||!input?.idempotency_key)return json({ok:false,error:"RECIPIENT_BODY_IDEMPOTENCY_REQUIRED"},400);
 if(input.recipient_user_id===actorId)return json({ok:false,error:"SELF_RECIPIENT_NOT_ALLOWED"},400);
 if(input.body.length>10000)return json({ok:false,error:"BODY_TOO_LARGE"},400);
 const {data:recipient}=await admin.auth.admin.getUserById(input.recipient_user_id); if(!recipient?.user)return json({ok:false,error:"RECIPIENT_NOT_FOUND"},404);
 const sourceEventId=`human:smart-mail-send:${input.idempotency_key}`;
 const {data:existingGrant,error:existingGrantError}=await userClient.from("nayanet_authority_grants").select("*").eq("issuer_id",actorId).eq("source_event_id",sourceEventId).maybeSingle(); if(existingGrantError)return json({ok:false,error:"AUTHORITY_GRANT_LOOKUP_FAILED",detail:existingGrantError.message},403); const {data:grant,error:grantError}=existingGrant?{data:existingGrant,error:null}:await userClient.rpc("nayanet_issue_authority_grant",{p_subject_id:actorId,p_source_event_id:sourceEventId,p_mission_id:"NayaNET-SMART-MAIL",p_scope:{target:input.recipient_user_id,project_id:input.project_id??"NayaNET"},p_actions:["smart_mail_send"],p_constraints:{kind:input.kind??"direct",no_model_authority:true},p_evidence:{human_action:"explicit authenticated Smart Mail send request",idempotency_key:input.idempotency_key,recipient_user_id:input.recipient_user_id},p_expires_at:null,p_parent_authority:null});
 if(grantError||!grant?.grant_id)return json({ok:false,error:"AUTHORITY_GRANT_ISSUANCE_FAILED",detail:grantError?.message??"GRANT_NOT_RETURNED"},403);
 const {data:validated, error:validationError}=await userClient.rpc("nayanet_validate_authority_grant",{p_grant_id:grant.grant_id,p_action:"smart_mail_send",p_target:input.recipient_user_id});
 if(validationError||validated?.status!=="AUTHORIZED")return json({ok:false,error:"AUTHORITY_GRANT_VALIDATION_FAILED",detail:validationError?.message??validated},403);
 const {data:result,error}=await userClient.rpc("nayanet_send_smart_mail_authorized",{p_sender_id:actorId,p_receiver_id:input.recipient_user_id,p_body:input.body,p_subject:input.subject??"NayaNET P0 communication proof",p_kind:input.kind??"direct",p_idempotency_key:input.idempotency_key,p_project_id:input.project_id??"NayaNET",p_policy_id:input.policy_id??null,p_experiment_case_id:input.experiment_case_id??null,p_policy_input_hash:input.policy_input_hash??null,p_policy_decision_hash:input.policy_decision_hash??null,p_authority_grant_id:grant.grant_id});
 if(error)return json({ok:false,error:"SMART_MAIL_TRANSACTION_FAILED",detail:error.message},500);
 return json({ok:true,...result});
});