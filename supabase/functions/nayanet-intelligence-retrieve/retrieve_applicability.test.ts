// Behavior matrix for the applicability v2.0 retrieval port (THETA-NEXT-1..4).
// IMPORTS THE SHIPPED MODULE — this test executes the real port code
// (retrieve_applicability.ts), not a mirror. Any behavior change must update
// this matrix.
//
// Contract: BRAIN/11-KNOWLEDGE/0005-APPLICABILITY-CONSUMER-CONTRACT-V1.md
// (Naya Beta, KNOW). Reference: tools/applicability.py::rank_adjust /
// apply_ranking. The TestRankingReference vectors below are named after
// tests/test_applicability_v2.py::TestRankingReference and must reproduce
// its multipliers verbatim (0.1 / 0.25 / 0.5 / 0.8 / 0.0).

import {
  applyApplicabilityRanking,
  blockToApplicabilityTag,
  rankAdjust,
  resolveSupersessionHead,
  MULT_EXPIRED,
  MULT_LOW_CONFIDENCE,
  MULT_OUT_OF_SCOPE,
  MULT_SUPERSEDED,
  MULT_UNREVIEWED,
  type ApplicabilityTag,
} from "./retrieve_applicability.ts";
import type { ScoredBlock } from "./retrieve.ts";

const NOW = new Date("2026-10-12T00:00:00Z");

function check(name: string, actual: unknown, expected: unknown): void {
  const a = JSON.stringify(actual);
  const e = JSON.stringify(expected);
  if (a !== e) throw new Error(`MATRIX FAIL [${name}]: expected ${e}, got ${a}`);
}

// A v2-shaped tag, like tools/applicability.py::produce() emits for a fresh
// CANDIDATE entry (valid_until a year out), with the heuristic ladder pinned.
function tag(overrides: Partial<ApplicabilityTag> = {}): ApplicabilityTag {
  return {
    areas: ["DECISION"],
    task_contexts: ["dispatch"],
    law_refs: [],
    freshness: {
      valid_from: "2026-10-01",
      valid_until: "2027-10-01",
      ttl_days: 365,
      assessed_at: "2026-10-12T00:00:00+00:00",
    },
    supersession: { superseded_by: null, supersedes: [] },
    confidence: 0.9,
    needs_review: false,
    source: "heuristic",
    ...overrides,
  };
}

// A servable ranked block as the nayanet_retrieve_blocks RPC returns it.
function block(
  id: string,
  overrides: Partial<ScoredBlock> = {},
): ScoredBlock {
  return {
    block_id: id,
    status: "ACTIVE",
    understanding_state: "VERIFIED",
    owner_scope: "TEAM",
    applicable_scope: null,
    content: { lesson: `lesson ${id}` },
    connections: null,
    superseded_by_block_id: null,
    evidence_refs: ["ev-1"],
    provenance: {},
    updated_at: "2026-10-01T00:00:00Z",
    score: 1.0,
    score_breakdown: {},
    why: [],
    ...overrides,
  };
}

function fetchFor(byId: Map<string, ScoredBlock>) {
  return (blockId: string): Promise<ScoredBlock | null> =>
    Promise.resolve(byId.get(blockId) ?? null);
}

// --- Contract vectors: TestRankingReference, reproduced verbatim ----------

Deno.test("vector — fresh in scope: full score", () => {
  const adj = rankAdjust(tag(), NOW, ["DECISION"], []);
  check("servable", adj.servable, true);
  check("multiplier", adj.multiplier, 1.0);
});

Deno.test("vector — expired demotes hard", () => {
  const t = tag();
  t.freshness.valid_until = "2026-01-01";
  const adj = rankAdjust(t, NOW);
  check("multiplier", adj.multiplier, MULT_EXPIRED);
  check("multiplier==0.1", adj.multiplier, 0.1);
  check(
    "reason",
    adj.reasons.some((r) => r.startsWith("expired:")),
    true,
  );
});

Deno.test("vector — timeless never expires", () => {
  const t = tag();
  t.freshness.valid_until = null; // timeless: ends only via supersession
  const adj = rankAdjust(t, new Date("2030-01-01T00:00:00Z"));
  check("multiplier", adj.multiplier, 1.0);
});

Deno.test("vector — out of scope demotes", () => {
  const t = tag({ areas: ["LEARN"], task_contexts: [] });
  const adj = rankAdjust(t, NOW, ["DECISION"], []);
  check("multiplier", adj.multiplier, MULT_OUT_OF_SCOPE);
  check("multiplier==0.25", adj.multiplier, 0.25);
  check("reason", adj.reasons.includes("out_of_scope"), true);
});

