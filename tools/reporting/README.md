# Team Naya Automated Reporting

Generates Shawn's three report types from live data sources. Distilled,
direct, evidence-backed — every item carries its source.

## Reports

| Wrapper | Schedule | Window |
|---|---|---|
| `morning_report.py` | 06:00 UTC | Overnight (since last nightly, or 23:00 UTC prev day) |
| `hourly_report.py` | 08:00–22:00 UTC | Since last report of any type |
| `nightly_report.py` | 23:00 UTC | Full day (since 00:00 UTC) |

Each wrapper prints the report to stdout and saves it under
`~/workspace/reports/` (override with `--save-dir`; skip with `--no-save`).
Watermarks are recorded in `state/last_report.json` so hourly deltas chain
correctly across report types.

## Report structure

```
# [MORNING/HOURLY/NIGHTLY] Report — [date/time]
## Scores (all levels)          — table: area, prev, now, Δ, status
## Top 10 Holes                 — priority-ranked, owner/source attached
## Top 10 Achievements          — since last report, with evidence
## Team Activity                — what each active worker did
## Intelligence Learned         — new lessons embedded in the system
## Next Actions                 — what's happening next
## Evidence Snapshot            — GitHub PRs + Supabase counts
```

## Data sources (all read-only)

- **Worker run logs** — `~/workspace/goals/super-brain-engine-to-10-10/hidden_files/*.md`
  (Scores / Work / Blockers / Next / Feeds sections)
- **GitHub** — `~/workspace/naya/bin/gh-api` (recent PRs, #1354 comments)
- **Supabase** — `~/workspace/skills/supabase/bin/sb-api`, SELECT-only aggregates
  (never writes; degrades gracefully to "unavailable" on failure)
- **Memory** — `~/memory/YYYY-MM-DD.md` daily logs (`[tag|severity]` entries)

## Score extraction rules (anti-corruption)

Worker logs and memory are free text, so extraction is heuristic — with
hard rules to prevent phantom score movements:

1. Area name and score must be in the **same sentence**.
2. A sentence with **multiple areas + one score is skipped** (never guess).
3. **Movement wins**: "8.5 → 8.8" yields 8.8; the "score:" inside
   "re-score:" never shadows it.
4. **Never downgrade**: an `authoritative` score is not overwritten by a
   heuristic claim's status.
5. Out-of-range values (>10) are ignored.

Scores persist in `state/score_state.json`. The seed carries the reconciled
2026-10-08 baselines (Learning 5.0 authoritative per Naya 1; rest are claims).

## Hole priority (transparent)

Baseline 5, plus: protected-gate/Shawn-word +30, red/CI-fail +25,
blocked/stalled +20, conflict +18, verify/review/merge +15.

## Tests

```
pytest tools/reporting/tests/test_report_generator.py -q   # 29 tests
```

All data sources are mocked in tests — no network, no Supabase, no GitHub.

## Delivery

The generator does **not** post to GitHub and does **not** write to Supabase.
Delivery (post to #1354 + chat to Shawn) is a separate integration step.
