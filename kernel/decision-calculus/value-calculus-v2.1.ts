/**
 * Decision Value Calculus V2.1 — deterministic reference implementation.
 *
 * Working spec: GitHub Issue #1182
 *   - "DIRECTOR-APPROVED DIRECTION — Decision Value Calculus V2.1 baseline candidate"
 *     (comment 5921148872, 2026-09-30T22:57:11Z)
 *   - "V2.1 patch — R1–R6 definitions" (comment 5921158459, 2026-09-30T22:58:03Z)
 *
 * Status: CANDIDATE, NOT RATIFIED. Not production-proven. OFFICIAL DIRECTION only.
 * Supersedes: value-calculus-v2.ts (PVAF) — specifically removes PV from Q (the
 *   rejected coupling), replaces absolute winner separation with relative dominance,
 *   and implements four-valued gates, baseline-relative ΔV, Pareto selection,
 *   evidence floors, provisional verification, and typed SmartLedger receipts.
 * Lineage: kernel/value_calculus.py (V1, NAYANODE/0025) remains untouched; this is
 *   the candidate successor, not a silent replacement.
 *
 * Pure functions only: no I/O, no side effects, deterministic.
 * Every threshold lives in CONFIG with version + hypothesis notes (V2.1 §12:
 *   flexible math — weights/thresholds are calibratable, never constitutional).
 */

// ============================================================ versioned config

export const CALCULUS_VERSION = 'decision-calculus-v2.1';

export type HarmScope =
  | 'physical' | 'rights' | 'financial' | 'data'
  | 'reputational' | 'informational' | 'resource';

export interface TauEntry {
  /** max P(unacceptable harm) for this scope; 0 = zero-tolerance class */
  p: number;
  /** severity at/above which a tail counts as "unacceptable harm" for this scope */
  severity: number;
  escalation: 'PROHIBITED' | 'NEEDS_AUTHORITY';
}

export interface CalculusConfig {
  version: string;
  qWeights: Record<QDimId, number>;
  criticalDims: QDimId[];
  /** a quality dimension below this caps autonomous readiness (hypothesis) */
  criticalDimFloor: number;
  qAutonomy: number; qDelight: number; qRework: number;
  cAggMin: number; cCritMin: number;
  kLow: number; kHigh: number;
  reversibilityMin: number;
  dominanceMargin: number;
  epsilon: number;
  /** Normalize() half-range scale, in domain value units (hypothesis; §3) */
  dScale: number;
  tauScope: Record<HarmScope, TauEntry>;
  windowsHours: Record<'reversible' | 'financial' | 'irreversible' | 'rights', number>;
  /** probabilities below this are modeling noise, not license (τ=0 classes) */
  materialP: number;
  /** points per unit of contribution credit (economy hypothesis; §11) */
  pointsPerCVS: number;
  /** attribution fraction for downstream-value receipts (hypothesis) */
  attributionFraction: number;
}

export const CONFIG: CalculusConfig = {
  version: CALCULUS_VERSION,
  qWeights: {
    objectiveFit: 0.20, evidenceSufficiency: 0.20, applicability: 0.15,
    robustness: 0.15, reversibility: 0.10, blastContainment: 0.10, simplicity: 0.10,
  },
  criticalDims: ['objectiveFit', 'evidenceSufficiency', 'robustness'],
  criticalDimFloor: 5.0,
  qAutonomy: 9.0, qDelight: 9.5, qRework: 7.0,
  cAggMin: 0.80, cCritMin: 0.75,          // §5 low-risk autonomous hypotheses
  kLow: 5, kHigh: 20,                     // R6 evidence floors
  reversibilityMin: 7.0,                  // R1: gate input, not multiplier
  dominanceMargin: 0.25,                  // R1: relative margin on V_safe (§6)
  epsilon: 1e-9,
  dScale: 1.0,
  tauScope: {                            // R4 seed table — hypotheses for director review
    physical:     { p: 0,     severity: 9, escalation: 'PROHIBITED' },
    rights:       { p: 0,     severity: 9, escalation: 'PROHIBITED' },
    financial:    { p: 0.001, severity: 7, escalation: 'NEEDS_AUTHORITY' },
    data:         { p: 0.001, severity: 7, escalation: 'NEEDS_AUTHORITY' },
    reputational: { p: 0.01,  severity: 5, escalation: 'NEEDS_AUTHORITY' },
    informational:{ p: 0.05,  severity: 3, escalation: 'NEEDS_AUTHORITY' },
    resource:     { p: 0.10,  severity: 2, escalation: 'NEEDS_AUTHORITY' },
  },
  windowsHours: { reversible: 24, financial: 168, irreversible: 720, rights: 2160 }, // R5
  materialP: 1e-6,
  pointsPerCVS: 100,
  attributionFraction: 0.10,
};

