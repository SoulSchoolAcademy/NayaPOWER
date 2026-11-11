**Intelligent Block:** IB-SMART-NOTE-20261111-sn02671-rubric-change-moves-the-median-annotate-the-break
**Smart Note:** SN-2671
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Staged by the smart-note distillation loop 2026-11-11 15:38 PST. Evidence: nightly intelligence report 2026-11-11 §2 (daily scorecard; ~/workspace/your_files/reports/nightly-intelligence-2026-11-11.md) + memory log ~/memory/2026-11-11.md (gate-stall-20261111-1440.md scored 8.5; 17th/18th consecutive identical stall). Number census this tick: branch counter max SN-2670; open PRs verified 1 (#3345 draft Smart Mail, no Smart Note claim) at 23:02 UTC; no SN-2671 claim on the branch (claim check runs inside the staging script).

## ✦ IN A NUTSHELL

The daily scorecard median moved 9.0 → 8.5 on 2026-11-11 — the first move off a 16-day flat 9.0 — and the work did not get worse. The scorer changed its rubric: identical gate-stall receipts now score 8.5 by default instead of 9.0. The 23-receipt window was 14×8.5, 6×9.0, 3×8.0, and the stall receipts were the 17th and 18th consecutive identical stalls — byte-identical work, new score. A trend line that does not record its rubric version cannot tell a performance change from a rubric change, so every trend claim must cite the rubric version, and every rubric change must be annotated as a series break in the same report that publishes the new numbers.

## 🩷 HUMAN NOTE

Shawn — the daily median dropped from 9.0 to 8.5 today, and it looks like the team got worse. It didn't. The scoring rule changed: the same stall paperwork that used to score 9.0 now scores 8.5 by default, so the average moved even though the work was identical — the eighteenth identical stall in a row. The number moved because the ruler moved. Whenever a score trend is quoted, the ruler's version has to travel with it, or a rule change will keep reading as a performance change.

## 🟣 CHILD NOTE

Imagine your teacher changes the grading so a good homework now gets 8.5 instead of 9. Your homework is exactly the same as yesterday — same answers, same neat handwriting — but your average drops. Did you get worse? No. The grading changed. If nobody writes down "the grading changed today," everyone looking at your average later will think you slipped. So every time the grading changes, you write it right next to the new average, in big letters.

## 🔵 GRANDMA NOTE

Dear, the team's daily score slipped from 9 to 8.5 today, and it worried everyone — until we looked closer. The work was the same as yesterday, word for word, the eighteenth identical report in a row. What changed was the scoring: the same work now earns 8.5 where it used to earn 9. The ruler moved, not the work. So from now on, whenever the ruler changes, we write the change down right beside the new number — otherwise a future reader will think the team faltered when all that happened was a new yardstick.

## 🟠 NAYA NOTE

The verified facts: (1) Daily scorecard 06:00 PST 2026-11-11: 23 receipts, median 9.0 → 8.5 — first move off a 16-day flat 9.0 (14×8.5, 6×9.0, 3×8.0, 0 ≥9.5); completion 100% (23/23), timeouts 0. (2) The nightly report §2 attributes the move to two causes: a scorer policy change (identical gate-stall receipts now score 8.5 by default) plus three 8.0 evidence-defect docks. (3) The policy-change leg is independently corroborated: the 2026-11-07 nightly report records gate-stall receipts scored 9.0, 9.0, 9.5, while the 2026-11-11 memory log records gate-stall-20261111-1440.md scored 8.5, and the 15:30 lane-scorer tick calls it the 17th/18th consecutive identical stall — same work, different score, so the rubric moved. (4) Honest scope: the 16-day flat and the "first move" framing are the nightly report's, cross-checked against the memory log's score entries; the three 8.0 docks are a second, smaller contributor and do not weaken the rubric leg — both legs move the median in the same direction. (5) This is not SN-0622 (which asks which instrument produced a score — this note adds the rubric-version axis: same instrument, new rubric, new numbers) and not SN-2207/SN-2215 (shared-state size — different measurement entirely). It is the scorecard-side mirror of the same discipline: a measurement is (instrument, rubric version, value), never value alone.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-2671",
  "slug": "rubric-change-moves-the-median-annotate-the-break",
  "title": "A rubric change moves the median — annotate the series break or the trend lies",
  "observation": false,
  "applies_when": [["scorecard", "daily-scorecard"], ["measurement", "trend-reading"], ["scorer", "rubric-policy"], ["scorecard", "median"]],
  "enforcement": "Daily scorecard receipts must carry a rubric-version field; the nightly report's score section must cite the rubric version for every trend claim, and any rubric change must be annotated as a series break in the same report that publishes the new numbers. The hourly learning review flags any median/trend claim that does not cite the rubric version — an unannotated trend is not quotable.",
  "evidence": "Nightly intelligence report 2026-11-11 §2 (~/workspace/your_files/reports/nightly-intelligence-2026-11-11.md): daily scorecard 06:00 PST, 23 receipts, median 9.0 -> 8.5, first move off a 16-day flat 9.0 (14x8.5, 6x9.0, 3x8.0, 0 >=9.5), cause stated as scorer policy change (identical stalls now score 8.5 by default) + three 8.0 evidence-defect docks. Corroboration: 2026-11-07 nightly report records gate-stall receipts scored 9.0/9.0/9.5; 2026-11-11 memory log records gate-stall-20261111-1440.md scored 8.5 and the 15:30 lane-scorer tick calls it the 17th/18th consecutive identical stall — same work, different score.",
  "decision_change": "When reading any score trend, check the rubric version before concluding the work changed; when changing a rubric, annotate the break in the same report that publishes the new numbers. The next decision this changes is the reading of the 9.0 -> 8.5 median move: it is a rubric change, not a performance decline, and no performance remedy follows from it.",
  "falsifier": "Re-score the same 23 receipts under the pre-change rubric — if the median reads 9.0, the attribution holds; if it still reads 8.5, the attribution is wrong. A future median move with no rubric change and no work change would falsify the mechanism as the sole cause.",
  "cousins": ["SN-0622 (canonical area score vs trial rung vs threshold — asks which instrument produced a score; this note adds the rubric-version axis: same instrument, new rubric, new numbers)", "SN-0356 (audit your evidence's completeness before declaring the gate wrong — same family: check the measurement before blaming the measured)"],
  "captured": "2026-11-11",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE"
}
```
