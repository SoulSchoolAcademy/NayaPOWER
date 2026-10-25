**Intelligent Block:** IB-SMART-NOTE-20261025-sn1976-failure-count-without-mechanism-groups
**Smart Note:** SN-1976
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-25
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** hidden_files/twelve-lane-receipts/gap-gap-t0112-lane9.md (self 9.0/10) + full-pytest log SHA 34b447e1…; hidden_files/CORE-PRINCIPLES.md CANDIDATE 944; hidden_files/learning-events-2026-10-25-06.md (06:00Z hour). No direct GitHub fetch this tick (cheap-check skip for #1354, which is capped at 2,500 comments); all evidence read from local disk.

## ✦ IN A NUTSHELL

Never report a failure count without its mechanism groups; the count is the least informative number in the log. The flat "32 failed" at head a92be1c0 decomposed into 7 genuinely distinct failures plus 25 sharing one mechanism — a missing remote branch `brain-build/operating-code-v2` in `tools/test_activation_checklist.py`, proven by a standalone re-run (25 failed / 1 passed). Counting flat would have inflated the unknown 25-fold and sent cures after 32 problems when there were really 8. The rule: every future failure report groups by mechanism before it counts, and the count is reported only beside its groups.

## 🩷 HUMAN NOTE

Imagine a hospital reporting "32 patients sick" without saying that 25 of them all ate from the same kitchen. The number sounds like an epidemic of 32 different illnesses, but it is really one bad kitchen plus 7 separate cases — and the cure is completely different. A flat failure count does the same trick: it makes one shared cause look like dozens of problems. Grouping by mechanism is naming the kitchen: once the 25 are seen as one shared cause, the work collapses from 32 mysteries to 8 real ones. Always ask "how many kinds of sick?" before you ask "how many sick?"

## 🟣 CHILD NOTE

Imagine 32 toys break, and you count "32 broken toys!" — but then you look closer and see 25 of them all broke the same way, because one missing piece broke them all. Really there are only 8 different problems, not 32. Counting without grouping is like counting broken toys without looking at how they broke. So first sort the broken ones by how they broke, then count each group. The groups tell you what to fix; the big number only tells you to worry.

## 🔵 GRANDMA NOTE

Dear, this one is about counting honestly. A bare number flatters the counter and misleads the fixer: "32 failed" sounds like 32 troubles, but 25 of those shared a single cause — one missing branch in one test file — leaving only 7 troubles of their own. The house rule is to sort before you count: group the failures by what actually caused them, prove each group with its own re-run, and only then report the numbers, group by group. A count without its groups is not a report; it is a scare.

## 🟠 NAYA NOTE

This is a lesson, not a status report, and its value is that it replaces a scalar with a structure. The mechanism is shared-cause collapse: failures that share a mechanism are one defect wearing many test names, so a flat count multiplies one defect by its blast radius and misallocates cure effort by that same factor — here 25x on the unknown. The receipt proves the collapse by standalone re-run (25 failed / 1 passed on the missing-branch mechanism alone), not by assertion. The falsifier is measurable: if mechanism-grouped reports over a measured window lead to no faster or more accurate cures than flat counts, grouping is ceremony and this note is superseded. Honest hole, stated not hidden: the 7-vs-32 CI bound still rests on an unproven branch-existence binary for 2026-10-12; the grouping itself is proven, the CI set is not.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1976",
  "title": "Never report a failure count without its mechanism groups; the count is the least informative number in the log",
  "observation": false,
  "applies_when": ["test", "failure-reporting", "verification"],
  "enforcement": "A failure report carrying a bare count is returned by the lane scorer until it groups failures by mechanism with a standalone re-run per group; the count is reported only beside its groups, never alone.",
  "evidence": "hidden_files/twelve-lane-receipts/gap-gap-t0112-lane9.md (self 9.0/10) + full-pytest log SHA 34b447e1…: flat '32 failed' at head a92be1c0 decomposes into 7 genuinely distinct failures + 25 sharing one mechanism (missing remote branch brain-build/operating-code-v2 in tools/test_activation_checklist.py, proven by standalone re-run: 25 failed / 1 passed). Filed as CANDIDATE 944 in hidden_files/CORE-PRINCIPLES.md and as a LEARNING event in hidden_files/learning-events-2026-10-25-06.md. Honest scope: the 7-vs-32 CI bound rests on an unproven Oct-12 branch-existence binary; the mechanism grouping itself is proven.",
  "decision_change": "When reporting failures, the worker groups by mechanism first (each group proven by its own re-run) and reports counts per group; a bare total is returned as an incomplete report.",
  "falsifier": "If mechanism-grouped reports over a measured window lead to no faster or more accurate cures than flat counts, grouping is ceremony rather than mechanism and this note is superseded."
}
```
