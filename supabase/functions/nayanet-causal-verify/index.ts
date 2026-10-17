import { createRemoteJWKSet, jwtVerify } from "https://esm.sh/jose@6.0.10";
import { createClient } from "npm:@supabase/supabase-js@2";
import { assessActIdempotencyReceipt } from "./verify-act-idempotency.ts";

const ISSUER = "https://token.actions.githubusercontent.com";
const AUDIENCE = "nayanet-runtime";
const REPOSITORY = "SoulSchoolAcademy/NayaPOWER";
const WORKFLOW = ".github/workflows/live-cvo-runtime-proof.yml";
const REF = "refs/heads/main";
const NAYA_ID = "NAYA-NODE-0001";
const OWNER_ID = "adfdf0b8-5558-41d1-9fed-ec51abf4fe2f";
const MISSION_ID = "NAYA-NODE-0001-CONTINUITY";
const DEFAULT_TREATMENT_ID = "6aee287d-c47d-4667-86ed-6b53be8bd384";
const DEFAULT_CONTROL_ID = "b00ed556-d7b7-4e5e-90a0-4620b9aaef67";
const JWKS = createRemoteJWKSet(new URL("https://token.actions.githubusercontent.com/.well-known/jwks"));

const json = (body: unknown, status = 200) => new Response(JSON.stringify(body), {
  status,
  headers: {"content-type":"application/json","cache-control":"no-store"},
});

async function authenticate(req: Request) {
  const auth = req.headers.get("authorization") ?? "";
  if (!auth.startsWith("Bearer ")) throw new Error("RUNTIME_IDENTITY_REQUIRED");
  let payload: Record<string, unknown>;
  try {
    const verified = await jwtVerify(auth.slice(7), JWKS, {issuer: ISSUER, audience: AUDIENCE});
    payload = verified.payload as Record<string, unknown>;
  } catch (_error) {
    throw new Error("GITHUB_OIDC_INVALID");
  }
  const workflowRef = REPOSITORY + "/" + WORKFLOW + "@" + REF;
  if (payload.repository !== REPOSITORY || payload.workflow_ref !== workflowRef || payload.ref !== REF) {
    throw new Error("WORKFLOW_BINDING_MISMATCH");
  }
  return {payload, workflowRef};
}

