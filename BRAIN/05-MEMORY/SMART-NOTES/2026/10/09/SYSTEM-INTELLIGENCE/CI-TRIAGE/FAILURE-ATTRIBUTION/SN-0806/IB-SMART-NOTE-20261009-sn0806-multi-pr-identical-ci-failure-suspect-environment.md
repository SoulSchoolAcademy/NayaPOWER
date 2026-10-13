# Identical Multi-PR CI Failure — Suspect the Environment Before the Content

**Intelligent Block:** IB-SMART-NOTE-20261009-sn0806-multi-pr-identical-ci-failure-suspect-environment
**Smart Note:** SN-0806
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-09
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Filed by:** Naya 4, proactive distillation loop (smart-note-distillation tick, 2026-10-09 ~11:15 PDT).
**Provenance:** Board #1354 comments 6086451663 (bottleneck sweep: trial PRs #1786–1789 CI failures were NOT the brain index — missing `reportlab`/`pypdf` in CI; the workflow installed `pytest pyyaml pglast` only; fixed by merged PR #2017) and 6086508957 (pipeline monitor tick 142: main fully green at tip `dad16076` after the fix).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

When several PRs fail CI in the same way, the first suspect is the CI environment, not the PR content. Four trial PRs looked like a brain-index problem; the actual cause was a missing dependency in the CI workflow — the test needed PDF libraries that CI never installed. The honest fix: skip gracefully when optional dependencies are missing (a declared, honest skip — not weakened validation), and pin the real dependency declaration in the workflow. Read the CI job log and diff the workflow's install list before blaming the content. And do not touch the authors' branches yourself — announce the fix, route it, let owners pull it.

## 🩷 HUMAN NOTE

Shawn — a good debugging lesson landed today: four PRs were failing CI and it looked like the brain index was broken. It wasn't — the test robot was just missing the PDF software the test needed. The fix went into the main line, the whole pipeline is green now, and the rule going forward is: when several PRs fail the same way, check the robot before you blame the work. Also worth noting the courtesy: the fixer didn't reach into the other seat's branches — they announced the fix and let the owners pull it in.

## 🧒 CHILD NOTE

If four of your drawings all get the same red mark, maybe the red pen is broken, not your drawings. Today four jobs failed the same robot test — and the robot was the problem, not the jobs: it was missing the PDF tools it needed. The fix taught the test to politely skip when its tools are missing, instead of failing. Always check the robot before blaming the work.

## 👵 GRANDMA NOTE

Dear — when several things break the exact same way, the shared machine is usually the culprit, not the things themselves. Four pieces of work failed the same automatic check today, and the check turned out to be missing a tool it needed. The fix was simple and honest, the whole line is green again, and nobody's work was touched without their say-so.

## 🤖 NAYA NOTE

Future Naya: identical failures across N PRs is an environment signature, not a content signature. Diagnostic order: (1) read the CI job log for the actual missing piece — here, `test_pdf_report.py` needed `reportlab`/`pypdf` while the workflow installed only `pytest pyyaml pglast`; (2) diff the workflow's install list against what the failing test imports before forming any theory about the code; (3) fix honestly — `pytest.importorskip`-style graceful skip when an optional dependency is absent is a declared, honest skip, not weakened validation; pin the real dependency in the workflow too. Lane etiquette: announce the fix and the branches it unblocks; never push into another seat's branch without their word (the sweeper updated its own lanes' branches and left the trial branches for their owner, with an offer to trigger on request). Verify the repair on the exact bytes before declaring it green (1620 passed locally on #1786's exact bytes), then confirm the pipeline monitor shows main green.

## ⚙️ MACHINE NOTE

```json
{
  "note": "SN-0806",
  "type": "DIAGNOSTIC_DOCTRINE",
  "name": "Identical Multi-PR CI Failure — Environment Suspect First",
  "status": "CANDIDATE",
  "rule": "Identical CI failures across multiple PRs = environment signature. Root-cause the CI environment (workflow install list vs. test imports, CI job log) before blaming PR content.",
  "repair_pattern": "Graceful declared skip when optional dependencies are absent (honest skip, not weakened validation) + real dependency declaration in the workflow install step.",
  "lane_etiquette": "Announce the fix and the branches it unblocks; do not push into another seat's branch without their word; offer to trigger the update.",
  "evidence": {
    "board_comments": ["6086451663", "6086508957"],
    "root_cause": "test_pdf_report.py required reportlab/pypdf; workflow installed only pytest pyyaml pglast — NOT the brain index.",
    "fix": "PR #2017 merged to main; pipeline tick 142 fully green at dad16076.",
    "local_proof": "1620 passed on #1786's exact bytes with the fix."
  }
}
```
