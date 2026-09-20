# NayaPOWER Smart Notes

## Canonical organization

Smart Notes are organized as a calendar tree so any Naya can navigate by **year → month → day → timestamp/topic**.

```text
SUPERBRAIN/
└── SMART-NOTES/
    ├── README.md
    └── YYYY/
        └── MM/
            └── DD/
                ├── INDEX.md
                ├── YYYY-MM-DDTHH-MM-SSZ__TOPIC.md
                ├── YYYY-MM-DDTHH-MM-SSZ__TOPIC.md
                └── ...
```

Example:

```text
SMART-NOTES/2026/09/17/
├── INDEX.md
└── 2026-09-17T16-04-43Z__NAYAPOWER-CONTINUITY-NORTH-STAR.md
```

## Why this is canonical

- **Year** answers when.
- **Month** groups the work chronologically.
- **Day** contains the complete day's Smart Notes.
- **Timestamped filename** gives exact order and prevents ambiguous same-day naming.
- **Topic** makes subject search obvious.
- **INDEX.md** gives a human- and machine-readable daily map.

A new Smart Note does **not** go into a flat root directory and does **not** go into `.naya/` merely because `.naya/` contains runtime storage.

`.naya/` is the machine/runtime control plane. `SUPERBRAIN/SMART-NOTES/` is the canonical human-readable Smart Note projection.

## Required Smart Note contract

Every meaningful Smart Note must contain, as applicable:

1. Parent / Grandma — inherited source intelligence.
2. Human — human observation, decision, value, need.
3. Naya — synthesis and reasoning.
4. Machine — implementation/runtime evidence.
5. Child / Derived — downstream intelligence/artifacts.
6. What happened.
7. What we learned.
8. Why it matters.
9. How to use it.
10. What's in it for me / you / us.
11. Evidence and canonical Smart Links.
12. Current state.
13. Exactly one Next Action.
14. Successor handoff.

## Naming rule

`YYYY-MM-DDTHH-MM-SSZ__TOPIC.md`

Use UTC for canonical timestamps. Keep the topic concise, searchable, and stable.

## Daily rule

All Smart Notes created on the same calendar day belong in that day's folder. The daily `INDEX.md` lists them chronologically and provides topic/status/action pointers.

## Continuity rule

A Smart Note is not a dead document. It must be traceable to Activity/evidence and must either point to the current state/next action or explicitly state why no continuation is required.

**Canonical path rule: SMART-NOTES → YEAR → MONTH → DAY → TIMESTAMPED NOTE.**