// ============================================================ types

export type QDimId =
  | 'objectiveFit' | 'evidenceSufficiency' | 'applicability' | 'robustness'
  | 'reversibility' | 'blastContainment' | 'simplicity';
export const Q_DIMS: QDimId[] = [
  'objectiveFit', 'evidenceSufficiency', 'applicability', 'robustness',
  'reversibility', 'blastContainment', 'simplicity',
];

export type Gate = 'PROHIBITED' | 'NEEDS_AUTHORITY' | 'NEEDS_EVIDENCE' | 'ADMISSIBLE';
export type Stakes = 'low' | 'medium' | 'high' | 'consequential';
export type QBand = 'DELIGHT' | 'ACCEPT' | 'BELOW_STANDARD' | 'REJECT';
export type Decision = 'EXECUTE' | 'BRIEF' | 'RESEARCH_PROBE' | 'REWORK';
export type VerifyState = 'PASS' | 'PASS_PENDING_WINDOW' | 'FAIL' | 'REOPENED' | 'ESCALATE';

/** PV components — all evidence-bound estimates, never asserted. */
export interface PVComponents { B: number; H: number; C: number; R: number }
export interface Tail { harm: number; probability: number; scope: HarmScope }

export interface Candidate {
  id: string;
  /** id of the baseline/current-course candidate in this decision set */
  baselineId: string;
  /** predicted PV components for THIS action */
  pv: PVComponents;
  /** declared PV(baseline); ΔV(a|b) = PV(a) − PV(b); ΔV(b|b) = 0 by definition */
  baselinePV: number;
  baselineEvidence: string;
  /**
   * Evidence-bound uncertainty on ΔV, in value units (≥0). A production estimator
   * derives this as z×SE from evidence; the reference takes it as an input.
   * Missing/unknown uncertainty is NOT defaulted — it fails the evidence floor.
   */
  dVUncertainty: number;
  tails: Tail[];
  qDims: Record<QDimId, number>;   // each [0,10]; value magnitude is NOT a dimension
  qConf: Record<QDimId, number>;   // each [0,1]
  /** evidence count behind this option's estimates */
  n: number;
  stakes: Stakes;
  authorized: boolean;
  /** true/false/undefined(=unknown). Unknown at non-low stakes escalates. */
  lawful: boolean | undefined;
  harmFlag?: boolean;          // Law of One
  knownWrongFlag?: boolean;    // Judgment Rule
  prohibitedHarmClass?: boolean;
  conflictingPrincipals?: boolean;
  intentAmbiguity?: boolean;
  /** collective-harm input: per-capita harm × parties × probability */
  collective?: { perCapitaHarm: number; parties: number; probability: number; scope: HarmScope };
  jurisdictions?: { id: string; lawful: boolean | undefined }[];
  resourceClaims?: string[];
  urgency?: number;             // [0,10] tiebreak input
  humanBurden?: number;        // [0,10] tiebreak input
  reversibility: number;        // [0,10]; mirrors qDims.reversibility, used as gate input
}

export interface Scored {
  c: Candidate;
  Q: number; capped: boolean;
  cAgg: number; cCrit: number;
  deltaV: number; vSafe: number; tailPenalty: number;
  gate: Gate; reasons: string[];
}

