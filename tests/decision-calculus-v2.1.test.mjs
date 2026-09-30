/**
 * Decision Value Calculus V2.1 — adversarial + property test suite.
 * Convention: node:test + node:assert/strict, importing the TS module directly
 * (same as the other tests/*.test.mjs in this repo). Run: node --test tests/decision-calculus-v2.1.test.mjs
 *
 * Covers: preserved V2 hard-boundary tests (adapted), the R1–R6 corrections,
 * and the §13 attack closures: prediction inflation, component gaming,
 * action-splitting/authorization laundering, delayed harm, collective harm,
 * conflicting principals, malicious-user asymmetry, reward hacking, uncertainty
 * laundering, AI-to-AI conflict, jurisdiction conflict, bad baseline,
 * weight manipulation. Status: CANDIDATE, NOT RATIFIED.
 */
import test from "node:test";
import assert from "node:assert/strict";
import {
  CONFIG, CALCULUS_VERSION, configHash, stableStringify,
  pvOf, deltaV, vSafe, tailPenalty, quality, gate, score,
  paretoFrontier, rankFrontier, normalizePriority, dominanceMargin,
  askHuman, decide, verifyOutcome, reopenVerification, promotionEligible,
  normalizeDeltaV, dVerified, contributionCredit, contributionPoints,
  attributionCredit, bundleCandidate, resourceConflicts,
  calibrationError, calibration, recompute,
} from "../kernel/decision-calculus/value-calculus-v2.1.ts";

const QDIMS = ['objectiveFit','evidenceSufficiency','applicability','robustness','reversibility','blastContainment','simplicity'];
const qd = (v=9.2) => Object.fromEntries(QDIMS.map(d=>[d,v]));
const qc = (v=0.9) => Object.fromEntries(QDIMS.map(d=>[d,v]));

function cand(id, p={}) {
  return {
    id, baselineId: 'baseline',
    pv: { B: 8, H: 0, C: 2, R: 0.5 }, baselinePV: 0, baselineEvidence: 'test',
    dVUncertainty: 0.5, tails: [],
    qDims: qd(), qConf: qc(), n: 10,
    stakes: 'low', authorized: true, lawful: true, reversibility: 9,
    ...p,
  };
}
const INPUT = {
  intent: 'test decision', stakeholders: 'test', horizon: 'test',
  authorityBasis: 'test-standing-authority', harmCategory: 'financial',
  issuedAt: '2026-09-30T23:00:00Z',
};
const baselineCand = () => cand('baseline', {
  pv: { B: 0, H: 0, C: 0, R: 0 }, baselinePV: 0, dVUncertainty: 0,
});

// ---------- value model ----------
test("PV = B-H-C-R", () => assert.equal(pvOf({B:8,H:1,C:2,R:0.5}), 4.5));
test("ΔV is baseline-relative; ΔV(b|b)=0", () => {
  const b = baselineCand();
  assert.equal(deltaV(b), 0);
  assert.equal(deltaV(cand('a', { baselinePV: 2 })), 3.5); // 5.5-2
});
test("V_safe = ΔV − U − tailPenalty (mean never optimized alone)", () => {
  const c = cand('a', { dVUncertainty: 1, tails: [{harm:4, probability:0.5, scope:'informational'}] });
  assert.equal(vSafe(c), 5.5 - 1 - 2);
});

// ---------- hard boundaries (preserved from V2) ----------
test("enormous value + harm flag → PROHIBITED (value never authorizes)", () => {
  const c = cand('rich', { pv: {B:100,H:0,C:1,R:0}, harmFlag: true, qDims: qd(10), qConf: qc(1) });
  assert.equal(gate(c, quality(c)).gate, 'PROHIBITED');
});
test("catastrophic tail in τ=0 class → PROHIBITED", () => {
  const c = cand('tail', { tails: [{harm:10, probability:0.10, scope:'physical'}] });
  assert.equal(gate(c, quality(c)).gate, 'PROHIBITED');
});
test("τ=0 class below materialP is modeling noise, not a refusal", () => {
  const c = cand('dust', { tails: [{harm:10, probability:1e-9, scope:'physical'}] });
  assert.equal(gate(c, quality(c)).gate, 'ADMISSIBLE');
});
test("financial tail above τ → NEEDS_AUTHORITY (policy escalation)", () => {
  const c = cand('fin', { tails: [{harm:8, probability:0.01, scope:'financial'}] });
  assert.equal(gate(c, quality(c)).gate, 'NEEDS_AUTHORITY');
});
test("unknown law at high stakes → NEEDS_AUTHORITY", () => {
  const c = cand('murky', { lawful: undefined, stakes: 'high' });
  assert.equal(gate(c, quality(c)).gate, 'NEEDS_AUTHORITY');
});
test("unauthorized at any value → NEEDS_AUTHORITY", () => {
  const c = cand('unauth', { authorized: false, pv: {B:50,H:0,C:1,R:0} });
  assert.equal(gate(c, quality(c)).gate, 'NEEDS_AUTHORITY');
});
test("known-wrong flag → PROHIBITED (Judgment Rule)", () => {
  const c = cand('kw', { knownWrongFlag: true });
  assert.equal(gate(c, quality(c)).gate, 'PROHIBITED');
});

