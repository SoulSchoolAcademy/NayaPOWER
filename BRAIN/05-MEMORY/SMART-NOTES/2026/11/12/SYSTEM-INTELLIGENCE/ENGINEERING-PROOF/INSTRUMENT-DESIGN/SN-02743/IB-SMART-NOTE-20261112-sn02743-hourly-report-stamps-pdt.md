**Intelligent Block:** IB-SMART-NOTE-20261112-sn02743-hourly-report-stamps-pdt
**Smart Note:** SN-2743
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-12
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** Staged by the smart-note distillation loop 2026-11-12 16:30 PST. Evidence read first-hand from local bytes (zero REST quota): shared-state stand_down=false, issue_1354_comments=2500 <= board watermark 6101230756, so no GitHub fetch per budget law; local lesson review only. Four hourly reports compared by file mtime (UTC) against their stamped window/Generated time; generator source read at hidden_files/bin/hourly_accountability_report.py line 33.

## ✦ IN A NUTSHELL

Every hourly accountability report since daylight saving ended stamps its window and Generated time one hour in the future. The generator hardcodes PDT as a fixed UTC-7 offset instead of using the America/Los_Angeles zone, so since November 1 it has read an hour ahead: a report written at 15:50 PST claims it covers 15:50→16:50 and was generated at 16:50, while its content is the hour just ended. The timestamps are evidence — when they lie, every verification that cites a report's window is misaimed by an hour.

## 🩷 HUMAN NOTE

Shawn — the hourly reports have been stamping the wrong time since daylight saving ended. The generator uses a fixed "PDT is 7 hours behind UTC" rule, but we're on PST now (8 hours behind), so every report claims to be from an hour in the future. The report written at 3:50pm says it covers 3:50 to 4:50 and was generated at 4:50. Its contents are fine — it's the previous hour's work — but the label on the box is wrong, and anyone checking "what happened between 3:50 and 4:50" from that label will look in the wrong hour. The fix is one line: use the real timezone instead of the hardcoded offset.

## 🟣 CHILD NOTE

Imagine your clock is stuck on summer time, but everyone else moved their clocks back an hour for winter. Your clock says 4:50 when it's really 3:50. Everything you write down with that clock looks like it happened an hour later than it did. The reports aren't lying on purpose — their clock just never learned that summer ended. Fix the clock, and the times become true again.

## 🔵 GRANDMA NOTE

Dear, the hourly reports have been telling the wrong time since the clocks went back. The little program that writes them still thinks we're on summer time, so it stamps everything an hour ahead — a report finished at half past three claims it was made at half past four. The work inside is all correct, love, but the time written on the outside is wrong, and anyone trusting that time will look in the wrong hour. It just needs to ask the real clock what time it is instead of guessing.

## 🟠 NAYA NOTE

The verified facts: (1) hidden_files/bin/hourly_accountability_report.py line 33: `PT = timezone(timedelta(hours=-7))  # PDT` — a hardcoded fixed UTC-7 offset, labelled PDT. (2) Daylight saving ended 2026-11-01 (first Sunday in November); America/Los_Angeles is PST (UTC-8) from then on, so a fixed UTC-7 offset reads exactly 60 minutes ahead. (3) Four consecutive reports, each verified by file mtime (UTC) against its stamped window and Generated line: 2026-11-12-1350.md written 20:50 UTC (12:50 PST) stamps window 12:50→13:50 PDT and Generated 13:50 PDT; 1450.md written 21:50 UTC stamps 13:50→14:50; 1550.md written 22:50 UTC stamps 14:50→15:50; 1650.md written 23:50 UTC (15:50 PST) stamps window 15:50→16:50 PDT and Generated 16:50 PDT. In every case the stamped window starts at the write time and ends 60 minutes after it, and the content is the hour before write time (1650.md contains only the 15:03 gate-stall receipt). (4) The defect is systematic, not a one-off: the same +60-minute shift appears in all four reports, and the mechanism (a constant offset) guarantees it in every report until fixed. (5) What is NOT new here: SN-1876 (timestamp legs canonicalize timezone), SN-1964 (compactor tick sort must normalize timezones), SN-1979 (scorer timestamps come from date -u at write time) — those are about sorting, legs, and scorer stamps. This is about a report generator stamping a future window with a stale DST offset. SN-2203 is the same instrument but a different defect (score-join reads the wrong field).

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-2743",
  "slug": "hourly-report-stamps-pdt",
  "title": "The hourly report still stamps PDT: a hardcoded UTC-7 offset reads one hour ahead after daylight saving ends",
  "observation": false,
  "applies_when": [["hourly-report", "timestamp"], ["instrument", "timezone"], ["report", "window"]],
  "enforcement": "Verify any hourly accountability report by comparing its stamped Generated time against the file mtime (they must agree within minutes); the generator must derive its zone from America/Los_Angeles (zoneinfo), never from a hardcoded UTC offset. Until fixed, cite a report by mtime plus content, never by its stamped window.",
  "evidence": "hidden_files/bin/hourly_accountability_report.py line 33: PT = timezone(timedelta(hours=-7))  # PDT. Daylight saving ended 2026-11-01; America/Los_Angeles is PST (UTC-8) after that. Four reports verified mtime-vs-stamp: 1350.md written 20:50 UTC stamps 12:50->13:50 PDT; 1450.md written 21:50 UTC stamps 13:50->14:50; 1550.md written 22:50 UTC stamps 14:50->15:50; 1650.md written 23:50 UTC (15:50 PST) stamps window 15:50->16:50 PDT and Generated 16:50 PDT, while its content is only the 15:03 gate-stall receipt. Existing doctrine checked and NOT duplicated: SN-1876, SN-1964, SN-1979 (timezone/sort/scorer-stamp cousins), SN-2203 (same instrument, score-join defect).",
  "decision_change": "When citing an hourly report, use file mtime plus content, never the stamped window; the generator's offset must come from the zone (America/Los_Angeles), not a constant, and any future report is checked mtime-vs-stamp before its window is trusted.",
  "falsifier": "If the generator is fixed to the zone and a later report's stamped Generated time matches its mtime, the defect is gone; if the offset flips the other way at the spring-forward boundary (reading an hour behind), the same stale-offset mechanism is confirmed in reverse.",
  "cousins": ["SN-1876 (timestamp legs canonicalize timezone)", "SN-1964 (compactor tick sort must normalize timezones: a PDT-hour key sorts as stale against UTC-hour keys)", "SN-1979 (scorer timestamps come from date -u at write time)", "SN-2203 (the hourly report's score join reads the wrong field — same instrument, different defect)"],
  "captured": "2026-11-12",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE"
}
```