**Intelligent Block:** IB-SMART-NOTE-20261111-sn02672-score-without-its-pin-is-not-a-measurement
**Smart Note:** SN-2672
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Staged by the smart-note distillation loop 2026-11-11 15:38 PST. Evidence: nightly intelligence report 2026-11-11 §2 and §7.7 (~/workspace/your_files/reports/nightly-intelligence-2026-11-11.md) — GRAPH-10 9.5 vs 9.0 unresolved all day; cold-retrieve figures at different pins. Number census this tick: branch counter max SN-2670, SN-2671 taken by this same tick; open PRs verified 1 (#3345 draft Smart Mail, no Smart Note claim) at 23:02 UTC; no SN-2672 claim on the branch (claim check runs inside the staging script).

## ✦ IN A NUTSHELL

Three score "conflicts" sat unresolved all day on 2026-11-11 — GRAPH-10 9.5 vs 9.0, cold-retrieve 8.5 vs 7.0, CONNECT 9.3 vs 9.0 — but the figures were measured at different pins, so most of the conflict dissolves on inspection: a score is a function of the code state at its pin and the instrument that measured it, and two scores at different pins are two measurements of two different states, not two measurements of one thing disagreeing. Before any score conflict is declared unresolved, compare the pins; if the pins differ, it is a time series, not a conflict, and no adjudication is owed. A score quoted without its pin is not a measurement — it is a number looking for a meaning.

## 🩷 HUMAN NOTE

Shawn — three scores "disagreed" all day: GRAPH-10 was 9.5 and 9.0 at the same time, cold-retrieve was 8.5 and 7.0. They weren't actually disagreeing. Each one was measured at a different point in the code — different commits, different days — so they were measuring different things. It's like weighing yourself in the morning and the evening and calling it a contradiction. Before we spend a meeting adjudicating a score conflict, we check whether the numbers were even taken at the same point. If not, there's nothing to adjudicate — it's just a timeline.

## 🟣 CHILD NOTE

Imagine two friends measure the same plant: one measures it on Monday and says it's 9 inches tall, the other measures it on Friday and says it's 10 inches tall. Are they disagreeing? No — the plant grew. The numbers are different because the plant was different when each friend measured it. Scores are the same: a score taken at one point in the code and a score taken at another point are measuring two different moments. Write down WHEN each score was taken, and most arguments about scores disappear.

## 🔵 GRANDMA NOTE

Dear, the team spent all day puzzling over scores that didn't match — one said 9.5, another said 9.0, for the very same thing. But they were taken at different times, after the work had moved on. Of course they differed; the thing being measured had changed in between. It's no mystery at all once you write the date beside each number. From now on, no score travels without its moment attached — and we only call it a disagreement when two scores taken at the same moment still don't match.

## 🟠 NAYA NOTE

The verified facts: (1) Nightly intelligence report 2026-11-11 §2 records three unsettled score conflicts carried all day: GRAPH-10 — self-build lane carries 9.5/10, Intelligent Graph drive loop carries 9.0/10, with the self-build 04:08 "re-correction" 9.5 → 9.0 NOT ADOPTED by the main seat (driver unevidenced/conflicting, no first-hand drill evidence); cold-retrieve — carried 8.5/10 (main seat), W46-TIPVERIFY-24 at pin 602cb81f 2.5 → 7.5, #3347 merge rung 7.0 → 8.5 at pin a3fa145f; CONNECT 9.3 → 9.0 driver re-score NOT ADOPTED as a main-seat fact. (2) The cold-retrieve figures are explicitly pinned to different commits (602cb81f vs a3fa145f) — different code states, so different rungs are expected, not contradictory. (3) The report's §7.7 tomorrow-action is "adjudicate the score conflicts — one canonical figure per area, with the pin and instrument named," which already concedes the fix: the canonical figure must carry its pin. (4) Honest scope: the GRAPH-10 conflict also involves an instrument disagreement (self-build lane vs drive loop) and an adoption dispute, not pin difference alone — the pin rule dissolves the pin-difference part of the conflict, not the instrument part. SN-0622 governs the instrument axis; this note governs the pin axis. (5) This is not SN-1650 (pin the PR's state before pinning its head — PR-state pinning for claims, not score qualification) and not SN-0622 (which instrument — this note is which pin). Together the two axes complete the qualification: a score is (instrument, pin, value).

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-2672",
  "slug": "score-without-its-pin-is-not-a-measurement",
  "title": "A score without its pin is not a measurement — two scores at different pins are two measurements, not a conflict",
  "observation": false,
  "applies_when": [["scorecard", "score-reconciliation"], ["measurement", "pin-qualification"], ["scorecard", "conflict-adjudication"], ["scorecard", "trend-reading"]],
  "enforcement": "Any score cited in a report must carry its pin + instrument; the nightly report's score section may not declare an 'unresolved conflict' until the pins are shown equal — the hourly learning review flags any pin-less score or any conflict claim without a pin comparison, and a conflict whose pins differ is reclassified as a time series, not adjudicated.",
  "evidence": "Nightly intelligence report 2026-11-11 §2 and §7.7 (~/workspace/your_files/reports/nightly-intelligence-2026-11-11.md): GRAPH-10 9.5 vs 9.0 unresolved all day (self-build lane 9.5, drive loop 9.0; 04:08 re-correction NOT ADOPTED); cold-retrieve 2.5 -> 7.5 at pin 602cb81f (W46-TIPVERIFY-24) vs 7.0 -> 8.5 at pin a3fa145f (#3347 merge rung) — explicitly different pins; CONNECT 9.3 vs 9.0 driver re-score NOT ADOPTED. §7.7 action: adjudicate conflicts with 'one canonical figure per area, with the pin and instrument named.'",
  "decision_change": "When two scores disagree, compare pins first; if pins differ, treat as a time series, not a conflict to adjudicate — no adjudication meeting, no 'unresolved conflict' flag. The next decision this changes is the §7.7 adjudication: the cold-retrieve 'conflict' needs no adjudication (different pins), only the GRAPH-10 instrument disagreement does.",
  "falsifier": "Two scores from the same instrument at the SAME pin that differ are a genuine conflict — the pin explanation is falsified for that case. If a same-pin pair agrees while different-pin pairs disagree, the rule holds; if same-pin pairs disagree as often as different-pin pairs, pins do not explain the variance.",
  "cousins": ["SN-0622 (canonical area score vs trial rung vs threshold — asks which instrument produced a score; this note adds the pin axis: same instrument, different pin, different measurement)", "SN-1650 (pin the PR's state before pinning its head — same pin discipline applied to claims; this note applies it to scores)"],
  "captured": "2026-11-11",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE"
}
```
