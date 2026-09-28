import { createRemoteJWKSet, jwtVerify } from "https://esm.sh/jose@6.0.10";
import { createClient } from "npm:@supabase/supabase-js@2";

const ISSUER = "https://token.actions.githubusercontent.com";
const AUDIENCE = "nayanet-runtime";
const REPOSITORY = "SoulSchoolAcademy/NayaPOWER";
const WORKFLOW = ".github/workflows/live-intelligence-commit-proof.yml";
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
  const workflowRef = REPOSITORY + "/" + WORKFLOW + "@" + REF;
  if (payload.repository !== REPOSITORY || payload.workflow_ref !== workflowRef || payload.ref !== REF) {
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

async function callCommit(admin: ReturnType<typeof adminClient>, body: Json, jti: string) {
  const {data, error} = await admin.rpc("nayanet_intelligence_commit_runtime", {
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
  });
  if (error) throw new Error(error.message);
  return data as Json;
}

async function read(admin: ReturnType<typeof adminClient>, id: string, table: string, ownerColumn: string) {
  const {data, error} = await admin.from(table).select("*").eq(
    table === "nayanet_cognition_events" ? "id" :
    table === "nayanet_intelligent_blocks" ? "intelligent_block_id" :
    table === "nayanet_intelligence_lineage" ? "id" :
    table === "nayanet_brain_relationships" ? "relationship_id" :
    table === "nayanet_project_cognition_state" ? "id" : "id", id
  ).eq(ownerColumn, OWNER_ID).maybeSingle();
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
      const result = await callCommit(admin, body, String(payload.jti ?? ""));
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

    if (mode === "verify") {
      const receiptId = String(body.receipt_id ?? "");
      const eventId = String(body.event_id ?? "");
      const blockId = String(body.intelligent_block_id ?? "");
      const lineageId = String(body.lineage_id ?? "");
      const relationshipId = String(body.relationship_id ?? "");
      const checkpointId = String(body.checkpoint_id ?? "");
      if (!receiptId || !eventId || !blockId || !lineageId || !relationshipId || !checkpointId) {
        return json({ok:false,error:"LINEAGE_IDS_REQUIRED"},400);
      }

      const [event, block, lineage, relationship, checkpoint, receipt] = await Promise.all([
        read(admin,eventId,"nayanet_cognition_events","user_id"),
        read(admin,blockId,"nayanet_intelligent_blocks","owner_id"),
        read(admin,lineageId,"nayanet_intelligence_lineage","user_id"),
        read(admin,relationshipId,"nayanet_brain_relationships","owner_id"),
        read(admin,checkpointId,"nayanet_project_cognition_state","user_id"),
        read(admin,receiptId,"nayanet_execution_receipts","user_id"),
      ]);

      const pass = Boolean(event && block && lineage && relationship && checkpoint && receipt) &&
        block.source_event_ids?.includes(event.id) &&
        lineage.source_event_id === event.id &&
        lineage.target_event_id === block.block_id &&
        relationship.target_id === block.intelligent_block_id &&
        checkpoint.state?.lineage_id === lineage.id &&
        checkpoint.state?.relationship_id === relationship.relationship_id &&
        checkpoint.state?.intelligent_block_id === block.intelligent_block_id &&
        checkpoint.state?.receipt_id === receipt.id &&
        receipt.action === "intelligence_commit";

      return json({
        ok: pass,
        status: pass ? "LINEAGE_VERIFIED" : "LINEAGE_BROKEN",
        independent_verification: true,
        runtime_identity: "naya-node-oidc",
        naya_id: NAYA_ID,
        owner_id: OWNER_ID,
        workflow_ref: workflowRef,
        token_jti: payload.jti ?? null,
        checks: {
          event_present: Boolean(event),
          block_present: Boolean(block),
          lineage_present: Boolean(lineage),
          relationship_present: Boolean(relationship),
          checkpoint_present: Boolean(checkpoint),
          receipt_present: Boolean(receipt),
          event_to_block: Boolean(event && block?.source_event_ids?.includes(event.id)),
          block_lineage: Boolean(lineage && lineage.source_event_id === event?.id && lineage.target_event_id === block?.block_id),
          block_relationship: Boolean(relationship && relationship.target_id === block?.intelligent_block_id),
          checkpoint_links_lineage: Boolean(checkpoint && checkpoint.state?.lineage_id === lineage?.id),
          checkpoint_links_relationship: Boolean(checkpoint && checkpoint.state?.relationship_id === relationship?.relationship_id),
          checkpoint_links_block: Boolean(checkpoint && checkpoint.state?.intelligent_block_id === block?.intelligent_block_id),
          checkpoint_links_receipt: Boolean(checkpoint && checkpoint.state?.receipt_id === receipt?.id),
          receipt_is_intelligence_commit: receipt?.action === "intelligence_commit",
        },
        persisted: {event,block,lineage,relationship,checkpoint,receipt},
      });
    }

    return json({ok:false,error:"UNSUPPORTED_MODE"},400);
  } catch (error) {
    return json({ok:false,error:String((error as Error)?.message ?? error)},400);
  }
});
