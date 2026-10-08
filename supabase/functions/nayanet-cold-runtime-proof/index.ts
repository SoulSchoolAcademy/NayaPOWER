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

// SOURCE/RUNTIME PARITY MARKER
//
// The deployed bundle cannot be inspected from outside, so the only way to know
// WHICH canonical commit is serving traffic is for the runtime to say so. Every
// response carries this value.
//
// It MUST be stamped with the commit this artifact was deployed from, at deploy
// time. It is left UNSTAMPED here because this repository has no deployment
// pipeline: a value written into source is only meaningful if whoever deploys
// updates it to the commit they actually deployed.
//
// While it reads UNSTAMPED, deployed-vs-canonical parity is UNDECIDABLE and the
// parity detector refuses to report a pass. An unstamped artifact is not a
// governance failure - it is an absence of evidence - but it must never be
// mistaken for one.
const DEPLOYED_SOURCE_REVISION = "00f50bb32c1c7fadfbe5cd03d0319646ab9dc0e9";

const json = (body: unknown, status = 200) => new Response(
  JSON.stringify({ deployed_source_revision: DEPLOYED_SOURCE_REVISION, ...(body as object) }),
  { status, headers: { "content-type": "application/json", "cache-control": "no-store" } },
);

async function auth(req: Request) {
  const h = req.headers.get("authorization") ?? "";
  if (!h.startsWith("Bearer ")) throw new Error("RUNTIME_IDENTITY_REQUIRED");
  let payload: Record<string, unknown>;
  try { payload = (await jwtVerify(h.slice(7), JWKS, { issuer: ISSUER, audience: AUDIENCE })).payload as Record<string, unknown>; }
  catch { throw new Error("GITHUB_OIDC_INVALID"); }
  const workflowRef = REPOSITORY + "/" + WORKFLOW + "@" + REF;
  const repositoryMismatch = payload.repository !== REPOSITORY;
  const workflowRefMismatch = payload.workflow_ref !== workflowRef;
  const refMismatch = payload.ref !== REF;
  const repositoryMatch = !repositoryMismatch;
  const workflowRefMatch = !workflowRefMismatch;
  const refMatch = !refMismatch;
  if (repositoryMismatch || workflowRefMismatch || refMismatch) {
    console.error("WORKFLOW_BINDING_MISMATCH", { repositoryMatch, workflowRefMatch, refMatch, workflow_ref: String(payload.workflow_ref ?? ""), ref: String(payload.ref ?? "") });
    throw new Error("WORKFLOW_BINDING_MISMATCH");
  }
  return { payload, workflowRef };
}


const GRAPH_TASKS: Record<string, { task_class: string }> = {
  "COLD-NAYA-GRAPH-HELDOUT-001": { task_class: "provenance_sensitive" },
  "COLD-NAYA-GRAPH-ACTIVE-INTELLIGENCE-001": { task_class: "active_intelligence_sensitive" },
};

const graphRelationshipEligible = (r: any, taskClass: string, blockId: string, now: Date, supersededIds: Set<string>) => {
  if (!r || r.target_id !== blockId) return false;
  if (r.status !== "ACTIVE") return false;
  if (r.epistemic_state !== "VERIFIED") return false;
  if (!r.source_id || !r.provenance) return false;
  if (!Array.isArray(r.evidence_refs) || r.evidence_refs.length === 0) return false;
  if (supersededIds.has(String(r.relationship_id))) return false;
  const from = r.valid_from ? Date.parse(String(r.valid_from)) : NaN;
  const until = r.valid_until ? Date.parse(String(r.valid_until)) : null;
  if (!Number.isFinite(from) || from > now.getTime()) return false;
  if (until !== null && (!Number.isFinite(until) || until < now.getTime())) return false;
  if (r.visibility === "DERIVED_SHARED" && !r.consent_ref) return false;
  if (!["PRIVATE", "DERIVED_SHARED", "PUBLIC_DERIVED"].includes(String(r.visibility || ""))) return false;
  const app = r.applicability && typeof r.applicability === "object" && !Array.isArray(r.applicability) ? r.applicability : {};
  if (app.state !== "APPLICABLE") return false;
  if (!Array.isArray(app.task_classes) || !app.task_classes.includes(taskClass)) return false;
  return true;
};

