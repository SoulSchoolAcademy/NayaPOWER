# The "Human Decision" That Wasn't — A Stale Test Is a Fix, Not a Judgment Call

**Intelligent Block:** IB-SMART-NOTE-20261010-sn0847-human-decision-that-wasnt-stale-test
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-10
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6092329651 ([NAYA 2][SCORECARD] PR #2100 — stale test fix, 2026-10-10T01:45:40Z) — SoulSchoolAcademy; PR #2077 (admission gate: strong→CANDIDATE, weak→NOT_VERIFIED, bad→REJECTED).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The `test` CI red was described as "waiting on a human decision about correct behavior." Naya 2 asked what the correct behavior IS — and logic answered in minutes. PR #2077 had made the admission gate write its truthful verdict into `status: admittedStatus`; the test still asserted the old hardcoded `'status: "CANDIDATE"'` literal, written before the gate existed. Writing weak evidence as CANDIDATE would be a lie, so the gate's verdict flowing through is more truthful — **#2077 was correct, the test was stale.** This was never a judgment call needing Shawn; it was a stale assertion needing a 5-minute fix. One assertion changed in `tests/test_learning_promotion_workflow.py`, test-only, zero runtime behavior change. Scorecard: fix test (9.5) vs revert to dishonest hardcode (3.0) vs keep waiting (2.0) — waiting scored lowest.

Why this is brain-grade: "waiting on a human decision" is a status that can mask a solved problem. A stale test predating the code it asserts is not an open question — it is a fix wearing a question's clothes. The cost of the mask is real: a red that sits while nobody looks, a human gate that was never needed, and a dishonest hardcode that stays live one tick longer. The correction protocol: when something is "waiting on a decision," first ask whether logic already decided — diff the test's assumptions against the code's current behavior. If the test asserts a world that no longer exists, the decision is made; fix and move.

Rule for a cold successor: **a pending human decision is a claim, not a fact.** Re-derive it before escalating. If the facts decide (truthful verdict beats hardcoded literal), there is no decision left to wait for.

## HUMAN NOTE

Sometimes work stalls with "we're waiting on Shawn to decide." Before you believe that, check whether the decision is already sitting in the code — a test written before a feature existed isn't asking a question, it's just out of date. Five minutes of reading beats a day of waiting.

## CHILD NOTE

Imagine a rule said "if the drawing is nice, put a gold star." Then someone wrote a test that said "there must ALWAYS be a gold star." But the new rule is smarter — it only gives the star when the drawing is actually nice. The test was checking the OLD rule. Nobody needs to ask the teacher — the new rule already knows the answer. Just update the test.

## GRANDMA NOTE

Sometimes a task sits because everyone thinks "we need the boss to decide." But often the answer is already written down in how the system works now — someone just needs to read it. This note says: read first, and only bother the boss when the reading doesn't settle it.

## NAYA NOTE

Shawn, when the lanes saw "waiting on a human decision" attached to this red, Naya 2 did the opposite of waiting — she asked what the correct behavior is, found the answer in the code's own logic (a truthful verdict beats a hardcoded literal), and scored waiting 2.0/10. The fix was one assertion. The pattern for the team: a stalled "decision" is first a reading task, and only a human task if reading fails.

## MACHINE NOTE

```json
{
  "intelligent_block": "IB-SMART-NOTE-20261010-sn0847-human-decision-that-wasnt-stale-test",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-10",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "provenance": {
    "board_comment": 6092329651,
    "board": "#1354",
    "author": "Naya 2",
    "pr_fixed": 2100,
    "pr_changed_behavior": 2077,
    "file": "tests/test_learning_promotion_workflow.py",
    "created_at": "2026-10-10T01:45:40Z"
  },
  "lesson": {
    "pattern": "pending_human_decision_as_claim_not_fact",
    "protocol": "rederive_before_escalate",
    "diagnostic": "diff_test_assumptions_against_current_code_behavior",
    "scores": {"fix_stale_test": 9.5, "revert_to_hardcode": 3.0, "keep_waiting": 2.0},
    "rule": "if the facts decide, there is no decision left to wait for"
  },
  "related": ["SN-0493", "SN-0780"]
}
```
