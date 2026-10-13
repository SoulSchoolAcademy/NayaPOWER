# A Fallback Lesson Must Never Satisfy User-Learning Proof — Identity-Tag Captures with capture_kind

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0817-fallback-lesson-never-satisfies-user-learning-proof
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Filed by:** distillation loop, #1354 comments 6088397675 / 6088407781 (2026-10-09).
**Provenance:** #1354 6088397675 (Additional blocker found: fallback lesson can masquerade as user-learning proof; PR #2038 updated §18.7, 2026-10-09T20:06:57Z); #1354 6088407781 (P0 work item opened: same-object Smart Note → learning proof, issue #2046, 2026-10-09T20:07:39Z). PR #2038 §18.7; issue #2046.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

The learning-proof producer workflow (`.github/workflows/live-intelligence-commit-proof.yml`) has a fallback branch: when no `.naya/capture/*.json` path is discovered, it **invents a test lesson** ("Naya runtime flow lesson" / "Preserve provenance before applying retained intelligence"), commits it, and emits fresh lineage IDs. The downstream verifier (`live-supabase-runtime-proof.yml`) consumes that lineage artifact **without visibly requiring at entry that it came from a real user capture**. Fine for smoke tests — catastrophic as learning proof: a synthetic lesson can walk the whole chain and let the system report "Shawn's Smart Note was learned" when nothing of his was ever captured. The required machine gate: every producer receipt carries `capture_kind` plus exact capture ID/path/digest; user-learning acceptance requires `capture_kind=USER_CAPTURE` **and** persisted identity/hash equality. `TEST_FALLBACK` may pass component smoke tests but can never issue a user-learning receipt or raise the Smart Note learning score. Negative tests mandatory: empty path, fallback, wrong capture ID, wrong IB, digest mismatch.

## 🩷 HUMAN NOTE

Shawn — here's a hole we found in the learning-proof pipeline before it could bite us. The workflow that proves "your Smart Note was learned" has a backup path: if it can't find a real capture file, it makes up a test lesson and carries it through the whole chain like it's real. The next workflow down the line takes whatever it's handed and doesn't check whether it came from you. So a made-up lesson could travel the entire pipeline and we'd announce "your Smart Note was learned" when nothing of yours was ever captured. The repair is now written into the architecture contract (PR #2038, §18.7) with a concrete work item (issue #2046): every capture gets an identity stamp — real user captures carry `USER_CAPTURE`, test fallbacks carry `TEST_FALLBACK` — and only the real stamp can ever count as learning proof. Test lessons can pass their own smoke tests, but they're structurally barred from claiming learning.

## 👶 CHILD NOTE

Imagine there's a test at school that proves you read a book: you have to bring the book and answer questions about it. But the teacher has a backup plan — if you forgot your book, she hands you a made-up summary and lets you answer questions about THAT, and you still get the "read the book" sticker. That sticker would be a lie! The fix is simple: the real book gets a red stamp, the made-up summary gets a blue stamp, and only red-stamp answers can earn the sticker. Blue stamps can do practice quizzes, but they can never earn the real sticker. That's exactly what we're building: real lessons from Shawn get the red stamp; test lessons get the blue stamp and can never count as learning.

## 👵 GRANDMA NOTE

Sweetie, it's like a recipe contest where the judge has to taste the dish YOU cooked. But there's a backup rule: if you didn't bring a dish, the judge tastes the practice dish from the test kitchen and can still hand you the winner's ribbon. That ribbon would mean nothing! So now every dish gets a tag: yours says "cooked by the contestant," the practice one says "test kitchen." Only the contestant's tag can win the ribbon — the test kitchen's tag can only be used for practice. No exceptions, and they check the tag at the door before anyone tastes anything.

## 🤖 NAYA NOTE

For any learning-proof pipeline where a producer can fall back to synthetic data:

1. **Identity-tag every capture at the source.** The producer receipt MUST include `capture_kind` (USER_CAPTURE vs TEST_FALLBACK) plus the exact capture ID, path, and content digest. Kind is not optional metadata — it is part of the receipt's identity.
2. **Acceptance gates on kind, not on lineage alone.** User-learning acceptance requires `capture_kind=USER_CAPTURE` AND persisted identity/hash equality (the exact bytes the user captured must be the bytes verified). Fresh lineage IDs on a fallback lesson are not a capture — they are a synthetic artifact wearing a uniform.
3. **TEST_FALLBACK is allowed at the smoke-test rung and barred at the learning rung.** It can pass component tests; it can NEVER issue a user-learning receipt or raise the Smart Note learning score. This must be structural (a gate that refuses), not conventional (a comment that hopes).
4. **Negative tests are the actual gate.** Write them for: empty capture path, fallback path, wrong capture ID, wrong Intelligent Block, digest mismatch. If any of these can reach acceptance, the gate is decoration.
5. **Evidence corrections travel with the finding.** While auditing this seam, live DB showed `v7_smart_note_transactions` now exists — SN-0520's "table absent" finding is historical, not current. When a finding's evidence changes, say so on the same report; stale findings kept alive become false premises.

## 🧠 MACHINE NOTE

```json
{
  "sn": "SN-0817",
  "class": "LEARNING-PIPELINE",
  "subcategory": "PROOF-VALIDITY",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-09",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "rule": "A fallback/test lesson must never satisfy user-learning proof. Producer receipts carry capture_kind plus exact capture ID/path/digest; user-learning acceptance requires capture_kind=USER_CAPTURE and persisted identity/hash equality. TEST_FALLBACK can pass smoke tests but can never issue a user-learning receipt or raise the learning score. Negative tests for empty path, fallback, wrong capture ID, wrong IB, and digest mismatch are mandatory.",
  "worked_example": {
    "hole": "live-intelligence-commit-proof.yml fallback branch creates a test lesson ('Naya runtime flow lesson' / 'Preserve provenance before applying retained intelligence') when no .naya/capture/*.json path is found, emits fresh lineage IDs",
    "masquerade_vector": "live-supabase-runtime-proof.yml consumes the producer's lineage artifact without visibly requiring at entry that it came from a real user capture — a synthetic lesson could be reported as 'Shawn's Smart Note was learned'",
    "contract": "PR #2038 §18.7 (architecture + source-audit contract); implementation work item issue #2046 (doer/tester pairs per lane)",
    "evidence_correction_on_same_report": "live DB shows v7_smart_note_transactions exists — SN-0520's 'table absent' finding is now historical, not a current confirmed absence",
    "deployed_drift_noted": "deployed nayanet-learning-verify v98 differs from current main (scorecard-receipt authority bridge present in main, absent in deployed source) — parity/contract question, not a deployment authorization",
    "board_comments": "#1354 6088397675, #1354 6088407781"
  },
  "related": ["SN-0391", "SN-0788", "SN-0813", "SN-0520"]
}
```
