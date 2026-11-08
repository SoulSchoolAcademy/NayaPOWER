**Intelligent Block:** IB-SMART-NOTE-20260930-sn02295-hourly-report-pdt-label-defect
**Smart Note:** SN-2295
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** First-hand verification this tick (2026-11-08 ~07:10 PST): hourly-reports/2026-11-08-0750.md header vs file mtime, plus the same +1h pattern in hourly-reports/2026-11-08-0650.md. Caught by the 06:51 PST clarity correction in ~/memory/2026-11-08.md (same file also carries hourly score-join miss #10, SN-2203 class — a different defect, already captured). The 07:04 morning briefing did NOT carry this defect (progress-morning-20261108-1457.md contains no PDT/DST/timestamp mention), so this note is its first durable record.

## ✦ IN A NUTSHELL

The hourly accountability reports' headers still label times in PDT (UTC-7) a week after daylight saving ended on 2026-11-01, so every "Window" and "Generated" timestamp reads one hour ahead of the actual local time. The 07:50 report (hourly-reports/2026-11-08-0750.md) says "Window: 06:50 → 07:50 PDT / Generated: 07:50 PDT" but the file was written at 14:50:33Z — 06:50:33 PST. The instant is right; the timezone label and offset are stale. The 06:50 report shows the same +1h pattern (mtime 13:50:35Z = 05:50:35 PST). Until the generator is fixed, read report times against the file's mtime, not the header — otherwise you misjudge recency, window coverage, and whether a receipt was scored in-window. The defect is falsifiable in one check: the next hourly report's header vs its mtime — matching PST labels mean fixed, a +1h PDT gap means it persists.

## 🩷 HUMAN NOTE

Shawn — the hourly reports are still telling the time in last week's timezone. Daylight saving ended November 1st, but the report generator kept writing "PDT" with the old offset, so every header time is an hour ahead of when the report actually ran. The 07:50 report was really written at 06:50. The clock on the wall is right; the label under it is wrong. Until someone fixes the generator, the rule is simple: believe the file's timestamp, not the header's. A reader who trusts the header will think a report covers an hour it doesn't — and can wrongly conclude a receipt was still "awaiting score" when it was already graded.

## 🟣 CHILD NOTE

Imagine your wall clock still says summer time, one hour fast, even though autumn came and everyone turned their clocks back. If you read the clock to decide when lunch was served, you'd be wrong by an hour — you'd think lunch happened later than it did. The hourly reports have that same fast clock: the words at the top say 07:50, but the report was really made at 06:50. So don't read the words at the top to know when it was made — look at the file's own time instead. That one is always honest.

## 🔵 GRANDMA NOTE

Dear, this one is a small clock that forgot the seasons changed. On November 1st the clocks went back an hour, from daylight time to standard time — but the machine that writes the hourly reports kept stamping the old daylight label on every page. So a report that says "07:50" was truly written at 06:50, an hour earlier than it claims. Nothing about the work inside is wrong — only the time written on the cover. Until the machine is taught the new time, the standing rule is: trust the file's own timestamp, never the header's. And the test is easy: the next report's header either matches its file time, and the clock is fixed, or it is still an hour ahead, and it isn't.

## 🟠 NAYA NOTE

This is a measurement-hygiene defect, not a status report, and its value is that it names a recurring misreading with a one-line correction. The mechanism is a stale timezone offset: the hourly-report generator labels headers PDT (UTC-7) after the 2026-11-01 fallback to PST (UTC-8), so the UTC instant is correct but the local label is +1h. Verified first-hand on two consecutive files this tick (0750: header 07:50 PDT vs mtime 14:50:33Z = 06:50:33 PST; 0650: same +1h pattern, mtime 13:50:35Z = 05:50:35 PST). The decision it changes is concrete: any seat judging recency, window coverage, or in-window scoring from an hourly report must use the file mtime (or header-minus-one-hour) until the generator is fixed — a header-trusting reader can wrongly mark a receipt "awaiting score" or misplace an event by an hour, which is exactly how the SN-2203 score-join misses compound. Honest holes, stated not hidden: the generator's code was not inspected this tick, so "stale offset" is the mechanism that fits both files, not a proven root cause in source; the fix itself (teach the generator PST) is owed, not done; and this note captures the defect, not the repair. Cousins, kept distinct: SN-2203 (hourly score-join defect — same report file, different defect: the score lookup reads "file" while scorer rows carry "receipt"); CANDIDATE 936 (compactor sort key must normalize timezones — different mechanism: mixed-offset sort keys, not header labels).

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-2295",
  "slug": "hourly-report-pdt-label-defect",
  "title": "Hourly report headers still label PDT a week after the DST fallback — every header timestamp reads one hour ahead; trust the file mtime, not the header",
  "observation": false,
  "applies_when": ["report", "hourly", "timestamp", "timezone", "dst", "measurement"],
  "enforcement": "Before citing any hourly report's Window or Generated time, compare the header against the file's mtime (UTC): a +1h gap with a PDT label after the 2026-11-01 fallback is the stale-offset defect — trust the mtime and subtract one hour from header times. A report whose header says PST and matches its mtime passes; a PDT-labeled header after the fallback fails the check and its times are not quotable.",
  "evidence": "hourly-reports/2026-11-08-0750.md header 'Window: 2026-11-08 06:50 → 07:50 PDT / Generated: 2026-11-08 07:50 PDT' vs file mtime 2026-11-08T14:50:33Z (= 06:50:33 PST) — +1h; same pattern in hourly-reports/2026-11-08-0650.md (mtime 13:50:35Z = 05:50:35 PST). Caught by the 06:51 PST clarity correction in ~/memory/2026-11-08.md (hourly score-join miss #10 in the same file). DST ended 2026-11-01 (PDT UTC-7 → PST UTC-8). Morning briefing progress-morning-20261108-1457.md does not carry the defect.",
  "decision_change": "Any seat judging recency, window coverage, or in-window scoring from an hourly report must use the file mtime (or header-minus-one-hour) instead of the header times, until the generator is fixed; a header-trusting reading can wrongly mark a receipt 'awaiting score' or misplace an event by an hour.",
  "falsifier": "The defect is refuted/fixed when the next hourly report's header labels PST and matches its file mtime to the minute; it persists while headers say PDT with a +1h gap to mtime. If a future report's header matches mtime while still saying PDT, the mechanism is not a stale offset and this note's diagnosis is wrong.",
  "cousins": ["SN-2203 (hourly score-join defect — same report file, different defect: score lookup reads 'file' while scorer rows carry 'receipt')", "CANDIDATE 936 (compactor sort key must normalize timezones — different mechanism: mixed-offset sort keys, not header labels)"],
  "captured": "2026-11-08",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE"
}
```
