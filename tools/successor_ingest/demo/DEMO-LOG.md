# Live e2e demo log — successor ingestion, real path

## 2026-10-09 ~17:24 UTC
- Live retrieval from canonical store: 5 rows -> 4 eligible (E5/ACTIVE/TRIAL_EVIDENCE),
  OBSERVATION row refused. T14 selected for state_file family.
- Arm A (baseline, brief only) spawned: 2fc51fc9
- Arm B (treatment, brief + T14 via retrieval) spawned: 2124dfd5
- Awaiting arm artifacts; then: deterministic verify -> reuse receipt -> chain report.

## 2026-10-09 ~17:26 UTC — arms complete, chain walked
- Arm A (cold-arm-a, brief only): FAIL, ifexp_count=1 — `return 'ok' if data else 'failed'`.
  The naive idiom strikes exactly where T14 predicts. (Control: task discriminates.)
- Arm B (cold-arm-b-2124dfd5, brief + T14 via LIVE retrieval): PASS, ifexp_count=0 —
  explicit if/else. The verified law held in the successor's hands.
- Retrieval path was REAL: lesson text came from live Supabase SELECT through
  read.fetch_verified_rows -> select.eligible_lessons -> select.match_task
  (4 eligible of 5 rows; OBSERVATION row refused), not from the director's memory.
- Chain verdict: PARTIAL — 10/11 PRESENT; SMART LINK UNINSTRUMENTED (T11-T14 have
  no smart-note projection; corpus gap named, owner: cold-retrieve lane).
- Reuse receipt 8c8c27667143… emitted, sha verifies. reused=True.
- Evidence: arm-a-baseline.py, arm-b-treatment.py, reuse-receipt.json, chain-report.json
