import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "npm:@supabase/supabase-js@2";

const URL = Deno.env.get("SUPABASE_URL")!;
const ANON = Deno.env.get("SUPABASE_ANON_KEY")!;
const SECRET = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const admin = createClient(URL, SECRET);
const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization,apikey,content-type,x-idempotency-key",
  "Access-Control-Allow-Methods": "POST,OPTIONS"
};
const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { ...cors, "Content-Type": "application/json" } });

const MISSION = "Make it dramatically easier for an ordinary human with a meaningful vision to accomplish extraordinary things with AI without becoming an AI project manager.";
const NORTH_STAR = "Maximum verified human value per unit of effort, with compounding intelligence and continuity.";
const PROJECT = "NayaNET";
const CANONICAL_HUB = "NAYANET/HUB/index.html";
const GITHUB_REPO = "SoulSchoolAcademy/NayaPOWER";
const GITHUB_REF = "main";

async function auth(req: Request) {
  const authorization = req.headers.get("Authorization");
  if (!authorization?.startsWith("Bearer ")) throw new Error("AUTHORIZATION_REQUIRED");
  const client = createClient(URL, ANON, { global: { headers: { Authorization: authorization } } });
  const { data, error } = await client.auth.getUser();
  if (error || !data.user) throw new Error("AUTHENTICATED_USER_REQUIRED");
  return { client, user: data.user };
}

async function logOp(client: any, userId: string, operation: string, status: string, input: any, output: any, sourceEventIds: string[] = []) {
  await client.from("nayanet_intelligence_operations").insert({
    user_id: userId, project_id: PROJECT, operation, status,
    input: input ?? {}, output: output ?? {}, source_event_ids: sourceEventIds
  });
}

async function record(client: any, event: any, action: string, expected: string, observed: string, learning: any[] = []) {
  const { data, error } = await client.rpc("nayanet_record_cognition_event", {
    p_project_id: PROJECT,
    p_event: event,
    p_action: action,
    p_expected_result: expected,
    p_observed_result: observed,
    p_learning: learning
  });
  if (error) throw error;
  return data;
}

