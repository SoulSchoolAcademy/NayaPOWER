/**
 * Learning-candidate admission gate — MACHINE LAW (TypeScript port).
 *
 * Faithful port of tools/learning_admission_gate.py (round 2). No learning
 * candidate enters the system without passing this gate. It validates
 * experiment DESIGN at the door; it never claims that learning occurred.
 *
 * PORT CONTRACT (WO3 · WO0 caveat): every verdict must agree with the Python
 * reference on the shared fixture set (see tests/admission_gate_fixtures.json
 * and .github/workflows/wo3-admission-gate-proof.yml). If the Python reference
 * changes, this port must be re-pinned before shipping.
 *
 * ADMISSION CONTRACT (all must hold):
 *   (a) falsifiable claim — IN SUBSTANCE (negation-paraphrase tautologies reject)
 *   (b) same named task in both arms
 *   (c) pre-registered success criterion, independent of the lesson IN SUBSTANCE,
 *       registered BEFORE the first measurement (temporal check, not claimed)
 *   (d) machine / different-seat / deterministic measurement
 *   (e) doer != scorer (identity normalized: case/whitespace-insensitive)
 *   (f) honest nulls admit as NOT_VERIFIED, never as CANDIDATE
 *   (g) both arms actually measured, with parseable timestamps
 *   (h) asserts a behavioral change, not a token difference (non-nulls only)
 *
 * The gate is pure: no DB, no network. It never throws for bad input — it
 * returns REJECTED. (The fail-closed wrapper at the call site catches even
 * unexpected throws and rejects; see index.ts.)
 */

export const ADMISSION_SCHEMA = "NAYAPOWER_LEARNING_CANDIDATE_ADMISSION_V1";

export const MEASUREMENT_METHODS = new Set(["machine", "different_seat", "deterministic"]);

export const CANDIDATE = "CANDIDATE";
export const NOT_VERIFIED = "NOT_VERIFIED";
export const REJECTED = "REJECTED";

// Rejection reason codes — must stay byte-identical to the Python reference.
export const SCHEMA_MISMATCH = "SCHEMA_MISMATCH";
export const CANDIDATE_MUST_BE_OBJECT = "CANDIDATE_MUST_BE_OBJECT";
export const CLAIM_REQUIRED = "CLAIM_REQUIRED";
export const CLAIM_NOT_FALSIFIABLE = "CLAIM_NOT_FALSIFIABLE";
export const TAUTOLOGICAL_FALSIFICATION = "TAUTOLOGICAL_FALSIFICATION";
export const NO_NAMED_TASK = "NO_NAMED_TASK";
export const NO_PREREGISTERED_CRITERION = "NO_PREREGISTERED_CRITERION";
export const CRITERION_NOT_INDEPENDENT = "CRITERION_NOT_INDEPENDENT";
export const TAUTOLOGICAL_CRITERION = "TAUTOLOGICAL_CRITERION";
export const CRITERION_REGISTERED_AT_REQUIRED = "CRITERION_REGISTERED_AT_REQUIRED";
export const CRITERION_TIMESTAMP_UNPARSEABLE = "CRITERION_TIMESTAMP_UNPARSEABLE";
export const MEASURED_AT_UNPARSEABLE = "MEASURED_AT_UNPARSEABLE";
export const POST_HOC_CRITERION = "POST_HOC_CRITERION";
export const NO_MACHINE_MEASUREMENT = "NO_MACHINE_MEASUREMENT";
export const DOER_AND_SCORER_REQUIRED = "DOER_AND_SCORER_REQUIRED";
export const DOER_EQUALS_SCORER = "DOER_EQUALS_SCORER";
export const ARMS_REQUIRE_OBSERVABLE_BEHAVIOR = "ARMS_REQUIRE_OBSERVABLE_BEHAVIOR";
export const ARMS_INDIMINISHABLE = "ARMS_INDIMINISHABLE";
export const NON_EXPERIMENT_NO_MEASURED_ARMS = "NON_EXPERIMENT_NO_MEASURED_ARMS";
export const TOKEN_DIFFERENCE_NOT_BEHAVIOR = "TOKEN_DIFFERENCE_NOT_BEHAVIOR";
export const BEHAVIORAL_MEASURE_REQUIRED = "BEHAVIORAL_MEASURE_REQUIRED";
// TS-port addition: the gate itself failed to evaluate (fail-closed signal).
export const GATE_EVALUATION_ERROR = "GATE_EVALUATION_ERROR";

