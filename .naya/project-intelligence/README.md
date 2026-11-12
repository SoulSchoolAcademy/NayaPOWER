# Project Intelligence — Canonical Home

> **This directory no longer holds competing copies.**
>
> On 2026-10-09, two lanes merged two versions of the same activation documents:
> PR #2052 (here, `.naya/project-intelligence/`) and PR #2054 (under `BRAIN/`).
> Per the Human Director's order — *"kill the duplication; when a cold Naya looks
> for 'where is the activation plan?' there is exactly ONE answer"* — the two
> sets were reconciled into **one canonical set**. No content was dropped:
> every section from both sources is present in the merged files.

## Where everything lives now

| Document | Canonical path |
|---|---|
| Machine core (v2.0, 40 laws, 9 merged nodes) | `BRAIN/00-ARCHITECTURE/MACHINE-INTELLIGENCE.json` |
| System blueprint | `BRAIN/00-ARCHITECTURE/SYSTEM-BLUEPRINT-20261009.md` |
| Activation charter | `BRAIN/00-ARCHITECTURE/ACTIVATION-NAYA-PROJECT.md` |
| Activation plan (consensus v1) | `BRAIN/00-ARCHITECTURE/ACTIVATION-NAYA-PLAN.md` |
| North Star ratification (2026-09-26) | `BRAIN/00-ARCHITECTURE/NORTH-STAR-RATIFICATION-2026-09-26.md` |
| Project Intelligence spec (v1.1) | `BRAIN/05-MEMORY/SYSTEM-INTELLIGENCE/PROJECT-INTELLIGENCE-SPEC.md` |
| Project Intelligence template (v2) | `BRAIN/05-MEMORY/SYSTEM-INTELLIGENCE/PROJECT-INTELLIGENCE-TEMPLATE.md` |
| Activation Naya intelligence (v2.0) | `BRAIN/05-MEMORY/SYSTEM-INTELLIGENCE/ACTIVATION-NAYA-INTELLIGENCE.md` |
| Discovery manifest (v2) | `BRAIN/05-MEMORY/SYSTEM-INTELLIGENCE/MANIFEST.json` |

**Start here:** read `BRAIN/05-MEMORY/SYSTEM-INTELLIGENCE/MANIFEST.json` — it's the
front door. It tells you what's available, where it lives, and how fresh it is.

## What was reconciled

- `activation-naya-machine.json` (36KB) + `MACHINE-INTELLIGENCE.json` (47KB)
  → one `MACHINE-INTELLIGENCE.json` v2.0 (85KB, 40 laws, 9 merged nodes)
- `activation-naya-plan-v1.md` → `BRAIN/00-ARCHITECTURE/ACTIVATION-NAYA-PLAN.md`
  (content preserved; references fixed to canonical paths)
- `project-intelligence-activation-naya.md` + `ACTIVATION-NAYA-INTELLIGENCE.md`
  → one `ACTIVATION-NAYA-INTELLIGENCE.md` v2.0 (decisions D-001..D-012, lessons
  L-001..L-012, evidence E-001..E-010)
- `project-intelligence-template.md` + `PROJECT-INTELLIGENCE-TEMPLATE.md`
  → one `PROJECT-INTELLIGENCE-TEMPLATE.md` v2 (9 sections + entry IDs + living mechanism)
- `NAYAPOWER-SYSTEM-NORTH-STAR-RATIFICATION-2026-09-26.md`
  → `BRAIN/00-ARCHITECTURE/` (RATIFIED content unchanged; companion references fixed)
- `MANIFEST.json` → v2 with all-canonical paths
- `brain-reconciliation-ledger-f648833b.md` (2026-09-30 baseline, superseded)
  → `BRAIN/99-ARCHIVE/` with a superseded note

## Rule going forward

**Nothing substantive lives in two places.** If it's not at its canonical path,
it doesn't exist for her. New project intelligence goes straight to
`BRAIN/05-MEMORY/SYSTEM-INTELLIGENCE/` following the v2 template.
