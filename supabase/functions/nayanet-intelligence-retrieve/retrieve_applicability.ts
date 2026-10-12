// retrieve_applicability.ts — THETA-NEXT-1..4
//
// Applicability v2.0 consumer for the TS retrieval path (Naya Theta, Retrieval).
//
// Reference implementation (the spec): tools/applicability.py::rank_adjust +
// apply_ranking (Naya Beta, KNOW). Consumer contract:
// BRAIN/11-KNOWLEDGE/0005-APPLICABILITY-CONSUMER-CONTRACT-V1.md
//
// The rule in one sentence: retrieval returns what APPLIES, not just what
// matches. final_score = base_match_score × multiplier, with:
//   superseded → 0.0 (never served as current; resolve to the lineage head)
//   expired (valid_until < now) → ×0.1
//   caller named a scope and the record matches none → ×0.25
//   unreviewed tag → ×0.5 ; low confidence (<0.5) → ×0.8
//   unknown/missing metadata → fail closed (×0.5), never treated as fresh
//
// What this does NOT change (contract §5, §8):
// - Base match scoring is untouched: applicability multiplies, never replaces.
// - No new authority: demoted records stay visible, only ranked lower.
// - The edge-level V2 gates (status, temporal, consent, applicability) from
//   the canonical connect_selector still apply FIRST; this ranks what they admit.

import {
  isServableTarget,
  type FetchBlock,
  type ScoredBlock,
} from "./retrieve.ts";
import { SUPERSESSION_REGISTRY } from "./supersession_registry.ts";

// --- Contract constants (identical values to tools/applicability.py) ---------
export const MULT_SUPERSEDED = 0.0; // superseded record: never served as current
export const MULT_EXPIRED = 0.1; // valid_until < now: knowledge no longer applies
export const MULT_OUT_OF_SCOPE = 0.25; // caller named a scope; record matches none
export const MULT_UNREVIEWED = 0.5; // tag unreliable / metadata unknown: fail closed
export const MULT_LOW_CONFIDENCE = 0.8; // heuristic confidence below 0.5
export const MAX_SUPERSESSION_HOPS = 3;

// The 12 area codes from the consumer contract §2. Used to split the derived
// block-surface scope tokens into areas vs task_contexts (stamped v2 tags
// carry the split already and are honored verbatim).
export const AREA_CODES = new Set([
  "LEARN", "KNOW", "ACT", "LAW", "VERIFY", "BLOCKS", "DECISION",
  "RETRIEVAL", "SUCCESSOR", "TEAM", "INFRA", "HUMAN_VALUE",
]);

// --- Types -------------------------------------------------------------------
export type ApplicabilityFreshness = {
  valid_from: string | null;
  valid_until: string | null;
  ttl_days: number | null;
  assessed_at: string | null;
};

export type ApplicabilitySupersession = {
  superseded_by: string | null;
  supersedes: string[];
};

export type ApplicabilityTag = {
  areas: string[];
  task_contexts: string[];
  law_refs: string[];
  freshness: ApplicabilityFreshness;
  supersession: ApplicabilitySupersession;
  confidence: number | null;
  needs_review: boolean;
  source: string | null;
};

export type RankAdjustment = {
  servable: boolean;
  multiplier: number;
  reasons: string[];
};

export type RankedBlock = ScoredBlock & {
  // applicability_base_score: best base match score among the lineage
  // members aggregated at this head (contract §4). score stays the head's
  // own RPC score; final_score = applicability_base_score × multiplier.
  applicability_base_score: number;
  final_score: number;
  applicability_multiplier: number;
  applicability_reasons: string[];
  applicability_servable: boolean;
  applicability_via_lineage: string[];
};

// --- Date handling (mirrors tools/applicability.py::_parse_date) -------------
//
// Python: datetime.fromisoformat(str).date(), falling back to
// strptime(str[:10], "%Y-%m-%d").date(); garbage -> None. Comparison is
// day-granular (vu < now_d on date objects). This port works in UTC-midnight
// epoch millis so the comparison is identical for the contract's ISO inputs.
// Port note: ISO week-date / ordinal forms accepted by fromisoformat are not
// mirrored (never produced by the v2 producer); standard ISO forms are exact.
function parseApplicabilityDay(value: unknown): number | null {
  if (value === null || value === undefined) return null;
  const s = String(value).trim();
  if (!s) return null;
  const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(s);
  if (m) {
    const y = Number(m[1]);
    const mo = Number(m[2]);
    const d = Number(m[3]);
    if (mo >= 1 && mo <= 12 && d >= 1 && d <= 31) {
      const ms = Date.UTC(y, mo - 1, d);
      const c = new Date(ms);
      if (
        c.getUTCFullYear() === y &&
        c.getUTCMonth() === mo - 1 &&
        c.getUTCDate() === d
      ) {
        return ms;
      }
    }
    return null;
  }
  const t = Date.parse(s);
  if (!Number.isNaN(t)) {
    const dt = new Date(t);
    return Date.UTC(
      dt.getUTCFullYear(),
      dt.getUTCMonth(),
      dt.getUTCDate(),
    );
  }
  return null;
}

