import { createRemoteJWKSet, jwtVerify } from "https://esm.sh/jose@6.0.10";
import { createClient } from "npm:@supabase/supabase-js@2";

const ISSUER = "https://token.actions.githubusercontent.com";
const AUDIENCE = "nayanet-runtime";
const REPOSITORY = "SoulSchoolAcademy/NayaPOWER";
const WORKFLOW = ".github/workflows/live-supabase-runtime-proof.yml";
const REF = "refs/heads/main";
const OWNER_ID = "adfdf0b8-5558-41d1-9fed-ec51abf4fe2f";
const JWKS = createRemoteJWKSet(new URL("https://token.actions.githubusercontent.com/.well-known/jwks"));
const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), {
    status,
    headers: {
      "content-type": "application/json",
      "cache-control": "no-store",
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Headers": "authorization,apikey,content-type",
      "Access-Control-Allow-Methods": "POST,OPTIONS",
    },
  });

async function authenticateRuntime(req: Request) {
  const header = req.headers.get("authorization") ?? "";
  if (!header.startsWith("Bearer ")) throw new Error("RUNTIME_IDENTITY_REQUIRED");

  let payload: Record<string, unknown>;
  try {
    payload = (await jwtVerify(header.slice(7), JWKS, {
      issuer: ISSUER,
      audience: AUDIENCE,
    })).payload as Record<string, unknown>;
  } catch {
    throw new Error("GITHUB_OIDC_INVALID");
  }

  const workflowRef = REPOSITORY + "/" + WORKFLOW + "@" + REF;
  if (
    payload.repository !== REPOSITORY ||
    payload.workflow_ref !== workflowRef ||
    payload.ref !== REF
  ) {
    throw new Error("WORKFLOW_BINDING_MISMATCH");
  }

  return { payload, workflowRef, ownerId: OWNER_ID };
}

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") return json({ ok: true });
  if (req.method !== "POST") return json({ ok: false, error: "METHOD_NOT_ALLOWED" }, 405);

  try {
    const { payload, workflowRef, ownerId } = await authenticateRuntime(req);
    const supabaseUrl = Deno.env.get("SUPABASE_URL");
    const serviceRole = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");
    if (!supabaseUrl || !serviceRole) return json({ ok: false, error: "SERVER_AUTH_CONFIG_MISSING" }, 500);

    const admin = createClient(supabaseUrl, serviceRole);
    const body = await req.json();
    const mode = String(body?.mode || "verify");

    if (mode === "candidate") {
      const blockId = String(body?.intelligent_block_id || "");
      if (!blockId) return json({ ok: false, error: "INTELLIGENT_BLOCK_ID_REQUIRED" }, 400);
      const { data: block, error: blockError } = await admin.from("nayanet_intelligent_blocks").select("id,intelligent_block_id,owner_id,owner_scope,status,understanding_state,content,evidence_refs,created_at").eq("intelligent_block_id", blockId).eq("owner_id", ownerId).maybeSingle();
      if (blockError) throw blockError;
      if (!block) return json({ ok: false, error: "INTELLIGENT_BLOCK_NOT_FOUND" }, 404);
      if (block.understanding_state !== "CANDIDATE") return json({ ok: false, error: "BLOCK_NOT_CANDIDATE" }, 409);
      const evidenceRefs = Array.isArray(block.evidence_refs) ? block.evidence_refs : [];
      const sourceEventId = String(evidenceRefs[0]?.event_id || "");
      const commitReceiptId = String(evidenceRefs[0]?.receipt_id || "");
      if (!sourceEventId || !commitReceiptId) return json({ ok: false, error: "BLOCK_PROVENANCE_INCOMPLETE" }, 409);
      const { data: event, error: eventError } = await admin.from("nayanet_cognition_events").select("id,event_id,created_at,receipt_id").eq("event_id", sourceEventId).eq("receipt_id", commitReceiptId).eq("user_id", ownerId).maybeSingle();
      if (eventError) throw eventError;
      if (!event) return json({ ok: false, error: "SOURCE_EVENT_NOT_FOUND" }, 409);
      const { data: lineage, error: lineageError } = await admin.from("nayanet_intelligence_lineage").select("id,source_event_id,target_event_id,relation,created_at").eq("source_event_id", event.id).maybeSingle();
      if (lineageError) throw lineageError;
      if (!lineage) return json({ ok: false, error: "LINEAGE_NOT_FOUND" }, 409);
      const { data: relationship, error: relationshipError } = await admin.from("nayanet_brain_relationships").select("relationship_id,source_id,target_id,relationship_type,epistemic_state,provenance").eq("target_id", blockId).eq("owner_id", ownerId).maybeSingle();
      if (relationshipError) throw relationshipError;
      if (!relationship) return json({ ok: false, error: "RELATIONSHIP_NOT_FOUND" }, 409);
      const { data: index, error: indexError } = await admin.from("nayanet_intelligence_index").select("id,source_id,source_table,object_type,status").eq("source_id", block.id).eq("owner_id", ownerId).maybeSingle();
      if (indexError) throw indexError;
      if (!index) return json({ ok: false, error: "INDEX_NOT_FOUND" }, 409);
      const { data: checkpointRows, error: checkpointError } = await admin.from("nayanet_project_cognition_state").select("id,state,status,revision,updated_at").eq("user_id", ownerId).eq("project_id", "NayaNET").order("updated_at", { ascending: false }).limit(1);
      if (checkpointError) throw checkpointError;
      const checkpoint = checkpointRows?.[0];
      if (!checkpoint || checkpoint.state?.intelligent_block_id !== blockId || checkpoint.state?.lineage_id !== lineage.id || checkpoint.state?.relationship_id !== relationship.relationship_id || checkpoint.state?.index_id !== index.id) return json({ ok: false, error: "CHECKPOINT_PROVENANCE_MISMATCH" }, 409);
      const lesson = String(block.content?.lesson || "").trim();
      if (!lesson) return json({ ok: false, error: "LESSON_CONTENT_REQUIRED" }, 409);
      const existingRows = await admin.from("learning_evidence").select("id,status,claim,source_event_id,observed_value,verification_method,provenance,created_at").eq("member_id", ownerId).eq("target_id", "NAYA-NODE-0001").eq("status", "CANDIDATE").limit(100);
      if (existingRows.error) throw existingRows.error;
      const existing = (existingRows.data || []).find((row: any) => row?.observed_value?.intelligent_block_id === blockId);
      if (existing) return json({ ok: true, created: false, learning: existing, source: { event, block, lineage, relationship, index, checkpoint }, runtime_identity: "github-actions-oidc", workflow_ref: workflowRef, token_jti: payload.jti ?? null });
      const candidate = { member_id: ownerId, target_id: "NAYA-NODE-0001", level: "E1_UNDERSTANDS", provenance: "OBSERVATION", status: "CANDIDATE", claim: lesson, observed_value: { intelligent_block_id: blockId, source_event_id: event.id, source_event_key: event.event_id, commit_receipt_id: commitReceiptId, lineage_id: lineage.id, relationship_id: relationship.relationship_id, index_id: index.id, checkpoint_id: checkpoint.id, provenance_preserved: true }, verification_method: "Pending independent causal verification of the persisted Event → Intelligent Block → Lineage → Relationship → Index → Checkpoint chain.", source_event_id: event.id };
      const { data: learning, error: createError } = await admin.from("learning_evidence").insert(candidate).select("*").single();
      if (createError) throw createError;
      return json({ ok: true, created: true, learning, source: { event, block, lineage, relationship, index, checkpoint }, runtime_identity: "github-actions-oidc", workflow_ref: workflowRef, token_jti: payload.jti ?? null });
    }

    const learningId = String(body?.learning_id || "");
    if (!learningId) return json({ ok: false, error: "LEARNING_ID_REQUIRED" }, 400);

    if (mode === "reread") {
      const { data: retained, error: retainedError } = await admin
        .from("learning_evidence")
        .select("*")
        .eq("id", learningId)
        .eq("member_id", ownerId)
        .maybeSingle();
      if (retainedError) throw retainedError;
      if (!retained) return json({ ok: false, error: "LEARNING_NOT_FOUND" }, 404);
      return json({
        ok: true,
        independent_reread: true,
        learning: retained,
        runtime_identity: "github-actions-oidc",
        workflow_ref: workflowRef,
        token_jti: payload.jti ?? null,
      });
    }

    const { data: learning, error: learningError } = await admin
      .from("learning_evidence")
      .select("*")
      .eq("id", learningId)
      .eq("member_id", ownerId)
      .maybeSingle();
    if (learningError) throw learningError;
    if (!learning) return json({ ok: false, error: "LEARNING_NOT_FOUND" }, 404);

    const refs = Array.isArray(body?.evidence_refs) ? body.evidence_refs : [];
    if (!refs.length) return json({ ok: true, verified: false, reason: "EVIDENCE_REQUIRED" });

    const { data: promoted, error: promoteError } = await admin
      .from("learning_evidence")
      .update({
        status: "ACTIVE",
        provenance: "VERIFICATION",
        verification_method: String(body?.verification_method || learning.verification_method || ""),
      })
      .eq("id", learningId)
      .eq("member_id", ownerId)
      .select("*")
      .single();
    if (promoteError) throw promoteError;

    const result = {
      schema: "NAYANET_LEARNING_VERIFY_V3",
      learning: promoted,
      verified: true,
      evidence_refs: refs,
    };

    const { data: operation, error: operationError } = await admin
      .from("nayanet_intelligence_operations")
      .insert({
        user_id: ownerId,
        project_id: "NayaNET",
        operation: "learning_verify",
        status: "SUCCESS",
        input: body,
        output: result,
      })
      .select("id")
      .single();
    if (operationError) throw operationError;

    let receipt = null;
    let lineage = null;
    const receiptId = String(body?.receipt_id || "");
    if (receiptId) {
      const { data: existingReceipt, error: receiptError } = await admin
        .from("nayanet_execution_receipts")
        .select("*")
        .eq("id", receiptId)
        .eq("user_id", ownerId)
        .eq("project_id", "NayaNET")
        .maybeSingle();
      if (receiptError) throw receiptError;
      if (!existingReceipt) return json({ ok: false, error: "RECEIPT_NOT_FOUND_OR_NOT_OWNED" }, 404);

      const evidence = Array.isArray(existingReceipt.evidence) ? existingReceipt.evidence : [];
      const foundLineage = [...evidence]
        .reverse()
        .find((x: any) => x?.lineage?.schema === "NAYANET_EVIDENCE_LINEAGE_RUNTIME_V1")?.lineage;
      if (!foundLineage) return json({ ok: false, error: "RUNTIME_LINEAGE_NOT_FOUND" }, 409);

      foundLineage.status = "VERIFIED_LEARNING_BOUND";
      foundLineage.nodes = foundLineage.nodes.map((node: any) =>
        node.kind === "verification"
          ? { ...node, ref: String(operation.id) }
          : node.kind === "learning"
            ? { ...node, ref: String(promoted.id) }
            : node
      );

      const { data: updatedReceipt, error: updateReceiptError } = await admin
        .from("nayanet_execution_receipts")
        .update({
          evidence: evidence.map((x: any) =>
            x?.lineage?.lineage_id === foundLineage.lineage_id ? { ...x, lineage: foundLineage } : x
          ),
          learning: [
            ...(Array.isArray(existingReceipt.learning) ? existingReceipt.learning : []),
            { learning_id: promoted.id, verification_operation_id: operation.id, verified: true },
          ],
        })
        .eq("id", receiptId)
        .eq("user_id", ownerId)
        .select("*")
        .single();
      if (updateReceiptError) throw updateReceiptError;

      receipt = updatedReceipt;
      lineage = foundLineage;
    }

    return json({
      ok: true,
      result,
      verification_operation_id: operation.id,
      receipt,
      lineage,
      runtime_identity: "github-actions-oidc",
      workflow_ref: workflowRef,
      token_jti: payload.jti ?? null,
    });
  } catch (error) {
    console.error("NAYA_LEARNING_VERIFY_ERROR", error);
    return json({ ok: false, error: String((error as Error)?.message ?? error) }, 400);
  }
});
