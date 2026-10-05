# Weekly Cold-Retrieve Drill

**Lane 1 (Learning Loop) · Area 3: Memory & Continuity · v1**

## Purpose

Prove, every week, that a clean session with zero context can retrieve a named
Smart Note through the normal KNOW path (`smart_note_v2.py retrieve`) and apply
it correctly to a bounded question. This is the continuity heartbeat: if a cold
successor cannot retrieve and apply retained intelligence, the brain is a
write-only archive.

## How it works

1. **Schedule:** weekly cron, Monday ~06:00 PDT (before the morning report).
   The cron worker is a fresh agent session — cold by construction.
2. **Select:** `drill.py --show --week <ISO-week>` picks the week's item from
   `drill_bank.json` (round-robin: `week mod len(items)`).
3. **Retrieve:** the worker runs the KNOW query from a worktree pinned to the
   current main tip and records the returned `smart_note_id`.
4. **Apply:** the worker reads the retrieved note and answers the application
   question using ONLY that note. Answer written to a file.
5. **Grade:** `drill.py --grade --answer-file <file> --week <n>` checks all
   expected phrases (case-insensitive substring). PASS = exit 0, FAIL = exit 1.
6. **Log:** append-only JSONL (`drill_log.jsonl`): week, drill id, corpus SHA,
   retrieved note id, verdict, latency. Never edited mid-run.
7. **Report:** one line on #1354 — PASS/FAIL with the corpus SHA and the
   retrieved note. FAILs get a follow-up: re-run once to rule out flakiness,
   then file the rung that broke.

## Drill bank

`drill_bank.json` — 4 seeded items (one month rotation), each verified against
the live corpus before seeding:

| id | note | tests |
|----|------|-------|
| drill-2026-w41-a | SN-015 (Active Intelligence) | raw transcript ≠ active intelligence; PERSISTED rung |
| drill-2026-w41-b | SN-016 (Judgment Rule) | green checks ≠ license to violate a law's spirit |
| drill-2026-w41-c | SN-0344 (Canary repair-drill) | canary-* RED → run the drill, `[CANARY-DRILL]` title |
| drill-2026-w41-d | SN-015 (variant phrasing) | retrieval robustness: isolated notes must be connected |

Items retire when their note is superseded or expires (SN-0344 expires
2026-10-12 — its item retires then). New items are added by PR with the same
verification bar: query must hit the expected note on current main.

## What this proves — and does not

- **Proves:** week after week, the retain → retrieve → apply chain fires for a
  named note in a cold session. A green week is a continuity heartbeat.
- **Does not prove:** judgment quality, compounding, autonomous distillation,
  or production readiness. A retrieval HIT is not active intelligence; only
  the applied answer counts.
- **Anti-gaming:** the worker is instructed to use ONLY the retrieved note.
  The grader is deterministic phrase matching, not an LLM judge. The log is
  append-only. The remaining way to fake a drill is to corrupt the machinery,
  not to write a confident paragraph.

## Cron definition

`cold-retrieve-drill` — weekly, Mondays ~06:00 PDT (America/Vancouver),
goal-owned. The job: pin main → worktree → `drill.py --show` → worker
retrieves + answers → `drill.py --grade` → append log → post one-line result
to #1354. First run: Monday 2026-10-12.