async function restore(client: any, userId: string) {
  const [state, events, learning, replays, receipts, ops, bridge] = await Promise.all([
    admin.from("nayanet_project_intelligence_state")
      .select("*").eq("project_id", PROJECT).maybeSingle(),
    client.from("nayanet_cognition_events")
      .select("id,event_id,type,classification,title,content,source,status,confidence,tags,parent_event_id,source_hash,schema_version,metadata,created_at")
      .eq("user_id", userId).eq("project_id", PROJECT).order("created_at", { ascending: false }).limit(30),
    client.from("learning_evidence")
      .select("id,target_id,level,status,claim,observed_value,verification_method,source_event_id,created_at")
      .eq("member_id", userId).order("created_at", { ascending: false }).limit(20),
    client.from("nayanet_dream_replays")
      .select("id,source_event_id,source_receipt_id,policy_version,status,verification,replay_output,created_at")
      .eq("user_id", userId).eq("project_id", PROJECT).order("created_at", { ascending: false }).limit(10),
    client.from("nayanet_execution_receipts")
      .select("id,revision,action,expected_result,observed_result,status,evidence,learning,value,created_at")
      .eq("user_id", userId).eq("project_id", PROJECT).order("created_at", { ascending: false }).limit(20),
    client.from("nayanet_intelligence_operations")
      .select("id,operation,status,output,created_at")
      .eq("user_id", userId).eq("project_id", PROJECT).order("created_at", { ascending: false }).limit(20),
    admin.from("nayanet_project_intelligence_bridge")
      .select("packet_id,project_id,source_ref,content_hash,receiver_transaction_id,receiver_event_id,receipt_id,persisted,indexed,projected,retrieved,rendered,retrieval_evidence,render_evidence,acknowledged_at,verified_at,accepted_at")
      .eq("project_id", PROJECT).order("accepted_at", { ascending: false }).limit(10)
  ]);
  for (const r of [state, events, learning, replays, receipts, ops, bridge]) if (r.error) throw r.error;

  const current = events.data?.[0] ?? null;
  const latestLearning = learning.data?.filter((x: any) => x.status === "ACTIVE").slice(0, 10) ?? [];
  const latestReplay = replays.data?.[0] ?? null;
  const latestReceipt = receipts.data?.[0] ?? null;
  const latestBridge = bridge.data?.[0] ?? null;
  const canonicalState = state.data ?? null;

  const proven = [
    ...(Array.isArray(canonicalState?.proven) ? canonicalState.proven : []),
    ...(latestBridge ? ["Project Intelligence Bridge transaction exists at receiver scope."] : []),
    ...(latestBridge?.persisted && latestBridge?.indexed && latestBridge?.projected ? ["Bridge persistence/index/projection are evidenced."] : []),
    ...(latestBridge?.retrieved && latestBridge?.rendered ? ["Bridge retrieval/render are evidenced for the latest transaction."] : [])
  ];

  const unknown = [
    ...(Array.isArray(canonicalState?.unknown) ? canonicalState.unknown : []),
    ...(!latestBridge?.retrieved ? ["Direct receiver retrieval of the latest bridge object is not evidenced."] : []),
    ...(!latestBridge?.rendered ? ["Direct receiver render of the latest bridge object is not evidenced."] : [])
  ];

  const blocked = Array.isArray(canonicalState?.blocked) ? canonicalState.blocked : [];
  const protectedRules = Array.isArray(canonicalState?.protected) ? canonicalState.protected : [
    "UNKNOWN is not VERIFIED",
    "BLOCKED is not PASS",
    "Truth over agreement",
    "Private by default • Shared by choice • Collective by consent • Public by decision",
    "Capability does not create authority"
  ];

  return {
    schema: "NAYANET_PROJECT_INTELLIGENCE_RESTORE_V2",
    restored_at: new Date().toISOString(),
    source_authority: {
      repository: GITHUB_REPO,
      ref: GITHUB_REF,
      current_source_resolution: "Resolve live GitHub main at execution time; recorded HEAD is not authoritative.",
      control_plane: [".naya/control-plane/STATE.json",".naya/control-plane/BLOCKS.json",".naya/control-plane/PROOF.json"],
      current_frontier: ".naya/project-intelligence/CURRENT-FRONTIER.md",
      team_naya: ".naya/TEAM-NAYA/00-NAYANET-HUB-NORTH-STAR-MISSION-LOCK.md"
    },

    "1_WHO_ARE_WE": "We are Project NayaNET — Project Intelligence itself. Shawn is the human director. Nayas are operating instances. NayaPOWER is the governed operating substrate.",
    "2_WHAT_ARE_WE_BUILDING": "A persistent, governed, interoperable intelligence network that captures experience, preserves evidence, retrieves relevant intelligence, applies authorized action, verifies outcomes, learns, compounds, and hands off to the next Naya.",
    "3_WHY_ARE_WE_BUILDING_IT": "So valuable human intelligence does not disappear when a conversation or Naya instance ends, and so humans do not have to repeatedly reconstruct context or manage AI project-by-project.",
    "4_WHAT_DOES_SUCCESS_MEAN": "A cold Naya restores the project, distinguishes truth from uncertainty, knows authority, chooses one authorized next action, acts, verifies, learns, updates durable intelligence, leaves a successor context, and another cold Naya continues without Shawn reconstructing the project.",
    "5_WHAT_IS_TRUE_RIGHT_NOW": {
      project: PROJECT,
      canonical_hub: CANONICAL_HUB,
      active_block: "PROJECT-INTELLIGENCE-PI-01",
      state: canonicalState?.status ?? "UNKNOWN",
      current_next_action: canonicalState?.current_next_action ?? {"action":"Prove Project Intelligence restore + receiver retrieval/render + cold successor continuation as one governed runtime journey."},
      latest_event: current,
      latest_bridge: latestBridge
    },
    "6_WHAT_HAS_ALREADY_BEEN_PROVEN": proven,
    "7_WHAT_IS_UNKNOWN": unknown,
    "8_WHAT_AUTHORITY_EXISTS": {
      human_director: "Shawn Vibert",
      rule: "Capability does not create authority.",
      runtime_rule: "Authenticated user authority is required for user-scoped operations; system-wide state and receiver acknowledgements must not be treated as implicit permission to change human authority.",
      secrets: "Secrets and tokens are never exposed in conversation."
    },
    "9_WHAT_HAPPENED_PREVIOUSLY": {
      recent_events: events.data ?? [],
      recent_receipts: receipts.data ?? [],
      recent_operations: ops.data ?? [],
      recent_bridge: bridge.data ?? []
    },
    "10_WHAT_DID_WE_LEARN": {
      active_learning: latestLearning,
      durable_lessons: [
        "Evidence outranks assertion.",
        "IMPLEMENTED is not VERIFIED.",
        "Transport/persistence/index/projection do not imply retrieval/render.",
        "Repair the smallest causal boundary and rerun the same proof.",
        "The system must not depend on a Naya remembering to remember."
      ]
    },
    "11_WHAT_SHOULD_HAPPEN_NEXT": canonicalState?.current_next_action ?? {
      action: "Prove Project Intelligence restore + receiver retrieval/render + cold successor continuation as one governed runtime journey.",
      reason: "Remove manual archaeology and make architecture carry continuity."
    },
    "12_HOW_DO_I_PROVE_IT": {
      chain: ["INTENT","IDENTITY","RECONSTRUCTION","COLD_RESTORE","RETRIEVAL","CURRENT_STATE","ONE_NEXT_ACTION","AUTHORITY","EXECUTION","VERIFICATION","LEARNING","UPDATE","COLD_SUCCESSOR"],
      rule: "Stop at the first deterministic failure, capture exact evidence, repair only that causal boundary, rerun the same proof, and record the result."
    },
    "13_WHERE_DO_I_RECORD_IT": {
      canonical_intelligence: ".naya/",
      state: ".naya/control-plane/STATE.json",
      block: ".naya/control-plane/BLOCKS.json",
      proof: ".naya/control-plane/PROOF.json",
      frontier: ".naya/project-intelligence/CURRENT-FRONTIER.md",
      team_naya: "NAYA/ACTIVITY/ and .naya/TEAM-NAYA/",
      runtime_operations: "public.nayanet_intelligence_operations",
      bridge_proof: "public.nayanet_project_intelligence_bridge"
    },
    "14_HOW_DOES_THE_NEXT_NAYA_CONTINUE": "Read this restore object and its cited canonical sources, resolve live main, verify the latest evidence, identify the first incomplete boundary, execute only the authorized next action, verify it, record learning and successor state, then leave the next Naya a better torch.",
    YOU_ARE_HERE: {
      project: PROJECT,
      mission: MISSION,
      vision: "A persistent, governed, interoperable intelligence infrastructure in which intelligence compounds across time, experience, decisions, learning and Nayas.",
      north_star: NORTH_STAR,
      active_block: "PROJECT-INTELLIGENCE-PI-01"
    },
    MISSION,
    VISION: "A persistent, governed, interoperable intelligence infrastructure in which intelligence compounds across time, experience, decisions, learning and Nayas.",
    NORTH_STAR,
    CURRENT_PROJECT: PROJECT,
    CURRENT_STATE: canonicalState?.current_state ?? null,
    PROVEN: proven,
    UNKNOWN: unknown,
    BLOCKED: blocked,
    PROTECTED: protectedRules,
    CURRENT_HUB: {
      type: "nayanet_intelligent_hub",
      canonical_source: CANONICAL_HUB,
      rule: "One Hub. Internal runtime code is implementation machinery behind this source."
    },
    CURRENT_BRIDGE: {
      contract: ".naya/project-intelligence/PROJECT-INTELLIGENCE-BRIDGE-CONTRACT-V1.md",
      target: "RECEIVE → AUTHENTICATE → IDENTIFY → VALIDATE → STORE → INDEX → PROJECT → RETRIEVE → RENDER → ACKNOWLEDGE",
      latest: latestBridge
    },
    CURRENT_LEARNING: latestLearning,
    RECENT_OUTCOMES: receipts.data ?? [],
    ACTIVE_DECISIONS: canonicalState?.current_next_action ?? null,
    CURRENT_NEXT_ACTION: canonicalState?.current_next_action ?? null,
    WHY: "Remove manual archaeology and make architecture carry continuity.",
    SUCCESS_CONDITION: canonicalState?.current_next_action?.success_condition ?? "Cold Naya restores, retrieves, acts, verifies, learns and hands off.",
    EVIDENCE_REQUIRED: ["restore response","exact bridge lineage","retrieval evidence","render evidence","execution/verification receipt","cold successor receipt","continuation outcome"],
    HANDOFF_REQUIREMENT: "Leave what happened, what changed, what was learned, unknowns, blocks, protections, next action, why, and evidence required.",
    successor_requirement: "Leave a durable successor context containing what happened, what changed, what was learned, what remains unknown, what is blocked, what is protected, the next action, why, and the evidence required."
  };
}

