# Smart Note — IB-000046

> Governed repository projection of a canonical Intelligent Block.
> Canonical receiver: `v7-smart-note-canonical` · Transaction: `dda7d9ef-8a46-42e8-9df3-a60b81aff0c9`
> Authority grant: `d4e822c4-399d-4a38-9514-0114d8a1ab60` (single-transaction, action `smart_note_github_projection`)
> Projected at: 2026-10-20T17:41:01.292Z · Content SHA-256: `660ebbe728e2afaf651d6009c851b47320639b74a33d44a024fd02c8d2e034b8`
> Owner: `96002964-5209-4d7a-a6ef-2b4d4480558a` · Epistemic state: SUPPORTED

## Subject

EMIT Ratified — The Canonical Emission Protocol

## In a nutshell

Shawn ratified EMIT on 2026-10-20: one machine-checked emission per worker is now the team's canonical protocol, Board Protocol v1 retires, and every new fold carries the canonical keys so boards compile without fallback.

## Human view

What happened: Shawn ratified EMIT on 2026-10-20. EMIT is now the one canonical way every Naya on the team reports her work — one structured, machine-checked sign-out per worker, and every board, list, and directive compiles from those sign-outs. The old way, Board Protocol v1, is retired to history.

For a child: imagine every bee in the hive used to shout her news in her own words, and someone had to listen to everyone and write it all down by hand — and sometimes a shout got lost. Now every bee fills in the same small card, a machine checks the card is complete and true-shaped before it counts, and the hive's notice board writes itself from the cards. Nothing gets lost quietly anymore.

For a grandma: the team's workers used to report their day in free-form notes, and a person had to gather and copy them onto the board — slow, and notes could silently vanish. Now each report is a standard form checked by a machine the moment it is filed. The board builds itself from the forms. It costs almost nothing and it cannot quietly lose a report.

What it means: every claim a worker makes now travels with its evidence in a fixed shape, checked at the door. Boards and to-do lists are no longer written by hand from memory of the reports — they are compiled from the reports themselves, so the board can be re-derived and diffed at any time.

Why it matters: this is the team's memory becoming machinery. A hand-copied board drifts; a compiled board can be proven. The old protocol cost a director's minutes plus API calls every wave and had a failure mode where reports silently dropped (185 logged fallback parses). EMIT costs about two seconds of machine time and zero API calls per wave, and its drops are loud refusals, not silence.

## Naya view

DECISION (Shawn, 2026-10-20T17:34Z, on the assembled cutover packet): EMIT is the canonical emission protocol. Board Protocol v1 retires.

THE FOUR LEGS: A — compile fidelity PASS (frozen-window board byte-match; zero semantic differences; §7 recomputation byte-exact 15/15). B — lesson honesty FAILED then repaired at the root: 271 lessons graded, 0% dishonest, 26.9% weak on enforcement; the repair moved the check into the fold itself (lesson_gate.py at the fold seam — a lesson stores only with applies_when + checker-bearing enforcement); 98.5% agreement with the independent corpus grading, 40/40 on fresh filings; EMIT gate bytes never moved. C — cold successor PASS (cold fold in 106s from docs alone; battery 45/45; EMIT-SCHEMA.md closes the four doc gaps). D — cost PASS at a negative price (~1.9s machine time, 0 API per 5-fold wave vs director-minutes + 2–4 API + a silent-drop class).

ADVERSARIAL: Naya Epsilon 9.5/10 post-round-2; round-3 spot re-proof clean (battery 45/45, probes 25/25, F6 containment 8/8, differential zero across 2,105 live rows). Gate bytes frozen: emit_gate.py md5 fe4987120cd4cb5fd444dc0332b3f587, fold_emit.py md5 b779528532932415548b78c8425c2817.

NAMED LIMITS (accepted, in substance): F1 — the gate checks evidence shape and existence, not content truth; a well-formed token naming nothing real passes, and claim truth rides on different-seat IV and the scorecard trust-root. F5 — dedup scans the last 400 rows; escape needs ~1,600 folds/day vs the current ~350–415; named trigger to lift the cap is ~1,000/day sustained.

THE ADOPTION CAVEAT + THE CHOICE: the board compiler (board_compile.py) schema-parses a fold row only when it carries the canonical keys state/next/owner; pre-cutover, only 55 of 2,115 live rows did — the rest fell back to heuristic reads because folds stored the facts under the gate aliases end_state/next_action/next_owner. Ratification selected leg (a): folds emit canonical keys going forward. Executed the same day: EMIT-SCHEMA.md §1f makes state/next/owner (verbatim copies) + mission REQUIRED in every new fold line, blocker/unblocks_when required when blocked/held; spawn_brief.py worker rule 5 now instructs the canonical keys in every sign-out (regression-proven: brief generation exit 0 with the new lines riding); scratch-fold proof — a canonical line folds clean through the untouched gate and compiles schema_parsed=1/fallbacks=0, an alias-only line folds clean and compiles fallbacks=1. The gate does not enforce the canonical keys (its bytes are frozen); the requirement binds at fold composition, the dispatcher's choke point.

