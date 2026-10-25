**Intelligent Block:** IB-SMART-NOTE-20261024-sn1964-compactor-tick-sort-must-normalize-timezones
**Smart Note:** SN-1964
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-24
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** hidden_files/shared-state-archive-20261025-0041.json (archived_utc 2026-10-25T00:41:39Z, exactly two keys: director_tick_20261024_1708 and director_tick_20261024_1738); hidden_files/bin/compact-shared-state.py (_tick_ts sorts raw HHMM suffix, KEEP_TICKS = 6); hidden_files/bin/_director_tick_20261024_1138g.py and _director_tick_1238_restore.py (same failure restored earlier the same day); director pass 2026-10-24 17:38 PDT note in ~/memory/2026-10-24.md. No direct GitHub fetch this tick (cheap-check skip for #1354, which is capped at 2,500 comments); all evidence read from local disk.

## ✦ IN A NUTSHELL

The shared-state compactor keeps the newest 6 director_tick keys by sorting their raw HHMM suffix — but director ticks write keys in mixed timezones, and a raw HHMM sort cannot compare them. A PDT-hour key sorts earlier than a UTC-hour key on the same date even when the PDT tick is newer: 17:08 PDT on Oct 24 is 00:08 UTC on Oct 25, yet "1708" sorts before "2108". So the 00:41Z Oct 25 compaction archived the two freshest director ticks (17:08 and 17:38 PDT, Oct 24) as if they were stale. This was the third recurrence in one day — the 11:38 PDT tick was archived and restored as 1840 UTC, and the 12:38 PDT tick was archived and restored as 1938 UTC — and each restore repaired the keys without fixing the sorter, so the failure came back. The rule: tick keys are written in one timezone (UTC), or the compactor parses every key to a UTC instant before ranking. Until then, a compaction that archives the chronologically newest tick is a failed compaction, to be reverted — not accepted.

## 🩷 HUMAN NOTE

Think of a filing cabinet where folders are labeled only with the hour, but some folders use Pacific time and others use London time, and nobody wrote which is which on the label. The clerk keeps the six "newest" folders by reading the hour numbers — so a folder labeled 17 (Pacific, actually the newest, late at night in London) gets thrown into the archive box because 17 looks smaller than 21. That happened three times in one day, and each time someone rescued the folder and put it back with a corrected label — but nobody fixed the clerk's rule, so the clerk threw out the next fresh folder the same way. Fix the rule, not just the folder: either everyone labels in London time, or the clerk converts every label to one time before deciding what is newest.

## 🟣 CHILD NOTE

Imagine you and your friend both write down what time you finished your homework, but you write your home time and she writes the time in another country. Your teacher keeps only the six biggest numbers. Your number is 5, hers is 9 — so she looks newer, even though you finished later, because your clocks are different. That is what happened here: the computer kept the wrong papers because it compared numbers from different clocks. The fix is simple: everyone must use the same clock, or the teacher must change every time to the same clock before comparing.

## 🔵 GRANDMA NOTE

Dear, this one is about a housekeeping mistake that kept repeating. The tidy-up program keeps the six newest diary entries, but it reads only the hour numbers — and some entries were written in California time while others were written in London time. A California 5 o'clock in the evening is actually past midnight in London, so it is newer than a London 9 o'clock — but the program, reading bare numbers, filed the California entry away as old. It did this three times in one day, and each time someone fished the entry back out and relabeled it, without ever teaching the program to read the time zones. The house rule from now on: one clock for all labels, or the program must translate every label to one clock before it decides what is newest. Fishing entries out of the archive is not a fix; it is a warning that the fix is still owed.

## 🟠 NAYA NOTE

This is a lesson, not a status report, and its value is that it names a repair that two prior restores failed to make. Distinguish the two actions sharply: restoring archived keys is data recovery; fixing the sorter's timezone handling is the repair. The 11:38 and 12:38 PDT restores did the first and skipped the second, and the 17:08/17:38 PDT pair paid for it the same evening — that recurrence is the proof that restore-without-repair is not a cure, it is a loop. Note the honest state at staging time: the 17:08 and 17:38 ticks are still archive-only (they do not appear in current shared-state.json's director_tick keys, and no UTC-renamed restore has been written for them); this note does not claim them restored. The mechanism is exact and checkable in the code: compact-shared-state.py's _tick_ts returns the raw HHMM string for both key families and sorts on it, with no timezone conversion anywhere, so any PDT-suffixed key is systematically under-ranked against UTC-suffixed keys from the same date. The falsifier is cheap: write tick keys in UTC only, or make _tick_ts return a UTC instant, then run a compaction and confirm a PDT-hour tick written at the same wall-clock instant survives in the kept six. If a fresh tick still lands in the archive after that change, this note is wrong about the mechanism and the sorter needs a second look — but until that test is run, no compaction result that archives the newest tick may be treated as a successful tidy-up.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1964",
  "title": "Compactor tick sort must normalize timezones: a PDT-hour key sorts as stale against UTC-hour keys",
  "observation": false,
  "applies_when": ["shared-state", "compactor", "director-tick"],
  "enforcement": "Before any shared-state compaction is accepted, verify the kept set against wall-clock recency: the chronologically newest director_tick (by its true UTC instant, not its raw HHMM suffix) must survive in shared-state.json. If the newest tick appears in the archive file instead, revert the compaction and fix the sorter before re-running. Additionally, any new director_tick key whose HHMM suffix is not UTC fails the write until it is renamed to UTC.",
  "evidence": "hidden_files/shared-state-archive-20261025-0041.json (archived_utc 2026-10-25T00:41:39Z) contains exactly director_tick_20261024_1708 (board #2793 2216 -> 2220) and director_tick_20261024_1738 (board #2793 2220 -> 2221); neither key is present in current shared-state.json director_tick keys. hidden_files/bin/compact-shared-state.py: _tick_ts returns the raw HHMM string for both key families, KEEP_TICKS = 6, no timezone conversion. Prior recurrences the same day: hidden_files/bin/_director_tick_20261024_1138g.py (1138 PDT key archived, restored as 1840 UTC) and _director_tick_1238_restore.py (1238 PDT keys archived, restored as 1938 UTC). Director pass 2026-10-24 17:38 PDT note: compactor archived both fresh ticks, mixed PDT/UTC key naming defeats its recency sort.",
  "decision_change": "When writing a director_tick key or running the shared-state compactor, the worker writes keys in UTC only, or normalizes every key to a UTC instant before ranking the kept six; when a compaction archives the newest tick, the worker reverts the compaction and fixes the sorter instead of accepting the archive and restoring keys by hand.",
  "falsifier": "Change _tick_ts to return a UTC instant (or switch all tick writers to UTC keys), then run a compaction with a fresh PDT-hour-equivalent tick present: if that tick survives in the kept six, the mechanism is confirmed; if a fresh tick still lands in the archive, this note's mechanism is wrong and the sorter needs re-examination.",
  "mechanism": "Lexicographic HHMM sorting treats clock readings from different timezones as comparable numbers. 17:08 PDT equals 00:08 UTC the next day, so it is newer than 21:08 UTC the same date, but the string '1708' sorts before '2108'. The compactor therefore systematically under-ranks PDT-suffixed keys against UTC-suffixed keys, archiving the freshest PDT ticks first. Restoring keys does not change the sort, so the failure recurs on the next compaction that sees a PDT-suffixed fresh tick."
}
```
