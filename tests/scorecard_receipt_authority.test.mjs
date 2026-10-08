/* Tests for scorecard receipt authority (learning promotion bridge).
 * Run: node tests/scorecard_receipt_authority.test.mjs
 * Fail-closed: every invalid receipt shape must validate false.
 */
import { validateScorecardReceipt, resolveScorecardReceiptAuthority } from "../supabase/functions/nayanet-learning-verify/scorecard_receipt_authority.js";

let passed = 0, failed = 0;
function check(name, cond) {
  if (cond) { passed++; }
  else { failed++; console.error("FAIL:", name); }
}

function goodReceipt() {
  return {
    scope_target: "IB-TEST-001",
    scope_action: "learning_lock_in",
    decided_at: new Date().toISOString(),
    decided_by: "naya-5",
    promotion_option_id: "promote",
    step1_enumerate: { options: [{ id: "promote" }, { id: "hold" }, { id: "reject" }] },
    step2_score: {
      scores: {
        promote: { value: 9, consequences: 9, mission_vision_alignment: 10, situational_awareness: 9 },
        hold:    { value: 6, consequences: 6, mission_vision_alignment: 6, situational_awareness: 6 },
        reject:  { value: 3, consequences: 4, mission_vision_alignment: 3, situational_awareness: 4 },
      },
    },
    step3_gate: { reversible: true, no_major_damage: true, positive_forward_effect: true },
    step4_decide: {
      winner: "promote",
      strongest_alternative: { summary: "Hold for one more verification cycle to reduce residual uncertainty." },
      falsifier: "A cold successor trial showing zero or negative delta attributable to this lesson.",
    },
    step5_receipt: { receipt_posted_comment_id: 1234567890 },
  };
}

const NOW = new Date();

// 1. Valid receipt authorizes.
{
  const r = resolveScorecardReceiptAuthority(goodReceipt(), "IB-TEST-001", NOW);
  check("valid receipt authorizes", r.authorized === true && r.reason === "VALID_SCORECARD_RECEIPT");
}

// 2. Scope mismatch denies.
{
  const rec = goodReceipt();
  const r = resolveScorecardReceiptAuthority(rec, "IB-OTHER-999", NOW);
  check("scope mismatch denies", r.authorized === false);
  check("scope mismatch reason", r.reason === "INVALID_SCORECARD_RECEIPT");
}

// 3. Expired receipt denies.
{
  const rec = goodReceipt();
  rec.decided_at = new Date(Date.now() - 8 * 24 * 60 * 60 * 1000).toISOString();
  const r = resolveScorecardReceiptAuthority(rec, "IB-TEST-001", NOW);
  check("expired receipt denies", r.authorized === false);
}

// 4. Winner not the promotion option denies.
{
  const rec = goodReceipt();
  rec.step4_decide.winner = "hold";
  // re-score so hold wins honestly
  rec.step2_score.scores.hold = { value: 10, consequences: 10, mission_vision_alignment: 10, situational_awareness: 10 };
  const v = validateScorecardReceipt(rec, "IB-TEST-001", NOW);
  check("non-promote winner denies", v.valid === false);
  check("non-promote winner reason mentions binding", v.reasons.some((x) => x.includes("not the promotion option")));
}

// 5. Winner under 9.0 denies.
{
  const rec = goodReceipt();
  rec.step2_score.scores.promote = { value: 8, consequences: 8, mission_vision_alignment: 8, situational_awareness: 8 };
  // hold/reject must stay below promote so winner math holds
  const v = validateScorecardReceipt(rec, "IB-TEST-001", NOW);
  check("sub-9.0 winner denies", v.valid === false);
  check("sub-9.0 reason mentions 9.0", v.reasons.some((x) => x.includes("9.0")));
}

// 6. Failed gate denies (no score overrides).
{
  const rec = goodReceipt();
  rec.step3_gate.no_major_damage = false;
  const v = validateScorecardReceipt(rec, "IB-TEST-001", NOW);
  check("failed gate denies", v.valid === false);
}

// 7. Winner not highest scorer denies (math decides, not author).
{
  const rec = goodReceipt();
  rec.step2_score.scores.hold = { value: 10, consequences: 10, mission_vision_alignment: 10, situational_awareness: 10 };
  const v = validateScorecardReceipt(rec, "IB-TEST-001", NOW);
  check("non-highest winner denies", v.valid === false);
}

// 8. Missing posted comment denies (private scorecard is not a gate).
{
  const rec = goodReceipt();
  delete rec.step5_receipt.receipt_posted_comment_id;
  const v = validateScorecardReceipt(rec, "IB-TEST-001", NOW);
  check("unposted receipt denies", v.valid === false);
}

// 9. Thin falsifier denies (theater check).
{
  const rec = goodReceipt();
  rec.step4_decide.falsifier = "bad";
  const v = validateScorecardReceipt(rec, "IB-TEST-001", NOW);
  check("thin falsifier denies", v.valid === false);
}

// 10. Anonymous scorer denies.
{
  const rec = goodReceipt();
  rec.decided_by = "";
  const v = validateScorecardReceipt(rec, "IB-TEST-001", NOW);
  check("anonymous scorer denies", v.valid === false);
}

// 11. Wrong action denies.
{
  const rec = goodReceipt();
  rec.scope_action = "merge";
  const v = validateScorecardReceipt(rec, "IB-TEST-001", NOW);
  check("wrong scope_action denies", v.valid === false);
}

// 12. Non-object receipt denies.
{
  const v = validateScorecardReceipt(null, "IB-TEST-001", NOW);
  check("null receipt denies", v.valid === false);
}

console.log(`\n${passed} passed, ${failed} failed`);
process.exit(failed ? 1 : 0);
