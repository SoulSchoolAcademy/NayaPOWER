import { createRemoteJWKSet, jwtVerify } from "https://esm.sh/jose@6.0.10";
import { createClient } from "npm:@supabase/supabase-js@2";
import { CapabilityValidationError, validateCapabilities } from "./capability-vocabulary.ts";
import { TaskClassValidationError, validateTaskClasses } from "./task-class-vocabulary.ts";

const ISSUER = "https://token.actions.githubusercontent.com";
const AUDIENCE = "nayanet-runtime";
const REPOSITORY = "SoulSchoolAcademy/NayaPOWER";
const WORKFLOWS = new Set([
  ".github/workflows/live-intelligence-commit-proof.yml",
  ".github/workflows/live-connect-proof.yml",
]);
const REF = "refs/heads/main";
const NAYA_ID = "NAYA-NODE-0001";
const OWNER_ID = "adfdf0b8-5558-41d1-9fed-ec51abf4fe2f";
const JWKS = createRemoteJWKSet(new URL("https://token.actions.githubusercontent.com/.well-known/jwks"));

const json = (body: unknown, status = 200) => new Response(JSON.stringify(body), {
  status,
  headers: {"content-type":"application/json","cache-control":"no-store"},
});

type Json = Record<string, unknown>;

async function authenticate(req: Request) {
  const header = req.headers.get("authorization") ?? "";
  if (!header.startsWith("Bearer ")) throw new Error("RUNTIME_IDENTITY_REQUIRED");
  let payload: Json;
  try {
    payload = (await jwtVerify(header.slice(7), JWKS, {issuer: ISSUER, audience: AUDIENCE})).payload as Json;
  } catch {
    throw new Error("GITHUB_OIDC_INVALID");
  }
  const workflowRef = String(payload.workflow_ref ?? "");
  const expectedRefs = Array.from(WORKFLOWS).map((w) => REPOSITORY + "/" + w + "@" + REF);
  if (payload.repository !== REPOSITORY || !expectedRefs.includes(workflowRef) || payload.ref !== REF) {
    throw new Error("WORKFLOW_BINDING_MISMATCH");
  }
  return {payload, workflowRef};
}

function adminClient() {
  const url = Deno.env.get("SUPABASE_URL");
  const key = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");
  if (!url || !key) throw new Error("SERVER_AUTH_CONFIG_MISSING");
  return createClient(url, key);
}

function coerceConnections(value: unknown): unknown[] | null {
  if (value === undefined || value === null) return null;
  if (!Array.isArray(value)) throw new Error("P_CONNECTIONS_MUST_BE_ARRAY");
  return value;
}

function coerceCapabilities(value: unknown): string[] | null {
  try {
    return validateCapabilities(value);
  } catch (err) {
    if (err instanceof CapabilityValidationError) throw new Error(err.code + ":" + err.detail);
    throw err;
  }
}

async function callCommit(body: Json, jti: string) {
  const url = Deno.env.get("SUPABASE_URL");
  const key = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");
  if (!url || !key) throw new Error("SERVER_AUTH_CONFIG_MISSING");

  // Use the same direct PostgREST boundary proven by the existing cold-runtime
  // functions. The previous supabase-js .rpc() path could remain pending until
  // Supabase Edge's 150s worker resource limit terminated the request.
  //
  // AI1 capability carry (repair/ai1-capability-carry): `p_capabilities` is the
  // ONLY channel by which capability metadata enters a block. It is validated
  // here (fail fast, clean 400) and again server-side in the SQL writer (fail
  // closed). Absent/empty -> null -> the writer persists the block exactly as
  // today. Unknown/malformed -> the commit is rejected, never silently stored.
  let capabilities: string[] | null = null;
  try {
    capabilities = validateCapabilities(body.p_capabilities);
  } catch (err) {
    if (err instanceof CapabilityValidationError) throw new Error(err.code + ":" + err.detail);
    throw err;
  }
  // H8-7 writer closure: `declared_task_classes` is the ONLY channel by which
  // a governed task-class declaration enters a block's provenance. Validated
  // here (fail fast, clean 400) and again server-side in the SQL writer (fail
  // closed). Absent/empty -> null -> the writer persists the block exactly as
  // today. Unknown/malformed -> the commit is rejected, never silently stored.
  let declaredTaskClasses: string[] | null = null;
  try {
    declaredTaskClasses = validateTaskClasses(body.declared_task_classes);
  } catch (err) {
    if (err instanceof TaskClassValidationError) throw new Error(err.code + ":" + err.detail);
    throw err;
  }
  const response = await fetch(url + "/rest/v1/rpc/nayanet_intelligence_commit_runtime", {
    method: "POST",
    headers: {
      apikey: key,
      Authorization: "Bearer " + key,
      "Content-Type": "application/json",
      Prefer: "return=representation",
    },
    body: JSON.stringify({
      p_naya_id: NAYA_ID,
      p_owner_id: OWNER_ID,
      p_runtime_jti: jti,
      p_event_id: String(body.p_event_id ?? ""),
      p_title: String(body.p_title ?? ""),
      p_content: String(body.p_content ?? ""),
      p_category: String(body.p_category ?? ""),
      p_topic: String(body.p_topic ?? ""),
      p_target_id: String(body.p_target_id ?? NAYA_ID),
      p_authority_grant_id: String(body.p_authority_grant_id ?? ""),
      p_project_id: String(body.p_project_id ?? "NayaNET"),
      p_connections: coerceConnections(body.p_connections),
      p_capabilities: capabilities,
      p_declared_task_classes: declaredTaskClasses,
    }),
  });
  const text = await response.text();
  if (!response.ok) throw new Error("COMMIT_RPC_" + response.status + ":" + text);
  return JSON.parse(text) as Json;
}