async function retrieve(client: any, userId: string, body: any) {
  const q = String(body.query ?? "").trim();
  if (!q) throw new Error("QUERY_REQUIRED");
  const limit = Math.min(Math.max(Number(body.limit ?? 20), 1), 50);
  const result = await client.from("nayanet_cognition_events")
    .select("id,event_id,type,classification,title,content,source,status,confidence,tags,parent_event_id,source_hash,schema_version,metadata,created_at")
    .eq("user_id", userId).eq("project_id", PROJECT)
    .or("title.ilike.%"+q+"%,content.ilike.%"+q+"%,type.ilike.%"+q+"%,classification.ilike.%"+q+"%")
    .order("created_at", { ascending: false }).limit(limit);
  if (result.error) throw result.error;
  return { schema: "NAYANET_PROJECT_INTELLIGENCE_RETRIEVE_V1", query: q, count: result.data?.length ?? 0, items: result.data ?? [] };
}

async function reconcile(client: any, userId: string) {
  const [ops, bridge] = await Promise.all([
    client.from("nayanet_intelligence_operations").select("operation,status,created_at,output").eq("user_id", userId).order("created_at",{ascending:false}).limit(20),
    admin.from("nayanet_project_intelligence_bridge").select("packet_id,source_ref,content_hash,persisted,indexed,projected,accepted_at").order("accepted_at",{ascending:false}).limit(5)
  ]);
  if (ops.error) throw ops.error;
  if (bridge.error) throw bridge.error;
  const latest = bridge.data?.[0] ?? null;
  return {
    schema: "NAYANET_INTELLIGENCE_RECONCILIATION_V1",
    status: latest ? "TRANSPORT_PROVEN_RETRIEVAL_OPEN" : "NO_BRIDGE_RECEIPT",
    bridge: latest ? {
      packet_id: latest.packet_id, source_ref: latest.source_ref,
      persisted: latest.persisted, indexed: latest.indexed, projected: latest.projected,
      accepted_at: latest.accepted_at,
      retrieval: "NOT_YET_EVIDENCED_BY_THIS RECONCILIATION"
    } : null,
    user_operations: ops.data ?? [],
    rule: "Runtime proof outranks stale documentation; transport flags are not retrieval/render proof."
  };
}

