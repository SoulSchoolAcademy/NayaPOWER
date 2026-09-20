# NayaPOWER Activity Feed

## Canonical organization

Human-readable Activity records are organized by **year → month → day → timestamp/topic**.

```text
SUPERBRAIN/
└── NAYA-ACTIVITY/
    ├── README.md
    └── YYYY/
        └── MM/
            └── DD/
                ├── INDEX.md
                ├── YYYY-MM-DDTHH-MM-SSZ__TOPIC.md
                └── ...
```

Example:

```text
NAYA-ACTIVITY/2026/09/17/
├── INDEX.md
└── 2026-09-17T16-05-08Z__CONTINUITY-NORTH-STAR.md
```

## Canonical role

`SUPERBRAIN/NAYA-ACTIVITY/` is the canonical human-readable Activity Feed projection.

`.naya/` remains the machine/runtime control plane and canonical event storage. It is not a competing human Activity Feed.

## Required Activity record

A substantive Activity record should make it possible to answer:

- What happened?
- When did it happen?
- What project/session/run was involved?
- Who/what acted?
- Under what authority?
- What was inspected?
- What changed?
- What evidence proves it?
- What failed or remains UNKNOWN?
- What was learned?
- What is the current state?
- What is the single Next Action?
- Who/what is the successor?
- Where are the Smart Links?

## Daily rule

Every Activity record created on the same calendar day belongs in that day's folder. The daily `INDEX.md` lists the records chronologically.

## Naming rule

`YYYY-MM-DDTHH-MM-SSZ__TOPIC.md`

Use UTC for canonical timestamps. Keep topics concise and searchable.

## Separation of concerns

- `.naya/memory/events/` = machine-readable canonical event storage.
- `SUPERBRAIN/NAYA-ACTIVITY/YYYY/MM/DD/` = human-readable Activity projection.
- `SUPERBRAIN/SMART-NOTES/YYYY/MM/DD/` = human-readable Smart Note library.

These layers must link to one another; they must not compete as separate truths.

**Canonical path rule: NAYA-ACTIVITY → YEAR → MONTH → DAY → TIMESTAMPED ACTIVITY.**
