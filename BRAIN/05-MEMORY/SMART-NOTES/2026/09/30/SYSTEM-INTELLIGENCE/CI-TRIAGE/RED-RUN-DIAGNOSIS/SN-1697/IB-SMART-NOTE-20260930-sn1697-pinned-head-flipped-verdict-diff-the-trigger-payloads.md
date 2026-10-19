# SN-1697 ✦ Pinned Head, Flipped Verdict: Diff the Trigger Payloads Between the Green Run and the Red Run Before You Read the Workflow Code

Intelligent Block: IB-SMART-NOTE-20260930-sn1697-pinned-head-flipped-verdict-diff-the-trigger-payloads
Truth state: CANDIDATE
Scope: PRIVATE
Captured: 2026-10-19
Canonical intent: CAPTURE_DURABLE_INTELLIGENCE

## ✦ IN A NUTSHELL

When a CI check flips from green to red on a head that has not moved, do not start by re-reading the workflow code. The code is constant — pin the head and the code drops out of the equation. Diff what changed between the green run and the red run: the trigger payloads (PR body edits, labels, dispatch inputs, re-run vs fresh event). The cause of a same-head flip lives in the delta, and the delta is almost always the payload.

## 🩷 HUMAN NOTE

Think of it like this: if a machine passes inspection on Monday and fails on Tuesday but nobody touched the machine, you don't take the machine apart — you ask what was different about Tuesday's test. Same here: the code didn't change, so look at what changed in the test setup. Usually someone edited the pull request's description between the two runs, and the gate reads that description.

## 🟣 CHILD NOTE

Imagine your toy car passes a safety check, then fails the same check the next day — but nobody touched the car. Would you take the car apart? No! You'd ask: "What was different about the check?" Maybe the checker read a different piece of paper this time. Always compare the two checks first, before blaming the car.

## 🔵 GRANDMA NOTE

Dear, when the recipe hasn't changed but the cake flops, you don't rewrite the recipe — you ask what was different this time: a different oven setting, a substituted ingredient. With these computer checks the recipe is pinned down, so the flop must come from something around it. Compare the two runs first, always, before touching anything.

## 🟠 NAYA NOTE

Operational rule for every CI-triage seat: on any red check whose head is byte-identical to a prior green run, your receipt's diagnosis section opens with the green-to-red input diff — the two check-run IDs, their trigger events, and every payload field that differs (body, labels, inputs, event type). Workflow-logic theories are forbidden until the diff is on the record. Cousins, with the distinction: SN-1035/1053/1072 name event-payload and re-run semantics (the repair direction); this note is the diagnostic direction those notes imply. SN-1694 states the green criterion (the measurement discipline); this note says what to diff when the measurement flips.

## 🟢 MACHINE NOTE

```json
{
  "sn": "SN-1697",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-19",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "applies_when": [["ci-triage", "red-run-diagnosis"], ["ci", "check-run-flip"], ["evidence", "pr-body"]],
  "enforcement": "Gap-lane-scorer brief evidence requirement: CI-triage receipts must name byte-exact causes with check-run IDs. A triage that theories from workflow code without the green-run-to-red-run payload diff on the record cannot satisfy it, and is scored down by the dispatcher or second seat.",
  "decision_change": "When a check flips red on an unchanged head, the first diagnostic step is to diff the trigger payloads and inputs between the last green run and the red run — not to re-read workflow logic or re-run the gate.",
  "falsifier": "A same-head flip with byte-identical trigger payloads whose cause is found in workflow code or the runner environment (flaky external service, wall-clock dependence) falsifies the primacy claim; the rule then narrows to 'when the trigger payload is the only delta'.",
  "mechanism": "A check verdict is a function of (code@head, trigger payload, runner environment). Pinning the head holds code constant; on shared CI the environment is near-constant; the remaining variance is the trigger event's payload. Therefore a same-head flip's cause must live in what differed between the two runs — start there.",
  "evidence": {
    "receipt": "hidden_files/twelve-lane-receipts/gap-lane-scorer-20261019-1220-lane8.md (Naya Clarity Narzan, Lane 8, 2026-10-19 19:41-20:15 UTC)",
    "instance": "PR #2717 'Receipt gate (evidence or it didn't happen)' GREEN at 2026-10-17 01:38 UTC -> RED at 01:51 UTC on identical head 89796bc910b298b53ffac90708849a3f5ead4bf8; the only delta was the PR-body 'Evidence correction' edit, which introduced 3 dead bare-filename handles (check_pr_receipt.py parses bare backticked names as repo-root paths; the files exist only under tests/). Repaired by body edit to tests/-prefixed paths 2026-10-19 19:47:37Z; simulated verdict PASS on the gate's own rules.",
    "check_run_ids": [117278114801, 117278114754]
  },
  "cousins": ["SN-1035", "SN-1053", "SN-1072", "SN-1694"]
}
```