async function learningRetrieve(client: any, userId: string, body: any) {
  const q = String(body.query ?? "").trim();
  const limit = Math.min(Math.max(Number(body.limit ?? 20), 1), 50);
  let query = client.from("learning_evidence")
    .select("id,target_id,level,status,claim,observed_value,verification_method,source_event_id,created_at")
    .eq("member_id", userId).eq("status", "ACTIVE").order("created_at",{ascending:false}).limit(limit);
  if (q) query = query.or("claim.ilike.%"+q+"%,target_id.ilike.%"+q+"%,verification_method.ilike.%"+q+"%");
  const {data,error}=await query;
  if(error) throw error;
  return {schema:"NAYANET_LEARNING_RETRIEVE_V1",query:q,count:data?.length??0,items:data??[]};
}

async function projectIntelligence(client: any, userId: string, body: any) {
  const sourceId=String(body.source_event_id??"").trim();
  if(!sourceId) throw new Error("SOURCE_EVENT_ID_REQUIRED");
  const {data:event,error:eventError}=await client.from("nayanet_cognition_events")
    .select("id,event_id,title,type,status,created_at,metadata").eq("id",sourceId).eq("user_id",userId).eq("project_id",PROJECT).single();
  if(eventError||!event) throw new Error("SOURCE_EVENT_NOT_FOUND");
  const {data:existing,error:existingError}=await client.from("nayanet_intelligence_index")
    .select("id,revision,updated_at").eq("owner_id",userId).eq("source_table","nayanet_cognition_events").eq("source_id",sourceId).maybeSingle();
  if(existingError) throw existingError;
  let row:any=existing;
  if(row){
    const {data,error}=await client.from("nayanet_intelligence_index").update({
      title:event.title,event_time:event.created_at,status:event.status,project_id:PROJECT,
      revision:Number(row.revision??0)+1,metadata:{...(event.metadata??{}),projection_source:event.event_id,projected_at:new Date().toISOString()}
    }).eq("id",row.id).select("*").single();
    if(error) throw error;
    row=data;
  } else {
    const {data,error}=await client.from("nayanet_intelligence_index").insert({
      owner_id:userId,source_table:"nayanet_cognition_events",source_id:sourceId,object_type:event.type,
      title:event.title,event_time:event.created_at,status:event.status,project_id:PROJECT,revision:1,
      metadata:{...(event.metadata??{}),projection_source:event.event_id,projected_at:new Date().toISOString()}
    }).select("*").single();
    if(error) throw error;
    row=data;
  }
  return {schema:"NAYANET_PROJECT_INTELLIGENCE_PROJECT_V1",status:"PROJECTED",index:row,source_event:event};
}

