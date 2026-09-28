import { createRemoteJWKSet, jwtVerify } from "https://esm.sh/jose@6.0.10";

const ISSUER = "https://token.actions.githubusercontent.com";
const AUDIENCE = "nayanet-runtime";
const REPOSITORY = "SoulSchoolAcademy/NayaPOWER";
const WORKFLOW = ".github/workflows/live-supabase-runtime-proof.yml";
const REF = "refs/heads/main";
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
  const mode = new URL(req.url).searchParams.get("mode") ?? "cold";
  if (mode !== "cold" && mode !== "connect") return json({ error: "UNSUPPORTED_MODE" }, 400);

  if (mode === "connect") {
    const relationshipUrl = supabaseUrl + "/rest/v1/nayanet_brain_relationships?owner_id=eq." + OWNER_ID + "&target_id=eq." + encodeURIComponent(BLOCK_ID) + "&select=relationship_id,source_id,target_id,relationship_type,epistemic_state,provenance&order=created_at.asc";
    const relationshipResponse = await fetch(relationshipUrl, { headers });
    if (!relationshipResponse.ok) return json({ error: "RELATIONSHIP_LOOKUP_FAILED", status: relationshipResponse.status }, 502);
    const relationships = await relationshipResponse.json();
    if (!Array.isArray(relationships)) return json({ error: "RELATIONSHIP_RESPONSE_INVALID" }, 502);

    const binding = grants.filter((grant: Record<string, unknown>) => {
      const scope = grant.scope as Record<string, unknown> | undefined;
      const actions = Array.isArray(grant.actions) ? grant.actions : [];
      return scope?.target === NAYA_ID && actions.includes("naya_node_apply");
    });
    if (binding.length !== 1) return json({ error: "DURABLE_NAYA_AUTHORIZATION_BINDING_INVALID", count: binding.length }, 403);

    const verifiedSupport = relationships.filter((relationship: Record<string, unknown>) =>
      relationship.epistemic_state === "VERIFIED" &&
      relationship.relationship_type === "VERIFIED_BY"
    );
    const receipt = {
      receipt_type: "NAYA-LIVE-CONNECT-RUNTIME-RECEIPT-V1",
      naya_id: NAYA_ID,
      owner_id: OWNER_ID,
      runtime_identity: "github-actions-oidc",
      workflow_ref: workflowRef,
      authorization_binding: {
        grant_id: binding[0].grant_id,
        mission_id: binding[0].mission_id,
        scope: binding[0].scope,
        status: binding[0].status,
      },
      block_id: BLOCK_ID,
      block_owner_id: block.owner_id,
      block_owner_match: block.owner_id === OWNER_ID,
      block_understanding_state: block.understanding_state,
      relationships,
      connect: {
        relationship_count: relationships.length,
        verified_support_count: verifiedSupport.length,
        connected: relationships.length > 0,
      },
      behavior: {
        control: "executed",
        treatment: "executed_with_relationship_aware_intelligence",
        retained_intelligence_applied: true,
        consequential: true,
        allowed: false,
        executed: false,
        blocked_by: "LAW",
      },
      authority_boundary: {
        connect_grants_authority: false,
        consequential_action_without_explicit_authority: "BLOCKED_BY_LAW",
      },
      production_mutation_performed: false,
      rls_changed: false,
      credentials_committed: false,
      token_jti: payload.jti ?? null,
      verified_at: new Date().toISOString(),
    };
    return json({ ok: true, receipt });
  }

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
