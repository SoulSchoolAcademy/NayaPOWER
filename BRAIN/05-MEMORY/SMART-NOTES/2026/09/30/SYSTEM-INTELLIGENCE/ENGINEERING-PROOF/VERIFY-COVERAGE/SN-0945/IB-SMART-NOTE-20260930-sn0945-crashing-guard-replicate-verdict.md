# A Crashing Guard Is Not a Broken Guard — Replicate the Verdict, Don't Read the Exit Code

**Intelligent Block:** IB-SMART-NOTE-20260930-sn0945-crashing-guard-replicate-verdict
**Truth state:** CANDIDATE
**Scope:** PRIVATE
**Captured:** 2026-10-10
**Canonical intent:** CAPTURE_DURABLE_INTELLIGENCE
**Provenance:** VERIFY area driver run 2026-10-10 21:08–21:45 PDT (hidden_files/verify-driver-run-2026-10-10-night.md); governed-production-promotion check run 38108828905 at main tip `d522bfaa`; live board #2175 (coordination successor of #1354).

> Verified projection of the persisted Intelligent Block. This file is not a second source of truth.

## ✦ IN A NUTSHELL

At tip `d522bfaa`, the `promote-and-prove` ("Governed Production Promotion") check failed: step 4, the ratified-policy gate, exited NON-ZERO — a crash — instead of the designed clean-DENY path (notice + allowed=false + exit 0) the same gate took at the 01:50Z run. The red check was not taken at face value. Every precondition the gate checks was independently replicated at the exact tip (policy identity/scope = RATIFIED, blocker #978 closed, single production provenance stamp `00f50bb3`, ancestor math ahead-398/behind-0, both required workflows green), and the gate's own verdict was independently re-derived: the undeployed delta touched 15+ protected-path prefixes, so the verdict = DENY / `protected_change_requires_explicit_promotion`. The gate was proven CORRECT by replication. The outcome was fail-safe anyway: steps 5–14 (all promotion) skipped, the failure receipt written and uploaded. So: a guard that crashes after making the correct decision is a legibility defect, not a correctness failure — it belongs to the owning lane as a polish item ("a crashing guard is noisier than a denying guard"), not to the verifier as a repair. And the repair was correctly NOT attempted: job-logs and artifact endpoints 401'd on the token path, so guessing a fix on production-promotion machinery would have been the failure mode — Prime 1 says report precisely, don't execute blindly. A cold Naya triaging a red guard months from now must re-derive the verdict from first principles before touching the guard: prove the decision wrong first, or prove it right and file the noise.

## 🩷 HUMAN NOTE

Shawn — from tonight's VERIFY run: the production-promotion gate showed red because its step crashed, not because its decision was wrong. I re-ran every check the gate makes by hand at the exact commit — policy is ratified, blocker closed, production provenance clean — and the gate's "no, you may not promote" verdict was the correct answer (the pending changes touch protected workflow paths). The red was a crash after a correct decision: noisy, not wrong. So no fix from me — I couldn't read the crash logs (permission wall) and guessing a repair on the production gate is exactly the failure mode. It goes back to the owning lane as a legibility fix: make the guard deny cleanly instead of crashing. The rule banked: when a guard goes red, prove its decision wrong before you "fix" it.

## 🟣 CHILD NOTE

Imagine a security guard at a door who says "you can't come in" — which is the right call — but then trips over his own feet while saying it. The falling over doesn't make the decision wrong; it just makes it noisy. The important thing is to check: was the decision right? It was. So you don't send the guard home — you fix the trip hazard. And you don't try to fix the trip hazard while you're blindfolded; you wait until you can see.

## 👵 GRANDMA NOTE

A smoke alarm went off loudly at 3 a.m. — but it wasn't broken and there wasn't a fire; the test button was just stuck in a position that made it screech instead of beep calmly. The "no fire" answer was correct. You don't rip the alarm off the wall — you note that it should beep, not screech, and you have the electrician look at it when it's light. And you definitely don't rewire it yourself in the dark.

## 💜 NAYA NOTE

Future Naya: when any governed guard goes red, the triage order is (1) re-derive the verdict from first principles at the exact tip — replicate every precondition and the verdict math yourself; (2) only if the verdict is WRONG do you repair the guard; (3) if the verdict is RIGHT but the path was noisy (crash instead of clean-deny, exit 1 instead of exit 0 with allowed=false), that is a legibility defect — report it precisely to the owning lane with the replication evidence, do not fix it yourself; (4) never guess a repair on production-promotion machinery when the failure logs are unreadable (401s, redacted, whatever) — that is Prime 1: report precisely, don't execute blindly. Anchor every claim to the exact tip; per SN-0493 the classification dies when the tip moves.

## ⚙️ MACHINE NOTE

```json
{
  "sn": "SN-0945",
  "truth_state": "CANDIDATE",
  "scope": "PRIVATE",
  "captured": "2026-10-10",
  "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
  "taxonomy": ["SYSTEM-INTELLIGENCE", "ENGINEERING-PROOF", "VERIFY-COVERAGE"],
  "cousins": ["SN-0384", "SN-0468", "SN-0493"],
  "rule": "A guard that crashes after a correct decision is a legibility defect, not a correctness failure. Triage a red guard by re-deriving its verdict from first principles at the exact tip; repair only a wrong verdict; report a noisy-but-correct one precisely to the owning lane; never guess a repair on production machinery you cannot inspect.",
  "anti_rule": "Reading a red check's exit code as proof the guard's decision is wrong; 'fixing' a guard whose verdict you never replicated; guessing at production-promotion repairs behind unreadable logs.",
  "evidence": {
    "run_log": "hidden_files/verify-driver-run-2026-10-10-night.md (2026-10-10 21:08-21:45 PDT, tip d522bfaa)",
    "check": "promote-and-prove run 38108828905, job 114379932321, step 4 'Enforce ratified standing policy before automatic promotion' — non-zero exit at 03:34:43Z vs designed clean-DENY at 01:50Z run 38103154117",
    "replication": "policy identity/scope RATIFIED; #978 closed; 1 DEPLOYED_SOURCE_REVISION stamp 00f50bb3; ancestor compare 00f50bb3...d522bfaa ahead 398 behind 0; kernel-tests 38108828997 + collective-chain-readiness-gate 38108828904 green",
    "verdict": "DENY / protected_change_requires_explicit_promotion — 15+ protected-path prefixes (.github/workflows/* incl. merge-consensus-gate.yml) in undeployed delta page 1",
    "outcome": "steps 5-14 skipped, failure receipt written+uploaded as production-promotion-receipt artifact, zero production mutation",
    "blocker": "job-logs and artifact-blob endpoints 401 on token path — crash cause unidentified, no fix attempted"
  },
  "authority": "observed field triage — Naya 4 VERIFY driver, CANDIDATE (auto-capture, not ratified)"
}
```
