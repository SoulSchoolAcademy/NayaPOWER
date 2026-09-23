import "jsr:@supabase/functions-js/edge-runtime.d.ts";
// NAYANET LIVE-PARITY REVALIDATION 2026-09-23
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const cors={"Access-Control-Allow-Origin":"*","Access-Control-Allow-Headers":"authorization, x-client-info, apikey, content-type, x-idempotency-key","Access-Control-Allow-Methods":"POST, OPTIONS"};
function json(body:unknown,status=200){return new Response(JSON.stringify(body),{status,headers:{...cors,"Content-Type":"application/json"}})}

function canonicalize(value:unknown):unknown{
  if(Array.isArray(value))return value.map(canonicalize);
  if(value&&typeof value==="object")return Object.fromEntries(Object.entries(value as Record<string,unknown>).sort(([a],[b])=>a.localeCompare(b)).map(([k,v])=>[k,canonicalize(v)]));
  return value;
}
async function sha256Hex(value:unknown):Promise<string>{
  const encoded=new TextEncoder().encode(JSON.stringify(canonicalize(value)));
  const digest=await crypto.subtle.digest("SHA-256",encoded);
  return [...new Uint8Array(digest)].map(b=>b.toString(16).padStart(2,"0")).join("");
}
function buildIntelligentBlock(args:{
  eventId:string;
  now:string;
  userId:string;
  subject:string;
  humanText:string;
  nayaText:string;
  nutshell:string;
  simpleText:string;
  machine:Record<string,unknown>;
  source:string;
  idempotencyKey:string;
}){
  return {
    identity:{
      object_id:"IB:"+args.eventId,
      event_id:args.eventId,
      version:1,
      namespace:"nayanet",
      schema_version:"NAYANET_INTELLIGENT_BLOCK_V1"
    },
    type:{
      object_type:"INTELLIGENT_EVENT",
      event_type:"SMART_NOTE",
      classification:"intelligence"
    },
    meaning:{
      subject:args.subject,
      title:args.subject,
      content:args.humanText,
      summary:args.nutshell,
      in_a_nutshell:args.nutshell,
      interpretation:args.nayaText||"The Smart Note was captured through the authenticated canonical receiver.",
      human:args.humanText,
      naya:args.nayaText,
      machine:JSON.stringify(args.machine),
      simple:args.simpleText
    },
    actors:{
      creator:args.userId,
      observer:args.userId,
      verifier:args.userId,
      authorizer:args.userId,
      executor:args.userId,
      beneficiary:args.userId,
      affected_parties:[args.userId]
    },
    context:{
      project:"NayaNET",
      scope:"PRIVATE",
      environment:"production",
      audience:["owner"],
      visibility:"PRIVATE"
    },
    time:{
      occurred_at:args.now,
      observed_at:args.now,
      effective_at:args.now,
      valid_from:args.now,
      valid_until:null,
      superseded_at:null
    },
    intent:{
      purpose:"Capture and preserve meaningful human intelligence as a reusable canonical event.",
      why:"Preserve meaning, evidence, authority, privacy, and continuity so the intelligence can be reused.",
      desired_outcome:"The same intelligence remains understandable and attributable across authorized systems.",
      expected_value:0
    },
    provenance:{
      source:args.source,
      source_ref:"smart_note:"+args.eventId,
      captured_by:args.userId,
      derived_from:[]
    },
    evidence:{
      evidence_state:"VERIFIED",
      evidence_refs:[args.eventId],
      verification:"Canonical Smart Note verification completed.",
      verification_method:"verify_smart_note"
    },
    truth:{
      state:"VERIFIED",
      confidence:1,
      conflicts:[]
    },
    authority:{
      state:"AUTHORIZED",
      authority_ref:"authenticated_owner_capture",
      constraints:["owner_only","private_by_default"]
    },
    relationships:[],
    value:{
      state:"UNKNOWN"
    },
    action:{
      action:"capture_smart_note",
      method:"v7-smart-note-canonical",
      authorization_basis:"authenticated owner",
      expected_result:"verified Smart Note with portable Intelligent Block"
    },
    outcome:{
      state:"UNKNOWN",
      observed_result:null,
      measurements:{},
      unexpected_effects:[]
    },
    learning:{
      what_changed:null,
      lesson:null,
      reusable_rule:null,
      evidence_basis:[],
      applicability:null
    },
    successor:{
      type:"NEXT_ACTION",
      target:"retrieve_and_verify",
      reason:"The canonical next step is to retrieve the event and verify semantic round-trip integrity."
    },
    lifecycle:{
      stage:"VERIFIED",
      captured_at:args.now,
      verified_at:args.now,
      updated_at:args.now
    },
    projections:{
      human:{subject:args.subject,summary:args.nutshell},
      naya:{interpretation:args.nayaText,why: "Preserve and reuse verified intelligence without changing its meaning."},
      machine:{event_id:args.eventId,schema_version:"NAYANET_INTELLIGENT_BLOCK_V1"},
      simple:{summary:args.simpleText},
      hub:{event_id:args.eventId,visibility:"PRIVATE"},
      api:{event_id:args.eventId,version:1}
    },
    metadata:{
      transport_version:"NAYANET_INTELLIGENT_BLOCK_V1",
      source_idempotency_key:args.idempotencyKey
    }
  };
}

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
  const canonicalHuman={...human,event_id:eventId};
  const canonicalNaya={...naya,event_id:eventId};
  const subject=String(body?.subject||human.subject||"Intelligent Note").trim()||"Intelligent Note";
  const humanText=String(human.text||human.content||"").trim();
  const nayaText=String(naya.text||naya.content||naya.summary||"").trim();
  const nutshell=typeof body?.in_a_nutshell==="string"&&body.in_a_nutshell.trim()?body.in_a_nutshell.trim():(naya.summary||naya.text||human.text||"Smart Note captured and interpreted.");
  const childGrandma=typeof body?.child_grandma==="string"&&body.child_grandma.trim()?body.child_grandma.trim():`In simple words: ${nutshell}`;
  const source=String(body?.source||"naya_conversation");
  const machine={event_id:eventId,schema:"nayanet.smart_note.machine.v2",occurred_at:now,source,type:human.type||"insight",actor:user.id,human_note_id:canonicalHuman.id||null,normalized_text:humanText,idempotency_key:idempotencyKey};
  const feed={event_id:eventId,kind:"smart_note.created",occurred_at:now,status:"verified",source,type:machine.type,summary:nutshell};
  const blockBase=buildIntelligentBlock({eventId,now,userId:user.id,subject,humanText,nayaText,nutshell,simpleText:childGrandma,machine,source,idempotencyKey});
  const blockHash=await sha256Hex(blockBase);
  const block={...blockBase,integrity:{algorithm:"SHA-256",content_hash:blockHash}};
  const artifactUrls=body?.artifact_urls&&typeof body.artifact_urls==="object"?body.artifact_urls:{};
  const evidence={receipt_id:crypto.randomUUID(),event_id:eventId,source,chain:["human_note","naya_note","machine_note","intelligence_feed","intelligent_block_v1"],verified_at:now,artifact_urls:artifactUrls,receipt_url:typeof body?.receipt_url==="string"?body.receipt_url:null,intelligent_block_v1:true,intelligent_block_hash:blockHash};
  const hubState={event_id:eventId,last_intelligence_event_at:now,smart_note_created:true,intelligent_block_created:true,intelligent_block_schema:"NAYANET_INTELLIGENT_BLOCK_V1",intelligent_block_hash:blockHash,feed_updated:true,canonical_collection:"Smart Notes",private_feed:true};
  const {data,error}=await supabase.rpc("v7_create_smart_note",{p_idempotency_key:idempotencyKey,p_user_id:user.id,p_human_note:canonicalHuman,p_naya_note:canonicalNaya,p_machine_note:machine,p_intelligent_feed:feed,p_intelligent_block:block,p_evidence:evidence,p_hub_state:hubState,p_subject:subject});
  if(error)throw error;

  // Idempotent replay must continue from the persisted canonical event identity.
  // The RPC is the transaction authority; a replay must never generate a fresh
  // downstream event/checkpoint identity or attempt to re-run learning against it.
  const persistedEventId=String(data?.evidence?.event_id||data?.hub_state?.event_id||"").trim();
  if(!persistedEventId)throw new Error("SMART_NOTE_CANONICAL_EVENT_ID_MISSING");
  if(persistedEventId!==eventId){
    return json({
      ok:true,
      pipeline:"replayed",
      canonical_event:true,
      collection:"Smart Notes",
      replayed:true,
      transaction:data
    });
  }

  // Every canonical Smart Note now enters the same governed learning/checkpoint boundary.
  // The Smart Note transaction remains the single source event; the checkpoint is its
  // provenance-bound cognitive state, not a second intelligence/event model.
  const learningClaim = nutshell;
  const learningLookup = await supabase.from("learning_evidence")
    .select("id,status,claim,target_id")
    .eq("member_id",user.id)
    .eq("source_event_id",eventId)
    .eq("claim",learningClaim)
    .maybeSingle();
  if(learningLookup.error)throw learningLookup.error;
  let learning = learningLookup.data;
  if(!learning){
    const createdLearning = await supabase.from("learning_evidence").insert({
      member_id:user.id,
      target_id:"smart-note:"+eventId,
      level:"E1_UNDERSTANDS",
      provenance:"USER",
      status:"CANDIDATE",
      claim:learningClaim.slice(0,2000),
      observed_value:{source:"v7-smart-note-canonical",event_id:eventId,subject},
      verification_method:"PENDING_OUTCOME_VERIFICATION",
      source_event_id:eventId
    }).select("id,status,claim,target_id").single();
    if(createdLearning.error)throw createdLearning.error;
    learning=createdLearning.data;
  }

  const checkpointResponse = await fetch(
    supabaseUrl + "/functions/v1/nayanet-compound-intelligence",
    {
      method:"POST",
      headers:{
        "Authorization":auth,
        "apikey":supabaseAnonKey,
        "Content-Type":"application/json",
        "x-idempotency-key":"smart-note-checkpoint:"+eventId
      },
      body:JSON.stringify({
        action:"checkpoint",
        checkpoint_id:"smart-note-checkpoint:"+eventId,
        source_event_ids:[eventId],
        current_understanding:nutshell,
        title:"Smart Note checkpoint: "+subject,
        confidence:1,
        tags:["smart-note","intelligent-block","checkpoint"],
        what_changed:"Canonical Smart Note was captured, projected as an Intelligent Block, and entered the governed learning boundary.",
        learned:learningClaim,
        evidence_refs:[
          {kind:"smart_note_receipt",receipt_id:evidence.receipt_id},
          {kind:"source_event",event_id:eventId},
          {kind:"intelligent_block_hash",sha256:blockHash},
          {kind:"learning_evidence",evidence_id:learning.id}
        ],
        authority_scope:"PERSONAL_INTELLIGENCE_ONLY",
        unknown:["Future applicability, behavior change, and outcome verification remain open."],
        applicable_scope:body?.applicable_scope||null,
        next_use:"Cold Naya retrieves this intelligence when the topic/context is relevant.",
        successor_relevance:"Successor must restore the checkpoint, assess applicability, use it when valid, verify the outcome, and improve the next checkpoint.",
        source_head:body?.source_head||null
      })
    }
  );
  const checkpointData = await checkpointResponse.json().catch(()=>({}));
  if(!checkpointResponse.ok || !checkpointData?.ok){
    throw new Error("SMART_NOTE_CHECKPOINT_FAILED:" + JSON.stringify(checkpointData));
  }

  const transactionWithIntelligence = {
    ...data,
    learning_evidence:{
      id:learning.id,
      status:learning.status,
      claim:learning.claim,
      target_id:learning.target_id
    },
    intelligence_checkpoint:checkpointData.result||null
  };
  return json({
    ok:true,
    pipeline:"completed",
    canonical_event:true,
    collection:"Smart Notes",
    transaction:transactionWithIntelligence
  });
 }catch(error){console.error(error);return json({ok:false,error:"SMART_NOTE_PIPELINE_FAILED",detail:String(error)},500)}
});