// ============================================================ utils

const clamp = (x: number, lo: number, hi: number) => Math.min(hi, Math.max(lo, x));
const r4 = (x: number) => Math.round(x * 10000) / 10000;

/** Canonical JSON: sorted keys, recursive — receipts hash stably. */
export function stableStringify(v: unknown): string {
  if (v === null || typeof v !== 'object') return JSON.stringify(v) ?? 'null';
  if (Array.isArray(v)) return '[' + v.map(stableStringify).join(',') + ']';
  const o = v as Record<string, unknown>;
  return '{' + Object.keys(o).sort().map(k => JSON.stringify(k) + ':' + stableStringify(o[k])).join(',') + '}';
}

/** FNV-1a 32-bit hex — dependency-free config fingerprint (weight-manipulation detection). */
export function configHash(cfg: CalculusConfig): string {
  let h = 0x811c9dc5;
  const s = stableStringify(cfg);
  for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 0x01000193); }
  return ('0000000' + (h >>> 0).toString(16)).slice(-8);
}

// ============================================================ value (baseline-relative)

export function pvOf(p: PVComponents): number { return r4(p.B - p.H - p.C - p.R); }

/** ΔV(a|b) = PV(a) − PV(b). Baseline-relative: ΔV(b|b) = 0. Harmful inaction is
 *  visible here — a status-quo baseline with negative drift makes action ΔV > 0. */
export function deltaV(c: Candidate): number { return r4(pvOf(c.pv) - c.baselinePV); }

export function tailPenalty(c: Candidate): number {
  return r4(c.tails.reduce((s, t) => s + t.harm * t.probability, 0));
}

/**
 * Conservative value: V_safe = LCB(ΔV) − TailRiskPenalty, with LCB(ΔV) =
 * ΔV_pred − U. Mean expected value is never optimized alone (§4).
 */
export function vSafe(c: Candidate): number {
  return r4(deltaV(c) - c.dVUncertainty - tailPenalty(c));
}

/** Effective tails including collective-harm expansion (§13: collective vs individual). */
function effectiveTails(c: Candidate): Tail[] {
  const tails = [...c.tails];
  if (c.collective && c.collective.parties > 0) {
    tails.push({
      harm: c.collective.perCapitaHarm * c.collective.parties,
      probability: c.collective.probability,
      scope: c.collective.scope,
    });
  }
  return tails;
}

// ============================================================ quality (pure — no value inside)

export interface Quality { Q: number; capped: boolean; cAgg: number; cCrit: number; band: QBand }

export function quality(c: Candidate, cfg: CalculusConfig = CONFIG): Quality {
  let Q = 0, cAgg = 0, cCrit = 1;
  for (const d of Q_DIMS) {
    const s = clamp(c.qDims[d], 0, 10);
    const cf = clamp(c.qConf[d], 0, 1);
    Q += cfg.qWeights[d] * s;
    cAgg += cfg.qWeights[d] * cf;
    if (cfg.criticalDims.includes(d)) cCrit = Math.min(cCrit, cf);
  }
  // A critical proof gap caps autonomous readiness regardless of the mean (§2).
  const minDim = Math.min(...Q_DIMS.map(d => clamp(c.qDims[d], 0, 10)));
  let capped = false;
  if (minDim < cfg.criticalDimFloor && Q >= cfg.qAutonomy) { Q = cfg.qAutonomy - 0.01; capped = true; }
  Q = r4(Q); cAgg = r4(cAgg); cCrit = r4(cCrit);
  const band: QBand =
    Q >= cfg.qDelight ? 'DELIGHT' : Q >= cfg.qAutonomy ? 'ACCEPT'
    : Q >= cfg.qRework ? 'BELOW_STANDARD' : 'REJECT';
  return { Q, capped, cAgg, cCrit, band };
}

// ============================================================ gates (four-valued)

function kFor(stakes: Stakes, cfg: CalculusConfig): number {
  return stakes === 'low' ? cfg.kLow : cfg.kHigh;
}

