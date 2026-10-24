**Intelligent Block:** IB-SMART-NOTE-20261024-sn1932-four-line-header-firing-instrument
**Smart Note:** SN-1932
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-24
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** twelve-lane-receipts/t1504-lane3.md (Evidence SHAs, batteries, latency statement); hidden_files/violation-rt/four-line-header-check.py; learning-events-2026-10-24-06.md (INTELLIGENT event); board #2721 comment 6236168626 (Shawn's four-line-header word)

## ✦ IN A NUTSHELL

Shawn's four-line-header word got its firing instrument. t1504-lane3 built `hidden_files/violation-rt/four-line-header-check.py` — pure stdlib, O(n), exit 0 clean / 1 violation — scoping feed blocks to the current tick and checking the header as four FIELDS in order (wraps allowed). Measured on a frozen copy of this tick's lane-feed (3/3 PASS, 0 violations, line-cited); firing proven on two adversarial batteries — and battery 1 caught a real bug: demanding four physical lines would have flagged every wrapped Did (the t1498-lane7 failure class), so a detector stricter than its owner manufactures violations. Fixed in the lab. This is prose → code on his standing law. Honest scope: detection-only (no enforcement wiring per brief authority); per-tick lane-executor adoption proposed, not adopted; second-seat review owed.

## 🩷 HUMAN NOTE

Shawn has a standing rule: every board post opens with four lines — Who, Team, Did, To. For years that rule lived in prose, and violations were caught only when a human happened to read a post and notice. Today a lane turned the rule into a tool: a small program that scans the whole tick's feed and flags any post whose four fields are missing or out of order. The best part: testing the tool caught a bug in the tool itself — a too-strict version would have flagged posts where the "Did" line wrapped onto two lines, manufacturing false violations. The fix: check four fields, not four physical lines. The lesson for the whole system: any standing rule can and should get a firing instrument — prose becomes code, and the code gets tested adversarially before it judges anyone.

## 🟣 CHILD NOTE

Imagine a rule at school: every paper must have your name, class, date, and title at the top. One day, a student builds a little robot that checks every paper for those four things and points out the ones missing. But the first robot was TOO strict — it complained when someone's title wrapped onto a second line! The student fixed the robot to check the four pieces of information, not just count lines. Now the rule is enforced fairly and automatically. The lesson: when there's an important rule, build a fair checker for it — and test the checker so it doesn't make up new rules of its own!

## 🔵 GRANDMA NOTE

Dear, there's a house rule: every note on the family board must start with who wrote it, which group they're in, what they did, and who it's for. Someone finally built a little machine that reads the board and points at any note missing one of those four things. While testing the machine, they caught it making a silly mistake — it complained about notes where one line spilled onto a second line, even though all four pieces were there. They fixed it to check the four pieces, not count the lines. The lesson: an important rule deserves a fair, automatic checker — and the checker itself must be tested before it judges anyone's notes.

## 🟠 NAYA NOTE

This is the prose→code pattern applied to Shawn's standing word: the four-line header (board #2721 comment 6236168626, Shawn's word 2026-10-17 ~08:55 PDT, mandatory per MEMORY.md) now has a firing instrument — `hidden_files/violation-rt/four-line-header-check.py`. Three discipline points carry forward: (1) fields, not lines — battery 1's catch of the t1498-lane7 class (demanding four physical lines would flag every wrapped Did) is the standing example of a detector stricter than its owner manufacturing violations; the check is four ordered FIELDS with wraps allowed. (2) Tick-scoping — the instrument scopes feed blocks to the current tick, so verdicts are about this tick's posts, not history. (3) The preregistered falsifier fired on the seat's own expectation (3 predicted violations, 2 real — bare "t1504" prose doesn't match the tick regex by design) and was honored, not rewritten. Adoption status is honestly PROPOSED: detection-only per brief authority, no enforcement wiring, per-tick lane-executor adoption not yet adopted, second-seat review owed. The instrument is real; the adoption is the next decision.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1932",
  "title": "Shawn's four-line-header word got its firing instrument: prose-to-code on the standing header law.",
  "applies_when": ["governance", "board-protocol", "lane-executor", "feed-posting"],
  "enforcement": "The instrument itself: hidden_files/violation-rt/four-line-header-check.py (pure stdlib, O(n), exit 0 clean / 1 violation) run per tick against a frozen copy of the tick's lane-feed; a tick's feed is clean only when the checker exits 0, and any flagged violation line-cites the offending block. Any change to the checker must re-run both adversarial batteries (field-vs-line scoping; preregistered-falsifier expectation) — a checker change that fails either battery does not ship.",
  "decision_change": "Four-line-header violations on the lane feed are now flagged mechanically per tick instead of by human audit — the per-tick lane-executor adoption decision is the next move (proposed, not adopted as of 2026-10-24).",
  "falsifiability": "Falsified by a wrapped-Did post the checker flags (battery-1 class resurrected) — a flag on a post whose four fields are all present proves the checker is stricter than the law it enforces. Falsified by a non-deterministic verdict — the same frozen tick feed must always produce the same exit code.",
  "mechanism": "The header is four ORDERED FIELDS (Who/Team/Did/To) with wrap-tolerant values, scoped to the tick's lane-feed blocks; a pure-stdlib O(n) scanner checks field order and presence per block — Shawn's standing prose becomes code that fires.",
  "evidence": ["twelve-lane-receipts/t1504-lane3.md (Evidence SHAs, two adversarial batteries, latency statement ≤1 tick)", "hidden_files/violation-rt/four-line-header-check.py", "board #2721 comment 6236168626 (Shawn's four-line-header word, 2026-10-17)"]
}
```
