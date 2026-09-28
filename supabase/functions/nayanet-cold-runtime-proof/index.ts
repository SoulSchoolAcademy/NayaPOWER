import { createRemoteJWKSet, jwtVerify } from "https://esm.sh/jose@6.0.10";

const ISSUER = "https://token.actions.githubusercontent.com";
const AUDIENCE = "nayanet-runtime";
const REPOSITORY = "SoulSchoolAcademy/NayaPOWER";
const WORKFLOW = ".github/workflows/live-supabase-runtime-proof.yml";
const REF = "refs/heads/naya/node-genome-aaa-v1";
const NAYA_ID = "NAYA-NODE-0001";
const OWNER_ID = "adfdf0b8-5558-41d1-9fed-ec51abf4fe2f";
const BLOCK_ID = "IB-NAYA-NODE-0001-0001";
const JWKS = createRemoteJWKSet(new URL("https://token.actions.githubusercontent.com/.well-known/jwks"));

const json = (body: unknown, status = 200) => new Response(JSON.stringify(body), {
  status,
  headers: { "content-type": "application/json", "cache-control": "no-store" },
});

Deno.serve(async (req: Request) => {
  if (req.method !== "GET") return json({ error: "METHOD_NOT_ALLOWED" }, 405);
  const auth = req.headers.get("authorization") ?? "";
  if (!auth.startsWith("Bearer ")) return json({ error: "RUNTIME_IDENTITY_REQUIRED" }, 401);

  let payload: Record<string, unknown>;
  try {
    const verified = await jwtVerify(auth.slice(7), JWKS, { issuer: ISSUER, audience: AUDIENCE });
    payload = verified.payload as Record<string, unknown>;
  } catch (_error) {
    return json({ error: "GITHUB_OIDC_INVALID" }, 401);
  }

  const workflowRef = REPOSITORY + "/" + WORKFLOW + "@" + REF;
  if (payload.repository !== REPOSITORY || payload.workflow_ref !== workflowRef || payload.ref !== REF) {
    return json({ error: "WORKFLOW_BINDING_MISMATCH" }, 403);
  }

  const serviceRole = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");
  const supabaseUrl = Deno.env.get("SUPABASE_URL");
  if (!serviceRole || !supabaseUrl) return json({ error: "SERVER_AUTH_CONFIG_MISSING" }, 500);

  const headers = { apikey: serviceRole, Authorization: "Bearer " + serviceRole };
  const blockUrl = supabaseUrl + "/rest/v1/nayanet_intelligent_blocks?intelligent_block_id=eq." + encodeURIComponent(BLOCK_ID) + "&owner_id=eq." + OWNER_ID + "&select=*";
  const blockResponse = await fetch(blockUrl, { headers });
  if (!blockResponse.ok) return json({ error: "BLOCK_LOOKUP_FAILED", status: blockResponse.status }, 502);
  const blocks = await blockResponse.json();
  if (!Array.isArray(blocks) || blocks.length !== 1) return json({ error: "CANONICAL_BLOCK_NOT_UNIQUE", count: Array.isArray(blocks) ? blocks.length : 0 }, 409);

  const grantUrl = supabaseUrl + "/rest/v1/nayanet_authority_grants?issuer_id=eq." + OWNER_ID + "&subject_id=eq." + OWNER_ID + "&mission_id=eq.NAYA-NODE-0001-CONTINUITY&status=eq.ACTIVE&select=grant_id,actions,constraints,evidence";
  const grantResponse = await fetch(grantUrl, { headers });
  if (!grantResponse.ok) return json({ error: "AUTHORITY_LOOKUP_FAILED", status: grantResponse.status }, 502);
  const grants = await grantResponse.json();
  if (!Array.isArray(grants) || grants.length < 1) return json({ error: "CANONICAL_AUTHORITY_MISSING" }, 403);

  const block = blocks[0];
  const lesson = block.content?.lesson;
  if (typeof lesson !== "string" || !lesson) return json({ error: "RETAINED_LESSON_MISSING" }, 409);

  const behavior = lesson.includes("Preserve provenance before applying retained intelligence")
    ? "PRESERVE_PROVENANCE_BEFORE_APPLY"
    : "RETAINED_INTELLIGENCE_RETRIEVED";

  const receipt = {
    receipt_type: "NAYA-COLD-RUNTIME-RECEIPT-V1",
    naya_id: NAYA_ID,
    owner_id: OWNER_ID,
    runtime_identity: "github-actions-oidc",
    workflow_ref: workflowRef,
    block_id: BLOCK_ID,
    block_owner_id: block.owner_id,
    authority_grant_id: grants[0].grant_id,
    retained_lesson: lesson,
    behavior,
    source_evidence: block.evidence_refs,
    token_jti: payload.jti ?? null,
    verified_at: new Date().toISOString(),
  };
  return json({ ok: true, receipt });
});