export function gate(c: Candidate, q: Quality, cfg: CalculusConfig = CONFIG): { gate: Gate; reasons: string[] } {
  const reasons: string[] = [];
  const refuse = (r: string): { gate: Gate; reasons: string[] } => { reasons.push(r); return { gate: 'PROHIBITED', reasons }; };
  const needAuth = (r: string): { gate: Gate; reasons: string[] } => { reasons.push(r); return { gate: 'NEEDS_AUTHORITY', reasons }; };

  // Hard law first — never scalarized (§1).
  if (c.harmFlag) return refuse('LAW_OF_ONE: harm flag set');
  if (c.knownWrongFlag) return refuse('JUDGMENT_RULE: known-wrong flag set');
  if (c.lawful === false) return refuse('UNLAWFUL: law/rights check failed');
  if (c.prohibitedHarmClass) return refuse('PROHIBITED_HARM_CLASS');

  // τ_scope tail gates (§4, R4).
  for (const t of effectiveTails(c)) {
    const tau = cfg.tauScope[t.scope];
    if (t.harm >= tau.severity) {
      if (tau.p === 0) {
        // Zero-tolerance class: any material probability refuses. Sub-material
        // probabilities are modeling noise, not license — and not a refusal.
        if (t.probability >= cfg.materialP) return refuse(`TAU_ZERO: ${t.scope} harm=${t.harm} p=${t.probability}`);
      } else if (t.probability > tau.p) {
        return tau.escalation === 'PROHIBITED'
          ? refuse(`TAU_EXCEEDED: ${t.scope} harm=${t.harm} p=${t.probability} > τ=${tau.p}`)
          : needAuth(`TAU_EXCEEDED: ${t.scope} harm=${t.harm} p=${t.probability} > τ=${tau.p}`);
      }
    }
  }

  // Jurisdiction conflict → law unknown → escalate (§13).
  if (c.jurisdictions && c.jurisdictions.length > 0) {
    const vals = c.jurisdictions.map(j => j.lawful);
    const conflict = vals.includes(false) || vals.includes(undefined) || new Set(vals).size > 1;
    if (conflict) return needAuth('JURISDICTION_CONFLICT: law status differs/unknown across jurisdictions');
  }

  if (!c.authorized) return needAuth('NOT_AUTHORIZED');
  if (c.lawful === undefined && c.stakes !== 'low') return needAuth('LAW_UNKNOWN_AT_STAKES');
  if (c.conflictingPrincipals) return needAuth('CONFLICTING_PRINCIPALS: human resolves');
  // Consequential + irreversible → human, regardless of score (§5, §7).
  if (c.stakes === 'consequential' && c.reversibility < cfg.reversibilityMin)
    return needAuth('CONSEQUENTIAL_IRREVERSIBLE');

  // Evidence floors — a crisp score cannot hide insufficient data (§5, R6).
  if (c.n < kFor(c.stakes, cfg))
    return { gate: 'NEEDS_EVIDENCE', reasons: [`DATA_FLOOR: n=${c.n} < k=${kFor(c.stakes, cfg)}`] };
  if (q.cAgg < cfg.cAggMin || q.cCrit < cfg.cCritMin)
    return { gate: 'NEEDS_EVIDENCE', reasons: [`CONFIDENCE_FLOOR: cAgg=${q.cAgg} cCrit=${q.cCrit}`] };

  return { gate: 'ADMISSIBLE', reasons: [] };
}

// ============================================================ pareto + selection

export function score(c: Candidate, cfg: CalculusConfig = CONFIG): Scored {
  const q = quality(c, cfg);
  const g = gate(c, q, cfg);
  return {
    c, Q: q.Q, capped: q.capped, cAgg: q.cAgg, cCrit: q.cCrit,
    deltaV: deltaV(c), vSafe: vSafe(c), tailPenalty: tailPenalty(c),
    gate: g.gate, reasons: g.reasons,
  };
}

