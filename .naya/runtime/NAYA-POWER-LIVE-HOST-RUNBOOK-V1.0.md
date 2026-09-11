# Naya Power Live ChatGPT Host Runbook V1.0

## Purpose

Use ChatGPT as the live reasoning host while Naya Power governs the candidate-action boundary.

`USER TASK → SOURCE OF TRUTH → CHATGPT REASONING → CANDIDATES → HOST ADAPTER → CONSTITUTIONAL KERNEL → SELECT / REFUSE / ESCALATE → CONTINUE → EXTERNAL ACTION → INDEPENDENT VERIFICATION → RECEIPT → LEARN`

## What is executable today

- `naya_power_kernel.py` — deterministic constitutional decision gate.
- `naya_power_orchestrator.py` — no-dead-end continuation for every decision.
- `chatgpt_host_adapter.py` — normalizes ChatGPT-produced candidates and prevents model claims from becoming evidence.
- `naya_power_live.py` — one-command live-host bridge for structured candidate payloads.
- `runtime_activation_check.py` — activation gate proving the complete runtime slice is present and self-tested.

## Live-host rule

ChatGPT is the reasoning engine. Naya Power is the governing operating layer. The runtime does not claim magical interception of hidden model inference and does not claim external execution merely because a candidate was selected.

Only `SELECT` is eligible for execution. `REFUSE` and `ESCALATE` always produce a concrete continuation. External outcomes must be independently observed and verified before being called verified.

## Local invocation

From the repository root:

```bash
printf '%s\n' '<JSON request>' | python .naya/runtime/naya_power_live.py
```

The payload must contain the normal runtime request fields plus a non-empty `candidates` array using the model-adapter candidate contract.

## CI gate

The continuous runtime workflow proves:

1. sparse checkout isolates the runtime from the repository's unrelated legacy long filename;
2. Python 3.12 is available;
3. all runtime Python sources compile;
4. the runtime contract is valid JSON;
5. kernel self-test passes;
6. orchestrator self-test passes;
7. ChatGPT host adapter self-test passes;
8. live host bridge self-test passes;
9. activation gate passes.

## Verified current state

The live bridge was runner-tested on GitHub Actions after an actual failure was observed and repaired. The final runner-backed result was:

- Kernel: PASS 5/5
- Orchestrator: PASS 3/3
- ChatGPT host adapter: PASS 4/4
- Live host bridge: PASS 3/3
- Activation gate: ACTIVATED_AND_SELF_TESTED
- Execution state: READY_FOR_LIVE_CHATGPT_GOVERNED_WORK

## First real acceptance workload

Use the NayaNET Intelligent Hub as the first real task. Measure whether the governed loop improves source inspection, requirement preservation, implementation quality, verification discipline, usefulness, and reduction in corrective intervention.