Deno.test("vector — no caller scope: no out-of-scope penalty", () => {
  const t = tag({ areas: ["LEARN"] });
  const adj = rankAdjust(t, NOW);
  check("multiplier", adj.multiplier, 1.0);
});

Deno.test("vector — unknown metadata fails closed", () => {
  const adj = rankAdjust(null, NOW);
  check("multiplier", adj.multiplier, MULT_UNREVIEWED);
  check("multiplier==0.5", adj.multiplier, 0.5);
  check("reason", adj.reasons.includes("metadata_unknown:fail_closed"), true);
  check("servable", adj.servable, true); // fail-closed still serves, demoted
});

Deno.test("vector — unreviewed tag demotes", () => {
  const t = tag({ needs_review: true, areas: [], task_contexts: [] });
  const adj = rankAdjust(t, NOW);
  check("multiplier", adj.multiplier, MULT_UNREVIEWED);
  check("multiplier==0.5", adj.multiplier, 0.5);
});

Deno.test("vector — low confidence demotes", () => {
  const t = tag({ confidence: 0.3 });
  const adj = rankAdjust(t, NOW);
  check("multiplier", adj.multiplier, MULT_LOW_CONFIDENCE);
  check("multiplier==0.8", adj.multiplier, 0.8);
});

Deno.test("vector — superseded never served as current", () => {
  const t = tag({
    supersession: { superseded_by: "IB-TEST-2", supersedes: [] },
  });
  const adj = rankAdjust(t, NOW);
  check("servable", adj.servable, false);
  check("multiplier", adj.multiplier, MULT_SUPERSEDED);
  check("multiplier==0.0", adj.multiplier, 0.0);
  check("reason", adj.reasons.includes("superseded_by:IB-TEST-2"), true);
});

Deno.test("vector — supersession wins over every other rule", () => {
  const t = tag({
    supersession: { superseded_by: "IB-TEST-2", supersedes: [] },
    needs_review: true,
    confidence: 0.1,
  });
  t.freshness.valid_until = "2020-01-01";
  const adj = rankAdjust(t, NOW, ["SOME-OTHER-AREA"], []);
  check("servable", adj.servable, false);
  check("multiplier", adj.multiplier, 0.0);
  check("single reason", adj.reasons, ["superseded_by:IB-TEST-2"]);
});

Deno.test("vector — expiry is day-granular: valid_until == today is not expired", () => {
  const t = tag();
  t.freshness.valid_until = "2026-10-12";
  const adj = rankAdjust(t, NOW);
  check("multiplier", adj.multiplier, 1.0);
});

Deno.test("vector — garbage valid_until never expires (fail open on the clock only)", () => {
  const t = tag();
  t.freshness.valid_until = "not-a-date";
  const adj = rankAdjust(t, NOW);
  check("multiplier", adj.multiplier, 1.0);
});

// --- Supersession resolution (contract §4) ---------------------------------

Deno.test("lineage — two-hop chain resolves to the head", async () => {
  const a = block("IB-A", { superseded_by_block_id: "IB-B" });
  const b = block("IB-B", { superseded_by_block_id: "IB-C" });
  const c = block("IB-C");
  const byId = new Map([["IB-A", a], ["IB-B", b], ["IB-C", c]]);
  const { head, lineage } = await resolveSupersessionHead(a, byId, fetchFor(byId));
  check("head", head.block_id, "IB-C");
  check("lineage", lineage, ["IB-B", "IB-C"]);
});

Deno.test("lineage — cycle stops before looping", async () => {
  const a = block("IB-A", { superseded_by_block_id: "IB-B" });
  const b = block("IB-B", { superseded_by_block_id: "IB-A" });
  const byId = new Map([["IB-A", a], ["IB-B", b]]);
  const { head, lineage } = await resolveSupersessionHead(a, byId, fetchFor(byId));
  check("lineage", lineage, ["IB-B"]); // stops before looping
  check("head", head.block_id, "IB-B");
});

Deno.test("lineage — missing head stops at the last resolvable record", async () => {
  const a = block("IB-A", { superseded_by_block_id: "IB-GHOST" });
  const byId = new Map([["IB-A", a]]);
  const { head, lineage } = await resolveSupersessionHead(a, byId, fetchFor(byId));
  check("lineage", lineage, []);
  check("head", head.block_id, "IB-A");
});

Deno.test("lineage — hop cap is 3", async () => {
  const mk = (id: string, next: string | null) =>
    block(id, { superseded_by_block_id: next });
  const bs = [mk("IB-1", "IB-2"), mk("IB-2", "IB-3"), mk("IB-3", "IB-4"), mk("IB-4", "IB-5"), mk("IB-5", null)];
  const byId = new Map(bs.map((b) => [b.block_id, b]));
  const { head, lineage } = await resolveSupersessionHead(bs[0], byId, fetchFor(byId));
  check("lineage length capped", lineage.length, 3);
  check("head", head.block_id, "IB-4");
});

