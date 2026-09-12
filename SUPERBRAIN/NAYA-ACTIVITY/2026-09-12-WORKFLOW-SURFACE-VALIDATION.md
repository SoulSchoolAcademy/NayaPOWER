# NayaPOWER Workflow Surface Validation — 2026-09-12

STATUS: CANONICAL EXECUTION RECORD
MISSION: Validate and optimize the reduced NayaPOWER automation surface without weakening the current constitutional/governance architecture.

## CURRENT TRUTH

Exact current `main` HEAD at record time:
`c35e20a49f4b4264fcbe161b6a10202163b6d0b8`

The `.github/workflows` tree at that exact commit contains seven workflows:
1. `deploy-nayanet-hub-canonical-v2.yml`
2. `naya-control-plane.yml`
3. `naya-memory-runtime.yml`
4. `naya-power-adversarial-p0.yml`
5. `nayapower-activity-feed-integrity.yml`
6. `superbrain-current-main-behavioral-proof.yml`
7. `verify-primary-intelligence-system.yml`

## RESPONSIBILITY MATRIX

| Workflow | Authority | Trigger model | Unique responsibility | Main overlap risk | Decision |
|---|---|---|---|---|---|
| deploy-nayanet-hub-canonical-v2.yml | Production Hub deployment | workflow_dispatch only | Exact-SHA build, governed public deployment, runtime proof | None material | KEEP |
| naya-control-plane.yml | Governance + CCT | main push + scoped PR | Governance kernel, execution boundaries, cold-start acceptance, CCT regression | P0 historically duplicated some governance tests | KEEP; PR trigger narrowed |
| naya-memory-runtime.yml | Memory/restore | scoped push + PR + dispatch | Memory contracts, Smart Note validation, restore tests/execution | Formerly duplicated CCT suite | KEEP; already surgically reduced |
| naya-power-adversarial-p0.yml | P0 adversarial | scoped push + dispatch | Behavioral bypass adversarial tests; explicit live harness | Formerly ran general runtime/control-plane checks | KEEP; trigger and offline/live boundary corrected |
| nayapower-activity-feed-integrity.yml | Activity Feed integrity | Feed-only push + dispatch | Exact triggering commit and Feed protocol validation | Must not become communication relay | KEEP |
| superbrain-current-main-behavioral-proof.yml | Superbrain behavioral proof | scoped push + dispatch | Local Superbrain suite and A→B→C compounding proof | Could overlap broad control-plane if broadened | KEEP |
| verify-primary-intelligence-system.yml | PIS verification | scoped push + dispatch | PIS projection, persistent adapter source, Hub artifact parity | Hub build cost overlaps deployment build | KEEP |

## EXECUTED OPTIMIZATIONS

1. Narrowed `naya-control-plane.yml` pull-request triggering from every PR on main to the same governed source paths as its push trigger, excluding Activity Feed projection paths.
2. Narrowed `naya-power-adversarial-p0.yml` push paths so ordinary `.naya/runtime/**` changes do not automatically invoke the P0 suite.
3. Removed duplicated cold-start/control-plane/Feed/governance execution from the P0 offline job. The P0 workflow now owns behavioral-bypass testing on ordinary pushes; live P0 harness remains explicitly dispatch-only.
4. Discovered that the old execution-boundary test suite still referenced three deliberately deleted workflows. Instead of restoring dead workflows, updated the test suite to govern the canonical seven-workflow surface.

## RUNTIME RECEIPTS

### Old control-plane run exposed the real cleanup consequence
Run `34710710374` on commit `76fa724b1fac6710c67ffd5bc48c03bb63b4d237` failed in `test_naya_execution_boundaries.py` because the test still expected:
- `naya-claim-evidence-enforcement.yml`
- `naya-governance-gate.yml`
- `build-nayahub-intelligent.yml`

The CCT regression job in the same run passed all seven CCT/claim/Intelligent Block/Note Event tests. The failure was stale governance-test references, not a demonstrated loss of the tested capabilities.

### P0 boundary correction
Run `34710715554` on commit `5e540b0a7d4679fa30b905a9be8b6460d65add3f` initially failed because the offline job invoked `tests/adversarial/run_p0.py` without a live target. The harness correctly returned `BLOCKED=26` and exit code 3. This exposed a workflow design error: an offline job was invoking a live-required harness.

That was corrected in commit `c35e20a49f4b4264fcbe161b6a10202163b6d0b8` by moving the P0 harness out of the offline push job and leaving it in the explicit-dispatch live job.

### Current P0 result
Run `34710756022` is associated exactly with current HEAD `c35e20a49f4b4264fcbe161b6a10202163b6d0b8` and completed `success`.
Its offline job completed successfully; the live-runtime job was skipped because this was a push event. This is a PASS for offline behavioral-bypass validation, not a production/live-runtime proof.

## EXACT-HEAD OBSERVATION

The current P0 run proves:
- workflow head SHA = current commit
- checkout SHA matched workflow SHA
- behavioral bypass adversarial tests: PASS
- live runtime: NOT OBSERVED / skipped by design on push

## REMAINING UNKNOWN

The available GitHub connector can inspect and verify workflow runs but does not expose a workflow-dispatch write operation in the loaded action surface. Therefore live P0, behavioral proof, PIS verification, and canonical deployment were not artificially claimed as executed from this turn.

## SELF-CHALLENGE

The seven-workflow architecture is substantially cleaner, but completeness still requires exact-head execution evidence for the remaining authorities. In particular, the current control-plane workflow should be observed after the execution-boundary test repair, and the Activity Feed should be tested with a genuinely Feed-only commit to prove that unrelated canonical workflows remain silent.

## NEXT ACTION

Use the current exact HEAD `c35e20a49f4b4264fcbe161b6a10202163b6d0b8` as the baseline. Inspect the latest control-plane run generated by the test repair. If it fails, repair the first concrete failure surgically. If it passes, perform the next isolated-trigger proof: make one Feed-only change, verify that only `nayapower-activity-feed-integrity.yml` reacts, and confirm the other six workflows do not react.

## SUCCESS CRITERIA

- Seven-workflow surface remains intact unless evidence requires a change.
- No deleted legacy workflow is restored merely to satisfy stale tests.
- Offline P0 is independent of unavailable live runtime.
- Current governance tests describe current authorities.
- Exact-head workflow identity is proven.
- PASS, FAIL, and NOT OBSERVED remain distinct.
- Feed-only communication does not trigger unrelated infrastructure.
- Cold Naya can identify one authority per responsibility without guessing.