/** a dominates b iff ≥ on all three objectives and strictly better on ≥1 (§6). */
function dominates(a: Scored, b: Scored): boolean {
  const ge = a.vSafe >= b.vSafe && a.Q >= b.Q && a.tailPenalty <= b.tailPenalty;
  const gt = a.vSafe > b.vSafe || a.Q > b.Q || a.tailPenalty < b.tailPenalty;
  return ge && gt;
}

export function paretoFrontier(scored: Scored[]): Scored[] {
  return scored.filter(s => !scored.some(o => o !== s && dominates(o, s)));
}

/** Frontier ranking (§6): V_safe → urgency → reversibility → lower burden → simplicity → confidence. */
export function rankFrontier(frontier: Scored[]): Scored[] {
  return [...frontier].sort((a, b) =>
    b.vSafe - a.vSafe ||
    (b.c.urgency ?? 0) - (a.c.urgency ?? 0) ||
    b.c.reversibility - a.c.reversibility ||
    (a.c.humanBurden ?? 0) - (b.c.humanBurden ?? 0) ||
    b.c.qDims.simplicity - a.c.qDims.simplicity ||
    b.cAgg - a.cAgg);
}

/** P_norm — saturating priority map for scheduling/queue ranking (R1).
 *  The AUTONOMY dominance margin is on V_safe (§6), not on this. */
export function normalizePriority(pRaw: number): number {
  return r4(Math.max(0, pRaw) / (1 + Math.max(0, pRaw)));
}

/** Relative dominance margin on conservative value (§6). */
export function dominanceMargin(v1: number, v2: number, cfg: CalculusConfig = CONFIG): number {
  return r4((v1 - v2) / Math.max(Math.abs(v1), cfg.epsilon));
}

export interface AskHumanFlags {
  authorityRequired: boolean; intentAmbiguity: boolean;
  consequentialIrreversibility: boolean; materialUncertainty: boolean;
  noClearDominantOption: boolean;
}
/** AskHuman law (§8). */
export function askHuman(f: AskHumanFlags): boolean {
  return f.authorityRequired || f.intentAmbiguity || f.consequentialIrreversibility ||
    f.materialUncertainty || f.noClearDominantOption;
}

export interface DecisionResult {
  decision: Decision;
  top3: Scored[];
  winner: Scored | null;
  margin: number | null;
  reasons: string[];
  receipt: DecisionReceipt;
}

// ============================================================ SmartLedger decision receipt (§10A)

export interface DecisionReceipt {
  ledger: 'smartledger'; stream: 'decision';
  calculusVersion: string; configHash: string;
  issuedAt: string;
  intent: string; baseline: string; stakeholders: string; horizon: string;
  candidates: { id: string; gate: Gate; reasons: string[]; Q: number; capped: boolean;
    cAgg: number; cCrit: number; deltaV: number; vSafe: number; tailPenalty: number }[];
  paretoIds: string[]; rankedIds: string[];
  decision: Decision; winnerId: string | null; margin: number | null;
  authorityBasis: string;
  verification: { state: VerifyState; windowHours: number; windowClosesAt: string | null };
  observation: { deltaVActual: number | null; dVerified: number | null;
    calibrationError: number | null; harmDetected: number | null };
  lesson: string | null;
}

export interface DecideInput {
  intent: string; stakeholders: string; horizon: string;
  authorityBasis: string;
  harmCategory: 'reversible' | 'financial' | 'irreversible' | 'rights';
  issuedAt: string;   // explicit clock for determinism
  choiceForced?: boolean;
}

