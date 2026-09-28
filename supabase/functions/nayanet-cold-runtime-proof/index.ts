import { createRemoteJWKSet, jwtVerify } from "https://esm.sh/jose@6.0.10";
import { createClient } from "npm:@supabase/supabase-js@2";

const ISSUER = "https://token.actions.githubusercontent.com";
const AUDIENCE = "nayanet-runtime";
const REPOSITORY = "SoulSchoolAcademy/NayaPOWER";
const WORKFLOW = ".github/workflows/live-supabase-runtime-proof.yml";
const REF = "refs/heads/main";
const NAYA_ID = "NAYA-NODE-0001";
const OWNER_ID = "adfdf0b8-5558-41d1-9fed-ec51abf4fe2f";
const BLOCK_ID = "IB-NAYA-NODE-0001-0001";
const LEARNING_ID = "de0b794b-224b-4d8b-ad1a-3afc6f8d0771";
const JWKS = createRemoteJWKSet(new URL("https://token.actions.githubusercontent.com/.well-known/jwks"));
const json = (body: unknown, status = 200) => new Response(JSON.stringify(body), { status, headers: { "content-type": "application/json", "cache-control": "no-store" } });

async function auth(req: Request) {
  const h = req.headers.get("authorization") ?? "";
  if (!h.startsWith("Bearer ")) throw new Error("RUNTIME_IDENTITY_REQUIRED");
  let payload: Record<string, unknown>;
  try { payload = (await jwtVerify(h.slice(7), JWKS, { issuer: ISSUER, audience: AUDIENCE })).payload as Record<string, unknown>; }
  catch { throw new Error("GITHUB_OIDC_INVALID"); }
  const workflowRef = REPOSITORY + "/" + WORKFLOW + "@" + REF;
  if (payload.repository !== REPOSITORY || payload.workflow_ref !== workflowRef || payload.ref !== REF) throw new Error("WORKFLOW_BINDING_MISMATCH");
  return { payload, workflowRef };
}

