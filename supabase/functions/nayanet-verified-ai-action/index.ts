import { createRemoteJWKSet, jwtVerify } from "https://esm.sh/jose@6.0.10";
import { createClient } from "npm:@supabase/supabase-js@2";

const ISSUER = "https://token.actions.githubusercontent.com";
const AUDIENCE = "nayanet-runtime";
const REPOSITORY = "SoulSchoolAcademy/NayaPOWER";
const WORKFLOW = ".github/workflows/live-verified-ai-action-proof.yml";
const REF = "refs/heads/main";
const NAYA_ID = "NAYA-NODE-0001";
const OWNER_ID = "adfdf0b8-5558-41d1-9fed-ec51abf4fe2f";
const BLOCK_ID = "IB-NAYA-NODE-0001-0001";
const MISSION_ID = "NAYA-NODE-0001-CONTINUITY";
const ACTION = "naya_node_apply";
const EXPERIMENT_CASE = "NAYA-0001-VERIFIED-AI-ACTION";
const DEPLOYED_SOURCE_REVISION = "e363732be6b96264d68ca6ee508012af4f93ae2a";
const REFUSAL_ACTION = "NAYA-NODE-0001-VERIFIED-AI-ACTION-REFUSAL";
const REFUSAL_EXPECTED_RESULT = "A consequential action must be refused when the presented authority grant is absent, inactive, revoked, expired, or does not cover the requested action and target.";
const EXECUTION_VERIFICATION_PENDING = "PENDING_INDEPENDENT_RUNTIME_VERIFICATION";
const INDEPENDENT_VERIFICATION_METHOD = "INDEPENDENT_RUNTIME_REREAD_OF_PERSISTED_AUTHORITATIVE_STATE";
const JWKS = createRemoteJWKSet(new URL("https://token.actions.githubusercontent.com/.well-known/jwks"));

const json = (body: unknown, status = 200) => new Response(JSON.stringify({deployed_source_revision: DEPLOYED_SOURCE_REVISION, ...(body as object)}), {
  status,
  headers: {"content-type": "application/json", "cache-control": "no-store"},
});

type Json = Record<string, unknown>;

async function auth(req: Request) {
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

const adminClient = () => {
  const url = Deno.env.get("SUPABASE_URL");
  const key = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");
  if (!url || !key) throw new Error("SERVER_AUTH_CONFIG_MISSING");
  return createClient(url, key);
};

async function canonicalDigest(lesson: string, provenance: unknown): Promise<string> {
  const bytes = new TextEncoder().encode(lesson + "|" + JSON.stringify(provenance ?? null));
  const hash = await crypto.subtle.digest("SHA-256", bytes);
  return Array.from(new Uint8Array(hash)).map((b) => b.toString(16).padStart(2, "0")).join("");
}

async function idempotencyRequestFingerprint(input: Json): Promise<string> {
  const canonical = JSON.stringify({
    authority_grant_id: String(input.authority_grant_id ?? ""),
    mission_id: String(input.mission_id ?? ""),
    action: String(input.action ?? ""),
    target: String(input.target ?? ""),
    canonical_block_id: String(input.canonical_block_id ?? ""),
    canonical_digest: String(input.canonical_digest ?? ""),
  });
  const hash = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(canonical));
  return Array.from(new Uint8Array(hash)).map((b) => b.toString(16).padStart(2, "0")).join("");
}

