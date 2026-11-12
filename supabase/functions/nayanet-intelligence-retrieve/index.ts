// nayanet-intelligence-retrieve — ONE contextual retrieval interface.
//
// A cold caller (zero prior context, no block IDs) supplies a free-text
// context query and receives RANKED Intelligent Blocks: keyword match +
// applicability + truth-state weighting + recency, with relationship-driven
// expansion (supersession chains, supporting edges, surfaced conflicts).
//
// This is the discovery path the cold-successor proof needs: the legacy
// cold proof fetched a HARDCODED block ID (lookup, not retrieval). A genuine
// cold Naya discovers; it does not already know.
//
// Auth: GitHub OIDC runtime identity (same pattern as
// nayanet-know-runtime / nayanet-cold-runtime-proof). Retrieval is read-only
// and never creates authority. A minimal receipt is recorded best-effort.

import { createRemoteJWKSet, jwtVerify } from "https://esm.sh/jose@6.0.10";
import { createClient } from "npm:@supabase/supabase-js@2";
import { expandRanked, type ScoredBlock } from "./retrieve.ts";
import { applyApplicabilityRanking } from "./retrieve_applicability.ts";

const ISSUER = "https://token.actions.githubusercontent.com";
const AUDIENCE = "nayanet-runtime";
const REPOSITORY = "SoulSchoolAcademy/NayaPOWER";
const REF = "refs/heads/main";

// Workflows allowed to mint the calling identity. Union of the proof-harness
// workflows that consume retrieval (know/prove/connect proofs + the
// supabase-runtime proof that runs the cold-successor check).
const WORKFLOWS = new Set([
  ".github/workflows/live-know-proof.yml",
  ".github/workflows/live-prove-proof.yml",
  ".github/workflows/live-connect-proof.yml",
  ".github/workflows/live-supabase-runtime-proof.yml",
]);

// Canonical organism owner (mirrors nayanet-know-runtime). Retrieval is
// owner-scoped; multi-tenant callers are future work, not silent scope.
const OWNER_ID = "adfdf0b8-5558-41d1-9fed-ec51abf4fe2f";
const PROJECT_ID = "NayaNET";

const JWKS = createRemoteJWKSet(
  new URL("https://token.actions.githubusercontent.com/.well-known/jwks"),
);

const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json", "cache-control": "no-store" },
  });

async function authenticate(req: Request) {
  const h = req.headers.get("authorization") ?? "";
  if (!h.startsWith("Bearer ")) throw new Error("RUNTIME_IDENTITY_REQUIRED");
  const { payload } = await jwtVerify(h.slice(7), JWKS, {
    issuer: ISSUER,
    audience: AUDIENCE,
  });
  const workflowRef = String(payload.workflow_ref ?? "");
  const expectedRefs = Array.from(WORKFLOWS).map(
    (w) => `${REPOSITORY}/${w}@${REF}`,
  );
  if (
    payload.repository !== REPOSITORY ||
    !expectedRefs.includes(workflowRef) ||
    payload.ref !== REF
  ) {
    throw new Error("WORKFLOW_BINDING_MISMATCH");
  }
  return { payload, workflowRef };
}

function adminClient() {
  const url = Deno.env.get("SUPABASE_URL");
  const key = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");
  if (!url || !key) throw new Error("SERVER_AUTH_CONFIG_MISSING");
  return createClient(url, key, { auth: { persistSession: false } });
}

type RetrieveBody = {
  mode?: string;
  query?: string;
  limit?: number;
  context?: Record<string, unknown>;
  include_related?: boolean;
  // THETA-NEXT-3: caller scope for the applicability ranking rule 3
  // (out-of-scope demotion). Optional; with no caller scope the rule is a
  // no-op and stale/unreviewed demotion still applies (contract §5).
  areas?: string[];
  task_contexts?: string[];
};

