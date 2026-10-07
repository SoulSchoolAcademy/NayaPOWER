# Tier-1 Verification Packages — 2026-10-08

**Built by:** Naya 4 (Shawn-authorized — Naya 5's announced packages were not on any accessible surface)
**Grant:** 57d83ce5 (ACTIVE, expires 2026-10-14)
**Status:** READY_FOR_VERIFIER

## Packages

| # | Package | Lesson | Trial | p-value | h | Gates |
|---|---------|--------|-------|---------|---|-------|
| 1 | T11-reserve-rule | Reserve Rule: dispatch lower when top two within 0.5 | T11 (#1786) | 0.0001 | 2.84 | 4/4 PASS |
| 2 | T12-compositional | Reserve + Critical Override with priority | T12 (#1787) | 0.000011 | 1.51 | 4/4 PASS |
| 3 | T13-crossdomain | Reserve Rule abstracts to ICU domain | T13 (#1788) | 0.0007 | 2.46 | 4/4 PASS |
| 4 | T14-statefile | Never write state files via inline conditionals | T14 (#1789) | 0.0007 | 1.10 | 4/4 PASS |
| 5 | T04R-coldsuccessor | Bridge notes enable cold-successor knowledge | T04R (#1768) | 1.1e-05 | 3.14 | 3/4 PASS* |

*T04R execution gate marked UNVERIFIED — it validates the bridge-note method, not a discrete promotable lesson.

## For Verifiers

Each package directory contains:
- `note.md` — the lesson content
- `package.json` — 4-gate assessment with evidence pointers
- `receipt.json` — paired receipt with verdict

Valid verdicts: VERIFIED / REJECTED / INCONCLUSIVE (per SN-0340).
Recuse if you built it.
