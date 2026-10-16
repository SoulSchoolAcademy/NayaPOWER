# Reports Room Read Contract — Daily Intelligence Pipeline

*Signed: Naya Nitro Pi (Team Nitro, KNOW seat — playing BUILD per the Chameleon Rule), 2026-10-16.*

This contract defines how the Reports room consumes the daily intelligence
pipeline: where the artifacts live, what shape they take, how the room reads
them, and the honesty rules that govern staleness. It is binding on any
loader, adapter, or future bridge writer that touches Daily Intelligence.

## 1. Canonical paths

| Artifact | Path (repo-relative, branch `nitro/daily-intelligence`) |
|---|---|
| Generator | `team-nitro/daily-intelligence-reports/<DATE>/generator.py` |
| Dated report (human) | `team-nitro/daily-intelligence-reports/<DATE>/report-<DATE>.md` |
| Dated report (machine) | `team-nitro/daily-intelligence-reports/<DATE>/report-<DATE>.json` |
| System briefing input | `team-nitro/daily-intelligence-reports/<DATE>/system-<DATE>.json` |
| This contract | `team-nitro/daily-intelligence-reports/<DATE>/REPORTS-READ-CONTRACT.md` |

`<DATE>` is the UTC calendar date (`YYYY-MM-DD`). One directory per date —
a new day never rewrites an old directory (the snapshot law).

The room page itself (`~/workspace/user/files/reports.html`, Shawn's
original — NEVER overwritten by this pipeline) currently renders embedded
`RAW_MD` markdown strings via `ReportsAdapter.parse`. Any build step that
wires a generated `report-<DATE>.md` into that page must copy the file
content into the `RAW_MD` array byte-identically — never re-author it.

Future mapping (governance: do not create a second report store): when the
Brain canonical home `BRAIN/05-MEMORY/INTELLIGENCE-REPORTS/DAILY/YYYY/MM/DD/`
is live, the dated repo artifact remains the source of truth and the Brain
copy is a mirror. There is exactly one store; everything else projects.

## 2. Markdown shape (`report-<DATE>.md`)

Must satisfy the room's `ReportsAdapter.parse` (fields it extracts):

- `# Canonical Intelligence Report Record` (skipped as a section; meta block):
  - `**Object type:**` = `DAILY_INTELLIGENCE_REPORT`
  - `**Intelligent Block ID:**` = `IB-DIR-NAYAPOWER-<YYYYMMDD>-001`
  - `**Report ID:**` = `DIR-NAYAPOWER-<YYYY-MM-DD>` (the room's `#report=<id>` hash key)
  - `**Period type:** DAILY` · `**Period date:** <YYYY-MM-DD>`
  - `**Scope:**` · `**Status:** CANONICAL DAILY REPORT SNAPSHOT`
  - `**Canonical repository representation:**` — exact repo path of this file
  - `**Snapshot law:**` — facts/SHAs/items true only as of the generation window
  - `**Built by:**` — attribution of the builder (no unattributed output)
- Briefing body: `# NayaPOWER Daily Intelligence Briefing — <Month D, YYYY>`
  followed by `## N. <SECTION>` sections (numbered `##` headings, matching the
  existing room content: WHAT CHANGED?, BIGGEST AHA, ONE THING TO REMEMBER).
- `## 3. LIVE WEB INTELLIGENCE` (or equivalent): per-source `###` subsections.
  Every web item is a list line: `- [title](url) — Source: <Source Name>`.
  A section with no items says so in plain words — never an invented item.
  The build must include a one-line reachability disclaimer: feed-level
  reachability verified at build time; target-page reachability not
  separately verified.

## 3. JSON shape (`report-<DATE>.json`) — the machine contract

Top-level keys (stable; additive changes only):
`report_id`, `ib_id`, `period_type`, `period_date`, `scope`, `status`,
`generated_at` (ISO-8601 Z), `built_by`, `md_path`, `sources[]`, `items[]`.

- `sources[]`: `{id, name, feed, reachable, fetched_at, items_returned, items_included}`
- `items[]`: `{source, source_id, title, url, published}` — one flat array;
  ordering is per-source groups in the order listed in `sources`.

A future bridge loader reads the JSON (not the markdown) for the Hub event
`INTELLIGENCE_REPORT_CREATED`: it carries `report_id`, `ib_id`,
`period_date`, the canonical repo path, the commit SHA (recorded at push
time by the scheduler — not by the generator), `scope`, and
`generated_at`. Idempotent on `report_id`.

## 4. Refresh cadence

- One report per UTC date. The scheduled run fires after 00:05 UTC and
  completes before 06:00 UTC.
- The generator is deterministic given its inputs; re-running for the same
  date is a no-op unless `--system-file` changed (the re-run is then
  recorded in the JSON `generated_at`, and the report's snapshot law still
  anchors facts to the original generation window).

## 5. Staleness rule (honesty, not decoration)

- A daily report is a **snapshot**, never a live signal. The room displays
  the newest `report-<DATE>.md` whose date it can read and labels it:
  `Daily Intelligence — <Month D, YYYY>` plus, when the newest report is
  older than one UTC day, a visible banner: **"Last report: <date> — no
  report published since."**
- No manufactured liveness: the room never simulates a current-day report
  when the artifact is absent. A missing report is shown as missing.
- The `## 3. LIVE WEB INTELLIGENCE` section is honest at its generation
  time; it ages by the snapshot law and must not be read as current on
  later days.

## 6. Design law compliance

The report page must meet `team-nitro/DESIGN-LAWS.md` (the canonical spec):
living depth (nothing flat, nothing dead), the 11-stop gold-only spectrum
wheel walked in spectral order (never clumped) for section jewels and
accents, contrast-as-king (gold never adjacent to yellow), and the Naya
voice on headers. When the room renders generated reports, each section
jewel walks the wheel in order — section N burns the Nth wheel stop. The
dead-button violation (black on black, hairline border, flat hover) is
banned from every control on the page.

## 7. Compliance checklist for the different-seat verifier

- [ ] All three output files exist at the dated path.
- [ ] `generator.py` runs end-to-end from a clean checkout with stdlib only.
- [ ] `report-<DATE>.md` contains ≥1 real item per web-intelligence
      subsection, every item source-labeled, all feed URLs reachable (HTTP 200) at build time.
- [ ] `report-<DATE>.json` parses and its item list matches the markdown.
- [ ] Markdown satisfies `ReportsAdapter.parse` (meta fields + section shape)
      — validated by test, not by reading.
- [ ] Branch pushed; `git ls-remote` head matches the local commit SHA.
- [ ] No unattributed output; nothing written under `~/workspace/user/files/`.
