import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const cors={"Access-Control-Allow-Origin":"*","Access-Control-Allow-Headers":"authorization, x-client-info, apikey, content-type, x-idempotency-key","Access-Control-Allow-Methods":"POST, OPTIONS"};
function json(body:unknown,status=200){return new Response(JSON.stringify(body),{status,headers:{...cors,"Content-Type":"application/json"}})}
Deno.serve(async(req)=>{
 if(req.method==="OPTIONS")return new Response("ok",{headers:cors});
 if(req.method!=="POST")return json({ok:false,error:"METHOD_NOT_ALLOWED"},405);
 try{
  const supabaseUrl=Deno.env.get("SUPABASE_URL"),supabaseAnonKey=Deno.env.get("SUPABASE_ANON_KEY");
  if(!supabaseUrl||!supabaseAnonKey)throw new Error("SUPABASE_RUNTIME_NOT_CONFIGURED");
  const auth=req.headers.get("Authorization");if(!auth)return json({ok:false,error:"AUTHORIZATION_REQUIRED"},401);
  const supabase=createClient(supabaseUrl,supabaseAnonKey,{global:{headers:{Authorization:auth}}});
  const {data:{user},error:userError}=await supabase.auth.getUser();if(userError||!user)return json({ok:false,error:"AUTHENTICATED_USER_REQUIRED"},401);
  const body=await req.json(),human=body?.human_note,naya=body?.naya_note,idempotencyKey=body?.idempotency_key||req.headers.get("x-idempotency-key");
  if(!idempotencyKey||typeof idempotencyKey!=="string")return json({ok:false,error:"SMART_NOTE_IDEMPOTENCY_KEY_REQUIRED"},400);
  if(!human||!naya)return json({ok:false,error:"HUMAN_AND_NAYA_NOTES_REQUIRED"},400);
  const now=new Date().toISOString(),eventId=crypto.randomUUID();
  const nutshell=typeof body?.in_a_nutshell==='string'&&body.in_a_nutshell.trim()?body.in_a_nutshell.trim():(naya.summary||naya.text||human.text||"Smart Note captured and interpreted.");
  const childGrandma=typeof body?.child_grandma==='string'&&body.child_grandma.trim()?body.child_grandma.trim():`In simple words: ${nutshell}`;
  const machine={event_id:eventId,schema:"nayanet.smart_note.machine.v2",occurred_at:now,source:body?.source||"naya_conversation",type:human.type||"insight",actor:user.id,human_note_id:human.id||null,normalized_text:human.text||human.content||"",idempotency_key:idempotencyKey};
  const feed={event_id:eventId,kind:"smart_note.created",occurred_at:now,status:"verified",source:machine.source,type:machine.type,summary:nutshell};
  const block={block_id:eventId,kind:"intelligent_block",created_at:now,subject:body?.subject||human.subject||"Intelligent Note",type:human.type||"INSIGHT",in_a_nutshell:nutshell,perspectives:{human:human.text||human.content||"",naya:naya.text||naya.content||naya.summary||"",machine,child_grandma:childGrandma},feed_summary:nutshell,status:"preserved",privacy:"PRIVATE",evidence_required:true};
  const artifactUrls=body?.artifact_urls&&typeof body.artifact_urls==="object"?body.artifact_urls:{};
  const evidence={receipt_id:crypto.randomUUID(),event_id:eventId,source:machine.source,chain:["human_note","naya_note","machine_note","intelligence_feed","intelligent_block"],verified_at:now,artifact_urls:artifactUrls,receipt_url:typeof body?.receipt_url==="string"?body.receipt_url:null};
  const hubState={event_id:eventId,last_intelligence_event_at:now,smart_note_created:true,intelligent_block_created:true,feed_updated:true,canonical_collection:"Smart Notes",private_feed:true};
  const {data,error}=await supabase.rpc("v7_create_smart_note",{p_idempotency_key:idempotencyKey,p_user_id:user.id,p_human_note:human,p_naya_note:naya,p_machine_note:machine,p_intelligent_feed:feed,p_intelligent_block:block,p_evidence:evidence,p_hub_state:hubState,p_subject:typeof body?.subject==="string"?body.subject:null});
  if(error)throw error;
  return json({ok:true,pipeline:"completed",canonical_event:true,collection:"Smart Notes",transaction:data});
 }catch(error){console.error(error);return json({ok:false,error:"SMART_NOTE_PIPELINE_FAILED",detail:String(error)},500)}
});