function dayStartUtc(d: Date): number {
  return Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate());
}

function round4(x: number): number {
  return Math.round(x * 10000) / 10000;
}

// --- rank_adjust: the contract's ranking rule, ported verbatim -------------
//
// For each candidate: final_score = base_match_score × multiplier.
// Returns { servable, multiplier, reasons }. Reasons strings match the
// reference implementation (e.g. "expired:2026-11-20", "out_of_scope",
// "superseded_by:IB-...") so demotions stay debuggable.
export function rankAdjust(
  tag: ApplicabilityTag | null | undefined,
  now: Date = new Date(),
  requestedAreas: string[] = [],
  requestedContexts: string[] = [],
): RankAdjustment {
  const reasons: string[] = [];
  let multiplier = 1.0;
  const servable = true;

  // Rule 5 — missing metadata is fail-closed. Unknown applicability is never
  // treated as fresh, in-scope, or current. (Early return, like the reference.)
  if (!tag || typeof tag !== "object") {
    return {
      servable: true,
      multiplier: MULT_UNREVIEWED,
      reasons: ["metadata_unknown:fail_closed"],
    };
  }

  // Rule 1 — supersession (hard). A superseded record is not current knowledge.
  // The consumer resolves to the lineage head instead of serving this record.
  const sup = tag.supersession ?? { superseded_by: null, supersedes: [] };
  if (sup.superseded_by) {
    return {
      servable: false,
      multiplier: MULT_SUPERSEDED,
      reasons: [`superseded_by:${sup.superseded_by}`],
    };
  }

  // Rule 2 — expired. valid_until=null means timeless: applicability ends only
  // via supersession, never by the clock.
  const vu = parseApplicabilityDay(tag.freshness?.valid_until ?? null);
  if (vu !== null && vu < dayStartUtc(now)) {
    multiplier *= MULT_EXPIRED;
    reasons.push(`expired:${String(tag.freshness?.valid_until)}`);
  }

  // Rule 3 — out of scope. Fires only when the caller named a scope; with no
  // caller scope this rule is a no-op (contract §5). The record still
  // surfaces (visibility beats silence) — it just cannot outrank in-scope
  // answers.
  const want = new Set<string>([...requestedAreas, ...requestedContexts]);
  if (want.size > 0) {
    const have = new Set<string>([...(tag.areas ?? []), ...(tag.task_contexts ?? [])]);
    let hit = false;
    for (const w of want) {
      if (have.has(w)) {
        hit = true;
        break;
      }
    }
    if (!hit) {
      multiplier *= MULT_OUT_OF_SCOPE;
      reasons.push("out_of_scope");
    }
  }

  // Rule 4 — unreviewed / low confidence. needs_review wins over confidence.
  if (tag.needs_review) {
    multiplier *= MULT_UNREVIEWED;
    reasons.push("unreviewed_tag");
  } else if (typeof tag.confidence === "number" && tag.confidence < 0.5) {
    multiplier *= MULT_LOW_CONFIDENCE;
    reasons.push(`low_confidence:${tag.confidence}`);
  }

  return { servable, multiplier: round4(multiplier), reasons };
}

// --- Block surface -> tag (THETA-NEXT-2: freshness into the read surface) ----
//
// Mapping onto the columns index.ts already selects (contract §2):
//   applicable_scope        ↔ areas + task_contexts
//   superseded_by_block_id  ↔ supersession.superseded_by
//   updated_at + provenance ↔ freshness (valid_until comes from
//                             provenance.applicability.freshness when stamped;
//                             there is no valid_until column yet — adding one
//                             is a DB migration, a protected gate, so the
//                             interim derives from provenance per the
//                             contract's "Theta's call" option)
// A full v2 stamp at provenance.applicability is honored verbatim when it
// carries the v2 shape; a malformed stamp is treated as unknown (fail closed),
// never as fresh.
function asStringArray(v: unknown): string[] {
  return Array.isArray(v) ? v.filter((x): x is string => typeof x === "string") : [];
}

