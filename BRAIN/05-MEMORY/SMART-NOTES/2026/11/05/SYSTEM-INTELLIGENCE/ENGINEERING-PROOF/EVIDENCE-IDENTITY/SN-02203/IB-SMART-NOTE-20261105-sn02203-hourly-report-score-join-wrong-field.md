# INTELLIGENT BLOCK — SN-2203

**Intelligent Block:** IB-SMART-NOTE-20261105-sn02203-hourly-report-score-join-wrong-field
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-11-05
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** hourly_accountability_report.py load_scores() reads `s.get("file")` (hidden_files/bin/hourly_accountability_report.py, lines ~111-116) while the lane scorer writes `receipt`: twelve-lane-scores.jsonl carries 3,560 `receipt`-keyed rows vs 133 legacy `file`-keyed rows (7,463 total). Live test this tick: load_scores() returns a 132-entry index; gate-stall-20261105-2121.md (scored 9.0 at the 21:21 tick) is NOT in it, gate-stall-20261105-2013.md (scored 9.0) is NOT in it, while legacy file-keyed coldnaya-lane4.md IS (control — the join works when the field matches). Consequence on the page: hourly-reports/2026-11-05-2250.md (mtime 21:50 PST) lists gate-stall-20261105-2121 as "awaiting score"; hourly-reports/2026-11-05-0050.md did the same for gate-stall-20261104-2349 (scored 9.0 at the 23:50 tick) — the feed-log tick at 00:38 PST already named this "the known generator score-join mismatch" and corrected the report, but the generator itself is still unfixed. Number census for this note at live tip d2abe4f9 (verified via ls-remote HEAD this tick): SN-2203 absent from the main tree, the branch tree at 3a9963e2, and the registry index .naya/memory/smart-notes/index.json (1,246 entries, max SN-2202); open PRs #3254 (daily report, 1 file), #3178, #3089 — none claims it; #1354 capped at 2,500 with commenting disabled.

## ✦ IN A NUTSHELL

The hourly accountability report says receipts are "awaiting score" when they were already scored — because its score join reads the wrong field. The scorer writes each score under the key `receipt`; the report generator looks it up under `file`. Only 133 legacy rows still carry `file`, so the join silently matches almost nothing and every current receipt lands in the "awaiting score" bucket. The ledger is the truth; the report's unscored counts are fiction until the generator reads `receipt` (falling back to `file`). The deeper rule: a join that matches zero rows must fail loudly, never report "nothing scored" — silence in a join is a defect, not a measurement.

## 🩷 HUMAN NOTE

Shawn — the hourly report has been telling us receipts are waiting to be scored when they were already scored hours ago. It is not a scoring problem; the scores are all there in the ledger. The report's lookup asks for each score by the wrong name — it looks for `file` while the scorer files everything under `receipt` — so it finds almost nothing and prints "awaiting score." The fix is one line: look up `receipt` first. Until then, nobody should quote an hourly report's "unscored" count — the ledger is the only true count. The feed has been correcting these reports by hand each hour; the correction belongs in the code, not in the corrections.

## 🟣 CHILD NOTE

Imagine a teacher keeps a big book where every homework grade is written under the word "receipt." Now imagine the helper who writes the class report looks in the book for the word "file" instead. The helper finds almost nothing and tells the class "nobody has a grade yet" — even though every grade is right there in the book. The grades were never missing; the helper just asked by the wrong name. The fix is easy: ask for "receipt" first. And the helper should learn a new rule: if you look in the book and find zero grades, don't say "nobody did homework" — say "I might be looking it up wrong" and check.

## 🔵 GRANDMA NOTE

Dear, it's like a filing cabinet where every letter is filed under "receipt," and the girl who makes the daily summary keeps opening the drawer labeled "file." She finds it nearly empty and reports that nothing arrived — but the cabinet is full, she is simply looking in the wrong drawer. The letters were never lost; the lookup was wrong. From now on she must open the "receipt" drawer first, and if she ever finds nothing at all, she must stop and say "something is off with my lookup" instead of telling everyone nothing came in. A report that says "nothing" because it looked in the wrong place is worse than no report at all.

## 🟠 NAYA NOTE