async function resolveAuthority(admin: ReturnType<typeof adminClient>, grantId: string) {
  if (!grantId) {
    return {allowed: false, reason: "AUTHORITY_ABSENT", grant: null};
  }
  const {data: grant, error} = await admin
    .from("nayanet_authority_grants")
    .select("grant_id,issuer_id,subject_id,mission_id,scope,actions,constraints,status,issued_at,expires_at,revoked_at")
    .eq("grant_id", grantId)
    .maybeSingle();
  if (error) throw error;
  if (!grant) return {allowed: false, reason: "AUTHORITY_ABSENT", grant: null};
  const grantIsActive = grant.status === "ACTIVE";
  if (!grantIsActive) return {allowed: false, reason: "AUTHORITY_NOT_ACTIVE", grant};
  if (grant.issuer_id !== OWNER_ID || grant.subject_id !== OWNER_ID) {
    return {allowed: false, reason: "AUTHORITY_CROSS_OWNER", grant};
  }
  if (grant.mission_id !== MISSION_ID) return {allowed: false, reason: "AUTHORITY_MISSION_MISMATCH", grant};
  if ((grant.scope as Json | undefined)?.target !== NAYA_ID) {
    return {allowed: false, reason: "AUTHORITY_SCOPE_MISMATCH", grant};
  }
  if (!Array.isArray(grant.actions) || !grant.actions.includes(ACTION)) {
    return {allowed: false, reason: "AUTHORITY_ACTION_NOT_GRANTED", grant};
  }
  if (grant.revoked_at) return {allowed: false, reason: "AUTHORITY_REVOKED", grant};
  if (grant.expires_at && new Date(grant.expires_at).getTime() <= Date.now()) {
    return {allowed: false, reason: "AUTHORITY_EXPIRED", grant};
  }
  return {allowed: true, reason: "ALLOW", grant};
}

async function readCanonicalBlock(admin: ReturnType<typeof adminClient>) {
  const {data, error} = await admin
    .from("nayanet_intelligent_blocks")
    .select("intelligent_block_id,owner_id,understanding_state,content,evidence_refs")
    .eq("intelligent_block_id", BLOCK_ID)
    .eq("owner_id", OWNER_ID)
    .maybeSingle();
  if (error) throw error;
  if (!data) throw new Error("CANONICAL_BLOCK_NOT_FOUND");
  return data;
}

async function nextRevision(admin: ReturnType<typeof adminClient>) {
  const {data, error} = await admin
    .from("nayanet_execution_receipts")
    .select("revision")
    .eq("user_id", OWNER_ID)
    .eq("project_id", "NayaNET")
    .order("revision", {ascending: false})
    .limit(1)
    .maybeSingle();
  if (error) throw error;
  return Number(data?.revision ?? 0) + 1;
}

async function insertReceipt(admin: ReturnType<typeof adminClient>, row: Json) {
  for (let attempt = 0; attempt < 4; attempt++) {
    const revision = await nextRevision(admin);
    const {data, error} = await admin.from("nayanet_execution_receipts").insert({...row, revision}).select("*").single();
    if (!error) return data;
    if (error.code !== "23505") throw new Error("RECEIPT_WRITE_" + error.code);
  }
  throw new Error("RECEIPT_REVISION_RETRY_EXHAUSTED");
}

async function insertIdempotentActionReceipt(
  admin: ReturnType<typeof adminClient>,
  row: Json,
  idempotencyKey: string,
) {
  for (let attempt = 0; attempt < 4; attempt++) {
    const revision = await nextRevision(admin);
    const {data, error} = await admin
      .from("nayanet_execution_receipts")
      .insert({...row, revision, idempotency_key: idempotencyKey})
      .select("*")
      .single();
    if (!error) return {receipt: data, replayed: false};
    if (error.code !== "23505") throw new Error("RECEIPT_WRITE_" + error.code);

    const {data: existing, error: existingError} = await admin
      .from("nayanet_execution_receipts")
      .select("*")
      .eq("user_id", OWNER_ID)
      .eq("project_id", "NayaNET")
      .eq("action", "NAYA-NODE-0001-VERIFIED-AI-ACTION")
      .eq("idempotency_key", idempotencyKey)
      .maybeSingle();
    if (existingError) throw existingError;
    if (existing) return {receipt: existing, replayed: true};
  }
  throw new Error("RECEIPT_IDEMPOTENCY_RETRY_EXHAUSTED");
}

