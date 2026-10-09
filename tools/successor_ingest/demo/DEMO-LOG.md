# Live e2e demo log — successor ingestion, real path

## 2026-10-09 ~17:24 UTC
- Live retrieval from canonical store: 5 rows -> 4 eligible (E5/ACTIVE/TRIAL_EVIDENCE),
  OBSERVATION row refused. T14 selected for state_file family.
- Arm A (baseline, brief only) spawned: 2fc51fc9
- Arm B (treatment, brief + T14 via retrieval) spawned: 2124dfd5
- Awaiting arm artifacts; then: deterministic verify -> reuse receipt -> chain report.
