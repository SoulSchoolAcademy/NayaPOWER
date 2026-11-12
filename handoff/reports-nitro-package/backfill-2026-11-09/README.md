# Reports Backfill Package — Daily Intelligence Reports 2026-10-24 → 2026-11-09 (17 rows)

Built 2026-11-09 (Resolve lane) as the continuation of
`handoff/reports-nitro-package/` (2026-10-22, 26 rows,
2026-09-27 → 2026-10-22). Same row shape, same extraction discipline,
same builder lineage — see `build_rows.py` in this folder, whose header
documents the format adaptation.

## Why this package exists — what the live room actually shows

A live-page audit of the Reports room (2026-11-09) found: the room's
newest REAL report is **2026-10-23**, and 2026-10-24 appears only as an
empty **"NO REPORT FILED"** placeholder. The room appears to be a baked
board last generated around Oct 24 — its week row ends Oct 24, and the
Oct 24 placeholder names the folder it expected:
`BRAIN/05-MEMORY/INTELLIGENCE-REPORTS/DAILY/2026/10/24/`. (The filed
Oct 24 edition on main lives at the flat path in the table below, not
in that folder.)

**This package is the verified content source for the room's 17 missing
days — 2026-10-24 → 2026-11-09 — which Nitro's room build must
ingest.** `rows.json` and `rows-seed.sql` are the portable form of that
content, shaped exactly like the original package. The seed targets
`public.hub_daily_intelligence_reports` because that is the original
package's shape; **it is NOT claimed that this table is proven to be
the room's live source** — the room's serving mechanism is Nitro's to
confirm in her build. Nothing here is deployed, no table is created,
no production write has happened, nothing was inserted, sent, posted,
or merged.

## Contents

| File | What it is |
|---|---|
| `rows.json` | THE ROWS as JSON — 17 objects, identical content to the seed. |
| `rows-seed.sql` | THE ROWS as SQL: one INSERT, 17 tuples, dollar-quoted verbatim bodies, `ON CONFLICT` re-runnable, same style as the original seed. |
| `build_rows.py` | The row builder (rerunnable): extraction rules documented in its header. |
| `sources/` | The 17 filed editions, downloaded byte-exact — provenance for every row body. |

## Census

- **17 rows, 2026-10-24 → 2026-11-09, no gaps.** Every day in the
  range has a filed `*-NAYAPOWER-DAILY-INTELLIGENCE-REPORT.md` edition.
- Combined with the original package (through 2026-10-22) and the
  2026-10-23 edition already live in the room, this closes the series
  through 2026-11-09.

## Provenance per row

Main tip anchored at build time (ref re-read, not the commits list):
`3127852d09934f2fc5a67b81312a8ebc00f6dba4`. 16 rows were fetched from
`raw.githubusercontent.com` at that SHA. **2026-11-07 does not exist on
main** — it was fetched byte-exact at the same repo path from open
**PR #3295's head** `21af3b9ad50f3bdbfb3560816655b9f76c6631dc`
(branch `resolve/dir-2026-11-07`) and is marked PR-provenance below and
in `build_rows.py`. PR #3295 was not merged or touched by this package.