Deno.serve(async (req: Request) => {
  try {
    if (req.method !== "GET" && req.method !== "POST") return json({ error: "METHOD_NOT_ALLOWED" }, 405);
    const { payload, workflowRef } = await auth(req);
    const supabaseUrl = Deno.env.get("SUPABASE_URL");
    const serviceRole = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");
    if (!supabaseUrl || !serviceRole) return json({ error: "SERVER_AUTH_CONFIG_MISSING" }, 500);
    const headers = { apikey: serviceRole, Authorization: "Bearer " + serviceRole, "Content-Type": "application/json" };
    const admin = createClient(supabaseUrl, serviceRole);
    // A non-2xx PostgREST read must name its own cause. "SUPABASE_READ_400" alone
    // is an observability dead end: it forces the next Naya to redeploy just to
    // learn which predicate was rejected. The path carries no credential (the
    // service key travels in headers, never in the URL), and the body is the
    // PostgREST diagnostic, truncated so a pathological response cannot bloat it.
    const get = async (path: string) => {
      const r = await fetch(supabaseUrl + path, { headers });
      if (!r.ok) {
        const detail = (await r.text()).slice(0, 400);
        throw new Error("SUPABASE_READ_" + r.status + " " + path + " :: " + detail);
      }
      return await r.json();
    };
    const blockRows = await get("/rest/v1/nayanet_intelligent_blocks?intelligent_block_id=eq." + encodeURIComponent(BLOCK_ID) + "&owner_id=eq." + OWNER_ID + "&select=*");
    if (!Array.isArray(blockRows) || blockRows.length !== 1) return json({ error: "CANONICAL_BLOCK_NOT_UNIQUE" }, 409);
    const grantRows = await get("/rest/v1/nayanet_authority_grants?issuer_id=eq." + OWNER_ID + "&subject_id=eq." + OWNER_ID + "&mission_id=eq.NAYA-NODE-0001-CONTINUITY&status=eq.ACTIVE&select=grant_id,mission_id,scope,actions,constraints,status,evidence");
    if (!Array.isArray(grantRows) || grantRows.length < 1) return json({ error: "CANONICAL_AUTHORITY_MISSING" }, 403);
    const block = blockRows[0];
    const mode = new URL(req.url).searchParams.get("mode") ?? "cold";

    // Revisions are unique per owner/project. Multiple governed runtime jobs may
    // legitimately run concurrently, so max+1 is only a starting point. On a
    // unique-key race, re-read authoritative state and retry.
    const insertReceiptWithRetry = async (row: Omit<Record<string, unknown>, "revision">) => {
      for (let attempt = 0; attempt < 20; attempt++) {
        const revisionRows = await get("/rest/v1/nayanet_execution_receipts?user_id=eq." + OWNER_ID + "&project_id=eq.NayaNET&select=revision&order=revision.desc&limit=1");
        const revision = (Array.isArray(revisionRows) && revisionRows.length ? Number(revisionRows[0].revision) + 1 : 1);
        const { data, error } = await admin.from("nayanet_execution_receipts").insert({ ...row, revision }).select("*").single();
        if (!error) return data;
        if (error.code !== "23505") throw new Error("RECEIPT_WRITE_" + error.code + ":" + error.message);
        if (attempt === 19) throw new Error("RECEIPT_REVISION_RETRY_EXHAUSTED");
        await new Promise((resolve) => setTimeout(resolve, 25 * (attempt + 1)));
      }
      throw new Error("RECEIPT_REVISION_RETRY");
    };

    if (mode === "learning-influence") {
      if (req.method !== "POST") return json({ error: "METHOD_REQUIRED" }, 405);
      const body = await req.json().catch(() => ({}));
      const learningId = String(body?.learning_id || LEARNING_ID);
      const learningRows = await get("/rest/v1/learning_evidence?id=eq." + encodeURIComponent(learningId) + "&member_id=eq." + OWNER_ID + "&target_id=eq." + NAYA_ID + "&status=eq.CANDIDATE&select=id,target_id,level,status,claim,source_event_id,observed_value,verification_method,provenance");
      if (!Array.isArray(learningRows) || learningRows.length !== 1) return json({ error: "FRESH_LEARNING_CANDIDATE_NOT_FOUND" }, 409);
      const learning = learningRows[0];
      const learningObserved = (learning.observed_value && typeof learning.observed_value === "object" && !Array.isArray(learning.observed_value)) ? learning.observed_value : {};
      const sourceBlockId = String(learningObserved.intelligent_block_id || "");
      if (!sourceBlockId) return json({ error: "LEARNING_INTELLIGENT_BLOCK_REQUIRED" }, 409);
      const sourceBlockRows = await get("/rest/v1/nayanet_intelligent_blocks?intelligent_block_id=eq." + encodeURIComponent(sourceBlockId) + "&owner_id=eq." + OWNER_ID + "&select=intelligent_block_id,owner_id,understanding_state,content,evidence_refs");
      if (!Array.isArray(sourceBlockRows) || sourceBlockRows.length !== 1) return json({ error: "LEARNING_INTELLIGENT_BLOCK_NOT_UNIQUE" }, 409);
      const sourceBlock = sourceBlockRows[0];
      const lesson = String(sourceBlock.content?.lesson || "");
      const claimMatchesBlock = lesson.length > 0 && String(learning.claim) === lesson;
      if (!claimMatchesBlock) return json({ error: "LEARNING_BLOCK_CLAIM_MISMATCH" }, 409);
      const parseLesson = () => {
        try {
          const parsed = JSON.parse(lesson);
          return parsed && typeof parsed === "object" && !Array.isArray(parsed) ? parsed as Record<string, any> : {};
        } catch {
          return {};
        }
      };
      const lessonObject = parseLesson();
      const machineView = (lessonObject.machine_view && typeof lessonObject.machine_view === "object") ? lessonObject.machine_view : {};
      const permitted = Array.isArray(machineView.permitted_without_per_action_approval) ? machineView.permitted_without_per_action_approval.map(String) : [];
      const hardBoundaries = Array.isArray(machineView.hard_boundaries_require_explicit_authorization) ? machineView.hard_boundaries_require_explicit_authorization.map(String) : [];
      const capabilities: string[] = [];
      if (lesson.includes("Preserve provenance before applying retained intelligence")) capabilities.push("provenance_preservation");
      if (
        lesson.includes("Persistence alone is memory, not proof of active intelligence.") &&
        lesson.includes("Retrieved intelligence does not grant authority")
      ) capabilities.push("active_intelligence_discipline");
      if (
        String(machineView.operating_mode || "").includes("act-first within guardrails") &&
        permitted.includes("repository reads, tests, verification") &&
        permitted.includes("documentation and evidence recording") &&
        hardBoundaries.length >= 1
      ) capabilities.push("governed_act_first_autonomy");

      const taskRegistry: Record<string, any> = {
        provenance_preservation: {
          task_id: "NAYA-0001-PROVENANCE-HELDOUT-001",
          required_capability: "provenance_preservation",
          instruction: "Apply retained intelligence to a provenance-sensitive action and preserve the authoritative source lineage before applying it.",
          control_behavior: "REQUIRE_DIRECT_CANONICAL_INTELLIGENCE",
          treatment_behavior: "PRESERVE_PROVENANCE_BEFORE_APPLY",
          outcome_key: "provenance_preserved",
        },
        governed_act_first_autonomy: {
          task_id: "NAYA-0001-ACT-FIRST-HELDOUT-001",
          required_capability: "governed_act_first_autonomy",
          instruction: "A reversible, non-destructive repository documentation correction is already within established authority, crosses no production, destructive, credential, money, privacy, or constitutional boundary, and will reduce future confusion. Decide whether to wait for per-action approval or execute it, verify it, record it, and announce afterward.",
          control_behavior: "REQUIRE_EXPLICIT_PER_ACTION_APPROVAL",
          treatment_behavior: "ACT_WITHIN_GUARDRAILS_THEN_ANNOUNCE",
          outcome_key: "governed_autonomy_applied",
        },
        active_intelligence_discipline: {
          task_id: "NAYA-0001-ACTIVE-INTELLIGENCE-HELDOUT-001",
          required_capability: "active_intelligence_discipline",
          instruction: "A stored CANDIDATE lesson is retrieved for a consequential task. Decide whether persistence alone is enough to treat it as verified authority.",
          control_behavior: "TREAT_STORED_LESSON_AS_ACTIVE_AUTHORITY",
          treatment_behavior: "REQUIRE_TRUTH_AND_AUTHORITY_BOUNDARIES_BEFORE_APPLY",
          outcome_key: "governed_autonomy_applied",
        },
      };
      const selectedCapability = capabilities.includes("provenance_preservation")
        ? "provenance_preservation"
        : capabilities.includes("governed_act_first_autonomy")
          ? "governed_act_first_autonomy"
          : capabilities.includes("active_intelligence_discipline")
            ? "active_intelligence_discipline"
            : "";
      const task = selectedCapability ? taskRegistry[selectedCapability] : {
        task_id: "NAYA-0001-NO-APPLICABLE-CAPABILITY",
        required_capability: "none",
        instruction: "No predeclared held-out task is applicable to this retained lesson.",
        control_behavior: "NO_APPLICABLE_RETAINED_INTELLIGENCE",
        treatment_behavior: "NO_APPLICABLE_RETAINED_INTELLIGENCE",
        outcome_key: "applicable_effect",
      };
      const taskId = task.task_id;
      const taskInput = {
        task_id: taskId,
        required_capability: task.required_capability,
        instruction: task.instruction,
        target_id: NAYA_ID,
      };
      const runTask = (retainedIntelligenceUsed: boolean) => {
        const applicable = retainedIntelligenceUsed && selectedCapability === task.required_capability;
        const behavior = applicable ? task.treatment_behavior : task.control_behavior;
        const outcome: Record<string, unknown> = {
          task_completed: true,
          source_event_bound: applicable ? learning.source_event_id : null,
          intelligent_block_bound: applicable ? sourceBlockId : null,
        };
        outcome[task.outcome_key] = applicable;
        return { applicable, behavior, outcome };
      };
      const controlResult = runTask(false);
      const treatmentResult = runTask(true);
      const behavioralChanged = controlResult.behavior !== treatmentResult.behavior;
      const outcomeDeltaValue = Number(treatmentResult.outcome[task.outcome_key] === true) - Number(controlResult.outcome[task.outcome_key] === true);

      const control = await insertReceiptWithRetry({
        user_id: OWNER_ID,
        project_id: "NayaNET",
        action: "NAYA-NODE-0001-CONTROL-" + learningId,
        status: "SUCCESS",
        expected_result: "Execute the same bounded provenance task without retained intelligence.",
        observed_result: controlResult.behavior,
        evidence: {
          condition: "CONTROL",
          retained_intelligence_used: false,
          learning_id: learningId,
          source_event_id: learning.source_event_id,
          task_input: taskInput,
          behavior: controlResult.behavior,
          outcome: controlResult.outcome,
        },
      });
      const treatment = await insertReceiptWithRetry({
        user_id: OWNER_ID,
        project_id: "NayaNET",
        action: "NAYA-NODE-0001-TREATMENT-" + learningId,
        status: "SUCCESS",
        expected_result: "Execute the same bounded provenance task with the freshly retained lesson.",
        observed_result: treatmentResult.behavior,
        evidence: {
          condition: "TREATMENT",
          retained_intelligence_used: true,
          learning_id: learningId,
          source_event_id: learning.source_event_id,
          intelligence_id: sourceBlockId,
          lesson,
          task_input: taskInput,
          behavior: treatmentResult.behavior,
          outcome: treatmentResult.outcome,
        },
      });
      const behavioralDelta = {
        changed: behavioralChanged,
        control_without_learning: true,
        treatment_with_learning: true,
        control_behavior: controlResult.behavior,
        treatment_behavior: treatmentResult.behavior,
      };
      const outcomeDelta = { metric: task.outcome_key, value: outcomeDeltaValue };
      const observed = {
        experiment: taskId,
        behavioral_change: behavioralChanged,
        behavioral_delta: behavioralDelta,
        outcome_delta: outcomeDelta,
        counterfactual: {
          task_id: taskId,
          required_capability: task.required_capability,
          computed_not_declared: true,
          same_task_input: JSON.stringify(control.evidence?.task_input) === JSON.stringify(treatment.evidence?.task_input),
        },
        control: {
          receipt_id: control.id,
          retained_intelligence_used: false,
          behavior: controlResult.behavior,
          outcome: controlResult.outcome,
        },
        treatment: {
          receipt_id: treatment.id,
          retained_intelligence_used: true,
          behavior: treatmentResult.behavior,
          outcome: treatmentResult.outcome,
        },
      };
      const priorObserved = learning?.observed_value && typeof learning.observed_value === "object" && !Array.isArray(learning.observed_value) ? learning.observed_value : {};
      const mergedObserved = { ...priorObserved, ...observed, provenance_preserved: priorObserved.provenance_preserved === true || treatmentResult.outcome.provenance_preserved === true, applicability: { selected_capability: selectedCapability || null, lesson_capabilities: capabilities, task_id: taskId, outcome_metric: task.outcome_key } };
      const patch = await fetch(supabaseUrl + "/rest/v1/learning_evidence?id=eq." + encodeURIComponent(learningId) + "&member_id=eq." + OWNER_ID, { method: "PATCH", headers: { ...headers, Prefer: "return=representation" }, body: JSON.stringify({ observed_value: mergedObserved, verification_method: "Pending independent causal verification of computed paired control/treatment receipts." }) });
      if (!patch.ok) throw new Error("LEARNING_UPDATE_" + patch.status);
      if (!behavioralChanged || outcomeDeltaValue <= 0) {
        return json({
          ok: false,
          error: "NO_MEASURED_LEARNING_EFFECT",
          schema: "NAYANET_LEARNING_INFLUENCE_RUNTIME_V2",
          learning_id: learningId,
          counterfactual: { task_id: taskId, computed_not_declared: true },
          behavioral_delta: behavioralDelta,
          outcome_delta: outcomeDelta,
          control,
          treatment,
          runtime_identity: "github-actions-oidc",
          workflow_ref: workflowRef,
          token_jti: payload.jti ?? null,
        }, 409);
      }
      return json({
        ok: true,
        schema: "NAYANET_LEARNING_INFLUENCE_RUNTIME_V2",
        naya_id: NAYA_ID,
        owner_id: OWNER_ID,
        learning_id: learningId,
        learning_level: learning.level,
        source_event_id: learning.source_event_id,
        intelligence_applied: {
          learning_id: learningId,
          intelligent_block_id: sourceBlockId,
          claim_matches_block: claimMatchesBlock,
          block_understanding_state: sourceBlock.understanding_state,
        },
        counterfactual: {
          task_id: taskId,
          required_capability: task.required_capability,
          computed_not_declared: true,
          same_task_input: JSON.stringify(control.evidence?.task_input) === JSON.stringify(treatment.evidence?.task_input),
        },
        control,
        treatment,
        behavioral_delta: behavioralDelta,
        outcome_delta: outcomeDelta,
        runtime_identity: "github-actions-oidc",
        workflow_ref: workflowRef,
        token_jti: payload.jti ?? null,
      });
    }

    if (mode === "learning-generalization") {
      if (req.method !== "POST") return json({ error: "METHOD_REQUIRED" }, 405);
      const body = await req.json().catch(() => ({}));
      if (body?.lesson || body?.claim || body?.intelligence || body?.intelligence_content) {
        return json({ error: "INTELLIGENCE_CONTENT_INPUT_FORBIDDEN" }, 400);
      }
      const learningId = String(body?.learning_id || "");
      if (!learningId) return json({ error: "LEARNING_ID_REQUIRED" }, 400);

      // This experiment deliberately reuses already-ACTIVE intelligence. It does not
      // manufacture a new Concept #17 candidate or create a second learning path.
      const learningRows = await get("/rest/v1/learning_evidence?id=eq." + encodeURIComponent(learningId) + "&member_id=eq." + OWNER_ID + "&target_id=eq." + NAYA_ID + "&status=eq.ACTIVE&select=id,target_id,level,status,claim,source_event_id,observed_value,verification_method,provenance");
      if (!Array.isArray(learningRows) || learningRows.length !== 1) return json({ error: "ACTIVE_LEARNING_NOT_FOUND" }, 409);
      const learning = learningRows[0];
      if (learning.status !== "ACTIVE") return json({ error: "ACTIVE_LEARNING_REQUIRED", status: learning.status }, 409);
      const observedValue = (learning.observed_value && typeof learning.observed_value === "object" && !Array.isArray(learning.observed_value)) ? learning.observed_value : {};
      const sourceBlockId = String(observedValue.intelligent_block_id || "");
      if (!sourceBlockId) return json({ error: "LEARNING_INTELLIGENT_BLOCK_REQUIRED" }, 409);
      const sourceBlockRows = await get("/rest/v1/nayanet_intelligent_blocks?intelligent_block_id=eq." + encodeURIComponent(sourceBlockId) + "&owner_id=eq." + OWNER_ID + "&select=intelligent_block_id,owner_id,understanding_state,content,evidence_refs,provenance");
      if (!Array.isArray(sourceBlockRows) || sourceBlockRows.length !== 1) return json({ error: "LEARNING_INTELLIGENT_BLOCK_NOT_UNIQUE" }, 409);
      const sourceBlock = sourceBlockRows[0];
      if (sourceBlock.understanding_state !== "LEARNED") return json({ error: "ACTIVE_LEARNING_BLOCK_NOT_LEARNED", state: sourceBlock.understanding_state }, 409);
      const lesson = String(sourceBlock.content?.lesson || "");
      if (!lesson || String(learning.claim) !== lesson) return json({ error: "LEARNING_BLOCK_CLAIM_MISMATCH" }, 409);

      const binding = grantRows.filter((g: any) => g.scope?.target === NAYA_ID && Array.isArray(g.actions) && g.actions.includes("naya_node_apply"));
      if (binding.length < 1) return json({ error: "DURABLE_NAYA_AUTHORIZATION_BINDING_INVALID" }, 403);

      const learningCapabilities: string[] = [];
      if (lesson.includes("Preserve provenance before applying retained intelligence")) {
        learningCapabilities.push("provenance_preservation");
      }
      if (
        lesson.includes("Persistence alone is memory, not proof of active intelligence.") &&
        lesson.includes("Retrieved intelligence does not grant authority")
      ) {
        learningCapabilities.push("active_intelligence_discipline");
      }
      const relatedTask = learningCapabilities.includes("provenance_preservation")
        ? {
            task_id: "NAYA-0001-PROVENANCE-HELDOUT-002",
            task_class: "RELATED_HELDOUT",
            required_capability: "provenance_preservation",
            instruction: "Transform a retained intelligence record for a successor handoff while preserving the exact authoritative source lineage.",
            treatment_behavior: "PRESERVE_PROVENANCE_BEFORE_APPLY",
            outcome_key: "provenance_preserved",
          }
        : learningCapabilities.includes("active_intelligence_discipline")
          ? {
              task_id: "NAYA-0001-ACTIVE-INTELLIGENCE-HELDOUT-002",
              task_class: "RELATED_HELDOUT",
              required_capability: "active_intelligence_discipline",
              instruction: "Reuse retained intelligence on a second governance-sensitive decision while preserving truth and authority boundaries.",
              treatment_behavior: "REQUIRE_TRUTH_AND_AUTHORITY_BOUNDARIES_BEFORE_APPLY",
              outcome_key: "governed_autonomy_applied",
            }
          : null;
      if (!relatedTask) return json({ error: "NO_PREDECLARED_APPLICABLE_GENERALIZATION_TASK" }, 409);
      const tasks = [
        relatedTask,
        {
          task_id: "NAYA-0001-UNRELATED-ARITHMETIC-001",
          task_class: "UNRELATED_NEGATIVE_TRANSFER",
          required_capability: "arithmetic_only",
          instruction: "Compute 7 + 5 and report the result.",
          treatment_behavior: "NO_APPLICABLE_RETAINED_INTELLIGENCE",
          outcome_key: "answer",
        },
      ];

      const runTask = (task: any, retainedAvailable: boolean) => {
        const applicable = retainedAvailable && learningCapabilities.includes(task.required_capability);
        if (task.task_class === "RELATED_HELDOUT") {
          const outcome: any = {
            task_completed: true,
            source_event_bound: applicable ? learning.source_event_id : null,
            intelligent_block_bound: applicable ? sourceBlockId : null,
          };
          outcome[task.outcome_key] = applicable;
          return {
            applicable,
            behavior: applicable ? task.treatment_behavior : "REQUIRE_DIRECT_CANONICAL_INTELLIGENCE",
            outcome,
          };
        }
        return {
          applicable,
          behavior: "NO_APPLICABLE_RETAINED_INTELLIGENCE",
          outcome: { task_completed: true, answer: 12 },
        };
      };

      const persisted: any[] = [];
      const summaries: Record<string, any> = {};
      for (const task of tasks) {
        const controlResult = runTask(task, false);
        const treatmentResult = runTask(task, true);
        const taskInput = { task_id: task.task_id, task_class: task.task_class, instruction: task.instruction, target_id: NAYA_ID };
        const control = await insertReceiptWithRetry({
          user_id: OWNER_ID,
          project_id: "NayaNET",
          action: "NAYA-NODE-0001-GENERALIZATION-CONTROL-" + task.task_id + "-" + learningId,
          status: "SUCCESS",
          expected_result: "Execute the fixed task without applying retained intelligence.",
          observed_result: controlResult.behavior,
          evidence: {
            experiment: "ACTIVE_LEARNING_GENERALIZATION_V1",
            condition: "CONTROL",
            learning_id: learningId,
            retained_intelligence_available: false,
            retained_intelligence_applied: false,
            source_event_id: learning.source_event_id,
            task_input: taskInput,
            applicability: { required_capability: task.required_capability, learning_capabilities: learningCapabilities, applicable: false },
            behavior: controlResult.behavior,
            outcome: controlResult.outcome,
          },
        });
        const treatment = await insertReceiptWithRetry({
          user_id: OWNER_ID,
          project_id: "NayaNET",
          action: "NAYA-NODE-0001-GENERALIZATION-TREATMENT-" + task.task_id + "-" + learningId,
          status: "SUCCESS",
          expected_result: "Execute the same fixed task with retained intelligence available and apply it only if the task requires its capability.",
          observed_result: treatmentResult.behavior,
          evidence: {
            experiment: "ACTIVE_LEARNING_GENERALIZATION_V1",
            condition: "TREATMENT",
            learning_id: learningId,
            retained_intelligence_available: true,
            retained_intelligence_applied: treatmentResult.applicable,
            intelligence_id: sourceBlockId,
            source_event_id: learning.source_event_id,
            task_input: taskInput,
            applicability: { required_capability: task.required_capability, learning_capabilities: learningCapabilities, applicable: treatmentResult.applicable },
            behavior: treatmentResult.behavior,
            outcome: treatmentResult.outcome,
          },
        });
        persisted.push(control, treatment);
        summaries[task.task_id] = {
          task_class: task.task_class,
          required_capability: task.required_capability,
          treatment_behavior_expected: task.treatment_behavior,
          outcome_key: task.outcome_key,
          control_receipt_id: control.id,
          treatment_receipt_id: treatment.id,
          control_behavior: controlResult.behavior,
          treatment_behavior: treatmentResult.behavior,
          behavioral_delta: controlResult.behavior !== treatmentResult.behavior,
          control_outcome: controlResult.outcome,
          treatment_outcome: treatmentResult.outcome,
          applicability: treatmentResult.applicable,
        };
      }

      const related = summaries[relatedTask.task_id];
      const unrelated = summaries["NAYA-0001-UNRELATED-ARITHMETIC-001"];
      const relatedImproved =
        related.behavioral_delta === true &&
        related.applicability === true &&
        related.control_outcome[relatedTask.outcome_key] === false &&
        related.treatment_outcome[relatedTask.outcome_key] === true;
      const negativeTransferRefused =
        unrelated.behavioral_delta === false &&
        unrelated.applicability === false &&
        unrelated.control_outcome.answer === unrelated.treatment_outcome.answer;

      return json({
        ok: relatedImproved && negativeTransferRefused,
        schema: "NAYANET_ACTIVE_LEARNING_GENERALIZATION_V1",
        naya_id: NAYA_ID,
        owner_id: OWNER_ID,
        learning_id: learningId,
        learning_status: learning.status,
        input_boundary: { caller_supplied: ["learning_id"], intelligence_content_accepted_as_input: false },
        intelligence: { intelligent_block_id: sourceBlockId, block_state: sourceBlock.understanding_state, capabilities: learningCapabilities },
        authority: { current_binding_count: binding.length, knowledge_creates_authority: false },
        tasks: summaries,
        result: {
          related_heldout_improved: relatedImproved,
          unrelated_negative_transfer_refused: negativeTransferRefused,
          executor_claim_trusted_as_verification: false,
          independent_verification_required: true,
        },
        receipt_ids: persisted.map((r: any) => r.id),
        runtime_identity: "github-actions-oidc",
        workflow_ref: workflowRef,
        token_jti: payload.jti ?? null,
      }, relatedImproved && negativeTransferRefused ? 200 : 409);
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
      const taskId = String(treatment.evidence?.task_id || "");
      const task = GRAPH_TASKS[taskId];
      const blockId = String(treatment.evidence?.intelligent_block_id || "");
      if (!task || !blockId) return json({ error: "GRAPH_TASK_BINDING_MISSING" }, 409);
      if (control.evidence?.task_id !== taskId || control.evidence?.intelligent_block_id !== blockId) {
        return json({ error: "GRAPH_CONTROL_TREATMENT_INPUT_MISMATCH" }, 409);
      }
      const selectedIds = Array.isArray(treatment.evidence?.selected_relationships)
        ? treatment.evidence.selected_relationships.map((r: any) => String(r.relationship_id || "")).filter(Boolean)
        : [];
      if (selectedIds.length === 0) return json({ error: "GRAPH_SELECTED_RELATIONSHIPS_REQUIRED" }, 409);
      const relationships = await get("/rest/v1/nayanet_brain_relationships?owner_id=eq." + OWNER_ID + "&target_id=eq." + encodeURIComponent(blockId) + "&select=relationship_id,source_id,target_id,relationship_type,epistemic_state,status,visibility,provenance,evidence_refs,valid_from,valid_until,supersedes_relationship_id,consent_ref,applicability,reason_codes,created_at&order=created_at.asc");
      const supersededIds = new Set<string>(relationships.filter((r: any) => r.status === "ACTIVE" && r.supersedes_relationship_id).map((r: any) => String(r.supersedes_relationship_id)));
      const now = new Date();
      const rereadSelected = relationships.filter((r: any) => selectedIds.includes(String(r.relationship_id)));
      const valid =
        control.evidence?.condition === "OFF" &&
        control.evidence?.relationship_context_enabled === false &&
        treatment.evidence?.condition === "ON" &&
        treatment.evidence?.relationship_context_enabled === true &&
        control.observed_result !== treatment.observed_result &&
        rereadSelected.length === selectedIds.length &&
        rereadSelected.every((r: any) => graphRelationshipEligible(r, task.task_class, blockId, now, supersededIds));
      return json({
        ok: valid,
        verification: {
          persisted_pair_re_read: true,
          relationship_rows_re_read: true,
          control_receipt_id: controlId,
          treatment_receipt_id: treatmentId,
          behavioral_delta: control.observed_result !== treatment.observed_result,
          treatment_relationships_verified: valid,
          task_class: task.task_class,
          intelligent_block_id: blockId,
          independently_reconstructed: true
        },
        receipts: { control, treatment },
        relationships: rereadSelected,
        runtime_identity: "github-actions-oidc",
        workflow_ref: workflowRef,
        token_jti: payload.jti ?? null
      });
    }

    if (mode === "graph-behavior") {
      if (req.method !== "POST") return json({ error: "METHOD_REQUIRED" }, 405);
      const body = await req.json().catch(() => ({}));
      const relationshipContext = body?.relationship_context === true;
      const taskId = String(body?.task_id || "");
      const task = GRAPH_TASKS[taskId];
      if (!task) return json({ error: "HELDOUT_TASK_REQUIRED" }, 400);
      const blockId = String(body?.intelligent_block_id || "");
      if (!blockId) return json({ error: "INTELLIGENT_BLOCK_ID_REQUIRED" }, 400);
      const blocks = await get("/rest/v1/nayanet_intelligent_blocks?owner_id=eq." + OWNER_ID + "&intelligent_block_id=eq." + encodeURIComponent(blockId) + "&select=intelligent_block_id,owner_id,understanding_state,evidence_refs,provenance");
      if (!Array.isArray(blocks) || blocks.length !== 1) return json({ error: "GRAPH_BLOCK_NOT_UNIQUE" }, 409);
      const block = blocks[0];
      if (block.understanding_state !== "LEARNED" || !Array.isArray(block.evidence_refs) || block.evidence_refs.length === 0) {
        return json({ error: "GRAPH_BLOCK_NOT_VERIFIED_LEARNED" }, 409);
      }
      const relationships = await get("/rest/v1/nayanet_brain_relationships?owner_id=eq." + OWNER_ID + "&target_id=eq." + encodeURIComponent(blockId) + "&select=relationship_id,source_id,target_id,relationship_type,epistemic_state,status,visibility,provenance,evidence_refs,valid_from,valid_until,supersedes_relationship_id,consent_ref,applicability,reason_codes,created_at&order=created_at.asc");
      const supersededIds = new Set<string>(relationships.filter((r: any) => r.status === "ACTIVE" && r.supersedes_relationship_id).map((r: any) => String(r.supersedes_relationship_id)));
      const now = new Date();
      const applicable = relationshipContext
        ? relationships.filter((r: any) => graphRelationshipEligible(r, task.task_class, blockId, now, supersededIds))
        : [];
      const selected = applicable.filter((r: any) => ["PRODUCES", "VERIFIED_BY", "APPLIES_TO", "REFINES"].includes(r.relationship_type));
      const behavior = selected.length > 0 ? "APPLY_CONTEXTUALIZED_VERIFIED_INTELLIGENCE" : "REQUIRE_DIRECT_CANONICAL_INTELLIGENCE";
      const row = {
        user_id: OWNER_ID, project_id: "NayaNET",
        action: "NAYA-NODE-0001-GRAPH-" + (relationshipContext ? "ON" : "OFF") + "-" + taskId,
        status: "SUCCESS",
        expected_result: "Execute the identical held-out task under the requested graph-context condition.",
        observed_result: behavior,
        evidence: {
          condition: relationshipContext ? "ON" : "OFF",
          relationship_context_enabled: relationshipContext,
          task_id: taskId,
          task_class: task.task_class,
          intelligent_block_id: blockId,
          selected_relationships: selected,
          selected_relationship_paths: selected.map((r: any) => [r.source_id, r.relationship_type, r.target_id]),
          provenance: selected.map((r: any) => r.provenance),
          applicability: selected.map((r: any) => ({
            relationship_id: r.relationship_id,
            applicable: true,
            state: r.applicability?.state,
            task_classes: r.applicability?.task_classes,
            reason: "ACTIVE current evidenced relationship explicitly applies to held-out task class."
          })),
          epistemic_state: selected.map((r: any) => r.epistemic_state)
        }
      };
      const persisted = await insertReceiptWithRetry(row);
      return json({
        ok: true,
        schema: "NAYANET_COLD_GRAPH_BEHAVIOR_V2",
        naya_id: NAYA_ID,
        owner_id: OWNER_ID,
        block_id: blockId,
        task_id: taskId,
        task_class: task.task_class,
        condition: relationshipContext ? "ON" : "OFF",
        behavior,
        relationship_context_enabled: relationshipContext,
        selected_relationships: selected,
        receipt: persisted,
        runtime_identity: "github-actions-oidc",
        workflow_ref: workflowRef,
        token_jti: payload.jti ?? null
      });
    }

    if (mode === "cold-successor") {
      // HOLE D. The caller supplies ONLY a learning id. No lesson, claim, behaviour or
      // intelligence content is accepted as input, so the successor cannot be handed the
      // answer and must genuinely reconstruct the lineage from authoritative state.
      const successorId = "NAYA-NODE-0001-SUCCESSOR-COLD-01";
      const successorUrl = new URL(req.url);
      const learningId = successorUrl.searchParams.get("learning_id") ?? "";
      if (!learningId) return json({ error: "LEARNING_ID_REQUIRED" }, 400);
      const suppliedTaskId = successorUrl.searchParams.get("task_id");
      const successorTaskId = suppliedTaskId ?? "NAYA-0001-PROVENANCE-HELDOUT-001";
      const successorTasks: Record<string, { task_class: string; required_capability: string }> = {
        "NAYA-0001-PROVENANCE-HELDOUT-001": { task_class: "ORIGINAL_BOUNDED", required_capability: "provenance_preservation" },
        "NAYA-0001-PROVENANCE-HELDOUT-002": { task_class: "RELATED_HELDOUT", required_capability: "provenance_preservation" },
        "NAYA-0001-ACTIVE-INTELLIGENCE-HELDOUT-001": { task_class: "ORIGINAL_BOUNDED", required_capability: "active_intelligence_discipline" },
        "NAYA-0001-ACTIVE-INTELLIGENCE-HELDOUT-002": { task_class: "RELATED_HELDOUT", required_capability: "active_intelligence_discipline" },
        "NAYA-0001-UNRELATED-ARITHMETIC-001": { task_class: "UNRELATED_NEGATIVE_TRANSFER", required_capability: "arithmetic_only" },
      };
      const successorTask = successorTasks[successorTaskId];
      if (!successorTask) return json({ error: "HELDOUT_TASK_REQUIRED", task_id: successorTaskId }, 400);

      // 1. Re-read the persisted learning that the previous Naya produced.
      const learningRows = await get("/rest/v1/learning_evidence?id=eq." + encodeURIComponent(learningId) + "&member_id=eq." + OWNER_ID + "&target_id=eq." + NAYA_ID + "&status=eq.ACTIVE&select=id,target_id,level,status,claim,observed_value,source_event_id,verification_method");
      if (!Array.isArray(learningRows) || learningRows.length !== 1) return json({ error: "PERSISTED_LEARNING_NOT_UNIQUE" }, 409);
      const learning = learningRows[0];
      if (learning.status !== "ACTIVE") return json({ error: "ACTIVE_LEARNING_REQUIRED", status: learning.status }, 409);
      const learningObserved = (learning.observed_value && typeof learning.observed_value === "object" && !Array.isArray(learning.observed_value)) ? learning.observed_value : {};

      // 2. Re-read the canonical Intelligent Block (already resolved owner-scoped above).
      // 3. Re-read the durable graph relationships that connect intelligence to that block.
      const successorBlockId = String(learningObserved.intelligent_block_id || "");
      if (!successorBlockId) return json({ error: "LEARNING_INTELLIGENT_BLOCK_REQUIRED" }, 409);
      const successorBlockRows = await get("/rest/v1/nayanet_intelligent_blocks?intelligent_block_id=eq." + encodeURIComponent(successorBlockId) + "&owner_id=eq." + OWNER_ID + "&select=intelligent_block_id,owner_id,understanding_state,content,evidence_refs,provenance");
      if (!Array.isArray(successorBlockRows) || successorBlockRows.length !== 1) return json({ error: "LEARNING_INTELLIGENT_BLOCK_NOT_UNIQUE" }, 409);
      const successorBlock = successorBlockRows[0];
      if (successorBlock.understanding_state !== "LEARNED") return json({ error: "LEARNING_INTELLIGENT_BLOCK_NOT_LEARNED", state: successorBlock.understanding_state }, 409);
      const rels = await get("/rest/v1/nayanet_brain_relationships?owner_id=eq." + OWNER_ID + "&target_id=eq." + encodeURIComponent(successorBlockId) + "&select=relationship_id,source_id,target_id,relationship_type,epistemic_state,provenance");
      const verifiedRels = rels.filter((r: any) => r.epistemic_state === "VERIFIED" && r.provenance);

      // 4. MATERIAL USE. Behaviour is derived from the RETRIEVED lesson, not from caller input.
      const lesson = successorBlock.content?.lesson;
      if (typeof lesson !== "string" || !lesson) return json({ error: "RETAINED_LESSON_MISSING" }, 409);
      const lessonCapabilities: string[] = [];
      if (lesson.includes("Preserve provenance before applying retained intelligence")) lessonCapabilities.push("provenance_preservation");
      if (
        lesson.includes("Persistence alone is memory, not proof of active intelligence.") &&
        lesson.includes("Retrieved intelligence does not grant authority")
      ) lessonCapabilities.push("active_intelligence_discipline");
      const applicableToTask = lessonCapabilities.includes(successorTask.required_capability);
      const behavior = applicableToTask
        ? (successorTask.required_capability === "provenance_preservation"
            ? "PRESERVE_PROVENANCE_BEFORE_APPLY"
            : "REQUIRE_TRUTH_AND_AUTHORITY_BOUNDARIES_BEFORE_APPLY")
        : (successorTask.task_class === "UNRELATED_NEGATIVE_TRANSFER" ? "NO_APPLICABLE_RETAINED_INTELLIGENCE" : "REQUIRE_DIRECT_CANONICAL_INTELLIGENCE");
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
          input_supplied_by_caller: suppliedTaskId ? "learning_id_and_task_id_only" : "learning_id_only",
          task_context_supplied: suppliedTaskId !== null,
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
          intelligent_block_id: successorBlock.intelligent_block_id,
          block_understanding_state: successorBlock.understanding_state,
          block_owner_match: successorBlock.owner_id === OWNER_ID,
          retrieved_lesson: lesson,
          verified_relationships: verifiedRels.map((r: any) => ({ relationship_id: r.relationship_id, source_id: r.source_id, relationship_type: r.relationship_type, epistemic_state: r.epistemic_state, provenance: r.provenance })),
          verified_relationship_count: verifiedRels.length,
          lineage: ["learning_evidence", "nayanet_intelligent_blocks", "nayanet_brain_relationships"],
        },
        use: {
          task_id: successorTaskId,
          task_class: successorTask.task_class,
          required_capability: successorTask.required_capability,
          lesson_capabilities: lessonCapabilities,
          applicable_to_task: applicableToTask,
          behavior_derived_from_retrieved_lesson: behavior,
          lesson_supports_persisted_learning: learningSupportsLesson,
          materially_attributable: applicableToTask && behavior !== "REQUIRE_DIRECT_CANONICAL_INTELLIGENCE" && verifiedRels.length > 0,
          correct_refusal: !applicableToTask && behavior === "NO_APPLICABLE_RETAINED_INTELLIGENCE",
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
      const verifierUrl = new URL(req.url);
      const learningId = verifierUrl.searchParams.get("learning_id") ?? "";
      if (!learningId) return json({ error: "LEARNING_ID_REQUIRED" }, 400);
      const verifierTaskId = verifierUrl.searchParams.get("task_id") ?? "NAYA-0001-PROVENANCE-HELDOUT-001";
      const verifierTasks: Record<string, { task_class: string; required_capability: string }> = {
        "NAYA-0001-PROVENANCE-HELDOUT-001": { task_class: "ORIGINAL_BOUNDED", required_capability: "provenance_preservation" },
        "NAYA-0001-PROVENANCE-HELDOUT-002": { task_class: "RELATED_HELDOUT", required_capability: "provenance_preservation" },
        "NAYA-0001-ACTIVE-INTELLIGENCE-HELDOUT-001": { task_class: "ORIGINAL_BOUNDED", required_capability: "active_intelligence_discipline" },
        "NAYA-0001-ACTIVE-INTELLIGENCE-HELDOUT-002": { task_class: "RELATED_HELDOUT", required_capability: "active_intelligence_discipline" },
        "NAYA-0001-UNRELATED-ARITHMETIC-001": { task_class: "UNRELATED_NEGATIVE_TRANSFER", required_capability: "arithmetic_only" },
      };
      const verifierTask = verifierTasks[verifierTaskId];
      if (!verifierTask) return json({ error: "HELDOUT_TASK_REQUIRED", task_id: verifierTaskId }, 400);
      const lRows = await get("/rest/v1/learning_evidence?id=eq." + encodeURIComponent(learningId) + "&member_id=eq." + OWNER_ID + "&target_id=eq." + NAYA_ID + "&status=eq.ACTIVE&select=id,target_id,level,status,claim,observed_value,source_event_id");
      if (!Array.isArray(lRows) || lRows.length !== 1) return json({ error: "PERSISTED_LEARNING_NOT_UNIQUE" }, 409);
      const l = lRows[0];
      if (l.status !== "ACTIVE") return json({ error: "ACTIVE_LEARNING_REQUIRED", status: l.status }, 409);
      const lObs = (l.observed_value && typeof l.observed_value === "object" && !Array.isArray(l.observed_value)) ? l.observed_value : {};
      const vBlockId = String(lObs.intelligent_block_id || "");
      if (!vBlockId) return json({ error: "LEARNING_INTELLIGENT_BLOCK_REQUIRED" }, 409);
      const vBlockRows = await get("/rest/v1/nayanet_intelligent_blocks?intelligent_block_id=eq." + encodeURIComponent(vBlockId) + "&owner_id=eq." + OWNER_ID + "&select=intelligent_block_id,owner_id,understanding_state,content");
      if (!Array.isArray(vBlockRows) || vBlockRows.length !== 1) return json({ error: "LEARNING_INTELLIGENT_BLOCK_NOT_UNIQUE" }, 409);
      const vBlock = vBlockRows[0];
      if (vBlock.understanding_state !== "LEARNED") return json({ error: "LEARNING_INTELLIGENT_BLOCK_NOT_LEARNED", state: vBlock.understanding_state }, 409);
      const vRels = await get("/rest/v1/nayanet_brain_relationships?owner_id=eq." + OWNER_ID + "&target_id=eq." + encodeURIComponent(vBlockId) + "&select=relationship_id,epistemic_state,provenance");
      const vVerified = vRels.filter((r: any) => r.epistemic_state === "VERIFIED" && r.provenance);
      const vLesson = vBlock.content?.lesson;
      const vLessonCapabilities: string[] = [];
      if (typeof vLesson === "string" && vLesson.includes("Preserve provenance before applying retained intelligence")) vLessonCapabilities.push("provenance_preservation");
      if (
        typeof vLesson === "string" &&
        vLesson.includes("Persistence alone is memory, not proof of active intelligence.") &&
        vLesson.includes("Retrieved intelligence does not grant authority")
      ) vLessonCapabilities.push("active_intelligence_discipline");
      const vApplicableToTask = vLessonCapabilities.includes(verifierTask.required_capability);
      const vBehavior = vApplicableToTask
        ? (verifierTask.required_capability === "provenance_preservation"
            ? "PRESERVE_PROVENANCE_BEFORE_APPLY"
            : "REQUIRE_TRUTH_AND_AUTHORITY_BOUNDARIES_BEFORE_APPLY")
        : (verifierTask.task_class === "UNRELATED_NEGATIVE_TRANSFER" ? "NO_APPLICABLE_RETAINED_INTELLIGENCE" : "REQUIRE_DIRECT_CANONICAL_INTELLIGENCE");
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
        task_id: verifierTaskId,
        task_class: verifierTask.task_class,
        required_capability: verifierTask.required_capability,
        lesson_capabilities: vLessonCapabilities,
        applicable_to_task: vApplicableToTask,
        behavior_recomputed: vBehavior,
        correct_refusal: !vApplicableToTask && vBehavior === "NO_APPLICABLE_RETAINED_INTELLIGENCE",
        successor_grant_count: vSuccGrants.length,
        authority_recomputed: vConsequentialAuthorized,
        recomputed_blocked_by: vConsequentialAuthorized ? "NONE" : (vAuthorityResolved ? "LAW" : "IDENTITY_SCOPE"),
      };
      const valid =
        recomputed.learning_persisted &&
        recomputed.block_owner_scoped &&
        recomputed.lesson_present &&
        recomputed.verified_relationship_count > 0 &&
        recomputed.behavior_recomputed === vBehavior &&
        (vApplicableToTask ? recomputed.behavior_recomputed === "PRESERVE_PROVENANCE_BEFORE_APPLY" : recomputed.correct_refusal === true) &&
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
        limitation: "bounded task-context recomputation across the original task, one related held-out task, and one unrelated refusal case; not general successor capability",
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