Deno.test("lineage — non-servable head resolves to deepest servable ancestor", async () => {
  const a = block("IB-A", { superseded_by_block_id: "IB-B" });
  const b = block("IB-B", { status: "ARCHIVED" }); // not a servable target
  const byId = new Map([["IB-A", a], ["IB-B", b]]);
  const { head, lineage, unservableStop } = await resolveSupersessionHead(
    a,
    byId,
    fetchFor(byId),
  );
  check("head", head.block_id, "IB-A");
  check("lineage", lineage, []);
  check("unservableStop", unservableStop, true);
});

// --- applyApplicabilityRanking: aggregation + ordering ----------------------

Deno.test("ranking — aggregates at the head; members never ranked separately", async () => {
  const a = block("IB-A", { superseded_by_block_id: "IB-B", score: 2.0 });
  const b = block("IB-B", { score: 1.0 });
  const byId = new Map([["IB-A", a], ["IB-B", b]]);
  const { ranked, excluded } = await applyApplicabilityRanking(
    [a, b],
    fetchFor(byId),
    { now: NOW },
  );
  check("one row", ranked.length, 1);
  check("head id", ranked[0].block_id, "IB-B");
  check("head inherits best member base", ranked[0].applicability_base_score, 2.0);
  check("final = base × multiplier", ranked[0].final_score, 1.0); // 2.0 × 0.5 fail-closed
  check("via lineage", ranked[0].applicability_via_lineage, ["IB-B"]);
  check("nothing excluded", excluded.length, 0);
});

Deno.test("ranking — expired ranks below an otherwise-identical fresh record", async () => {
  const fresh = block("IB-FRESH", {
    score: 1.0,
    provenance: {
      applicability: {
        areas: ["DECISION"],
        task_contexts: [],
        law_refs: [],
        freshness: { valid_from: "2026-10-01", valid_until: "2027-10-01", ttl_days: 365, assessed_at: null },
        supersession: { superseded_by: null, supersedes: [] },
        confidence: 0.9,
        needs_review: false,
        source: "stamped",
      },
    },
  });
  const stale = block("IB-STALE", {
    score: 1.0,
    provenance: {
      applicability: {
        areas: ["DECISION"],
        task_contexts: [],
        law_refs: [],
        freshness: { valid_from: "2025-01-01", valid_until: "2026-01-01", ttl_days: 365, assessed_at: null },
        supersession: { superseded_by: null, supersedes: [] },
        confidence: 0.9,
        needs_review: false,
        source: "stamped",
      },
    },
  });
  const byId = new Map([["IB-FRESH", fresh], ["IB-STALE", stale]]);
  const { ranked } = await applyApplicabilityRanking([stale, fresh], fetchFor(byId), { now: NOW });
  check("order", ranked.map((r) => r.block_id), ["IB-FRESH", "IB-STALE"]);
  check("fresh final", ranked[0].final_score, 1.0);
  check("stale final", ranked[1].final_score, 0.1);
  check(
    "stale reason",
    ranked[1].applicability_reasons.some((r) => r.startsWith("expired:")),
    true,
  );
});

Deno.test("ranking — unstamped corpus: order preserved, uniform fail-closed, nothing lost", async () => {
  const bs = [
    block("IB-1", { score: 3.0 }),
    block("IB-2", { score: 2.0 }),
    block("IB-3", { score: 1.0 }),
  ];
  const byId = new Map(bs.map((b) => [b.block_id, b]));
  const { ranked, excluded } = await applyApplicabilityRanking(bs, fetchFor(byId), { now: NOW });
  // Every block is unknown -> ×0.5 uniformly: the flip cannot silently
  // reorder a corpus that carries no applicability signal.
  check("order preserved", ranked.map((r) => r.block_id), ["IB-1", "IB-2", "IB-3"]);
  check("uniform multiplier", ranked.map((r) => r.applicability_multiplier), [0.5, 0.5, 0.5]);
  check("finals", ranked.map((r) => r.final_score), [1.5, 1.0, 0.5]);
  check("nothing excluded", excluded.length, 0);
  check(
    "fail-closed reasons",
    ranked.every((r) => r.applicability_reasons.includes("metadata_unknown:fail_closed")),
    true,
  );
});

