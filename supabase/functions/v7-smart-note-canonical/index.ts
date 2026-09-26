// Canonical receiver contract: authoritative live IB identity is allocated here; repository projections never guess IDs. Acceptance semantics remain provenance-bound.
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
async function stableUuid(value:string):Promise<string>{
  const bytes=new Uint8Array(await crypto.subtle.digest("SHA-256",new TextEncoder().encode(value)));
  bytes[6]=(bytes[6]&0x0f)|0x50;bytes[8]=(bytes[8]&0x3f)|0x80;
  const hex=[...bytes.slice(0,16)].map(byte=>byte.toString(16).padStart(2,"0")).join("");
  return `${hex.slice(0,8)}-${hex.slice(8,12)}-${hex.slice(12,16)}-${hex.slice(16,20)}-${hex.slice(20)}`;
}
const normalizedText=(value:unknown)=>String(value??"").replace(/\s+/g," ").trim();
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
  childText:string;
  grandmaText:string;
  learningText:string;
  meaningText:string;
  connectsText:string;
  applyText:string;
  valueText:string;
}){
  return {
    identity:{
      object_id:"event:"+args.eventId,
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
      simple:args.childText
    },
    perspectives:{
      human:args.humanText,
      child:args.childText,
      grandma:args.grandmaText,
      naya:args.nayaText,
      machine:JSON.stringify(args.machine),
      learning:args.learningText,
      meaning:args.meaningText,
      connections:args.connectsText,
      application:args.applyText,
      value:args.valueText
    },
    distillation:{
      method:"canonical-smart-note-v1",
      source_count:1,
      preserved:["human meaning","Naya interpretation","required perspectives","provenance","evidence","current state","next action"],
      removed_as_redundant:[],
      compression_notes:"One coherent intelligence event is represented once; perspectives are projections of the same meaning."
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
      evidence_state:"OBSERVED",
      evidence_refs:[args.eventId],
      verification:"Persistence and lineage were verified; content truth remains bound to its source and evidence.",
      verification_method:"canonical_smart_note_persistence_and_lineage"
    },
    truth:{
      state:"SUPPORTED",
      confidence:0,
      conflicts:[]
    },
    authority:{
      state:"AUTHORIZED",
      authority_ref:"authenticated_owner_capture",
      constraints:["owner_only","private_by_default"]
    },
    relationships:[],
    value:{
      state:"POTENTIAL",
      benefit:0,
      harm:0,
      cost:0,
      risk:0,
      effort:0,
      relevance:0,
      responsible_value:0
    },
    action:{
      action:args.applyText,
      method:"v7-smart-note-canonical",
      authorization_basis:"authenticated owner",
      expected_result:"canonical Smart Note / Intelligent Block is retrievable and reusable"
    },
    outcome:{
      state:"UNKNOWN",
      observed_result:null,
      measurements:{},
      unexpected_effects:[]
    },
    learning:{
      what_changed:args.learningText,
      lesson:args.learningText,
      reusable_rule:null,
      evidence_basis:[args.eventId],
      applicability:"Pending future application and outcome verification."
    },
    successor:{
      type:"NEXT_ACTION",
      target:"retrieve_and_verify",
      reason:args.applyText
    },
    lifecycle:{
      stage:"DISTILLED",
      captured_at:args.now,
      verified_at:null,
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
 let canonicalEventId:string|null=null,canonicalReceiptId:string|null=null,canonicalTransactionId:string|null=null;
 try{
  const supabaseUrl=Deno.env.get("SUPABASE_URL"),supabaseAnonKey=Deno.env.get("SUPABASE_ANON_KEY");
  if(!supabaseUrl||!supabaseAnonKey)throw new Error("SUPABASE_RUNTIME_NOT_CONFIGURED");
  const auth=req.headers.get("Authorization");if(!auth)return json({ok:false,error:"AUTHORIZATION_REQUIRED"},401);
  const supabase=createClient(supabaseUrl,supabaseAnonKey,{global:{headers:{Authorization:auth}}});
  const {data:{user},error:userError}=await supabase.auth.getUser();if(userError||!user)return json({ok:false,error:"AUTHENTICATED_USER_REQUIRED"},401);
  const body=await req.json(),human=body?.human_note,naya=body?.naya_note,idempotencyKey=body?.idempotency_key||req.headers.get("x-idempotency-key");
  if(!idempotencyKey||typeof idempotencyKey!=="string")return json({ok:false,error:"SMART_NOTE_IDEMPOTENCY_KEY_REQUIRED"},400);
  if(!human||!naya)return json({ok:false,error:"HUMAN_AND_NAYA_NOTES_REQUIRED"},400);
   const now=new Date().toISOString();let eventId=crypto.randomUUID();canonicalEventId=eventId;

  const canonicalHuman={...human,event_id:eventId};
  const canonicalNaya={...naya,event_id:eventId};
  const subject=String(body?.subject||human.subject||"Intelligent Note").trim()||"Intelligent Note";
  const humanText=String(human.text||human.content||"").trim();
  const nayaText=String(naya.text||naya.content||naya.summary||"").trim();
  const nutshell=typeof body?.in_a_nutshell==="string"&&body.in_a_nutshell.trim()?body.in_a_nutshell.trim():(naya.summary||naya.text||human.text||"Smart Note captured and interpreted.");
  const childText=String(body?.child_note||body?.child||("In simple words: "+nutshell)).trim();
  const grandmaText=String(body?.grandma_note||body?.grandma||("In practical everyday terms: "+nutshell)).trim();
  const learningText=String(body?.learning_lesson||body?.learning||"Learning candidate: preserve this intelligence and test its future usefulness.").trim();
  const meaningText=String(body?.what_it_means||body?.meaning||"This turns meaningful human input into reusable intelligence that can be retrieved and applied later.").trim();
  const connectsText=String(body?.how_it_connects||body?.connections||"Connect this Smart Note to its source event, related intelligence, learning evidence, Feed/Hub projections, and successor work.").trim();
  const applyText=String(body?.how_to_apply||body?.how_to_use||"Retrieve this intelligence when relevant, apply it within authority, and verify the outcome.").trim();
  const valueText=String(body?.value||"Preserves important intelligence so future Nayas and the human do not have to reconstruct it from conversation.").trim();
  const source=String(body?.source||"naya_conversation");
  const machine={event_id:eventId,schema:"nayanet.smart_note.machine.v2",occurred_at:now,source,type:human.type||"insight",actor:user.id,human_note_id:canonicalHuman.id||null,normalized_text:humanText,idempotency_key:idempotencyKey};
  const feed={event_id:eventId,kind:"smart_note.created",occurred_at:now,status:"verified",source,type:machine.type,summary:nutshell};
  const artifactUrls=body?.artifact_urls&&typeof body.artifact_urls==="object"?body.artifact_urls:{};
  const projectionCategory=String(body?.projection_category||body?.category||"system").trim().toLowerCase().replace(/[^a-z0-9]+/g,"-").replace(/^-+|-+$/g,"").slice(0,64)||"system";
  const projectionTopic=String(body?.projection_topic||body?.topic||subject).trim().toLowerCase().replace(/[^a-z0-9]+/g,"-").replace(/^-+|-+$/g,"").split("-").filter(Boolean).slice(0,3).join("-")||"smart-note";
  const blockBase=buildIntelligentBlock({eventId,now,userId:user.id,subject,humanText,nayaText,nutshell,simpleText:childText,childText,grandmaText,learningText,meaningText,connectsText,applyText,valueText,machine,source,idempotencyKey});
  blockBase.metadata={...blockBase.metadata,projection_category:projectionCategory,projection_topic:projectionTopic};
  const blockHash=await sha256Hex(blockBase);
  const block={...blockBase,integrity:{algorithm:"SHA-256",content_hash:blockHash}};
  const evidence={receipt_id:crypto.randomUUID(),event_id:eventId,source,correlation_id:typeof body?.correlation_id==='string'?body.correlation_id:null,chain:["human_note","naya_note","machine_note","intelligence_feed","intelligent_block_v1"],verified_at:now,artifact_urls:artifactUrls,receipt_url:typeof body?.receipt_url==="string"?body.receipt_url:null,intelligent_block_v1:true,intelligent_block_hash:blockHash};canonicalReceiptId=evidence.receipt_id;
  const hubState={event_id:eventId,last_intelligence_event_at:now,smart_note_created:true,intelligent_block_created:true,intelligent_block_schema:"NAYANET_INTELLIGENT_BLOCK_V1",intelligent_block_hash:blockHash,feed_updated:true,canonical_collection:"Smart Notes",private_feed:true};
   const {data,error}=await supabase.rpc("v7_create_smart_note",{p_idempotency_key:idempotencyKey,p_user_id:user.id,p_human_note:canonicalHuman,p_naya_note:canonicalNaya,p_machine_note:machine,p_intelligent_feed:feed,p_intelligent_block:block,p_evidence:evidence,p_hub_state:hubState,p_subject:subject});
   if(error)throw error;canonicalTransactionId=String(data?.id||data?.transaction_id||"");
   const persistedEventId=String(data?.evidence?.event_id||data?.hub_state?.event_id||"").trim();
   if(!persistedEventId)throw new Error("SMART_NOTE_CANONICAL_EVENT_ID_MISSING");
   const replayed=persistedEventId!==eventId;
   if(replayed){
     const persistedHuman=normalizedText(data?.human_note?.text??data?.human_note?.content);
     const persistedNaya=normalizedText(data?.naya_note?.text??data?.naya_note?.content??data?.naya_note?.summary);
     const persistedSubject=normalizedText(data?.human_note?.subject||data?.intelligent_block?.meaning?.subject);
     if(persistedHuman!==normalizedText(humanText)||persistedNaya!==normalizedText(nayaText)||persistedSubject!==normalizedText(subject))throw new Error("SMART_NOTE_IDEMPOTENCY_CONFLICT");
     eventId=persistedEventId;
   }
   canonicalEventId=eventId;
   const persistedBlock:any=data?.intelligent_block||{};
   const persistedEvidence:any=data?.evidence||{};
   const persistedSubject=normalizedText(persistedBlock?.meaning?.subject||data?.human_note?.subject||subject)||subject;
   const persistedNutshell=normalizedText(persistedBlock?.meaning?.in_a_nutshell||data?.in_a_nutshell||data?.human_note?.in_a_nutshell||nutshell)||nutshell;
   const persistedReceiptId=normalizedText(persistedEvidence?.smart_note_receipt_id||persistedEvidence?.receipt_id||evidence.receipt_id);
   const persistedBlockHash=normalizedText(persistedBlock?.integrity?.content_hash||persistedEvidence?.intelligent_block_hash||blockHash);
   if(!persistedReceiptId||!persistedBlockHash)throw new Error("SMART_NOTE_PERSISTED_LINEAGE_INCOMPLETE");
   canonicalReceiptId=persistedReceiptId;

   const learningClaim=persistedNutshell;
    const learningId=await stableUuid("nayanet-learning:"+user.id+":"+eventId);
    const learningById=await supabase.from("learning_evidence").select("id,status,claim,target_id").eq("id",learningId).maybeSingle();
    if(learningById.error)throw learningById.error;
    let learning:any=learningById.data;

   if(!learning){
     const legacyLearning=await supabase.from("learning_evidence").select("id,status,claim,target_id").eq("member_id",user.id).eq("source_event_id",eventId).eq("claim",learningClaim).limit(1).maybeSingle();
     if(legacyLearning.error)throw legacyLearning.error;
     learning=legacyLearning.data;
   }
   if(!learning){
     const createdLearning=await supabase.from("learning_evidence").insert({
       id:learningId,
       member_id:user.id,
       target_id:"smart-note:"+eventId,
       level:"E1_UNDERSTANDS",
       provenance:"USER",
       status:"CANDIDATE",
       claim:learningClaim.slice(0,2000),
       observed_value:{source:"v7-smart-note-canonical",event_id:eventId,subject:persistedSubject},
       verification_method:"PENDING_OUTCOME_VERIFICATION",
       source_event_id:eventId
     }).select("id,status,claim,target_id").single();
     if(createdLearning.error&&createdLearning.error.code!=="23505")throw createdLearning.error;
     learning=createdLearning.data;
     if(!learning){
       const retry=await supabase.from("learning_evidence").select("id,status,claim,target_id").eq("id",learningId).maybeSingle();
       if(retry.error)throw retry.error;
       learning=retry.data;
     }
   }
   if(!learning?.id)throw new Error("SMART_NOTE_LEARNING_EVIDENCE_MISSING");


  const checkpointId="smart-note-checkpoint:"+eventId;
  const checkpointResponse=await fetch(
    supabaseUrl+"/functions/v1/nayanet-compound-intelligence",
    {
      method:"POST",
      headers:{
        "Authorization":auth,
        "apikey":supabaseAnonKey,
        "Content-Type":"application/json",
        "x-idempotency-key":checkpointId
      },
      body:JSON.stringify({
        action:"checkpoint",
        checkpoint_id:checkpointId,
        source_event_ids:[eventId],
        current_understanding:persistedNutshell,
        title:"Smart Note checkpoint: "+persistedSubject,
        confidence:1,
        tags:["smart-note","intelligent-block","checkpoint"],
        what_changed:"Canonical Smart Note was captured, projected as an Intelligent Block, and entered the governed learning boundary.",
        learned:learningClaim,
        evidence_refs:[
          {kind:"smart_note_receipt",receipt_id:persistedReceiptId},
          {kind:"source_event",event_id:eventId},
          {kind:"intelligent_block_hash",sha256:persistedBlockHash},
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
  const checkpointData=await checkpointResponse.json().catch(()=>({}));
  const checkpoint=checkpointData?.result;
  const checkpointReceiptId=normalizedText(checkpoint?.receipt?.id||checkpoint?.receipt?.receipt_id);
  const checkpointEvidence=Array.isArray(checkpoint?.checkpoint?.metadata?.evidence_refs)?checkpoint.checkpoint.metadata.evidence_refs:[];
  const checkpointEvidenceMatches=checkpointEvidence.some(ref=>ref?.kind==="smart_note_receipt"&&String(ref.receipt_id||"")===persistedReceiptId)&&checkpointEvidence.some(ref=>ref?.kind==="source_event"&&String(ref.event_id||"")===eventId)&&checkpointEvidence.some(ref=>ref?.kind==="intelligent_block_hash"&&String(ref.sha256||"")===persistedBlockHash)&&checkpointEvidence.some(ref=>ref?.kind==="learning_evidence"&&String(ref.evidence_id||"")===String(learning.id));
  if(!checkpointResponse.ok||!checkpointData?.ok||checkpoint?.status!=="CHECKPOINT_VERIFIED"||String(checkpoint?.checkpoint?.event_id||"")!==checkpointId||!checkpointReceiptId||!checkpointEvidenceMatches){
    throw new Error("SMART_NOTE_CHECKPOINT_FAILED:"+JSON.stringify({status:checkpoint?.status||"UNAVAILABLE",checkpoint_id:checkpoint?.checkpoint?.event_id||"UNAVAILABLE",receipt_id:checkpointReceiptId||"UNAVAILABLE"}));
  }

  const transactionWithIntelligence={
    ...data,
    learning_evidence:{
      id:learning.id,
      status:learning.status,
      claim:learning.claim,
      target_id:learning.target_id
    },
    intelligence_checkpoint:checkpoint
  };
  // Final runtime boundary: prove the canonical event is actually visible to the authenticated owner's Smart Feed before returning completion.
  const feedVerification=await supabase.from("nayanet_cognition_events")
    .select("id,event_id,user_id,project_id,status,created_at")
    .eq("event_id",eventId)
    .eq("user_id",user.id)
    .eq("project_id","NayaNET")
    .maybeSingle();
  if(feedVerification.error)throw feedVerification.error;
  if(!feedVerification.data)throw new Error("SMART_NOTE_FEED_VERIFICATION_FAILED");
  const feedVerificationReceipt={
    verified:true,
    verified_at:new Date().toISOString(),
    source_id:String(feedVerification.data.id),
    event_id:String(feedVerification.data.event_id),
    stream:"personal",
    visibility:"private"
  };

  const intelligentBlockId=normalizedText(transactionWithIntelligence?.intelligent_block?.identity?.intelligent_block_id);
  if(!/^IB-\d{6}$/.test(intelligentBlockId))throw new Error("SMART_NOTE_CANONICAL_IB_ID_INVALID");
   const repositoryProjection={
     status:"PENDING",
     rule:"Repository Smart Note projection MUST use the authoritative live intelligent_block_id returned by this receiver; repository code MUST NOT allocate or guess IB identities.",
     intelligent_block_id:intelligentBlockId||null,
     source_event_id:eventId,
     canonical_receiver:"v7-smart-note-canonical"
   };
  const hubDeepLink="/hub?ib="+encodeURIComponent(intelligentBlockId);
  const smartLink=null;
  const completionReceipt={
    schema:"naya/smart-note-receiver-receipt/v1",
    canonical_receiver:"v7-smart-note-canonical",
    status:replayed?"replayed":"completed",
    intelligent_block_id:intelligentBlockId,
    event_id:eventId,
    transaction_id:canonicalTransactionId,
    feed_verification:feedVerificationReceipt,
    smart_link:null,
    hub_deep_link:hubDeepLink,
    repository_projection:{
      status:"PENDING",
      category:projectionCategory,
      topic:projectionTopic,
      intelligent_block_id:intelligentBlockId,
      source_event_id:eventId,
      canonical_receiver:"v7-smart-note-canonical",
      workflow:"project-canonical-smart-note.yml",
      transaction_id:canonicalTransactionId
    }
  };
  return json({
    ok:true,
    pipeline:replayed?"replayed":"completed",
    canonical_event:true,
    collection:"Smart Notes",
    replayed,
    intelligent_block_id:intelligentBlockId||null,
    transaction_id:canonicalTransactionId,
    transaction:transactionWithIntelligence,
    feed_verification:feedVerificationReceipt,
    smart_link:null,
    hub_deep_link:hubDeepLink,
    completion_receipt:completionReceipt,
    repository_projection:{
      ...repositoryProjection,
      category:projectionCategory,
      topic:projectionTopic,
      workflow:"project-canonical-smart-note.yml",
      transaction_id:canonicalTransactionId
    }
  });

 }catch(error){console.error(error);return json({ok:false,pipeline:"failed",error:"SMART_NOTE_PIPELINE_FAILED",detail:String(error),event_id:canonicalEventId,receipt_id:canonicalReceiptId,transaction_id:canonicalTransactionId},500)}
});