Deno.serve(async (req: Request) => {
  try {
    if (req.method === "GET") {
      return json({ ok: true, service: "nayanet-intelligence-retrieve", mode: "health" });
    }
    if (req.method !== "POST") return json({ ok: false, error: "METHOD_NOT_ALLOWED" }, 405);

    const { payload, workflowRef } = await authenticate(req);
    const body = (await req.json()) as RetrieveBody;
    if ((body.mode ?? "retrieve") !== "retrieve") {
      return json({ ok: false, error: "UNSUPPORTED_MODE" }, 400);
    }

    const query = typeof body.query === "string" ? body.query : "";
    const limit = Math.max(1, Math.min(Number(body.limit ?? 10) || 10, 50));
    const context =
      body.context && typeof body.context === "object" ? body.context : {};
    const includeRelated = body.include_related !== false;
    // THETA-NEXT-3: optional caller scope. Plain string arrays; anything
    // else is ignored (never a 400 — scope is advisory, not gating).
    const areas = Array.isArray(body.areas)
      ? body.areas.filter((s): s is string => typeof s === "string")
      : [];
    const taskContexts = Array.isArray(body.task_contexts)
      ? body.task_contexts.filter((s): s is string => typeof s === "string")
      : [];

    const admin = adminClient();

    // Ranked candidates from the search substrate (migration
    // 20261006235900_nayanet_cold_retrieve_search_v1).
    const { data, error } = await admin.rpc("nayanet_retrieve_blocks", {
      p_query: query,
      p_owner_id: OWNER_ID,
      p_limit: limit,
      p_context: context,
    });
    if (error) throw new Error(`RETRIEVE_RPC_FAILED: ${error.message}`);
    const candidates = (Array.isArray(data) ? data : []) as ScoredBlock[];

    // Relationship expansion (GAP C): supersession swap, supporting edges,
    // surfaced conflicts. Needs block-by-ID fetch for successor hops.
    const fetchBlock = async (blockId: string): Promise<ScoredBlock | null> => {
      const { data: rows, error: e } = await admin
        .from("nayanet_intelligent_blocks")
        .select(
          "intelligent_block_id,status,understanding_state,owner_scope,applicable_scope,content,connections,superseded_by_block_id,evidence_refs,provenance,updated_at",
        )
        .eq("intelligent_block_id", blockId)
        .eq("owner_id", OWNER_ID)
        .maybeSingle();
      if (e || !rows) return null;
      const r = rows as Record<string, unknown>;
      return {
        block_id: String(r.intelligent_block_id),
        status: String(r.status ?? ""),
        understanding_state: String(r.understanding_state ?? ""),
        owner_scope: String(r.owner_scope ?? ""),
        applicable_scope: r.applicable_scope,
        content: r.content,
        connections: (r.connections as ScoredBlock["connections"]) ?? null,
        superseded_by_block_id: r.superseded_by_block_id
          ? String(r.superseded_by_block_id)
          : null,
        evidence_refs: Array.isArray(r.evidence_refs) ? r.evidence_refs : [],
        provenance: r.provenance,
        updated_at: String(r.updated_at ?? ""),
        score: 0,
        score_breakdown: {},
        why: [],
      };
    };

    const now = new Date();

    // THETA-NEXT-1..4 — applicability ranking (the default flip:
    // matches-not-applies -> applies). final_score = base_match_score ×
    // multiplier (contract §3); superseded records resolve to their lineage
    // head and are never served as current (contract §3 rule 1, §4).
    //
    // Guardrails (contract §5, §8), all preserved:
    // - Base match scoring untouched: applicability multiplies, never replaces.
    // - Demoted records stay visible, only ranked lower.
    // - No caller scope -> rule 3 (out-of-scope) is a no-op; stale and
    //   unreviewed demotion still apply.
    // - The edge-level V2 gates from the canonical connect_selector applied
    //   first (inside expandBlock); this ranks what those gates admit.
    const { ranked, excluded } = await applyApplicabilityRanking(candidates, fetchBlock, {
      areas,
      taskContexts,
      now,
    });

    // Supersession is truth maintenance, not optional "related context".
    // Even when the caller opts out of related context/conflicts, the result
    // still resolves to the current successor rather than returning stale
    // intelligence. (Heads arrive pre-resolved from the ranking step; the
    // lineage walk below is a no-op for them and stays as defense in depth.)
    const expanded = await expandRanked(ranked, fetchBlock, now, includeRelated);

    // expandRanked nulls via_lineage for zero-hop heads; reattach the
    // lineage string the ranking step resolved (expandBlock's format).
    const rankedById = new Map(ranked.map((r) => [String(r.block_id), r]));
    const results = expanded.map((e) => {
      const src = rankedById.get(String(e.block_id));
      if (src && src.applicability_via_lineage.length > 0 && !e.via_lineage) {
        const last = src.applicability_via_lineage[src.applicability_via_lineage.length - 1];
        return { ...e, via_lineage: `SUPERSEDED_BY:${last}` };
      }
      return e;
    });

    // Best-effort receipt: retrieval evidence, never fails the call.
    let receipt: unknown = null;
    try {
      const { data: r } = await admin
        .from("nayanet_execution_receipts")
        .insert({
          user_id: OWNER_ID,
          project_id: PROJECT_ID,
          action: "intelligence_retrieval",
          status: "SUCCESS",
          expected_result:
            "Ranked Intelligent Blocks for a cold context query; retrieval creates no authority.",
          observed_result: `HIT:${results.length}`,
          evidence: {
            schema: "naya.retrieve.receipt.v1",
            node_id: "NAYA-KERNEL-KNOW",
            query: query.slice(0, 500),
            context,
            result_count: results.length,
            top_block_ids: results.slice(0, 5).map((x) => x.block_id),
            retrieval_creates_authority: false,
            runtime_identity: "naya-node-oidc",
            runtime_jti: (payload.jti as string) ?? null,
            workflow_ref: workflowRef,
            // Applicability v2.0 (THETA-NEXT-1..4): the ranking is explainable.
            applicability: {
              mode: "applies",
              requested_areas: areas,
              requested_contexts: taskContexts,
              ranked_count: ranked.length,
              excluded_count: excluded.length,
              excluded,
              top_adjustments: ranked.slice(0, 10).map((r) => ({
                block_id: r.block_id,
                base_score: r.applicability_base_score,
                multiplier: r.applicability_multiplier,
                final_score: r.final_score,
                reasons: r.applicability_reasons,
                via_lineage: r.applicability_via_lineage,
              })),
            },
          },
          learning: [],
        })
        .select("id")
        .single();
      receipt = r;
    } catch (e) {
      receipt = { receipt_failed: String((e as Error)?.message ?? e) };
    }

    return json({
      ok: true,
      status: results.length > 0 ? "RETRIEVED" : "NO_MATCH",
      node_id: "NAYA-KERNEL-KNOW",
      query: query.slice(0, 500),
      result_count: results.length,
      results,
      receipt,
      retrieval_creates_authority: false,
      handoff_to: "NAYA-KERNEL-PROVE",
    });
  } catch (e) {
    const msg = String((e as Error)?.message ?? e);
    const status =
      msg === "RUNTIME_IDENTITY_REQUIRED" || msg === "WORKFLOW_BINDING_MISMATCH"
        ? 401
        : 400;
    return json({ ok: false, error: msg }, status);
  }
});
