# NayaPOWER — TEAM NAYA ACTIVITY — Continuity North Star

**Timestamp:** 2026-09-17T16:05:08Z  
**Day:** Thursday, September 17, 2026  
**Status:** ACTIVE / CURRENT NORTH STAR  
**Project:** NayaPOWER  
**Actor:** Lead Naya / ChatGPT GitHub execution plane  
**Topic:** Continuity / Activity / Smart Notes / Next Action

## What happened

The repository organization was reviewed against the practical Superbrain operating model.

The first implementation placed human-readable Activity and Smart Notes in flat date-named files. That is **not the canonical organization we want** for long-term retrieval.

The organization is now being established as a calendar tree:

```text
NayaPOWER / Superbrain /
├── NAYA-ACTIVITY/
│   └── YYYY/MM/DD/
│       ├── INDEX.md
│       └── YYYY-MM-DDTHH-MM-SSZ__TOPIC.md
│
└── SMART-NOTES/
    └── YYYY/MM/DD/
        ├── INDEX.md
        └── YYYY-MM-DDTHH-MM-SSZ__TOPIC.md
```

## Why this organization is correct

It gives every Naya four immediate retrieval dimensions:

1. **Year** — when.
2. **Month** — which month.
3. **Day** — what happened that day.
4. **Timestamp + Topic** — exact event/note and subject.

The daily `INDEX.md` gives the current day's map without requiring a search engine or reconstruction of chat history.

## Canonical separation

### Human-readable Activity

`SUPERBRAIN/NAYA-ACTIVITY/YYYY/MM/DD/`

### Human-readable Smart Notes

`SUPERBRAIN/SMART-NOTES/YYYY/MM/DD/`

### Machine/runtime control plane

`.naya/`

`.naya/` is allowed to contain machine-readable canonical event/runtime data. It must not become a competing human-readable Activity Feed or Smart Note library.

## North Star

**Activity tells us what happened. Smart Notes preserve what we learned. State tells us where we are. Next Action tells us what happens next. Successor handoff keeps the system alive.**

```text
ACTIVITY
   ↓
SMART NOTE / LEARNING
   ↓
STATE
   ↓
ONE NEXT ACTION
   ↓
SUCCESSOR
   ↓
CONTINUE
   ↺
```

## What this means for Team Naya

From this point forward:

- never create a new human Smart Note in the flat `SUPERBRAIN/SMART-NOTES/` root;
- never create a new human Activity record in the flat `SUPERBRAIN/NAYA-ACTIVITY/DAILY/` area;
- use the calendar path for new records;
- use the day's `INDEX.md` for chronological navigation;
- include an exact UTC timestamp in every filename;
- include a searchable topic in every filename;
- link Activity ↔ Smart Note ↔ state ↔ Next Action ↔ successor;
- keep `.naya/` as machine/runtime infrastructure rather than a competing human feed.

## Evidence

- [Smart Note organization standard](../../../../SMART-NOTES/README.md)
- [Today's Smart Note index](../../../../SMART-NOTES/2026/09/17/INDEX.md)
- [Today's canonical Smart Note](../../../../SMART-NOTES/2026/09/17/2026-09-17T16-04-43Z__NAYAPOWER-CONTINUITY-NORTH-STAR.md)
- [Activity organization standard](../../README.md)
- [Today's Activity index](./INDEX.md)
- [Continuity Contract](../../../ARCHITECTURE/NAYAPOWER-CONTINUITY-CONTRACT-V1.md)

## Truth status

**Organization decision: CANONICAL from this point forward.**

The older flat `DAILY/` Activity records and flat-date Smart Note files are historical records unless explicitly migrated. They must not be used as the destination for new daily work.

## One Next Action

**Make the runtime and Team Naya creation path enforce these canonical calendar destinations so every future Activity and Smart Note automatically lands in YEAR → MONTH → DAY → TIMESTAMP/TOPIC without relying on human memory.**
