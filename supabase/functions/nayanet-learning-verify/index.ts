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


function deriveGraphApplicability(block: any) {
  const lesson = String(block?.content?.lesson ?? "");
  if (/preserve provenance|provenance before applying retained intelligence/i.test(lesson)) {
    return {
      state: "APPLICABLE",
      task_classes: ["provenance_sensitive", "learning_reuse", "contextual_retrieval"],
      limitations: ["Only use where provenance preservation is materially relevant."],
    };
  }
  if (/act-first within guardrails|asking permission and acting|within the guardrails and adds value/i.test(lesson)) {
    return {
      state: "APPLICABLE",
      task_classes: ["repository_correction", "learning_reuse", "contextual_retrieval"],
      limitations: ["Does not create authority; LAW must independently authorize consequential action."],
    };
  }
  return {
    state: "UNKNOWN",
    task_classes: [],
    limitations: ["NO_PREDECLARED_TASK_CLASS"],
  };
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
      const requestedCheckpointId = String(body?.checkpoint_id || "");
      if (!blockId) return json({ ok: false, error: "INTELLIGENT_BLOCK_ID_REQUIRED" }, 400);
      const { data: block, error: blockError } = await admin.from("nayanet_intelligent_blocks").select("block_id,intelligent_block_id,owner_id,owner_scope,status,understanding_state,content,evidence_refs,created_at").eq("intelligent_block_id", blockId).eq("owner_id", ownerId).maybeSingle();
      if (blockError) throw blockError;
      if (!block) return json({ ok: false, error: "INTELLIGENT_BLOCK_NOT_FOUND" }, 404);
      if (!["CANDIDATE", "LEARNED"].includes(block.understanding_state)) {
        return json({ ok: false, error: "BLOCK_NOT_REVALIDATABLE", state: block.understanding_state }, 409);
      }
      const evidenceRefs = Array.isArray(block.evidence_refs) ? block.evidence_refs : [];
      const sourceEventId = String(evidenceRefs[0]?.event_id || "");
      const commitReceiptId = String(evidenceRefs[0]?.receipt_id || "");
      if (!sourceEventId || !commitReceiptId) return json({ ok: false, error: "BLOCK_PROVENANCE_INCOMPLETE" }, 409);
      const { data: event, error: eventError } = await admin.from("nayanet_cognition_events").select("id,event_id,created_at,receipt_id").eq("id", sourceEventId).eq("receipt_id", commitReceiptId).eq("user_id", ownerId).maybeSingle();
      if (eventError) throw eventError;
      if (!event) return json({ ok: false, error: "SOURCE_EVENT_NOT_FOUND" }, 409);
      const { data: lineage, error: lineageError } = await admin.from("nayanet_intelligence_lineage").select("id,source_event_id,target_event_id,relation,created_at").eq("source_event_id", event.id).maybeSingle();
      if (lineageError) throw lineageError;
      if (!lineage) return json({ ok: false, error: "LINEAGE_NOT_FOUND" }, 409);
      const { data: relationship, error: relationshipError } = await admin.from("nayanet_brain_relationships").select("relationship_id,source_id,target_id,relationship_type,epistemic_state,provenance").eq("target_id", blockId).eq("owner_id", ownerId).maybeSingle();
      if (relationshipError) throw relationshipError;
      if (!relationship) return json({ ok: false, error: "RELATIONSHIP_NOT_FOUND" }, 409);
      const { data: index, error: indexError } = await admin.from("nayanet_intelligence_index").select("id,source_id,source_table,object_type,status").eq("source_id", block.block_id).eq("owner_id", ownerId).maybeSingle();
      if (indexError) throw indexError;
      if (!index) return json({ ok: false, error: "INDEX_NOT_FOUND" }, 409);
      const checkpointQuery = admin.from("nayanet_project_cognition_state").select("id,state,status,revision,updated_at").eq("user_id", ownerId).eq("project_id", "NayaNET");
      const { data: checkpointRows, error: checkpointError } = requestedCheckpointId
        ? await checkpointQuery.eq("id", requestedCheckpointId).limit(1)
        : await checkpointQuery.order("updated_at", { ascending: false }).limit(1);
      if (checkpointError) throw checkpointError;
      const checkpoint = checkpointRows?.[0];
      if (!checkpoint) {
        return json({ ok: false, error: "CHECKPOINT_PROVENANCE_MISMATCH", reason: "CHECKPOINT_NOT_FOUND", checkpoint_id: requestedCheckpointId || null }, 409);
      }
      // The checkpoint row is keyed on (user_id, project_id) and upserted by every
      // intelligence commit, so this guard fires both when a chain was rebuilt
      // incorrectly AND when a later commit superseded the checkpoint the artifact
      // was bound to. Both arrive as one opaque string today, which is the same
      // observability dead end that made SUPABASE_READ_400 unresolvable from a log.
      // Name the link that disagrees and give both sides; ids only, no secret.
      const rebuiltChain: Record<string, string> = {
        intelligent_block_id: blockId,
        lineage_id: lineage.id,
        relationship_id: relationship.relationship_id,
        index_id: index.id,
      };
      const mismatched = Object.entries(rebuiltChain)
        .filter(([field, value]) => checkpoint.state?.[field] !== value)
        .map(([field, value]) => ({ field, checkpoint_state: checkpoint.state?.[field] ?? null, rebuilt_chain: value }));
      if (mismatched.length) {
        return json({ ok: false, error: "CHECKPOINT_PROVENANCE_MISMATCH", checkpoint_id: checkpoint.id, checkpoint_revision: checkpoint.revision ?? null, mismatched }, 409);
      }
      const lesson = String(block.content?.lesson || "").trim();
      if (!lesson) return json({ ok: false, error: "LESSON_CONTENT_REQUIRED" }, 409);
      const existingRows = await admin.from("learning_evidence").select("id,status,claim,source_event_id,observed_value,verification_method,provenance,created_at").eq("member_id", ownerId).eq("target_id", "NAYA-NODE-0001").eq("status", "CANDIDATE").limit(100);
      if (existingRows.error) throw existingRows.error;
      const candidates = existingRows.data || [];
      const matchingCandidates = candidates.filter(
        (row: any) =>
          row?.observed_value?.intelligent_block_id === blockId ||
          (
            typeof row?.claim === "string" &&
            row.claim === lesson &&
            row?.source_event_id
          )
      );
      if (matchingCandidates.length > 1) {
        return json({ ok: false, error: "AMBIGUOUS_EXISTING_LEARNING_CANDIDATES", candidate_ids: matchingCandidates.map((row: any) => row.id) }, 409);
      }
      const existing = matchingCandidates[0];
      if (existing) {
        const repairedObserved = {
          ...(existing.observed_value && typeof existing.observed_value === "object" && !Array.isArray(existing.observed_value) ? existing.observed_value : {}),
          intelligent_block_id: blockId,
          source_event_id: event.id,
          source_event_key: event.event_id,
          commit_receipt_id: commitReceiptId,
          lineage_id: lineage.id,
          relationship_id: relationship.relationship_id,
          index_id: index.id,
          checkpoint_id: checkpoint.id,
          provenance_preserved: true,
        };
        const { data: repaired, error: repairError } = await admin.from("learning_evidence").update({ source_event_id: event.id, observed_value: repairedObserved }).eq("id", existing.id).eq("member_id", ownerId).select("*").single();
        if (repairError) throw repairError;
        return json({
          ok: true,
          created: false,
          learning: repaired,
          source: { event, block, lineage, relationship, index, checkpoint },
          reuse_reason: "EXACT_PERSISTED_LESSON_CLAIM",
          runtime_identity: "github-actions-oidc",
          workflow_ref: workflowRef,
          token_jti: payload.jti ?? null,
        });
      }
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
      const observed = retained.observed_value && typeof retained.observed_value === "object" && !Array.isArray(retained.observed_value)
        ? retained.observed_value
        : {};
      const [block, relationship, checkpoint] = await Promise.all([
        admin.from("nayanet_intelligent_blocks").select("intelligent_block_id,understanding_state,provenance").eq("intelligent_block_id", String((observed as any).intelligent_block_id || "")).eq("owner_id", ownerId).maybeSingle(),
        admin.from("nayanet_brain_relationships").select("relationship_id,epistemic_state,provenance").eq("relationship_id", String((observed as any).relationship_id || "")).eq("owner_id", ownerId).maybeSingle(),
        admin.from("nayanet_project_cognition_state").select("id,state,status,revision,updated_at").eq("id", String((observed as any).checkpoint_id || "")).eq("user_id", ownerId).eq("project_id", "NayaNET").maybeSingle(),
      ]);
      if (block.error) throw block.error;
      if (relationship.error) throw relationship.error;
      if (checkpoint.error) throw checkpoint.error;
      const integration = {
        core_intelligence_updated: block.data?.understanding_state === "LEARNED",
        progressive_intelligence_lock_in: checkpoint.data?.state?.status === "LEARNED",
        intelligent_block_state: block.data?.understanding_state ?? null,
        relationship_epistemic_state: relationship.data?.epistemic_state ?? null,
        checkpoint_state_status: checkpoint.data?.state?.status ?? null,
        checkpoint_id: checkpoint.data?.id ?? null,
      };
      return json({
        ok: true,
        independent_reread: true,
        learning: retained,
        integration,
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

    const verificationMethod = String(
      body?.verification_method || learning.verification_method || "Independent runtime verification."
    );
    const { data: promoted, error: promoteError } = await admin
      .from("learning_evidence")
      .update({
        status: "ACTIVE",
        provenance: "VERIFICATION",
        verification_method: verificationMethod,
      })
      .eq("id", learningId)
      .eq("member_id", ownerId)
      .select("*")
      .single();
    if (promoteError) throw promoteError;

    const result = {
      schema: "NAYANET_LEARNING_VERIFY_V4",
      learning: promoted,
      verified: true,
      evidence_refs: refs,
    };

    let receipt = null;
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

      const learningEntries = Array.isArray(existingReceipt.learning) ? existingReceipt.learning : [];
      const verificationRecord = {
        learning_id: promoted.id,
        verified: true,
        verification_method: verificationMethod,
        verification_runtime: "github-actions-oidc",
        verification_runtime_jti: payload.jti ?? null,
        verified_at: new Date().toISOString(),
      };
      const alreadyRecorded = learningEntries.some(
        (entry: any) =>
          entry?.learning_id === promoted.id &&
          entry?.verified === true &&
          entry?.verification_runtime_jti === verificationRecord.verification_runtime_jti
      );

      const { data: updatedReceipt, error: updateReceiptError } = await admin
        .from("nayanet_execution_receipts")
        .update({
          learning: alreadyRecorded ? learningEntries : [...learningEntries, verificationRecord],
        })
        .eq("id", receiptId)
        .eq("user_id", ownerId)
        .select("*")
        .single();
      if (updateReceiptError) throw updateReceiptError;
      receipt = updatedReceipt;
    }

    const observed = promoted.observed_value && typeof promoted.observed_value === "object" && !Array.isArray(promoted.observed_value)
      ? promoted.observed_value
      : {};
    const intelligentBlockId = String((observed as any).intelligent_block_id || "");
    const relationshipId = String((observed as any).relationship_id || "");
    const checkpointId = String((observed as any).checkpoint_id || "");
    const lineageId = String((observed as any).lineage_id || "");
    const indexId = String((observed as any).index_id || "");
    if (!intelligentBlockId || !relationshipId || !checkpointId || !lineageId || !indexId) {
      return json({ ok: false, error: "LEARNING_PROVENANCE_LINKS_REQUIRED" }, 409);
    }

    const { data: blockBefore, error: blockReadError } = await admin
      .from("nayanet_intelligent_blocks")
      .select("*")
      .eq("intelligent_block_id", intelligentBlockId)
      .eq("owner_id", ownerId)
      .maybeSingle();
    if (blockReadError) throw blockReadError;
    if (!blockBefore) return json({ ok: false, error: "INTELLIGENT_BLOCK_NOT_FOUND_FOR_LOCK_IN" }, 404);
    if (!["CANDIDATE", "LEARNED"].includes(blockBefore.understanding_state)) {
      return json({ ok: false, error: "INTELLIGENT_BLOCK_LOCK_IN_STATE_INVALID", state: blockBefore.understanding_state }, 409);
    }

    const verificationRefs = Array.from(new Set([
      ...(Array.isArray(blockBefore.evidence_refs) ? blockBefore.evidence_refs : []),
      ...refs.map((ref: string) => ({ learning_verification_ref: ref })),
      { learning_id: promoted.id, causal_verification_id: refs.find((ref: string) => ref.startsWith("CVO-")) || null, receipt_id: receipt?.id || receiptId || null },
    ]));
    const blockProvenance = {
      ...(blockBefore.provenance && typeof blockBefore.provenance === "object" ? blockBefore.provenance : {}),
      learning_id: promoted.id,
      learning_status: promoted.status,
      learning_provenance: promoted.provenance,
      verification_runtime: "github-actions-oidc",
      verification_runtime_jti: payload.jti ?? null,
      progressive_intelligence_lock_in: "LEARNED",
      locked_in_at: new Date().toISOString(),
    };
    const { data: blockAfter, error: blockUpdateError } = await admin
      .from("nayanet_intelligent_blocks")
      .update({
        understanding_state: "LEARNED",
        evidence_refs: verificationRefs,
        provenance: blockProvenance,
      })
      .eq("intelligent_block_id", intelligentBlockId)
      .eq("owner_id", ownerId)
      .select("*")
      .single();
    if (blockUpdateError) throw blockUpdateError;

    const { data: relationshipBefore, error: relationshipReadError } = await admin
      .from("nayanet_brain_relationships")
      .select("*")
      .eq("relationship_id", relationshipId)
      .eq("owner_id", ownerId)
      .maybeSingle();
    if (relationshipReadError) throw relationshipReadError;
    if (!relationshipBefore) return json({ ok: false, error: "RELATIONSHIP_NOT_FOUND_FOR_LOCK_IN" }, 404);
    const relationshipProvenance = {
      ...(relationshipBefore.provenance && typeof relationshipBefore.provenance === "object" ? relationshipBefore.provenance : {}),
      learning_id: promoted.id,
      learning_verification: true,
      causal_verification_id: refs.find((ref: string) => ref.startsWith("CVO-")) || null,
      verification_runtime: "github-actions-oidc",
      verification_runtime_jti: payload.jti ?? null,
    };
    const graphApplicability = deriveGraphApplicability(blockAfter);
    const relationshipEvidenceRefs = verificationRefs;
    const relationshipReasonCodes = graphApplicability.state === "APPLICABLE"
      ? ["INDEPENDENT_CAUSAL_VERIFICATION", "LEARNING_VERIFIED", "TASK_APPLICABILITY_DERIVED_FROM_VERIFIED_LESSON"]
      : ["INDEPENDENT_CAUSAL_VERIFICATION", "LEARNING_VERIFIED", "APPLICABILITY_UNCLASSIFIED"];
    const { data: relationshipAfter, error: relationshipUpdateError } = await admin
      .from("nayanet_brain_relationships")
      .update({
        epistemic_state: "VERIFIED",
        status: "ACTIVE",
        visibility: "PRIVATE",
        provenance: relationshipProvenance,
        evidence_refs: relationshipEvidenceRefs,
        applicability: graphApplicability,
        reason_codes: relationshipReasonCodes,
      })
      .eq("relationship_id", relationshipId)
      .eq("owner_id", ownerId)
      .select("*")
      .single();
    if (relationshipUpdateError) throw relationshipUpdateError;

    const { data: checkpointBefore, error: checkpointReadError } = await admin
      .from("nayanet_project_cognition_state")
      .select("*")
      .eq("id", checkpointId)
      .eq("user_id", ownerId)
      .eq("project_id", "NayaNET")
      .maybeSingle();
    if (checkpointReadError) throw checkpointReadError;
    if (!checkpointBefore) return json({ ok: false, error: "CHECKPOINT_NOT_FOUND_FOR_LOCK_IN" }, 404);
    const checkpointState = {
      ...(checkpointBefore.state && typeof checkpointBefore.state === "object" ? checkpointBefore.state : {}),
      status: "LEARNED",
      learning_id: promoted.id,
      learning_provenance: promoted.provenance,
      intelligent_block_id: intelligentBlockId,
      lineage_id: lineageId,
      relationship_id: relationshipId,
      index_id: indexId,
      receipt_id: receipt?.id || receiptId || null,
      causal_verification_id: refs.find((ref: string) => ref.startsWith("CVO-")) || null,
      progressive_intelligence_lock_in: "LEARNED",
      last_learning_verified_at: new Date().toISOString(),
    };
    const { data: checkpointAfter, error: checkpointUpdateError } = await admin
      .from("nayanet_project_cognition_state")
      .update({ state: checkpointState })
      .eq("id", checkpointId)
      .eq("user_id", ownerId)
      .eq("project_id", "NayaNET")
      .select("*")
      .single();
    if (checkpointUpdateError) throw checkpointUpdateError;

    const integration = {
      core_intelligence_updated: true,
      progressive_intelligence_lock_in: "LEARNED",
      learning_id: promoted.id,
      intelligent_block: {
        id: blockAfter.intelligent_block_id,
        understanding_state: blockAfter.understanding_state,
      },
      relationship: {
        id: relationshipAfter.relationship_id,
        epistemic_state: relationshipAfter.epistemic_state,
      },
      cognitive_checkpoint: {
        id: checkpointAfter.id,
        state_status: checkpointAfter.state?.status,
      },
    };

    return json({
      ok: true,
      result,
      verification_record: receipt
        ? (receipt.learning || []).find((entry: any) => entry?.learning_id === promoted.id && entry?.verified === true) ?? null
        : null,
      receipt,
      integration,
      runtime_identity: "github-actions-oidc",
      workflow_ref: workflowRef,
      token_jti: payload.jti ?? null,
    });
  } catch (error) {
    console.error("NAYA_LEARNING_VERIFY_ERROR", error);
    return json({ ok: false, error: String((error as Error)?.message ?? error) }, 400);
  }
});
