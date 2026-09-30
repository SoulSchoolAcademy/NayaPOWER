// NAYANET VERIFY — independent recomputation of ACT idempotency (P7).
//
// The ACT executor (supabase/functions/nayanet-verified-ai-action/index.ts)
// binds its idempotency key to a persisted request fingerprint:
//   idempotencyRequestFingerprint({authority_grant_id, mission_id, action,
//     target, canonical_block_id, canonical_digest})
// VERIFY must not trust that binding on the executor's word. This module
// re-derives the expected fingerprint from the receipt's own persisted
// inputs using an independent copy of the canonicalization, and compares.
// Mismatch — or any inability to recompute — is FAIL CLOSED, never a
// silent pass.
//
// The canonicalization below is duplicated from the executor BY DESIGN:
// VERIFY does not import the executor's code path, so silent drift in the
// executor's hashing is caught here instead of inherited. The known-answer
// vector in tests pins the byte-exact canonical form.

export type ActIdempotencyInputs = {
  authority_grant_id: unknown;
  mission_id: unknown;
  action: unknown;
  target: unknown;
  canonical_block_id: unknown;
  canonical_digest: unknown;
};

export type ActIdempotencyAssessment = {
  ok: boolean;
  code: string;
  receipt_id: string | null;
  claimed_fingerprint: string | null;
  recomputed_fingerprint: string | null;
  inputs_complete: boolean;
  missing_inputs: string[];
  fingerprint_matches: boolean | null;
  receipt_is_act_execution: boolean | null;
  fail_closed: boolean;
};

// Canonical field order — MUST match the ACT executor exactly:
// authority_grant_id, mission_id, action, target, canonical_block_id,
// canonical_digest. Key order is load-bearing: it determines the hash.
const FINGERPRINT_FIELDS = [
  "authority_grant_id",
  "mission_id",
  "action",
  "target",
  "canonical_block_id",
  "canonical_digest",
] as const;

export async function recomputeActIdempotencyFingerprint(
  input: ActIdempotencyInputs,
): Promise<string> {
  const canonical = JSON.stringify({
    authority_grant_id: String(input.authority_grant_id ?? ""),
    mission_id: String(input.mission_id ?? ""),
    action: String(input.action ?? ""),
    target: String(input.target ?? ""),
    canonical_block_id: String(input.canonical_block_id ?? ""),
    canonical_digest: String(input.canonical_digest ?? ""),
  });
  const hash = await crypto.subtle.digest(
    "SHA-256",
    new TextEncoder().encode(canonical),
  );
  return Array.from(new Uint8Array(hash))
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
}

type ReceiptLike = {
  id?: unknown;
  action?: unknown;
  status?: unknown;
  evidence?: unknown;
} | null | undefined;

function evidenceObject(receipt: ReceiptLike): Record<string, unknown> {
  const evidence = (receipt as { evidence?: unknown } | null)?.evidence;
  if (Array.isArray(evidence)) {
    // Defensive: merge array-form evidence the way the causal-verify
    // runtime does, so a nonstandard receipt shape cannot slip through
    // as "missing".
    return evidence
      .filter((item) => item && typeof item === "object")
      .reduce(
        (acc, item) => ({ ...acc, ...(item as Record<string, unknown>) }),
        {} as Record<string, unknown>,
      );
  }
  return evidence && typeof evidence === "object"
    ? (evidence as Record<string, unknown>)
    : {};
}

const failed = (
  code: string,
  partial: Partial<ActIdempotencyAssessment> = {},
): ActIdempotencyAssessment => ({
  ok: false,
  code,
  receipt_id: null,
  claimed_fingerprint: null,
  recomputed_fingerprint: null,
  inputs_complete: false,
  missing_inputs: [],
  fingerprint_matches: null,
  receipt_is_act_execution: null,
  fail_closed: true,
  ...partial,
});

// Maps receipt evidence fields back to the six fingerprint inputs the ACT
// executor persisted at execute time (see nayanet-verified-ai-action
// index.ts, execute mode: evidence.authority_grant_id,
// evidence.authority_mission, evidence.requested_action,
// evidence.requested_target, evidence.canonical_block_id,
// evidence.canonical_digest).
function extractInputs(
  evidence: Record<string, unknown>,
): { inputs: ActIdempotencyInputs; missing: string[] } {
  const raw: Record<string, unknown> = {
    authority_grant_id: evidence.authority_grant_id,
    mission_id: evidence.authority_mission,
    action: evidence.requested_action,
    target: evidence.requested_target,
    canonical_block_id: evidence.canonical_block_id,
    canonical_digest: evidence.canonical_digest,
  };
  const missing = FINGERPRINT_FIELDS.filter((field) => {
    const value = raw[field];
    return value === null || value === undefined || String(value) === "";
  });
  return { inputs: raw as ActIdempotencyInputs, missing: [...missing] };
}

export async function assessActIdempotencyReceipt(
  receipt: ReceiptLike,
): Promise<ActIdempotencyAssessment> {
  const receiptId =
    receipt && typeof receipt.id !== "undefined" && receipt.id !== null
      ? String(receipt.id)
      : null;

  if (!receipt) {
    return failed("RECEIPT_NOT_FOUND", { receipt_id: receiptId });
  }

  const isActExecution =
    String(receipt.action ?? "") === "NAYA-NODE-0001-VERIFIED-AI-ACTION";
  if (!isActExecution) {
    return failed("NOT_AN_ACT_EXECUTION_RECEIPT", {
      receipt_id: receiptId,
      receipt_is_act_execution: false,
    });
  }

  if (String(receipt.status ?? "") !== "SUCCESS") {
    return failed("RECEIPT_NOT_SUCCESSFUL", {
      receipt_id: receiptId,
      receipt_is_act_execution: true,
    });
  }

  const evidence = evidenceObject(receipt);
  const claimed = String(evidence.idempotency_request_fingerprint ?? "");
  if (!claimed) {
    // The fingerprint is the entire basis of the idempotency claim. A
    // receipt without one cannot be verified — fail closed, never assume
    // the executor bound it correctly.
    return failed("FINGERPRINT_NOT_PERSISTED", {
      receipt_id: receiptId,
      receipt_is_act_execution: true,
      claimed_fingerprint: null,
    });
  }

  const { inputs, missing } = extractInputs(evidence);
  if (missing.length > 0) {
    // Cannot re-derive the expected key without all six inputs. A
    // partial recomputation would be a guess, not a verification.
    return failed("FINGERPRINT_INPUTS_INCOMPLETE", {
      receipt_id: receiptId,
      receipt_is_act_execution: true,
      claimed_fingerprint: claimed,
      inputs_complete: false,
      missing_inputs: missing,
    });
  }

  const recomputed = await recomputeActIdempotencyFingerprint(inputs);
  const matches = recomputed === claimed;
  if (!matches) {
    return {
      ok: false,
      code: "IDEMPOTENCY_FINGERPRINT_MISMATCH",
      receipt_id: receiptId,
      claimed_fingerprint: claimed,
      recomputed_fingerprint: recomputed,
      inputs_complete: true,
      missing_inputs: [],
      fingerprint_matches: false,
      receipt_is_act_execution: true,
      fail_closed: true,
    };
  }

  return {
    ok: true,
    code: "ACT_IDEMPOTENCY_RECOMPUTED",
    receipt_id: receiptId,
    claimed_fingerprint: claimed,
    recomputed_fingerprint: recomputed,
    inputs_complete: true,
    missing_inputs: [],
    fingerprint_matches: true,
    receipt_is_act_execution: true,
    fail_closed: false,
  };
}
