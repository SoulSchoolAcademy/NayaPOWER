// admission_contract.ts — Admission contract for system-captured learning candidates.
//
// TypeScript port of the canonical Python machine law in
// kernel/protocol/learning_capture.py (check_admission). Rule identifiers are
// IDENTICAL across both implementations so a verdict from either side is
// comparable. If the two ever disagree, the Python module is canonical and
// this file must be brought back into sync — see
// BRAIN/07-LEARNING/ADMISSION-CONTRACT-HANDOFF.md.
//
// A system-captured candidate may enter CANDIDATE status only if its
// preregistered experiment design passes ALL seven rules. A candidate that
// fails ANY rule is REJECTED — never admitted. Fail-closed: no named task +
// no pre-registered criterion + no machine check => do not admit.
//
// This port applies ONLY to the system path (nayanet-learning-verify,
// provenance OBSERVATION). The human-director-verified instant path and the
// v7-smart-note-canonical Receiver path are separate lanes and are never
// gated by this contract.

export const RULE_FALSIFIABLE = "falsifiable_claim";
export const RULE_SAME_TASK = "same_named_task";
export const RULE_PREREGISTERED = "preregistered_criterion";
export const RULE_MEASUREMENT = "machine_measurement";
export const RULE_DOER_SCORER = "doer_scorer_separation";
export const RULE_NULL = "null_not_verified";
export const RULE_REPLICATION = "replication_gate";

export const ADMISSION_RULES: string[] = [
  RULE_FALSIFIABLE,
  RULE_SAME_TASK,
  RULE_PREREGISTERED,
  RULE_MEASUREMENT,
  RULE_DOER_SCORER,
  RULE_NULL,
  RULE_REPLICATION,
];

export const REPLICATIONS_REQUIRED = 3;

export interface AdmissionDesign {
  claim?: unknown;
  named_task_id?: unknown;
  control_task_id?: unknown;
  treatment_task_id?: unknown;
  control_description?: unknown;
  treatment_description?: unknown;
  preregistered_criterion?: unknown;
  preregistered_at?: unknown;
  arms_ran_at?: unknown;
  measurement?: unknown;
  doer_seat?: unknown;
  scorer_seat?: unknown;
  outcome?: unknown;
  measured_capability_delta?: unknown;
  replications_on_unseen_tasks?: unknown;
}

export interface AdmissionVerdict {
  passed: boolean;
  failed_rules: string[];
  reasons: string[];
}

const APPLIED_LESSON_RE =
  /appl(ied|y|ication)(\s+of)?(\s+the)?(\s+retained)?\s+(lesson|intelligence)/i;
const NO_APPLY_RE =
  /did\s+not\s+apply|without(\s+the|\s+applying)?(\s+retained)?\s+(lesson|intelligence)|no\s+lesson\s+applied/i;
const TOKEN_DIFF_RE =
  /different\s+(tokens?|outputs?|output)|tokens?\s+differ|outputs?\s+differ|emits?\s+different|output\s+differs/i;
const METRIC_RE =
  /provenance_preserved|governed_autonomy_applied|accuracy|success\s+rate|\bpass(es|ed|ing)?\b|increas\w*|decreas\w*|reduc\w*|improv\w*|preserv\w*|≥|>=|>|\b\d+\s*%|rate\b|score\b|metric\b/i;

const str = (v: unknown): string =>
  typeof v === "string" ? v : "";

function namesObservable(d: AdmissionDesign): boolean {
  const claim = str(d.claim).toLowerCase();
  const named = str(d.named_task_id).trim().toLowerCase();
  if (named && claim.includes(named)) return true;
  return METRIC_RE.test(claim);
}

function ruleFalsifiable(d: AdmissionDesign): [boolean, string] {
  const claim = str(d.claim).trim();
  if (claim.length < 12) {
    return [false, "falsifiable_claim: claim is vacuous — no observable outcome is stated that could be false."];
  }
  if (TOKEN_DIFF_RE.test(claim)) {
    return [false, "falsifiable_claim: definitional token change — the claim only asserts the arms emitted different tokens/output. That is true by construction of the arms, not a capability delta that could be false (SN-042: measure capability delta)."];
  }
  const treatmentIsApplication = APPLIED_LESSON_RE.test(str(d.treatment_description));
  const controlIsNonApplication = NO_APPLY_RE.test(str(d.control_description));
  if (treatmentIsApplication && controlIsNonApplication && !namesObservable(d)) {
    return [false, "falsifiable_claim: tautology — the treatment arm is defined as 'applied the lesson' and the claim asserts only that behavior differs. That tests obedience, not learning; the predicted outcome is entailed by the arm assignment and cannot be false."];
  }
  if (!namesObservable(d)) {
    return [false, "falsifiable_claim: the claim names no observable outcome on the named task — nothing measurable is stated that could be false."];
  }
  return [true, ""];
}

