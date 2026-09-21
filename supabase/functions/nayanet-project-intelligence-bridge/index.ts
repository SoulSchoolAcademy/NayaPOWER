import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "npm:@supabase/supabase-js@2";
import { createRemoteJWKSet, jwtVerify } from "npm:jose";

const supabase=createClient(Deno.env.get("SUPABASE_URL")!,Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
const jwks=createRemoteJWKSet(new URL("https://token.actions.githubusercontent.com/.well-known/jwks"));
const AUDIENCE="nayanet-project-intelligence-bridge",ISSUER="https://token.actions.githubusercontent.com",REPOSITORY="SoulSchoolAcademy/NayaPOWER";
const fail=(status:number,code:string,detail?:string)=>new Response(JSON.stringify({status:"REJECTED",code,detail}),{status,headers:{"content-type":"application/json"}});
Deno.serve(async req=>{
 if(req.method!=="POST")return fail(405,"METHOD_NOT_ALLOWED");
 const auth=req.headers.get("authorization")||"";if(!auth.startsWith("Bearer "))return fail(401,"UNAUTHORIZED");
 try{const {payload}=await jwtVerify(auth.slice(7),jwks,{issuer:ISSUER,audience:AUDIENCE});if(payload.repository!==REPOSITORY)return fail(403,"REPOSITORY_NOT_AUTHORIZED");if(payload.ref!=="refs/heads/main")return fail(403,"REF_NOT_AUTHORIZED");if(payload.repository_visibility!=="public")return fail(403,"VISIBILITY_NOT_AUTHORIZED");}catch(e){return fail(401,"OIDC_INVALID",String(e))}
 let packet:any;try{packet=await req.json()}catch{return fail(400,"INVALID_JSON")}
 const required=["protocol","packet_id","project_id","source_ref","content_hash","operating_context","intelligence","provenance","privacy","idempotency_key","owner_id"];
 const missing=required.filter(k=>packet?.[k]===undefined||packet?.[k]===null||packet?.[k]==="");if(missing.length)return fail(400,"INVALID_PACKET",missing.join(","));
 if(packet.protocol!=="NAYANET_PROJECT_INTELLIGENCE_BRIDGE_V1")return fail(400,"PROTOCOL_MISMATCH");if(packet.project_id!=="NayaNET")return fail(400,"PROJECT_MISMATCH");
 if(packet.sender?.repository!==REPOSITORY)return fail(403,"SENDER_MISMATCH");if(packet.receiver?.canonical_source!=="NAYANET/HUB/index.html")return fail(403,"RECEIVER_MISMATCH");if(packet.privacy?.default_visibility!=="PRIVATE")return fail(403,"PRIVACY_POLICY_REQUIRED");
 const ownerId=String(packet.owner_id);const {data:owner,error:ownerError}=await supabase.auth.admin.getUserById(ownerId);if(ownerError||!owner?.user)return fail(403,"OWNER_NOT_FOUND");
 const {data:existing,error:lookupError}=await supabase.from("nayanet_project_intelligence_bridge").select("packet_id,project_id,source_ref,content_hash,owner_id,receiver_transaction_id,receiver_event_id,receipt_id,persisted,indexed,projected,retrieved,rendered,accepted_at").eq("idempotency_key",packet.idempotency_key).maybeSingle();
 if(lookupError)return fail(500,"LOOKUP_FAILED",lookupError.message);if(existing)return new Response(JSON.stringify({status:"ACCEPTED",replay:true,...existing}),{status:200,headers:{"content-type":"application/json"}});
 const transactionId=crypto.randomUUID(),receiverEventId=crypto.randomUUID(),receiptId=crypto.randomUUID();
 const {data:bridge,error}=await supabase.from("nayanet_project_intelligence_bridge").insert({packet_id:packet.packet_id,project_id:packet.project_id,source_ref:packet.source_ref,content_hash:packet.content_hash,idempotency_key:packet.idempotency_key,packet,owner_id:ownerId,receiver_transaction_id:transactionId,receiver_event_id:receiverEventId,receipt_id:receiptId,indexed:false,projected:false}).select("packet_id,project_id,source_ref,content_hash,owner_id,receiver_transaction_id,receiver_event_id,receipt_id,persisted,indexed,projected,retrieved,rendered,accepted_at").single();
 if(error)return fail(500,"PERSIST_FAILED",error.message);
 const title=String(packet.project_intelligence_reconstruction?.current?.mission||packet.operating_context?.current_next_action?.action||"NayaNET Project Intelligence");
 const content=JSON.stringify({protocol:packet.protocol,project_id:packet.project_id,source_ref:packet.source_ref,content_hash:packet.content_hash,operating_context:packet.operating_context,project_intelligence_reconstruction:packet.project_intelligence_reconstruction,intelligence:packet.intelligence,provenance:packet.provenance,privacy:packet.privacy,bridge:{packet_id:packet.packet_id,receiver_transaction_id:transactionId,receiver_event_id:receiverEventId,receipt_id:receiptId}});
 const {data:event,error:eventError}=await supabase.from("nayanet_cognition_events").insert({user_id:ownerId,project_id:"NayaNET",event_id:receiverEventId,type:"project_intelligence_bridge",classification:"project_intelligence",title,content,source:"nayanet-project-intelligence-bridge",status:"active",actor:"machine",confidence:1,tags:["project-intelligence","bridge","github","private"],parent_event_id:null,source_hash:packet.content_hash,schema_version:"1.0.0",receipt_id:receiptId,metadata:{bridge_packet_id:packet.packet_id,receiver_transaction_id:transactionId,receiver_event_id:receiverEventId,receipt_id:receiptId,owner_id:ownerId,privacy:"PRIVATE",source_ref:packet.source_ref,content_hash:packet.content_hash,projected_at:new Date().toISOString()}}).select("id,event_id,title,type,status,created_at").single();
 if(eventError){await supabase.from("nayanet_project_intelligence_bridge").delete().eq("packet_id",packet.packet_id);return fail(500,"COGNITION_PROJECTION_FAILED",eventError.message)}
 const {data:index,error:indexError}=await supabase.from("nayanet_intelligence_index").select("id").eq("owner_id",ownerId).eq("source_table","nayanet_cognition_events").eq("source_id",event.id).maybeSingle();
 if(indexError)return fail(500,"INDEX_PROJECTION_FAILED",indexError.message);
 if(!index)return fail(500,"INDEX_PROJECTION_MISSING","cognition event trigger did not create canonical index");
 const {data:updated,error:updateError}=await supabase.from("nayanet_project_intelligence_bridge").update({indexed:true,projected:true}).eq("packet_id",packet.packet_id).select("packet_id,project_id,source_ref,content_hash,owner_id,receiver_transaction_id,receiver_event_id,receipt_id,persisted,indexed,projected,retrieved,rendered,accepted_at").single();
 if(updateError)return fail(500,"PROJECTION_FLAG_UPDATE_FAILED",updateError.message);
 return new Response(JSON.stringify({status:"COMPLETED",replay:false,...updated,projection:{cognition_event_id:event.id,index_id:index.id}}),{status:200,headers:{"content-type":"application/json"}});
});