async function ackBridge(client: any, userId: string, body: any) {
  const packetId=String(body.packet_id??"").trim();
  if(!packetId) throw new Error("PACKET_ID_REQUIRED");
  const retrievalEvidence=Array.isArray(body.retrieval_evidence)?body.retrieval_evidence:[];
  const renderEvidence=Array.isArray(body.render_evidence)?body.render_evidence:[];
  const retrieved=body.retrieved===true;
  const rendered=body.rendered===true;
  if(!retrieved || !rendered || retrievalEvidence.length===0 || renderEvidence.length===0) {
    throw new Error("ACK_REQUIRES_RETRIEVED_RENDERED_AND_EVIDENCE");
  }
  const existing=await admin.from("nayanet_project_intelligence_bridge").select("*").eq("packet_id",packetId).single();
  if(existing.error||!existing.data) throw new Error("BRIDGE_PACKET_NOT_FOUND");
  const now=new Date().toISOString();
  const {data,error}=await admin.from("nayanet_project_intelligence_bridge").update({
    retrieved:true,rendered:true,retrieval_evidence:retrievalEvidence,render_evidence:renderEvidence,
    acknowledged_at:now,verified_at:now
  }).eq("packet_id",packetId).select("*").single();
  if(error) throw error;
  return {
    schema:"NAYANET_PROJECT_INTELLIGENCE_ACK_V1",
    packet_id:packetId,source_ref:existing.data.source_ref,content_hash:existing.data.content_hash,
    receiver_transaction_id:existing.data.receiver_transaction_id,receiver_event_id:existing.data.receiver_event_id,
    receipt_id:existing.data.receipt_id,persisted:existing.data.persisted,indexed:existing.data.indexed,
    projected:existing.data.projected,retrieved:true,rendered:true,acknowledged_at:now,verified_at:now,
    actor:userId,record:data
  };
}

async function stateUpdate(client: any, userId: string, body: any) {
  const {data:member,error:memberError}=await client.from("members").select("id,display_name").eq("id",userId).maybeSingle();
  if(memberError) throw memberError;
  if(!member) throw new Error("MEMBER_NOT_FOUND");
  const {data:current,error:readError}=await admin.from("nayanet_project_intelligence_state").select("*").eq("project_id",PROJECT).single();
  if(readError) throw readError;
  const allowed=["current_state","current_next_action","unknown","blocked","protected","evidence_refs"];
  const patch:any={updated_at:new Date().toISOString(),version:Number(current.version??1)+1};
  for(const key of allowed) if(Object.prototype.hasOwnProperty.call(body,key)) patch[key]=body[key];
  if(Object.keys(patch).length===2) throw new Error("STATE_PATCH_REQUIRED");
  const {data,error}=await admin.from("nayanet_project_intelligence_state").update(patch).eq("project_id",PROJECT).select("*").single();
  if(error) throw error;
  return {schema:"NAYANET_PROJECT_INTELLIGENCE_STATE_UPDATE_V1",status:"UPDATED",actor:userId,operator:member.display_name,state:data};
}

