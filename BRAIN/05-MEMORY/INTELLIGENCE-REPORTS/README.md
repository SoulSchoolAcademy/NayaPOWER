# Intelligence Reports

**Status:** CANONICAL PROGRAM CONTRACT — Human Director direction 2026-10-01  
**Owner domain:** BRAIN / 05-MEMORY  
**Human projection:** Hub → Reports  
**Purpose:** preserve periodic intelligence reflections as durable, searchable intelligence artifacts that compound across time without replacing Smart Notes, Activity, or runtime evidence.

## 1. Canonical object classes

NayaPOWER maintains four periodic report classes:

- `DAILY`
- `WEEKLY`
- `MONTHLY`
- `YEARLY`

Each report is a durable intelligence artifact with its own identity, date/period, scope, provenance, evidence boundary, and snapshot status.

A report is not merely prose. It is part of the intelligence lifecycle and SHOULD carry a stable Intelligent Block identifier.

## 2. Repository organization

Daily reports are organized exactly by calendar date:

`BRAIN/05-MEMORY/INTELLIGENCE-REPORTS/DAILY/YYYY/MM/DD/<IB-ID>.md`

Weekly reports:

`BRAIN/05-MEMORY/INTELLIGENCE-REPORTS/WEEKLY/YYYY/Www/<IB-ID>.md`

Monthly reports:

`BRAIN/05-MEMORY/INTELLIGENCE-REPORTS/MONTHLY/YYYY/MM/<IB-ID>.md`

Yearly reports:

`BRAIN/05-MEMORY/INTELLIGENCE-REPORTS/YEARLY/YYYY/<IB-ID>.md`

The date hierarchy is part of the retrieval contract so a cold successor or Hub projection can deterministically locate a report for any period.

## 3. Identity convention

Project/system daily report Intelligent Block IDs use:

`IB-DIR-<SCOPE>-YYYYMMDD-NNN`

Example:

`IB-DIR-NAYAPOWER-20261001-001`

Related report IDs use:

`DIR-<SCOPE>-YYYY-MM-DD`

IDs are stable after publication. A corrected report should preserve lineage and supersede rather than silently rewrite historical truth.

## 4. Report vs Smart Note vs Activity

These are three linked but distinct intelligence objects:

1. **Daily Intelligence Report** — full daily operating reflection and historical snapshot.
2. **Smart Note / distilled intelligence** — reusable lessons or rules extracted from the report for future cognition.
3. **Activity event** — concise signal that the report/intelligence was created or changed.

The Hub may mirror all three surfaces, but one must never substitute for another.

## 5. Hub projection

The intended human journey is:

`Hub → Reports → Daily | Weekly | Monthly | Yearly → select period → open report → inspect sources/evidence → follow linked Smart Notes/activity → continue`

Required Hub capabilities:

- list reports by period;
- search by date, text, topic, scope, and Intelligent Block ID;
- open the full canonical report;
- show lineage, source period, status, and supersession;
- link related Smart Notes and Activity;
- aggregate Daily → Weekly → Monthly → Yearly without erasing the lower-level reports.

The Hub is a projection surface, not the source of truth.

## 6. Runtime / persistence alignment

The repository already contains owner-scoped runtime report models:

- `public.v7_intelligence_reports` with `DAILY|WEEKLY|MONTHLY|YEARLY`;
- historical `public.v7_daily_intelligence`;
- Smart Ledger hooks that record `INTELLIGENCE_REPORT` events.

These runtime records and the Brain representation have different responsibilities:

- **Brain file:** portable/canonical project intelligence representation and cold-successor-readable history.
- **Owner-scoped runtime row:** operational per-user report state for Hub/runtime use.
- **Smart Ledger:** provenance/event lineage.
- **Hub:** human-readable projection.

Do not create a second report subsystem. Reconcile future automation through these existing seams.

## 7. Compounding law

Periodic reports compound upward:

`DAILY → WEEKLY → MONTHLY → YEARLY`

Higher-period reports MUST cite or resolve the lower-period reports they summarize. They do not replace them.

The useful long-term behavior is:

`experience → daily reflection → distilled lessons → weekly synthesis → monthly synthesis → yearly trajectory → future retrieval → better decisions`

## 8. Snapshot law

A periodic report is a historical snapshot. Repository SHAs, proof states, blockers, and scorecards inside it are true only as of that report's inspection window.

Later truth MUST NOT silently rewrite the historical report. Corrections require explicit lineage/supersession.

## 9. Historical continuity discovered in git

Daily intelligence reporting existed before this canonical Brain home but was fragmented across locations. Historical examples include:

- 2026-09-26 — `.naya/project-intelligence/NAYAPOWER-DAILY-INTELLIGENCE-REPORT-2026-09-26.md` (commit `96a7ffaa...`);
- 2026-09-22 — `NAYA/REPORTS/DAILY/2026/09/2026-09-22.md` (commit `ed989247...`);
- 2026-09-19 — `.naya/intelligence/2026-09-19-DAILY-INTELLIGENCE-REPORT.md` and Activity mirror;
- 2026-09-11 — `.naya/daily-intelligence-reports/2026-09-11-DAILY-INTELLIGENCE-REPORT.md`;
- 2026-09-08 / 2026-09-07 — earlier Intelligence Feed / root-era reports.

Those are historical evidence, not competing current homes. Do not delete history. Future reports should use this Brain path.

## 10. Current canonical report

- [2026-10-01 — IB-DIR-NAYAPOWER-20261001-001](./DAILY/2026/10/01/IB-DIR-NAYAPOWER-20261001-001.md)

## 11. Automation target

The target operating rule is:

**one owner/scope → one Daily Intelligence Report per calendar day when meaningful activity exists → deterministic identity → canonical persistence → Hub projection → later weekly/monthly/yearly synthesis.**

Generation is not proof. Every report must preserve the distinction between observed, documented, verified, production-proven, blocked, and unknown.