export function decide(
  candidates: Candidate[], input: DecideInput, cfg: CalculusConfig = CONFIG,
): DecisionResult {
  const reasons: string[] = [];
  const baseline = candidates.find(c => c.id === c.baselineId);
  if (!baseline) {
    const rs = ['BASELINE_MISSING: no candidate carries the declared baseline id'];
    const receipt = makeReceipt(candidates.map(c => score(c, cfg)), input, 'REWORK', null, null, cfg);
    return { decision: 'REWORK', top3: [], winner: null, margin: null, reasons: rs, receipt };
  }
  const scored = candidates.map(c => score(c, cfg));
  const admissible = scored.filter(s =>
    s.gate === 'ADMISSIBLE' && s.Q >= cfg.qAutonomy && s.vSafe > 0);
  const frontier = paretoFrontier(admissible);
  const ranked = rankFrontier(frontier);
  const top3 = ranked.slice(0, 3);
  const [r1, r2] = top3;

  let decision: Decision = 'REWORK';
  let margin: number | null = null;
  if (r1) {
    margin = r2 ? dominanceMargin(r1.vSafe, r2.vSafe, cfg) : null;
    const human = askHuman({
      authorityRequired: top3.some(s => s.gate !== 'ADMISSIBLE'),
      intentAmbiguity: !!r1.c.intentAmbiguity,
      consequentialIrreversibility: r1.c.stakes === 'consequential' && r1.c.reversibility < cfg.reversibilityMin,
      materialUncertainty: r1.c.dVUncertainty >= Math.abs(r1.deltaV) && r1.deltaV !== 0,
      noClearDominantOption: r2 !== undefined && (margin as number) < cfg.dominanceMargin,
    });
    if (r1.c.reversibility >= cfg.reversibilityMin && !human &&
        (r2 === undefined || (margin as number) >= cfg.dominanceMargin)) {
      decision = 'EXECUTE';
      reasons.push('AUTONOMOUS: admissible, Q≥9, V_safe>0, floors pass, reversible enough, clear relative dominance');
    } else if (scored.some(s => s.gate === 'NEEDS_EVIDENCE')) {
      decision = 'RESEARCH_PROBE';
      reasons.push('EVIDENCE_BLOCKER: at least one candidate needs evidence; probe or narrow scope');
    } else {
      decision = 'BRIEF';
      reasons.push('BRIEF_TOP3: no autonomous winner; human decides with recommendation + exact authority needed');
    }
  } else {
    if (scored.some(s => s.gate === 'NEEDS_EVIDENCE')) {
      decision = 'RESEARCH_PROBE';
      reasons.push('EVIDENCE_BLOCKER: no admissible candidate; gather evidence or probe');
    } else {
      reasons.push('NO_ADMISSIBLE_CANDIDATE: rework required');
    }
  }
  const receipt = makeReceipt(scored, input, decision, r1 ?? null, margin, cfg);
  return { decision, top3, winner: r1 ?? null, margin, reasons, receipt };
}

function makeReceipt(
  scored: Scored[], input: DecideInput, decision: Decision,
  winner: Scored | null, margin: number | null, cfg: CalculusConfig,
): DecisionReceipt {
  const windowHours = cfg.windowsHours[input.harmCategory];
  return {
    ledger: 'smartledger', stream: 'decision',
    calculusVersion: cfg.version, configHash: configHash(cfg),
    issuedAt: input.issuedAt,
    intent: input.intent, baseline: scored[0]?.c.baselineId ?? 'UNKNOWN',
    stakeholders: input.stakeholders, horizon: input.horizon,
    candidates: scored.map(s => ({
      id: s.c.id, gate: s.gate, reasons: s.reasons, Q: s.Q, capped: s.capped,
      cAgg: s.cAgg, cCrit: s.cCrit, deltaV: s.deltaV, vSafe: s.vSafe, tailPenalty: s.tailPenalty,
    })),
    paretoIds: paretoFrontier(scored.filter(s => s.gate === 'ADMISSIBLE')).map(s => s.c.id),
    rankedIds: rankFrontier(paretoFrontier(scored.filter(s => s.gate === 'ADMISSIBLE'))).map(s => s.c.id),
    decision, winnerId: winner?.c.id ?? null, margin,
    authorityBasis: input.authorityBasis,
    verification: {
      state: 'PASS_PENDING_WINDOW',
      windowHours,
      windowClosesAt: new Date(new Date(input.issuedAt).getTime() + windowHours * 3600e3).toISOString(),
    },
    observation: { deltaVActual: null, dVerified: null, calibrationError: null, harmDetected: null },
    lesson: null,
  };
}

