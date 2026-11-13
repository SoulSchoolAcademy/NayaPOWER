**Intelligent Block:** IB-SMART-NOTE-20261112-sn02746-wave-log-counter-misses
**Smart Note:** SN-2746
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Staged by the smart-note distillation loop 2026-11-12 18:38 PST. Evidence read from local bytes plus git protocol (zero REST quota): shared-state stand_down=false, issue_1354_comments=2500 (GitHub hard cap; commenting disabled 2026-10-10), so no GitHub comment fetch per budget law; local lesson review only. Board #3352 comment 6841500718 (Naya 5 hourly 01:55Z) as relayed in two agreeing local records: live-plan.md director tick (wave-log-utc counter missed Eta 00:55:47Z + Lambda/Mu/Alpha 01:46:20Z; 3rd instance of this counter class) and the main-seat TIPVERIFY-62 board read in ~/memory/2026-11-12.md. Live-main check this tick: git ls-remote main 091961ba, shallow blobless clone, SN-2746 absent on main tip. Novelty checked against learn/lessons.md: no wave-log counter note exists. Filed as OBSERVATION (mechanism not established — see NAYA NOTE).

## ✦ IN A NUTSHELL

The wave-log-utc dispatch counter misses entries: the 01:55Z hourly said 6 dispatched when 7 workers were dispatched, and the counter missed four named dispatches — the third instance of this counter class. Count dispatches against the wave-log entries for the window, never against the counter.

## 🩷 HUMAN NOTE

Shawn — the hourly report's dispatch counter keeps getting the count wrong. This morning it said 6 workers went out when 7 actually did, and it missed four named dispatches entirely. It's the third time this same counter has been caught. The fix for now is boring but necessary: whoever writes the hourly should count the dispatch lines in the log by hand instead of trusting the counter's number. The deeper reconciliation — making the report instrument and the wave log agree — is already owed to Naya 5.

## 🟣 CHILD NOTE

Imagine counting how many friends came to play by asking a robot to count — but the robot keeps missing some friends. Three times now the robot's number was wrong. The friends are all there in the sign-in book, though. So you count the names in the book yourself and don't trust the robot's number until someone fixes the robot.

## 🔵 GRANDMA NOTE

Dear, the little counting helper keeps losing count — it said six when seven workers had gone out, and it missed four names clean off its list. It's the third time, love, so we don't argue with it anymore: we count the names in the book ourselves, with our own eyes. The helper can be trusted again once someone mends it — until then, the book is the truth.

## 🟠 NAYA NOTE

The verified facts (OBSERVATION — the measurement, not a mechanism): (1) Board #3352 comment 6841500718 (Naya 5 hourly 01:55Z): "6 dispatched" is WRONG, 7 workers dispatched; the wave-log-utc counter missed Eta 00:55:47Z + Lambda/Mu/Alpha 01:46:20Z — the 3rd instance of this counter class. The queue count in the same hourly (+4, 1,331 → 1,335) verified EXACT, so the defect is in the dispatch counter, not in the hourly's counting in general. (2) Earlier instances of the same class are on record in live-plan.md: a report saying "1 dispatched" while the wave-log shows 4 (wave-log says 5); "wave-log 1,251 (gap 2, was 1)" with "report instrument vs wave-log reconciliation owed (owner: Naya 5)." (3) The mechanism is NOT established: whether the counter's window, its read timing, or its entry matching drops dispatches is unknown — no cause read exists. This note records the measurement and the standing check; it does not claim a cause. (4) The standing check already exists in live-plan.md: compare each hourly's dispatched count against the wave-log entry for the same window; a mismatch is a report bug, not a dispatch bug. (5) What this is not: the dispatch itself was correct (7 workers were dispatched); only the counter's reading of it was wrong. Nothing here disputes any dispatch, fold, or queue number.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-2746",
  "slug": "wave-log-counter-misses",
  "title": "The wave-log-utc dispatch counter misses entries: verify dispatch counts against the wave-log entries, never the counter",
  "observation": true,
  "applies_when": [["report", "hourly"], ["instrument", "wave-log"], ["measurement", "dispatch-count"]],
  "enforcement": "Each hourly report's dispatched count is checked against the wave-log entries for the same window; any mismatch is flagged as a report bug and the counter's number is never cited as the count. The report-instrument vs wave-log reconciliation stays owed (owner: Naya 5) until a window shows the counter matching the entry count exactly.",
  "evidence": "Board #3352 comment 6841500718 (Naya 5 hourly 01:55Z): '6 dispatched' WRONG, 7 workers dispatched; wave-log-utc counter missed Eta 00:55:47Z + Lambda/Mu/Alpha 01:46:20Z; 3rd instance of this counter class; queue +4 (1,331 -> 1,335) verified EXACT. Relayed in two agreeing local records: hidden_files/live-plan.md director tick and ~/memory/2026-11-12.md (main-seat TIPVERIFY-62 board read). Earlier instances in live-plan.md: report '1 dispatched' vs wave-log showing 4 (wave-log says 5); wave-log 1,251 (gap 2, was 1) with report-instrument vs wave-log reconciliation owed (owner: Naya 5). Mechanism not established — no cause read exists; filed as OBSERVATION per the triage rule. Novelty: no wave-log counter note in learn/lessons.md.",
  "decision_change": "Hourly reporters verify dispatch counts against the wave-log entries for the window directly, never the wave-log-utc counter; a mismatch is treated as a report bug, not a dispatch bug, and the counter is not cited until a window proves it exact.",
  "falsifier": "A window in which the wave-log-utc counter matches the wave-log entry count exactly, or a fix that makes the counter count entries, would show this observation cured for that window; repeated exact matches retire it.",
  "cousins": ["SN-2655 (hourly report generator hardcodes PDT — same hourly-report instrument family, different defect: the clock, not the counter)", "SN-2743 (the hourly report still stamps PDT — same instrument family: a hardcoded offset reading ahead after DST ends)"],
  "captured": "2026-11-12",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE"
}
```