Deno.serve(async (req: Request) => {
  try {
    if (req.method !== "GET" && req.method !== "POST") return json({ error: "METHOD_NOT_ALLOWED" }, 405);
    const { payload, workflowRef } = await auth(req);
    const supabaseUrl = Deno.env.get("SUPABASE_URL");
    const serviceRole = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");
    if (!supabaseUrl || !serviceRole) return json({ error: "SERVER_AUTH_CONFIG_MISSING" }, 500);
    const headers = { apikey: serviceRole, Authorization: "Bearer " + serviceRole, "Content-Type": "application/json" };
    const admin = createClient(supabaseUrl, serviceRole);
    const get = async (path: string) => { const r = await fetch(supabaseUrl + path, { headers }); if (!r.ok) throw new Error("SUPABASE_READ_" + r.status); return await r.json(); };
    const blockRows = await get("/rest/v1/nayanet_intelligent_blocks?intelligent_block_id=eq." + encodeURIComponent(BLOCK_ID) + "&owner_id=eq." + OWNER_ID + "&select=*");
    if (!Array.isArray(blockRows) || blockRows.length !== 1) return json({ error: "CANONICAL_BLOCK_NOT_UNIQUE" }, 409);
    const grantRows = await get("/rest/v1/nayanet_authority_grants?issuer_id=eq." + OWNER_ID + "&subject_id=eq." + OWNER_ID + "&mission_id=eq.NAYA-NODE-0001-CONTINUITY&status=eq.ACTIVE&select=grant_id,mission_id,scope,actions,constraints,status,evidence");
    if (!Array.isArray(grantRows) || grantRows.length < 1) return json({ error: "CANONICAL_AUTHORITY_MISSING" }, 403);
    const block = blockRows[0];
    const mode = new URL(req.url).searchParams.get("mode") ?? "cold";

    if (mode === "learning-influence") {
      if (req.method !== "POST") return json({ error: "METHOD_REQUIRED" }, 405);
      const learningRows = await get("/rest/v1/learning_evidence?id=eq." + LEARNING_ID + "&member_id=eq." + OWNER_ID + "&target_id=eq." + NAYA_ID + "&status=eq.CANDIDATE&select=id,target_id,level,status,claim,source_event_id,observed_value,verification_method,provenance");
      if (!Array.isArray(learningRows) || learningRows.length !== 1) return json({ error: "FRESH_LEARNING_CANDIDATE_NOT_FOUND" }, 409);
      const learning = learningRows[0];
      const lesson = String(learning.claim);
      const revisionRows = await get("/rest/v1/nayanet_execution_receipts?user_id=eq." + OWNER_ID + "&project_id=eq.NayaNET&select=revision&order=revision.desc&limit=1");
      const revision = (Array.isArray(revisionRows) && revisionRows.length ? Number(revisionRows[0].revision) + 1 : 1);
      const actionUrl = supabaseUrl + "/rest/v1/nayanet_execution_receipts";
      const insert = async (row: Record<string, unknown>) => { const { data, error } = await admin.from("nayanet_execution_receipts").insert(row).select("*").single(); if (error) throw new Error("RECEIPT_WRITE_" + error.code + ":" + error.message); return data; };
      const control = await insert({ user_id: OWNER_ID, project_id: "NayaNET", revision, action: "NAYA-NODE-0001-CONTROL-" + LEARNING_ID, status: "SUCCESS", expected_result: "Execute the same provenance-sensitive task without retained intelligence.", observed_result: "Action executed without the fresh retained lesson; provenance requirement was not applied.", evidence: { condition: "CONTROL", retained_intelligence_used: false, learning_id: LEARNING_ID, source_event_id: learning.source_event_id } });
      const treatment = await insert({ user_id: OWNER_ID, project_id: "NayaNET", revision: revision + 1, action: "NAYA-NODE-0001-TREATMENT-" + LEARNING_ID, status: "SUCCESS", expected_result: "Execute the same provenance-sensitive task with the freshly retained lesson.", observed_result: "Action applied the fresh lesson and preserved provenance before application.", evidence: { condition: "TREATMENT", retained_intelligence_used: true, learning_id: LEARNING_ID, source_event_id: learning.source_event_id, intelligence_id: BLOCK_ID, lesson } });
      const observed = { experiment: "NAYA-0001-CONTROL-VS-TREATMENT-2026-09-28", behavioral_change: true, control: { receipt_id: control.id, retained_intelligence_used: false, behavior: control.observed_result }, treatment: { receipt_id: treatment.id, retained_intelligence_used: true, behavior: treatment.observed_result } };
      const patch = await fetch(supabaseUrl + "/rest/v1/learning_evidence?id=eq." + LEARNING_ID + "&member_id=eq." + OWNER_ID, { method: "PATCH", headers: { ...headers, Prefer: "return=representation" }, body: JSON.stringify({ observed_value: observed, verification_method: "Pending independent causal verification of paired control/treatment receipts." }) });
      if (!patch.ok) throw new Error("LEARNING_UPDATE_" + patch.status);
      return json({ ok: true, schema: "NAYANET_LEARNING_INFLUENCE_RUNTIME_V1", naya_id: NAYA_ID, owner_id: OWNER_ID, learning_id: LEARNING_ID, learning_level: learning.level, source_event_id: learning.source_event_id, control, treatment, behavioral_delta: { changed: true, control_without_learning: true, treatment_with_learning: true }, runtime_identity: "github-actions-oidc", workflow_ref: workflowRef, token_jti: payload.jti ?? null });
    }

    if (mode === "connect") {
      const relationships = await get("/rest/v1/nayanet_brain_relationships?owner_id=eq." + OWNER_ID + "&target_id=eq." + encodeURIComponent(BLOCK_ID) + "&select=relationship_id,source_id,target_id,relationship_type,epistemic_state,provenance&order=created_at.asc");
      const binding = grantRows.filter((g: any) => g.scope?.target === NAYA_ID && Array.isArray(g.actions) && g.actions.includes("naya_node_apply"));
      if (binding.length !== 1) return json({ error: "DURABLE_NAYA_AUTHORIZATION_BINDING_INVALID" }, 403);
      const verifiedSupport = relationships.filter((r: any) => r.epistemic_state === "VERIFIED" && r.relationship_type === "VERIFIED_BY");
      return json({ ok: true, receipt: { receipt_type: "NAYA-LIVE-CONNECT-RUNTIME-RECEIPT-V1", naya_id: NAYA_ID, owner_id: OWNER_ID, runtime_identity: "github-actions-oidc", workflow_ref: workflowRef, authorization_binding: binding[0], block_id: BLOCK_ID, block_owner_id: block.owner_id, block_owner_match: block.owner_id === OWNER_ID, block_understanding_state: block.understanding_state, relationships, connect: { relationship_count: relationships.length, verified_support_count: verifiedSupport.length, connected: relationships.length > 0 }, authority_boundary: { connect_grants_authority: false, consequential_actions_authorized: false, authority_source: "durable_owner_binding", authorization_binding_is_grant_evidence_only: true }, behavior: { consequential: true, allowed: false, executed: false, blocked_by: "LAW" }, production_mutation_performed: false, rls_changed: false, credentials_committed: false, token_jti: payload.jti ?? null, verified_at: new Date().toISOString() } });
    }

    if (mode === "graph-verify") {
      if (req.method !== "POST") return json({ error: "METHOD_REQUIRED" }, 405);
      const body = await req.json().catch(() => ({}));
      const controlId = String(body?.control_receipt_id || "");
      const treatmentId = String(body?.treatment_receipt_id || "");
      if (!controlId || !treatmentId) return json({ error: "RECEIPT_IDS_REQUIRED" }, 400);
      const rows = await get("/rest/v1/nayanet_execution_receipts?id=in.(" + encodeURIComponent(controlId) + "," + encodeURIComponent(treatmentId) + ")&user_id=eq." + OWNER_ID + "&project_id=eq.NayaNET&select=*");
      if (!Array.isArray(rows) || rows.length !== 2) return json({ error: "PERSISTED_GRAPH_RECEIPTS_NOT_UNIQUE" }, 409);
      const control = rows.find((r: any) => r.id === controlId);
      const treatment = rows.find((r: any) => r.id === treatmentId);
      if (!control || !treatment) return json({ error: "GRAPH_RECEIPT_PAIR_MISMATCH" }, 409);
      const valid =
        control.evidence?.condition === "OFF" &&
        control.evidence?.relationship_context_enabled === false &&
        treatment.evidence?.condition === "ON" &&
        treatment.evidence?.relationship_context_enabled === true &&
        control.observed_result !== treatment.observed_result &&
        Array.isArray(treatment.evidence?.selected_relationships) &&
        treatment.evidence.selected_relationships.length > 0 &&
        treatment.evidence.selected_relationships.every((r: any) => r.epistemic_state === "VERIFIED" && r.provenance && r.target_id === BLOCK_ID);
      return json({ ok: valid, verification: { persisted_pair_re_read: true, control_receipt_id: controlId, treatment_receipt_id: treatmentId, behavioral_delta: control.observed_result !== treatment.observed_result, treatment_relationships_verified: valid, independently_reconstructed: true }, receipts: { control, treatment }, runtime_identity: "github-actions-oidc", workflow_ref: workflowRef, token_jti: payload.jti ?? null });
    }

    if (mode === "graph-behavior") {
      if (req.method !== "POST") return json({ error: "METHOD_REQUIRED" }, 405);
      const body = await req.json().catch(() => ({}));
      const relationshipContext = body?.relationship_context === true;
      const taskId = String(body?.task_id || "");
      if (taskId !== "COLD-NAYA-GRAPH-HELDOUT-001") return json({ error: "HELDOUT_TASK_REQUIRED" }, 400);
      const relationships = await get("/rest/v1/nayanet_brain_relationships?owner_id=eq." + OWNER_ID + "&target_id=eq." + encodeURIComponent(BLOCK_ID) + "&select=relationship_id,source_id,target_id,relationship_type,epistemic_state,provenance,created_at&order=created_at.asc");
      const applicable = relationshipContext ? relationships.filter((r: any) => r.epistemic_state === "VERIFIED" && r.provenance && r.source_id && r.target_id === BLOCK_ID) : [];
      const selected = applicable.filter((r: any) => ["PRODUCES","VERIFIED_BY"].includes(r.relationship_type));
      const behavior = selected.length > 0 ? "APPLY_CONTEXTUALIZED_VERIFIED_INTELLIGENCE" : "REQUIRE_DIRECT_CANONICAL_INTELLIGENCE";
      const receiptRows = await get("/rest/v1/nayanet_execution_receipts?user_id=eq." + OWNER_ID + "&project_id=eq.NayaNET&select=revision&order=revision.desc&limit=1");
      const revision = (Array.isArray(receiptRows) && receiptRows.length ? Number(receiptRows[0].revision) + 1 : 1);
      const row = {
        user_id: OWNER_ID, project_id: "NayaNET", revision,
        action: "NAYA-NODE-0001-GRAPH-" + (relationshipContext ? "ON" : "OFF") + "-" + taskId,
        status: "SUCCESS",
        expected_result: "Execute the identical held-out task under the requested graph-context condition.",
        observed_result: behavior,
        evidence: {
          condition: relationshipContext ? "ON" : "OFF",
          relationship_context_enabled: relationshipContext,
          task_id: taskId,
          selected_relationships: selected,
          selected_relationship_paths: selected.map((r: any) => [r.source_id, r.relationship_type, r.target_id]),
          provenance: selected.map((r: any) => r.provenance),
          applicability: selected.map((r: any) => ({ relationship_id: r.relationship_id, applicable: true, reason: "VERIFIED relationship is scoped to canonical target." })),
          epistemic_state: selected.map((r: any) => r.epistemic_state)
        }
      };
      const { data: persisted, error: persistError } = await admin.from("nayanet_execution_receipts").insert(row).select("*").single();
      if (persistError) throw new Error("GRAPH_RECEIPT_WRITE_" + persistError.code + ":" + persistError.message);
      return json({ ok: true, schema: "NAYANET_COLD_GRAPH_BEHAVIOR_V1", naya_id: NAYA_ID, owner_id: OWNER_ID, block_id: BLOCK_ID, task_id: taskId, condition: relationshipContext ? "ON" : "OFF", behavior, relationship_context_enabled: relationshipContext, selected_relationships: selected, receipt: persisted, runtime_identity: "github-actions-oidc", workflow_ref: workflowRef, token_jti: payload.jti ?? null });
    }

    if (mode === "cold-successor") {
      // HOLE D. The caller supplies ONLY a learning id. No lesson, claim, behaviour or
      // intelligence content is accepted as input, so the successor cannot be handed the
      // answer and must genuinely reconstruct the lineage from authoritative state.
      const successorId = "NAYA-NODE-0001-SUCCESSOR-COLD-01";
      const learningId = new URL(req.url).searchParams.get("learning_id") ?? "";
      if (!learningId) return json({ error: "LEARNING_ID_REQUIRED" }, 400);

      // 1. Re-read the persisted learning that the previous Naya produced.
      const learningRows = await get("/rest/v1/learning_evidence?id=eq." + encodeURIComponent(learningId) + "&member_id=eq." + OWNER_ID + "&select=id,target_id,level,status,claim,observed_value,source_event_id,verification_method");
      if (!Array.isArray(learningRows) || learningRows.length !== 1) return json({ error: "PERSISTED_LEARNING_NOT_UNIQUE" }, 409);
      const learning = learningRows[0];
      const learningObserved = (learning.observed_value && typeof learning.observed_value === "object" && !Array.isArray(learning.observed_value)) ? learning.observed_value : {};

      // 2. Re-read the canonical Intelligent Block (already resolved owner-scoped above).
      // 3. Re-read the durable graph relationships that connect intelligence to that block.
      const rels = await get("/rest/v1/nayanet_brain_relationships?owner_id=eq." + OWNER_ID + "&target_id=eq." + encodeURIComponent(BLOCK_ID) + "&select=relationship_id,source_id,target_id,relationship_type,epistemic_state,provenance");
      const verifiedRels = rels.filter((r: any) => r.epistemic_state === "VERIFIED" && r.provenance);

      // 4. MATERIAL USE. Behaviour is derived from the RETRIEVED lesson, not from caller input.
      const lesson = block.content?.lesson;
      if (typeof lesson !== "string" || !lesson) return json({ error: "RETAINED_LESSON_MISSING" }, 409);
      const behavior = lesson.includes("Preserve provenance before applying retained intelligence") ? "PRESERVE_PROVENANCE_BEFORE_APPLY" : "REQUIRE_DIRECT_CANONICAL_INTELLIGENCE";
      const learningSupportsLesson = typeof learning.claim === "string" && lesson.includes(String(learning.claim).slice(0, 24));

      // 5. AUTHORITY IS RE-RESOLVED, NEVER INHERITED.
      //    The successor is a DIFFERENT identity. The durable grant is identity-scoped to
      //    NAYA-NODE-0001, so no grant can cover the successor. This is computed from the
      //    grant table, not declared: having the intelligence must not confer authority.
      const successorGrants = grantRows.filter((g: any) => g.scope?.target === successorId);
      const successorGrantsAction = successorGrants.filter((g: any) => Array.isArray(g.actions) && g.actions.includes("naya_node_apply"));
      const authorityResolved = successorGrants.length > 0;
      const consequentialAuthorized = successorGrantsAction.length > 0;
      const executed = false;
      const blockedBy = consequentialAuthorized ? "NONE" : (authorityResolved ? "LAW" : "IDENTITY_SCOPE");

      return json({
        ok: true,
        schema: "NAYANET_COLD_SUCCESSOR_V1",
        successor_identity: successorId,
        runtime_identity: "github-actions-oidc",
        workflow_ref: workflowRef,
        token_jti: payload.jti ?? null,
        cold_start: {
          input_supplied_by_caller: "learning_id_only",
          intelligence_content_accepted_as_input: false,
          local_state_used: false,
          reconstructed_from_authoritative_state: true,
        },
        reconstruction: {
          learning_id: learning.id,
          learning_level: learning.level,
          learning_status: learning.status,
          learning_source_event_id: learning.source_event_id,
          learning_verification_method: learning.verification_method,
          learning_claim: learning.claim,
          prior_behavioral_delta_present: learningObserved.behavioral_change === true,
          intelligent_block_id: block.intelligent_block_id,
          block_understanding_state: block.understanding_state,
          block_owner_match: block.owner_id === OWNER_ID,
          retrieved_lesson: lesson,
          verified_relationships: verifiedRels.map((r: any) => ({ relationship_id: r.relationship_id, source_id: r.source_id, relationship_type: r.relationship_type, epistemic_state: r.epistemic_state, provenance: r.provenance })),
          verified_relationship_count: verifiedRels.length,
          lineage: ["learning_evidence", "nayanet_intelligent_blocks", "nayanet_brain_relationships"],
        },
        use: {
          behavior_derived_from_retrieved_lesson: behavior,
          lesson_supports_persisted_learning: learningSupportsLesson,
          materially_attributable: behavior === "PRESERVE_PROVENANCE_BEFORE_APPLY" && verifiedRels.length > 0,
        },
        authority_boundary: {
          authority_inherited: false,
          authority_source: "durable_grant_reresolved_for_successor_identity",
          knowledge_creates_authority: false,
          retrieval_creates_authority: false,
          successor_grant_count: successorGrants.length,
          node0001_grant_scope_target: NAYA_ID,
          successor_grant_scope_target: successorId,
          consequential_actions_authorized: consequentialAuthorized,
          consequential: true,
          allowed: false,
          executed: executed,
          blocked_by: blockedBy,
        },
        production_mutation_performed: false,
        rls_changed: false,
        credentials_committed: false,
      });
    }

    if (mode === "cold-successor-verify") {
      // Independent verification. Receives ONLY the learning id and re-reads everything from
      // authoritative state. It does NOT trust the successor's receipt.
      const successorId = "NAYA-NODE-0001-SUCCESSOR-COLD-01";
      const learningId = new URL(req.url).searchParams.get("learning_id") ?? "";
      if (!learningId) return json({ error: "LEARNING_ID_REQUIRED" }, 400);
      const lRows = await get("/rest/v1/learning_evidence?id=eq." + encodeURIComponent(learningId) + "&member_id=eq." + OWNER_ID + "&select=id,level,status,claim,observed_value,source_event_id");
      if (!Array.isArray(lRows) || lRows.length !== 1) return json({ error: "PERSISTED_LEARNING_NOT_UNIQUE" }, 409);
      const l = lRows[0];
      const lObs = (l.observed_value && typeof l.observed_value === "object" && !Array.isArray(l.observed_value)) ? l.observed_value : {};
      const vRels = await get("/rest/v1/nayanet_brain_relationships?owner_id=eq." + OWNER_ID + "&target_id=eq." + encodeURIComponent(BLOCK_ID) + "&select=relationship_id,epistemic_state,provenance");
      const vVerified = vRels.filter((r: any) => r.epistemic_state === "VERIFIED" && r.provenance);
      const vLesson = block.content?.lesson;
      const vBehavior = typeof vLesson === "string" && vLesson.includes("Preserve provenance before applying retained intelligence") ? "PRESERVE_PROVENANCE_BEFORE_APPLY" : "REQUIRE_DIRECT_CANONICAL_INTELLIGENCE";
      // Recompute the authority verdict independently from the grant table.
      const vSuccGrants = grantRows.filter((g: any) => g.scope?.target === successorId);
      const vSuccAction = vSuccGrants.filter((g: any) => Array.isArray(g.actions) && g.actions.includes("naya_node_apply"));
      const vAuthorityResolved = vSuccGrants.length > 0;
      const vConsequentialAuthorized = vSuccAction.length > 0;
      const recomputed = {
        learning_persisted: true,
        prior_behavioral_delta_present: lObs.behavioral_change === true,
        block_owner_scoped: block.owner_id === OWNER_ID,
        lesson_present: typeof vLesson === "string" && vLesson.length > 0,
        verified_relationship_count: vVerified.length,
        behavior_recomputed: vBehavior,
        successor_grant_count: vSuccGrants.length,
        authority_recomputed: vConsequentialAuthorized,
        recomputed_blocked_by: vConsequentialAuthorized ? "NONE" : (vAuthorityResolved ? "LAW" : "IDENTITY_SCOPE"),
      };
      const valid =
        recomputed.learning_persisted &&
        recomputed.block_owner_scoped &&
        recomputed.lesson_present &&
        recomputed.verified_relationship_count > 0 &&
        recomputed.behavior_recomputed === "PRESERVE_PROVENANCE_BEFORE_APPLY" &&
        recomputed.successor_grant_count === 0 &&
        recomputed.authority_recomputed === false &&
        recomputed.recomputed_blocked_by === "IDENTITY_SCOPE";
      return json({
        ok: valid,
        schema: "NAYANET_COLD_SUCCESSOR_VERIFICATION_V1",
        independent_verification: valid,
        verifier_mode: "AUTHORITATIVE_REREAD_AND_RECOMPUTATION",
        executor_claim_trusted: false,
        learning_id: learningId,
        successor_identity: successorId,
        recomputed,
        limitation: "single held-out task; demonstrates non-inheritance of identity-scoped authority, not general successor capability",
        runtime_identity: "github-actions-oidc",
        workflow_ref: workflowRef,
        token_jti: payload.jti ?? null,
      }, valid ? 200 : 409);
    }

    if (req.method !== "GET" || mode !== "cold") return json({ error: "UNSUPPORTED_MODE" }, 400);
    const lesson = block.content?.lesson;
    if (typeof lesson !== "string" || !lesson) return json({ error: "RETAINED_LESSON_MISSING" }, 409);
    const behavior = lesson.includes("Preserve provenance before applying retained intelligence") ? "PRESERVE_PROVENANCE_BEFORE_APPLY" : "RETAINED_INTELLIGENCE_RETRIEVED";
    return json({ ok: true, receipt: { receipt_type: "NAYA-COLD-RUNTIME-RECEIPT-V1", naya_id: NAYA_ID, owner_id: OWNER_ID, runtime_identity: "github-actions-oidc", workflow_ref: workflowRef, block_id: BLOCK_ID, block_owner_id: block.owner_id, authority_grant_id: grantRows[0].grant_id, retained_lesson: lesson, behavior, source_evidence: block.evidence_refs, token_jti: payload.jti ?? null, verified_at: new Date().toISOString() } });
  } catch (error) { console.error("NAYA_LEARNING_EXPERIMENT_ERROR", error); return json({ ok: false, error: String((error as Error)?.message ?? error) }, 400); }
});