// ============================================================ verification (§9, R5)

/** Versioned domain-specific normalization, then clamp to the ±9 display anchor (§3). */
export function normalizeDeltaV(dV: number, dScale: number = CONFIG.dScale): number {
  return r4(9 * dV / (dScale + Math.abs(dV)));
}
export function dVerified(dVActual: number, dScale: number = CONFIG.dScale): number {
  return r4(clamp(normalizeDeltaV(dVActual, dScale), -9, 9));
}

export interface VerifiedReceipt extends DecisionReceipt {
  observation: { deltaVActual: number; dVerified: number; calibrationError: number; harmDetected: number };
}

export function verifyOutcome(
  receipt: DecisionReceipt,
  observed: { deltaVActual: number; harmDetected: number; now: string },
  cfg: CalculusConfig = CONFIG,
): VerifiedReceipt {
  const pred = receipt.candidates.find(c => c.id === receipt.winnerId)?.deltaV ?? 0;
  const windowOpen = receipt.verification.windowClosesAt !== null &&
    new Date(observed.now).getTime() < new Date(receipt.verification.windowClosesAt).getTime();
  const state: VerifyState =
    observed.harmDetected > 0 ? 'FAIL'
    : windowOpen ? 'PASS_PENDING_WINDOW' : 'PASS';
  return {
    ...receipt,
    verification: { ...receipt.verification, state },
    observation: {
      deltaVActual: r4(observed.deltaVActual),
      dVerified: dVerified(observed.deltaVActual, cfg.dScale),
      calibrationError: r4(Math.abs(pred - observed.deltaVActual)),
      harmDetected: observed.harmDetected,
    },
  };
}

/** A prior PASS may be reopened when later evidence contradicts it (§9). */
export function reopenVerification(
  receipt: VerifiedReceipt, evidence: string, now: string,
): VerifiedReceipt {
  return {
    ...receipt,
    verification: { ...receipt.verification, state: 'REOPENED' },
    lesson: `REOPENED at ${now}: ${evidence}`,
  };
}

/** No irreversible learning promotion on a still-open window where delayed harm is material (§9). */
export function promotionEligible(receipt: DecisionReceipt, maxTailHarm: number, now: string): boolean {
  const windowOpen = receipt.verification.windowClosesAt !== null &&
    new Date(now).getTime() < new Date(receipt.verification.windowClosesAt).getTime();
  if (windowOpen && maxTailHarm >= CONFIG.tauScope.physical.severity) return false;
  return receipt.verification.state === 'PASS';
}

// ============================================================ contribution credit (§11, candidate)

export interface Contribution {
  id: string;
  contributor: string;
  /** verified baseline-relative value created */
  dVVerified: number;
  quality: number; relevance: number; verification: number; impact: number; novelty: number; // [0,1]
  provenance: string;
}

/**
 * CVS_j = sign(ΔV) × 9 × (Q×Rel×Ver×Impact×Novelty)^(1/5) — CANDIDATE anti-spam
 * formula, not ratified law. Activity ≠ Value: raw likes/comments/shares earn
 * nothing by themselves; they earn only through downstream verified value via
 * attribution receipts (fraction of the reuse's CVS, with provenance link).
 */
export function contributionCredit(j: Contribution, cfg: CalculusConfig = CONFIG): number {
  const g = Math.pow(
    clamp(j.quality, 0, 1) * clamp(j.relevance, 0, 1) * clamp(j.verification, 0, 1) *
    clamp(j.impact, 0, 1) * clamp(j.novelty, 0, 1), 1 / 5);
  return r4(Math.sign(j.dVVerified) * 9 * g * (j.dVVerified === 0 ? 0 : 1));
}
export function contributionPoints(cvs: number, cfg: CalculusConfig = CONFIG): number {
  return Math.round(cvs * cfg.pointsPerCVS);
}
/** Attribution: a share/like/comment that led to verified reuse earns a fraction. */
export function attributionCredit(reuseCVS: number, cfg: CalculusConfig = CONFIG): number {
  return r4(reuseCVS * cfg.attributionFraction);
}

