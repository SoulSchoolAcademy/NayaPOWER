# Intelligence Reports

**Purpose:** durable human- and machine-addressable projections of canonical NayaPOWER intelligence.

Reports are **projections, not a second brain**. The canonical intelligence/evidence substrate remains authoritative; reports summarize that truth for continuity, human review, and future Hub projection.

## Hierarchy

```
DAILY → WEEKLY → MONTHLY
```

- **Daily** — atomic operational intelligence record for one reporting period.
- **Weekly** — derived rollup of Daily reports; never replaces them.
- **Monthly** — derived rollup of Weekly/Daily lineage; never replaces the sources.

## One report, two views

Every published report has:

1. **Human view** — Markdown, optimized for reading and review.
2. **Machine view** — JSON, stable IDs, explicit epistemic status, provenance, evidence references, and next action.

These are two representations of the **same report identity**. They are not two stores.

## Canonical layout

```
BRAIN/90-OPERATIONS/REPORTS/
├── README.md
├── 0001-DAILY-INTELLIGENCE-REPORT-CONTRACT-V1.md
├── DAILY/
│   ├── INDEX.json
│   ├── 2026/
│   │   └── 09/
│   │       ├── 2026-09-28-DAILY-INTELLIGENCE-REPORT.md
│   │       └── 2026-09-28-DAILY-INTELLIGENCE-REPORT.json
│   └── ...
├── WEEKLY/
├── MONTHLY/
└── EVENTS/
    ├── INDEX.json
    └── REPORT-PUBLISHED-2026-09-28.json
```

## Retrieval

A cold Naya should be able to find the current Daily report from:

- this README;
- `DAILY/INDEX.json`;
- the machine-readable brain index;
- the dated report identity.

A report must always carry its source boundary and evidence references so a successor can distinguish **FACT / INTERPRETATION / UNKNOWN / PROPOSED ACTION** without conversation archaeology.

## Publication path

Current durable repository publication:

```
CANONICAL INTELLIGENCE/EVIDENCE
        ↓
DAILY REPORT PROJECTION
        ↓
HUMAN MARKDOWN + MACHINE JSON
        ↓
REPORT_PUBLISHED EVENT
        ↓
future Activity Feed projection
        ↓
future Hub: Today → Daily Intelligence
```

The Activity Feed and Hub are **consumers/projections**. They must not become a competing report store.

## Operating rule

Do not hand-edit a report's truth after publication. Corrections create a new revision/superseding report identity while preserving the prior record and lineage.

## Status vocabulary

`DRAFT` · `VERIFIED` · `PUBLISHED` · `SUPERSEDED`

## Future automation

Once runtime publication is implemented and independently verified, the same report contract should drive:

- automatic Daily creation;
- publication event emission;
- Activity Feed entry;
- Hub Daily Intelligence projection;
- weekly rollup generation;
- monthly rollup generation;
- cold-successor retrieval.

Until then, repository artifacts are the durable engineering record and must not be described as automatic runtime publication.