function ruleSameTask(d: AdmissionDesign): [boolean, string] {
  const named = str(d.named_task_id).trim();
  const control = str(d.control_task_id).trim();
  const treatment = str(d.treatment_task_id).trim();
  if (!named || !control || !treatment) {
    return [false, "same_named_task: no named task — treatment and control must attempt the identical named task; at least one arm has no task."];
  }
  if (!(control === treatment && treatment === named)) {
    return [false, `same_named_task: arms diverge — treatment=${JSON.stringify(treatment)} control=${JSON.stringify(control)} named=${JSON.stringify(named)}. Both arms must attempt the identical named task.`];
  }
  return [true, ""];
}

function parseTs(v: unknown): number | null {
  if (typeof v !== "string" || !v.trim()) return null;
  const t = Date.parse(v.trim());
  return Number.isNaN(t) ? null : t;
}

function rulePreregistered(d: AdmissionDesign): [boolean, string] {
  const criterion = str(d.preregistered_criterion).trim();
  if (criterion.length < 8) {
    return [false, "preregistered_criterion: no success criterion was written before the arms ran — fail closed."];
  }
  if (criterion === str(d.claim).trim()) {
    return [false, "preregistered_criterion: the 'criterion' merely restates the claim — it is not an independent success statement."];
  }
  const preregistered = parseTs(d.preregistered_at);
  const ran = parseTs(d.arms_ran_at);
  if (preregistered === null || ran === null) {
    return [false, "preregistered_criterion: preregistered_at/arms_ran_at missing or unparseable — cannot prove the criterion predates the arms; fail closed."];
  }
  if (!(preregistered < ran)) {
    return [false, `preregistered_criterion: the criterion was not written before the arms ran (preregistered_at=${JSON.stringify(d.preregistered_at)} arms_ran_at=${JSON.stringify(d.arms_ran_at)}).`];
  }
  return [true, ""];
}

function ruleMeasurement(d: AdmissionDesign): [boolean, string] {
  const m = str(d.measurement).trim().toLowerCase();
  if (m === "machine" || m === "different_seat" || m === "deterministic") return [true, ""];
  if (m === "self_report" || m === "self-report" || m === "claimant") {
    return [false, "machine_measurement: the outcome was scored by the claimant's own report — self-attestation is not measurement (SN-042: independence must be real)."];
  }
  return [false, "machine_measurement: no machine, different-seat, or deterministic measurement declared — fail closed."];
}

function ruleDoerScorer(d: AdmissionDesign): [boolean, string] {
  const doer = str(d.doer_seat).trim();
  const scorer = str(d.scorer_seat).trim();
  if (!doer || !scorer) {
    return [false, "doer_scorer_separation: doer and scorer seats must both be named — unnamed scoring is not independent."];
  }
  if (doer.toLowerCase() === scorer.toLowerCase()) {
    return [false, `doer_scorer_separation: doer and scorer are the same seat (${JSON.stringify(doer)}) — the scorer must differ from the doer.`];
  }
  return [true, ""];
}

function ruleNull(d: AdmissionDesign): [boolean, string] {
  const outcome = str(d.outcome).trim().toLowerCase();
  if (outcome === "null") {
    return [false, "null_not_verified: the experiment returned a null result (behavioral_change:false). A null is kept as negative evidence — it is never verification and cannot enter CANDIDATE."];
  }
  if (outcome !== "positive") {
    return [false, `null_not_verified: no positive outcome was measured (outcome=${JSON.stringify(d.outcome ?? "")}) — nothing ran or nothing was found; not admittable.`];
  }
  if (d.measured_capability_delta !== true) {
    return [false, "null_not_verified: no measured capability delta — an observed output difference without a capability delta is not learning (SN-042: measure capability delta, not output difference)."];
  }
  return [true, ""];
}

function ruleReplication(d: AdmissionDesign): [boolean, string] {
  const n = typeof d.replications_on_unseen_tasks === "number" ? d.replications_on_unseen_tasks : 0;
  if (n >= REPLICATIONS_REQUIRED) return [true, ""];
  return [false, `replication_gate: ${n} replication(s) on unseen tasks; ${REPLICATIONS_REQUIRED} required before a candidate may be admitted.`];
}

const PREDICATES: Array<[string, (d: AdmissionDesign) => [boolean, string]]> = [
  [RULE_FALSIFIABLE, ruleFalsifiable],
  [RULE_SAME_TASK, ruleSameTask],
  [RULE_PREREGISTERED, rulePreregistered],
  [RULE_MEASUREMENT, ruleMeasurement],
  [RULE_DOER_SCORER, ruleDoerScorer],
  [RULE_NULL, ruleNull],
  [RULE_REPLICATION, ruleReplication],
];

/** Run the admission contract. Fails closed on a missing/malformed design. */
export function checkAdmission(design: unknown): AdmissionVerdict {
  if (!design || typeof design !== "object" || Array.isArray(design)) {
    return {
      passed: false,
      failed_rules: [...ADMISSION_RULES],
      reasons: ["admission bundle missing or malformed — fail closed: no design, no CANDIDATE."],
    };
  }
  const d = design as AdmissionDesign;
  const failed_rules: string[] = [];
  const reasons: string[] = [];
  for (const [ruleId, predicate] of PREDICATES) {
    const [ok, reason] = predicate(d);
    if (!ok) {
      failed_rules.push(ruleId);
      reasons.push(reason);
    }
  }
  return { passed: failed_rules.length === 0, failed_rules, reasons };
}
