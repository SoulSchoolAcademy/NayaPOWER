# IB-SMART-NOTE — SN-0579 — NaN Compares False to Everything: Finiteness Is the Gate

Intelligent Block: IB-SMART-NOTE-20261007-sn0579-nan-comparisons-false-finiteness-is-the-gate
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-07
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## IN A NUTSHELL
Every comparison against NaN is False — so a range check like `v < 0 or v > 10` silently PASSES a NaN score. Any gate that validates untrusted numbers must require `math.isfinite(v)` (or its equivalent), not just range bounds. A fabricated scorecard with NaN scores walked straight through the merge gate's step-2 check.

## HUMAN NOTE
The Scorecard Law's enforcement arm (`tools/auto_merge_gate.py`, step 2) checked scores with `v < 0 or v > 10`. The SAFETY red-team (2026-10-07) found that NaN slips through: NaN < 0 is False, NaN > 10 is False, so the check says "fine" — the total becomes NaN and the winner check passes too. In other words, a scorecard full of fake NaN scores would have authorized a merge. The fix was one line: require `math.isfinite(v)` in the loop. Six regression tests (NaN/Inf cases) green; repair landed as PR #1780 (CANDIDATE, not merged). This is the kind of bug that passes every eyeball review — the code reads correctly until you remember NaN's special rule.

## CHILD NOTE
Imagine a rule: "nobody under 5 feet or over 7 feet can ride." Now someone shows up and says their height is "I don't know." The rule checks: are they under 5? The answer is "I don't know." Are they over 7? "I don't know." The rule shrugs and lets them ride — even though they might be 3 feet tall. You have to check FIRST whether the number is even real before you measure it.

## GRANDMA NOTE
Honey, when you check whether a number is in range, first check whether it's a number at all. "I don't know" is not between 0 and 10, and it certainly isn't safe to approve.

## NAYA NOTE
Standing validation doctrine: every numeric gate on untrusted input is a two-part check — (1) `math.isfinite(v)` (rejects NaN, ±Inf), then (2) the range check. Never write the range check alone. This applies to scorecards, merge gates, thresholds, weights, anything where a fabricated input could authorize an action. The red-team pattern generalizes: when you write a validator, hand it to the adversarial seat (or your own adversarial pass) and ask "how would I sneak a bad value through this?" — the NaN bypass survived exactly because nobody asked. Evidence: #1354 comment 6047695918, PR #1780, found by SAFETY red-team 2026-10-07, repaired under SN-0575 proactive fix authority.

## MACHINE NOTE
{
  "smart_note_id": "SN-0579",
  "intelligent_block_id": "IB-SMART-NOTE-20261007-sn0579-nan-comparisons-false-finiteness-is-the-gate",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "category": "SYSTEM_INTELLIGENCE",
  "topic": "GOVERNANCE",
  "subtopic": "SECURITY_POSTURE",
  "captured_at": "2026-10-07",
  "rule": "numeric_gates_require_finiteness_first",
  "pattern": "isfinite(v) before range check v in [lo, hi]",
  "finding": "tools/auto_merge_gate.py step-2 range check `v < 0 or v > 10` passes NaN (all NaN comparisons are False); NaN total then passes winner check",
  "repair": "require math.isfinite(v) in step-2 loop; 6/6 regression tests green; PR #1780",
  "evidence": {
    "board_comment": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/1354#issuecomment-6047695918",
    "pr": "https://github.com/SoulSchoolAcademy/NayaPOWER/pull/1780",
    "found_by": "SAFETY red-team",
    "found_at": "2026-10-07"
  }
}