export interface AdmissionResult {
  admitted: boolean;
  admitted_as: string; // CANDIDATE | NOT_VERIFIED | REJECTED
  reasons: string[]; // empty when admitted; rejection codes otherwise
}

export function normalize_identity(value: unknown): string {
  // Canonical identity comparison: case- and whitespace-insensitive.
  // "Naya-5", "naya-5 " and "NAYA-5" are the same seat.
  return String(value).trim().toLowerCase();
}

function nonemptyStr(value: unknown): value is string {
  return typeof value === "string" && value.trim().length > 0;
}

function parseTs(value: unknown): Date | null {
  // Parse an ISO-8601 timestamp. Naive values are assumed UTC (per spec,
  // Date.parse treats timezone-less ISO as UTC). Null if unparseable.
  // Never throws.
  if (!nonemptyStr(value)) return null;
  const text = value.trim();
  try {
    const ms = Date.parse(text);
    if (Number.isNaN(ms)) return null;
    return new Date(ms);
  } catch {
    return null;
  }
}

// --- Substantive independence -------------------------------------------
// Port of Python difflib.SequenceMatcher.ratio() for the no-junk case.
// Inputs here are content signatures well under 200 chars, so Python's
// autojunk heuristic never engages — the plain longest-match recursion
// below is verdict-identical to the reference.

function findLongestMatch(
  a: string, b: string, b2j: Map<string, number[]>,
  alo: number, ahi: number, blo: number, bhi: number
): [number, number, number] {
  let besti = alo, bestj = blo, bestsize = 0;
  for (let i = alo; i < ahi; i++) {
    const js = b2j.get(a[i]);
    if (!js) continue;
    for (const j0 of js) {
      if (j0 < blo) continue;
      if (j0 >= bhi) break;
      let k = 1;
      while (i + k < ahi && j0 + k < bhi && a[i + k] === b[j0 + k]) k++;
      if (k > bestsize) {
        besti = i; bestj = j0; bestsize = k;
      }
    }
  }
  return [besti, bestj, bestsize];
}

function sequenceMatcherRatio(a: string, b: string): number {
  const la = a.length, lb = b.length;
  if (la + lb === 0) return 1.0;
  if (la === 0 || lb === 0) return 0.0;
  const b2j = new Map<string, number[]>();
  for (let j = 0; j < lb; j++) {
    const c = b[j];
    let arr = b2j.get(c);
    if (!arr) { arr = []; b2j.set(c, arr); }
    arr.push(j);
  }
  let matches = 0;
  const queue: [number, number, number, number][] = [[0, la, 0, lb]];
  while (queue.length > 0) {
    const [alo, ahi, blo, bhi] = queue.pop()!;
    const [i, j, k] = findLongestMatch(a, b, b2j, alo, ahi, blo, bhi);
    if (k > 0) {
      matches += k;
      if (alo < i && blo < j) queue.push([alo, i, blo, j]);
      if (i + k < ahi && j + k < bhi) queue.push([i + k, ahi, j + k, bhi]);
    }
  }
  return (2.0 * matches) / (la + lb);
}

const NEGATION_PHRASES = [
  "did not", "does not", "do not", "would not", "will not", "is not",
  "are not", "was not", "were not", "has not", "have not", "had not",
  "cannot", "could not", "should not",
];
const NEGATION_TOKENS = new Set([
  "not", "no", "never", "n't", "neither", "nor", "without", "lacks", "lack",
  "lacking", "fails", "failed", "failing", "failure", "unable", "absence",
  "absent", "against", "didnt", "doesnt", "dont", "cant", "wont",
]);
const STOPWORDS = new Set([
  "the", "a", "an", "if", "then", "of", "on", "in", "to", "for", "with",
  "and", "or", "is", "are", "was", "were", "be", "by", "as", "at", "it",
  "its", "this", "that", "these", "those", "than", "when", "where",
  "which", "what", "how", "how", "s", "t", "over", "under",
]);
const PARAPHRASE_THRESHOLD = 0.75;

