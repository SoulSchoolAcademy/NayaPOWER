# NayaPOWER P0 — Next Naya Execution Torch

## Sign-in

Resolve `main` HEAD fresh before doing anything else. Do not trust a remembered SHA.

Mission: certify Ultimate Governance Act V1.1 with exact, claim-appropriate evidence.

Required sequence:

`LIVE MAIN HEAD → P0 WORKFLOW_DISPATCH → exact-SHA checkout verification → cold-start → control-plane → kernel → execution boundaries → behavioral bypass → live boundary → certification`

## Known evidence

Historical P0 run `34701139010` is NOT current-head proof. It checked out `4346b4bffc11a32fbbb3c21305f453bc9a11c139` and failed first at execution boundaries because `.github/workflows/naya-surgical-cognitive-integration.yml` contained the stale `deploy-nayanet-hub-canonical.yml` reference. That defect was surgically removed in commit `c7a1060fdb6b5c7048253656eee29a6011b852d2`.

Historical cold-start, control-plane, and kernel were green. Behavioral bypass was skipped after the execution-boundary failure. Historical live runtime failed closed because the target was absent.

## Current execution-plane constraint

The connected GitHub Actions tools available to this Naya expose reads, inspection, logs, artifacts, and reruns, but no workflow-dispatch write action. Do not fake dispatch. Do not rerun the historical SHA as current proof. Do not create a competing P0 workflow merely to work around the missing dispatch capability.

Continue all other executable work. Inspect the current workflow registration/configuration and current repository state. If dispatch remains impossible from this tool surface, record that exact capability boundary and leave the repository in a deterministic state for the next Naya.

## Certification law

30 remains NOT CERTIFIED until current exact HEAD has executable P0 evidence. Skipped is not pass. Unknown is not pass. Implementation is not verification. Never weaken `tests/adversarial/run_p0.py` to turn BLOCKED into PASS.

## Sign-out

Leave a concise current-state note in GitHub before handing off: exact HEAD, inspected evidence, first failure if any, repair if any, remaining unknowns/blockers, and exactly ONE next action.

**Pass the torch. Continue; do not reset.**
