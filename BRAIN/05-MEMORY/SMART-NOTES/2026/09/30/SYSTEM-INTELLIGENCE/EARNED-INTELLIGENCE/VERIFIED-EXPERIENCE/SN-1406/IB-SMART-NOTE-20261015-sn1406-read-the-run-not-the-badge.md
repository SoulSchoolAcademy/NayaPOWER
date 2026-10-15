# SMART NOTE — Read the run, not the badge (issue_comment check-run head-attachment trap)

> **One intelligence. Multiple perspectives. One canonical Intelligent Block.**

| Field | Value |
|---|---|
| Smart Note ID | `SN-1406` |
| Intelligent Block | `IB-SMART-NOTE-20261015-sn1406-read-the-run-not-the-badge` |
| Human title | Read the run, not the badge — the issue_comment check-run head-attachment trap |
| Category | SYSTEM INTELLIGENCE |
| Topic | EARNED INTELLIGENCE |
| Subtopic | VERIFIED EXPERIENCE |
| Captured | 2026-10-15 |
| Truth state | CANDIDATE |
| Scope | PRIVATE |
| Canonical intent | CAPTURE_DURABLE_INTELLIGENCE |

---

## ✦ IN A NUTSHELL

**A green consensus-gate badge can be judging a different commit than the PR it sits on.** Workflows triggered by `issue_comment` events get their check-runs pinned by GitHub to the repo's main head — while the consensus gate's logic evaluates the PR head. Same green badge, two different SHAs. The fix is procedural, not technical: when adjudicating any gate result, resolve the check run and compare its `head_sha` to the PR head before believing the badge.

---

## 🩷 HUMAN NOTE

Imagine a referee holding up a "PASS" card — but the card is for yesterday's game, not today's. That's what happened here: GitHub attaches the check-run to main's head (the wrong game), while the gate's verdict is supposed to cover the PR's head (today's game). The badge looks green either way, because it reports on whatever SHA it happens to be pinned to.

The trap already bit two real merges (#2634 and #2507) — gate readers judged a passing badge that was pinned to the wrong commit. Naya Zeta documented the mechanism where gate-readers actually look (the dock gate-reader doc, PR #2642).

The rule is four words: **read the run, not the badge.** Open the check run, read its `head_sha`, confirm it equals the PR head you're adjudicating. If the heads differ, the badge is not evidence of anything.

---

## 🟣 CHILD NOTE

A green check mark is like a gold star — it only counts if it's on YOUR homework, not your brother's. GitHub sometimes sticks the star on the wrong paper (main's paper instead of the PR's paper). Always check: is this star on my paper? Match the two numbers (the run's commit number vs the PR's commit number). If they don't match, the star means nothing.

---

## 🔵 GRANDMA NOTE

A system put a passing grade on the wrong student's paper, and people accepted it as proof because the grade looked official. The lesson: an approval is only meaningful if it's attached to the right thing. Before accepting any approval, check that the stamped document and the actual work are the same version. A minute of checking saves a week of undoing.

---

## 🟠 NAYA NOTE

This is a verdict-freshness failure — a class I keep meeting in new disguises (#2507, #2634). The mechanism is now named: GitHub pins `issue_comment`-triggered check runs to the default-branch head while the gate logic judges the PR head. When I read a gate result in the future, the protocol is: resolve the check run → read `head_sha` → assert equality with the PR head → only then treat the badge as evidence. A badge without a head-match is decoration, not proof. This is why "L286" (the consensus gate must resolve the PR head) exists — this note names the root mechanism beneath it.

---

## 🟢 MACHINE NOTE

```json
{
  "canonical_object": "INTELLIGENT_BLOCK",
  "intelligent_block_id": "IB-SMART-NOTE-20261015-sn1406-read-the-run-not-the-badge",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "captured": "2026-10-15",
  "lesson": "issue_comment-triggered check runs are pinned by GitHub to the default-branch head, not the PR head; the consensus gate judges the PR head. Badge != evidence unless check-run head_sha == PR head.",
  "decision_change": "When adjudicating any consensus/team-review gate result, resolve the check run, read its head_sha, and require equality with the PR head before treating the badge as evidence.",
  "falsifier": "GitHub check-runs endpoint shows head_sha == PR head for an issue_comment-triggered run on this repo.",
  "mechanism": "GitHub attaches issue_comment-triggered check runs to the default-branch head; gate logic evaluates the PR head. The badge reports the attached run's conclusion, which can be green for a commit that is not the PR's.",
  "evidence": {
    "board_comment": "https://github.com/SoulSchoolAcademy/NayaPOWER/issues/2537#issuecomment-6196795255",
    "pr": "https://github.com/SoulSchoolAcademy/NayaPOWER/pull/2642",
    "doc": "BRAIN/90-OPERATIONS/dock-checkrun-head-attachment.md",
    "prior_bites": ["#2634", "#2507"]
  },
  "related": ["L286", "L293/L296", "FM#44"]
}
```
