# NayaNET Intelligence Reports

## Purpose

Daily Intelligence Reports are canonical, durable intelligence artifacts produced from the project's verified operating state.

They are not conversation-only summaries.

## Canonical report hierarchy

```
NAYA/REPORTS/
├── DAILY/
│   └── YYYY/MM/YYYY-MM-DD.md
├── WEEKLY/
│   └── YYYY/YYYY-Www.md
├── MONTHLY/
│   └── YYYY/YYYY-MM.md
└── YEARLY/
    └── YYYY.md
```

## Identity

Every report must have:

- deterministic date
- report type
- report ID
- canonical repository
- current control-plane state
- evidence-backed accomplishments
- genuinely open gaps
- lessons learned
- current next action

A report must never claim verification that is not supported by recorded evidence.

## Three-object rule

A daily reporting cycle produces three separate linked intelligence objects:

1. **Daily Intelligence Report**
   - full historical record
   - canonical source of the day's intelligence
   - human-readable and successor-readable

2. **Daily Intelligence Smart Note**
   - distilled reusable intelligence
   - optimized for future cognition and retrieval
   - must point back to the canonical report

3. **Daily Intelligence Activity Event**
   - concise operational signal
   - tells humans and Naya that the report and Smart Note were produced
   - must point to both artifacts

These are related objects, not one object rendered three ways.

## Required relationship

```
DAILY WORK
   ↓
VERIFIED EVIDENCE
   ↓
DAILY INTELLIGENCE REPORT
   ├──→ DISTILLED SMART NOTE
   └──→ ACTIVITY EVENT
            ↓
      INTELLIGENCE HUB
            ↓
     REPORTS / TODAY / ACTIVITY
```

## Hub synchronization contract

The intended automatic path is:

```
GitHub canonical report
        ↓
authorized NayaNET report index / runtime
        ↓
managed persistence / intelligence index
        ↓
Hub Reports projection
```

The Hub must **not** scrape arbitrary GitHub branches or treat a historical branch as current authority.

The runtime must resolve reports from the canonical repository/ref and preserve:

- report ID
- report date
- report type
- source path
- source revision
- content or normalized report payload
- provenance
- authorization state
- retrieval timestamp

## No-fabrication rule

If the runtime cannot retrieve or verify a report, the Hub must show that retrieval is unavailable.

It must not manufacture a report from stale browser state or infer success from the existence of a filename.

## Automation boundary

The desired recurring lifecycle is:

**produce → canonicalize → index → persist → retrieve → render → verify**

The current Hub contains a Reports surface, but its present implementation is primarily a projection of visible Hub blocks rather than a proven GitHub-report synchronization pipeline.

Therefore:

**Daily Report → Hub automatic sync remains an implementation/proof gap.**

That gap should be closed at the smallest boundary without redesigning the Hub.

## Weekly / monthly / yearly rollups

Rollups should be derived from canonical daily reports, not independently invented.

- Weekly report = linked/derived synthesis of its canonical daily reports.
- Monthly report = linked/derived synthesis of its canonical weekly/daily reports.
- Yearly report = linked/derived synthesis of its canonical monthly/daily reports.

No rollup may silently replace the underlying daily source records.

## Current canonical artifact

**Daily:** `NAYA/REPORTS/DAILY/2026/09/2026-09-22.md`

## Next implementation boundary

**Prove one end-to-end path:**

`canonical GitHub Daily Report → authorized report retrieval → Hub Reports projection → reload → same report identity/provenance`

Do not expand to weekly/monthly/yearly automation until this daily path is proven.