| Date | Source (repo path under `BRAIN/05-MEMORY/INTELLIGENCE-REPORTS/DAILY/`) | Fetched from | Headline mode |
|---|---|---|---|
| 2026-10-24 | `2026-10-24-NAYAPOWER-DAILY-INTELLIGENCE-REPORT.md` | main @ 3127852d | day-in-one-line |
| 2026-10-25 | `2026-10-25-NAYAPOWER-DAILY-INTELLIGENCE-REPORT.md` | main @ 3127852d | day-in-one-line |
| 2026-10-26 | `2026-10-26-NAYAPOWER-DAILY-INTELLIGENCE-REPORT.md` | main @ 3127852d | day-in-one-line |
| 2026-10-27 | `2026-10-27-NAYAPOWER-DAILY-INTELLIGENCE-REPORT.md` | main @ 3127852d | day-in-one-line |
| 2026-10-28 | `2026-10-28-NAYAPOWER-DAILY-INTELLIGENCE-REPORT.md` | main @ 3127852d | day-in-one-line |
| 2026-10-29 | `2026-10-29-NAYAPOWER-DAILY-INTELLIGENCE-REPORT.md` | main @ 3127852d | day-in-one-line |
| 2026-10-30 | `2026-10-30-NAYAPOWER-DAILY-INTELLIGENCE-REPORT.md` | main @ 3127852d | day-in-one-line |
| 2026-10-31 | `2026-10-31-NAYAPOWER-DAILY-INTELLIGENCE-REPORT.md` | main @ 3127852d | first lesson title |
| 2026-11-01 | `2026-11-01-NAYAPOWER-DAILY-INTELLIGENCE-REPORT.md` | main @ 3127852d | first lesson title |
| 2026-11-02 | `2026-11-02-NAYAPOWER-DAILY-INTELLIGENCE-REPORT.md` | main @ 3127852d | first lesson title |
| 2026-11-03 | `2026-11-03-NAYAPOWER-DAILY-INTELLIGENCE-REPORT.md` | main @ 3127852d | day-in-one-line |
| 2026-11-04 | `2026-11-04-NAYAPOWER-DAILY-INTELLIGENCE-REPORT.md` | main @ 3127852d | day-in-one-line |
| 2026-11-05 | `2026-11-05-NAYAPOWER-DAILY-INTELLIGENCE-REPORT.md` | main @ 3127852d | arc-of-the-day |
| 2026-11-06 | `2026-11-06-NAYAPOWER-DAILY-INTELLIGENCE-REPORT.md` | main @ 3127852d | arc-of-the-day |
| 2026-11-07 | `2026-11-07-NAYAPOWER-DAILY-INTELLIGENCE-REPORT.md` | **PR #3295 head @ 21af3b9a — NOT main** | arc-of-the-day |
| 2026-11-08 | `2026-11-08-NAYAPOWER-DAILY-INTELLIGENCE-REPORT.md` | main @ 3127852d | arc-of-the-day |
| 2026-11-09 | `2026-11-09-NAYAPOWER-DAILY-INTELLIGENCE-REPORT.md` | main @ 3127852d | arc-of-the-day |

## Shaping — and the one extraction deviation, named

Row shape is the original package's: `report_date`, `report_id`,
`headline`, `lessons_summary`, `body_md`, `source_path`.

- `body_md` = the filed edition, byte-identical (verified below).
- `report_id`: the original `report_id_for()` unchanged — no edition
  in this range carries a `Report ID:` line, so all 17 fall back to
  `DIR-NAYAPOWER-<date>`, exactly as the original builder fell back.
- `headline` = the record's own one-line summary (the original
  package's DIR mode): `**The day in one line:**` for 9 rows,
  `**Arc of the day:**` for 5 rows (2026-11-05 → 11-09). The 3 rows
  carrying neither line (2026-10-31, 2026-11-01, 2026-11-02) use the
  original default mode — the day's first lesson title ("A gate that
  lives in a log is not a gate" · "Fix means fix — never rebuild" ·
  "A move is a sequence, not a rename"). `strip_md` applied exactly as
  in the original. All headlines are verbatim-derived; none written.
- `lessons_summary` = the day's lessons section verbatim — **the one
  deviation from the original code's literal heading names, applied
  uniformly to all 17 rows and recorded here**: this range's editions
  are the post-2026-10-24 DIR format, which carries neither the
  LEARNING-EVENT headings (`## THE DAILY INTELLIGENCE`, `## Distilled…`)
  nor the IB-DIR headings (SURVIVE / REMEMBER / TORCH). Every one of
  the 17 carries its lessons in one consistent shape —
  `## 4. TOP 10 LESSONS…` — and that block is what was extracted,
  verbatim, as the original extracted its format's lessons block
  (including its honored pre-standardization variants). The original
  IB-DIR fallback (first two sections) was deliberately NOT used: it
  would have put `## 1. IN A NUTSHELL` + `## 2. THE DAY IN NUMBERS`
  into `lessons_summary`, which is not lessons. No summary text was
  written by the builder for any row.

