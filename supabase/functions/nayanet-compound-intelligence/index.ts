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
  const [events, learning, replays, receipts, ops] = await Promise.all([
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
      .eq("user_id", userId).eq("project_id", PROJECT).order("created_at", { ascending: false }).limit(10)
  ]);
  for (const r of [events, learning, replays, receipts, ops]) if (r.error) throw r.error;

  const current = events.data?.[0] ?? null;
  const latestLearning = learning.data?.filter((x: any) => x.status === "ACTIVE").slice(0, 10) ?? [];
  const latestReplay = replays.data?.[0] ?? null;
  const latestReceipt = receipts.data?.[0] ?? null;

  return {
    schema: "NAYANET_PROJECT_INTELLIGENCE_RESTORE_V1",
    restored_at: new Date().toISOString(),
    project: PROJECT,
    mission: MISSION,
    vision: "A persistent, governed, interoperable intelligence infrastructure in which intelligence compounds across time, experience, decisions, learning and Nayas.",
    north_star: NORTH_STAR,
    YOU_ARE_HERE: {
      latest_event_id: current?.event_id ?? null,
      latest_event_at: current?.created_at ?? null,
      latest_receipt_id: latestReceipt?.id ?? null,
      latest_learning_id: latestLearning[0]?.id ?? null
    },
    CURRENT_STATE: current ? {
      title: current.title, type: current.type, classification: current.classification,
      status: current.status, confidence: current.confidence, content: current.content,
      source: current.source, source_hash: current.source_hash
    } : null,
    PROVEN: {
      active_learning_count: latestLearning.length,
      latest_verified_receipt: latestReceipt?.status === "SUCCESS" ? latestReceipt.id : null,
      latest_dream_replay: latestReplay?.id ?? null
    },
    UNKNOWN: [
      "Current human-facing runtime proof must remain tied to current source scope.",
      "Claims not supported by durable evidence remain UNKNOWN."
    ],
    BLOCKED: [],
    PROTECTED: [
      "UNKNOWN is not VERIFIED",
      "BLOCKED is not PASS",
      "Truth over agreement",
      "Private by default • Shared by choice • Collective by consent • Public by decision",
      "Capability does not create authority"
    ],
    CURRENT_NEXT_ACTION: {
      action: "RESTORE → RETRIEVE → DECIDE → ACT → VERIFY → LEARN → HANDOFF",
      reason: "The system must prepare the next Naya instead of requiring Shawn to reconstruct context."
    },
    RECENT_LEARNING: latestLearning,
    RECENT_DREAM: latestReplay,
    RECENT_RECEIPT: latestReceipt,
    RECENT_OPERATIONS: ops.data ?? [],
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
  if (!id || !method) throw new Error("EVIDENCE_ID_AND_VERIFICATION_METHOD_REQUIRED");
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
      case "successor_handoff": result=await successor(client,user.id,body); break;
      case "share": result=await share(client,user.id,body); break;
      case "supersede": result=await supersede(client,user.id,body); break;
      case "health": result=await health(client,user.id); break;
      case "dream": {
        result={next:"invoke naya-dream-replay", reason:"Dream/replay remains the governed simulation capability; this orchestrator records the lifecycle seam without duplicating it."};
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