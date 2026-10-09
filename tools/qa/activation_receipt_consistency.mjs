// Naya activation source/receipt consistency falsifier — QA-only candidate.
// Caller MUST independently fetch the GitHub state and calculate receipt_sha256
// from the exact JSON bytes. Accepting builder-supplied "trusted" state is UNSAFE.
// CONSISTENT_FOR_INDEPENDENT_REVIEW != activated/comprehended/authorized/verified.
export function checkActivationReceipt(receipt, expected, workProduct, nowIso) {
  const violations = [];
  const sha40 = v => typeof v === "string" && /^[a-f0-9]{40}$/i.test(v);
  const sha64 = v => typeof v === "string" && /^[a-f0-9]{64}$/i.test(v);
  if (!receipt || typeof receipt !== "object" || Array.isArray(receipt)) return {readiness:"REJECT",violations:["RECEIPT_MISSING"],authorized:false,verified:false};
  if (!expected || typeof expected !== "object" || Array.isArray(expected)) return {readiness:"REJECT",violations:["TRUSTED_STATE_MISSING"],authorized:false,verified:false};
  if (receipt.schema !== "naya.activation.receipt.v2" || receipt.status !== "ACTIVATED") violations.push("WRONG_SCHEMA_OR_STATE");
  if (!receipt.session_id || !receipt.naya_identity || !receipt.human_authority || !receipt.repository) violations.push("IDENTITY_INCOMPLETE");
  if (!receipt.job || !Array.isArray(receipt.gates) || !receipt.gates.length || !receipt.proof_plan) violations.push("JOB_GATES_PROOF_MISSING");
  if (!sha40(receipt.main_sha) || !sha40(expected.main_sha) || receipt.main_sha !== expected.main_sha) violations.push("MAIN_STALE_OR_MISMATCH");
  for (const key of ["design_blob","blocks_blob"]) {
    if (!sha40(receipt.loaded?.[key]) || !sha40(expected[key]) || receipt.loaded[key] !== expected[key]) violations.push(`DOC_MISMATCH_${key.toUpperCase()}`);
  }
  for (const key of ["goals_digest","feed_digest"]) {
    if (!sha64(receipt.loaded?.[key]) || !sha64(expected[key]) || receipt.loaded[key] !== expected[key]) violations.push(`CONTEXT_MISMATCH_${key.toUpperCase()}`);
  }
  const now = Date.parse(nowIso), activated = Date.parse(receipt.activated_at);
  if (!Number.isFinite(now) || !Number.isFinite(activated)) violations.push("TIMESTAMP_INVALID");
  else if (activated > now + 120000) violations.push("FUTURE_ACTIVATION");
  else if (now - activated > 4*60*60*1000) violations.push("ACTIVATION_EXPIRED");
  if (!sha64(expected.receipt_sha256)) violations.push("RECEIPT_DIGEST_UNTRUSTED_OR_MISSING");
  else if (typeof workProduct !== "string" || !workProduct.includes(`NAYA-ACTIVATION-RECEIPT-SHA256:${expected.receipt_sha256}`)) violations.push("DELIVERABLE_RECEIPT_CITATION_MISSING");
  return {readiness:violations.length?"REJECT":"CONSISTENT_FOR_INDEPENDENT_REVIEW",violations,authorized:false,verified:false};
}
