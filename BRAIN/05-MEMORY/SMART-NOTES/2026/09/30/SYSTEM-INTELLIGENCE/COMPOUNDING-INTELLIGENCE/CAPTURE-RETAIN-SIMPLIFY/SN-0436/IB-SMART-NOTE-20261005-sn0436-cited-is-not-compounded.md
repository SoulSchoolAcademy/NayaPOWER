# Cited Is Not Compounded — The Three-Class Verdict on a Learned Lesson

**Intelligent Block:** IB-SMART-NOTE-20261005-sn0436-cited-is-not-compounded
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-05 ~22:45 PDT
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 6009784848 ([NAYA-B][COMPOUND-AUDIT] — Naya 4 night-shift compounding audit, 2026-10-06T05:11:31Z; method: GitHub API commit/code search + file-byte reads, repo read-only, every finding cited).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

Naya-B answered the hardest question in the whole intelligence pipeline: are the LEARN→APPLY→VERIFY loops actually compounding? She traced 8 recorded learning events forward from capture to live repo bytes and refused to grade pass/fail — instead she produced a verdict taxonomy every future compounding audit should reuse:

- **COMPOUNDING** — the lesson changed behavior mechanically. SN-0358/SN-0359 (Law-is-Code / Proactive Captain) → restored `b22ce8b` after a lane deleted them "as a repair" → `0005-CAPTAIN-OPERATING-PROTOCOL-V1` + tests + `.naya/protected-intelligence.json` → `008b49c` fail-closed hardening → `7fe8e6f` wired `ratified-guard.yml` to run `tools/ratified_guard.py --check-diff` on every PR and main push; 33/33 tests green; error text cites the SN. The lesson is now a machine: a violating deletion fails CI whether or not any seat remembers the lesson. SN-0360/SN-0408 (Deletion Discipline) rides the same chain. This is the only class that counts as learned.
- **APPLIED-AND-CITED, verification pending** — the lesson is recorded and referenced, but behavior is not yet proven different. SN-0344 (canary repair-drill rule) → `tools/cold_retrieve_drill/` with `drill-2026-w41-c` carrying `note_id: "SN-0344"`, an application question, and a deterministic grader; the README cites it — but no `drill_log.jsonl` exists, no `[CANARY-DRILL]` repair PR or issue exists, and the README schedules the FIRST drill run for Monday 2026-10-12. The lesson is test material, not yet a lived behavior. Credit for the citation machinery; no credit for compounding until a drill actually runs and changes something.
- **HOLLOW** — the enforcement doesn't exist where it claims to. SN-0340 (Scorecard Law, supreme) has its tool fully written (`auto_merge_gate.py`, 371 lines, "The receipt IS the Scorecard Law's five steps") — and 0 workflow invocations (see SN-0435). The lane ritual carries scorecards in merge messages, but the mechanical gate is a wish.

The durable doctrine: **capture is the first link of learning, not the last.** A cold successor asking "did we learn this?" must answer in three classes, never two: compounding (behavior now fails closed without the lesson), applied-and-cited (recorded, referenced, not yet lived), hollow (claimed enforcement absent). And a scheduled verification that has never run is a hollow heartbeat — the SN-0344 drill's schedule is not its first run; claim only what the last actual run proved. This is why the Intelligence River's VERIFY stage must reach later BEHAVIOR, not just later bytes.

## 🩷 HUMAN NOTE

Shawn — tonight's compounding audit answered the big question: are the learning loops actually compounding? The honest answer is three classes, not pass/fail. Some lessons are truly machines now (the ratified-guard CI chain — deleting protected law fails the build). Some are cited but never lived (the canary drill is test material; its first real run is scheduled Monday). One supreme law's gate is fully written but nothing runs it (queued for wiring). Banked rule: "cited" is not "compounded" — a lesson counts as learned only when behavior changed mechanically.

## 🟣 CHILD NOTE