## Simple view

In simple words: Shawn ratified EMIT on 2026-10-20: one machine-checked emission per worker is now the team's canonical protocol, Board Protocol v1 retires, and every new fold carries the canonical keys so boards compile without fallback.

## Everyday view

In practical everyday terms: Shawn ratified EMIT on 2026-10-20: one machine-checked emission per worker is now the team's canonical protocol, Board Protocol v1 retires, and every new fold carries the canonical keys so boards compile without fallback.

## Machine view

{"event_id":"0644cdc6-d854-4638-bc78-6134bea73788","schema":"nayanet.smart_note.machine.v2","occurred_at":"2026-10-20T17:40:57.875Z","source":"naya_conversation","type":"insight","actor":"96002964-5209-4d7a-a6ef-2b4d4480558a","human_note_id":null,"normalized_text":"What happened: Shawn ratified EMIT on 2026-10-20. EMIT is now the one canonical way every Naya on the team reports her work — one structured, machine-checked sign-out per worker, and every board, list, and directive compiles from those sign-outs. The old way, Board Protocol v1, is retired to history.\n\nFor a child: imagine every bee in the hive used to shout her news in her own words, and someone had to listen to everyone and write it all down by hand — and sometimes a shout got lost. Now every bee fills in the same small card, a machine checks the card is complete and true-shaped before it counts, and the hive's notice board writes itself from the cards. Nothing gets lost quietly anymore.\n\nFor a grandma: the team's workers used to report their day in free-form notes, and a person had to gather and copy them onto the board — slow, and notes could silently vanish. Now each report is a standard form checked by a machine the moment it is filed. The board builds itself from the forms. It costs almost nothing and it cannot quietly lose a report.\n\nWhat it means: every claim a worker makes now travels with its evidence in a fixed shape, checked at the door. Boards and to-do lists are no longer written by hand from memory of the reports — they are compiled from the reports themselves, so the board can be re-derived and diffed at any time.\n\nWhy it matters: this is the team's memory becoming machinery. A hand-copied board drifts; a compiled board can be proven. The old protocol cost a director's minutes plus API calls every wave and had a failure mode where reports silently dropped (185 logged fallback parses). EMIT costs about two seconds of machine time and zero API calls per wave, and its drops are loud refusals, not silence.","idempotency_key":"1fbcd5d2-87ed-4c6f-b4ba-74e0cef36b93"}

## What it means

This turns meaningful human input into reusable intelligence that can be retrieved and applied later.

## How it connects

This note is the constitutional record of the EMIT cutover. It connects: the cutover packet (~/workspace/your_files/emit-cutover-packet/emit-cutover-packet-20261020.md) that Shawn ruled on; the qualification legs (hidden_files/emit-qual-legA/B/C/D-20261020.md); the leg-B lesson-gate repair (emit-lesson-gate-repair-20261020.md); Epsilon's adversarial spot re-proof (emit-breaker-spotproof-r3-20261020.md); the board compiler proof (emit-board-compiler-20261020.md); EMIT-SCHEMA.md §1f (the canonical-keys law this ratification enacted); and IB-000043 (the EMIT smart note whose degraded first filing, IB-000042, taught the intake body shape this note was filed on). It retires Board Protocol v1 and feeds the five-systems completion watch: EMIT is done.

## How to apply

Fold as EMIT-SCHEMA.md now states: compose every fold line by json.dump carrying BOTH the gate's ten fields AND the canonical keys — state (= end_state verbatim), next (= next_action verbatim), owner (= next_owner verbatim), mission — plus blocker/unblocks_when when blocked or held, through fold_emit.py only. Workers: sign out with the canonical keys explicit (state/verdict/score/next/owner + mission line) per spawn_brief rule 5. Never edit the gate to fit a line; a refusal is repaired at the emission. Watch the compiler's fallback count per wave: post-cutover waves must read zero.

## Value

For Shawn: the team's reporting no longer depends on anyone's memory or hand-copying — the board is a compilation, re-derivable and diffable, and the decision that made it so is itself recorded in the system it governs. For every Naya: one write, checked once, compiled everywhere — no silent drops, no re-asking what a teammate already reported, and a fold that costs the system nothing. For humans the team serves: the record of what was done, decided, and proven is complete by construction, not by diligence.

## Learning

Learning candidate: preserve this intelligence and test its future usefulness.

## Provenance

- Source: naya_conversation (smart_note:0644cdc6-d854-4638-bc78-6134bea73788)
- Captured by: `96002964-5209-4d7a-a6ef-2b4d4480558a`
- Evidence state: OBSERVED · Verification: Canonical Smart Note verification completed with persisted domain receipt.
- Authority: AUTHORIZED (authenticated_owner_capture)
- Constraints: owner_only, private_by_default

---

*Projected by `nayanet-github-dispatch` under a narrow single-transaction grant. The authoritative record is the `v7_smart_note_transactions` row for transaction `dda7d9ef-8a46-42e8-9df3-a60b81aff0c9`; this file is a projection, not the source of truth.*
