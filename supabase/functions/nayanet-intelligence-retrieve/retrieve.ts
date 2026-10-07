// nayanet-intelligence-retrieve / retrieve.ts
//
// Relationship-driven retrieval expansion (GAP C).
//
// IMPORTANT: Graph V2 admission reuses the CONNECT-owned canonical edge
// selector (supabase/functions/_shared/connect_selector.ts) instead of
// inventing a second status/time/consent/applicability policy. Retrieval
// may route context; it never creates authority.

import { selectableConnections } from "../_shared/connect_selector.ts";

export type ScoredBlock = {
  block_id: string;
  status: string;
  understanding_state: string;
  owner_scope: string;
  applicable_scope: unknown;
  content: unknown;
  connections: BlockConnection[] | null;
  superseded_by_block_id: string | null;
  evidence_refs: unknown[];
  provenance: unknown;
  updated_at: string;
  score: number;
  score_breakdown: Record<string, number>;
  why: string[];
};

export type BlockConnection = {
  target_block_id?: string | null;
  relationship_type?: string | null;
  relationship_id?: string | null;
  supersedes_relationship_id?: string | null;
  status?: string | null;
  epistemic_state?: string | null;
  valid_from?: string | null;
  valid_until?: string | null;
  visibility?: string | null;
  consent_ref?: string | null;
  applicability?: {
    state?: string | null;
    task_classes?: unknown;
    limitations?: unknown;
  } | null;
};

export type RelatedContextEntry = {
  block_id: string;
  relationship_type: string;
  epistemic_state: string | null;
  why_admitted: string;
};

export type ConflictEntry = {
  block_id: string;
  relationship_type: string;
  epistemic_state: string | null;
  note: string;
};

export type ExpandedBlock = ScoredBlock & {
  via_lineage: string | null;
  related_context: RelatedContextEntry[];
  conflicts: ConflictEntry[];
};

// FetchBlock: the block-fetch callback expandBlock/expandRanked resolve
// supersession lineage through. Type-only (erased at runtime); declared so
// the edge type-check gate stays green. Shape matches the index.ts caller.
export type FetchBlock = (blockId: string) => Promise<ScoredBlock | null>;

// Retrieval-local admission sets. Edge-level V2 gates (status, temporal,
// consent, applicability) come from the canonical selector above; these sets
// decide which admitted relationship types attach context vs surface
// conflict, and which block states are servable as retrieval targets.
const CONTEXT_EDGE_ALLOWLIST = new Set([
  "SUPPORTS", "REFINES", "CONTEXTUALIZES", "VERIFIED_BY", "DERIVED_FROM",
  "APPLIES_TO", "CORRECTS", "LEARNED_FROM", "ENABLES", "PRODUCES",
]);

const CONFLICT_EDGE_TYPES = new Set(["CONTRADICTS", "INVALIDATES"]);
const SERVABLE_STATUS = new Set(["ACTIVE", "DURABLE", "RELEASED"]);
const SERVABLE_STATES = new Set(["VERIFIED", "DISTILLED", "APPLIED", "LEARNED"]);
const MAX_RELATED = 5;
const MAX_SUPERSESSION_HOPS = 3;

function isServableTarget(block: ScoredBlock | null): block is ScoredBlock {
  if (!block) return false;
  if (!SERVABLE_STATUS.has(String(block.status ?? "").toUpperCase())) return false;
  if (!SERVABLE_STATES.has(String(block.understanding_state ?? "").toUpperCase())) return false;
  if (!block.provenance || typeof block.provenance !== "object") return false;
  if (!Array.isArray(block.evidence_refs) || block.evidence_refs.length === 0) return false;
  return true;
}

/**
 * Expand one scored block:
 *  1. ALWAYS resolve block-level supersession to the current servable head.
 *  2. Optionally attach Graph-V2-admitted supporting context.
 *  3. Optionally surface Graph-V2-admitted conflicts, never merge them.
 *
 * "includeRelated" controls only steps 2-3. It may not disable step 1,
 * because returning a known superseded block as current would be a truth bug.
 */
export async function expandBlock(
  block: ScoredBlock,
  fetchBlock: FetchBlock,
  now = new Date(),
  includeRelated = true,
): Promise<ExpandedBlock> {
  const nowMs = now.getTime();
  let current = block;
  let via_lineage: string | null = null;
  const visited = new Set<string>([String(block.block_id)]);

  for (let hop = 0; hop < MAX_SUPERSESSION_HOPS; hop++) {
    const nextId = String(current.superseded_by_block_id ?? "").trim();
    if (!nextId || visited.has(nextId)) break;
    const next = await fetchBlock(nextId);
    if (!isServableTarget(next)) break;
    visited.add(nextId);
    via_lineage = `SUPERSEDED_BY:${nextId}`;
    current = {
      ...next,
      why: [...next.why, `lineage_successor_of:${block.block_id}`],
    };
  }

  const related_context: RelatedContextEntry[] = [];
  const conflicts: ConflictEntry[] = [];
  if (!includeRelated) {
    return { ...current, via_lineage, related_context, conflicts };
  }

  const seen = new Set<string>();
  for (const c of selectableConnections(current, nowMs)) {
    const t = String(c.relationship_type);
    const targetId = String(c.target_block_id);
    if (!targetId || targetId === current.block_id || seen.has(targetId)) continue;
    if (!CONFLICT_EDGE_TYPES.has(t) && !CONTEXT_EDGE_ALLOWLIST.has(t)) continue;

    const target = await fetchBlock(targetId);
    if (!isServableTarget(target)) continue;
    seen.add(targetId);

    if (CONFLICT_EDGE_TYPES.has(t)) {
      conflicts.push({
        block_id: targetId,
        relationship_type: t,
        epistemic_state: c.epistemic_state ?? null,
        note: "surfaced, not merged: disagreement is visible, never silently applied",
      });
      continue;
    }
    if (related_context.length < MAX_RELATED) {
      related_context.push({
        block_id: targetId,
        relationship_type: t,
        epistemic_state: c.epistemic_state ?? null,
        why_admitted: `edge:${t}`,
      });
    }
  }

  return { ...current, via_lineage, related_context, conflicts };
}

export async function expandRanked(
  blocks: ScoredBlock[],
  fetchBlock: FetchBlock,
  now = new Date(),
  includeRelated = true,
): Promise<ExpandedBlock[]> {
  const out: ExpandedBlock[] = [];
  for (const b of blocks) out.push(await expandBlock(b, fetchBlock, now, includeRelated));
  return out;
}