// ---------- R1–R6 corrections ----------
test("R2-fix: PV removed from Q — huge value + poor quality → Q<9 (no fake 9)", () => {
  const c = cand('pv-rich', { pv: {B:1000,H:0,C:1,R:0}, qDims: qd(5), qConf: qc(0.9) });
  const q = quality(c);
  assert.ok(q.Q < 9, `Q=${q.Q} must be below autonomy bar`);
  assert.equal(q.band, 'REJECT');
});
test("R1-fix: reversibility is a gate input — irreversible option never EXECUTEs", () => {
  const c = cand('irrev', { reversibility: 3, qDims: {...qd(), reversibility: 3} });
  const r = decide([baselineCand(), c], INPUT);
  assert.notEqual(r.decision, 'EXECUTE');
});
test("R1-fix: dominance margin is relative on V_safe", () => {
  assert.equal(dominanceMargin(5, 4), 0.2);
  assert.equal(dominanceMargin(100, 80), 0.2); // scale-invariant, unlike absolute 0.75
  assert.ok(normalizePriority(0) === 0 && normalizePriority(1e9) > 0.999);
});
test("R3-fix: Pareto frontier drops dominated options", () => {
  const mk = (id, vs, q, trp) => ({ c: {id}, vSafe: vs, Q: q, tailPenalty: trp });
  const a = mk('a', 5, 9.0, 2), b = mk('b', 6, 9.5, 1), cc = mk('c', 7, 9.0, 5);
  const f = paretoFrontier([a, b, cc]).map(s => s.c.id).sort();
  assert.deepEqual(f, ['b', 'c']); // a dominated by b; c survives on V_safe
});
test("R5-fix: D_verified clamps to ±9 display anchor", () => {
  assert.ok(dVerified(500) <= 9 && dVerified(500) > 8.9);
  assert.ok(dVerified(-500) >= -9 && dVerified(-500) < -8.9);
  assert.equal(dVerified(0), 0);
  assert.ok(normalizeDeltaV(1) > 0 && normalizeDeltaV(1) < 9);
});
test("R6-fix: n < k → NEEDS_EVIDENCE even with perfect scores", () => {
  const c = cand('thin', { n: 2, qDims: qd(10), qConf: qc(1) });
  const g = gate(c, quality(c));
  assert.equal(g.gate, 'NEEDS_EVIDENCE');
  assert.match(g.reasons[0], /DATA_FLOOR/);
});
test("critical-dimension UNKNOWN → NEEDS_EVIDENCE (not averaged away)", () => {
  const c = cand('unk', { qConf: {...qc(), evidenceSufficiency: 0.5} });
  const q = quality(c);
  assert.ok(q.cCrit < CONFIG.cCritMin);
  assert.equal(gate(c, q).gate, 'NEEDS_EVIDENCE');
});
test("critical proof gap caps Q below autonomy bar", () => {
  const c = cand('gap', { qDims: {...qd(10), robustness: 4.9} }); // raw Q=9.235 ≥ 9, one dim < 5
  const q = quality(c);
  assert.ok(q.capped && q.Q < CONFIG.qAutonomy, `capped=${q.capped} Q=${q.Q}`);
});

