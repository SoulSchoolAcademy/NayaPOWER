# NEXT EXECUTION — TORCH 4: CONNECT TORCH TO EXECUTION

schema_version: 1
status: READY

## Project
Naya Power Superbrain (`PRJ-NAYAPOWER-SUPERBRAIN`)

## North Star
Every Naya should restore context, identify the highest-value executable action, execute it with authority, verify the result, extract durable value, and leave the next Naya stronger.

## Current state
Torch 3 Executable Torch has been implemented and its seven-case deterministic adversarial suite has been executed successfully in an isolated Python harness. The repository also contains the authoritative `project_execution_contract.py`, which validates and consumes canonical NEXT-EXECUTION successors. Torch 4 now connects the validated Torch representation to that existing canonical execution authority without creating a second execution engine.

## Completed work
- Verified the current collective running feed and execution/continuity law.
- Executed the deterministic Torch 3 adversarial suite: 7/7 tests passed.
- Added `torch_execution_adapter.py` as a thin binding layer.
- Added adversarial coverage for canonical successor invalidity and Torch/canonical divergence.
- Preserved the existing project execution contract as the authority for canonical successor validation.

## Verified evidence
- `executable_torch.py` defines the validated ExecutableTorch boundary.
- `executable_torch_test.py` contains seven adversarial cases and the isolated execution harness returned `Ran 7 tests ... OK`.
- `project_execution_contract.py` exposes `validate_next_execution()` and canonical successor semantics.
- `torch_execution_adapter.py` imports and delegates successor validation to `project_execution_contract.validate_next_execution`.

## Unresolved issues
- Torch 4 adapter execution must be verified against the actual repository runtime and authoritative CI.
- The adapter must not drift from the canonical NEXT-EXECUTION contract.
- GitHub Actions remains the authoritative final verification layer.

## Constraints
- Do not create a second execution authority.
- Do not execute work inside the adapter; it only validates and binds representations.
- Do not weaken Priority, Claim, Execution, Verification, or Learning contracts.
- Do not claim GitHub Actions PASS without workflow evidence on the exact commit.
- Preserve the existing canonical NEXT-EXECUTION artifact contract and 12 required semantic fields.

## Current objective
Prove that an ExecutableTorch can be safely bound to the existing canonical NEXT-EXECUTION execution authority, with divergence rejected fail-closed.

## Next action
Run `.naya/runtime/torch_execution_adapter_test.py` against the repository runtime. Capture exact output. If a real contract failure appears, repair the smallest true boundary and rerun the complete Torch 4 suite. If PASS, run the existing canonical project/continuity successor-consumption tests, record evidence, and advance to Torch 5: Execution → Evidence.

## Execution instructions
- Import `ExecutableTorch` from `executable_torch.py`.
- Import the existing `validate_next_execution` authority from `project_execution_contract.py` through `torch_execution_adapter.py`.
- Execute `python .naya/runtime/torch_execution_adapter_test.py` from the repository runtime.
- Confirm valid binding succeeds.
- Confirm missing canonical fields fail.
- Confirm next-action, evidence, constraints, and acceptance-criteria divergence fail.
- Confirm the adapter does not execute work or add execution state.
- Record exact test count and result.
- If the deterministic adapter suite passes, run the canonical successor behavioral tests required by the existing execution gate before advancing.

## Success criteria
- Valid Torch + valid canonical successor binds successfully.
- Invalid canonical successor is rejected by the existing canonical validator.
- Divergent next action is rejected.
- Divergent evidence requirement is rejected.
- Divergent constraints are rejected.
- Divergent acceptance criteria are rejected.
- Adapter remains non-executing and non-authoritative.
- Exact repository execution evidence is captured.
- No existing authority is duplicated or weakened.

## Verification requirements
- Exact repository: `SoulSchoolAcademy/NayaPOWER`.
- Exact branch: `main`.
- Tested commit SHA must be recorded.
- Execute the adapter suite against the actual repository files, not a reconstructed copy.
- Execute canonical NEXT-EXECUTION validation/consumption tests after adapter PASS.
- Preserve exact stdout, test count, and exit status as evidence.
- GitHub Actions must ultimately verify the accumulated stack before any verified release claim.

## Architectural boundary
**Priority selects → Torch packages → Claim authorizes → Execution executes → Verification proves → Smart Notes extract value → CSI compounds.**

The adapter only binds Torch to the already-authoritative canonical successor contract. It does not select priority, grant authorization, execute work, verify results, or persist learning.

## Finalization contract
When Torch 4 is complete, update the collective running feed with DONE / WHY / EVIDENCE / REVELATION / PROBLEM / RECOVERY / NEXT PRIORITY / NEXT ACTION / SUCCESS CRITERIA / DO NOT, then issue the next executable torch.