async function understand(client: any, userId: string, body: any) {
  const content = String(body.content ?? "").trim();
  if (!content) throw new Error("CONTENT_REQUIRED");
  const eventId = "understanding:" + crypto.randomUUID();
  const event = {
    event_id: eventId, type: "understanding", classification: "interpretation",
    title: String(body.title ?? "Project Intelligence understanding"),
    content, source: "nayanet-compound-intelligence", status: "active", actor: "naya",
    confidence: Number.isFinite(Number(body.confidence)) ? Number(body.confidence) : 0.8,
    tags: Array.isArray(body.tags) ? body.tags : ["project-intelligence","understanding"],
    parent_event_id: body.parent_event_id ?? null,
    source_hash: "understanding:" + eventId, schema_version: "1.0.0",
    metadata: { interpretation: true, human_verified: false, generated_at: new Date().toISOString() }
  };
  const receipt = await record(client,event,"understand_project_intelligence","Understanding persisted","Canonical understanding event persisted.");
  return { event, receipt, caution: "Interpretation is not verified fact until evidence promotes it." };
}

async function learningCandidate(client: any, userId: string, body: any) {
  const claim = String(body.claim ?? "").trim();
  const target = String(body.target_id ?? "").trim();
  const sourceEvent = body.source_event_id ? String(body.source_event_id) : null;
  if (!claim || !target) throw new Error("CLAIM_AND_TARGET_REQUIRED");
  if (!sourceEvent) throw new Error("SOURCE_EVENT_ID_REQUIRED_FOR_CANDIDATE");
  const { data: source } = await client.from("nayanet_cognition_events").select("id,event_id").eq("event_id",sourceEvent).eq("user_id",userId).eq("project_id",PROJECT).maybeSingle();
  if (!source) throw new Error("SOURCE_EVENT_NOT_FOUND");
  const row = {
    member_id: userId, target_id: target, level: String(body.level ?? "E1_UNDERSTANDS"),
    provenance: String(body.provenance ?? "nayanet-compound-intelligence"),
    status: "CANDIDATE", claim,
    observed_value: body.observed_value ?? {},
    verification_method: String(body.verification_method ?? "PENDING_VERIFICATION"),
    source_event_id: sourceEvent
  };
  const { data, error } = await client.from("learning_evidence").insert(row).select("*").single();
  if (error) throw error;
  return { status: "CANDIDATE", learning: data };
}

async function learningVerify(client: any, userId: string, body: any) {
  const id = String(body.evidence_id ?? "").trim();
  const method = String(body.verification_method ?? "").trim();
  const evidenceRefs = Array.isArray(body.evidence_refs) ? body.evidence_refs : [];
  if (!id || !method) throw new Error("EVIDENCE_ID_AND_VERIFICATION_METHOD_REQUIRED");
  if (evidenceRefs.length === 0 && !body.observed_value) throw new Error("VERIFICATION_EVIDENCE_REQUIRED");
  const { data: evidence, error: readError } = await client.from("learning_evidence").select("*").eq("id",id).eq("member_id",userId).single();
  if (readError || !evidence) throw new Error("LEARNING_EVIDENCE_NOT_FOUND");
  if (evidence.status !== "CANDIDATE" && evidence.status !== "ACTIVE") throw new Error("LEARNING_EVIDENCE_NOT_PROMOTABLE");
  const observed = body.observed_value ?? evidence.observed_value;
  const { data, error } = await client.from("learning_evidence").update({
    status: "ACTIVE", verification_method: method, observed_value: observed
  }).eq("id",id).eq("member_id",userId).select("*").single();
  if (error) throw error;
  return { status: "VERIFIED_LEARNING", learning: data, rule: "Verification promotes evidence; it does not change authority or policy by itself." };
}

