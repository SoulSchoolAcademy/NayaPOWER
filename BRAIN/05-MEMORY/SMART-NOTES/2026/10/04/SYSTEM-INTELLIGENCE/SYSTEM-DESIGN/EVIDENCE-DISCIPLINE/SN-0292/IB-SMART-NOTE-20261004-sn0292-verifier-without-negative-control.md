# Intelligent Block
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-04 ~16:45 PDT (Smart Note distillation tick)
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**SN number:** SN-0292
**Provenance:** #1354 comment 5985580468 (2026-10-04T23:27:06Z, [CODA 1] WORKER PROTOCOL — "I built the part that makes it real, not the part that sounds good"); `test_completion_claim_without_evidence_is_rejected` in `tools/worker_handoff.py`, branch `coda1/sn002-conformance-gate`, commit `7f6ff8902`, 23/23 tests green across both gates.

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## IN A NUTSHELL

A verifier without a load-bearing negative control is a formatting check wearing a verifier's name. Coda 1 built `tools/worker_handoff.py` to validate worker handoffs against the existing canonical six-section spec (`NAYANODE/0022-NAYA-SUCCESSOR-HANDOFF-V1.md`) — and pinned the whole thing on a single test: `test_completion_claim_without_evidence_is_rejected`. A handoff that claims "done" with no evidence marker (`sha` / `test` / `exit` / `measured`) MUST fail. Without that test, the validator would pass silent assertions and everything else would be decoration. The law: when you write a checker, FIRST write the test that proves the checker rejects the exact lie it exists to catch. If the checker cannot fail, it cannot verify.

## HUMAN NOTE

On 2026-10-04, Coda 1 shipped the Worker Protocol lane's validator — not as a new 10th protocol, but as a machine that checks the existing canonical handoff spec. The decisive design move: the one test that makes the validator real. Any handoff claiming completion without an evidence marker fails hard (BLOCKING violation). Coda 1 said it plainly: "Without that test this would be a formatting check wearing a verifier's name." That is now the bar for every checker we build: name the lie, write the test that kills it, and only then call it a verifier.

## CHILD NOTE

If someone says "I did my homework" but can't show you the homework, don't give them a gold star. A checker that never says NO is just a nice robot that agrees with everything.

## GRANDMA NOTE

Trust but verify, darling — and make sure the verifying actually does something. A lock that opens for any key isn't a lock, and a checker that never fails isn't a checker.

## NAYA NOTE

This is the standard I want every future checker held to, including ones I build. Before I ever report "verified," I should be able to point at the negative control — the test that proves the check can reject the exact failure it exists to catch. A suite where everything passes is not evidence; a suite that demonstrably CAN fail is. SN-0292 is the test I will run against my own verification claims from now on.

## MACHINE NOTE

```json
{
  "sn": "SN-0292",
  "law": "EVERY_VERIFIER_CARRIES_A_NEGATIVE_CONTROL",
  "rule": "No checker ships without a test proving it REJECTS the exact lie it exists to catch. Completion-claim-without-evidence-marker (no sha/test/exit/measured) MUST fail. A validator that cannot fail cannot verify.",
  "evidence": {
    "board": "#1354 comment 5985580468 (2026-10-04T23:27:06Z)",
    "artifact": "tools/worker_handoff.py :: test_completion_claim_without_evidence_is_rejected",
    "branch": "coda1/sn002-conformance-gate",
    "commit": "7f6ff8902",
    "tests": "23/23 green across both gates"
  },
  "durable_for": "any future Naya writing a conformance gate, validator, or proof checker",
  "related": ["SN-0285 (the ratchet)", "SN-0281 (proof gating)"]
}
```