function provenanceTag(provenance: unknown): ApplicabilityTag | null {
  if (!provenance || typeof provenance !== "object") return null;
  const app = (provenance as Record<string, unknown>).applicability;
  if (!app || typeof app !== "object") return null;
  const t = app as Record<string, unknown>;
  if (
    !Array.isArray(t.areas) ||
    typeof t.freshness !== "object" || t.freshness === null ||
    typeof t.supersession !== "object" || t.supersession === null
  ) {
    return null; // malformed stamp: unknown, fail closed
  }
  const fr = t.freshness as Record<string, unknown>;
  const su = t.supersession as Record<string, unknown>;
  const conf = t.confidence;
  return {
    areas: asStringArray(t.areas),
    task_contexts: asStringArray(t.task_contexts),
    law_refs: asStringArray(t.law_refs),
    freshness: {
      valid_from: typeof fr.valid_from === "string" ? fr.valid_from : null,
      valid_until: typeof fr.valid_until === "string" ? fr.valid_until : null,
      ttl_days: typeof fr.ttl_days === "number" ? fr.ttl_days : null,
      assessed_at: typeof fr.assessed_at === "string" ? fr.assessed_at : null,
    },
    supersession: {
      superseded_by:
        typeof su.superseded_by === "string" && su.superseded_by.trim()
          ? su.superseded_by.trim()
          : null,
      supersedes: asStringArray(su.supersedes),
    },
    confidence: typeof conf === "number" ? conf : null,
    needs_review: t.needs_review === true,
    source: typeof t.source === "string" ? t.source : "stamped:provenance",
  };
}

// The live applicable_scope column is a free-form key/value jsonb object
// (see migration 20261006235900: nayanet_applicability_match echoes context
// keys against it). The derived tag flattens its tokens; area codes split
// into areas, everything else into task_contexts.
function scopeTokens(scope: unknown): string[] {
  const out = new Set<string>();
  if (Array.isArray(scope)) {
    for (const v of scope) {
      if (typeof v === "string" && v.trim()) out.add(v.trim());
    }
    return [...out];
  }
  if (scope && typeof scope === "object") {
    for (const [k, v] of Object.entries(scope as Record<string, unknown>)) {
      if (typeof v === "string" && v.trim()) out.add(v.trim());
      else if (typeof v === "number" || typeof v === "boolean") out.add(String(v));
      if (k.trim()) out.add(k.trim());
    }
  }
  return [...out];
}

function supersededByOf(block: ScoredBlock): string | null {
  // THETA-NEXT-4: the durable home is the block lineage table
  // (superseded_by_block_id); the JSON registry is the interim source of
  // truth. The column wins when both speak.
  const col = typeof block.superseded_by_block_id === "string"
    ? block.superseded_by_block_id.trim()
    : "";
  if (col) return col;
  const reg = SUPERSESSION_REGISTRY[String(block.block_id)];
  return typeof reg === "string" && reg.trim() ? reg.trim() : null;
}

export function blockToApplicabilityTag(block: ScoredBlock): ApplicabilityTag | null {
  // 1. A stamped v2 tag in provenance wins — honor the KNOW-side stamps.
  const stamped = provenanceTag(block.provenance);
  if (stamped) return stamped;

  // 2. Otherwise derive from the block surface. A supersession link is itself
  //    applicability metadata (the record is not current); scope tokens feed
  //    rule 3. With neither, the block is unknown -> fail closed (null).
  const supersededBy = supersededByOf(block);
  const tokens = scopeTokens(block.applicable_scope);
  if (tokens.length === 0 && !supersededBy) return null;

  const areas: string[] = [];
  const contexts: string[] = [];
  for (const tok of tokens) {
    if (AREA_CODES.has(tok.toUpperCase())) areas.push(tok.toUpperCase());
    else contexts.push(tok);
  }
  return {
    areas,
    task_contexts: contexts,
    law_refs: [],
    freshness: {
      valid_from: typeof block.updated_at === "string" ? block.updated_at : null,
      valid_until: null, // no valid_until column yet (THETA-NEXT-2 interim)
      ttl_days: null,
      assessed_at: null,
    },
    supersession: { superseded_by: supersededBy, supersedes: [] },
    confidence: null,
    // No stamp, no review signal: the tag is unreliable by definition.
    // (Contract rule 4/5 — unknown is never treated as fresh.)
    needs_review: true,
    source: "derived:block-surface",
  };
}