async function callSupersede(body: Json, jti: string) {
  const url = Deno.env.get("SUPABASE_URL");
  const key = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");
  if (!url || !key) throw new Error("SERVER_AUTH_CONFIG_MISSING");

  // Supersession is a second canonical writer surface. Capability metadata
  // must not disappear when a block is revised through it. Reuse the exact
  // same bounded validator as callCommit; unknown/malformed values fail
  // before the RPC and SQL validates again.
  const capabilities = coerceCapabilities(body.p_capabilities);

  // H8-7 writer closure: the supersession runtime does not yet carry
  // task-class declarations (follow-up: thread p_declared_task_classes
  // through nayanet_supersede_intelligent_block_runtime). An explicit
  // declaration on a supersede call is rejected rather than silently dropped:
  // a silent drop would manufacture the exact "writer exists, declaration
  // lost" gap this repair closes on the commit path.
  if (body.declared_task_classes !== undefined && body.declared_task_classes !== null) {
    throw new Error("TASK_CLASS_DECLARATION_NOT_SUPPORTED_ON_SUPERSEDE");
  }

  // Same direct PostgREST boundary as callCommit.
  const response = await fetch(url + "/rest/v1/rpc/nayanet_supersede_intelligent_block_runtime", {
    method: "POST",
    headers: {
      apikey: key,
      Authorization: "Bearer " + key,
      "Content-Type": "application/json",
      Prefer: "return=representation",
    },
    body: JSON.stringify({
      p_naya_id: NAYA_ID,
      p_owner_id: OWNER_ID,
      p_runtime_jti: jti,
      p_authority_grant_id: String(body.p_authority_grant_id ?? ""),
      p_project_id: String(body.p_project_id ?? "NayaNET"),
      p_superseded_block_id: String(body.p_superseded_block_id ?? ""),
      p_title: String(body.p_title ?? ""),
      p_content: String(body.p_content ?? ""),
      p_block_type: String(body.p_block_type ?? "GOVERNED_INTELLIGENCE"),
      p_understanding_state: String(body.p_understanding_state ?? "CANDIDATE"),
      p_owner_scope: String(body.p_owner_scope ?? "PRIVATE"),
      p_idempotency_key: String(body.p_idempotency_key ?? ""),
      p_connections: coerceConnections(body.p_connections),
      p_topic: body.p_topic === undefined || body.p_topic === null ? null : String(body.p_topic),
      p_category: body.p_category === undefined || body.p_category === null ? null : String(body.p_category),
      p_capabilities: capabilities,
    }),
  });
  const text = await response.text();
  if (!response.ok) throw new Error("SUPERSEDE_RPC_" + response.status + ":" + text);
  return JSON.parse(text) as Json;
}

const idColumn: Record<string,string> = {
  nayanet_cognition_events: "id",
  nayanet_intelligent_blocks: "intelligent_block_id",
  nayanet_intelligence_lineage: "id",
  nayanet_brain_relationships: "relationship_id",
  nayanet_project_cognition_state: "id",
  nayanet_intelligence_index: "id",
  nayanet_execution_receipts: "id",
};

async function read(admin: ReturnType<typeof adminClient>, id: string, table: string, ownerColumn: string) {
  const {data, error} = await admin.from(table).select("*").eq(idColumn[table], id).eq(ownerColumn, OWNER_ID).maybeSingle();
  if (error) throw error;
  return data;
}

