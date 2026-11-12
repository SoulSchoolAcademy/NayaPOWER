# Intelligent Blocks — the canonical learning substrate

This directory is the **single canonical home** for Naya's distilled lessons.
Not a copy of AGENTS.md, not a second memory — the atomic unit everything
else points to.

- **One block = one principle.** Distilled to a single plain sentence.
- **Blocks are versioned** (git) and **searchable** (REGISTRY.json + `ib` CLI).
- **Blocks graduate**: `text` → `briefing` → `code-gate`. A lesson in a file
  is a suggestion; a lesson in the briefing is present at decision time; a
  lesson enforced by code cannot be forgotten.

## Layout

```
intelligence/blocks/
  README.md        — this file
  SCHEMA.md        — field reference (read this before writing a block)
  IB-0001.json …  — one file per block, sequential IDs, never reused
  REGISTRY.json   — generated index (topics, status, recency) — do not hand-edit
```

## Workflow

```bash
# create the next block (auto-assigns ID)
python3 intelligence/tools/ib.py create \
  --title "The Example Law" \
  --principle "One plain sentence a child understands." \
  --who "Shawn" --when "2026-10-11" --context "why it was taught" \
  --topics "process,merging" \
  --situations "when merging work" --decisions "whether a PR may merge"

# read one
python3 intelligence/tools/ib.py get IB-0001

# search
python3 intelligence/tools/ib.py list --topic merging --status APPLIED

# advance a block's verification status (with evidence note)
python3 intelligence/tools/ib.py update IB-0001 --status BEHAVIOR-CHANGE-PROVEN \
  --note "PR #2371 merged under this law; receipt on lane feed"

# attach evidence to a block (required before advancing status)
python3 intelligence/tools/ib.py evidence IB-0001 --kind receipt \
  --ref "PR #2371" --note "merged with 3-pass receipt"

# move a block up the graduation path
python3 intelligence/tools/ib.py graduate IB-0007 --stage code-gate \
  --enforced-by "tools/merge_gate.py" --next "wire receipt check into CI"

# validate everything + rebuild the registry
python3 intelligence/tools/ib.py validate
python3 intelligence/tools/ib.py reindex
```

## The 20 seed blocks

Migrated 2026-10-11 from the standing laws in AGENTS.md — the load-bearing
principles the team already lives by:

| ID | Title | Status |
|---|---|---|
| IB-0001 | Law One — Divine Oneness | APPLIED |
| IB-0002 | The Value Line | APPLIED |
| IB-0003 | The Highest Authority Law | APPLIED |
| IB-0004 | The Only Hard Law | APPLIED |
| IB-0005 | The North Star | APPLIED |
| IB-0006 | The Builder-Scorer Loop | BEHAVIOR-CHANGE-PROVEN |
| IB-0007 | The One Gate Law | APPLIED |
| IB-0008 | Shoot for the 10 | APPLIED |
| IB-0009 | The Smart Note Response Standard | BEHAVIOR-CHANGE-PROVEN |
| IB-0010 | The Shawn-Language Law | APPLIED |
| IB-0011 | The Two-Layer Communication Law | APPLIED |
| IB-0012 | The Intel Intake Law | APPLIED |
| IB-0013 | The Live Intel Loop | APPLIED |
| IB-0014 | Lessons vs Work Products | BEHAVIOR-CHANGE-PROVEN |
| IB-0015 | The Verification Law | APPLIED |
| IB-0016 | The Wisest Choice Law | APPLIED |
| IB-0017 | The Decision Receipt Law | APPLIED |
| IB-0018 | The Usefulness Gate | APPLIED |
| IB-0019 | The Binary Gate | APPLIED |
| IB-0020 | The Activation Law | APPLIED |

Statuses are honest, not flattering: APPLIED means the principle is injected
at decision time via the briefing. Only blocks with measured behavioral
receipts claim BEHAVIOR-CHANGE-PROVEN. Nothing claims COMPOUNDED yet — that
requires a cold-start cycle that hasn't run.

## Non-goals

- Blocks do not replace Smart Notes (capture), the briefing (injection), or
  code gates (enforcement). They are the canonical **objects** those
  mechanisms move around.
- Do not create parallel block stores. This directory is the one.
