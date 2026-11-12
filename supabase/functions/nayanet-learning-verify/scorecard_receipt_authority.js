/* NayaPOWER Scorecard Receipt Authority — learning promotion bridge.
 *
 * SN-0340 (The Scorecard Law): "If you did your scorecard honestly, you don't
 * need to ask — just do it." The Human Director designed the scale, ratified
 * the procedure, and commanded the highest honest score to act without asking.
 *
 * A valid scorecard receipt therefore carries his authority. The learning
 * promotion gate accepts EITHER a personal grant (nayanet_authority_grants)
 * OR a valid scorecard receipt meeting the law's five steps plus the
 * learning-promotion bindings below. Fail-closed: no valid receipt, no
 * promotion. The safety is not removed; its authority comes from the math.
 *
 * The five mechanical steps are ported from tools/auto_merge_gate.py
 * (_check_receipt), the law's enforcement arm, so the two gates cannot drift.
 * Written without TS annotations so the shipped block can be executed
 * verbatim in the loop's node harness.
 */

// Step 2 scoring dimensions — the law's four, in the law's words.
const RECEIPT_SCORE_DIMENSIONS = ["value", "consequences", "mission_vision_alignment", "situational_awareness"];

// Step 3 hard stops — no score overrides a failed gate.
const RECEIPT_GATE_FIELDS = ["reversible", "no_major_damage", "positive_forward_effect"];

// Learning-promotion bindings (beyond the five steps):
const RECEIPT_MAX_AGE_MS = 7 * 24 * 60 * 60 * 1000; // 7 days — matches grant expiry pattern
const RECEIPT_MIN_WINNER_AVG = 9.0;                 // nothing under 9.0 ships as done
const RECEIPT_MIN_FALSIFIER_LEN = 20;

function receiptReasons() { return []; }