Deno.test("ranking — base scoring untouched: final is exactly base × multiplier", async () => {
  const b = block("IB-1", { score: 2.3456 });
  const byId = new Map([["IB-1", b]]);
  const { ranked } = await applyApplicabilityRanking([b], fetchFor(byId), {
    now: NOW,
    areas: ["DECISION"],
  });
  // Unstamped + caller scope: fail-closed 0.5 only (rule 3 needs a tag to
  // judge scope against; unknown scope is not judged out-of-scope).
  check("final", ranked[0].final_score, 1.1728);
  check("base preserved on score", ranked[0].score, 2.3456);
});

Deno.test("ranking — caller scope demotes out-of-scope, keeps in-scope", async () => {
  const mk = (id: string, areas: string[]) =>
    block(id, {
      score: 1.0,
      applicable_scope: Object.fromEntries(areas.map((a) => [a.toLowerCase(), a])),
    });
  const inScope = mk("IB-IN", ["DECISION"]);
  const outScope = mk("IB-OUT", ["LEARN"]);
  const byId = new Map([["IB-IN", inScope], ["IB-OUT", outScope]]);
  const { ranked } = await applyApplicabilityRanking([outScope, inScope], fetchFor(byId), {
    now: NOW,
    areas: ["DECISION"],
  });
  check("order", ranked.map((r) => r.block_id), ["IB-IN", "IB-OUT"]);
  check("in-scope multiplier", ranked[0].applicability_multiplier, 0.5); // derived tag: needs_review
  check("out-of-scope multiplier", ranked[1].applicability_multiplier, 0.125); // 0.5 × 0.25
  check(
    "out-of-scope reason",
    ranked[1].applicability_reasons.includes("out_of_scope"),
    true,
  );
});

Deno.test("ranking — superseded member excluded, head served once with lineage", async () => {
  const old = block("IB-OLD", { superseded_by_block_id: "IB-NEW", score: 5.0 });
  const cur = block("IB-NEW", { score: 1.0 });
  const byId = new Map([["IB-OLD", old], ["IB-NEW", cur]]);
  const { ranked, excluded } = await applyApplicabilityRanking([old, cur], fetchFor(byId), { now: NOW });
  check("one row", ranked.length, 1);
  check("head served", ranked[0].block_id, "IB-NEW");
  check("head base", ranked[0].applicability_base_score, 5.0); // best member base
  check("head final", ranked[0].final_score, 2.5); // 5.0 × 0.5 fail-closed
  check("via lineage", ranked[0].applicability_via_lineage, ["IB-NEW"]);
  check("nothing excluded (member folded into head)", excluded.length, 0);
});

Deno.test("ranking — ghost supersession chain is withheld from current, with reasons", async () => {
  const a = block("IB-A", { superseded_by_block_id: "IB-GHOST", score: 4.0 });
  const byId = new Map([["IB-A", a]]);
  const { ranked, excluded } = await applyApplicabilityRanking([a], fetchFor(byId), { now: NOW });
  check("withheld", ranked.length, 0);
  check("excluded", excluded.map((e) => e.block_id), ["IB-A"]);
  check(
    "reason",
    excluded[0].reasons.some((r) => r.startsWith("superseded_by:")),
    true,
  );
});

// --- blockToApplicabilityTag: read-surface mapping (THETA-NEXT-2) ------------

Deno.test("tag mapping — stamped v2 tag in provenance honored verbatim", () => {
  const stamped = {
    areas: ["HUMAN_VALUE"],
    task_contexts: ["briefing"],
    law_refs: ["SN-0522"],
    freshness: { valid_from: "2026-01-01", valid_until: null, ttl_days: null, assessed_at: "2026-10-12" },
    supersession: { superseded_by: null, supersedes: [] },
    confidence: 1.0,
    needs_review: false,
    source: "manual",
  };
  const b = block("IB-1", { provenance: { applicability: stamped } });
  const t = blockToApplicabilityTag(b);
  check("areas", t?.areas, ["HUMAN_VALUE"]);
  check("needs_review", t?.needs_review, false);
  check("confidence", t?.confidence, 1.0);
});

Deno.test("tag mapping — malformed stamp fails closed, never fresh", () => {
  const b = block("IB-1", { provenance: { applicability: { areas: "oops" } } });
  check("tag", blockToApplicabilityTag(b), null);
  const adj = rankAdjust(blockToApplicabilityTag(b), NOW);
  check("multiplier", adj.multiplier, 0.5);
});

Deno.test("tag mapping — db superseded_by column feeds rule 1", () => {
  const b = block("IB-1", { superseded_by_block_id: "IB-2" });
  const t = blockToApplicabilityTag(b);
  check("superseded_by", t?.supersession.superseded_by, "IB-2");
  const adj = rankAdjust(t, NOW);
  check("servable", adj.servable, false);
  check("multiplier", adj.multiplier, 0.0);
});