// ============================================================ bundles (§13: action-splitting defense)

/**
 * Authorization laundering via action splitting: evaluate the bundle as one
 * candidate. Splitting a consequential action into sub-threshold pieces does
 * not evade the gate — the bundle carries the combined tails and value.
 */
export function bundleCandidate(id: string, parts: Candidate[]): Candidate {
  const first = parts[0];
  const pv: PVComponents = { B: 0, H: 0, C: 0, R: 0 };
  let dVUncertainty = 0;
  const tails: Tail[] = [];
  const qDims = {} as Record<QDimId, number>;
  const qConf = {} as Record<QDimId, number>;
  for (const d of Q_DIMS) { qDims[d] = 0; qConf[d] = 0; }
  for (const p of parts) {
    pv.B += p.pv.B; pv.H += p.pv.H; pv.C += p.pv.C; pv.R += p.pv.R;
    dVUncertainty += p.dVUncertainty * p.dVUncertainty;
    tails.push(...p.tails);
    for (const d of Q_DIMS) { qDims[d] += p.qDims[d] / parts.length; qConf[d] += p.qConf[d] / parts.length; }
  }
  return {
    ...first, id,
    pv, dVUncertainty: r4(Math.sqrt(dVUncertainty)), tails, qDims, qConf,
    n: Math.min(...parts.map(p => p.n)),
    stakes: parts.some(p => p.stakes === 'consequential') ? 'consequential'
      : parts.some(p => p.stakes === 'high') ? 'high'
      : parts.some(p => p.stakes === 'medium') ? 'medium' : 'low',
    reversibility: Math.min(...parts.map(p => p.reversibility)),
  };
}

/** Resource contention between agents (§13: AI-to-AI conflict) → human. */
export function resourceConflicts(candidates: Candidate[]): [string, string, string][] {
  const out: [string, string, string][] = [];
  for (let i = 0; i < candidates.length; i++)
    for (let j = i + 1; j < candidates.length; j++) {
      const a = candidates[i].resourceClaims ?? [], b = candidates[j].resourceClaims ?? [];
      for (const r of a) if (b.includes(r)) out.push([candidates[i].id, candidates[j].id, r]);
    }
  return out;
}

// ============================================================ learning (§12)

export function calibrationError(dVPred: number, dVActual: number): number {
  return r4(Math.abs(dVPred - dVActual));
}
export function calibration(errs: number[]): { meanAbsDelta: number; n: number } {
  return {
    meanAbsDelta: errs.length ? r4(errs.reduce((a, b) => a + b, 0) / errs.length) : 0,
    n: errs.length,
  };
}

/**
 * Independent recomputation: rerun the decision from the receipt's candidate
 * inputs under a given config. Detects weight/rubric manipulation (config hash
 * mismatch) and nondeterminism. Cold-successor check: same facts + same config
 * → same decision.
 */
export function recompute(
  receipt: DecisionReceipt, candidates: Candidate[], input: DecideInput, cfg: CalculusConfig,
): { status: 'MATCH' | 'DECISION_MISMATCH' | 'CONFIG_MISMATCH'; detail: string } {
  if (configHash(cfg) !== receipt.configHash)
    return { status: 'CONFIG_MISMATCH', detail: `config hash ${configHash(cfg)} ≠ receipt ${receipt.configHash}` };
  const r = decide(candidates, input, cfg);
  if (r.decision !== receipt.decision || r.winner?.c.id !== receipt.winnerId)
    return { status: 'DECISION_MISMATCH', detail: `recomputed ${r.decision}/${r.winner?.c.id} ≠ receipt ${receipt.decision}/${receipt.winnerId}` };
  return { status: 'MATCH', detail: 'decision reproduces exactly' };
}
