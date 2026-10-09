import { createRemoteJWKSet, jwtVerify } from "https://esm.sh/jose@6.0.10";
import { createClient } from "npm:@supabase/supabase-js@2";
import { resolveScorecardReceiptAuthority } from "./scorecard_receipt_authority.js";
import { checkAdmission } from "./admission_contract.js";

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

// H13-LOCK-IN-LAW-START
// H13 (2026-10-03): the lock-in below mutates canonical learning state
// (block->LEARNED, relationship->VERIFIED, checkpoint->LEARNED). It must
// re-resolve a live LAW authority grant, not rely on OIDC workflow-binding
// alone. Decision semantics mirror supabase/functions/nayanet-law-runtime/law.ts
// (evaluateLaw / targetMatches / expiry). The CI workflow cannot satisfy
// NEEDS_HUMAN_AUTHORIZATION, so the fail-closed mapping here is: any decision
// other than AUTHORIZED denies the lock-in. Written without TS annotations so
// the shipped block can be executed verbatim in the loop's node harness.
const LEARNING_LOCK_IN_ACTION = "learning_lock_in";

const lawGrantTargetMatches = (grant, intelligentBlockId, learningTargetId, projectId) => {
  const scope = (grant && grant.scope) || {};
  const matches = (value, requested) =>
    typeof value === "string" && value.trim().length > 0 &&
    typeof requested === "string" && requested.trim().length > 0 &&
    value === requested;
  return matches(scope.target, intelligentBlockId) ||
    matches(scope.target, learningTargetId) ||
    matches(scope.project_id, intelligentBlockId) ||
    matches(scope.project_id, projectId);
};

const lawGrantIsExpired = (grant, now) =>
  Boolean(grant && grant.expires_at && new Date(String(grant.expires_at)).getTime() <= now.getTime());

async function resolveLearningLockInLaw(admin, ownerId, intelligentBlockId, learningTargetId) {
  const { data, error } = await admin
    .from("nayanet_authority_grants")
    .select("*")
    .eq("issuer_id", ownerId)
    .eq("subject_id", ownerId);
  if (error) throw error;
  const grants = data || [];
  const now = new Date();
  const sameSubject = grants.filter((g) => g.subject_id === ownerId && g.issuer_id === ownerId);
  const matchingIntent = sameSubject.filter(
    (g) => Array.isArray(g.actions) && g.actions.includes(LEARNING_LOCK_IN_ACTION) &&
      lawGrantTargetMatches(g, intelligentBlockId, learningTargetId, "NayaNET")
  );
  const invalid = matchingIntent.find(
    (g) => g.status === "REVOKED" || Boolean(g.revoked_at) || g.status === "INVALID" ||
      lawGrantIsExpired(g, now)
  );
  if (invalid) {
    const grantId = String(invalid.grant_id || "");
    const reason = (invalid.status === "REVOKED" || Boolean(invalid.revoked_at)) ? "GRANT_REVOKED"
      : lawGrantIsExpired(invalid, now) ? "GRANT_EXPIRED" : "GRANT_INVALID";
    return { authorized: false, reason: reason, authority_refs: [grantId], expires_at: invalid.expires_at || null };
  }
  const active = matchingIntent.find(
    (g) => g.status === "ACTIVE" && !g.revoked_at && !lawGrantIsExpired(g, now)
  );
  if (active) {
    return {
      authorized: true,
      reason: "ACTIVE_IN_SCOPE_GRANT",
      authority_refs: [String(active.grant_id || "")],
      expires_at: active.expires_at || null,
    };
  }
  return { authorized: false, reason: "NO_MATCHING_ACTIVE_AUTHORITY", authority_refs: [], expires_at: null };
}
// H13-LOCK-IN-LAW-END