For every seat that reads, writes, or repairs an accountability report: (1) never quote an hourly report's "awaiting score" / unscored count — twelve-lane-scores.jsonl is the truth; the report's pending bucket is wrong for every current-schema receipt until the generator is fixed; (2) the fix is one line in hidden_files/bin/hourly_accountability_report.py load_scores(): read `s.get("receipt") or s.get("file", "")` instead of `s.get("file", "")` — keep the `file` fallback for the 133 legacy rows; (3) after the fix, re-run load_scores() against the live ledger and assert the newest scored receipt joins by filename before trusting any report again; (4) harden the join: a report window in which zero receipts join scores while the ledger holds scores for that window must alarm instead of printing "awaiting score" — a zero-match join is a defect signal, never a measurement; (5) the 2026-10-14 root fix recorded in the generator's docstring (tick-only fallback misattributed lane 3's 9.0 as lane 1's on t0780) fixed which key the join uses, not which field it reads — a join fix that never re-checks the field name against the writer's current schema is the same bug one layer down; every future join repair must re-verify the field name against a live writer row. The feed-log corrections of reports 0050 and 2250 treat the symptom each hour; the cure is the one-line reader fix plus the zero-match alarm.

## 🟢 MACHINE NOTE

```json
{
  "slug": "hourly-report-score-join-wrong-field",
  "sn": "SN-2203",
  "title": "The Hourly Report's Score Join Reads the Wrong Field — Scored Receipts Shown as Awaiting Score",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-11-05",
  "intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "kind": "lesson",
  "applies_when": ["accountability", "hourly-report", "score-join", "schema-drift"],
  "enforcement": "Run hourly_accountability_report.load_scores() against live twelve-lane-scores.jsonl and assert the newest scored receipt joins by filename; until the generator reads 'receipt' (fallback 'file'), no hourly report's 'awaiting score' count may be quoted — twelve-lane-scores.jsonl is the truth. Regression test: add one current-schema ('receipt'-keyed) row and assert it joins; a report window with zero score joins while the ledger holds scores for that window must alarm instead of printing 'awaiting score'. The one-line fix: in load_scores(), read s.get('receipt') or s.get('file', '') instead of s.get('file', '').",
  "falsifier": "A run of the generator's load_scores() that returns a current-schema ('receipt'-keyed) receipt as scored would prove the join works and collapse this note — the live test this tick shows the opposite (gate-stall-20261105-2121.md, scored 9.0, absent from the 132-entry index; legacy file-keyed coldnaya-lane4.md present). A score row carrying a 'file' field matching a receipt filename that then appears as scored in a report would falsify the field-name claim the same way.",
  "decision_changed": "Whether an hourly report's 'awaiting score' count is believed or checked: the reader now treats every such count as suspect and verifies against twelve-lane-scores.jsonl before quoting it, and the generator owner fixes the reader to 'receipt' (fallback 'file') instead of hand-correcting one report per hour in the feed. A future join repair must re-verify the field name against a live writer row, not just the join key.",
  "mechanism": "Schema drift between a writer and a reader with no contract test: the lane scorer writes each score row under 'receipt' (3,560 of 7,463 rows; the current schema), while hourly_accountability_report.py load_scores() keys its index on s.get('file') — the field the scorer's rows carried when the generator was written (133 legacy rows). The join itself is correct (by receipt filename, per the 2026-10-14 root fix for the t0780 misattribution), but it looks up a key that current rows never populate, so it silently matches only legacy rows and files every current receipt under 'awaiting score'. Silence is the failure mode: load_scores() returns a 132-entry index with no error, and the report renders 'awaiting score' as if it were a measured state. The feed-log corrections of reports 0050 and 2250 prove the defect recurs every hour the generator runs unrepaired.",
  "provenance": "Generator: hidden_files/bin/hourly_accountability_report.py load_scores() (s.get('file', '') at lines ~111-116; join scores.get(r['file']) at ~151; docstring records the 2026-10-14 tick-only-fallback root fix, t0780). Ledger: twelve-lane-scores.jsonl — 7,463 rows; 3,560 carry 'receipt', 133 carry 'file'. Live test 2026-11-05 ~22:15 PST: load_scores() index size 132; gate-stall-20261105-2121.md (scored 9.0, tick 20261105-2121) absent; gate-stall-20261105-2013.md (scored 9.0) absent; legacy coldnaya-lane4.md present (control). Reports: hourly-reports/2026-11-05-2250.md (mtime 21:50 PST) lists gate-stall-20261105-2121 'awaiting score'; hourly-reports/2026-11-05-0050.md listed gate-stall-20261104-2349 'awaiting score' (scored 9.0 at the 23:50 tick); feed-log tick 2026-11-05 00:38 PST named it 'the known generator score-join mismatch' and corrected the report. Number census at live tip d2abe4f9 (ls-remote HEAD, this tick): SN-2203 absent from main tree paths, branch tree at 3a9963e2, and registry index .naya/memory/smart-notes/index.json (1,246 entries, max SN-2202); open PRs #3254 (daily report, 1 file), #3178, #3089 claim no SN; #1354 capped at 2,500, commenting disabled."
}
```
