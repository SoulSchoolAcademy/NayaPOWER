# SMART-NOTES — IB Input Contract (DRAFT)

**Status:** DRAFT — Naya 4 demo, 2026-10-01. Not canonical until ratified.
**Model (Shawn, 2026-10-01):** the Hub is the OUTPUT of intelligence, not the input.
Intelligence enters when any AI captures a Smart Note / Activity / Report as an
Intelligent Block here. A trigger validates new IBs and fans events out to the
Hub feed (personal: identified to owner · collective: anonymized).

## Path scheme

`BRAIN/04-INTELLIGENCE/SMART-NOTES/<YYYY>/<MM>/<DD>/<slug>.md`

## Frontmatter (required)

```yaml
ib: IB-2026-10-01-001        # unique IB id
kind: smart-note              # smart-note | activity | report
title: "..."                  # feed headline
streams: [personal, collective]
tone: "#ff4fd8"               # feed accent
glyph: "🔱"                   # feed glyph
time: 2026-10-01T18:20:00-07:00
provenance: "Smart Note · shared to collective"
anonymous: true               # collective projection strips identity
```

## Layers (markdown `##` sections)

`## In a nutshell` (required — the only hard requirement) plus, in order:

Human note · Child note · Grandma note · Naya note · Machine note ·
Learning lesson · What it ultimately means · How to use it · What's in it for you

Missing layers render as absent — never fabricated. The trigger fails closed on
missing frontmatter or a missing nutshell.

## Trigger

- Demo: `hub-build/ib-ingest.py` → `.block` HTML → Hub build injects into `#blocks`.
- Production (candidate): `.github/workflows/ib-feed-trigger.yml` — validates IBs on
  push, emits `feed-events.json`. No deploy (human director's gate).

## The three streams

1. **Smart Notes** — intelligent events (IBs). Show on personal feed (identified)
   and collective feed (anonymized).
2. **Activity** — what's happening now. Same pipeline, `kind: activity`.
3. **Reports** — daily syntheses. Same pipeline, `kind: report`; also feed the
   Reports room, which reads the same `.block` elements.