// SN-0521 CV-07: evidence_refs content validation.
// Non-empty was the only check; junk strings ("", " ", "0", "not-a-verification")
// and forged CVO IDs ("CVO-forged") promoted learnings while recording
// causal_verification_id: null. Fail-closed: reject junk before any mutation.
//
// Policy: at least one ref must be a well-formed causal-verification ID
// (CVO- prefix, uppercase alphanumeric/hyphen segments, e.g.
// CVO-NAYA-NODE-0001-FRESH-LEARNING-2026-09-28). The verification_method
// requires "independent causal verification"; without a CVO ref the promotion
// would discharge a requirement it never checks.
const CVO_ID_PATTERN = /^CVO-[A-Z0-9-]+$/;
function validateEvidenceRefs(refs: any[]): { valid: boolean; reason?: string; invalidRefs?: string[] } {
  const invalidRefs: string[] = [];
  let hasValidCvo = false;
  for (const ref of refs) {
    const s = String(ref ?? "").trim();
    // Reject empty, whitespace-only, or trivially short refs ("0", "x", "ab").
    if (!s || s.length < 3) {
      invalidRefs.push(String(ref));
      continue;
    }
    if (s.startsWith("CVO-")) {
      // CVO- refs must be uppercase alphanumeric/hyphen. Rejects "CVO-forged".
      // "CVO-1" (test shorthand) passes; real IDs like CVO-NAYA-NODE-0001-... pass.
      if (!CVO_ID_PATTERN.test(s) || s.length < 5) {
        invalidRefs.push(String(ref));
        continue;
      }
      hasValidCvo = true;
    }
  }
  if (invalidRefs.length > 0) {
    return { valid: false, reason: "EVIDENCE_REFS_INVALID", invalidRefs };
  }
  if (!hasValidCvo) {
    return { valid: false, reason: "EVIDENCE_REFS_MISSING_CAUSAL_VERIFICATION", invalidRefs: [] };
  }
  return { valid: true };
}
// SN-0521-CV-07-END

// H8-7 repair (2026-10-03): governed task-class registry. Applicability is a
// GOVERNED assertion, not a text-derived one. The trigger regexes only PROPOSE
// candidate classes; APPLICABLE requires a provenance-attested declaration
// (block.provenance.declared_task_classes, written by a governed capture path)
// that is a member of this closed registry. Lesson text alone can never yield
// APPLICABLE — fail-closed on TEXT_TRIGGER_WITHOUT_GOVERNED_DECLARATION.
const TASK_CLASS_REGISTRY: Record<string, { triggers: RegExp; limitations: string[] }> = {
  provenance_sensitive: {
    triggers: /preserve provenance|provenance before applying retained intelligence/i,
    limitations: ["Only use where provenance preservation is materially relevant."],
  },
  repository_correction: {
    triggers: /act-first within guardrails|asking permission and acting|within the guardrails and adds value/i,
    limitations: ["Does not create authority; LAW must independently authorize consequential action."],
  },
  active_intelligence_sensitive: {
    triggers: /persistence alone is memory, not proof of active intelligence|retrieved intelligence does not grant authority/i,
    limitations: ["Persistence and retrieval never create verification or authority; truth and LAW boundaries remain mandatory."],
  },
  learning_reuse: {
    triggers: /(?:preserve provenance|act-first within guardrails|persistence alone is memory, not proof of active intelligence)/i,
    limitations: ["Reuses verified learning only; never a standalone authority claim."],
  },
  contextual_retrieval: {
    triggers: /(?:provenance before applying retained intelligence|asking permission and acting|retrieved intelligence does not grant authority)/i,
    limitations: ["Retrieval context only; does not alter verification or authority state."],
  },
};