function contentSignature(text: string): string {
  let lowered = text.toLowerCase();
  for (const phrase of NEGATION_PHRASES) {
    lowered = lowered.split(phrase).join(" ");
  }
  const tokens = (lowered.match(/[a-z0-9]+/g) || []).filter(
    (tok) => !NEGATION_TOKENS.has(tok) && !STOPWORDS.has(tok)
  );
  return tokens.join(" ");
}

function isNegationParaphrase(claim: string, condition: string): boolean {
  const sigClaim = contentSignature(claim);
  const sigCondition = contentSignature(condition);
  if (!sigClaim || !sigCondition) return false;
  return sequenceMatcherRatio(sigClaim, sigCondition) >= PARAPHRASE_THRESHOLD;
}

function isNullOutcome(candidate: Record<string, unknown>): boolean {
  if (String(candidate["outcome"] ?? "pending").trim().toLowerCase() === "null") return true;
  return candidate["asserts_behavioral_change"] === false;
}

function isRecord(v: unknown): v is Record<string, unknown> {
  return typeof v === "object" && v !== null && !Array.isArray(v);
}

export function admit_candidate(candidate: unknown): AdmissionResult {
  // Pure: never throws for bad input — returns REJECTED with reasons.
  if (!isRecord(candidate)) {
    return { admitted: false, admitted_as: REJECTED, reasons: [CANDIDATE_MUST_BE_OBJECT] };
  }
  const errors: string[] = [];

  if (candidate["schema"] !== ADMISSION_SCHEMA) {
    errors.push(SCHEMA_MISMATCH);
  }

  // (a) falsifiable claim — IN SUBSTANCE.
  const claim = candidate["claim"];
  const falsification = candidate["falsification_condition"];
  if (!nonemptyStr(claim)) {
    errors.push(CLAIM_REQUIRED);
  }
  if (!nonemptyStr(falsification)) {
    errors.push(CLAIM_NOT_FALSIFIABLE);
  } else if (nonemptyStr(claim) && isNegationParaphrase(claim as string, falsification as string)) {
    errors.push(TAUTOLOGICAL_FALSIFICATION);
  }

  // (b) same named task in both arms
  if (!nonemptyStr(candidate["task"])) {
    errors.push(NO_NAMED_TASK);
  }

  // (c) pre-registered success criterion, independent IN SUBSTANCE.
  const criterion = candidate["success_criterion"];
  if (!nonemptyStr(criterion)) {
    errors.push(NO_PREREGISTERED_CRITERION);
  } else {
    if (candidate["criterion_independent_of_lesson"] !== true) {
      errors.push(CRITERION_NOT_INDEPENDENT);
    }
    if (nonemptyStr(claim) && isNegationParaphrase(claim as string, criterion as string)) {
      errors.push(TAUTOLOGICAL_CRITERION);
    }
  }

  // (d) machine / different-seat / deterministic measurement
  const measurement = candidate["measurement"];
  const method = isRecord(measurement) ? measurement["method"] : undefined;
  if (typeof method !== "string" || !MEASUREMENT_METHODS.has(method)) {
    errors.push(NO_MACHINE_MEASUREMENT);
  }

  // (e) doer != scorer — identity normalized.
  const doer = candidate["doer"];
  const scorer = candidate["scorer"];
  if (!nonemptyStr(doer) || !nonemptyStr(scorer)) {
    errors.push(DOER_AND_SCORER_REQUIRED);
  } else if (normalize_identity(doer) === normalize_identity(scorer)) {
    errors.push(DOER_EQUALS_SCORER);
  }

  // (g) both arms actually measured — with parseable timestamps.
  const arms = candidate["arms"];
  const armsRec = isRecord(arms) ? arms : {};
  const treatment = isRecord(armsRec["treatment"]) ? (armsRec["treatment"] as Record<string, unknown>) : {};
  const control = isRecord(armsRec["control"]) ? (armsRec["control"] as Record<string, unknown>) : {};
  const treatmentObs = treatment["observable"];
  const controlObs = control["observable"];
  const treatmentTs = parseTs(treatment["measured_at"]);
  const controlTs = parseTs(control["measured_at"]);
  if (!nonemptyStr(treatmentObs) || !nonemptyStr(controlObs)) {
    errors.push(ARMS_REQUIRE_OBSERVABLE_BEHAVIOR);
  } else if (
    (treatmentObs as string).trim().toLowerCase() === (controlObs as string).trim().toLowerCase()
  ) {
    errors.push(ARMS_INDIMINISHABLE);
  }
  if (treatmentTs === null || controlTs === null) {
    if (!nonemptyStr(treatment["measured_at"]) || !nonemptyStr(control["measured_at"])) {
      errors.push(NON_EXPERIMENT_NO_MEASURED_ARMS);
    } else {
      errors.push(MEASURED_AT_UNPARSEABLE);
    }
  }

  // (c-temporal) criterion registered BEFORE the first measurement.
  const registeredRaw = candidate["criterion_registered_at"];
  if (!nonemptyStr(registeredRaw)) {
    errors.push(CRITERION_REGISTERED_AT_REQUIRED);
  } else {
    const registeredTs = parseTs(registeredRaw);
    if (registeredTs === null) {
      errors.push(CRITERION_TIMESTAMP_UNPARSEABLE);
    } else if (treatmentTs !== null && controlTs !== null) {
      const firstMeasured = treatmentTs < controlTs ? treatmentTs : controlTs;
      if (registeredTs >= firstMeasured) {
        errors.push(POST_HOC_CRITERION);
      }
    }
  }

  if (errors.length > 0) {
    return { admitted: false, admitted_as: REJECTED, reasons: errors };
  }

  // (f) honest nulls admit as NOT VERIFIED — after design checks, before
  // behavioral-assertion requirements.
  if (isNullOutcome(candidate)) {
    return { admitted: true, admitted_as: NOT_VERIFIED, reasons: [] };
  }

  // (h) behavioral change, not a token difference — non-nulls only.
  if (candidate["asserts_behavioral_change"] !== true) {
    errors.push(TOKEN_DIFFERENCE_NOT_BEHAVIOR);
  } else if (!nonemptyStr(candidate["behavioral_measure"])) {
    errors.push(BEHAVIORAL_MEASURE_REQUIRED);
  }

  if (errors.length > 0) {
    return { admitted: false, admitted_as: REJECTED, reasons: errors };
  }
  return { admitted: true, admitted_as: CANDIDATE, reasons: [] };
}

