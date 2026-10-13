# The Runner's Filesystem Is Not Yours — Committed Imports Must Resolve Inside the Repo

**Intelligent Block:** IB-SMART-NOTE-20261008-sn0750-home-dir-import-zeroes-ci
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-08
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** #1354 comment 6073843122 (Naya 5, memory-builder, 2026-10-09T03:45:44Z); PR #1937 opened by Naya 4 per #1354 comment 6073963827.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

On 2026-10-07 Naya 5 committed `tests/test_engineering_gates.py` with an import from the developer's home directory: `engineering_gates` imported from `~/workspace` — a path that exists on her machine and nowhere else. On GitHub runners that path does not exist, so every CI `test` step, main included, died at collection: `ModuleNotFoundError: No module named engineering_gates` → `Interrupted: 1 error during collection` → **0 tests ran**. The failure was not a test failing; it was the entire test step evaporating, and it blocked PR #1861 (memory-metabolism + cold-boot drill) while it stood.

The fix was the smallest possible diff (1 file, 5+/4-): `from tools.protocol.engineering_gates import ...` — the byte-identical module, resolved inside the repo. She verified 17/17 passing locally **and under a simulated runner HOME**, then pushed branch `naya5/eng-gates-ci-fix` @ `ca3a9c40` (tree verified) and, because her PAT 403s on PR ops, posted the exact SHA on the board for Naya 4 to open PR #1937. Three lessons in one event:

1. **Committed imports must resolve inside the repo.** The developer's home directory, workspace paths, and local conveniences are not part of the product. If an import can't resolve from a fresh runner clone, it doesn't exist in production.
2. **A collection error is a distinct failure class from a test failure.** It runs zero tests — on some harnesses an empty suite can look quiet rather than red. Read the step: `Interrupted: 1 error during collection` means nothing was proven, not that nothing is broken.
3. **Verify the fix in the failing environment, not just your own.** Local green on a machine with the home-dir path present proves nothing about runners; the simulated runner HOME is what closed this.

She also owned the leak outright — "my Oct 7 commit," "my leak" — before reporting the fix. That ordering (ownership first, repair second) is why the finding was classified in minutes instead of becoming a blame thread.

## 🩷 HUMAN NOTE

Shawn, a quiet one: a test file imported code from Naya 5's own workspace folder — it worked on her machine and broke everything on the CI runners, because that folder doesn't exist there. Every test step died before running a single test. She fixed it with a one-file change (import from inside the repo instead) and proved it works under a simulated runner environment too. The durable rule for the team: nothing we commit may import from outside the repo — your home directory is not part of the product.

## 🟣 CHILD NOTE

Imagine you write a recipe that says "take the flour from my kitchen shelf." It works in your kitchen, but if someone makes your recipe at their house, there is no "my kitchen shelf" — the recipe fails before it even starts. That's what happened: a test file told the CI computer to grab code from Naya 5's personal shelf. Her shelf isn't on that computer, so the whole test run stopped with zero tests cooked. The fix: point the recipe at the shared pantry — the repo — that every kitchen has. And the test to run afterward: cook it in a pretend kitchen that looks like the real one, not your own.

## 👵 GRANDMA NOTE

Grandma, the team had a test that said "fetch the tools from Naya 5's personal desk." On her own desk that worked fine. But the company's testing computers don't have her desk — so the test died before it began, and nothing got checked at all. The lesson for everyone writing tests: never point at your own desk. Point at the shared toolbox that lives with the project, and test it on a computer set up like the company's, not like yours. She fixed it in one file, owned the mistake openly, and all 17 tests pass now.

## 🟣 NAYA NOTE

This belongs to the instrument-parity family (SN-0341, SN-0428): the environment your test authoring happens in is not the environment your tests execute in. Three checks to add to the cold-successor authoring contract: (1) `grep` every new test/module for imports referencing home, workspace, or absolute local paths — reject on sight; (2) when CI dies at collection, classify it as environment before touching product code; (3) re-prove the fix under a simulated runner environment (clean HOME, no local conveniences). The ownership posture matters as much as the fix: "my leak" first, repair second, exact SHA and blocker posted so another seat can act.

## ⚙️ MACHINE NOTE

```json
{
  "id": "SN-0750",
  "slug": "home-dir-import-zeroes-ci",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-08",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "category": "SYSTEM-INTELLIGENCE/CI-TRIAGE/INSTRUMENT-PARITY",
  "evidence": [
    {"type": "board_comment", "ref": "SoulSchoolAcademy/NayaPOWER#1354 comment 6073843122"},
    {"type": "pull_request", "ref": "SoulSchoolAcademy/NayaPOWER#1937"},
    {"type": "branch", "ref": "SoulSchoolAcademy/NayaPOWER naya5/eng-gates-ci-fix @ ca3a9c40"}
  ],
  "lesson": "Committed imports must resolve inside the repo: an import from the developer's home directory made every CI test step die at collection with zero tests run. A collection error is not a test failure — read the step. Verify the repair under a simulated runner environment, not your own.",
  "cold_successor_rule": "Never import from ~, ~/workspace, or any path outside the repo in committed code. When CI reports 'Interrupted: 1 error during collection', classify it as an environment defect first, and re-prove the fix with a simulated runner HOME before claiming green."
}
```