function deriveGraphApplicability(block: any) {
  const lesson = String(block?.content?.lesson ?? "");
  // (1) Proposals from lesson text — advisory only, never authoritative.
  const proposedTaskClasses: string[] = [];
  for (const taskClass of Object.keys(TASK_CLASS_REGISTRY)) {
    if (TASK_CLASS_REGISTRY[taskClass].triggers.test(lesson)) proposedTaskClasses.push(taskClass);
  }
  // (2) Governed decision: only provenance-attested declarations count.
  const declaredRaw = block?.provenance?.declared_task_classes;
  const declared: string[] = Array.isArray(declaredRaw)
    ? declaredRaw.filter((c: unknown) => typeof c === "string")
    : [];
  const governed = declared.filter((c) => Object.prototype.hasOwnProperty.call(TASK_CLASS_REGISTRY, c));
  const ungoverned = declared.filter((c) => !Object.prototype.hasOwnProperty.call(TASK_CLASS_REGISTRY, c));
  if (governed.length > 0) {
    const classes = Array.from(new Set(governed));
    return {
      state: "APPLICABLE",
      task_classes: classes,
      limitations: Array.from(new Set(classes.flatMap((c) => TASK_CLASS_REGISTRY[c].limitations))),
      proposed_task_classes: proposedTaskClasses,
      ungoverned_declared_task_classes: ungoverned,
    };
  }
  return {
    state: "UNKNOWN",
    task_classes: [],
    proposed_task_classes: proposedTaskClasses,
    limitations: proposedTaskClasses.length > 0
      ? ["TEXT_TRIGGER_WITHOUT_GOVERNED_DECLARATION", "NO_PREDECLARED_TASK_CLASS"]
      : ["NO_PREDECLARED_TASK_CLASS"],
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

      let checkpointProvenance = "CURRENT_STATE_MATCH";
      let immutableCheckpointEvidence: any = null;
      if (mismatched.length) {
        // nayanet_project_cognition_state is intentionally one mutable row per
        // (owner, project). A later intelligence commit may advance it beyond an
        // older block. Historical learning must therefore reconstruct the old
        // checkpoint from the immutable intelligence_commit receipt rather than
        // clobbering or trusting the current mutable row.
        const { data: commitReceipt, error: commitReceiptError } = await admin
          .from("nayanet_execution_receipts")
          .select("id,action,evidence,created_at")
          .eq("id", commitReceiptId)
          .eq("user_id", ownerId)
          .eq("project_id", "NayaNET")
          .maybeSingle();
        if (commitReceiptError) throw commitReceiptError;
        const ev = commitReceipt?.evidence && typeof commitReceipt.evidence === "object" ? commitReceipt.evidence : {};
        const receiptMatchesHistoricalChain =
          commitReceipt?.action === "intelligence_commit" &&
          ev.checkpoint_id === checkpoint.id &&
          ev.event_row_id === event.id &&
          ev.intelligent_block_id === blockId &&
          ev.lineage_id === lineage.id &&
          ev.relationship_id === relationship.relationship_id &&
          ev.index_id === index.id;
        if (!receiptMatchesHistoricalChain) {
          return json({
            ok: false,
            error: "CHECKPOINT_PROVENANCE_MISMATCH",
            checkpoint_id: checkpoint.id,
            checkpoint_revision: checkpoint.revision ?? null,
            mismatched,
            immutable_receipt_reconstruction: false,
          }, 409);
        }
        checkpointProvenance = "IMMUTABLE_COMMIT_RECEIPT_SNAPSHOT";
        immutableCheckpointEvidence = {
          receipt_id: commitReceipt.id,
          checkpoint_id: ev.checkpoint_id,
          event_id: ev.event_row_id,
          intelligent_block_id: ev.intelligent_block_id,
          lineage_id: ev.lineage_id,
          relationship_id: ev.relationship_id,
          index_id: ev.index_id,
          content_hash: ev.content_hash ?? null,
          authority_grant_id: ev.authority_grant_id ?? null,
        };
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
          checkpoint_provenance: checkpointProvenance,
          immutable_checkpoint_evidence: immutableCheckpointEvidence,
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
      // ADMISSION CONTRACT (2026-10-09, kernel/protocol/learning_capture.py):
      // a system-captured candidate may enter CANDIDATE status only with a
      // preregistered experiment design that passes all seven rules. Fail
      // closed: a missing or malformed design is rejected, and nothing is
      // inserted. The repair path above only re-links an already-admitted
      // row and is intentionally not re-gated. The human-director lane and
      // the v7-smart-note-canonical Receiver path are separate lanes and
      // are never gated by this contract.
      const admissionDesign = (body as any)?.admission ?? null;
      const admission = checkAdmission(admissionDesign);
      if (!admission.passed) {
        return json({
          ok: false,
          error: "ADMISSION_CONTRACT_REJECTED",
          failed_rules: admission.failed_rules,
          reasons: admission.reasons,
        }, 409);
      }
      const admissionVerdict = {
        passed: true,
        failed_rules: [],
        checked_at: new Date().toISOString(),
        contract: "kernel/protocol/learning_capture.py:check_admission",
      };
      const candidate = { member_id: ownerId, target_id: "NAYA-NODE-0001", level: "E1_UNDERSTANDS", provenance: "OBSERVATION", status: "CANDIDATE", claim: lesson, observed_value: { intelligent_block_id: blockId, source_event_id: event.id, source_event_key: event.event_id, commit_receipt_id: commitReceiptId, lineage_id: lineage.id, relationship_id: relationship.relationship_id, index_id: index.id, checkpoint_id: checkpoint.id, checkpoint_provenance: checkpointProvenance, immutable_checkpoint_evidence: immutableCheckpointEvidence, provenance_preserved: true, admission_design: admissionDesign, admission_verdict: admissionVerdict }, verification_method: "Pending independent causal verification of the persisted Event → Intelligent Block → Lineage → Relationship → Index → Checkpoint chain.", source_event_id: event.id };
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
      const [block, relationship, checkpoint, commitReceipt] = await Promise.all([
        admin.from("nayanet_intelligent_blocks").select("intelligent_block_id,understanding_state,provenance").eq("intelligent_block_id", String((observed as any).intelligent_block_id || "")).eq("owner_id", ownerId).maybeSingle(),
        admin.from("nayanet_brain_relationships").select("relationship_id,epistemic_state,provenance").eq("relationship_id", String((observed as any).relationship_id || "")).eq("owner_id", ownerId).maybeSingle(),
        admin.from("nayanet_project_cognition_state").select("id,state,status,revision,updated_at").eq("id", String((observed as any).checkpoint_id || "")).eq("user_id", ownerId).eq("project_id", "NayaNET").maybeSingle(),
        admin.from("nayanet_execution_receipts").select("id,action,evidence,learning").eq("id", String((observed as any).commit_receipt_id || "")).eq("user_id", ownerId).eq("project_id", "NayaNET").maybeSingle(),
      ]);
      if (block.error) throw block.error;
      if (relationship.error) throw relationship.error;
      if (checkpoint.error) throw checkpoint.error;
      if (commitReceipt.error) throw commitReceipt.error;
      const historicalReceiptLockIn =
        (observed as any).checkpoint_provenance === "IMMUTABLE_COMMIT_RECEIPT_SNAPSHOT" &&
        Array.isArray(commitReceipt.data?.learning) &&
        commitReceipt.data.learning.some((entry: any) => entry?.learning_id === retained.id && entry?.verified === true);
      const integration = {
        core_intelligence_updated: block.data?.understanding_state === "LEARNED",
        progressive_intelligence_lock_in: checkpoint.data?.state?.status === "LEARNED" || historicalReceiptLockIn,
        intelligent_block_state: block.data?.understanding_state ?? null,
        relationship_epistemic_state: relationship.data?.epistemic_state ?? null,
        checkpoint_state_status: checkpoint.data?.state?.status ?? null,
        checkpoint_id: checkpoint.data?.id ?? null,
        checkpoint_provenance: (observed as any).checkpoint_provenance || "CURRENT_STATE_MATCH",
        historical_receipt_lock_in: historicalReceiptLockIn,
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

    // SN-0521 CV-07: validate evidence_refs content before any mutation.
    // Junk strings must not promote.
    const evidenceValidation = validateEvidenceRefs(refs);
    if (!evidenceValidation.valid) {
      return json({
        ok: false,
        error: evidenceValidation.reason,
        invalid_refs: evidenceValidation.invalidRefs,
      }, 400);
    }

    const verificationMethod = String(
      body?.verification_method || learning.verification_method || "Independent runtime verification."
    );

    // SN-0521 CV-06: read provenance links BEFORE any mutation. The LAW gate
    // needs intelligentBlockId, and every canonical mutation must sit behind
    // the grant gate. observed_value is unchanged by promotion, so reading
    // from `learning` (pre-promotion) is equivalent.
    const observed = learning.observed_value && typeof learning.observed_value === "object" && !Array.isArray(learning.observed_value)
      ? learning.observed_value
      : {};
    const intelligentBlockId = String((observed as any).intelligent_block_id || "");
    const learningTargetId = String((learning as any).target_id || "").trim();
    const relationshipId = String((observed as any).relationship_id || "");
    const checkpointId = String((observed as any).checkpoint_id || "");
    const lineageId = String((observed as any).lineage_id || "");
    const indexId = String((observed as any).index_id || "");
    if (!intelligentBlockId || !relationshipId || !checkpointId || !lineageId || !indexId) {
      return json({ ok: false, error: "LEARNING_PROVENANCE_LINKS_REQUIRED" }, 409);
    }

    // SN-0521 CV-06: LAW gate runs BEFORE any mutation. A refusal must prevent
    // writes, not just report them. Zero mutations have occurred at this point.
    // H13: fail-closed LAW authorization for the canonical lock-in mutations below.
    // Authority bridge (SN-0340 Scorecard Law): a personal grant OR a valid
    // scorecard receipt carries the Human Director's authority. The receipt IS
    // his decision — he designed the scale and commanded the highest honest
    // score to act. Fail-closed: neither valid, no promotion.
    const lawDecision = await resolveLearningLockInLaw(admin, ownerId, intelligentBlockId, learningTargetId);
    let authorityDecision = lawDecision;
    const scorecardReceipt = (body as any)?.scorecard_receipt;
    if (!lawDecision.authorized && scorecardReceipt && typeof scorecardReceipt === "object") {
      const receiptDecision = resolveScorecardReceiptAuthority(scorecardReceipt, intelligentBlockId, new Date());
      if (receiptDecision.authorized) {
        authorityDecision = receiptDecision;
      } else if ((receiptDecision as any).receipt_reasons?.length) {
        // Receipt was offered but invalid — surface why, still denied.
        return json({
          ok: false,
          error: "LEARNING_LOCK_IN_LAW_DENIED",
          reason: receiptDecision.reason,
          receipt_reasons: (receiptDecision as any).receipt_reasons,
          authority_refs: [],
          action: LEARNING_LOCK_IN_ACTION,
          target: intelligentBlockId,
        }, 403);
      }
    }
    if (!authorityDecision.authorized) {
      return json({
        ok: false,
        error: "LEARNING_LOCK_IN_LAW_DENIED",
        reason: authorityDecision.reason,
        authority_refs: authorityDecision.authority_refs,
        action: LEARNING_LOCK_IN_ACTION,
        target: intelligentBlockId,
      }, 403);
    }

    // SN-0521 CV-06: validate receipt existence BEFORE promoting learning.
    // Previously RECEIPT_NOT_FOUND_OR_NOT_OWNED fired after learning was ACTIVE.
    let existingReceiptForUpdate: any = null;
    const receiptId = String(body?.receipt_id || "");
    if (receiptId) {
      const { data: receiptLookup, error: receiptLookupError } = await admin
        .from("nayanet_execution_receipts")
        .select("*")
        .eq("id", receiptId)
        .eq("user_id", ownerId)
        .eq("project_id", "NayaNET")
        .maybeSingle();
      if (receiptLookupError) throw receiptLookupError;
      if (!receiptLookup) return json({ ok: false, error: "RECEIPT_NOT_FOUND_OR_NOT_OWNED" }, 404);
      existingReceiptForUpdate = receiptLookup;
    }

    // All gates passed. Mutations begin here.
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
    if (receiptId && existingReceiptForUpdate) {
      const existingReceipt = existingReceiptForUpdate;
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

    let historicalCommitReceipt = null;
    const historicalCommitReceiptId = String((observed as any).commit_receipt_id || "");
    const historicalCheckpointProvenance = (observed as any).checkpoint_provenance === "IMMUTABLE_COMMIT_RECEIPT_SNAPSHOT";
    if (historicalCheckpointProvenance) {
      if (!historicalCommitReceiptId) {
        return json({ ok: false, error: "HISTORICAL_COMMIT_RECEIPT_REQUIRED" }, 409);
      }
      const { data: originalReceipt, error: originalReceiptError } = await admin
        .from("nayanet_execution_receipts")
        .select("*")
        .eq("id", historicalCommitReceiptId)
        .eq("user_id", ownerId)
        .eq("project_id", "NayaNET")
        .maybeSingle();
      if (originalReceiptError) throw originalReceiptError;
      if (!originalReceipt || originalReceipt.action !== "intelligence_commit") {
        return json({ ok: false, error: "HISTORICAL_COMMIT_RECEIPT_NOT_FOUND" }, 409);
      }
      const immutableLearning = Array.isArray(originalReceipt.learning) ? originalReceipt.learning : [];
      const immutableVerificationRecord = {
        learning_id: promoted.id,
        verified: true,
        verification_method: verificationMethod,
        verification_runtime: "github-actions-oidc",
        verification_runtime_jti: payload.jti ?? null,
        verified_at: new Date().toISOString(),
        historical_checkpoint_provenance: "IMMUTABLE_COMMIT_RECEIPT_SNAPSHOT",
        law_authority_refs: lawDecision.authority_refs,
        law_decision_reason: lawDecision.reason,
      };
      const immutableAlreadyRecorded = immutableLearning.some(
        (entry: any) => entry?.learning_id === promoted.id && entry?.verified === true
      );
      const { data: updatedOriginalReceipt, error: originalReceiptUpdateError } = await admin
        .from("nayanet_execution_receipts")
        .update({ learning: immutableAlreadyRecorded ? immutableLearning : [...immutableLearning, immutableVerificationRecord] })
        .eq("id", historicalCommitReceiptId)
        .eq("user_id", ownerId)
        .select("*")
        .single();
      if (originalReceiptUpdateError) throw originalReceiptUpdateError;
      historicalCommitReceipt = updatedOriginalReceipt;
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
      law_authority_refs: lawDecision.authority_refs,
      law_decision_reason: lawDecision.reason,
      law_evaluated_at: new Date().toISOString(),
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
      law_authority_refs: lawDecision.authority_refs,
      law_decision_reason: lawDecision.reason,
      law_evaluated_at: new Date().toISOString(),
    };
    const graphApplicability = deriveGraphApplicability(blockAfter);
    const relationshipEvidenceRefs = verificationRefs;
    const relationshipReasonCodes = graphApplicability.state === "APPLICABLE"
      ? ["INDEPENDENT_CAUSAL_VERIFICATION", "LEARNING_VERIFIED", "TASK_APPLICABILITY_GOVERNED_DECLARATION"]
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

    const historicalCheckpoint = historicalCheckpointProvenance;
    const { data: checkpointBefore, error: checkpointReadError } = await admin
      .from("nayanet_project_cognition_state")
      .select("*")
      .eq("id", checkpointId)
      .eq("user_id", ownerId)
      .eq("project_id", "NayaNET")
      .maybeSingle();
    if (checkpointReadError) throw checkpointReadError;
    if (!checkpointBefore) return json({ ok: false, error: "CHECKPOINT_NOT_FOUND_FOR_LOCK_IN" }, 404);

    let checkpointAfter = checkpointBefore;
    if (!historicalCheckpoint) {
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
        law_authority_refs: lawDecision.authority_refs,
        law_decision_reason: lawDecision.reason,
        law_evaluated_at: new Date().toISOString(),
      };
      const checkpointUpdate = await admin
        .from("nayanet_project_cognition_state")
        .update({ state: checkpointState })
        .eq("id", checkpointId)
        .eq("user_id", ownerId)
        .eq("project_id", "NayaNET")
        .select("*")
        .single();
      if (checkpointUpdate.error) throw checkpointUpdate.error;
      checkpointAfter = checkpointUpdate.data;
    }

    const integration = {
      core_intelligence_updated: true,
      progressive_intelligence_lock_in: "LEARNED",
      law_authority: { refs: lawDecision.authority_refs, reason: lawDecision.reason },
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
        state_status: historicalCheckpoint ? "LEARNED_VIA_IMMUTABLE_RECEIPT" : checkpointAfter.state?.status,
        checkpoint_provenance: historicalCheckpoint ? "IMMUTABLE_COMMIT_RECEIPT_SNAPSHOT" : "CURRENT_STATE_MATCH",
      },
    };

    return json({
      ok: true,
      result,
      verification_record: receipt
        ? (receipt.learning || []).find((entry: any) => entry?.learning_id === promoted.id && entry?.verified === true) ?? null
        : null,
      receipt,
      historical_commit_receipt: historicalCommitReceipt,
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