async function successor(client: any, userId: string, body: any) {
  const restored = await restore(client,userId);
  const successorEvent = {
    event_id: "successor:" + crypto.randomUUID(), type: "successor_handoff", classification: "continuity",
    title: "Next Naya successor context", content: JSON.stringify({
      what_happened: body.what_happened ?? restored.CURRENT_STATE,
      what_changed: body.what_changed ?? null,
      learned: body.learned ?? restored.RECENT_LEARNING,
      unknown: restored.UNKNOWN, blocked: restored.BLOCKED, protected: restored.PROTECTED,
      next_action: body.next_action ?? restored.CURRENT_NEXT_ACTION,
      why: body.why ?? "Continue the highest verified value path.",
      evidence_required: body.evidence_required ?? "Verify the outcome and persist the evidence.",
      source_restore: restored.YOU_ARE_HERE
    }), source: "nayanet-compound-intelligence", status: "active", actor: "naya",
    confidence: 1, tags: ["successor","continuity","cold-naya"], parent_event_id: body.parent_event_id ?? null,
    source_hash: "successor", schema_version: "1.0.0", metadata: { restore_schema: restored.schema }
  };
  const receipt = await record(client,successorEvent,"successor_handoff","Successor context persisted","Next-Naya continuation context persisted.");
  return { successor: successorEvent, receipt };
}

async function share(client: any, userId: string, body: any) {
  const sourceId = String(body.source_event_id ?? "").trim();
  if (!sourceId) throw new Error("SOURCE_EVENT_ID_REQUIRED");
  const own = await client.from("nayanet_cognition_events").select("id,event_id,title,content").eq("id",sourceId).eq("user_id",userId).single();
  if (own.error || !own.data) throw new Error("SOURCE_NOT_OWNED");
  const result = await client.from("nayanet_intelligence_publications").upsert({
    intelligence_event_id: sourceId, owner_id: userId, status: "published",
    consent_state: "explicit", published_at: new Date().toISOString(), updated_at: new Date().toISOString()
  },{onConflict:"intelligence_event_id"}).select("*").single();
  if (result.error) throw result.error;
  return { status:"SHARED_BY_EXPLICIT_CONSENT", publication:result.data };
}

async function supersede(client: any, userId: string, body: any) {
  const oldId = String(body.superseded_event_id ?? "").trim();
  const content = String(body.content ?? "").trim();
  if (!oldId || !content) throw new Error("SUPERSEDED_EVENT_AND_CONTENT_REQUIRED");
  const old = await client.from("nayanet_cognition_events").select("event_id").eq("id",oldId).eq("user_id",userId).single();
  if (old.error || !old.data) throw new Error("SUPERSEDED_EVENT_NOT_OWNED");
  const event = {
    event_id: "supersede:" + crypto.randomUUID(), type:"intelligence_revision", classification:"supersession",
    title:String(body.title ?? "Superseding intelligence"), content, source:"nayanet-compound-intelligence",
    status:"active", actor:"naya", confidence:Number(body.confidence ?? 1), tags:["intelligence","supersedes"],
    parent_event_id:old.data.event_id, source_hash:"supersede", schema_version:"1.0.0",
    metadata:{supersedes:old.data.event_id, reason:String(body.reason ?? "New verified evidence")}
  };
  const receipt=await record(client,event,"supersede_intelligence","New intelligence revision persisted","Superseding event persisted with explicit lineage.");
  return {event,receipt,lineage:{supersedes:old.data.event_id}};
}