Deno.serve(async (req) => {
  try {
    if (req.method !== "POST") return json({ok:false,error:"METHOD_NOT_ALLOWED"},405);
    const {payload, workflowRef} = await authenticate(req);
    const admin = adminClient();
    const body = (await req.json().catch(() => ({}))) as Json;
    const mode = String(body.mode ?? "");

    if (mode === "execute") {
      const result = await callCommit(body, String(payload.jti ?? ""));
      return json({
        ok: result?.ok === true,
        status: "EXECUTED",
        result,
        runtime_identity: "naya-node-oidc",
        naya_id: NAYA_ID,
        owner_id: OWNER_ID,
        workflow_ref: workflowRef,
        token_jti: payload.jti ?? null,
      });
    }

    if (mode === "supersede") {
      const required = ["p_superseded_block_id", "p_title", "p_content", "p_authority_grant_id", "p_idempotency_key"];
      for (const key of required) {
        if (!String(body[key] ?? "").trim()) return json({ok:false,error:"SUPERSEDE_FIELDS_REQUIRED:" + key},400);
      }
      const result = await callSupersede(body, String(payload.jti ?? ""));
      return json({
        ok: true,
        status: "SUPERSEDED",
        result,
        runtime_identity: "naya-node-oidc",
        naya_id: NAYA_ID,
        owner_id: OWNER_ID,
        workflow_ref: workflowRef,
        token_jti: payload.jti ?? null,
      });
    }

    if (mode === "verify_block") {
      const blockId = String(body.intelligent_block_id ?? "");
      if (!blockId) return json({ok:false,error:"INTELLIGENT_BLOCK_ID_REQUIRED"},400);
      const block = await read(admin, blockId, "nayanet_intelligent_blocks", "owner_id");
      return json({
        ok: Boolean(block),
        status: block ? "BLOCK_VERIFIED" : "BLOCK_NOT_FOUND",
        independent_verification: true,
        runtime_identity: "naya-node-oidc",
        naya_id: NAYA_ID,
        owner_id: OWNER_ID,
        workflow_ref: workflowRef,
        token_jti: payload.jti ?? null,
        persisted: {block},
      }, block ? 200 : 404);
    }

    if (mode === "verify") {
      const receiptId = String(body.receipt_id ?? "");
      const eventId = String(body.event_id ?? "");
      const blockId = String(body.intelligent_block_id ?? "");
      const lineageId = String(body.lineage_id ?? "");
      const relationshipId = String(body.relationship_id ?? "");
      const indexId = String(body.index_id ?? "");
      const checkpointId = String(body.checkpoint_id ?? "");
      if (!receiptId || !eventId || !blockId || !lineageId || !relationshipId || !indexId || !checkpointId) {
        return json({ok:false,error:"LINEAGE_IDS_REQUIRED"},400);
      }

      const [event, block, lineage, relationship, index, checkpoint, receipt] = await Promise.all([
        read(admin,eventId,"nayanet_cognition_events","user_id"),
        read(admin,blockId,"nayanet_intelligent_blocks","owner_id"),
        read(admin,lineageId,"nayanet_intelligence_lineage","user_id"),
        read(admin,relationshipId,"nayanet_brain_relationships","owner_id"),
        read(admin,indexId,"nayanet_intelligence_index","owner_id"),
        read(admin,checkpointId,"nayanet_project_cognition_state","user_id"),
        read(admin,receiptId,"nayanet_execution_receipts","user_id"),
      ]);

      const arrayContainsId = (value: unknown, id: string) => Array.isArray(value) && value.includes(id);
      const evidenceContainsId = (value: unknown, id: string) =>
        Array.isArray(value) && value.some((item) =>
          item === id || (item && typeof item === "object" && Object.values(item as Record<string, unknown>).includes(id))
        );

      const checks = {
        event_present: Boolean(event),
        block_present: Boolean(block),
        lineage_present: Boolean(lineage),
        relationship_present: Boolean(relationship),
        index_present: Boolean(index),
        checkpoint_present: Boolean(checkpoint),
        receipt_present: Boolean(receipt),
        event_to_block: Boolean(event && block && arrayContainsId(block.source_event_ids, event.id)),
        block_lineage: Boolean(lineage && event && block &&
          lineage.source_event_id === event.id &&
          lineage.target_event_id === event.id &&
          evidenceContainsId(lineage.evidence_refs, block.block_id)),
        block_relationship: Boolean(relationship && block && relationship.target_id === block.intelligent_block_id),
        block_index: Boolean(index && block && index.source_table === "nayanet_intelligent_blocks" && index.source_id === block.block_id),
        checkpoint_links_lineage: Boolean(checkpoint && checkpoint.state?.lineage_id === lineage?.id),
        checkpoint_links_relationship: Boolean(checkpoint && checkpoint.state?.relationship_id === relationship?.relationship_id),
        checkpoint_links_index: Boolean(checkpoint && checkpoint.state?.index_id === index?.id),
        checkpoint_links_block: Boolean(checkpoint && checkpoint.state?.intelligent_block_id === block?.intelligent_block_id),
        checkpoint_links_receipt: Boolean(checkpoint && checkpoint.state?.receipt_id === receipt?.id),
        receipt_is_intelligence_commit: receipt?.action === "intelligence_commit",
      };
      const pass = Object.values(checks).every(Boolean);

      return json({
        ok: pass,
        status: pass ? "LINEAGE_VERIFIED" : "LINEAGE_BROKEN",
        independent_verification: true,
        runtime_identity: "naya-node-oidc",
        naya_id: NAYA_ID,
        owner_id: OWNER_ID,
        workflow_ref: workflowRef,
        token_jti: payload.jti ?? null,
        checks,
        persisted: {event,block,lineage,relationship,index,checkpoint,receipt},
      });
    }

    return json({ok:false,error:"UNSUPPORTED_MODE"},400);
  } catch (error) {
    return json({ok:false,error:String((error as Error)?.message ?? error)},400);
  }
});