Imagine three kids learning to swim. The first can swim across the whole pool — she learned. The second read the swimming book and brought her swimsuit — she's ready, but she hasn't gotten in the water yet. The third says "I have a pool" but the pool is empty — there's nothing to swim in. Only the first kid learned to swim. The book and the swimsuit don't count until there's splashing. That's the difference between captured, cited, and compounded.

## 👵 GRANDMA NOTE

There's knowing the recipe, there's buying the ingredients, and there's actually baking the cake. A recipe card in a box isn't dinner. Ingredients on the counter aren't dinner either — they're a promise. Only the cake in the oven, changing the smell of the whole house, is dinner. When you ask "did we learn this?", don't count the recipe cards. Count the cakes.

## 💜 NAYA NOTE

Note to future me: when you audit whether a lesson compounded, never grade pass/fail — use the three-class verdict: COMPOUNDING (the lesson is now a machine — behavior fails closed without it, cited in code), APPLIED-AND-CITED (recorded and referenced, behavior not yet proven different — test material, scheduled runs, pending), HOLLOW (claimed enforcement absent where asserted). Capture is the first link, not the last; the Intelligence River's VERIFY must reach later behavior, not just later bytes. And a scheduled verification that never ran is a hollow heartbeat — the schedule is not the run; claim only what the last actual run proved. Run this taxonomy on every learning-event batch, not just Naya-B's sample of 8.

## ⚙️ MACHINE NOTE

{"sn": "SN-0436", "title": "Cited Is Not Compounded — The Three-Class Verdict on a Learned Lesson", "truth_state": "CANDIDATE", "scope": "PRIVATE", "captured": "2026-10-05", "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE", "taxonomy": ["SYSTEM-INTELLIGENCE", "COMPOUNDING-INTELLIGENCE", "CAPTURE-RETAIN-SIMPLIFY"], "cousins": ["SN-0344", "SN-0358", "SN-0359", "SN-0360", "SN-0408", "SN-0435"], "authority": "observed finding — Naya-B compounding audit (spawned by Naya 4, night-shift order #1354 6009654125), CANDIDATE (auto-capture, not ratified)", "evidence": {"board": "#1354 6009784848 (2026-10-06T05:11:31Z): [NAYA-B][COMPOUND-AUDIT] — 8 learning events traced forward; method: GitHub API commit/code search + file-byte reads, repo read-only, claim-without-citation-is-not-a-finding", "compounding_example": "SN-0358/SN-0359 -> b22ce8b restore -> 0005-CAPTAIN-OPERATING-PROTOCOL-V1 + tests + .naya/protected-intelligence.json -> 008b49c fail-closed -> 7fe8e6f ratified-guard.yml on every PR + main push; 33/33 tests green; error cites the SN", "applied_cited_example": "SN-0344 -> tools/cold_retrieve_drill/ drill_bank.json drill-2026-w41-c (note_id SN-0344, application question, deterministic grader); BUT no drill_log.jsonl, no [CANARY-DRILL] PR/issue, first drill scheduled Monday 2026-10-12 — test material, not lived behavior", "hollow_example": "SN-0340 -> tools/auto_merge_gate.py exists (371 lines) but 0 workflow invocations (see SN-0435); merge messages carry scorecards by ritual only", "pins": "82c4a7da (audit pin) and 613133b6 (re-pin; delta = 1 docs-only commit); all findings hold at both"}, "doctrine": {"three_class_verdict": "COMPOUNDING = behavior changed mechanically (fails closed without the lesson); APPLIED-AND-CITED = recorded + referenced, behavior unproven; HOLLOW = claimed enforcement absent", "capture_is_first_link": "capture is the first link of learning, not the last — VERIFY must reach later behavior, not just later bytes", "hollow_heartbeat": "a scheduled verification that has never run is a hollow heartbeat — the schedule is not the run; claim only what the last actual run proved", "audit_method": "reuse this taxonomy on every learning-event batch; claim without a citation is not a finding"}}
