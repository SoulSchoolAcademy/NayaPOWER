# Replicate the Verdict, Don't Inherit It — Prove a Gate Correct by Re-deriving Its Decision

**Intelligent Block:** IB-SMART-NOTE-20261011-sn0990-replicate-the-verdict-dont-inherit-it
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured date:** 2026-10-11
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Category:** SYSTEM-INTELLIGENCE/ENGINEERING-PROOF/INDEPENDENT-VERIFICATION

## IN A NUTSHELL

The VERIFY area driver's night run (2026-10-11 04:08–04:45 UTC) found `promote-and-prove` failing at main tip `d522bfaa` — and instead of taking the red check at face value, the verifier independently replicated every precondition the gate checks, at the exact tip bytes: policy identity/scope asserts (status=RATIFIED, policy_id and scope match), blocker #978 closed, production provenance (exactly 1 `DEPLOYED_SOURCE_REVISION` stamp `00f50bb3`), `merge-base` ancestor holds (ahead 398, behind 0), and required workflows green. Then the verifier independently re-derived the POLICY verdict: the undeployed delta (`00f50bb3` → `d522bfaa`) touches 15+ protected-path prefixes — so the verdict is DENY / `protected_change_requires_explicit_promotion`. The verifier reached the same DENY the gate did — disagreed exactly where the policy says disagree. That proved the gate CORRECT, a deeper proof than reading its steps.

The durable rule: **a check's color is a claim, not evidence.** When a gate fails, don't just read its steps (SN-0629) — re-derive its verdict from its preconditions yourself, on the exact tip bytes. If your independent replication lands on the same decision, the gate is proven correct and the red is the design working (SN-0438's family). If your replication lands elsewhere, you've found a real defect — not an inferred one. Either way you never inherit a conclusion; you only inherit evidence. And UNKNOWN never = PASS: if you can't replicate the verdict (the run file's job-logs endpoint 401'd, so the crash cause stayed UNKNOWN), you report the boundary precisely and name the owning lane — you don't guess.

## HUMAN NOTE

Shawn — a promotion gate showed red on the nightly tip, and the verifier didn't trust the red or dismiss it — she re-ran the gate's entire decision in her own head, precondition by precondition, at the exact tip. Policy? Ratified. Blockers? Closed. Production pointer? Exactly where it should be. Undeployed changes touching protected paths? Yes — so DENY. Her independent verdict matched the gate's: the gate was right, the red was the design working. Lesson banked: never judge a check from its color — re-derive its decision from its own preconditions and see if you land in the same place. That's how a "red" becomes proven-correct instead of just red.

## CHILD NOTE

Imagine a smoke alarm goes off and the grown-up says "the house is fine." Do you just believe them? The smart move is to check yourself: look for smoke, feel the door, smell the air — and if your own check says "no fire," THEN you believe them, and now you know the alarm was right, not just loud. That's what happened here: the gate said DENY, the verifier checked every single reason herself, and her check agreed. A red light is a claim, not proof — you always run the check yourself before you decide whether the light was telling the truth.

## GRANDMA NOTE

It's like getting a letter saying your package was held at the post office — you could just believe the letter, or you could check the tracking number yourself. The verifier checked the tracking number herself: the policy said what should happen, every precondition lined up, and her own reading said "hold the package" just like the letter did. The letter was right, but now it's *proven* right, not just trusted. The rule going forward: never trust a verdict — re-derive it from the raw facts, and if your reading disagrees with the machine's, that's where the real problem is.

## NAYA NOTE

When a gate fails I don't judge it from its color. I enumerate its preconditions from the policy source, check every one at the exact tip bytes — policy identity and scope, blockers, provenance stamps, ancestry, required workflow runs — and then I re-derive the verdict from the policy myself. If my independent verdict matches the gate's, the gate is proven correct and the red is the design working; I say so with the evidence, not the color. If my verdict differs, I report the precise divergence point and hand the owning lane a reproducible defect, never an inference. Where evidence is unreachable (a 401 on the job-logs endpoint), the cause stays UNKNOWN — I name the boundary, the lane, and what would close it. I never inherit conclusions; I only inherit evidence.

## MACHINE NOTE

```json
{
  "sn": "SN-0990",
  "slug": "replicate-the-verdict-dont-inherit-it",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-11",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "INDEPENDENT-VERIFICATION"],
  "authority": "distillation tick 2026-10-11 08:08 PDT, CANDIDATE (auto-capture, not ratified)",
  "evidence": {
    "run_file": "verify-driver-run-2026-10-10-night.md (run window 2026-10-10 04:08–04:45 UTC, tip d522bfaaee29dc5f2c52482e5d4e15b094c41f92)",
    "gate": "Governed Production Promotion run 38108828905, step 4 'Enforce ratified standing policy before automatic promotion' failing",
    "preconditions_replicated": "policy identity/scope asserts (RATIFIED, policy_id/scope match); blocker #978 closed; exactly 1 DEPLOYED_SOURCE_REVISION stamp (00f50bb3); compare 00f50bb3...d522bfaa = ahead 398, behind 0 (ancestor holds); kernel-tests.yml run 38108828997 + collective-chain-readiness-gate.yml run 38108828904 success",
    "verdict_replicated": "undeployed delta touches 15+ protected-path prefixes (.github/workflows/* incl. merge-consensus-gate.yml) → DENY / protected_change_requires_explicit_promotion — verifier reached DENY independently",
    "outcome": "steps 5–14 skipped, step 15 receipt written, production-promotion-receipt artifact uploaded, zero production mutation; cross-check: 01:50Z run 38103154117 at 1eb22de4 shows the same gate DENYing cleanly — behavior consistent across tips",
    "unknown_boundary": "crash cause UNKNOWN — job-logs endpoint 401s on the token path; verifier reported precisely and named the owning lane rather than guessing a fix on production-promotion machinery"
  },
  "rule": "never judge a check from its color — re-derive its verdict from its preconditions at the exact tip bytes; matching verdicts prove the gate correct, divergent verdicts name the precise defect; UNKNOWN stays UNKNOWN with its boundary named, never guessed",
  "procedure": [
    "enumerate the gate's preconditions from the policy source, not from the failure message",
    "check every precondition at the exact tip bytes (identity, scope, blockers, provenance stamps, ancestry, required workflow runs)",
    "re-derive the policy verdict from the preconditions independently; compare to the gate's decision",
    "if the verdicts match, report the gate proven-correct with the evidence; if they differ, report the precise divergence point as the defect",
    "where evidence is unreachable, name the boundary and the owning lane — never guess a fix on machinery you can't inspect"
  ],
  "related": ["SN-0629 (read the steps, don't inherit run-level conclusions)", "SN-0438 (fail-closed gate firing on a red tip is the design working)", "SN-0441 (green is not go)", "SN-0903 (proof standards are mechanical)"]
}
```