// --- Supersession resolution (contract §4) -----------------------------------
//
// Follow superseded_by links, at most 3 hops, with a visited-set cycle guard
// (seeded with self so a cycle back to self stops). Stop early on a missing
// head and keep the last resolvable record. A chain that points at a
// non-servable head is a data bug: resolve to the deepest servable ancestor
// and let the caller emit reason "supersession_head_unservable".
export type HeadResolution = {
  head: ScoredBlock;
  lineage: string[];
  unservableStop: boolean;
};

export async function resolveSupersessionHead(
  block: ScoredBlock,
  byId: Map<string, ScoredBlock>,
  fetchBlock: FetchBlock,
  maxHops: number = MAX_SUPERSESSION_HOPS,
): Promise<HeadResolution> {
  const visited = new Set<string>([String(block.block_id)]);
  let current = block;
  const lineage: string[] = [];
  let unservableStop = false;
  for (let hop = 0; hop < maxHops; hop++) {
    const nextId = supersededByOf(current);
    if (!nextId || visited.has(nextId)) break;
    const next = byId.get(nextId) ?? (await fetchBlock(nextId));
    if (!next) break;
    visited.add(nextId);
    if (!isServableTarget(next)) {
      unservableStop = true;
      break;
    }
    lineage.push(nextId);
    current = next;
  }
  return { head: current, lineage, unservableStop };
}

// --- applyApplicabilityRanking: the ranking path -----------------------------
//
// Mirrors tools/applicability.py::apply_ranking: candidates aggregate at
// their supersession head (the head inherits the best base score among its
// lineage members and is ranked once — members are never ranked separately),
// the head's tag drives rank_adjust, and final_score = base × multiplier,
// sorted descending. Rows that are not servable (superseded, multiplier 0)
// are withheld from "current" and reported in `excluded` with their reasons
// so the call stays debuggable. Demoted-but-servable rows stay visible.
export type ApplicabilityRanking = {
  ranked: RankedBlock[];
  excluded: { block_id: string; reasons: string[] }[];
};

export async function applyApplicabilityRanking(
  blocks: ScoredBlock[],
  fetchBlock: FetchBlock,
  opts: { areas?: string[]; taskContexts?: string[]; now?: Date } = {},
): Promise<ApplicabilityRanking> {
  const now = opts.now ?? new Date();
  const areas = opts.areas ?? [];
  const taskContexts = opts.taskContexts ?? [];
  const byId = new Map<string, ScoredBlock>(
    blocks.map((b) => [String(b.block_id), b]),
  );

  type Agg = {
    head: ScoredBlock;
    base: number;
    lineage: string[];
    unservableStop: boolean;
  };
  const byHead = new Map<string, Agg>();
  for (const b of blocks) {
    const { head, lineage, unservableStop } = await resolveSupersessionHead(
      b,
      byId,
      fetchBlock,
    );
    const hid = String(head.block_id);
    let agg = byHead.get(hid);
    if (!agg) {
      agg = { head, base: 0, lineage: [], unservableStop: false };
      byHead.set(hid, agg);
    }
    const base = typeof b.score === "number" && Number.isFinite(b.score) ? b.score : 0;
    if (base > agg.base) agg.base = base;
    for (const l of lineage) {
      if (!agg.lineage.includes(l)) agg.lineage.push(l);
    }
    agg.unservableStop = agg.unservableStop || unservableStop;
  }

  const ranked: RankedBlock[] = [];
  const excluded: { block_id: string; reasons: string[] }[] = [];
  for (const [hid, agg] of byHead) {
    const tag = blockToApplicabilityTag(agg.head);
    const adj = rankAdjust(tag, now, areas, taskContexts);
    const reasons = [...adj.reasons];
    if (agg.unservableStop && !reasons.includes("supersession_head_unservable")) {
      reasons.push("supersession_head_unservable");
    }
    if (!adj.servable || adj.multiplier <= 0) {
      excluded.push({ block_id: hid, reasons });
      continue;
    }
    const breakdown = {
      ...(agg.head.score_breakdown ?? {}),
      applicability_multiplier: adj.multiplier,
    };
    ranked.push({
      ...agg.head,
      applicability_base_score: round4(agg.base),
      final_score: round4(agg.base * adj.multiplier),
      applicability_multiplier: adj.multiplier,
      applicability_reasons: reasons,
      applicability_servable: adj.servable,
      applicability_via_lineage: agg.lineage,
      score_breakdown: breakdown,
      why: [
        ...agg.head.why,
        ...reasons.map((r) => `applicability:${r}`),
      ],
    });
  }
  ranked.sort(
    (a, b) =>
      b.final_score - a.final_score ||
      (a.block_id < b.block_id ? -1 : a.block_id > b.block_id ? 1 : 0),
  );
  return { ranked, excluded };
}