Deno.serve(async (req) => {
  try {
    if (req.method !== "POST") return json({ok: false, error: "METHOD_NOT_ALLOWED"}, 405);
    const {payload, workflowRef} = await auth(req);
    const admin = adminClient();
    const body = (await req.json().catch(() => ({}))) as Json;
    const mode = String(body.mode ?? "");
    const grantId = String(body.authority_grant_id ?? "").trim();
    const idempotencyKey = String(body.idempotency_key ?? "").trim();
    const authorityDecision = await resolveAuthority(admin, grantId);

    if (mode === "execute") {
      if (!idempotencyKey) {
        return json({
          ok: false,
          status: "BLOCKED",
          error: "IDEMPOTENCY_KEY_REQUIRED",
          execution_outcome_id: null,
        }, 400);
      }
      if (!authorityDecision.allowed) {
        const receipt = await insertReceipt(admin, {
          user_id: OWNER_ID,
          project_id: "NayaNET",
          action: REFUSAL_ACTION,
          status: "BLOCKED",
          expected_result: REFUSAL_EXPECTED_RESULT,
          observed_result: "Refused before execution: no governed action was performed and no execution outcome was created.",
          evidence: {
            stage: "authorization",
            authority_decision: "DENY",
            authority_reason: authorityDecision.reason,
            authority_absent: authorityDecision.reason === "AUTHORITY_ABSENT",
            authority_grant_id_presented: grantId || null,
            authority_grant_status: authorityDecision.grant?.status ?? null,
            requested_action: ACTION,
            requested_target: NAYA_ID,
            requested_mission: MISSION_ID,
            runtime_identity: "github-actions-oidc",
            workflow_ref: workflowRef,
            token_jti: payload.jti ?? null,
            token_sub: payload.sub ?? null,
            action_executed: false,
            outcome_created: false,
            owner_id: OWNER_ID,
          },
          learning: ["Capability does not create authority. An unauthorized request is refused and the refusal itself is persisted."],
        });
        console.error("VERIFIED_ACTION_REFUSED", authorityDecision.reason, receipt.id);
        return json({
          ok: false,
          status: "BLOCKED",
          error: "AUTHORITY_ABSENT",
          authority_reason: authorityDecision.reason,
          refusal_receipt_id: receipt.id,
          execution_outcome_id: null,
        }, 403);
      }

      const grant = authorityDecision.grant as Json;
      const block = await readCanonicalBlock(admin);
      const lesson = String((block.content as Json | undefined)?.lesson ?? "");
      if (!lesson) return json({ok: false, error: "RETAINED_LESSON_MISSING"}, 409);
      const digest = await canonicalDigest(lesson, block.evidence_refs);

      const requestFingerprint = await idempotencyRequestFingerprint({
        authority_grant_id: grant.grant_id,
        mission_id: MISSION_ID,
        action: ACTION,
        target: NAYA_ID,
        canonical_block_id: BLOCK_ID,
        canonical_digest: digest,
      });

      const observed = lesson.includes("Preserve provenance before applying retained intelligence")
        ? "PRESERVE_PROVENANCE_BEFORE_APPLY"
        : "RETAINED_INTELLIGENCE_RETRIEVED";
      const {receipt, replayed: idempotentReplay} = await insertIdempotentActionReceipt(admin, {
        user_id: OWNER_ID,
        project_id: "NayaNET",
        action: "NAYA-NODE-0001-VERIFIED-AI-ACTION",
        status: "SUCCESS",
        expected_result: "Under explicit active authority, NAYA-NODE-0001 applies its retained lesson to the bounded governed target and the applied result is durably observable.",
        observed_result: `${observed} | canonical_digest=${digest} | target=${NAYA_ID} | idempotency:${idempotencyKey || "none"}`,
        evidence: {
          stage: "execution",
          authority_decision: "ALLOW",
          idempotency_request_fingerprint: requestFingerprint,
          authority_grant_id: grant.grant_id,
          authority_status: grant.status,
          authority_mission: grant.mission_id,
          authority_scope: grant.scope,
          authority_actions: grant.actions,
          authority_constraints: grant.constraints,
          requested_action: ACTION,
          requested_target: NAYA_ID,
          applied_behavior: observed,
          canonical_block_id: BLOCK_ID,
          canonical_digest: digest,
          lesson,
          provenance_present: Array.isArray(block.evidence_refs) && block.evidence_refs.length > 0,
          understanding_state: block.understanding_state,
          runtime_identity: "github-actions-oidc",
          workflow_ref: workflowRef,
          token_jti: payload.jti ?? null,
          token_sub: payload.sub ?? null,
          owner_id: OWNER_ID,
        },
        learning: ["Authorized action is distinct from capability. Authority is resolved from the durable grant before any governed effect."],
      }, idempotencyKey);

      if (idempotentReplay) {
        const persistedFingerprint = String(((receipt.evidence ?? {}) as Json).idempotency_request_fingerprint ?? "");
        if (!persistedFingerprint || persistedFingerprint !== requestFingerprint) {
          return json({
            ok: false,
            status: "BLOCKED",
            error: "IDEMPOTENCY_KEY_REUSE_CONFLICT",
            idempotent_replay: false,
            receipt_id: receipt.id,
          }, 409);
        }
        const {data: replayOutcome, error: replayOutcomeError} = await admin
          .from("nayanet_execution_outcomes")
          .select("outcome_id,receipt_id,verified,verification_method")
          .eq("receipt_id", receipt.id)
          .maybeSingle();
        if (replayOutcomeError) throw replayOutcomeError;
        if (!replayOutcome) {
          const recoverOutcomeFromReceipt = async () => {
            const evidence = (receipt.evidence ?? {}) as Json;
            const {data: recovered, error: recoveryError} = await admin
              .from("nayanet_execution_outcomes")
              .insert({
                receipt_id: receipt.id,
                user_id: OWNER_ID,
                project_id: "NayaNET",
                experiment_case_id: EXPERIMENT_CASE,
                outcome_type: "GOVERNED_ACTION_OUTCOME",
                verifier_id: OWNER_ID,
                evidence: {
                  action_receipt_id: receipt.id,
                  authority_grant_id: evidence.authority_grant_id,
                  requested_action: evidence.requested_action,
                  requested_target: evidence.requested_target,
                  canonical_block_id: evidence.canonical_block_id,
                  canonical_digest: evidence.canonical_digest,
                  applied_behavior: evidence.applied_behavior,
                  observed_change: "Recovered canonical outcome from the durable bound execution receipt after response/outcome persistence loss.",
                  owner_id: OWNER_ID,
                  runtime_identity: "github-actions-oidc",
                  workflow_ref: workflowRef,
                  recovery_reason: "IDEMPOTENT_REPLAY_OUTCOME_RECOVERED",
                },
                benefit: 1,
                harm: 0,
                cost: 0,
                risk_adjusted_loss: 0,
                verified: false,
                verification_method: "PENDING_INDEPENDENT_RUNTIME_VERIFICATION",
              })
              .select("outcome_id,receipt_id,verified,verification_method")
              .single();
            if (recoveryError) {
              if (recoveryError.code !== "23505") throw new Error("OUTCOME_RECOVERY_WRITE_" + recoveryError.code);
              const {data: concurrentOutcome, error: concurrentReadError} = await admin
                .from("nayanet_execution_outcomes")
                .select("outcome_id,receipt_id,verified,verification_method")
                .eq("receipt_id", receipt.id)
                .maybeSingle();
              if (concurrentReadError) throw concurrentReadError;
              if (!concurrentOutcome) throw new Error("OUTCOME_RECOVERY_RACE_UNRESOLVED");
              return concurrentOutcome;
            }
            return recovered;
          };
          const recoveredOutcome = await recoverOutcomeFromReceipt();
          return json({
            ok: true,
            status: "EXECUTED",
            recovery: "IDEMPOTENT_REPLAY_OUTCOME_RECOVERED",
            idempotent_replay: true,
            receipt,
            outcome: recoveredOutcome,
          });
        }
        return json({ok: true, status: "EXECUTED", idempotent_replay: true, receipt, outcome: replayOutcome});
      }

      const {data: insertedOutcome, error: outcomeError} = await admin
        .from("nayanet_execution_outcomes")
        .insert({
          receipt_id: receipt.id,
          user_id: OWNER_ID,
          project_id: "NayaNET",
          experiment_case_id: EXPERIMENT_CASE,
          outcome_type: "GOVERNED_ACTION_OUTCOME",
          verifier_id: OWNER_ID,
          evidence: {
            action_receipt_id: receipt.id,
            authority_grant_id: grant.grant_id,
            requested_action: ACTION,
            requested_target: NAYA_ID,
            canonical_block_id: BLOCK_ID,
            canonical_digest: digest,
            applied_behavior: observed,
            observed_change: `Governed action applied the retained lesson (${observed}); provenance preserved before application.`,
            owner_id: OWNER_ID,
            runtime_identity: "github-actions-oidc",
            workflow_ref: workflowRef,
            executor_token_jti: payload.jti ?? null,
          },
          benefit: 1,
          harm: 0,
          cost: 0,
          risk_adjusted_loss: 0,
          verified: false,
          verification_method: "PENDING_INDEPENDENT_RUNTIME_VERIFICATION",
        })
        .select("*")
        .single();

      let outcome = insertedOutcome;
      if (outcomeError) {
        if (outcomeError.code !== "23505") throw new Error("OUTCOME_WRITE_" + outcomeError.code);
        const {data: concurrentOutcome, error: concurrentReadError} = await admin
          .from("nayanet_execution_outcomes")
          .select("*")
          .eq("receipt_id", receipt.id)
          .maybeSingle();
        if (concurrentReadError) throw concurrentReadError;
        if (!concurrentOutcome) throw new Error("OUTCOME_WRITE_RACE_UNRESOLVED");
        outcome = concurrentOutcome;
      }

      return json({
        ok: true,
        status: "EXECUTED",
        receipt,
        outcome,
        authority_decision: "ALLOW",
        canonical_digest: digest,
        runtime_identity: "github-actions-oidc",
        workflow_ref: workflowRef,
        token_jti: payload.jti ?? null,
      });
    }

    if (mode === "verify-idempotency") {
      if (!idempotencyKey) return json({ok: false, error: "IDEMPOTENCY_KEY_REQUIRED"}, 400);

      const {data: receipts, error: receiptsError} = await admin
        .from("nayanet_execution_receipts")
        .select("id,user_id,project_id,action,status,observed_result,evidence,idempotency_key")
        .eq("user_id", OWNER_ID)
        .eq("project_id", "NayaNET")
        .eq("action", "NAYA-NODE-0001-VERIFIED-AI-ACTION")
        .eq("idempotency_key", idempotencyKey);
      if (receiptsError) throw receiptsError;

      const receiptIds = (receipts ?? []).map((r: any) => r.id);
      const {data: outcomes, error: outcomesError} = receiptIds.length === 0
        ? {data: [], error: null}
        : await admin
            .from("nayanet_execution_outcomes")
            .select("outcome_id,receipt_id,user_id,project_id,verified,verification_method,evidence")
            .in("receipt_id", receiptIds)
            .eq("user_id", OWNER_ID)
            .eq("project_id", "NayaNET");
      if (outcomesError) throw outcomesError;

      const receipt = (receipts ?? [])[0] ?? null;
      const outcome = (outcomes ?? [])[0] ?? null;
      const grantId = String(receipt?.evidence?.authority_grant_id ?? "");
      const independentAuthority = await resolveAuthority(admin, grantId);
      const block = await readCanonicalBlock(admin);
      const lesson = String((block.content as Json | undefined)?.lesson ?? "");
      const digest = await canonicalDigest(lesson, block.evidence_refs);
      const expectedFingerprint = independentAuthority.allowed
        ? await idempotencyRequestFingerprint({
            authority_grant_id: independentAuthority.grant?.grant_id,
            mission_id: MISSION_ID,
            action: ACTION,
            target: NAYA_ID,
            canonical_block_id: BLOCK_ID,
            canonical_digest: digest,
          })
        : "";

      const checks = {
        exactly_one_receipt: (receipts ?? []).length === 1,
        exactly_one_outcome: (outcomes ?? []).length === 1,
        receipt_success: receipt?.status === "SUCCESS",
        outcome_matches_receipt: outcome?.receipt_id === receipt?.id,
        request_fingerprint_matches: String(receipt?.evidence?.idempotency_request_fingerprint ?? "") === expectedFingerprint,
        authority_still_valid: independentAuthority.allowed === true,
        canonical_digest_matches: String(outcome?.evidence?.canonical_digest ?? "") === digest,
      };
      const passed = Object.values(checks).every((v) => v === true);
      return json({
        ok: passed,
        status: passed ? "IDEMPOTENCY_CONCURRENCY_VERIFIED" : "IDEMPOTENCY_CONCURRENCY_INCONCLUSIVE",
        independent_verification: passed,
        executor_claim_trusted_as_verification: false,
        idempotency_key: idempotencyKey,
        receipt_count: (receipts ?? []).length,
        outcome_count: (outcomes ?? []).length,
        receipt_id: receipt?.id ?? null,
        outcome_id: outcome?.outcome_id ?? null,
        checks,
        runtime_identity: "github-actions-oidc",
        workflow_ref: workflowRef,
        token_jti: payload.jti ?? null,
      }, passed ? 200 : 409);
    }

    if (mode === "verify") {
      const receiptId = String(body.action_receipt_id ?? "").trim();
      const refusalId = String(body.refusal_receipt_id ?? "").trim();
      if (!receiptId) return json({ok: false, error: "ACTION_RECEIPT_ID_REQUIRED"}, 400);

      const readReceipt = async (id: string) => {
        const {data, error} = await admin
          .from("nayanet_execution_receipts")
          .select("id,user_id,project_id,revision,action,status,expected_result,observed_result,evidence,created_at")
          .eq("id", id)
          .eq("user_id", OWNER_ID)
          .eq("project_id", "NayaNET")
          .maybeSingle();
        if (error) throw error;
        return data;
      };
      const readOutcome = async (id: string) => {
        const {data, error} = await admin
          .from("nayanet_execution_outcomes")
          .select("outcome_id,receipt_id,user_id,project_id,experiment_case_id,outcome_type,verified,verified_value,verification_method,evidence,created_at")
          .eq("receipt_id", id)
          .eq("user_id", OWNER_ID)
          .eq("project_id", "NayaNET")
          .maybeSingle();
        if (error) throw error;
        return data;
      };

      const receipt = await readReceipt(receiptId);
      if (!receipt) return json({ok: false, error: "ACTION_RECEIPT_NOT_FOUND"}, 404);
      const outcome = await readOutcome(receiptId);
      if (!outcome) return json({ok: false, error: "EXECUTION_OUTCOME_NOT_FOUND"}, 404);

      // Independent authority re-evaluation: resolve the grant row directly.
      const receiptEvidence = (receipt.evidence ?? {}) as Json;
      const grantIdPresented = String(receiptEvidence.authority_grant_id ?? "");
      const independentAuthority = await resolveAuthority(admin, grantIdPresented);

      const block = await readCanonicalBlock(admin);
      const lesson = String((block.content as Json | undefined)?.lesson ?? "");
      const expectedDigest = await canonicalDigest(lesson, block.evidence_refs);
      const outcomeEvidence = (outcome.evidence ?? {}) as Json;
      const digestInObserved = String(receipt.observed_result ?? "").includes(`canonical_digest=${expectedDigest}`);

      let refusalChecks: Json = {refusal_requested: false};
      let refusalReceipt: Json | null = null;
      if (refusalId) {
        refusalReceipt = await readReceipt(refusalId);
        const refusalEvidence = (refusalReceipt?.evidence ?? {}) as Json;
        const refusalGrantIdPresented = String(refusalEvidence.authority_grant_id_presented ?? "");
        const refusalAuthority = refusalReceipt
          ? await resolveAuthority(admin, refusalGrantIdPresented)
          : null;
        const refusalAuthorityReason = refusalAuthority?.reason ?? null;
        const refusalOutcome = await admin
          .from("nayanet_execution_outcomes")
          .select("outcome_id")
          .eq("receipt_id", refusalId)
          .maybeSingle();
        if (refusalOutcome.error) throw refusalOutcome.error;
        const refusalOutcomePresent = refusalOutcome.data !== null;
        const refusalReceiptContractValid = Boolean(
          refusalReceipt
          && refusalReceipt.user_id === OWNER_ID
          && refusalReceipt.project_id === "NayaNET"
          && refusalReceipt.action === REFUSAL_ACTION
          && refusalReceipt.status === "BLOCKED"
          && refusalReceipt.expected_result === REFUSAL_EXPECTED_RESULT
          && refusalReceipt.observed_result === "Refused before execution: no governed action was performed and no execution outcome was created."
          && refusalEvidence.stage === "authorization"
          && refusalEvidence.authority_decision === "DENY"
          && refusalEvidence.authority_reason === refusalAuthorityReason
          && refusalEvidence.authority_absent === (refusalAuthorityReason === "AUTHORITY_ABSENT")
          && refusalEvidence.authority_grant_id_presented === (refusalGrantIdPresented || null)
          && refusalEvidence.requested_action === ACTION
          && refusalEvidence.requested_target === NAYA_ID
          && refusalEvidence.requested_mission === MISSION_ID
          && refusalEvidence.action_executed === false
          && refusalEvidence.outcome_created === false
          && refusalEvidence.owner_id === OWNER_ID
        );
        refusalChecks = {
          refusal_requested: true,
          refusal_receipt_present: Boolean(refusalReceipt),
          refusal_receipt_owner_matches: refusalReceipt?.user_id === OWNER_ID,
          refusal_status_blocked: refusalReceipt?.status === "BLOCKED",
          refusal_authority_denied: refusalEvidence.authority_decision === "DENY",
          refusal_authority_absent: refusalEvidence.authority_absent === true,
          refusal_action_not_executed: refusalEvidence.action_executed === false,
          refusal_outcome_absent: refusalOutcomePresent === false,
          unauthorized_outcome_exists: refusalOutcomePresent,
          refusal_receipt_contract_valid: refusalReceiptContractValid,
        };
      }

      const authorizedChecks = {
        runtime_identity_bound: payload.repository === REPOSITORY,
        owner_scoped: receipt.user_id === OWNER_ID,
        durable_binding_valid: independentAuthority.allowed === true,
        authority_actively_granted: independentAuthority.grant?.status === "ACTIVE",
        action_authorized_for_target: receipt.action === "NAYA-NODE-0001-VERIFIED-AI-ACTION" && receiptEvidence.requested_target === NAYA_ID,
        action_receipt_exists: true,
        action_receipt_success: receipt.status === "SUCCESS",
        execution_outcome_exists: true,
        outcome_matches_receipt: outcome.receipt_id === receipt.id,
        outcome_not_self_certified_at_execution: outcome.verified === false && outcome.verification_method === EXECUTION_VERIFICATION_PENDING,
        observed_result_exists: Boolean(receipt.observed_result),
        observed_result_matches_live_canonical_state: digestInObserved,
        canonical_digest_recomputed: expectedDigest === outcomeEvidence.canonical_digest,
      };

      const authorizedOk = Object.entries(authorizedChecks).every(([, v]) => v === true);
      const refusalChecksPass = !refusalId || (
        refusalChecks.refusal_receipt_present === true &&
        refusalChecks.refusal_status_blocked === true &&
        refusalChecks.refusal_authority_denied === true &&
        refusalChecks.refusal_authority_absent === true &&
        refusalChecks.refusal_action_not_executed === true &&
        refusalChecks.refusal_outcome_absent === true &&
        refusalChecks.unauthorized_outcome_exists === false &&
        refusalChecks.refusal_receipt_owner_matches === true &&
        refusalChecks.refusal_receipt_contract_valid === true
      );
      const passed = authorizedOk && refusalChecksPass;

      if (!passed) {
        return json({
          ok: false,
          status: "INCONCLUSIVE",
          independent_verification: false,
          independent_checks: authorizedChecks,
          refusal_checks: refusalChecks,
        }, 409);
      }

      const {data: verified, error: verifyError} = await admin
        .from("nayanet_execution_outcomes")
        .update({
          verified: true,
          verification_method: INDEPENDENT_VERIFICATION_METHOD,
        })
        .eq("outcome_id", outcome.outcome_id)
        .eq("user_id", OWNER_ID)
        .eq("verified", false)
        .eq("verification_method", EXECUTION_VERIFICATION_PENDING)
        .select("*")
        .single();
      if (verifyError) throw verifyError;

      return json({
        ok: true,
        status: "OUTCOME_VERIFIED",
        independent_verification: true,
        independent_checks: authorizedChecks,
        refusal_checks: refusalChecks,
        independent_authority: {
          grant_id: independentAuthority.grant?.grant_id ?? null,
          status: independentAuthority.grant?.status ?? null,
          decision: independentAuthority.reason,
        },
        action_receipt_id: receipt.id,
        refusal_receipt_id: refusalReceipt?.id ?? null,
        execution_outcome_id: verified.outcome_id,
        canonical_digest: expectedDigest,
        verified_outcome: verified,
        runtime_identity: "github-actions-oidc",
        workflow_ref: workflowRef,
        token_jti: payload.jti ?? null,
      });
    }

    return json({ok: false, error: "UNSUPPORTED_MODE"}, 400);
  } catch (error) {
    console.error("NAYANET_VERIFIED_AI_ACTION_ERROR", String((error as Error)?.message ?? error));
    return json({ok: false, error: String((error as Error)?.message ?? error)}, 400);
  }
});