## Verification (run 2026-11-09, all pass)

- **Bodies byte-identical: 17/17.** sha256 of each row's `body_md`
  equals sha256 of its `sources/<date>.md` file:

| Date | sha256 (body_md = source file) |
|---|---|
| 2026-10-24 | `198c33745ad147e624045d2ef86442a6abd7cedb6802fd9943f4f6fe1b9bdde3` |
| 2026-10-25 | `688e610ed83d6bde59caa048de30e0365d3db9ea48b05f5edb011eee0a7902aa` |
| 2026-10-26 | `a3e49b2be713a9675270e6ff059ad781df55e8b703046c9fe1542d5d2a5e6bb2` |
| 2026-10-27 | `7585211e6cadae271b44cf312d9ef7d77387ecfe63f44ad675835e3bad635aae` |
| 2026-10-28 | `cd8bb15e4110ce5fddc45f7608d8d511cf33756292dd38356e87a7cf24c5f9a9` |
| 2026-10-29 | `9c1107b437e618b3979b82033590e5de1c34869210bc93a0595996e19965d48d` |
| 2026-10-30 | `b2619efc11a6883f89f0fe19a7e0e976398db300afe3a8c04d42e7d67d424bf7` |
| 2026-10-31 | `b51e177ef3164788c96672af52928f2366cae6aec7e198af88ebe2bc6fcd6498` |
| 2026-11-01 | `1c3338dc0a772410b3f719f05f7315cc2088998ee8ee3b66eea55237ae1ff66c` |
| 2026-11-02 | `8519d2d3c89d00f41966819b521d75d66d2a4f9d73c4be9209daee55f99752de` |
| 2026-11-03 | `959f425a19857ecfde2b0fbfd619f16d63a788075c23146b191bc794cded2c3a` |
| 2026-11-04 | `63941d4b0c405b71c04c8d9d1e4da936fc62db4754084b19afb8e269be399093` |
| 2026-11-05 | `44ca842917e0d64d02466e5d059e7a9968e6cbe1ca4256088155b67768b0ef71` |
| 2026-11-06 | `64f4b69a83830d967a9d80fa2659f12257b07795e41cb5c932f5b741dd3b891e` |
| 2026-11-07 | `76eb49f77b4328b7de24c94c45cb67a43d2723e252b8778ec35fb628d0dbfa13` |
| 2026-11-08 | `f33cb9b25efec35961eec07250cca579517445323d75ab3f847ed096bd9b46ea` |
| 2026-11-09 | `10dfcefa109db28250d8e0d6a93e42fd3fd6bcedb299538740c0dbace5606b01` |

- **Lessons summaries are verbatim contiguous slices: 17/17** — each
  `lessons_summary` is found intact inside its `body_md`
  (`body_md.find(lessons_summary) ≥ 0`), and each begins with its
  edition's `## 4. TOP 10 LESSONS…` heading.
- **Headlines single-line: 17/17** (no `\n` / `\r` in any headline;
  full set printed by the builder and eyeballed — see `rows.json`).
- **JSON ↔ SQL identical: 17/17** — every field of every row
  (`report_id`, `headline`, `lessons_summary`, `body_md`,
  `source_path`) extracted back out of `rows-seed.sql`'s dollar-quoted
  values matches `rows.json` exactly; the seed holds one INSERT with
  17 tuples and the original `ON CONFLICT` upsert tail.
- **No invented content** — every value in every row is either a
  verbatim slice of its edition or the original builder's documented
  fallback (`report_id`).

## Use order (for the handover)

1. Nitro's room build ingests these 17 rows (via `rows.json`, or via
   `rows-seed.sql` after `schema.sql` if the table route is the one
   her build uses — her call, per the framing above).
2. 2026-11-07's row should be re-based on main once PR #3295 lands;
   until then its provenance is the PR head, named above.
3. Verify in the room: census = 17 new days present, newest
   2026-11-09, each opening its full filed edition.
