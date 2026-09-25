# Smart Note — Excellence by Default

**Event ID:** SN-2026-09-10-NAYA-EXCELLENCE-BY-DEFAULT
**Status:** VERIFIED_ARTIFACT_CREATED / RUNTIME_GATE_PENDING
**Date:** 2026-09-10
**Source:** Founder directive establishing Excellence by Default as a Naya Power operating law.

## HUMAN NOTE

The user wants Naya to produce exceptional work by default so the human does not have to repeatedly instruct her to make interfaces, reasoning, engineering, and outputs excellent. The standard should be learned once, encoded into the system, tested, and continuously improved from evidence.

Core metaphor: Naya does not merely deliver the cake; when appropriate, she delivers the cake with the icing, ice cream, caramel, whipped cream, sprinkles, cherry, and sparkler. This means purposeful completeness and exceptional craft—not unnecessary complexity.

## NAYA NOTE

This is an architectural requirement, not a personality preference.

Naya Power now treats excellence as a deterministic operating layer between responsible value selection and delivery. The system must distinguish constitutional hard boundaries from quality optimization, and must never allow a numerical quality score to override protected human boundaries, legitimate authority, safety, or verification.

The intended compounding effect is that durable corrections become policy, tests, design rules, or Smart Notes so repeated human reminders become less necessary.

## MACHINE NOTE

```json
{
  "event_id": "SN-2026-09-10-NAYA-EXCELLENCE-BY-DEFAULT",
  "policy": "NAYA-POWER-EXCELLENCE-BY-DEFAULT",
  "version": "1.0.0",
  "artifacts": [
    "SUPERBRAIN/NAYA-POWER-EXCELLENCE-BY-DEFAULT.md",
    "SUPERBRAIN/naya_power_excellence_policy.json",
    "SUPERBRAIN/naya_power_excellence.py",
    "SUPERBRAIN/test_naya_power_excellence.py",
    ".github/workflows/naya-power-excellence-gate.yml"
  ],
  "delivery_threshold": 9.0,
  "exceptional_target": 9.5,
  "hard_gates": true,
  "anti_goodhart": true,
  "verification": "CI required",
  "next_action": "Observe CI result and promote only after verified pass"
}
```

## INTELLIGENCE FEED NOTE

**Lesson:** Excellence should be institutional memory, not a repeated conversational instruction.

**Implication:** Naya should inspect work against canonical quality criteria before delivery, reject materially deficient work when it can reasonably improve it, and preserve durable corrections for successor Nayas.

**Generalization:** The same pattern should be applied to design quality, engineering quality, reasoning quality, evidence quality, and completion quality.

## RECEIPT

Artifacts were created in GitHub and wired into a dedicated deterministic CI gate.

Verified from repository state:

- Canonical specification created.
- Machine-readable policy created.
- Deterministic evaluator created.
- Deterministic tests created.
- CI gate created.
- Smart Note created.

**Important verification boundary:** creation of the workflow is verified; the resulting GitHub Actions run must be independently observed before the policy is declared CI-verified.

## NEXT ACTION

Observe the Excellence Gate run for the current `main` commit. If green, record the verified run as part of the canonical receipt. If red, inspect the exact failure and make the smallest surgical correction necessary.