Deno.serve(async (req: Request) => {
  if (req.method !== "POST") return json({ok:false,error:"METHOD_NOT_ALLOWED"},405);
  try {
    const {payload, workflowRef} = await authenticate(req);
    const supabaseUrl = Deno.env.get("SUPABASE_URL");
    const serviceRole = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");
    if (!supabaseUrl || !serviceRole) return json({ok:false,error:"SERVER_AUTH_CONFIG_MISSING"},500);
    const admin = createClient(supabaseUrl, serviceRole);

    const {data: grants, error: grantError} = await admin
      .from("nayanet_authority_grants")
      .select("grant_id,issuer_id,subject_id,mission_id,scope,actions,constraints,status,evidence")
      .eq("issuer_id", OWNER_ID)
      .eq("subject_id", OWNER_ID)
      .eq("mission_id", MISSION_ID)
      .eq("status", "ACTIVE");
    if (grantError) throw grantError;
    const binding = (grants ?? []).filter((grant: Record<string,unknown>) => {
      const scope = grant.scope as Record<string,unknown> | undefined;
      const actions = Array.isArray(grant.actions) ? grant.actions : [];
      return scope?.target === NAYA_ID && actions.includes("naya_node_apply");
    });
    if (binding.length !== 1) { console.error("CVO_REJECT", "DURABLE_NAYA_AUTHORIZATION_BINDING_INVALID", binding.length); return json({ok:false,error:"DURABLE_NAYA_AUTHORIZATION_BINDING_INVALID",count:binding.length},403); }

    const body = await req.json().catch(() => ({}));
    const mode = String(body.mode ?? "cvo");
    const treatmentId = String(body.treatment_receipt_id ?? DEFAULT_TREATMENT_ID);
    const controlId = String(body.control_receipt_id ?? DEFAULT_CONTROL_ID);
    if (mode !== "cvo" && mode !== "verify" && mode !== "recover-learning-outcomes" && mode !== "verify-act-idempotency") return json({ok:false,error:"UNSUPPORTED_MODE"},400);

    if (mode === "verify-act-idempotency") {
      // P7: VERIFY independently recomputes the ACT idempotency binding.
      // The executor's fingerprint claim is re-derived here from the
      // receipt's own persisted inputs and compared. Any mismatch — or
      // any inability to recompute — is FAIL CLOSED (409), never a pass.
      const receiptId = String(body.action_receipt_id ?? "").trim();
      if (!receiptId) return json({ok:false,error:"ACTION_RECEIPT_ID_REQUIRED"},400);
      const {data: actReceipt, error: actReceiptError} = await admin
        .from("nayanet_execution_receipts")
        .select("id,user_id,project_id,action,status,observed_result,evidence,idempotency_key")
        .eq("id", receiptId)
        .eq("user_id", OWNER_ID)
        .eq("project_id", "NayaNET")
        .maybeSingle();
      if (actReceiptError) throw actReceiptError;
      const assessment = await assessActIdempotencyReceipt(actReceipt);
      const ok = assessment.ok === true;
      if (!ok) console.error("VERIFY_ACT_IDEMPOTENCY_REJECT", assessment.code, receiptId);
      return json({
        ok,
        schema: "NAYANET_VERIFY_ACT_IDEMPOTENCY_V1",
        independent_verification: ok,
        executor_claim_trusted: false,
        executor_claim_trusted_as_verification: false,
        assessment,
        receipt_id: receiptId,
        runtime_identity: "github-actions-oidc",
        workflow_ref: workflowRef,
        token_jti: payload.jti ?? null,
      }, ok ? 200 : 409);
    }

    const {data:treatment,error:te} = await admin.from("nayanet_execution_receipts").select("*").eq("id",treatmentId).eq("user_id",OWNER_ID).eq("project_id","NayaNET").maybeSingle();
    if (te) throw te;
    const {data:control,error:ce} = await admin.from("nayanet_execution_receipts").select("*").eq("id",controlId).eq("user_id",OWNER_ID).eq("project_id","NayaNET").maybeSingle();
    if (ce) throw ce;
    if (!treatment || !control) { console.error("CVO_REJECT", "PAIRED_ACTION_RECEIPTS_NOT_FOUND", treatmentId, controlId); return json({ok:false,error:"PAIRED_ACTION_RECEIPTS_NOT_FOUND"},404); }

    if (mode === "recover-learning-outcomes") {
      const evidenceOf = (receipt: any) => {
        if (Array.isArray(receipt?.evidence)) {
          return receipt.evidence
            .filter((item: any) => item && !item?.causal_verification)
            .reduce((acc: any, item: any) => ({...acc, ...item}), {});
        }
        return receipt?.evidence && typeof receipt.evidence === "object" ? receipt.evidence : {};
      };
      const controlEvidence = evidenceOf(control);
      const treatmentEvidence = evidenceOf(treatment);
      const controlTask = controlEvidence.task_input ?? null;
      const treatmentTask = treatmentEvidence.task_input ?? null;
      const sameTask = controlTask !== null && JSON.stringify(controlTask) === JSON.stringify(treatmentTask);
      const sameLearning = Boolean(controlEvidence.learning_id)
        && controlEvidence.learning_id === treatmentEvidence.learning_id;
      const sameSourceEvent = Boolean(controlEvidence.source_event_id)
        && controlEvidence.source_event_id === treatmentEvidence.source_event_id;
      const controlValid = String(control.action).startsWith("NAYA-NODE-0001-CONTROL-")
        && control.status === "SUCCESS"
        && controlEvidence.condition === "CONTROL"
        && controlEvidence.retained_intelligence_used === false
        && controlEvidence.outcome?.task_completed === true
        && controlEvidence.outcome?.provenance_preserved === false
        && String(control.observed_result) === String(controlEvidence.behavior ?? "");
      const treatmentValid = String(treatment.action).startsWith("NAYA-NODE-0001-TREATMENT-")
        && treatment.status === "SUCCESS"
        && treatmentEvidence.condition === "TREATMENT"
        && treatmentEvidence.retained_intelligence_used === true
        && typeof treatmentEvidence.intelligence_id === "string"
        && treatmentEvidence.intelligence_id.length > 0
        && treatmentEvidence.outcome?.task_completed === true
        && treatmentEvidence.outcome?.provenance_preserved === true
        && treatmentEvidence.outcome?.intelligent_block_bound === treatmentEvidence.intelligence_id
        && String(treatment.observed_result) === String(treatmentEvidence.behavior ?? "");
      const taskId = String(controlTask?.task_id ?? "");
      if (!sameTask || !sameLearning || !sameSourceEvent || !controlValid || !treatmentValid || taskId !== "NAYA-0001-PROVENANCE-HELDOUT-001") {
        return json({
          ok:false,
          error:"LEARNING_OUTCOME_RECOVERY_PAIR_INVALID",
          recomputed:{same_task:sameTask,same_learning:sameLearning,same_source_event:sameSourceEvent,control_valid:controlValid,treatment_valid:treatmentValid,task_id:taskId},
        },409);
      }

      const {data: existingOutcomes, error: existingOutcomeError} = await admin
        .from("nayanet_execution_outcomes")
        .select("outcome_id,receipt_id,experiment_case_id,outcome_type,evidence,verified,verification_method,verified_value")
        .in("receipt_id",[controlId,treatmentId])
        .eq("user_id",OWNER_ID)
        .eq("project_id","NayaNET");
      if (existingOutcomeError) throw existingOutcomeError;
      if ((existingOutcomes ?? []).length === 1) {
        return json({ok:false,error:"LEARNING_OUTCOME_RECOVERY_PARTIAL_STATE",existing_outcomes:existingOutcomes},409);
      }

      const method = "INDEPENDENT_RUNTIME_RECOMPUTATION_FROM_PERSISTED_CAUSAL_RECEIPTS";
      if ((existingOutcomes ?? []).length === 0) {
        const rows = [
          {
            receipt_id: controlId,
            user_id: OWNER_ID,
            project_id: "NayaNET",
            experiment_case_id: taskId,
            outcome_type: "CAUSAL_CONTROL_OUTCOME",
            verifier_id: OWNER_ID,
            evidence: {
              control_condition: true,
              treatment_condition: false,
              provenance_present: false,
              learning_id: controlEvidence.learning_id,
              source_event_id: controlEvidence.source_event_id,
              task_input: controlTask,
              behavior: controlEvidence.behavior,
              observed_result: control.observed_result,
              task_completed: true,
              runtime_identity: "github-actions-oidc",
              workflow_ref: workflowRef,
              verifier_token_jti: payload.jti ?? null,
            },
            verified: true,
            verification_method: method,
          },
          {
            receipt_id: treatmentId,
            user_id: OWNER_ID,
            project_id: "NayaNET",
            experiment_case_id: taskId,
            outcome_type: "CAUSAL_TREATMENT_OUTCOME",
            verifier_id: OWNER_ID,
            evidence: {
              control_condition: false,
              treatment_condition: true,
              provenance_present: true,
              intelligence_id: treatmentEvidence.intelligence_id,
              learning_id: treatmentEvidence.learning_id,
              source_event_id: treatmentEvidence.source_event_id,
              task_input: treatmentTask,
              behavior: treatmentEvidence.behavior,
              observed_result: treatment.observed_result,
              task_completed: true,
              runtime_identity: "github-actions-oidc",
              workflow_ref: workflowRef,
              verifier_token_jti: payload.jti ?? null,
            },
            verified: true,
            verification_method: method,
          },
        ];
        const {error: insertOutcomeError} = await admin.from("nayanet_execution_outcomes").insert(rows);
        if (insertOutcomeError) throw insertOutcomeError;
      }

      const {data: recovered, error: rereadError} = await admin
        .from("nayanet_execution_outcomes")
        .select("outcome_id,receipt_id,experiment_case_id,outcome_type,evidence,verified,verification_method,verified_value")
        .in("receipt_id",[controlId,treatmentId])
        .eq("user_id",OWNER_ID)
        .eq("project_id","NayaNET");
      if (rereadError) throw rereadError;
      if (!Array.isArray(recovered) || recovered.length !== 2) {
        return json({ok:false,error:"LEARNING_OUTCOME_RECOVERY_REREAD_FAILED",count:Array.isArray(recovered)?recovered.length:0},409);
      }
      const byReceipt = new Map(recovered.map((row:any) => [String(row.receipt_id), row]));
      const recoveredControl:any = byReceipt.get(controlId);
      const recoveredTreatment:any = byReceipt.get(treatmentId);
      const valid = recoveredControl?.verified === true
        && recoveredTreatment?.verified === true
        && recoveredControl?.verification_method === method
        && recoveredTreatment?.verification_method === method
        && recoveredControl?.experiment_case_id === taskId
        && recoveredTreatment?.experiment_case_id === taskId
        && recoveredControl?.evidence?.control_condition === true
        && recoveredControl?.evidence?.provenance_present === false
        && recoveredTreatment?.evidence?.treatment_condition === true
        && recoveredTreatment?.evidence?.provenance_present === true
        && recoveredTreatment?.evidence?.intelligence_id === treatmentEvidence.intelligence_id
        && JSON.stringify(recoveredControl?.evidence?.task_input) === JSON.stringify(controlTask)
        && JSON.stringify(recoveredTreatment?.evidence?.task_input) === JSON.stringify(treatmentTask);
      return json({
        ok:valid,
        schema:"NAYANET_CAUSAL_OUTCOME_RECOVERY_V1",
        independent_verification:valid,
        executor_claim_trusted:false,
        recovery_mode:(existingOutcomes ?? []).length === 0 ? "CREATED_AND_REREAD" : "REPLAYED_AND_REREAD",
        receipt_ids:[controlId,treatmentId],
        outcomes:recovered,
        recomputed:{same_task:sameTask,same_learning:sameLearning,same_source_event:sameSourceEvent,control_valid:controlValid,treatment_valid:treatmentValid},
        workflow_ref:workflowRef,
        token_jti:payload.jti ?? null,
      },valid?200:409);
    }

    const {data:treatmentOutcome,error:toe} = await admin
      .from("nayanet_execution_outcomes")
      .select("outcome_id,receipt_id,experiment_case_id,outcome_type,evidence,verified,verification_method,verified_value")
      .eq("receipt_id",treatmentId)
      .eq("user_id",OWNER_ID)
      .eq("project_id","NayaNET")
      .maybeSingle();
    if (toe) throw toe;
    const {data:controlOutcome,error:coe} = await admin
      .from("nayanet_execution_outcomes")
      .select("outcome_id,receipt_id,experiment_case_id,outcome_type,evidence,verified,verification_method,verified_value")
      .eq("receipt_id",controlId)
      .eq("user_id",OWNER_ID)
      .eq("project_id","NayaNET")
      .maybeSingle();
    if (coe) throw coe;
    if (!treatmentOutcome || !controlOutcome) return json({ok:false,error:"PAIRED_ACTION_OUTCOMES_NOT_FOUND"},404);
    if (!treatmentOutcome.verified || !controlOutcome.verified) return json({ok:false,error:"PAIRED_ACTION_OUTCOMES_NOT_VERIFIED"},409);
    if (treatmentOutcome.experiment_case_id !== "NAYA-NODE-0001-COLD-BEHAVIOR" || controlOutcome.experiment_case_id !== "NAYA-NODE-0001-COLD-BEHAVIOR") {
      return json({ok:false,error:"PAIRED_ACTION_OUTCOME_CASE_INVALID"},409);
    }
    const treatmentOutcomeEvidence = (treatmentOutcome.evidence ?? {}) as Record<string,unknown>;
    const controlOutcomeEvidence = (controlOutcome.evidence ?? {}) as Record<string,unknown>;
    if (treatmentOutcomeEvidence.treatment_condition !== true || treatmentOutcomeEvidence.intelligence_id !== "IB-NAYA-NODE-0001-0001" || treatmentOutcomeEvidence.provenance_present !== true) {
      return json({ok:false,error:"TREATMENT_OUTCOME_EVIDENCE_INVALID"},409);
    }
    if (controlOutcomeEvidence.control_condition !== true || controlOutcomeEvidence.provenance_present !== false) {
      return json({ok:false,error:"CONTROL_OUTCOME_EVIDENCE_INVALID"},409);
    }

    if (treatment.action !== "NAYA-NODE-0001-TREATMENT" || control.action !== "NAYA-NODE-0001-BASELINE") {
      { console.error("CVO_REJECT", "PAIRED_ACTION_RECEIPTS_INVALID", treatment.action, control.action); return json({ok:false,error:"PAIRED_ACTION_RECEIPTS_INVALID"},409); }
    }
    if (treatment.status !== "SUCCESS" || control.status !== "SUCCESS") {
      { console.error("CVO_REJECT", "PAIRED_ACTION_OUTCOME_NOT_SUCCESS", treatment.status, control.status); return json({ok:false,error:"PAIRED_ACTION_OUTCOME_NOT_SUCCESS"},409); }
    }

    if (mode === "verify") {
      const evidence = Array.isArray(treatment.evidence) ? treatment.evidence : [];
      const causal = evidence.find((item: Record<string,unknown>) => item?.causal_verification)?.causal_verification as Record<string,unknown> | undefined;
      if (!causal) return json({ok:false,error:"CVO_NOT_PERSISTED"},409);
      // Narrow before reading: an independent verifier must compare against persisted
      // structure, not coerce whatever happens to be in the JSONB. A missing/malformed
      // evidence arm now fails closed with a reason instead of silently reading undefined.
      const causalEvidence=(causal.evidence??{}) as {
        treatment?:{outcome_id?:unknown; evidence?:{provenance_present?:unknown}};
        control?:{outcome_id?:unknown; evidence?:{provenance_present?:unknown}};
      };
      const valid = causal.schema === "NAYANET_CAUSAL_VERIFICATION_V1"
        && causal.receipt_id === treatmentId
        && causal.comparison_receipt_id === controlId
        && causal.causal_method === "CONTROLLED_INTERVENTION"
        && causal.causal_assessment === "CAUSAL_SUPPORTED"
        && causal.verification_status === "OUTCOME_VERIFIED"
        && causal.production_action_executed === true
        && causal.observed_change === treatment.observed_result
        && causalEvidence.treatment?.outcome_id === treatmentOutcome.outcome_id
        && causalEvidence.control?.outcome_id === controlOutcome.outcome_id
        && causalEvidence.treatment?.evidence?.provenance_present === true
        && causalEvidence.control?.evidence?.provenance_present === false;
      return json({ok:valid,verification:{independent_verification:valid,receipt_id:treatmentId,comparison_receipt_id:controlId,causal_verification:causal,active_authorization_grant_id:binding[0].grant_id,workflow_ref:workflowRef,token_jti:payload.jti ?? null}}, valid ? 200 : 409);
    }


    const causal = {
      schema: "NAYANET_CAUSAL_VERIFICATION_V1",
      causal_id: "CVO-NAYA-NODE-0001-TREATMENT-V1",
      receipt_id: treatmentId,
      comparison_receipt_id: controlId,
      intent: {
        action: treatment.action,
        expected_result: treatment.expected_result,
      },
      authority: {
        status: "AUTHORIZED",
        grant_id: binding[0].grant_id,
        issuer_id: binding[0].issuer_id,
        subject_id: binding[0].subject_id,
        mission_id: binding[0].mission_id,
      },
      permission: {
        basis: "existing active Naya continuity authorization; causal verification observes an already-completed governed action and does not grant execution authority",
        scope: binding[0].scope,
        actions: binding[0].actions,
        constraints: binding[0].constraints,
      },
      action: {
        name: treatment.action,
        production_action_executed: true,
      },
      observation: {
        result: treatment.observed_result,
        status: treatment.status,
      },
      evidence: {
        refs: [treatmentId, controlId, "IB-NAYA-NODE-0001-0001"],
        control: { outcome_id: controlOutcome.outcome_id, evidence: controlOutcomeEvidence },
        treatment: { outcome_id: treatmentOutcome.outcome_id, evidence: treatmentOutcomeEvidence },
      },
      causal_method: "CONTROLLED_INTERVENTION",
      causal_assessment: "CAUSAL_SUPPORTED",
      alternative_explanations: [
        "execution-context differences unrelated to retained intelligence",
        "provenance availability independent of the retained Intelligent Block",
      ],
      limitations: [
        "paired proof is a bounded experiment and does not establish universal causal effect across all action types",
      ],
      verification_status: "OUTCOME_VERIFIED",
      verification_method: "independent-runtime-reread-of-persisted-treatment-receipt",
      production_action_executed: true,
      observed_change: treatment.observed_result,
      verified_at: new Date().toISOString(),
    };

    const existingEvidence = Array.isArray(treatment.evidence) ? treatment.evidence : [];
    const updatedEvidence = [
      ...existingEvidence.filter((item:Record<string,unknown>) => !item?.causal_verification),
      {causal_verification:causal},
    ];
    const {data:updated,error:ue} = await admin
      .from("nayanet_execution_receipts")
      .update({evidence:updatedEvidence})
      .eq("id",treatmentId)
      .eq("user_id",OWNER_ID)
      .select("id,action,status,evidence")
      .single();
    if (ue) throw ue;

    return json({ok:true,schema:"NAYANET_CAUSAL_VERIFY_RUNTIME_V1",operation_id:causal.causal_id,causal_verification:causal,receipt:updated,runtime_identity:"github-actions-oidc",workflow_ref:workflowRef,token_jti:payload.jti ?? null});
  } catch (error) {
    console.error("NAYA_CVO_ERROR", error);
    return json({ok:false,error:String((error as Error)?.message ?? error)},400);
  }
});
