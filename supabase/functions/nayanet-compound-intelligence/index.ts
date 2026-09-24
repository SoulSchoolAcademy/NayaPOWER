// PI deterministic reconstruction timezone normalization verified 2026-09-21
import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "npm:@supabase/supabase-js@2";

const URL = Deno.env.get("SUPABASE_URL")!;
const ANON = Deno.env.get("SUPABASE_ANON_KEY")!;
const SECRET = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const admin = createClient(URL, SECRET);
const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization,apikey,content-type,x-idempotency-key,x-client-info,traceparent,tracestate,baggage",
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

async function validateIntelligenceCommitAuthority(client: any, authorityGrantId: string) {
  const { data, error } = await client.rpc("nayanet_validate_authority_grant", {
    p_grant_id: authorityGrantId,
    p_action: "intelligence_commit",
    p_target: PROJECT
  });
  if (error) throw error;
  if (data?.status !== "AUTHORIZED") {
    throw new Error("AUTHORITY_REQUIRED:" + String(data?.reason ?? "AUTHORIZATION_BLOCKED"));
  }
  return data;
}

async function record(client: any, event: any, action: string, expected: string, observed: string, learning: any[] = [], executionAuthorization: any = null) {
  const { data, error } = await client.rpc("nayanet_record_cognition_event", {
    p_project_id: PROJECT,
    p_event: event,
    p_action: action,
    p_expected_result: expected,
    p_observed_result: observed,
    p_learning: learning,
    p_execution_authorization: executionAuthorization
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
    "QUESTION_METADATA": {
      "rule": "Every consequential answer carries status, source_path, source_scope, evidence_identity, freshness, next_responsible_action.",
      "items": {
        "1_WHO_ARE_WE": {"status":"DOCUMENTED","source_path":".naya/project-intelligence/COLD-NAYA-14-QUESTION-RECONSTRUCTION-CONTRACT.md","source_scope":"Project Intelligence identity","evidence_identity":"cold-naya-14-contract-v1","freshness":"reconcile live main at execution","next_responsible_action":"preserve canonical identity"},
        "2_WHAT_ARE_WE_BUILDING": {"status":"DOCUMENTED","source_path":".naya/project-intelligence/PROJECT-INTELLIGENCE-OPERATING-CONTEXT.json","source_scope":"NayaNET mission and operating model","evidence_identity":"project-intelligence-operating-context-v1","freshness":"reconcile live main at execution","next_responsible_action":"execute only the active P0 block"},
        "3_WHY_ARE_WE_BUILDING_IT": {"status":"DOCUMENTED","source_path":".naya/control-plane/STATE.json","source_scope":"mission/north-star","evidence_identity":"control-plane-state","freshness":"live HEAD plus canonical state","next_responsible_action":"maximize verified human value with continuity"},
        "4_WHAT_DOES_SUCCESS_MEAN": {"status":"DOCUMENTED","source_path":".naya/control-plane/BLOCKS.json","source_scope":"PI-01 acceptance","evidence_identity":"PROJECT-INTELLIGENCE-PI-01","freshness":"live block reconciliation required","next_responsible_action":"complete all acceptance boundaries"},
        "5_WHAT_IS_TRUE_RIGHT_NOW": {"status":"CURRENT_REQUIRES_LIVE_RECONCILIATION","source_path":".naya/control-plane/STATE.json","source_scope":"live repository/control plane/runtime evidence","evidence_identity":"live-head-resolution","freshness":"LIVE_AT_EXECUTION_TIME","next_responsible_action":"resolve live main before consequential action"},
        "6_WHAT_HAS_ALREADY_BEEN_PROVEN": {"status":"PROVEN_AT_RECORDED_SCOPES","source_path":".naya/control-plane/PROOF.json","source_scope":"claim-specific evidence","evidence_identity":"proof-registry","freshness":"source-scope dependent","next_responsible_action":"never generalize beyond recorded scope"},
        "7_WHAT_IS_UNKNOWN": {"status":"UNKNOWN_UNTIL_PROVEN","source_path":".naya/project-intelligence/CURRENT-FRONTIER.md","source_scope":"current frontier","evidence_identity":"frontier-open-boundaries","freshness":"reconcile after every proof","next_responsible_action":"attack the first open causal boundary"},
        "8_WHAT_AUTHORITY_EXISTS": {"status":"GOVERNED","source_path":".naya/codex/11-RUNTIME-CONSTITUTION.md","source_scope":"authority and fail-closed execution","evidence_identity":"runtime-constitution","freshness":"canonical law","next_responsible_action":"check authority before consequential action"},
        "9_WHAT_HAPPENED_PREVIOUSLY": {"status":"PROVEN_HISTORY","source_path":".naya/control-plane/PROOF.json","source_scope":"execution history and receipts","evidence_identity":"proof-and-receipt-lineage","freshness":"historical evidence; reconcile current state","next_responsible_action":"reuse verified lessons, not stale assumptions"},
        "10_WHAT_DID_WE_LEARN": {"status":"VERIFIED_ENGINEERING_LESSONS","source_path":".naya/control-plane/PROOF.json","source_scope":"failure/repair learning","evidence_identity":"causal-boundary-lessons","freshness":"durable unless superseded","next_responsible_action":"repair smallest causal boundary and rerun proof"},
        "11_WHAT_SHOULD_HAPPEN_NEXT": {"status":"ACTIVE_NEXT_ACTION","source_path":".naya/control-plane/BLOCKS.json","source_scope":"single-next-action contract","evidence_identity":"PI-01-next-action","freshness":"live block state","next_responsible_action":"execute exactly one highest-value authorized action"},
        "12_HOW_DO_I_PROVE_IT": {"status":"CANONICAL_PROOF_METHOD","source_path":".naya/control-plane/PROOF.json","source_scope":"claim evidence and freshness rules","evidence_identity":"proof-contract","freshness":"canonical unless amended","next_responsible_action":"capture claim-appropriate evidence"},
        "13_WHERE_DO_I_RECORD_IT": {"status":"CANONICAL_RECORDING_CONTRACT","source_path":".naya/project-intelligence/COLD-NAYA-14-QUESTION-RECONSTRUCTION-CONTRACT.md","source_scope":"state/block/proof/frontier/runtime records","evidence_identity":"recording-contract-v1","freshness":"reconcile live paths","next_responsible_action":"record durable state and receipt"},
        "14_HOW_DOES_THE_NEXT_NAYA_CONTINUE": {"status":"CANONICAL_SUCCESSOR_CONTRACT","source_path":".naya/project-intelligence/COLD-NAYA-14-QUESTION-RECONSTRUCTION-CONTRACT.md","source_scope":"successor torch","evidence_identity":"successor-contract-v1","freshness":"reconcile after each execution","next_responsible_action":"leave a runnable successor with one next action"}
      }
    },
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

async function coldRestore(client: any, userId: string) {
  const restored = await restore(client, userId);
  const requiredQuestions = Array.from({ length: 14 }, (_, i) => `${i + 1}_`);
  const missing = requiredQuestions.filter((prefix) =>
    !Object.keys(restored).some((key) => key.startsWith(prefix))
  );
  if (missing.length) throw new Error("COLD_RESTORE_CONTRACT_INCOMPLETE:" + missing.join(","));
  const metadata = restored.QUESTION_METADATA?.items ?? {};
  const missingMetadata = requiredQuestions.filter((prefix) =>
    !Object.keys(metadata).some((key) => key.startsWith(prefix))
  );
  if (missingMetadata.length) throw new Error("COLD_RESTORE_METADATA_INCOMPLETE:" + missingMetadata.join(","));
  return {
    schema: "NAYANET_COLD_NAYA_RESTORE_V1",
    status: "COLD_RESTORE_VERIFIED",
    mandatory_pre_action: true,
    question_count: 14,
    questions: restored,
    contract: ".naya/project-intelligence/COLD-NAYA-14-QUESTION-RECONSTRUCTION-CONTRACT.md",
    rule: "Resolve canonical Project Intelligence before consequential Universal Agent Interface action."
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
    const {data,error}=await admin.from("nayanet_intelligence_index").update({
      title:event.title,event_time:event.created_at,status:event.status,project_id:PROJECT,
      revision:Number(row.revision??0)+1,metadata:{...(event.metadata??{}),projection_source:event.event_id,projected_at:new Date().toISOString()}
    }).eq("id",row.id).select("*").single();
    if(error) throw error;
    row=data;
  } else {
    const {data,error}=await admin.from("nayanet_intelligence_index").insert({
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
  if (body.authority !== "PROJECT_DIRECTOR") throw new Error("STATE_UPDATE_AUTHORITY_REQUIRED");
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
    provenance: String(body.provenance ?? "OBSERVATION"),
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

async function issuePiAuthority(client: any, userId: string, body: any) {
  const sourceEventId=String(body.source_event_id ?? "").trim();
  const target=String(body.target ?? "").trim();
  if(!sourceEventId || !target) throw new Error("AUTHORITY_SOURCE_AND_TARGET_REQUIRED");
  const {data:grant,error}=await client.rpc("nayanet_issue_authority_grant",{
    p_subject_id:userId,
    p_source_event_id:sourceEventId,
    p_mission_id:"NayaNET Project Intelligence",
    p_scope:{project_id:PROJECT,target},
    p_actions:["pi.continue"],
    p_constraints:{single_use:true},
    p_evidence:{reason:"cold-successor Project Intelligence continuation"}
  });
  if(error) throw error;
  return {schema:"NAYANET_PROJECT_INTELLIGENCE_AUTHORITY_V1",status:"AUTHORIZED",grant};
}

async function continueAuthorized(client: any, userId: string, body: any) {
  const grantId=String(body.authority_grant_id ?? "").trim();
  const parentEventId=String(body.parent_event_id ?? "").trim();
  if(!grantId || !parentEventId) throw new Error("AUTHORITY_GRANT_AND_PARENT_EVENT_REQUIRED");
  const {data:grant,error:grantError}=await client.from("nayanet_authority_grants")
    .select("grant_id,issuer_id,subject_id,mission_id,scope,actions,status,expires_at,evidence")
    .eq("grant_id",grantId).eq("issuer_id",userId).eq("subject_id",userId).eq("status","ACTIVE").maybeSingle();
  if(grantError) throw grantError;
  if(!grant) throw new Error("ACTIVE_AUTHORITY_GRANT_NOT_FOUND");
  if(grant.expires_at && new Date(grant.expires_at).getTime() <= Date.now()) throw new Error("AUTHORITY_GRANT_EXPIRED");
  const actions=Array.isArray(grant.actions)?grant.actions.map(String):[];
  if(!actions.includes("pi.continue")) throw new Error("AUTHORIZED_ACTION_NOT_GRANTED");
  const scope=(grant.scope && typeof grant.scope==="object")?grant.scope:{};
  if(String(scope.project_id ?? "") !== PROJECT) throw new Error("AUTHORITY_SCOPE_PROJECT_MISMATCH");
  if(String(scope.target ?? "") !== parentEventId) throw new Error("AUTHORITY_SCOPE_TARGET_MISMATCH");
  const {data:parent,error:parentError}=await client.from("nayanet_cognition_events")
    .select("id,event_id,title").eq("event_id",parentEventId).eq("user_id",userId).eq("project_id",PROJECT).maybeSingle();
  if(parentError) throw parentError;
  if(!parent) throw new Error("PARENT_EVENT_NOT_FOUND");
  const continuationEvent={
    event_id:"continuation:"+crypto.randomUUID(),
    type:"project_intelligence_continuation",
    classification:"authorized_continuation",
    title:"Authorized Project Intelligence continuation",
    content:JSON.stringify({
      action:"pi.continue",
      parent_event_id:parentEventId,
      authority_grant_id:grantId,
      mission_id:grant.mission_id,
      outcome:body.outcome ?? "Authorized successor continuation executed and verified.",
      source_head:body.source_head ?? null
    }),
    source:"nayanet-compound-intelligence",
    status:"verified",
    actor:"naya",
    confidence:1,
    tags:["project-intelligence","continuation","authorized","cold-successor"],
    parent_event_id:parentEventId,
    source_hash:"continuation:"+parentEventId,
    schema_version:"1.0.0",
    metadata:{
      authority_grant_id:grantId,
      mission_id:grant.mission_id,
      authorized_action:"pi.continue",
      verified:true
    }
  };
  const receipt=await record(
    client,
    continuationEvent,
    "pi.authorized_continuation",
    "Authorized Project Intelligence continuation executed",
    "Authorized continuation executed against the exact owner-bound parent event.",
    [{
      type:"authority",
      grant_id:grantId,
      action:"pi.continue",
      scope,
      parent_event_id:parentEventId
    }]
  );
  return {
    schema:"NAYANET_PROJECT_INTELLIGENCE_AUTHORIZED_CONTINUATION_V1",
    status:"CONTINUATION_VERIFIED",
    continuation_event:continuationEvent,
    receipt,
    authority:{
      grant_id:grantId,
      mission_id:grant.mission_id,
      action:"pi.continue",
      scope
    }
  };
}

async function consolidatePiGates(client: any, userId: string, body: any) {
  const flags = body.flags ?? {};
  const required = ["CANONICAL_CURRENT_TRUTH_RESOLUTION","FULL_PROJECT_INTELLIGENCE_RECONSTRUCTION","COLD_NAYA_CONSUMPTION","COLD_SUCCESSOR_CONTINUATION"];
  if(required.some(k=>flags[k]!==true)) throw new Error("PI_GATE_CONSOLIDATION_REQUIRES_ALL_FOUR_PASS");
  const sourceHead=String(body.source_head ?? "").trim();
  const proofRunId=String(body.proof_run_id ?? "").trim();
  if(!sourceHead || !proofRunId) throw new Error("PI_GATE_SOURCE_HEAD_AND_RUN_REQUIRED");
  const event={
    event_id:"pi-gates:"+crypto.randomUUID(),
    type:"project_intelligence_gate_consolidation",
    classification:"proof_consolidation",
    title:"Project Intelligence four-gate current-head consolidation",
    content:JSON.stringify({flags,source_head:sourceHead,proof_run_id:proofRunId,evidence_refs:Array.isArray(body.evidence_refs)?body.evidence_refs:[]}),
    source:"nayanet-compound-intelligence",
    status:"verified",
    actor:"naya",
    confidence:1,
    tags:["project-intelligence","proof","consolidated-gates"],
    parent_event_id:body.parent_event_id ?? null,
    source_hash:"pi-gates:"+sourceHead+":"+proofRunId,
    schema_version:"1.0.0",
    metadata:{flags,source_head:sourceHead,proof_run_id:proofRunId,verified:true}
  };
  const receipt=await record(client,event,"pi.gates.consolidated","All four Project Intelligence acceptance gates passed","Current-head cold-successor proof consolidated the four PI gates.",[...required.map(k=>({gate:k,status:"PASS"})),{source_head:sourceHead,proof_run_id:proofRunId,evidence_refs:body.evidence_refs??[]}]);
  return {schema:"NAYANET_PROJECT_INTELLIGENCE_GATE_CONSOLIDATION_V1",status:"PI_GATES_CONSOLIDATED",event,receipt,flags,source_head:sourceHead,proof_run_id:proofRunId};
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
  const blockId = String(body.superseded_block_id ?? "").trim();
  const content = String(body.content ?? "").trim();
  const idempotencyKey = String(body.idempotency_key ?? "").trim();
  if (!oldId || !content) throw new Error("SUPERSEDED_EVENT_AND_CONTENT_REQUIRED");
  if (!idempotencyKey) throw new Error("SUPERSEDE_IDEMPOTENCY_KEY_REQUIRED");
  const old = await client.from("nayanet_cognition_events").select("id,event_id,title,type,status,metadata").eq("id",oldId).eq("user_id",userId).single();
  if (old.error || !old.data) throw new Error("SUPERSEDED_EVENT_NOT_OWNED");
  if (!blockId) throw new Error("SUPERSEDED_BLOCK_ID_REQUIRED");
  const requestedNewBlockId = String(body.new_block_id ?? "").trim();
  if (requestedNewBlockId) {
    const replay = await client.from("nayanet_intelligent_blocks").select("*").eq("block_id",requestedNewBlockId).eq("owner_id",userId).maybeSingle();
    if (replay.error) throw replay.error;
    if (replay.data) {
      if (String(replay.data.provenance?.idempotency_key ?? "") !== idempotencyKey) throw new Error("SUPERSEDE_IDEMPOTENCY_KEY_MISMATCH");
      return {event:null,receipt:null,replayed:true,lineage:{superseded_block_id:blockId,new_block_id:requestedNewBlockId},intelligent_block:replay.data};
    }
  }
  const oldBlock = await client.from("nayanet_intelligent_blocks").select("*").eq("block_id",blockId).eq("owner_id",userId).single();
  if (oldBlock.error || !oldBlock.data) throw new Error("SUPERSEDED_BLOCK_NOT_OWNED");
  const event = {
    event_id: "supersede:" + crypto.randomUUID(), type:"intelligence_revision", classification:"supersession",
    title:String(body.title ?? "Superseding intelligence"), content, source:"nayanet-compound-intelligence",
    status:"active", actor:"naya", confidence:Number(body.confidence ?? 1), tags:["intelligence","supersedes"],
    parent_event_id:old.data.event_id, source_hash:"supersede", schema_version:"1.0.0",
    metadata:{supersedes:old.data.event_id, supersedes_block_id:blockId, reason:String(body.reason ?? "New verified evidence")}
  };
  const receipt=await record(client,event,"supersede_intelligence","New intelligence revision persisted","Superseding event persisted with explicit lineage.");
  const newEvent = await client.from("nayanet_cognition_events").select("id,event_id").eq("event_id",event.event_id).eq("user_id",userId).single();
  if (newEvent.error || !newEvent.data) throw new Error("SUPERSEDE_EVENT_PERSISTENCE_ID_NOT_FOUND");
  const evidenceRefs = Array.isArray(body.evidence_refs) ? body.evidence_refs : [{receipt_id:receipt?.id ?? receipt?.receipt_id ?? null, event_id:event.event_id}];
  const rpc = await client.rpc("nayanet_supersede_intelligent_block",{
    p_superseded_block_id:blockId,
    p_new_block_id:String(body.new_block_id ?? crypto.randomUUID()),
    p_owner_id:userId,
    p_subject_id:body.subject_id ?? oldBlock.data.subject_id,
    p_title:body.title ?? ("Superseding "+oldBlock.data.title),
    p_block_type:body.block_type ?? oldBlock.data.block_type,
    p_understanding_state:body.verified===true && evidenceRefs.length>0 ? "VERIFIED" : "CANDIDATE",
    p_owner_scope:body.owner_scope ?? oldBlock.data.owner_scope,
    p_source_event_ids:[...(oldBlock.data.source_event_ids ?? []),newEvent.data.id],
    p_evidence_refs:evidenceRefs,
    p_provenance:{source:"nayanet-compound-intelligence",source_event_id:newEvent.data.id,reason:String(body.reason ?? "New verified evidence")},
    p_value_context:body.value_context ?? oldBlock.data.value_context,
    p_applicable_scope:body.applicable_scope ?? oldBlock.data.applicable_scope,
    p_content:{...(oldBlock.data.content ?? {}),superseding_content:content},
    p_schema_version:"INTELLIGENT_BLOCK_V1",
    p_idempotency_key:idempotencyKey
  });
  if (rpc.error || !rpc.data) throw rpc.error ?? new Error("INTELLIGENT_BLOCK_SUPERSESSION_FAILED");
  return {event,receipt,lineage:{supersedes:old.data.event_id,superseded_block_id:blockId,new_block_id:rpc.data.block_id},intelligent_block:rpc.data};
}

async function checkpointIntelligence(client: any, userId: string, body: any) {
  const checkpointId = String(body.checkpoint_id ?? ("checkpoint:" + crypto.randomUUID())).trim();
  const sourceEventIds = Array.isArray(body.source_event_ids) ? body.source_event_ids.map(String).filter(Boolean) : [];
  const understanding = String(body.current_understanding ?? "").trim();
  if (!understanding) throw new Error("CURRENT_UNDERSTANDING_REQUIRED");
  if (sourceEventIds.length === 0) throw new Error("SOURCE_EVENT_IDS_REQUIRED");

  const existing = await client.from("nayanet_cognition_events")
    .select("*")
    .eq("event_id", checkpointId)
    .eq("user_id", userId)
    .eq("project_id", PROJECT)
    .maybeSingle();
  if (existing.error) throw existing.error;
  if (existing.data) {
    const existingSources = Array.isArray(existing.data.metadata?.source_event_ids) ? existing.data.metadata.source_event_ids.map(String) : [];
    if (existing.data.metadata?.checkpoint_id !== checkpointId || existingSources.join("|") !== sourceEventIds.join("|")) {
      throw new Error("CHECKPOINT_IDENTITY_CONFLICT");
    }
    return {
      schema: "NAYANET_INTELLIGENCE_CHECKPOINT_V1",
      status: "CHECKPOINT_VERIFIED",
      replayed: true,
      checkpoint: existing.data,
      source_events: [],
      receipt: null,
      rule: "Checkpoint replay returns the original checkpoint identity."
    };
  }

  const source = await client.from("nayanet_cognition_events")
    .select("id,event_id,title,content,status,confidence,metadata,created_at")
    .in("event_id", sourceEventIds)
    .eq("user_id", userId)
    .eq("project_id", PROJECT);

  if (source.error) throw source.error;
  const found = new Set((source.data ?? []).map((x: any) => String(x.event_id)));
  const missing = sourceEventIds.filter((id: string) => !found.has(id));
  if (missing.length) throw new Error("CHECKPOINT_SOURCE_EVENT_NOT_FOUND:" + missing.join(","));

  const event = {
    event_id: checkpointId,
    type: "intelligence_checkpoint",
    classification: "cognitive_checkpoint",
    title: String(body.title ?? "Naya cognitive checkpoint"),
    content: understanding,
    source: "nayanet-compound-intelligence",
    status: "active",
    actor: "naya",
    confidence: Number.isFinite(Number(body.confidence)) ? Number(body.confidence) : 1,
    tags: Array.isArray(body.tags) ? body.tags.map(String) : ["intelligence","checkpoint","compounding"],
    parent_event_id: sourceEventIds[0] ?? null,
    source_hash: "checkpoint:" + sourceEventIds.join("|"),
    schema_version: "NAYANET_INTELLIGENCE_CHECKPOINT_V1",
    metadata: {
      checkpoint_id: checkpointId,
      source_event_ids: sourceEventIds,
      what_changed: body.what_changed ?? null,
      learned: body.learned ?? null,
      evidence_refs: Array.isArray(body.evidence_refs) ? body.evidence_refs : [],
      authority_scope: body.authority_scope ?? null,
      unknown: Array.isArray(body.unknown) ? body.unknown : [],
      applicable_scope: body.applicable_scope ?? null,
      next_use: body.next_use ?? null,
      successor_relevance: body.successor_relevance ?? null,
      source_head: body.source_head ?? null,
      authority_grant_id: body.authority_grant_id ?? null,
      checkpointed_at: new Date().toISOString()
    }
  };

  const receipt = await record(
    client,
    event,
    "intelligence_checkpoint",
    "Cognitive checkpoint persisted",
    "Current understanding was checkpointed against provenance-bound source events.",
    [{ type: "checkpoint", checkpoint_id: checkpointId, source_event_ids: sourceEventIds }],
    body.authority_grant_id ? {authority_id:String(body.authority_grant_id),actor_id:userId,permission:"intelligence_commit",governance_state:"AUTHORIZED"} : null
  );

  return {
    schema: "NAYANET_INTELLIGENCE_CHECKPOINT_V1",
    status: "CHECKPOINT_VERIFIED",
    checkpoint: event,
    source_events: source.data ?? [],
    receipt,
    rule: "Checkpoint persistence does not by itself prove learning; later retrieval and behavior change are required."
  };
}

async function commitIntelligence(client: any, userId: string, body: any) {
  const idempotencyKey = String(body.idempotency_key ?? "").trim();
  const content = String(body.content ?? "").trim();
  if (!idempotencyKey) throw new Error("INTELLIGENCE_IDEMPOTENCY_KEY_REQUIRED");
  if (!content) throw new Error("INTELLIGENCE_CONTENT_REQUIRED");
  const eventId = "intelligence:" + idempotencyKey;
  const checkpointId = "checkpoint:" + idempotencyKey;
  const title = String(body.title ?? "Intelligent Block");
  const category = String(body.category ?? "INTELLIGENCE");
  const topic = String(body.topic ?? "GENERAL");
  const tags = Array.isArray(body.tags) ? body.tags.map(String) : ["intelligence","intelligent-block","compounding"];
  const authorityGrantId = String(body.authority_grant_id ?? "").trim();
  if (!authorityGrantId) throw new Error("AUTHORITY_GRANT_ID_REQUIRED");
  await validateIntelligenceCommitAuthority(client, authorityGrantId);
  const existing = await client.from("nayanet_cognition_events").select("id,event_id,title,content,metadata,created_at")
    .eq("event_id", eventId).eq("user_id", userId).eq("project_id", PROJECT).maybeSingle();
  if (existing.error) throw existing.error;
  let sourceEvent:any = existing.data;
  let captureReceipt:any = null;
  if (sourceEvent) {
    if (String(sourceEvent.metadata?.idempotency_key ?? "") !== idempotencyKey || String(sourceEvent.content ?? "") !== content) {
      throw new Error("INTELLIGENCE_IDENTITY_CONFLICT");
    }
  } else {
    const event = {
      event_id:eventId,type:"intelligent_block_capture",classification:"intelligent_block",title,content,
      source:"nayanet-compound-intelligence",status:"active",actor:"naya",
      confidence:Number.isFinite(Number(body.confidence)) ? Number(body.confidence) : 0.8,tags,
      parent_event_id:body.parent_event_id ?? null,source_hash:"intelligence:"+idempotencyKey,
      schema_version:"INTELLIGENT_BLOCK_V1",
      metadata:{idempotency_key:idempotencyKey,category,topic,applicable_scope:body.applicable_scope ?? null,
        limits:body.limits ?? null,human_teaching:body.human_teaching === true,authority_grant_id:authorityGrantId,captured_at:new Date().toISOString()}
    };
    captureReceipt=await record(client,event,"intelligence.capture",
      "Meaningful intelligence captured as a provenance-bound Intelligent Block source event",
      "Canonical Intelligent Block source event persisted.",
      [{type:"intelligent_block_capture",event_id:eventId,idempotency_key:idempotencyKey}],
      {authority_id:authorityGrantId,actor_id:userId,permission:"intelligence_commit",governance_state:"AUTHORIZED"});
    const persisted=await client.from("nayanet_cognition_events").select("id,event_id,title,content,metadata,created_at")
      .eq("event_id",eventId).eq("user_id",userId).eq("project_id",PROJECT).single();
    if(persisted.error || !persisted.data) throw new Error("INTELLIGENCE_CAPTURE_PERSISTENCE_NOT_FOUND");
    sourceEvent=persisted.data;
  }
  await validateIntelligenceCommitAuthority(client, authorityGrantId);
  const projection=await projectIntelligence(client,userId,{source_event_id:sourceEvent.id});
  const blockSeed = new TextEncoder().encode("NayaNET:IntelligentBlockV1:"+userId+":"+idempotencyKey);
  const blockDigest = new Uint8Array(await crypto.subtle.digest("SHA-256", blockSeed));
  blockDigest[6] = (blockDigest[6] & 0x0f) | 0x50;
  blockDigest[8] = (blockDigest[8] & 0x3f) | 0x80;
  const blockId = Array.from(blockDigest.slice(0,16)).map((v)=>v.toString(16).padStart(2,"0")).join("")
    .replace(/^(.{8})(.{4})(.{4})(.{4})(.{12})$/,"$1-$2-$3-$4-$5");
  const learningClaim=String(body.learning_claim ?? content).trim();
    const learningExisting=await client.from("learning_evidence").select("*").eq("member_id",userId)
    .eq("source_event_id",eventId).eq("claim",learningClaim).maybeSingle();
  if(learningExisting.error) throw learningExisting.error;
  let learning:any=learningExisting.data;
  if(!learning){
    await validateIntelligenceCommitAuthority(client, authorityGrantId);
    const inserted=await client.from("learning_evidence").insert({
      member_id:userId,target_id:String(body.target_id ?? "intelligent-block:"+eventId),
      level:"E1_UNDERSTANDS",provenance:"USER",status:"CANDIDATE",claim:learningClaim.slice(0,2000),
      observed_value:{category,topic,applicable_scope:body.applicable_scope ?? null},
      verification_method:"PENDING_OUTCOME_VERIFICATION",source_event_id:eventId
    }).select("*").single();
    if(inserted.error) throw inserted.error;
    learning=inserted.data;
  }
  const checkpoint=await checkpointIntelligence(client,userId,{
    checkpoint_id:checkpointId,source_event_ids:[eventId],current_understanding:content,
    title:"Intelligent Block checkpoint: "+title,confidence:body.confidence,
    tags:["intelligence","checkpoint","intelligent-block",category,topic],
    what_changed:body.what_changed ?? "New intelligence was captured and integrated into the canonical intelligence index.",
    learned:learningClaim,
    evidence_refs:[
      {kind:"capture_receipt",receipt_id:captureReceipt?.id ?? captureReceipt?.receipt_id ?? null},
      {kind:"source_event",event_id:eventId},{kind:"intelligence_index",index_id:projection.index?.id ?? null}
    ],
    authority_scope:body.authority_scope ?? "PERSONAL_INTELLIGENCE_ONLY",
    unknown:Array.isArray(body.unknown) ? body.unknown : ["Outcome-based verification of future behavior remains required."],
    applicable_scope:body.applicable_scope ?? null,
    next_use:body.next_use ?? "Cold Naya retrieves this intelligence when the topic/context is relevant.",
    successor_relevance:"Cold successor must restore this checkpoint, recognize applicability, use it when valid, and verify the outcome.",
    source_head:body.source_head ?? null,
    authority_grant_id:authorityGrantId
  });
  const existingBlock = await admin.from("nayanet_intelligent_blocks")
    .select("*").eq("block_id",blockId).eq("owner_id",userId).maybeSingle();
  if (existingBlock.error) throw existingBlock.error;
  let intelligentBlock:any = existingBlock.data;
  if (!intelligentBlock) {
    await validateIntelligenceCommitAuthority(client, authorityGrantId);
    const blockContent:any = {
      identity:{object_id:"IB:"+blockId,event_id:eventId,version:1,namespace:"nayanet",schema_version:"NAYANET_INTELLIGENT_BLOCK_V1"},
      context:{project_id:PROJECT,category,topic,visibility:"PRIVATE",owner_id:userId},
      truth:{state:"CANDIDATE",status:"UNVERIFIED",source:"nayanet-compound-intelligence",confidence:Number(body.confidence ?? 0.8)},
      authority:{state:"AUTHORIZED",scope:body.authority_scope ?? "PERSONAL_INTELLIGENCE_ONLY",actor:userId},
      value:{state:"CAPTURED",learning_claim:learningClaim,applicable_scope:body.applicable_scope ?? null},
      lifecycle:{stage:"CAPTURED_INTEGRATED_CHECKPOINTED",captured_at:new Date().toISOString(),checkpoint_id:checkpointId},
      content:{title,content,category,topic,tags,what_changed:body.what_changed ?? null,next_use:body.next_use ?? null,successor_relevance:"Cold successor must restore this intelligence, recognize applicability, use it when valid, and verify the outcome."}
    };
    const blockHashBytes = new Uint8Array(await crypto.subtle.digest("SHA-256",new TextEncoder().encode(JSON.stringify(blockContent))));
    blockContent.integrity={algorithm:"SHA-256",content_hash:Array.from(blockHashBytes).map((v)=>v.toString(16).padStart(2,"0")).join("")};
    const insertedBlock = await admin.from("nayanet_intelligent_blocks").insert({
      block_id:blockId,owner_id:userId,subject_id:String(body.target_id ?? topic),
      title,block_type:category || "INTELLIGENCE",version:1,status:"ACTIVE",
      understanding_state:"CANDIDATE",owner_scope:"PRIVATE",source_event_ids:[sourceEvent.id],
      evidence_refs:[
        {kind:"capture_receipt",receipt_id:captureReceipt?.id ?? captureReceipt?.receipt_id ?? null},
        {kind:"source_event",event_id:eventId,source_row_id:sourceEvent.id},
        {kind:"intelligence_index",index_id:projection.index?.id ?? null},
        {kind:"checkpoint",checkpoint_id:checkpointId,receipt_id:checkpoint.receipt?.id ?? checkpoint.receipt?.receipt_id ?? null}
      ],
      provenance:{source:"nayanet-compound-intelligence",idempotency_key:idempotencyKey,canonical_event_id:eventId,source_event_id:sourceEvent.id,checkpoint_id:checkpointId},
      value_context:body.value_context ?? {learning_claim:learningClaim},
      applicable_scope:body.applicable_scope ?? {},
      content:blockContent,
      schema_version:"INTELLIGENT_BLOCK_V1"
    }).select("*").single();
    if (insertedBlock.error) throw insertedBlock.error;
    intelligentBlock=insertedBlock.data;
  }
  return {
    schema:"NAYANET_INTELLIGENCE_COMMIT_V1",status:"CAPTURED_INTEGRATED_CHECKPOINTED",
    idempotency_key:idempotencyKey,source_event:sourceEvent,projection,
    learning:{status:learning.status,evidence_id:learning.id,target_id:learning.target_id},
    checkpoint:{status:checkpoint.status,replayed:checkpoint.replayed===true,
      checkpoint_id:checkpoint.checkpoint?.metadata?.checkpoint_id ?? checkpointId,
      receipt_id:checkpoint.receipt?.id ?? checkpoint.receipt?.receipt_id ?? null},
    proof_boundary:"Capture + integration + checkpoint are persisted. Applicability, behavior change, outcome verification, and improvement remain required before the lesson is promoted to VERIFIED/WISDOM.",
    rule:"One governed commit path; idempotent identity; no second intelligence store; private by default."
  };
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
    const preActionExempt = new Set(["restore","cold_restore","retrieve","reconcile","health"]);
    if (!preActionExempt.has(action)) {
      const gate = await coldRestore(client,user.id);
      if (gate.status !== "COLD_RESTORE_VERIFIED" || gate.mandatory_pre_action !== true || gate.question_count !== 14) {
        throw new Error("PRE_ACTION_PROJECT_INTELLIGENCE_GATE_FAILED");
      }
    }
    let result:any;
    if (action === "universal_meaningful_output") {
      const sourceType = String(body.source_type ?? "").trim();
      const privacy = String(body.privacy ?? "PRIVATE").trim();
      const destinationClass = String(body.destination_class ?? "").trim();
      const requestedAction = String(body.requested_action ?? "").trim();
      if (!String(body.output_id ?? "").trim()) throw new Error("UNIVERSAL_OUTPUT_ID_REQUIRED");
      if (!String(body.source_ref ?? "").trim()) throw new Error("UNIVERSAL_SOURCE_REF_REQUIRED");
      if (!String(body.title ?? "").trim()) throw new Error("UNIVERSAL_TITLE_REQUIRED");
      if (!String(body.content ?? "").trim()) throw new Error("UNIVERSAL_CONTENT_REQUIRED");
      if (!["conversation","execution","tool_result","document","existing_intelligence","other"].includes(sourceType)) throw new Error("UNIVERSAL_SOURCE_TYPE_INVALID");
      if (!["PRIVATE","SHARED_BY_CHOICE","COLLECTIVE_BY_CONSENT","PUBLIC_BY_DECISION"].includes(privacy)) throw new Error("UNIVERSAL_PRIVACY_INVALID");
      if (!["knowledge","procedure","checklist","test","contract","architecture","mission_state","guardrail","existing_intelligence","other"].includes(destinationClass)) throw new Error("UNIVERSAL_DESTINATION_INVALID");
      if (!["PROPOSE_ONLY","CAPTURE_IF_AUTHORIZED","ROUTE_IF_AUTHORIZED"].includes(requestedAction)) throw new Error("UNIVERSAL_REQUESTED_ACTION_INVALID");
      if (privacy !== "PRIVATE" && !String(body.authority_ref ?? "").trim()) throw new Error("UNIVERSAL_AUTHORITY_REQUIRED");
      if (destinationClass !== "existing_intelligence") throw new Error("UNIVERSAL_DESTINATION_NOT_IN_BOUNDED_PROOF");
      if (requestedAction === "PROPOSE_ONLY") throw new Error("UNIVERSAL_PROPOSAL_ONLY_NOT_COMMITTABLE");
      result = await commitIntelligence(client,user.id,{
        ...body,
        idempotency_key: String(body.output_id).trim(),
        value_context: {
          ...(body.value_context ?? {}),
          universal_adapter: "UNIVERSAL_MEANINGFUL_OUTPUT_V1",
          source_type: sourceType,
          output_id: String(body.output_id).trim(),
          output_version: Number(body.output_version ?? 1),
          source_ref: String(body.source_ref).trim(),
          provenance_refs: Array.isArray(body.provenance_refs) ? body.provenance_refs : [String(body.source_ref).trim()],
          evidence_state: String(body.evidence_state ?? "OBSERVED"),
          privacy,
          destination_class: destinationClass
        }
      });
      result.schema = "NAYANET_UNIVERSAL_MEANINGFUL_OUTPUT_V1";
      result.adapter = "UNIVERSAL_MEANINGFUL_OUTPUT_V1";
    } else {
      switch(action) {
        case "restore": result=await restore(client,user.id); break;
        case "cold_restore": result=await coldRestore(client,user.id); break;
        case "retrieve": result=await retrieve(client,user.id,body); break;
        case "reconcile": result=await reconcile(client,user.id,body); break;
        case "understand": result=await understand(client,user.id,body); break;
        case "learning_candidate": result=await learningCandidate(client,user.id,body); break;
        case "learning_verify": result=await learningVerify(client,user.id,body); break;
        case "learning_retrieve": result=await learningRetrieve(client,user.id,body); break;
        case "project": result=await projectIntelligence(client,user.id,body); break;
        case "ack": result=await ackBridge(client,user.id,body); break;
        case "state_update": result=await stateUpdate(client,user.id,body); break;
        case "successor_handoff": result=await successor(client,user.id,body); break;
        case "issue_pi_authority": result=await issuePiAuthority(client,user.id,body); break;
        case "continue_authorized": result=await continueAuthorized(client,user.id,body); break;
        case "consolidate_pi_gates": result=await consolidatePiGates(client,user.id,body); break;
        case "share": result=await share(client,user.id,body); break;
        case "supersede": result=await supersede(client,user.id,body); break;
        case "checkpoint": result=await checkpointIntelligence(client,user.id,body); break;
        case "intelligence_commit": result=await commitIntelligence(client,user.id,body); break;
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
    }
    await logOp(client,user.id,action,"SUCCESS",body,result);
    return json({ok:true,action,result});
  } catch(e) {
    const detail=String(e?.message||e);
    try { await logOp(client,user.id,action,"FAILED",body,{error:detail}); } catch {}
    return json({ok:false,action,error:detail},400);
  }
});