async function health(client: any, userId: string) {
  const [e,l,r,d,o] = await Promise.all([
    client.from("nayanet_cognition_events").select("id",{count:"exact",head:true}).eq("user_id",userId).eq("project_id",PROJECT),
    client.from("learning_evidence").select("id",{count:"exact",head:true}).eq("member_id",userId),
    client.from("nayanet_execution_receipts").select("id",{count:"exact",head:true}).eq("user_id",userId).eq("project_id",PROJECT),
    client.from("nayanet_dream_replays").select("id",{count:"exact",head:true}).eq("user_id",userId).eq("project_id",PROJECT),
    client.from("nayanet_intelligence_operations").select("id",{count:"exact",head:true}).eq("user_id",userId).eq("project_id",PROJECT)
  ]);
  for(const x of [e,l,r,d,o]) if(x.error) throw x.error;
  return {schema:"NAYANET_INTELLIGENCE_HEALTH_V1",status:"OBSERVED",counts:{cognition:e.count??0,learning:l.count??0,receipts:r.count??0,dream:d.count??0,operations:o.count??0},laws:["unknown_not_verified","blocked_not_pass","truth_over_agreement","capability_does_not_create_authority"]};
}

Deno.serve(async (req) => {
  if(req.method==="OPTIONS") return new Response("ok",{headers:cors});
  if(req.method!=="POST") return json({ok:false,error:"METHOD_NOT_ALLOWED"},405);
  let ctx:any;
  try { ctx = await auth(req); } catch(e) { return json({ok:false,error:String(e?.message||e)},401); }
  const { client, user } = ctx;
  let body:any={}; try { body=await req.json(); } catch {}
  const action=String(body.action||"restore").trim();
  try {
    let result:any;
    switch(action) {
      case "restore": result=await restore(client,user.id); break;
      case "retrieve": result=await retrieve(client,user.id,body); break;
      case "reconcile": result=await reconcile(client,user.id); break;
      case "understand": result=await understand(client,user.id,body); break;
      case "learning_candidate": result=await learningCandidate(client,user.id,body); break;
      case "learning_verify": result=await learningVerify(client,user.id,body); break;
      case "learning_retrieve": result=await learningRetrieve(client,user.id,body); break;
      case "project": result=await projectIntelligence(client,user.id,body); break;
      case "ack": result=await ackBridge(client,user.id,body); break;
      case "state_update": result=await stateUpdate(client,user.id,body); break;
      case "successor_handoff": result=await successor(client,user.id,body); break;
      case "share": result=await share(client,user.id,body); break;
      case "supersede": result=await supersede(client,user.id,body); break;
      case "health": result=await health(client,user.id); break;
      case "dream": {
        const dreamUrl = `${URL}/functions/v1/naya-dream-replay`;
        const dreamHeaders:any = { "Authorization": req.headers.get("Authorization")!, "apikey": ANON, "Content-Type": "application/json" };
        const dreamBody = { ...body, project_id: PROJECT, idempotency_key: body.idempotency_key ?? req.headers.get("x-idempotency-key") ?? ("compound-dream-" + crypto.randomUUID()) };
        const dreamResponse = await fetch(dreamUrl, { method: "POST", headers: dreamHeaders, body: JSON.stringify(dreamBody) });
        const dreamResult = await dreamResponse.json().catch(() => ({}));
        if (!dreamResponse.ok || dreamResult?.ok !== true) throw new Error("DREAM_REPLAY_DELEGATE_FAILED:" + JSON.stringify(dreamResult));
        result = { schema: "NAYANET_COMPOUND_DREAM_SEAM_V2", delegated: true, replay: dreamResult.replay, idempotent: dreamResult.idempotent === true };
        break;
      }
      case "compound": {
        const restored=await restore(client,user.id);
        result={schema:"NAYANET_COMPOUND_INTELLIGENCE_CYCLE_V1",stages:["EXPERIENCE","CAPTURE","UNDERSTAND","RETAIN","RETRIEVE","DECIDE","ACT","VERIFY","LEARN","DREAM","APPLY","SUCCESSOR"],current_context:restored.YOU_ARE_HERE,next:"Use verified context to choose one authorized action, then persist outcome and successor context.",automation_boundary:"No silent authority escalation or unverified learning promotion."};
        break;
      }
      default: throw new Error("UNKNOWN_ACTION");
    }
    await logOp(client,user.id,action,"SUCCESS",body,result);
    return json({ok:true,action,result});
  } catch(e) {
    const detail=String(e?.message||e);
    try { await logOp(client,user.id,action,"FAILED",body,{error:detail}); } catch {}
    return json({ok:false,action,error:detail},400);
  }
});