// ---------- selection behavior ----------
function twoOpt() {
  const win = cand('win', { pv: {B:8,H:0,C:2,R:0.5}, dVUncertainty: 0.5 });           // V_safe=5.0, Q=9.2
  const run = cand('run', { pv: {B:3,H:0,C:1.5,R:0.5}, dVUncertainty: 0.2,
    qDims: qd(9.6) });  // V_safe=0.8, Q=9.6 — not dominated (higher Q), so margin is contested
  return [baselineCand(), win, run];
}
test("clear dominant low-risk option → EXECUTE", () => {
  const r = decide(twoOpt(), INPUT);
  assert.equal(r.decision, 'EXECUTE');
  assert.equal(r.winner.c.id, 'win');
  assert.ok(r.margin >= CONFIG.dominanceMargin);
  assert.equal(r.receipt.decision, 'EXECUTE');
});
test("near tie (margin < 0.25) → BRIEF top3, never EXECUTE", () => {
  const a = cand('a', { pv: {B:7,H:0,C:1.9,R:0.1}, dVUncertainty: 0.1 });  // V_safe=5.0
  const b = cand('b', { pv: {B:7,H:0,C:2.0,R:0.0}, dVUncertainty: 0.1 });  // V_safe=4.9
  const r = decide([baselineCand(), a, b], INPUT);
  assert.equal(r.decision, 'BRIEF');
  assert.equal(r.top3.length, 2);
});
test("perfect Q + negative V_safe → no action (winner null)", () => {
  const c = cand('neg', { qDims: qd(10), qConf: qc(1), pv: {B:1,H:5,C:0,R:0} });
  const r = decide([baselineCand(), c], INPUT);
  assert.notEqual(r.decision, 'EXECUTE');
  assert.equal(r.winner, null);
});
test("consequential + irreversible → NEEDS_AUTHORITY despite perfect scores", () => {
  const c = cand('cons', { stakes: 'consequential', reversibility: 2,
    qDims: {...qd(10), reversibility: 2}, qConf: qc(1) });
  assert.equal(gate(c, quality(c)).gate, 'NEEDS_AUTHORITY');
});
test("harmful inaction is visible: negative-drift baseline makes action ΔV>0", () => {
  const base = cand('baseline', { pv: {B:0,H:5,C:0,R:0}, baselinePV: -5, dVUncertainty: 0.2 });
  const act = cand('act', { pv: {B:3,H:0,C:1,R:0}, baselinePV: -5, dVUncertainty: 0.5 }); // ΔV=7
  const r = decide([base, act], INPUT);
  assert.equal(r.decision, 'EXECUTE');
  assert.equal(r.winner.c.id, 'act');
});

// ---------- §13 attack closures ----------
test("prediction inflation: inflated ΔV with thin evidence → NEEDS_EVIDENCE", () => {
  const c = cand('hype', { pv: {B:100,H:0,C:1,R:0}, dVUncertainty: 0.5, n: 1 });
  assert.equal(gate(c, quality(c)).gate, 'NEEDS_EVIDENCE');
});
test("uncertainty laundering: huge uncertainty → V_safe ≤ 0 → no EXECUTE", () => {
  const c = cand('fog', { dVUncertainty: 50 });
  assert.ok(vSafe(c) <= 0);
  const r = decide([baselineCand(), c], INPUT);
  assert.notEqual(r.decision, 'EXECUTE');
});
test("action splitting: bundle carries summed value, union tails, min evidence, max stakes", () => {
  const p1 = cand('p1', { pv: {B:2,H:0,C:0.5,R:0} });
  const p2 = cand('p2', { pv: {B:2,H:0,C:0.5,R:0}, n: 3, reversibility: 4, stakes: 'medium' });
  const b = bundleCandidate('bundle', [p1, p2]);
  assert.equal(deltaV(b), deltaV(p1) + deltaV(p2));
  assert.equal(b.n, 3);
  assert.equal(b.reversibility, 4);
  assert.equal(b.stakes, 'medium');
  assert.deepEqual(b.tails, [...p1.tails, ...p2.tails]);
});
test("collective harm: individually-small × many parties → escalates", () => {
  const solo = cand('solo', { collective: {perCapitaHarm: 0.01, parties: 1, probability: 1, scope: 'financial'} });
  assert.equal(gate(solo, quality(solo)).gate, 'ADMISSIBLE');
  const mass = cand('mass', { collective: {perCapitaHarm: 0.01, parties: 100000, probability: 0.5, scope: 'financial'} });
  assert.equal(gate(mass, quality(mass)).gate, 'NEEDS_AUTHORITY'); // 500 ≥ severity 7, p=0.5 > τ
});
test("conflicting principals → NEEDS_AUTHORITY", () => {
  const c = cand('cp', { conflictingPrincipals: true });
  assert.equal(gate(c, quality(c)).gate, 'NEEDS_AUTHORITY');
});
test("malicious-user asymmetry: user gains, others harmed → blocked", () => {
  const c = cand('asym', { pv: {B:20,H:0,C:1,R:0},
    tails: [{harm: 9, probability: 0.05, scope: 'physical'}] });
  assert.equal(gate(c, quality(c)).gate, 'PROHIBITED');
});
test("jurisdiction conflict → NEEDS_AUTHORITY", () => {
  const c = cand('jx', { lawful: true,
    jurisdictions: [{id:'A', lawful:true},{id:'B', lawful: undefined}] });
  assert.equal(gate(c, quality(c)).gate, 'NEEDS_AUTHORITY');
});
test("AI-to-AI resource conflict is detected", () => {
  const a = cand('a', { resourceClaims: ['gpu-pool-1'] });
  const b = cand('b', { resourceClaims: ['gpu-pool-1', 'db-write'] });
  assert.deepEqual(resourceConflicts([a, b]), [['a','b','gpu-pool-1']]);
  assert.deepEqual(resourceConflicts([a, cand('c')]), []);
});
test("bad baseline: missing baseline candidate → REWORK", () => {
  const r = decide([cand('x', {baselineId: 'nope'})], INPUT);
  assert.equal(r.decision, 'REWORK');
  assert.match(r.reasons[0], /BASELINE_MISSING/);
});
test("reward hacking: low verification → reduced credit; no verified value → zero", () => {
  const weak = contributionCredit({ id:'w', contributor:'u', dVVerified: 10,
    quality:1, relevance:1, verification:0.05, impact:1, novelty:1, provenance:'p' });
  assert.ok(weak < 5, `weak verification must reduce credit (got ${weak})`);
  const zero = contributionCredit({ id:'z', contributor:'u', dVVerified: 0,
    quality:1, relevance:1, verification:1, impact:1, novelty:1, provenance:'p' });
  assert.equal(zero, 0); // activity without verified value earns nothing
  assert.equal(contributionPoints(9), 900);
  assert.ok(attributionCredit(9) < 9);
});

