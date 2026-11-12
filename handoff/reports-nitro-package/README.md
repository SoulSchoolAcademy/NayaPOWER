# Reports Package for Nitro — dynamic Reports room (view + table + rows)

Built 2026-10-22 (main-seat lane) on Naya Nitro's operator evidence
(15:23Z): the live page is machine-rebaked from generator inputs, so
baked content cannot survive; the working pattern is a view that fetches
Supabase (anon read) at view-open and renders client-side. This package
is that pattern, finished and ready to hand over. **Nothing here is
deployed, no table is created, no production write has happened.**
(The handover letter itself is the main seat's; the cover note was
skipped per its update.)

## Contents — `hidden_files/reports-nitro-package/`

| File | What it is |
|---|---|
| `reports-view.html` | THE VIEW. Single self-contained page, Hub design language (obsidian stack, purple signature, spectrum accents, 18px body). Holds **zero** report content: on open it reads the reports table via anon key, lists days newest-first (date + headline), opens the full report on tap (`#report=<id>` deep links, older/newer navigation), renders markdown with a built-in renderer (no external deps). Failure and staleness are shown visibly, never silent. |
| `schema.sql` | THE TABLE. Proposed name **`hub_daily_intelligence_reports`** (existing `hub_` pattern). One row per day: `report_date` PK, `report_id`, `headline`, `lessons_summary`, `body_md`, `source_path`, timestamps. RLS on; **one anon policy: SELECT only** — no anon insert/update/delete policies exist, so anonymous writes are denied; team inserts run under service_role. |
| `rows-seed.sql` | THE ROWS as SQL: 26 INSERTs (dollar-quoted verbatim bodies, `ON CONFLICT` re-runnable). Run after `schema.sql`. |
| `rows.json` | THE ROWS as JSON — identical content to the seed. |
| `build_rows.py` | The row builder (rerunnable): extraction rules documented in its header. |
| `sources/` | The 26 filed editions, downloaded byte-exact from NayaPOWER main @ `f289672e78c2b314cbb76a6f08d8f7c273a58b88` — provenance for every row body. |

## The rows — census and shaping

- **26 rows, 2026-09-27 → 2026-10-22, no gaps, ZERO distilled-from-notes.**
  Every day in the range has a filed edition in
  `BRAIN/05-MEMORY/INTELLIGENCE-REPORTS/DAILY/` at the tip above
  (backfill PR #2917 + the Oct 22 edition from PR #2915, merged today).
- Shaped on the 2026-10-21 edition's format: `headline` = the day's first
  lesson title (IB-DIR days: the record's own "major intelligence / big
  shift / big picture / current signal" line); `lessons_summary` = the
  day's lessons section verbatim — for learning-events the
  `## THE DAILY INTELLIGENCE` block (lessons with their declared behavior
  changes); pre-standardization variants honored (Oct 9 "Distilled
  intelligence", Oct 11 "Distilled lessons"); IB-DIR days: the
  SURVIVE/REMEMBER/TORCH span. `body_md` = the filed edition,
  **byte-identical** to its repo source (verified per row).
- Verified: 26/26 bodies byte-identical to `sources/`; every
  `lessons_summary` is a verbatim contiguous slice of its body; all 26
  headlines single-line and sane (extraction printed + eyeballed).

## The view — config and verification

- **Placeholders, clearly marked** at the top of the script's CONFIG
  block: `SUPABASE_URL` and `SUPABASE_ANON_KEY`. The real values are
  **not in this repo** (searched the Hub app sources, team-nitro, and
  the live page bytes, 2026-10-22) — they live in the flagship
  dashboards' config on Nitro's box; she pastes them once. The table
  name is a third constant beside them, so a rename is one line.
- If unconfigured, the view says so on its face instead of failing
  quietly; a failed read shows a visible error panel; a newest-row
  older than a day raises the gold staleness banner.
- Proofs run here: CSS brace balance 53/53 (her deploy gate's check);
  `node --check` passes on the script; the markdown renderer was run
  against four real editions spanning every format (Oct 21 standard,
  Sep 27 compact IB-DIR, Oct 1 long-form, Oct 9 pre-standard) —
  headings/lists render, **zero** leftover `##` scaffolding; the file
  contains no report content (checked by string absence).

## Use order (for the handover)

1. `schema.sql` → create the table (Nitro's lane per the main seat's letter).
2. `rows-seed.sql` → load the 26 rows.
3. Paste the two config values into `reports-view.html`; deploy via her
   gated path (`python3 ~/workspace/factory-pipeline/deploy.py reports-view.html hub`).
4. Verify per her spec: md5 byte-compare of the view after deploy +
   survives one rebake; anon-read census = 26 rows, newest 2026-10-22.