export function submit_learning_claim(candidate: unknown): AdmissionResult {
  // THE choke point for creating learning candidates.
  return admit_candidate(candidate);
}

export function rejection_log(candidate_id: string, result: AdmissionResult): string {
  // One-line door log for a rejected candidate.
  return `ADMISSION_REJECTED id=${candidate_id} reasons=${result.reasons.join(",")}`;
}

/** Deterministic input hash for the door log (log correlation, not security). */
export function inputHash(canonicalJson: string): string {
  // cyrb53 — deterministic across runtimes, no async crypto needed.
  let h1 = 0xdeadbeef, h2 = 0x41c6ce57;
  for (let i = 0; i < canonicalJson.length; i++) {
    const ch = canonicalJson.charCodeAt(i);
    h1 = Math.imul(h1 ^ ch, 2654435761);
    h2 = Math.imul(h2 ^ ch, 1597334677);
  }
  h1 = Math.imul(h1 ^ (h1 >>> 16), 2246822507) ^ Math.imul(h2 ^ (h2 >>> 13), 3266489909);
  h2 = Math.imul(h2 ^ (h2 >>> 16), 2246822507) ^ Math.imul(h1 ^ (h1 >>> 13), 3266489909);
  return (4294967296 * (2097151 & h2) + (h1 >>> 0)).toString(16);
}

/** Canonical JSON: sorted keys, for stable input hashes. */
export function canonicalJson(value: unknown): string {
  if (Array.isArray(value)) {
    return "[" + value.map(canonicalJson).join(",") + "]";
  }
  if (isRecord(value)) {
    const keys = Object.keys(value).sort();
    return "{" + keys.map((k) => JSON.stringify(k) + ":" + canonicalJson(value[k])).join(",") + "}";
  }
  return JSON.stringify(value) ?? "null";
}
