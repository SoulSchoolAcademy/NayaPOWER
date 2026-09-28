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
    const learningId = String(body?.learning_id || "");
    if (!learningId) return json({ ok: false, error: "LEARNING_ID_REQUIRED" }, 400);

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