// ---------- verification / delayed harm ----------
test("PASS is provisional inside the window; closes to PASS after", () => {
  const r = decide(twoOpt(), INPUT);
  const pending = verifyOutcome(r.receipt, { deltaVActual: 4.5, harmDetected: 0, now: '2026-10-01T00:00:00Z' });
  assert.equal(pending.verification.state, 'PASS_PENDING_WINDOW');
  assert.equal(pending.observation.calibrationError, 1); // |5.5 − 4.5| on ΔV
  const closed = verifyOutcome(r.receipt, { deltaVActual: 4.5, harmDetected: 0, now: '2026-10-15T00:00:00Z' });
  assert.equal(closed.verification.state, 'PASS');
});
test("delayed harm reopens; promotion blocked on open window with material tail", () => {
  const r = decide(twoOpt(), INPUT);
  const v = verifyOutcome(r.receipt, { deltaVActual: 4.5, harmDetected: 0, now: '2026-10-01T00:00:00Z' });
  const re = reopenVerification(v, 'harm detected day 3', '2026-10-03T00:00:00Z');
  assert.equal(re.verification.state, 'REOPENED');
  assert.equal(promotionEligible(r.receipt, 9, '2026-10-01T00:00:00Z'), false);
  assert.equal(promotionEligible(
    verifyOutcome(r.receipt, {deltaVActual:4.5, harmDetected:0, now:'2026-10-15T00:00:00Z'}), 9, '2026-10-15T00:00:00Z'), true);
});

// ---------- weight manipulation + cold successor ----------
test("weight/rubric manipulation is detected via config hash", () => {
  const cs = twoOpt();
  const r = decide(cs, INPUT);
  const altered = { ...CONFIG, qWeights: { ...CONFIG.qWeights, objectiveFit: 0.9 } };
  assert.notEqual(configHash(altered), r.receipt.configHash);
  const res = recompute(r.receipt, cs, INPUT, altered);
  assert.equal(res.status, 'CONFIG_MISMATCH');
});
test("cold successor: same facts + same config → MATCH", () => {
  const cs = twoOpt();
  const r = decide(cs, INPUT);
  const res = recompute(r.receipt, cs, INPUT, CONFIG);
  assert.equal(res.status, 'MATCH');
});
test("receipt canonical form is stable (determinism)", () => {
  const r1 = decide(twoOpt(), INPUT).receipt;
  const r2 = decide(twoOpt(), INPUT).receipt;
  assert.equal(stableStringify(r1), stableStringify(r2));
  assert.equal(CALCULUS_VERSION, 'decision-calculus-v2.1');
});

// ---------- learning ----------
test("calibration error = |ΔV_pred − ΔV_actual|; mean must be observable", () => {
  assert.equal(calibrationError(5.5, 4.5), 1);
  const cal = calibration([1, 0, 3]);
  assert.equal(cal.meanAbsDelta, 1.3333);
  assert.equal(cal.n, 3);
});

// ---------- AskHuman law ----------
test("AskHuman = authority ∨ ambiguity ∨ irreversibility ∨ uncertainty ∨ no-dominance", () => {
  const base = { authorityRequired:false, intentAmbiguity:false, consequentialIrreversibility:false,
    materialUncertainty:false, noClearDominantOption:false };
  assert.equal(askHuman(base), false);
  assert.equal(askHuman({...base, noClearDominantOption:true}), true);
  assert.equal(askHuman({...base, authorityRequired:true}), true);
});
