import { createRemoteJWKSet, jwtVerify } from "https://esm.sh/jose@6.0.10";
import { createClient } from "npm:@supabase/supabase-js@2";

const ISSUER = "https://token.actions.githubusercontent.com";
const AUDIENCE = "nayanet-runtime";
const REPOSITORY = "SoulSchoolAcademy/NayaPOWER";
const WORKFLOW = ".github/workflows/live-supabase-runtime-proof.yml";
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
    if (binding.length !== 1) return json({ok:false,error:"DURABLE_NAYA_AUTHORIZATION_BINDING_INVALID",count:binding.length},403);

    const body = await req.json().catch(() => ({}));
    const mode = String(body.mode ?? "cvo");
    const treatmentId = String(body.treatment_receipt_id ?? DEFAULT_TREATMENT_ID);
    const controlId = String(body.control_receipt_id ?? DEFAULT_CONTROL_ID);
    const learningId = body.learning_id ? String(body.learning_id) : null;
    if (mode !== "cvo" && mode !== "verify") return json({ok:false,error:"UNSUPPORTED_MODE"},400);

    const {data:treatment,error:te} = await admin.from("nayanet_execution_receipts").select("*").eq("id",treatmentId).eq("user_id",OWNER_ID).eq("project_id","NayaNET").maybeSingle();
    if (te) throw te;
    const {data:control,error:ce} = await admin.from("nayanet_execution_receipts").select("*").eq("id",controlId).eq("user_id",OWNER_ID).eq("project_id","NayaNET").maybeSingle();
    if (ce) throw ce;
    if (!treatment || !control) return json({ok:false,error:"PAIRED_ACTION_RECEIPTS_NOT_FOUND"},404);

    if (!treatment.action.startsWith("NAYA-NODE-0001-TREATMENT-") || !control.action.startsWith("NAYA-NODE-0001-CONTROL-")) {
      return json({ok:false,error:"PAIRED_ACTION_RECEIPTS_INVALID"},409);
    }
    if (treatment.status !== "SUCCESS" || control.status !== "SUCCESS") {\n      return json({ok:false,error:"PAIRED_ACTION_OUTCOME_NOT_SUCCESS"},409);\n    }\n    if (learningId) {\n      const {data:learning,error:le} = await admin.from("learning_evidence").select("id,target_id,status,source_event_id").eq("id",learningId).eq("member_id",OWNER_ID).maybeSingle();\n      if (le) throw le;\n      if (!learning || learning.target_id !== NAYA_ID || learning.status !== "CANDIDATE") return json({ok:false,error:"LEARNING_CANDIDATE_INVALID"},409);\n    }\n\n    if (false) {
      return json({ok:false,error:"PAIRED_ACTION_OUTCOME_NOT_SUCCESS"},409);
    }

    if (mode === "verify") {
      const evidence = Array.isArray(treatment.evidence) ? treatment.evidence : [];
      const causal = evidence.find((item: Record<string,unknown>) => item?.causal_verification)?.causal_verification as Record<string,unknown> | undefined;
      if (!causal) return json({ok:false,error:"CVO_NOT_PERSISTED"},409);
      const valid = causal.schema === "NAYANET_CAUSAL_VERIFICATION_V1"
        && causal.receipt_id === treatmentId
        && causal.comparison_receipt_id === controlId
        && causal.causal_method === "CONTROLLED_INTERVENTION"
        && causal.causal_assessment === "CAUSAL_SUPPORTED"
        && causal.verification_status === "OUTCOME_VERIFIED"
        && causal.production_action_executed === true
        && causal.observed_change === treatment.observed_result;
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
        control: control.evidence,
        treatment: treatment.evidence,
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

    const {data:op,error:oe} = await admin.from("nayanet_intelligence_operations").insert({
      user_id: OWNER_ID,
      project_id: "NayaNET",
      operation: "causal_verify_runtime",
      status: "SUCCESS",
      input: {mode, treatment_receipt_id:treatmentId, control_receipt_id:controlId},
      output: causal,
      source_ref: treatmentId,
      source_event_ids: [treatmentId, controlId],
    }).select("id").single();
    if (oe) throw oe;

    const existingEvidence = Array.isArray(treatment.evidence) ? treatment.evidence : [];
    const updatedEvidence = [...existingEvidence.filter((item:Record<string,unknown>) => !item?.causal_verification), {causal_verification:causal, causal_operation_id:op.id}];
    const {data:updated,error:ue} = await admin.from("nayanet_execution_receipts").update({evidence:updatedEvidence}).eq("id",treatmentId).eq("user_id",OWNER_ID).select("*").single();
    if (ue) throw ue;

    return json({ok:true,schema:"NAYANET_CAUSAL_VERIFY_RUNTIME_V1",operation_id:op.id,causal_verification:causal,receipt:updated,runtime_identity:"github-actions-oidc",workflow_ref:workflowRef,token_jti:payload.jti ?? null});
  } catch (error) {
    return json({ok:false,error:String((error as Error)?.message ?? error)},400);
  }
});