function validateScorecardReceipt(receipt, intelligentBlockId, now) {
  const reasons = receiptReasons();
  const at = now instanceof Date ? now : new Date(now || Date.now());

  if (!receipt || typeof receipt !== "object" || Array.isArray(receipt)) {
    reasons.push("receipt: missing or not an object (no receipt, no promotion)");
    return { valid: false, reasons };
  }

  // ---- Binding A: scope_target must name the block being promoted.
  const scopeTarget = receipt.scope_target;
  if (typeof scopeTarget !== "string" || !scopeTarget.trim() || scopeTarget !== intelligentBlockId) {
    reasons.push("binding: scope_target must exactly match the promotion target block id");
  }

  // ---- Binding B: scope_action must be the learning lock-in action.
  if (receipt.scope_action !== "learning_lock_in") {
    reasons.push('binding: scope_action must be "learning_lock_in"');
  }

  // ---- Binding C: decided_at must exist and be within max age.
  const decidedAt = receipt.decided_at ? new Date(String(receipt.decided_at)) : null;
  if (!decidedAt || isNaN(decidedAt.getTime())) {
    reasons.push("binding: decided_at missing or unparsable");
  } else if (at.getTime() - decidedAt.getTime() > RECEIPT_MAX_AGE_MS) {
    reasons.push("binding: receipt expired (decided_at older than 7 days)");
  } else if (decidedAt.getTime() > at.getTime() + 60000) {
    reasons.push("binding: decided_at is in the future");
  }

  // ---- Binding D: decided_by must name the scorer (attribution, not anonymity).
  if (typeof receipt.decided_by !== "string" || !receipt.decided_by.trim()) {
    reasons.push("binding: decided_by missing — a receipt without a named scorer is not authority");
  }

  // ---- Step 1: ENUMERATE — >= 2 options, each with an id.
  let optionIds = [];
  const s1 = receipt.step1_enumerate;
  if (s1 && typeof s1 === "object" && Array.isArray(s1.options)) {
    if (s1.options.length < 2) {
      reasons.push("step1: must enumerate >= 2 options");
    } else {
      optionIds = s1.options.filter((o) => o && typeof o === "object" && o.id).map((o) => String(o.id));
      if (optionIds.length < 2) reasons.push("step1: each enumerated option needs an id");
    }
  } else {
    reasons.push("step1: step1_enumerate.options must be a list");
  }

  // ---- Step 2: SCORE — every option scored on all four dimensions, 0-10 numeric.
  const totals = {};
  const s2 = receipt.step2_score;
  if (s2 && typeof s2 === "object" && s2.scores && typeof s2.scores === "object") {
    for (const oid of optionIds) {
      const dims = s2.scores[oid];
      if (!dims || typeof dims !== "object") {
        reasons.push("step2: option '" + oid + "' has no score entry");
        continue;
      }
      let total = 0, ok = true;
      for (const dim of RECEIPT_SCORE_DIMENSIONS) {
        const v = dims[dim];
        if (typeof v !== "number" || isNaN(v) || v < 0 || v > 10) {
          reasons.push("step2: option '" + oid + "' dimension '" + dim + "' must be numeric 0-10");
          ok = false; break;
        }
        total += v;
      }
      if (ok) totals[oid] = total;
    }
  } else {
    reasons.push("step2: step2_score.scores must be an object keyed by option id");
  }

  // ---- Step 3: GATE — hard stops; no score overrides a failed gate.
  let gatesPass = true;
  const gates = receipt.step3_gate;
  if (gates && typeof gates === "object") {
    for (const g of RECEIPT_GATE_FIELDS) {
      if (gates[g] !== true) {
        reasons.push("step3: gate '" + g + "' is not true — hard stop, no score overrides it");
        gatesPass = false;
      }
    }
  } else {
    reasons.push("step3: step3_gate missing or not an object");
    gatesPass = false;
  }

  // ---- Step 4: DECIDE — winner is an enumerated id with the highest total.
  let winner = null;
  const s4 = receipt.step4_decide;
  if (s4 && typeof s4 === "object") {
    winner = s4.winner;
    if (!optionIds.includes(winner)) {
      reasons.push("step4: winner must match an enumerated option id");
      winner = null;
    } else if (gatesPass && Object.keys(totals).length > 0) {
      const best = Math.max(...Object.values(totals));
      if ((totals[winner] ?? -1) < best) {
        reasons.push("step4: winner does not hold the highest total score — the math decides, not the author");
      }
    }
    const alt = s4.strongest_alternative;
    if (!alt || typeof alt !== "object" || !alt.summary) {
      reasons.push("step4: strongest_alternative.summary is empty (theater check failed)");
    }
    const falsifier = s4.falsifier;
    if (typeof falsifier !== "string" || falsifier.trim().length < RECEIPT_MIN_FALSIFIER_LEN) {
      reasons.push("step4: falsifier must state concrete evidence that would prove the decision wrong");
    }
  } else {
    reasons.push("step4: step4_decide missing or not an object");
  }

  // ---- Step 5: RECEIPT — written AND posted.
  const s5 = receipt.step5_receipt;
  if (s5 && typeof s5 === "object") {
    if (!Number.isInteger(s5.receipt_posted_comment_id)) {
      reasons.push("step5: receipt_posted_comment_id missing — a private scorecard is not a gate");
    }
  } else {
    reasons.push("step5: step5_receipt missing or not an object");
  }

  // ---- Binding E: the winner must be the promotion option, at 9.0+.
  const promotionOptionId = receipt.promotion_option_id;
  if (typeof promotionOptionId !== "string" || !promotionOptionId) {
    reasons.push("binding: promotion_option_id missing — the receipt must declare which option authorizes promotion");
  } else if (winner && winner !== promotionOptionId) {
    reasons.push("binding: winner is not the promotion option — this receipt authorizes a different decision");
  }
  if (winner && totals[winner] !== undefined) {
    const avg = totals[winner] / RECEIPT_SCORE_DIMENSIONS.length;
    if (avg < RECEIPT_MIN_WINNER_AVG) {
      reasons.push("binding: winner averages " + avg.toFixed(2) + " < 9.0 — nothing under 9.0 ships as done");
    }
  }

  return { valid: reasons.length === 0, reasons };
}

// Resolve receipt authority for a promotion target. Returns the same shape as
// resolveLearningLockInLaw so the call site can treat either as authority.
function resolveScorecardReceiptAuthority(receipt, intelligentBlockId, now) {
  const at = now instanceof Date ? now : new Date(now || Date.now());
  const check = validateScorecardReceipt(receipt, intelligentBlockId, at);
  if (!check.valid) {
    return {
      authorized: false,
      reason: "INVALID_SCORECARD_RECEIPT",
      authority_refs: [],
      expires_at: null,
      receipt_reasons: check.reasons,
    };
  }
  const decidedAt = new Date(String(receipt.decided_at));
  const expiresAt = new Date(decidedAt.getTime() + RECEIPT_MAX_AGE_MS);
  return {
    authorized: true,
    reason: "VALID_SCORECARD_RECEIPT",
    authority_refs: ["receipt:" + String(receipt.decided_by || "unknown") + "@" + decidedAt.toISOString()],
    expires_at: expiresAt.toISOString(),
  };
}
// SCORECARD-RECEIPT-AUTHORITY-END

// Real ESM exports — the Deno edge function imports this module directly.
// (Review fix: the previous CommonJS-only guard left the named import
// undefined in Deno, which would have crashed the verifier's LAW gate.)
export { validateScorecardReceipt, resolveScorecardReceiptAuthority };
