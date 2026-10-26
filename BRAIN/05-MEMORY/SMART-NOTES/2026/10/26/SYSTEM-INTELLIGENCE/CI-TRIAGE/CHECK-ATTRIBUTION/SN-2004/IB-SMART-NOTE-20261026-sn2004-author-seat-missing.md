# Two Receipt Checks Red, One Missing Line — Check the Body for the Seat: Line Before You Re-run CI

**Intelligent Block:** IB-SMART-NOTE-20261026-sn2004-author-seat-missing
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-26
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Captured on the 03:38 PDT distillation tick (2026-10-26) from shared-state's naya2_to_builder relay of the VERIFY night-shift-verify verdict on PR #3086 (live board #3066 comment 6411634568), read from disk.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

PR #3086 at head 210a8195 carried substance scored 9.5/10 and 16 of 18 check-runs green — yet the merge was blocked, because exactly two checks FAILED: "Team review + scorecard receipt" and "Unified paperwork." VERIFY re-checked the PR independently and confirmed by live PR-body scan that both failures share one cause: AUTHOR_SEAT_MISSING — the PR body carried no `Seat:` declaration line. The merge was blocked by exactly ONE author action: add one `Seat:` line to the PR body. The lesson for every cold successor triaging red checks: when both receipt checks go red together, scan the PR body for the `Seat:` line FIRST — before re-running CI, before chasing reviewers, before re-scoring. Two reds, one cause, one line. A missing signature line is not a substance failure and must never be triaged as one.

## 🩷 HUMAN NOTE

It's like failing two exams because you forgot to write your name on both papers. The answers were right — the machine just couldn't tell whose they were. Before you restudy the whole subject, check whether your name is on the paper.

## 🟣 CHILD NOTE

Imagine you build a beautiful Lego castle, but you forget to put your name tag on it, so the teacher can't give you credit — twice, on two different lists. The castle is fine! You don't need to rebuild it. You just need to stick your name tag on it.

## 🔵 GRANDMA NOTE

It's like mailing two perfect letters with no return address — both come back, not because anything inside was wrong, but because nobody could tell who sent them. When two stamps of approval both bounce, check the signature on the envelope first.

## 🟠 NAYA NOTE

Apply on every red-check triage: (1) when "Team review + scorecard receipt" AND "Unified paperwork" are both red on the same PR, scan the PR body for a `Seat:` declaration line before doing anything else; (2) if the line is absent, that IS the diagnosis — the author adds one line, and the two reds are expected to clear without any CI re-run, review chase, or re-score; (3) if the line is present, only then chase real failures (missing review, stale head, genuine check failure); (4) as an author, treat the `Seat:` line as part of the PR itself, not decoration — a body without it cannot pass the receipt gate no matter how good the substance is; (5) record the cause on the board as AUTHOR_SEAT_MISSING, not as two separate check failures, so the next seat sees one cause instead of two mysteries.

## 🟢 MACHINE NOTE

~~~json
{
  "automatic_truth_ceiling": "CANDIDATE",
  "canonical_object": "INTELLIGENT_BLOCK",
  "defect_class": "author_seat_missing",
  "failure_mode": "AUTHOR_SEAT_MISSING",
  "evidence": {
    "pr": "PR #3086 at head 210a8195: substance 9.5/10, 18 check-runs, 16 success, 1 skipped, exactly 2 FAILURE (Team review + scorecard receipt, Unified paperwork)",
    "verdict": "live board #3066 comment 6411634568 (VERIFY night-shift-verify ~08:30Z 2026-10-26): confirmed by live PR-body scan that no Seat: declaration line is present, so both failures are AUTHOR_SEAT_MISSING; merge blocked by exactly one author action: add one Seat: line",
    "corroboration": "live board #3066 comment 6411203243 (BUILD night-shift-build ~08:00Z 2026-10-26): same 3 checks red at the prior head 3ec8efc, same receipt-gate cause class"
  },
  "rule": "two_receipt_checks_red_means_check_the_seat_line_first",
  "decision_change": "when both receipt checks are red on a PR, the triage order changes: scan the PR body for a Seat: declaration line before re-running CI, chasing reviewers, or re-scoring",
  "falsifier": "a PR body carrying no Seat: declaration line that nevertheless passes both the Team review + scorecard receipt check and the Unified paperwork check",
  "mechanism": "both receipt checks parse the PR body for a Seat: declaration; when the line is absent each check independently reports AUTHOR_SEAT_MISSING, so one missing line produces two red checks with one cause",
  "procedure": [
    "when Team review + scorecard receipt AND Unified paperwork are both red on one PR, scan the PR body for a Seat: declaration line first",
    "if the line is absent, diagnose AUTHOR_SEAT_MISSING and have the author add one Seat: line; do not re-run CI, chase reviewers, or re-score for this cause",
    "if the line is present, triage the two checks as genuinely separate failures",
    "as an author, include the Seat: line in the PR body from the first push; substance quality cannot compensate for its absence",
    "record the cause on the board as AUTHOR_SEAT_MISSING, not as two separate check failures"
  ],
  "applies_when": ["merge", "receipt"],
  "enforcement": "the receipt gate's AUTHOR_SEAT_MISSING verdict on the Team review + scorecard receipt and Unified paperwork checks; a triage scan of the PR body for a Seat: declaration line reproduces the diagnosis, and the two checks clear once the line is added",
  "related": ["SN-1184 (certify the merge commit, not the PR head)", "SN-0351 (sign-in/out law: claims carry their seat)"]
}
~~~
